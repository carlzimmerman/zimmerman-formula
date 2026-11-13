#!/usr/bin/env python3
"""
LMC1 -- the LMC's pull on the DESI DR1 BHB halo stars, in the framework's own Milky Way field.
Criteria: FROZEN_CRITERIA.md (sha256 in FREEZE_STAMP.txt), written before any LMC run and before any star was read; AMENDMENT_A1.md (bracket low end 1.6e10) after run 1 stopped at K6;
AMENDMENT_A2.md (K4 reference: Galactocentric 49.7, not the heliocentric 50.1) after run 2 stopped at K4;
AMENDMENT_A3.md (K7 q precision failed in run 3: recorded, not a stop; adverse 2 err_q robustness test).
Usage: python3 -I -B lmc1.py <path to MWS_BHB.fits>
Writes lmc1.out (main), lmc1_results.json, lmc1_mut.out (mutations, separate).
Known-answer checks run first; the script stops before any label if one fails.
Copied (not imported) from closure_2026_11_12/RAW1_halo_stars_direct/raw1.py: prof_interval, fit_disp,
sgr_matrix, sgr_lat_lon, frame_affine, load, build (S1-S6 cuts, proper-motion part dropped).
Reads RAW1's committed raw1_results.json for its ratios (read only).
Seeds: tracers 11, bootstrap 21.
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os
for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_k] = "1"
import sys, json, math
import numpy as np
from scipy.optimize import minimize_scalar, brentq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import lmc1_core as C
from astropy.io import fits
import astropy.units as u
from astropy.coordinates import SkyCoord, Galactocentric, CartesianRepresentation, CartesianDifferential
from astropy.coordinates.matrix_utilities import rotation_matrix

FITS = sys.argv[1]
OUT = open(os.path.join(HERE, "lmc1.out"), "w")
def say(s=""):
    print(s); OUT.write(str(s) + "\n"); OUT.flush()
def sec(t):
    say("\n" + "=" * 100); say(t); say("=" * 100)
FAIL = []
def check(name, ok, detail):
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    if not ok: FAIL.append(name)
def stop_if_failed():
    if FAIL:
        say("\nKNOWN-ANSWER CHECK FAILED: " + ", ".join(FAIL) + ". Stopping before any label."); OUT.close(); sys.exit(2)

BINS = C.BINS; NAMES = [f"{a:.0f}-{b:.0f}" for a, b in BINS]
R0, ZSUN, VSUN = 8.122, 20.8, (12.9, 245.6, 7.78)
N = 150000; DT = 2.0; AOUT = 5.5; BETA0 = 0.6
MASSES = {"low": 1.6e10, "central": 2.5e10, "high": 4.0e10}   # A1.1: low end 1.6e10 (was 1.7e10)
M_M1 = 1.5e11
FOOT_LAB = [("FW_census", "canonical"), ("FW_census", "alt")]
FOOT_REP = [("FW_rc", "canonical"), ("FW_rc", "alt")]
E0_REF, Z0_REF = 11.81, 2.25

# ------------------------------------------------------------------ copied from raw1.py
def prof_interval(nll, lo, hi):
    res = minimize_scalar(nll, bounds=(lo, hi), method="bounded", options=dict(xatol=1e-6))
    xb, nb = res.x, res.fun
    def side(direction):
        step = max(abs(xb) * 0.02, 1e-3); x = xb
        for _ in range(200):
            xn = x + direction * step
            if (direction < 0 and xn < lo) or (direction > 0 and xn > hi): return (lo if direction < 0 else hi)
            if nll(xn) - nb > 0.5:
                return brentq(lambda t: nll(t) - nb - 0.5, min(x, xn), max(x, xn), xtol=1e-6)
            x = xn; step *= 1.3
        return lo if direction < 0 else hi
    return xb, side(-1), side(+1), nb
def fit_disp(v, e):
    def nll_s(s):
        var = s * s + e * e
        mu = np.sum(v / var) / np.sum(1 / var)
        return 0.5 * np.sum((v - mu) ** 2 / var + np.log(var))
    sb, slo, shi, _ = prof_interval(nll_s, 1.0, 400.0)
    var = sb * sb + e * e; mu = np.sum(v / var) / np.sum(1 / var)
    return dict(sigma=float(sb), lo=float(slo), hi=float(shi), h=float(0.5 * (shi - slo)), mu=float(mu), n=int(len(v)))
def sgr_matrix():
    D = rotation_matrix((180 + 3.75) * u.deg, "z"); Cm = rotation_matrix((90 - 13.46) * u.deg, "x")
    B = rotation_matrix((180 + 14.111534) * u.deg, "z"); A = np.diag([1., 1., -1.])
    return A @ B @ Cm @ D
def sgr_lat_lon(l_deg, b_deg):
    l, b = np.radians(l_deg), np.radians(b_deg)
    x = np.array([np.cos(b) * np.cos(l), np.cos(b) * np.sin(l), np.sin(b)])
    xs = sgr_matrix() @ x
    return np.degrees(np.arctan2(xs[1], xs[0])) % 360.0, np.degrees(np.arcsin(np.clip(xs[2], -1, 1)))
def frame_affine(R0, zsun):
    gc = Galactocentric(galcen_distance=R0 * u.kpc, z_sun=zsun * u.pc, galcen_v_sun=CartesianDifferential([0, 0, 0] * u.km / u.s))
    def tr(xyz):
        c = SkyCoord(CartesianRepresentation(np.asarray(xyz, float).T * u.kpc), frame="icrs").transform_to(gc)
        return np.vstack([c.x.to_value(u.kpc), c.y.to_value(u.kpc), c.z.to_value(u.kpc)]).T
    p0 = tr(np.zeros((1, 3)))[0]
    Rm = (tr(np.eye(3)) - p0).T
    return p0, Rm
def load():
    h = fits.open(FITS, memmap=False)
    rv, fm = h["RVTAB"].data, h["FIBERMAP"].data
    return dict(tid=np.asarray(rv["TARGETID"]), tid_fm=np.asarray(fm["TARGETID"]), primary=np.asarray(rv["PRIMARY"]).astype(bool),
                vrad=np.asarray(rv["VRAD"], float), verr=np.asarray(rv["VRAD_ERR"], float),
                ra=np.asarray(rv["TARGET_RA"], float), dec=np.asarray(rv["TARGET_DEC"], float),
                dist=np.asarray(fm["DIST"], float), g=np.asarray(fm["MAG_DERED_G"], float), Mg=np.asarray(fm["ABS_MAG_G"], float))
def build(D):
    m = D["primary"] & np.isfinite(D["vrad"]) & (D["verr"] > 0) & (D["dist"] > 0) & np.isfinite(D["g"]) & np.isfinite(D["Mg"])
    idx = np.where(m)[0]
    ra, dec = np.radians(D["ra"][idx]), np.radians(D["dec"][idx]); d = D["dist"][idx]
    p0, Rm = frame_affine(R0, ZSUN)
    n = np.vstack([np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)]).T @ Rm.T
    pos = p0 + d[:, None] * n; r = np.linalg.norm(pos, axis=1)
    vgsr = D["vrad"][idx] + n @ np.array(VSUN)
    c = SkyCoord(ra=D["ra"][idx] * u.deg, dec=D["dec"][idx] * u.deg, frame="icrs").galactic
    lam, bet = sgr_lat_lon(c.l.deg, c.b.deg)
    keep = (np.abs(bet) >= 15.0) & (r >= 20.0) & (r < 80.0) & (np.abs(vgsr) <= 400.0)
    k = np.where(keep)[0]
    return dict(r=r[k], pos=pos[k], n=n[k], vgsr=vgsr[k], verr=D["verr"][idx][k], p0=p0)

# ------------------------------------------------------------------ helpers
def excess(sig, h):
    E = sig[1] - 0.5 * (sig[0] + sig[2]); z = E / math.sqrt(h[1] ** 2 + (h[0] ** 2 + h[2] ** 2) / 4)
    return E, z
def word(E1, z1, E0):
    if z1 < 1.0: return "LMC EXPLAINS THE BIN"
    if E1 <= 0.8 * E0: return "LMC PART OF IT"
    if E1 < 1.2 * E0: return "LMC NEGLIGIBLE"
    return "LMC MAKES IT WORSE"
def grade(fs, ss):
    cold = [nm for f, s, nm in zip(fs, ss, NAMES) if f < 1 - 2 * s]; hot = [nm for f, s, nm in zip(fs, ss, NAMES) if f > 1 + 2 * s]
    if not cold and not hot: return "PASSES", []
    if cold and hot: return "FAILS COLD AND HOT", cold + hot
    return ("FAILS COLD", cold) if cold else ("FAILS HOT", hot)
def wstd(v, w):
    sw = w.sum(); mu = np.sum(w * v) / sw; return math.sqrt(np.sum(w * (v - mu) ** 2) / sw)

# ================================================================== K6 bracket (no simulation, no data)
sec("K6 effective-mass bracket (before any simulation)")
LO, HI = 1.6e10 * 0.99, 4.0e10 * 1.01   # A1.2
D_LMC_GC = None
# LMC today (needed for r_LMC); astropy transform of published numbers
gc_frame = Galactocentric(galcen_distance=R0 * u.kpc, z_sun=ZSUN * u.pc, galcen_v_sun=CartesianDifferential(list(VSUN) * u.km / u.s))
lmc = SkyCoord(ra=78.76 * u.deg, dec=-69.19 * u.deg, distance=49.59 * u.kpc, pm_ra_cosdec=1.910 * u.mas / u.yr,
               pm_dec=0.229 * u.mas / u.yr, radial_velocity=262.2 * u.km / u.s, frame="icrs").transform_to(gc_frame)
XL0 = np.array([lmc.x.to_value(u.kpc), lmc.y.to_value(u.kpc), lmc.z.to_value(u.kpc)])
VL0 = np.array([lmc.v_x.to_value(u.km / u.s), lmc.v_y.to_value(u.km / u.s), lmc.v_z.to_value(u.km / u.s)])
rL = float(np.linalg.norm(XL0))
Gsi = C.G; Ms = C.MSUN; KPC = C.KPC
Mi = (91.7e3) ** 2 * 8.7 * KPC / Gsi / Ms
BR = dict(i_measured=Mi)
check("K6 (i) measured V^2 r / G at 8.7 kpc", LO <= Mi <= HI, f"{Mi:.4e} Msun")
Mb_tot = C.M_b(200.0)
for (mdl, ft) in FOOT_LAB:
    gMW = float(C.g_model(rL, mdl, ft)); VMW = math.sqrt(gMW * rL * KPC) / 1e3
    r_eq = rL * (91.7 / VMW) ** 2; M_up = (91.7e3) ** 2 * r_eq * KPC / Gsi / Ms
    r_J = rL * 91.7 / (math.sqrt(2) * VMW); M_J = (91.7e3) ** 2 * r_J * KPC / Gsi / Ms
    check(f"K6 (i) upper end {ft}: flat curve to the equal-field radius", LO <= M_up <= HI,
          f"V_MW({rL:.2f}) {VMW:.1f} km/s, r_eq {r_eq:.2f} kpc, M {M_up:.4e} Msun (Jacobi variant, reported: r_J {r_J:.2f} kpc, M {M_J:.4e})")
    gb = C.G * C.M_b(rL) * Ms / (rL * KPC) ** 2; nu = float(C.nu_fw(gb / C.A0[ft]))
    for mb in (3.2e9, 3.0e9):
        check(f"K6 (ii) kernel on LMC baryons {mb:.1e} {ft}", LO <= nu * mb <= HI,
              f"g_b,MW({rL:.2f}) = {gb:.4e} m/s^2 (M_b(<r) {C.M_b(rL):.4e}), nu {nu:.4f}, M_eff {nu * mb:.4e}")
    Miii = 3.2e9 / Mb_tot * gMW * (rL * KPC) ** 2 / Gsi / Ms
    check(f"K6 (iii) momentum, baryonic inertia {ft}", LO <= Miii <= HI,
          f"m_LMC / m_MW = 3.2e9 / {Mb_tot:.4e} = {3.2e9 / Mb_tot:.4f}; g_MW {gMW:.4e} m/s^2; equivalent M_eff {Miii:.4e}")
    BR[ft] = dict(VMW=VMW, r_eq=r_eq, M_up=M_up, r_J=r_J, M_J=M_J, nu=nu, M_ii=nu * 3.2e9, M_ii_30=nu * 3.0e9, M_iii=Miii)
stop_if_failed()

# ================================================================== K1, K4 (no data)
sec("K1 integrator checks (static census-canonical field) and K4 LMC today")
FC = C.Field("FW_census", "canonical")
def energy(F, x, v): r = np.sqrt(np.einsum("ij,ij->i", x, x)); return 0.5 * np.einsum("ij,ij->i", v, v) + F.phi_of_r(r)
vc30 = math.sqrt(float(FC.g_of_r(np.array([30.0]))[0]) * 30.0)
x0 = np.array([[30.0, 0, 0], [60.0, 0, 0]]); v0 = np.array([[0, vc30, 0], [0, 0.4 * math.sqrt(float(FC.g_of_r(np.array([60.0]))[0]) * 60.0), 0]])
E0a = energy(FC, x0, v0); dEmax = np.zeros(2); rdev = 0.0; xx, vv = x0, v0
for _ in range(50):
    xx, vv, _ = C.integrate(FC, xx, vv, DT, 50)
    dEmax = np.maximum(dEmax, np.abs(energy(FC, xx, vv) / E0a - 1)); rdev = max(rdev, abs(np.linalg.norm(xx[0]) / 30 - 1))
check("K1a circular 30 kpc energy", dEmax[0] < 1e-4, f"max |dE/E| {dEmax[0]:.2e}")
check("K1b circular stays circular", rdev < 1e-3, f"max |r/30 - 1| {rdev:.2e}")
check("K1c eccentric orbit energy", dEmax[1] < 1e-4, f"max |dE/E| {dEmax[1]:.2e}")
XT, VT = C.lmc_track(FC, XL0, VL0 * C.KMS, 0.0, 3000.0, DT)
ET = 0.5 * np.einsum("ij,ij->i", VT, VT) + FC.phi_of_r(np.linalg.norm(XT, axis=1))
check("K1d LMC-track integrator, M = 0, 3 Gyr", np.max(np.abs(ET / ET[-1] - 1)) < 1e-4, f"max |dE/E| {np.max(np.abs(ET / ET[-1] - 1)):.2e}")
vL = float(np.linalg.norm(VL0)); vrad = float(VL0 @ XL0 / rL); vtan = math.sqrt(vL ** 2 - vrad ** 2)
check("K4 r_GC (A2.1)", abs(rL - 49.7) <= 1.0, f"{rL:.3f} kpc vs 49.7 (K13 position at their distance 50.1); position {np.round(XL0, 3).tolist()} kpc")
K13 = np.array([-1.0, -41.0, -28.0]) * 49.59 / 50.1
check("K4 position components (A2.1)", bool(np.all(np.abs(XL0 - K13) <= 1.0)), f"scaled K13 {np.round(K13, 3).tolist()}; max |diff| {np.max(np.abs(XL0 - K13)):.3f} kpc")
check("K4 speed", abs(vL - 321) <= 24, f"{vL:.2f} vs 321 +/- 24 km/s")
check("K4 v_rad", abs(vrad - 64) <= 7, f"{vrad:.2f} vs 64 +/- 7")
check("K4 v_tan", abs(vtan - 314) <= 24, f"{vtan:.2f} vs 314 +/- 24")
stop_if_failed()

# ================================================================== K5 data
sec("K5 sample check (real stars)")
D = load()
check("K5a TARGETID RVTAB == FIBERMAP", bool(np.all(D["tid"] == D["tid_fm"])), f"{len(D['tid'])} rows")
S = build(D); P0 = S["p0"]
bsel = [(S["r"] >= a) & (S["r"] < b) for a, b in BINS]
counts = [int(m.sum()) for m in bsel]
check("K5b counts", counts == [865, 264, 241, 125], f"{counts}")
DISP = [fit_disp(S["vgsr"][m], S["verr"][m]) for m in bsel]
ref = [97.24, 106.74, 92.62, 95.30]
check("K5c dispersions", all(abs(d["sigma"] - x) <= 0.05 for d, x in zip(DISP, ref)), ", ".join(f"{d['sigma']:.3f}" for d in DISP))
SIG0 = [d["sigma"] for d in DISP]; H0 = [d["h"] for d in DISP]
E0, Z0 = excess(SIG0, H0)
check("K5d E0, z0", abs(E0 - E0_REF) <= 0.01 and abs(Z0 - Z0_REF) <= 0.01, f"E0 {E0:.3f} km/s, z0 {Z0:.3f}")
stop_if_failed()
PIX = [C.pix_of_dir(S["n"][m]) for m in bsel]
FOOT = [np.unique(p) for p in PIX]
say("  footprint pixels (nside 4, of 192) per bin: " + ", ".join(f"{nm}: {len(f)}" for nm, f in zip(NAMES, FOOT)))
RAW1 = json.load(open(os.path.join(HERE, "..", "RAW1_halo_stars_direct", "raw1_results.json")))["nominal"]["f"]

# ================================================================== relaxation per footing, K3
def relax(mdl, ft, beta0=BETA0, seed=11, label=True):
    F = C.Field(mdl, ft)
    x, v = C.sample_tracers(F, N, seed, a_out=AOUT, beta=beta0)
    x, v, _ = C.integrate(F, x, v, DT, 1000)            # -5 -> -3 Gyr
    s3 = (x.copy(), v.copy())
    x, v, _ = C.integrate(F, x, v, DT, 500)             # -3 -> -2
    s2 = (x.copy(), v.copy())
    snaps = set(range(0, 1001, 125))
    def fn(x, v):
        r, n, vl = C.observe(x, v, P0); rh = x / r[:, None]; vr = np.einsum("ij,ij->i", v, rh); vt2 = np.einsum("ij,ij->i", v, v) - vr ** 2
        out = []
        for a, b in BINS:
            m = (r >= a) & (r < b); out.append((float(np.std(vl[m])), float(1 - np.mean(vt2[m]) / (2 * np.mean(vr[m] ** 2)))))
        m = (r >= 20) & (r < 80); lr = np.log(r[m])
        def nll(al):
            k = 3 - al; Z = (80 ** k - 20 ** k) / k
            return -(np.sum((2 - al) * lr) - m.sum() * math.log(Z))
        return out, float(minimize_scalar(nll, bounds=(1.01, 9), method="bounded", options=dict(xatol=1e-6)).x)
    x, v, SN = C.integrate(F, x, v, DT, 1000, snaps=snaps, snap_fn=fn)   # -2 -> 0
    t = np.array(sorted(SN)) * DT
    say(f"{mdl}/{ft} (initial beta {beta0}): relaxed 5 Gyr; at t = 0 alpha(20-80) {SN[1000][1]:.3f}")
    ok = True
    for j, nm in enumerate(NAMES):
        sg = np.array([SN[s][0][j][0] for s in sorted(SN)]); bt = SN[1000][0][j][1]
        slope = np.polyfit(t, sg, 1)[0]; drift = slope * 2000.0 / sg.mean()
        brng = (0.5, 0.85) if j < 2 else (0.35, 0.85)
        say(f"   bin {nm}: sigma(t) " + " ".join(f"{s:.2f}" for s in sg) + f"; trend drift {drift:+.4f}; beta(0) {bt:.3f}")
        if label:
            check(f"K3 drift {mdl}/{ft} {nm}", abs(drift) < 0.02, f"{drift:+.4f}")
            check(f"K3 beta {mdl}/{ft} {nm}", brng[0] <= bt <= brng[1], f"{bt:.3f} in {brng}")
        else:
            ok &= abs(drift) < 0.02 and brng[0] <= bt <= brng[1]
    if label: check(f"K3 alpha {mdl}/{ft}", 4.5 <= SN[1000][1] <= 5.5, f"{SN[1000][1]:.3f}")
    else:
        ok &= 4.5 <= SN[1000][1] <= 5.5; say(f"   [INFO] reported footing, K3-style tests {'pass' if ok else 'DO NOT pass'} (not a gate)")
    return F, s3, s2, (x, v), SN

sec("K3 relaxation without the LMC (labelled footings)")
REL = {}
for mdl, ft in FOOT_LAB:
    REL[(mdl, ft)] = relax(mdl, ft)
stop_if_failed()

# ================================================================== twins
def run_twin(key, M, T=2000.0, mirror=False, beta_rel=None):
    F, s3, s2, fin, _ = (beta_rel if beta_rel is not None else REL[key])
    xl, vl = XL0.copy(), VL0.copy()
    if mirror: xl[2] = -xl[2]; vl[2] = -vl[2]
    track, _ = C.lmc_track(F, xl, vl * C.KMS, M, 3000.0, DT)
    if T == 2000.0: x, v, _ = C.integrate(F, s2[0], s2[1], DT, 1000, track=track, M=M, k0=500)
    else: x, v, _ = C.integrate(F, s3[0], s3[1], DT, 1500, track=track, M=M, k0=0)
    rr = np.linalg.norm(track, axis=1)
    return (x, v), dict(r_today=float(rr[-1]), r_peri=float(rr.min()), t_peri=float((np.argmin(rr) * DT) - 3000.0),
                        r_2gyr=float(rr[500]), r_3gyr=float(rr[0]), r_max=float(rr.max()))

def q_of(with_, without, nboot=300, seed=21):
    """q per bin in footprint and its bootstrap error (same Poisson weights for both twins)."""
    (xw, vw), (x0_, v0_) = with_, without
    rw, nw, vlw = C.observe(xw, vw, P0); r0, n0, vl0 = C.observe(x0_, v0_, P0)
    pw, p0_ = C.pix_of_dir(nw), C.pix_of_dir(n0)
    MW_ = [(rw >= a) & (rw < b) & np.isin(pw, FOOT[j]) & (np.abs(vlw) <= 400) for j, (a, b) in enumerate(BINS)]
    M0_ = [(r0 >= a) & (r0 < b) & np.isin(p0_, FOOT[j]) & (np.abs(vl0) <= 400) for j, (a, b) in enumerate(BINS)]
    rng = np.random.default_rng(seed); QS = [[] for _ in BINS]
    for _ in range(nboot):
        w = rng.poisson(1.0, N).astype(float)
        for j in range(len(BINS)): QS[j].append(wstd(vlw[MW_[j]], w[MW_[j]]) / wstd(vl0[M0_[j]], w[M0_[j]]))
    out = []
    for j, (a, b) in enumerate(BINS):
        mw, m0, qs = MW_[j], M0_[j], QS[j]
        q = float(np.std(vlw[mw]) / np.std(vl0[m0]))
        # full sky, reported
        mwf = (rw >= a) & (rw < b) & (np.abs(vlw) <= 400); m0f = (r0 >= a) & (r0 < b) & (np.abs(vl0) <= 400)
        out.append(dict(q=q, err=float(np.std(qs)), n_with=int(mw.sum()), n_without=int(m0.sum()),
                        sig_with=float(np.std(vlw[mw])), sig_without=float(np.std(vl0[m0])),
                        q_fullsky=float(np.std(vlw[mwf]) / np.std(vl0[m0f])),
                        dip_foot=C.dipole_fit(vlw[mw], nw[mw]), dip_full=C.dipole_fit(vlw[mwf], nw[mwf]),
                        dip_foot_without=C.dipole_fit(vl0[m0], n0[m0])))
    m50 = (rw >= 50) & (rw < 80)
    return out, C.dipole_fit(vlw[m50], nw[m50])

def corrected(Q):
    sig = [s / qq["q"] for s, qq in zip(SIG0, Q)]
    h = [math.hypot(hh / qq["q"], s * qq["err"] / qq["q"]) for hh, s, qq in zip(H0, sig, Q)]
    return sig, h

SHELLS = np.arange(18.75, 81.3, 2.5)
def vfield(x, v):
    r = np.sqrt(np.einsum("ij,ij->i", x, x)); rh = x / r[:, None]; out = []
    for c in SHELLS:
        m = (r >= c - 1.25) & (r < c + 1.25)
        A = np.hstack([np.ones((m.sum(), 1)), rh[m]]); co, *_ = np.linalg.lstsq(A, v[m] / C.KMS, rcond=None); out.append(co)
    return np.array(out)    # (nshell, 4, 3)
def template(with_, without):
    Dl = vfield(*with_) - vfield(*without)
    r = S["r"]; rh = S["pos"] / r[:, None]
    co = np.stack([np.stack([np.interp(r, SHELLS, Dl[:, i, k]) for k in range(3)], -1) for i in range(4)], 1)  # (Nstar, 4, 3)
    vel = co[:, 0, :] + np.einsum("ni,nik->nk", rh, co[:, 1:, :])
    return np.einsum("nk,nk->n", vel, S["n"])
def nll_scale(v, e, T, s):
    vv = v - s * T
    def nll_s(sg):
        var = sg * sg + e * e; mu = np.sum(vv / var) / np.sum(1 / var)
        return 0.5 * np.sum((vv - mu) ** 2 / var + np.log(var))
    return minimize_scalar(nll_s, bounds=(1.0, 400.0), method="bounded", options=dict(xatol=1e-6)).fun
def fit_scale(v, e, T):
    sb, lo, hi, nb = prof_interval(lambda s: nll_scale(v, e, T, s), -60.0, 60.0)
    return dict(s=float(sb), lo=float(lo), hi=float(hi), h=float(0.5 * (hi - lo)))

RES = dict(bracket=BR, lmc_today=dict(x=XL0.tolist(), v=VL0.tolist(), r=rL, speed=vL, vrad=vrad, vtan=vtan),
           sample=dict(counts=counts, disp=DISP, E0=E0, z0=Z0), footprint=[len(f) for f in FOOT], footings={})
sec("Twins: with and without the LMC (labelled footings)")
TWINS = {}
for key in FOOT_LAB:
    without = REL[key][3]
    for nm, M in MASSES.items():
        w, orb = run_twin(key, M); Q, d50 = q_of(w, without)
        TWINS[(key, nm)] = (w, Q, d50, orb)
        say(f"{key[0]}/{key[1]} M_eff {M:.2e} ({nm}): LMC orbit r today {orb['r_today']:.2f}, pericentre {orb['r_peri']:.2f} kpc at "
            f"{orb['t_peri']:+.0f} Myr, r(-2 Gyr) {orb['r_2gyr']:.1f}, r(-3 Gyr) {orb['r_3gyr']:.1f}, max {orb['r_max']:.1f}")
        for j, qq in enumerate(Q):
            say(f"   bin {NAMES[j]}: q {qq['q']:.5f} +/- {qq['err']:.5f} (n {qq['n_with']}/{qq['n_without']}; sigma {qq['sig_with']:.2f} / {qq['sig_without']:.2f}); "
                f"full-sky q {qq['q_fullsky']:.5f}")
        say(f"   full-sky 50-80 kpc dipole {d50['amp']:.2f} km/s toward l {d50['l']:.0f}, b {d50['b']:+.0f}")
# K2 zero mass
K7FAIL = []
key = FOOT_LAB[0]
F, s3, s2, fin, _ = REL[key]
track0, _ = C.lmc_track(F, XL0, VL0 * C.KMS, 2.5e10, 3000.0, DT)
xz, vz, _ = C.integrate(F, s2[0], s2[1], DT, 1000, track=track0, M=0.0, k0=500)
check("K2 zero-mass twin equals the no-LMC state bitwise", bool(np.array_equal(xz, fin[0]) and np.array_equal(vz, fin[1])),
      f"max |dx| {np.max(np.abs(xz - fin[0])):.1e} kpc, max |dv| {np.max(np.abs(vz - fin[1])):.1e} kpc/Myr")
for key in FOOT_LAB:
    Q = TWINS[(key, "central")][1]
    ok7 = all(qq["err"] < 0.005 for qq in Q)
    say(f"  [{'PASS' if ok7 else 'FAIL'}] K7 q error {key[1]} central (A3.1: recorded, not a stop): " + ", ".join(f"{qq['err']:.5f}" for qq in Q))
    if not ok7: K7FAIL.append(key[1])
stop_if_failed()

# ================================================================== labels
sec("LABELS (primary estimator, sigma_c = sigma_obs / q)")
say(f"Before: sigma_obs {', '.join(f'{s:.2f}' for s in SIG0)}; E0 {E0:.3f} km/s, z0 {Z0:.3f}")
LAB = {}; QN = {}
for key in FOOT_LAB:
    words = {}
    for nm in MASSES:
        Q = TWINS[(key, nm)][1]; sc, hc = corrected(Q); E1, z1 = excess(sc, hc); words[nm] = (word(E1, z1, E0), E1, z1, sc, hc)
        sh = []
        for sgn in (+1, -1):   # A3.2 adverse shifts: q2 - 2 e2, q1 + 2 e1, q3 + 2 e3 (and the opposite)
            Qs = [dict(qq) for qq in Q]
            for j, dirn in ((0, +1), (1, -1), (2, +1)): Qs[j]["q"] = Q[j]["q"] + sgn * dirn * 2 * Q[j]["err"]
            s_, h_ = corrected(Qs); Es, zs = excess(s_, h_); sh.append((word(Es, zs, E0), Es, zs))
        QN[(key, nm)] = sh
        say(f"{key[1]:9s} M {nm:7s}: sigma_c " + ", ".join(f"{s:.2f}+/-{h:.2f}" for s, h in zip(sc, hc)) + f"; E1 {E1:.3f} (E1/E0 {E1 / E0:.4f}), z1 {z1:.3f} -> {words[nm][0]}")
    for nm in MASSES:
        say(f"  {key[1]} {nm} A3.2 adverse q shifts: " + "; ".join(f"E1 {e:.3f} z1 {z:.3f} -> {w}" for w, e, z in QN[(key, nm)]))
    w0 = words["central"][0]; frag = any(words[k][0] != w0 for k in ("low", "high"))
    fragq = any(w != words[nm][0] for nm in MASSES for w, _, _ in QN[(key, nm)])
    LAB[key[1]] = dict(word=w0, fragile=frag, fragile_qnoise=fragq, qshift={nm: QN[(key, nm)] for nm in MASSES}, E1=words["central"][1], z1=words["central"][2], low=words["low"][:3], high=words["high"][:3])
    say(f"  ==> census {key[1]}: {w0}{', FRAGILE' if frag else ' (robust across the bracket)'}{', FRAGILE (q NOISE)' if fragq else ' (robust to 2 err_q)'}"
        + (" [graded with K7 FAILED, A3]" if K7FAIL else ""))

# ================================================================== reported: 3 Gyr, second estimator, ratios, dipoles, scale
sec("Reported: 3 Gyr orbit variant (census canonical, central)")
key = FOOT_LAB[0]
w3, orb3 = run_twin(key, 2.5e10, T=3000.0); Q3, d3 = q_of(w3, REL[key][3])
sc3, hc3 = corrected(Q3); E3, z3 = excess(sc3, hc3)
say("  q " + ", ".join(f"{qq['q']:.5f}+/-{qq['err']:.5f}" for qq in Q3) + f"; E1 {E3:.3f}, z1 {z3:.3f} -> {word(E3, z3, E0)}; 50-80 dipole {d3['amp']:.2f} (l {d3['l']:.0f}, b {d3['b']:+.0f})")
RES["variant_3gyr"] = dict(q=Q3, E1=E3, z1=z3, word=word(E3, z3, E0), orbit=orb3)

sec("Reported: second estimator (model's mean LMC-induced velocity subtracted star by star, RAW1's estimator refit)")
TEMPL = {}
for key in FOOT_LAB:
    T = template(TWINS[(key, "central")][0], REL[key][3]); TEMPL[key] = T
    d2 = [fit_disp(S["vgsr"][m] - T[m], S["verr"][m]) for m in bsel]
    E2, z2 = excess([d["sigma"] for d in d2], [d["h"] for d in d2])
    say(f"{key[1]}: template rms by bin " + ", ".join(f"{np.sqrt(np.mean(T[m] ** 2)):.2f}" for m in bsel) + " km/s; mean " + ", ".join(f"{np.mean(T[m]):+.2f}" for m in bsel))
    say(f"   sigma after subtraction " + ", ".join(f"{d['sigma']:.2f} [{d['lo']:.2f}, {d['hi']:.2f}]" for d in d2) + f"; E1' {E2:.3f}, z1' {z2:.3f} -> {word(E2, z2, E0)}")
    RES["footings"].setdefault(key[1], {})["second"] = dict(disp=d2, E1=E2, z1=z2, word=word(E2, z2, E0))

sec("Reported: RAW1 ratios divided by q (NOT A RE-GRADE; RAW1's predicted dispersion is not recomputed)")
RATIOS = {}
def ratios_for(case, Q):
    rows = RAW1[case]; fs = [r["f"] / qq["q"] for r, qq in zip(rows, Q)]; ss = [r["s"] / qq["q"] for r, qq in zip(rows, Q)]
    g = grade(fs, ss); g0 = grade([r["f"] for r in rows], [r["s"] for r in rows])
    say(f"{case:20s} before " + "  ".join(f"{r['f']:.3f}" for r in rows) + f" ({g0[0]} {g0[1]}); after " + "  ".join(f"{f:.3f}+/-{s:.3f}" for f, s in zip(fs, ss)) + f" -> RAW1's rule would say {g[0]} {g[1]}")
    RATIOS[case] = dict(f=fs, s=ss, rule=g[0], bins=g[1])
for key in FOOT_LAB: ratios_for(f"{key[0]}/{key[1]}", TWINS[(key, "central")][1])

sec("Reported: rotation-curve stellar mass footings (central M_eff), and the tracer variant (initial beta 0.45)")
REP = {}
for key in FOOT_REP:
    rel = relax(*key, label=False); w, orb = run_twin(key, 2.5e10, beta_rel=rel); Q, d50 = q_of(w, rel[3])
    sc, hc = corrected(Q); E1, z1 = excess(sc, hc)
    say(f"  {key[0]}/{key[1]}: q " + ", ".join(f"{qq['q']:.5f}+/-{qq['err']:.5f}" for qq in Q) + f"; E1 {E1:.3f}, z1 {z1:.3f} -> {word(E1, z1, E0)} (reported)")
    ratios_for(f"{key[0]}/{key[1]}", Q); REP[key[1]] = dict(q=Q, E1=E1, z1=z1, word=word(E1, z1, E0))
relb = relax("FW_census", "canonical", beta0=0.45, label=False); w, _ = run_twin(FOOT_LAB[0], 2.5e10, beta_rel=relb); Qb, _ = q_of(w, relb[3])
scb, hcb = corrected(Qb); Eb, zb = excess(scb, hcb)
say(f"  tracer variant beta0 0.45, census canonical: q " + ", ".join(f"{qq['q']:.5f}+/-{qq['err']:.5f}" for qq in Qb) + f"; E1 {Eb:.3f}, z1 {zb:.3f} -> {word(Eb, zb, E0)} (reported)")
RES["reported_rc"] = REP; RES["variant_beta045"] = dict(q=Qb, E1=Eb, z1=zb)

sec("Reported: dipoles (v_gsr = m + d . n_sun; direction in Galactocentric-axis l, b)")
DIPS = {}
for j, m in enumerate(bsel):
    dr = C.dipole_fit(S["vgsr"][m], S["n"][m]); DIPS[NAMES[j]] = dr
    say(f"bin {NAMES[j]}: real stars {dr['amp']:.1f} km/s (l {dr['l']:.0f}, b {dr['b']:+.0f}), monopole {dr['mono']:+.1f}")
    for key in FOOT_LAB:
        qq = TWINS[(key, "central")][1][j]
        say(f"   model {key[1]} central: footprint {qq['dip_foot']['amp']:.2f} (l {qq['dip_foot']['l']:.0f}, b {qq['dip_foot']['b']:+.0f}); "
            f"full sky {qq['dip_full']['amp']:.2f} (l {qq['dip_full']['l']:.0f}, b {qq['dip_full']['b']:+.0f}); without-LMC footprint {qq['dip_foot_without']['amp']:.2f}")

sec("Reported: template scale factor fitted to the real stars (v = mu + s T), and the power to tell 2.5e10 from 1.5e11")
SCALE = {}
for key in FOOT_LAB:
    T = TEMPL[key]; rows = []
    for j, m in enumerate(bsel):
        fs = fit_scale(S["vgsr"][m], S["verr"][m], T[m]); rows.append(fs)
        say(f"{key[1]} bin {NAMES[j]}: s = {fs['s']:+.2f} [{fs['lo']:+.2f}, {fs['hi']:+.2f}]")
    wts = np.array([1 / r["h"] ** 2 for r in rows]); sc_ = float(np.sum(wts * np.array([r["s"] for r in rows])) / wts.sum()); hs = float(1 / math.sqrt(wts.sum()))
    say(f"   combined s = {sc_:+.2f} +/- {hs:.2f}; |6 - 1| > 2 sigma_s: {5.0 > 2 * hs}")
    SCALE[key[1]] = dict(rows=rows, s=sc_, h=hs)

# ================================================================== mutations (separate file)
MUT = open(os.path.join(HERE, "lmc1_mut.out"), "w")
def msay(s): print("[MUT] " + s); MUT.write(s + "\n"); MUT.flush()
msay("LMC1 mutations (criteria FROZEN_CRITERIA.md section 8). M1 BORROWED mass 1.5e11: CONTEXT ONLY, no label.")
MUTRES = {}
for key in FOOT_LAB:
    w, orb = run_twin(key, M_M1); Q, d50 = q_of(w, REL[key][3]); dc = TWINS[(key, "central")][2]
    sc, hc = corrected(Q); E1, z1 = excess(sc, hc); bites = d50["amp"] >= 3 * dc["amp"]
    msay(f"M1 {key[1]}: LMC r today {orb['r_today']:.2f}, pericentre {orb['r_peri']:.2f} at {orb['t_peri']:+.0f} Myr, r(-2 Gyr) {orb['r_2gyr']:.1f}")
    msay(f"   q " + ", ".join(f"{qq['q']:.5f}+/-{qq['err']:.5f}" for qq in Q) + "; sigma_c " + ", ".join(f"{s:.2f}" for s in sc) + f"; E {E1:.3f}, z {z1:.3f} (context)")
    msay(f"   full-sky 50-80 dipole {d50['amp']:.2f} km/s (l {d50['l']:.0f}, b {d50['b']:+.0f}) vs central {dc['amp']:.2f}: ratio {d50['amp'] / dc['amp']:.2f}; bites (>= 3): {bites}")
    T1 = template(w, REL[key][3])
    case = f"{key[0]}/{key[1]}"; fs = [r["f"] / qq["q"] for r, qq in zip(RAW1[case], Q)]
    msay(f"   RAW1 ratios / q (context): " + ", ".join(f"{f:.3f}" for f in fs))
    # likelihood of the M1 template vs the central template (both at s = 1)
    Tc = TEMPL[key]; d2 = 0.0
    for m in bsel: d2 += 2 * (nll_scale(S["vgsr"][m], S["verr"][m], T1[m], 1.0) - nll_scale(S["vgsr"][m], S["verr"][m], Tc[m], 1.0))
    s1 = [fit_scale(S["vgsr"][m], S["verr"][m], T1[m]) for m in bsel]
    msay(f"   M1 template scale per bin " + ", ".join(f"{r['s']:+.2f}+/-{r['h']:.2f}" for r in s1) + f"; Delta(-2 lnL) M1 template minus central template {d2:+.3f}")
    MUTRES[f"M1/{key[1]}"] = dict(q=Q, E=E1, z=z1, dip50=d50, ratio=d50["amp"] / dc["amp"], bites=bool(bites), raw1_over_q=fs, dlnL2=d2, scale=s1)
msay("   published reflex (PROVISIONAL): 32 +/- 4 km/s toward (l, b) = (56 +/- 9, -34 +10/-9) deg, 40-120 kpc tracers (Petersen & Penarrubia 2021)")
key = FOOT_LAB[0]
w, orb = run_twin(key, 2.5e10, mirror=True); Q, d50 = q_of(w, REL[key][3]); dc = TWINS[(key, "central")][2]
bites = np.sign(d50["vec"][2]) != np.sign(dc["vec"][2]) and d50["vec"][2] != 0
msay(f"M2 mirrored LMC, canonical central: 50-80 dipole vector {np.round(d50['vec'], 3).tolist()} vs central {np.round(dc['vec'], 3).tolist()}; z sign flips: {bool(bites)}")
msay("   q " + ", ".join(f"{qq['q']:.5f}" for qq in Q))
MUTRES["M2"] = dict(dip50=d50, central=dc, bites=bool(bites), q=Q)
MUT.write("kappa = 1/2 FITTED; not theory closed. Adopts nothing.\n"); MUT.close()
say("\nMutations: " + "; ".join(f"{k} bites {v['bites']}" for k, v in MUTRES.items()) + " (lmc1_mut.out)")

def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.ndarray): return clean(o.tolist())
    return o
for key in FOOT_LAB:
    RES["footings"].setdefault(key[1], {}).update(label=LAB[key[1]], q={nm: TWINS[(key, nm)][1] for nm in MASSES},
                                                  dip50={nm: TWINS[(key, nm)][2] for nm in MASSES}, orbit={nm: TWINS[(key, nm)][3] for nm in MASSES},
                                                  scale=SCALE[key[1]])
RES.update(ratios=RATIOS, dipoles_real=DIPS, mutations=MUTRES, K7_failed=K7FAIL)
json.dump(clean(RES), open(os.path.join(HERE, "lmc1_results.json"), "w"), indent=1)
say("\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.")
OUT.close()

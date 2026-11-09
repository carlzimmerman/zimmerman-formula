#!/usr/bin/env python3
"""KO1 E8 (AMENDMENT_A3.md, d0424b7a57): the neighbours' term in the two-phase reading, for host-free lenses.  REPORTED ONLY.
Each pool neighbour inside the lens's measured range and within 230 Mpc is a point of (1 + X) M_b; exact annulus averages;
the same sum around shuffled sky positions is subtracted (chance projections, survey edges).
Run: python3 ko1_neighbours.py -> ko1_neighbours.json, ko1_neighbours.out  (reads ko1_shape.json for k and the inner amplitude).
kappa = 1/2 FITTED; not theory closed.  Adopts nothing.
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import json, math, time
import numpy as np
from scipy.spatial import cKDTree
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
T0 = time.time(); OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(s)
G = 6.674e-11; Msun = 1.989e30; Mpc = 3.0857e22; c_SI = 2.998e8; H0_SI = 70e3 / Mpc
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FOOT = ("canonical", "alt"); NPAT = 50
X_SHARE = 0.11958060485606123 / 0.0215; X_CAP = 53.64; W = 230.0
def nu(y): return 0.5 + np.sqrt(0.25 + 1.0 / y)
def glaw(g, a0): return nu(g / a0) * g
def DC(z, n=2048):
    zz = np.linspace(0, np.max(z), n); E = np.sqrt(0.3 * (1 + zz) ** 3 + 0.7)
    chi = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))]) * (c_SI / H0_SI) / Mpc
    return np.interp(z, zz, chi)
def unitvec(ra_deg, dec_deg):
    ra, dec = np.radians(ra_deg), np.radians(dec_deg)
    return np.c_[np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)]
def mgal_of(logMs): return 10 ** logMs * (1 + 10 ** (-0.69 * logMs + 6.63))

ln = np.load(os.path.join(DATA, "lr_lenses.npz")); PL = np.load(os.path.join(DATA, "cfg110_perlens.npz"))
WG, WW, EDGES = PL["WG"], PL["WW"], PL["gbar_edges"]
patch = np.load(os.path.join(DATA, "cfg96_stack.npz"))["patch"]
NL = len(ln["ra"]); zl = ln["z"]; logMs = ln["logM"]; Mg = ln["Mgal"] * Msun; chil = ln["chi"]
OUTER = [0, 1, 2, 3]; XG, WGL = np.polynomial.legendre.leggauss(24); R3 = (3.0 * Mpc) ** 2
T_LO = np.stack([G * Mg / EDGES[k + 1] for k in OUTER], axis=1)                 # R1^2 (m^2)
T_HI = np.stack([np.minimum(G * Mg / EDGES[k], R3) for k in OUTER], axis=1)     # R2^2 (m^2)
OKC = T_HI > T_LO
def law_cells(a0):
    m = np.zeros((NL, 4))
    for c in range(4):
        t = T_LO[:, c][:, None] + (T_HI[:, c] - T_LO[:, c])[:, None] * (XG[None, :] + 1) / 2
        with np.errstate(divide="ignore", invalid="ignore"):
            f = glaw(G * Mg[:, None] / t, a0)
        m[:, c] = np.where(OKC[:, c], (f * WGL[None, :]).sum(1) / 2, 0.0)
    return m
LAW = {f: law_cells(A0[f]) for f in FOOT}
WGo, WWo = WG[:, OUTER], WW[:, OUTER]
def psum(arr, mask):
    pm = patch[mask]; a = arr[mask]
    return np.stack([np.bincount(pm, weights=a[:, c], minlength=NPAT) for c in range(arr.shape[1])], axis=1)
def data_amp(mask, Mo):
    Sg = psum(WGo, mask); Sw = psum(WWo, mask); Sm = psum(WWo * Mo, mask)
    tg, tw, tm = Sg.sum(0), Sw.sum(0), Sm.sum(0)
    D = 4 * G * tg / tw; M = tm / tw; Dl = 4 * G * (tg - Sg) / (tw - Sw)
    sk = np.sqrt((NPAT - 1) / NPAT * ((Dl - Dl.mean(0)) ** 2).sum(0))
    return float((D * M / sk ** 2).sum() / (M * M / sk ** 2).sum()), M, sk
def model_amp(mask, T, Mo, sk):
    """amplitude of the per-lens term T (m/s^2 per cell) against the law model, with the data's bin weights; patch jackknife."""
    St = psum(WWo * T, mask); Sw = psum(WWo, mask); Sm = psum(WWo * Mo, mask)
    tt, tw, tm = St.sum(0), Sw.sum(0), Sm.sum(0)
    N = tt / tw; M = tm / tw
    a = float((N * M / sk ** 2).sum() / (M * M / sk ** 2).sum())
    Nl = (tt - St) / (tw - Sw); Ml = (tm - Sm) / (tw - Sw)
    al = (Nl * Ml / sk ** 2).sum(1) / (Ml * Ml / sk ** 2).sum(1)
    return a, al, [float(x) for x in N / M]

# ------------------------------------------------------------------ catalogue
HB = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample.fits"), memmap=True); b = HB[1].data
HL = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample_LePhare.fits"), memmap=True); Lp = HL[1].data
r_ = np.array(b["MAG_AUTO_CALIB"], dtype="f8"); z_ = np.array(b["zphot_ANNz2"], dtype="f8")
logM_ = np.array(Lp["MASS_MED"], dtype="f8") + 0.15; ra_ = np.array(b["RAJ2000"], dtype="f8"); dec_ = np.array(b["DECJ2000"], dtype="f8")
del b, Lp; HB.close(); HL.close()
nb = (r_ < 20) & (z_ >= 0.02) & (z_ <= 0.8) & np.isfinite(logM_) & (logM_ > 7); inb = np.where(nb)[0]
xN = unitvec(ra_[inb], dec_[inb]); chiN = DC(z_[inb]); logMN = logM_[inb]; mN = mgal_of(logMN) * Msun
key = {(a, d): i for i, (a, d) in enumerate(zip(ra_[inb], dec_[inb]))}
selfN = np.array([key[(a, d)] for a, d in zip(ln["ra"], ln["dec"])]); treeN = cKDTree(xN); xL = xN[selfN]
RH = np.minimum(3.0, np.sqrt(G * mgal_of(logMs) * Msun / 1e-15) / Mpc); DAl = chil / (1 + zl)
def scan(idx, Lx, Lself, fac=1.0, dm=None, term=False, CH=300):
    """for the lenses idx: either host-free flags (dm given) or the neighbours' point-mass term per outer cell (term=True)."""
    chord = 2 * np.sin(fac * RH[idx] * (1 + zl[idx]) / chil[idx] / 2)
    dmin = np.full(len(idx), np.inf); T = np.zeros((len(idx), 4)); npair = 0
    for i0 in range(0, len(idx), CH):
        i1 = min(i0 + CH, len(idx))
        lists = treeN.query_ball_point(Lx[i0:i1], r=chord[i0:i1])
        c = np.fromiter((len(x) for x in lists), dtype=np.int64, count=len(lists)); tot = int(c.sum())
        if tot == 0: continue
        k = np.repeat(np.arange(len(c)), c); j = np.fromiter((jj for x in lists for jj in x), dtype=np.int64, count=tot)
        li = i0 + k; gl = idx[li]
        keep = j != Lself[li]
        dc = np.abs(chiN[j] - chil[gl])
        if dm is not None:
            keep &= logMN[j] >= logMs[gl] + dm
            np.minimum.at(dmin, li[keep], dc[keep]); continue
        keep &= dc < W
        li, j, gl = li[keep], j[keep], gl[keep]; npair += len(j)
        d2 = (2 * np.arcsin(np.minimum(np.linalg.norm(xN[j] - Lx[li], axis=1) / 2, 1.0)) * DAl[gl] * Mpc) ** 2      # m^2
        for cidx in range(4):
            t1, t2 = T_LO[gl, cidx], T_HI[gl, cidx]
            with np.errstate(divide="ignore", invalid="ignore"):
                Kin = np.log(t2 / t1)                                  # 2 ln(R2/R1) = ln(t2/t1)
                Kmid = np.log(t2 / np.maximum(d2, 1e-300)) - 1.0       # 2 ln(R2/d) - 1
            K = np.where(d2 < t1, Kin, np.where(d2 < t2, Kmid, 0.0))
            K = np.where(OKC[gl, cidx], K, 0.0)
            with np.errstate(divide="ignore", invalid="ignore"):
                contrib = np.where(OKC[gl, cidx], 4 * G * mN[j] * K / (math.pi * (t2 - t1)), 0.0)
            np.add.at(T[:, cidx], li, contrib)
    return (dmin if dm is not None else T), npair

ALLI = np.arange(NL)
HFf = {}
for fac in (1.0, 1.6):
    dmin, _ = scan(ALLI, xL, selfN, fac=fac, dm=0.3); HFf[fac] = dmin >= W
    P(f"veto radius {fac:.1f} R_h: host-free {int(HFf[fac].sum()):,}  [{time.time() - T0:.0f} s]")
assert int(HFf[1.0].sum()) == 40667 and int(HFf[1.6].sum()) == 17335
# known answer for the kernel: uniformly scattered points give zero net shear in every cell
rng = np.random.default_rng(52); R1, R2 = 1.0, 1.7; dd = np.sqrt(rng.uniform(0, 9.0, 2_000_000))
Kc = np.where(dd < R1, 2 * math.log(R2 / R1), np.where(dd < R2, 2 * np.log(R2 / dd) - 1, 0.0))
ka = float(Kc.mean() / (2 * math.log(R2 / R1) * (R1 / 3.0) ** 2))
P(f"known answer, uniform points give zero net annulus shear: mean kernel / its inner-part share = {ka:+.4f} (|.| < 0.02 required)")
assert abs(ka) < 0.02
SH = json.load(open(os.path.join(HERE, "ko1_shape.json")))
RES = dict(lane="KO1", stage="E8 neighbours", amendment="d0424b7a57", note="reported only", ka_uniform=ka, sets={})
for fac in (1.0, 1.6):
    S = HFf[fac]; idx = np.where(S)[0]
    Treal, npair = scan(idx, xL[idx], selfN[idx], term=True)
    Tfull = np.zeros((NL, 4)); Tfull[idx] = Treal
    shuf = []
    rs = np.random.default_rng(52)
    for _ in range(5):
        perm = rs.permutation(len(idx)); Ts, _ = scan(idx, xL[idx][perm], selfN[idx][perm], term=True)
        Tf = np.zeros((NL, 4)); Tf[idx] = Ts; shuf.append(Tf)
    P(f"\n=== host-free, veto radius {fac:.1f} R_h: {len(idx):,} lenses, {npair:,} neighbour pairs inside range and window  [{time.time() - T0:.0f} s]")
    entry = {}
    for foot in FOOT:
        L = LAW[foot]; A_out, M, sk = data_amp(S, L)
        a_real, al_real, per_real = model_amp(S, Tfull, L, sk)
        a_sh = [model_amp(S, Tf, L, sk) for Tf in shuf]
        a_shuf = float(np.mean([x[0] for x in a_sh])); al_shuf = np.mean([x[1] for x in a_sh], axis=0)
        net = a_real - a_shuf; nl = al_real - al_shuf
        s_net = float(np.sqrt((NPAT - 1) / NPAT * ((nl - nl.mean()) ** 2).sum()))
        k = SH["foot"][foot]["PH3"][f"{fac:.1f}"]["k"]; A_in = SH["foot"][foot]["E7"][f"{fac:.1f}"]["inner"][0]; Rs = SH["foot"][foot]["PH3"][f"{fac:.1f}"]["Rs"]
        share = (1 + X_SHARE) * net; cap = (1 + X_CAP) * net
        zsplit = {}
        for name, m in (("z low", S & (zl <= np.median(zl[S]))), ("z high", S & (zl > np.median(zl[S])))):
            _, _, skz = data_amp(m, L)
            ar = model_amp(m, Tfull, L, skz)[0]; ash = float(np.mean([model_amp(m, Tf, L, skz)[0] for Tf in shuf]))
            zsplit[name] = ar - ash
        entry[foot] = dict(A_outer_data=A_out, a_real=a_real, a_shuffled=a_shuf, a_net=net, s_net=s_net, per_bin_real=per_real,
                           term_share=share, term_cap=cap, s_share=(1 + X_SHARE) * s_net, k=k, A_inner=A_in, Rs_data=Rs,
                           Rs_term_share=k * share / A_in, Rs_term_cap=k * cap / A_in,
                           Rs_two_phase_share_with_neighbours=SH["foot"][foot]["PH3"][f"{fac:.1f}"]["Rs_two_phase_share"] + k * share / A_in,
                           a_net_by_z=zsplit)
        e = entry[foot]
        P(f"  {foot}: per unit (1 + X): around the lenses {a_real:+.5f}, around shuffled positions {a_shuf:+.5f}, net a_nb {net:+.5f} +- {s_net:.5f} of the law's level")
        P(f"     at the record's share (X {X_SHARE:.3f}): {share:+.4f} +- {(1 + X_SHARE) * s_net:.4f};  at the census cap (X {X_CAP}): {cap:+.3f}   [data outer amplitude {A_out:.3f}]")
        P(f"     calibration-free (k {k:.2f}, inner {A_in:.3f}): neighbours add {k * share / A_in:+.4f} to R_s at the record's share ({k * cap / A_in:+.3f} at the cap); "
          f"two-phase with the record's share and its neighbours: {e['Rs_two_phase_share_with_neighbours']:.3f} against the measured {Rs[0]:.3f} +- {Rs[1]:.3f} "
          f"({(Rs[0] - e['Rs_two_phase_share_with_neighbours']) / Rs[1]:+.2f} sigma)")
        P(f"     net a_nb by redshift half: low {zsplit['z low']:+.5f}, high {zsplit['z high']:+.5f}")
        # the share the outer bins need when every neighbour carries the same share: R_s(X) = (1 + X) k (a_unit + a_nb) / A_inner
        a_unit = SH["foot"][foot]["PH3"][f"{fac:.1f}"]["Rs_two_phase_cap"] * A_in / (k * (1 + X_CAP))
        need = lambda r: r * A_in / (k * (a_unit + net)) - 1
        Xb, Xlo, Xhi = need(Rs[0]), need(Rs[0] - 2 * Rs[1]), need(Rs[0] + 2 * Rs[1])
        def weight_over_force(X, a0):                              # shell of X M_b at the allowance radius (g_bar 7.5e-15), exact W
            y = 7.5e-15 / a0; u = y / 2 + math.sqrt(y * y / 4 + y); Wv = u - math.log1p(u) - u * u / (2 * (1 + u) ** 2)
            return y * X * (1 + X / 2) / (Wv / y)
        e.update(a_unit=a_unit, X_best_with_neighbours=Xb, X_2sigma_with_neighbours=(Xlo, Xhi),
                 weight_over_force_at_2sigma_min=weight_over_force(Xlo, A0[foot]), weight_over_force_at_best=weight_over_force(Xb, A0[foot]),
                 share_multiple_2sigma_min=Xlo / X_SHARE)
        P(f"     share needed when neighbours carry it too: X {Xb:.0f} (2 sigma {Xlo:.0f} to {Xhi:.0f}) = at least {Xlo / X_SHARE:.1f} shares; "
          f"such a shell outweighs the wall force by {weight_over_force(Xlo, A0[foot]):.1f} (2 sigma minimum) and {weight_over_force(Xb, A0[foot]):.1f} (best fit)")
    RES["sets"][f"{fac:.1f}"] = dict(n=int(len(idx)), pairs=int(npair), foot=entry)
P(f"\nruntime {time.time() - T0:.0f} s")
P("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.ndarray): return [clean(v) for v in o.tolist()]
    if isinstance(o, (np.floating, float)): return float(o) if np.isfinite(o) else None
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
json.dump(clean(RES), open(os.path.join(HERE, "ko1_neighbours.json"), "w"), indent=1)
open(os.path.join(HERE, "ko1_neighbours.out"), "w").write("\n".join(OUT) + "\n")

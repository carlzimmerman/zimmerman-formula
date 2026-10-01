#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG245 Gate G0 -- DEFINITIONS AND CONTROLS (frozen criteria section 3): the local-field target, its identity with the CFG44 target for extended
baryons, positivity, conservation of the relaxation operator, and ownership from the local form.

  G0.1 C-L1  3D 4th-order finite-difference rho_ph = -div[(nu-1) g_N]/(4 pi G) against (a) the spherical enclosed-mass form and (b) the hand closed form
             rho_ph = rho_b (nu-1)^2/(2 nu) + M_b(<r)/(4 pi r^3 y nu)  (P2, spherical), tolerance 1e-3 relative.
  G0.2       R_loc = C_loc / C_44 on the exponential spheres (CFG118's h = 2,3,4,5 kpc at 1e9..1e12), x in [0.1, 30], both footings and kernels
             (reported, not binding); C-L2 point mass: R_loc = 1 for P2.
  G0.3       positivity: spherical min rho_ph >= 0; non-spherical f_neg = int rho_ph^- / int |rho_ph| for two equal masses (d = 1, 3, 10 r_M, box +-20 r_M)
             and an exponential thin disc; PASS iff f_neg <= 0.01 else UNDEFINED for non-spherical flows.
  G0.4       the relaxation (flux) operator conserves mass inside the closed domain D to 1e-12; M_ph(<r) grows linearly (reported).
  G0.5       ownership from the local form: internal-to-Newtonian ratio of a satellite in a host field; PASS iff 1 (expected FAIL).
Units for the field tests: G = 1, a0 = 1 (so r_M = sqrt(G M_b/a0) = 1 for M_b = 1).
Run: ZF_REPO=<repo> python3 CFG245_G0_target.py ; MUTATE=MG1|MG2|MG3 python3 CFG245_G0_target.py   (MUTATE exits 1 when the control bites)
kappa = 1/2 FITTED; no dark-matter particle; the mass is required; nothing here is closure.
"""
import os, sys, math
sys.dont_write_bytecode = True
import numpy as np
from scipy.special import gammainc
from scipy.signal import fftconvolve
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG245_common as K

MUT = os.environ.get("MUTATE", "").strip()
SLUG = "CFG245_G0_target"
R = K.Report(SLUG, MUT or None)
ACTIVE = ""      # the mutation currently applied inside the test functions (set by main)
HEXP = {1e9: 2.0, 1e10: 3.0, 1e11: 4.0, 1e12: 5.0}      # kpc (CFG118's exponential spheres, as in the frozen text)


def nu_fn(kernel):
    return K.KERNELS[kernel]


# ------------------------------------------------------------------------------------------------ 3D finite differences (4th order)
def div4(Fx, Fy, Fz, h):
    """4th-order central divergence on the interior (shape N-4 per axis)."""
    def d(F, ax):
        sl = lambda a, b: tuple(slice(a, F.shape[i] - b) if i == ax else slice(2, F.shape[i] - 2) for i in range(3))
        return (-F[sl(4, 0)] + 8 * F[sl(3, 1)] - 8 * F[sl(1, 3)] + F[sl(0, 4)]) / (12 * h)
    return d(Fx, 0) + d(Fy, 1) + d(Fz, 2)


def interior_coords(L, N):
    x = np.linspace(-L, L, N)
    h = x[1] - x[0]
    xi = x[2:-2]
    return x, xi, h


# ------------------------------------------------------------------------------------------------ spherical enclosed-mass references
def sph_rho_ph(rg, Menc, kernel="P2"):
    """rho_ph(r) = (1/(4 pi r^2)) d/dr [r^2 (nu - 1) g_N], g_N = M(<r)/r^2, a0 = G = 1; numerical derivative on a fine grid."""
    g = Menc(rg) / rg ** 2
    Mph = rg ** 2 * (nu_fn(kernel)(g) - 1.0) * g
    # note r^2 (nu-1) g = G M_ph(<r); with g = M_b(<r)/r^2 this is (nu-1) M_b(<r)
    dM = np.gradient(Mph, rg, edge_order=2)
    return dM / (4 * math.pi * rg ** 2), Mph, g


def closed_form_p2(r, Menc, rho_b):
    g = Menc(r) / r ** 2
    y = g
    nu = np.sqrt(1 + 1 / y)
    return rho_b(r) * (nu - 1) ** 2 / (2 * nu) + Menc(r) / (4 * math.pi * r ** 3 * y * nu)


SPH = {
    "uniform sphere (a = 3 r_M)": dict(
        Menc=lambda r: np.where(r < 3.0, (r / 3.0) ** 3, 1.0),
        rho=lambda r: np.where(r < 3.0, 3.0 / (4 * math.pi * 27.0), 0.0), a=3.0),
    "Plummer (eps = 0.5 r_M)": dict(
        Menc=lambda r: r ** 3 / (r * r + 0.25) ** 1.5,
        rho=lambda r: 3.0 * 0.25 / (4 * math.pi) / (r * r + 0.25) ** 2.5, a=None),
    "exponential sphere (h = 1 r_M)": dict(
        Menc=lambda r: gammainc(3.0, r / 1.0),
        rho=lambda r: np.exp(-r / 1.0) / (8 * math.pi), a=None),
}


def test_CL1(res):
    R.banner("G0.1 / C-L1 -- the local-field target by 3D finite differences against the spherical enclosed-mass form and the hand closed form (P2)")
    N, L = 161, 8.0
    x, xi, h = interior_coords(L, N)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij", sparse=True)
    Xi, Yi, Zi = np.meshgrid(xi, xi, xi, indexing="ij", sparse=True)
    rr = np.sqrt(Xi ** 2 + Yi ** 2 + Zi ** 2)
    rg = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
    out = {}
    worst = 0.0
    for name, s in SPH.items():
        Menc, rho = s["Menc"], s["rho"]
        rsafe = np.maximum(rg, 1e-9)
        gmag = Menc(rsafe) / rsafe ** 2                  # inward magnitude
        nu = nu_fn("P2")(gmag)
        fac = -(nu - 1.0) * gmag / rsafe                 # (nu-1) g_N vector = fac * (x, y, z)  (g_N points inward)
        div = div4(fac * X, fac * Y, fac * Z, h)
        rho3 = -div / (4 * math.pi)
        # spherical references on a fine grid, interpolated to the 3D points
        rf = np.linspace(0.02, 9.0, 450001)
        rs, _, _ = sph_rho_ph(rf, Menc, "P2")
        rho_sph = np.interp(rr, rf, rs)
        rho_cf = closed_form_p2(np.maximum(rr, 1e-9), Menc, rho)
        msk = (rr >= 1.0) & (rr <= 5.0)
        if s["a"] is not None:
            msk &= np.abs(rr - s["a"]) > 3 * h
        e1 = np.abs(rho3[msk] / rho_sph[msk] - 1).max()
        e2 = np.abs(rho3[msk] / rho_cf[msk] - 1).max()
        e3 = np.abs(rho_sph[msk] / rho_cf[msk] - 1).max()
        out[name] = (float(e1), float(e2), float(e3), int(msk.sum()))
        worst = max(worst, e1, e2)
        R.P(f"  {name:34s} n = {int(msk.sum()):8d}: max rel diff  3D-FD vs spherical form {e1:.2e};  3D-FD vs hand closed form {e2:.2e};  spherical numeric vs closed form {e3:.2e}")
    ok = worst < 1e-3
    R.cell("C-L1 3D local-field target equals the spherical form and the hand closed form (tolerance 1e-3, r in [1,5] r_M, away from the sphere edge; h = %.3f, N = %d, 4th-order)" % (h, N),
           "PASS" if ok else "FAIL", f"worst {worst:.2e}")
    res["C-L1"] = dict(ok=bool(ok), detail=out, worst=float(worst))
    return ok


def test_CL2(res):
    R.banner("C-L2 -- point mass: C_loc = C_44 (P2) exactly; nu_mono point-mass ratio at x = 1 (CFG44 README:39: 1.46)")
    rg = np.geomspace(0.1, 30.0, 4001)
    out = {}
    for kern in ("P2", "nu_mono"):
        rs, Mph, g = sph_rho_ph(rg, lambda r: np.ones_like(r), kern)
        nu = nu_fn(kern)(g)
        Closs = rs * rg ** 3 * nu * g                       # rho_ph r^3 g_tot, a0 = G = 1, g_tot = nu g_N
        C44 = np.full_like(rg, 1.0 / (4 * math.pi))
        ratio = Closs / C44
        mid = (rg > 0.15) & (rg < 25)
        out[kern] = dict(max_dev=float(np.abs(ratio[mid] - 1).max()), ratio_at_1=float(np.interp(1.0, rg, ratio)))
        R.P(f"  {kern:8s}: max |C_loc/C_44 - 1| on x in [0.15, 25] = {out[kern]['max_dev']:.3e};  ratio at x = 1: {out[kern]['ratio_at_1']:.4f}")
    ok = out["P2"]["max_dev"] < 1e-3 and abs(out["nu_mono"]["ratio_at_1"] - 1.46) < 0.02
    R.cell("C-L2 point mass: P2 C_loc/C_44 = 1.000 (1e-3); nu_mono ratio at x = 1 equals CFG44's 1.46 (within 0.02)", "PASS" if ok else "FAIL")
    res["C-L2"] = dict(ok=bool(ok), **out)
    # deep-limit uniform sphere factor 2.5
    r = np.linspace(0.05, 0.4, 200)
    a = 50.0                                                  # a large uniform sphere: deep MOND interior at r << a
    Menc = lambda rr: (rr / a) ** 3
    rho = 3.0 / (4 * math.pi * a ** 3)
    g = Menc(r) / r ** 2
    nu = nu_fn("P2")(g)
    Rloc = 1 + 2 * math.pi * r ** 3 * rho * g * (nu - 1) ** 2 / (Menc(r))
    R.P(f"  uniform sphere interior, deep regime (r << r_M): C_loc/C_44 = {Rloc.min():.3f}-{Rloc.max():.3f} (hand: 2.5)")
    res["deep_uniform_factor"] = float(Rloc.mean())
    return ok


# ------------------------------------------------------------------------------------------------ G0.2
def test_G02(res):
    R.banner("G0.2 -- target identity: R_loc = C_loc/C_44 on CFG118's exponential spheres (reported; IDENTICAL if max R_loc <= 1.10, else DIFFERS)")
    out = {}
    xg = np.geomspace(0.1, 30.0, 3000)
    anyd = False
    for kern in ("P2", "nu_mono"):
        for foot in K.FOOTS:
            for M in K.MASSES:
                rm = K.r_M(M, foot)
                hh = HEXP[M] / rm
                Menc = lambda r, hh=hh: gammainc(3.0, r / hh)
                rho = lambda r, hh=hh: np.exp(-r / hh) / (8 * math.pi * hh ** 3)
                rs, Mph, g = sph_rho_ph(xg, Menc, kern)
                nu = nu_fn(kern)(g)
                Closs = rs * xg ** 3 * nu * g
                C44 = Menc(xg) / (4 * math.pi)
                Rl = Closs / C44
                if ACTIVE == "MG1":
                    Rl = np.ones_like(Rl)                       # the target replaced by the true C(r)
                mx = float(Rl.max()); xm = float(xg[Rl.argmax()])
                mn = float(Rl.min())
                out[f"{kern}|{foot}|{M:.0e}"] = dict(h_over_rM=hh, max=mx, x_at_max=xm, min=mn, min_rho_ph=float(rs.min()))
    for kern in ("P2", "nu_mono"):
        for foot in K.FOOTS:
            R.P(f"  {kern:8s} {foot:10s} " + "  ".join(f"{M:.0e}: max R_loc {out[f'{kern}|{foot}|{M:.0e}']['max']:.3f} at x={out[f'{kern}|{foot}|{M:.0e}']['x_at_max']:.2f} (h/r_M = {out[f'{kern}|{foot}|{M:.0e}']['h_over_rM']:.2f})" for M in K.MASSES))
    mxall = max(v["max"] for k, v in out.items() if k.startswith("P2"))
    cat = "IDENTICAL" if mxall <= 1.10 else "DIFFERS"
    R.cell("G0.2 target identity (P2, all exponential spheres, both footings; reported, not binding)", cat, f"max R_loc (P2) = {mxall:.3f}; max R_loc (nu_mono) = {max(v['max'] for k, v in out.items() if k.startswith('nu_mono')):.3f}")
    res["G0.2"] = dict(category=cat, max_P2=mxall, table=out)
    return cat


# ------------------------------------------------------------------------------------------------ G0.3
def plummer_g(x, y, z, c, eps, m=1.0):
    dx, dy, dz = x - c[0], y - c[1], z - c[2]
    r2 = dx * dx + dy * dy + dz * dz + eps * eps
    f = -m / r2 ** 1.5
    return f * dx, f * dy, f * dz


def fneg_two_masses(d, N, L=20.0, eps=0.3, kernel="P2"):
    x, xi, h = interior_coords(L, N)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij", sparse=True)
    g1 = plummer_g(X, Y, Z, (-d / 2, 0, 0), eps)
    g2 = plummer_g(X, Y, Z, (d / 2, 0, 0), eps)
    gx, gy, gz = g1[0] + g2[0], g1[1] + g2[1], g1[2] + g2[2]
    gm = np.sqrt(gx ** 2 + gy ** 2 + gz ** 2)
    nu = nu_fn(kernel)(gm) if ACTIVE != "MG2" else np.ones_like(gm)      # MG2: Newton (nu = 1) => rho_ph = 0
    f = (nu - 1.0)
    rho = -div4(f * gx, f * gy, f * gz, h) / (4 * math.pi)
    neg = float(-rho[rho < 0].sum()); tot = float(np.abs(rho).sum())
    return (neg / tot if tot > 0 else 0.0), float(rho.min()), float(rho.max()), h


def disc_fneg(rM_over_hd, N=121, Nz=65, Lh=12.0, Lz=4.0, z0=0.25, eps=0.2, kernel="P2"):
    """exponential thin disc (h_d = 1, M = 1, exponential in |z| with scale z0); g_N by FFT convolution with the softened kernel."""
    x = np.linspace(-Lh, Lh, N); z = np.linspace(-Lz, Lz, Nz)
    hx, hz = x[1] - x[0], z[1] - z[0]
    X, Y, Z = np.meshgrid(x, x, z, indexing="ij", sparse=True)
    Rr = np.sqrt(X ** 2 + Y ** 2)
    rho = np.exp(-Rr) * np.exp(-np.abs(Z) / z0) / (4 * math.pi * z0)
    mass = rho * hx * hx * hz
    mass *= 1.0 / mass.sum()
    kx = (np.arange(2 * N - 1) - (N - 1)) * hx; kz = (np.arange(2 * Nz - 1) - (Nz - 1)) * hz
    KX, KY, KZ = np.meshgrid(kx, kx, kz, indexing="ij", sparse=True)
    den = (KX ** 2 + KY ** 2 + KZ ** 2 + eps ** 2) ** 1.5
    g = []
    for comp in (KX, KY, KZ):
        Kc = -comp / den
        g.append(fftconvolve(mass, Kc, mode="same"))
    gm = np.sqrt(g[0] ** 2 + g[1] ** 2 + g[2] ** 2)
    a0 = 1.0 / rM_over_hd ** 2
    nu = nu_fn(kernel)(gm / a0)
    f = nu - 1.0
    # anisotropic spacing: do the divergence axis by axis with the right h
    def d4(F, ax, hh):
        sl = lambda a, b: tuple(slice(a, F.shape[i] - b) if i == ax else slice(2, F.shape[i] - 2) for i in range(3))
        return (-F[sl(4, 0)] + 8 * F[sl(3, 1)] - 8 * F[sl(1, 3)] + F[sl(0, 4)]) / (12 * hh)
    div = d4(f * g[0], 0, hx) + d4(f * g[1], 1, hx) + d4(f * g[2], 2, hz)
    rho_ph = -div / (4 * math.pi)
    # exclude a margin of the outer 4 cells in x,y (the FFT 'same' truncation is not a true isolated field there)
    rho_ph = rho_ph[4:-4, 4:-4, :]
    neg = float(-rho_ph[rho_ph < 0].sum()); tot = float(np.abs(rho_ph).sum())
    return neg / tot, float(rho_ph.min()), float(rho_ph.max())


def test_G03(res):
    R.banner("G0.3 -- positivity of the local-field target")
    # spherical
    G02 = res.get("G0.2", {}).get("table", {})
    mins = {k: v["min_rho_ph"] for k, v in G02.items()}
    smin = min(mins.values()) if mins else float("nan")
    R.P(f"  spherical exponential spheres (all kernels/footings/masses): min rho_ph = {smin:.3e} (P2 closed form is >= 0; nu_mono reported)")
    R.cell("G0.3 spherical positivity (P2)", "PASS" if min(v for k, v in mins.items() if k.startswith("P2")) >= -1e-12 else "FAIL", f"min over P2 rows {min(v for k, v in mins.items() if k.startswith('P2')):.3e}")
    # two masses
    tm = {}
    R.P("  two equal masses (M = 1 each, r_M = 1), Plummer eps = 0.3, box +-20 r_M, 4th-order differences; f_neg = int rho_ph^- / int |rho_ph|")
    for d in (1.0, 3.0, 10.0):
        row = {}
        for N in (161, 201):
            fn, mn, mx, h = fneg_two_masses(d, N)
            row[N] = dict(fneg=fn, rho_min=mn, rho_max=mx, h=h)
        tm[d] = row
        R.P(f"    d = {d:4.1f} r_M: " + "; ".join(f"N = {N} (h = {row[N]['h']:.3f}): f_neg = {row[N]['fneg']:.4f}, rho_ph in [{row[N]['rho_min']:.2e}, {row[N]['rho_max']:.2e}]" for N in row))
    two_mx = max(tm[d][N]["fneg"] for d in tm for N in tm[d])
    R.cell("G0.3 non-spherical, two equal masses (f_neg <= 0.01 at every separation and both resolutions)", "PASS" if two_mx <= 0.01 else "UNDEFINED (f_neg > 0.01)", f"max f_neg = {two_mx:.4f}")
    dd = {}
    if not ACTIVE:
        R.P("  exponential thin disc (h_d = 1, scale height 0.25), r_M/h_d = 0.3, 1, 3 (a0 = 1/r_M^2):")
        for rm in (0.3, 1.0, 3.0):
            fn, mn, mx = disc_fneg(rm)
            dd[rm] = dict(fneg=fn, rho_min=mn, rho_max=mx)
            R.P(f"    r_M/h_d = {rm}: f_neg = {fn:.4f}, rho_ph in [{mn:.2e}, {mx:.2e}]")
        dmx = max(v["fneg"] for v in dd.values())
        R.cell("G0.3 non-spherical, exponential thin disc (f_neg <= 0.01)", "PASS" if dmx <= 0.01 else "UNDEFINED (f_neg > 0.01)", f"max f_neg = {dmx:.4f}")
    res["G0.3"] = dict(two_masses={str(k): {str(n): v for n, v in r.items()} for k, r in tm.items()}, two_max=two_mx, disc={str(k): v for k, v in dd.items()}, spherical_min=smin,
                       two_outcome=("PASS" if two_mx <= 0.01 else "UNDEFINED"), disc_outcome=(("PASS" if max(v["fneg"] for v in dd.values()) <= 0.01 else "UNDEFINED") if dd else "not run"))
    return two_mx


# ------------------------------------------------------------------------------------------------ G0.4
def test_G04(res):
    R.banner("G0.4 -- mass conservation of the relaxation (flux) operator inside the closed domain D, and positivity of the relaxed density")
    out = {}
    ok_all = True
    for foot in ("canonical",):
        for kernel_mode in ("two", "one"):
            M, q = 1e10, 0.1
            p = K.passive(M, q, foot)
            Mc0 = p["Minf"].copy()
            Mph = p["Mph"]
            S_D = Mc0[-1]                                   # closed sub-domain: D = [0, x_last], its own mass the cap
            Mt = np.minimum(Mph, S_D)
            G = K.HL
            def rhs(Mc):
                if kernel_mode == "two":
                    return G * (Mt - Mc)
                return G * np.maximum(Mt - Mc, 0.0)
            Mc = Mc0.copy()
            nst = 4000; dt = K.T0 / nst
            for _ in range(nst):
                k1 = rhs(Mc); k2 = rhs(Mc + 0.5 * dt * k1); k3 = rhs(Mc + 0.5 * dt * k2); k4 = rhs(Mc + dt * k3)
                Mc = Mc + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            # the closed boundary: the mass inside the outermost grid radius must not change (zero net flux)
            dMout = abs(Mc[-1] - Mc0[-1]) / Mc0[-1]
            dens = np.diff(np.concatenate([[0.0], Mc]))
            minden = float(dens.min())
            out[f"{foot}|{kernel_mode}"] = dict(mass_change_rel=float(dMout), min_shell_mass=minden)
            ok = dMout < 1e-12 and minden >= 0
            ok_all &= ok
            R.P(f"  {foot} {kernel_mode}-sided: |M_c(<R_D, t_0) - M_c(<R_D, 0)|/M = {dMout:.2e}; min shell mass after relaxation = {minden:.3e} Msun (>= 0: density non-negative)")
    # creation form: no cap, mass is created
    M, q = 1e10, 0.1
    p = K.passive(M, q, "canonical")
    e = math.exp(-K.HL * K.T0)
    Mcr = K.relaxed_Mc(p["Minf"], p["Mph"], p["S"], e, "two", create=True)
    created = (Mcr[-1] - p["Minf"][-1]) / M
    out["creation form"] = dict(mass_created_over_Mb=float(created))
    R.P(f"  creation form (variant V-CREATE), no cap: M_c(<x = {K.XC[-1]:.1f}) changes by {created:+.3f} M_b over t_0 (mass is NOT conserved)")
    R.cell("G0.4 flux operator conserves mass in D to 1e-12 and keeps the density non-negative", "PASS" if ok_all else "FAIL",
           "; ".join(f"{k}: {v}" for k, v in out.items()))
    # linear growth of M_ph
    R.P("  M_ph(<r) for a point mass = M_b (sqrt(1+x^2) - 1) -> sqrt(M a0/G) r: coefficient M_b/r_M (Msun/kpc): " +
        ", ".join(f"{M:.0e}: {M / K.r_M(M):.3e}" for M in K.MASSES))
    res["G0.4"] = dict(ok=bool(ok_all), table=out, linear_coeff={f"{M:.0e}": M / K.r_M(M) for M in K.MASSES})
    return ok_all


# ------------------------------------------------------------------------------------------------ G0.5
def test_G05(res):
    R.banner("G0.5 -- ownership from the local form: a satellite in a host's field (local-field target on the TOTAL Newtonian field)")
    Mh = 6e10
    ext = {}
    a0 = K.A0K["canonical"]
    G = K.G_KPC
    nu = nu_fn("P2")
    xg, wg = np.polynomial.legendre.leggauss(96)           # cos(theta) w.r.t. the host-satellite axis
    rows = []
    allok = True
    worst = 0.0
    for ms in (1e5, 1e8):
        rMs = K.r_M(ms)
        for dist in (30.0, 100.0, 250.0):
            gh_sat = G * Mh / dist ** 2                       # host field at the satellite centre (points toward the host: -x direction)
            for rfac in (0.3, 1.0, 3.0):
                r = rfac * rMs
                ct = xg; st = np.sqrt(1 - ct ** 2)
                # position relative to the host: host at origin, satellite at (dist, 0, 0); field point = sat + r n, n = (ct, st, 0) (axisymmetric about x)
                px = dist + r * ct; py = r * st
                rho_h = np.sqrt(px ** 2 + py ** 2)
                ghx = -G * Mh * px / rho_h ** 3; ghy = -G * Mh * py / rho_h ** 3
                rs_ = r
                gsx = -G * ms * ct / rs_ ** 2; gsy = -G * ms * st / rs_ ** 2   # satellite's own Newtonian field (inward)
                gx, gy = ghx + gsx, ghy + gsy
                gm = np.hypot(gx, gy)
                nuv = nu(gm / a0)
                lx, ly = nuv * gx, nuv * gy
                # the law evaluated with the host alone at the satellite centre (uniform external field) is subtracted
                gc = np.array([-gh_sat, 0.0])
                lc = nu(gh_sat / a0) * gc
                ix, iy = lx - lc[0], ly - lc[1]
                inward = -(ix * ct + iy * st)                    # inward radial component
                avg = 0.5 * np.sum(wg * inward)
                gN_int = G * ms / r ** 2
                if ACTIVE == "MG3":
                    avg = gN_int                                 # the bound-only label: owned => Newtonian internal acceleration
                ratio = avg / gN_int
                rows.append(dict(m_sat=ms, d_kpc=dist, r_over_rM=rfac, ratio=float(ratio)))
                worst = max(worst, abs(ratio - 1))
    # isolated (top-level) comparison
    iso = {rf: float(nu(1.0 / rf ** 2) ) for rf in (0.3, 1.0, 3.0)}
    for ms in (1e5, 1e8):
        R.P(f"  m_sat = {ms:.0e} Msun (r_M = {K.r_M(ms):.4f} kpc): " + "  ".join(
            f"d={d:5.0f}: " + "/".join(f"{[x['ratio'] for x in rows if x['m_sat']==ms and x['d_kpc']==d and x['r_over_rM']==rf][0]:.3f}" for rf in (0.3, 1.0, 3.0)) for d in (30.0, 100.0, 250.0)))
    R.P("  columns: ratio at r = 0.3 / 1 / 3 r_M(sat); the isolated top-level law gives nu(1/x^2) = " + " / ".join(f"{iso[rf]:.3f}" for rf in (0.3, 1.0, 3.0)))
    ok = worst < 1e-3
    R.cell("G0.5 ownership produced by the local form (internal ratio = 1 within 1e-3 at every row)", "PASS" if ok else "FAIL",
           f"max |ratio - 1| = {worst:.3f}; expected FAIL: ownership is a separate label (ChainCert ownership_not_field_local)")
    res["G0.5"] = dict(ok=bool(ok), worst=float(worst), rows=rows, isolated=iso)
    return ok


def main():
    global ACTIVE
    res = {}
    R.banner("CFG245 Gate G0 -- definitions and controls (frozen section 3)" + (f"  (MUTATE {MUT})" if MUT else ""))
    if MUT:
        # baseline (no mutation) first, then the mutated cell; a control bites only if the target cell FLIPS
        ACTIVE = ""
        if MUT == "MG1":
            cat0 = test_G02({})
            ACTIVE = "MG1"; cat1 = test_G02({})
            bites = (cat0 != cat1)
            R.P(f"  MUTATE MG1: G0.2 category baseline {cat0} -> with the target replaced by C_44 {cat1}")
        elif MUT == "MG2":
            r0 = {}; test_G02(r0)
            two0 = test_G03(r0)
            ACTIVE = "MG2"; r1 = {}; test_G02(r1); two1 = test_G03(r1)
            c0 = "PASS" if two0 <= 0.01 else "UNDEFINED"; c1 = "PASS" if two1 <= 0.01 else "UNDEFINED"
            bites = (c0 != c1)
            R.P(f"  MUTATE MG2: two-mass positivity cell baseline {c0} (max f_neg {two0:.4f}) -> with nu = 1 {c1} (max f_neg {two1:.4f}); the frozen premise was baseline UNDEFINED (f_neg > 0.01)")
        elif MUT == "MG3":
            ok0 = test_G05({})
            ACTIVE = "MG3"; ok1 = test_G05({})
            bites = (ok0 != ok1)
            R.P(f"  MUTATE MG3: ownership cell baseline {'PASS' if ok0 else 'FAIL'} -> with the bound-only label {'PASS' if ok1 else 'FAIL'}")
        else:
            raise SystemExit(f"MUTATE {MUT} is not a G0 control")
        R.finish(dict(binding_fail=False, mutate_bites=bool(bites)))
        K.exit_mutate(bites, True)
    ok1 = test_CL1(res)
    ok2 = test_CL2(res)
    cat = test_G02(res)
    two = test_G03(res)
    test_G04(res)
    ok5 = test_G05(res)
    controls_ok = bool(res["C-L1"]["ok"] and res["C-L2"]["ok"])
    R.cell("G0 controls (C-L1, C-L2) -- the lane stops UNDEFINED only if one fails", "PASS" if controls_ok else "FAIL")
    R.finish(dict(binding_fail=False, controls_ok=controls_ok, results=res,
                  outcomes={"G0.2": cat, "G0.3 two masses": res["G0.3"]["two_outcome"], "G0.3 disc": res["G0.3"]["disc_outcome"], "G0.4": "PASS" if res["G0.4"]["ok"] else "FAIL",
                            "G0.5": "PASS" if ok5 else "FAIL"}))
    return 0


if __name__ == "__main__":
    sys.exit(main())

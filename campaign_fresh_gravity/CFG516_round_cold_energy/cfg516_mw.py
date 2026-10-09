#!/usr/bin/env python3
"""CFG516 Part 1: Milky Way K_z,1.1(R) robustness of the round enclosed-mass rule (RM) across baryon models.

Frozen criteria: FROZEN_CRITERIA.md (committed alone first, b35642ca6).
Models per baryon model (B1 McMillan17, B2 L172/CFG513 6.0e10, B2b 7.3e10, B3 short disc):
  PD    full QUMOND (nu_mono) field = the phantom disc (CFG514's framework)
  RMphi spherical cold energy with the shell-averaged phantom's enclosed mass (CFG514's MUTATE)
  RMv   spherical cold energy with M_law(<r) = r v_law(r)^2/G, v_law = algebraic law on the in-plane Newtonian field
  N     baryons + NFW fitted to Eilers+19
MUTATE (CFG516_MUTATE=1): each RM's cold mass placed in an oblate homeoid of axis ratio q = 0.3 (same M(<m)),
solved by Poisson; it must reproduce the rejection (chi2 >= RM + 4).
Solver, data loaders and McMillan17 baryons are CFG514's (executed from its committed file, not edited).
kappa = 1/2 is FITTED; both footings; cold energy mass still required; not theory closed.
Run: nice -n 15 python3 cfg516_mw.py   (<= 4 threads)
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "4"
import sys, json, math, time
import numpy as np
from scipy.optimize import least_squares, minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
SRC514 = os.path.join(HERE, "..", "CFG514_directional_milky_way", "cfg514_directional.py")
src = open(SRC514).read()
head = src.split("# ------------------------------------------------------------------ build the framework / rival")[0]
ns = {"__file__": os.path.abspath(SRC514)}
exec(compile(head, "cfg514_head", "exec"), ns)
G, R0, A0, KZ_UNIT, F_B = ns["G"], ns["R0"], ns["A0"], ns["KZ_UNIT"], ns["F_B"]
Grid, Model, nu_mono = ns["Grid"], ns["Model"], ns["nu_mono"]
phi_kepler, phi_qumond_sph = ns["phi_kepler"], ns["phi_qumond_sph"]
nfw_params, nfw_g = ns["nfw_params"], ns["nfw_g"]
rho_mcm = ns["rho_baryon"]
EIL_R, EIL_V, EIL_E = ns["EIL_R"], ns["EIL_V"], ns["EIL_E"]
BR_R, BR_K, BR_E, BR_E5, BR = ns["BR_R"], ns["BR_K"], ns["BR_E"], ns["BR_E5"], ns["BR"]

MUTATE = os.environ.get("CFG516_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
Q_MUT = 0.3
OUT = []
CHECKS = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); OUT.append(s)


def check(cond, msg):
    CHECKS.append((bool(cond), msg)); P(f"  [{'PASS' if cond else 'FAIL'}] {msg}")
    return bool(cond)


T0 = time.time()
P("=" * 110)
P(f"CFG516 Part 1  Milky Way K_z robustness of the round enclosed-mass rule  {'*** MUTATE: q=0.3 homeoid ***' if MUTATE else 'PRIMARY'}")
P("=" * 110)
GR = Grid()

# ------------------------------------------------------------------ baryon models
PC2, PC3 = 1e6, 1e9


def rho_b2(R, z, Mtot=6.0e10):
    s = Mtot / 6.0e10
    Mbul, abul = 0.90e10 * s, 0.7
    Md, Rd, hd = 4.03e10 * s, 2.6, 0.3
    Mg, Rg, hg = 1.08e10 * s, 6.0, 0.1
    z = np.abs(z); r = np.maximum(np.sqrt(R * R + z * z), 1e-7)
    bul = Mbul * abul / (2 * math.pi * r * (r + abul) ** 3)
    disc = Md / (4 * math.pi * Rd ** 2 * hd) * np.exp(-R / Rd - z / hd)
    gas = Mg / (4 * math.pi * Rg ** 2 * hg) * np.exp(-R / Rg - z / hg)
    return bul + disc + gas


# B3: McMillan thin/thick with R_d -> 2.15, renormalised to keep each disc's own Sigma(R0)
S0_THIN, RD_THIN, ZD_THIN = ns["S0_THIN"], ns["RD_THIN"], ns["ZD_THIN"]
S0_THICK, RD_THICK, ZD_THICK = ns["S0_THICK"], ns["RD_THICK"], ns["ZD_THICK"]
RD_SHORT = 2.15


def rho_b3(R, z):
    zz = np.abs(z)
    old_thin = (S0_THIN / (2 * ZD_THIN)) * np.exp(-zz / ZD_THIN - R / RD_THIN)
    old_thick = (S0_THICK / (2 * ZD_THICK)) * np.exp(-zz / ZD_THICK - R / RD_THICK)
    s_thin = S0_THIN * math.exp(-R0 / RD_THIN + R0 / RD_SHORT)
    s_thick = S0_THICK * math.exp(-R0 / RD_THICK + R0 / RD_SHORT)
    new_thin = (s_thin / (2 * ZD_THIN)) * np.exp(-zz / ZD_THIN - R / RD_SHORT)
    new_thick = (s_thick / (2 * ZD_THICK)) * np.exp(-zz / ZD_THICK - R / RD_SHORT)
    return rho_mcm(R, z) - old_thin - old_thick + new_thin + new_thick


BARYONS = {
    "B1_McMillan17": rho_mcm,
    "B2_L172_6.0e10": lambda R, z: rho_b2(R, z, 6.0e10),
    "B2b_L172_7.3e10": lambda R, z: rho_b2(R, z, 7.3e10),
    "B3_short_disc_2.15": rho_b3,
}

RS = np.geomspace(0.02, 2500.0, 240)           # radial table for spherical cold mass (Gauss-flux masses: smooth)


def flux_mass(gRz, r, nth=200):
    """M(<r) = r^2 <g_r> / G over the sphere (Gauss), from a field function returning (dPhi/dR, dPhi/d|z|)."""
    mu = (np.arange(nth) + 0.5) / nth
    out = []
    for rr in np.atleast_1d(r):
        z = rr * mu; R = rr * np.sqrt(1 - mu ** 2)
        dR, dz = gRz(R, z)
        out.append(rr ** 2 * np.mean((dR * R + dz * z) / rr) / G)
    return np.array(out)


def Mtab(M, r):
    """interpolate a cold-mass table in log r; M ~ r^3 inside the first table radius."""
    r = np.asarray(r, float)
    return np.where(r < RS[0], M[0] * (r / RS[0]) ** 3, np.interp(np.log(np.maximum(r, RS[0])), np.log(RS), M))
FOOTS = ("canonical", "alt")


def chi2_kz(K):
    return float(np.sum(((K - BR_K) / BR_E5) ** 2))


def chi2_rc(v):
    return float(np.sum(((v - EIL_V) / EIL_E) ** 2))


def expfit(Rv, K, e):
    def r(x):
        return (x[0] * np.exp(-(Rv - R0) / x[1]) - K) / e
    f = least_squares(r, x0=[70, 2.7])
    return f.x


class Base:
    """Newtonian baryon field of one model (amplitude 1) on the grid."""

    def __init__(self, name, fun):
        self.name = name
        self.rho = fun(GR.RR, GR.ZZ)
        self.Mb = 2 * np.sum(2 * math.pi * self.rho * GR.VOL)
        self.pR, self.pZ = phi_kepler(self.Mb, GR.rbR), phi_kepler(self.Mb, GR.rbZ)
        self.Phi = GR.poisson(self.rho, self.pR, self.pZ)
        self.m = Model("N_" + name, GR, self.Phi, self.pR, self.pZ, None)
        self.Menc = flux_mass(self.m.gRz, RS)            # 3-D spherical enclosed baryon mass (Gauss flux), amplitude 1
        dR, dz = GR.grad(self.Phi, self.pR, self.pZ)
        self.gmag = np.hypot(dR, dz)
        # in-plane Newtonian radial field on the RS table (amplitude 1)
        Rq = np.clip(RS, GR.Rc[0], GR.Rc[-1])
        self.gNplane = self.m.gRz(Rq, np.full_like(Rq, GR.zc[0]))[0]

    def KzN(self, R, z):
        return self.m.Kz(R, z)

    def vN2(self, R):
        return R * self.m.gRz(R, np.full_like(R, GR.zc[0]))[0]


# ------------------------------------------------------------------ models
class FieldModel:
    """total field = A * Newtonian baryons + a cold part given either as a spherical M_cold(<r) table or a grid field."""

    def __init__(self, base, A, Mcold=None, gridmodel=None):
        self.b, self.A, self.Mcold, self.gm = base, A, Mcold, gridmodel

    def gRz(self, R, z):
        R = np.asarray(R, float); z = np.asarray(z, float)
        if self.gm is not None:                          # PD: full grid solution (contains baryons)
            return self.gm.gRz(R, z)
        dR, dz = self.b.m.gRz(R, z)
        dR, dz = self.A * dR, self.A * dz
        r = np.sqrt(R ** 2 + z ** 2)
        if self.Mcold is not None:
            if callable(self.Mcold):                     # homeoid grid model of the cold part only
                cR, cz = self.Mcold(R, z)
            else:
                M = Mtab(self.Mcold, r)
                gr = G * M / r ** 2
                cR, cz = gr * R / r, gr * np.abs(z) / r
            dR, dz = dR + cR, dz + cz
        return dR, dz

    def vc(self, R):
        R = np.asarray(R, float)
        return np.sqrt(np.maximum(R * self.gRz(R, np.full_like(R, GR.zc[0]))[0], 0))

    def Kz(self, R, z):
        return self.gRz(R, z)[1]


def build_PD(base, A, foot):
    a0 = A0[foot]
    rho_b = A * base.rho; Mb = A * base.Mb
    PhiN = A * base.Phi; pNR, pNZ = A * base.pR, A * base.pZ
    dR, dz = GR.grad(PhiN, pNR, pNZ)
    nu_c = nu_mono(np.hypot(dR, dz) / a0)
    rho_ph = GR.phantom_source(PhiN, pNR, pNZ, nu_c)
    pbR, pbZ = phi_qumond_sph(Mb, a0, GR.rbR), phi_qumond_sph(Mb, a0, GR.rbZ)
    Phi = GR.poisson(rho_b + rho_ph, pbR, pbZ)
    m = Model("PD", GR, Phi, pbR, pbZ, rho_ph)
    return FieldModel(base, A, gridmodel=m), rho_ph


def Mcold_phi(base, A, foot):
    """enclosed phantom mass = Gauss flux mass of the full QUMOND field minus that of the (scaled) baryons."""
    pd, rho_ph = build_PD(base, A, foot)
    return flux_mass(pd.gm.gRz, RS) - A * base.Menc, rho_ph


def Mcold_v(base, A, foot):
    a0 = A0[foot]
    gN = A * base.gNplane
    vlaw2 = RS * nu_mono(np.abs(gN) / a0) * np.abs(gN)
    return RS * vlaw2 / G - A * base.Menc


def homeoid_field(Mc, q=Q_MUT, mmax=300.0):
    """oblate homeoid rho(m), m^2 = R^2 + z^2/q^2, with mass inside m = Mc(<m); truncated at mmax (homeoid shells beyond
    exert no force inside, Newton's homeoid theorem); Poisson solve on the grid; returns a gRz function."""
    rr = RS[RS <= mmax]; Mm = Mc[RS <= mmax]
    dM = np.gradient(Mm, rr)
    rho_m = dM / (4 * math.pi * q * rr ** 2)
    m_cells = np.sqrt(GR.RR ** 2 + (GR.ZZ / q) ** 2)
    rho = np.where(m_cells <= mmax, np.interp(m_cells, rr, rho_m), 0.0)
    Mtot = 2 * np.sum(2 * math.pi * rho * GR.VOL)
    pR, pZ = phi_kepler(Mtot, GR.rbR), phi_kepler(Mtot, GR.rbZ)
    Phi = GR.poisson(rho, pR, pZ)
    mm = Model("homeoid", GR, Phi, pR, pZ, None)
    Mgrid = np.array([2 * np.sum(2 * math.pi * rho * GR.VOL * (m_cells <= mc)) for mc in (5.0, 20.0, 100.0)])
    return (lambda R, z: mm.gRz(R, z)), float(Mtot), Mgrid, rho


def fitA(make_v):
    res = minimize_scalar(lambda A: chi2_rc(make_v(A)), bounds=(0.6, 2.5), method="bounded", options=dict(xatol=2e-3))
    return float(res.x)


# ------------------------------------------------------------------ controls
P("\n--- controls")
b1 = Base("B1_McMillan17", rho_mcm)
check(abs(b1.Mb / 6.64e10 - 1) < 0.02, f"C1 B1 grid baryon mass {b1.Mb:.4e} matches CFG514's 6.64e10 to 2%")
for foot in FOOTS:
    pd, rph = build_PD(b1, 1.0, foot)
    Mphi, _ = Mcold_phi(b1, 1.0, foot)
    rr = np.array([5.0, 10.0, 20.0, 50.0])
    # flux-enclosed mass of PD minus baryons vs the shell sum of the phantom
    Mflux = pd.gm.M_enclosed(rr) - b1.m.M_enclosed(rr)
    dev = np.max(np.abs(Mtab(Mphi, rr) / Mflux - 1))
    Mcell = GR.enclosed(rph, rr)
    devc = np.max(np.abs(Mcell / Mflux - 1))
    check(devc < 0.01, f"C2b [{foot}] phantom cell sum (CFG514 MUTATE's shell average) vs Gauss flux mass, 5-50 kpc: max dev {devc:.2%} (< 1%)")
    check(dev < 0.01, f"C2 [{foot}] RM-phi enclosed phantom (Gauss flux) vs PD Gauss flux mass, 5-50 kpc: max dev {dev:.2%} (< 1%)")
# C3 homeoid with q = 1 must equal the spherical field
Mtest = Mcold_v(b1, 1.0, "canonical")
fh, _, _, _ = homeoid_field(Mtest, q=1.0)
Rt = np.array([4.0, 8.122, 12.0]); zt = np.full(3, 1.1)
Ksph = FieldModel(b1, 1.0, Mcold=Mtest).Kz(Rt, zt) - b1.KzN(Rt, zt)
Kh = fh(Rt, zt)[1]
dev = np.max(np.abs(Kh / Ksph - 1))
check(dev < 0.02, f"C3 homeoid solver at q = 1 reproduces the spherical cold K_z at |z| = 1.1: max dev {dev:.2%} (< 2%)")

# ------------------------------------------------------------------ main loop
RESULTS = dict(mutate=MUTATE, models={}, cells=[], data={})
(dK0, dh) = expfit(BR_R, BR_K, BR_E5)
RESULTS["data"] = dict(K0=float(dK0), h=float(dh))
P(f"\n  data: exponential refit K0 = {dK0:.1f}, h = {dh:.2f} kpc (Bovy & Rix 43 MAPs, sigma (+) 5%)")
ZB = np.full_like(BR_R, 1.1)
cells = []
for bname, fun in BARYONS.items():
    t1 = time.time()
    base = b1 if bname == "B1_McMillan17" else Base(bname, fun)
    P("\n" + "=" * 110 + f"\n{bname}: M_b = {base.Mb:.3e} Msun, Newtonian v_c(R0) = {math.sqrt(base.vN2(np.array([R0]))[0]):.1f} km/s, "
      f"K_z,N(R0,1.1) = {base.KzN(np.array([R0]), np.array([1.1]))[0] / KZ_UNIT:.1f}\n" + "=" * 110)
    # NFW rival at A = 1
    def nfw_v(x, base=base):
        p = nfw_params(10 ** x[0], x[1])
        return np.sqrt(np.maximum(base.vN2(EIL_R) + EIL_R * nfw_g(p, EIL_R), 0))
    fN = least_squares(lambda x: (nfw_v(x) - EIL_V) / EIL_E, x0=[12.0, 10.0], bounds=([11.0, 1.0], [13.3, 40.0]))
    pN = nfw_params(10 ** fN.x[0], fN.x[1])
    rB = np.sqrt(BR_R ** 2 + 1.1 ** 2)
    KN = (base.KzN(BR_R, ZB) + nfw_g(pN, rB) * 1.1 / rB) / KZ_UNIT
    c2N = chi2_kz(KN); hN = expfit(BR_R, KN, BR_E5)[1]
    KNR0 = float((base.KzN(np.array([R0]), np.array([1.1]))[0] + nfw_g(pN, math.hypot(R0, 1.1)) * 1.1 / math.hypot(R0, 1.1)) / KZ_UNIT)
    P(f"  N (NFW): log M200 = {fN.x[0]:.3f}, c = {fN.x[1]:.2f}, chi2_RC = {np.sum(fN.fun**2):.1f}; K_z chi2 = {c2N:.1f}, K(R0) = {KNR0:.1f}, h = {hN:.2f}")
    RESULTS["models"][bname] = dict(Mb=base.Mb, N=dict(logM200=float(fN.x[0]), c=float(fN.x[1]), chi2_rc=float(np.sum(fN.fun ** 2)),
                                                      chi2_kz=c2N, K_R0=KNR0, h=float(hN)))
    P(f"  {'foot':<10}{'var':<4}{'model':<7}{'A':>7}{'chi2_RC':>9}{'vc(R0)':>8}{'K(R0)':>8}{'h':>6}{'chi2_Kz':>9}{'d vs N':>9}{'negM%':>7}")
    for foot in FOOTS:
        for var in ("F0", "FA"):
            row = {}
            # PD
            if var == "F0":
                A_pd = 1.0
            else:
                A_pd = fitA(lambda A: build_PD(base, A, foot)[0].vc(EIL_R))
            pd, _ = build_PD(base, A_pd, foot)
            # RM-phi
            def mk_phi(A):
                return FieldModel(base, A, Mcold=Mcold_phi(base, A, foot)[0])
            def mk_v(A):
                return FieldModel(base, A, Mcold=Mcold_v(base, A, foot))
            A_phi = 1.0 if var == "F0" else fitA(lambda A: mk_phi(A).vc(EIL_R))
            A_v = 1.0 if var == "F0" else fitA(lambda A: mk_v(A).vc(EIL_R))
            mods = {"PD": (pd, A_pd), "RMphi": (mk_phi(A_phi), A_phi), "RMv": (mk_v(A_v), A_v)}
            for key in ("RMphi", "RMv"):
                fm = mods[key][0]
                Mc = fm.Mcold
                dM = np.diff(Mc); rmask = RS[1:] <= 30.0       # negative cold density = M_cold decreasing
                negfrac = float(-np.sum(np.minimum(dM, 0)[rmask]) / max(np.sum(np.abs(dM)[rmask]), 1e-30))
                row[key + "_negfrac"] = negfrac
                if MUTATE:
                    fh, Mt, Mg, _ = homeoid_field(Mc, q=Q_MUT)
                    rcheck = np.array([5.0, 20.0, 100.0])
                    row[key + "_mut_massdev"] = float(np.max(np.abs(Mg / Mtab(Mc, rcheck) - 1)))
                    mods[key + "_MUT"] = (FieldModel(base, mods[key][1], Mcold=fh), mods[key][1])
            for key, (fm, A) in mods.items():
                K = fm.Kz(BR_R, ZB) / KZ_UNIT
                c2 = chi2_kz(K); h = expfit(BR_R, K, BR_E5)[1]
                vR0 = float(fm.vc(np.array([R0]))[0]); KR0 = float(fm.Kz(np.array([R0]), np.array([1.1]))[0] / KZ_UNIT)
                crc = chi2_rc(fm.vc(EIL_R))
                row[key] = dict(A=A, chi2_kz=c2, chi2_rc=crc, vc_R0=vR0, K_R0=KR0, h=float(h), d_vs_N=c2 - c2N)
                neg = row.get(key + "_negfrac", float("nan"))
                P(f"  {foot:<10}{var:<4}{key:<9}{A:>5.3f}{crc:>9.1f}{vR0:>8.1f}{KR0:>8.1f}{h:>6.2f}{c2:>9.1f}{c2 - c2N:>+9.1f}"
                  + (f"{100*neg:>7.2f}" if key in ("RMphi", "RMv") else ""))
            for key in ("RMphi", "RMv"):
                d = row[key]["chi2_kz"] - row["PD"]["chi2_kz"]
                cell = dict(baryon=bname, foot=foot, var=var, rm=key, d_RM_minus_PD=d, beats=bool(d <= -4),
                            d_RM_vs_N=row[key]["d_vs_N"], d_PD_vs_N=row["PD"]["d_vs_N"], negfrac=row[key + "_negfrac"])
                if MUTATE:
                    dm = row[key + "_MUT"]["chi2_kz"] - row[key]["chi2_kz"]
                    cell.update(d_MUT_minus_RM=dm, mut_reproduces=bool(dm >= 4), mut_massdev=row[key + "_mut_massdev"])
                cells.append(cell)
            RESULTS["models"][bname][f"{foot}_{var}"] = row
    P(f"  ({time.time() - t1:.0f} s)")

# ------------------------------------------------------------------ verdict table
P("\n" + "=" * 110 + "\nCELL TABLE: dchi2(RM - PD) on K_z,1.1 (round beats disc if <= -4)" + ("; MUTATE dchi2(homeoid - RM) (reproduces if >= +4)" if MUTATE else "") + "\n" + "=" * 110)
for c in cells:
    s = (f"  {c['baryon']:<20}{c['foot']:<10}{c['var']:<4}{c['rm']:<7} RM-PD {c['d_RM_minus_PD']:>+8.1f}  {'BEATS' if c['beats'] else 'no   '}"
         f"   RM vs N {c['d_RM_vs_N']:>+7.1f}   PD vs N {c['d_PD_vs_N']:>+7.1f}   neg {100*c['negfrac']:.2f}%")
    if MUTATE:
        s += f"   MUT-RM {c['d_MUT_minus_RM']:>+7.1f} {'REPRO' if c['mut_reproduces'] else 'NOT'}  (M dev {c['mut_massdev']:.1e})"
    P(s)
RESULTS["cells"] = cells
for rm in ("RMphi", "RMv"):
    sub = [c for c in cells if c["rm"] == rm]
    nb = sum(c["beats"] for c in sub)
    P(f"  {rm}: round beats disc in {nb}/{len(sub)} cells; RM within +4 of NFW in {sum(c['d_RM_vs_N'] <= 4 for c in sub)}/{len(sub)}")
    RESULTS[f"summary_{rm}"] = dict(beats=nb, n=len(sub), fail_cells=[f"{c['baryon']}/{c['foot']}/{c['var']}" for c in sub if not c["beats"]])
if MUTATE:
    allrep = all(c["mut_reproduces"] for c in cells if c["beats"])
    P(f"  MUTATE: homeoid reproduces the rejection in {sum(c['mut_reproduces'] for c in cells if c['beats'])}/{sum(c['beats'] for c in cells)} "
      f"counted cells (and {sum(c['mut_reproduces'] for c in cells)}/{len(cells)} overall) -> {'DETECTED' if allrep else 'NOT DETECTED'}")
    RESULTS["mutate_detected"] = bool(allrep)
    mdev = max(c["mut_massdev"] for c in cells)
    check(mdev < 0.02, f"M1 homeoid enclosed-mass on grid vs RM's M(<m) at 5/20/100 kpc: max dev {mdev:.2%} (< 2%) [homeoid cells inside m vs the spherical M(<r) table at r = m; cell-edge discreteness]")

RESULTS["checks"] = [dict(ok=o, msg=m) for o, m in CHECKS]
RESULTS["runtime_s"] = time.time() - T0
P(f"\nchecks: {sum(o for o, _ in CHECKS)}/{len(CHECKS)} pass; runtime {time.time() - T0:.0f} s")


def jc(o):
    if isinstance(o, dict):
        return {k: jc(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jc(v) for v in o]
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.bool_):
        return bool(o)
    return o


json.dump(jc(RESULTS), open(os.path.join(HERE, f"cfg516_mw_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg516_mw{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if MUTATE:
    sys.exit(1 if RESULTS["mutate_detected"] else 0)

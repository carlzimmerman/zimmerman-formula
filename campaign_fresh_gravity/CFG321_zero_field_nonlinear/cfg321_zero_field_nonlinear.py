#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG321 -- RECIPE G5/G10 ON THE UNGATED CHASSIS: does the nonlinear system regularise the Hadamard instability of its own
zero-field (FRW) background?

THE QUESTION.  FP5 G-2f (a26136bc4) C3: at an open zero-field region (grad U ~ 0 -- the ungated C-H/K chassis's own FRW
background) the linearisation is BPS khronometric gravity with alpha_eff = 2 + alpha_c > 2: omega^2 < 0 at every k,
growth proportional to k, Hadamard ill-posed.  C4 (reported only) said the band is bounded below y* and saturates at
y ~ y*.  CFG294 proved conditional local well-posedness only AWAY from zero-field regions (its C3/A5).  Does the
nonlinear system reach a regular saturated state that depends continuously on the data, or do solutions branch, blow up
or depend discontinuously on the data?  Criteria frozen first: FROZEN_CRITERIA.md (commit cb089fb29).

PARTS
  A  C-SYM: the scalar block rebuilt from the action (FP5's ADM machinery, copied, not imported), the shift and lapse
     eliminated, U kept: the reduced system, its exact map to the dimensionless form with one stiffness parameter
     eps = alpha^2/(4 - alpha^2), and its energy functional.
  B  C-FP5: FP5 C4's band and rates reproduced; C-BKG (reported): the FRW + Lambda + dust scale separation.
  C  C-LIN: the nonlinear code linearised about a uniform field reproduces the rates (1-D: C_L; 2-D: C_T).
  D  C-GR: the MOND sector off (GR + healthy BPS khronon): convergence, energy, pairs.
  E  the nonlinear runs (1+1 and 2+1, three resolutions, the eps ladder, pairs), parallel.
  F  R1-R4, FAIL signatures, verdict; the saturated state (y distribution, energy in physical units).
MUTATE (CFG321_MUTATE=1): the record's turning kernel mu_exp, a0 -> y* a0; must NOT return CONDITIONAL (rc = 1).

Large work arrays go to ../_external_data/cfg321_work/ (outside git, relative to the repository root).
Run from the repository root:  python3 campaign_fresh_gravity/CFG321_zero_field_nonlinear/cfg321_zero_field_nonlinear.py
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, json, math, time, warnings
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")   # spurious macOS BLAS flags; results finite (checked)
import numpy as np
import sympy as sp
from multiprocessing import get_context

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import cfg321_engine as EN

MUTATE = os.environ.get("CFG321_MUTATE", "0") == "1"
SLUG = "cfg321_zero_field_nonlinear" + ("_MUTATE" if MUTATE else "")
EXT = os.path.join(os.path.dirname(REPO), "_external_data", "cfg321_work" + ("_MUTATE" if MUTATE else ""))
NPROC = int(os.environ.get("CFG321_NPROC", "14"))
OUT = {"lane": "CFG321", "gate": "recipe G5/G10", "mutate": MUTATE, "frozen": "cb089fb29", "checks": {}, "numbers": {}}
CH = []
T0 = time.time()


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 112 + "\n" + t + "\n" + "=" * 112)


def check(name, measured, ok, load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}")
    return ok


def jread(rel):
    return json.load(open(os.path.join(REPO, rel)))


P(__doc__.split("PARTS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: kernel -> mu_exp (a0 -> y* a0); the verdict must NOT be CONDITIONAL ***")

# ------------------------------------------------------------------------------------------------- committed inputs
j340 = jread("real_research/g03_audit_2026/L340_filtered_khronon_completion_results.json")
jfp5 = jread("real_research/derivation_chain_2026/FP5_dof_and_a0_field_results.json")
A_MAX = float(j340["numbers"]["P1"]["alpha_c_max"]); A_MIN = float(j340["numbers"]["P1"]["alpha_c_min"])
C2_TOP = float(j340["numbers"]["P1"]["c2_max"])
XI_PC = float(j340["numbers"]["S1"]["canonical/nu_mono"]["xi_M"])
c_SI, G_SI = 299792458.0, 6.67430e-11
PC, YR, MPC = 3.0856775814913673e16, 3.15576e7, 3.0856775814913673e22
H0 = 67.36e3 / MPC; OM_L = 0.6847
RHO_L = OM_L * 3 * H0 ** 2 / (8 * math.pi * G_SI)
A0 = {"canonical": 0.5 * c_SI * math.sqrt(G_SI * RHO_L), "alt": 0.5 * c_SI * math.sqrt(G_SI * RHO_L / OM_L)}
P(f"\n  inputs: alpha_c window [{A_MIN:.4e}, {A_MAX:.4e}] (L340 P1), c_2 corner {C2_TOP:.4f}, xi = {XI_PC:.5f} pc (L340 S1); "
  f"a0 = {A0['canonical']:.4e} (canonical) / {A0['alt']:.4e} (alt) m/s^2; kappa = 1/2 FITTED (plays no role)")

# ================================================================================================= PART A
banner("PART A  C-SYM: the reduced system from the action (FP5 scalar block, shift + lapse eliminated, U per leaf)")
# ----- FP5's ADM machinery, copied verbatim from real_research/derivation_chain_2026/FP5_dof_and_a0_field.py (lines 183-261) -----
t, z = sp.symbols('t z', real=True)
eps = sp.Symbol('epsilon')
w, k = sp.symbols('omega k', positive=True)
xiB, lamB, eta, cCH, Cs, c2, ac = sp.symbols('xi_B lambda_B eta c_CH C c_2 alpha_c', real=True)
dz = sp.Symbol('Delta_z', positive=True)


def Fn(n):
    return sp.Function(n)(t, z)


hp, hc, hs, Hxz, Hyz, Hzz = (Fn(q) for q in ('hp', 'hc', 'hs', 'Hxz', 'Hyz', 'Hzz'))
phi, nx, ny, nzf, u = (Fn(q) for q in ('phi', 'nx', 'ny', 'nz', 'u'))
BASE = [hp, hc, Hxz, Hyz, Hzz, hs, phi, nx, ny, nzf, u]
BASEN = ['hp', 'hc', 'Hxz', 'Hyz', 'Hzz', 'hs', 'phi', 'nx', 'ny', 'nz', 'u']


def tr(e, n=2):
    e = sp.expand(e)
    return sum(e.coeff(eps, i) * eps ** i for i in range(n + 1))


def adm_L2():
    """Second-order unitary-gauge ADM Lagrangian of  N sqrt(h)[xi_B R3 + K_ij K^ij - lambda_B K^2 + eta a^2 + c_CH |DU - a|^2]
    around flat space, fields depending on (t, z) (k along z)."""
    H = sp.Matrix([[hs + hp, hc, Hxz], [hc, hs - hp, Hyz], [Hxz, Hyz, Hzz]])
    h = sp.eye(3) + eps * H
    hinv = (sp.eye(3) - eps * H + eps ** 2 * H * H).applyfunc(tr)
    trH, trH2 = H.trace(), (H * H).trace()
    sqrth = 1 + eps * trH / 2 + eps ** 2 * (trH ** 2 / 8 - trH2 / 4)
    N = 1 + eps * phi
    invN = 1 - eps * phi + eps ** 2 * phi ** 2
    Nup = sp.Matrix([nx, ny, nzf]) * eps
    Ndn = (h * Nup).applyfunc(tr)
    d = lambda e, i: 0 if i < 2 else sp.diff(e, z)
    Gam = [[[tr(sum(hinv[kk, l] * (d(h[l, j], i) + d(h[l, i], j) - d(h[i, j], l)) for l in range(3)) / 2)
             for j in range(3)] for i in range(3)] for kk in range(3)]
    DN = sp.Matrix(3, 3, lambda i, j: tr(d(Ndn[j], i) - sum(Gam[kk][i][j] * Ndn[kk] for kk in range(3))))
    Kij = sp.Matrix(3, 3, lambda i, j: tr((sp.diff(h[i, j], t) - DN[i, j] - DN[j, i]) * invN / 2))
    Kup = (hinv * Kij * hinv).applyfunc(tr)
    KK = tr(sum(Kij[i, j] * Kup[i, j] for i in range(3) for j in range(3)))
    Ktr = tr(sum(hinv[i, j] * Kij[i, j] for i in range(3) for j in range(3)))

    def Ric(i, j):
        e = sum(d(Gam[kk][i][j], kk) for kk in range(3)) - sum(d(Gam[kk][i][kk], j) for kk in range(3))
        e += sum(Gam[kk][kk][l] * Gam[l][i][j] for kk in range(3) for l in range(3))
        e -= sum(Gam[kk][j][l] * Gam[l][i][kk] for kk in range(3) for l in range(3))
        return tr(e)
    R3 = tr(sum(hinv[i, j] * Ric(i, j) for i in range(3) for j in range(3)))
    lnN = eps * phi - eps ** 2 * phi ** 2 / 2
    az = sp.diff(lnN, z)
    a2 = tr(hinv[2, 2] * az ** 2)
    CHt = tr(hinv[2, 2] * (eps * sp.diff(u, z) - az) ** 2)
    Lg = tr(N * sqrth * (xiB * R3 + KK - lamB * Ktr ** 2 + eta * a2 + cCH * CHt))
    return Lg.coeff(eps, 1), Lg.coeff(eps, 2)


def fourier_matrix(L2, fields):
    """Hermitian M(w,k) of the quadratic action S2 = Int X^dagger M X for plane waves exp(i(kz - wt)); total derivatives drop."""
    L2 = sp.expand(L2)
    atoms = {}
    for a in L2.atoms(sp.Derivative):
        atoms[a] = (a.expr, sum(cn for v, cn in a.variable_count if v == t), sum(cn for v, cn in a.variable_count if v == z))
    for f in fields:
        atoms[f] = (f, 0, 0)
    items = list(atoms.items())
    syms = [sp.Symbol(f'S{i}') for i in range(len(items))]
    rep = {a: s for (a, _), s in zip(items, syms)}
    Ls = sp.expand(L2.xreplace({a: rep[a] for a in sorted(rep, key=lambda q: -sp.count_ops(q))}))
    idx = {f: i for i, f in enumerate(fields)}
    M = sp.zeros(len(fields), len(fields))
    fac = lambda nt, nzz: (-sp.I * w) ** nt * (sp.I * k) ** nzz
    for mon, cf in sp.Poly(Ls, *syms).terms():
        ids = [i for i, e in enumerate(mon) for _ in range(e)]
        if len(ids) != 2:
            raise ValueError("non-quadratic term in L2")
        (fa, ta, za), (fb, tb, zb) = items[ids[0]][1], items[ids[1]][1]
        M[idx[fb], idx[fa]] += cf * fac(ta, za) * sp.conjugate(fac(tb, zb))
    return ((M + M.H) / 2).applyfunc(sp.expand)

# ----- end of the copied block -----

P("  building the second-order ADM Lagrangian from the action (FP5's adm_L2, copied verbatim above) ...")
L1, L2 = adm_L2()
M_base = fourier_matrix(L2, BASE)
KEEP = [i for i, nm in enumerate(BASEN) if nm not in ('Hxz', 'Hyz', 'Hzz')]          # FP5's complete gauge fixing
Mg = M_base.extract(KEEP, KEEP); NG = [BASEN[i] for i in KEEP]
SCAL = ['hs', 'phi', 'nz', 'u']
MS0 = Mg.extract([NG.index(q) for q in SCAL], [NG.index(q) for q in SCAL])
Csym = sp.Symbol('C', positive=True)
al = sp.Symbol('alpha', positive=True)
MS = MS0.subs({xiB: 1, lamB: 1 + c2, eta: al, cCH: 2})
MS[3, 3] += 2 * Csym * k ** 2                                                         # the MOND tangent on U (filter absorbed, FP5 B2)
P(f"  scalar block (hs, phi, n_z, u), chassis values: {MS.applyfunc(sp.factor)}")
# the lapse equation (row phi) solved for phi: elliptic (k^2 phi coefficient alpha + 2 > 0)
hs_, phi_, nz_, u_ = sp.symbols('hs_ phi_ nz_ u_')
X = sp.Matrix([hs_, phi_, nz_, u_])
rows = MS * X
phi_sol = sp.solve(rows[1], phi_)[0]
nz_sol = sp.solve(rows[2], nz_)[0]
lapse_ok = sp.simplify(phi_sol - (2 * u_ - hs_) / (2 + al)) == 0
P(f"  lapse equation -> phi = {sp.factor(phi_sol)};  momentum constraint -> n_z = {sp.factor(nz_sol)}")
# Schur reduction onto (hs, u)
ik, ie = [0, 3], [1, 2]
Mred = (MS.extract(ik, ik) - MS.extract(ik, ie) * MS.extract(ie, ie).inv() * MS.extract(ie, ik)).applyfunc(sp.simplify)
Kk = (2 + 3 * c2) / (2 * c2)
Mred_pred = sp.Matrix([[Kk * w ** 2 + al * k ** 2 / (2 * (2 + al)), 2 * k ** 2 / (2 + al)],
                       [2 * k ** 2 / (2 + al), 2 * al * k ** 2 / (2 + al) + 2 * Csym * k ** 2]])
red_ok = (Mred - Mred_pred).applyfunc(sp.simplify) == sp.zeros(2, 2)
P(f"  reduced (hs, u) block = {Mred.applyfunc(sp.factor)}")
P("  i.e.  K hs_tt = -(alpha/(2(2+alpha))) Lap hs - (2/(2+alpha)) Lap u,   u = argmin of the leaf functional,  K = (2+3c_2)/(2c_2)")
# dispersion vs FP5 B3
W2 = sp.Symbol('W2')
disp = sp.solve(sp.factor(Mred.det()).subs(w, sp.sqrt(W2)), W2)
E_C = al + 2 * Csym * 2 / (2 + 2 * Csym)
b3 = c2 * (2 - E_C) * k ** 2 / (E_C * (2 + 3 * c2))
b3_ok = len(disp) == 1 and sp.simplify(disp[0] - b3) == 0
# the GR (C -> 0) and zero-field (C -> oo) ends
cs2 = sp.simplify(disp[0].subs(Csym, 0) / k ** 2)
zf = sp.simplify(sp.limit(disp[0] / k ** 2, Csym, sp.oo))
ends_ok = (sp.simplify(cs2 - c2 * (2 - al) / (al * (2 + 3 * c2))) == 0
           and sp.simplify(zf + c2 * al / ((2 + al) * (2 + 3 * c2))) == 0)
# the dimensionless map: x = C/C*, eps = alpha^2/(4 - alpha^2), omega = s * omega_hat, s^2 = c_2 alpha/((2+alpha)(2+3c_2))
xs, epsS = sp.symbols('x varepsilon', positive=True)
Cst = (2 - al) / al
eps_al = al ** 2 / (4 - al ** 2)
s2 = c2 * al / ((2 + al) * (2 + 3 * c2))
lane_disp = ((1 + epsS) / (xs + epsS) - 1) * k ** 2
map_ok = sp.simplify(disp[0].subs(Csym, Cst * xs) / s2 - lane_disp.subs(epsS, eps_al)) == 0
# field map: u/hs ratio, physical vs lane (u_hat = psi_tilde/(x + eps)); hs = -a psi_tilde, u = b u_hat, a/b constant
ratio_phys = sp.solve(Mred[1, 0] * hs_ + Mred[1, 1] * u_, u_)[0] / hs_          # u/hs
a_over_b = sp.simplify(-1 / (ratio_phys.subs(Csym, Cst * xs) * (xs + eps_al)))
field_ok = sp.simplify(sp.diff(a_over_b, xs)) == 0 and sp.simplify(a_over_b - al * (4 / al ** 2 - 1)) == 0
# energy functional (linear): V_k = -k^2 psi^2 - (1+eps) min_u [(x+eps)k^2 u^2 - 2 k^2 psi u]  ->  omega_hat^2 coefficient
uu, pp = sp.symbols('uu pp', real=True)
Fq = (xs + epsS) * k ** 2 * uu ** 2 - 2 * k ** 2 * pp * uu
umin = sp.solve(sp.diff(Fq, uu), uu)[0]
Vk = -k ** 2 * pp ** 2 - (1 + epsS) * Fq.subs(uu, umin)
energy_ok = sp.simplify(Vk / pp ** 2 - lane_disp) == 0
OUT["numbers"]["A"] = {"phi": str(phi_sol), "n_z": str(nz_sol), "Mred": str(Mred), "omega2": str(disp),
                       "cS2": str(cs2), "zero_field": str(zf), "a_over_b": str(a_over_b)}
check("C-SYM the scalar block rebuilt from the action reduces (momentum constraint for n_z, the elliptic lapse equation "
      "phi = (2u - hs)/(2 + alpha)) to K hs_tt = -(alpha/(2(2+alpha))) Lap hs - (2/(2+alpha)) Lap u with U per leaf; its "
      "dispersion equals FP5 B3 exactly (C -> 0: the healthy c_S^2 of CFG294; C -> oo: FP5 C3's -c_2 alpha/((2+alpha)(2+3c_2))); "
      "the dimensionless map (x = C/C*, eps = alpha^2/(4 - alpha^2), slow time) is exact, the field map constant "
      "(a/b = alpha(Lambda - 1)), and the energy functional reproduces V_k = k^2 psi^2((1+eps)/(x+eps) - 1)",
      f"lapse {lapse_ok}; reduced block {red_ok}; B3 {b3_ok}; ends {ends_ok} (c_S^2 = {cs2}, zero field {zf}); map {map_ok}; "
      f"field map {field_ok} ({a_over_b}); energy {energy_ok}",
      lapse_ok and red_ok and b3_ok and ends_ok and map_ok and field_ok and energy_ok)

EPS_PHYS = A_MAX ** 2 / (4 - A_MAX ** 2)
S_TIME = math.sqrt(C2_TOP * A_MAX / ((2 + A_MAX) * (2 + 3 * C2_TOP)))
TAU_UNIT_S = (XI_PC * PC / c_SI) / S_TIME
P(f"  physical eps = {EPS_PHYS:.4e} (alpha_max) / {A_MIN ** 2 / 4:.3e} (alpha_min); slow-time unit = {TAU_UNIT_S:.3e} s = "
  f"{TAU_UNIT_S / YR:.3e} yr (c_2 = {C2_TOP:.4f}, xi = {XI_PC:.4f} pc)")
OUT["numbers"]["units"] = {"eps_phys": EPS_PHYS, "tau_unit_yr": TAU_UNIT_S / YR}

# ================================================================================================= PART B
banner("PART B  C-FP5: FP5 C4's band and rates from this lane's kernel; C-BKG (reported): FRW + Lambda + dust")
KN = EN.NuMonoKernel(A_MAX)
ys_fp5 = float(jfp5["numbers"]["C1"]["alpha_c max (L340 P1)|T"])
P(f"  y*_T (this lane, closed form log1p(1/C*)^2) = {KN.ystar:.6e}; FP5 C1 = {ys_fp5:.6e}")
rows_b = []
for (m_, yv, kx_f, g_f, tau_f) in jfp5["numbers"]["C4"]:
    y = KN.ystar * 10 ** (-m_)
    C0 = 1.0 / math.expm1(math.sqrt(y))                                     # C_T(y) = h_RAR/y below the splice
    kmax = math.sqrt(math.log(C0 / KN.Cstar))
    kx = np.linspace(1e-3, kmax, 400)
    Ek = A_MAX + 2 * C0 * np.exp(-kx ** 2) / (1 + C0 * np.exp(-kx ** 2))
    gam = kx * np.sqrt(np.clip(C2_TOP * (Ek - 2) / (Ek * (2 + 3 * C2_TOP)), 0, None))
    # the same rate from the lane's dimensionless form at the physical eps
    xg = C0 * np.exp(-kx ** 2) / KN.Cstar
    gl = kx * np.sqrt(np.clip(1 - (1 + EPS_PHYS) / (xg + EPS_PHYS), 0, None)) * S_TIME
    tau = (XI_PC * PC / c_SI) / gam.max() / YR
    rows_b.append((m_, kmax, kx_f, gam.max(), g_f, tau, tau_f, gl.max()))
    P(f"    y = y*/1e{m_:<2d}: k_max xi = {kmax:.4f} (FP5 {kx_f:.4f}); max growth {gam.max():.4e} c/xi (FP5 {g_f:.4e}; lane form "
      f"{gl.max():.4e}); e-fold {tau:.4e} yr (FP5 {tau_f:.4e})")
fp5_ok = (abs(KN.ystar / ys_fp5 - 1) < 1e-3
          and all(abs(r[1] / r[2] - 1) < 0.01 and abs(r[3] / r[4] - 1) < 0.01 and abs(r[5] / r[6] - 1) < 0.01
                  and abs(r[7] / r[3] - 1) < 1e-6 for r in rows_b))
check("C-FP5 FP5 C4's three rows (k_max xi = sqrt(ln(C/C*)), max growth, e-fold at the fastest corner) and y*_T are "
      "reproduced from this lane's kernel; the lane's dimensionless rate at the physical eps equals FP5's formula",
      f"y* ratio {KN.ystar / ys_fp5:.6f}; rows (k_max, growth, e-fold ratios, lane/FP5): "
      + "; ".join(f"1e{r[0]}: {r[1] / r[2]:.5f}, {r[3] / r[4]:.5f}, {r[5] / r[6]:.5f}, {r[7] / r[3]:.8f}" for r in rows_b), fp5_ok)
OUT["numbers"]["B"] = {"ystar": KN.ystar, "rows": rows_b}
# C-BKG
Hxi = H0 * XI_PC * PC / c_SI
k_xi = 1.0 / (XI_PC * PC)
W_frw = -3.18e-52                                      # CFG312 committed: FLRW today, m^-2 (read below if present)
try:
    j312 = jread("campaign_fresh_gravity/CFG312_lapse_condition_W/cfg312_lapse_condition_W_results.json")
    s312 = json.dumps(j312["numbers"])
    import re as _re
    mm = _re.search(r"FLRW[^\]]*?(-3\.1[0-9]*e-52)", s312)
    if mm:
        W_frw = float(mm.group(1))
except Exception:
    pass
P(f"  H0 xi/c = {Hxi:.3e}; |W_FRW|/k^2 at k = 1/xi: {abs(W_frw) / k_xi ** 2:.3e} (CFG312's W = {W_frw:.3e} m^-2); "
  f"slow-time unit / Hubble time = {TAU_UNIT_S * H0:.3e}")
OUT["numbers"]["BKG"] = {"H_xi_over_c": Hxi, "W_over_k2": abs(W_frw) / k_xi ** 2, "tau_unit_H0": TAU_UNIT_S * H0}

# ================================================================================================= workers
KERN_MAIN = "mu_exp" if MUTATE else "nu_mono"
L1D, L2D = 16.0, 8.0
YRMS0 = 1e-4
T1D, T2D = 80.0, 60.0
if os.environ.get("CFG321_SMOKE"):              # development smoke test only (separate outputs)
    T1D, T2D = 12.0, 12.0
    SLUG += "_SMOKE"; EXT += "_SMOKE"


def make_kernel(name):
    return {"nu_mono": EN.NuMonoKernel, "mu_exp": EN.MuExpKernel, "off": EN.ZeroKernel}[name](A_MAX)


def task(spec):
    warnings.filterwarnings("ignore", message=".*encountered in matmul.*")
    kind = spec["kind"]
    t0 = time.time()
    if kind == "lin":
        dim, n, L, eps = spec["dim"], spec["n"], spec["L"], spec["eps"]
        gr = EN.Grid(dim, n, L); K = make_kernel("nu_mono")
        Gb = np.zeros(dim); Gb[0] = 1e-4
        yb = 1e-4
        gb = eps * Gb + K.CT(np.array([yb]))[0] * Gb
        X = gr.coords()
        res = []
        for (axis, m_) in spec["modes"]:
            kk = 2 * np.pi * m_ / L
            u0 = 1e-5 * yb * np.cos(kk * X[axis]) / kk
            psi0 = EN.psi_from_u(gr, K, eps, u0, Gb)
            o = EN.evolve(gr, K, eps, psi0, u0, Gb.copy(), gb, 3.0, dtout=0.02)
            comp = axis
            idx = [0] * dim; idx[axis] = m_
            amp = np.array([np.fft.fftn((sw[comp]).reshape(gr.shape))[tuple(idx)] for sw in o["snaps_w"]])
            amp = np.real(amp * np.conj(amp[0])) / abs(amp[0]) ** 2
            tt = o["snaps_t"]
            Cdir = float(K.CL(np.array([yb]))[0]) if axis == 0 else float(K.CT(np.array([yb]))[0])
            om2 = kk ** 2 * ((1 + eps) / (Cdir * math.exp(-kk ** 2) + eps) - 1)
            # one-parameter least squares on a fine grid (no use of the prediction)
            if om2 < 0:
                cand = np.linspace(1e-3, 4.0, 40001)
                errs = [np.sum((np.cosh(c_ * tt) - amp) ** 2 / np.cosh(c_ * tt) ** 2) for c_ in cand[::100]]
                c0 = cand[::100][int(np.argmin(errs))]
                fine = np.linspace(max(1e-4, c0 - 0.02), c0 + 0.02, 4001)
                errs = [np.sum((np.cosh(c_ * tt) - amp) ** 2 / np.cosh(c_ * tt) ** 2) for c_ in fine]
                meas = float(fine[int(np.argmin(errs))]); pred = math.sqrt(-om2); typ = "growth"
            else:
                cand = np.linspace(1e-3, 60.0, 60001)
                errs = [np.sum((np.cos(c_ * tt) - amp) ** 2) for c_ in cand[::50]]
                c0 = cand[::50][int(np.argmin(errs))]
                fine = np.linspace(max(1e-4, c0 - 0.06), c0 + 0.06, 6001)
                errs = [np.sum((np.cos(c_ * tt) - amp) ** 2) for c_ in fine]
                meas = float(fine[int(np.argmin(errs))]); pred = math.sqrt(om2); typ = "frequency"
            res.append({"axis": axis, "m": m_, "k": kk, "C": Cdir, "type": typ, "measured": meas, "predicted": pred,
                        "edge": math.sqrt(math.log(Cdir)), "status": o["status"]})
        return {"spec": spec, "res": res, "wall": time.time() - t0}
    if kind == "gr":
        n, eps, delta = spec["n"], spec["eps"], spec["delta"]
        gr = EN.Grid(1, n, L1D); K = make_kernel("off")
        psi0, u0, G0, g0 = EN.initial_data(gr, K, eps, 321, YRMS0, delta=delta, seed2=322)
        o = EN.evolve(gr, K, eps, psi0, u0, G0, g0, 10.0)
        # exact solution: psi_k(t) = psi_k(0) cos(k t/sqrt(eps)) (omega^2 = k^2((1+eps)/eps - 1)), u = psi/eps
        Pk0 = gr.fft(psi0)
        om = np.sqrt(gr.k2 * ((1 + eps) / eps - 1))
        errs = []
        for tt, sw in zip(o["snaps_t"], o["snaps_w"]):
            ue = gr.ifft(Pk0 * np.cos(om * tt)) / eps
            we = gr.Bop(ue)
            errs.append(float(np.linalg.norm(sw[0] - we[0]) / np.linalg.norm(we[0])))
        return {"spec": spec, "rec": o["rec"], "snaps_w": o["snaps_w"], "status": o["status"], "err": errs,
                "dt": o["dt"], "wall": time.time() - t0}
    # main
    dim, n, eps, delta, kname = spec["dim"], spec["n"], spec["eps"], spec["delta"], spec["kern"]
    L = L1D if dim == 1 else L2D
    T = T1D if dim == 1 else T2D
    gr = EN.Grid(dim, n, L); K = make_kernel(kname)
    psi0, u0, G0, g0 = EN.initial_data(gr, K, eps, 321, YRMS0, delta=delta, seed2=322)
    nout = int(round(T / 0.25))
    probe_idx = tuple(int(round(f * nout)) for f in (0.25, 0.5, 0.75, 1.0)) if spec.get("probe") else ()
    o = EN.evolve(gr, K, eps, psi0, u0, G0, g0, T, probe_idx=probe_idx)
    tag = f"{kname}_d{dim}_n{n}_eps{eps:.0e}_delta{delta:.0e}"
    try:
        os.makedirs(EXT, exist_ok=True)
        np.savez_compressed(os.path.join(EXT, f"cfg321_{tag}.npz"), snap_t=o["snaps_t"], snap_w=o["snaps_w"],
                            psi_T=o["psi"], u_T=o["u"], **{"rec_" + k_: np.array(v_) for k_, v_ in o["rec"].items()})
        saved = True
    except Exception as e_:
        saved = f"not saved: {e_}"
    return {"spec": spec, "rec": o["rec"], "snaps_w": o["snaps_w"], "status": o["status"], "n_indef": o["n_indef"],
            "max_res": o["max_res"], "dt": o["dt"], "wall": time.time() - t0, "probes": o["probes"], "n_refac": o["n_refac"],
            "saved": saved}


# ================================================================================================= task list
specs = []
if not MUTATE:
    specs.append({"kind": "lin", "dim": 1, "n": 63, "L": L1D, "eps": 1e-2, "modes": [(0, 1), (0, 3), (0, 5), (0, 6), (0, 8)]})
    specs.append({"kind": "lin", "dim": 2, "n": 15, "L": L2D, "eps": 1e-2, "modes": [(1, 1), (1, 2), (1, 3), (0, 2), (0, 3)]})
    for n in (63, 127, 255):
        for dl in (0.0, 1e-3, 1e-5):
            specs.append({"kind": "gr", "n": n, "eps": 1e-2, "delta": dl})
N1, N2D = (63, 127, 255), (15, 21, 29)
EPS1 = (1e-2,) if MUTATE else (1e-2, 1e-3)
for eps in EPS1:
    for n in N1:
        for dl in (0.0, 1e-3, 1e-5):
            specs.append({"kind": "main", "dim": 1, "n": n, "eps": eps, "delta": dl, "kern": KERN_MAIN,
                          "probe": (dl == 0.0 and n == N1[-1])})
if not MUTATE:
    for n in (63, 127):
        specs.append({"kind": "main", "dim": 1, "n": n, "eps": 1e-4, "delta": 0.0, "kern": KERN_MAIN, "probe": False})
for n in N2D:
    for dl in (0.0, 1e-3, 1e-5):
        specs.append({"kind": "main", "dim": 2, "n": n, "eps": 1e-2, "delta": dl, "kern": KERN_MAIN,
                      "probe": (dl == 0.0 and n == N2D[-1])})
if not MUTATE:
    for n in N2D:
        specs.append({"kind": "main", "dim": 2, "n": n, "eps": 1e-3, "delta": 0.0, "kern": KERN_MAIN,
                      "probe": n == N2D[-1]})


def cost(s):
    if s["kind"] != "main":
        return 1.0
    nn = s["n"] ** s["dim"]
    return nn ** (1.6 if s["dim"] == 1 else 2.2) / math.sqrt(s["eps"])


specs.sort(key=lambda s: -cost(s))
banner(f"PARTS C-E  {len(specs)} runs on {NPROC} processes (controls C-LIN, C-GR; the nonlinear runs)")
results = []
with get_context("fork").Pool(NPROC) as pool:
    for r in pool.imap_unordered(task, specs):
        s = r["spec"]
        P(f"  done: {s['kind']:4s} " + ", ".join(f"{k_}={v_}" for k_, v_ in s.items() if k_ not in ("kind", "modes", "probe"))
          + f"  status={r.get('status', 'ok')}  wall={r['wall']:.0f} s  (elapsed {time.time() - T0:.0f} s)")
        results.append(r)


def find(**kw):
    out = [r for r in results if all(r["spec"].get(k_) == v_ for k_, v_ in kw.items())]
    return out[0] if out else None


# ================================================================================================= PART C/D: controls
if not MUTATE:
    banner("PART C  C-LIN: the nonlinear code linearised about a uniform field yhat_b = 1e-4")
    lin_ok = True; lin_rows = []
    for r in [x_ for x_ in results if x_["spec"]["kind"] == "lin"]:
        d_ = r["spec"]["dim"]
        for q in r["res"]:
            rel = q["measured"] / q["predicted"] - 1
            side = "inside" if q["k"] < q["edge"] else "outside"
            P(f"    {d_}-D k {'||' if q['axis'] == 0 else 'perp'} G, k xi = {q['k']:.4f} ({side} the band edge {q['edge']:.4f}): "
              f"{q['type']} measured {q['measured']:.5f}, predicted {q['predicted']:.5f}  (rel {rel:+.2e}); status {q['status']}")
            lin_rows.append((d_, q["axis"], q["k"], q["type"], q["measured"], q["predicted"], side))
            lin_ok &= abs(rel) < 0.01 and q["status"] == "ok"
    sides = {(r_[0], r_[6]) for r_ in lin_rows}
    lin_ok &= all((d_, s_) in sides for d_ in (1, 2) for s_ in ("inside", "outside"))
    check("C-LIN the nonlinear code, linearised about yhat_b = 1e-4, reproduces omega^2 = k^2((1+eps)/(C sigma^2 + eps) - 1) "
          "to 1% (1-D: k || G, C_L; 2-D: k perp G, C_T, and k || G), on both sides of the band edge k xi = sqrt(ln C)",
          "; ".join(f"{r_[0]}D {'L' if r_[1] == 0 else 'T'} k={r_[2]:.3f} {r_[3][0]} {r_[4] / r_[5] - 1:+.1e}" for r_ in lin_rows), lin_ok)
    OUT["numbers"]["C_LIN"] = lin_rows

    banner("PART D  C-GR: the MOND sector off (C -> 0): GR + the healthy BPS khronon, 1-D, eps = 1e-2, T = 10")
    gr_rows = []
    for n in (63, 127, 255):
        b = find(kind="gr", n=n, delta=0.0); p3 = find(kind="gr", n=n, delta=1e-3); p5 = find(kind="gr", n=n, delta=1e-5)
        E = np.array(b["rec"]["E"]); Ek = np.array(b["rec"]["Ekin"])
        drift = float(np.max(np.abs(E - E[0])) / max(np.max(np.abs(E)), 1e-300))
        D3 = [float(np.linalg.norm(a_ - c_) / np.linalg.norm(a_)) for a_, c_ in zip(b["snaps_w"], p3["snaps_w"])]
        D5 = [float(np.linalg.norm(a_ - c_) / np.linalg.norm(a_)) for a_, c_ in zip(b["snaps_w"], p5["snaps_w"])]
        gr_rows.append({"n": n, "dt": b["dt"], "err_T": b["err"][-1], "drift": drift, "maxD5": max(D5) / 1e-5,
                        "ratio": D3[-1] / D5[-1], "status": b["status"]})
        P(f"    N = {n}: dt {b['dt']:.3e}; error vs exact at T = 10: {b['err'][-1]:.3e}; energy drift {drift:.2e}; "
          f"max D/delta {max(D5) / 1e-5:.3f}; D(1e-3)/D(1e-5) at T = {D3[-1] / D5[-1]:.3f}")
    e_ = [r_["err_T"] for r_ in gr_rows]; h_ = [r_["dt"] for r_ in gr_rows]
    p_gr = math.log(e_[1] / e_[2]) / math.log(h_[1] / h_[2])
    gr_ok = (p_gr >= 1.8 and all(r_["drift"] <= 1e-3 and r_["maxD5"] <= 10 and abs(r_["ratio"] / 100 - 1) < 0.01
                                  and r_["status"] == "ok" for r_ in gr_rows))
    check("C-GR with the MOND sector off the reduced system is the healthy khronon wave equation: error vs the exact solution "
          "converges with order >= 1.8, energy drift <= 1e-3, pair separation bounded (max D/delta <= 10) and linear in delta",
          f"order {p_gr:.3f} (errors {', '.join(f'{x_:.2e}' for x_ in e_)}); drifts {[f'{r_['drift']:.1e}' for r_ in gr_rows]}; "
          f"max D/delta {[round(r_['maxD5'], 3) for r_ in gr_rows]}; ratios {[round(r_['ratio'], 3) for r_ in gr_rows]}", gr_ok)
    OUT["numbers"]["C_GR"] = {"rows": gr_rows, "order": p_gr}

# ================================================================================================= PART F
banner("PART F  the nonlinear runs: R1 regular/bounded, R2 resolution, R3 continuous dependence, R4 eps ladder")


def common_vec(r, dim, nc):
    gr_n = r["spec"]["n"]; NN = gr_n ** dim
    out = []
    for sw in r["snaps_w"]:
        comps = []
        for a_ in range(dim):
            Fk = np.fft.fftn(sw[a_].reshape((gr_n,) * dim)) / NN
            if dim == 1:
                sel = np.concatenate([Fk[:nc + 1], Fk[-nc:]])
            else:
                ii = np.r_[0:nc + 1, gr_n - nc:gr_n]
                sel = Fk[np.ix_(ii, ii)].ravel()
            comps.append(sel)
        out.append(np.concatenate(comps))
    return np.array(out)


def tau_first(rec, thr=0.1):
    y = np.array(rec["yrms"]); t = np.array(rec["t"])
    i = np.where(y >= thr)[0]
    return float(t[i[0]]) if len(i) else None


def boot_mean(x, block=20, nb=2000, seed=0):
    x = np.asarray(x); nbk = len(x) // block
    bm = np.array([x[i * block:(i + 1) * block].mean() for i in range(nbk)])
    rng = np.random.default_rng(seed)
    s = [rng.choice(bm, size=nbk, replace=True).mean() for _ in range(nb)]
    return float(x.mean()), float(np.std(s))


def window_stats(r, T, Vol):
    rec = r["rec"]; t = np.array(rec["t"]); sel = t >= T / 2 - 1e-9
    out = {}
    for key, arr in (("rms", rec["yrms"]), ("median", rec["ymed"]), ("p90", rec["p90"]),
                     ("Ekin", np.array(rec["Ekin"]) / Vol), ("fpin", rec["fpin"])):
        out[key] = boot_mean(np.asarray(arr)[sel])
    return out


def pair_D(rb, rp):
    return np.array([float(np.linalg.norm(a_ - c_) / max(np.linalg.norm(a_), 1e-300)) for a_, c_ in zip(rb["snaps_w"], rp["snaps_w"])])


def lyap(D, t):
    sel = (D >= 1e-4) & (D <= 1e-1)
    if sel.sum() < 8:
        return None
    return float(np.polyfit(t[sel], np.log(D[sel]), 1)[0])


def order_fit(d12, d23, h):
    # d12/d23 = (h1^p - h2^p)/(h2^p - h3^p), solved for p in (0.2, 8)
    from scipy.optimize import brentq
    f = lambda p: (h[0] ** p - h[1] ** p) / (h[1] ** p - h[2] ** p) - d12 / d23
    try:
        return brentq(f, 0.2, 8.0)
    except Exception:
        return float("nan")


SETS = [(1, e_) for e_ in EPS1] + [(2, 1e-2)]
R = {"R1": True, "R2": True, "R3": True, "R4": True}
FAILSIG = []
summary = {}
for (dim, eps) in SETS:
    Ns = N1 if dim == 1 else N2D
    T = T1D if dim == 1 else T2D
    L = L1D if dim == 1 else L2D
    Vol = L ** dim
    nc = (Ns[0] - 1) // 2
    P(f"\n  --- set: {dim}-D, eps = {eps:.0e}, kernel {KERN_MAIN} ---")
    base = {n: find(kind="main", dim=dim, n=n, eps=eps, delta=0.0) for n in Ns}
    p3 = {n: find(kind="main", dim=dim, n=n, eps=eps, delta=1e-3) for n in Ns}
    p5 = {n: find(kind="main", dim=dim, n=n, eps=eps, delta=1e-5) for n in Ns}
    # ---------------------------------------------------------------- R1
    r1 = True; r1_txt = []
    for n in Ns:
        for lab, rr in (("base", base[n]), ("d1e-3", p3[n]), ("d1e-5", p5[n])):
            E = np.array(rr["rec"]["E"]); Ek = np.array(rr["rec"]["Ekin"])
            drift = float(np.max(np.abs(E - E[0])) / max(Ek.max(), 1e-300)) if len(E) else float("inf")
            ok_ = rr["status"] == "ok" and rr["max_res"] <= 1e-8 and rr["n_indef"] == 0 and drift <= 1e-3
            if rr["status"] == "blowup" or rr["status"].startswith("leaf-fail"):
                FAILSIG.append(f"{dim}-D eps {eps:.0e} N {n} {lab}: {rr['status']}")
            if rr["n_indef"] > 0:
                FAILSIG.append(f"{dim}-D eps {eps:.0e} N {n} {lab}: {rr['n_indef']} indefinite leaf Hessians (non-convex leaf: branching)")
            r1 &= ok_
            r1_txt.append(f"N{n}/{lab}: {rr['status']}, res {rr['max_res']:.1e}, indef {rr['n_indef']}, drift {drift:.1e}, "
                          f"max yhat {max(rr['rec']['ymax']) if rr['rec']['ymax'] else float('nan'):.3f}")
    top = max(base[Ns[-1]]["rec"]["top"]) if base[Ns[-1]]["rec"]["top"] else float("inf")
    r1 &= top <= 1e-6
    probes = base[Ns[-1]]["probes"]
    pr_ok = len(probes) == 4 and all(pq[1] <= 1e-6 and pq[2] for pq in probes)
    if not pr_ok and len(probes):
        if any(pq[1] > 1e-6 or not pq[2] for pq in probes):
            FAILSIG.append(f"{dim}-D eps {eps:.0e}: leaf-uniqueness probe failed {probes}")
    r1 &= pr_ok
    for tx in r1_txt:
        P("    " + tx)
    P(f"    finest: top-third khronon gradient energy max {top:.2e}; leaf probes (t, two-start diff, PD): "
      + ", ".join(f"({pq[0]:.0f}, {pq[1]:.1e}, {pq[2]})" for pq in probes))
    check(f"R1 [{dim}-D eps {eps:.0e}] every run regular and bounded: no blow-up, leaf solved (<= 1e-8) with zero indefinite "
          "Hessians, energy drift <= 1e-3 max E_kin, finest grid-top-third <= 1e-6, leaf unique at 4 probe times",
          f"all runs ok: {r1}; top {top:.1e}; probes ok {pr_ok}", r1)
    R["R1"] &= r1
    if not all(base[n]["status"] == "ok" for n in Ns):
        summary[(dim, eps)] = {"broken": True}
        R["R2"] = R["R3"] = False
        continue
    # ---------------------------------------------------------------- R2
    taus = tau_first(base[Ns[-1]]["rec"])
    if taus is None:
        check(f"R2a [{dim}-D eps {eps:.0e}] growth-phase reference time exists", "rms yhat never reached 0.1", False)
        R["R2"] = False; continue
    it = int(round(taus / 0.25))
    V = {n: common_vec(base[n], dim, nc)[it] for n in Ns}
    d12 = float(np.linalg.norm(V[Ns[0]] - V[Ns[1]]) / np.linalg.norm(V[Ns[2]]))
    d23 = float(np.linalg.norm(V[Ns[1]] - V[Ns[2]]) / np.linalg.norm(V[Ns[2]]))
    hs = [base[n]["dt"] for n in Ns]
    p_obs = order_fit(d12, d23, hs) if d23 > 0 else float("inf")
    r2a = (d23 <= 1e-3 and p_obs >= 1.5) or d23 <= 1e-9
    check(f"R2a [{dim}-D eps {eps:.0e}] growth phase converges pointwise: at tau_s = {taus:.2f} the two finest grids differ by "
          "<= 1e-3 (relative L2 of w on common modes) with observed order >= 1.5 (fitted against dt)",
          f"d12 = {d12:.3e}, d23 = {d23:.3e}, dt = {[f'{x_:.3e}' for x_ in hs]}, p = {p_obs:.3f}", r2a)
    ws = {n: window_stats(base[n], T, Vol) for n in Ns}
    r2b = True; txt = []
    for key in ("rms", "median", "p90", "Ekin", "fpin"):
        a_, sa = ws[Ns[-1]][key]; b_, sb = ws[Ns[-2]][key]; c_, sc_ = ws[Ns[0]][key]
        tol = max(0.10 * abs(a_), 2 * math.hypot(sa, sb))
        ok_ = abs(a_ - b_) <= tol
        r2b &= ok_
        txt.append(f"{key}: {c_:.4g}/{b_:.4g}/{a_:.4g} (+-{sa:.2g}; |diff| {abs(a_ - b_):.3g} vs tol {tol:.3g}) {'ok' if ok_ else 'MISS'}")
    for tx in txt:
        P("    " + tx)
    check(f"R2b [{dim}-D eps {eps:.0e}] the saturated state (window [T/2, T]) is resolution independent: <rms>, <median>, <p90> "
          "of yhat, <E_kin>/Vol, <f_pin> agree between the two finest grids within max(10%, 2 sigma)",
          "; ".join(t_.split(' (')[0] + (' ok' if t_.endswith('ok') else ' MISS') for t_ in txt), r2b)
    R["R2"] &= r2a and r2b
    # ---------------------------------------------------------------- R3
    tt = np.array(base[Ns[-1]]["rec"]["t"])
    A_, LAM, RAT = {}, {}, {}
    for n in Ns:
        D3 = pair_D(base[n], p3[n]); D5 = pair_D(base[n], p5[n])
        RAT[n] = D3[it] / max(D5[it], 1e-300)
        A_[n] = D5[it] / 1e-5
        LAM[n] = lyap(D5, np.array(base[n]["rec"]["t"])[:len(D5)])
        P(f"    N = {n}: D(1e-3)/D(1e-5) at tau_s = {RAT[n]:.2f}; amplification A = {A_[n]:.3g}; Lyapunov lambda = "
          f"{LAM[n] if LAM[n] is None else round(LAM[n], 4)}; D_1e-5 at T = {D5[-1]:.2e}")
        summary.setdefault((dim, eps), {})[f"D5_{n}"] = D5.tolist()
    r3a = all(30 <= RAT[n] <= 300 for n in Ns)
    r3b = 0.5 <= A_[Ns[-1]] / A_[Ns[-2]] <= 2
    if LAM[Ns[-1]] is not None and LAM[Ns[-2]] is not None:
        r3c = 0.8 <= LAM[Ns[-1]] / LAM[Ns[-2]] <= 1.25; lam_txt = f"{LAM[Ns[-1]] / LAM[Ns[-2]]:.3f}"
    else:
        r3c = r3b; lam_txt = "not reached"
    check(f"R3 [{dim}-D eps {eps:.0e}] continuous dependence: separation linear in delta at tau_s (ratio in [30, 300] at every "
          "grid), amplification and Lyapunov exponent not growing with resolution (finest/next in [0.5, 2] and [0.8, 1.25])",
          f"ratios {[round(RAT[n], 2) for n in Ns]}; A {[f'{A_[n]:.3g}' for n in Ns]} (finest/next {A_[Ns[-1]] / A_[Ns[-2]]:.3f}); "
          f"lambda {[None if LAM[n] is None else round(LAM[n], 4) for n in Ns]} (finest/next {lam_txt})", r3a and r3b and r3c)
    R["R3"] &= r3a and r3b and r3c
    if RAT[Ns[-1]] < 3:
        FAILSIG.append(f"{dim}-D eps {eps:.0e}: order-one response to infinitesimal data (ratio {RAT[Ns[-1]]:.2f})")
    if A_[Ns[1]] / A_[Ns[0]] > 2 and A_[Ns[2]] / A_[Ns[1]] > 2:
        FAILSIG.append(f"{dim}-D eps {eps:.0e}: amplification grows with resolution at both steps")
    if all(LAM[n] is not None for n in Ns) and LAM[Ns[1]] / LAM[Ns[0]] > 1.25 and LAM[Ns[2]] / LAM[Ns[1]] > 1.25:
        FAILSIG.append(f"{dim}-D eps {eps:.0e}: Lyapunov exponent grows with resolution at both steps")
    summary[(dim, eps)].update({"tau_s": taus, "d12": d12, "d23": d23, "p": p_obs, "ws": {n: ws[n] for n in Ns},
                                "ratio": RAT, "A": A_, "lambda": LAM})

# ---------------------------------------------------------------- R1 for the eps-ladder-only runs (frozen: every run of section 4)
if not MUTATE:
    lad_runs = [x_ for x_ in results if x_["spec"]["kind"] == "main" and ((x_["spec"]["dim"] == 1 and x_["spec"]["eps"] == 1e-4)
                                                                        or (x_["spec"]["dim"] == 2 and x_["spec"]["eps"] == 1e-3))]
    r1l = True; txt = []
    for rr in lad_runs:
        E = np.array(rr["rec"]["E"]); Ek = np.array(rr["rec"]["Ekin"])
        drift = float(np.max(np.abs(E - E[0])) / max(Ek.max(), 1e-300)) if len(E) else float("inf")
        ok_ = rr["status"] == "ok" and rr["max_res"] <= 1e-8 and rr["n_indef"] == 0 and drift <= 1e-3
        if rr["status"] == "blowup" or rr["status"].startswith("leaf-fail"):
            FAILSIG.append(f"ladder {rr['spec']}: {rr['status']}")
        if rr["n_indef"] > 0:
            FAILSIG.append(f"ladder {rr['spec']}: indefinite leaf Hessians")
        if rr["spec"]["dim"] == 2 and rr["spec"]["n"] == N2D[-1]:
            top = max(rr["rec"]["top"]) if rr["rec"]["top"] else float("inf")
            pr = rr["probes"]; pr_ok = len(pr) == 4 and all(pq[1] <= 1e-6 and pq[2] for pq in pr)
            if len(pr) and any(pq[1] > 1e-6 or not pq[2] for pq in pr):
                FAILSIG.append(f"ladder 2-D eps 1e-3: leaf-uniqueness probe failed {pr}")
            ok_ &= top <= 1e-6 and pr_ok
            txt.append(f"2-D n {rr['spec']['n']} eps 1e-3 top {top:.1e} probes {[(round(pq[0]), f'{pq[1]:.1e}', pq[2]) for pq in pr]}")
        r1l &= ok_
        txt.append(f"{rr['spec']['dim']}-D n {rr['spec']['n']} eps {rr['spec']['eps']:.0e}: {rr['status']}, res {rr['max_res']:.1e}, "
                   f"indef {rr['n_indef']}, drift {drift:.1e}")
    for tx in txt:
        P("    " + tx)
    check("R1 [eps-ladder runs: 1-D eps 1e-4, 2-D eps 1e-3] regular and bounded (same criteria)", "; ".join(txt), r1l)
    R["R1"] &= r1l

# ---------------------------------------------------------------- R4
if not MUTATE:
    P("\n  --- R4: the eps ladder ---")
    r4_all = True
    for (dim, n, e_lo, e_hi) in ((1, 127, 1e-4, 1e-3), (2, 29, 1e-3, 1e-2)):
        T = T1D if dim == 1 else T2D; L = L1D if dim == 1 else L2D
        ra = find(kind="main", dim=dim, n=n, eps=e_lo, delta=0.0); rb = find(kind="main", dim=dim, n=n, eps=e_hi, delta=0.0)
        if ra["status"] != "ok" or rb["status"] != "ok":
            check(f"R4 [{dim}-D N {n}] eps ladder runs complete", f"{ra['status']} / {rb['status']}", False); r4_all = False; continue
        sa_, sb_ = window_stats(ra, T, L ** dim), window_stats(rb, T, L ** dim)
        ok4 = True; txt = []
        for key in ("rms", "median", "p90", "Ekin"):
            a_, ea = sa_[key]; b_, eb = sb_[key]
            tol = max(0.15 * abs(a_), 2 * math.hypot(ea, eb)); ok_ = abs(a_ - b_) <= tol; ok4 &= ok_
            txt.append(f"{key} {a_:.4g} vs {b_:.4g} ({'ok' if ok_ else 'MISS'}, tol {tol:.3g})")
        ta, tb = tau_first(ra["rec"]), tau_first(rb["rec"])
        okt = ta is not None and tb is not None and abs(ta / tb - 1) <= 0.10
        ok4 &= okt
        # all runs of the ladder at this resolution (reported)
        lad = [x_ for x_ in results if x_["spec"]["kind"] == "main" and x_["spec"]["dim"] == dim and x_["spec"]["n"] == n
               and x_["spec"]["delta"] == 0.0]
        P(f"    {dim}-D N = {n}: " + "; ".join(f"eps {x_['spec']['eps']:.0e}: <rms yhat> {window_stats(x_, T, L ** dim)['rms'][0]:.4f}, "
                                           f"tau_s {tau_first(x_['rec'])}" for x_ in sorted(lad, key=lambda q: q['spec']['eps'])))
        check(f"R4 [{dim}-D N {n}] eps ladder {e_lo:.0e} vs {e_hi:.0e}: saturated statistics within max(15%, 2 sigma), tau_s within 10%",
              "; ".join(txt) + f"; tau_s {ta} vs {tb}", ok4)
        r4_all &= ok4
    R["R4"] = r4_all
else:
    R["R4"] = None

# ---------------------------------------------------------------- the saturated state (reported)
banner("THE SATURATED STATE (reported, not graded)")
sat = {}
for (dim, eps, n) in ((1, min(EPS1), N1[-1]), (2, 1e-2, N2D[-1])):
    r = find(kind="main", dim=dim, n=n, eps=eps, delta=0.0)
    if r is None or r["status"] != "ok":
        continue
    T = T1D if dim == 1 else T2D; L = L1D if dim == 1 else L2D
    t = np.array(r["snaps_t"] if "snaps_t" in r else r["rec"]["t"])
    tt_ = np.array(r["rec"]["t"])
    ys = np.concatenate([np.sqrt(np.sum(np.asarray(sw) ** 2, axis=0)) for sw, ti in zip(r["snaps_w"], tt_) if ti >= T / 2])
    q = np.percentile(ys, [1, 10, 50, 90, 99, 99.9])
    f3, f2 = float(np.mean(ys < 1e-3)), float(np.mean(ys < 1e-2))
    Ekv = boot_mean(np.array(r["rec"]["Ekin"])[tt_ >= T / 2] / L ** dim)
    Etot = float(np.mean(np.array(r["rec"]["E"]))) / L ** dim
    # physical energy density: H_phys = lambda_E e_lane, lambda_E = c^4/(16 pi G xi^2) U0^2 alpha a^2/(2(2+alpha)),
    # U0 = (a0 xi/c^2) y*, a = alpha (Lambda - 1) at the physical alpha (Part A field map)
    xi_m = XI_PC * PC
    U0 = A0["canonical"] * xi_m / c_SI ** 2 * KN.ystar
    a_f = A_MAX * (4 / A_MAX ** 2 - 1)
    lamE = c_SI ** 4 / (16 * math.pi * G_SI * xi_m ** 2) * U0 ** 2 * A_MAX * a_f ** 2 / (2 * (2 + A_MAX))
    e_phys = lamE * Ekv[0]
    rhoL_c2 = RHO_L * c_SI ** 2
    g_sat = q[2] * KN.ystar * A0["canonical"]
    tsat_yr = (tau_first(r["rec"]) or float("nan")) * TAU_UNIT_S / YR
    disp_m = 0.5 * (q[4] * KN.ystar * A0["canonical"]) * (T * TAU_UNIT_S) ** 2
    h_max = a_f * U0 * float(np.max(np.abs(r["rec"]["ymax"])))     # order of the metric perturbation (|psi_tilde| ~ yhat^(1/2) <~ 1)
    P(f"  {dim}-D N = {n}, eps = {eps:.0e}: yhat percentiles (1, 10, 50, 90, 99, 99.9) = {', '.join(f'{x_:.3g}' for x_ in q)}; "
      f"fraction yhat < 1e-3: {f3:.4f}, < 1e-2: {f2:.4f}")
    P(f"     median field = {q[2]:.3f} y* = {g_sat:.2e} m/s^2; growth phase {tsat_yr:.2e} yr (1/H0 = {1 / H0 / YR:.2e} yr); "
      f"<E_kin>/Vol = {Ekv[0]:.4f} +- {Ekv[1]:.4f} (lane units) -> {e_phys:.2e} J/m^3 = {e_phys / rhoL_c2:.1e} rho_Lambda c^2; "
      f"dust displacement over T: {disp_m:.1e} m (xi = {xi_m:.2e} m); metric perturbation <~ {h_max:.1e}")
    sat[f"{dim}D"] = {"percentiles": q.tolist(), "f_lt_1e-3": f3, "f_lt_1e-2": f2, "Ekin_per_vol": Ekv, "E_per_vol": Etot,
                      "e_phys_J_m3": e_phys, "over_rhoL": e_phys / rhoL_c2, "g_median_SI": g_sat, "t_growth_yr": tsat_yr,
                      "dust_disp_m": disp_m, "metric_pert": h_max}
OUT["numbers"]["saturated"] = sat

# ---------------------------------------------------------------- verdict
banner("VERDICT (frozen rule)")
ctrl_ok = all(ok for (nm, ok, lb) in CH if nm.startswith(("C-SYM", "C-FP5", "C-LIN", "C-GR")))
if FAILSIG:
    verdict = "FAIL"
elif R["R1"] and R["R2"] and R["R3"] and (R["R4"] is True) and ctrl_ok:
    verdict = "CONDITIONAL"
else:
    verdict = "OPEN"
P(f"  R1 {R['R1']}, R2 {R['R2']}, R3 {R['R3']}, R4 {R['R4']}; controls {ctrl_ok}; FAIL signatures: {FAILSIG if FAILSIG else 'none'}")
P(f"  VERDICT: {verdict}" + (" (MUTATE run: must NOT be CONDITIONAL)" if MUTATE else ""))
P("  Scope: says NOTHING about growth or sigma_8 -- L341's failure (sigma_8 = 18-27) and FP2's failed linear cosmology stand.")
OUT["verdict"] = verdict; OUT["R"] = R; OUT["fail_signatures"] = FAILSIG
OUT["numbers"]["sets"] = {f"{k_[0]}D_eps{k_[1]:.0e}": {kk: (vv if not isinstance(vv, dict) else {str(a): b for a, b in vv.items()})
                                                      for kk, vv in v_.items() if not kk.startswith("D5_")} for k_, v_ in summary.items()}
OUT["runs"] = [{"spec": {k_: v_ for k_, v_ in r["spec"].items() if k_ != "modes"}, "status": r.get("status", "ok"),
                "wall_s": r["wall"], "dt": r.get("dt"), "n_refac": r.get("n_refac"), "max_res": r.get("max_res"),
                "n_indef": r.get("n_indef")} for r in results]

if MUTATE:
    mut_ok = verdict != "CONDITIONAL"
    check("MUTATE the turning kernel mu_exp (a0 -> y* a0) does NOT return CONDITIONAL", f"verdict {verdict}; {FAILSIG}", mut_ok)

npass = sum(1 for c_ in CH if c_[1]); nlb = sum(1 for c_ in CH if c_[2]); nlbp = sum(1 for c_ in CH if c_[1] and c_[2])
P(f"\n  {npass}/{len(CH)} checks pass ({nlbp}/{nlb} load-bearing); verdict {verdict}; wall {time.time() - T0:.0f} s")
OUT["summary"] = {"pass": npass, "total": len(CH), "lb_pass": nlbp, "lb_total": nlb, "wall_s": time.time() - T0}
json.dump(OUT, open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
if MUTATE:
    sys.exit(1 if mut_ok else 0)      # the control "fails as required" <=> rc = 1
sys.exit(0 if (npass == len(CH)) else 1)

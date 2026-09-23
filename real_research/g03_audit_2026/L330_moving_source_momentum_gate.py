#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L330 -- THE MOVING-SOURCE GATE: a MOND sector that carries no momentum cannot carry a phantom that follows
matter.  astra's C-H realises the T-B static functional only as INITIAL DATA, under either causality criterion.

THE QUESTION THE RECORD HAD NOT RUN
  G03's candidate C-H (qwen_claude_field_theory/closure_2026/g03_covariant_action_2026/ACTION.md) reproduces the
  T-B static functional on a stationary branch with the shift set to zero.  Its static gates (Cassini via T-B,
  lensing = dynamics at leading static order) are real.  L318 reduced its remaining causal question to a choice
  of criterion.  Nobody asked whether the static MOND solution is REACHED: does the phantom form as a galaxy
  assembles, and does it follow a galaxy that moves?  astra's ACTION.md (lines 248-274) found, in a truncated
  constant-background block, that "the modified static branch depends on a spatial integration function F; it is
  not selected by the instantaneous source", and FULL_VARIATION.md sec. 3 found a conserved datum
  (partial_t delta C = 0) in the exact spherical equations.  Both were left as "initial-data content".  This lane
  draws the physical consequence and shows it does not depend on the truncation.

WHAT THIS LANE SHOWS
  M1 SHIFT-INDEPENDENCE (symbolic, every building block of C-H's modification).  In the unitary gauge tau = t, for
     a metric with arbitrary lapse N(t,x), arbitrary shift N^i(t,x) and conformally flat leaves:
     h^{mu nu}(D_mu U - a_mu)(D_nu U - a_nu) = gamma^{ij}(d_i U - d_i ln N)(d_j U - d_j ln N), with a_i = d_i ln N,
     n.a = 0; the same projector gives h^{mu nu} dW dW = gamma^{ij} d_iW d_jW; Delta_h is intrinsic; the measure is
     N sqrt(gamma).  No shift and no time derivative appear, to all orders.  Hence the (n,i) Einstein equation is
     exactly GR's with MATTER momentum only -- astra's own FULL_VARIATION.md sec. 2 states G_ni = 8 pi G T_m,ni.
  M2 THE FROZEN-DENSITY IDENTITY (symbolic, general h_ij and shift about Minkowski).  The divergence of the
     linearised momentum constraint is identically (1/2) d_t R3, with R3 = d_i d_j h_ij - lap h the linearised
     curvature of the preferred leaves; every shift term cancels.  With matter conserved,
         d_t [ R3 - 16 pi G rho_m ] = 0 :
     the non-baryonic density that the spatial curvature sees, rho_dark = R3/(16 pi G) - rho_m, is time-independent.
     It is exact in the MOND sector's nonlinearity (that sector never enters) and linear only in the metric
     (errors O(Phi/c^2) ~ 1e-6 for galaxies).  Control: a momentum-carrying extra sector (K^2 coefficient
     lambda != 1, the Horava/khronometric c_2 channel) leaves (1 - lambda) lap K, and the identity FAILS.
  M3 astra's TRUNCATED BLOCK, REPRODUCED (ACTION.md L_2).  The lapse phi = F(1+C)/C depends on the integration
     constant F only, never on rho_s; the Bardeen potential is psi_N + F; GR control (C = 0) forces F = 0; the
     static MOND branch F = C psi_N is a solution only while rho_s is constant.
  M4 WHAT IT COSTS, IN NUMBERS.  (a) FORMATION: a galaxy assembled from near-uniform initial data has rho_dark set
     at the start, not by its baryons -- no phantom forms in the leaf curvature.  (b) MOTION: a phantom present at
     t0 stays where it was; a pair or satellite moving at v relative to the (single-valued, irrotational) normal
     congruence leaves it behind by v t, against halo scales of r_M.  (c) THE DICHOTOMY: either the dynamical
     potential is also unresponsive (no MOND phenomenology is ever generated: SPARC's RAR/BTFR unexplained), or it
     responds through the lapse while the leaf curvature does not, and lensing sees (g_dyn + g_bar)/2 -- about
     HALF the phantom -- where KiDS-1000 finds the lensing RAR on the dynamical one (Brouwer+2021, adopted by the
     record's TRIANGLE_KIDS).
  M5 THE PINCER.  The shift-independence that freezes the phantom is the same fact that gives alpha_1 = alpha_2 = 0
     on the record (fable_independent_2026/FINDINGS.md, the clock-candidate PPN block: "the clock is exactly
     shift-independent ... T^phi_0i = 0").  A MOND sector passes the preferred-frame bounds this way only by
     giving up a co-moving phantom; one that carries the phantom's momentum must depend on the shift, which is
     where AeST's alpha_1 = -2(K_B+2) came from.  SCOPE: C-H is in scope (M1, verified).  The L297 clock
     candidate's MOND scalar is leaf-projected (in scope), but its khronon's c_2 K^2 term (lambda - 1 = c_2 ~
     2.5e-5) is a momentum channel; whether it can carry the phantom is NOT computed here (OPEN, named).

  MUTATE=1 gives the extra sector a momentum channel (lambda = 1 + eps in M2; the required phantom current added
  to the block's momentum constraint in M3).  The frozen-density checks must then FAIL (rc = 1).

Run from the repository root:  python3 real_research/g03_audit_2026/L330_moving_source_momentum_gate.py
"""
import os, sys, json, math
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
LANE = "L330"
SLUG = "L330_moving_source_momentum_gate"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": LANE, "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 104); P(t); P("=" * 104)


P(__doc__.split("WHAT THIS LANE SHOWS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the extra sector is given a momentum channel; the frozen-density checks must FAIL ***")

# ============================================================================================ M1
banner("M1  C-H's MODIFICATION IS SHIFT-INDEPENDENT AND FREE OF TIME DERIVATIVES (unitary gauge, symbolic)")
t, x, y, z = X = sp.symbols('t x y z', real=True)
N = sp.Function('N', positive=True)(*X)
b = [sp.Function(f'b{i}')(*X) for i in range(3)]          # shift N^i
w = sp.Function('w')(*X)                                   # conformal factor of the leaves
U = sp.Function('U')(*X)
Wb = sp.Function('W')(*X)
gam = sp.diag(*(3 * [sp.exp(2 * w)]))
gami = gam.inv()
bl = [sum(gam[i, j] * b[j] for j in range(3)) for i in range(3)]
g = sp.zeros(4)
g[0, 0] = -N**2 + sum(bl[i] * b[i] for i in range(3))
for i in range(3):
    g[0, i + 1] = g[i + 1, 0] = bl[i]
    for j in range(3):
        g[i + 1, j + 1] = gam[i, j]
gi = sp.zeros(4)
gi[0, 0] = -1 / N**2
for i in range(3):
    gi[0, i + 1] = gi[i + 1, 0] = b[i] / N**2
    for j in range(3):
        gi[i + 1, j + 1] = gami[i, j] - b[i] * b[j] / N**2
inv_ok = sp.simplify(g * gi - sp.eye(4)) == sp.zeros(4)
n_lo = [-N, 0, 0, 0]                                        # n_mu = -N d_mu tau, tau = t
n_up = [sum(gi[m, k] * n_lo[k] for k in range(4)) for m in range(4)]
Gam = [[[sum(gi[l, s] * (sp.diff(g[s, m], X[nn]) + sp.diff(g[s, nn], X[m]) - sp.diff(g[m, nn], X[s]))
             for s in range(4)) / 2 for nn in range(4)] for m in range(4)] for l in range(4)]
a_lo = [sp.simplify(sum(n_up[nn] * (sp.diff(n_lo[m], X[nn]) - sum(Gam[l][nn][m] * n_lo[l] for l in range(4)))
                        for nn in range(4))) for m in range(4)]
a_target = [sum(b[i] * sp.diff(sp.log(N), X[i + 1]) for i in range(3))] + [sp.diff(sp.log(N), X[i + 1]) for i in range(3)]
a_ok = all(sp.simplify(a_lo[m] - a_target[m]) == 0 for m in range(4))
na = sp.simplify(sum(n_up[m] * a_lo[m] for m in range(4)))
h_up = [[gi[m, nn] + n_up[m] * n_up[nn] for nn in range(4)] for m in range(4)]
V = [sp.diff(U, X[m]) - a_lo[m] for m in range(4)]
Q_acc = sp.simplify(sum(h_up[m][nn] * V[m] * V[nn] for m in range(4) for nn in range(4)))
Q_acc_leaf = sum(gami[i, j] * (sp.diff(U, X[i + 1]) - sp.diff(sp.log(N), X[i + 1]))
                 * (sp.diff(U, X[j + 1]) - sp.diff(sp.log(N), X[j + 1])) for i in range(3) for j in range(3))
Q_W = sp.simplify(sum(h_up[m][nn] * sp.diff(Wb, X[m]) * sp.diff(Wb, X[nn]) for m in range(4) for nn in range(4)))
Q_W_leaf = sum(gami[i, j] * sp.diff(Wb, X[i + 1]) * sp.diff(Wb, X[j + 1]) for i in range(3) for j in range(3))
measure_ok = sp.simplify(-g.det() - N**2 * sp.exp(6 * w)) == 0      # -det g = N^2 det(gamma)
reduce_ok = sp.simplify(Q_acc - Q_acc_leaf) == 0 and sp.simplify(Q_W - Q_W_leaf) == 0
no_shift = not any(e.has(bb) for e in (Q_acc, Q_W) for bb in b)
no_tdot = not any(e.has(sp.Derivative(f, t)) for e in (Q_acc, Q_W) for f in (U, Wb))
P(f"    ADM inverse verified: {inv_ok};  a_mu = D_mu ln N: {a_ok};  n.a = {na};  sqrt(-g) = N sqrt(gamma): {measure_ok}")
P(f"    h(DU - a)^2 and h dW dW reduce to the leaf forms: {reduce_ok};  shift absent: {no_shift};  dU/dt, dW/dt absent: {no_tdot}")
OUT["numbers"]["M1"] = {"inverse": inv_ok, "a_is_DlnN": a_ok, "measure": measure_ok, "leaf_reduction": reduce_ok,
                        "shift_free": no_shift, "time_derivative_free": no_tdot}
check("M1 every term of C-H's modification (2|DU-a|^2, 2 alpha^2 q(|DW_b|^2), the heat constraint with the intrinsic "
      "Delta_h, lambda_0(W_0-U), measure N sqrt h) is independent of the shift and of all time derivatives",
      f"leaf reduction {reduce_ok}; shift-free {no_shift}; time-derivative-free {no_tdot}; a = D ln N {a_ok}",
      inv_ok and a_ok and na == 0 and measure_ok and reduce_ok and no_shift and no_tdot,
      "the (n,i) equation is GR's momentum constraint with matter momentum only, on every background and to all "
      "orders in the MOND nonlinearity (astra's FULL_VARIATION sec. 2: G_ni = 8 pi G T_m,ni)")

# ============================================================================================ M2
banner("M2  THE FROZEN-DENSITY IDENTITY: div(momentum constraint) = (1/2) d_t R3, every shift term cancels")
hij = [[None] * 3 for _ in range(3)]
for i in range(3):
    for j in range(i, 3):
        hij[i][j] = hij[j][i] = sp.Function(f'h{i}{j}')(*X)
Ni = [sp.Function(f'N{i}')(*X) for i in range(3)]
xs = X[1:]
lam = sp.Symbol('lambda')
Kij = [[(sp.diff(hij[i][j], t) - sp.diff(Ni[j], xs[i]) - sp.diff(Ni[i], xs[j])) / 2 for j in range(3)] for i in range(3)]
Ktr = sum(Kij[i][i] for i in range(3))
lap = lambda f: sum(sp.diff(f, v, 2) for v in xs)
R3 = sum(sp.diff(hij[i][j], xs[i], xs[j]) for i in range(3) for j in range(3)) - lap(sum(hij[i][i] for i in range(3)))
divMC = sum(sp.diff(Kij[i][j], xs[i], xs[j]) for i in range(3) for j in range(3)) - lam * lap(Ktr)
resid_gr = sp.simplify(sp.expand(divMC.subs(lam, 1) - sp.diff(R3, t) / 2))
eps = sp.Rational(1, 10**5)
lam_used = 1 + eps if MUTATE else 1
resid_used = sp.simplify(sp.expand(divMC.subs(lam, lam_used) - sp.diff(R3, t) / 2))
shift_in_used = any(resid_used.has(nn) for nn in Ni)
P(f"    GR kinetic structure (lambda = 1):   div MC - (1/2) d_t R3 = {resid_gr}")
P(f"    control, lambda = 1 + 1e-5:          residual = (1 - lambda) lap K  (contains the shift: "
  f"{any(sp.simplify(sp.expand(divMC.subs(lam, 1 + eps) - sp.diff(R3, t) / 2)).has(nn) for nn in Ni)})")
P(f"    used in this run (lambda = {lam_used}): residual zero: {resid_used == 0}; shift present: {shift_in_used}")
OUT["numbers"]["M2"] = {"residual_lambda1": str(resid_gr), "lambda_used": str(lam_used), "residual_used": str(resid_used)[:200]}
check("M2 with GR's kinetic structure and a momentum-free extra sector the divergence of the momentum constraint is "
      "(1/2) d_t R3 with every shift term cancelled, so d_t[R3 - 16 pi G rho_m] = 0 for conserved matter (sign fixed by "
      "GR's Hamiltonian constraint, the C = 0 control of M3): the non-baryonic density seen by the leaf curvature is frozen",
      f"residual {resid_used if resid_used == 0 else 'nonzero, contains the shift'}",
      resid_used == 0 and not shift_in_used,
      "rho_dark = R3/(16 pi G) - rho_m cannot change unless the extra sector carries momentum; the control "
      "(lambda != 1) shows the identity can fail")

# ============================================================================================ M3
banner("M3  astra's TRUNCATED BLOCK (ACTION.md L_2), REPRODUCED: the MOND lapse is the integration constant")
k, C = sp.symbols('k C', positive=True)
psi, phi, beta, Uf, rho, tsf = [sp.Function(nm)(t) for nm in ('psi', 'phi', 'beta', 'U', 'rho', 't_s')]
j_s = sp.diff(rho, t)
j_ph = C * sp.diff(rho, t) if MUTATE else 0        # MUTATE: the phantom's required current (momentum channel)
L2 = (-6 * sp.diff(psi, t)**2 + 4 * k**2 * beta * sp.diff(psi, t) + 2 * k**2 * psi**2 - 4 * k**2 * phi * psi
      + 2 * k**2 * (Uf - phi)**2 + 2 * k**2 * C * Uf**2 - rho * phi + (j_s + j_ph) * beta - tsf * psi)
EL = lambda f: sp.expand(sp.diff(L2, f) - sp.diff(sp.diff(L2, sp.diff(f, t)), t))
F = sp.Symbol('F')
psi_sol = sp.integrate(sp.solve(EL(beta), sp.diff(psi, t))[0], t) + F      # momentum constraint, integrated
U_sol = sp.solve(EL(Uf), Uf)[0]
phi_sol = sp.simplify(sp.solve(EL(phi).subs({Uf: U_sol, psi: psi_sol}), phi)[0])
phi_has_rho = phi_sol.has(rho)
psiN = -rho / (4 * k**2)
F_static = sp.simplify(sp.solve(sp.Eq(psi_sol, (1 + C) * psiN), F)[0]) if not MUTATE else None
gr_ctrl = sp.simplify(EL(phi).subs({Uf: U_sol.subs(C, 0), psi: psi_sol}).subs(C, 0))
P(f"    momentum constraint integrated: psi = {psi_sol}")
P(f"    U = {U_sol};   lapse phi = {phi_sol}   (depends on rho: {phi_has_rho})")
P(f"    GR control C = 0: lapse equation becomes {gr_ctrl} = 0  => F = 0")
if F_static is not None:
    P(f"    static MOND branch psi = (1+C) psi_N needs F = {F_static}: a constant F only while rho is constant")
OUT["numbers"]["M3"] = {"psi": str(psi_sol), "phi": str(phi_sol), "phi_depends_on_rho": phi_has_rho,
                        "GR_control": str(gr_ctrl)}
check("M3 in astra's block the lapse is set by the integration constant alone (phi = F(1+C)/C), the leaf potential "
      "is psi_N + F, and GR (C = 0) forces F = 0",
      f"phi = {phi_sol}; depends on the source: {phi_has_rho}; GR control {gr_ctrl}",
      (not phi_has_rho) and sp.simplify(gr_ctrl + 4 * F * k**2) == 0,
      "astra's 'integration function F' is the frozen rho_dark of M2, seen in one Fourier block; M1-M2 show it "
      "survives the background stresses and mixing the block omits, because none of them enters the momentum constraint")

# ============================================================================================ M4
banner("M4  WHAT THE FROZEN PHANTOM COSTS: formation, motion, and the lensing/dynamics dichotomy (both footings)")
G, Msun, kpc = 6.674e-11, 1.989e30, 3.0857e19
Gyr = 3.156e16
footings = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
nu = lambda yv: 1.0 / (1.0 - np.exp(-np.sqrt(yv)))            # the framework's kernel nu_RAR
rows = {}
for lab, a0 in footings.items():
    rM = {m: math.sqrt(G * m * Msun / a0) / kpc for m in (1e7, 1e9, 6e10)}
    disp = {v: v * 1e3 * Gyr / kpc for v in (100, 200, 370)}              # kpc per Gyr
    # lensing seen with a Newtonian leaf potential and a MOND lapse: g_lens = (g_dyn + g_bar)/2
    ybins = np.array([1e-4, 1e-3, 1e-2, 1e-1]) * (1.2e-10 / a0)          # KiDS g_bar 1.2e-14 .. 1.2e-11 m/s^2
    ratio = (1 + 1 / nu(ybins)) / 2                                       # g_lens / g_dyn
    rows[lab] = {"r_M_kpc": {f"{m:.0e}": round(r, 3) for m, r in rM.items()},
                 "kpc_per_Gyr": {v: round(d, 1) for v, d in disp.items()},
                 "g_lens_over_g_dyn": [round(float(r), 3) for r in ratio],
                 "offset_dex": [round(float(np.log10(r)), 3) for r in ratio]}
    P(f"  {lab:9s} a0 = {a0:.4e}:  r_M = {rM[1e7]:.2f} / {rM[1e9]:.2f} / {rM[6e10]:.1f} kpc for M_b = 1e7 / 1e9 / 6e10 Msun")
    P(f"            displacement at 100 / 200 / 370 km/s: {disp[100]:.0f} / {disp[200]:.0f} / {disp[370]:.0f} kpc per Gyr")
    P(f"            branch (b), KiDS g_bar = 1.2e-14..1.2e-11: g_lens/g_dyn = {', '.join(f'{r:.3f}' for r in ratio)}"
      f"  ({', '.join(f'{np.log10(r):+.2f}' for r in ratio)} dex)")
OUT["numbers"]["M4"] = rows
t_cross_dsph = {lab: rows[lab]["r_M_kpc"]["1e+07"] / (150 * 1e3 * Gyr / kpc) * 1e3 for lab in rows}   # Myr at 150 km/s
P(f"    a 1e7 Msun satellite at 150 km/s leaves its own r_M in {t_cross_dsph['canonical']:.1f} / {t_cross_dsph['alt']:.1f} Myr "
  f"(canonical / alt); a Milky-Way pair at 200 km/s relative leaves r_M = {rows['canonical']['r_M_kpc']['6e+10']:.1f} kpc in "
  f"{rows['canonical']['r_M_kpc']['6e+10'] / rows['canonical']['kpc_per_Gyr'][200] * 1e3:.0f} Myr")
deep_offset = min(min(rows[l]["offset_dex"]) for l in rows)
frozen = (resid_used == 0) and (not phi_has_rho)          # computed in M2 and M3, not set by the MUTATE flag
check("M4 branch (b) -- dynamics responds through the lapse, the leaf curvature cannot -- puts the lensing RAR a factor "
      "~2 below the dynamical RAR at KiDS accelerations; branch (a) generates no MOND at all",
      f"g_lens/g_dyn = {rows['canonical']['g_lens_over_g_dyn']} (canonical); deepest offset {deep_offset:+.2f} dex; "
      f"a satellite leaves r_M in ~{t_cross_dsph['canonical']:.0f} Myr",
      frozen and max(max(rows[l]["g_lens_over_g_dyn"]) for l in rows) < 0.8,
      "a consequence, not a data test: KiDS-1000 (Brouwer+2021) finds the lensing RAR on the dynamical one at "
      "a0 ~ 1.2e-10, and a 0.3 dex deficit is not what they report (a formal sigma needs the per-bin data, not in "
      "the repository).  The normals form one irrotational congruence; two members of a pair, a satellite and its "
      "host, or cluster members moving through one another cannot all be at rest in it, and they cross their "
      "own r_M in ~1-50 Myr, far inside a Hubble time", load_bearing=False)

# ============================================================================================ M5
banner("M5  THE PINCER AND ITS SCOPE")
scope = [
    ("C-H (astra, G03)", "shift-free, no time derivatives (M1)", "IN SCOPE: the phantom is initial data"),
    ("clock candidate MOND scalar (L279-L297)", "leaf-projected Y = h dphi dphi; FINDINGS: T^phi_0i = 0",
     "IN SCOPE for the scalar; khronon c_2 K^2 gives lambda - 1 = c_2 ~ 2.5e-5: a momentum channel, NOT computed (OPEN)"),
    ("AeST / v9 (vector)", "shift-dependent aether kinetic terms", "carries momentum; killed on alpha_1 = -2(K_B+2)"),
    ("dynamical QUMOND auxiliary", "time derivative on the wrong-sign auxiliary", "ghost (Theorem 8 / H045)"),
]
for s in scope:
    P(f"    {s[0]:42s} | {s[1]:52s} | {s[2]}")
OUT["numbers"]["M5"] = scope
check("M5 the preferred-frame safety the record certifies (alpha_1 = alpha_2 = 0 from shift-independence) and a "
      "co-moving phantom are exclusive for a momentum-free MOND sector",
      "same fact (d L_extra/d N^i = 0) gives both; M1-M2 carry the frozen side",
      all(OUT['checks'][c]['ok'] for c in list(OUT['checks'])[:3]),
      "a G03 candidate must carry the phantom's momentum through a shift-dependence that vanishes in the Solar "
      "System (e.g. proportional to nu - 1) without the ghost of a dynamical QUMOND auxiliary", load_bearing=False)

# ============================================================================================ verdict
banner("VERDICT")
P("""  C-H's modification is independent of the shift and of every time derivative (M1), so its momentum constraint
  is GR's with matter alone, and the non-baryonic density seen by the preferred leaves' curvature is conserved
  (M2).  astra's integration function F is that density (M3).  The static MOND solution of C-H is therefore a
  choice of initial data: a galaxy that assembles from near-uniform data forms no phantom in the leaf curvature,
  and a phantom present at t0 cannot follow a source that moves relative to the normal congruence (M4).  Either
  the dynamics is unmodified too (no MOND is ever generated), or lensing sees about half of what the dynamics
  does; both fail gates the record already holds.  This is independent of the causality criterion L318 left to
  decide: under (B) C-H survives causality and still fails here.  The shift-independence that fails this gate is
  the same property that passes alpha_1 = alpha_2 (M5).  G03 stays open only for a construction that carries the
  phantom's momentum; the L297 khronon channel is the one such channel on the record and is not computed here.""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)

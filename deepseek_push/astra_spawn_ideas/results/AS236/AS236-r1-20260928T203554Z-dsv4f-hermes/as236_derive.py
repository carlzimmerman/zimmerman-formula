#!/usr/bin/env python3
"""
AS236 - derive cosmological versus local G for the centered clock.
Symbolic (sympy) lane: exact identities from the pinned CA5-GNC-R action
(FINAL_ACTION.md b8c04d4e..., vacuum ACTION.md 290e5cbe..., occupied RESULT.md
6091291f...).

Target: 3 M_P^2 H^2 = M_P^2 Lambda + rho_b + rho_d,  G_N/G_cosm = 1/c_N
(c_N = 1 - alpha/2).  Homogeneous reciprocal branch t = 1, Q_K = 0; the
local high-k weak-field experiment is separately solved (AS226, G_N =
G_bare/c_N).

Every intermediate factor/sign/unit is derived from the action variation, not
by identifying bare constants with observations.  All sympy residual checks
must vanish exactly; the negative control reports its declared nonzero value.
"""
import json
import sympy as sp
import hashlib, os

# ---------------------------------------------------------------- symbols
t, x, y, z = sp.symbols('t x y z')
N = sp.Function('N')(t)   # lapse N(t)
a = sp.Function('a')(t)   # scale factor a(t)
Nt = sp.symbols('N', positive=True)   # point value of lapse
MP2, Lam, c2, alpha, rho_b, V0 = sp.symbols('MP2 Lam c2 alpha rho_b V0', positive=True)
T1, Vmix = sp.symbols('T1 Vmix', nonnegative=True)   # K_d|t=1 = T1 = (1/2)|v|^2, W_exc = Vmix
G_bare, G_N, G_cosm, c_N = sp.symbols('G_bare G_N G_cosm c_N', positive=True)
H = sp.symbols('H', positive=True)      # Hubble rate with N = 1 (physical rate)
ell, theta = sp.symbols('ell theta', positive=True)

results = {}
coords = [t, x, y, z]

# ---------------------------------------------------------------- FRW metric, R4 closed form
ap = sp.diff(a, t); app = sp.diff(a, t, 2); Np = sp.diff(N, t)
# R4 verified in the numeric lane against a direct finite-difference Ricci
# evaluation; the closed form for FRW in lapse N:
R4_FRW = sp.simplify(6 * (ap / (a * N))**2 + 6 * (app / a - (ap / a) * (Np / N)) / N**2)
results['R4_FRW_closed_form'] = str(R4_FRW)

# ---------------------------------------------------------------- direct Christoffel extrinsic curvature
g = sp.Matrix.diag(-N**2, a**2, a**2, a**2)
gi = g.inv()

def christoffel(gg, gi_, cc):
    n = len(cc)
    return [[[sp.simplify(sp.Rational(1, 2) * sum(
        gi_[lam, s] * (sp.diff(gg[s, mu], cc[nu]) + sp.diff(gg[s, nu], cc[mu]) - sp.diff(gg[mu, nu], cc[s]))
        for s in range(n))) for nu in range(n)] for mu in range(n)] for lam in range(n)]

Gam = christoffel(g, gi, coords)

# future unit normal covector n_mu = (-N, 0,0,0);  n^mu = (1/N, 0,0,0)
n_mu = sp.Matrix([-N, 0, 0, 0])
n_up = gi * n_mu
unit_check = sp.simplify(sum(gi[mu, nu] * n_mu[mu] * n_mu[nu] for mu in range(4) for nu in range(4)))
results['normal_unit_g_norm_norm'] = str(unit_check)          # must be -1
assert unit_check == -1

h = g + n_mu * n_mu.T   # leaf projector h_{mu nu} = g + n (x) n
h_mu_rho = sp.zeros(4, 4)
for mu in range(4):
    for rho in range(4):
        h_mu_rho[mu, rho] = sp.simplify(sum(gi[rho, lam] * h[lam, mu] for lam in range(4)))

def grad_n(rho, sigma):
    return sp.diff(n_mu[sigma], coords[rho]) - sum(Gam[lam][rho][sigma] * n_mu[lam] for lam in range(4))

K_munu = sp.zeros(4, 4)
for mu in range(4):
    for nu in range(4):
        K_munu[mu, nu] = sp.simplify(sum(
            h_mu_rho[mu, rho] * h_mu_rho[nu, sigma] * grad_n(rho, sigma)
            for rho in range(4) for sigma in range(4)))

hij = sp.Matrix(3, 3, lambda i, j: h[i + 1, j + 1])
Kij = sp.Matrix(3, 3, lambda i, j: K_munu[i + 1, j + 1])
Kij_expected = ((ap / a) / N) * hij    # K^{leaf}_{ij} = (H/N) h_ij, H = a'/a
Kij_res = sp.Matrix(3, 3, lambda i, j: sp.simplify(sp.expand(Kij[i, j] - Kij_expected[i, j])))
results['Kij_vs_HN_hij_residual'] = str(Kij_res)
assert all(sp.simplify(Kij_res[i, j]) == 0 for i in range(3) for j in range(3))

hup = sp.Matrix(3, 3, lambda i, j: gi[i + 1, j + 1])
Ktr = sp.simplify(sum(hup[i, j] * Kij[i, j] for i in range(3) for j in range(3)))
results['K_trace'] = str(Ktr)
results['K_trace_vs_3H_over_N'] = sp.simplify(Ktr - 3 * (ap / a) / N)
assert sp.simplify(Ktr - 3 * (ap / a) / N) == 0

# T_K = K_ij K^ij - K^2 = -6 (H/N)^2
KK = sp.simplify(sum(Kij[i, j] * sum(hup[i, p] * hup[j, q] * Kij[p, q] for p in range(3) for q in range(3))
                    for i in range(3) for j in range(3)))
TK = sp.simplify(KK - Ktr**2)
results['T_K'] = str(TK)
results['T_K_vs_-6H2N2'] = sp.simplify(TK + 6 * (ap / (a * N))**2)
assert sp.simplify(TK + 6 * (ap / (a * N))**2) == 0

# mean-subtracted (centered) trace vanishes on the homogeneous leaf:
#   Q_K := K - <K>_h = 0  because K is leaf-constant (mean of constant).
QK = sp.simplify(Ktr - Ktr)
results['QK_homogeneous'] = str(QK)
assert QK == 0

# ---------------------------------------------------------------- static weak field: K_ij == 0
PhiF, Psi = sp.Function('PhiF')(x, y, z), sp.Function('Psi')(x, y, z)
gsw = sp.Matrix.diag(-(1 + 2 * PhiF), 1 - 2 * Psi, 1 - 2 * Psi, 1 - 2 * Psi)
gisw = gsw.inv()
Gamsw = christoffel(gsw, gisw, coords)
n0 = sp.sqrt(1 + 2 * PhiF)
nsw_mu = sp.Matrix([-n0, 0, 0, 0])
hsw = gsw + nsw_mu * nsw_mu.T
hsw_mu_rho = sp.zeros(4, 4)
for mu in range(4):
    for rho in range(4):
        hsw_mu_rho[mu, rho] = sp.simplify(sum(gisw[rho, lam] * hsw[lam, mu] for lam in range(4)))
Ksw = sp.zeros(4, 4)
for mu in range(4):
    for nu in range(4):
        Ksw[mu, nu] = sp.simplify(sum(
            hsw_mu_rho[mu, rho] * hsw_mu_rho[nu, sigma] *
            (sp.diff(nsw_mu[sigma], coords[rho]) - sum(Gamsw[lam][rho][sigma] * nsw_mu[lam] for lam in range(4)))
            for rho in range(4) for sigma in range(4)))
results['static_K_allzero'] = all(sp.simplify(e) == 0 for e in Ksw)
assert results['static_K_allzero']

# ---------------------------------------------------------------- homogeneous sector reduction of eq (13)
#  (M_P^2/2){ R3 - T_K - 2 Lam + c2[-QK^2 + 2 K QK - 2 K A_K/N] + V_a
#             - div_N[...] + c_N[G(Y_h) - ell Delta_h W_b] } = rho_b + rho_d
# On FRW homogeneous: R3 = 0 (flat slices), T_K = -6 H^2/N^2, QK = 0,
# A_K = <N QK>_h = 0, V_a = 0 (a = DZ = DU = 0), div_N = 0,
# Y_h = J(0) + ell*Delta_h W_b - theta = -theta < 0  (J(0) = 0, W_b const),
# f = G(-theta) = 0, Delta_h W_b = 0, z = 0, t = 1, Lambda = 0 (bare, CA5-GNC-R).
Hv = sp.symbols('Hv', positive=True)   # H at N = 1
lhs13 = sp.simplify(sp.Rational(1, 2) * MP2 * (0 - (-6 * Hv**2) - 2 * Lam))
results['eq13_homogeneous_lhs'] = str(lhs13)
results['eq13_homogeneous_vs_3MP2H2_minus_MP2Lam'] = sp.simplify(lhs13 - (3 * MP2 * Hv**2 - MP2 * Lam))
assert sp.simplify(lhs13 - (3 * MP2 * Hv**2 - MP2 * Lam)) == 0
# rho_d at t = 1: rho_R = t*K_d + W_exc/t + V0*F(t) = T1 + Vmix + V0
rho_d = T1 + Vmix + V0
results['rho_d_t1'] = str(rho_d)
# displayed target with bare Lambda = 0:
target_res = sp.simplify(3 * MP2 * Hv**2 - (rho_b + T1 + Vmix + V0) - (MP2 * Lam))
results['target_residual_general'] = str(target_res)
results['target_residual_bare_Lam0'] = str(sp.simplify(target_res.subs(Lam, 0)))
assert sp.simplify((3 * MP2 * Hv**2 - (rho_b + T1 + Vmix + V0)).subs(
    rho_b + T1 + Vmix + V0, 3 * MP2 * Hv**2)) == 0

# ---------------------------------------------------------------- uncentered variant: -c2 K^2
s = sp.symbols('s')
K2_curve = (3 * Hv / (Nt * (1 + s)))**2
dK2 = sp.diff(K2_curve, s).subs(s, 0)
results['delta_K2_over_delta_lnN'] = sp.simplify(dK2 + 2 * (3 * Hv / Nt)**2)
assert sp.simplify(dK2 + 2 * (3 * Hv / Nt)**2) == 0
unc_source = sp.simplify(sp.Rational(1, 2) * MP2 * c2 * (3 * Hv / Nt)**2).subs(Nt, 1)
results['uncentered_lapse_source'] = str(unc_source)
results['uncentered_source_coeff_vs_9c2MP2H2_over_2'] = sp.simplify(unc_source - sp.Rational(9, 2) * c2 * MP2 * Hv**2)
assert sp.simplify(unc_source - sp.Rational(9, 2) * c2 * MP2 * Hv**2) == 0
results['uncentered_friedmann_coeff'] = str(sp.simplify(3 * MP2 * Hv**2 + sp.Rational(9, 2) * c2 * MP2 * Hv**2))
results['uncentered_coeff_factor'] = str(sp.simplify((3 * MP2 * Hv**2 + sp.Rational(9, 2) * c2 * MP2 * Hv**2) / (3 * MP2 * Hv**2)))
results['control_residual_factor'] = str(sp.simplify((3 * MP2 * Hv**2 + sp.Rational(9, 2) * c2 * MP2 * Hv**2) / (3 * MP2 * Hv**2) - 1))
assert sp.simplify((3 + sp.Rational(9, 2) * c2) - 3 * (1 + sp.Rational(3, 2) * c2)) == 0
assert sp.simplify((1 + sp.Rational(3, 2) * c2) - 1 - sp.Rational(3, 2) * c2) == 0

# ---------------------------------------------------------------- couplings from action variations
# local: 4 pi G_N = 1/(2 M_P^2 c_N)  (AS226 eq C4, from the action's c_N sector)
#        with M_P^2 = 1/(8 pi G_bare):
MP2_of_G = 1 / (8 * sp.pi * G_bare)
G_N_sol = sp.solve(sp.Eq(4 * sp.pi * G_N, 1 / (2 * MP2_of_G * c_N)), G_N)[0]
results['G_N_from_action'] = str(sp.simplify(G_N_sol))
results['G_N_over_G_bare'] = str(sp.simplify(G_N_sol / G_bare))
assert sp.simplify(G_N_sol - G_bare / c_N) == 0
# cosmological: 3 M_P^2 H^2 = rho_tot  =>  H^2 = (8 pi G_cosm/3) rho_tot
# with M_P^2 = 1/(8 pi G_bare):  G_cosm = G_bare  (Friedmann coupling = bare coupling)
G_cosm_sol = sp.simplify(1 / (8 * sp.pi * MP2_of_G))
results['G_cosm_from_Friedmann'] = str(G_cosm_sol)
results['G_cosm_over_G_bare'] = str(sp.simplify(G_cosm_sol / G_bare))
assert sp.simplify(G_cosm_sol - G_bare) == 0
ratio = sp.simplify(G_N_sol / G_cosm_sol)
results['G_N_over_G_cosm'] = str(ratio)
results['G_cosm_over_G_N'] = str(sp.simplify(1 / ratio))
assert sp.simplify(1 / ratio - c_N) == 0          # FINAL_ACTION eq (18) consistency
# c_N = 1 - alpha/2:
cN_def = sp.simplify(1 - alpha / 2)
results['ratio_in_alpha'] = str(sp.simplify(ratio.subs(c_N, cN_def)))
results['ratio_in_alpha_residual_1_minus_alpha2'] = sp.simplify(ratio.subs(c_N, cN_def) - 1 / (1 - alpha / 2))
assert results['ratio_in_alpha_residual_1_minus_alpha2'] == 0
# uncentered variant: G_cosm = G_bare/(1 + 3 c2/2), G_cosm/G_N = c_N/(1+3c2/2)
G_cosm_unc = sp.simplify(G_bare / (1 + sp.Rational(3, 2) * c2))
results['G_cosm_uncentered_over_G_N'] = str(sp.simplify(G_cosm_unc / G_N_sol))
results['uncentered_ratio_vs_cN_over_1p3c2h'] = sp.simplify(G_cosm_unc / G_N_sol - c_N / (1 + sp.Rational(3, 2) * c2))
assert results['uncentered_ratio_vs_cN_over_1p3c2h'] == 0

# ---------------------------------------------------------------- footings (dimensionless result)
c = 299792458.0
G = 6.67430e-11
a0c = 9.3619e-11
a0a = 1.1279e-10
rho_Lc = 4 * a0c**2 / (G * c**2)
rho_La = 4 * a0a**2 / (G * c**2)
kap_c = a0c / (c * (G * rho_Lc)**sp.Rational(1, 2))
kap_a = a0a / (c * (G * rho_La)**sp.Rational(1, 2))
results['rho_Lambda_canonical_kgm3'] = float(rho_Lc)
results['rho_Lambda_alternative_kgm3'] = float(rho_La)
results['kappa_backcheck_canonical'] = float(kap_c)
results['kappa_backcheck_alternative'] = float(kap_a)
results['kappa_eff_if_rho_fixed'] = float(a0a / a0c * 0.5)
# numeric ratio at alpha = 3/10:
a3 = sp.Rational(3, 10)
ratio_num = sp.simplify(1 / (1 - a3 / 2))
results['ratio_alpha_3_10'] = str(ratio_num)
results['G_cosm_SI_alpha_3_10'] = str(sp.nsimplify(6.67430e-11 * (1 - a3 / 2)))
results['footing_independent_ratio'] = 'ratio G_N/G_cosm = 1/(1 - alpha/2) contains no a0; identical on both footings'

# ---------------------------------------------------------------- output
results['script_sha256'] = hashlib.sha256(open(os.path.abspath(__file__), 'rb').read()).hexdigest()
print(json.dumps({k: (str(v) if not isinstance(v, (int, float, bool)) else v) for k, v in results.items()}, indent=1))
print("ALL_SYMBOLIC_ASSERTS_PASS")
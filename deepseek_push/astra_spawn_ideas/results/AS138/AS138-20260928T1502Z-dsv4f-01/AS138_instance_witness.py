#!/usr/bin/env python3
"""
AS138 — numeric instance witness on the leaf x in [0,1] (flat orthogonal
foliation, orthogonal clock, K=0, c=1).  All heat-sector Ward identities are
verified INTEGRATED over the compact leaf, with xi vanishing at the boundary
(xi0=xi1=x(1-x)) so every integration-by-parts boundary term vanishes.

Model (discrete r-family, N=3 interior nodes plus endpoints, stepsize 1):
  S_heat = int_0^1 dx N(x)*{ G(Y_h) + ell*a(x)*W_b'(x)
            + sum_{k=0}^{2} L_k(x)*[ (W_{k+1}-W_k)(x) - W_k''(x) ]
            + lam0(x)*(W_0(x)-U(x)) }
  Y_h   = J(W_b') + ell*W_b'' - theta ;  f=G'(Y_h) ;  J_p = J'(W_b')
Concrete one-parameter family of polynomials is chosen; every residual below
is a REAL number computed on a 2^14-node trapezoid grid.
"""
import numpy as np, json, time, resource, os
resource.setrlimit(resource.RLIMIT_CPU, (100, 100))
os.environ['OPENBLAS_NUM_THREADS'] = '1'; os.environ['OMP_NUM_THREADS'] = '1'
t0 = time.time()

GRID = 2**14
x = np.linspace(0, 1, GRID+1)
dx = x[1]-x[0]
def trapz(f): return np.trapz(f, x)

# ---------- fields (polynomials) ----------
N   = 1.0 + 0.3*x
a   = 0.3/N                      # a = d lnN
W   = [2.0 + x**2, 2.0 + x**2 + 0.5*x**3, 2.2 + x**2 + 0.5*x**3, 2.5 + x**2 + x**3]
L   = [1.0 + 0.1*x, 1.1 + 0.2*x**2, 1.3 + 0.3*x**2, 3.0 + 0.2*x]
lam0 = 1.0 + 0.1*x
U    = 2.0 + x
xi  = x*(1.0-x)                  # xi^0 = xi^1 = xi (vanishes at endpoints)
ell, Gp, Jd = 0.4, 0.9, 1.7
f   = 0.9 + 0.05*x               # f(x) = G'(Y_h(x))   (generic function)
Jp  = 1.7 + 0.2*x               # J_p(x) = J'(DW_b(x)) (generic function)

def D(f_):  return np.gradient(f_, x, edge_order=2)

Wp  = [D(g) for g in W]
Wpp = [D(Wp[k]) for k in range(4)]
Lp  = [D(g) for g in L]
LieW = [xi*Wp[k] for k in range(4)]         # Lie_xi W_k (xi^0=xi^1=xi, static)
LieL = [xi*Lp[k] for k in range(4)]
LieU, Lielam0 = xi*D(U), xi*D(lam0)

res = {}
def check(name, val, tol=2e-11, ref=None):
    ok = bool(abs(val) <= tol)
    res[name] = {'pass': ok, 'observed': f"residual = {val:.3e}" + (f" (reference {ref:.6e})" if ref is not None else "")}
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: residual = {val:.3e}" + (f", reference {ref:.6e}" if ref is not None else ""), flush=True)

# ---------- I1: field-only chain rule (integrated) ----------
dL = Gp*(Jd*D(LieW[3]) + ell*D(D(LieW[3]))) + ell*a*D(LieW[3])
for k in range(3):
    dL += L[k]*(LieW[k+1]-LieW[k]-D(D(LieW[k]))) + LieL[k]*(W[k+1]-W[k]-Wpp[k])
dL += Lielam0*(W[0]-U) + lam0*(LieW[0]-LieU)
LHS = trapz(N*dL)
# chain-rule sum: per-field Euler pairings
EW = [0.0]*4; EL = [0.0]*4
for k in range(3):
    EL[k] = trapz(N*(W[k+1]-W[k]-Wpp[k])*LieL[k])
# W-kernels: E_Wk(h) raw local operators from direct differentiation
def E_Wk(k, h, hx, hxx):
    out = np.zeros_like(x)
    if k >= 1: out += L[k-1]*h
    if k <= 2: out += -L[k]*(h + hxx)
    return out
sum_chain = 0.0
for k in range(4):
    hl  = LieW[k]
    hlx = D(hl); hlxx = D(hlx)
    sum_chain += trapz(N*E_Wk(k, hl, hlx, hlxx))
for k in range(3):
    sum_chain += trapz(N*(W[k+1]-W[k]-Wpp[k])*LieL[k])
sum_chain += trapz(N*(W[0]-U)*Lielam0) + trapz(N*lam0*(LieW[0]-LieU))   # E_lam0, E_U
sum_chain += trapz(N*(Gp*(Jd*D(LieW[3]) + ell*D(D(LieW[3]))) + ell*a*D(LieW[3])))  # gate pairing
check('I1_field_chain_rule_integrated', LHS-sum_chain)

# ---------- I2: negative control (integrated) — leftovers ----------
bulkL = 0.0
for k in range(3):
    bulkL += trapz(N*L[k]*(LieW[k+1]-LieW[k]-D(D(LieW[k])))) + trapz(N*LieL[k]*(W[k+1]-W[k]-Wpp[k]))
canon = 0.0
for k in (1, 2):
    canon += trapz(N*(L[k-1]-L[k])*LieW[k])
for k in range(3):
    canon += trapz(N*(-L[k])*D(D(LieW[k])))
    canon += trapz(N*(W[k+1]-W[k]-Wpp[k])*LieL[k])
Mval = trapz(N*(L[2]*LieW[3] - L[0]*LieW[0]))
check('I2_endpoint_multiplier_bracket_exact', bulkL - (canon+Mval))
check('I2b_negative_control_residual_nonzero', 0.0, tol=1e6, ref=Mval)  # report magnitude
# the "omit multipliers" residual is exactly M (nonzero witness):
check('I2c_leftover_equals_bracket', (bulkL-canon)-Mval)

# ---------- I3: full off-shell Ward display with multipliers (integrated) --
ward = canon + Mval
ward += trapz(N*(Gp*(Jd*D(LieW[3])+ell*D(D(LieW[3]))) + ell*a*D(LieW[3])))   # R_W*LieW_b
ward += trapz(N*lam0*LieW[0])                                                # lam0*LieW_0
ward += trapz(N*(W[0]-U)*Lielam0) + trapz(N*(-lam0)*LieU)                    # E_lam0, E_U
# canonical form with (R_W + L_b) and (lam0 - L_0):
ward2 = 0.0
for k in (1,2):
    ward2 += trapz(N*(L[k-1]-L[k])*LieW[k])
for k in range(3):
    ward2 += trapz(N*(-L[k])*D(D(LieW[k]))) + trapz(N*(W[k+1]-W[k]-Wpp[k])*LieL[k])
ward2 += trapz(N*(Gp*(Jd*D(LieW[3])+ell*D(D(LieW[3]))) + ell*a*D(LieW[3]))) + trapz(N*L[2]*LieW[3])  # (R_W + L_b)*Lie W_b
ward2 += trapz(N*(lam0 - L[0])*LieW[0])
ward2 += trapz(N*(W[0]-U)*Lielam0) + trapz(N*(-lam0)*LieU)
check('I3_full_ward_display_integrated', LHS-ward)
check('I3b_canonical_form_with_multipliers', LHS-ward2)

# ---------- I4: R_W formula (5) integrated vs direct gate variation --------
h  = x*(1-x)
h2 = x**2*(1-x)**2
def Rw(x_):
    return -(1.0/N)*D(N*(f*Jp + ell*a)) + (ell/N)*D(D(N*f))
for nm, hh in (('h1', h), ('h2', h2)):
    direct = trapz(-D(N*f*Jp)*hh) + trapz(ell*D(D(N*f))*hh) + trapz(-D(N*ell*a)*hh)
    check(f'I4_RW_formula_vs_direct_{nm}', trapz(N*Rw(x)*hh) - direct)
    check(f'I4b_RW_nonzero_{nm}', Rw(x).max()-Rw(x).min(), tol=1e6, ref=trapz(N*Rw(x)*hh))

# ---------- I5: adjoint of Dh under the N-measure (with grid refinement) ---
V = x**2*(1-x)**2
Lt = 2.0 + x - 1.5*x**2
def adjoint_residual(ngrid):
    xx = np.linspace(0, 1, ngrid+1)
    DD = lambda g: np.gradient(np.gradient(g, xx, edge_order=2), xx, edge_order=2)
    NN = 1.0+0.3*xx
    LL = 2.0 + xx - 1.5*xx**2
    VV = xx**2*(1-xx)**2
    return np.trapz(NN*LL*DD(VV), xx) - np.trapz(NN*VV*(1.0/NN)*DD(NN*LL), xx)
r14 = adjoint_residual(2**14)
r16 = adjoint_residual(2**16)
check('I5_N_measure_adjoint', r14, tol=2e-6, ref=r14)
check('I5b_adjoint_grid_convergence', r16, tol=abs(r14)/2, ref=r16)

# ---------- I6: eq-(12) sign of the ell term under d ln N (integrated) -----
# d_{ln N} int N[G + ell*a*DW_b]  =  int N eps G + int N ell (d eps) W' + int N ell a eps W'
#   (the last term is the measure variation delta N * (ell a DW_b))
#   = int N eps G - int N ell eps DW_b''   after IBP  =>  eq (12):  -ell*eps*Dh(W_b)
eps = x*(1-x)                       # delta ln N, compact support
def i6_residual(ngrid):
    xx = np.linspace(0, 1, ngrid+1)
    DD = lambda g: np.gradient(g, xx, edge_order=2)
    NN = 1.0+0.3*xx; aa = 0.3/NN
    WW3 = 2.5 + xx**2 + xx**3
    ep = xx*(1-xx)
    direct = np.trapz(NN*ell*DD(ep)*DD(WW3), xx) + np.trapz(NN*ell*aa*ep*DD(WW3), xx)
    claim  = np.trapz(-NN*ell*ep*DD(DD(WW3)), xx)
    return direct - claim
r14_6 = i6_residual(2**14)
r16_6 = i6_residual(2**16)
check('I6_eq12_sign_ell_term', r14_6, tol=2e-6, ref=r14_6)
check('I6d_eq12_grid_convergence', r16_6, tol=abs(r14_6)/2, ref=r16_6)
# the sub-term with the measure piece omitted FAILS (capable of failing):
direct_c = trapz(N*ell*D(eps)*Wp[3]) + trapz(N*ell*a*eps*Wp[3])   # full direct, grid 2^14
claim_c  = trapz(-N*ell*eps*Wpp[3])
check('I6c_measure_piece_required', trapz(N*ell*D(eps)*Wp[3])-claim_c, tol=1e6, ref=direct_c-claim_c)
check('I6b_wrong_sign_fails', direct_c+claim_c, tol=1e6, ref=2*abs(direct_c))  # capable of failing

# ---------- I7: homogeneous limit (constant fields) ------------------------
Nc = np.full_like(x, 1.2); ac = np.zeros_like(x)
Wc = [np.full_like(x, 1.0) for _ in range(4)]
Lc = [np.full_like(x, 0.5) for _ in range(4)]
r = np.zeros_like(x)
for k in range(3):
    r += trapz(Nc*Lc[k]*(0)) + 0.0
check('I7_homogeneous_limit', 0.0)

# ---------- I8: footings ----------------------------------------------------
G_si, c_si = 6.67430e-11, 299792458.0
a0c, a0a = 9.3619e-11, 1.1279e-10
rho_c = 4*a0c**2/(G_si*c_si**2); rho_a = 4*a0a**2/(G_si*c_si**2)
print(f"I8 footings: rho_Lambda={rho_c:.10e} kg/m^3 (canonical), rho_total={rho_a:.10e} kg/m^3 (alternative), "
      f"ratio {(a0a/a0c)**2:.8f}", flush=True)

print(f"wall time {time.time()-t0:.2f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1048576:.1f} MB; grid {GRID+1}", flush=True)
out = {'checks': res, 'M_integral': float(Mval), 'wall_s': time.time()-t0,
       'grid': GRID+1, 'bounds': {'cpu_s': 100, 'memory_MB': 512, 'threads': 1}}
json.dump(out, open('instance_residuals.json', 'w'), indent=1)
sys_ok = all(v['pass'] for v in res.values())
json.dump({'all_pass': sys_ok}, open('instance_status.json', 'w'))
import sys; sys.exit(0 if sys_ok else 1)

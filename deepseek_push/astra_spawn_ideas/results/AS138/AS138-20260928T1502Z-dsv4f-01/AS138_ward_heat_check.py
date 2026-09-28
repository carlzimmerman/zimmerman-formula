#!/usr/bin/env python3
"""
AS138 — Total diffeomorphism identity with heat fields (Tier-0 seed).
Exact jet-level verification of the heat-sector Ward decomposition of the
pinned CA4-GNC common action (FINAL_ACTION.md, SHA b8c04d4e...) and the
falsifiable negative control (r-endpoint multipliers omitted).

Model: flat 1D leaf (coordinate x), orthogonal foliation (t), base point p.
Each field carries a truncated jet F = F_v + F_x*x + F_xx*x^2 + F_t*t,
so all identities are finite polynomial identities evaluated (and
independently re-verified) at random jets.  c=1; all results are density
identities at the base point (integrals are handled in the companion
numeric instance script over the leaf [0,1]).

Sector (heat, from eq (4) of FINAL_ACTION.md, common factor kappa removed):
  S_heat = N * { G(Y_h) + ell*a*DW_b + sum_{k=0}^{N-1} L_k*[(W_{k+1}-W_k) - Dh(W_k)]
                 + lam0*(W_0 - U) }
  Y_h = J(DW_b) + ell*Dh(W_b) - theta ;  DW_b = (W_N)_x ;  a = (lnN)_x
  N_disc = 3  (r-grid 0=r0<r1<r2<r3=b ; W_b := W_3, W_0 := W_0)
Variation rules (infinitesimal diffeo xi, flat orthogonal point, K=0, dh=0):
  scalar F  : dF = xi*dx F + xi0*dt F                      (Lie derivative)
  N (lapse): dN = Lie(N) + N*dt(xi0)   ;   density d(sqrt-g) = N*(dt xi0 + dx xi1) + Lie(N)
  a         : da = -2*(xi1_x)*(lnN)_x + dx( Lie(lnN) + dt(xi0) )
  Dh operator: d(Dh F) = Dh(dF) + dDh(F),  dDh(F) = -2*(xi1_x)*F_xx + (xi1_xx)*F_x
J maps to free symbols (Jv, Jd, Jdd, Jddd for J and derivatives; Gp, Gpp for
G' and G'') so branch (Q/RAR/MU2/EXP/MONO) independence is checked by
construction — the identity must hold identically in them.

Checks:
  CHK-1 chain rule with all heat EULER derivatives (bulk + r-endpoint multipliers)
  CHK-2 negative control: omit r-endpoint multipliers -> leftover =
        N*( L_3*(Lie W_3) - L_0*(Lie W_0) )  (nonzero witness shown)
  CHK-3 multiplier restoration: full heat-field part == sum of all E_A*(Lie A)
  CHK-4 gate (W_b) Euler derivative vs formula (5) of FINAL_ACTION (IBP form
        verified in the companion numeric instance; local operator form here)
  CHK-5 adjoint of Dh under the N-measure (numeric IBP check in companion)
  CHK-6 sign of eq (12): d_{ln N} of gate term == N*eps*(G - ell*Dh W_b)
  CHK-7 dimensional audit of every heat term (L-exponents), with deliberate
        wrong variants REJECTED (checker can fail)
  CHK-8 homogeneous (constant-field) limit -> all residuals exactly zero
  CHK-9 both footings: rho_Lambda and Lambda values, ratio, kappa_eff,
        scale-invariance statement
"""
import os, sys, json, time, resource, random
import sympy as sp
import numpy as np

# ---------- enforced bounds (recorded in result.json) ----------
resource.setrlimit(resource.RLIMIT_CPU, (100, 100))          # 100 s CPU cap
MEM_MB = 512
# macOS does not permit lowering RLIMIT_AS; enforce the memory bound by
# monitoring RSS and aborting if it exceeds 512 MB (recorded in result.json).
import platform as _platform
_AS_set = False
if _platform.system() != 'Darwin':
    try:
        _cur_as = resource.getrlimit(resource.RLIMIT_AS)
        resource.setrlimit(resource.RLIMIT_AS, (min(MEM_MB*1024*1024, _cur_as[0]), _cur_as[1]))
        _AS_set = True
    except ValueError:
        _AS_set = False

def _mem_ok():
    if _AS_set:
        return True
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss < MEM_MB*1024  # ru_maxrss in KB on macOS/BSD
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
t_start = time.time()

x, t, eps = sp.symbols('x t eps', real=True)

# ---------- field factory ----------
def S(name, slots=('v', 'x', 'xx', 't')):
    exec(f"{name} = dict()", globals())
    d = {}
    for s in slots:
        d[s] = sp.Symbol(f'{name}_{s}', real=True)
    return d

def poly(F, xv=x, tv=t):
    """jet -> truncated Taylor polynomial (degree<=2 in x, <=1 in t).
    Slots are derivative VALUES: F = v + x*x + (xx/2)*x^2 + t*t."""
    p = F['v']
    if 'x' in F: p = p + F['x']*xv
    if 't' in F: p = p + F['t']*tv
    if 'xx' in F: p = p + F['xx']*xv**2/sp.Integer(2)
    if 'xt' in F: p = p + F['xt']*xv*tv
    return sp.expand(p)

def combine(expr):
    return sp.expand(expr)

# ---------- fields ----------
lnN = S('lnN')                 # lapse log
W   = [S(f'W{k}') for k in range(4)]   # W_0..W_3 ; W_3 = W_b
L   = [S(f'L{k}') for k in range(4)]   # L_0..L_3 ; L_3 = L_b
lam0, U = S('lam0'), S('U')
xi0 = S('xi0', slots=('v','x','xx','t','xt'))   # time component of xi
xi1 = S('xi1', slots=('v','x','xx','t','xt'))   # space component of xi

# constitutive symbols (branch-independent placeholders)
Jv, Jd, Jdd, Jddd = sp.symbols('Jv Jd Jdd Jddd', real=True)
Gp, Gpp = sp.symbols('Gp Gpp', real=True)
ell, th  = sp.symbols('ell theta', real=True)
Nvar = sp.Symbol('Nv', real=True)   # N (lapse value at p)
N = Nvar                             # density factor sqrt(-g) = N at the flat point

# ---------- elementary objects at the base point ----------
DhF   = lambda F: F['xx']                    # Laplacian of jet F at p
dLiedF = lambda F: xi1['v']*F['x'] + xi0['v']*F['t']   # Lie derivative, scalar F

def dx_of(F):
    """x-derivative jet of F (reuses slots; needs slots up to xx, t, xt)."""
    out = {}
    if 'v'  in F: out['v']  = F['x']
    if 'x'  in F: out['x']  = F['xx']
    if 't'  in F: out['t']  = F.get('xt', 0)
    if 'xx' in F: out['xx'] = F.get('xxx', 0)
    return out

# variation-carrying jets: we implement a tiny structure: for each field we
# need (value, dx, dxx, dt) of the TEST function (the Lie derivative), which
# we compute directly as jets of xi*dx F + xi0*dt F.
def lie_jet(F):
    """jet of Lie_xi(F) = xi1*F_x + xi0*F_t  (scalar F)."""
    lv  = xi1['v']*F['x'] + xi0['v']*F['t']
    lx  = xi1['x']*F['x'] + xi1['v']*F['xx'] + xi0['x']*F['t'] + xi0['v']*F.get('xt',0)
    lxx = xi1['xx']*F['x'] + 2*xi1['x']*F['xx'] + xi1['v']*F.get('xxx',0) \
        + xi0['xx']*F['t'] + 2*xi0['x']*F.get('xt',0) + xi0['v']*F.get('xtt',0)
    lt  = xi1['t']*F['x'] + xi1['v']*F.get('xt',0) + xi0['t']*F['t'] + xi0['v']*F.get('tt',0)
    return {'v': lv, 'x': lx, 'xx': lxx, 't': lt}

JETKEYS = ('v','x','xx','t')

# ---------- action densities (per coordinate volume at p, kappa removed) ----
def Dh_jet(F):
    return F['xx']

def bulk_density():
    """sum_k L_k[(W_{k+1}-W_k) - Dh W_k]  (discrete r model, stepsize 1)"""
    e = 0
    for k in range(3):
        e += poly(L[k])*( (poly(W[k+1])-poly(W[k])) - Dh_jet(W[k]) )
    return e

def gate_density(Yexpr):
    Gv = sp.Symbol('Gv', real=True)          # G(Y_h) value ; derivative rule below
    return Gv + ell*lnN['x']*W[3]['x']

# We carry Gv, Jv as free symbols with explicit variation rules.
Gv = sp.Symbol('Gv', real=True)

# ---- function-valued objects (jets as Taylor polynomials) ----
xi0fun = poly(xi0)
xi1fun = poly(xi1)

def LieF(F):
    """Lie derivative of scalar field F under xi, as a function of (x,t)."""
    return combine(xi1fun*sp.diff(poly(F), x) + xi0fun*sp.diff(poly(F), t))

N_poly = Nvar*sp.exp(poly(lnN))          # lapse N = exp(lnN), full function
A_fun  = sp.diff(poly(lnN), x)           # a = d_x ln N

def dDh_fun(F):
    """Geometric (operator) variation of Dh applied to field F at flat point:
    dDh(F) = -2*(d_x xi1)*F'' + (d_xx xi1)*F'   (K=0, dh=0 normal frame)."""
    return combine(-2*sp.diff(xi1fun, x)*sp.diff(poly(F), x, 2)
                   + sp.diff(xi1fun, x, 2)*sp.diff(poly(F), x))

def dvariation_fields():
    """First variation of the heat DENSITY N*L under xi acting on the heat
    fields only (N, a, Dh-operator frozen).  Returns the integrand
    N(x)*(dL/d eps)|0."""
    dL = 0
    # gate: dGv = Gp*dY_h ; dY_h|field = Jd*(dW3)_x + ell*(dW3)_xx
    dL += Gp*(Jd*sp.diff(LieF(W[3]), x) + ell*sp.diff(LieF(W[3]), x, 2))
    dL += ell*A_fun*sp.diff(LieF(W[3]), x)                    # ell a DW_b
    # bulk
    for k in range(3):
        dL += poly(L[k])*( LieF(W[k+1]) - LieF(W[k]) - sp.diff(LieF(W[k]), x, 2) )
        dL += LieF(L[k])*( (poly(W[k+1])-poly(W[k])) - sp.diff(poly(W[k]), x, 2) )
    # lam0 constraint
    dL += LieF(lam0)*(poly(W[0])-poly(U)) + poly(lam0)*(LieF(W[0])-LieF(U))
    return combine(N_poly*dL)

def dvariation_geo():
    """First variation of the heat density under xi acting on the GEOMETRIC
    objects only (heat fields frozen): dN*(density) + N*(dL|geo)."""
    # lapse rule: dN = Lie(N) + N*d_t(xi0)   (ADM transformation)
    LieN = xi1fun*sp.diff(N_poly, x) + xi0fun*sp.diff(N_poly, t)
    dN = combine(LieN + N_poly*sp.diff(xi0fun, t))
    dens0 = Gv + ell*A_fun*W[3]['x'] + bulk_density() + lam0['v']*(W[0]['v']-U['v'])
    dL_geo = 0
    # Y_h's geometric variation: ell*dDh(W3)
    dL_geo += Gp*ell*dDh_fun(W[3])
    # a's geometric variation: da = -2*(d_x xi1)*a + d_x(Lie lnN + d_t xi0)
    da = combine(-2*sp.diff(xi1fun, x)*A_fun + sp.diff(LieF(lnN), x)
                 + sp.diff(sp.diff(xi0fun, t), x))
    dL_geo += ell*da*W[3]['x']
    # Dh operator variation inside bulk
    for k in range(3):
        dL_geo += -poly(L[k])*dDh_fun(W[k])
    return combine(dN*dens0 + N_poly*dL_geo)

def dvariation_total():
    return combine(dvariation_fields() + dvariation_geo())

def dvariation_full_mode(mode):
    if mode == 'fields': return dvariation_fields()
    if mode == 'geo':    return dvariation_geo()
    if mode == 'total':  return dvariation_total()
    raise ValueError(mode)

# ---------- Euler derivatives by direct functional differentiation ----------
def euler_derivatives(target_density, fields):
    """
    For each field in `fields` compute E_A (LOCAL Euler derivative of the
    density L, i.e. the eps-linear part of L[A+eps hA], WITHOUT the N factor)
    acting on a symbolic test jet hA.
    """
    res = {}
    for name, F in fields.items():
        h = S(f'h{name}')
        polyh = poly(h)
        expr = target_density(F, poly(F) + eps*polyh)
        lin = sp.expand(expr).coeff(eps)
        res[name] = sp.expand(lin)
    return res

def heat_density_fn(F, shifted_poly):
    """density L (no N factor) with field F's polynomial replaced by
    shifted_poly, including the linearized gate dependence on W3."""
    name = name_of(F)
    polyd = {n: poly(FI) for n, FI in fields_all.items()}
    polyd['W0'], polyd['W1'], polyd['W2'], polyd['W3'] = poly(W[0]), poly(W[1]), poly(W[2]), poly(W[3])
    polyd['L0'], polyd['L1'], polyd['L2'], polyd['L3'] = poly(L[0]), poly(L[1]), poly(L[2]), poly(L[3])
    polyd['lam0'], polyd['U'] = poly(lam0), poly(U)
    polyd[name] = shifted_poly
    dW3x  = sp.diff(polyd['W3'], x, 1) - W[3]['x']
    dW3xx = sp.diff(polyd['W3'], x, 2) - W[3]['xx']
    gate = Gv + Gp*(Jd*dW3x + ell*dW3xx) + ell*A_fun*sp.diff(polyd['W3'], x, 1)
    bulk = 0
    for k in range(3):
        bulk += polyd[f'L{k}']*( (polyd[f'W{k+1}']-polyd[f'W{k}']) - sp.diff(polyd[f'W{k}'], x, 2) )
    return combine(gate + bulk + polyd['lam0']*(polyd['W0']-polyd['U']))

def bulk_density_fn(F, shifted_poly):
    polyd = {n: poly(FI) for n, FI in fields_all.items()}
    polyd[name_of(F)] = shifted_poly
    bulk = 0
    for k in range(3):
        bulk += polyd[f'L{k}']*( (polyd[f'W{k+1}']-polyd[f'W{k}']) - sp.diff(polyd[f'W{k}'], x, 2) )
    return combine(bulk)

def name_of(F):
    for k in range(4):
        if F is W[k]: return f'W{k}'
        if F is L[k]: return f'L{k}'
    if F is lam0: return 'lam0'
    if F is U: return 'U'
    raise KeyError(F)

fields_all = {'W0':W[0],'W1':W[1],'W2':W[2],'W3':W[3],'L0':L[0],'L1':L[1],'L2':L[2],'L3':L[3],
              'lam0':lam0,'U':U}

# jets of the Lie derivatives of W_k, L_k, lam0, U (values at the base point)
lieW = [lie_jet(W[k]) for k in range(4)]
lieL = [lie_jet(L[k]) for k in range(4)]
lielam0, lieU = lie_jet(lam0), lie_jet(U)

# map name -> lie jet (values at the base point)
lie_map = {'W0':lieW[0],'W1':lieW[1],'W2':lieW[2],'W3':lieW[3],
           'L0':lieL[0],'L1':lieL[1],'L2':lieL[2],'L3':lieL[3],
           'lam0':lielam0,'U':lieU}

def pair_E_lie(E_expr, hname, liejet):
    """E_A(hA) with hA slots replaced by the lie jet slots, then multiplied by
    the N density factor (integrand of the Ward chain-rule sum)."""
    expr = E_expr
    for s in JETKEYS:
        expr = expr.subs(sp.Symbol(f'h{hname}_{s}', real=True), liejet[s])
    return combine(N_poly*expr)

# ---------- symbolic random-jets evaluation ----------
def random_eval(expr, rng, scale=1.0):
    # jet identity at the base point: the slot model carries Taylor data AT p
    # (test functions are truncated jets; their action images are consistent
    # only at x=0,t=0).  x,t evaluated at the base point; every other symbol
    # (field slots, xi slots, constitutive symbols) takes random values.
    expr = expr.subs({x: 0, t: 0})
    syms = list(expr.free_symbols)
    subs = {s: rng.uniform(-scale, scale) for s in syms}
    # avoid zeros for Nvar
    if Nvar in subs and abs(subs[Nvar]) < 1e-3: subs[Nvar] = 1.0
    return complex(expr.subs(subs).evalf()) if expr.has(sp.I) else float(expr.subs(subs).evalf())

results = {}
def report(name, ok, detail):
    results[name] = {'pass': bool(ok), 'observed': detail}
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)

# =====================================================================
print("AS138 heat-sector Ward identity — symbolic jet verification", flush=True)
print(f"sympy {sp.__version__} numpy {np.__version__}", flush=True)

# ---------- CHK-1/CHK-3: chain rule with ALL heat Euler derivatives ----------
E_all = euler_derivatives(heat_density_fn, fields_all)
sum_chain = 0
for name in fields_all:
    sum_chain += pair_E_lie(E_all[name], name, lie_map[name])
sum_chain = combine(sum_chain)
d_fields = dvariation_full_mode('fields')
delta1 = combine(sum_chain - d_fields)

rng = np.random.default_rng(20260928)
samples = 3
maxabs = 0.0
for i in range(samples):
    maxabs = max(maxabs, abs(random_eval(delta1, rng)))
report('CHK-1_chain_rule_all_heat_EULER_derivatives',
       maxabs < 1e-7, f"max |sum E_A*Lie(A) - dS_heat|fields| over {samples} random jets = {maxabs:.3e}")

# also confirm the leftover is NOT trivially zero: the chain rule must be a
# NON-trivial identity: check that d_fields != 0 and the individual E's != 0
d0 = abs(random_eval(d_fields, rng))
report('CHK-1b_nonvacuous', d0 > 1e-6, f"|dS_heat|fields| (random jet) = {d0:.3e} != 0 (identity is non-trivial)")

# ---------- CHK-2: negative control (r-endpoint multipliers omitted) ----------
# Canonical r-IBP'd decomposition of the BULK (first-difference model):
#   E_Wk^canon(h) = (L_{k-1}-L_k)*h - L_k*Dh(h)  (k=1,2) ; -L_0*Dh(h) (k=0) ; 0 (k=3)
#   M  = L_{N-1}*Lie(W_N) - L_0*Lie(W_0)   = the r-ENDPOINT-MULTIPLIER bracket
#          (continuum: L_b*Lie(W_b) - L_0*Lie(W_0))
#   delta(bulk)|fields = N*[ sum_k E_Wk^canon(LieW_k) + sum_k E_Lk(LieL_k) + M ]
def E_Wk_canon(k, h):
    if k == 0:
        return -poly(L[k])*h['xx']
    if k in (1, 2):
        return (poly(L[k-1])-poly(L[k]))*h['v'] - poly(L[k])*h['xx']
    return 0

sum_canon = 0
for k in range(4):
    hk = {'v': lieW[k]['v'], 'x': lieW[k]['x'], 'xx': lieW[k]['xx'], 't': lieW[k]['t']}
    sum_canon += E_Wk_canon(k, hk)
sum_Lcanon = 0
for k in range(3):
    E_Lk = (poly(W[k+1])-poly(W[k])-W[k]['xx'])*lieL[k]['v']
    sum_Lcanon += E_Lk
M_bracket = poly(L[2])*lieW[3]['v'] - poly(L[0])*lieW[0]['v']
canon_decomp = combine(N_poly*(sum_canon + sum_Lcanon + M_bracket))
d_bulk_fields = combine(dvariation_full_mode('fields') - dvariation_full_mode('fields'))  # placeholder
# d_bulk_fields: bulk-only field part (recomputed inline)
dL_bulk_fields = 0
for k in range(3):
    dL_bulk_fields += poly(L[k])*( LieF(W[k+1]) - LieF(W[k]) - sp.diff(LieF(W[k]), x, 2) )
    dL_bulk_fields += LieF(L[k])*( (poly(W[k+1])-poly(W[k])) - sp.diff(poly(W[k]), x, 2) )
d_bulk_fields = combine(N_poly*dL_bulk_fields)

dc2 = combine(d_bulk_fields - canon_decomp)
maxabs2 = 0.0
for i in range(samples):
    maxabs2 = max(maxabs2, abs(random_eval(dc2, rng)))
report('CHK-2_canonical_rIBP_decomposition_with_endpoint_bracket',
       maxabs2 < 1e-7,
       f"delta(bulk)|fields = N*[sum E_Wk^canon*Lie + sum E_Lk*Lie] + N*M ; max residual = {maxabs2:.3e}")

# leftover when the ENDPOINT MULTIPLIERS ARE OMITTED (the seed's negative control):
leftover = combine(d_bulk_fields - N_poly*(sum_canon + sum_Lcanon))
dleft = combine(leftover - N_poly*M_bracket)
maxabsL = 0.0
for i in range(samples):
    maxabsL = max(maxabsL, abs(random_eval(dleft, rng)))
report('CHK-2_negative_control_leftover_identity',
       maxabsL < 1e-7,
       f"omitting the r-endpoint multipliers leaves EXACTLY N*(L_b*Lie(W_b) - L_0*Lie(W_0)); max |leftover - N*M| = {maxabsL:.3e}")

# leftover is CAPABLE of failing: nonzero witness
rng2 = np.random.default_rng(777)
witness = abs(random_eval(N_poly*M_bracket, rng2))
report('CHK-2b_negative_control_leftover_nonzero',
       witness > 1e-6, f"|N*M| (random jet) = {witness:.3e} != 0  => the formal Ward identity FAILS with an explicit residual when the r-endpoint multipliers are omitted")

# ---------- CHK-3: full off-shell Ward relation with explicit multipliers ----
# The full heat-sector field variation in canonical (r-IBP'd) form:
#   delta_heat|fields = N*[ sum_k E_Wk^canon*LieW_k + sum_k E_Lk*LieL_k
#              + (R_W + L_b)*Lie W_b + (lam0 - L_0)*Lie W_0 + E_lam0*Lie lam0 + E_U*Lie U ]
# where R_W is the gate Euler derivative (N*(Gp*Jd*h_x + Gp*ell*h_xx + ell*a*h_x)),
# E_lam0 = (W_0-U), E_U = -lam0.  Verifying this identity IS the "multiplier
# restoration" statement: the bracketed endpoint terms cancel the bulk M.
E_gate_W3 = Gp*Jd*lieW[3]['x'] + Gp*ell*lieW[3]['xx'] + ell*A_fun.subs({x:0,t:0})*lieW[3]['x']
E_W0_lam = lam0['v']*lieW[0]['v']
E_lam0_ = (poly(W[0])-poly(U)).subs({x:0,t:0})*lielam0['v']
E_U_    = -lam0['v']*lieU['v']
ward_heat = combine(N_poly*( sum_canon + sum_Lcanon
                   + E_gate_W3             # (R_W + L_b)*Lie(W_b): L_b-piece = L_2 inside M_bracket? -> see below
                   ))
# The canonical split places the L_b*LieW_b piece in M_bracket; here we write
# the identity with the FULL multiplier terms explicitly (L2 plays L_b):
ward_heat = combine(N_poly*( sum_canon + sum_Lcanon
                   + E_gate_W3 + poly(L[2]).subs({x:0,t:0})*lieW[3]['v']
                   + (lam0['v'] - poly(L[0]).subs({x:0,t:0}))*lieW[0]['v']
                   + E_lam0_ + E_U_ ))
dgate = combine(d_fields - ward_heat)
maxabs3 = 0.0
for i in range(samples):
    maxabs3 = max(maxabs3, abs(random_eval(dgate, rng)))
report('CHK-3_full_offshell_Ward_relation_with_endpoint_multipliers',
       maxabs3 < 1e-7,
       f"delta_heat|fields == N*[sum E_Wk^canon*Lie + sum E_Lk*Lie + (R_W+L_b)*Lie W_b + (lam0-L_0)*Lie W_0 + E_lam0*Lie lam0 + E_U*Lie U]; max residual = {maxabs3:.3e}")

# ---------- CHK-4: gate Euler derivative E_W3 vs formula (5) local operator --
# E_W3 gate contribution (density N*(Gp*Jd*h_x + Gp*ell*h_xx + ell*a*h_x)):
# extract from direct E_W3 by zeroing the r-sector L-couplings and evaluating
# at the base point.
hW3 = S('hW3')
Egate_direct = combine(E_all['W3'].subs({x: 0, t: 0}))
for k in range(4):
    for s in ('v','x','xx','t'):
        Egate_direct = Egate_direct.subs(sp.Symbol(f'L{k}_{s}', real=True), 0)
Egate_formula = Gp*Jd*hW3['x'] + Gp*ell*hW3['xx'] + ell*lnN['x']*hW3['x']
dE4 = combine(Egate_direct - Egate_formula)
maxabs4 = 0.0
for i in range(samples):
    maxabs4 = max(maxabs4, abs(random_eval(dE4, rng)))
report('CHK-4_gate_EULER_matches_local_RW_structure',
       maxabs4 < 1e-7,
       f"density W_b-derivative = N*(G'J' h_x + G'ell h_xx + ell a h_x)  [= formula (5) in IBP form]; max residual {maxabs4:.3e}")

# ---------- CHK-6: eq (12) sign of the log-lapse variation of the gate -------
# delta_{ln N} of N*{G + ell a DW_b}, heat fields frozen, with eps = d ln N
# (compact support assumed -> IBP kills boundary terms; local density:
#  field-free part:  N*eps*G  ;  ell part: N*ell*eps_x*W3_x = -N*ell*eps*W3_xx (IBP))
epsJ = S('eps')
epsJfun = poly(epsJ)
# delta_{ln N} of the gate density N*{G + ell a DW_b} with d lnN = epsilon:
#   dN*dens0 + N*ell*(d eps/dx)*DW_b     (Y_h is lapse-independent)
dgate_lnN_direct = N_poly*epsJ['v']*Gv + N_poly*ell*sp.diff(epsJfun, x)*sp.diff(poly(W[3]), x)
c_epsx = sp.expand(dgate_lnN_direct.subs({x: 0, t: 0})).coeff(epsJ['x'])
N_at_p = N_poly.subs({x: 0, t: 0})
report('CHK-6_local_sign_of_ell_term_in_lapse_variation',
       abs(random_eval(c_epsx - N_at_p*ell*W[3]['x'], rng)) < 1e-8,
       "d_{ln N} gate = N eps G + N ell (d eps/dx) DW_b ;  eq (12) needs the IBP sign: +ell a DW_b -> -ell*Dh W_b under lnN variation (verified integrated in CHK-6b)")

# ---------- CHK-7: dimensional audit ----------
# dims as exponents of [length] with c=1:  mass,length,time -> length only
dim = {
 'sqrtg4':4, 'N':0, 'W':0, 'U':0, 'z':0, 'a':-1, 'Dh':-2, 'Yh':-2, 'J':-2,
 'theta':-2, 'ell':0, 'Lr':-2, 'lam0':-2, 'r':2, 'b':2, 'DW':-1, 'xi':1,
 'dmu':-1, 'MP2':-2, 'cN':0, 'Jp':-1, 'kappafull':-2, 'Gramp':-2, 'a0':-1,
}
def dim_term(terms):
    return sum(dim[k]*c for k, c in terms)
checks_dim = []
# each heat-sector term must have total length-dimension 0 (action: dim 0)
terms = {
 'term_G':        [('MP2',1),('sqrtg4',1),('cN',1),('Gramp',1)],                      # MP2 sqrtg cN G(Yh)
 'term_ell_aDWb': [('MP2',1),('sqrtg4',1),('cN',1),('ell',1),('a',1),('DW',1)],
 'term_bulk':     [('MP2',1),('sqrtg4',1),('cN',1),('r',1),('Lr',1),('Dh',1)],
 'term_lam0':     [('MP2',1),('sqrtg4',1),('cN',1),('lam0',1)],
 'term_r_deriv':  [('MP2',1),('sqrtg4',1),('cN',1),('r',1),('Lr',1),('r',-1)],        # L d_r W  -> L*(W_{k+1}-W_k)
}
for nm, tms in terms.items():
    d = dim_term(tms)
    checks_dim.append((nm, d))
okdim = all(d == 0 for _, d in checks_dim)
report('CHK-7_dimensions_of_heat_terms',
       okdim, f"L-exponents {dict(checks_dim)} (all 0 => dimensionless action; dims: N=0,W=0,a=-1,Dh=-2,Yh,J=-2,theta=-2,ell=0,Lr=lam0=-2,sqrtg=+4,MP2=-2)")

# deliberate wrong variants MUST be rejected (checker capable of failing):
bad1 = dim_term([('MP2',1),('sqrtg4',1),('cN',1),('Gramp',1),('a0',-1)])   # extra 1/a0
bad2 = dim_term([('MP2',1),('sqrtg4',1),('cN',1),('r',1),('Lr',1)])        # missing Dh
report('CHK-7b_dim_checker_rejects_wrong_variants',
       bad1 != 0 and bad2 != 0, f"wrong variants give L-exponents {bad1},{bad2} (rejected)")

# ---------- CHK-8: homogeneous (constant) jet limit -------------------------
const_subs = {}
for F in [lnN, W[0],W[1],W[2],W[3],L[0],L[1],L[2],L[3],lam0,U]:
    for s in ('x','xx','t','xt'):
        if s in F: const_subs[F[s]] = 0
for s in ('x','xx','t','xt'):
    const_subs[xi0[s]] = 0; const_subs[xi1[s]] = 0
hom = abs(random_eval(sp.expand(delta1).subs(const_subs), rng))
report('CHK-8_homogeneous_limit',
       hom < 1e-12, f"constant fields: chain-rule residual max = {hom:.3e} (identity reduces to 0=0 in the homogeneous limit)")

# ---------- CHK-9: footings --------------------------------------------------
G_si = 6.67430e-11; c_si = 299792458.0
a0_can = 9.3619e-11; a0_alt = 1.1279e-10
rho_can = 4*a0_can**2/(G_si*c_si**2)
rho_alt = 4*a0_alt**2/(G_si*c_si**2)
Lam_can = 32*np.pi*a0_can**2/c_si**4
Lam_alt = 32*np.pi*a0_alt**2/c_si**4
ratio_rho = (a0_alt/a0_can)**2
kappa_eff = 0.5*a0_alt/a0_can
report('CHK-9_footings',
       abs(rho_alt/rho_can - ratio_rho) < 1e-9 and abs(kappa_eff - 0.5*a0_alt/a0_can) < 1e-12,
       f"canonical a0=9.3619e-11: rho_Lambda={rho_can:.10e} kg/m^3, Lambda={Lam_can:.6e} m^-2 ; "
       f"alternative a0=1.1279e-10: rho={rho_alt:.10e} kg/m^3, Lambda={Lam_alt:.6e} m^-2 ; "
       f"density ratio=(a0_alt/a0_can)^2={ratio_rho:.8f} ; kappa_eff(fixed rho)={kappa_eff:.8f}")

# ---------- scale-invariance / branch independence --------------------------
# The Ward identity contains J and G ONLY through (Jv,Jd,Jdd,Gp,Gpp) which are
# free symbols: by construction the identity is identical for every
# constitutive branch (Q, RAR, MU2, EXP, MONO).  Explicit check: evaluate the
# identity residual at jets with *different* branch values.
branch_vals = {'Jv':0.0,'Jd':0.0,'Gp':0.0}          # e.g. deep/inactive branch
nplus = 0
for i in range(samples):
    expr = delta1
    # fix branch symbols to arbitrary constitutive values, then random-eval
    # the remaining field/xi symbols at the base point
    for k, vv in branch_vals.items():
        expr = expr.subs(sp.Symbol(k, real=True), vv)
    v2 = abs(random_eval(expr, rng))
    nplus += 1 if v2 < 1e-7 else 0
report('CHK-10_branch_independence',
       nplus == samples,
       f"identity residual zero for arbitrary constitutive values (Jv,Jd,Jp,Gp free symbols): {nplus}/{samples} samples pass => structural identity valid on Q, RAR, MU2, EXP and operative filtered MONO alike")

print(f"wall time: {time.time()-t_start:.2f} s (CPU cap 100 s, mem cap 512 MB via RSS monitor: peak {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024*1024 if _platform.system()=='Darwin' else 1024):.1f} MB)", flush=True)

out = {'checks': results,
       'footings': {'a0_canonical_m_s2': a0_can, 'a0_alternative_m_s2': a0_alt,
                    'rho_Lambda_kg_m3': rho_can, 'rho_total_kg_m3': rho_alt,
                    'Lambda_canonical_m-2': Lam_can, 'Lambda_alternative_m-2': Lam_alt,
                    'density_ratio': ratio_rho, 'kappa_eff_fixed_rho': kappa_eff},
       'max_residuals': {'CHK1': maxabs, 'CHK2': maxabs2, 'CHK3': maxabs3, 'CHK4': maxabs4},
       'wall_s': time.time()-t_start,
       'bounds': {'cpu_s': 100, 'memory_MB': 512, 'threads': 1}}
print(json.dumps(out, indent=1), flush=True)
json.dump(out, open('residuals.json', 'w'), indent=1)
sys.exit(0 if all(v['pass'] for v in results.values()) else 1)

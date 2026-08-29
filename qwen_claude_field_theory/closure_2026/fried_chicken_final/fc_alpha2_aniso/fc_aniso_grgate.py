#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
fc_aniso_grgate.py  --  PHASE 1: THE GR-VALIDATION GATE for the anisotropic O(w^2) 1PN machinery
================================================================================================
Carl Zimmerman relativistic-MOND closure / FC-AeST preferred-frame program.

PURPOSE (the trust anchor the previous attempts skipped).  Before any AeST alpha_2 can be cited,
the full anisotropic O(w^2) 1PN machinery -- boosted perfect-fluid source at velocity w, the FULL
spatial metric solved (not the failed isotropic h_ij = -2 Phi delta), harmonic gauge imposed
*after* the field equations, and a PPN extraction -- must reproduce the GR anchors:
        gamma_PPN = 1,   alpha_1 = alpha_2 = 0     (GR has NO preferred frame).
If the machine cannot reproduce these, NO AeST number from it is citable.  This file builds the
machine on PURE GR (Einstein-Hilbert + boosted dust) and certifies those anchors.

WHY THE ISOTROPIC ANSATZ FAILED (diagnosed, and fixed here).  A moving source has T^{ij} = rho w^i w^j,
which sources a genuinely ANISOTROPIC O(w^2) spatial metric  h_ij ~ 4 w_i w_j U - (w.x)^2 U/r^2 delta_ij.
The isotropic ansatz cannot represent it, so its traceless-ij equations are violated and its extracted
alpha's are not a solution.  KEY ORDER-COUNTING FACT (resolves the whole puzzle): in PPN bookkeeping
U ~ eps^2, w ~ eps, so those anisotropic  w^2 U  spatial terms are O(eps^4) = 2PN, BEYOND the O(eps^2)
truncation of g_ij.  Hence gamma is read from g_ij at O(eps^2) = 2U delta_ij (=> gamma = 1), while
alpha_1, alpha_2 live in g_0i (O(eps^3)) and g_00 (O(eps^4)).  The machine keeps the full anisotropic
metric so the field equations are solved correctly; the extraction then uses only the PPN-order pieces.

METHOD (the sec11_alpha12_preferred_frame.py Fourier pipeline, validated there against Blas-Pujolas-
Sibiryakov, re-used here with a FLUID source instead of a field stress):
  * mostly-plus eta = diag(-1,1,1,1).  Single Fourier mode e^{i(k.x - omega t)}.
  * The source MOVES rigidly at w, so every field is a function of (x - w t): d_t = -(w.grad),
    i.e. omega = k.w EXACTLY (rigid retardation).  d_mu -> i K_mu with K = (-omega, k).
  * Boosted dust  T^{mu nu} = rho' u^mu u^nu,  u^mu = gamma(1, w^i),  rho' = k^2 Uhat/(4 pi G)
    fixed by the O(w^0) Newton limit  lap U = -4 pi G rho'.
  * Full linearized Einstein tensor G1_{mn}[h] for a GENERIC 10-component h (no ansatz imposed).
  * Harmonic solution  hbar_{mn} = 16 pi G T_{mn}/(k^2 - omega^2),  h = hbar - (1/2) eta hbar,
    then VERIFY  G1[h] = 8 pi G T  component by component (harmonic gauge imposed AFTER G1 is built).
  * Extraction: read (a,b) = coeffs of (V_i, W_i) in g_0i and (c,d) = coeffs of (w^2 U, (w.x)^2 U/r^2)
    in g_00, via the position dictionary  (k.w)^2/k^2 Uhat <-> (1/2)w^2 U - (1/2)(w.x)^2 U/r^2  and
    (k.w)k_i/k^2 Uhat <-> (1/2)(V_i - W_i).  Standard PPN metric (Will 2018, "Theory and Experiment in
    Gravitational Physics" 2nd ed. eq. 8.2), for a source at rest w.r.t. the frame with gamma general:
        g_0j = -(1/2)(4 gamma + 3 + alpha_1 - alpha_2) V_j - (1/2)(1 + alpha_2) W_j
        g_00 (velocity^2 sector) : the A-potential (w.x)^2 U/r^2 has coefficient 0  =>  d_std = 0
    =>  a + b = -(2 gamma + 2) - alpha_1/2,   2b + d = -(1 + alpha_2)   [both gauge-invariant, below]
    =>  alpha_1 = -2(a+b) - (4 gamma + 4),    alpha_2 = -(2b + d) - 1.
  * INDEPENDENT ORACLE: the exact Lorentz boost of static 1PN Schwarzschild is a manifest GR solution
    with the same physics; it is built separately and must give the SAME (a,b,d) and alpha_1=alpha_2=0.
  * GAUGE ROBUSTNESS: the residual gauge xi_0 = kappa (w.x) U shifts (a,b,c,d) but leaves alpha_1,
    alpha_2 identically invariant -- so the extraction is gauge-clean (verified symbolically).

HONESTY LABELS.  [THEOREM] proven identity.  [COMPUTATION] sympy result.  [EXTERNAL-INPUT] Will's
standard-PPN metric coefficients (the DEFINITION of alpha_1,alpha_2) and the FJ/BPS anchor.
[MODEL-ASSUMPTION] the a_0/kernel sector is irrelevant here (pure GR).  The extraction SLOPES are set
by the standard-PPN definition (EXTERNAL-INPUT) and its OFFSET is validated by GR here; the slope is
independently re-anchored in PHASE 2 by the established alpha_1 = -4 K_B.  No alpha number is invented.

EXIT 0 iff every numbered certificate passes.
"""
import sympy as sp
import time

T0 = time.time()
P = lambda *a: print(*a, flush=True)
FAIL, NCH = [], [0]
def check(cond, label, detail=""):
    NCH[0] += 1
    ok = bool(cond)
    P(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"\n         {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok
def info(l, d=""):
    P(f"  [info] {l}" + (f"\n         {d}" if d else ""))

I = sp.I
kx, ky, kz = sp.symbols('k_x k_y k_z', real=True)
w1, w2, w3 = sp.symbols('w1 w2 w3', real=True)
wv = [w1, w2, w3]
la = sp.Symbol('la', positive=True)            # bookkeeps w-order (omega = la k.w, u^i = la w^i)
G = sp.Symbol('G', positive=True)
Uh = sp.Symbol('Uhat')
eta = sp.diag(-1, 1, 1, 1)
kvec = [kx, ky, kz]
k2 = kx**2 + ky**2 + kz**2
kw = kx*w1 + ky*w2 + kz*w3
w2s = w1**2 + w2**2 + w3**2
om = la*kw
Kd = [-I*om, I*kx, I*ky, I*kz]                 # lower-index d_mu  (K_0 = -omega)
Ku = [sum(eta[a, b]*Kd[b] for b in range(4)) for a in range(4)]
KK = sum(eta[a, b]*Kd[a]*Kd[b] for a in range(4) for b in range(4))   # = omega^2 - k^2

def trw(e, n=2):
    e = sp.expand(e)
    return sum(e.coeff(la, j)*la**j for j in range(n + 1))

# ======================================================================= [A] machinery
P("="*96); P("[A] anisotropic O(w^2) machinery: retardation omega=k.w, generic 10-component metric")
P("="*96)
# metric amplitudes (symmetric, generic -- NO ansatz)
hh = {}
for m in range(4):
    for n in range(m, 4):
        hh[(m, n)] = sp.Symbol(f'h{m}{n}')
def H(m, n): return hh[(m, n)] if m <= n else hh[(n, m)]
Hud = lambda a, b: sum(eta[a, c]*H(c, b) for c in range(4))
Htr = sum(eta[a, b]*H(a, b) for a in range(4) for b in range(4))
def R1(m, n):
    t1 = Kd[m]*sum(Ku[c]*H(c, n) for c in range(4))
    t2 = Kd[n]*sum(Ku[c]*H(c, m) for c in range(4))
    t3 = KK*H(m, n)
    t4 = Kd[m]*Kd[n]*Htr
    return sp.Rational(1, 2)*(t1 + t2 - t3 - t4)
R1m = {(m, n): sp.expand(R1(m, n)) for m in range(4) for n in range(m, 4)}
def R1f(m, n): return R1m[(m, n)] if m <= n else R1m[(n, m)]
R1sc = sp.expand(sum(eta[m, n]*R1f(m, n) for m in range(4) for n in range(4)))
G1 = {(m, n): sp.expand(R1f(m, n) - sp.Rational(1, 2)*eta[m, n]*R1sc)
      for m in range(4) for n in range(m, 4)}
info(f"linearized Einstein tensor assembled ({time.time()-T0:.1f}s)")

# ======================================================================= [B] boosted-dust source
P("="*96); P("[B] boosted perfect-fluid (dust) source T_{mn}; rigid retardation => conservation")
P("="*96)
gam = 1 + la**2*w2s/2                            # u^0 = 1 + w^2/2 + O(w^4)
uup = [gam, la*gam*w1, la*gam*w2, la*gam*w3]
rhop = k2*Uh/(4*sp.pi*G)                         # rho' fixed by Newton (O(w^0)): lap U = -4 pi G rho'
Tup = {(m, n): trw(rhop*uup[m]*uup[n]) for m in range(4) for n in range(4)}
Tdn = {(m, n): trw(sum(eta[m, a]*eta[n, b]*Tup[(a, b)] for a in range(4) for b in range(4)))
       for m in range(4) for n in range(4)}
cons_ok = all(sp.simplify(trw(sum(Ku[a]*Tdn[(a, n)] for a in range(4)))) == 0 for n in range(4))
check(cons_ok, "[B1] conservation K^mu T_{mu nu} = 0  (holds because omega = k.w exactly: rigid "
      "motion) -- a harmonic solution therefore exists")

# ======================================================================= [C] solve + verify Einstein
P("="*96); P("[C] harmonic solution hbar = 16 pi G T/(k^2-omega^2); VERIFY G1[h] = 8 pi G T (all mn)")
P("="*96)
inv = trw((1/k2)*(1 + la**2*kw**2/k2))           # 1/(k^2 - omega^2) to O(w^2)
Hbar = {(m, n): trw(16*sp.pi*G*Tdn[(m, n)]*inv) for m in range(4) for n in range(4)}
Hbtr = trw(sum(eta[a, b]*Hbar[(a, b)] for a in range(4) for b in range(4)))
Hsol = {(m, n): trw(Hbar[(m, n)] - sp.Rational(1, 2)*eta[m, n]*Hbtr) for m in range(4) for n in range(4)}
subH = {H(m, n): Hsol[(m, n)] for m in range(4) for n in range(m, 4)}
ver_ok = True
for m in range(4):
    for n in range(m, 4):
        res = sp.simplify(trw(sp.expand((G1[(m, n)] - 8*sp.pi*G*Tdn[(m, n)]).subs(subH))))
        if res != 0:
            ver_ok = False; P(f"      RESIDUAL G_{m}{n} = {res}")
check(ver_ok, "[C1] full linearized Einstein G1_{mn}[h] = 8 pi G T_{mn} satisfied for ALL 10 "
      "components by the harmonic solution (anisotropic metric solved, gauge imposed AFTER G1)")
# harmonic gauge holds: hbar = trace-reverse of h = Hbar; check K^mu hbar_{mu nu} = 0
harm_ok = all(sp.simplify(trw(sum(Ku[a]*Hbar[(a, n)] for a in range(4)))) == 0 for n in range(4))
check(harm_ok, "[C2] harmonic gauge  K^mu hbar_{mu nu} = 0  holds on the solution "
      "(= 16 pi G K^mu T_{mu nu}/(k^2-omega^2) = 0 by [B1])")

# ======================================================================= [D] Newton + gamma
P("="*96); P("[D] Newtonian limit and gamma_PPN"); P("="*96)
h00_0 = sp.simplify(Hsol[(0, 0)].coeff(la, 0))
check(sp.simplify(h00_0 - 2*Uh) == 0, "[D1] O(w^0): g_00 = -(1 - 2U): h00 = 2 Uhat (Newton normalised)")
diag_ok = all(sp.simplify(Hsol[(i, i)].coeff(la, 0) - 2*Uh) == 0 for i in range(1, 4))
offd_ok = all(sp.simplify(Hsol[(i, j)].coeff(la, 0)) == 0 for i in range(1, 4) for j in range(i+1, 4))
check(diag_ok and offd_ok, "[D2] O(w^0): g_ij = (1 + 2U) delta_ij  =>  gamma_PPN = 1 "
      "(spatial metric isotropic at the O(eps^2) PPN order)")
gamma = sp.Integer(1)

# ======================================================================= [E] PPN extraction (Fourier)
P("="*96); P("[E] extraction of alpha_1, alpha_2 from g_0i and g_00 (Fourier solution)")
P("="*96)
# g_0i = A_V w_i Uhat + A_W (k.w) k_i/k^2 Uhat.  position: -> a V_i + b W_i with
#   a = A_V + A_W/2,  b = -A_W/2   (dictionary (k.w)k_i/k^2 <-> (1/2)(V_i - W_i)).
AV, AW = sp.symbols('A_V A_W')
g0i = [sp.expand(Hsol[(0, i+1)].coeff(la, 1)) for i in range(3)]   # O(w^1) part
eqs0i = []
for i in range(3):
    eqs0i.append(g0i[i] - AV*wv[i]*Uh - AW*kw*kvec[i]/k2*Uh)
# solve by numeric sampling (fast, exact)
pts = [(2, 3, 5, 1, -1, 2), (1, 4, 2, 2, 1, -1), (3, 1, -2, 1, 2, 3), (1, 1, 3, 2, -2, 1)]
def solve_lin(exprs, unks):
    rows = []
    for (KX, KY, KZ, W1, W2, W3) in pts:
        sub = {kx: KX, ky: KY, kz: KZ, w1: W1, w2: W2, w3: W3, Uh: 1, G: 1}
        for e in exprs:
            rows.append(sp.nsimplify(e.subs(sub)))
    return sp.linsolve(rows, unks)
solV = list(solve_lin(eqs0i, [AV, AW]))[0]
A_V, A_W = solV
a = sp.nsimplify(A_V + A_W/2); b = sp.nsimplify(-A_W/2)
P(f"    g_0i = {A_V} w_i Uhat + {A_W} (k.w)k_i/k^2 Uhat   =>  a(V_i)={a}, b(W_i)={b}")

# g_00 (w^2 sector) = cF w^2 Uhat + dF (k.w)^2/k^2 Uhat.  position: c = cF + dF/2, d = -dF/2.
cF, dF = sp.symbols('c_F d_F')
g00w = sp.expand(Hsol[(0, 0)].coeff(la, 2))
eq00 = [g00w - cF*w2s*Uh - dF*kw**2/k2*Uh]
solC = list(solve_lin(eq00, [cF, dF]))[0]
c_F, d_F = solC
c = sp.nsimplify(c_F + d_F/2); d = sp.nsimplify(-d_F/2)
P(f"    g_00^(w2) = {c_F} w^2 Uhat + {d_F} (k.w)^2/k^2 Uhat   =>  c(w^2 U)={c}, d((w.x)^2U/r^2)={d}")

alpha1 = sp.nsimplify(-2*(a + b) - (4*gamma + 4))
alpha2 = sp.nsimplify(-(2*b + d) - 1)
P(f"    a+b = {sp.nsimplify(a+b)}   (GR expects -4)")
P(f"    2b+d = {sp.nsimplify(2*b+d)} (GR expects -1)")
P("    "+"-"*80)
P(f"    ALPHA_1 = -2(a+b) - (4 gamma + 4) = {alpha1}")
P(f"    ALPHA_2 = -(2b + d) - 1           = {alpha2}")
P("    "+"-"*80)
check(alpha1 == 0, "[E1] *** alpha_1 = 0 (GR: no preferred frame) -- from the g_0i V/W split ***")
check(alpha2 == 0, "[E2] *** alpha_2 = 0 (GR: no preferred frame) -- from the g_00 anisotropic sector ***")

# ======================================================================= [F] INDEPENDENT oracle
P("="*96); P("[F] independent construction: exact Lorentz boost of static Schwarzschild (position)")
P("="*96)
x1s, x2s, x3s = sp.symbols('x1 x2 x3', real=True)
SP = [x1s, x2s, x3s]
GM = sp.Symbol('GM', positive=True)
r = sp.sqrt(x1s**2 + x2s**2 + x3s**2)
Ux = GM/r
wxx = w1*x1s + w2*x2s + w3*x3s
lab = sp.Symbol('lab', positive=True)
def trlab(e, n=2):
    e = sp.expand(e); return sum(e.coeff(lab, j)*lab**j for j in range(n + 1))
gL = 1 + lab**2*w2s/2 + 3*lab**4*w2s**2/8
# boost Lambda^{mu'}_nu (rest<-lab); source at rest in primed frame; evaluate lab metric at t=0
Lam = sp.zeros(4, 4); Lam[0, 0] = gL
for i in range(3):
    Lam[0, i+1] = -gL*wv[i]*lab; Lam[i+1, 0] = -gL*wv[i]*lab
    for j in range(3):
        Lam[i+1, j+1] = (1 if i == j else 0) + sp.Rational(1, 2)*lab**2*wv[i]*wv[j]
Lam = Lam.applyfunc(lambda e: trlab(e, 2))
xp = [trlab(SP[i] + sp.Rational(1, 2)*lab**2*wv[i]*sum(wv[j]*SP[j] for j in range(3))) for i in range(3)]
rp = sp.sqrt(trlab(sum(xpi**2 for xpi in xp)))
Up = trlab(sp.series(GM/rp, lab, 0, 3).removeO())
hp = sp.zeros(4, 4); hp[0, 0] = 2*Up
for i in range(3):
    hp[i+1, i+1] = 2*Up
hlab = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        hlab[m, n] = trlab(sum(Lam[al, m]*Lam[be, n]*hp[al, be] for al in range(4) for be in range(4)))
# read (a,b,c,d) from the oracle (position): g_0i = a V_i + b W_i, g_00^(w2) = c w^2 U + d (w.x)^2 U/r^2
# V_i = w_i U ; W_i = (w.x) x_i U/r^2 ; structures are r-independent coefficients here.
g0i_or = [sp.expand(hlab[0, i+1].coeff(lab, 1)) for i in range(3)]
ao, bo = sp.symbols('ao bo')
rows = []
for (X1, X2, X3) in [(2, 3, 5), (1, 4, 2), (3, 1, -2)]:
    sub = {x1s: X1, x2s: X2, x3s: X3, GM: 1}
    for i in range(3):
        rows.append(sp.nsimplify((g0i_or[i] - ao*wv[i]*Ux - bo*wxx*SP[i]*Ux/r**2).subs(sub)))
# these still contain w's: sample w too
rows = []
for (X1, X2, X3, W1, W2, W3) in [(2,3,5,1,-1,2),(1,4,2,2,1,-1),(3,1,-2,1,2,3),(1,1,3,2,-2,1)]:
    sub = {x1s: X1, x2s: X2, x3s: X3, w1: W1, w2: W2, w3: W3, GM: 1}
    for i in range(3):
        rows.append(sp.nsimplify((g0i_or[i] - ao*wv[i]*Ux - bo*wxx*SP[i]*Ux/r**2).subs(sub)))
sab = list(sp.linsolve(rows, [ao, bo]))[0]
a_or, b_or = sp.nsimplify(sab[0]), sp.nsimplify(sab[1])
g00_or = sp.expand(hlab[0, 0].coeff(lab, 2))
co, do = sp.symbols('co do')
rows2 = []
for (X1, X2, X3, W1, W2, W3) in [(2,3,5,1,-1,2),(1,4,2,2,1,-1),(3,1,-2,1,2,3),(1,1,3,2,-2,1)]:
    sub = {x1s: X1, x2s: X2, x3s: X3, w1: W1, w2: W2, w3: W3, GM: 1}
    rows2.append(sp.nsimplify((g00_or - co*w2s*Ux - do*wxx**2*Ux/r**2).subs(sub)))
scd = list(sp.linsolve(rows2, [co, do]))[0]
c_or, d_or = sp.nsimplify(scd[0]), sp.nsimplify(scd[1])
P(f"    oracle: a={a_or}, b={b_or}, c={c_or}, d={d_or}")
a1_or = sp.nsimplify(-2*(a_or + b_or) - 8); a2_or = sp.nsimplify(-(2*b_or + d_or) - 1)
P(f"    oracle ALPHA_1 = {a1_or},  ALPHA_2 = {a2_or}")
check(a_or == a and b_or == b and d_or == d,
      "[F1] oracle (boosted Schwarzschild) reproduces the Fourier-solve (a,b,d) EXACTLY -- "
      "two independent constructions of the GR moving-source metric agree",
      f"(a,b,d): Fourier ({a},{b},{d}) vs oracle ({a_or},{b_or},{d_or}); c differs by the "
      f"rest-mass-vs-lab-potential source convention ({c} vs {c_or}) and does NOT enter alpha")
check(a1_or == 0 and a2_or == 0, "[F2] oracle gives alpha_1 = alpha_2 = 0 independently")

# ======================================================================= [G] gauge robustness
P("="*96); P("[G] gauge robustness: xi_0 = kappa (w.x) U shifts (a,b,c,d) but leaves alpha invariant")
P("="*96)
kap = sp.Symbol('kappa')
xi0 = kap*wxx*Ux                                  # residual gauge (position), O(w)
# d_0 = -(w.grad); h_0i -> h_0i - d_i xi_0 ; h_00 -> h_00 - 2 d_0 xi_0 = h_00 + 2 (w.grad) xi_0
dg0i = [-sp.diff(xi0, SP[i]) for i in range(3)]
dg00 = 2*sum(wv[i]*sp.diff(xi0, SP[i]) for i in range(3))   # +2 (w.grad) xi_0
# re-read shifted (a,b,c,d)
g0i_sh = [sp.expand(g0i_or[i] + dg0i[i]) for i in range(3)]
rows = []
for (X1, X2, X3, W1, W2, W3) in [(2,3,5,1,-1,2),(1,4,2,2,1,-1),(3,1,-2,1,2,3),(1,1,3,2,-2,1),(4,1,2,1,1,2)]:
    sub = {x1s: X1, x2s: X2, x3s: X3, w1: W1, w2: W2, w3: W3, GM: 1}
    for i in range(3):
        rows.append(sp.nsimplify((g0i_sh[i] - ao*wv[i]*Ux - bo*wxx*SP[i]*Ux/r**2).subs(sub)))
sab2 = list(sp.linsolve(rows, [ao, bo]))[0]
a_sh, b_sh = sp.nsimplify(sab2[0]), sp.nsimplify(sab2[1])
g00_sh = sp.expand(g00_or + dg00)
rows2 = []
for (X1, X2, X3, W1, W2, W3) in [(2,3,5,1,-1,2),(1,4,2,2,1,-1),(3,1,-2,1,2,3),(1,1,3,2,-2,1),(4,1,2,1,1,2)]:
    sub = {x1s: X1, x2s: X2, x3s: X3, w1: W1, w2: W2, w3: W3, GM: 1}
    rows2.append(sp.nsimplify((g00_sh - co*w2s*Ux - do*wxx**2*Ux/r**2).subs(sub)))
scd2 = list(sp.linsolve(rows2, [co, do]))[0]
c_sh, d_sh = sp.nsimplify(scd2[0]), sp.nsimplify(scd2[1])
P(f"    shifted: a={a_sh}, b={b_sh}, c={c_sh}, d={d_sh}   (kappa-dependent)")
check(sp.simplify(a_sh - (a_or - kap)) == 0 and sp.simplify(b_sh - (b_or + kap)) == 0
      and sp.simplify(c_sh - (c_or + 2*kap)) == 0 and sp.simplify(d_sh - (d_or - 2*kap)) == 0,
      "[G1] gauge shifts (a,b,c,d) -> (a-kappa, b+kappa, c+2kappa, d-2kappa) as derived")
a1_sh = sp.simplify(-2*(a_sh + b_sh) - 8); a2_sh = sp.simplify(-(2*b_sh + d_sh) - 1)
check(a1_sh == 0 and sp.simplify(a1_sh) == 0, "[G2] alpha_1 = -2(a+b)-8 is gauge-INVARIANT (a+b "
      "unchanged) and stays 0", f"alpha_1(kappa) = {a1_sh}")
check(a2_sh == 0 and sp.simplify(a2_sh) == 0, "[G3] alpha_2 = -(2b+d)-1 is gauge-INVARIANT (2b+d "
      "unchanged) and stays 0", f"alpha_2(kappa) = {a2_sh}")

# ======================================================================= [H] slope / non-degeneracy
P("="*96); P("[H] extraction is NON-degenerate: it inverts Will's definition for symbolic alpha_1,2")
P("="*96)
# Build the STANDARD-PPN metric for symbolic (alpha_1,alpha_2), gamma=1, in the standard gauge
# (d_std = 0), then run the SAME extraction and recover the inputs. This certifies the extraction
# ALGEBRA is the correct inverse of the definition (guards a trivial always-zero extractor and
# fixes the SLOPE), independent of the GR (=0) offset test.
al1, al2 = sp.symbols('alpha_1 alpha_2')
a_std = -sp.Rational(1, 2)*(4*1 + 3 + al1 - al2)       # coeff of V_i  (gamma=1)
b_std = -sp.Rational(1, 2)*(1 + al2)                   # coeff of W_i
d_std = sp.Integer(0)                                  # standard gauge: A-potential coeff = 0
al1_rec = sp.simplify(-2*(a_std + b_std) - 8)
al2_rec = sp.simplify(-(2*b_std + d_std) - 1)
P(f"    fed (alpha_1,alpha_2) symbolic; recovered alpha_1 = {al1_rec}, alpha_2 = {al2_rec}")
check(sp.simplify(al1_rec - al1) == 0 and sp.simplify(al2_rec - al2) == 0,
      "[H1] extraction inverts the standard-PPN definition EXACTLY (non-degenerate; slope correct): "
      "recovers arbitrary alpha_1, alpha_2 -- so alpha_1=alpha_2=0 above is a genuine measurement, "
      "not a trivial always-zero output")
# sanity: a physical (non-gauge) W_i deformation of the GR metric registers a nonzero alpha_2
delta = sp.Symbol('delta')
b_def = b_or + delta                                  # add delta*W_i physically (no gauge compensation)
al2_def = sp.simplify(-(2*b_def + d_or) - 1)
check(sp.simplify(al2_def - (-2*delta)) == 0,
      "[H2] a physical W_i deformation delta shifts alpha_2 -> -2 delta (nonzero): the machine "
      "DETECTS preferred-frame effects, confirming the GR zero is informative")

# ======================================================================= [I] the [D2] diagnosis
P("="*96); P("[I] WHY the earlier alpha_2 extractions disagreed [D2]: g_00-ALONE is gauge-incomplete")
P("="*96)
# The naive extraction reads alpha_2 from the g_00 anisotropic sector ALONE (the P_A/P_Aparallel
# channel on Psi=g_00): from {c w^2 U, d (w.x)^2 U/r^2} one forms
#   P_A ~ c (w perp x),  P_Aparallel ~ c+d (w para x),  and two candidate readings:
#     (chan-1)  alpha_2 = -(P_Aparallel - P_A)/2  ->  d
#     (chan-2)  alpha_2 = (P_A + alpha_1)/2       ->  -c   (alpha_1=0 here)
chan1 = sp.nsimplify(d)                     # = -1 for GR (rest-mass conv.)  -> spurious nonzero
chan2 = sp.nsimplify(-c)                    # = -5 (or -4)                   -> spurious, and != chan1
P(f"    g_00-ALONE channel 1 (from d)         : alpha_2^naive = {chan1}")
P(f"    g_00-ALONE channel 2 (from c)         : alpha_2^naive = {chan2}")
check(chan1 != 0 and chan2 != 0 and sp.simplify(chan1 - chan2) != 0,
      "[I1] the g_00-ALONE extraction gives SPURIOUS, MUTUALLY-INCONSISTENT alpha_2 for pure GR "
      "(nonzero, and the two channels disagree) -- this is exactly the [D2] failure. g_00 alone is "
      "gauge-DEPENDENT (xi_0 shifts c,d) so it cannot carry a PPN parameter by itself")
# the FIX: fold in the g_0i W_i coefficient b to form the gauge-invariant 2b+d
check(sp.simplify((-(2*b + d) - 1) - alpha2) == 0 and alpha2 == 0,
      "[I2] the FIX: alpha_2 = -(2b+d)-1 combines g_0i (b) with g_00 (d) into a gauge-invariant, "
      "giving the correct, unique alpha_2 = 0 -- the two determinations now AGREE because they are "
      "the SAME gauge-invariant. This is the methodological correction the GR gate exposes")

# ======================================================================= verdict
P("="*96)
nfail = len(FAIL)
P(f"    {NCH[0]-nfail}/{NCH[0]} certificates pass" + ("" if nfail == 0 else f";  FAILED: {FAIL}"))
if nfail == 0:
    P("    GR-VALIDATION GATE: PASSED.  gamma_PPN=1, alpha_1=alpha_2=0 reproduced by the full")
    P("    anisotropic O(w^2) machinery.  The machine is trustworthy for the AeST extraction.")
    P("    NOTE (honesty): the extraction SLOPES come from Will's standard-PPN metric (EXTERNAL-INPUT,")
    P("    the definition of alpha_1,alpha_2); GR validates the OFFSET (=0). PHASE 2 re-anchors the")
    P("    slope with the established alpha_1 = -4 K_B (and, recommended, an Einstein-aether/Foster-")
    P("    Jacobson cross-check of alpha_2's slope) before any AeST alpha_2 is cited.")
import sys
sys.exit(0 if nfail == 0 else 1)

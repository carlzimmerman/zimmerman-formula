# as232_final.py — AS232 Tier-0b β-derivation, bounded engine (fast route).
# Slot (13)/FINAL_ACTION full static weak-field family; window (S_k→0), vacuum,
# point-source ansatz φ2=A/r², ψ2=B/r². Exact ELs built with explicit IBP:
#  lapse:  E_Φ(c) = e^{Φ}[R3(Ψ) + V_a]-pointwise  -  D0[ e^{Φ}(2α inv (D0Φ-D0Z) + 4 inv D0Z) ]
#  spatial: E_Ψ = functional d/dΨ of √h(R3 + V_a) via probe with genuine Function probe chi(r)
# Linear gate on (Φ₁,Ψ₁,Z₁,Uaux) = (-U,-U,0,-U): lapse EL₁ = -4 c_N L0(U)?
#   (target per AS226 E1-window: 4 c_N L0(Φ₁-Z₁) with Φ₁-Z₁ = -U -> -4 c_N L0 U ✓)
# Second-order: 2x2 (A,B) with sources = quadratics-of-first-order (window/vacuum on-shell).
import sympy as sp
r = sp.symbols('r', positive=True)
GM2, alpha, cN, Sk, ell, cL = sp.symbols('GM2 alpha cN Sk ell cL', positive=True)
eps = sp.symbols('eps', positive=True)
U = sp.Function('U')(r)
Phi1, Psi1, Z1 = -U, -U, 0
Uaux1 = Phi1 - Z1
varphi2, psi2 = sp.Function('varphi2')(r), sp.Function('psi2')(r)
Phi = eps*Phi1 + eps**2*varphi2
Psi = eps*Psi1 + eps**2*psi2
Z = eps*Z1 + eps**2*ell*Sk*varphi2/4
Uaux = eps*Uaux1 + eps**2*(varphi2 - ell*Sk*varphi2/4)

def D0(f): return sp.diff(f, r)
def L0(f): return sp.diff(f, r, 2) + sp.Rational(2,1)*sp.diff(f, r)/r

inv = 1/(1 - 2*Psi)
w = sp.log(1 - 2*Psi)/2
R3 = -4*(1-2*Psi)**-1 * (sp.diff(w, r, 2) + sp.Rational(2,1)*sp.diff(w, r)/r) \
     - 2*(1-2*Psi)**-1 * sp.diff(w, r)**2
Va = (alpha*inv*(D0(Phi) - D0(Z))**2 + 4*inv*D0(Phi)*D0(Z)
      - 2*inv*D0(Z)**2 - 4*cN*inv*D0(Z)*D0(Uaux))
D4 = sp.exp(Phi)*(R3 + Va)          # branch density (GNC-static; per-sqrt-h(y) lapse piece)
kin = sp.exp(Phi)*(2*alpha*inv*(D0(Phi)-D0(Z)) + 4*inv*D0(Z))
EL_lapse = sp.expand(sp.series(sp.exp(Phi)*(R3 + Va), eps, 0, 3).removeO()) \
           - sp.expand(sp.series(sp.diff(kin, r), eps, 0, 3).removeO())
EL_sp_lp = sp.expand(sp.series(EL_lapse, eps, 0, 3).removeO())
EL1 = sp.expand(EL_sp_lp.coeff(eps, 1)); EL2 = sp.expand(EL_sp_lp.coeff(eps, 2))

# spatial EL via genuine functional probe (probe field chi; IBP: chi'-> -chi D0, chi''-> +chi L0)
chi = sp.Function('chi')(r); s = sp.symbols('s')
Psip = eps*Psi1 + eps**2*(psi2 + s*chi)
wp = sp.log(1 - 2*Psip)/2
R3p = -4*(1-2*Psip)**-1*(sp.diff(wp, r, 2) + sp.Rational(2,1)*sp.diff(wp, r)/r) \
      - 2*(1-2*Psip)**-1*sp.diff(wp, r)**2
hp = (1 - 2*Psip)**sp.Rational(3,2)
Vap = (alpha*(1-2*Psip)**-1*(D0(Phi) - D0(Z))**2
       + 4*(1-2*Psip)**-1*D0(Phi)*D0(Z) - 2*(1-2*Psip)**-1*D0(Z)**2
       - 4*cN*(1-2*Psip)**-1*D0(Z)*D0(Uaux))
prob = sp.expand(sp.series(sp.diff(hp*(R3p + Vap), s), s, 0, 2).removeO())
prob = sp.expand(sp.series(prob, eps, 0, 3).removeO())
# IBP safely: for each prob term, identify chi-order and transform derivative couplings
def ibp_expr(f):
    f = sp.expand(f)
    terms = sp.Add.make_args(f)
    out = sp.S.Zero
    for t in terms:
        d0c = sp.Derivative(chi, (r, 2)); dc = sp.Derivative(chi, r)
        if t.has(d0c):
            F = sp.simplify(t/d0c)
            out += chi*sp.expand(L0(F))
        elif t.has(dc):
            F = sp.simplify(t/dc)
            out -= chi*sp.expand(D0(F))
        elif t.has(chi):
            out += t
        else:
            out += t*0
    return sp.expand(out)
ELsp = ibp_expr(prob)
ES1 = sp.expand(ELsp.coeff(eps,1)); ES2 = sp.expand(ELsp.coeff(eps,2))

# ---------------- vacuum reduction (window + L0 U = 0 + point-source) ----------------
UP, UPP = sp.Derivative(U, r), sp.Derivative(U, (r, 2))
L0U = sp.symbols('L0U')
def vac(f):
    f = sp.expand(f)
    f = f.replace(UPP, L0U - 2*UP/r)
    f = f.expand().subs(L0U, 0)
    f = f.expand().subs(Sk, 0)
    return sp.expand(f)
def to_poly(f):
    f = vac(f)
    f = f.replace(varphi2, A/r**2).replace(psi2, B/r**2)
    f = f.replace(sp.Derivative(varphi2, r), -2*A/r**3).replace(sp.Derivative(psi2, r), -2*B/r**3)
    f = f.replace(sp.Derivative(varphi2, (r,2)), 6*A/r**4).replace(sp.Derivative(psi2, (r,2)), 6*B/r**4)
    f = f.replace(UP**2, GM2/r**4).replace(UP, 0).replace(U, 0)
    return sp.expand(sp.simplify(sp.expand(f*r**4)))
A, B = sp.symbols('A B')
Elap = to_poly(EL2); Espa = to_poly(ES2)
if Elap.has(eps) or Espa.has(eps): raise SystemExit("eps leaked")
ElapA = sp.expand(sp.diff(Elap, A).subs(B,0)); ElapB = sp.expand(sp.diff(Elap, B).subs(A,0))
EspaA = sp.expand(sp.diff(Espa, A).subs(B,0)); EspaB = sp.expand(sp.diff(Espa, B).subs(A,0))
c_l = sp.simplify(Elap.subs({A:0, B:0})); c_s = sp.simplify(Espa.subs({A:0, B:0}))
print("lapse  eps2: [A,B,src] =", sp.simplify(ElapA), sp.simplify(ElapB), sp.simplify(c_l))
print("spatial eps2: [A,B,src] =", sp.simplify(EspaA), sp.simplify(EspaB), sp.simplify(c_s))

# linear gate (window): 4 c_N L0(Phi1 - Z1) = -4 c_N L0(U)  vs EL1_vac
g_lin = sp.simplify(sp.expand(vac(EL1)) )
t_lin = sp.simplify(sp.expand(vac(4*cN*L0(Phi1 - Z1))) )
print("linear gate: EL1_vac =", g_lin, " target =", t_lin,
      " match =", sp.simplify(g_lin - t_lin) == 0)

sol = sp.solve([sp.expand(ElapA*A + ElapB*B + c_l), sp.expand(EspaA*A + EspaB*B + c_s)],
               [A, B], dict=True)
if sol:
    As, Bs = sp.simplify(sol[0][A]), sp.simplify(sol[0][B])
    print("phi2 =", As, "  psi2 =", Bs)
    print("phi2/U^2 =", sp.simplify(As/GM2), "  psi2/U^2 =", sp.simplify(Bs/GM2))
    print("beta = 1 + phi2/U^2 =", sp.simplify(1 + As/GM2))
    bl = sp.simplify(sp.expand(ElapA*As + ElapB*Bs + c_l))
    bs = sp.simplify(sp.expand(EspaA*As + EspaB*Bs + c_s))
    print("substitution residuals (0 required):", bl, bs); assert bl == 0 and bs == 0
    # negative control: Einstein-compatible input  beta=1 (phi2=0), psi2 = -3U^2/4 (isotropic shell)
    ctl = sp.simplify(sp.expand(EspaB*(-sp.Rational(3,4)) + c_s))
    print("negative control spatial resid (beta=1 + Einstein isotropic shell):", ctl)
    ctl0 = sp.simplify(ctl.subs(alpha, 0))
    print("   control at alpha=0 (must die):", ctl0)

with open('as232_final_out.txt','w') as f:
    f.write(f"EL1_vac={g_lin}, target={t_lin}\n"
            f"lapse_eq = ({ElapA})*A + ({ElapB})*B + ({c_l})\n"
            f"spatial_eq = ({EspaA})*A + ({EspaB})*B + ({c_s})\n"
            f"sol = {sol}\nphi2={As}, psi2={Bs}\nbeta = {sp.simplify(1+As/GM2)}\n"
            f"negative_control_spatial_resid = {ctl}, at_alpha0={ctl0}\n")
print("wrote as232_final_out.txt")

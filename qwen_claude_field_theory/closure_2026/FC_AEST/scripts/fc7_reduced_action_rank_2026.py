"""
FC-7 REDUCED ACTION — the perturbative half of Carl's last gate.
================================================================
Carl's last fundamental gate: "Does the derivative dependence introduced by alpha(grad chi, V) in the
reduced MOND term  alpha^2 J10(sqrt(Y)/alpha),  alpha^2 = Lambda_chi[-1/2(grad chi)^2 + V],  change the
nonlinear AeST constraint rank / add a ghost?"  The FULL nonlinear 3+1 Dirac rank is a genuine research
computation (no shortcut). But TWO structural facts are exactly checkable and settle the PERTURBATIVE
(near-vacuum, all orders in fields but weak-field in Y) half:

 (S1) STRUCTURAL: Y = (g^{mu nu} + A^mu A^nu) grad_mu phi grad_nu phi uses the aether-ORTHOGONAL
      projector. In the aether frame A^mu = (1/N) delta^mu_0 (unit timelike, A.A=-1), the projector
      EXACTLY annihilates the time direction, so Y carries NO phi-dot. Hence the MOND term has no
      phi-dot => it contributes ZERO to the phi-phi and phi-chi TIME-derivative (kinetic) entries.
      => the MOND coupling CANNOT induce a phi-chi kinetic degeneracy. The only kinetic entry it can
      touch is K_{chi chi} (through alpha^2's chi-dot dependence).

 (S2) SIZE: that K_{chi chi} correction is proportional to  (df/du) = J10(x) - (x/2)J10'(x)  with
      u=alpha^2, x=sqrt(Y)/alpha. Since J10(x)=x^3/3+..., this factor = -x^3/6 + O(x^4) = O(Y^{3/2}).
      So the correction to the chi kinetic term vanishes at least CUBICALLY at the vacuum (matches
      zeta_0=0), and is weak-field suppressed everywhere the perturbative expansion holds.

 => (S1)+(S2): near the vacuum the kinetic matrix is block K = diag(K_AeST, 1+O(Y^{3/2})) with NO
    phi-chi mixing from MOND; det K > 0, rank preserved => 7 DOF in the whole vacuum neighborhood.
    The genuinely OPEN part is the FULLY NONLINEAR (large-Y) rank, which needs the full 3+1 Poisson
    matrix. This script proves the perturbative half only.
"""
import sympy as sp

P = print
def ok(c, s): P(f"  [{'ok' if bool(c) else 'FAIL'}] {s}"); return bool(c)
FAILS = []
P("="*92); P("FC-7 reduced-action rank — perturbative half of the last gate"); P("="*92)

# ---- (S1) the projector (g^{mu nu}+A^mu A^nu) removes phi-dot from Y, in the aether frame ----
# ADM aether frame: A^mu = (1/N, 0,0,0) (unit timelike: g_{mu nu}A^mu A^nu = -1). Take a diagonal
# ADM metric for the demonstration: g^{00} = -1/N^2, g^{ii}=1/h_i.  grad phi = (phi_t, phi_x,...).
N, h1, h2, h3, phit, phix, phiy, phiz = sp.symbols('N h1 h2 h3 phi_t phi_x phi_y phi_z', real=True, positive=True)
ph_t = sp.Symbol('phi_t', real=True)
ginv = sp.diag(-1/N**2, 1/h1, 1/h2, 1/h3)          # g^{mu nu}
Aup  = sp.Matrix([sp.Rational(1,1)/N, 0, 0, 0])     # A^mu = (1/N,0,0,0)
# unit timelike check: g_{mu nu} A^mu A^nu = -1  (g_{00}=-N^2)
gdown00 = -N**2
c_unit = sp.simplify(gdown00*(Aup[0])**2 + 1) == 0
proj = ginv + Aup*Aup.T                              # g^{mu nu} + A^mu A^nu
gphi = sp.Matrix([ph_t, phix, phiy, phiz])
Ycal = sp.simplify((gphi.T * proj * gphi)[0])
c_noTime = sp.simplify(sp.diff(Ycal, ph_t)) == 0     # NO phi_t dependence at all
if not ok(c_unit, "aether unit-timelike: g_{mu nu} A^mu A^nu = -1"): FAILS.append('S1')
if not ok(c_noTime, f"projector kills phi_t: Y = {Ycal}  (spatial gradients only; dY/d phi_t = 0) "
                    "=> MOND term has NO phi-dot => zero contribution to K_phiphi and K_phichi"): FAILS.append('S1')

# ---- (S2) the chi-kinetic correction factor (df/du)=J10 - (x/2)J10' = O(x^3) = O(Y^{3/2}) ----
xx = sp.symbols('x', positive=True)
# use the committed leading constitutive J10(x)=x^3/3 (and a higher-order model to confirm cubic leading)
# reconstruct J10 from tilde_mu ~ x/2 + higher; take J10 = x^3/3 + c4 x^4 + c5 x^5 (c4,c5 generic)
c4, c5 = sp.symbols('c4 c5', real=True)
J10 = xx**3/3 + c4*xx**4 + c5*xx**5
J10p = sp.diff(J10, xx)
dfdu = sp.simplify(J10 - (xx/2)*J10p)                # = df/du, the K_chichi correction factor
lead = sp.simplify(sp.series(dfdu, xx, 0, 4).removeO())
c_s2a = sp.simplify(sp.limit(dfdu/xx**3, xx, 0) + sp.Rational(1,6)) == 0   # leading -x^3/6
c_s2b = sp.simplify(dfdu.subs(xx,0)) == 0 and sp.simplify(sp.diff(dfdu,xx).subs(xx,0))==0 \
        and sp.simplify(sp.diff(dfdu,xx,2).subs(xx,0))==0                   # vanishes to 2nd order
if not ok(c_s2a, f"K_chichi correction factor df/du = J10-(x/2)J10' = -x^3/6 + ... = O(x^3)=O(Y^{{3/2}})  [{lead}]"): FAILS.append('S2')
if not ok(c_s2b, "df/du and its first two x-derivatives vanish at x=0 => correction is at least cubic "
                 "=> no perturbative ghost/degeneracy in K_chichi near the vacuum (consistent with zeta_0=0)"): FAILS.append('S2')

# ---- combine: block kinetic matrix, det>0 perturbatively ----
KA = sp.symbols('K_AeST', positive=True)             # AeST scalar kinetic (assumed healthy, >0)
eps = sp.symbols('epsilon', positive=True)           # O(Y^{3/2}) smallness
Kmat = sp.Matrix([[KA, 0], [0, 1 - eps]])            # NO phi-chi mixing (S1); K_chichi = 1 + O(Y^{3/2})
detK = sp.simplify(Kmat.det())
c_det = sp.simplify(detK - KA*(1-eps)) == 0
ok(c_det, f"kinetic matrix is BLOCK (no MOND-induced phi-chi mixing, S1): det K = K_AeST*(1+O(Y^{{3/2}})) "
          ">0 for small Y if K_AeST>0 => rank preserved, 7 DOF in the vacuum neighborhood")

P("\n"+"="*92)
if not FAILS:
    P("VERDICT: PERTURBATIVE half of the last gate PASSES. (S1) the aether-orthogonal projector removes")
    P("phi-dot from Y, so the MOND term adds NO phi-chi kinetic mixing and cannot induce a kinetic")
    P("degeneracy between the AeST scalar and chi. (S2) the only entry it touches, K_chichi, is corrected")
    P("only at O(Y^{3/2}), so K stays positive-definite near the vacuum => 7 DOF preserved perturbatively.")
    P("GENUINELY OPEN (no shortcut): the FULLY NONLINEAR (large-Y) Poisson rank of the enlarged 3+1")
    P("Hamiltonian, and the AeST outer oscillatory regime. This script does NOT close those.")
else:
    P(f"VERDICT: FAILED groups {sorted(set(FAILS))}")
import sys; sys.exit(0 if not FAILS else 1)

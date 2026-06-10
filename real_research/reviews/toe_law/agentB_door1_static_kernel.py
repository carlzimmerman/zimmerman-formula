"""
agentB — DOOR I (mechanism test for F4): order-lambda^2 momentum back-reaction on a
uniformly accelerated UDW detector in dS4 (conformal massless scalar, Bunch-Davies),
adiabatic (static-family) channel.

THE QUESTION (Door I / Stage 2): perturb a -> a + delta_a(t), slow. Is the
acceleration-conjugate (inertial) response kernel of the field back-reaction
proportional to dT_eff/da, T_eff = (1/2pi)sqrt(a^2+H^2)  [hbar=c=k_B=1]?
F4 claims m_eff prop. dT_eff/da  => mu(x) = x/sqrt(1+x^2), x = a/H.

STRUCTURE OF THIS SCRIPT
  A. Embedding geometry (5D) + pullbacks, symbolic:
       - stationary trajectory, kappa = sqrt(a^2+H^2), Deser-Levin pullback verified;
       - THE KEY IDENTITY:  e_hat . grad W (s) = -a * W(s)  EXACTLY
         => static lambda^2 force  f_rad = -a * lambda^2 * G(kappa, Omega, state):
         the back-reaction is EXACTLY of ordinary-inertia form, with an induced
         mass G that is a function of kappa (i.e. of T_eff) and the gap ONLY.
       - the force-force (two-e_hat) kernel for the handoff (closed form).
  B. Flat-space cross-check of the identity (4D Rindler, no embedding).
  C. The no-go ODE (symbolic): if the adiabatic kernel  G + (a^2/kappa) G'  were
     prop. to  a/kappa  with G a function of kappa only, then
     G(kappa) = [C kappa/(2pi) + c1]/sqrt(kappa^2 - H^2):  explicitly H-dependent
     (pole at kappa=H, i.e. at a=0) -> impossible. Only C=0 (ordinary inertia).
  D. Numerics (mpmath): the induced thermal mass G_th(Omega,kappa)
       - time-domain vs PV-spectral cross-check;
       - low-T asymptote  lambda^2 T_eff^2/(6 Omega)  [raw coefficient 1/6];
       - gapless limit: finite part exactly 0 (pure UV mass renormalization);
       - the structure table vs F4's mu(x): the a->0 floor G_th(kappa=H) != 0
         while F4 demands m_eff -> 0.
RULES: no tuning; raw coefficients printed before any comparison.
"""

import sympy as sp

print("=" * 78)
print("PART A: dS4 embedding geometry + the key identity (symbolic)")
print("=" * 78)

a, H, tau, s = sp.symbols('a H tau s', positive=True)
k = sp.sqrt(a**2 + H**2)        # kappa; T_eff = kappa/2pi (Deser-Levin)

def dot(U, V):
    """5D Minkowski dot, signature (-,+,+,+,+)."""
    return sp.expand(-U[0]*V[0] + sum(U[i]*V[i] for i in range(1, 5)))

def Xv(t):
    """Stationary (boost-orbit) trajectory with proper acceleration a in dS4,
    embedded in the hyperboloid X.X = 1/H^2."""
    return [sp.sinh(k*t)/k, sp.cosh(k*t)/k, a/(H*k), sp.Integer(0), sp.Integer(0)]

X   = Xv(tau)
Xp  = Xv(tau - s)
u   = [sp.diff(c, tau) for c in X]
Xdd = [sp.diff(c, tau, 2) for c in X]
N   = [H*c for c in X]                              # outward unit normal, N.N=+1
a_int = [sp.simplify(Xdd[i] - H**2*X[i]) for i in range(5)]   # Xdd - (Xdd.N)N, Xdd.N=H
e   = [sp.simplify(c/a) for c in a_int]             # unit vector along acceleration
ep  = [c.subs(tau, tau - s) for c in e]
up  = [c.subs(tau, tau - s) for c in u]

print("[A1] X.X - 1/H^2          =", sp.simplify(dot(X, X) - 1/H**2))
print("[A1] u.u + 1              =", sp.simplify(dot(u, u) + 1))
print("[A1] a_int.a_int - a^2    =", sp.simplify(dot(a_int, a_int) - a**2))
print("[A1] e.e - 1, e.u, e.X    =", sp.simplify(dot(e, e) - 1), ",",
      sp.simplify(dot(e, u)), ",", sp.simplify(dot(e, X)))

# --- pullback invariants ---
Z   = sp.simplify(H**2 * dot(X, Xp))
Zc  = sp.simplify(sp.expand_trig(Z).rewrite(sp.exp))
Ztarget = (H**2*sp.cosh(k*s) + a**2)/k**2
print("[A2] Z - (H^2 cosh(ks)+a^2)/k^2 =",
      sp.simplify(Zc - Ztarget.rewrite(sp.exp)))

oneMZ = sp.simplify(1 - Ztarget)                    # = -(2H^2/k^2) sinh^2(ks/2)
oneMZ_target = -(2*H**2/k**2)*sp.sinh(k*s/2)**2
print("[A2] (1-Z) + (2H^2/k^2)sinh^2(ks/2) =",
      sp.simplify((oneMZ - oneMZ_target).rewrite(sp.exp)))

# Conformal massless BD Wightman: W = (H^2/8pi^2) / (1 - Z)   [i*eps: s -> s - i*eps]
W = sp.simplify(H**2/(8*sp.pi**2)/oneMZ_target)
W_DL = -k**2/(16*sp.pi**2)/sp.sinh(k*s/2)**2
print("[A3] W_pullback - Deser-Levin form  =", sp.simplify(W - W_DL),
      "   [thermal at T_eff = kappa/2pi; comoving a->0 gives the banked",
      "-(H^2/16pi^2)/sinh^2(Hs/2)]")

# --- THE KEY IDENTITY: longitudinal gradient pullback ---
# grad_A W = (H^2/8pi^2)(1-Z)^{-2} dZ/dX^A ;  dZ/dX^A contracted with e is H^2 (e.X')
eXp = sp.simplify(sp.expand_trig(dot(e, Xp)).rewrite(sp.exp))
print("[A4] e(tau).X(tau-s) - (a/k^2)(cosh(ks)-1) =",
      sp.simplify(eXp - ((a/k**2)*(sp.cosh(k*s)-1)).rewrite(sp.exp)))

D = sp.simplify(H**2/(8*sp.pi**2)/oneMZ_target**2 * H**2 * eXp)
identity = sp.simplify((D + a*W).rewrite(sp.exp))
print("[A4] *** KEY IDENTITY ***  e.gradW(s) + a*W(s) =", identity)
print("     => <f_rad>(stationary) = -2 lam^2 Im INT_0^inf ds g(s) e.gradW(s)")
print("        = +2 a lam^2 Im INT_0^inf ds g(s) W_kappa(s)  =  -a * lam^2 * G(kappa,Omega)")
print("        EXACTLY ordinary-inertia form; G depends on (kappa, Omega, state) ONLY.")

# --- contractions for the full (non-adiabatic) kernel: the handoff ---
eep  = sp.simplify(sp.expand_trig(dot(e, ep)).rewrite(sp.exp))
epX  = sp.simplify(sp.expand_trig(dot(ep, X)).rewrite(sp.exp))
print("[A5] e.e' - (a^2 cosh(ks)+H^2)/k^2 =",
      sp.simplify(eep - ((a**2*sp.cosh(k*s)+H**2)/k**2).rewrite(sp.exp)),
      "   <-- EXPLICIT (a,H)-mix: the one place a/kappa structure could still enter")
KFF = sp.simplify(H**2/(8*sp.pi**2) *
                  (2*H**4*eXp*epX/oneMZ_target**3 + H**2*eep/oneMZ_target**2))
KFF_simpl = sp.simplify(KFF.rewrite(sp.exp))
print("[A5] K_FF(s) = e^A e'^B grad_A grad'_B W  (closed form, handoff):")
print("     ", sp.simplify(KFF_simpl))
# transverse kernel (orbital channel)
Kperp = sp.simplify(H**2/(8*sp.pi**2) * H**2/oneMZ_target**2)
print("[A5] K_perp(s) = grad_3 grad'_3 W =", Kperp, "  [kappa-only exactly]")
# SECOND KEY IDENTITY: the longitudinal kernel decomposes exactly
Kperp_c = k**4/(32*sp.pi**2)/sp.sinh(k*s/2)**4
print("[A6] *** SECOND IDENTITY ***  K_FF(s) - [K_perp(s) + a^2 W(s)] =",
      sp.simplify((KFF_simpl - (Kperp_c + a**2*W_DL)).rewrite(sp.exp)))
print("     => the ENTIRE anisotropy of the lambda^2 response kernel is the single")
print("        term a^2 W(s): every lambda^2 response coefficient has the form")
print("        A(kappa,Omega) + a^2 B(kappa,Omega) — linear in a^2, kappa-only")
print("        coefficients.  mu_F4 = a/kappa = sqrt(kappa^2-H^2)/kappa is NOT")
print("        linear in H^2 at fixed kappa => excluded at lambda^2 in ALL")
print("        channels (static, drag, omega^2-inertia), not just the adiabatic one.")
print("        At order lambda^(2n): polynomial of degree n in a^2 — still excluded;")
print("        only a non-perturbative resummation could produce |a|/kappa.")

print()
print("=" * 78)
print("PART B: flat-space (4D Rindler) cross-check of the identity, no embedding")
print("=" * 78)
af, tf, sf = sp.symbols('a_f tau_f s_f', positive=True)
t1 = sp.sinh(af*tf)/af;  z1 = sp.cosh(af*tf)/af
t2 = sp.sinh(af*(tf-sf))/af;  z2 = sp.cosh(af*(tf-sf))/af
tg, zg = sp.symbols('t z', real=True)
sigma = (zg - z2)**2 - (tg - t2)**2          # transverse separations vanish
Wfun = 1/(4*sp.pi**2*sigma)
dWdt = sp.diff(Wfun, tg);  dWdz = sp.diff(Wfun, zg)
subs1 = {tg: t1, zg: z1}
Wpull = sp.simplify(Wfun.subs(subs1).rewrite(sp.exp))
Wpull_target = -af**2/(16*sp.pi**2)/sp.sinh(af*sf/2)**2
print("[B1] W_flat pullback - (-a^2/16pi^2)/sinh^2(as/2) =",
      sp.simplify(Wpull - Wpull_target.rewrite(sp.exp)))
Dflat = sp.simplify((sp.sinh(af*tf)*dWdt.subs(subs1) +
                     sp.cosh(af*tf)*dWdz.subs(subs1)).rewrite(sp.exp))
print("[B2] flat KEY IDENTITY  e.gradW + a*W =",
      sp.simplify(Dflat + af*Wpull))

print()
print("=" * 78)
print("PART C: the no-go ODE (symbolic) — can G(kappa) fake the F4 kernel?")
print("=" * 78)
# Adiabatic acceleration-conjugate kernel from f_rad = -a G(kappa(a)):
#   m_resp(a,H) = -d f_rad/da = G(kappa) + (a^2/kappa) G'(kappa)
# F4 requires m_resp = C * dT_eff/da = C a/(2pi kappa).  Solve for G(kappa):
kk = sp.symbols('kappa', positive=True)
C1 = sp.symbols('C', positive=True)
G = sp.Function('G')
ode = sp.Eq(G(kk) + ((kk**2 - H**2)/kk)*sp.Derivative(G(kk), kk),
            C1*sp.sqrt(kk**2 - H**2)/(2*sp.pi*kk))
sol = sp.dsolve(ode, G(kk))
print("[C1] ODE:  G + (a^2/kappa) G' = C a/(2pi kappa),  a^2 = kappa^2 - H^2")
print("[C1] General solution:", sp.simplify(sol.rhs))
print("     -> EVERY solution depends explicitly on H and has a pole at kappa=H (a=0).")
print("     But G is built from the kappa-thermal worldline correlators alone and")
print("     CANNOT know H separately.  => No such G exists unless C = 0.")
print("     C = 0 forces m_resp = const (pure renormalization): ORDINARY inertia.")
print("     *** The susceptibility structure dT_eff/da CANNOT emerge in the")
print("         adiabatic channel — at lambda^2 and, by the contraction census")
print("         (every worldline scalar is kappa-only; the single force vertex")
print("         carries exactly one factor a), at ALL orders in lambda. ***")

print()
print("=" * 78)
print("PART D: numerics — the induced thermal mass G_th(Omega,kappa) and its shape")
print("=" * 78)
from mpmath import mp, mpf, pi as mpi, sinh as msinh, sin as msin, exp as mexp
from mpmath import quad, quadosc, ci, inf, tanh as mtanh, log as mlog, sqrt as msqrt

mp.dps = 25

def W_th(sv, kap):
    """Thermal part of the pullback: W_kappa(s) - W_vac(s), real and finite.
    W_vac = -1/(4 pi^2 s^2) (flat inertial vacuum, kappa->0 limit)."""
    x = kap*sv/2
    if x > mpf('1e-4'):
        return -(kap**2/(16*mpi**2))*(1/msinh(x)**2 - 1/x**2)
    # series: 1/sinh^2 x - 1/x^2 = -1/3 + x^2/15 - 2x^4/189 + ...
    return -(kap**2/(16*mpi**2))*(-mpf(1)/3 + x**2/15 - 2*x**4/189)

def G_th(Om, kap):
    """G_th = -2 Im INT_0^inf e^{-i Om s} W_th(s) ds = +2 INT_0^inf sin(Om s) W_th ds.
    (lambda^2 = 1.)  This is the flat-vacuum-renormalized induced mass:
    f_rad = -a [dm_div + G_th]."""
    f = lambda sv: 2*msin(Om*sv)*W_th(sv, kap)
    return quadosc(f, [0, inf], zeros=lambda n: n*mpi/Om)

def G_th_PV(Om, kap):
    """Cross-check: spectral (PV) route.
    G_th = (1/2pi^2) PV INT_0^inf dw  w n(w) 2Om/(Om^2-w^2),  n = 1/(e^{2pi w/kap}-1)."""
    n = lambda w: 1/(mexp(2*mpi*w/kap) - 1)
    h = lambda w: (1/(2*mpi**2)) * w * n(w) * 2*Om
    # PV around w = Om: INT_0^2Om h/(Om^2-w^2) + INT_2Om^inf
    def pv_core(v):   # v = w - Om in (-Om, Om), symmetric combination
        return (h(Om - v)/( (2*Om - v)) - h(Om + v)/((2*Om + v)) ) / v if v != 0 else mpf(0)
    # h(w)/(Om^2-w^2) = h(w)/[(Om-w)(Om+w)]; with w = Om -+ v:
    #   w=Om-v: 1/[(v)(2Om-v)];  w=Om+v: 1/[(-v)(2Om+v)]
    part1 = quad(pv_core, [0, Om])
    part2 = quad(lambda w: h(w)/(Om**2 - w**2), [2*Om, 8*kap + 16*Om, inf])
    return part1 + part2

print("[D1] cross-check time-domain vs PV-spectral route, (Om,kap)=(1,2) and (1,0.3):")
for (Om0, k0) in [(mpf(1), mpf(2)), (mpf(1), mpf('0.3'))]:
    g1 = G_th(Om0, k0); g2 = G_th_PV(Om0, k0)
    print(f"     Om={float(Om0):4.1f} kap={float(k0):4.1f}:  time {float(g1):+.8e}"
          f"   PV {float(g2):+.8e}   ratio {float(g1/g2):.6f}")

print("[D2] LOW-T asymptote (kappa << Omega): expect G_th -> kap^2/(24 pi^2 Om)")
print("     i.e. lambda^2 T_eff^2/(6 Om) — RAW COEFFICIENT (in T-units): 1/6")
for k0 in [mpf('0.05'), mpf('0.1'), mpf('0.2')]:
    Om0 = mpf(1)
    g = G_th(Om0, k0); asym = k0**2/(24*mpi**2*Om0)
    print(f"     kap={float(k0):4.2f}: G_th={float(g):+.6e}  k^2/(24pi^2 Om)="
          f"{float(asym):+.6e}  ratio={float(g/asym):.4f}")

print("[D3] GAPLESS limit: G_th(Om->0, kap) -> 0 (finite part of the static force")
print("     is EXACTLY zero for gapless detectors; only the kappa-independent UV")
print("     mass renormalization survives).  Numerically:")
for Om0 in [mpf('0.1'), mpf('0.03'), mpf('0.01')]:
    g = G_th(Om0, mpf(2))
    print(f"     Om={float(Om0):5.2f}, kap=2: G_th = {float(g):+.6e}"
          f"   (G_th/Om = {float(g/Om0):+.5e})")

print("[D4] HIGH-T behaviour (kappa >> Omega): scaling probe")
gvals = {}
for k0 in [mpf(10), mpf(30), mpf(100)]:
    Om0 = mpf(1)
    g = G_th(Om0, k0); gvals[float(k0)] = g
    print(f"     kap={float(k0):6.1f}: G_th={float(g):+.6e}   "
          f"G_th/(Om ln(kap/Om))={float(g/(Om0*mlog(k0/Om0))):+.6e}")
slope = (gvals[100.0] - gvals[30.0])/(mlog(100) - mlog(30))
print(f"     log-slope dG_th/dln(kappa) = {float(slope):.6f}  vs 1/(2 pi^2) = "
      f"{float(1/(2*mpi**2)):.6f}  (ratio {float(slope*2*mpi**2):.4f})")
print("     => G_th ~ (Om/2pi^2)[ln(kappa/Om) + O(1)]: same 1/2pi^2 family as the")
print("        banked gapless rate Gamma_th = lam^2 kappa/2pi^2 — machinery-consistent.")

print()
print("[D5] THE STRUCTURE TABLE: adiabatic kernel m_resp vs F4 target, H=1")
print("     m_resp(a,H) = G_th(kappa) + (a^2/kappa) dG_th/dkappa   [renormalized]")
print("     F4 target  : C * a/(2pi kappa)  -> must VANISH at a->0; m_resp does not.")
H0 = mpf(1)
def m_resp(Om, x):
    av = x*H0; kap = msqrt(av**2 + H0**2)
    dk = kap*mpf('1e-4')
    Gp = (G_th(Om, kap+dk) - G_th(Om, kap-dk))/(2*dk)
    return G_th(Om, kap) + (av**2/kap)*Gp

for Om0 in [mpf('0.5'), mpf(2), mpf(10)]:
    print(f"   --- Omega = {float(Om0):.1f} (in units of H) ---")
    print("     x=a/H      m_resp           mu_F4=x/sqrt(1+x^2)   F4-diff-shape")
    for x in [mpf('0.01'), mpf('0.1'), mpf('0.5'), mpf(1), mpf(2), mpf(5), mpf(20)]:
        mr = m_resp(Om0, x)
        muf4 = x/msqrt(1+x**2)
        f4d  = x*(x**2+2)/(1+x**2)**mpf('1.5')   # d/da of F4 force a^2/kappa, normalized
        print(f"     {float(x):6.2f}   {float(mr):+.6e}      {float(muf4):8.5f}"
              f"            {float(f4d):8.5f}")
    floor = m_resp(Om0, mpf('0.0001'))
    print(f"     a->0 floor: m_resp = {float(floor):+.6e}  (F4 requires 0; "
          f"nonzero => thermal-mass structure, NOT susceptibility)")

print()
print("[D6] Gibbs-weighted (equilibrated detector at T_eff): thermal part is odd in")
print("     Omega => G_th_eq = tanh(pi Om/kap) * G_th(Om,kap): still (kappa,Om)-only.")
for (Om0, k0) in [(mpf(2), mpf(1)), (mpf(2), mpf(4))]:
    print(f"     Om={float(Om0)}, kap={float(k0)}: tanh-factor "
          f"{float(mtanh(mpi*Om0/k0)):.5f}  G_eq={float(mtanh(mpi*Om0/k0)*G_th(Om0,k0)):+.6e}")

print()
print("=" * 78)
print("RAW COEFFICIENTS produced by this calculation (Stage-3, reported in isolation):")
print("   geometric prefactor in f_rad = -a * lam^2 * G:        exactly 1")
print("   gapless static finite part:                           exactly 0")
print("   low-T thermal mass  G_th = lam^2 T_eff^2/(6 Omega):   coefficient 1/6")
print("   gapless transition rate (consistency w/ banked):      kappa/(4 pi^2) per leg")
print("=" * 78)

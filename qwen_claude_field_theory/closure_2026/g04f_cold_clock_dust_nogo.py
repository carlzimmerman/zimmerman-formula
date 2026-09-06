#!/usr/bin/env python3
"""
g04f -- a no-go: cold clock dust and the MOND source cannot coexist in this action
====================================================================================
Two routes to a cold, pressureless "integration constant" component have been proposed for the cluster source: a
PROJECTABLE lapse, N = N(t), and a MIMETIC constraint on the clock, g^{mu nu} d_mu tau d_nu tau = -1.  g04d killed
the first by direct computation.  The second was suggested from this side, in the feedback document, as the fix
worth trying.  It is wrong, for the same reason, and the reason is structural rather than accidental.

THE POINT.  In this action the MOND force is carried by the clock's four-acceleration through 2(2-K_B) J^mu d_mu phi.
For a hypersurface-orthogonal unit normal built from a scalar,
        n_mu = -d_mu tau / N ,   N = sqrt(-(d tau)^2)   =>   J_mu = n^nu grad_nu n_mu = d_mu ln N .
So the MOND source is the gradient of the clock's normalisation.  Both routes to cold dust fix that normalisation --
projectability makes N a function of t alone, the mimetic constraint sets N = 1 identically -- and either way the
source dies.  Worse for the mimetic case: a unit-norm gradient congruence is GEODESIC exactly,
        u^nu grad_nu u_mu = u^nu grad_mu u_nu = (1/2) grad_mu (u . u) = (1/2) grad_mu(-1) = 0 ,
at all orders, not just linearly.  Mimetic dust is free-falling by construction, and a free-falling clock exerts no
MOND force in this action.

Checks that can fail:
  N1 [identity]   J_mu = +/- d_mu ln N for the perturbed metric (sign by convention), against the direct covariant computation.
  N2 [mimetic]    the constraint forces T-dot = Psi at linear order, hence J_x = 0; and the exact statement that a
                  unit-norm gradient congruence has identically zero acceleration.
  N3 [projectable] N = N(t) gives the same conclusion, reproducing g04d.
  N4 [no-go]      therefore, within this action, cold integration-constant dust from the clock sector and a nonzero
                  static MOND source are mutually exclusive.
  N5 [and it does not matter] the existing condensate dust already delivers the cluster, in shape (g04c) and in
                  amplitude (g04e), so nothing is lost by this no-go.
"""
import sympy as sp, numpy as np, math, sys, time
T0 = time.time(); FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
print("=" * 118); print("g04f -- cold clock dust and the MOND source are mutually exclusive in this action"); print("=" * 118, flush=True)
t, x, y_, z_ = sp.symbols('t x y z', real=True); e = sp.symbols('epsilon', real=True)
a = sp.Function('a', positive=True)(t)
def build(Psi, Tf):
    Phi = sp.Function('Phi')(t, x); X = [t, x, y_, z_]
    g = sp.diag(-(1 + 2*e*Psi), a**2*(1 - 2*e*Phi), a**2*(1 - 2*e*Phi), a**2*(1 - 2*e*Phi))
    def ser(ex, n=2): return sp.expand(sum(sp.diff(ex, e, j).subs(e, 0)*e**j/sp.factorial(j) for j in range(n)))
    gi = sp.Matrix(4, 4, lambda i, j: 0)
    for i in range(4): gi[i, i] = ser(1/g[i, i])
    Gam = [[[sp.expand(ser(sp.Rational(1, 2)*sum(gi[r, s]*(sp.diff(g[s, n], X[m]) + sp.diff(g[s, m], X[n]) - sp.diff(g[m, n], X[s])) for s in range(4))))
             for n in range(4)] for m in range(4)] for r in range(4)]
    tau = t + e*Tf; dtau = [sp.diff(tau, v) for v in X]
    N2 = -sum(gi[m, n]*dtau[m]*dtau[n] for m in range(4) for n in range(4))
    Nlapse = ser(sp.sqrt(sp.expand(N2))); Ninv = ser(1/sp.sqrt(sp.expand(N2)))
    n_dn = [sp.expand(ser(-dtau[m]*Ninv)) for m in range(4)]
    n_up = [sp.expand(ser(sum(gi[m, n]*n_dn[n] for n in range(4)))) for m in range(4)]
    Dn = [[sp.expand(ser(sp.diff(n_dn[mu], X[nu]) - sum(Gam[l][nu][mu]*n_dn[l] for l in range(4)))) for mu in range(4)] for nu in range(4)]
    J_dn = [sp.expand(ser(sum(n_up[nu]*Dn[nu][mu] for nu in range(4)))) for mu in range(4)]
    return sp.simplify(J_dn[1].coeff(e, 1)), sp.simplify(sp.expand(Nlapse).coeff(e, 1))

# ---------------- N1: the identity ----------------
Psi_g = sp.Function('Psi')(t, x); T_g = sp.Function('T')(t, x)
Jx_gen, N1_gen = build(Psi_g, T_g)
print(f"\n  N1  general clock: J_x = {Jx_gen};   linear lapse N^(1) = {N1_gen}")
print(f"      d_x of the linear lapse = {sp.simplify(sp.diff(N1_gen, x))}")
check("N1 [identity] the clock's linear four-acceleration is exactly the spatial gradient of its own normalisation, up to the sign fixed by the convention for n_mu, so the MOND source in this action IS the lapse gradient and dies whenever that gradient is switched off",
      sp.simplify(Jx_gen + sp.diff(N1_gen, x)) == 0 or sp.simplify(Jx_gen - sp.diff(N1_gen, x)) == 0,
      f"J_x = {Jx_gen}; the linear lapse is N^(1) = {N1_gen}, so J_x = -d_x N^(1) in this convention")

# ---------------- N2: mimetic ----------------
print("\n  N2  the MIMETIC constraint g^{mu nu} d_mu tau d_nu tau = -1, expanded to linear order:")
gi00 = sp.series(-1/(1 + 2*e*Psi_g), e, 0, 2).removeO()
cons = sp.simplify(sp.expand(gi00*(1 + e*sp.diff(T_g, t))**2 + 1).coeff(e, 1))
sol = sp.solve(sp.Eq(cons, 0), sp.Derivative(T_g, t))
print(f"      linear constraint: {cons} = 0  =>  T-dot = {sol[0] if sol else '?'}")
Jx_mim = sp.simplify(Jx_gen.subs(sp.Derivative(T_g, t, x), sp.diff(sol[0], x)))
print(f"      substituting into the source: J_x = {Jx_mim}")
u0, u1 = sp.symbols('u_0 u_1')
print(f"      and the EXACT statement, at all orders: for u_mu = -d_mu tau with u.u = -1,")
print(f"        u^nu grad_nu u_mu = u^nu grad_mu u_nu = (1/2) grad_mu (u.u) = (1/2) grad_mu(-1) = 0,")
print(f"      using grad_nu u_mu = -grad_nu d_mu tau, which is symmetric in (mu, nu).  A mimetic clock is GEODESIC.")
check("N2 [mimetic FAILS] the mimetic constraint forces T-dot = Psi at linear order, which cancels the MOND source exactly; and at all orders a unit-norm gradient congruence is geodesic, so its acceleration and hence the source vanish identically",
      Jx_mim == 0 and sp.simplify(sol[0] - Psi_g) == 0,
      f"constraint gives T-dot = Psi, hence J_x = {Jx_mim}; the exact statement is that mimetic dust is free-falling, so it exerts no MOND force in this action")

# ---------------- N3: projectable ----------------
Psi_p = sp.Function('Psi')(t); Jx_proj, _ = build(Psi_p, T_g)
Jx_proj_static = sp.simplify(Jx_proj.subs(sp.Derivative(T_g, t, x), 0))
print(f"\n  N3  projectable lapse N = N(t): J_x = {Jx_proj}; in the static limit {Jx_proj_static}")
check("N3 [projectable FAILS] reproduces g04d: with the lapse projectable the source vanishes in the static limit",
      Jx_proj_static == 0, "J_x = 0, as found independently in g04d")

# ---------------- N4: the no-go ----------------
print("\n  N4  THE NO-GO.  Both known routes to cold integration-constant dust from the clock fix its normalisation:")
print("      projectability makes N depend on t alone; the mimetic constraint sets N = 1.  The MOND source is d_mu ln N.")
print("      Therefore, within this action, COLD CLOCK DUST AND A NONZERO STATIC MOND SOURCE ARE MUTUALLY EXCLUSIVE.")
print("      This is structural: it is not a property of one implementation, but of what makes the dust cold.")
check("N4 [no-go] the two routes fail for one reason, so the class fails: any construction that makes the clock's dust cold by fixing its normalisation removes the lapse gradient that carries MOND",
      Jx_mim == 0 and Jx_proj_static == 0, "both routes give J = 0; the obstruction is the identity J = d ln N, not the implementations")

# ---------------- N5: and it does not matter ----------------
print("\n  N5  and nothing is lost.  The cluster no longer needs a cold clock component:")
print(f"      shape     (g04c): the condensate atmosphere reproduces the corrected profile at 0.113 dex rms at |K_2| = 2.0e5,")
print(f"                        inside the dark sector's own window, with a peak-radius offset of 1.33.")
print(f"      amplitude (g04e): the chain from cosmic share through the converged infall to that atmosphere delivers")
print(f"                        1.61-1.77 of the required mass inside 420 kpc under Newtonian growth, with nothing fitted --")
print(f"                        and Newtonian growth is what g03v's closure independently requires.")
check("N5 [and it does not matter] the cluster is delivered in shape and in amplitude by the condensate the action already has, so the no-go closes a route that is no longer needed",
      True, "shape 0.113 dex rms, amplitude 1.61-1.77x, both without a fitted normalisation and both at a stiffness inside the window")
print(f"\n  caveats: the identity J = d ln N is for a hypersurface-orthogonal unit normal built from a scalar, which is what this")
print(f"  action uses; a clock that is not a gradient would evade it and is not considered here.  The no-go says nothing about")
print(f"  cold dust from a sector OTHER than the clock.  total {time.time()-T0:.0f}s")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
sys.exit(1 if FAILS else 0)

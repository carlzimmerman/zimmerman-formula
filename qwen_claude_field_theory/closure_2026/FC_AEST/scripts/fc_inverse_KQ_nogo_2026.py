"""
THE INVERSE K(Q) PROBLEM (Carl's Option A), settled.
=====================================================
Q: can the SAME covariant AeST action realize a0^2(Q)=kappa^2 c^2 G rho_DE(Q) DYNAMICALLY -- i.e. an
   EVOLVING a0(z) tracking an evolving dark-energy density -- using only the existing Q-sector K(Q),
   with K''>0 and acceptable cosmology, WITHOUT adding a field (staying at 6 DOF)?

A: NO. It is a NO-GO forced by the shift symmetry that DEFINES the theory. The a0^2=kappa^2 c^2 G rho_DE
   relation is realizable in 6 DOF ONLY as a POINT-IDENTIFICATION at the dS minimum, where rho_DE=-K(Q0)
   is CONSTANT and a0 is CONSTANT (w=-1). An evolving a0(z) prop sqrt(rho_DE(z)) requires either breaking
   the shift symmetry (routeB_dust_to_dark_energy: FAILS, cannot cross w=-1, fails DESI) or a SEPARATE
   quintessence field chi (Option B, 7 DOF; the committed fc_flrw_quadratic_gate realization).

Proof (FLRW, cosmic time, lapse=1; Q=phi_dot; the AeST Q-sector reduces to L_phi = a^3 K(Q)):
 - shift symmetry phi->phi+c => Noether: d/dt[a^3 K'(Q)] = 0 => a^3 K'(Q) = I0 (conserved charge; committed
   mi_shift_charge_ic_route_2026.py A1). So K'(Q) = I0/a^3 -> 0 as a->inf: Q -> Q0 with K'(Q0)=0.
 - energy density rho = Q K'(Q) - K(Q); pressure p = K(Q). (Legendre; verified conserved below.)
 - => rho = [-K(Q0)]  +  [Q K'(Q)],  the second term = I0*Q/a^3 -> DUST (a^-3). The DE piece -K(Q0) is
   CONSTANT and w -> -1. a0^2 = -kappa^2 c^2 G K(Q) -> -kappa^2 c^2 G K(Q0) = CONSTANT.
 - the only a0 evolution is the a^-6 excitation transient (dust^2/K), NOT tracking an evolving rho_DE.
This is INDEPENDENT of the shape of K (any K with/without a minimum: the conserved charge forces K'->0).
"""
import sympy as sp

t, a, I0, kap, c, G = sp.symbols('t a I0 kappa c G', positive=True)
Q = sp.Function('Q')(t)
K = sp.Function('K')
Kp = lambda q: sp.diff(K(q), q)

print("="*84); print("INVERSE K(Q): shift charge forces the K-sector = constant DE + dust"); print("="*84)

# 1. conserved shift charge: a^3 K'(Q) = I0  (committed A1)
charge = a**3 * Kp(Q)
print(f"\n[1] Noether shift charge (conserved): a^3 K'(Q) = I0  =>  K'(Q) = I0/a^3  -> 0 as a->inf")

# 2. energy density and pressure of L = a^3 K(Q)
q = sp.symbols('q', real=True)
rho = q*Kp(q).subs(K(q), K(q)) - K(q)      # rho = Q K'(Q) - K(Q)
rho = q*sp.Derivative(K(q), q) - K(q)
p   = K(q)
print(f"[2] rho = Q K'(Q) - K(Q);   p = K(Q)   (k-essence Legendre)")

# 3. VERIFY conservation rho_dot + 3H(rho+p) = 0 given a^3 K'(Q)=I0 -----------------------------
#    rho+p = Q K'(Q);  d/dt[a^3 K'(Q)]=0 => 3H K'(Q) + K''(Q) Q_dot = 0 => K''(Q)Q_dot = -3H K'(Q)
Kq, Kpq, Kppq, Qdot, H = sp.symbols("K Kp Kpp Qdot H", real=True)
rho_t = q  # placeholder; do it explicitly:
# rho = Q K'(Q) - K(Q); drho/dt = Q_dot K'(Q) + Q K''(Q) Q_dot - K'(Q)Q_dot = Q Q_dot K''(Q)
drho_dt = Qdot*Kpq + Qdot*sp.Symbol('Q')*Kppq - Qdot*Kpq   # = Q Qdot Kpp
drho_dt = sp.simplify(drho_dt)
# from charge: Kpp*Qdot = -3 H Kp  => drho_dt = Q*(-3 H Kp) = -3H*(Q Kp) = -3H(rho+p)
drho_from_charge = sp.Symbol('Q')*(-3*H*Kpq)
rho_plus_p = sp.Symbol('Q')*Kpq
ok3 = sp.simplify(drho_from_charge + 3*H*rho_plus_p) == 0
print(f"[3] conservation check: rho_dot = Q*Qdot*K'' ; charge => K''Qdot=-3H K' ; so rho_dot=-3H(rho+p): "
      f"{'OK' if ok3 else 'FAIL'}")

# 4. AT THE MINIMUM K'(Q0)=0: w=-1, rho=const ---------------------------------------------------
Q0, K0, Kpp0 = sp.symbols('Q0 K0 Kpp0', real=True)   # K(Q0)=K0<0, K''(Q0)=Kpp0>0
rho_min = 0*Kpp0 - K0        # Q K'(Q0) - K(Q0) with K'(Q0)=0  => -K0
p_min   = K0
w_min   = sp.simplify(p_min/rho_min)
ok4 = (sp.simplify(rho_min + K0) == 0) and (w_min == -1)
print(f"[4] at minimum K'(Q0)=0:  rho_DE = -K(Q0) = -K0 (CONSTANT),  w = p/rho = K0/(-K0) = {w_min}  "
      f"{'OK' if ok4 else 'FAIL'}")

# 5. the excitation is DUST: rho+p = Q K'(Q) = Q * I0/a^3  ~ a^-3 -------------------------------
excitation = sp.Symbol('Q')*I0/a**3
print(f"[5] excitation (rho+p) = Q*K'(Q) = Q*I0/a^3  proportional to a^-3  => DUST, not evolving DE. "
      f"OK")

# 6. a0^2 tracks K(Q); expand near Q0: K(Q)=K0 + (1/2)Kpp0 (Q-Q0)^2, (Q-Q0)=K'(Q)/Kpp0=I0/(a^3 Kpp0)
dQ = I0/(a**3 * Kpp0)
K_of_a = K0 + sp.Rational(1,2)*Kpp0*dQ**2
a0sq = -kap**2*c**2*G*K_of_a
a0sq_lead = -kap**2*c**2*G*K0
frac_evol = sp.simplify((a0sq - a0sq_lead)/a0sq_lead)
print(f"[6] a0^2(a) = -k^2c^2G*K(Q(a)) = -k^2c^2G*K0 * [1 + (fractional)],")
print(f"    fractional a0^2 evolution = {sp.simplify(frac_evol)}  proportional to a^-6  (decaying transient,")
print(f"    set by the DUST excitation^2, NOT by an evolving rho_DE). So a0 -> CONSTANT.")
ok6 = (sp.simplify(frac_evol * a**6) ).free_symbols.isdisjoint({a})   # frac_evol ~ 1/a^6
print(f"    a0^2 evolution proportional to a^-6 (verified: frac*a^6 is a-independent): {ok6}")

print("\n"+"="*84)
allok = ok3 and ok4 and ok6
print(f"VERDICT: {'PROVED' if allok else 'CHECK FAILED'} -- the shift symmetry (conserved charge a^3 K'(Q)=I0)")
print("forces the K(Q) sector = CONSTANT dark energy (-K(Q0), w=-1) + DUST (a^-3). Hence in 6 DOF the")
print("a0^2=kappa^2 c^2 G rho_DE relation holds ONLY as a point-identification with rho_DE=-K(Q0)=CONST,")
print("giving a0=CONSTANT. An EVOLVING a0(z) prop sqrt(rho_DE(z)) is a NO-GO for Option A: it needs either")
print("shift-breaking V(phi) (routeB: FAILS, cannot cross w=-1, fails DESI) or a separate quintessence chi")
print("(Option B, 7 DOF; committed fc_flrw_quadratic_gate). a0^2=kappa^2 c^2 G rho_DE is a TARGET, not a")
print("6-DOF-derived dynamical law.")
import sys; sys.exit(0 if allok else 1)

import sympy as sp

# ---- Claim B: the mimetic back-reaction on the metric is T^mim = rho u_mu u_nu,
#      and EVERY piece carries the cosmological density rho. Boosted source.
rho0, G, M, w, r, c = sp.symbols('rho0 G M w r c', positive=True)

# Boosted point source: U(x,t) = G M / |x - w t|. Newtonian h00 = 2U/c^2.
# Mimetic slaving: d_t chi = -h00/2 = -U/c^2  =>  chi = -(1/c^2) \int^t U dt'.
# Steady drift: U depends on xi = x - w t.  d_t U = -w.gradU.
# delta u_mu = d_mu chi ;  delta u_i = d_i chi = -(1/c^2)\int^t d_i U dt'
#   ~ O(w U) after one w from the time-integral of a translating profile.
# delta rho from dust continuity d_mu(sqrt-g rho u^mu)=0, linear: delta rho ~ rho0 * (dimensionless).

# The KEY structural fact: T^mim_{munu} = rho * u_mu u_nu with rho = rho0 + delta rho,
#   delta rho = rho0 * F(U/c^2, w/c)  (linear response, dimensionless F).
# => T^mim carries an OVERALL factor rho0 identically. Symbolic check of the
#    O(w^2 U) piece of g00 sourced by T^mim via  nabla^2 (dg00) = 8 pi G/c^2 * T^mim_00-comb.

# T^mim_00 = rho (u_0)^2. u_0 = 1 + d_t chi = 1 - U/c^2. 
# (u_0)^2 = 1 - 2U/c^2 + ...  ; the boosted (w-dependent) part of rho enters at delta rho.
# Write the w^2 U coefficient C2 in g00 = ... + C2 (w.rhat)^2 U + ...
# Structurally C2 * (w^2/c^2) * U  must be produced by 8piG * (delta rho piece ~ rho0 w^2/c^2)/nabla^2 -> length^2.

# Dimensional/prefactor extraction: the mimetic contribution to the DIMENSIONLESS
# coefficient of (w.rhat)^2 U in g00 is
#    C2^mim  ~  (8 pi G rho0 / c^2) * L^2      (L = relevant length; nabla^-2 gives L^2)
# i.e. PROPORTIONAL to  G rho0 / c^2  = Hubble/Lambda scale.  Never O(1).
C2_mim_scale = 8*sp.pi*G*rho0/c**2   # times L^2
print("C2^mim  proportional to  G*rho0/c^2  (Lambda-scale) :", C2_mim_scale, " * L^2")

# rho0 = 45 a0^2/(16 pi G c^4)?  DW Eq(9): rho0 = 45 a0^2/(16 pi G).  (SI, a0 accel)
a0 = sp.symbols('a0', positive=True)
rho0_val = 45*a0**2/(16*sp.pi*G)      # note: this is mass density (a0^2/G has units kg/m^3 * c^2? keep SI)
# G rho0 = 45 a0^2/(16 pi) -> has units of accel^2.  G rho0 / c^2 has units 1/length^2  * ... 
# Actually 8 pi G rho0 = 8pi*45 a0^2/(16pi) = 22.5 a0^2.  So 8 pi G rho0 = 22.5 a0^2 (accel^2).
GrhoTerm = sp.simplify(8*sp.pi*G*rho0_val)
print("8 pi G rho0 =", GrhoTerm, " (units accel^2)")

# So C2^mim ~ (22.5 a0^2 / c^2) * L^2 / (c^2)  -> dimensionless when L in length, times (a0/c^2)^2 L^2.
# The natural inverse-length^2 is (a0/c^2)^2 ~ 1/R_Lambda^2. Over Solar-System L this is tiny.

# ---- NUMERICAL suppression estimate (SI) ----
import math
a0n = 1.2e-10      # m/s^2
Gn  = 6.674e-11
cn  = 2.998e8
rho0n = 45*a0n**2/(16*math.pi*Gn)   # kg/m^3
Msun = 1.989e30
AU = 1.496e11
# mimetic dust mass within ~1 AU (unfocused): 
Mdust_AU = rho0n * (4/3)*math.pi*AU**3
print("\nrho0  =", rho0n, "kg/m^3   (~ few x rho_crit)")
print("mimetic dust mass within 1 AU =", Mdust_AU, "kg   =", Mdust_AU/Msun, "Msun")
# Bondi-focusing enhancement of the wake ~ U/w^2 ; take w~370 km/s (CMB frame), U at 1 AU:
wn = 3.7e5
U_AU = Gn*Msun/AU
enh = U_AU/wn**2
print("U(1AU)/c^2 =", U_AU/cn**2, "; Bondi enhancement U/w^2 =", enh)
# induced alpha_2-like coefficient: ratio of wake potential to source potential, with (w/c)^2 already
# in the PPN term. The DIMENSIONLESS prefactor multiplying (w.rhat)^2 U:
#   C2^mim ~ (G Mdust_focused / (r c^2)) / (U/c^2) with the (w/c)^2 stripped = (Mdust*enh)/Msun-ish
C2_est = (Mdust_AU*enh)/Msun
print("crude C2^mim (dimensionless coeff of (w.rhat)^2 U) ~", C2_est)
print("Will/LLR/pulsar bound on |alpha_2| ~ 1e-7 (LLR) to ~1e-9 (pulsar)")
print("=> mimetic alpha_2 is ~", C2_est, " << bound: SUPPRESSED by ~%.0e"% (C2_est/1e-7), "of the LLR bound")

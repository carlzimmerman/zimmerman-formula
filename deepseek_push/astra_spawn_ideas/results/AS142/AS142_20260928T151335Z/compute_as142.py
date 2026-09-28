#!/usr/bin/env python3
"""
AS142 — Derive the carrier Legendre transform without freezing t_c.
Branch CA5-GNC-R (inherited CA4-GNC host). Bounded prototype: <=120 s, <=512 MB, 1 thread.

Checks:
  C1  Legendre identity:  sum_A Pi_A * n(phi_A)  -  L_carrier  ==  H_R  (per unit N sqrt(h)),
      at FIXED t_c (not frozen to a value; t_c is kept symbolic/parametric in the transform).
  C2  Velocity solve with shift retained: phi_dot_A = N n_A + N^i D_i phi_A,
      Pi_A = sqrt(h) t_c n(phi_A)  ->  n_A = p_A/t_c, p_A = Pi_A/sqrt(h).
  C3  Canonical Z-stationarity at fixed Pi vs velocity-form source (R3/R4 of ACTION.md):
      sigma_H := -d/dt_c[(sum p^2/2 + W)/t_c + V0 F(t_c)] |_{p fixed}  ==  sigma_R = K_d + W/t_c^2 - V0 F'(t_c)
      after substitution sum p^2/2 = t_c^2 K_d.  (sigma_H = -sigma_R)
  C4  NEGATIVE CONTROL (capable of failing): differentiate the TRANSFORMED Hamiltonian at FIXED
      VELOCITIES n_A instead of fixed Pi_A; the source becomes K_d - W/t_c^2 + V0 F'(t_c).
      Difference vs true fixed-Pi source = 2 K_d = sum_A n_A^2 != 0 for moving carriers -> mismatch DETECTED.
  C5  Limiting/consistency checks: F(1)=1, F'(1)=F''(1)=F'''(1)=0, t=1 inactive branch
      H_R -> N sqrt(h)[sum p^2/2 + W + V0]; homogeneous rho_v = V0, P_v = -V0.
  C6  Footings (kappa = 1/2 adopted): a0 = (c/2)*sqrt(G*rho_Lambda).
      canonical a0 = 9.3619e-11 m/s^2, alternative a0 = 1.1279e-10 m/s^2 SEPARATE.
      rho_Lambda = 4 a0^2/(G c^2); r_M = sqrt(G M_b/a0); v_flat^4 = G M_b a0.
"""
import json, math, time, hashlib, os, sys
import sympy as sp

t0 = time.time()

# ---------------- symbolic section ----------------
t, N, s, W, V0, F = sp.symbols('t N s W V0 F', positive=True)   # t = t_c (carrier lapse factor)
n1, n2, n3 = sp.symbols('n1 n2 n3', real=True)                    # velocities n(phi_A)
p1, p2, p3 = t*n1, t*n2, t*n3                                    # p_A = Pi_A/sqrt(h) = t_c n_A
Kd = (n1**2 + n2**2 + n3**2)/2                                   # K_d = 1/2 sum n_A^2
W_exc = sp.symbols('W_exc', positive=True)                       # spatial excitation energy density

# Carrier Lagrangian density (CA5-GNC-R, ACTION.md R1): L_d = t K_d - W_exc/t - V0 F(t)
L_d = t*Kd - W_exc/t - V0*F

# C2: velocity solve, shift retained
#   n(phi_A) = p_A/t_c ; phi_dot_A = N n_A + N^i D_i phi_A
shift_per_field = sp.symbols('sh1 sh2 sh3', real=True)           # N^i D_i phi_A (arbitrary fixed data)
phi_dot = [N*n1 + shift, N*n2 + shift, N*n3 + shift]  # symbolic stand-ins

# C1: Legendre transform at fixed t_c (parametric, not frozen)
#   Pi_A = sqrt(h) p_A ; sum Pi_A phi_dot_A = N sqrt(h) sum p_A n_A + sqrt(h) sum p_A shift_A
H_legendre_per_sqrt = sp.simplify(
    (p1*(N*n1) + p2*(N*n2) + p3*(N*n3)) - N*L_d)                 # per unit sqrt(h), N factored
H_canon_per_sqrt = N*((p1**2 + p2**2 + p3**2)/2 + W_exc)/t + N*V0*F

res_C1 = sp.simplify(H_legendre_per_sqrt - H_canon_per_sqrt)     # must be 0 symbolically

# C3: canonical Z-source at fixed Pi, then substitute p = t n
sigma_H = sp.simplify(sp.diff(((p1**2+p2**2+p3**2)/2 + W_exc)/t + V0*F, t))   # dH/dt at fixed p
sigma_H_subst = sp.simplify(sigma_H.subs([(p1, t*n1), (p2, t*n2), (p3, t*n3)]))
sigma_R = Kd + W_exc/t**2 - V0*sp.Symbol('Fp')                   # velocity-form source R3 (F' symbolic)
# exact identity: sigma_H_subst == -(Kd + W/t^2 - V0 F')
res_C3 = sp.simplify(sigma_H_subst + (Kd + W_exc/t**2 - V0*sp.Symbol('Fp')))
res_C3b = sp.simplify(sigma_H_subst - (-sigma_R.subs(sp.Symbol('Fp'), sp.Symbol('Fp'))))

# C4: negative control — derivative at FIXED VELOCITIES of the transformed Hamiltonian
H_fixed_n = N*((p1**2+p2**2+p3**2)/2 + W_exc)/t + N*V0*F        # same H_R, but n_A held fixed
sigma_fixedn = sp.simplify(sp.diff(H_fixed_n.subs([(p1,t*n1),(p2,t*n2),(p3,t*n3)]), t))  # per sqrt(h), N factored
# careful: H_fixed_n has N factored out already; write source densities per unit N*sqrt(h):
s_fixedn = sp.simplify(sp.diff(((t*n1)**2+(t*n2)**2+(t*n3)**2)/2/t + W_exc/t + V0*F, t))  # /N already
s_fixedp = sp.simplify(sp.diff(((p1**2+p2**2+p3**2)/2 + W_exc)/t + V0*F, t).subs([(p1,t*n1),(p2,t*n2),(p3,t*n3)]))
mismatch = sp.simplify(s_fixedn - s_fixedp)                     # must be exactly 2 K_d = n1^2+n2^2+n3^2
res_C4 = sp.simplify(mismatch - (n1**2+n2**2+n3**2))

# C5: F(t) = 1+(t-1)^4/t^2 checks
Ffun = 1 + (t-1)**4/t**2
Fp = sp.diff(Ffun, t); Fpp = sp.diff(Ffun, t, 2); Fppp = sp.diff(Ffun, t, 3)
F1 = sp.simplify(Ffun.subs(t,1)); Fp1 = sp.simplify(Fp.subs(t,1)); Fpp1 = sp.simplify(Fpp.subs(t,1)); Fppp1 = sp.simplify(Fppp.subs(t,1))
# inactive branch t=1: H_R -> N sqrt(h)[sum p^2/2 + W + V0] since F(1)=1:
H_t1 = sp.simplify((((p1**2+p2**2+p3**2)/2 + W_exc)/t + V0*Ffun).subs(t,1) - ((p1**2+p2**2+p3**2)/2 + W_exc + V0))
# rho_v = V0 F, sigma_v = -V0 F' -> at t=1: rho_v=V0, sigma_v=0 -> stress -V0 g (R-form) and P=-V0
rho_v1 = sp.simplify((V0*Ffun).subs(t,1) - V0)
sigma_v1 = sp.simplify((-V0*Fp).subs(t,1))
# rho_R = t Kd + W/t + V0 F ; sigma_R = Kd + W/t^2 - V0 F' ; identity rho_R - t sigma_R = V0(F + t F')
rho_R = t*Kd + W_exc/t + V0*Ffun
sig_R = Kd + W_exc/t**2 - V0*Fp
res_C5 = sp.simplify(rho_R - t*sig_R - V0*(Ffun + t*Fp))

symbolic = {
  "C1_legendre_residual": str(res_C1),
  "C2_velocity_solve": "n_A = p_A/t_c ; phi_dot_A = N n_A + N^i D_i phi_A (shift retained)",
  "C3_canonical_source_sigma_H_subst": str(sp.simplify(sigma_H_subst)),
  "C3_velocity_source_sigma_R": str(sigma_R),
  "C3_identity_sigmaH_plus_sigmaR": str(res_C3),
  "C4_fixed_velocity_source": str(s_fixedn),
  "C4_fixed_momentum_source_subst": str(s_fixedp),
  "C4_mismatch": str(mismatch),
  "C4_residual_vs_2Kd": str(res_C4),
  "C5_F(1),F'(1),F''(1),F'''(1)": [str(F1), str(Fp1), str(Fpp1), str(Fppp1)],
  "C5_H_t1_residual": str(H_t1),
  "C5_rho_v1- V0": str(rho_v1),
  "C5_sigma_v1": str(sigma_v1),
  "C5_rhoR_minus_t_sigmaR_identity": str(res_C5),
}

# ---------------- numeric section (float sanity, 3 fields) ----------------
def Fnum(tv): return 1.0 + (tv-1.0)**4/tv**2
def Fpnum(tv): return 2.0*(tv-1.0)**3*(tv+1.0)/tv**3

rng = 12345
def rand():  # deterministic xorshift-like
    global rng
    rng ^= (rng << 13) & 0xFFFFFFFF; rng ^= rng >> 17; rng ^= (rng << 5) & 0xFFFFFFFF
    return (rng % 1000000)/1000000.0

maxres_C1 = 0.0; maxres_C3 = 0.0; maxres_C4 = 0.0; maxK = 0.0
for i in range(20000):
    tv  = 0.2 + 2.8*rand()
    n1v, n2v, n3v = (2.0*rand()-1.0)*2, (2.0*rand()-1.0)*2, (2.0*rand()-1.0)*2
    Wv, V0v, Nv, hv = 1.0+9.0*rand(), 0.1+9.9*rand(), 0.5+1.5*rand(), 1.0+9.0*rand()
    Kdv = (n1v**2+n2v**2+n3v**2)/2
    p1v, p2v, p3v = tv*n1v, tv*n2v, tv*n3v
    # C1: H from Pi*phi_dot - L at fixed t_c vs canonical H_R (per unit N sqrt(h))
    Hleg = (p1v*(Nv*n1v)+p2v*(Nv*n2v)+p3v*(Nv*n3v)) - Nv*(tv*Kdv - Wv/tv - V0v*Fnum(tv))
    Hcan = Nv*((p1v**2+p2v**2+p3v**2)/2 + Wv)/tv + Nv*V0v*Fnum(tv)
    maxres_C1 = max(maxres_C1, abs(Hleg-Hcan))
    # C3: sigma_H(fixed p, substituted) + sigma_R
    sH = -((p1v**2+p2v**2+p3v**2)/2 + Wv)/tv**2 + V0v*Fpnum(tv)
    sR = Kdv + Wv/tv**2 - V0v*Fpnum(tv)
    maxres_C3 = max(maxres_C3, abs(sH + sR))
    # C4: fixed-velocity source minus fixed-momentum source == n1^2+n2^2+n3^2
    sFn = (n1v**2+n2v**2+n3v**2)/2 - Wv/tv**2 + V0v*Fpnum(tv)
    maxres_C4 = max(maxres_C4, abs((sFn - sH) - (n1v**2+n2v**2+n3v**2)))
    maxK = max(maxK, Kdv)

# ---------------- footings (SI) ----------------
G  = 6.67430e-11
c  = 299792458.0
Msun = 1.98847e30
a0_can = 9.3619e-11
a0_alt = 1.1279e-10

footings = {}
for name, a0 in (("canonical", a0_can), ("alternative", a0_alt)):
    rho_L = 4.0*a0**2/(G*c**2)                 # kappa = 1/2 -> a0 = (c/2) sqrt(G rho)
    kappa_fixed_rho = a0/(c*math.sqrt(G*rho_L))  # if rho_L held at the OTHER footing's value
    Mb = 1.0e11*Msun
    rM = math.sqrt(G*Mb/a0)
    vflat = (G*Mb*a0)**0.25
    footings[name] = {
        "a0": a0,
        "kappa_adopted": 0.5,
        "rho_Lambda": rho_L,
        "epsilon_Lambda": rho_L*c**2,
        "Lambda_eff_same_G": 32.0*math.pi*a0**2/c**4,
        "r_M(1e11 Msun)": rM,
        "v_flat(1e11 Msun)": vflat,
    }
# cross-footing: kappa implied by alternative a0 if canonical rho_Lambda held fixed
rho_can = footings["canonical"]["rho_Lambda"]
footings["alternative"]["kappa_if_canonical_rho_fixed"] = a0_alt/(c*math.sqrt(G*rho_can))

t1 = time.time()
out = {
  "symbolic": symbolic,
  "numeric_20000_samples": {
     "C1_max_abs_residual|Hleg-Hcan|": maxres_C1,
     "C3_max_abs_residual|sigmaH+sigmaR|": maxres_C3,
     "C4_max_abs_residual|mismatch-2Kd|": maxres_C4,
     "max_Kd_seen": maxK,
  },
  "footings": footings,
  "wall_s": round(t1-t0, 3),
}
print(json.dumps(out, indent=1, default=str))
with open("raw_output.json", "w") as f:
    json.dump(out, f, indent=1, default=str)

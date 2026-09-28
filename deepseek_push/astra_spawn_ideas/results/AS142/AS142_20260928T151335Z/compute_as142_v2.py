#!/usr/bin/env python3
"""
AS142 — Derive the carrier Legendre transform without freezing t_c.
Branch CA5-GNC-R (inherited CA4-GNC host). Bounded prototype: <=120 s, <=512 MB, 1 thread.

Setup (CA5-GNC-R, ACTION.md R1 + PERSPECTIVE_VARIANT P1-P7, inherited CA4-GNC host FINAL_ACTION (4)):
  t_c = 1 + Z - <Z>_h  (>0, varied, NOT frozen)
  L_d = t_c K_d - W_exc/t_c - V0 F(t_c),   F(t)=1+(t-1)^4/t^2,  F'(t)=2(t-1)^3(t+1)/t^3
  K_d = (1/2) sum_A n(phi_A)^2,  W_exc = (1/2) sum_A |D phi_A|^2 + Vmix (V0 floor separate in R-variant)
  pi_A = sqrt(h) p_A,  p_A = Pi_A/sqrt(h) = t_c n(phi_A)
  phi_dot_A = N n(phi_A) + N^i D_i phi_A   (shift retained)

Checks:
  C1  Legendre identity WITH shift:  H = sum_A Pi_A phi_dot_A - N sqrt(h) L_d
        = N sqrt(h)[(sum p_A^2/2 + W_exc)/t_c + V0 F(t_c)] + sqrt(h) sum_A p_A (N^i D_i phi_A)
      verified symbolically (id of sympy expressions) and numerically.
  C2  Velocity solve: n_A = p_A/t_c  (p_A = Pi_A/sqrt(h)); phi_dot_A = N n_A + N^i D_i phi_A.
  C3  Canonical Z-stationarity at FIXED Pi vs velocity-form source (R3/R4 of ACTION.md):
      sigma_H := -d/dt_c[(sum p^2/2+W)/t_c + V0 F(t_c)] |_{p fixed}  ==  sigma_R = K_d + W/t_c^2 - V0 F'(t_c)
      after substitution sum p^2/2 = t_c^2 K_d.  (exact identity sigma_H = -sigma_R; R4 matches.)
  C4  NEGATIVE CONTROL (capable of failing): differentiate the TRANSFORMED Hamiltonian at FIXED
      VELOCITIES n_A instead of fixed Pi_A; source becomes +K_d - W/t_c^2 + V0 F'(t_c).
      Difference vs true fixed-Pi source = 2 K_d = sum_A n_A^2 != 0 for moving carriers -> mismatch DETECTED.
  C5  Limiting/consistency: F(1)=1, F'(1)=0, t=1 inactive branch H_R -> N sqrt(h)[sum p^2/2+W+V0];
      homogeneous rho_v=V0, P_v=-V0; rho_R - t sigma_R = V0(F + t F') identity.
  C6  Footings (kappa = 1/2 adopted): a0 = (c/2)*sqrt(G*rho_Lambda).
      canonical a0 = 9.3619e-11 m/s^2, alternative a0 = 1.1279e-10 m/s^2 SEPARATE.
      rho_Lambda = 4 a0^2/(G c^2); r_M = sqrt(G M_b/a0); v_flat^4 = G M_b a0.
"""
import json, math, time
import sympy as sp

t0 = time.time()

# ---------------- symbolic section ----------------
t, N, s, V0, F = sp.symbols('t N s V0 F', positive=True)          # t = t_c (carrier lapse factor, parametric)
n1, n2, n3 = sp.symbols('n1 n2 n3', real=True)                    # velocities n(phi_A)
p1, p2, p3 = sp.symbols('p1 p2 p3', real=True)                    # canonical p_A = Pi_A/sqrt(h)
sh1, sh2, sh3 = sp.symbols('sh1 sh2 sh3', real=True)              # shift data N^i D_i phi_A
W_exc = sp.symbols('W_exc', positive=True)                        # spatial excitation energy density

Kd = (n1**2 + n2**2 + n3**2)/2                                    # K_d = 1/2 sum n_A^2

# C2: velocity solve: p_A = t_c n_A  ->  n_A = p_A / t_c   (t_c kept symbolic; solved, not frozen)
# phi_dot_A = N n_A + N^i D_i phi_A  (shift retained)
phi_dot = [N*p1/t + sh1, N*p2/t + sh2, N*p3/t + sh3]

# C1: Legendre transform at fixed (parametric) t_c:  H = sum Pi_A phi_dot_A - N sqrt(h) L_d
#   Pi_A = sqrt(h) p_A ;  L_d = t K_d - W_exc/t - V0 F
H_full_expr = sp.expand(
    (p1*phi_dot[0] + p2*phi_dot[1] + p3*phi_dot[2]) * s            # sum Pi_A phi_dot_A  (s=sqrt h)
    - s * N * (t*Kd - W_exc/t - V0*F)                              # - L_d * N * sqrt(h)
)
# substitute p_A = t n_A  (momentum-velocity relation)
subs = {p1: t*n1, p2: t*n2, p3: t*n3}
H_Leg = sp.simplify(H_full_expr.subs(subs))
# displayed target: N sqrt(h)[(sum p^2/2+W_exc)/t + V0 F] + sqrt(h) sum_A p_A (N^i D_i phi_A), p_A=t n_A:
H_disp = sp.simplify(
    N*s*((n1**2 + n2**2 + n3**2)*t/2 + W_exc/t + V0*F)
    + s*t*(n1*sh1 + n2*sh2 + n3*sh3)
)
res_C1 = sp.simplify(H_Leg - H_disp)                              # must be 0

# C3: canonical Z-source at fixed Pi -> sigma_H, compare to velocity source sigma_R
# F treated as a function F(t_c); Fp := Derivative(F(t),t) as an independent symbol.
Ffun_sym = sp.Function('F')(t)
eps = (p1**2 + p2**2 + p3**2)/2 + W_exc                          # epsilon_0 canonical density
sigma_H = sp.simplify(sp.diff(eps/t + V0*Ffun_sym, t))           # dH_c/dt at fixed p (per unit N sqrt(h)): -(eps)/t^2 + V0 F'(t)
sigma_H_subst = sp.simplify(sigma_H.subs(subs))                  # at the image p = t n  ->  -(Kd + W/t^2) + V0 F'(t)
Fp = sp.symbols('Fp', real=True)                                 # F'(t_c)
sigma_H_subst = sigma_H_subst.replace(sp.Derivative(Ffun_sym, t), Fp).replace(Ffun_sym, sp.Symbol('F'))
sigma_R = sp.simplify(Kd + W_exc/t**2 - V0*Fp)                   # R3 velocity-form source
res_C3 = sp.simplify(sigma_H_subst + sigma_R)                    # must be 0  (sigma_H = -sigma_R)

# C4: negative control - differentiate at FIXED VELOCITIES instead of fixed p
# velocity-form image of the canonical density: h_v = t Kd + W/t + V0 F(t)  (p = t n substituted)
h_v = sp.simplify(t*Kd + W_exc/t + V0*Ffun_sym)
sigma_fixedn = sp.simplify(sp.diff(h_v, t))                      # dH_c/dt at fixed n = Kd - W/t^2 + V0 F'(t)
sigma_fixedn = sigma_fixedn.replace(sp.Derivative(Ffun_sym, t), Fp).replace(Ffun_sym, sp.Symbol('F'))
# at the SAME phase point (p = t n), the fixed-p source is sigma_H_subst:
mismatch = sp.simplify(sigma_fixedn - sigma_H_subst)
res_C4 = sp.simplify(mismatch - (n1**2 + n2**2 + n3**2))         # must be 0: mismatch = 2 Kd

# C5: F checks
Ffun = 1 + (t-1)**4/t**2
Fp_expr = sp.diff(Ffun, t); Fpp_expr = sp.diff(Ffun, t, 2); Fppp_expr = sp.diff(Ffun, t, 3)
C5 = {
  "F(1)": sp.simplify(Ffun.subs(t, 1)),
  "F'(1)": sp.simplify(Fp_expr.subs(t, 1)),
  "F''(1)": sp.simplify(Fpp_expr.subs(t, 1)),
  "F'''(1)": sp.simplify(Fppp_expr.subs(t, 1)),
  "F_minus1_times_t2_minus(t-1)^4": sp.simplify((Ffun - 1)*t**2 - (t-1)**4),
}
# inactive branch t=1: H_R -> N sqrt(h)[sum p^2/2 + W + V0]
H_t1 = sp.simplify((sp.simplify(N*s*((n1**2+n2**2+n3**2)*t/2 + W_exc/t + V0*Ffun))).subs(t, 1))
C5["H_t1_residual"] = sp.simplify(H_t1 - N*s*((n1**2+n2**2+n3**2)/2 + W_exc + V0))
# homogeneous: rho_R = t Kd + W/t + V0 F ; sigma_R = Kd + W/t^2 - V0 F' ; rho_R - t sigma_R = V0(F + t F')
rho_R = t*Kd + W_exc/t + V0*Ffun
sig_R_t = Kd + W_exc/t**2 - V0*Fp_expr
C5["rhoR_minus_t_sigmaR_identity"] = sp.simplify(rho_R - t*sig_R_t - V0*(Ffun + t*Fp_expr))

symbolic = {
  "C1_H_Legendre": str(H_Leg),
  "C1_H_displayed": str(H_disp),
  "C1_residual": str(res_C1),
  "C2_solve": "n_A = p_A/t_c ; phi_dot_A = N n_A + N^i D_i phi_A (shift retained, t_c NOT frozen)",
  "C3_sigma_H(fixed p, substituted)": str(sigma_H_subst),
  "C3_sigma_R(velocity form)": str(sigma_R),
  "C3_residual_sigmaH_plus_sigmaR": str(res_C3),
  "C4_sigma(fixed n)": str(sigma_fixedn),
  "C4_sigma(fixed p)@same_point": str(sigma_H_subst),
  "C4_mismatch": str(mismatch),
  "C4_residual_mismatch_minus_2Kd": str(res_C4),
  "C5": {k: str(v) for k, v in C5.items()},
}

# ---------------- numeric section ----------------
def Fnum(tv): return 1.0 + (tv-1.0)**4/tv**2
def Fpnum(tv): return 2.0*(tv-1.0)**3*(tv+1.0)/tv**3

rng = 12345
def rand():
    global rng
    rng ^= (rng << 13) & 0xFFFFFFFF; rng ^= rng >> 17; rng ^= (rng << 5) & 0xFFFFFFFF
    return (rng % 1000000)/1000000.0

mx = {"C1": 0.0, "C3": 0.0, "C4": 0.0}
maxK = 0.0
for _ in range(50000):
    tv  = 0.2 + 2.8*rand()
    n1v, n2v, n3v = (2.0*rand()-1.0)*2, (2.0*rand()-1.0)*2, (2.0*rand()-1.0)*2
    Wv, V0v, Nv, sv = 1.0+9.0*rand(), 0.1+9.9*rand(), 0.5+1.5*rand(), 1.0+9.0*rand()
    Kdv = (n1v**2+n2v**2+n3v**2)/2
    sh1v, sh2v, sh3v = rand()-0.5, rand()-0.5, rand()-0.5
    # C1 (with shift, s = sqrt(h))
    Hleg = sv*Nv*(tv*Kdv + Wv/tv + V0v*Fnum(tv)) + sv*tv*(n1v*sh1v + n2v*sh2v + n3v*sh3v)
    Hcan = (sv*Nv*(((tv*n1v)**2+(tv*n2v)**2+(tv*n3v)**2)/2 + Wv)/tv + sv*Nv*V0v*Fnum(tv)
            + sv*(tv*n1v*sh1v + tv*n2v*sh2v + tv*n3v*sh3v))
    mx["C1"] = max(mx["C1"], abs(Hleg-Hcan))
    # C3
    sH = -(((tv*n1v)**2+(tv*n2v)**2+(tv*n3v)**2)/2 + Wv)/tv**2 + V0v*Fpnum(tv)
    sR = Kdv + Wv/tv**2 - V0v*Fpnum(tv)
    mx["C3"] = max(mx["C3"], abs(sH + sR))
    # C4
    sFn = Kdv - Wv/tv**2 + V0v*Fpnum(tv)
    mx["C4"] = max(mx["C4"], abs((sFn - sH) - (n1v**2+n2v**2+n3v**2)))
    maxK = max(maxK, Kdv)

# ---------------- footings (SI) ----------------
G  = 6.67430e-11
c  = 299792458.0
Msun = 1.98847e30
a0_can = 9.3619e-11
a0_alt = 1.1279e-10

footings = {}
for name, a0 in (("canonical", a0_can), ("alternative", a0_alt)):
    rho_L = 4.0*a0**2/(G*c**2)
    Mb = 1.0e11*Msun
    footings[name] = {
        "a0": a0,
        "kappa": 0.5,
        "rho_Lambda": rho_L,
        "epsilon_Lambda": rho_L*c**2,
        "Lambda_eff": 32.0*math.pi*a0**2/c**4,
        "r_M(1e11 Msun)": math.sqrt(G*Mb/a0),
        "v_flat(1e11 Msun)": (G*Mb*a0)**0.25,
    }
rho_can = footings["canonical"]["rho_Lambda"]
footings["alternative"]["kappa_if_canonical_rho_fixed"] = a0_alt/(c*math.sqrt(G*rho_can))

t1 = time.time()
out = {
  "symbolic": symbolic,
  "numeric_50000_samples": mx,
  "footings": footings,
  "wall_s": round(t1-t0, 3),
}
print(json.dumps(out, indent=1, default=str))
with open("raw_output.json", "w") as f:
    json.dump(out, f, indent=1, default=str)
#!/usr/bin/env python3
"""
ROUTE 2 [mi_vs_aqual]: Quantify the MI-vs-AQUAL EFE difference for the wide-binary gamma_cap.
How wrong was the normal-MOND headline (AQUAL/simple-mu gamma_cap = 1.32)?

THE WHOLE POINT: use the FRAMEWORK'S OWN modified-inertia (dS-Unruh), do NOT smuggle simple-mu/AQUAL.
The framework interpolation is the dS-Unruh / Unruh-MOND form:
    g_obs = sqrt(g_N^2 + g_N a0) = g_N nu(g_N/a0),  nu(y) = sqrt(1 + 1/y).
This is NOT McGaugh simple-mu (mu=x/(1+x)) and NOT the standard mu (x/sqrt(1+x^2)).

We compute the SAME wide-binary EFE config THREE ways with the framework a0=9.36e-11 (and 1.2e-10 row):
  (a) framework dS-Unruh MI  -- the framework's own prediction (vector-MI kernel on total accel)
  (b) AQUAL anisotropic-G with simple-mu  -- the normal-MOND machinery in the banked 1.32 headline
  (c) simple-mu nu-cap (1D)  -- the simple interpolation, vector-MI prescription
plus, for completeness, the standard-mu (sharp) shape that the banked 'F4/standard' actually used.

MI PRESCRIPTION (Milgrom 2011/2023, MOND as modified inertia):
  - For a CIRCULAR orbit with NO external field, MI gives EXACTLY the algebraic MOND relation:
        mu(V^2/(R a0)) V^2/R = g_N   <=>   g_obs = g_N nu(g_N/a0).   (astroweb/Scholarpedia)
  - In a DOMINANT external field the EFE is governed by nu/mu evaluated on the TOTAL worldline
    acceleration |a_ext + a_int|. The standard vector-MI prescription: the boost is the orientation
    average of nu(|y_ext zhat + y_int nhat|) over the internal-orbit direction nhat. This is the
    framework's actual MI EFE -- NOT the AQUAL anisotropic-G tensor (Milgrom proved MI != MG for EFE).
    Caveat (Milgrom): for non-circular / time-varying internal motion MI carries a theta>1 frequency
    factor; for the quasi-circular median statistic theta->1 to leading order (flagged, second order).

C. Zimmerman campaign, Opus 4.8 (1M) extended research, 2026-06-14.
"""
import numpy as np
rng = np.random.default_rng(20260614)

# ---- the three interpolation shapes (as MI nu = g_obs/g_N as a function of y = g/a0) ----
def nu_dsU(y):     # FRAMEWORK dS-Unruh / Unruh-MOND:  g_obs = sqrt(g^2 + g a0)  => nu = sqrt(1+1/y)
    return np.sqrt(1.0 + 1.0/y)
def nu_simple(y):  # simple-mu mu=x/(1+x):  inversion nu(y) = 1/2 + sqrt(1/4 + 1/y)
    return 0.5 + np.sqrt(0.25 + 1.0/y)
def nu_std(y):     # standard-mu mu=x/sqrt(1+x^2):  nu = sqrt((1+sqrt(1+4/y^2))/2)
    return np.sqrt((1.0 + np.sqrt(1.0 + 4.0/y**2))/2.0)

SHAPES = {'dS-Unruh (FRAMEWORK)': nu_dsU, 'simple-mu': nu_simple, 'standard-mu (sharp)': nu_std}

g_ext = 2.151e-10   # V_c^2/R0 = (233 km/s)^2/8.178 kpc, footing-independent

# =====================================================================================
# (a)/(c) VECTOR-MI boost: orientation-average of nu(|y_ext + y_int|) over internal direction
#     gamma_MI(s) = < nu(|y_ext zhat + y_int nhat|) >_nhat   (acceleration boost g_obs/g_N)
#     EFE CAP = limit y_int -> 0:  gamma_cap_MI = nu(y_ext)  (isotropic, the internal accel vanishes)
# =====================================================================================
def gamma_MI(nu, y_int, y_ext, n=400000):
    u = rng.uniform(-1, 1, n)                       # cos angle(internal accel, external field), isotropic
    ytot = np.sqrt(y_ext**2 + y_int**2 + 2*y_ext*y_int*u)
    return np.mean(nu(ytot))

# =====================================================================================
# (b) AQUAL anisotropic-G tensor (Bekenstein-Milgrom 1984 / Banik-Zhao 2018) -- MODIFIED GRAVITY
#     deep inside a dominant external field, with e=g_ext/a0, mu the AQUAL IF, L=dln mu/dln x at e:
#         G_par/G  = 1/[mu(e)(1+L)]   (along g_ext)
#         G_perp/G = 1/mu(e)          (perpendicular)
#     orbit/orientation average:  gamma_cap = (1/3) G_par/G + (2/3) G_perp/G.
#     This is the normal-MOND machinery in the banked 1.32 headline (uses simple-mu).
# =====================================================================================
def mu_simple_x(x):   return x/(1.0+x)              # simple-mu in mu(x) form
def mu_std_x(x):      return x/np.sqrt(1.0+x*x)     # standard-mu in mu(x) form
def aqual_cap(mu_x, e, dx=1e-6):
    m  = mu_x(e)
    L  = (np.log(mu_x(e*(1+dx))) - np.log(mu_x(e*(1-dx))))/(2*dx)   # dln mu/dln x at x=e
    Gpar  = 1.0/(m*(1.0+L))
    Gperp = 1.0/m
    return (1.0/3.0)*Gpar + (2.0/3.0)*Gperp, m, L, Gpar, Gperp

# =====================================================================================
# RUN
# =====================================================================================
for a0, lab in [(9.36e-11, 'FRAMEWORK a0=9.36e-11'), (1.20e-10, 'canonical a0=1.20e-10')]:
    y_ext = g_ext/a0
    print("="*100)
    print(f"  {lab}   |   e = y_ext = g_ext/a0 = {y_ext:.4f}")
    print("="*100)

    # ---- (i) vector-MI gamma(s) curve + cap, all three shapes ----
    print("\n  (i) VECTOR-MI boost gamma = g_obs/g_N  (orientation-averaged nu(|y_ext+y_int|)); v/v_N = sqrt(gamma)")
    print(f"      {'y_int=g_N/a0':>13s} | " + " | ".join(f"{k:>22s}" for k in SHAPES))
    for y_int in (1.0, 0.5, 0.18, 0.06, 0.018, 1e-6):
        row = []
        for nu in SHAPES.values():
            g = gamma_MI(nu, y_int, y_ext)
            row.append(g)
        tag = "  <-- EFE CAP (y_int->0)" if y_int < 1e-3 else ""
        print(f"      {y_int:13.4f} | " + " | ".join(f"g={g:6.4f} v={100*(np.sqrt(g)-1):+5.1f}%" for g in row) + tag)

    # cap is exactly nu(y_ext) for MI (internal accel vanishes -> isotropic)
    print("\n      MI EFE CAP (closed form gamma_cap = nu(y_ext)):")
    for k, nu in SHAPES.items():
        gc = nu(y_ext)
        print(f"        {k:24s}: gamma_cap = {gc:.4f}   (v/v_N = {100*(np.sqrt(gc)-1):+.1f}%)")

    # ---- (ii) AQUAL anisotropic-G cap (MODIFIED GRAVITY) for simple-mu and standard-mu ----
    print("\n  (ii) AQUAL anisotropic-G EFE CAP (MODIFIED GRAVITY, Bekenstein-Milgrom tensor):")
    for k, mux in [('simple-mu', mu_simple_x), ('standard-mu (sharp)', mu_std_x)]:
        cap, m, L, Gpar, Gperp = aqual_cap(mux, y_ext)
        print(f"        {k:24s}: mu(e)={m:.4f} L={L:+.4f} G_par/G={Gpar:.4f} G_perp/G={Gperp:.4f}"
              f"  => gamma_cap={cap:.4f} (v/v_N={100*(np.sqrt(cap)-1):+.1f}%)")
    print()

# =====================================================================================
# HEAD-TO-HEAD at the framework a0: the three numbers the prompt asks to tabulate
# =====================================================================================
y_ext = g_ext/9.36e-11
print("#"*100)
print("# HEAD-TO-HEAD EFE CAP at FRAMEWORK a0=9.36e-11 (e=2.30) -- the three ways")
print("#"*100)
g_a = nu_dsU(y_ext)                                   # (a) framework dS-Unruh MI
cap_b, *_ = aqual_cap(mu_simple_x, y_ext)             # (b) AQUAL simple-mu (the banked headline machinery)
g_c = nu_simple(y_ext)                                # (c) simple-mu nu-cap (1D MI)
g_std_mi = nu_std(y_ext)                              # what the banked 'F4/standard' actually computed
print(f"  (a) framework dS-Unruh MI   gamma_cap = {g_a:.4f}   (v/v_N {100*(np.sqrt(g_a)-1):+.1f}%)  <== THE FRAMEWORK'S OWN")
print(f"  (b) AQUAL simple-mu (MG)    gamma_cap = {cap_b:.4f}   (v/v_N {100*(np.sqrt(cap_b)-1):+.1f}%)  <== banked headline 1.32")
print(f"  (c) simple-mu nu-cap (1D)   gamma_cap = {g_c:.4f}   (v/v_N {100*(np.sqrt(g_c)-1):+.1f}%)")
print(f"  (x) standard-mu MI (sharp)  gamma_cap = {g_std_mi:.4f}   (v/v_N {100*(np.sqrt(g_std_mi)-1):+.1f}%)  <== banked 'F4/standard' MISLABEL")
print()
print(f"  MI(framework dS-Unruh) vs AQUAL-simple-mu(1.32):  Delta gamma = {g_a - cap_b:+.4f}  ({100*(g_a-cap_b)/cap_b:+.1f}%)")
print(f"  => framework MI gives a {'LARGER' if g_a>cap_b else 'SMALLER'} boost than the AQUAL 1.32 headline by |Delta|={abs(g_a-cap_b):.3f}")
print(f"  Headline error threshold from prompt: >0.1 in gamma means the headline is WRONG.  |Delta|={abs(g_a-cap_b):.3f} "
      f"=> {'WRONG (recompute verdict)' if abs(g_a-cap_b)>0.1 else 'cosmetic'}")

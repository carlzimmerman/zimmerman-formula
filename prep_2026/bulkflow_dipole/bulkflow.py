#!/usr/bin/env python3
"""
LANE A -- BULK FLOW vs Sarkar/Qin-2021 CMB-frame convergence critique.

Framework: de Sitter-Unruh MODIFIED-INERTIA.
  a0 = cH_Lambda/Z = 9.36e-11 (canonical)  |  1.13e-10 (alt total-rho footing)
  nu(y) = sqrt(1 + 1/y),  y = g_bar/a0   (Milgrom-1999 kernel; framework coeff cH_L/Z)

Pipeline (HONEST, quasi-linear -- see RESULT.md flag):
  (1) Reproduce LCDM linear bulk flow V_LCDM(R) from a BBKS-CDM P(k), sigma8 normed.
  (2) Compute RMS coherent peculiar acceleration g_pec(R) on the SAME P(k), same window.
      (Newtonian linear relation g = (3/2) H0 Om / f  *  sigma_v, field-level, same k-weight.)
  (3) MI boost B(R) = nu(g_pec(R)/a0), both footings -> V_MI(R) = B(R) V_LCDM(R).
  (4) Overlay on Qin-2021 CF4TF/W09/... points.

We ALSO report the alternative reading in which nu is fed the LOCAL environmental
acceleration (~a0) rather than the tiny coherent field -- the two readings bracket
the effect (see RESULT.md). NO 'proves' language; a null is verified as hard as a win.
"""
import numpy as np
from scipy.integrate import quad

# ---------------- cosmology ----------------
h      = 0.70
Om     = 0.30
Ob     = 0.048
ns     = 0.96
s8     = 0.80
f_g    = Om**0.55                 # growth rate ~0.51
H0_kms = 100.0*h                  # km/s/Mpc
Mpc_m  = 3.0856775814913673e22
H0_si  = H0_kms*1e3/Mpc_m         # 1/s

A0_CANON = 9.36e-11               # m/s^2  (rho_DE / cH_Lambda / Z)
A0_ALT   = 1.13e-10               # m/s^2  (rho_total / cH0)

# ---------------- BBKS transfer + P(k) ----------------
# Sugiyama-corrected shape parameter (Ob screening)
Gamma = Om*h*np.exp(-Ob*(1.0+np.sqrt(2.0*h)/Om))

def T_bbks(k):                    # k in h/Mpc
    q = k/Gamma
    q = np.where(q < 1e-8, 1e-8, q)
    t = (np.log(1.0+2.34*q)/(2.34*q)) * \
        (1.0 + 3.89*q + (16.1*q)**2 + (5.46*q)**3 + (6.71*q)**4)**(-0.25)
    return t

def Pk_unnorm(k):                 # (Mpc/h)^3 up to A
    return k**ns * T_bbks(k)**2

def Wth(x):                       # top-hat window (Fourier)
    x = np.asarray(x, float)
    out = np.ones_like(x)
    m = x > 1e-4
    xm = x[m]
    out[m] = 3.0*(np.sin(xm)-xm*np.cos(xm))/xm**3
    return out

# normalize to sigma8
def sig2_R(R, A):                 # density variance in sphere R (Mpc/h)
    integ = lambda k: A*Pk_unnorm(k)*Wth(k*R)**2*k**2
    val,_ = quad(integ, 1e-4, 50.0, limit=300)
    return val/(2.0*np.pi**2)
A_norm = s8**2 / sig2_R(8.0, 1.0)

# ---------------- bulk-flow variance ----------------
# sigma_v^2(R) = (H0 f)^2/(2 pi^2) * INT P(k) W^2(kR) dk   (3D vector variance)
def sigmav_kms(R):
    integ = lambda k: A_norm*Pk_unnorm(k)*Wth(k*R)**2
    val,_ = quad(integ, 1e-4, 50.0, limit=300)
    var = (H0_kms*f_g)**2/(2.0*np.pi**2)*val   # (km/s)^2
    return np.sqrt(var)

# field-level Newtonian relation: v = (2 f)/(3 H0 Om) g  ->  g = 3 H0 Om/(2 f) * v
# (g and v share the SAME k-weight delta(k)/k, so g_rms(R)/sigma_v(R) is a constant.)
def gpec_si(R):
    v_ms = sigmav_kms(R)*1e3
    return (3.0*H0_si*Om)/(2.0*f_g)*v_ms       # m/s^2

def nu(y):
    return np.sqrt(1.0 + 1.0/y)

# ---------------- Qin 2021 (approx, from the slide) ----------------
# (label, R [h^-1 Mpc], V [km/s])
qin = [("CF4TF",35,380),("W09",100,410),("H14",30,260),("S16",60,290),
       ("M13",50,310),("T12",100,250),("D11",150,190),("C11",180,260)]

Rgrid = np.linspace(20, 300, 40)
Vl    = np.array([sigmav_kms(R) for R in Rgrid])
g_R   = np.array([gpec_si(R)   for R in Rgrid])

print("="*74)
print("LANE A -- MODIFIED-INERTIA BULK-FLOW BOOST  (both footings)")
print("="*74)
print(f"Gamma={Gamma:.4f}  f={f_g:.3f}  sigma8={s8}  A_norm={A_norm:.4e}")
print(f"a0 canonical={A0_CANON:.3e}  alt={A0_ALT:.3e}  m/s^2\n")

print(f"{'R[h/Mpc]':>8} {'V_LCDM':>8} {'g_pec':>10} {'y_can':>8} {'nu_can':>7} "
      f"{'V_MI_can':>9} {'nu_alt':>7} {'V_MI_alt':>9}")
for R in [30,50,100,150,200,300]:
    V = sigmav_kms(R); g = gpec_si(R)
    yc, ya = g/A0_CANON, g/A0_ALT
    nc, na = nu(yc), nu(ya)
    print(f"{R:8.0f} {V:8.1f} {g:10.3e} {yc:8.4f} {nc:7.2f} "
          f"{V*nc:9.1f} {na:7.2f} {V*na:9.1f}")

# summary numbers at the data scales
print("\n--- confrontation with Qin points (coherent-field reading) ---")
over = []
for lab,R,Vd in qin:
    V = sigmav_kms(R); g = gpec_si(R)
    nc = nu(g/A0_CANON)
    Vmi = V*nc
    over.append(Vmi/Vd)
    print(f"{lab:>6} R={R:4d}  data={Vd:4d}  V_LCDM={V:6.1f} "
          f"(data/LCDM={Vd/V:4.2f})  nu_can={nc:5.2f}  V_MI={Vmi:7.0f}  "
          f"V_MI/data={Vmi/Vd:5.1f}x")
over = np.array(over)
print(f"\nCoherent-field V_MI overshoots data by median {np.median(over):.1f}x "
      f"(range {over.min():.1f}-{over.max():.1f}x).")

# what nu would be NEEDED to lift LCDM to the data
needed = np.mean([Vd/sigmav_kms(R) for lab,R,Vd in qin])
print(f"nu NEEDED to fit (mean data/LCDM) = {needed:.2f}  "
      f"-> requires g_bar/a0 = {1.0/(needed**2-1):.2f} "
      f"(i.e. g ~ {(1.0/(needed**2-1))*A0_CANON:.2e} m/s^2, ~environmental/a0-scale,\n"
      f"     NOT the coherent field g_pec~{gpec_si(60):.1e}).")

# ---------------- figure ----------------
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8.4,6.0))
    # LCDM curve
    ax.plot(Rgrid, Vl, 'm-', lw=2.2, label=r'$V_{\Lambda CDM}(R)$ (this work, BBKS)')
    # MI coherent-field boost, both footings
    Bc = np.array([nu(g/A0_CANON) for g in g_R])
    Ba = np.array([nu(g/A0_ALT)   for g in g_R])
    ax.plot(Rgrid, Vl*Bc, 'r-',  lw=2.0,
            label=r'$V_{MI}=\nu(g_{pec}/a_0)\,V_{\Lambda CDM}$  (canon, coherent field)')
    ax.plot(Rgrid, Vl*Ba, 'r--', lw=1.6, label='  (alt footing, coherent field)')
    # milder environmental-a0 reading band nu(0.5..2)
    ax.fill_between(Rgrid, Vl*nu(2.0), Vl*nu(0.5), color='orange', alpha=0.25,
                    label=r'MI env.-$a_0$ reading  $\nu(g\sim0.5$-$2\,a_0)$')
    # data
    for lab,R,Vd in qin:
        ax.errorbar(R, Vd, yerr=30, fmt='ko', ms=6, capsize=3)
        ax.annotate(lab, (R,Vd), textcoords="offset points", xytext=(5,5), fontsize=8)
    ax.set_yscale('log')
    ax.set_xlabel(r'$R\ [h^{-1}\,{\rm Mpc}]$')
    ax.set_ylabel(r'bulk flow $V\ [{\rm km/s}]$')
    ax.set_title('MI bulk-flow boost vs Qin+2021 (Sarkar critique) -- quasi-linear estimate')
    ax.set_ylim(30, 8000)
    ax.legend(fontsize=8, loc='upper right')
    ax.grid(alpha=0.3, which='both')
    fig.tight_layout()
    fig.savefig("/Users/carlzimmerman/new_physics/prep_2026/bulkflow_dipole/bulkflow_fig.png", dpi=130)
    print("\nfigure -> bulkflow_fig.png")
except Exception as e:
    print("plot skipped:", e)

print("\nDONE (exit 0).")

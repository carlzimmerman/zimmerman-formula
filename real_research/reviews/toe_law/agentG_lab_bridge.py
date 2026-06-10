#!/usr/bin/env python3
"""
agentG: the laboratory / particle-physics confrontation of the F4 modified-inertia shape
mu_std(x) = x/sqrt(1+x^2), x = |a|/s, s in {9.36e-11 (framework a0 = c^2 sqrt(Lambda/32pi)),
5.42e-10 (hostile = cH_Lambda, the bath coefficient)} -- against ALREADY-PUBLISHED experiments.

Prescription map (the deliverable is prescription-RESOLVED; "F4 predicts" is ill-posed without it):
  P-A  instantaneous total KINEMATIC |a| in the local quasi-inertial frame (gravity = force).
       This is the banked reading used repo-wide (SPARC, Saturn, WB-EFE, eccentric orbits).
       Lab background: Earth rotation ~2.3e-2 m/s^2 (dominant), solar orbit 5.9e-3, galactic 2.2e-10.
  P-B  instantaneous total PROPER |a| (accelerometer reading; the UDW/bath-mechanism-natural one).
       Lab suspended mass: 9.8. Free-faller: ~0  -> deep-MOND IN THE LAB. (NB: P-B alone cannot be
       the galactic law -- orbiting stars are free-falling, x_proper=0 -> no MOND. Flagged.)
  P-C  linearized response kernel about the background trajectory (the Door-I lambda^2 structure:
       every finite-order kernel coefficient is A(kappa)+a^2 B(kappa), kappa = background total).
       Small superposed oscillations are LINEAR -> they inherit mu(x_background), never mu(x_osc).
  P-D  mode/axis-AMPLITUDE reading: mu evaluated on the small oscillatory acceleration itself
       (= Gundlach's own Eq. (2): mu(|r theta''|/a0) per mass element). The only reading under
       which a lab signal scales with the SIGNAL's smallness.

Experiments pinned (real published bounds):
  [G07] Gundlach et al., PRL 98, 150801 (2007): torsion pendulum, kappa=2.36e-9 N m/rad,
        tau0=795 s, r_e=0.023 m, amplitudes 13 nrad..19 urad -> a in [1.9e-14, 2.7e-11] m/s^2;
        F prop a confirmed, residuals ~ +-2e-14 m/s^2 (Fig. 2), MOND-sim recovery a0 in 1e-16..1e-9.
  [AV86] Abramovici & Vager, PRD 34, 3240 (1986): F=ma agreement down to 3e-11 m/s^2.
  [PCC99] Peters, Chung & Chu, Nature 400, 849 (1999): atom gravimeter, |dg/g| ~ 3e-9 absolute.
  [A20] Asenbaum et al., PRL 125, 191101 (2020) (arXiv:2005.11624): dual-species AI EP test,
        eta = [1.6 +- 1.8(stat) +- 3.4(syst)]e-12, 2 s free fall (T ~ 0.955 s).
  [M22] MICROSCOPE final, PRL 129, 121102 (2022) (arXiv:2209.15487):
        eta(Ti,Pt) = [-1.5 +- 2.3(stat) +- 1.5(syst)]e-15; 710 km orbit.
  [BD21] Blinov & Draper, PRD 104, 076024 (2021) (arXiv:2107.03530): CKN-depletion vs lepton g-2.
C. Zimmerman / agentG, 2026-06-10. No git. Both normalizations, every prescription, both ways.
"""
import numpy as np

S_FW = 9.36e-11    # framework a0 = c^2 sqrt(Lambda/32pi)
S_H  = 5.42e-10    # hostile  = cH_Lambda (bath coefficient, Z-off)
NORM = [("framework 9.36e-11", S_FW), ("hostile cH_L 5.42e-10", S_H)]

def mu(x):  return x/np.sqrt(1.0+x*x)
def nu(y):
    """a = nu(y)*g_N solves mu(a/s)*a = g_N, y = g_N/s (exact inversion of mu_std)."""
    y = np.asarray(y, dtype=float)
    return np.sqrt((y+np.sqrt(y*y+4.0))/(2.0*y))

def dev_high_x(x):  # fractional deviation a/g_N - 1 = 1/(2x^2) for x >> 1
    return 1.0/(2.0*x*x)

print("="*100)
print("SECTION 0 -- backgrounds and sanity")
print("="*100)
OMEGA_E = 7.2921e-5                      # Earth sidereal rotation, rad/s
A_ROT   = OMEGA_E**2*6.371e6*np.cos(np.radians(47.65))   # Seattle latitude
A_ORB   = 5.93e-3                        # Earth orbital accel about Sun
A_GAL   = 2.15e-10                       # galactocentric (repo g_ext)
print(f"lab kinematic background (P-A): Earth rotation {A_ROT:.4f} m/s^2 (dominant), "
      f"solar orbit {A_ORB:.2e}, galactic {A_GAL:.2e}")
print(f"  -> |a_kin| range over a day: [{abs(A_ROT-A_ORB):.4f}, {A_ROT+A_ORB:.4f}] m/s^2; nominal {A_ROT:.4f}")
print(f"lab proper background (P-B, suspended body): g = 9.80 m/s^2")
# closure check of the kernel identity a0 = c E_L^2 / (2 hbar E_P)  (CKN seesaw, banked)
c=2.99792458e8; hbar=1.054572e-34; E_L=2.24e-3*1.602177e-19; E_P=1.9561e9
print(f"kernel closure check: c*E_Lambda^2/(2 hbar E_Planck) = {c*E_L**2/(2*hbar*E_P):.3e} m/s^2 "
      f"(= a0 to <1%; the banked CKN-seesaw identity)")

# ----------------------------------------------------------------------------------------------
print()
print("="*100)
print("TASK 1 -- Gundlach et al. PRL 98, 150801 (2007): torsion-balance test of F = ma")
print("="*100)
KAPPA=2.36e-9; TAU0=795.0; RE=0.023
W0=2*np.pi/TAU0; W02=W0*W0; I_P=KAPPA/W02
print(f"pendulum: kappa={KAPPA:.2e} N m/rad, tau0={TAU0} s, r_e={RE} m -> I={I_P:.3e} kg m^2")
A_MIN_ACC=5e-14          # smallest acceleration at which F prop a confirmed (paper abstract)
A_TOP_ACC=2.7e-11        # top of their amplitude range (19 urad)
RESID=2e-14              # residual envelope from Fig. 2, m/s^2
print(f"published bound: F prop a over a in [{A_MIN_ACC:.0e}, {A_TOP_ACC:.1e}] m/s^2, "
      f"residuals ~ +-{RESID:.0e} m/s^2;")
print(f"  fractional precision: {RESID/A_TOP_ACC*100:.2f}% at top of range, O(40%) at the 5e-14 floor")

print("\n--- P-A / P-B / P-C (background-anchored readings): predicted deviation 1/(2 x_bg^2) ---")
for lab,s in NORM:
    for bgn,bg in [("P-A kinematic 2.28e-2",A_ROT),("P-B proper 9.80",9.80)]:
        x=bg/s; d=dev_high_x(x)
        eps=RESID/1e-11   # demonstrated fractional bound at a_N = 1e-11 (mid-decade), = 0.2%
        print(f"  s={lab:24s} {bgn:22s}: x_bg={x:.3e}  dev={d:.2e}  "
              f"margin vs 0.2% bound = {eps/d:.1e}x  -> SAFE")
print("  P-C (linearized kernel about background): response to the mHz oscillation inherits "
      "mu(x_bg); amplitude")
print("  cannot enter a LINEAR kernel -> same numbers as above. Additionally the bath-kernel "
      "memory time at a=9.8 is")
tau_c=2*np.pi*c/9.80
print(f"  tau_c = 2 pi c/a = {tau_c:.2e} s -> omega_pend*tau_c = {W0*tau_c:.1e} >> 1: the pendulum "
      f"is deep-UV for the kernel;")
print("  the oscillation sees the BARE inertia (suppression beyond the static estimate). SAFE.")

print("\n--- P-D (amplitude reading; = the paper's own Eq. (2)) : full ODE integration ---")
def period_PD(A0, s, n_per=3):
    """Integrate mu(|r_e th''|/s) th'' = -w0^2 th exactly: th'' = -sign(th)(s/r_e) X,
       X = Y nu(Y), Y = w0^2 |th| r_e / s.  RK4; returns mean period from zero crossings."""
    Ymax=W02*A0*RE/s
    tau_guess=TAU0*max(0.02, Ymax**0.25 if Ymax<1 else 1.0)
    dt=tau_guess/4e4; t=0.0; th=A0; v=0.0
    def acc(th):
        if th==0.0: return 0.0
        Y=W02*abs(th)*RE/s
        X=Y*float(nu(Y))
        return -np.sign(th)*(s/RE)*X
    crossings=[]; last=th
    nstep=int(n_per*tau_guess/dt)+int(4e4)
    for i in range(nstep):
        k1v=acc(th);            k1x=v
        k2v=acc(th+0.5*dt*k1x); k2x=v+0.5*dt*k1v
        k3v=acc(th+0.5*dt*k2x); k3x=v+0.5*dt*k2v
        k4v=acc(th+dt*k3x);     k4x=v+dt*k3v
        th_n=th+dt/6*(k1x+2*k2x+2*k3x+k4x); v_n=v+dt/6*(k1v+2*k2v+2*k3v+k4v)
        t+=dt
        if last>0>=th_n and v_n<0: crossings.append(t- dt*th_n/(th_n-last+1e-300))
        last=th_n; th=th_n; v=v_n
        if len(crossings)>=2*n_per: break
    if len(crossings)<2: return np.nan
    per=np.diff(crossings)       # downward crossings only -> successive diffs ARE full periods
    return np.mean(per) if len(per)>0 else np.nan

# validation against the paper's own Fig. 1 simulation: a0 = 1e-12, amplitude ~200 nrad
tau_val=period_PD(200e-9, 1e-12)
print(f"  validation vs paper Fig. 1 (a0=1e-12, A=200 nrad): predicted period {tau_val:.0f} s "
      f"(ratio {tau_val/TAU0:.2f}); the figure shows ~3 cycles in ~1600 s (~530 s). "
      f"{'OK' if 400<tau_val<650 else 'CHECK'}")

for lab,s in NORM:
    print(f"  s = {lab}:")
    for aN,note in [(5e-14,"floor (their smallest confirmed)"),(1e-11,"mid-range"),
                    (A_TOP_ACC,"top of range")]:
        A0=aN/(RE*W02); Y=aN/s; nv=float(nu(Y))
        tau=period_PD(A0,s) if aN<=1e-11 else np.nan
        frac_bound=RESID/aN
        kill=(nv-1)/frac_bound
        tau_s = f"{tau:6.0f} s (x{tau/TAU0:.3f})" if np.isfinite(tau) else "   --"
        print(f"    a_N={aN:.1e} ({note:32s}): Y={Y:.2e} nu={nv:8.2f} "
              f"(accel excess {100*(nv-1):9.1f}%) period->{tau_s}  "
              f"observed |dev|<{100*frac_bound:5.1f}% -> effect-size kill x{kill:8.0f}")
    # the s-scale exclusion: largest s compatible with their residuals (two conservatisms)
    for eps,where,aref in [(0.5,"ultra-conservative: 50% at the 5e-14 floor",5e-14),
                           (0.002,"their 0.2% proportionality at 1e-11",1e-11)]:
        # solve nu(aref/s_k)-1 = eps  ->  bisect in s
        lo,hi=1e-18,1e-8
        for _ in range(200):
            mid=np.sqrt(lo*hi)
            if float(nu(aref/mid))-1>eps: hi=mid
            else: lo=mid
        s_k=np.sqrt(lo*hi)
        print(f"    P-D exclusion ({where:42s}): s_kill={s_k:.1e} -> this s EXCLUDED x{s/s_k:7.0f}")

print("\n--- the one P-A lab loophole, quantified (Ignatiev PRL 98, 101101 (2007), gr-qc/0612159) ---")
rate=OMEGA_E*A_ROT
for lab,s in NORM:
    print(f"  s={lab:24s}: kinematic-cancellation window 2s/(omega_E a_rot) = {2*s/rate:.1e} s "
          f"(Ignatiev-class ~1 ms, twice/yr, ~80deg lat); never attempted")

# ----------------------------------------------------------------------------------------------
print()
print("="*100)
print("TASK 2 -- atom interferometry: free-falling atoms (proper acceleration ~ 0)")
print("="*100)
print("--- existing gravimeter data (PCC99: |dg/g| ~ 3e-9; resol. 2e-8/shot, 1e-10/2 days) ---")
for lab,s in NORM:
    x=9.80/s; d=dev_high_x(x)
    print(f"  P-A  s={lab:24s}: falling atom x=g/s={x:.3e} -> dg/g={d:.2e}  "
          f"margin vs 3e-9: {3e-9/d:.1e}x  SAFE/UNTESTABLE")
print("  P-B  (proper): between pulses the atom is FORCE-FREE -> the worldline law mu(a)a=F reads "
      "0=0; photon kicks")
vrec=2*6.62607e-34/(780.241e-9*1.44316e-25)
print(f"       occur at a_pulse ~ v_rec/tau ~ {vrec:.3e}/1e-5 ~ {vrec/1e-5:.0e} m/s^2 (x>>1, "
      f"Newtonian recoil).")
print("       -> F4-P-B predicts EXACTLY the standard phase k_eff g T^2: existing AI gravimeter "
      "data are SILENT on F4. NO reading is tested by published AI data.")

print("\n--- THE DOOR: designed applied-force protocol (free-fall atom + calibrated sub-a0 force) ---")
print("    observable: extra differential phase dphi = k_eff (a - F/m) T^2, a = nu(y) F/m, y=(F/m)/s")
KEFF=4*np.pi/780.241e-9; T_INT=0.955
dstat=1.8e-12*9.8; dtot=np.sqrt(1.8**2+3.4**2)*1e-12*9.8
print(f"    instrument class [A20]: k_eff={KEFF:.3e} 1/m, T={T_INT} s; demonstrated differential-"
      f"acceleration accuracy: {dstat:.2e} (stat) / {dtot:.2e} (total) m/s^2")
for lab,s in NORM:
    yg=np.linspace(0.01,3.0,3000); da=s*yg*(nu(yg)-1.0)
    i=np.argmax(da); ymax=yg[i]; damax=da[i]
    print(f"  s={lab}:")
    print(f"    {'y=(F/m)/s':>10s} {'nu':>7s} {'a/F-1':>8s} {'Delta_a [m/s^2]':>16s} "
          f"{'dphi [rad]':>11s} {'sigma(stat)':>11s} {'sigma(tot)':>10s}")
    for y in (0.1,0.25,ymax,1.0,2.0):
        n=float(nu(y)); d=s*y*(n-1)
        print(f"    {y:10.3f} {n:7.3f} {100*(n-1):7.1f}% {d:16.2e} {KEFF*d*T_INT**2:11.2e} "
              f"{d/dstat:11.2f} {d/dtot:10.2f}")
    print(f"    optimum y={ymax:.2f}: Delta_a = {damax:.2e} m/s^2 = {damax/dstat:.1f} sigma(stat) "
          f"/ {damax/dtot:.1f} sigma(tot) per A20-equivalent campaign")

# ----------------------------------------------------------------------------------------------
print()
print("="*100)
print("TASK 3 -- MICROSCOPE (final results 2022): eta(Ti,Pt) = [-1.5 +- 2.3 +- 1.5]e-15")
print("="*100)
GM=3.986004e14; R_ORB=6.371e6+7.10e5
g_orb=GM/R_ORB**2; grad=2*GM/R_ORB**3
print(f"orbit: r={R_ORB/1e3:.0f} km -> g={g_orb:.2f} m/s^2; radial gravity gradient 2GM/r^3 = "
      f"{grad:.3e} /s^2")
sig_eta=np.sqrt(2.3**2+1.5**2)*1e-15
print(f"published bound: eta = -1.5e-15 +- {sig_eta:.1e} (total 1sigma); "
      f"differential-acceleration scale eta*g = {sig_eta*g_orb:.1e} m/s^2")
print("\n--- the EP channel: F4 prediction (ALL readings) ---")
print("  mu multiplies the inertia of BOTH masses identically (same trajectory, same x, "
      "composition-blind)")
print(f"  -> eta_F4 = 0 exactly. Measured: -1.5 +- {sig_eta/1e-15:.1f} e-15 -> consistent at "
      f"{1.5/(sig_eta/1e-15):.2f} sigma.")
print("  VERDICT: PASS but BLIND -- the celebrated 1e-15 carries ZERO bits about universal "
      "modified inertia.")
print("\n--- P-A (banked): common-mode inertia deviation ---")
for lab,s in NORM:
    x=g_orb/s; print(f"  s={lab:24s}: x={x:.2e} -> common-mode dev {dev_high_x(x):.2e}; "
                     f"no published channel at this level. SAFE/UNTESTABLE")
print("\n--- P-B (proper): the test masses' x = applied electrostatic acceleration / s ---")
w_spin=2*np.pi*2.9425e-3
rows=[("gravity gradient @ 10 um offset", grad*10e-6),
      ("gravity gradient @ 20 um offset", grad*20e-6),
      ("gravity gradient @ 100 um offset", grad*100e-6),
      ("centrifugal, V3 spin (2.94 mHz) @ 20 um", w_spin**2*20e-6),
      ("drag-free in-band residual (class)", 1e-12),
      ("in-flight calibration stimuli (class)", 1e-7)]
print(f"  {'applied-acceleration source':42s} {'a [m/s^2]':>10s} | "
      f"{'x_fw':>9s} {'mu_fw':>7s} | {'x_host':>9s} {'mu_host':>7s}")
for name,a in rows:
    xf=a/S_FW; xh=a/S_H
    print(f"  {name:42s} {a:10.1e} | {xf:9.2e} {float(mu(xf)):7.4f} | {xh:9.2e} {float(mu(xh)):7.4f}")
print("  -> under P-B the masses genuinely STRADDLE x=1 (the only macroscopic precision system "
      "that does),")
print("     but the F4 effect is a COMMON-MODE force/acceleration scale factor 1/mu(x): "
      "degenerate with gain")
print("     calibration (done at x>>1) and offset estimation. NOT constrained by the published "
      "eta; a dedicated")
print("     instrument-consistency reanalysis could reach the few-% to 10x anomalies predicted "
      "at x ~ 0.1-10.")

# ----------------------------------------------------------------------------------------------
print()
print("="*100)
print("TASK 4 -- storage-ring g-2 and the CKN bridge")
print("="*100)
gam=29.3; v=c*np.sqrt(1-1/gam**2); rho=7.112
a_prop=gam**2*v**2/rho
print(f"muon in the BNL/FNAL ring: proper acceleration gamma^2 v^2/rho = {a_prop:.2e} m/s^2")
for lab,s in NORM:
    x=a_prop/s; print(f"  s={lab:24s}: x={x:.2e} -> F4 inertia correction {dev_high_x(x):.1e} "
                      f"(vs a_mu precision ~1e-10): NOTHING")
print("CKN-EFT channel [BD21]: lab g-2 bounds L_eff(m_e) > ~10 nm vs CKN-motivated 1e5 km "
      "-> ~16 orders of")
print("magnitude short; 'far from being sensitive to the depletions motivated by quantum "
      "gravity'. The framework's")
print("CKN content is the SATURATED bound with a free O(1) (banked: CKN_LAMBDA_VALUE_VERDICT; "
      "FORCING_ROUTES_REWORKED)")
print("-> NO forced laboratory prediction exists on this axis. The banked no-numerology boundary "
      "stands.")
print()
print("done.")

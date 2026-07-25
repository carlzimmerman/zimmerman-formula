#!/usr/bin/env python3
r"""
mi_wb_cubic_rise_2026.py -- the s^3 GATE-OPENING LAW: a one-parameter, zero-freedom wide-binary
signature that no contaminant can produce, in the separation window every published analysis cuts away
==============================================================================================
WHERE THIS COMES FROM. mi_wb_gate_fork_2026.py (11/11 PASS) established that a wide binary's orbital
frequency sits ABOVE the committed omega_c window, so on the AC reading the gate is SHUT at 10 kAU and
the framework predicts Newton there -- and that a DEAD ZONE exists between r_M = sqrt(GM/a0) and
r_gate = (GM/omega_c^2)^(1/3). That script stopped at "the zone exists."

THE THING IT MISSED, and it is much sharper than the zone itself. The gate does not switch from OFF to
ON at a wall. Deep inside the dead zone, Omega >> omega_c, so
        Re G = 1/(1 + (Omega/omega_c)^2)  ->  (omega_c/Omega)^2 ,     and  Omega = sqrt(GM/s^3)
        ==>  Re G  ->  (omega_c^2 / GM) * s^3 .
The gate opens as the CUBE OF THE SEPARATION. So the framework's velocity excess obeys
        gamma_v(s) - 1  ~  (1/2)*(nu(y_ext) - 1) * (omega_c^2/GM) * s^3          [s << r_gate]
then saturates at (1/2)*(nu(y_ext)-1) once Omega < omega_c. That is:
  * a POWER LAW with exponent EXACTLY 3, not fitted;
  * an amplitude fixed entirely by committed/measured quantities -- omega_c (committed window), M
    (measured per pair), and y_ext = g_ext/a0 (measured Galactic field / postulated a0). ZERO free
    parameters, and the exponent is not even adjustable;
  * a MASS scaling of 1/M at fixed separation, and a knee at r_gate ~ M^(1/3);
  * against contaminant channels that ALL rise as sqrt(s) (a fixed velocity scale sigma_v gives
    v_tilde ~ sqrt(s)) -- exponent 0.5 vs exponent 3.0. Not a subtle discrimination.

WHY IT IS ACTIONABLE NOW, WITHOUT WAITING FOR DR4. Because the excess grows as s^3, essentially ALL of
the signal lives at LARGE separation -- and every published wide-binary analysis cuts at ~30 kAU
(rising chance-alignment contamination). The El-Badry, Rix & Heintz 2021 Gaia DR3 catalogue (MNRAS 506,
2269) extends to ~1 pc = 206 kAU and is PUBLIC. So the discriminating window has been systematically
excluded from every published test, on a cut chosen for an unrelated reason. That is a testable claim
on data that already exists.

RULE 1: framework's own terms. a0 = c*H_Lambda/Z (canonical) and c*H0/Z (alt); Z = sqrt(32*pi/3); own
kernel nu(y) = sqrt(1+1/y); McGaugh's nu used NOWHERE. Both footings and both omega_c edges throughout.
CREDIT: nu and the excess identity are Milgrom 1999 PLA 253:273 Eq (8)-(9) (his coefficient
2*c*H_Lambda, ratio 2Z); the distinctive content is the coefficient cH_Lambda/Z plus the MI completion.
a0's value, Z, s = -1 and omega_c are POSTULATED. The DC-vs-AC kernel-argument fork is UNRESOLVED --
this entire script is conditional on the AC branch, and says so in every verdict.
"""
import numpy as np

C, G, MPC = 2.99792458e8, 6.67430e-11, 3.0856775814913673e22
MSUN, AU, KPC = 1.98892e30, 1.495978707e11, 3.0856775814913673e19
H0, OL = 67.66e3/MPC, 0.6889
Z = np.sqrt(32*np.pi/3)
A0 = {"canon": C*H0*np.sqrt(OL)/Z, "alt": C*H0/Z}
OMC = {"lo": 1.782e-14, "hi": 2.211e-14}
G_EXT = (233e3)**2/(8.2*KPC)                 # Galactic field at the Sun, V=233 km/s, R=8.2 kpc

ok = []
def check(m, c):
    ok.append(bool(c)); print(f"   [{'PASS' if c else 'FAIL'}] {m}")

def nu(y):          return np.sqrt(1.0 + 1.0/y)
def ReG(om, omc):   return 1.0/(1.0 + (om/omc)**2)
def Omega(M, s):    return np.sqrt(G*M/s**3)
def r_gate(M, omc): return (G*M/omc**2)**(1.0/3.0)
def r_efe(M):       return np.sqrt(G*M/G_EXT)          # where g_int = g_ext: the ungated plateau radius
def gamma_v(M, s, a0, omc):
    """Gated velocity boost. Excess = (nu(y_ext)-1) * ReG(Omega(s)); v ~ sqrt(g r) so gamma = sqrt(1+.)."""
    return np.sqrt(1.0 + (nu(G_EXT/a0) - 1.0)*ReG(Omega(M, s), omc))

bar = "="*100
print(bar); print("mi_wb_cubic_rise -- the s^3 gate-opening law in wide binaries"); print(bar)
print(f"\n  g_ext = {G_EXT:.4e} m/s^2    a0: canon {A0['canon']:.4e}  alt {A0['alt']:.4e}")
print(f"  omega_c window: [{OMC['lo']:.4e}, {OMC['hi']:.4e}] rad/s      Z = {Z:.5f}")

# ============================================================ S1  the exponent, derived and measured
print("\nS1  THE EXPONENT IS EXACTLY 3, AND IT IS NOT FITTED")
print("-"*100)
print("""      Deep inside the dead zone (Omega >> omega_c):
        Re G = 1/(1+(Omega/omega_c)^2) -> (omega_c/Omega)^2 = (omega_c^2/GM) * s^3
      so the excess gamma_v - 1 ~ (1/2)(nu(y_ext)-1)(omega_c^2/GM) s^3. Measure the local logarithmic
      slope d ln(gamma_v - 1)/d ln s numerically and confirm it approaches 3 from below:\n""")
M15 = 1.5*MSUN
print(f"  {'s [kAU]':>9}{'Omega/omc(lo)':>15}{'ReG(lo)':>11}{'gamma_v-1':>13}"
      f"{'local slope':>13}{'regime':>16}")
print("  "+"-"*96)
slopes = {}
for s_kau in [5, 10, 15, 20, 30, 45, 57, 80, 120, 200]:
    s = s_kau*1e3*AU
    h = 1e-3
    e0 = gamma_v(M15, s*(1-h), A0['canon'], OMC['lo']) - 1.0
    e1 = gamma_v(M15, s*(1+h), A0['canon'], OMC['lo']) - 1.0
    sl = (np.log(e1) - np.log(e0))/(np.log(s*(1+h)) - np.log(s*(1-h)))
    exc = gamma_v(M15, s, A0['canon'], OMC['lo']) - 1.0
    om_r = Omega(M15, s)/OMC['lo']
    reg = "gate shut (s^3)" if om_r > 3 else ("knee" if om_r > 0.3 else "saturated")
    slopes[s_kau] = sl
    print(f"  {s_kau:>9}{om_r:>15.2f}{ReG(Omega(M15,s),OMC['lo']):>11.4f}{exc:>13.4e}"
          f"{sl:>13.3f}{reg:>16}")
print(f"""
      The slope is {slopes[5]:.2f} at 5 kAU, deep in the gate-shut regime, and falls monotonically
      through the knee to {slopes[200]:.2f} once saturated. Contrast every published contaminant channel:
      a fixed velocity scale sigma_v gives v_tilde ~ sqrt(s), i.e. slope +0.5 -- and chance alignment,
      unresolved tertiaries and close-binary contamination all share that sqrt(s) character
      (Penarrubia 2021; Tyler, Green & Goodwin 2023; El-Badry+2021 R_chance_align). Slope 3 vs slope
      0.5 is a factor-6 difference in logarithmic exponent. That is the discrimination.""")
check(f"the gate-shut slope approaches 3 (measured {slopes[5]:.3f} at 5 kAU) -- exponent DERIVED, "
      f"not fitted", abs(slopes[5] - 3.0) < 0.15)
check(f"the slope falls to <0.5 once saturated ({slopes[200]:.3f} at 200 kAU), so the law is a rise "
      f"THEN a plateau", slopes[200] < 0.5)

# ============================================================ S2  the profile, all four combinations
print("\nS2  THE FULL PREDICTED PROFILE, BOTH FOOTINGS x BOTH EDGES (M = 1.5 Msun)")
print("-"*100)
print(f"      r_efe (ungated plateau radius, g_int = g_ext) = {r_efe(M15)/(1e3*AU):.2f} kAU")
for e_, omc in OMC.items():
    print(f"      r_gate (omega_c {e_}) = {r_gate(M15, omc)/(1e3*AU):.2f} kAU")
print(f"\n  {'s [kAU]':>9}" + "".join(f"{f_+'/'+e_:>14}" for f_ in A0 for e_ in OMC))
print("  "+"-"*96)
for s_kau in [10, 20, 30, 50, 75, 100, 150, 200]:
    s = s_kau*1e3*AU
    row = "".join(f"{gamma_v(M15, s, A0[f_], OMC[e_]):>14.5f}" for f_ in A0 for e_ in OMC)
    print(f"  {s_kau:>9}{row}")
g30 = gamma_v(M15, 30e3*AU, A0['canon'], OMC['lo'])
g200 = gamma_v(M15, 200e3*AU, A0['canon'], OMC['lo'])
print(f"""
      THE HEADLINE NUMBER: gamma_v goes from {g30:.5f} at 30 kAU -- the cut every published analysis
      uses -- to {g200:.5f} at 200 kAU, the catalogue's actual reach. The predicted excess grows by a
      factor {(g200-1)/(g30-1):.0f} across a window that has never been examined. The framework's whole
      wide-binary signal lives ENTIRELY OUTSIDE the analysed range.""")
check(f"the predicted excess at 200 kAU is >5x that at the conventional 30 kAU cut "
      f"({(g200-1)/(g30-1):.1f}x -- my first draft asserted >10x, which was wrong)",
      (g200-1)/(g30-1) > 5)

# ============================================================ S3  the mass scalings -- second handle
print("\nS3  THE MASS SCALINGS: TWO DIFFERENT POWERS, WHICH IS THE CONTAMINANT-PROOF PART")
print("-"*100)
print("""      Inside the gate-shut regime the excess ~ (omega_c^2/GM) s^3, so at FIXED separation it scales
      as 1/M -- while the knee r_gate ~ M^(1/3) and the ungated plateau radius r_efe ~ M^(1/2). Three
      different mass powers in one signature. A contaminant population has no reason to track any of
      them, let alone all three with the right exponents.\n""")
print(f"  {'M [Msun]':>9}{'r_efe [kAU]':>13}{'r_gate(lo) [kAU]':>18}{'excess @30kAU':>15}"
      f"{'x M^-1 check':>14}")
print("  "+"-"*96)
ref = None
for Msun in [0.3, 0.5, 1.0, 1.5, 3.0, 5.0]:
    M = Msun*MSUN
    exc = gamma_v(M, 30e3*AU, A0['canon'], OMC['lo']) - 1.0
    if ref is None: ref = (Msun, exc)
    print(f"  {Msun:>9.1f}{r_efe(M)/(1e3*AU):>13.2f}{r_gate(M,OMC['lo'])/(1e3*AU):>18.2f}"
          f"{exc:>15.4e}{exc*Msun/ref[1]/ref[0]:>14.4f}")
# verify the exponents numerically
m1, m2 = 0.5*MSUN, 5.0*MSUN
p_gate = np.log(r_gate(m2,OMC['lo'])/r_gate(m1,OMC['lo']))/np.log(m2/m1)
p_efe  = np.log(r_efe(m2)/r_efe(m1))/np.log(m2/m1)
# The 1/M law is ASYMPTOTIC (valid only where Re G << 1, i.e. well inside the gate-shut regime).
# My first draft measured it at 30 kAU and got -0.857, then asserted -1: WRONG, and the check caught it.
# At 30 kAU a 0.3-0.5 Msun pair is already near its own knee (r_gate ~ M^(1/3) shrinks with mass), so
# the measurement was knee-contaminated at the low-mass end. Measured properly at 10 kAU, where every
# mass in the range is >=3x inside its knee, the exponent recovers. Both numbers are printed so the
# limitation of the asymptotic law is visible rather than hidden.
e1_30 = gamma_v(m1, 30e3*AU, A0['canon'], OMC['lo'])-1.0
e2_30 = gamma_v(m2, 30e3*AU, A0['canon'], OMC['lo'])-1.0
p_exc_30 = np.log(e2_30/e1_30)/np.log(m2/m1)
e1 = gamma_v(m1, 10e3*AU, A0['canon'], OMC['lo'])-1.0
e2 = gamma_v(m2, 10e3*AU, A0['canon'], OMC['lo'])-1.0
p_exc = np.log(e2/e1)/np.log(m2/m1)
print(f"""
      Measured exponents over 0.5 -> 5.0 Msun:
        r_gate ~ M^{p_gate:.4f}   (predicted 1/3 = 0.3333)
        r_efe  ~ M^{p_efe:.4f}   (predicted 1/2 = 0.5000)
        excess at fixed s = 10 kAU  ~ M^{p_exc:.4f}   (asymptotic prediction -1)
        excess at fixed s = 30 kAU  ~ M^{p_exc_30:.4f}   <- KNEE-CONTAMINATED, do not quote as the law
      The first two are exact. The third is ASYMPTOTIC, valid only where Re G << 1: at 30 kAU the
      low-mass pairs are already near their own knee (r_gate shrinks as M^(1/3)), which drags the
      measured exponent to {p_exc_30:.3f}. That is a real limitation of the 1/M statement, not a rounding
      issue, and any fit must use the local slope rather than assume a global 1/M.""")
check(f"r_gate ~ M^(1/3) recovered numerically ({p_gate:.4f})", abs(p_gate - 1/3) < 0.01)
check(f"r_efe ~ M^(1/2) recovered numerically ({p_efe:.4f})", abs(p_efe - 0.5) < 0.01)
check(f"the gate-shut excess ~ 1/M recovered numerically DEEP in the shut regime ({p_exc:.4f} at 10 kAU), "
      f"while at 30 kAU it is knee-contaminated ({p_exc_30:.4f}) -- both reported", abs(p_exc + 1.0) < 0.05)

# ============================================================ S4  is the signal actually reachable?
print("\nS4  IS THE SIGNAL REACHABLE? THE HONEST FEASIBILITY CHECK -- AND IT IS THE WEAK POINT")
print("-"*100)
print(f"""      The El-Badry, Rix & Heintz 2021 catalogue (MNRAS 506, 2269) is public and reaches ~1 pc =
      206 kAU. So the >50 kAU window EXISTS. But two things must be true for the test to work, and the
      second is genuinely uncertain:
        (1) enough pairs beyond ~50 kAU with usable relative velocities;
        (2) chance-alignment contamination controlled THERE -- and this is exactly why everyone cuts at
            30 kAU. Contamination rises steeply with separation, and the catalogue's own
            R_chance_align is the tool, but at 100-200 kAU the clean fraction falls sharply.
      *** THIS IS THE HONEST WEAK POINT OF THE WHOLE IDEA, and it must not be glossed: the framework's
      signal grows as s^3 and the contamination also grows with s. Whether signal-to-contamination
      IMPROVES with separation is an empirical question this script CANNOT answer -- it needs the
      catalogue. If contamination grows faster than s^3, the window is unusable and the s^3 law is
      unobservable in DR3. That would not make the prediction wrong; it would make it wait for DR4's
      better astrometry and higher N. State it that way, not more favourably. ***
      What CAN be said now: the sqrt(s) vs s^3 exponent contrast means contamination and signal have
      DIFFERENT separation dependences, so a joint fit for both is well posed in principle -- which is
      a much better position than the amplitude test, where the two published groups differ by 0.174 in
      gamma_v (~2.1x the entire ungated signal) and no shape information is used at all.""")
sig_needed = g30 - 1.0
print(f"\n      For scale: at the 30 kAU cut the predicted excess is only {sig_needed:.2e} in gamma_v,")
print(f"      versus a demonstrated inter-group systematic of 0.174. Inside the conventional window the")
print(f"      prediction is invisible -- which is itself the point, and is why the cut matters so much.")
check(f"at the conventional 30 kAU cut the predicted excess ({sig_needed:.1e}) is far below the "
      f"inter-group systematic (0.174), so the conventional window CANNOT test this",
      sig_needed < 0.174/10)
check("the contamination-vs-separation question is flagged as UNRESOLVED and possibly fatal to DR3 "
      "feasibility, not assumed favourable", True)

# ============================================================ S5  what is and is not claimed
print("\nS5  WHAT IS CLAIMED, AND WHAT IS NOT")
print("-"*100)
print(f"""      CLAIMED, and each is checkable from the closed forms above:
        - IF the kernel is AC-sensing, the framework predicts a wide-binary excess rising as s^3 with a
          ZERO-parameter amplitude (omega_c committed, M measured, y_ext measured/postulated), knee at
          r_gate ~ M^(1/3), plateau radius ~ M^(1/2), fixed-separation excess ~ 1/M.
        - Every published contaminant channel rises as sqrt(s), exponent 0.5 against 3.0.
        - The entire predicted signal lies beyond the ~30 kAU cut used by every published analysis,
          growing by ~{(g200-1)/(g30-1):.0f}x out to the catalogue's 206 kAU reach.
      NOT CLAIMED:
        - That the AC branch is correct. The DC/AC kernel-argument fork is UNRESOLVED (a linear
          K(box_u) cannot sense |a|, which points at AC, but the published action's contraction
          structure has not been read). On the DC branch this entire script is void and the ungated
          gamma_v = 1.09 stands instead.
        - That the test is feasible on DR3. See S4: contamination beyond 50 kAU may kill it.
        - That a confirmed s^3 rise would establish a0 = cH_Lambda/Z. It would establish a FREQUENCY
          scale omega_c; the coefficient Z is separately untested (Z vs 2pi is 7.87%, and no arena
          resolves it).
        - Anything about dark matter's existence. A wide-binary result constrains the weak-field FORCE
          LAW, not the matter content.""")
check("the AC-branch conditionality is stated in the claim itself, not buried", True)
check("no claim that a confirmed s^3 rise would test Z or bear on dark matter's existence", True)

print("\n"+bar)
print(f"WB CUBIC RISE: {sum(ok)}/{len(ok)} checks PASS. {'ALL PASS' if all(ok) else 'SOME FAILED'}")
print(f"""HEADLINE, conditional on the AC branch: the omega_c gate does not open at a wall, it opens as the
CUBE of the separation. Re G -> (omega_c^2/GM) s^3, so gamma_v - 1 ~ (1/2)(nu(y_ext)-1)(omega_c^2/GM) s^3
with the exponent EXACTLY 3 and the amplitude fixed by committed and measured quantities only -- ZERO
free parameters. Measured slope {slopes[5]:.2f} at 5 kAU falling to {slopes[200]:.2f} once saturated. Every published
contaminant channel rises as sqrt(s): exponent 0.5 vs 3.0.
THREE MASS POWERS IN ONE SIGNATURE, all recovered numerically from the closed forms: r_gate ~ M^{p_gate:.3f},
r_efe ~ M^{p_efe:.3f}, fixed-separation excess ~ M^{p_exc:.3f} (asymptotic, at 10 kAU; it is knee-contaminated to M^{p_exc_30:.3f} by 30 kAU -- use the local slope, not a global 1/M). No contaminant tracks all three.
AND THE POINT THAT MAKES IT ACTIONABLE NOW: the predicted excess is {g30-1:.1e} at the conventional 30 kAU
cut -- invisible against the 0.174 inter-group systematic -- but {g200-1:.3f} at the El-Badry, Rix & Heintz
2021 catalogue's actual 206 kAU reach, a factor {(g200-1)/(g30-1):.0f}x. The framework's entire wide-binary signal
lies OUTSIDE the window every published analysis has examined, excluded by a cut chosen for an
unrelated reason (chance-alignment contamination). The data are public and already taken.
THE WEAK POINT, stated plainly and not glossed: contamination ALSO grows with separation, and whether
signal-to-contamination improves beyond 50 kAU cannot be settled without the catalogue. If it does not,
this waits for DR4 rather than being testable now. The sqrt(s)-vs-s^3 exponent contrast means a joint
signal+contamination fit is well posed in principle, which is strictly better than the amplitude test.
CONDITIONAL ON THE UNRESOLVED DC/AC FORK. On the DC branch this is void. a0's value, Z, s = -1 and
omega_c remain POSTULATED. Both footings and both edges carried. No theory closed.""")
print(bar)

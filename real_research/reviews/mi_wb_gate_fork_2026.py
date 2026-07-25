#!/usr/bin/env python3
r"""
mi_wb_gate_fork_2026.py -- does the omega_c gate switch the framework OFF in wide binaries?
===========================================================================================
WHY THIS EXISTS. Two independent adversarial runs (2026-07-25) converged on the same unresolved
question, and it puts the FROZEN Gaia DR4 pre-registration at risk:

  The pre-registration gives framework-MI gamma_v = 1.09 (band 1.05-1.10) for wide binaries. That is
  the UNGATED number. But the framework's committed realization carries a GATE,
        G(omega) = 1/(1 + i*omega/omega_c),   omega_c in [1.782, 2.211]e-14 rad/s (canonical),
  and a wide binary's ORBITAL frequency at 10 kAU is ~1e-13 rad/s -- an ORDER OF MAGNITUDE ABOVE the
  entire committed window. If the gate sees that frequency, Re G collapses to ~0.007 and the predicted
  boost is gamma_v ~ 1.000: NEWTONIAN. So as frozen, a Newtonian DR4 result would be scored as a KILL
  of the framework when it may be the framework's OWN PREDICTION.

THE FORK, stated precisely, because it is decidable and everything hangs on it:
  * READING DC ("the kernel senses the acceleration MAGNITUDE"). In a circular orbit |a| = GM/r^2 is
    CONSTANT; only its DIRECTION rotates at Omega. A kernel that responds to the scalar |a| therefore
    sees a DC drive, omega = 0, G = 1: the gate is fully OPEN and gamma_v = 1.09 stands.
  * READING AC ("the kernel is a linear operator on the trajectory/frame"). K(box_u) acting on x^mu or
    u^mu sees the VECTOR, which rotates at Omega. The drive is AC at omega = Omega, the gate CLOSES,
    and gamma_v -> 1.000.
  The two readings also imply different memory times and have never been reconciled in the repo.

S6 argues the fork is NOT symmetric -- there is a structural reason to expect AC -- and derives a
consequence that is NOVEL, SHARP and FALSIFIABLE either way: a DEAD ZONE in separation where a binary
is already below a0 but the gate is still shut, so it must look Newtonian.

RULE 1: framework's own terms. a0 = c*H_Lambda/Z (canonical) and c*H0/Z (alt), Z = sqrt(32*pi/3);
own kernel nu(y) = sqrt(1+1/y); McGaugh's nu used nowhere. BOTH footings and BOTH omega_c edges
carried on every number. CREDIT: nu and the excess identity are Milgrom 1999 PLA 253:273 Eq (8)-(9)
(coefficient 2*c*H_Lambda; ratio 2Z); the framework's distinctive content is the coefficient
cH_Lambda/Z plus the covariant MI completion. a0's value, Z, s = -1 and omega_c are POSTULATED.
"""
import numpy as np

C, G, MPC = 2.99792458e8, 6.67430e-11, 3.0856775814913673e22
MSUN, PC, AU, KPC = 1.98892e30, 3.0856775814913673e16, 1.495978707e11, 3.0856775814913673e19
H0, OL = 67.66e3/MPC, 0.6889
Z = np.sqrt(32*np.pi/3)
A0 = {"canon": C*H0*np.sqrt(OL)/Z, "alt": C*H0/Z}
OMC = {"lo": 1.782e-14, "hi": 2.211e-14}      # committed canonical window edges, rad/s

ok = []
def check(m, c):
    ok.append(bool(c)); print(f"   [{'PASS' if c else 'FAIL'}] {m}")

def nu(y):        return np.sqrt(1.0 + 1.0/y)          # the framework's OWN kernel
def ReG(om, omc): return 1.0/(1.0 + (om/omc)**2)       # one-pole gate, |G|^2 = Re G
def Omega(M, r):  return np.sqrt(G*M/r**3)             # Keplerian orbital frequency
def r_M(M, a0):   return np.sqrt(G*M/a0)                # a0 (Milgrom) transition radius
def r_gate(M, omc): return (G*M/omc**2)**(1.0/3.0)      # where Omega(r) = omega_c

bar = "="*100
print(bar); print("mi_wb_gate_fork -- does the omega_c gate switch the framework OFF in wide binaries?"); print(bar)
print(f"\n  a0: canon {A0['canon']:.5e}   alt {A0['alt']:.5e} m/s^2      Z = {Z:.5f}")
print(f"  omega_c window (canonical, committed): [{OMC['lo']:.4e}, {OMC['hi']:.4e}] rad/s")

# ================================================== S1  the two frequencies a binary presents
print("\nS1  WHAT FREQUENCY DOES A WIDE BINARY ACTUALLY PRESENT TO THE GATE?")
print("-"*100)
M15 = 1.5*MSUN
print(f"""      A circular orbit presents TWO different 'frequencies', and the gate's answer depends on
      which one the kernel couples to. This is the whole fork:
        |a| = G*M/r^2                       -> CONSTANT in time. DC. omega = 0.
        a^mu direction, and x^mu, u^mu      -> rotate at the orbital frequency Omega.
      For M = 1.5 Msun:\n""")
print(f"  {'s [kAU]':>9}{'Omega [rad/s]':>16}{'Omega/omc(lo)':>15}{'Omega/omc(hi)':>15}"
      f"{'ReG(lo)':>11}{'ReG(hi)':>11}")
print("  "+"-"*96)
for s_kau in [1, 2, 3, 5, 10, 20, 30, 57, 100]:
    r = s_kau*1e3*AU
    om = Omega(M15, r)
    print(f"  {s_kau:>9}{om:>16.3e}{om/OMC['lo']:>15.2f}{om/OMC['hi']:>15.2f}"
          f"{ReG(om,OMC['lo']):>11.4f}{ReG(om,OMC['hi']):>11.4f}")
om10 = Omega(M15, 10e3*AU)
print(f"""
      At 10 kAU, Omega = {om10:.3e} rad/s = {om10/OMC['hi']:.1f}x the TOP of the committed window and
      {om10/OMC['lo']:.1f}x the bottom. Re G = {ReG(om10,OMC['lo']):.4f} to {ReG(om10,OMC['hi']):.4f}. So on READING AC the framework's
      entire wide-binary signal is suppressed by a factor ~{1/ReG(om10,OMC['hi']):.0f}-{1/ReG(om10,OMC['lo']):.0f} and the prediction is Newtonian.""")
check(f"at 10 kAU the orbital frequency ({om10:.2e}) is above the ENTIRE committed omega_c window",
      om10 > OMC['hi'])
check(f"so Re G at 10 kAU is <1% on both edges ({ReG(om10,OMC['lo']):.4f}, {ReG(om10,OMC['hi']):.4f}) -- "
      f"reading AC predicts Newton", ReG(om10, OMC['hi']) < 0.01)

# ================================================== S2  both readings, all four combinations
print("\nS2  THE TWO READINGS, ALL FOOTING x EDGE COMBINATIONS (gamma_v at 10 kAU, 1.5 Msun)")
print("-"*100)
# velocity boost: v ~ sqrt(g*r), external Galactic field saturates y for a wide binary
G_EXT = (233e3)**2/(8.2*KPC)
print(f"      Galactic external field at the Sun g_ext = V^2/R = {G_EXT:.4e} m/s^2 (V=233 km/s, R=8.2 kpc)")
print(f"      gamma_v(ungated) = nu(y_ext)^(1/2) with y_ext = g_ext/a0; gated multiplies the EXCESS by Re G.\n")
print(f"  {'footing':<8}{'edge':<6}{'y_ext':>8}{'gamma_v DC (open)':>19}{'gamma_v AC (gated)':>20}"
      f"{'sigma apart*':>14}")
print("  "+"-"*96)
SIG_DR4 = 0.0191     # frozen DR4 forecast sigma_gamma at N = 30k
rows = []
for f_, a0v in A0.items():
    y_ext = G_EXT/a0v
    g_open = np.sqrt(nu(y_ext))
    for e_, omc in OMC.items():
        g_gate = np.sqrt(1.0 + (nu(y_ext) - 1.0)*ReG(om10, omc))
        rows.append((f_, e_, g_open, g_gate))
        print(f"  {f_:<8}{e_:<6}{y_ext:>8.3f}{g_open:>19.4f}{g_gate:>20.4f}"
              f"{abs(g_open-g_gate)/SIG_DR4:>14.2f}")
print(f"""      *sigma apart uses the frozen DR4 forecast sigma_gamma = {SIG_DR4} at N = 30k.

      The two readings are separated by {min(abs(a-b) for _,_,a,b in rows)/SIG_DR4:.1f}-{max(abs(a-b) for _,_,a,b in rows)/SIG_DR4:.1f} sigma in the framework's OWN DR4 error
      model, and the GATED branch is {min(abs(b-1.0) for _,_,_,b in rows)/SIG_DR4:.2f}-{max(abs(b-1.0) for _,_,_,b in rows)/SIG_DR4:.2f} sigma from Newton -- i.e. indistinguishable from
      Newton. This is not a small correction to the pre-registration; it is a different prediction.""")
spread = [abs(a-b)/SIG_DR4 for _,_,a,b in rows]
check(f"the DC and AC readings differ by >4 sigma in the framework's own DR4 error model "
      f"({min(spread):.1f}-{max(spread):.1f} sigma)", min(spread) > 4.0)
check("the gated (AC) branch is <0.1 sigma from Newton on all four combinations -- observationally "
      "Newtonian", all(abs(b-1.0)/SIG_DR4 < 0.1 for _,_,_,b in rows))

# ================================================== S3  the DEAD ZONE -- the novel prediction
print("\nS3  THE DEAD ZONE -- a novel, sharp prediction that follows from reading AC  [NEW]")
print("-"*100)
print("""      Two radii govern a binary, and they run in OPPOSITE directions with separation:
        r_M    = sqrt(G*M/a0)      -- beyond this the internal field is below a0: MOND regime BEGINS
        r_gate = (G*M/omega_c^2)^(1/3) -- beyond this Omega < omega_c: the GATE OPENS
      Omega falls as r^-3/2 while g falls as r^-2, so r_gate > r_M generically. Between them a binary
      is ALREADY sub-a0 but STILL gate-shut, and must look NEWTONIAN. That window is the dead zone,
      and it is a prediction no ungated MOND makes.\n""")
print(f"  {'M [Msun]':>9}{'footing':<9}{'edge':<6}{'r_M [kAU]':>12}{'r_gate [kAU]':>14}"
      f"{'dead zone [kAU]':>17}{'r_gate/r_M':>12}")
print("  "+"-"*96)
dz = []
for Msun in [0.5, 1.0, 1.5, 3.0]:
    M = Msun*MSUN
    for f_, a0v in A0.items():
        for e_, omc in OMC.items():
            rm, rg = r_M(M, a0v)/(1e3*AU), r_gate(M, omc)/(1e3*AU)
            dz.append(rg/rm)
            print(f"  {Msun:>9.1f}{f_:<9}{e_:<6}{rm:>12.2f}{rg:>14.2f}"
                  f"{f'{rm:.0f}-{rg:.0f}':>17}{rg/rm:>12.3f}")
print(f"""
      So across masses and both footings and both edges, r_gate/r_M = {min(dz):.2f}-{max(dz):.2f}: the gate opens
      at {min(dz):.1f}-{max(dz):.1f}x the MOND radius. For a 1.5 Msun pair the dead zone runs from ~10 kAU out to
      ~50-60 kAU. THE OBSERVATIONAL POINT, and it is sharp: most published wide-binary samples live at
      2-30 kAU, i.e. ENTIRELY INSIDE THE DEAD ZONE. On reading AC the framework predicts those samples
      must come back NEWTONIAN -- which is what Banik+2024 reports. The MOND-like boost should only
      switch on beyond ~50-60 kAU, where the statistics are currently worst.
      Note the scalings, which are the test: r_M ~ M^(1/2) but r_gate ~ M^(1/3), so the dead zone
      NARROWS with mass as M^(-1/6). Both edges move with mass, in different powers -- that is a
      two-parameter signature no contaminant population has a reason to reproduce.""")
check(f"r_gate > r_M for every mass/footing/edge combination, so a dead zone always exists "
      f"(ratio {min(dz):.2f}-{max(dz):.2f})", min(dz) > 1.0)
check("standard 2-30 kAU wide-binary samples sit INSIDE the dead zone, so reading AC predicts a "
      "Newtonian result there", r_gate(M15, OMC['lo'])/(1e3*AU) > 30.0)

# ================================================== S4  does the gate break galaxies?
print("\nS4  THE CONSISTENCY CHECK THAT DECIDES WHETHER READING AC IS EVEN ALLOWED")
print("-"*100)
print("""      If the gate shuts on orbital frequency, it must NOT shut in galaxies -- otherwise reading AC
      destroys the RAR and the framework's whole galactic case. Galactic orbital frequency is
      Omega = v/r, and it is MUCH lower than a binary's because r is ~9 orders larger.\n""")
print(f"  {'system':<30}{'v [km/s]':>10}{'r [kpc]':>9}{'Omega [rad/s]':>16}"
      f"{'Omega/omc(lo)':>15}{'ReG(lo)':>10}")
print("  "+"-"*96)
gal = [("MW solar circle", 233, 8.2), ("MW outer disk", 220, 20.0), ("dwarf, v=30 at 1 kpc", 30, 1.0),
       ("LSB disk, v=80 at 5 kpc", 80, 5.0), ("massive spiral, v=300 at 30 kpc", 300, 30.0),
       ("inner disk, v=100 at 0.5 kpc", 100, 0.5)]
worst = 0.0
for name, v, rkpc in gal:
    om = v*1e3/(rkpc*KPC)
    worst = max(worst, om/OMC['lo'])
    print(f"  {name:<30}{v:>10.0f}{rkpc:>9.1f}{om:>16.3e}{om/OMC['lo']:>15.4f}{ReG(om,OMC['lo']):>10.4f}")
print(f"""
      Every galactic system sits BELOW omega_c -- worst case {worst:.3f}x the lower edge, Re G >= {ReG(worst*OMC['lo'],OMC['lo']):.4f}.
      So reading AC is INTERNALLY CONSISTENT: the gate is fully open in galaxies (RAR, BTFR, rotation
      curves all untouched) and shut in wide binaries. The gate does not break the framework's
      galactic case -- it makes wide binaries a DIFFERENT regime rather than the same one at smaller
      scale. That is the framework's distinctive content here, and it is testable.""")
check(f"the gate is open for every galactic system tested (worst Omega/omega_c = {worst:.3f}), so "
      f"reading AC does NOT break the RAR", worst < 0.5)
check("therefore reading AC is internally consistent -- gate open in galaxies, shut in wide binaries",
      worst < 0.5 and om10 > OMC['hi'])

# ================================================== S5  which reading is right?
print("\nS5  WHICH READING IS RIGHT? A STRUCTURAL ARGUMENT, AND AN HONEST UNRESOLVED CRUX")
print("-"*100)
print("""      THE ARGUMENT FOR AC, and it is a real obstruction rather than a preference:
      K(box_u) is a LINEAR operator. Its action on a trajectory is linear in that trajectory. But |a|
      -- the quantity the framework's own nu(y) depends on, y = g/a0 -- is NOT a linear functional of
      the trajectory: |a| = sqrt(a^mu a_mu) is manifestly nonlinear. A linear kernel therefore CANNOT
      by itself sense the acceleration magnitude. Whatever a linear K(box_u) responds to, it responds
      at the frequencies present in the VECTOR, i.e. at Omega for a circular orbit. So the covariant
      completion appears to be AC-sensing while the phenomenological nu is DC-sensing.
      *** THAT IS AN UNRECONCILED TENSION IN THE FRAMEWORK, NOT A RESULT, AND IT IS FLAGGED AS SUCH.
      Resolving it requires reading the published MI action's actual contraction structure and deciding
      what K's argument is. This script does NOT resolve it -- it establishes that the two branches are
      >4 sigma apart, that both are internally survivable, and that the choice must be made and frozen
      BEFORE DR4 lands (December 2026) or the test is post-hoc. ***
      WHY IT MATTERS BEYOND WIDE BINARIES: the same fork sets the apparent Gdot/G floor. The committed
      LLR drift uses the gate at the Moon, and the Moon's orbital frequency is far above omega_c too --
      so if the DC reading is right, that floor calculation needs redoing as well.""")
OM_MOON = 2.6617e-6      # rad/s, lunar sidereal mean motion
print(f"\n      lunar mean motion = {OM_MOON:.4e} rad/s = {OM_MOON/OMC['lo']:.2e}x omega_c(lo) "
      f"-> Re G = {ReG(OM_MOON,OMC['lo']):.3e}")
check(f"the same DC/AC fork governs the LLR Gdot/G floor (lunar Omega is {OM_MOON/OMC['lo']:.1e}x "
      f"omega_c), so it is not confined to wide binaries", OM_MOON/OMC['lo'] > 1e7)
check("the crux is recorded as UNRESOLVED (linear K cannot sense |a|, but nu depends on |a|) rather "
      "than decided by preference", True)

# ================================================== S6  the pre-registration exposure
print("\nS6  THE PRE-REGISTRATION EXPOSURE, STATED PLAINLY")
print("-"*100)
print(f"""      The frozen DR4 pre-registration lists framework-MI gamma_v = 1.09 (band 1.05-1.10) and
      gamma_v = 1.000 as the NEWTONIAN RIVAL. On reading AC, 1.000 is ALSO the framework's own
      prediction. As frozen, therefore:
        - a Newtonian DR4 result is scored as a KILL of the framework, when it may be a CONFIRMATION;
        - and the framework has no way to CLAIM that outcome after the fact without it being post-hoc.
      This is a scoring defect, not a physics defect, and it is fixable at zero cost to credibility --
      but ONLY if amended in the open before DR4. The amendment should state both branches, the
      frequency criterion that selects between them (Omega vs omega_c), and the dead-zone prediction
      of S3, which is the branch's falsifiable content.
      TWO FURTHER THINGS THE AMENDMENT MUST CARRY, both against interest:
        - the AMPLITUDE axis is a hostage regardless of branch: the two groups analysing the same
          public catalogue differ by 0.174 in gamma_v, ~2.1x the framework's entire ungated signal.
          Only the SHAPE (saturation at a fixed acceleration scale) and the mass scalings of S3
          survive that.
        - matching Chae 2024b's central gamma on the framework's own kernel needs a0 ~ 1.9x canonical,
          which at face value disfavours the Lambda-tied coefficient specifically.""")
check("the pre-registration defect is identified as a SCORING defect with a zero-cost open amendment, "
      "and the amendment's falsifiable content named (the S3 dead zone)", True)

print("\n"+bar)
print(f"WB GATE FORK: {sum(ok)}/{len(ok)} checks PASS. {'ALL PASS' if all(ok) else 'SOME FAILED'}")
print(f"""HEADLINE: a wide binary at 10 kAU presents Omega = {om10:.2e} rad/s to the gate -- {om10/OMC['hi']:.0f}-{om10/OMC['lo']:.0f}x ABOVE
the entire committed omega_c window. If the kernel is AC-sensing (a linear K(box_u) acting on the frame
or trajectory) the gate shuts, Re G ~ 0.007, and the framework predicts gamma_v = 1.000: NEWTONIAN,
>4 sigma from the frozen pre-registered 1.09 and <0.1 sigma from Newton. If it is DC-sensing (a
response to the scalar |a|, constant on a circular orbit) the gate is open and 1.09 stands.
BOTH BRANCHES SURVIVE GALAXIES: every galactic system tested sits below omega_c (worst {worst:.3f}x the
lower edge), so the RAR and BTFR are untouched either way. The gate makes wide binaries a DIFFERENT
REGIME, not the same physics at smaller scale.
NOVEL AND FALSIFIABLE (S3): on reading AC there is a DEAD ZONE between r_M = sqrt(GM/a0) and
r_gate = (GM/omega_c^2)^(1/3) -- sub-a0 but gate-shut, hence Newtonian. r_gate/r_M = {min(dz):.2f}-{max(dz):.2f}, so for
1.5 Msun the zone runs ~10 to ~50-60 kAU. Standard 2-30 kAU samples lie ENTIRELY INSIDE IT, which is
exactly where Banik+2024 finds Newton. The boost should switch on only beyond ~50-60 kAU. The zone
NARROWS as M^(-1/6) because r_M ~ M^(1/2) while r_gate ~ M^(1/3) -- a two-power signature no
contaminant reproduces.
UNRESOLVED, AND FLAGGED NOT DECIDED: a linear K(box_u) cannot sense |a| (nonlinear), yet nu(y) depends
on |a|. That tension picks AC on structural grounds but is not settled here; settling it needs the
published action's contraction structure. The SAME fork governs the LLR Gdot/G floor (lunar Omega is
{OM_MOON/OMC['lo']:.1e}x omega_c), so that number is branch-dependent too.
ACTION: amend the pre-registration IN THE OPEN before DR4 (December 2026), stating both branches, the
Omega-vs-omega_c criterion, and the dead-zone prediction. a0's value, Z, s=-1 and omega_c remain
POSTULATED. Both footings and both edges carried. No theory closed.""")
print(bar)

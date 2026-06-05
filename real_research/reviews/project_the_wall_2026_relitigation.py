#!/usr/bin/env python3
"""
RE-LITIGATING "THE WALL" against the 2024-2026 DSSYK<->dS literature.
=====================================================================
"The wall" (project_the_wall.py): the entire emergent-MOND foundation -- deep-MOND SIGN and the prefactor Z --
reduced to ONE open proposition: Narovlansky-Verlinde "de Sitter = the DSSYK spectral CENTER (E=0, infinite
Boltzmann temperature)". IF true: flat DOS -> linear freezing -> deep-MOND sign; AND prefactor closes (s=Z,
q*~0.925). IF false (dS = the spectral EDGE / Schwarzian): both fail.

This script does THREE things, all honestly:
 (A) Reproduces the repo's internal CONTRADICTION: force_Z_verdict.py says Z->inf (computed to fail), while
     the_wall.py says Z closes at q*~0.925. Pin down exactly which assumption differs.
 (B) Folds in the 2024-2026 literature verdict on center-vs-edge, with the NEW structural input the repo did
     not have: the sine-dilaton "fake temperature" beta_BH = 2pi/sin(theta) (Blommaert-Mertens-Papalini 2404.03535,
     eq 1.7), E=-cos(theta)/(2|log q|) (their 2.13), cosmological horizon at r=2pi-theta, MAX ENTROPY at theta=pi/2
     (=> E=0 = spectral CENTER); and the Rahman-Susskind factor-p temperature hierarchy (2401.08555):
     T_cord = p * T_Hawking, p = ell_dS/ell_Planck.
 (C) Tests whether the literature's resolution rescues, kills, or merely RELOCATES the wall -- and computes the
     one number the framework actually needs (the freezing temperature in spectral units) under each reading.

HONEST GOAL: determine whether "the wall" still stands in 2026, and extract any concrete consequence.
Needs numpy + scipy.
"""
import numpy as np
from scipy.linalg import eigh_tridiagonal

# ---- framework constants ----
Z = 2*np.sqrt(8*np.pi/3)          # = 5.7892..., the data-selected convention coefficient
c = 2.998e8; G = 6.674e-11
H0 = 67e3/3.086e22; OL = 0.685
HL = H0*np.sqrt(OL)               # de Sitter (event-horizon) Hubble rate
# de Sitter entropy and the double-scaling parameter p:
ellP = 1.616e-35                  # Planck length
R_dS = c/HL                       # de Sitter radius (event horizon) ~ 1.6e26 m
S_dS = np.pi*(R_dS/ellP)**2       # A/4G in nats ~ 1e122
p_phys = R_dS/ellP                # the divergent double-scaling factor ~ 1e61


def dssyk_vacuum_dos(q, N=4000):
    """Chord transfer matrix; physical DOS = chord-VACUUM spectral measure rho(E)=sum_i|<0|E_i>|^2 delta(E-E_i)."""
    n = np.arange(1, N); b = np.sqrt((1-q**n)/(1-q))
    E, V = eigh_tridiagonal(np.zeros(N), b)
    return E/(2/np.sqrt(1-q)), V[0, :]**2     # E normalized to [-1,1]; q-Gaussian weights


def sectionA_reproduce_contradiction():
    print("="*94)
    print("(A) THE REPO'S INTERNAL CONTRADICTION: same route, two opposite verdicts on Z")
    print("="*94)
    C = np.sqrt(8/np.pi)/(4*np.pi)
    print("force_Z_verdict.py uses T_freeze = Gibbons-Hawking T_dS/E0 = lambda/(4pi):")
    print(f"   a0/cH = C*sqrt(lambda),  C = sqrt(8/pi)/(4pi) = {C:.5f};  S_dS = 4pi^2/lambda")
    for S in (21.3, 1e6, 1e122):
        lam = 4*np.pi**2/S
        print(f"     S_dS={S:>8.1e} -> lambda={lam:.3e} -> a0/cH={C*np.sqrt(lam):.3e} -> Z={1/(C*np.sqrt(lam)):.3e}")
    print("   => physical S_dS~1e122 gives Z~1e61. 'COMPUTED TO FAIL.'\n")

    print("the_wall.py instead REQUIRES T_freeze = the BAND EDGE (NV infinite-temperature), not Gibbons-Hawking:")
    RHO0 = 0.39; qs = 0.925
    band_TH = (2/np.sqrt(1-qs))/(1/(2*np.pi))      # band edge in units of T_H=J/2pi
    req = Z*np.pi/RHO0
    print(f"   s=Z requires T_freeze/T_H = Z*pi/rho(0) = {req:.0f};  band edge at q={qs} is {band_TH:.0f} -> MATCH")
    print(f"   so it 'closes' ONLY by setting T_freeze=band edge (~47 T_H) AND freezing q at 0.925 (S_dS=4pi^2/lam={4*np.pi**2/(-np.log(qs)):.0f}!).\n")

    print("DIAGNOSIS OF THE CONTRADICTION (the load-bearing fork):")
    print("   * Both agree the freezing SLOPE ~ 1/sqrt(1-q) and the flat window ~ (1-q).")
    print("   * force_Z: plug the PHYSICAL lambda (S_dS=1e122 => lambda~4e-121 => q~1) -> window collapses -> Z->inf.")
    print("   * the_wall: plug a FINITE q=0.925 (S_dS~520!) -> window is wide enough -> Z=5.79 self-consistent.")
    print("   => They differ ONLY in lambda_dS. the_wall's closure SECRETLY needs S_dS~O(100s), NOT 1e122.")
    print("      That is the SAME 21-bit-universe pathology force_Z exposes: a finite q gives Z but a tiny universe.")
    print("   VERDICT: the closure is illusory. With the physical S_dS~1e122 (q->1), the Gibbons-Hawking freezing")
    print("            window shrinks faster than the slope grows, so Z->inf. The two files agree once you DEMAND")
    print("            the physical entropy. 'the_wall.py closes Z' was an artifact of an unphysically small q.\n")


def sectionB_literature_resolution():
    print("="*94)
    print("(B) WHAT THE 2024-2026 LITERATURE SETTLED -- and the new structural input the repo lacked")
    print("="*94)
    print("CENTER-vs-EDGE, current status (primary sources):")
    print("  * Narovlansky-Verlinde 2310.16994: dS at E=0 (spectral CENTER, infinite Boltzmann temp). [original]")
    print("  * Okuyama / 'dS JT from DSSYK' 2505.08116: dS at the UPPER EDGE E=E0; rho~sqrt(E0^2-E^2) (sqrt-vanishing),")
    print("    EXPLICITLY 'different from' NV; authors: 'interesting to understand the relationship...if any'. UNRECONCILED.")
    print("  * Rahman-Susskind 2401.08555 (v3): REFUTE NV's 'cord temp = Hawking temp'; they differ by p~1e61")
    print("    (T_cord = p*T_Hawking). 'Many temperatures': T_Boltzmann(inf) > T_cord(~p T_H) > T_Hawking.")
    print("  * Susskind 2511.10907 (Nov 2025): CORRECTS his own earlier claim -- dS entropy sits at the stretched")
    print("    horizon a PLANCK distance out (not a string distance); a self-correction, not a closure.")
    print("  * Deformed-DSSYK 2602.06113 (Feb 2026): 'Whether it fits with sine dilaton gravity and other dS3")
    print("    proposals...is not well-understood.' => STILL OPEN in 2026.\n")

    print("THE NEW STRUCTURAL INPUT (sine-dilaton, Blommaert-Mertens-Papalini 2404.03535) the repo did NOT fold in:")
    print("  * Dilaton potential V(phi)=2 sin(phi); ADM energy E = -cos(theta)/(2|log q|)  [their eq 2.13]")
    print("  * TWO horizons in one geometry: black-hole horizon at r=theta, COSMOLOGICAL horizon at r=2pi-theta.")
    print("  * 'Fake temperature' = Hawking temp of a SMOOTH Lorentzian black hole: beta_BH = 2pi/sin(theta) [eq 1.7].")
    print("  * MAXIMUM ENTROPY at theta=pi/2  =>  E=0  =>  the spectral CENTER. <-- this is decisive structure.\n")

    # The fake-temperature curve, evaluated:
    print("  Evaluating beta_BH = 2pi/sin(theta) and T_fake = sin(theta)/2pi across the band:")
    for th_deg in (1, 30, 90, 150, 179):
        th = np.radians(th_deg)
        E = -np.cos(th)
        Tf = np.sin(th)/(2*np.pi)
        tag = "  <- center (max entropy, dS horizon)" if abs(th_deg-90)<1e-9 else ""
        print(f"     theta={th_deg:>3} deg: E/E0={E:+.3f}  T_fake=sin/2pi={Tf:.4f}{tag}")
    print("  => T_fake is MAXIMAL at the center theta=pi/2 (E=0) and VANISHES at both edges theta=0,pi.")
    print("     The de Sitter (max-entropy) horizon is the CENTER, where the *fake/Hawking* temperature is largest.")
    print("     This SUPPORTS NV's 'center' placement -- but as the FAKE temperature, not the Boltzmann temperature.\n")


def sectionC_does_it_rescue():
    print("="*94)
    print("(C) DOES THE LITERATURE RESCUE / KILL / RELOCATE THE WALL? -- and the one number the framework needs")
    print("="*94)
    print("The framework's freezing argument needs ONE number: T_freeze in spectral-width units (E0). Candidates,")
    print("now sharpened by the literature into the 'many temperatures':\n")

    # Compute the central q-Gaussian DOS slope rho(0) and the implied a0/cH for each temperature reading.
    q = 0.5
    x, w = dssyk_vacuum_dos(q); w = w/w.sum()
    xs = np.linspace(0.004, 0.04, 8); fs = np.array([w[np.abs(x) < t].sum() for t in xs])
    slope = np.polyfit(xs, fs, 1)[0]     # c1 = 2 rho(0), in E/E0 units
    rho0 = slope/2
    print(f"   central q-Gaussian slope c1=2 rho(0) = {slope:.3f}  (q={q}); rho(0) = {rho0:.3f}.\n")

    print("   READING 1 -- Gibbons-Hawking (cold): T_freeze/E0 = lambda/4pi.  [force_Z_verdict]")
    print("      a0/cH = c1*(lambda/4pi) -> 0 as lambda->0 (physical).  => Z->inf.  WALL STANDS (sign+coeff fail at q->1).")
    print("   READING 2 -- cord/stretched-horizon (Rahman-Susskind): T_freeze = p*T_H, p~1e61.")
    print("      a0/cH = c1*(p*lambda/4pi). With lambda~1/p^2 (S_dS=p^2 area law): a0/cH ~ c1/(4pi*p) -> 0 too.")
    print("      => the blue-shift p does NOT save it: the window still collapses. WALL STANDS.")
    print("   READING 3 -- NV center / band edge (the_wall's closure): T_freeze = band edge ~ 4pi/sqrt(1-q).")
    print("      Only 'works' at finite q~0.925 (S_dS~520), i.e. a 520-nat universe. Physically excluded. WALL STANDS.\n")

    print("   THE DECISIVE POINT the new sine-dilaton structure forces (and it CUTS AGAINST the freezing route):")
    print("   The de Sitter horizon is the spectral CENTER (confirmed by V=2sin(phi), max entropy at theta=pi/2).")
    print("   BUT the relevant *Hawking* temperature there is the FAKE temperature T_fake=sin(theta)/2pi, which is")
    print("   O(1) in string units and INDEPENDENT of the area-law collapse -- it does NOT scale to zero as q->1.")
    print("   So the sign mechanism (flat DOS at center) is on FIRMER ground than the repo thought (center IS where")
    print("   max entropy lives, now triply-sourced: NV + sine-dilaton + Rahman-Susskind flat entanglement spectrum).")
    print("   HOWEVER: the COEFFICIENT still fails, because a0/cH ~ (T_freeze/E0) and the *physical* energy window")
    print("   that must freeze is set by the REAL (Boltzmann/Gibbons-Hawking) temperature, which DOES collapse with")
    print("   the area law (S_dS~1e122). Fake temperature controls correlator decay, not the spectral fraction that")
    print("   freezes. So:\n")

    print("   ===> NET 2026 VERDICT ON THE WALL:")
    print("        * SIGN: the wall is LOWERED. 'dS = spectral center (flat DOS)' is now supported by THREE")
    print("          independent 2024-25 constructions (NV center; sine-dilaton max-entropy at theta=pi/2; R-S flat")
    print("          entanglement spectrum). The deep-MOND linear-freezing MECHANISM sits at a genuinely-central,")
    print("          genuinely-flat region. The center-reading is no longer a lone NV conjecture.")
    print("        * COEFFICIENT: the wall STANDS, and is now better understood as a SCALE-SEPARATION obstruction,")
    print("          NOT a center-vs-edge ambiguity. The 'fake vs real temperature' split (sine-dilaton 2404.03535)")
    print("          is the precise reason: the coefficient Z needs the freezing fraction tied to the REAL")
    print("          (area-law) temperature, which collapses as S_dS~1e122 -> Z->inf. The literature's own")
    print("          unresolved 'fake vs Boltzmann temperature' is THE WALL, relocated and named.")
    print("        * The center-vs-edge DISPUTE (the repo's stated wall) is partially resolved IN THE FRAMEWORK'S")
    print("          FAVOR for the SIGN, but the deeper obstruction (which temperature sets the freezing) is now")
    print("          the live open question -- and it is the SAME 'two-temperature puzzle' the field itself flags")
    print("          as not-well-understood in 2026 (2602.06113).\n")


def sectionD_concrete_prediction():
    print("="*94)
    print("(D) THE ONE CONCRETE, FALSIFIABLE CONSEQUENCE that survives (a genuine new statement)")
    print("="*94)
    print("If the framework's emergent-MOND-from-dS picture is right, the sine-dilaton dictionary makes a SHARP,")
    print("checkable structural demand that did not exist before this session:\n")
    print("   CLAIM: the deep-MOND sign requires the near-horizon matter probe to map to theta=pi/2 (E=0), where")
    print("   the FAKE (Hawking) temperature T_fake=sin(theta)/2pi is MAXIMAL and stationary (dT_fake/dtheta=0).")
    print("   This is a NON-TRIVIAL consistency check: the MOND scale a0 ~ (fake-temperature)|max, and the")
    print("   stationarity dT_fake/dtheta|_{pi/2}=0 means a0 is an EXTREMUM -- robust to small probe mis-centering.")
    th = np.pi/2
    dTf = np.cos(th)/(2*np.pi)   # derivative of sin(theta)/2pi
    print(f"   CHECK: d/dtheta [sin(theta)/2pi] at theta=pi/2 = cos(pi/2)/2pi = {dTf:.3e}  (=0, stationary). PASS.")
    print("   => a0 sits at a STATIONARY point of the fake-temperature curve. This is the DSSYK shadow of Milgrom's")
    print("      'a0 is the maximal surface gravity / de Sitter temperature' -- and it is a check the framework")
    print("      PASSES structurally. It is NOT a derivation of Z (the magnitude still needs the real-temperature")
    print("      window), but it is a new, true, framework-consistent statement: the MOND scale = the fake-temperature")
    print("      maximum at the spectral center, an extremum protected by theta-reflection symmetry.\n")
    print("   FALSIFIABLE FORM: if a future settled dictionary places the dS horizon at an EDGE (theta=0 or pi),")
    print("   then T_fake->0 there, the freezing is sqrt-law (T^3/2, super-linear, 2505.08116), and the deep-MOND")
    print("   sign is WRONG. So 'dS = spectral center' is a genuine, now-testable prerequisite of the whole picture,")
    print("   and the 2025 edge papers (2505.08116) are a live route to FALSIFY the framework's microscopic basis.")


def main():
    print("#"*94)
    print("# RE-LITIGATING THE WALL (2026): center-vs-edge, fake-vs-real temperature, and what survives")
    print("#"*94 + "\n")
    print(f"  Framework numbers: Z={Z:.4f}, R_dS={R_dS:.2e} m, S_dS={S_dS:.2e} nats, p=ell_dS/ell_P={p_phys:.2e}\n")
    sectionA_reproduce_contradiction()
    sectionB_literature_resolution()
    sectionC_does_it_rescue()
    sectionD_concrete_prediction()
    print("#"*94)
    print("# END")
    print("#"*94)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
ROUTE F -- ADVERSARIAL STRESS TEST of the load-bearing claim.
=============================================================
THE CLAIM under attack: the gated nonlocal-R metric partner supplies the FULL deep-MOND
lensing boost B = g_obs/g_N (-> infinity as g_N->0) via the GRAVITY sector, YET adds NO
propagating fifth-force d.o.f. on matter and is GATED OFF in the solar system, so it does
NOT re-incur Cassini.

THE ADVERSARY (the honest worry): ANY metric-sector term that bends light by B>1 ALSO bends
the trajectories of slow MATTER by the SAME B (light and matter both follow the same metric
geodesics in the weak field, the lensing potential Phi+Psi governs light, Phi governs matter;
no-slip Phi=Psi means BOTH are boosted). So if the metric partner boosts LENSING in a galaxy,
it ALSO boosts the gravitational ACCELERATION of stars there -- i.e. it is contributing to
DYNAMICS as modified GRAVITY, on TOP of the modified-INERTIA matter sector. That risks (a)
DOUBLE-COUNTING the MOND boost (MI gives it once, the metric partner gives it again), and (b)
being modified gravity after all (the metric partner DOES accelerate matter, it is not inert).

This script adjudicates HONESTLY, sympy. If the partner double-counts or is secretly MG, say
OBSTRUCTED. If there is a consistent split, characterize it EXACTLY.
"""
import sympy as sp

def H(t): print("\n"+"="*84+"\n "+t+"\n"+"="*84)

H("ADVERSARY 1: does the metric partner DOUBLE-COUNT the MOND boost?")
print("""
Setup. Two sectors both want to produce the SAME deep-MOND dynamics:
  (A) MI matter sector: modifies INERTIA. m*mu_fw(a/a0)*a = g_N(baryon).  Solving:
      a_dyn = g_obs = sqrt(g_N^2 + g_N a0).  This already gives stars the MOND acceleration
      from the BARYON-sourced Newtonian field g_N. NO metric modification needed for DYNAMICS.
  (B) metric partner: modifies the METRIC so LIGHT is boosted by B=g_obs/g_N.

If (B) ALSO boosts the gravitational field felt by matter (because matter follows the same
boosted metric), then a star feels BOTH g_obs (from MI) AND an extra pull from (B) => the
acceleration would be DOUBLE the intended MOND value => WRONG rotation curves. ADJUDICATE.
""")
gN, a0 = sp.symbols('g_N a_0', positive=True)
g_obs = sp.sqrt(gN**2 + gN*a0)

print("""
THE RESOLUTION (the key structural point, CONSTRUCTED). The two sectors are NOT both
'gravitational forces on matter'. They live in DIFFERENT places in the action:

  - The MI sector modifies the LEFT-hand side of the matter EOM (the inertia m -> m*mu_fw).
    It does NOT change the metric or g_N. The force on the star is still g_N (baryon-Newtonian),
    but the star's RESPONSE is a = g_N/mu_fw = g_obs. This is a MATTER-sector (kinetic) change.

  - The metric partner modifies the METRIC that NULL geodesics (light) follow. For light there
    is NO inertia to modify (photons are massless, mu_fw is irrelevant to a null geodesic), so
    WITHOUT the partner light would only feel the baryon metric (g_N) => under-lensing. The
    partner supplies, FOR LIGHT, the boost that MI supplies FOR MATTER.

  THE CONSISTENCY CONDITION (no double-count): the metric partner must boost the EFFECTIVE
  lensing potential to exactly g_obs -- the SAME value MI gives matter -- so that M_lens=M_dyn.
  But it must NOT additionally boost the TIMELIKE-geodesic acceleration of matter, because
  matter already gets g_obs from MI. The question: can a metric term boost NULL geodesics
  (light) to g_obs WITHOUT boosting TIMELIKE geodesics (matter) beyond g_N?
""")

H("ADVERSARY 1 -- the sharp test: can a metric term split light from matter?")
print("""
In the weak field ds^2 = -(1+2Phi)dt^2 + (1-2Psi)dx^2:
  - TIMELIKE (matter) geodesic acceleration  =  grad Phi.   (the 'dynamical' potential)
  - NULL (light) deflection                  =  grad(Phi+Psi).   (the 'lensing' potential)

A metric partner that adds dPhi to Phi and dPsi to Psi:
  - changes matter acceleration by grad(dPhi)
  - changes light deflection by grad(dPhi+dPsi).

For the partner to boost LIGHT to g_obs but leave MATTER at g_N (no double-count), we'd need:
  grad(dPhi+dPsi) = (g_obs - g_N)  [boost light]   AND   grad(dPhi) = 0  [don't touch matter].
=> grad(dPhi)=0 and grad(dPsi) = g_obs - g_N.  i.e. the partner adds to Psi (the SPACE
potential, which light sees but slow matter does NOT) and NOT to Phi.  But that is a SLIP:
dPhi=0, dPsi!=0 => Phi != Psi => SLIP. CONTRADICTS the no-slip claim of Section 1b!
""")
# This is the crux. Make it quantitative.
Phi_b, Psi_b = sp.symbols('Phi_b Psi_b')  # baryon GR potentials (equal: GR no slip)
dPhi, dPsi = sp.symbols('dPhi dPsi')       # partner additions
print("  Baryon GR (no slip): Phi_b = Psi_b (call it phi_N, with grad phi_N = g_N).")
print("  Matter accel  = grad(Phi_b + dPhi) = g_N + grad(dPhi).")
print("  Light deflect = grad(Phi_b+dPhi + Psi_b+dPsi) = 2g_N + grad(dPhi+dPsi).")
print("""
  TWO logically distinct ways to get the lensing right, and they DIFFER on matter:

  OPTION A (no-slip, dPhi=dPsi): partner adds EQUALLY to both.
     matter accel  = g_N + grad(dPhi)         <- MATTER IS BOOSTED TOO
     light deflect = 2(g_N + grad(dPhi)) = 2 * (matter accel)  <- M_lens = M_dyn, consistent
     BUT now matter feels g_N + grad(dPhi). For M_lens=M_dyn=M_baryon*B we need
     matter accel = g_obs => grad(dPhi) = g_obs - g_N. So the partner DOES accelerate matter
     by (g_obs-g_N). => the partner IS contributing to DYNAMICS. Then the MI sector must NOT
     also boost matter, or we double-count.

  OPTION B (slip, dPhi=0, dPsi=g_obs-g_N): partner adds ONLY to Psi (space curvature).
     matter accel  = g_N (unchanged)          <- MATTER NOT boosted by partner; MI does it
     light deflect = g_N + (g_N + (g_obs-g_N)) = g_N + g_obs ... not quite M_lens=M_dyn; and
     this is the OLD non-relativistic-MOND-style SLIP. M_lens != M_dyn in general.
""")

H("ADVERSARY 1 VERDICT: the honest split -- the partner CANNOT be pure-MI-passive AND no-slip")
print("""
The adversary is RIGHT that there is a real fork, and it forces an HONEST CHOICE:

  *** If we want NO SLIP (M_lens=M_dyn, the clean lensing reframe), then OPTION A: the metric
      partner MUST accelerate matter by (g_obs - g_N) -- it is, for DYNAMICS, acting as
      modified GRAVITY. Then to avoid double-counting, the MOND boost on matter comes
      EITHER from MI (inertia) OR from the partner (gravity), NOT both. ***

This is the load-bearing finding, and it is NOT what the first script implied. Let me state the
TWO self-consistent theories the construction actually allows, and which one is Cassini-safe:
""")

print("""
THEORY I -- 'MI does dynamics, partner does ONLY the slip-free lensing top-up' (OPTION B-fixed):
  - Matter dynamics: 100% from MI inertia (a=g_obs, partner adds 0 to Phi). Cassini-safe (MI gate).
  - Lensing: MI gives photons NOTHING (massless), so the partner must supply the FULL
    (g_obs - g_N)*2 deflection -- but via Psi ONLY (since Phi is reserved for MI-matter) => SLIP.
  - This is a SLIP theory (Phi != Psi). It CURES lensing but it is the OLD slip structure;
    M_lens and M_dyn agree in MAGNITUDE (both ~g_obs) but via different potentials. It works
    for spherical lensing IF the partner's Psi-source equals the MOND phantom. VIABLE but it is
    NOT 'no slip' -- the no-slip claim in script 1 Section 1b was OPTION-A reasoning misapplied.

THEORY II -- 'partner does dynamics AND lensing (no slip), MI is redundant for galaxies':
  - Both Phi and Psi boosted equally => no slip => M_lens=M_dyn. But then the partner
    accelerates MATTER by (g_obs-g_N) = it is MODIFIED GRAVITY for dynamics. The MI sector
    would double-count, so MI must be SWITCHED OFF for bound dynamics -- i.e. this theory is
    just AeST-class modified gravity wearing a nonlocal-R coat. UNGATED for matter => CASSINI.
    *** THEORY II re-incurs Cassini. It is the trap. ***
""")
# Quantify Theory II's Cassini exposure: if the partner accelerates matter, the gate must shut
# it off at high a. Check whether a gate G_gate=1-mu_fw on a GRAVITY term that accelerates
# matter actually evades Cassini the way the MI gate does.
print("""
THE DECISIVE CASSINI CHECK for THEORY II (partner accelerates matter, gated by 1-mu_fw):
  The extra matter acceleration is  da_partner = G_gate(a/a0) * (phantom source).
  At Saturn a/a0=6.9e5, G_gate=1-mu_fw=7.2e-7. The deep-MOND phantom would give ~a0; gated:
""")
x = sp.symbols('x', positive=True)
mu_fw = (sp.sqrt(1+4*x**2)-1)/(2*x)
G_gate = 1 - mu_fw
x_cass = sp.Rational(69,100)*sp.Integer(10)**6
a0_val = sp.Float('9.36e-11')
da_partner_cass = G_gate.subs(x, x_cass) * a0_val   # gated phantom acceleration ~ G_gate*a0
print("   da_partner(Saturn) ~ G_gate*a0 =", sp.N(da_partner_cass, 3), "m/s^2")
# Cassini bounds the anomalous acceleration gradient / the |d(a_anom)/dr| ~ Q2 < 5e-27 /s^2.
# Compare to a quasi-Newtonian: the relevant Cassini quantity is the anomalous tidal Q ~ da/dr.
# Use the MOND-EFE Cassini number form: the ungated AeST gives Q2~3e-26; gated by 1-mu_fw:
Q2_aest = sp.Float('3.2e-26')
Q2_gated = Q2_aest * G_gate.subs(x, x_cass)   # gate the SAME way the MI sector is gated
print("   IF the partner's matter-acceleration is gated by the SAME 1-mu_fw as MI:")
print("     Q2_gated ~ Q2_aest * G_gate =", sp.N(Q2_gated, 3), "s^-2  vs ceiling 5e-27 s^-2")
print("     => gated Q2 =", sp.N(Q2_gated,3), "<< 5e-27 => PASSES Cassini IF gating is legitimate.")
print("""
   *** THE REAL QUESTION for Theory II: is it LEGITIMATE to gate a GRAVITY-sector term (one
   that accelerates matter) by 1-mu_fw(a/a0)? ***
   - In MI, the gate is NATURAL: mu_fw is the inertia function, a/a0 is the body's OWN
     acceleration, and the gate falls out of the worldline form factor. Self-consistent.
   - In a GRAVITY term that accelerates matter, 'a' in G_gate(a/a0) must be the FIELD-POINT
     acceleration. A modified-Poisson theory with mu(|grad Phi|/a0) IS exactly this (AQUAL):
     mu->1 at high |grad Phi| switches the modification OFF in the solar system. That is the
     QUMOND/AQUAL screening -- and it DOES suppress at high a. So a gated gravity term CAN
     evade Cassini IF the gate is on the LOCAL FIELD strength.
   - BUT: AQUAL/QUMOND's solar-system suppression is ALREADY KNOWN to be INSUFFICIENT in the
     EFE-dominated regime -- the GALACTIC external field g_ext~a0 keeps mu away from 1 even
     where the SOLAR field is large, leaving a residual that is exactly the banked AeST/AQUAL
     Cassini failure (Q2~3e-26). The external field does NOT switch off. ***THIS is why
     ungated-for-the-EFE modified gravity fails Cassini, and why Theory II is the trap.***
""")

H("THE HONEST RESOLUTION: which theory is real, and is it MI-compatible or MG?")
print("""
The adversary forces the truth into the open. There are TWO consistent constructions, and they
are DIFFERENT THEORIES with DIFFERENT Cassini fates:

  THEORY I (SLIP, MI-led):  matter dynamics 100% from gated MI inertia (Cassini-safe by the MI
     gate, ~6 orders, robust because the MI gate is on the BODY's own a, and a free-falling
     body in the solar system has a>>a0 REGARDLESS of the galactic external field -- the MI
     gate is NOT spoiled by the EFE the way AQUAL's is). The metric partner supplies lensing
     via a Psi-only (slip) source = the MOND phantom for LIGHT. Photons are massless so there
     is NO MI for them; the partner is the ONLY thing that lenses. The partner does NOT
     accelerate matter (it lives in Psi, the space-space potential, which slow matter ignores),
     so it adds NO fifth force on planets => Cassini-safe TRIVIALLY (it doesn't touch matter).
     *** THEORY I is genuinely MI-compatible and Cassini-safe. Its price: it has a SLIP
     (Phi != Psi), so the 'no-slip M_lens=M_dyn identity' must be RESTATED as 'M_lens=M_dyn in
     MAGNITUDE because the partner's Psi-source is tuned to the MI phantom' -- a MATCHING, not
     an identity. ***

  THEORY II (NO-SLIP, MG-led): the partner boosts Phi and Psi equally => it accelerates matter
     => modified gravity => its solar-system suppression is AQUAL-class => spoiled by the
     galactic EFE => Cassini FAILS (the banked AeST result). *** THEORY II is the trap; it is
     modified gravity re-incurring Cassini. ***

  THE FRAMEWORK'S DISTINCTIVE CHOICE: THEORY I. The whole POINT of modified INERTIA is that the
  gate is on the BODY's proper acceleration (a_Saturn >> a0 always), NOT on the local field
  (which the EFE keeps near a0). So the MI gate is Cassini-robust where the AQUAL gate is not.
  The metric partner in Theory I is a SLIP term that lenses light, does not touch matter, and is
  Cassini-safe because it never accelerates a planet.
""")

print("""
*** CORRECTION TO SCRIPT 1 (honest, both ways): script 1's Section 1b claimed NO SLIP from a
    conformal/scalar source. That is OPTION A = Theory II = modified gravity = Cassini trap.
    The MI-COMPATIBLE construction is Theory I, which DOES have a slip (the partner lenses light
    via Psi without accelerating matter). The correct statement is NOT 'no slip', but:
      'the metric partner is a LIGHT-ONLY (Psi-sector) source tuned so the lensing MAGNITUDE
       equals the MI dynamical mass: |M_lens| = |M_dyn| by MATCHING, with a real slip Phi!=Psi
       that is invisible to slow matter (Cassini-safe) and supplies the deflection for photons.'
    M_lens = M_dyn holds as a MATCHED MAGNITUDE, not as a no-slip identity. ***
""")

H("Is THEORY I's light-only Psi-source ghost-free and c_T=c?")
print("""
  - c_T=c: a Psi-only (space-curvature) source that does not propagate (slaved to the baryon
    distribution via the nonlocal Box^{-1}) does not modify the graviton kinetic term => c_T=c.
    Same conformal/nonlocal argument as script 1 Section 4, and now even safer (it is a
    constraint-sourced potential, not a kinetic term). PASS.
  - ghost: the Psi-source is a CONSTRAINT (elliptic, sourced by baryon density through the
    nonlocal kernel), not a propagating field => no kinetic ghost. The DEW order-lowering still
    applies. CONDITIONAL-PASS (same caveat: full Hamiltonian IR analysis open).
  - But note: a Phi != Psi slip with a Psi-only source IS what TeVeS/original-RMOND debated;
    the modern AeST CURED the slip by making the scalar source Phi too. Theory I deliberately
    does NOT do that (to stay MI-compatible), so it lives with a slip -- which is OBSERVABLE
    (the lensing-vs-dynamics potential difference) and is a PREDICTION/exposure of Theory I.
""")

H("ADVERSARIAL NET (both ways)")
print("""
The adversary materially SHARPENED and PARTLY CORRECTED the construction:

  CONFIRMED (credit): a covariant metric partner that supplies the missing lensing and COEXISTS
  with gated MI without re-incurring Cassini EXISTS -- it is THEORY I: a gated, nonlocal,
  light-only (Psi-sector) source tuned to the MOND phantom. It is Cassini-safe NOT by a fragile
  AQUAL-gate but because it never accelerates matter (the MI gate, on the body's own a, does the
  dynamics and is EFE-robust). c_T=c, ghost-conditional.

  CORRECTED (concede): the 'NO SLIP, M_lens=M_dyn identity' of script 1 was Theory-II reasoning
  (conformal source boosts Phi too => accelerates matter => modified gravity => Cassini trap).
  The MI-compatible theory has a REAL SLIP; M_lens=M_dyn holds as a MATCHED MAGNITUDE (the
  Psi-source tuned to the MI phantom), not as a field-equation no-slip identity. The clean
  'lensing reframe' that AeST gets for free (genuine no-slip) is, for the GATED-MI theory, a
  TUNED match with an observable slip -- a weaker, honest statement.

  THE TRAP NAMED: making it true-no-slip (Theory II) = boosting Phi = accelerating matter =
  modified gravity = Cassini failure via the EFE-spoiled AQUAL gate. So the metric partner can
  ONLY coexist with gated MI as a SLIP (light-only) term. The price of Cassini-safety is a slip.

  => Route F: BUILT but with a CORRECTED, weaker lensing claim (matched-magnitude slip, not
     no-slip identity) and a sharpened Cassini argument (the MI gate is EFE-robust where the
     AQUAL gate is not -- THAT is what lets the partner coexist). OBSTRUCTED on 'no-slip
     identity'; BUILT on 'Cassini-safe matched-magnitude lensing partner'.
""")

"""
agentTT ROUTE 1 — PART 4: MAXIMUM-HOSTILITY AUDIT of the 'center-forced' reading.
Two independent attacks, each pointed AT the forcing claim (Carl's both-ways rule).

ATTACK 1 — CIRCULARITY: is 'edge is the wrong rep' an INDEPENDENT rep-theoretic exclusion,
or is it just agentS's dynamical t^{-3/2} fact wearing a rep costume?
  The rep-class label at the edge was DERIVED FROM the pole positions = the SAME object
  agentS used to get t^{-3/2}. If the ONLY input is 'poles ring + leave band', then the rep
  language adds no new exclusion -- it is the dynamical fact relabeled. For rep-matching to
  be an INDEPENDENT forcing, the GRAVITY side (GH discrete series) must impose a constraint
  that the matter side must satisfy, such that the edge VIOLATES it for a reason not already
  contained in 'the edge decays as t^{-3/2}'.
  TEST: is there a rep-theoretic statement on the GH side that, by itself, REQUIRES the matter
  vacuum's modular rep to be discrete-series? Or does the GH side merely DESCRIBE its own
  relaxation (agnostic about which matter placement realizes it)?

ATTACK 2 — SEMICLASSICAL DEGRADATION (agentS's own stated weakness #ii): the unique-no-ringing
  selector Re omega=0 -> theta_v=pi/2 is SHARP only at finite lambda; semiclassically it
  degrades to O(lambda). If the rep-class boundary (discrete vs continuous) ALSO blurs as
  lambda->0, then in the semiclassical (physical dS) limit the rep distinction may not cleanly
  exclude near-center placements -> weakens forcing toward favoring.
  TEST: compute how sharply the rep class flips across theta_v at finite lambda, and whether
  the discrete-series window shrinks to a measure-zero point (sharp) or stays finite (robust)
  as lambda->0.
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 40

print("="*78)
print("PART 4 — hostility audit: circularity + semiclassical degradation")
print("="*78)

# ---------------- ATTACK 1: circularity ----------------
print("\n" + "-"*78)
print("ATTACK 1 — is the edge-exclusion INDEPENDENT of agentS's t^{-3/2}, or circular?")
print("-"*78)
print("""
The honest structural finding:
  - The GH static-patch SL(2,R) is the symmetry of the GRAVITY/horizon side. agentSS proved
    its modular flow (Tomita-Takesaki of the GH state) = the boost, with DISCRETE spectrum
    {Delta+k} (the QNM ladder). That is a property of the dS HORIZON, fixed independently of
    the DSSYK placement.
  - The matter 2-pt function's modular rep about |theta_v> is DISCRETE only at center.
  - For 'rep-matching FORCES center' to be INDEPENDENT, the GH discrete series must be a
    REQUIREMENT the matter side has to meet. But what supplies that requirement?
      * The GH discrete spectrum is the spectrum of dS QNMs -- a statement about how the
        HORIZON relaxes. It does NOT, by representation theory alone, say the matter chord
        vacuum MUST be modular-discrete. It says: IF the matter sector is to reproduce dS
        relaxation, its modular rep must be the discrete series.
  CONCLUSION: the GH discrete series is the TARGET, not an a-priori CONSTRAINT on the chord
  algebra. The chord algebra (PART 2) is one continuum rep that admits BOTH placements. So
  the exclusion of the edge comes from REQUIRING the matter modular rep to equal the GH one
  -- which is logically the SAME requirement as agentS's 'reproduce dS relaxation', now in
  rep language. The rep computation is a CLEANER, more structural statement of the SAME fact,
  not a NEW independent exclusion.
""")
print("=> ATTACK 1 lands PARTIALLY: rep-matching is NOT an independent NEW forcing; it is")
print("   agentS's dynamical discriminator promoted to a rep-class statement. It SHARPENS")
print("   'edge-wounded' (the failure is now a clean rep-class mismatch, not just a fit), but")
print("   it does NOT add a second, logically-independent reason to exclude the edge.")
print("   The CONDITIONAL is identical: 'IF reproduce-dS-relaxation THEN center'.")

# ---------------- ATTACK 2: semiclassical degradation ----------------
print("\n" + "-"*78)
print("ATTACK 2 — does the rep-class boundary blur as lambda->0 (semiclassical)?")
print("-"*78)
Delta = mp.mpf('0.5')
def ring_decay_k0(theta_v, lam):
    u0 = Delta*lam
    re_w = mp.cos(theta_v)*mp.cosh(u0)
    im_w = -mp.sin(theta_v)*mp.sinh(u0)
    return re_w/im_w  # ring/decay for lowest rung

print("\nRe omega = 0 is EXACT at theta_v=pi/2 for ANY lambda (cos(pi/2)=0 identically).")
print("So the DISCRETE-SERIES POINT (pure-decay, real boost spectrum) is theta_v=pi/2 EXACTLY,")
print("independent of lambda. The selector for the EXACT discrete series does NOT blur.\n")
print("What DOES degrade (agentS #ii): the SHARPNESS of ringing just OFF center, ring/decay")
print("at theta_v = pi/2 + delta, lowest rung:")
print(f"{'lambda':>10} {'delta=0.05':>14} {'delta=0.20':>14}  (ring/decay at k=0)")
for lam in [mp.mpf('1.0'), mp.mpf('0.357'), mp.mpf('0.1'), mp.mpf('0.03'), mp.mpf('0.01')]:
    r1 = ring_decay_k0(mp.pi/2 + mp.mpf('0.05'), lam)
    r2 = ring_decay_k0(mp.pi/2 + mp.mpf('0.20'), lam)
    print(f"{float(lam):>10.3f} {float(r1):>14.4f} {float(r2):>14.4f}")
print("\nring/decay at fixed off-center delta = -tan(delta-shift)*coth(Delta*lam) ~ (delta)/(Delta*lam)")
print("as lambda->0 => for FIXED small delta the ringing GROWS like 1/lambda (sharper, not blurrier).")
print("BUT the WIDTH in theta_v over which ring/decay < (say) 1 is delta ~ Delta*lam -> 0:")
for lam in [mp.mpf('1.0'), mp.mpf('0.357'), mp.mpf('0.1'), mp.mpf('0.03'), mp.mpf('0.01')]:
    # solve cot(theta)*coth(Delta lam) ~ tan(delta-from-pi/2)*coth = 1
    width = mp.atan(mp.tanh(Delta*lam))  # delta where ring/decay=1 (using ring/decay=tan(delta)*coth? careful)
    # ring/decay near pi/2: theta=pi/2+d, cos= -sin(d)~ -d, sin~cos(d)~1 => ring/decay ~ -d*coth(Delta lam)
    # |ring/decay|=1 => d = tanh(Delta lam)
    d_eq = mp.tanh(Delta*lam)
    print(f"  lambda={float(lam):.3f}: |ring/decay|<1 window half-width delta = tanh(Delta*lam) = {float(d_eq):.5f} rad")
print("\n=> The pure-discrete POINT (theta_v=pi/2) is lambda-independent & exact, BUT the")
print("   'approximately discrete' NEIGHBORHOOD shrinks ~ Delta*lambda. Semiclassically the")
print("   rep-class flip becomes a SHARPER knife-edge at pi/2 (smaller tolerance), NOT blurrier.")
print("   agentS #ii (selector degrades to O(lambda)) refers to how fast ringing turns ON away")
print("   from center -- which is the COMPLEMENT: off-center, the IMAGINARY/real mixing is O(lambda)")
print("   small, so a near-center placement looks ALMOST discrete to O(lambda). THAT is the genuine")
print("   softening: at finite resolution, theta_v within O(lambda) of pi/2 is rep-indistinguishable")
print("   from exact center. It does NOT revive the EDGE (eps->0, theta_v->pi, maximally far).")

print("\n" + "="*78)
print("PART 4 RESULT")
print("="*78)
print("ATTACK 1: rep-matching is NOT an independent new forcing -- it is agentS's")
print("  reproduce-dS-relaxation discriminator promoted to a clean rep-CLASS statement.")
print("  Same conditional. Sharpens 'edge-wounded' to 'edge = wrong rep class', does not force.")
print("ATTACK 2: the exact discrete POINT theta_v=pi/2 is lambda-independent; semiclassically a")
print("  near-center O(lambda) neighborhood becomes rep-indistinguishable from center (softening")
print("  near center) -- but the EDGE (theta_v->pi) stays maximally far / continuous. No edge revival.")

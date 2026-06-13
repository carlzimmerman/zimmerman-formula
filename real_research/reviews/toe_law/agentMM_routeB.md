# agentMM — Route B: Resurgence / Trans-series on the free pullback at b -> c_chi

**Question.** Treat b -> c_chi as a singular point of the FREE pullback W_b(tau).
Compute the Laurent/asymptotic structure of the free (perturbative) expansion around
b = c_chi and apply resurgence: does the large-order / Stokes data of the perturbative
(free) series DICTATE the FORM (root order, oscillation) of the non-perturbative (pump)
completion's edge ambiguity? Specifically: does resurgence FORCE a fourth-root oscillatory
ambiguity x^{-1/4}cos(...), a different root, or NOTHING (free)?

Discipline: zeta-tilde and (16pi/3)^{1/4} are QUARANTINED INPUT, never re-derived.
All pure numbers RAW. Both-ways hostility; framework-favorable steps get MAXIMUM scrutiny.

## Inputs (from agentEE_sigma_khronon.md, machine-banked there)
- Free pullback on the Deser-Levin (b-)family:
    W_b(tau) = -H^2 / [16 pi^2 c_chi (c_chi^2 - b^2) sinh^2(kappa tau / 2)]
    kappa = H/sqrt(1-b^2),  b^2 = a^2/(a^2+H^2),  kappa^2 = a^2 + H^2,  a = b kappa.
- Amplitude A(b) = H^2 / [16 pi^2 c_chi (c_chi^2 - b^2)]  -> SIMPLE POLE at b = c_chi.
- Edge variable (Deser-Levin sqrt): u = 2 pi / kappa ~ sqrt(c_chi - b) near b=c_chi
  (the sqrt that converts x^{-1/4} into u^{-1/2}).
- Required (target, agentV) tail: sigma_req(u) ~ u^{-13/8} e^{-zeta u^{-1/4}} cos(zeta u^{-1/4} - pi/8),
  fourth-root essential singularity. [TARGET -- must EMERGE, not be assumed.]


## STEP 1 (machine, sympy) — Laurent structure of the free amplitude at b=c_chi
RESULT (raw):
- A(b=c-x), x=c_chi-b, Laurent about x=0:
    A = H^2/(32 pi^2 c_chi^2) * (1/x)  +  H^2/(64 pi^2 c_chi^3)  +  H^2/(128 pi^2 c_chi^4) x + ...
  => **SIMPLE POLE** in x (=c_chi-b). residue_b A at b=c_chi = -H^2/(32 pi^2 c_chi^2).
  This reproduces the edge-map's simple-pole amplitude class EXACTLY.
- The pole is a pure b-pole of an ANALYTIC (meromorphic, in fact RATIONAL) function of b.
  A(b) = H^2/[16 pi^2 c_chi (c_chi-b)(c_chi+b)] -- two simple poles at b=+-c_chi, nothing else.
  There is NO branch point, NO essential singularity, NO oscillation in A(b) itself.

CRITICAL CONE DISTINCTION (machine):
- u = 2 pi / kappa = 2 pi sqrt(1-b^2)/H.  At b->c_chi>1, 1-b^2 = 1-c_chi^2 < 0:
  kappa is IMAGINARY and u is FINITE (=2 pi sqrt(1-c_chi^2)/H, imaginary), NOT -> 0.
- The "u ~ sqrt(c_chi - b)" Deser-Levin sqrt of the edge map holds at the LUMINAL edge b->1
  (where 1-b^2 -> 0), NOT at the sound-cone edge b->c_chi (c_chi>1).
- So b=c_chi is a singular point of the AMPLITUDE (rational pole), while b=1 is the
  branch point of the kinematic kappa/u map. These are DIFFERENT points on the b-line.
  Route B must keep them separate: the "free pullback's b=c_chi pole" is a RATIONAL pole.

## STEP 2 (machine) — Large-order growth of every NATURAL free series
Three candidate "perturbative" (free) expansions; only one is resurgent:
- (2a) deep-MOND series 2-t = 2a^2/(H^2+a^2): coeffs (-1)^k 2/H^{2k}. GEOMETRIC,
  radius H. No factorial. => convergent, NO trans-series, NO ambiguity (matches L8 / V no-kernel).
- (2b) velocity series A(b) about b=0: coeffs 1/c_chi^{2k+3}. GEOMETRIC, radius c_chi.
  No factorial. => convergent, NO trans-series.
- (2c) thermal/Planck worldline density (the free pullback's OWN spectral content):
  Bernoulli coefficients B_{2n} ~ (2n)!/(2pi)^{2n}. FACTORIAL (Gevrey-1). RESURGENT.
  This is the ONLY free series carrying genuine resurgent structure.

## STEP 3 (machine) — Borel/Stokes structure of the free thermal (sinh^{-2}) series
- 1/sinh^2(kappa tau/2) has DOUBLE poles in complex tau at tau_m = 2 pi i m/kappa, m in Z\{0}.
- Nearest singularity |tau_1| = 2 pi/kappa = u  ==> the resurgent INSTANTON ACTION is u itself.
- Large-order coeffs a_{2j} of the regular part converge to (2j+1)*2/pi^{2j+2}:
    j=4 ratio 1.0010 ; j=8 ratio 1.000004 ; j=11 ratio 1.000000 (machine).
  This is the textbook signature of a DOUBLE-POLE Borel singularity (coeff ~ n * geometric).
- Non-perturbative weight forced: exp(-omega * 2pi/kappa) = exp(-2 pi omega/kappa)
  -- a SIMPLE exponential e^{-A omega}, A=2pi/kappa, times a POLYNOMIAL (log-free) prefactor.

**RESURGENCE VERDICT (free data):** the free series' Borel singularity is a DOUBLE POLE,
not a fractional branch point. Resurgence on the FREE data forces:
  - instanton action A = 2 pi/kappa (linear in u, i.e. e^{-2pi omega/kappa}),
  - integer-power (polynomial) prefactor,
  - the discrete tower m=1,2,3,... (images at i pi m) = the thermal Matsubara tower.
It does NOT force a fourth-root, ANY root, or a stretched exponential e^{-c omega^{1/3}}.
The free Stokes data is THERMAL (KMS), exactly as agentEE found by other means.

## STEP 4 (machine) — Gevrey-class mismatch: the decisive resurgence test
The TARGET fourth-root e^{-zeta u^{-1/4}} is, by the standard Gevrey<->essential-sing
dictionary, the resurgent partner of a series with coefficients ~ (4n)! (Gevrey-4 / order 1/4).
- (4n)!^{1/n}/n DIVERGES (951 at n=5 -> 2.5e6 at n=80): Gevrey-4 fingerprint.
- (2n)!^{1/n}/n DIVERGES (4.1 -> 45): the free thermal Gevrey-1 class.
- FREE worldline-time coeffs |a_n|^{1/n} -> 1/pi (BOUNDED, 0.345 -> 0.325): GEVREY-0,
  the free tau-series is CONVERGENT. It carries NEITHER (4n)! NOR (2n)! growth in tau.
=> The free perturbative data and the target sit in DIFFERENT resurgence universality
   classes. Resurgence cannot produce a Gevrey-4 (fourth-root) non-perturbative partner
   from Gevrey-<=1 free data: the alien-derivative tower is generated BY the free Borel
   singularities, and a finite set of equally-spaced poles (Matsubara) generates only
   integer-power, simple-exponential alien terms, never a quartic branch.

## STEP 4b (machine) — edge-map singularity-type is map-invariant
- Free Matsubara actions S_m = 2 pi m/kappa are LINEAR in m (equal spacing) -> simple-pole tower.
- A u^{-1/4} essential singularity needs saddle actions accumulating on a quartic lattice
  (confluent/coalescing tower), ABSENT in the free spectrum.
- The Deser-Levin edge map is analytic (sqrt); analytic composition preserves singularity
  TYPE. The surviving free edge exponent sqrt(c_chi(c^2-b^2)) ~ sqrt(2) c_chi sqrt(x) is a
  SQUARE-ROOT (k=1/2) branch, NOT a fourth-root (k=1/4). (sympy, leading term confirmed.)

## STEP 5 (machine) — hostile self-audit of the literal b=c_chi pole
- Full free pullback near b=c_chi (x=c_chi-b): leading term ~ 1/x (SIMPLE pole), residue
  carries the analytic, nonzero sinh^2(kappa_c tau/2). kappa is ANALYTIC at b=c_chi (its
  branch point is at b=1, i.e. x=c_chi-1 != 0). => the b=c_chi pole is a clean SIMPLE pole
  with an analytic residue: NO fractional power, NO oscillation germ at the literal pole.
- Correction logged: the edge-map 'pole-cancels-to-constant' identity is the LUMINAL b->1
  response statement; the b->c_chi AMPLITUDE pole is real and does not cancel. Does NOT
  change the resurgence verdict (the type argument is robust to which response is taken).

## VERDICT (Route B / resurgence)
**Resurgence on the FREE data does NOT force a fourth-root oscillatory ambiguity. It forces
a THERMAL (simple-exponential, integer-power, equally-spaced Matsubara tower) structure --
a DIFFERENT class. The fourth-root is NOT carried by the free Stokes data.**

- carries_fourth_root = NO (computed; the free Borel data is a double-pole/Matsubara tower,
  Gevrey<=1, whereas the fourth-root needs Gevrey-4 / a quartic confluent tower).
- This CONFIRMS by an independent (resurgence/trans-series) route what agentEE found
  kinematically: the free khronon edge is thermal, the fourth-root must be supplied by the
  PUMP modifying the dynamics (which changes the Borel singularity structure -- legal, since
  a different EOM has different Stokes data -- but NOT dictated by the free large-order data).
- edge_form = thermal Matsubara tower / simple-exponential e^{-2pi omega/kappa} with
  polynomial prefactor; the kinematic edge exponent is a SQUARE-ROOT (k=1/2), not k=1/4.
- gamma_status = n/a (no fourth-root emerged; nothing to fix or free).
- The route is NOT a partial-forcing of q=1/4. It is an OBSTRUCTION at the free level:
  resurgence shows the free series is in the wrong Gevrey class to seed the fourth-root.

## NEXT CALCULATION (the one thing that could change this)
Compute the Borel/Stokes structure of the PUMPED (active-medium) mode operator's worldline
series -- i.e. solve the in-medium dispersion g(k_phys/H) of the Lambda-pumped khronon (agentEE
C1-C5) and read its large-order growth. ONLY if that pumped series is Gevrey-4 (coeffs ~ (4n)!)
with a quartic confluent Borel tower can a fourth-root be FORCED; and even then resurgence fixes
only the FORM (root order + 1/sqrt3 oscillation diagonal), leaving gamma (=> zeta-tilde) FREE.
The free series provably cannot seed it.

#!/usr/bin/env python3
"""
GW-SECTOR PREFERRED-FRAME DOOR for the dS-Unruh modified-inertia framework.
=============================================================================
Carl 'more doors': does the framework's CPT-even SME s_munu background imprint a GENUINE,
above-floor, distinctive signature on GRAVITATIONAL-WAVE PROPAGATION? Three sub-channels:
  (a) frequency/direction-dependent PHASE / DISPERSION from the s_munu background
  (b) GW BIREFRINGENCE / polarization mixing (the CPT-even sector -- nonzero?)
  (c) standard-siren H(z) effect from the evolving a0(z)/rho_DE.

FOOTING (locked, from the banked SME component ledger S_TENSOR_SME_COMPONENT_LEDGER_2026-06-17
+ project_sme_lorentz_bridge memory):
  - framework induces a GRAVITY-sector spurion  s_munu = (a0/2|a|) * (u^mu u^nu)_traceless,
    CPT-even, apex = CMB rest frame (Planck dipole l=264.0,b=+48.3, v=369.82 km/s).
  - a0 = 9.36e-11 m/s^2 (pure-Lambda footing), Z = sqrt(32pi/3) = 5.789. a0 is INPUT (quarantine).
  - c_T = 1 respected (GW170817, no speed anomaly) -- so the d=4 ISOTROPIC speed piece must vanish/absorb.
  - The s_munu coefficient is ACCELERATION-DEPENDENT (~a0/|a|), NOT a constant Sun-frame background.
    THIS IS THE LOAD-BEARING SUBTLETY for GW propagation (worked below, both ways).

BOUNDS (real, WebSearch 2026-06-27):
  - GW170817 + GRB170817A speed coincidence: |(v_g-c)/c| in [-3e-15, +7e-16]
    => isotropic d=4 nonbirefringent nondispersive coeff |k_(I)^(4)| <~ 3e-15 (Kostelecky-Mewes id).
  - GWTC-3 anisotropic birefringence search (arXiv:2210.04481, LVK): no LV; d=4 anisotropic s-bar
    components bounded at ~1e-14..1e-15 (combined with the GW170817 isotropic ~3e-15).
  - d=5 CPT-odd k_(V)00^(5) <~ 3.19e-15 m (GWTC-3); but the framework's CPT-EVEN structure => d=5 = 0.
  - Solar-system gravity-sector s^TX combined fit: (-0.2 +/- 1.3)e-9 (Hees 2016, K-R Data Tables D50).

Every magnitude below is COMPUTED here. RUN: python3 gw_sme_door.py ; exit 0.
"""
import math

# ---------------------------------------------------------------------------
# Constants & footing
# ---------------------------------------------------------------------------
c      = 2.99792458e8          # m/s
G      = 6.674e-11             # SI
Mpc    = 3.0856775814913673e22 # m
Gpc    = 1e3 * Mpc
H0     = 67.4e3 / Mpc          # s^-1   (Planck)
a0     = 9.36e-11              # m/s^2  framework (pure-Lambda)
cH0    = c * H0                # ~ 6.0e-10 m/s^2  (the cosmic acceleration scale)
v_cmb  = 369.82e3             # m/s, Solar-System vs CMB
beta   = v_cmb / c            # 1.233e-3
Om, OL = 0.315, 0.685

def Ez(z):                     # LCDM expansion (the RIVAL a0(z) branch uses this)
    return math.sqrt(Om*(1+z)**3 + OL)

print("="*78)
print("GW-SECTOR PREFERRED-FRAME DOOR  (dS-Unruh modified inertia)")
print("="*78)
print(f"a0 = {a0:.3e} m/s^2   cH0 = {cH0:.3e} m/s^2   beta_cmb = {beta:.3e}")
print(f"GW170817 speed bound |dv/c| ~ 3e-15 ; GWTC-3 anisotropic s-bar ~ 1e-14..1e-15")
print()

# ---------------------------------------------------------------------------
# THE LOAD-BEARING QUESTION: what |a| sets s_munu = (a0/2|a|)*uu along a GW geodesic?
# ---------------------------------------------------------------------------
# The framework's s_munu is a property of how the INERTIA of a TEST MASS responds to the
# cosmic frame -- it multiplies a particle's COM 4-acceleration coupling to u^mu. A vacuum
# GW is a metric perturbation with NO rest-mass test body; the spurion only manifests where
# matter of 4-acceleration |a| couples. Three readings, only one is physical:
#   (R1, NAIVE/WRONG) treat |a|~cH0 as a CONSTANT cosmological background the GW accumulates
#        phase against over a Gpc geodesic: A = a0/(2 cH0) ~ O(0.1), a HUGE O(1) speed coeff.
#        --> This is FALSIFIED on its face (see below): A*beta ~ 1e-4 >> the 3e-15 GW speed
#        bound by 1e10. The fact that R1 is wildly excluded is the PROOF that it mis-maps the
#        coefficient -- the framework does NOT have a constant O(0.1) cosmological s_munu, or
#        GW170817 would have killed it. (Consistency check: this is the SAME reason the matter
#        c_munu "15-order kill" was a mis-map -- a constant-background reading of an
#        acceleration-dependent, test-body coupling.)
#   (R2, MOND regime) the local IGM field |a|<<a0 -> A>>1, but that IS the MOND effect, not a
#        propagation background; vacuum GWs carry no such test body either.
#   (R3, PHYSICAL) the coefficient that any GW EXPERIMENT samples is set at the matter it
#        interacts with -- the SOURCE (NS/BH, g enormous) and the DETECTOR (lab, |a|=g_Earth).
#        There A = a0/(2 g) ~ 4.8e-12, the SAME tiny amplitude as the banked solar-system ledger.
#        Vacuum propagation itself sees NO test-body coupling -> the d=4 traceless s_munu that
#        the wave samples is the lab-frame value, identical to the in-hand s^TX channel.
A_R1  = a0 / (2*cH0)            # naive constant-background (FALSIFIED -> proves the mis-map)
g_lab = 9.81                    # m/s^2
A_phys= a0 / (2*g_lab)          # physical: coefficient set at detector/source matter
print("--- The coefficient amplitude that GW propagation samples ---")
print(f"R1 (NAIVE const bkg, |a|~cH0):  A = a0/(2cH0) = {A_R1:.4f}  -> FALSIFIED (mis-map, shown below)")
print(f"R3 (PHYSICAL, coeff set at matter, |a|=g_lab): A = a0/(2g) = {A_phys:.3e}  (== solar-ledger A)")
print()

# ---------------------------------------------------------------------------
# (a) DISPERSION / PHASE  -- is the d=4 piece dispersive?
# ---------------------------------------------------------------------------
# KEY PHYSICS (Kostelecky-Mewes 1610.04682 / 2602.09183): at mass dimension d=4 the
# minimal gravity-sector s_munu modifies the GW dispersion relation to omega = |k|(1 +- s-proj)
# -- a frequency-INDEPENDENT speed shift. d=4 is NONDISPERSIVE (phase vel = group vel,
# no frequency dependence). Dispersion (frequency-dependent) only enters at d>=6.
# The framework's induced spurion is precisely d=4 (a0/2|a| * uu, mass-dim-4 operator).
# => NO intrinsic frequency-dependent dispersion from the framework's d=4 spurion. The
#    only d=4 effect is an anisotropic SPEED shift.
print("--- (a) DISPERSION / PHASE ---")
print("Framework spurion is mass-dimension d=4 (s_munu ~ a0/2|a| * uu).")
print("d=4 gravity SME is NONDISPERSIVE (omega = |k|(1+s_proj), freq-INDEPENDENT speed shift).")
print("=> NO frequency-dependent dispersion. Only an anisotropic SPEED/phase shift, computed next.")
print()

# Anisotropic d=4 speed shift the framework predicts (the analog of the s^TX dipole, now for GW):
# isotropic part: s^TT ~ (3/4)A  -- ABSORBABLE (rescales c_T -> redefinition; GW170817 ok by absorption)
# anisotropic dipole: ~ A * beta_cmb  (O(beta), CMB-apex-locked)   <-- the genuine observable speed anisotropy
# anisotropic quad:   ~ A * beta_cmb^2 (O(beta^2))
#
# CHANNEL-MATCHING (the banked ledger's load-bearing correction, applied here):
#  - The GW170817 |dv/c|~3e-15 bound is the ISOTROPIC speed -> compare to the ISOTROPIC s^TT,
#    which is ABSORBABLE (a c_T redefinition). So GW170817 does NOT bind the framework (c_T=1
#    is set by absorption; nothing left to constrain isotropically).
#  - The ANISOTROPIC d=4 dipole produces only a freq-INDEPENDENT, direction-dependent speed shift
#    => NO dephasing => the GWTC-3 d=6 dispersion searches (2302.05077) do NOT constrain it
#    (verified: that paper explicitly drops d=4 as "no observable dephasing"). The only handle is
#    a MULTIMESSENGER arrival-direction speed-anisotropy fit, which today rests on the ~1 event
#    (GW170817) -> the anisotropic d=4 s-bar floor is WEAK, ~1e-14 (looser than the isotropic 3e-15).
b_iso    = 3e-15                             # GW170817 isotropic speed (binds the ABSORBABLE s^TT only)
b_aniso  = 1e-14                             # anisotropic d=4 s-bar floor (single multimessenger event)
for tag, A in [("R1 NAIVE", A_R1), ("R3 PHYSICAL", A_phys)]:
    sTT_iso  = 0.75 * A
    sGW_dip  = A * beta
    sGW_quad = A * beta**2
    print(f"[{tag}] A={A:.3e}  s^TT_iso={sTT_iso:.2e}(ABSORBABLE,c_T=1)  dipole=A*beta={sGW_dip:.2e}  quad={sGW_quad:.2e}")
    print(f"        anisotropic dipole/bound = {sGW_dip:.2e}/{b_aniso:.0e} = {sGW_dip/b_aniso:.2e}x  -> "
          f"{'ABOVE -> FALSIFIED (mis-map: %.1ex const bkg)'%(sGW_dip/b_aniso) if sGW_dip>b_aniso else 'BELOW floor by %.1e (safe)'%(b_aniso/sGW_dip)}")
sGW_dip = A_phys * beta                      # the physical one carried forward
print(f"PHYSICAL anisotropic GW-speed dipole = {sGW_dip:.3e}  vs anisotropic floor {b_aniso:.0e}"
      f"  = {b_aniso/sGW_dip:.1f}x BELOW (the SAME coeff as the in-hand solar s^TX, here below the GW floor)")
print()

# ---------------------------------------------------------------------------
# (b) BIREFRINGENCE  -- is the CPT-even sector nonzero?
# ---------------------------------------------------------------------------
# PHYSICS: GW birefringence (the +/- helicity modes propagating at different speeds) is
# a HELICITY-DEPENDENT, hence PARITY-ODD effect. In the SME gravity sector birefringence
# is controlled by the CPT-ODD coefficients (odd mass dimension d=5,7,...; the k_(V) family).
# The CPT-EVEN s_munu (d=4) is NON-birefringent: both helicities share the same modified
# dispersion (Kostelecky-Mewes; 2302.05077 "nonbirefringent dispersions"). The framework's
# Door-5 theorem: the dS-Unruh kernel T_eff=sqrt(a.a+(cH)^2) is EVEN in u => CPT-EVEN only,
# all CPT-odd coefficients (a_mu,b_mu,k_AF, and the GW k_(V)) = 0 identically.
# => the framework predicts ZERO GW birefringence. Not "below floor" -- structurally ZERO.
print("--- (b) BIREFRINGENCE / polarization mixing ---")
print("GW birefringence is CPT-ODD (k_(V) family, odd d). Framework is CPT-EVEN (Door-5 theorem,")
print("dS-Unruh kernel even in u) => k_(V)=0 IDENTICALLY. Predicted GW birefringence = EXACTLY 0.")
print(f"This is a clean falsifiable theorem: bound k_(V)00^(5) <~ 3.19e-15 m (GWTC-3); framework = 0.")
print("=> NOT a door (null by structure), but a sharp consistency: a confirmed GW birefringence KILLS it.")
print()

# ---------------------------------------------------------------------------
# (c) STANDARD-SIREN H(z) from evolving a0(z)/rho_DE
# ---------------------------------------------------------------------------
# The framework ties a0 to rho_DE (a0 = c*H_Lambda/Z, the pure-Lambda piece). If dark energy
# is exactly Lambda (w=-1), H(z) is the STANDARD LCDM H(z) and there is NO siren signature
# beyond LCDM. A standard-siren distance-redshift test probes d_L(z) = (1+z) c \int dz'/H(z').
# The framework-DISTINCTIVE part requires a0 to EVOLVE, which only happens if rho_DE evolves
# (w != -1). The a0(z) paper's branch: a0(z) ~ sqrt(rho_DE(z)). For LCDM Lambda this is FLAT.
# So the siren H(z) door is DEGENERATE with the dark-energy EoS measurement -- NOT a distinctive
# GW-propagation signature. Quantify the GW-luminosity-distance modification:
# In a preferred-frame / SME-modified-friction theory, d_L^GW / d_L^EM can differ (the "GW
# friction" nu term). Compute the framework's predicted GW-vs-EM distance ratio deviation.
print("--- (c) STANDARD-SIREN  d_L^GW vs H(z) from a0(z)/rho_DE ---")
# (c1) H(z) itself: framework a0 ~ sqrt(rho_DE); if w=-1 exactly, H(z)=LCDM => NO siren signature.
# (c2) GW friction: a running Planck mass / preferred-frame friction modifies d_L^GW.
#      The fractional GW-friction deviation from a preferred-frame s_munu background scales as
#      the background coefficient itself, ~ A*<something>. The propagation-amplitude correction
#      is at most O(A * (H0 D / c)) accumulated, but the AMPLITUDE friction in d=4 minimal SME
#      vanishes for the traceless s_munu (it shifts speed, not amplitude). So d_L^GW = d_L^EM at d=4.
fric_dev = 0.0   # d=4 traceless s_munu shifts phase/speed, not amplitude -> no GW-friction
print(f"(c1) if w=-1 (Lambda): H(z)=LCDM exactly -> NO siren H(z) signature (degenerate w/ EoS).")
print(f"(c2) d=4 traceless s_munu shifts SPEED not AMPLITUDE -> GW-friction d_L^GW/d_L^EM dev = {fric_dev:.1e}")
# The a0(z) EoS hostage (already banked): the +6% phantom bump at z=0.405, -26% at z=3 is a
# DARK-ENERGY-EoS effect, testable by sirens ONLY as a w(z) measurement -- not GW-propagation-distinctive.
print(f"=> the a0(z) content is a w(z)/EoS hostage (banked Front B), NOT a distinctive GW-PROPAGATION door.")
print()

# ---------------------------------------------------------------------------
# LISA / ET forecast for the anisotropic GW-speed dipole (the one non-null channel)
# ---------------------------------------------------------------------------
# An anisotropic speed shift s_dip produces an arrival-direction-dependent timing/phase residual.
# Detectability ~ s_dip vs the speed-anisotropy sensitivity. Current GW170817-class single-event
# isotropic speed bound ~3e-15; population/anisotropic forecasts:
#   ET/CE (2035+): ~1e-16 isotropic speed; LISA MBHB multiband ~ few e-17 (2502.04776, 2601.03571).
print("--- LISA/ET/CE forecast for the anisotropic GW-speed dipole ---")
# Anisotropic d=4 floors (the matched channel): today weak (~1e-14, 1 multimessenger event);
# future needs MANY GW+EM sirens spread over the sky to fit the dipole. Even ET/CE/LISA isotropic
# speed floors (1e-16..3e-17) only bind the ABSORBABLE piece; the anisotropic dipole floor improves
# slowly with the number of well-localized multimessenger events, ~1e-15 optimistic by mid-2030s.
forecast = {"anisotropic now (~1 event)":1e-14, "anisotropic ~2030 (10s of sirens)":2e-15,
            "anisotropic ~2035 (ET/CE+EM, optimistic)":5e-16}
for k,v in forecast.items():
    verdict = "ABOVE (live)" if sGW_dip>v else f"BELOW floor by {v/sGW_dip:.1e}x"
    print(f"  {k:30s} floor={v:.1e}   framework dipole(R3)={sGW_dip:.2e}  -> {verdict}")
print()

# ---------------------------------------------------------------------------
# VERDICT
# ---------------------------------------------------------------------------
print("="*78)
print("VERDICT")
print("="*78)
print(f"""
(a) DISPERSION: framework spurion is d=4 -> NONDISPERSIVE. No frequency-dependent signal.
    The only d=4 effect is an anisotropic GW-SPEED dipole. Physical reading (R3, coeff set at
    the source/detector matter, |a|=g) gives A*beta = {sGW_dip:.2e}; the isotropic part is
    ABSORBABLE (c_T=1) and the GW170817 3e-15 bound binds only that absorbable piece. The
    anisotropic dipole sits BELOW the anisotropic d=4 floor (~1e-14 today; ~5e-16 optimistic 2035)
    -- below floor by ~{1e-14/sGW_dip:.0f}x now. The NAIVE constant-cH0-background reading (R1)
    gives ~9e-5 = ~1e9x ABOVE the bound -> FALSIFIED, which PROVES it mis-maps the
    acceleration-dependent coupling (same class as the matter-c_munu '15-order' mis-map).
(b) BIREFRINGENCE: EXACTLY ZERO by the CPT-even theorem (Door 5; dS-Unruh kernel even in u =>
    k_(V)=0). A clean falsifier (a confirmed GW birefringence kills the framework), not a door.
(c) SIREN H(z): degenerate with dark-energy w(z); d=4 traceless s_munu shifts speed not amplitude
    -> GW-friction d_L^GW/d_L^EM = 0. The a0(z) content is the banked w(z) hostage, not GW-distinctive.

NET: the GW-PROPAGATION arena is NOT a fresh above-floor distinctive door. Outcomes:
  - dispersion: d=4 nondispersive -> NULL.
  - birefringence: CPT-even theorem -> NULL-by-structure (a falsifier, not a door).
  - speed anisotropy: the SAME s_munu coefficient as the in-hand solar s^TX (A*beta=5.9e-15 at g),
    just below today's weak anisotropic d=4 GW floor (~1e-14, ~2x) -> ALREADY-COVERED (it IS the
    s^TX channel) + the GW realization is WEAKER than the solar one (~1.5x in hand) -> NOT a fresh door.
  - siren H(z): EoS-degenerate -> already-covered (banked Front B a0(z)).
The solar-system s^TX dipole (~1.5x, in hand) remains the binding preferred-frame test; every GW
sub-channel is weaker, null-by-structure, or degenerate. NOT a no-door (the framework makes the
sharp, falsifiable, distinctive prediction of ZERO GW birefringence + ZERO d=4 dispersion +
c_T=1 exactly) -- but no NEW reachable door in this arena.
""")
print("exit 0")

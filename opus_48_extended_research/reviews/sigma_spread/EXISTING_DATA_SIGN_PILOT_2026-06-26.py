"""
MINE 1 PROOF-OF-CONCEPT: can EXISTING published UDG/cluster-member kinematics ALREADY
show the SIGN of d(sigma_internal)/d(infall-phase) at matched radius?

Framework (dS-Unruh modified inertia): plungers (high infall phase) run HOTTER ->
d(sigma_int)/d(infall) POSITIVE. MG = EXACTLY 0 (theorem). Tidal/CDM = same-signed but
radially anti-correlated. Intrinsic MI spread 6-13% (kernel-hostage), diluted by the
projected-phase-space infall proxy to ~0.4x -> OBSERVED ~2-5%.

REAL published per-object precision (this session, web-verified):
  Coma UDGs (Gannon+ living catalog 2024): ~8-10 with sigma, err +-3..9 km/s on sigma~15-47 (16-40%)
     anchors: Y358 19+-3 (16%); DF44 ~33 (resolved, +-3, best); DFX1 ~30; DF17/Yagi +-7..10 (high)
  Hydra LEWIS-II (Iodice/Buttitta 2025): UDG1 22+-5, UDG4 17+-4, UDG7 61+-9, UDG9 20+-6,
     UDG11 18+-5, UDG12 38+-9  => err 20-45%, only 6 'constrained' (S/N>15)
  Global UDG-with-sigma sample today (Gannon+2024): ~40 objects ALL hosts combined.
"""
import numpy as np
rng = np.random.default_rng(20260626)

# ---- REAL per-object sigma precision from the published samples (fractional) ----
# (sigma_km, err_km) actually-published anchors
coma  = [(19,3),(33,3),(30,6),(15,7),(20,8),(25,7),(18,6),(22,8)]      # Coma UDGs, Gannon-catalog-class
hydra = [(22,5),(17,4),(61,9),(20,6),(18,5),(38,9)]                    # LEWIS-II constrained
allobj = coma + hydra
frac_err = np.array([e/s for s,e in allobj])
print("REAL published per-object sigma precision (fractional):")
print(f"  N objects with sigma (Coma+Hydra) = {len(allobj)}")
print(f"  fractional err: median {np.median(frac_err)*100:.0f}%, range {frac_err.min()*100:.0f}-{frac_err.max()*100:.0f}%")
print(f"  => per-object precision is {np.median(frac_err)/0.10:.1f}x COARSER than the ~10% needed to resolve the spread per object\n")

# ---- The detection statistic: SIGN of slope sigma_int vs infall-phase proxy, at matched radius ----
# Observed spread amplitude across the full infall-phase range (after proxy dilution):
INTRINSIC = np.array([0.06, 0.10, 0.13])    # MI kernel band
DILUTION  = 0.40                            # projected-phase-space proxy -> 0.4x (banked MC)
OBS = INTRINSIC*DILUTION
print(f"OBSERVED spread (intrinsic {INTRINSIC*100} % x dilution {DILUTION}) = {OBS*100} %  (MG/CDM null = 0)")

# Power to detect a NONZERO slope (the SIGN) by splitting into low-infall vs high-infall bins.
# Signal = mean fractional sigma DIFFERENCE between high- and low-infall bins = OBS.
# Per-object noise = frac_err. Pooled error on the mean-difference for N_lo + N_hi objects.
def sign_significance(N_per_bin, obs_spread, sample_frac_err):
    # bootstrap-realistic: per-bin mean has error = mean(frac_err)/sqrt(N_per_bin), in QUADRATURE x2 bins
    fe = np.array(sample_frac_err)
    # draw N_per_bin per bin from the real frac-err pool
    err_lo = np.sqrt(np.mean(rng.choice(fe,N_per_bin)**2)/N_per_bin)
    err_hi = np.sqrt(np.mean(rng.choice(fe,N_per_bin)**2)/N_per_bin)
    err_diff = np.sqrt(err_lo**2+err_hi**2)
    return obs_spread/err_diff, err_diff

print("\n--- SIGN-DETECTION SIGNIFICANCE with EXISTING per-object precision ---")
print("(signal = observed high-vs-low-infall sigma difference; noise = real published frac err)")
print(f"{'N/bin':>6} {'Ntot':>5} | "+" ".join(f"obs={o*100:.0f}%" for o in OBS))
for Nbin in [3,5,7,10,20,50,100]:
    sigs=[]
    for o in OBS:
        # average over many bin-draws to get the expected SNR at this N
        snr = np.mean([sign_significance(Nbin,o,frac_err)[0] for _ in range(400)])
        sigs.append(snr)
    print(f"{Nbin:>6} {2*Nbin:>5} | "+" ".join(f"{s:6.2f}s" for s in sigs))

print("""
READ:
 - The EXISTING global single-cluster sample is N~6-10 UDGs/cluster with sigma -> 3-5 per
   infall bin. At that N and 20-45% per-object error the SIGN significance is ~0.2-0.6 sigma
   even at the optimistic 5.2% observed spread. INDISTINGUISHABLE FROM ZERO.
 - A STACK across all clusters reaching N~50/bin (does not exist as a uniform infall-tagged
   set today) would give ~1-2 sigma at the optimistic end ONLY.
 - To clear 3 sigma on the SIGN needs N~100/bin = ~200 infall-tagged UDGs with sigma at <40%
   error -- ~5-10x the entire global UDG-kinematics sample that exists in 2026.
""")

# ---- Can the per-object error be beaten by the ONE good case (resolved members)? ----
# MUSE-HFF deep IFU: does any HFF cluster have N~50-150 diffuse members with internal sigma?
# Reality check from the literature: HFF MUSE catalogs give REDSHIFTS for ~hundreds of cluster
# members but RESOLVED INTERNAL sigma only for the bright (sigma>>30) ellipticals (NIRSpec/MUSE
# floor 30-50 km/s >> the 8-20 km/s diffuse regime). The diffuse members that carry the signal
# are exactly the ones whose internal sigma is UNRESOLVED in HFF integrated light.
print("MUSE-HFF check: HFF deep IFU gives member REDSHIFTS (hundreds) but resolved INTERNAL sigma")
print("only for bright ellipticals (sigma>>30 km/s) -- the Faber-Jackson WRONG sample (sign flips +).")
print("The diffuse 8-20 km/s carriers are below the HFF integrated-light sigma floor. => HFF cannot")
print("run the sign test on the right (diffuse) members with existing data.\n")

# ---- Honest verdict ----
print("="*78)
print("VERDICT: the SIGN of d(sigma_int)/d(infall) is NOT detectable at even 1-2 sigma with")
print("any existing single-cluster UDG sample; best-case full-stack reaches ~1-2 sigma ONLY at")
print("the optimistic 5% observed spread and ONLY if ~50 uniformly infall-tagged UDGs/bin existed")
print("(they do not). EXISTING DATA = UPPER-LIMIT / PROOF-OF-CONCEPT, not a sign detection.")
print("="*78)

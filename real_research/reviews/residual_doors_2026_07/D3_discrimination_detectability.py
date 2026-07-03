#!/usr/bin/env python3
r"""
D3 LANE, TASKS 3+4 -- DISCRIMINATION POWER + DETECTABILITY (honest, both ways).
================================================================================
Question: can the unsettled-population transient be told apart from
 (a) ordinary tidal heating, (b) MG/AeST (exactly zero relational effect),
 (c) plain MOND-MI without the transient/memory piece (instantaneous mu(y))?

DISCRIMINATION TABLE (rows = observables; entries = predicted signal):
                              MI+transient      MI-only(instant)  MG/AeST     LCDM+tides
 1 sigma excess at fixed        +10..30% (post-     0                0          + (grows toward
   current a_ext,mass,rh        peri carriers)                                  SMALL r_peri)
 2 time-since-peri decay        EXP tau=0.45Gyr     --               --         NO decay
   (hysteresis direction)       (excess DECAYS)                                 (heat PERSISTS)
 3 sign on FIRST INFALL         DEFICIT (-10..20%)  0                0          0 or + (pre-
   (pre-peri, y rising)         SIGN FLIP at peri                               processing heats)
 4 density gate (dense,         NULL (Leo I ~0)     0                0          + (tides don't
   high-ecc object)                                                             care re density)
 5 late tail n_orb>2            POWER LAW 1/n,      0                0          persists/grows
                                +0.4..2% (chL)
CLEANEST SINGLE COMPARISON: matched-pericentre, matched-density PAIR (or triple)
differing only in ORBITAL PHASE: pre-peri member (predicted COLD, deficit) vs
recent post-peri (predicted HOT, excess) vs long-post-peri (predicted settled).
Tides predict monotone heating with NO sign flip and NO decay; MG predicts three
IDENTICAL sigmas. The SIGN FLIP + EXPONENTIAL DECAY pair is MI-unique.

DETECTABILITY (computed below): required sigma_v precision + sample size vs
Gaia DR4 (Dec 2026: full PMs -> phases + in/out branch), WEAVE/4MOST (sigma to
0.2-0.5 km/s for diffuse dwarfs; CHANCES 150 clusters 2028-2031), Rubin (new
diffuse satellites + infall morphologies), ELT (~2031+: crowd-field sigma at
M31). Exit 0 = all assertions hold.
"""
import math

# ---------- channel M (the fused memory signal, carriers) ----------
S_M=(0.06,0.13,0.27)     # relational excess band: cluster band 6-13%; CraterII-like up to 27%
# ---------- channel L alone (the genuinely NEW piece of this lane) ----------
S_L=(0.004,0.02)         # sigma-level 0.4% (n=10) .. 2% (n=2) power-law tail

print("="*100)
print(" D3 TASKS 3+4: discrimination + detectability (numbers below back the table in the docstring)")
print("="*100)

# per-object errors today and funded:
# Crater II sigma=2.7+-0.3 (11%); WEAVE/4MOST-era diffuse dwarfs ~0.2-0.3 km/s on 3-6 km/s -> 5-8%
# binaries floor after multi-epoch: ~3-5% on sigma~3 km/s systems.
def N_needed(signal, err_per_obj, nsig=3.0):
    """objects per arm (carrier vs matched control), two-arm comparison."""
    return math.ceil(2*(nsig*err_per_obj/signal)**2)

print("\n A) CHANNEL M (memory transient == the banked sigma-spread front, now phase-resolved):")
for err,era in [(0.11,"today (CraterII-grade, 11%/obj)"),(0.07,"DR4+WEAVE/4MOST 2027-29 (7%/obj)"),
                (0.05,"deep follow-up 2029-31 (5%/obj)")]:
    for s in S_M:
        print(f"   signal {s*100:4.1f}%  err {err*100:4.0f}%/obj [{era}]: N/arm(3sig)={N_needed(s,err):4d}")
# carriers available: MW diffuse-eccentric dwarfs with DR4 phases ~10-20 (Pace+22 class);
# cluster members: WEAVE WWFCS thousands/cluster, CHANCES >1000/cluster x150.
n_carriers_MW=(10,20)
sM_mid=0.10; err=0.07
Nreq=N_needed(sM_mid,err)
print(f"   -> MW-dwarf arm: need {Nreq}/arm at 10% signal; DR4-era carriers ~{n_carriers_MW} => "
      f"{'DECISIVE' if Nreq<=n_carriers_MW[1] else 'MARGINAL'} ~2029-2030 (3sig).")
assert Nreq<=n_carriers_MW[1]
# cluster arm (banked): CHANCES-scale already exceeds statistical need; systematics-limited
sC=0.06; errC=0.02   # stacked bin dispersion error at N~1000/bin: 1/sqrt(2N)~2%
print(f"   -> cluster arm: 6% signal vs {errC*100:.0f}% bin error -> {sC/errC:.0f} sigma statistical by CHANCES "
      f"(2028-2031); PURITY/tides systematics take over (banked separator: radial trend + hysteresis + SIGN FLIP).")
assert sC/errC>=3

print("\n B) CHANNEL L ALONE (the 1/n tail -- what THIS lane adds beyond the banked front):")
for s in S_L:
    for err in (0.05,0.02):
        print(f"   signal {s*100:4.1f}%  err {err*100:3.0f}%/obj: N/arm(3sig)={N_needed(s,err):7d}")
Ntail=N_needed(0.01,0.05)
print(f"   -> separating chL from chM needs matched-y_eff samples at n_orb=2-10 with ~1% signal:"
      f" N/arm ~{Ntail} diffuse carriers per n_orb bin. NOT AVAILABLE from any funded survey through ~2036.")
assert Ntail>400
print("   VERDICT ON chL: real, sign-locked (+), power-law -- and UNOBSERVABLE FOR AT LEAST A DECADE.")
print("   Its only near-term role: a ~+2..15% (envelope) top-up on sub-orbit carriers (CraterII), which")
print("   slightly STEEPENS the predicted phase-decay curve vs memory-only MI; not separately testable yet.")

print("\n C) INSTRUMENT/YEAR LADDER (3-sigma decisive dates, honest):")
print("   2026-12 Gaia DR4: orbital phases + in/out branch for all MW satellites -> classify carriers,")
print("            find first-infall (sign-flip) candidates. (Enables, does not decide.)")
print("   2027-29 WEAVE WWFCS + 4MOST: dwarf sigmas to 5-8% + cluster infall/virialized bins ->")
print("            MW-dwarf matched-phase test 3sig ~2029-2030; cluster relational spread 3sig 2028-2031.")
print("   2029-31 Rubin: new diffuse satellites (bigger carrier arm), tidal-tail vetoes.")
print("   2031+   ELT: M31 diffuse-satellite sigmas -> second, independent host.")
print("   >2036   chL 1/n tail on its own: underpowered for a decade -- SAID PLAINLY.")

print("\nALL ASSERTIONS PASSED (D3 discrimination+detectability)")

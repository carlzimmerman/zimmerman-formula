#!/usr/bin/env python3
"""
Does the BOSS parity-odd 4PCF "2/2 confirmed" actually test anything?
====================================================================

proper_parity_odd_4pcf_analysis.py reports "BOSS DATA CONSISTENT WITH T3/Z2
TOPOLOGY, score 2/2". This script loads the SAME data and asks whether the two
passing tests carry any evidential weight. Verdict up front: they do not. The
analysis computes no covariance matrix, no mock-based null, and no significance
for parity violation -- so it cannot establish one. Its two "confirmed"
predictions are (1) trivially true for any data and (2) a shared-shape feature
expected in standard LCDM with NO topology.

Pure stdlib + numpy. Run:  python reviews/parity_odd_4pcf_nulltest.py
"""

import numpy as np
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / \
    "research/offensive_campaign/Parity-Odd-4PCF/data"


def load_cap(fname):
    lines = [l for l in open(fname) if not l.startswith('#')]
    l1 = np.array([int(x) for x in lines[0].split()])
    l2 = np.array([int(x) for x in lines[1].split()])
    l3 = np.array([int(x) for x in lines[2].split()])
    zeta = np.array([[float(x) for x in ln.split()][3:] for ln in lines[3:]])
    odd = (l1 + l2 + l3) % 2 == 1
    return zeta[:, odd], (l1[odd], l2[odd], l3[odd])


def main():
    ngc_f = DATA / "boss_cmassN.zeta_4pcf.txt"
    sgc_f = DATA / "boss_cmassS.zeta_4pcf.txt"
    if not ngc_f.exists():
        print(f"Data not found at {DATA} -- run the original script first.")
        return
    ngc, (l1, l2, l3) = load_cap(ngc_f)
    sgc, _ = load_cap(sgc_f)
    print("=" * 78)
    print(f"Loaded odd-parity 4PCF: NGC {ngc.shape}, SGC {sgc.shape} "
          f"(bin-triplets x multipoles)")
    print("=" * 78)

    print("\n(TEST 1) 'Parity-odd signal exists' = mean(|zeta|) > 0")
    print("-" * 78)
    m = np.mean(np.abs(ngc))
    print(f"  mean(|zeta_odd|) = {m:.3e} > 0  -> PASS")
    print("  But this is mean of ABSOLUTE values: it is > 0 for ANY non-zero array.")
    print("  Pure Gaussian noise passes identically. Evidential content: ZERO.")
    # demonstrate on noise
    noise = np.random.normal(size=ngc.shape)
    print(f"  (same test on random noise: mean(|noise|) = {np.mean(np.abs(noise)):.3f}"
          f" > 0 -> also PASS)")

    print("\n(TEST 2) 'Globally coherent' = corr(NGC_flat, SGC_flat) > 0.5")
    print("-" * 78)
    raw = np.corrcoef(ngc.flatten(), sgc.flatten())[0, 1]
    print(f"  raw flattened correlation = {raw:.3f}  -> PASS (the script's headline)")
    print("  Decompose WHERE that correlation lives:")

    # (a) mode concentration: how much power is in the top few multipoles?
    power = np.mean(((ngc + sgc) / 2) ** 2, axis=0)
    order = np.argsort(power)[::-1]
    tot = power.sum()
    cum = np.cumsum(power[order]) / tot
    print(f"  * power concentration: top mode = {power[order][0]/tot*100:.0f}% of all"
          f" odd power; top 3 = {cum[2]*100:.0f}%; top 5 = {cum[4]*100:.0f}%.")
    top = order[0]
    print(f"    the single dominant multipole is (l1,l2,l3)="
          f"({l1[top]},{l2[top]},{l3[top]}). 'Global coherence' is a FEW modes, not 60.")

    # (b) envelope vs fluctuation: correlate per-multipole RMS envelopes
    rms_n = np.sqrt(np.mean(ngc ** 2, axis=0))
    rms_s = np.sqrt(np.mean(sgc ** 2, axis=0))
    env_corr = np.corrcoef(rms_n, rms_s)[0, 1]
    print(f"  * envelope correlation (per-multipole RMS, NGC vs SGC) = {env_corr:.3f}")
    print("    -> the agreement is the SHARED SHAPE of the 4PCF, which both caps have")
    print("       because both measure the SAME LCDM cosmology -- with or without")
    print("       topology. This is expected in a parity-CONSERVING universe.")

    # (c) z-score each multipole (remove envelope), re-correlate the fluctuations
    def zscore(a):
        mu, sd = a.mean(0), a.std(0)
        sd[sd == 0] = 1
        return (a - mu) / sd
    zcorr = np.corrcoef(zscore(ngc).flatten(), zscore(sgc).flatten())[0, 1]
    print(f"  * correlation of fluctuations after removing per-multipole envelope:"
          f" {zcorr:.3f}")
    print("    -> once the shared shape is divided out, the mode-by-mode agreement is"
          f" {'far weaker' if zcorr < 0.7 else 'still present'}.")

    print("\n(THE FATAL GAP) no covariance, no mocks, no null, no significance")
    print("-" * 78)
    print("  * Published parity-odd 4PCF analyses (Hou+22; Philcox 22) estimate the")
    print("    4PCF COVARIANCE from THOUSANDS of mock catalogs, then chi^2 vs the")
    print("    parity-conserving null. This script has NO covariance and NO mocks, so")
    print("    it computes NO p-value for parity violation. Its only 'sigma' (the 1.6")
    print("    asymmetry) uses a naive sqrt(2/N) that is not the (highly non-diagonal)")
    print("    4PCF covariance -- it is not a real significance.")
    print("  * Even the REAL literature is unsettled: Hou+22 got ~7sigma, Philcox 22")
    print("    got ~2.9sigma on the SAME data -- the gap is the covariance-estimation")
    print("    fragility -- and later reanalyses (covariance + look-elsewhere) find the")
    print("    BOSS parity signal is NOT robust / consistent with systematics.")

    print("\n" + "=" * 78)
    print("VERDICT")
    print("=" * 78)
    print("  The '2/2 confirmed' is a NON-result:")
    print("   - Test 1 ('signal exists') is a tautology (|x| > 0).")
    print("   - Test 2 ('global coherence') is the shared LCDM 4PCF shape (envelope")
    print(f"     corr {env_corr:.2f}), expected WITHOUT topology; it is dominated by a")
    print("     couple of multipoles, and it is not a covariance-based significance.")
    print("   - The one distinctive Z2 prediction (axis at 287,9) is 'cannot test'.")
    print("  So BOSS is not shown 'consistent with T3/Z2' in any testable sense here.")
    print("  And it cuts the other way too: IF a real 20.6 Gpc T3/Z2 produced a parity")
    print("  signal, it would ALSO imprint ~42 deg matched circles in the CMB")
    print("  (matched_circle_ghost_location.py) -- which are ABSENT. The two topology")
    print("  'evidences' in the repo contradict each other; the CMB one is decisive.")


if __name__ == "__main__":
    main()

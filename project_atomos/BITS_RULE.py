#!/usr/bin/env python3
"""BITS_RULE.py -- what the informative-ceiling result actually changes about the search.

GATE_POWER_ANALYSIS.py established that N(D) ~ 30^(D-4) outruns any fixed precision past D~10-13, so
all power is in Gate C. That has a sharp consequence the campaign does NOT currently implement:
Gate C should not COUNT targets, it should SUM BITS. Adding a loosely-measured target raises k while
contributing almost no information, so k inflates while surprise does not. The correct threshold is
    SUM_i log2(1/w_i)  >  log2(N(D)) + margin.
This script computes that threshold and prints the pass/fail rule to use when JACKPOT fires.
Local-only project.
"""
import numpy as np
BASE, D0, MARGIN = 30.0, 4, 10.0     # 10 bits ~ 1000:1 safety over the look-elsewhere cost
T = [("m_p/m_e",3.49e-14),("1/alpha",3.06e-10),("m_mu/m_e",4.45e-9),("koide_Q_lep",2.0e-5),
     ("r_tau_mu",1.4e-4),("sin^2 theta_W",3.4e-4),("m_t/m_b",7.0e-3),("alpha_s(M_Z)",1.5e-2)]
bits = lambda w: np.log2(1.0/w)
print("="*92); print("BITS_RULE -- Gate C must sum BITS, not count targets"); print("="*92)
print(f"\n  {'target':<16}{'window w':>13}{'bits':>8}   note")
print("  "+"-"*88)
for n,w in T:
    note = "HELD BACK (validation)" if n in ("koide_Q_lep","r_tau_mu") else ""
    print(f"  {n:<16}{w:>13.2e}{bits(w):>8.1f}   {note}")
print("\n  look-elsewhere cost log2(N(D)) and the bits needed to beat it:\n")
print(f"  {'depth D':>9}{'N(D)':>12}{'cost [bits]':>13}{'needed = cost+margin':>22}")
print("  "+"-"*88)
for D in (10,13,16,18,20):
    N = BASE**(D-D0); cost = np.log2(N)
    print(f"  {D:>9}{N:>12.2e}{cost:>13.1f}{cost+MARGIN:>22.1f}")
cost18 = np.log2(BASE**(18-D0)); need18 = cost18+MARGIN
fit = [(n,w) for n,w in T if n not in ("koide_Q_lep","r_tau_mu")]
fit.sort(key=lambda t: t[1])
print(f"\n  AT THE CAMPAIGN'S DEPTH 18: need > {need18:.1f} bits from FITTABLE targets (holdout excluded).")
run = 0.0
for i,(n,w) in enumerate(fit,1):
    run += bits(w)
    print(f"    interlock {i} ({n:<14}) -> cumulative {run:6.1f} bits   {'PASS' if run>need18 else 'short'}")
kmin = next(i for i,_ in enumerate([sum(bits(w) for _,w in fit[:j]) for j in range(1,len(fit)+1)],1)
            if sum(bits(w) for _,w in fit[:i])>need18)
print(f"""
  => MINIMUM: {kmin} interlocked fittable targets, and only if they are the TIGHTEST ones. The two
     tightest (m_p/m_e + 1/alpha) give only {bits(fit[0][1])+bits(fit[1][1]):.1f} bits and FALL SHORT of {need18:.1f} -- the two most
     precisely measured numbers in physics are NOT enough on their own at depth 18. But {kmin} LOOSE targets
     would not: alpha_s + m_t/m_b + sin^2 theta_W = {bits(1.5e-2)+bits(7.0e-3)+bits(3.4e-4):.1f} bits, FAR short.
  => SO THE RULE CHANGES FROM 'k >= 4' TO A BITS TEST. Counting targets is the wrong statistic:
     three loose targets look like k=3 but carry {bits(1.5e-2)+bits(7.0e-3)+bits(3.4e-4):.1f} bits, while two tight ones carry {bits(fit[0][1])+bits(fit[1][1]):.1f}.
  => AND STOP ESCALATING DEPTH. Each depth costs {np.log2(BASE):.1f} bits of look-elsewhere for free. Depth 18
     already costs {cost18:.1f} bits; depth 20 costs {np.log2(BASE**16):.1f}. Compute is better spent sampling MORE at
     depths 10-14 than reaching depth 19+, because the bits needed rise with D while the available
     target precision is fixed.
JACKPOT READ-OUT RULE: report (a) sum of bits over interlocked fittable targets, (b) log2(N(D)) at the
survivor's depth, (c) the r_tau_mu out-of-sample sigma. Survivor is interesting iff (a) > (b) + 10 AND
(c) < 2. Koide Q passing is NOT evidence (exact 2/3 is 0.91 sigma away and known since 1981).""")
print("="*92)

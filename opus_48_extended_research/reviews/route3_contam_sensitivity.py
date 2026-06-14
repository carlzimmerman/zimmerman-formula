#!/usr/bin/env python3
"""Both-ways sensitivity: how good must DR4 contamination control be to separate fw from MOND?
Avoid manufacturing a deficit — show the f_multi-control level at which the 0.092 gap becomes
detectable, and whether DR4 can plausibly reach it."""
import numpy as np
gamma_FW, gamma_MOND, gamma_NEWT = 1.307, 1.399, 1.000
gap_mond_fw   = gamma_MOND-gamma_FW   # 0.092
gap_fw_newt   = gamma_FW-gamma_NEWT   # 0.307
sig_gext = 0.013
sigconst = 0.155*np.sqrt(36)          # 0.93

print("="*90)
print("BOTH-WAYS: required f_multi control + sample size to reach 3sigma framework-vs-MOND")
print("="*90)
print(f"  gap framework-MOND = {gap_mond_fw:.3f};  to reach 3sigma need sigma_tot < {gap_mond_fw/3:.3f}")
print(f"  But sigma_tot >= sqrt(sig_stat^2 + contam^2 + g_ext^2), and g_ext alone = {sig_gext:.3f}")
print(f"  => need contam floor < sqrt(({gap_mond_fw/3:.3f})^2 - {sig_gext:.3f}^2) = {np.sqrt((gap_mond_fw/3)**2 - sig_gext**2):.3f}")
need_contam = np.sqrt((gap_mond_fw/3)**2 - sig_gext**2)
print(f"  With d gamma/d f_multi ~ 1.0, that means pinning f_multi to +/- {need_contam:.3f}")
print(f"  (i.e. ~{need_contam*100:.0f}% absolute on the triple fraction). DR4 epoch astrometry helps but")
print(f"  the literature current best is +/- ~0.1-0.2 (Banik/Chae disagree by 0.4). So sub-3%")
print(f"  contamination control on f_multi is BEYOND plausible DR4 reach.\n")

print("  Scenario grid (N, contam floor) -> framework-vs-MOND SNR:")
print(f"  {'contam_floor':>13s} | " + " | ".join(f"N={n}" for n in [1000,3000,8000,30000]))
for cf in [0.10, 0.05, 0.03, 0.02, 0.01]:
    row=[]
    for n in [1000,3000,8000,30000]:
        st=sigconst/np.sqrt(n); stot=np.sqrt(st**2+cf**2+sig_gext**2)
        row.append(gap_mond_fw/stot)
    star = "  <- realistic DR4" if cf==0.10 else ("  <- needs sub-% f_multi" if cf<=0.02 else "")
    print(f"  {cf:13.2f} | " + " | ".join(f"{v:5.1f}s" for v in row)+star)

print("\n  Same grid, framework-vs-NEWTON SNR (the DETECTION, not discrimination):")
print(f"  {'contam_floor':>13s} | " + " | ".join(f"N={n}" for n in [1000,3000,8000,30000]))
for cf in [0.10, 0.05, 0.03, 0.02, 0.01]:
    row=[]
    for n in [1000,3000,8000,30000]:
        st=sigconst/np.sqrt(n); stot=np.sqrt(st**2+cf**2+sig_gext**2)
        row.append(gap_fw_newt/stot)
    print(f"  {cf:13.2f} | " + " | ".join(f"{v:5.1f}s" for v in row))

print("\n" + "="*90)
print("VERDICT (both ways)")
print("="*90)
print(f"""  * framework vs NEWTON survives contamination: even at the pessimistic contam=0.10 floor it is
    ~3 sigma at N>=3000, and >=6 sigma if f_multi is pinned to 0.05. The {gap_fw_newt:.2f} super-Newtonian
    signal IS a clean DR4 detection. The lower a0 does NOT blunt this below detectability.
  * framework vs MOND needs f_multi pinned to ~2-3% absolute to reach 3 sigma even at N=30000.
    That is beyond plausible DR4 contamination control. The {gap_mond_fw:.3f} gap is MOND-degenerate.
  * NOT a manufactured deficit: the gap is real and small BECAUSE the lower a0 is real; the
    contamination floor that buries it is the SAME floor that splits Banik(Newton) from Chae(MOND)
    on today's data — an independently-attested, not invented, systematic. Both ways: the wide-binary
    front is a clean DETECTION channel (boosted-vs-Newton) and a NON-DIAGNOSTIC channel for a0
    (framework-vs-MOND), and g_ext is not what limits either — contamination + interp function are.""")

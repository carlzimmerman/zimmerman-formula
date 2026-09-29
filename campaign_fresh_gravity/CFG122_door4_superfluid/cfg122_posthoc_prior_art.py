#!/usr/bin/env python3
"""CFG122 R5 (POST-HOC, labelled; run only AFTER every gate run): side-by-side with the repo's prior superfluid art.
Reads (read-only): real_research/superfluid_phonon_baryon_coupling_price_2026.py (executed, stdout parsed) and superfluid_2026/sfD_superfluid_phonon_2026.out (headline lines).
No number here enters a pass line.  Disagreements are disclosed, not repaired.
Run: ZF_REPO=<repo> python3 cfg122_posthoc_prior_art.py"""
import os, sys, re, json, subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg122_common import Report, REPO, HERE

R = Report("cfg122_posthoc_prior_art")
P = R.P
if REPO is None:
    P("repo not found (set ZF_REPO)"); sys.exit(2)
pr = os.path.join(REPO, "real_research", "superfluid_phonon_baryon_coupling_price_2026.py")
out = subprocess.run([sys.executable, "-B", pr], capture_output=True, text=True, cwd=os.path.dirname(pr)).stdout
R.banner("R5a  the prior pricing script's Solar-System numbers (its own footing a0 = 9.3619e-11 / 1.1279e-10) against this lane's G5.4 (a0 = 9.3603e-11 / 1.1312e-10)")
mine = json.load(open(os.path.join(HERE, "cfg122_g4_g5solar_results.json")))["numbers"]["G5.4_readings"]
blocks = re.split(r"FOOTING (canonical|alt):", out)
prior = {}
for i in range(1, len(blocks), 2):
    foot, txt = blocks[i], blocks[i + 1]
    for rd in ("A", "B"):
        seg = re.search(r"READING " + rd + r"(.*?)(?=-- READING|-- \(c\))", txt, re.S)
        if not seg:
            continue
        s = seg.group(1)
        g = lambda pat: float(re.search(pat, s).group(1))
        prior[(foot, rd)] = dict(eta_mic_x=g(r"eta_MICROSCOPE = [\d.e+-]+\s+-> ([\d.e+-]+)x the 1e-15"), gamma_sigma=g(r"-> ([\d.e+-]+) sigma vs Cassini"), ephem_over=g(r"OVER by ([\d.e+-]+)x"))
for foot in ("canonical", "alt"):
    for rd in ("A", "B"):
        pv, mv = prior[(foot, rd)], mine[f"{foot}|{rd}"]
        P(f"  [{foot}] reading {rd}: Cassini (x bound) prior {pv['gamma_sigma']:.4g} vs here {mv['gamma_minus_1'] / 2.3e-5:.4g};  MICROSCOPE (x 1e-15) prior {pv['eta_mic_x']:.4g} vs here {mv['eta_mic'] / 1e-15:.4g};  "
          f"ephemeris ceiling (x) prior {pv['ephem_over']:.4g} vs here {mv['anomaly_over_a0'] / 1.27e-5:.4g}")
P("  Disagreements: MICROSCOPE differs by ~7% (this lane uses 48Ti/195Pt isotope masses for Delta(B/mu), the prior script mean-element proxies; both recalled, unverified); Cassini and the ephemeris ratios agree to the digits shown.")
R.banner("R5b  the prior superfluid_2026 lane (sfD, on the framework's OWN DBI kernel, not the BK P ~ X^(3/2)): headline lines")
sfd = open(os.path.join(REPO, "superfluid_2026", "sfD_superfluid_phonon_2026.out")).read().splitlines()[:40]
for l in sfd[:6]:
    P("  | " + l)
P("  ...")
P("  Comparison: sfD studies the DBI kernel K(Q) = -M^4 sqrt(1 - (Q-Q0)^2/Lam_D^2), a different EFT from the BK P(X) used here; its headline (the a0-line shape available but keyed to the potential, and the condensate density ∝ the potential, not 1/r^2)"
  " is consistent in spirit with this lane's finding that the P(X) condensate density does not follow the target's r-dependence, but the two are not the same computation and no number transfers.")
P("  sf06 (prior theorem: an ENVIRONMENTAL phase boundary cannot screen the Solar System because the Sun is at 0.67 of the MW's r_M) is reproduced independently in G5.4(iv): the NFW density at the MW's r_M is 0.83 of that at the Sun, the dispersion is the same, T/T_c differs by <20%.")
R.check("R5 (reported) prior-art comparison recorded", "see the table above", True, load_bearing=False)
nf, gf = R.write()
sys.exit(0)

# Common rules for lanes A36 onward

This folder is a quarantined research experiment. It maps how a rival group could reverse-engineer ("swoop") the core framework: the galaxy law g_obs = (g_b + sqrt(g_b^2 + 4 g_b a0))/2 with the tie a0(z) = kappa c sqrt(G rho_DE(z)), kappa = 1/2 FITTED. The rival side is not believed; everything here is rival language, adopts nothing, and never feeds any other folder. Never write "theory closed", never say data favour the law or rule the rival out. No personal names in files.

Read first: README.md (history A1 onward), FROZEN_RECIPE.md (gates; tie gates G1 to G5 in Amendment A13; A15 corrections), COVERAGE_MAP.md (your family's row and lane brief), FROZEN_A29.md (evolving-DE backgrounds and the tracking gate; background code in scripts/recipe31.py), scripts/lib.py.

Gates:
- E1 rms to law <= 0.02 dex, E2 p95 per-galaxy <= 0.04, E3 worst bin <= 0.02, holdout (tune GS[::2], unseen GS[1::2]) <= 0.025.
- G1 kappa_eff within 0.05 dex of 0.5; G2 slope d ln a / d ln rho_DE = 0.5 +- 0.05; G3 a(z)/a(0) inside [0.76,1.03], [0.71,1.12], [0.33,1.21] at z 1, 1.5, 2.33; G4 one constant across hosts (log M200 11 to 12.5) rms <= 0.1 dex; G5 operative at galaxy radii (>= 0.1 a0 effect at 1 to 30 kpc).
- GT tracking: |log10[a(z)/a(0)] - 0.5 log10[rho_DE(z)/rho_DE(0)]| <= 0.05 dex at z 1, 1.5, 2.33 in the A29 backgrounds.
- Where relevant, solar system: Cassini as graded in A9 (scripts/recipe11.py).

Rules:
1. Write FROZEN_Axx.md (route, the paper's equations as implemented and where they came from, knobs, gates, tolerances) BEFORE computing any number. Commit nothing; the parent session commits.
2. Script scripts/recipeNN.py with output .out, run from scripts/. Single-threaded (OMP_NUM_THREADS=1, MKL and OPENBLAS too), under about 1 GB RSS, checkpoint anything over 10 minutes. Machine memory is tight. Do not touch other lanes' files.
3. Web look-ups (WebFetch/WebSearch reading only) are PROVISIONAL; quote the equation used and its source; flag anything from memory. Do not download PDFs, data or code; if one is needed, stop and report filename, source and size. Never WebFetch a PDF link (arxiv.org/pdf/..., journal .pdf URLs): the tool saves the file. Use arxiv.org/abs/ or ar5iv HTML pages only.
4. A bug found after a run: keep the wrong output as *_before_fix.out and disclose it.
5. Verify a fail as hard as a pass. Count every parameter; disclose knobs at bounds; state what is derived in the source and what is imposed.
6. Append results and deviations to FROZEN_Axx.md, ending with "Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed."

Final report to the parent (under 300 words): verdict per gate with the .out line for each number, deviations, provisional items.

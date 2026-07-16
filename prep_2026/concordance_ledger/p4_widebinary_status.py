#!/usr/bin/env python3
"""
P4 -- GAIA WIDE BINARIES: STATUS ROW (pending), NOT a decided band. Microarcsecond
astrometry; systematics (contamination by triples/flyby projection, mass estimation)
fully disjoint from P1/P2/P3.

FRAMEWORK PREDICTION (banked, corrected 2026-06-15): the pure-MI theta(0)-family gives
gamma = v_wb/v_Newton ~ 1.05-1.14 (MOST-Newtonian of the MOND family); the modified-
GRAVITY momentary-field value is 1.137; simple-mu MOND ~1.25+; Newton exactly 1.00.
Pure MI with no EFE channel predicts the smallest boost of any MOND reading -- so this
row can KILL the framework (hard Newtonian null kills all of MOND incl. this framework)
or separate MI from MG (>=15-20% boost favors MG over MI).

IN-REPO DRY-RUN RECORD (committed outputs, Gaia (E)DR3, re-read here verbatim):
  real_research/data/widebinaries/wb_exact_replication.out  (selection replication)
  real_research/data/widebinaries/wb_deprojection_mc.out    (calibrated deprojection MC)
Session-banked headline gamma = 1.205 +/- 0.035 (DR3 dry-run) carries an UNRESOLVED
contamination-axis caveat and is NOT independently recomputed here -- quoted as status
only. What IS in the committed record (verified below by re-parsing the .out files):
deep-bin medians sit ~2.4-3.2 z above the calibrated Newton MC, FAR below the naive
MOND upper bound, and a separation-dependent triple fraction (physically expected) can
absorb most of the excess. DR4 (~Dec 2026) is the decider. STATUS: PENDING.
"""
import re, os

WB = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/widebinaries"
dep = open(os.path.join(WB, "wb_deprojection_mc.out")).read()

# re-extract the committed deep-bin comparison (verbatim from the committed output)
z_line = re.search(r"z\(data-Newton\)=\[([\d.\s]+)\]", dep).group(1).split()
mond_line = re.search(r"z\(data-MOND\*\)=\[([-\d.\s]+)\]", dep).group(1).split()
deep = re.search(r"deep-bin medians:\s+data=\[([\d.\s]+)\]\s+Newton=\[([\d.\s]+)\]\s+MOND\*=\[([\d.\s]+)\]", dep)
d_data = [float(x) for x in deep.group(1).split()]
d_newt = [float(x) for x in deep.group(2).split()]
d_mond = [float(x) for x in deep.group(3).split()]

print("="*88)
print("P4 WIDE-BINARY STATUS ROW (Gaia DR3 dry-run; DR4 pending -- NOT a decided band)")
print("="*88)
print("  framework prediction: pure-MI gamma ~ 1.05-1.14 (theta(0)-family; most-Newtonian")
print("  MOND reading); MG momentary-field 1.137; Newton 1.00. a0-degenerate: this row")
print("  tests the PREMISE (boost vs none), not the a0 value.")
print()
print("  committed DR3 dry-run record (re-parsed from the frozen repo outputs):")
for i, (dd, dn, dm) in enumerate(zip(d_data, d_newt, d_mond)):
    print(f"    deep bin {i+1}: median v_t data={dd:.3f} vs Newton-MC={dn:.3f} "
          f"(ratio {dd/dn:.2f}) vs naive-MOND upper bound={dm:.2f}")
print(f"    z(data - Newton MC)     = {z_line}   (excess present, ~2.4-3.2 z)")
print(f"    z(data - MOND upper)    = {mond_line}   (naive full boost strongly disfavored)")
print()
print("  session-banked headline: gamma(DR3 dry-run) = 1.205 +/- 0.035 -- carried with the")
print("  CONTAMINATION-AXIS CAVEAT (a separation-dependent triple fraction, physically")
print("  expected, absorbs most of the deep-bin excess in the committed discriminator")
print("  scan); not recomputed here, and NOT to be read as a detection.")
print()
print("  STATUS: PENDING (Gaia DR4, ~Dec 2026). Ledger treatment: no band claimed; the")
print("  row exists because it is the one probe that can return a HARD kill (Newtonian")
print("  null) or a clean MI-vs-MG separation. Neither outcome is banked today.")

"""CFG234 post-freeze item (2026-09-30, the data chat's z > 3.5 independent-baryon list, commit 2ad335eea). POST-FREEZE, labelled: nothing here changes a frozen line.
Which three discs beyond the six dust-detected ones the 9-disc route uses, their gas status, one-sided bounds on their delta, and the strict class-A route verdict."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CFG234_common import *
t = start("CFG234_postfreeze")
df = load_cristal()
UL = [i for i in ROUTE9 if i not in DETECTED6]
print("route set (finite SED M*, finite f_molgas, finite fitted M_bary, primary set):", ROUTE9)
print("dust-DETECTED per the data chat list (02 03 07a 11 19 20):", DETECTED6)
print("the other three the 9-disc route uses:", UL, "-> per the data chat list these have gas UPPER LIMITS only (continuum below threshold); the repo's kinematics table carries them as VALUES (f_molgas with errors), with no upper-limit flag column:")
for i in UL:
    r = df.loc[i]; k = pd.read_csv(os.path.join(AT, "cristal2025_kinematics.csv")).set_index("id").loc[i]
    print(f"   {i}: f_molgas {r.f_molgas} (+{k.errhi} / -{k.errlo}); M* {r.logMstar}; route factor {float(route_factor(df.loc[[i]])[0]):.3f}")
print("also excluded/other: 15 (excluded; gas upper limit per the list), 06b (no f_molgas), 10a-E (no M*, no f_molgas), 23c (no M*; gas upper limit per the list), 09 (excluded)")
print("\none-sided bounds (an upper limit on M_gas is an upper limit on g_bar,ind; under the recompute reading delta FALLS as g_bar rises, so each delta below is a LOWER bound on the true delta):")
for i in UL:
    d = df.loc[[i]]; rf = route_factor(d)
    b = {law: float(cell(d, rival=(law == "rival"), gbar_mul=rf, route="recompute")[0][0]) for law in ("flat", "rival")}
    f = {law: float(cell(d, rival=(law == "rival"))[0][0]) for law in ("flat", "rival")}
    print(f"   {i}: delta_flat >= {b['flat']:+.3f}, delta_rival >= {b['rival']:+.3f}   (fit route: {f['flat']:+.3f}, {f['rival']:+.3f}); D_ind = D/route factor = {float(cell(d, gbar_mul=rf, route='recompute')[1][0]):.3f}")
print("\nstrict CRISTAL class A (six detections), n = 6, mono canonical k=3.36, seed 234, 10,000 resamples:")
d6 = df.loc[DETECTED6]; rf6 = route_factor(d6)
for rt in ("recompute", "hold"):
    print(f"   SED + gas route, reading {rt}: flat {fmt(stat(cell(d6, gbar_mul=rf6, route=rt)[0]))} | rival {fmt(stat(cell(d6, rival=True, gbar_mul=rf6, route=rt)[0]))}")
print("   fit route, same six:      flat", fmt(stat(cell(d6)[0])), "| rival", fmt(stat(cell(d6, rival=True)[0])))
print("   all four kernel/footing cells, recompute reading, rival class:", [stat(cell(d6, kernel=kn, foot=ft, rival=True, gbar_mul=rf6, route="recompute")[0])["cls"] for kn in ("mono", "p2") for ft in A0])
print("   all four kernel/footing cells, recompute reading, flat class :", [stat(cell(d6, kernel=kn, foot=ft, gbar_mul=rf6, route="recompute")[0])["cls"] for kn in ("mono", "p2") for ft in A0])
print("\nGN20 (CO) and REBELS-25 (CO, paper not on disk): no per-disc table of V, f_DM/D, R, M*, M_gas exists in the repo (grep of data_assembly and real_research/data finds only the data chat's list and the source table);")
print("the strict class-A set of 8 therefore cannot be scored here; the CRISTAL six is the part of it that can.")
print("\nDoes the 9-disc verdict rest on the upper limits? drop the three upper-limit discs (n = 6) -> both laws still CONSISTENT (recompute); the rival median moves from -0.198 to -0.144; the fit route on the same six keeps the rival DISFAVOURED-under. The route CONSISTENT label does not depend on them; the size of the interval does (n = 6 bootstrap is wide).")

# ------------------------------------------------------------------------------------------------ POST-HOC extra (after the runs above; reported only)
print("\n== POST-HOC: per-galaxy route deltas (recompute reading, mono canonical) and leave-one-out of the route class ==")
d9 = df.loc[ROUTE9]; rf9 = route_factor(d9)
dl_f, D_ind, _ = cell(d9, gbar_mul=rf9, route="recompute"); dl_r = cell(d9, rival=True, gbar_mul=rf9, route="recompute")[0]
for i, a, b, Dv, rr in zip(ROUTE9, dl_f, dl_r, D_ind, rf9):
    print(f"   {i:4s} route factor {rr:5.3f}  D_ind {Dv:6.3f}{'  (< 1: baryons exceed the dynamical mass)' if Dv < 1 else ''}  delta_flat {a:+.3f}  delta_rival {b:+.3f}  {'[dust UPPER LIMIT used as a value]' if i in UL else ''}")
print("   D_ind < 1 in", int(np.sum(D_ind < 1)), "of 9;", ", ".join(i for i, v in zip(ROUTE9, D_ind) if v < 1))
for j, i in enumerate(ROUTE9):
    dd = d9.drop(i); rr = route_factor(dd)
    sf = stat(cell(dd, gbar_mul=rr, route="recompute")[0]); sr = stat(cell(dd, rival=True, gbar_mul=rr, route="recompute")[0])
    print(f"   leave out {i:4s}: flat {fmt(sf)} | rival {fmt(sr)}")

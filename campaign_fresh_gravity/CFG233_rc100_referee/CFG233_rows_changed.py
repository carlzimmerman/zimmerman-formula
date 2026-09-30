"""CFG233 rows-changed disclosure (post-freeze item 2): which of the 16 rows differing between the COMMITTED csv and the CORRECTED six-field copy enter which set, and what they do."""
import sys, os
os.environ.setdefault("DATA", "committed")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CFG233_common import *
start("CFG233_rows_changed")
a = load_rc100("committed"); b = load_rc100("corrected")
print("rows committed/corrected:", len(a["z"]), len(b["z"]), "; idx aligned:", bool(np.all(a["idx"] == b["idx"])), "; z, R_e, sigma0 identical:", bool(np.all(a["z"] == b["z"]) and np.all(a["Re"] == b["Re"]) and np.all(a["s0"] == b["s0"])))
ma, *_ = rc41_match(a); mb, *_ = rc41_match(b)
chg = [i for i in range(len(a["z"])) if (a["name"][i] != b["name"][i]) or a["logM"][i] != b["logM"][i] or a["f"][i] != b["f"][i] or a["Vc"][i] != b["Vc"][i]]
print(f"rows that differ: {len(chg)} (idx {[int(a['idx'][i]) for i in chg]})")
fa, ra = delta_pair(a["D"], a["gbar"], a["z"]); fb, rb = delta_pair(b["D"], b["gbar"], b["z"])
print(" idx | z | field changes | RC41 (committed names) | RC41 (corrected names) | delta_flat committed -> corrected | g_bar/a0 committed -> corrected")
R = {}
for i in chg:
    ch = []
    if a["name"][i] != b["name"][i]: ch.append(f"name {a['name'][i]}->{b['name'][i]}")
    if a["logM"][i] != b["logM"][i]: ch.append(f"logM {a['logM'][i]}->{b['logM'][i]}")
    if a["f"][i] != b["f"][i]: ch.append(f"f {a['f'][i]}->{b['f'][i]}")
    if a["Vc"][i] != b["Vc"][i]: ch.append(f"Vc {a['Vc'][i]:.0f}->{b['Vc'][i]:.0f}")
    print(f" {int(a['idx'][i]):3d} | {a['z'][i]:.2f} | {'; '.join(ch)} | {'RC41' if ma[i] else '62-set'} | {'RC41' if mb[i] else '59-set'} | {fa[i]:+.3f} -> {fb[i]:+.3f} | {a['gbar'][i]/A0['canonical']:.2f} -> {b['gbar'][i]/A0['canonical']:.2f}")
print(f"\nmatched RC41 by name: committed {int(ma.sum())}, corrected {int(mb.sum())}; rows that change RC41 membership: {[int(a['idx'][i]) for i in range(len(ma)) if ma[i] != mb[i]]}")
print("changed rows inside the 38-set (committed names):", int(sum(ma[i] for i in chg)), "; inside the 62-set:", int(sum(not ma[i] for i in chg)), "; inside the corrected 41-set:", int(sum(mb[i] for i in chg)), "; corrected 59-set:", int(sum(not mb[i] for i in chg)))
print("changed rows by kind: logM_bar", [int(a['idx'][i]) for i in chg if a['logM'][i] != b['logM'][i]], "| Vc", [int(a['idx'][i]) for i in chg if a['Vc'][i] != b['Vc'][i]], "| f", [int(a['idx'][i]) for i in chg if a['f'][i] != b['f'][i]], "| name only", [int(a['idx'][i]) for i in chg if a['name'][i] != b['name'][i] and a['logM'][i] == b['logM'][i]])
print("rows 65 (logM 9.63 -> 11.33) etc. change g_bar only through the table's M_bar in variant (d) and the M_bar-based gas grid; in the primary (f_DM, V_c) quantities the logM_bar column does NOT enter, so only rows 36, 43, 44 change the primary delta.")
same = np.array([i not in chg for i in range(len(a["z"]))])
zz = a["z"][same]
s84 = (ts(zz, fa[same]), ts(zz, ra[same]))
print(f"\nslopes on the {same.sum()} unchanged rows (identical in both files): flat {s84[0]:+.4f}, rival {s84[1]:+.4f}")
prim_rows = [i for i in chg if a["f"][i] != b["f"][i] or a["Vc"][i] != b["Vc"][i]]
print("slopes with only the primary-affecting rows (idx %s) replaced: committed flat %+.4f rival %+.4f -> corrected flat %+.4f rival %+.4f" % (
    [int(a['idx'][i]) for i in prim_rows], ts(a["z"], fa), ts(a["z"], ra), ts(b["z"], fb), ts(b["z"], rb)))
R = dict(changed_idx=[int(a["idx"][i]) for i in chg], rc41_committed=int(ma.sum()), rc41_corrected=int(mb.sum()), slopes84=s84,
         prim_committed=(ts(a["z"], fa), ts(a["z"], ra)), prim_corrected=(ts(b["z"], fb), ts(b["z"], rb)))
savejson("CFG233_rows_changed", R)

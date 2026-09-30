"""CFG234 attack (c): the pressure term. k in {0,1.68,2.52,3.36,5} x {H-g, H-f} x kernel x footing x law; vector-inferred k; break-even k*;
count of D_k < 1; NOEMA3D pressure sensitivity. Reports; exit 0."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CFG234_common import *

t = start("CFG234_attack_c")
B = 10000
df = load_cristal(); d12 = df.loc[ID12]
R = {}
KS = [0.0, 1.68, 2.52, 3.36, 5.0]
CELLS = [("mono", "canonical"), ("mono", "alt"), ("p2", "canonical"), ("p2", "alt")]

print("== c1: k x {H-g, H-f} x cells (12 disks, seed 234) ==")
grid = {}
for mode in ("Hg", "Hf"):
    print(f"-- mode {mode}")
    for k in KS:
        for kn, ft in CELLS:
            row = []
            for law in ("flat", "rival"):
                dl, D, y = cell(d12, k=k, mode=mode, kernel=kn, foot=ft, rival=(law == "rival"))
                s = stat(dl, 234, B); grid[f"{mode}|{k}|{kn}|{ft}|{law}"] = dict(s, nD_lt1=int(np.sum(D < 1)))
                row.append(f"{law} {s['med']:+.3f} {s['cls']:5s}")
            nD = int(np.sum(cell(d12, k=k, mode=mode)[1] < 1))
            print(f"  k={k:4.2f} {kn:4s} {ft:9s}: " + " | ".join(row) + f" | D_k<1 in {nD} of 12")
R["c1"] = grid


def robust(mode, law, ks=(3.36, 1.68)):
    cl = [grid[f"{mode}|{k}|{kn}|{ft}|{law}"]["cls"] for k in ks for kn, ft in CELLS]
    return cl
for mode in ("Hg", "Hf"):
    for law in ("flat", "rival"):
        cl = robust(mode, law)
        print(f"robustness over k in {{3.36,1.68}} x 4 kernel/footing cells, {mode}, {law}: {cl} -> {'ROBUST ' + cl[0] if len(set(cl)) == 1 else 'NOT robust'}")
fmed = {m: [grid[f"{m}|{k}|mono|canonical|flat"]["med"] for k in KS] for m in ("Hg", "Hf")}
print("flat median vs k (mono canonical):", {m: [round(v, 3) for v in fmed[m]] for m in fmed}, " -> change over k 3.36 -> 0:", {m: round(fmed[m][3] - fmed[m][0], 3) for m in fmed})
rmed = {m: [grid[f"{m}|{k}|mono|canonical|rival"]["med"] for k in KS] for m in ("Hg", "Hf")}
print("rival median vs k (mono canonical):", {m: [round(v, 3) for v in rmed[m]] for m in rmed})

print("\n== c2: vector-inferred pressure coefficient k_i = (V_tot,vec(R_e)^2 - V_rot,table^2) / sigma_0,table^2 ==")
cur, pts, val, out = load_vector()
ki = {}
for i in ID14:
    vid = VEC_ALIAS.get(i, i); r = df.loc[i]
    Vt = vec_at(cur, vid, "V_tot", r.Re)
    ki[i] = (Vt ** 2 - r.Vrot ** 2) / r.sig ** 2
    print(f"  {i:5s}: V_tot,vec(R_e) {Vt:6.1f}  V_rot {r.Vrot:6.1f}  sigma_0 {r.sig:5.1f}  k_i = {ki[i]:5.2f}")
clean5 = ["03", "07a", "20", "23b", "23c"]
k14 = np.array([ki[i] for i in ID14]); k12 = np.array([ki[i] for i in ID12]); k5 = np.array([ki[i] for i in clean5])
print(f"median k: 14 disks {np.median(k14):.2f} [16-84 {np.percentile(k14,16):.2f}, {np.percentile(k14,84):.2f}]; 12: {np.median(k12):.2f}; five figure-clean disks (03 07a 20 23b 23c): {np.median(k5):.2f} (values {np.round(k5,2)})")
R["c2"] = dict(ki=ki, med14=float(np.median(k14)), med12=float(np.median(k12)), med5=float(np.median(k5)))

print("\n== c3: break-even k* (mono canonical; bootstrap indices fixed, seed 234) ==")
rng = np.random.default_rng(234)
IDX = rng.integers(0, 12, size=(B, 12))


def summ(k, mode, law):
    dl = cell(d12, k=k, mode=mode, rival=(law == "rival"))[0]
    m = np.median(dl[IDX], axis=1)
    return float(np.median(dl)), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def root(fun, lo=0.0, hi=60.0):
    flo, fhi = fun(lo), fun(hi)
    if flo * fhi > 0: return None
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if fun(mid) * flo > 0: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)


kst = {}
for mode in ("Hg", "Hf"):
    for law in ("flat", "rival"):
        kmed = root(lambda k: summ(k, mode, law)[0])
        khi = root(lambda k: summ(k, mode, law)[2]) if law == "rival" else None
        klo = root(lambda k: summ(k, mode, law)[1]) if law == "flat" else None
        kst[f"{mode}|{law}"] = dict(k_median_zero=kmed, k_upper_edge_zero=khi, k_lower_edge_zero=klo)
        print(f"  {mode} {law}: median delta = 0 at k* = {kmed if kmed is None else round(kmed,2)}" + (f"; CI upper edge = 0 at k = {khi if khi is None else round(khi,2)}" if law == 'rival' else f"; CI lower edge = 0 at k = {klo if klo is None else round(klo,2)}"))
R["c3"] = kst

print("\n== c4: NOEMA3D pressure sensitivity (V_c read as circular at k = 3.36; k varied per the criteria) ==")
dn = load_noema(); fn, Vrot2 = noema_frame(dn)
c4 = {}
for mode in ("Hg", "Hf"):
    for k in (3.36, 1.68, 0.0):
        row = []
        for law in ("flat", "rival"):
            dl, D, y = cell_noema(fn, Vrot2, k=k, mode=mode, rival=(law == "rival"))
            s = stat(dl, 234, B); c4[f"{mode}|{k}|{law}"] = s
            row.append(f"{law} {fmt(s)}")
        print(f"  {mode} k={k:4.2f}: " + " | ".join(row))
R["c4"] = c4
savejson("CFG234_attack_c", R)
sys.exit(0)

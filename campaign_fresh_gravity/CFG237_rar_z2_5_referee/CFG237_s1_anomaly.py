"""CFG237 attack 3: the S1 g_obs < g_bar anomaly. Algebra first, then the pre-declared grid (frozen section 5.8), the two mass-level tests,
per-galaxy leverage, single-axis minimal moves, the decision rule. Exit 0."""
import sys, itertools
from CFG237_common import *

t = start("CFG237_s1_anomaly")
ck = Checks()
R = {}
d = load_s1()
P0 = s1_points(d)
print("ids", list(d.alessid))

# ------------------------------------------------------------------ algebra checks
print("\n== algebra (frozen 5.3): at r = 2 R_e, y = r/(2 R_d) = 1.678 for every source, so g_bar = c0 G M_bar / R_e^2 ==")
y = 2 * RD_FAC / 2
f = y ** 2 * (special.i0(y) * special.k0(y) - special.i1(y) * special.k1(y))
# g_bar = V^2/r, V^2 = 2GM/Rd * f ; r = 2 Re = 2*1.67835 Rd  => g = 2GM f/(Rd * 2*1.67835*Rd) = G M f / (1.67835 Rd^2) = G M f * 1.67835 / Re^2
c0 = f * RD_FAC
print(f"   y = {y:.4f}, f(y) = {f:.6f}, c0 = f * 1.67835 = {c0:.6f} (g_bar = c0 G M_bar/R_e^2)")
chk_c0 = np.max(np.abs(P0["gbar"] / (c0 * G * (P0["Mst"] + P0["Mg"]) * MSUN / (P0["re"] * KPC) ** 2) - 1))
ck.add("algebra: g_bar = c0 G M_bar / R_e^2 for all nine (1e-10)", chk_c0 < 1e-10, f"{chk_c0:.2e}")
Ps = s1_points(d, s=1.5)
ck.add("algebra: D scales exactly with R_e (x1.5 -> D x1.5) at fixed V, M", np.max(np.abs(Ps["D"] / P0["D"] - 1.5)) < 1e-9)
inc = d.inc_deg.values
Pi = s1_points(d, di=-10)
ok_i = True
for j in range(len(d)):
    inew = np.clip(inc[j] - 10, 15, max(85, inc[j]))
    ok_i &= abs(Pi["D"][j] / P0["D"][j] - (np.sin(np.radians(inc[j])) / np.sin(np.radians(inew))) ** 2) < 1e-9
ck.add("algebra: D scales as (sin i / sin i_new)^2", ok_i)
Pa = s1_points(d, alpha=1.84)
ck.add("algebra: D(alpha) = D / (1 + gas share (alpha/0.92 - 1)), per galaxy", np.max(np.abs(Pa["D"] / (P0["D"] / (1 + P0["g_gas"] / P0["gbar"] * (1.84 / 0.92 - 1))) - 1)) < 1e-9)

# ------------------------------------------------------------------ the anomaly itself
print("\n== per-galaxy baseline ==")
Dst = P0["gobs"] / P0["g_st"]   # stars-only D (alpha = 0)
names = list(d.alessid)
print("   id      z     re_kpc  inc   V   logM*  logMgas  gas share  D(base)  D(stars only)  M_bar/M_dyn(10kpc)")
Mdyn10 = d.mdyn_10kpc_1e11msun.values * 1e11
Mbar = d.Mstar.values + d.Mgas.values
RM = Mbar / Mdyn10
x = 2 * P0["re"] / (P0["re"] / RD_FAC)
frac = 1 - (1 + x) * np.exp(-x)
Mdyn2 = (d.V.values * 1e3) ** 2 * (2 * P0["re"] * KPC) / G / MSUN
R2 = Mbar * frac / Mdyn2
for j in range(len(d)):
    print(f"   {names[j]}  {d.z[j]:.3f}  {P0['re'][j]:5.2f}  {inc[j]:4.0f} {d.V[j]:4.0f}  {d.logMstar[j]:5.2f}  {d.logMgas_msun[j]:5.2f}    {P0['g_gas'][j] / P0['gbar'][j]:4.2f}     {P0['D'][j]:5.3f}     {Dst[j]:5.3f}        {RM[j]:5.2f}   (R_2re {R2[j]:.2f})")
print(f"   median D {np.median(P0['D']):.3f}; stars-only (alpha = 0) median D {np.median(Dst):.3f}, n(D_star>=1) = {int(np.sum(Dst >= 1))}")
print(f"   mass-level: R_M = M_bar/M_dyn(<10 kpc): median {np.median(RM):.2f}, n(R_M >= 1) = {int(np.sum(RM >= 1))} of 9; R_2re (enclosed baryons / V^2 2r_e/G): median {np.median(R2):.2f}, n(R_2re >= 1) = {int(np.sum(R2 >= 1))}")
print(f"   M* only vs M_dyn(10 kpc): median {np.median(d.Mstar.values / Mdyn10):.2f}, n(M*/Mdyn >= 1) = {int(np.sum(d.Mstar.values >= Mdyn10))}")
R["base"] = dict(D=P0["D"], Dstar=Dst, RM=RM, R2=R2, gas_share=P0["g_gas"] / P0["gbar"], median_D=float(np.median(P0["D"])))
# internal consistency of the dynamical table: M(<2re) from V vs M_dyn(10 kpc) (flat curve: M ~ r)
ratio = Mdyn2 / Mdyn10
print("   V^2 (2 r_e)/G  /  M_dyn(10 kpc) (flat-curve test, expect ~ 2 r_e / 10 kpc):", np.round(ratio, 2), " vs 2 r_e/10 kpc:", np.round(2 * P0["re"] / 10, 2))

# ------------------------------------------------------------------ the grid
ALPHA = [0.15, 0.30, 0.46, 0.60, 0.80, 0.92, 1.5, 2.5, 3.6, 4.3]
BM = [-0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3]
DI = [-15, -10, -5, 0, 5, 10, 15]
SS = [0.75, 1.0, 1.33, 1.5, 2.0]
MS = [1, 2]
KK = [0.0, 3.36]
cells = []
for a, b, di_, s_, m_, k_ in itertools.product(ALPHA, BM, DI, SS, MS, KK):
    Pg = s1_points(d, alpha=a, bM=b, di=di_, s=s_, mstar_mult=m_, k=k_)
    Dm = float(np.median(Pg["D"])); n1 = int(np.sum(Pg["D"] >= 1))
    dl = float(np.median(delta(Pg["gobs"], Pg["gbar"], Pg["z"], "FLAT")))
    C = math.sqrt((math.log10(a / 0.92) / 0.15) ** 2 + (b / 0.2) ** 2 + (di_ / 7.0) ** 2 + (math.log10(s_) / 0.10) ** 2 + (1.0 if m_ == 2 else 0.0) ** 2 + (1.0 if k_ == 3.36 else 0.0) ** 2)
    cells.append(dict(alpha=a, b=b, di=di_, s=s_, m=m_, k=k_, Dmed=Dm, n1=n1, dflat=dl, C=C, restore=(Dm >= 1 and n1 >= 5)))
cdf = pd.DataFrame(cells)
print(f"\n== grid: {len(cdf)} cells (alpha {len(ALPHA)} x b {len(BM)} x di {len(DI)} x s {len(SS)} x m* {len(MS)} x k {len(KK)}) ==")
print(f"   baseline cell (0.92, 0, 0, 1, 1, 0): median D {cdf[(cdf.alpha == 0.92) & (cdf.b == 0) & (cdf.di == 0) & (cdf.s == 1) & (cdf.m == 1) & (cdf.k == 0)].Dmed.iloc[0]:.3f}")
rs = cdf[cdf.restore]
print(f"   cells with median D >= 1 and n(D>=1) >= 5: {len(rs)} of {len(cdf)}")
R["n_restore"] = int(len(rs)); R["n_cells"] = int(len(cdf))
if len(rs):
    mc = rs.sort_values("C").head(8)
    print("   lowest-cost restoring cells:")
    print(mc.to_string(index=False))
    R["min_cost_cell"] = mc.iloc[0].to_dict()
# single-axis (others at baseline)
base = dict(alpha=0.92, b=0.0, di=0, s=1.0, m=1, k=0.0)
print("\n-- single-axis moves (others at baseline) --")
single = {}
for ax, vals in (("alpha", ALPHA), ("b", BM), ("di", DI), ("s", SS), ("m", MS), ("k", KK)):
    sub = cdf.copy()
    for k2, v2 in base.items():
        if k2 != ax: sub = sub[sub[k2] == v2]
    sub = sub.sort_values(ax)
    print(f"   axis {ax:5s}: " + "; ".join(f"{r[ax]}: D {r.Dmed:.2f}, n1 {r.n1}" + (" *RESTORES*" if r.restore else "") for _, r in sub.iterrows()))
    single[ax] = [dict(v=float(r[ax]), D=float(r.Dmed), n1=int(r.n1), restore=bool(r.restore)) for _, r in sub.iterrows()]
R["single_axis"] = single
# continuous single-axis minimal moves (bisection)
def find(fn, lo, hi, target=1.0):
    flo = fn(lo) - target; fhi = fn(hi) - target
    if flo * fhi > 0: return None
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if (fn(mid) - target) * flo > 0: lo = mid; flo = fn(mid) - target
        else: hi = mid
    return 0.5 * (lo + hi)
med = lambda **kw: float(np.median(s1_points(d, **kw)["D"]))
need = {}
need["alpha"] = find(lambda a: med(alpha=a), 0.0, 0.92)
need["b_dex"] = find(lambda b: med(bM=b), -3.0, 0.0)
need["s"] = find(lambda s_: med(s=s_), 1.0, 5.0)
need["di_deg"] = find(lambda x_: med(di=x_), -60.0, 0.0)
print("\n-- continuous single-axis value at which median D reaches 1 (None = not reachable within the bracket) --")
print(f"   alpha_CO needed: {need['alpha']}  (alpha = 0 gives median D {med(alpha=0.0):.3f})")
print(f"   M* zero point needed (dex): {need['b_dex']}")
print(f"   R_e scale needed (x): {need['s']}")
print(f"   inclination shift needed (deg; bounded 15..max(85,i)): {need['di_deg']}  (di=-60 gives D {med(di=-60.0):.3f})")
R["need"] = need
# what dominates: decompose per galaxy
print("\n-- which galaxies carry D < 1, and through what --")
for j in range(len(d)):
    kind = "stars" if P0["g_gas"][j] / P0["gbar"][j] < 0.5 else "gas"
    print(f"   {names[j]}: D {P0['D'][j]:.2f} (stars-only D {Dst[j]:.2f}); baryons dominated by {kind}; M*/M_dyn(10kpc) {d.Mstar.values[j] / Mdyn10[j]:.2f}")
print(f"   n(D<1) = {int(np.sum(P0['D'] < 1))}; of these, n with stars-only D < 1 (no gas at all would still overshoot): {int(np.sum((P0['D'] < 1) & (Dst < 1)))}")
R["n_D_lt1_stars_only"] = int(np.sum((P0["D"] < 1) & (Dst < 1)))

# ordinary-range restorations
ordr = cdf[(cdf.alpha.between(0.6, 1.5)) & (cdf.b.abs() <= 0.2) & (cdf.di.abs() <= 5) & (cdf.s <= 1.33) & (cdf.restore)]
print(f"\n-- cells inside the 'ordinary' ranges (alpha 0.6-1.5, |b|<=0.2, |di|<=5 deg (grid step below 7), s<=1.33) that restore: {len(ordr)} --")
R["n_ordinary_restore"] = int(len(ordr))
c2 = rs[rs.C <= 2.0]
print(f"   restoring cells with C <= 2: {len(c2)}; axes used by them: " + (", ".join(sorted({ax for _, r in c2.iterrows() for ax, bs in (('alpha', 0.92), ('b', 0.0), ('di', 0), ('s', 1.0), ('m', 1), ('k', 0.0)) if r[ax] != bs})) if len(c2) else "none"))
R["n_restore_C_le_2"] = int(len(c2))
law_ok = cdf[cdf.dflat.abs() < 0.1]
print(f"   cells with |median delta_FLAT| < 0.1: {len(law_ok)}; with restore also: {int((law_ok.restore).sum())}; lowest cost among them: " + (f"{law_ok.C.min():.2f}" if len(law_ok) else "n/a"))
R["n_delta_lt_0p1"] = int(len(law_ok))

# decision rule (frozen)
mass_level = int(np.sum(RM >= 1)) >= 5
geom_only_c2 = len(c2[(c2.alpha == 0.92) & (c2.b == 0.0)]) > 0
alpha_only = len(rs[(rs.b == 0.0) & (rs.di == 0) & (rs.s == 1.0) & (rs.m == 1) & (rs.k == 0.0) & (rs.alpha >= 0.46)]) > 0
mincost = float(rs.C.min()) if len(rs) else float("inf")
axes_c2 = {ax for _, r in c2.iterrows() for ax, bs in (("alpha", 0.92), ("b", 0.0), ("di", 0), ("s", 1.0)) if r[ax] != bs}
if len(rs) == 0: verdict = "NO RESTORATION"
elif mass_level: verdict = "MASS-LEVEL (R_M >= 1 in >= 5 of 9)"
elif alpha_only: verdict = "ALPHA-CO-RESTORABLE"
elif geom_only_c2: verdict = "GEOMETRY-RESTORABLE"
elif mincost > 3 or len(axes_c2) >= 2: verdict = "JOINT / NOT DECIDABLE"
else: verdict = "JOINT / NOT DECIDABLE"
print(f"\nDECISION (frozen rule): mass-level test R_M>=1 in {int(np.sum(RM >= 1))}/9 -> {mass_level}; alpha-only restores (alpha>=0.46): {alpha_only}; geometry-only C<=2 restores: {geom_only_c2}; min cost of any restoring cell: {mincost:.2f}; => {verdict}")
R["verdict"] = verdict; R["mass_level_count"] = int(np.sum(RM >= 1))
ordinary_single = []
for ax, lim in (("alpha", lambda v: 0.6 <= v <= 1.5 and v != 0.92), ("b", lambda v: abs(v) <= 0.2 and v != 0.0), ("di", lambda v: abs(v) <= 5 and v != 0), ("s", lambda v: 1.0 < v <= 1.33)):
    for e_ in single[ax]:
        if lim(e_["v"]) and e_["restore"]: ordinary_single.append((ax, e_["v"]))
ck.add("frozen H13 as WORDED (single-axis moves inside the ordinary ranges): none restores D >= 1 (P 0.7)", len(ordinary_single) == 0, f"{ordinary_single}")
ck.add("frozen H13 as CODED by me (any JOINT cell inside the ordinary ranges): none restores -- a STRONGER claim than the wording; kept", len(ordr) == 0, f"{len(ordr)} joint cells restore (they use m*=2 and/or k=3.36 or corner combinations)")
ck.add("frozen H13 expectation: alpha_CO alone at >= 0.6 does not restore (P 0.97)", not any(v["restore"] for v in single["alpha"] if v["v"] >= 0.6))
ck.add("frozen H13 expectation: verdict JOINT / NOT DECIDABLE (P 0.6)", verdict.startswith("JOINT"), verdict)
ck.add("frozen H13 expectation: mass-level overshoot R_M >= 1 in >= 5 of 9 (P 0.5)", mass_level, f"{int(np.sum(RM >= 1))} of 9")
ck.add("frozen H13 expectation: alpha_CO alone needs about 0.3 (the phase-1 guess from three gas-rich rows)", need["alpha"] is not None and 0.2 <= need["alpha"] <= 0.4, f"alpha needed = {need['alpha']}")
savejson("CFG237_s1_anomaly", R)
cdf.to_csv(os.path.join(HERE, "CFG237_s1_grid_cells.csv"), index=False)
print(f"\nSUMMARY: {len(ck.rows)} lines, {ck.n_fail()} FAIL (frozen expectations that did not hold are kept)")
for r_ in ck.rows:
    if not r_[1]: print("   FAILED:", r_[0], "::", r_[2])
sys.exit(0)

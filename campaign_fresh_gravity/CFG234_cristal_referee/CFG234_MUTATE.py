"""CFG234 MUTATE controls M1-M7 (MUTATE=k). Exit 1 when the control bites (as defined in the frozen criteria), 0 otherwise."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CFG234_common import *

K = int(os.environ.get("MUTATE", "0"))
assert 1 <= K <= 7, "set MUTATE=1..7"
t = start(f"CFG234_MUTATE_{K}")
B = 10000
df = load_cristal(); d12 = df.loc[ID12]
base = {law: stat(cell(d12, rival=(law == "rival"))[0], 234, B) for law in ("flat", "rival")}
print("baseline (unmutated, mono canonical k=3.36):", {k: fmt(v) for k, v in base.items()})
res = dict(K=K, base=base)
bites = False

if K == 1:
    off = 0.20
    mut = {law: stat(cell(d12, rival=(law == "rival"), Dmul=10 ** off)[0], 234, B) for law in ("flat", "rival")}
    shift = {law: mut[law]["med"] - base[law]["med"] for law in mut}
    print("M1: D_obs x 10^0.20 ->", {k: fmt(v) for k, v in mut.items()}, "median shifts", shift)
    exact = all(abs(s - off) < 1e-9 for s in shift.values())
    flips = mut["rival"]["cls"] != "under" and mut["flat"]["cls"] == "over"
    print("shift exactly 0.2000 (1e-9):", exact, "| rival leaves under and flat becomes over:", flips)
    bites = bool(exact and flips); res.update(mut=mut, shift=shift, exact=exact, flips=flips)

elif K == 2:
    # swap: 'flat' evaluated at A0 E(z), 'rival' at A0
    swf = stat(cell(d12, rival=True)[0], 234, B); swr = stat(cell(d12, rival=False)[0], 234, B)
    same = abs(swf["med"] - base["rival"]["med"]) < 1e-12 and abs(swr["med"] - base["flat"]["med"]) < 1e-12
    print("M2: reported-flat", fmt(swf), "| reported-rival", fmt(swr), "| reproduces main rival/flat rows to 1e-12:", same)
    bites = bool(same and swf["cls"] == "under"); res.update(swf=swf, swr=swr, same=same)

elif K == 3:
    mut = {law: stat(cell(d12, k=0.0, rival=(law == "rival"))[0], 234, B) for law in ("flat", "rival")}
    drop = base["flat"]["med"] - mut["flat"]["med"]
    print("M3: k = 0 (H-g):", {k: fmt(v) for k, v in mut.items()}, "flat median fall", round(drop, 3))
    h1_lost = mut["flat"]["cls"] == "under"
    bites = bool(mut["flat"]["cls"] != base["flat"]["cls"] and mut["flat"]["cls"] == "under" and drop >= 0.05); res.update(mut=mut, drop=drop)

elif K == 4:
    z0 = np.zeros(len(d12))
    dl_r0 = cell(d12, rival=True, Zlaw=z0)[0]; dl_f = cell(d12)[0]
    eq = float(np.max(np.abs(dl_r0 - dl_f)))
    sr = stat(dl_r0, 234, B)
    print("M4: E = 1: max |delta_rival - delta_flat| =", eq, "| rival class:", sr["cls"], "| flat class:", base["flat"]["cls"])
    bites = bool(eq < 1e-12 and sr["cls"] == base["flat"]["cls"] and sr["cls"] != base["rival"]["cls"]); res.update(eq=eq, sr=sr)

elif K == 5:
    rng = np.random.default_rng(234)
    zsh = rng.permutation(d12.z.values)
    dl_r = cell(d12, rival=True, Zlaw=zsh)[0]
    sr = stat(dl_r, 234, B)
    mv = sr["med"] - base["rival"]["med"]
    print("M5: z shuffled among the 12 (seed 234), rival a0 at shuffled z:", fmt(sr), "| median change", round(mv, 4), "| class unchanged:", sr["cls"] == base["rival"]["cls"])
    print("frozen expectation: |change| < 0.02 and class unchanged => does NOT bite (exit 0)")
    exp_line = abs(mv) < 0.02
    print("frozen magnitude line (|change| < 0.02):", "held" if exp_line else "MISSED (wrong expectation, kept)", "| exit follows the frozen exit rule: 1 only if the class changes")
    rng2 = np.random.default_rng(235)
    mvs = [float(np.median(cell(d12, rival=True, Zlaw=rng2.permutation(d12.z.values))[0]) - base["rival"]["med"]) for _ in range(200)]
    print("info (not frozen): 200 further shuffles (seed 235): median change mean %+.4f, sd %.4f, max |change| %.4f" % (np.mean(mvs), np.std(mvs), np.max(np.abs(mvs))))
    bites = bool(sr["cls"] != base["rival"]["cls"]); res.update(sr=sr, move=mv, magnitude_line_held=bool(exp_line), info_mvs=mvs)

elif K == 6:
    d9 = df.loc[ROUTE9]
    mult = np.full(9, 10 ** 0.30)
    out = {}
    for rt in ("hold", "recompute"):
        for law in ("flat", "rival"):
            r_ = law == "rival"
            b0 = stat(cell(d9, rival=r_, gbar_mul=np.ones(9), route=rt)[0], 234, B)
            m1 = stat(cell(d9, rival=r_, gbar_mul=mult, route=rt)[0], 234, B)
            # analytic first-order shift from the kernel slope at each galaxy's own y
            dl0, D0_, y0 = cell(d9, rival=r_, gbar_mul=np.ones(9), route=rt)
            h = 1e-4
            s_ = (np.log10(nu_mono(y0 * 10 ** h)) - np.log10(nu_mono(y0 * 10 ** -h))) / (2 * h)
            ana = np.median(-s_ * 0.30 - (0.30 if rt == "recompute" else 0.0))
            out[f"{rt}/{law}"] = dict(base=b0, mut=m1, shift=m1["med"] - b0["med"], analytic_first_order=float(ana))
            print(f"M6 [{rt:9s}] {law:5s}: {fmt(b0)} -> {fmt(m1)}; median shift {m1['med'] - b0['med']:+.3f} vs first-order analytic {ana:+.3f}"
                  f" ({'within 10 %' if abs((m1['med'] - b0['med']) / ana - 1) <= 0.10 else 'NOT within 10 %'})")
    bites = any(v["mut"]["cls"] != v["base"]["cls"] for v in out.values()); res["out"] = out

elif K == 7:
    d = df.loc[ID12]
    dl_f, _, yf = cell(d); dl_r, _, yr = cell(d, rival=True)
    s = mad_sigma(dl_f)
    rr, ok = recovery_control(yf, yr, s, seed=234, N=2000, B=300, n=12)
    print(f"M7 recovery (s = {s:.3f}):", json.dumps(rr))
    print("recovery", "PASS (control does not bite)" if ok else "FAIL (classifier uninformative at n = 12)")
    bites = not ok; res.update(rr=rr, ok=ok)

print(f"M{K} bites: {bites}  -> exit {1 if bites else 0}")
res["bites"] = bites
savejson(f"CFG234_MUTATE_{K}", res)
sys.exit(1 if bites else 0)

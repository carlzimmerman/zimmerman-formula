"""CFG236 MUTATE controls M1..M7 (frozen in CFG236_FROZEN_CRITERIA.md section 7).  MUTATE=k python3 CFG236_MUTATE.py
Exit 1 when the control bites (machinery responds as the frozen prediction says), 0 when it does not."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG236_common as c

K = int(os.environ.get("MUTATE", "1"))
B = int(os.environ.get("B", "2000"))
SEED = 236
os.environ["CFG236_SUFFIX"] = f"_M{K}"
o = c.Out("MUTATE")
c.header(o, f"CFG236 MUTATE M{K}")
T = c.load_numeric()
idx, cnt = c.sample(T)
C = c.get_cols(T, idx)
z = C["z"]
zmed = float(np.median(z))
DAT = c.dat_available()
if DAT:
    dat = c.load_dat(T, idx)
    gp = c.gperp_reading(dat["v1"], C["Re"], C["incl"], "a")


def slopes(cfg, mode, label, Zaxis=None, zcfg=None):
    cfg = dict(cfg)
    cfg["mode"] = mode
    if mode == "R199":
        cfg["gperp"] = gp
    R = c.routes(C, cfg)
    cols = {r: np.log10(R["a0_" + r]) for r in ("i", "ii", "iii")}
    zz = z if Zaxis is None else Zaxis
    st, bs = c.slope_table(zz, cols, B, SEED, {"d": ("i", "ii")})
    o.P(f"[{mode} {label}] n={[st[r]['n'] for r in 'i ii iii'.split()]} b_i {st['i']['b']:+.3f} [{st['i']['lo']:+.3f},{st['i']['hi']:+.3f}]  "
        f"b_ii {st['ii']['b']:+.3f} [{st['ii']['lo']:+.3f},{st['ii']['hi']:+.3f}]  b_iii {st['iii']['b']:+.3f}  Delta b {st['d']['b']:+.3f}")
    return st, R


modes = ["R198"] + (["R199"] if DAT else [])
bite = False
o.res["M"] = K
for mode in modes:
    base, Rb = slopes({}, mode, "baseline")
    if K == 1:
        acc = 10 ** (0.30 * (z - zmed))
        st, _ = slopes(dict(accscale=acc), mode, "g x 10^(0.30 (z-zmed)) at fixed D")
        dshift = {r: st[r]["b"] - base[r]["b"] for r in ("i", "ii", "iii")}
        dd = st["d"]["b"] - base["d"]["b"]
        ok = all(abs(v - 0.30) <= 0.03 for v in dshift.values()) and abs(dd) <= 0.02
        o.P(f"   shifts {dshift}; Delta b change {dd:+.4f}; frozen prediction (+0.300 +- 0.03 each, Delta b within 0.02): {'as predicted' if ok else 'NOT as predicted'}")
        bite |= all(v >= 0.25 for v in dshift.values())
        o.res[mode] = dict(dshift=dshift, dd=dd, as_predicted=ok)
    elif K == 2:
        st, _ = slopes(dict(swap=True), mode, "routes swapped")
        flips = st["d"]["b"] > 0 and base["d"]["b"] < 0
        o.P(f"   Delta b {base['d']['b']:+.3f} -> {st['d']['b']:+.3f}; sign flips: {flips}; frozen prediction: +0.6 to +0.95")
        bite |= flips
        o.res[mode] = dict(d_base=base["d"]["b"], d_mut=st["d"]["b"], in_range=bool(0.6 <= st["d"]["b"] <= 0.95))
    elif K == 3:
        st, _ = slopes(dict(tau=0.72), mode, "SED M* bias tau=+0.72 dex/z (true = SED - tau (z-zmed))")
        ok1 = abs(st["d"]["b"]) <= 0.35
        ok2 = abs(st["ii"]["b"] - st["i"]["b"]) <= 0.40
        o.P(f"   |Delta b| {abs(st['d']['b']):.3f} <= 0.35: {ok1};  |b_ii - b_i| {abs(st['ii']['b']-st['i']['b']):.3f} <= 0.40: {ok2}")
        bite |= ok1
        o.res[mode] = dict(ok_d=bool(ok1), ok_b=bool(ok2), d=st["d"]["b"], bii=st["ii"]["b"])
    elif K == 4:
        if mode == "R198":
            o.P("   (drift term acts on R199 only)")
            continue
        gd1 = c.gperp_reading(dat["v1"], C["Re"], C["incl"], "a", dat["s1"], "D1")
        cfg = dict(mode="R199", gperp=gd1)
        R = c.routes(C, cfg)
        cols = {r: np.log10(R["a0_" + r]) for r in ("i", "ii", "iii")}
        st, _ = c.slope_table(z, cols, B, SEED, {"d": ("i", "ii")})
        di, dii, dd = st["i"]["b"] - base["i"]["b"], st["ii"]["b"] - base["ii"]["b"], st["d"]["b"] - base["d"]["b"]
        o.P(f"   drift D1 ON: b_i {base['i']['b']:+.3f}->{st['i']['b']:+.3f} ({di:+.3f}); b_ii ->{st['ii']['b']:+.3f} ({dii:+.3f}); Delta b change {dd:+.3f}; |di-dii| {abs(di-dii):.3f} (frozen < 0.02); |dd| < 0.03: {abs(dd)<0.03}")
        bite |= abs(di) >= 0.03
        o.res[mode] = dict(di=di, dii=dii, dd=dd)
    elif K == 5:
        rng = np.random.default_rng(2365)
        perm = rng.permutation(len(z))
        zs = z[perm]
        stA, _ = slopes({}, mode, "axis shuffled (a0, mu at true z)", Zaxis=zs)
        allz = all(abs(stA[r]["b"]) < 2 * stA[r]["sd"] for r in ("i", "ii", "iii"))
        d_star = C["logMfit"] - C["logMsed"]
        ds = c.theil_sen(zs, d_star)
        o.P(f"   axis shuffle: every |b| < 2 SD: {allz}; Delta* slope after shuffle {ds:+.3f}")
        # both shuffled: z used in mu too
        C2 = dict(C); C2["z"] = zs
        cfg = dict(mode=mode)
        if mode == "R199":
            cfg["gperp"] = gp
        R2 = c.routes(C2, cfg)
        cols = {r: np.log10(R2["a0_" + r]) for r in ("i", "ii", "iii")}
        st2, _ = c.slope_table(zs, cols, B, SEED)
        o.P(f"   both shuffled: b_i {st2['i']['b']:+.3f}, b_ii {st2['ii']['b']:+.3f}, b_iii {st2['iii']['b']:+.3f} (SD {st2['i']['sd']:.2f},{st2['ii']['sd']:.2f},{st2['iii']['sd']:.2f})")
        bite |= allz
        o.res[mode] = dict(axis_all_null=bool(allz), dstar=ds)
    elif K == 6:
        cols = {r: np.log10(Rb["a0_" + r]) for r in ("i", "ii", "iii")}
        zmax = z.max()
        res = {r: (c.theil_sen(z, cols[r]), c.theil_sen(-z, cols[r])) for r in cols}
        err = max(abs(a + b) for a, b in res.values())
        o.P(f"   [{mode}] Theil-Sen antisymmetry |b(z)+b(-z)| max {err:.2e}")
        bite |= err < 1e-10
        o.res[mode] = dict(err=err)
    elif K == 7:
        st, _ = slopes(dict(floor=1.5), mode, "D floor 1.5")
        dn = base["ii"]["n"] - st["ii"]["n"]
        o.P(f"   n(ii) {base['ii']['n']} -> {st['ii']['n']} (drop {dn}); b_ii {base['ii']['b']:+.3f} -> {st['ii']['b']:+.3f}")
        bite |= dn >= 10
        o.res[mode] = dict(dn=dn, bii=st["ii"]["b"])
o.P(f"MUTATE M{K}: control {'BITES' if bite else 'DOES NOT BITE'} (exit {1 if bite else 0})")
o.res["bites"] = bool(bite)
o.finish()
sys.exit(1 if bite else 0)

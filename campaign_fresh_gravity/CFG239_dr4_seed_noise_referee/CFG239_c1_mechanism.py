#!/usr/bin/env python3
"""CFG239 c1: claim (1) the stage-G vt_error_mc stream (C1a-C1f, MU2, MU3).  DR3 = code-path test only (Amdt 7(e)).
main: exit 0.  MUTATE=2|3: exit 1 when the control bites."""
import os, sys, subprocess, hashlib, time
import numpy as np
from scipy import stats
import CFG239_common as C

MUT = int(os.environ.get("MUTATE", "0"))
G = C.SEED


# ------------------------------------------------------------ tracer (C1a)
class TraceRNG:
    calls = []
    counter = 0
    def __init__(self, seed=None):
        TraceRNG.calls = []; TraceRNG.counter = 0
    def _take(self, name, shape):
        size = int(np.prod(shape)); s = TraceRNG.counter
        TraceRNG.counter += size
        TraceRNG.calls.append((name, tuple(np.atleast_1d(shape)), s))
        return (s + np.arange(size, dtype=float)).reshape(shape)
    def standard_normal(self, size):
        return self._take("standard_normal", size if hasattr(size, "__len__") else (size,))
    def random(self, size):
        return self._take("random", (size,))
    def choice(self, a, size):
        return self._take("choice", (size,))


def trace(B, mc, sel):
    with C.patched_rng(TraceRNG):
        with np.errstate(all="ignore"):
            mc.run(G, sel=sel)
    return list(TraceRNG.calls)


def slots(calls, n):
    """stamp of every (trial, block, pair, comp) slot -> dict block-key -> array (n, w)."""
    out = {}
    for c, (name, shape, s) in enumerate(calls):
        t, b = divmod(c, 6)
        w = shape[1] if len(shape) > 1 else 1
        out[(t, b)] = s + np.arange(shape[0] * w).reshape(shape[0], w)
    return out


# ------------------------------------------------------------ per-pair stream (C1e)
class PairRNG:
    """one generator per pair, SeedSequence([G, id1, id2]); serves the frozen call pattern."""
    ids = None
    def __init__(self, seed):
        id1, id2 = PairRNG.ids
        n = len(id1); T = 212
        self.n = n
        self.Z1 = np.empty((n, T, 3)); self.Z2 = np.empty((n, T, 3)); self.U = np.empty((n, T))
        self.SG = np.empty((n, T)); self.N1 = np.empty((n, T)); self.N2 = np.empty((n, T))
        for i in range(n):
            g = np.random.Generator(np.random.PCG64(np.random.SeedSequence([int(seed), int(id1[i]), int(id2[i])])))
            self.Z1[i] = g.standard_normal((T, 3)); self.Z2[i] = g.standard_normal((T, 3))
            self.U[i] = g.random(T); self.SG[i] = g.integers(0, 2, T) * 2.0 - 1.0
            self.N1[i] = g.standard_normal(T); self.N2[i] = g.standard_normal(T)
        self.c = 0
    def _nxt(self):
        t, b = divmod(self.c, 6); self.c += 1
        return t, b
    def standard_normal(self, size):
        t, b = self._nxt()
        shp = tuple(size) if hasattr(size, "__len__") else (size,)
        if b == 0: assert shp == (self.n, 3); return self.Z1[:, t, :]
        if b == 1: assert shp == (self.n, 3); return self.Z2[:, t, :]
        if b == 4: assert shp == (self.n,); return self.N1[:, t]
        if b == 5: assert shp == (self.n,); return self.N2[:, t]
        raise AssertionError("call order differs from the traced one")
    def random(self, size):
        t, b = self._nxt(); assert b == 2 and size == self.n; return self.U[:, t]
    def choice(self, a, size):
        t, b = self._nxt(); assert b == 3 and size == self.n; return self.SG[:, t]


def run_perpair(mc, seed, sel):
    PairRNG.ids = (mc.id1[sel], mc.id2[sel])
    with C.patched_rng(lambda s: PairRNG(s)):
        return mc.run(seed, sel=sel)


def relchg(a, b):
    return np.abs(b - a) / a


def child():
    B = C.load_builder(); arr = C.build_array(B, C.EXT / "stage_F.npz", "k0"); mc = C.MC(B, arr)
    s = mc.run(G)
    print(hashlib.sha256(s.tobytes()).hexdigest())


def main():
    if "--child" in sys.argv:
        return child()
    log = C.Tee(C.HERE / ("CFG239_c1_mechanism%s.out" % (f"_MUTATE{MUT}" if MUT else "")))
    log("CFG239 c1 mechanism | repo <repo> | DR3 = code-path test only (Amdt 7(e)) | MUTATE =", MUT)
    C.WORK.mkdir(exist_ok=True)
    h0 = C.guard(); log("guard ok: builder", h0[0][:12], "pipeline", h0[1][:12])
    B = C.load_builder()
    arr = C.build_array(B, C.EXT / "stage_F.npz", "k0"); mc = C.MC(B, arr)
    n = len(arr["a"]); log("array U:", n, "pairs; uncovered correlation id entries (zero-filled):", mc.n_unc)
    rng = np.random.default_rng(239)
    res = {"n": n}

    if MUT in (2, 3):
        # mutated controls: assert the per-pair claim on the SEQUENTIAL stream; it must fail
        sel = np.arange(400)
        base = mc.run(G, sel=sel)
        if MUT == 2:
            sub = np.delete(sel, 200); other = mc.run(G, sel=sub); ref = np.delete(base, 200)
        else:
            perm = rng.permutation(400); other_p = mc.run(G, sel=sel[perm]); other = other_p[np.argsort(perm)]; ref = base
        changed = float(np.mean(other != ref))
        log(f"MUTATE{MUT}: sequential stream, changed fraction = {changed:.4f}; assertion 'no other pair changes' ",
            "holds" if changed == 0 else "FAILS")
        bites = changed > 0
        log("control bites (exit 1)" if bites else "control toothless (exit 0)")
        sys.exit(1 if bites else 0)

    # ------------------------------ C1a trace
    log("\n[C1a] dummy-RNG stamp trace on a 50-pair slice")
    sel = np.arange(50)
    tr_full = trace(B, mc, sel)
    ok_seq = [(nm, sh) for nm, sh, _ in tr_full[:6]]
    log("  calls:", len(tr_full), "(expect 6 x 212 = 1272); first trial:", ok_seq)
    pat = [("standard_normal", (50, 3)), ("standard_normal", (50, 3)), ("random", (50,)), ("choice", (50,)),
           ("standard_normal", (50,)), ("standard_normal", (50,))]
    order_ok = len(tr_full) == 1272 and all(((nm, sh) == pat[c % 6]) for c, (nm, sh, _) in enumerate(tr_full))
    log("  call order/shapes as read from the source:", order_ok)
    res["trace_order_ok"] = bool(order_ok)
    sl0 = slots(tr_full, 50)
    for j, name in ((0, "first"), (25, "middle"), (49, "last")):
        sub = np.delete(sel, j)
        tr = trace(B, mc, sub)
        sl = slots(tr, 49)
        # pair i (orig index) maps to i if i<j else i-1 in the reduced run
        same = 0; tot = 0; pair_any = np.zeros(49, bool)
        for key in sl0:
            a0 = sl0[key]; a1 = sl[key]
            keep = np.delete(np.arange(50), j)
            eq = (a0[keep] == a1)
            eq = eq.all(axis=1) if eq.ndim == 2 else eq
            same += int(eq.sum()); tot += eq.size
            pair_any |= eq.all() if False else ~eq   # pair has at least one changed slot
        log(f"  remove {name} pair: slots with identical stamp {same}/{tot} = {same/tot:.5f}; "
            f"pairs with >=1 changed slot {pair_any.sum()}/49")
        res[f"trace_remove_{name}"] = dict(same=same, tot=tot, pairs_changed=int(pair_any.sum()))
    tr = trace(B, mc, sel[::-1].copy()); sl = slots(tr, 50)
    same = tot = 0
    for key in sl0:
        eq = (sl0[key][::-1] == sl[key]); eq = eq.all(axis=1) if eq.ndim == 2 else eq
        same += int(eq.sum()); tot += eq.size
    log(f"  reverse the 50 pairs: identical-stamp slots {same}/{tot} = {same/tot:.5f} (palindromic centre only)")
    res["trace_reverse_same_frac"] = same / tot

    # ------------------------------ C1b real stream removal
    log("\n[C1b] real stream (seed SEED), one-pair removal / reversal / permutation")
    pred_med, pred_p90 = 0.6745 * np.sqrt(2) / np.sqrt(2 * 211), 1.645 * np.sqrt(2) / np.sqrt(2 * 211)
    log(f"  predicted (independent re-draw): median {pred_med:.4f}, p90 {pred_p90:.4f}")
    out_b = {}
    allrel = {}
    for label, sel in (("slice2000", np.arange(2000)), ("full", np.arange(n))):
        base = mc.run(G, sel=sel); m = len(sel)
        for pos_name, pos in (("first", 0), ("middle", m // 2), ("last", m - 1)):
            sub = np.delete(sel, pos); s1 = mc.run(G, sel=sub); ref = np.delete(base, pos)
            r = relchg(ref, s1)
            d = dict(identical=float(np.mean(s1 == ref)), median=float(np.median(r)), p90=float(np.quantile(r, .9)))
            out_b[f"{label}_remove_{pos_name}"] = d
            allrel[f"{label}_remove_{pos_name}"] = r
            log(f"  {label:9s} remove {pos_name:6s}: bit-identical {d['identical']*100:.3f}%  median |rel| {d['median']:.4f}  p90 {d['p90']:.4f}")
        s1 = mc.run(G, sel=sel[::-1].copy())[::-1]
        r = relchg(base, s1); d = dict(identical=float(np.mean(s1 == base)), median=float(np.median(r)), p90=float(np.quantile(r, .9)))
        out_b[f"{label}_reverse"] = d
        log(f"  {label:9s} reversed     : bit-identical {d['identical']*100:.3f}%  median {d['median']:.4f}  p90 {d['p90']:.4f}")
        perm = rng.permutation(m); s1 = mc.run(G, sel=sel[perm]); s1 = s1[np.argsort(perm)]
        r = relchg(base, s1); d = dict(identical=float(np.mean(s1 == base)), median=float(np.median(r)), p90=float(np.quantile(r, .9)))
        out_b[f"{label}_permute"] = d
        log(f"  {label:9s} permuted     : bit-identical {d['identical']*100:.3f}%  median {d['median']:.4f}  p90 {d['p90']:.4f}")
    res["C1b"] = out_b

    # ------------------------------ C1c independent re-draw identification
    log("\n[C1c] removal change vs a different global seed (SEED+1) on the full array")
    base = mc.run(G); alt = mc.run(G + 1)
    r_seed = relchg(base, alt)
    sub = np.delete(np.arange(n), n // 2); r_rm = relchg(np.delete(base, n // 2), mc.run(G, sel=sub))
    ks = stats.ks_2samp(r_seed, r_rm)
    log(f"  seed change: median {np.median(r_seed):.4f} p90 {np.quantile(r_seed,.9):.4f}; removal: median {np.median(r_rm):.4f} "
        f"p90 {np.quantile(r_rm,.9):.4f}; KS D={ks.statistic:.4f} p={ks.pvalue:.3f}")
    res["C1c"] = dict(seed_median=float(np.median(r_seed)), rm_median=float(np.median(r_rm)), ks_p=float(ks.pvalue),
                      seed_p90=float(np.quantile(r_seed, .9)), rm_p90=float(np.quantile(r_rm, .9)))

    # ------------------------------ C1d catalogue consequence
    log("\n[C1d] final-pair flips caused by removing ONE pair (same seed) vs by a seed change")
    F0 = base_mask = mc.final_mask(base)
    d1 = {}
    for pos_name, pos in (("first", 0), ("middle", n // 2), ("last", n - 1)):
        sub = np.delete(np.arange(n), pos); s1 = mc.run(G, sel=sub)
        fm = np.zeros(n, bool); fm[sub] = mc.av_ok[sub] & (s1 <= mc.thr[sub])
        keep = np.ones(n, bool); keep[pos] = False
        one_way = int((F0 & ~fm & keep).sum()); rev = int((fm & ~F0 & keep).sum())
        d1[pos_name] = (one_way, rev)
        log(f"  remove {pos_name:6s}: one-way flips {one_way}, reverse {rev}")
    fm = mc.final_mask(alt)
    log(f"  seed SEED+1 (no removal): one-way {int((F0 & ~fm).sum())}, reverse {int((fm & ~F0).sum())}; final counts {F0.sum()} / {fm.sum()}")
    res["C1d"] = dict(removal=d1, seed=(int((F0 & ~fm).sum()), int((fm & ~F0).sum())))

    # ------------------------------ C1e per-pair stream
    log("\n[C1e] per-pair stream (SeedSequence([G, id1, id2])): removal / permutation / global seed")
    t0 = time.time()
    all_ = np.arange(n)
    pp0 = run_perpair(mc, G, all_); log(f"  per-pair MC on the full array: {time.time()-t0:.0f} s")
    e = {}
    for pos_name, pos in (("first", 0), ("middle", n // 2), ("last", n - 1)):
        sub = np.delete(all_, pos); s1 = run_perpair(mc, G, sub)
        e[f"remove_{pos_name}_changed"] = int((s1 != np.delete(pp0, pos)).sum())
    perm = rng.permutation(n); s1 = run_perpair(mc, G, all_[perm])[np.argsort(perm)]
    e["permute_changed"] = int((s1 != pp0).sum())
    log("  pairs whose sigma_vt changed: removal first/middle/last", [e[k] for k in e if k.startswith("remove")],
        "permutation", e["permute_changed"], "(expect 0 everywhere)")
    flips = []
    pp_masks = [mc.final_mask(pp0)]
    for k in range(1, 7):
        pp_masks.append(mc.final_mask(run_perpair(mc, G + k, all_)))
    for k in range(1, 7):
        flips.append(int((pp_masks[0] & ~pp_masks[k]).sum()))
    seq_masks = [mc.final_mask(mc.run(G + k)) for k in range(7)]
    flips_seq = [int((seq_masks[0] & ~seq_masks[k]).sum()) for k in range(1, 7)]
    log(f"  one-way flips vs a different GLOBAL seed (k=1..6): per-pair {flips} mean {np.mean(flips):.1f}; "
        f"sequential {flips_seq} mean {np.mean(flips_seq):.1f}")
    e["global_seed_flips_perpair"] = flips; e["global_seed_flips_seq"] = flips_seq
    res["C1e"] = e

    # ------------------------------ C1f determinism
    log("\n[C1f] determinism: same seed/array, thread settings")
    a = mc.run(G); b = mc.run(G); log("  in-process twice bit-identical:", bool(np.array_equal(a, b)))
    hs = {}
    for name, env in (("default", {}), ("threads1", dict(OMP_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", OPENBLAS_NUM_THREADS="1")),
                      ("omp8", dict(OMP_NUM_THREADS="8", VECLIB_MAXIMUM_THREADS="8"))):
        r = subprocess.run([sys.executable, "-B", str(C.HERE / "CFG239_c1_mechanism.py"), "--child"], capture_output=True, text=True,
                           env=dict(os.environ, **env))
        hs[name] = r.stdout.strip().splitlines()[-1] if r.returncode == 0 else "ERR " + r.stderr[-200:]
    mine = hashlib.sha256(a.tobytes()).hexdigest()
    log("  child hashes:", {k: v[:12] for k, v in hs.items()}, "| in-process", mine[:12])
    det = all(v == mine for v in hs.values()) and np.array_equal(a, b)
    log("  bit-identical across threads/processes:", det)
    res["C1f"] = dict(det=bool(det), hashes={k: v[:12] for k, v in hs.items()})

    # ------------------------------ assertions
    full = out_b
    checks = {
        "C1a order": order_ok,
        "C1b >=99.9% changed (all removals, reverse, permute; slice and full)": all(d["identical"] <= 0.001 for d in full.values()),
        "C1b median within 10% of 0.0465 (full, middle)": abs(full["full_remove_middle"]["median"] / pred_med - 1) < 0.10,
        "C1c KS p>=0.05": ks.pvalue >= 0.05,
        "C1d one-pair removal flips ~ seed-change level (>=100)": all(v[0] >= 100 for v in d1.values()),
        "C1e per-pair removal/permutation changed == 0": all(e[k] == 0 for k in e if k.startswith("remove") or k == "permute_changed"),
        "C1e global-seed flips persist (per-pair mean >= 100)": np.mean(flips) >= 100,
        "C1f determinism": det,
    }
    log("\nASSERTIONS")
    for k, v in checks.items():
        log(f"  [{'PASS' if v else 'FAIL'}] {k}")
    res["checks"] = {k: bool(v) for k, v in checks.items()}
    C.jdump(res, C.HERE / "CFG239_c1_mechanism.json")
    h1 = C.guard(); assert h1 == h0
    log("guard after run ok")
    sys.exit(0)


if __name__ == "__main__":
    main()

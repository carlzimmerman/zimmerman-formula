#!/usr/bin/env python3
"""SI3_nested_isolation (criteria 60575303a2): the hole term. Isolated-random and plain-random catalogues for KiDS's nested samples, and their stacks through P2's record path.
    OMP_NUM_THREADS=1 nice -n 15 python3 si3_hole.py cat <work_dir>
    OMP_NUM_THREADS=1 nice -n 15 python3 si3_hole.py measure <kids_source_cache> <work_dir> north|south
kappa = 1/2 FITTED; footings never pooled; the theory stays open."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import io, json, math, time, resource, contextlib
from itertools import chain
import numpy as np

T0 = time.time(); HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar"); F2SRC = os.path.join(REB, "F2_outer_lensing", "f2_outer_lensing.py"); P2F = os.path.join(REB, "P2_spec_isolated_lensing", "p2_spec_isolated_lensing.py")
SAMPLES = ("S10", "S20", "S30", "S_strict", "S_x300")
VETO = {"S10": (10.0, None), "S20": (20.0, None), "S30": (30.0, None), "S_strict": (30.0, 100.0), "S_x300": (30.0, 300.0)}     # F2 and CFG96: |dchi| window of the 3 Mpc veto; host-veto window
KI, KR, SEED = 4, 2, 20261031
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
def P(s=""): print(f"[{time.time() - T0:7.0f} s, {rss():.2f} GB] {s}", flush=True)


def f2_sections(TF):
    """F2's text: sections 1 and 4 (as X53 executes them), plus CENTRAL, Track B's definitions and samples up to its grading loop, plus the S_x300 sample."""
    s1 = TF[:TF.index("# ============================================================================ 2. K0")]
    s4 = TF[TF.index("# ============================================================================ 4. lens inventory"):TF.index("# ============================================================================ 5. Track A")]
    cen = 'CENTRAL = dict(h=H_NAT["mid"], dMs=0.0, dcold=0.0, fhot=0.5, ye="noclu", pz=1.0)'; assert TF.count(cen) == 1
    s6 = TF[TF.index("# ============================================================================ 6. Track B"):TF.index("TRACKB = {}\n")]
    a = TF.index("# (a) wider host-veto window"); b = TF.index('P(f"   (a) S_x300 = S30'); assert a < b
    return s1, s4, cen + "\n" + s6 + "\n" + TF[a:b]


def patch_edges(ra, dec, npatch=50):
    """agentK's assign_patches, with its quantile edges kept."""
    south = dec < -15.0; ra_u = np.where(south, (ra + 180.0) % 360.0, ra); E = []
    for m in (~south, south):
        q = np.quantile(ra_u[m], np.linspace(0, 1, npatch // 2 + 1)); q[0] -= 1e-6; q[-1] += 1e-6; E.append(q)
    return E


def apply_patches(ra, dec, E, npatch=50):
    south = dec < -15.0; ra_u = np.where(south, (ra + 180.0) % 360.0, ra); patch = np.zeros(len(ra), np.int64); off = 0
    for m, q in zip((~south, south), E):
        patch[m] = off + np.clip(np.searchsorted(q, ra_u[m], side="right") - 1, 0, npatch // 2 - 1); off += npatch // 2
    return patch


def run_cat(WORK):
    from astropy.io import fits
    from scipy.spatial import cKDTree
    s1, s4, extra = f2_sections(open(F2SRC).read()); NF = {"__file__": F2SRC, "__name__": "f2_ro"}; argv0 = sys.argv; sys.argv = [F2SRC]; buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(s1 + "\n" + s4 + "\n" + extra, F2SRC, "exec"), NF)
    sys.argv = argv0; P("F2 Track B text executed; its checks " + ", ".join(f"{k} {v}" for k, v in NF["CHK"].items()))
    LN, SAMP, LBIN, treeP, UL, iself, host, host300, lMP, chiH, zP, logMs, zl, uvec = (NF[k] for k in ("LN", "SAMP", "LBIN", "treeP", "UL", "iself", "host", "host300", "lMP", "chiP", "zP", "logMs70", "zl", "uvec"))
    chiL = np.array(LN["chi"], "f8"); UP = treeP.data
    T96 = open(os.path.join(REPO, "campaign_fresh_gravity", "CFG96_stage_stack.py")).read(); G96 = dict(np=np, c=2.998e8, Mpc=3.0857e22, H0=70 * 1e3 / 3.0857e22)
    exec(compile(T96[T96.index("def DC(z, n=2048):"):T96.index("def assign_patches")], "cfg96_dc", "exec"), G96); chiW = G96["DC"](zP)
    def veto_hits(U, z, chi, lm, W, hw, selfp=None, chunk=20000):
        """True where CFG96's 3 Mpc veto at window W (or F2's host veto at window hw, if given) fires."""
        hit = np.zeros(len(U), bool)
        for i0 in range(0, len(U), chunk):
            sl = slice(i0, min(len(U), i0 + chunk)); lists = treeP.query_ball_point(U[sl], r=3.0 / chi[sl]); n = len(lists)
            cnt = np.fromiter(map(len, lists), dtype=np.int64, count=n); js = np.fromiter(chain.from_iterable(lists), dtype=np.int64, count=int(cnt.sum())); k = np.repeat(np.arange(n), cnt)
            if selfp is not None:
                keep = js != selfp[sl][k]; js, k = js[keep], k[keep]
            lmk, chk = lm[sl][k], chi[sl][k]
            h = np.bincount(k[(lMP[js] > lmk - 1.0) & (np.abs(chk - chiW[js]) < W)], minlength=n) > 0
            if hw is not None:
                d = UP[js] - U[sl][k]; th = (1.0 + z[sl][k]) / chk
                h |= np.bincount(k[(lMP[js] >= lmk) & (np.abs(chiH[js] - chk) < hw) & (np.einsum("ij,ij->i", d, d) <= th * th)], minlength=n) > 0
            hit[sl] = h
        return hit
    # K_H2: the veto function on every real lens, with self-exclusion
    nl = len(zl); mism = {}
    mism["S10"] = int(np.sum(veto_hits(UL, zl, chiL, logMs, 10.0, None, iself) != ~SAMP["S10"]))
    mism["S20"] = int(np.sum(veto_hits(UL, zl, chiL, logMs, 20.0, None, iself) != ~SAMP["S20"]))
    mism["S30"] = int(np.sum(veto_hits(UL, zl, chiL, logMs, 30.0, None, iself) != ~SAMP["S30"]))
    mism["host"] = int(np.sum(veto_hits(UL, zl, chiL, logMs, 0.0, 100.0, iself) != host))
    mism["host300"] = int(np.sum(veto_hits(UL, zl, chiL, logMs, 0.0, 300.0, iself) != host300))
    kh2 = all(v == 0 for v in mism.values()); P(f"K_H2 veto on {nl:,} real lenses, mismatches {mism}: {'PASS' if kh2 else 'FAIL'}")
    # footprint: CFG903's rule
    bh = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample.fits"), memmap=True)[1].data
    ra = np.array(bh["RAJ2000"], "f8"); dec = np.array(bh["DECJ2000"], "f8"); masked = np.array(bh["masked"]); del bh
    treeA = cKDTree(uvec(ra, dec)); boxes = []; south = dec < -15.0
    for m in (~south, south):
        rau = np.where(dec[m] < -15.0, (ra[m] + 180.0) % 360.0, ra[m]); lo, hi = float(rau.min()), float(rau.max()); dlo, dhi = float(dec[m].min()), float(dec[m].max())
        boxes.append((lo, hi, dlo, dhi, np.radians(hi - lo) * (math.sin(math.radians(dhi)) - math.sin(math.radians(dlo)))))
    pbox = np.array([b[4] for b in boxes]); pbox /= pbox.sum(); CHR = 2 * math.sin(math.radians(4.0 / 60.0) / 2); P(f"footprint boxes {[tuple(round(x, 3) for x in b[:4]) for b in boxes]}; {len(ra):,} bright rows")
    def draw(rng, n):
        fb = rng.random(n) < pbox[1]; rr = np.empty(n); dd = np.empty(n)
        for q, b in enumerate(boxes):
            mm = fb if q == 1 else ~fb; lo, hi, dlo, dhi = b[:4]; rau = lo + (hi - lo) * rng.random(int(mm.sum()))
            sd = math.sin(math.radians(dlo)) + (math.sin(math.radians(dhi)) - math.sin(math.radians(dlo))) * rng.random(int(mm.sum()))
            rr[mm] = (rau - 180.0) % 360.0 if q == 1 else rau; dd[mm] = np.degrees(np.arcsin(sd))
        dist, nn = treeA.query(uvec(rr, dd), k=1); ok = (dist < CHR) & (masked[nn] == 0)
        return rr[ok], dd[ok], n
    SS = dict(zip([f"I_{s}" for s in SAMPLES] + [f"R_{s}" for s in SAMPLES], np.random.SeedSequence(SEED).spawn(10))); OKL = (LBIN >= 0) & (LBIN < 4); OUTC = {}; INFO = dict(criteria="60575303a2", K_H2=dict(mismatches=mism, ok=kh2), n_lens={s: int((SAMP[s] & OKL).sum()) for s in SAMPLES}, cats={})
    for kind, kk in (("I", KI), ("R", KR)):
        for s in SAMPLES:
            name = f"{kind}_{s}"; rng = np.random.default_rng(SS[name]); idx = np.where(SAMP[s] & OKL)[0]; target = kk * len(idx); W, hw = VETO[s]; got = 0; A, tried, tried_foot = [], 0, 0
            while got < target:
                rr, dd, nt = draw(rng, 100000); tried_foot += nt; li = idx[rng.integers(0, len(idx), len(rr))]; tried += len(rr)
                keep = np.ones(len(rr), bool) if kind == "R" else ~veto_hits(uvec(rr, dd), zl[li], chiL[li], logMs[li], W, hw)
                A.append((rr[keep], dd[keep], li[keep])); got += int(keep.sum())
            OUTC[name + "_ra"] = np.concatenate([a[0] for a in A])[:target]; OUTC[name + "_dec"] = np.concatenate([a[1] for a in A])[:target]; OUTC[name + "_li"] = np.concatenate([a[2] for a in A])[:target].astype(np.int32)
            INFO["cats"][name] = dict(n=target, accept_after_footprint=got / tried, footprint_accept=tried / tried_foot); P(f"{name}: {target:,} points; veto acceptance {got / tried:.3f}, footprint acceptance {tried / tried_foot:.3f}")
    np.savez(os.path.join(WORK, "si3_cats.tmp.npz"), **OUTC); os.replace(os.path.join(WORK, "si3_cats.tmp.npz"), os.path.join(WORK, "si3_cats.npz"))
    json.dump(INFO, open(os.path.join(WORK, "si3_cats.json"), "w"), indent=1); P(f"catalogues written; total {sum(c['n'] for c in INFO['cats'].values()):,} points")


def run_measure(CACHE, WORK, REGION):
    T = open(P2F).read(); a = T.index("def ranges_for(ra, de, th_deg):"); b = T.index("# F1 conventions (K0a), copied from"); code = T[a:b]
    def rep(x, y):
        nonlocal code
        assert code.count(x) == 1, x; code = code.replace(x, y)
    # the record's rule: a centre with fewer than 5 background sources contributes nothing (CFG110's stage)
    rep("    n = len(cra)\n", "    n = len(cra); _NBACK = np.zeros(n, np.int64)\n")
    rep("            zs_all_rec = zs; cid_all_rec = cid\n", "            zs_all_rec = zs; cid_all_rec = cid; _NBACK[i:j] = np.bincount(cid, minlength=j - i)\n")
    rep("    if MUT:\n        WG, WX = WX, WG", "    for _a in (WG, WX, WW, W2, NN): _a[_NBACK < 5] = 0.0\n    if MUT:\n        WG, WX = WX, WG")
    c0 = T.index("# record (CFG110) conventions (K0b)"); c1 = T.index("PHA = os.path.join(WORK")
    G = dict(np=np, G_SI=6.674e-11, C_SI=2.998e8, MSUN=1.989e30, MPC=3.0857e22, MUT=False, CELL=0.2, NRA=int(round(360 / 0.2)))
    exec(compile(T[c0:c1], "p2_record", "exec"), G); exec(compile(code, "p2_measure", "exec"), G)
    def npy_range(path, i0=None, i1=None):
        with open(path, "rb") as fh:
            ver = np.lib.format.read_magic(fh); shape, fo, dtype = np.lib.format._read_array_header(fh, ver); off = fh.tell(); i0 = 0 if i0 is None else i0; i1 = shape[0] if i1 is None else i1
            fh.seek(off + i0 * dtype.itemsize); return np.fromfile(fh, dtype=dtype, count=i1 - i0)
    cell = npy_range(os.path.join(CACHE, "cell.npy")); assert np.all(cell[1:] >= cell[:-1]); isp = int(np.searchsorted(cell, np.int32(int(np.floor((-15.0 + 90) / 0.2)) * G["NRA"])))
    i0, i1 = (isp, len(cell)) if REGION == "north" else (0, isp); cs = cell[i0:i1]; del cell
    SRC = {k: npy_range(os.path.join(CACHE, f"{k}.npy"), i0, i1) for k in ("ra", "dec", "e1", "e2", "w", "zb")}
    CSTART = np.r_[0, np.flatnonzero(cs[1:] != cs[:-1]) + 1]; UCELL = cs[CSTART].copy(); CEND = np.r_[CSTART[1:], len(cs)]; G.update(SRC=SRC, UCELL=UCELL, CSTART=CSTART, CEND=CEND); nsrc = len(cs); del cs
    P(f"{REGION}: {nsrc:,} sources; dec range {SRC['dec'].min():.2f} to {SRC['dec'].max():.2f}")
    LN = np.load(os.path.join(DATA, "lr_lenses.npz")); lra, ldec, lz, lchi, lM, llogM = (np.array(LN[k], "f8") for k in ("ra", "dec", "z", "chi", "Mgal", "logM"))
    STK = np.load(os.path.join(DATA, "cfg96_stack.npz")); E = patch_edges(lra, ldec); kh3a = bool(np.array_equal(apply_patches(lra, ldec, E), STK["patch"]))
    LBIN = np.digitize(llogM, [8.5, 10.3, 10.6, 10.8, 11.0001]) - 1; REG = (lambda de: de > -15.0) if REGION == "north" else (lambda de: de <= -15.0)
    measure = G["measure"]; WF = os.path.join(WORK, f"si3_hole_{REGION}.npz"); CATS = [f"I_{s}" for s in SAMPLES] + [f"R_{s}" for s in SAMPLES]
    if os.path.exists(WF):
        z_ = np.load(WF); SUM = {k: z_[k].copy() for k in z_.files if k != "progress_json"}; PROG = json.loads(str(z_["progress_json"])); P(f"resumed from checkpoint: {PROG}")
    else:
        SUM = {}; PROG = {}
    # K_H1: P2's record path on seeded real lenses against CFG110's and CFG116's per-lens arrays
    if "KH1_WGm" not in SUM:
        rk = np.sort(np.random.default_rng(SEED + 1).choice(len(lra), 3000, replace=False)); rk = rk[REG(ldec[rk])]; o = np.argsort(np.round(ldec[rk] / 2) * 1000 + lra[rk]); rk = rk[o]
        m = measure(lra[rk], ldec[rk], lz[rk], "record", extra=np.c_[lM[rk], lchi[rk]]); PL = np.load(os.path.join(DATA, "cfg110_perlens.npz")); WGr, WWr = PL["WG"][rk], PL["WW"][rk]; del PL; WXr = np.load(os.path.join(DATA, "cfg116_perlens.npz"))["WX"][rk]
        SUM.update(KH1_rk=rk, KH1_WGm=m["WG"].sum(0), KH1_WWm=m["WW"].sum(0), KH1_W2m=m["W2"].sum(0), KH1_WXm=m["WX"].sum(0), KH1_WGr=WGr.sum(0), KH1_WWr=WWr.sum(0), KH1_WXr=WXr.sum(0),
                   KH1_maxrelWW=np.array(float(np.max(np.abs(m["WW"] - WWr) / np.maximum(WWr, 1e-300) * (WWr > 0)))), KH1_nzero=np.array(int(np.sum((m["WW"] > 0) != (WWr > 0)))))
        del WGr, WWr, WXr; P(f"K_H1 piece: {len(rk):,} real lenses measured; max per-lens relative |dWW| {float(SUM['KH1_maxrelWW']):.1e}; cells where only one side is empty {int(SUM['KH1_nzero'])}")
    cat = np.load(os.path.join(WORK, "si3_cats.npz")); CH = 4000
    def save():
        tmp = WF + ".tmp.npz"; np.savez(tmp, progress_json=np.array(json.dumps(PROG)), **SUM); os.replace(tmp, WF)
    t_last = time.time()
    for name in CATS:
        if PROG.get(name, -1) == -2: continue
        ra = cat[name + "_ra"]; de = cat[name + "_dec"]; li = cat[name + "_li"]; half = np.arange(len(ra)) % 2; sel = np.where(REG(de))[0]; ra, de, li, half = ra[sel], de[sel], li[sel], half[sel]
        o = np.lexsort((ra, np.round(de)));  ra, de, li, half = ra[o], de[o], li[o], half[o]; pa = apply_patches(ra, de, E); lb = LBIN[li]; start = max(PROG.get(name, 0), 0)
        for k in ("WG", "WX", "WW", "NN"):
            SUM.setdefault(f"{name}_{k}", np.zeros((2, 50, 4, 15)))
        for c0 in range(start, len(ra), CH):
            c1 = min(len(ra), c0 + CH); j = li[c0:c1]; m = measure(ra[c0:c1], de[c0:c1], lz[j], "record", extra=np.c_[lM[j], lchi[j]]); ix = (half[c0:c1], pa[c0:c1], lb[c0:c1])
            for k in ("WG", "WX", "WW", "NN"):
                np.add.at(SUM[f"{name}_{k}"], ix, m[k])
            PROG[name] = c1
            if time.time() - t_last > 240:
                save(); t_last = time.time(); P(f"  {name}: {c1:,}/{len(ra):,}")
        PROG[name] = -2; save(); t_last = time.time(); P(f"{name}: {len(ra):,} centres in {REGION} done")
    SUM["kh3a"] = np.array(kh3a); save(); P(f"{REGION} complete; patch labels reproduce the June ones: {kh3a}")


if __name__ == "__main__":
    if sys.argv[1] == "cat":
        os.makedirs(sys.argv[2], exist_ok=True); run_cat(sys.argv[2])
    else:
        run_measure(sys.argv[2], sys.argv[3], sys.argv[4])

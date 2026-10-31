#!/usr/bin/env python3
"""SI3 AMENDMENT A2 (post-result; changes no frozen line): per-lens clones I_c. si3_hole.py's and si3_grade.py's own text with asserted replacements, so the footprint rule, veto, estimator and statistic are the frozen ones.
    OMP_NUM_THREADS=1 nice -n 15 python3 si3_a2.py cat <work_dir>
    OMP_NUM_THREADS=1 nice -n 15 python3 si3_a2.py measure <kids_source_cache> <work_dir> north|south
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 si3_a2.py grade <work_dir>
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 si3_a2.py noise <work_dir>
kappa = 1/2 FITTED; footings never pooled; cold dark energy is never a particle."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
AH = os.path.dirname(os.path.abspath(__file__)); SH = os.path.join(AH, "si3_hole.py"); SG = os.path.join(AH, "si3_grade.py"); MODE = sys.argv[1]
if MODE in ("cat", "measure"):
    src = open(SH).read(); src = src[:src.index('if __name__ == "__main__":')]
    def rep(a, b):
        global src
        assert src.count(a) == 1, a[:80]; src = src.replace(a, b)
    if MODE == "cat":
        a = src.index('    SS = dict(zip([f"I_{s}" for s in SAMPLES]'); b = src.index("def run_measure(CACHE, WORK, REGION):")
        NEW = '''    OKL = (LBIN >= 0) & (LBIN < 4); OUTC = {}; INFO = dict(criteria="60575303a2", amendment="A2", K_H2=dict(mismatches=mism, ok=kh2), n_lens={s: int((SAMP[s] & OKL).sum()) for s in SAMPLES}, cats={})
    SS = dict(zip(SAMPLES, np.random.SeedSequence(SEED + 3).spawn(5))); KEEP, CAP = 4, 100000
    for s in SAMPLES:
        rng = np.random.default_rng(SS[s]); idx = np.where(SAMP[s] & OKL)[0]; W, hw = VETO[s]; RA = np.full((len(idx), KEEP), np.nan); DE = RA.copy(); have = np.zeros(len(idx), np.int64); tries = np.zeros(len(idx), np.int64)
        while True:
            act = np.where((have < KEEP) & (tries < CAP))[0]
            if len(act) == 0: break
            rr, dd, _n = draw(rng, max(2000, int(len(act) / 0.5))); who = act[np.arange(len(rr)) % len(act)]; li = idx[who]; tries += np.bincount(who, minlength=len(idx))
            ok = ~veto_hits(uvec(rr, dd), zl[li], chiL[li], logMs[li], W, hw)
            for k_, ra_, de_ in zip(who[ok], rr[ok], dd[ok]):
                if have[k_] < KEEP: RA[k_, have[k_]] = ra_; DE[k_, have[k_]] = de_; have[k_] += 1
        fill = np.isfinite(RA); OUTC[f"I_{s}_ra"] = RA[fill]; OUTC[f"I_{s}_dec"] = DE[fill]; OUTC[f"I_{s}_li"] = np.repeat(idx, have).astype(np.int32)
        INFO["cats"][f"I_{s}"] = dict(n=int(fill.sum()), lenses_short=int(np.sum(have < KEEP)), lenses_empty=int(np.sum(have == 0)), draws=int(tries.sum()), max_draws_per_lens=int(tries.max()))
        P(f"I_{s}: {int(fill.sum()):,} points for {len(idx):,} lenses; {int(tries.sum()):,} draws after footprint; most draws for one lens {int(tries.max()):,}; lenses short of 4: {int(np.sum(have < KEEP))}; with none: {int(np.sum(have == 0))}")
    np.savez(os.path.join(WORK, "si3_cats_a2.tmp.npz"), **OUTC); os.replace(os.path.join(WORK, "si3_cats_a2.tmp.npz"), os.path.join(WORK, "si3_cats_a2.npz"))
    json.dump(INFO, open(os.path.join(WORK, "si3_cats_a2.json"), "w"), indent=1); P("A2 catalogues written")
'''
        src = src[:a] + NEW + "\n\n" + src[b:]
        G = {"__file__": SH, "__name__": "si3_hole_a2"}; exec(compile(src, SH, "exec"), G); os.makedirs(sys.argv[2], exist_ok=True); G["run_cat"](sys.argv[2])
    else:
        rep('WF = os.path.join(WORK, f"si3_hole_{REGION}.npz"); CATS = [f"I_{s}" for s in SAMPLES] + [f"R_{s}" for s in SAMPLES]', 'WF = os.path.join(WORK, f"si3_a2_{REGION}.npz"); CATS = [f"I_{s}" for s in SAMPLES]')
        rep('cat = np.load(os.path.join(WORK, "si3_cats.npz")); CH = 4000', 'cat = np.load(os.path.join(WORK, "si3_cats_a2.npz")); CH = 4000')
        G = {"__file__": SH, "__name__": "si3_hole_a2"}; exec(compile(src, SH, "exec"), G); G["run_measure"](sys.argv[2], sys.argv[3], sys.argv[4])
else:
    gs = open(SG).read()
    def grep_(a, b):
        global gs
        assert gs.count(a) == 1, a[:80]; gs = gs.replace(a, b)
    # I from the A2 files and catalogue; R, estimator check and veto check as in the frozen run; nothing else
    grep_('        HOLE[c] = {k: Zs[0][f"{c}_{k}"] + Zs[1][f"{c}_{k}"] for k in ("WG", "WX", "WW", "NN")}\n',
          '        HOLE[c] = {k: (ZA[0] if c[0] == "I" else Zs[0])[f"{c}_{k}"] + (ZA[1] if c[0] == "I" else Zs[1])[f"{c}_{k}"] for k in ("WG", "WX", "WW", "NN")}\n')
    grep_('if HAVE:\n    for c in [f"I_{s}" for s in SAMPLES] + [f"R_{s}" for s in SAMPLES]:\n',
          'ZA = [dict(np.load(os.path.join(WORK, f"si3_a2_{r}.npz"))) for r in ("north", "south")]\nif HAVE:\n    for c in [f"I_{s}" for s in SAMPLES] + [f"R_{s}" for s in SAMPLES]:\n')
    grep_('INFOC = json.load(open(os.path.join(WORK, "si3_cats.json"))); RES["cats"] = INFOC["cats"]; cats = np.load(os.path.join(WORK, "si3_cats.npz"));',
          'INFOC = json.load(open(os.path.join(WORK, "si3_cats_a2.json"))); RES["cats"] = INFOC["cats"]; cats = np.load(os.path.join(WORK, "si3_cats_a2.npz"));')
    grep_('Q(f"SI3_nested_isolation  criteria 60575303a2{\'  [MUTATE: halo x 0.5, lens WG x 1.10, I from cross shear]\' if MUTS else \'\'}")', 'Q("SI3 AMENDMENT A2: post-result, reported only. I = per-lens clones I_c; every other line is si3_grade.py\'s own text. The frozen verdict stays NO VERDICT")')
    grep_('Q(f"\\nVERDICT (frozen; canonical, R2, Delta = L - I, S_strict): {VERD}")', 'Q(f"\\nA2 READING (post-result; the frozen rule on Delta_c = L - I_c; not the lane verdict): {VERD}")')
    grep_('VERD = "NO VERDICT (hole-term check failed)"', 'VERD = "NO READING (hole-term check failed on I_c)"')
    grep_('json.dump(RES, open(os.path.join(SHERE, f"si3_results{SFX}.json"), "w"), indent=1, default=float); open(os.path.join(SHERE, f"si3{SFX}.out"), "w").write("\\n".join(OUT) + "\\n")', 'json.dump(RES, open(os.path.join(SHERE, "si3_a2_results.json"), "w"), indent=1, default=float); open(os.path.join(SHERE, "si3_a2.out"), "w").write("\\n".join(OUT) + "\\n")')
    if MODE == "grade":
        __file__ = SG; sys.argv = [SG, sys.argv[2]]; exec(compile(gs, "si3_grade_a2", "exec"))
    else:   # "noise", reported only: how much of Delta_c's dchi2 is the random catalogue's own noise. Two halves of I_c, covariance and models fixed; jackknife of their difference
        CUTV = 'VARS = (("D", "Delta = L - I"), ("L", "raw L"))'; assert gs.count(CUTV) == 1
        __file__ = SG; sys.argv = [SG, sys.argv[2]]; exec(compile(gs[:gs.index(CUTV)], "si3_grade_a2_head", "exec"))
        OUT.clear(); F0 = json.load(open(os.path.join(SHERE, "si3_results.json")))["lines"]; NOI = {}; Q("SI3 AMENDMENT A2, reported only: I_c's own noise in dchi2, from its two halves. sig(I_c) = jackknife of half A - half B, over 2. Shift = dchi2 with I_c minus dchi2 with the frozen I")
        for foot in FOOTS:
            for rg in RUNGS:
                Q(f"[{foot} {rg}]")
                for s in SAMPLES:
                    d, dj, var = dvec(s, "D"); bk = blocks_J(d, dj, var, RALL); mL, mH = MS[foot][rg][s]["L"][0], MS[foot][rg][s]["H"][0]; dl, djl = ratio(LSUM[s]["sg"], LSUM[s]["sw"], fdat); da, dja = ratio(*hsum("I_" + s, half=0), fdat); db, djb = ratio(*hsum("I_" + s, half=1), fdat)
                    X = lambda v: chi2b(bk, v - mH) - chi2b(bk, v - mL); xa, xb, xf = X(dl - da), X(dl - db), X(d); dp = np.array([X(djl[p_] - dja[p_]) - X(djl[p_] - djb[p_]) for p_ in range(NP_)]); sg = 0.5 * math.sqrt(JKF * np.sum((dp - dp.mean()) ** 2)); f0 = F0[foot]["D"][rg][s]["all"]["dchi2"]
                    NOI[f"{foot}|{rg}|{s}"] = dict(dchi2=xf, half_A=xa, half_B=xb, sig_Ic=sg, frozen_dchi2=f0, shift=xf - f0); Q(f"  {s:8s} dchi2 {xf:+8.1f}; half A {xa:+8.1f}, half B {xb:+8.1f}; sig(I_c) {sg:5.1f}; frozen I {f0:+8.1f}; shift {xf - f0:+7.1f} ({(xf - f0) / (math.sqrt(2) * sg):+.1f} sigma of two such catalogues)")
        json.dump(NOI, open(os.path.join(SHERE, "si3_a2_noise.json"), "w"), indent=1, default=float); open(os.path.join(SHERE, "si3_a2_noise.out"), "w").write("\n".join(OUT) + "\n")

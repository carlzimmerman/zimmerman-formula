#!/usr/bin/env python3
"""HOT1 POST HOC checks, written by the lead on 2026-11-12 AFTER hot1.out and RESULT.md had been read.
Not graded. Changes no label. Nothing here is covered by FROZEN_CRITERIA.md.

Usage: python3 -I -B hot1_posthoc.py <path to MWS_BHB.fits>

Why: the frozen label is CLUMPED (L3), but L3's null shuffles velocities over the whole bin, so the pair
count also rises when the mean velocity or the dispersion merely differs from one part of the sky to
another. These checks ask which it is, and whether mean offsets across the sky carry the bin's heat.

  P1  independent recount of L3's observed pair count (haversine on l, b instead of unit-vector products).
  P2  L3 against a WITHIN-CELL null: velocities shuffled only among stars of the same HEALPix nside = 1 cell.
      That null keeps every cell's own velocity distribution and breaks only the association below a cell.
  P3  a dipole in v_gsr across the sky: least squares v = m + d . n_hat, permutation p of |d|, and the
      dispersion of the residuals.
  P4  cell means: permutation one-way test of the between-cell means, and the dispersion after each cell's
      own mean is removed.
P2 to P4 are run on the three inner bins. 5,000 permutations each. Seeds: P2 20261201 + bin index,
P3 20261210 + bin index, P4 20261220 + bin index.

The sample and estimators are hot1.py's own: this script parses hot1.py and executes only its import,
function-definition and constant statements (no top-level run, so hot1.py's outputs are not rewritten).
"""
import os, sys, ast, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
tree = ast.parse(open(os.path.join(HERE, "hot1.py")).read())
keep = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef))
        or (isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
            and n.targets[0].id in ("BINS", "NOMINAL", "NPERM"))]
H = {"FITS": sys.argv[1], "__name__": "hot1_functions"}
exec(compile(ast.Module(body=keep, type_ignores=[]), "hot1.py", "exec"), H)

OUT = open(os.path.join(HERE, "hot1_posthoc.out"), "w")
def say(s=""):
    print(s); OUT.write(s + "\n")
NPERM = 5000
F_OLD = (1.205, 1.155, 1.135, 1.114)
REC = {}

say("HOT1 POST HOC (lead, after the result; not graded; changes no label)")
D = H["load"](); S = H["build"](D, dict(H["NOMINAL"])); BINS = H["BINS"]
bidx = [np.where((S["r"] >= a) & (S["r"] < b))[0] for a, b in BINS]
counts = [len(x) for x in bidx]
d30 = H["fit_disp"](S["vgsr"][bidx[1]], S["verr"][bidx[1]])
ok = counts == [865, 264, 241, 125] and abs(d30["sigma"] - 106.74) <= 0.05
say(f"sample check: counts {counts}, 30-40 dispersion {d30['sigma']:.3f}: {'PASS' if ok else 'FAIL'}")
if not ok:
    say("STOP: sample check failed"); sys.exit(1)

def close_pairs(l, b, deg):
    l, b = np.radians(l), np.radians(b)
    dl = l[:, None] - l[None, :]; db = b[:, None] - b[None, :]
    hav = np.sin(db / 2) ** 2 + np.cos(b)[:, None] * np.cos(b)[None, :] * np.sin(dl / 2) ** 2
    sep = 2 * np.degrees(np.arcsin(np.sqrt(np.clip(hav, 0, 1))))
    return np.where(np.triu(sep < deg, k=1))

def count_pairs(V, i, j, dv, chunk=250):
    out = np.empty(V.shape[0])
    for s in range(0, V.shape[0], chunk):
        out[s:s + chunk] = np.sum(np.abs(V[s:s + chunk, i] - V[s:s + chunk, j]) < dv, axis=1)
    return out

def pge(null, obs): return float((1 + np.sum(null >= obs - 1e-12)) / (1 + len(null)))

for k in (1, 0, 2):
    a, b = BINS[k]; T = bidx[k]
    v, e, l, bb = S["vgsr"][T], S["verr"][T], S["l"][T], S["b"][T]
    cells = H["cell_of"](l, bb); X = H["gal_unit"](l, bb); N = len(v)
    full = H["fit_disp"](v, e)
    say(""); say("=" * 96)
    say(f"bin {a:.0f}-{b:.0f} kpc: N {N}, ML dispersion {full['sigma']:.2f} [{full['lo']:.2f}, {full['hi']:.2f}]"
        + ("   (TEST BIN)" if k == 1 else "   (control)"))
    say("=" * 96)

    # P1 and P2
    i, j = close_pairs(l, bb, 10.0)
    obs = float(np.sum(np.abs(v[i] - v[j]) < 30.0))
    say(f"P1 pairs < 10 deg: {len(i)}; of those within 30 km/s: {obs:.0f}"
        + ("   (hot1.out: 213 of 1125)" if k == 1 else ""))
    if k == 1 and (len(i) != 1125 or obs != 213):
        say("STOP: independent recount disagrees with hot1.out"); sys.exit(1)
    rng = np.random.default_rng(20261201 + k)
    PA = rng.permuted(np.tile(v, (NPERM, 1)), axis=1)
    PW = np.tile(v, (NPERM, 1))
    for c in np.unique(cells):
        m = np.where(cells == c)[0]
        if len(m) > 1: PW[:, m] = rng.permuted(np.tile(v[m], (NPERM, 1)), axis=1)
    nA = count_pairs(PA, i, j, 30.0); nW = count_pairs(PW, i, j, 30.0)
    say(f"P2 whole-bin null: mean {nA.mean():.1f}, p = {pge(nA, obs):.4f}   (hot1's null, new seed)")
    say(f"P2 WITHIN-CELL null: mean {nW.mean():.1f}, sd {nW.std():.1f}, p = {pge(nW, obs):.4f}")

    # P3 dipole
    A = np.hstack([np.ones((N, 1)), X]); pinv = np.linalg.pinv(A)
    co = pinv @ v; dvec = co[1:]; amp = float(np.linalg.norm(dvec))
    res = v - A @ co; fr = H["fit_disp"](res, e)
    rng = np.random.default_rng(20261210 + k)
    PV = rng.permuted(np.tile(v, (NPERM, 1)), axis=1)
    CO = PV @ pinv.T; ampn = np.linalg.norm(CO[:, 1:], axis=1)
    rmsn = np.sqrt(np.mean((PV - CO @ A.T) ** 2, axis=1)) / v.std()
    say(f"P3 dipole: |d| = {amp:.1f} km/s toward l {math.degrees(math.atan2(dvec[1], dvec[0])) % 360:.0f}, "
        f"b {math.degrees(math.asin(dvec[2] / amp)):+.0f}; monopole {co[0]:+.1f}; null mean |d| {ampn.mean():.1f}, p = {pge(ampn, amp):.4f}")
    say(f"   dispersion of the residuals: {fr['sigma']:.2f} [{fr['lo']:.2f}, {fr['hi']:.2f}] "
        f"(ratio to the bin {fr['sigma'] / full['sigma']:.4f}; a chance fit gives {rmsn.mean():.4f})")

    # P4 cell means (cells with >= 15 stars each; the rest pooled as one group)
    grp = cells.copy()
    for c in np.unique(cells):
        if np.sum(cells == c) < 15: grp[cells == c] = -1
    gl = [np.where(grp == g)[0] for g in np.unique(grp)]
    def within_ratio(V):
        ss = np.zeros(V.shape[0])
        for m in gl: ss += np.sum((V[:, m] - V[:, m].mean(1, keepdims=True)) ** 2, axis=1)
        return np.sqrt(ss / V.shape[1]) / V.std(1)
    r_obs = float(within_ratio(v[None])[0])
    rng = np.random.default_rng(20261220 + k)
    r_null = within_ratio(rng.permuted(np.tile(v, (NPERM, 1)), axis=1))
    p4 = float((1 + np.sum(r_null <= r_obs + 1e-12)) / (1 + NPERM))
    res4 = v.copy()
    for m in gl: res4[m] = v[m] - v[m].mean()
    f4 = H["fit_disp"](res4, e)
    say(f"P4 cell means ({len(gl)} groups): within-group rms / total rms = {r_obs:.4f}; chance {r_null.mean():.4f}; "
        f"p (between-cell means larger than chance) = {p4:.4f}")
    say(f"   dispersion with each group's own mean removed: {f4['sigma']:.2f} [{f4['lo']:.2f}, {f4['hi']:.2f}]")
    REC[k] = dict(asis=full, dipole=fr, cellmeans=f4)

say(""); say("=" * 96)
say("Like for like: the 30-40 bin against the mean of its two neighbours, all three treated the same way")
say("=" * 96)
for tag, lab in (("asis", "as measured"), ("dipole", "each bin's own dipole removed"), ("cellmeans", "each bin's cell means removed")):
    t, n0, n2 = REC[1][tag], REC[0][tag], REC[2][tag]
    nb = 0.5 * (n0["sigma"] + n2["sigma"]); ex = t["sigma"] - nb
    z = ex / math.sqrt(t["h"] ** 2 + (n0["h"] ** 2 + n2["h"] ** 2) / 4)
    say(f"  {lab:32s}: 30-40 {t['sigma']:7.2f}, neighbours' mean {nb:6.2f}, excess {ex:+6.2f} km/s, z = {z:.2f}; "
        f"RAW1 f rescaled by the 30-40 dispersion alone: " + ", ".join(f"{f * t['sigma'] / 106.74:.3f}" for f in F_OLD))
say("  The rescaled f values are not a correction: RAW1's predicted dispersion was not recomputed.")
say("")
say("Reading rule used by the lead (stated after the fact): if the within-cell null gives p > 0.05, the pair")
say("excess is carried by differences between cells in mean velocity or dispersion, not by clumps below a cell.")
say("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
OUT.close()

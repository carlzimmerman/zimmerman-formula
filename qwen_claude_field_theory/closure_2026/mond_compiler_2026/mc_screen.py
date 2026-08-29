"""
mc_screen.py -- the stage-1 screen: sample the coefficient space, run the gate chain,
log a per-gate mortality table, and report survivors.

Sampling families.  Pure random sampling over a 65-dimensional space would never land on
the fine-tuned surfaces where a survivor could live, so most of the budget goes to
TARGETED families that SOLVE for the tuning instead of hoping for it:

  RAND_SPARSE   k in [2,8] nonzero coefficients, log-uniform magnitudes    (baseline)
  RAND_DENSE    every coefficient nonzero                                  (baseline)
  MOND_SCAFFOLD a core that is KNOWN to pass G1/G3 (algebraic chi + polynomial potential)
                plus 1-3 random extra operators and a random matter frame
  FRAME_TUNED   scaffold + a candidate disformal partner, with ONE matter-frame parameter
                ROOT-FOUND so that the frame slip Phi~' - Psi~' vanishes at a reference
                Sigma.  Then the chain checks whether it stays zero at every other y.
                (this is the inverse-design move: solve for the tuning, do not sample it)
  SIGMAP_TUNED  scaffold + a stress-carrying operator, with ONE coefficient ROOT-FOUND so
                that the traceless stress Sigma_P vanishes at a reference Sigma; the chain
                then tests all the other y -- i.e. how many points can be zeroed at once
  DEGEN_TUNED   ONE coefficient ROOT-FOUND so that the kinetic Hessian acquires an extra
                null direction (det H = 0): the Palatini chi = -3/25 archetype generalised
  PALATINI      the connection-distortion subspace (A^2, chi A^2, div A, S nabla A, ...)
  NAMED         the named constructions and Gaussian neighbourhoods of them
"""
import argparse
import collections
import json
import os
import sys
import time

import numpy as np

import mc_gates as G
import mc_reduce_static as RS
from mc_basis import (N_OPS, N_PARAM, OP_INDEX, PARAM_IDS, NAMED, _vec, MFRAME,
                      basis_json)

HERE = os.path.dirname(os.path.abspath(__file__))

# operator groups used by the structured samplers
MOND_CORES = [
    dict(P2=-0.5, V3=1.0 / 3.0),                       # AQUAL, cubic potential
    dict(P2=-0.5, V3=1.0 / 3.0, V2=0.3),               # + quadratic (bends mu)
    dict(P2=-0.5, V3=1.0 / 3.0, V4=-0.2),
    dict(P3=-0.5, V4=0.25),                            # chi^2 X with quartic potential
    dict(P2=-0.5, V3=1.0 / 3.0, V1=0.1),
]
STRESS_OPS = ["P1", "P4", "P5", "P6", "P7", "P8", "K3", "K4", "K5", "K8", "K9",
              "K12", "K13", "K14", "C4", "C5", "C7", "C8", "V12", "V17", "D4", "D5"]
DISFORMAL_PARTNERS = {
    "vector": dict(ops=dict(V15=1.0, K4=-0.25), mkeys=["M5_disf_AA_phi", "M3_disf_AA"]),
    "tensor": dict(ops=dict(V18=1.0, K8=-0.5, K9=1.0), mkeys=["M6_disf_S_phi", "M4_disf_S"]),
    "tensor_alg": dict(ops=dict(V10=-1.0, V13=0.3), mkeys=["M6_disf_S_phi", "M4_disf_S"]),
    "scalar_grad": dict(ops={}, mkeys=["M7_disf_dphidphi", "M8_disf_dphidphi_phi"]),
    "vector_alg": dict(ops=dict(V6=-1.0, V9=0.25), mkeys=["M5_disf_AA_phi", "M3_disf_AA"]),
    "vec_tens": dict(ops=dict(V15=1.0, K4=-0.25, V12=0.5), mkeys=["M5_disf_AA_phi",
                                                                  "M6_disf_S_phi"]),
}
PALATINI_OPS = ["V6", "V7", "V8", "V9", "V12", "D1", "D2", "D3", "D4", "D5", "D8",
                "V1", "V2", "V3", "V4", "V15", "V16"]


def _mk(d):
    c = np.zeros(N_PARAM)
    for k, v in d.items():
        c[OP_INDEX[k]] = v
    return c


def _rand_mag(rng, n):
    return rng.choice([-1.0, 1.0], size=n) * 10.0 ** rng.uniform(-1.5, 1.5, size=n)


# ----------------------------------------------------------------------------------
# targeted tunings
# ----------------------------------------------------------------------------------

SIG_REF = 8.0


def _frame_slip_at(cvec, Sigma=SIG_REF):
    cext = np.concatenate([cvec[:N_OPS], [1.0]])
    mpar = cvec[N_OPS:]
    rng = np.random.default_rng(7)
    for X0 in G.initial_guesses(Sigma, None, 1.0, rng, n_rand=2):
        X, ok, d = G.solve_static(cext, mpar, Sigma, X0, tol=1e-9)
        if ok:
            ob = G.observables(X, mpar)
            if abs(ob["g_dyn"]) < 1e-300:
                return None
            return (ob["Phit1"] - ob["Psit1"]) / abs(ob["g_dyn"])
    return None


def _sigmaP_at(cvec, Sigma=SIG_REF):
    cext = np.concatenate([cvec[:N_OPS], [1.0]])
    mpar = cvec[N_OPS:]
    rng = np.random.default_rng(7)
    for X0 in G.initial_guesses(Sigma, None, 1.0, rng, n_rand=2):
        X, ok, d = G.solve_static(cext, mpar, Sigma, X0, tol=1e-9)
        if ok:
            Mv = np.asarray(G._rt()["Mfun"](*X), float).reshape(N_OPS + 1, RS.N_COL)
            parts = cext * Mv[:, RS.SIGP_COL]
            sc = float(np.abs(parts).max())
            return float(parts.sum()) / max(sc, 1e-300)
    return None


def _root_find(fun, c, idx, lo, hi, nscan=13, iters=45):
    """bracket-and-bisect on c[idx] to make fun(c) cross zero.

    The scan is LOG-spaced in |t| over both signs: the tunings that matter (Bekenstein's
    M5 = -4 relative to M1 = -1, say) live at O(1)-O(10) but the interesting corners can
    be small, and a linear scan of [-12, 12] misses them.
    """
    mag = np.logspace(-3, np.log10(max(abs(lo), abs(hi))), nscan // 2)
    ts = np.concatenate([-mag[::-1], [0.0], mag])
    vals = []
    for t in ts:
        c[idx] = t
        v = fun(c)
        vals.append(v)
    br = None
    for i in range(len(ts) - 1):
        a, b = vals[i], vals[i + 1]
        if a is None or b is None or not np.isfinite(a) or not np.isfinite(b):
            continue
        if a == 0.0:
            c[idx] = ts[i]
            return True
        if a * b < 0:
            br = (ts[i], ts[i + 1], a, b)
            break
    if br is None:
        return False
    lo_, hi_, fa, fb = br
    for _ in range(iters):
        mid = 0.5 * (lo_ + hi_)
        c[idx] = mid
        fm = fun(c)
        if fm is None or not np.isfinite(fm):
            return False
        if fa * fm <= 0:
            hi_, fb = mid, fm
        else:
            lo_, fa = mid, fm
        if abs(hi_ - lo_) < 1e-13 * max(1.0, abs(mid)):
            break
    c[idx] = 0.5 * (lo_ + hi_)
    return True


def _degen_tune(c, idx, lo, hi, rng=None):
    """EXACT tuning of c[idx] so the carrier Hessian acquires an extra null direction.

    H_AB is LINEAR in the coefficients, H(t) = H0 + t Hi, so det H(t) = 0 exactly at
    t = -lambda for the generalised eigenvalues of the pencil (H0, Hi).  This is the
    Palatini archetype's mechanism (3 + 25 chi = 0 annihilates the A-equation) solved
    rather than sampled -- no bracketing, no missed roots.
    """
    from scipy.linalg import eig
    H, _, _, _ = G.hess_tensors(G.REF_BG[1])
    c2 = c.copy()
    c2[idx] = 0.0
    H0 = np.einsum('i,iab->ab', c2[:N_OPS], H)
    Hi = H[idx]
    H0 = 0.5 * (H0 + H0.T)
    Hi = 0.5 * (Hi + Hi.T)
    if np.abs(Hi).max() < 1e-14:
        return False
    try:
        w = eig(H0, -Hi, right=False)
    except Exception:
        return False
    w = w[np.isfinite(w)]
    w = w[np.abs(w.imag) < 1e-9 * (1.0 + np.abs(w.real))].real
    w = w[(np.abs(w) > 1e-8) & (np.abs(w) < 1e4)]
    if w.size == 0:
        return False
    c[idx] = float(w[0] if rng is None else rng.choice(w))
    return True


# tolerance floor of the multi-point tuner.  It must NOT be tighter than what the static
# Newton solve itself can deliver (rel 1e-9 per equation, which propagates to ~1e-8 in the
# frame slip): a tighter value rejects genuinely converged tunings -- verified failure mode,
# it made the Bekenstein point itself report as "no 2-point tuning".
MULTI_TUNE_TOL = 1e-7


def _multi_tune(c, idxs, sigmas, iters=12, tol=MULTI_TUNE_TOL):
    """Simultaneously zero the frame slip at SEVERAL Sigma using len(idxs) parameters.

    This is the quantitative form of the no-go question: a one-parameter tuning can
    always kill the slip at ONE acceleration; the theory-level question is whether it can
    be killed at two (or more) at once, i.e. whether the zero is a curve in coefficient
    space or an isolated point.  Damped Newton with a finite-difference Jacobian.
    """
    idxs = list(idxs)
    n = len(idxs)
    m = len(sigmas)

    def F(cc):
        out = []
        for S in sigmas:
            v = _frame_slip_at(cc, S)
            if v is None or not np.isfinite(v):
                return None
            out.append(v)
        return np.array(out)

    F0 = F(c)
    if F0 is None:
        return False
    for _ in range(iters):
        if float(np.max(np.abs(F0))) < tol:
            return True
        J = np.zeros((m, n))
        for k, i in enumerate(idxs):
            h = 1e-5 * max(1.0, abs(c[i]))
            cp = c.copy(); cp[i] += h
            Fp = F(cp)
            if Fp is None:
                return False
            J[:, k] = (Fp - F0) / h
        try:
            dx, *_ = np.linalg.lstsq(J, -F0, rcond=None)
        except np.linalg.LinAlgError:
            return False
        if not np.all(np.isfinite(dx)):
            return False
        nrm = np.linalg.norm(dx)
        if nrm > 5.0:
            dx *= 5.0 / nrm
        best = None
        for a in (1.0, 0.5, 0.25, 0.1, 0.03):
            ct = c.copy()
            for k, i in enumerate(idxs):
                ct[i] += a * dx[k]
            Ft = F(ct)
            if Ft is not None and float(np.max(np.abs(Ft))) < float(np.max(np.abs(F0))):
                best = (ct, Ft)
                break
        if best is None:
            return False
        c[:] = best[0]
        F0 = best[1]
    return float(np.max(np.abs(F0))) < tol


# ----------------------------------------------------------------------------------
# candidate generators
# ----------------------------------------------------------------------------------

def gen_candidate(family, rng):
    c = np.zeros(N_PARAM)
    if family == "RAND_SPARSE":
        k = int(rng.integers(2, 9))
        idx = rng.choice(N_PARAM, size=k, replace=False)
        c[idx] = _rand_mag(rng, k)
        return c
    if family == "RAND_DENSE":
        c[:] = _rand_mag(rng, N_PARAM) * 0.3
        return c
    if family == "MOND_SCAFFOLD":
        c = _mk(MOND_CORES[int(rng.integers(len(MOND_CORES)))])
        k = int(rng.integers(1, 4))
        idx = rng.choice(N_OPS, size=k, replace=False)
        c[idx] += _rand_mag(rng, k)
        nm = int(rng.integers(1, 4))
        midx = rng.choice(len(MFRAME), size=nm, replace=False)
        c[N_OPS + midx] = _rand_mag(rng, nm)
        return c
    if family == "FRAME_TUNED":
        c = _mk(MOND_CORES[int(rng.integers(len(MOND_CORES)))])
        key = list(DISFORMAL_PARTNERS)[int(rng.integers(len(DISFORMAL_PARTNERS)))]
        part = DISFORMAL_PARTNERS[key]
        for k, v in part["ops"].items():
            c[OP_INDEX[k]] = v
        if rng.random() < 0.5:
            j = int(rng.integers(N_OPS))
            c[j] += float(_rand_mag(rng, 1)[0])
        c[N_OPS + MFRAME.index("M1_conf_phi")] = float(rng.choice([-1.0, 1.0])) * \
            10.0 ** rng.uniform(-0.5, 0.5)
        tk = part["mkeys"][int(rng.integers(len(part["mkeys"])))]
        tidx = N_OPS + MFRAME.index(tk)
        ok = _root_find(_frame_slip_at, c, tidx, -30.0, 30.0, nscan=17)
        return c if ok else None
    if family == "FRAME_TUNED2":
        c = _mk(MOND_CORES[int(rng.integers(len(MOND_CORES)))])
        key = list(DISFORMAL_PARTNERS)[int(rng.integers(len(DISFORMAL_PARTNERS)))]
        part = DISFORMAL_PARTNERS[key]
        for k, v in part["ops"].items():
            c[OP_INDEX[k]] = v
        c[N_OPS + MFRAME.index("M1_conf_phi")] = float(rng.choice([-1.0, 1.0])) * \
            10.0 ** rng.uniform(-0.4, 0.4)
        free = [N_OPS + MFRAME.index(k) for k in part["mkeys"]]
        if len(free) < 2:
            free.append(N_OPS + MFRAME.index("M2_conf_chi"))
        for i in free:
            c[i] = float(rng.normal(scale=2.0))
        ok = _multi_tune(c, free[:2], [8.0e-3, 8.0e3])
        return c if ok else None
    if family == "SIGMAP_TUNED":
        c = _mk(MOND_CORES[int(rng.integers(len(MOND_CORES)))])
        op = STRESS_OPS[int(rng.integers(len(STRESS_OPS)))]
        tidx = OP_INDEX[op]
        j = int(rng.integers(N_OPS))
        c[j] += float(_rand_mag(rng, 1)[0]) * 0.5
        nm = int(rng.integers(1, 3))
        midx = rng.choice(len(MFRAME), size=nm, replace=False)
        c[N_OPS + midx] = _rand_mag(rng, nm)
        ok = _root_find(_sigmaP_at, c, tidx, -30.0, 30.0, nscan=17)
        return c if ok else None
    if family == "DEGEN_TUNED":
        c = _mk(MOND_CORES[int(rng.integers(len(MOND_CORES)))])
        k = int(rng.integers(1, 4))
        idx = rng.choice(N_OPS, size=k, replace=False)
        c[idx] += _rand_mag(rng, k)
        nm = int(rng.integers(1, 4))
        midx = rng.choice(len(MFRAME), size=nm, replace=False)
        c[N_OPS + midx] = _rand_mag(rng, nm)
        tidx = int(rng.choice([OP_INDEX[o] for o in
                               ["P1", "P2", "P4", "P5", "P6", "K3", "K4", "K5",
                                "K8", "K9", "K12", "K13"]]))
        ok = _degen_tune(c, tidx, -8.0, 8.0, rng)
        return c if ok else None
    if family == "PALATINI":
        k = int(rng.integers(3, 8))
        ops = rng.choice(PALATINI_OPS, size=k, replace=False)
        for o in ops:
            c[OP_INDEX[o]] = float(_rand_mag(rng, 1)[0])
        c[OP_INDEX["V6"]] = 3.0
        c[OP_INDEX["V7"]] = 25.0
        if rng.random() < 0.7:
            c[OP_INDEX["P2"]] = -0.5
            c[OP_INDEX["V3"]] = 1.0 / 3.0
        nm = int(rng.integers(0, 4))
        if nm:
            midx = rng.choice(len(MFRAME), size=nm, replace=False)
            c[N_OPS + midx] = _rand_mag(rng, nm)
        return c
    if family == "NAMED":
        names = list(NAMED)
        c = _vec(NAMED[names[int(rng.integers(len(names)))]]).copy()
        if rng.random() < 0.85:
            c = c + rng.normal(scale=0.25, size=N_PARAM) * (np.abs(c) > 0)
            k = int(rng.integers(0, 3))
            if k:
                idx = rng.choice(N_PARAM, size=k, replace=False)
                c[idx] += _rand_mag(rng, k) * 0.3
        return c
    raise ValueError(family)


# ----------------------------------------------------------------------------------
# worker
# ----------------------------------------------------------------------------------

def _init():
    np.seterr(all='ignore')
    G._rt()


def _work(args):
    family, seed = args
    rng = np.random.default_rng(seed)
    try:
        c = gen_candidate(family, rng)
    except Exception as e:
        return dict(family=family, verdict="GEN_ERROR", note=str(e)[:120])
    if c is None:
        return dict(family=family, verdict="TUNING_FAILED", reason=family + ":no_root")
    if not np.all(np.isfinite(c)):
        return dict(family=family, verdict="GEN_ERROR", note="nonfinite")
    try:
        v, info = G.run_chain(c, rng=rng)
    except Exception as e:
        return dict(family=family, verdict="CHAIN_ERROR", note=f"{type(e).__name__}:{e}"[:160])
    out = dict(family=family, verdict=v,
               reason=str(info.get({"Gate-H": "H_pre", "Gate-CARRIER": "carrier",
                                    "Gate-MOND": "mond", "Gate-SLIP": "slip",
                                    "Gate-H2": "H2", "Gate-PPN": "ppn"}.get(v, "ppn"),
                                   ""))[:110])
    # keep the full vector for anything that got past Gate-MOND
    if v in ("SURVIVOR", "Gate-PPN", "Gate-H2", "Gate-SLIP"):
        out["cvec"] = [float(x) for x in c]
        out["info"] = {k: (float(x) if isinstance(x, (int, float, np.floating)) else str(x))
                       for k, x in info.items()}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=100000)
    ap.add_argument("--procs", type=int, default=os.cpu_count())
    ap.add_argument("--seed", type=int, default=20260829)
    ap.add_argument("--out", default=os.path.join(HERE, "screen_results.json"))
    ap.add_argument("--only", default=None,
                    help="restrict the screen to a single sampling family")
    args = ap.parse_args()

    mix = {"RAND_SPARSE": 0.30, "RAND_DENSE": 0.05, "MOND_SCAFFOLD": 0.20,
           "FRAME_TUNED": 0.15, "FRAME_TUNED2": 0.05, "SIGMAP_TUNED": 0.10,
           "DEGEN_TUNED": 0.08, "PALATINI": 0.05, "NAMED": 0.02}
    if args.only:
        mix = {args.only: 1.0}
    tasks = []
    rng = np.random.default_rng(args.seed)
    for fam, frac in mix.items():
        n = int(round(args.n * frac))
        for i in range(n):
            tasks.append((fam, int(rng.integers(1, 2**62))))
    rng.shuffle(tasks)
    print(f"basis: {N_OPS} operators + {len(MFRAME)} matter-frame parameters "
          f"= {N_PARAM} searchable coefficients")
    print(f"screening {len(tasks)} candidates on {args.procs} processes")
    with open(os.path.join(HERE, "basis.json"), "w") as fh:
        json.dump(basis_json(), fh, indent=2)

    t0 = time.time()
    mort = collections.Counter()
    fam_mort = collections.defaultdict(collections.Counter)
    reasons = collections.defaultdict(collections.Counter)
    keep = []
    import multiprocessing as mp
    with mp.Pool(args.procs, initializer=_init) as pool:
        for k, r in enumerate(pool.imap_unordered(_work, tasks, chunksize=8)):
            v = r["verdict"]
            mort[v] += 1
            fam_mort[r["family"]][v] += 1
            reasons[v][r.get("reason", "")] += 1
            if "cvec" in r:
                keep.append(r)
            if (k + 1) % 2000 == 0:
                el = time.time() - t0
                print(f"  {k+1}/{len(tasks)}  {el:.0f}s  "
                      f"({el/(k+1)*1000:.1f} ms/cand)  {dict(mort)}", flush=True)

    el = time.time() - t0
    survivors = [r for r in keep if r["verdict"] == "SURVIVOR"]
    out = dict(
        n_evaluated=len(tasks), wall_seconds=el,
        basis_size=dict(operators=N_OPS, matter_frame=len(MFRAME), total=N_PARAM),
        mortality=dict(mort),
        mortality_by_family={k: dict(v) for k, v in fam_mort.items()},
        reasons={k: dict(v.most_common(14)) for k, v in reasons.items()},
        n_survivors=len(survivors),
        survivors=survivors[:200],
        deep_candidates=[r for r in keep if r["verdict"] in ("Gate-PPN", "Gate-H2")][:200],
        param_ids=PARAM_IDS,
    )
    with open(args.out, "w") as fh:
        json.dump(out, fh, indent=2)
    print(f"\nDONE {len(tasks)} candidates in {el:.0f}s")
    print("MORTALITY:", dict(mort))
    for k, v in reasons.items():
        print(f"  {k}: {dict(v.most_common(8))}")
    print(f"SURVIVORS: {len(survivors)}")
    print(f"-> {args.out}")


if __name__ == "__main__":
    main()

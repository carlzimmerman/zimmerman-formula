"""CFG579 runner: executes CFG529's cfg529_score.py UNEDITED except three asserted run-time substitutions.
Env: CFG579_REGION in {ALL, NORTH, SOUTH}; CFG579_COV in {scaled, regionjk}. Criteria: FROZEN_CRITERIA.md (d2b13b22e).
Outputs: cfg579_<REGION>_<COV>.json / .out in this lane (CFG529's files are never written).
"""
import os, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, "..", "CFG529_f30_matched_environment", "cfg529_score.py"))
REGION = os.environ.get("CFG579_REGION", "ALL")
COV = os.environ.get("CFG579_COV", "scaled")
TAG = f"{REGION}_{COV}"
src = open(SRC).read()

subs = [
    ('F30 = np.load(os.path.join(DATA, "cfg96_isoflags.npz"))["f30"].astype(bool)',
     'F30 = np.load(os.path.join(DATA, "cfg96_isoflags.npz"))["f30"].astype(bool)\n'
     'F30_FULL = F30.copy()\n'
     'F30 = F30 & CFG579_REGMASK(lens)'),
    ('d30, C30 = esd_full_loo(WG, WW, patch, F30)',
     'd30, C30 = esd_full_loo(WG, WW, patch, F30)\n'
     'C30 = CFG579_COVFN(WG, WW, patch, F30, F30_FULL, C30, esd_full_loo, hart)'),
    ('json.dump(RES, open(os.path.join(HERE, f"cfg529_score_results{SUF}.json"), "w"), indent=1, default=float)',
     'json.dump(RES, open(os.path.join(CFG579_OUT, CFG579_TAG + ".json"), "w"), indent=1, default=float)'),
    ('open(os.path.join(HERE, f"cfg529_score{SUF}.out"), "w").write("\\n".join(LOG) + "\\n")',
     'open(os.path.join(CFG579_OUT, CFG579_TAG + ".out"), "w").write("\\n".join(LOG) + "\\n")'),
]
for a, b in subs:
    n = src.count(a)
    assert n == 1, f"C3 substitution must apply exactly once (found {n}): {a[:60]}"
    src = src.replace(a, b)


def regmask(lens):
    dec = np.asarray(lens["dec"])
    return {"ALL": np.ones(len(dec), bool), "NORTH": dec > -15.0, "SOUTH": dec < -15.0}[REGION]


def covfn(WG, WW, patch, F30, F30_FULL, C30_naive, esd_full_loo, hart):
    if REGION == "ALL":
        return C30_naive                                   # identity: CFG529's own covariance
    if COV == "scaled":
        _, CF = esd_full_loo(WG, WW, patch, F30_FULL)
        r = WW[F30_FULL].sum(0) / WW[F30].sum(0)
        return CF * np.sqrt(np.outer(r, r))
    # region-only jackknife over the occupied patches, Hartlap for that patch count
    KG = 1.98847e30 / (3.0857e16) ** 2
    occ = np.unique(patch[F30]); n = len(occ)
    wg = np.array([WG[F30 & (patch == q)].sum(0) for q in occ]); w = np.array([WW[F30 & (patch == q)].sum(0) for q in occ])
    tg, tw = wg.sum(0), w.sum(0)
    loo = (tg[None] - wg) / (tw[None] - w) / KG
    dev = loo - loo.mean(0)
    C = (n - 1) / n * dev.T @ dev
    h_n = (n - 15 - 2) / (n - 1)
    return C * hart(15) / h_n                              # the script divides by hart(15); net = C / h_n


ns = {"__file__": SRC, "__name__": "__main__", "CFG579_REGMASK": regmask, "CFG579_COVFN": covfn,
      "CFG579_OUT": HERE, "CFG579_TAG": f"cfg579_{TAG}"}
print(f"CFG579 run: region {REGION}, covariance {COV}; substitutions applied: {len(subs)}")
exec(compile(src, SRC, "exec"), ns)

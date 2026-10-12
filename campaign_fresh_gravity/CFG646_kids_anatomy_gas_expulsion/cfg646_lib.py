"""CFG646 shared loader: exec cfg596_native.py's library part UNCHANGED (everything before its run loop), which itself exec's
CFG592's library unchanged.  Returns the namespace plus helpers to rebuild CFG596's canonical (and test530) run dicts.
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.abspath(os.path.join(HERE, ".."))
SRC596 = os.path.join(CFG, "CFG596_lean_pm_1024", "cfg596_native.py")

def load_ns(test530=False):
    code = open(SRC596).read(); cut = code.index("def strip(r):")
    saved = list(sys.argv)
    sys.argv = [SRC596] + (["--test530"] if test530 else [])
    os.environ["CFG596_MUTATE"] = "0"
    NS = {"__file__": SRC596, "__name__": "cfg596_native_lib"}
    try:
        exec(compile(code[:cut], SRC596, "exec"), NS)
    finally:
        sys.argv = saved
    return NS

def KK_of(NS, bg="PM"):
    chi = NS["BG"][bg][0]; return (NS["LN"][:, None] + 0.5) / chi[None, :]

def runs(NS):
    """[(foot, run, held, extra, B0)] exactly as cfg596_native.py builds them."""
    out = []
    for foot, F, S, N, L in NS["runs_list"]():
        run, held, extra, B0 = NS["build"](F, S, N, L, foot, f"L{L:g}_N{N}_{foot}")
        out.append((foot, run, held, extra, B0, F, S))
    return out

def keep_mask(NS, Sv, run, PS0):
    f = NS["support_mask"](Sv, run, PS0); return Sv["pubkeep"] & (f >= 0.9)

def kfractions(NS, Sv, run, PS0, edges=(0.0, 0.3, 1.0, 2.0, np.inf), bg="PM"):
    """absolute-integrand fractions of every published point in k bins (support-mask construction: S0, nominal nuisances, no IA)
    and the median k (50% of the cumulative absolute integrand)."""
    x0, _, _, unpack, _ = NS["nuis_spec"](Sv, 1.0, False); par = unpack(x0)
    q, I, wchi = NS["G"]["kernels"](Sv, par["dz"], bg); KK = KK_of(NS, bg)
    PW = PS0 * wchi[None, :]
    def proj(mask):
        t = np.einsum("lj,aj,bj->abl", PW * mask, q, q); Ct = np.array([t[a - 1, b - 1] for a, b in Sv["pairs"]])
        fp = Ct @ Sv["Ap"].T; fm = Ct @ Sv["Am"].T
        return np.where(Sv["isp_all"], fp[Sv["ip_all"], Sv["ia_all"]], fm[Sv["ip_all"], Sv["ia_all"]])
    tot = proj(np.ones_like(KK))
    fr = [proj((KK >= lo) & (KK < hi)) / tot for lo, hi in zip(edges[:-1], edges[1:])]
    kg = np.geomspace(0.01, 50, 61); cum = np.array([proj(KK < kc) / tot for kc in kg])     # [kc, point]
    kmed = np.array([float(np.exp(np.interp(0.5, cum[:, i], np.log(kg)))) for i in range(cum.shape[1])])
    return np.array(fr), kmed

#!/usr/bin/env python3
"""CFG626: kernel re-check of CFG620 with the repaired nu_mono. FROZEN_CRITERIA.md (1c69c8300).

Thin driver: CFG620's cfg620.py / cfg620_lib.py are imported read only and executed unchanged; only the kernel is swapped.
  CFG626_KERNEL = mono (default) | exp
  CFG626_MODE   = main (CFG620 main run) | mutate (CFG620 MUTATE run; reads the same kernel's main JSON) | crep (C-REP control)
Kernel swap (mono): CFG544 nu_m1 (Mph_enc and everything built on it), CFG541 nu_m1 (Model: rho_ph, r_*, dW), the CFG544 copy
inside CFG550/CFG554, and CFG620's law_S (Part S). Cell geometry (r_*, f_ret, r_ta, M_cat, dW) from CFG541's own Model in both
modes. Outputs to ../_external_data/cfg626_work/<kernel or crep>/ (CFG620 output names); CFG620's folder is never written.
kappa = 1/2 FITTED; footings never pooled; candidate B; G9; no EFE; cold energy mass required; not "theory closed".
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg626.py      (2 processes)
"""
import os, sys, json, math
os.environ.setdefault("OMP_NUM_THREADS", "1")
KERNEL = os.environ.get("CFG626_KERNEL", "mono")
MODE = os.environ.get("CFG626_MODE", "main")
assert KERNEL in ("mono", "exp") and MODE in ("main", "mutate", "crep")
if MODE == "crep":
    assert KERNEL == "exp", "C-REP runs the exponential kernel"
os.environ["CFG620_MUTATE"] = "1" if MODE == "mutate" else "0"
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
D620 = os.path.join(HERE, "..", "CFG620_anisotropic_velocity_target")
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg626_work", "crep" if MODE == "crep" else KERNEL))
sys.path.insert(0, D620)
import cfg620 as C                                                               # noqa: E402  (read-only import, unchanged)

T544, M541 = C.T544, C.M541
J620 = json.load(open(os.path.join(D620, "cfg620_results.json")))

# ------------------------------------------------------------------ repaired nu_mono (verbatim from CFG596_lean_pm_1024/cfg596_pm.py)
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def dh_rar(y, e=1e-6):
    return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)
Y_P = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0); H_P = float(h_rar(Y_P)); DELTA = 0.05
LYG = np.linspace(-12, 12, 240001); YG = 10**LYG
DH_MONO = np.maximum(dh_rar(YG), DELTA * H_P / (YG + Y_P))
H_MONO = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH_MONO[1:] + DH_MONO[:-1]) * np.diff(YG))])
def nu_mono(y):
    y = np.maximum(np.asarray(y, float), 1e-12); return 1.0 + np.interp(np.log10(y), LYG, H_MONO) / y
# -------------------------------------------------------------------------------------------------------------------------------


def nu_m1_mono(y):
    """nu_mono(y) - 1, evaluated as H_MONO(y)/y (algebraically identical; no cancellation)."""
    y = np.maximum(np.asarray(y, float), 1e-12)
    return np.interp(np.log10(y), LYG, H_MONO) / y


def law_S_mono(b, R):
    """CFG620 law_S with the repaired kernel: units G = M_b = r_M = a0 = 1, y = g_N/a0 = M_b(r)/r^2."""
    def Mb(r):
        r = np.asarray(r, float); return np.ones_like(r) if b == 0 else r ** 2 / (r + b) ** 2
    def Mph(r):
        r = np.asarray(r, float); m = Mb(r); return m * nu_m1_mono(m / r ** 2)
    MR = float(Mph(np.array([R]))[0])
    def g(r):
        r = np.asarray(r, float); return (Mb(r) + np.where(r < R, Mph(np.minimum(r, R)), MR)) / r ** 2
    return Mb, Mph, g


_orig_hollow = C.hollow_toy
RPK_EXP_KPC = {k: (v["r_pk_toy"] * v["rstar_kpc"] if v.get("r_pk_toy") else None) for k, v in J620["cells"].items()}


def hollow_toy_626(c):
    """the kernel's own hollow; in mono mode, if none, CFG620's exponential r_pk at the same physical radius (inner region)."""
    own = _orig_hollow(c)
    if own is not None or KERNEL == "exp":
        return own
    rp = RPK_EXP_KPC.get(f"{c['sys']}_{c['foot']}")
    return None if rp is None else rp / c["rstar_kpc"]


if KERNEL == "mono":
    T544.nu_m1 = nu_m1_mono
    M541.nu_m1 = nu_m1_mono
    if hasattr(C.T554, "T550") and hasattr(C.T554.T550, "T544"):
        C.T554.T550.T544.nu_m1 = nu_m1_mono
    C.law_S = law_S_mono
    C.hollow_toy = hollow_toy_626
C.NPROC = 2
C.HERE = WORK


def j541_from_model():
    """CFG541's own Model with the active kernel: the fields CFG544's make_cell and CFG620's dW541 read from cfg541_results.json."""
    one = {}
    for foot, a0 in T544.FOOT.items():
        one[foot] = {}
        for s, d in T544.SYS.items():
            f = M541.fret_census(d["Mb"])[0]
            mod = M541.Model(d["Mb"], d["a_kpc"], a0, f)
            ran = mod.analytic_rstar()
            r = mod.run(alpha=1.0); m0 = mod.rhoc0 * mod.V
            Wi, _ = mod.energy(m0); Wf, _ = mod.energy(r["m"])
            one[foot][s] = dict(r_analytic_kpc=ran / M541.KPC, fret=f, rta_kpc=mod.rta / M541.KPC,
                                Mcat_over_Mb=mod.Mcat / mod.Mb, dW_per_mass=(Wi - Wf) / mod.Mcat)
    return {"one_d": one}


def kernel_check():
    """table accuracy of nu_mono against the exponential form below the repair (reported)."""
    y = np.geomspace(1e-8, 2.0, 2001)
    ex = 1.0 / np.expm1(np.sqrt(y))
    y2 = np.geomspace(2.0, 1e3, 400)
    return dict(Y_P=Y_P, H_P=H_P, DELTA=DELTA,
                max_rel_dev_nu_m1_y_le_2=float(np.max(np.abs(nu_m1_mono(y) / ex - 1))),
                first_y_dev_gt_1e3=float(y2[np.argmax(np.abs(nu_m1_mono(y2) * np.expm1(np.sqrt(y2)) - 1) > 1e-3)]),
                nu_ratio_mono_over_exp_at_y=[dict(y=float(v), ratio=float(nu_mono(v) / (1 + 1 / np.expm1(math.sqrt(v)))))
                                             for v in (1.0, 2.5, 5.0, 10.0, 30.0, 100.0, 1e3)])


def tag_res(J):
    C.RES["lane"] = "CFG626 (CFG620 pipeline, kernel swapped)" if KERNEL == "mono" else "CFG626 (CFG620 pipeline, exp kernel)"
    C.RES["criteria_commit"] = "1c69c8300 (CFG626); pipeline criteria 93abcbeb6 (CFG620, committed as CFG598)"
    C.RES["date"] = "2026-10-11"
    C.RES["settings"]["kernel"] = ("repaired nu_mono (cfg596_pm construction; Y_P %.4f, DELTA 0.05)" % Y_P if KERNEL == "mono"
                                   else "exponential RAR nu(y)=1/(1-exp(-sqrt y)) (CFG620's own functions)")
    C.RES["cfg626"] = dict(kernel=KERNEL, mode=MODE, kernel_check=kernel_check(), cell_source="CFG541 Model with the active kernel",
                           j541_model=J["one_d"])


def crep():
    """C-REP: exp kernel through this driver against CFG620's committed JSON."""
    os.makedirs(WORK, exist_ok=True)
    cells = C.all_cells()
    out = dict(lane="CFG626 C-REP", criteria_commit="1c69c8300", kernel="exp", cells={}, dW={}, partN={}, runs={})
    tol_rel, tol = 1e-12, 1e-9
    fails = []
    for k, c in cells.items():
        rec = {kk: vv for kk, vv in c.items() if kk not in ("Vf2_SI", "rstar_SI")}
        rec.update(C4=abs(float(C.Mph_enc(c, np.array([1.0]))[0]) / c["Mcat"] - 1), r99_analytic=T544.r99_analytic(c),
                   r_pk_toy=C.hollow_toy(c))
        ref = J620["cells"][k]; dev = {}
        for kk, vv in rec.items():
            rv = ref.get(kk)
            if isinstance(vv, (int, float)) and not isinstance(vv, bool) and isinstance(rv, (int, float)):
                dev[kk] = abs(vv - rv) / max(abs(rv), 1e-300)
            elif vv != rv:
                dev[kk] = f"mismatch {vv} vs {rv}"
        bad = {kk: v for kk, v in dev.items() if isinstance(v, str) or v > tol_rel}
        out["cells"][k] = dict(max_rel_dev=max([v for v in dev.values() if not isinstance(v, str)] or [0.0]), bad=bad)
        if bad: fails.append(f"cell {k}: {bad}")
        dw = C.dW541(k, c); rdw = J620["dW541"][k]
        out["dW"][k] = abs(dw - rdw) / abs(rdw)
        if out["dW"][k] > tol_rel: fails.append(f"dW {k}")
    out["CS"] = C.control_CS()
    for kk in ("bin_err", "maxdev_r_le_3", "maxdev_r_0p1_to_3"):
        if abs(out["CS"][kk] - J620["CS"][kk]) > tol: fails.append(f"CS {kk}")
    S = C.part_S(cells)
    out["partS"] = {}
    for k in cells:
        a, b = S[k], J620["partS"][k]; d = {}
        for kk in ("solver_err", "r_pk_over_rM", "beta_hollow_median", "beta_bulk_median", "edge_sr2_over_st2_last_bin"):
            if a[kk] is None or b[kk] is None:
                d[kk] = 0.0 if a[kk] == b[kk] else "mismatch"
            else:
                d[kk] = abs(a[kk] - b[kk])
        d["hollow_same"] = a["hollow"] == b["hollow"]
        lp = {kk: (a.get(kk), b.get(kk)) for kk in ("LP_ISO_hollow_dmin", "LP_ISO_outer_dmin", "LP_MIRROR_dmin", "LP_MIRROR_hollow_dmin")}
        und = {kk: (a.get(kk), b.get(kk)) for kk in a if kk.endswith("undetermined_LPs")}
        out["partS"][k] = dict(dev=d, LP=lp, LP_undetermined=und)
        if (not d["hollow_same"]) or any(isinstance(v, str) or (not isinstance(v, bool) and v > tol) for v in d.values()):
            fails.append(f"partS {k}: {d}")
    for k, c in cells.items():
        T = C.toy_target(c); rc = T["rc"]; bta = T["beta"]; sh = (rc > 0.1) & (rc < 0.9)
        ref = J620["partN"][k]
        d = dict(solver_err=abs(T["sol"]["err"] - ref["solver_err"]), beta_shell=abs(float(np.median(bta[sh])) - ref["beta_shell_median"]),
                 beta_edge=abs(float(bta[-1]) - ref["beta_edge_last_bin"]),
                 beta_inner=(abs(float(np.median(bta[rc < 0.05])) - ref["beta_inner_median"]) if ref["beta_inner_median"] is not None else 0.0))
        out["partN"][k] = d
        if max(d.values()) > tol: fails.append(f"partN {k}: {d}")
    jobs = [j for j in C.jobs_main(cells) if j["name"].split("|")[1] in ("A_C_a1.0", "b_C", "C2p_vlasov_F")]
    jobs.sort(key=lambda j: -C.cost(j))
    from multiprocessing import Pool
    with Pool(C.NPROC) as pool:
        res = pool.map(C.run, jobs, chunksize=1)
    keys = ("logXJ", "D", "dln_r99", "d_logXJ_last2", "d_D_last2", "sink", "H")
    for o in res:
        ref = J620["runs"][o["name"]]; md = 0.0; det = {}
        for tr, rd in o["reads"].items():
            rr = ref["reads"][tr]
            for kk in keys:
                if kk in rd or kk in rr:
                    dv = abs(rd[kk] - rr[kk]); det[f"{tr}:{kk}"] = dv; md = max(md, dv)
        out["runs"][o["name"]] = dict(max_abs_dev=md, mass_exact=o["mass_exact"], detail=det)
        if md > tol: fails.append(f"run {o['name']}: {md}")
    out["fails"] = fails; out["C_REP_pass"] = not fails
    json.dump(out, open(os.path.join(WORK, "cfg626_crep.json"), "w"), indent=1, default=str)
    print("C-REP", "PASS" if not fails else "FAIL", fails, flush=True)


def main():
    os.makedirs(WORK, exist_ok=True)
    J = j541_from_model()
    T544.J541 = J                                  # CFG544 make_cell and CFG620 dW541 read these (computed with the active kernel)
    if MODE == "crep":
        crep(); return
    tag_res(J)
    cells = C.all_cells()
    C.RES["cfg626"]["hollow_own_kernel"] = {k: _orig_hollow(c) for k, c in cells.items()}
    C.RES["cfg626"]["inner_region_fallback_r_over_rstar"] = {k: hollow_toy_626(c) for k, c in cells.items()} if KERNEL == "mono" else None
    C.main()


if __name__ == "__main__":
    main()

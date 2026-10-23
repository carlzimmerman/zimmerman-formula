#!/usr/bin/env python3
"""L1_khronon_pm production scorer (FROZEN_CRITERIA.md §5 + AMENDMENT A3 item 6): raw KiDS-1000 xi+- (DES reported) with the
CFG592 library exec'd unchanged and CFG596's node construction; Delta chi^2 (KX - S0) and (LIN - S0) at the same z_i.

  OMP_NUM_THREADS=1 nice -n 15 python3 l1_score.py [--dir work/prod]        -> l1_score<label>.out, l1_score<label>_results.json
  L1_MUTATE=1 ...  : the NZ1 control (S0 spectra through the F path) is replaced by S0 x 1.2 -> S3 must FAIL.
kappa = 1/2 FITTED; footings never pooled; never 'the data favour the framework'; no dark-matter particle."""
import os, sys, json, math, time, glob, argparse
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CFG = os.path.join(REPO, "campaign_fresh_gravity")
ap = argparse.ArgumentParser(); ap.add_argument("--dir", default=os.path.join(HERE, "work", "prod")); ap.add_argument("--label", default="")
args = ap.parse_args()
MUT = os.environ.get("L1_MUTATE", "0") == "1"; SUF = args.label + ("_MUTATE" if MUT else "")
sys.path.insert(0, HERE)
import khronon_pm as K
np.seterr(all="ignore")          # spurious FP flags from Accelerate's matmul inside the CFG592 library (results unaffected; F3 K0 reproduced CFG596 the same way)
OUT, RES, CHK = [], {"lane": "L1_khronon_pm", "part": "score", "dir": os.path.relpath(args.dir, HERE), "mutate": MUT}, {}
T0 = time.time()
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def check(name, ok, val, thr):
    CHK[name] = dict(ok=bool(ok), value=val, threshold=thr); P(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")

SRC = os.path.join(CFG, "CFG592_cosmic_shear_likelihood", "cfg592_native.py")
code = open(SRC).read(); cut = code.index("# ------------------------------------------------------------------ run\n")
G = {"__file__": SRC, "__name__": "cfg592_native_lib"}
exec(compile(code[:cut], SRC, "exec"), G)
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
SURV, Pmat, fit, support_mask, subset, nuis_spec, theory, klass, BG = (G[k] for k in ("SURV", "Pmat", "fit", "support_mask", "subset", "nuis_spec", "theory", "klass", "BG"))
from scipy.stats import chi2 as CH
P("L1_khronon_pm production scorer" + (" [MUTATE]" if MUT else "") + ": CFG592 library unchanged; CFG596 node construction; kappa = 1/2 FITTED; footings never pooled")

# model-B projection variant (F3 K3 style): background(Om_B), D(z) from the dust-limit ODE (radiation included)
bgB = K.MODEL_B
dsol = K.two_fluid(np.array([0.1]), None, bgB.Om, bgB.Ob, bgB.h, "dust", 1e-3, tuple(sorted(set(list(G["AG"]) + [0.5, 1.0]))))
_aa = sorted(set(list(G["AG"]) + [0.5, 1.0])); _D = np.array([(bgB.Ob * s[0][0] + bgB.Otau * s[1][0]) / bgB.Om for s in dsol]); _D /= _D[-1]
DgB = lambda a: float(np.interp(a, _aa, _D))
BG["NAT_B"] = G["background"](bgB.Om)
LIBSTATE = dict(Om=G["Om"], DZG=G["DZG"].copy(), Dgrow=G["Dgrow"])
def use_bg(bg):
    if bg == "NAT_B": G["Om"] = bgB.Om; G["DZG"] = np.array([DgB(a) for a in G["AG"]]); G["Dgrow"] = DgB
    else: G["Om"], G["DZG"], G["Dgrow"] = LIBSTATE["Om"], LIBSTATE["DZG"], LIBSTATE["Dgrow"]

ZK = {0.0: "z0", 0.5: "z0.5", 1.0: "z1"}
runs = {}
for fn in sorted(glob.glob(os.path.join(args.dir, "*", "result.json"))):
    r = json.load(open(fn))
    if r.get("status") != "done": continue
    runs[os.path.basename(os.path.dirname(fn))] = r
P(f"  completed runs found: {sorted(runs)}")
pairs = []
for tag, r in runs.items():
    c = r["cfg"]
    if c["mode"] in ("KX", "LIN"):
        s0 = [t for t, q in runs.items() if q["cfg"]["mode"] == "S0" and q["cfg"]["zi"] == c["zi"] and q["cfg"]["N"] == c["N"] and q["cfg"]["L"] == c["L"]]
        if s0: pairs.append((tag, s0[0]))
RES["pairs"] = pairs

def score_pair(Ftag, Stag):
    F, S = runs[Ftag], runs[Stag]; N, L = int(F["cfg"]["N"]), float(F["cfg"]["L"])
    k = np.array(F["snap"]["z0"]["k"]); assert np.allclose(k, np.array(S["snap"]["z0"]["k"]), rtol=1e-9)
    nodes = {z: (np.array(F["snap"][key]["P"]), np.array(S["snap"][key]["P"])) for z, key in ZK.items()}
    run = dict(name=Ftag, k=k, k_lo=float(k[0]), k_hi=float(math.pi * N / (4 * L)), B=np.ones_like(k), nodes=nodes)
    own = np.array(F["snap"]["z0"]["P"]) / np.array(S["snap"]["z0"]["P"])
    inj = lambda KK: np.exp(np.interp(np.log(np.clip(KK, k[0], run["k_hi"])), np.log(k), np.log(own)))
    out = dict(k_lo=run["k_lo"], k_hi=run["k_hi"], sigma8_F=F["snap"]["z0"]["sigma8"], sigma8_S0=S["snap"]["z0"]["sigma8"], bg={})
    for bg in (("PM",) if Ftag in ONLY_PM else ("PM", "NAT_B")):
        use_bg(bg)
        PS0 = Pmat(run, "S0", bg=bg); PF = Pmat(run, "F", bg=bg)
        F0 = Pmat(run, "S0", bg=bg) * (1.2 if MUT else 1.0)
        res_bg = {}
        for sn, Sv in SURV.items():
            f = support_mask(Sv, run, PS0, bg=bg); keep = Sv["pubkeep"] & (f >= 0.9); D = subset(Sv, keep)
            r = dict(N_kept=D["N"], N_published=int(Sv["pubkeep"].sum())); N_ok = D["N"] >= 10
            if D["N"] == 0:
                r["class"] = r["class_noIA"] = "NOT DIAGNOSTIC"; res_bg[sn] = r; continue
            fits = {}
            for ia in (True, False):
                s0 = fit(Sv, D, PS0, bg=bg, ia=ia); fF = fit(Sv, D, PF, bg=bg, ia=ia)
                fits["IA" if ia else "noIA"] = dict(S0=dict(chi2=s0["chi2"], chi2_data=s0["chi2_data"], A_IA=s0["A_IA"]),
                                                    F=dict(chi2=fF["chi2"], chi2_data=fF["chi2_data"], A_IA=fF["A_IA"]), dchi2=fF["chi2"] - s0["chi2"])
                if ia: s0best = s0
            d = fits["IA"]["dchi2"]
            rob = dict(widen2=fit(Sv, D, PF, bg=bg, widen=2.0)["chi2"] - fit(Sv, D, PS0, bg=bg, widen=2.0)["chi2"], noIA=fits["noIA"]["dchi2"])
            if bg == "PM":
                rob["DESI"] = fit(Sv, D, Pmat(run, "F", bg="DESI"), bg="DESI")["chi2"] - fit(Sv, D, Pmat(run, "S0", bg="DESI"), bg="DESI")["chi2"]
            rob_noIA = dict(widen2=fit(Sv, D, PF, bg=bg, widen=2.0, ia=False)["chi2"] - fit(Sv, D, PS0, bg=bg, widen=2.0, ia=False)["chi2"])
            cls = klass(d, list(rob.values()), N_ok); cls_noIA = klass(fits["noIA"]["dchi2"], list(rob_noIA.values()), N_ok)
            par = nuis_spec(Sv, 1.0, True)[3](np.array(s0best["x"]))
            mock = theory(Sv, D, par, Pmat(run, "S0", bg=bg, inject=inj), bg); town = fit(Sv, D, PS0, bg=bg, data=mock)["chi2"]
            if town < 9: cls = cls_noIA = "NOT DIAGNOSTIC"
            nz1 = abs(fit(Sv, D, F0, bg=bg)["chi2"] - fits["IA"]["S0"]["chi2"])
            r.update(fits=fits, dchi2=d, robust=rob, robust_noIA=rob_noIA, **{"class": cls}, class_noIA=cls_noIA, T_OWN_chi2=town,
                     T_OWN=bool(town >= 9), NZ1_absdchi2=nz1, p_S0=float(CH.sf(fits["IA"]["S0"]["chi2_data"], D["N"])),
                     p_F=float(CH.sf(fits["IA"]["F"]["chi2_data"], D["N"])))
            res_bg[sn] = r
            P(f"  {Ftag} vs {Stag} [{bg}] {sn}: N_kept {D['N']}; chi2 S0 {fits['IA']['S0']['chi2']:.2f}, F {fits['IA']['F']['chi2']:.2f} -> dchi2 {d:+.2f}; "
              f"robust {({a: round(b, 2) for a, b in rob.items()})}; T-OWN chi2 {town:.2f}; NZ1 |dchi2| {nz1:.1e} -> {cls} (noIA {cls_noIA})")
        out["bg"][bg] = res_bg
    use_bg("PM")
    return out
# S0 (reproduce the record first): CFG596 canonical P1 (F arm = P_grav) vs P0 (S0) through this scorer's own code path
W596 = os.path.join(G["EXT"], "cfg596_work")
def load596(job):
    f = glob.glob(os.path.join(W596, job, "cfg596_*.json")); return json.load(open(f[0])) if f else None
F596, S596 = load596("P1"), load596("P0")
runs["CFG596_P1_RES"] = dict(cfg=dict(mode="F", zi=49, N=int(F596["np"]), L=float(F596["L"])),
                             snap={key: dict(k=F596["snap"][key]["k"], P=F596["snap"][key]["P_grav"], sigma8=F596["snap"][key]["sigma8_grav"]) for key in ZK.values()})
runs["CFG596_P0_S0"] = dict(cfg=dict(mode="S0ref", zi=49, N=int(S596["np"]), L=float(S596["L"])),
                            snap={key: dict(k=S596["snap"][key]["k"], P=S596["snap"][key]["P"], sigma8=S596["snap"][key]["sigma8"]) for key in ZK.values()})
ONLY_PM = {"CFG596_P1_RES"}
SC = {}
rep = score_pair("CFG596_P1_RES", "CFG596_P0_S0")
ref = json.load(open(os.path.join(CFG, "CFG596_lean_pm_1024", "cfg596_native_results.json")))["runs"]["L100_N1024_canonical"]["surveys"]["KiDS"]
mine = rep["bg"]["PM"]["KiDS"]; r0 = (ref["fits"]["IA"]["S0"]["chi2"], ref["fits"]["IA"]["F"]["chi2"], ref["dchi2"])
m0 = (mine["fits"]["IA"]["S0"]["chi2"], mine["fits"]["IA"]["F"]["chi2"], mine["dchi2"]); dev = max(abs(a - b) for a, b in zip(m0, r0))
RES["S0_reproduce_CFG596"] = dict(mine=m0, record=r0, max_dev=dev, class_mine=mine["class"], class_record=ref.get("class"), N_kept=mine["N_kept"])
check("S0", dev <= 0.05, f"CFG596 canonical KiDS: S0 {m0[0]:.2f} F {m0[1]:.2f} dchi2 {m0[2]:+.2f} (record {r0[0]:.2f}/{r0[1]:.2f}/{r0[2]:+.2f}; "
      f"N_kept {mine['N_kept']}; class {mine['class']} vs record {ref.get('class')})", "max|dev| <= 0.05")
for Ft, St in pairs:
    SC[Ft] = score_pair(Ft, St); SC[Ft]["S0"] = St
RES["scores"] = SC
check("S1", len(pairs) > 0, f"{len(pairs)} pairs scored: {[p[0] for p in pairs]}", "at least one KX/LIN vs S0 pair")
check("S2", all("T_OWN_chi2" in s for v in SC.values() for b in v["bg"].values() for s in b.values() if s.get("N_kept", 0) > 0), "T-OWN computed for every kept-point set", "computed")
nz = [s["NZ1_absdchi2"] for v in SC.values() for b in v["bg"].values() for s in b.values() if "NZ1_absdchi2" in s]
nz += [s["NZ1_absdchi2"] for s in rep["bg"]["PM"].values() if "NZ1_absdchi2" in s]
check("S3", len(nz) > 0 and max(nz) <= 1e-6, f"max NZ1 |dchi2| {max(nz) if nz else float('nan'):.1e}", "S0 spectra through the F path give dchi2 = 0 (<= 1e-6)")
RES["checks"] = CHK; RES["runtime_s"] = time.time() - T0
npass = sum(v["ok"] for v in CHK.values()); ntot = len(CHK)
P(f"L1_SCORE COMPLETE: {npass}/{ntot} checks PASS.  ({RES['runtime_s']:.0f} s)")
K.atomic_json(os.path.join(HERE, f"l1_score{SUF}_results.json"), RES)
K.atomic_text(os.path.join(HERE, f"l1_score{SUF}.out"), "\n".join(OUT) + "\n")
sys.exit(0 if npass == ntot else 1)

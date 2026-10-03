#!/usr/bin/env python3
"""CFG303 R5 / A2.4 -- X-COP identity reading (CFG4_clusters, 0.946 +- 0.080) with the gas profile's radius decoded from R/R500 with
R500,FORW (solved from the forward hydrostatic mass) instead of the gas file's NFW-derived R500 (LCDM-MODEL).
The audit's own loader / profile builder (cluster_audit.run, no writing) and CFG4_clusters' cluster_table / summ, exec'd from committed source.
R500,FORW: M_FORW(<R) = 500 rho_c(z) (4 pi / 3) R^3, rho_c(z) for H0 = 70, Omega_m = 0.3, Omega_L = 0.7 (the X-COP release convention: geometry),
z from real_research/data/xcop/xcop_r500_ettori2019.json.
Frozen criteria: FROZEN_CRITERIA.md (52976ec22) + ADDENDUM_1 + ADDENDUM_2 (section A2.4), written before any native number was computed.
kappa = 1/2 FITTED.  The cold mass is still required (this is the cluster test of it); no dark-matter particle is added.
Run:  python3 campaign_fresh_gravity/CFG303_lcdm_free_inputs/cfg303_xcop_LCDMFREE.py
Outputs: cfg303_xcop_LCDMFREE.out, cfg303_xcop_LCDMFREE_results.json (this lane only).
"""
import os, sys, io, json, math, contextlib, time, hashlib, copy
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq

T0 = time.time()
LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
os.environ.pop("MUTATE", None)
OUT, CHK = [], []


def P(s=""):
    print(s, flush=True); OUT.append(s)


def check(name, val, ok):
    CHK.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


P(__doc__.split("Run:")[0].strip())
for f in ("FROZEN_CRITERIA.md", "FROZEN_CRITERIA_ADDENDUM_1.md", "FROZEN_CRITERIA_ADDENDUM_2.md"):
    P(f"  {f}: sha256 {sha(os.path.join(LANE, f))}")
FA = os.path.join(REPO, "qwen_claude_field_theory", "closure_2026", "cluster_measurement_audit_2026", "cluster_audit.py")
srcA = open(FA).read()
STOPA = "def json_safe(x):"
assert srcA.count(STOPA) == 1
nsA = {"__file__": FA, "__name__": "cfg303_exec"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(srcA[:srcA.index(STOPA)], "cluster_audit[defs]", "exec"), nsA)
F4 = os.path.join(CFG, "CFG4_clusters.py")
src4 = open(F4).read()
STOP4 = "TAB = {}"
assert src4.count(STOP4) == 1
sys.path.insert(0, CFG)
ns4 = {"__file__": F4, "__name__": "cfg303_exec"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src4[:src4.index(STOP4)], "CFG4_clusters[upto TAB]", "exec"), ns4)
P(f"  cluster_audit.py (sha {sha(FA)[:12]}) definitions and CFG4_clusters.py (sha {sha(F4)[:12]}) up to its table loop: exec'd")
C4, cluster_table, summ = ns4["C"], ns4["cluster_table"], ns4["summ"]
J4 = json.load(open(os.path.join(CFG, "CFG4_clusters_results.json")))
H2c = J4["numbers"]["H2"]
JZ = json.load(open(os.path.join(REPO, "real_research", "data", "xcop", "xcop_r500_ettori2019.json")))

# ----------------------------------------------------------------------------------------------- R500,FORW
G, MSUN, KPC = nsA["G"], nsA["MSUN"], nsA["KPC"]
MPC = KPC * 1e3


def rho_c(z, H0=70.0, Om=0.3, OL=0.7):
    H = H0 * 1e3 / MPC * math.sqrt(Om * (1 + z) ** 3 + OL)
    return 3 * H ** 2 / (8 * math.pi * G)


orig_load = nsA["load_cluster"]
R500F, R500H = {}, {}
for p in sorted(nsA["DATA"].iterdir()):
    if not p.is_dir():
        continue
    c = orig_load(p.name)
    z = JZ[p.name]["z"]
    rc = rho_c(z)
    f = lambda rk: math.log(nsA["loginterp"](np.array([rk]), c["rh"], c["M_FORW"])[0] * MSUN / (500 * rc * 4 / 3 * math.pi * (rk * KPC) ** 3))
    R500F[p.name] = brentq(f, c["rh"][1] * 1.0001, c["rh"][-1] * 0.9999, xtol=1e-6)
    R500H[p.name] = c["R500"]
P("\nR500 (kpc): the gas file's NFW-derived header value -> the forward-mass value")
P("  " + "; ".join(f"{n} {R500H[n]:.0f} -> {R500F[n]:.0f} ({math.log10(R500F[n] / R500H[n]):+.3f} dex)" for n in R500F))
rat = np.array([math.log10(R500F[n] / R500H[n]) for n in R500F])
P(f"  median log10(R500,FORW / R500,header) {np.median(rat):+.4f} dex (range {rat.min():+.3f} to {rat.max():+.3f})")


def run_with(R500map, scale=1.0, skip_pressure=False):
    """skip_pressure: the audit's pressure-gradient diagnostic (relaxed clusters only; it feeds no row) is skipped by emptying RELAXED for this call."""
    def load_patched(name):
        c = orig_load(name)
        if c["gas_unit"] == "R/R500":
            c["rg"] = c["rg"] / c["R500"] * R500map[name] * scale
            c["R500"] = R500map[name] * scale
        return c
    nsA["load_cluster"] = load_patched
    rel0 = nsA["RELAXED"]
    if skip_pressure:
        nsA["RELAXED"] = ()
    try:
        rep = nsA["run"]()
    finally:
        nsA["load_cluster"] = orig_load
        nsA["RELAXED"] = rel0
    return rep


def table_from(rep):
    A0a = rep["a0_m_s2"]
    rows = {}
    for rw in rep["rows"]:
        foot = rw.get("footing", "canonical")
        rows.setdefault(foot, {}).setdefault(rw["cluster"], []).append((float(rw["r_kpc"]), float(rw["g_baryon_over_a0"]) * A0a[foot], float(rw["g_hse_over_a0"]) * A0a[foot]))
    ns4["ROWS"] = rows
    ns4["R500"] = {d["name"]: d["own_R500_kpc"] for d in rep["radius_audit"]}
    out = {}
    for foot in C4.FOOTS:
        for kn, kf in (("P2", C4.nu_p2), ("nu_mono", C4.nu_mono)):
            t = cluster_table(kf, foot, 0.0)
            out[f"{foot}|{kn}"] = dict(eta=summ(t, "eta")[0], id_ratio=summ(t, "id_ratio")[0], id_sd=summ(t, "id_ratio")[1], resid=summ(t, "resid")[0],
                                       r_kpc=float(np.median([x["r_kpc"] for x in t])), frac_R500=float(np.median([x["frac_R500"] for x in t])))
    return out


P("\nCONTROLS")
AUD = json.load(open(os.path.join(REPO, "qwen_claude_field_theory", "closure_2026", "cluster_measurement_audit_2026", "results.json")))
t_c = table_from(AUD)
d_c = max(max(abs(t_c[k]["eta"] - H2c[k]["eta"]), abs(t_c[k]["id_ratio"] - H2c[k]["id_ratio"])) for k in H2c)
check("C-ii the committed audit rows through CFG4_clusters' exec'd cluster_table / summ reproduce CFG4_clusters' committed eta and identity ratio (4 cells)",
      f"max |diff| {d_c:.1e}", d_c <= 1e-9)
rep_h = run_with(R500H)
t_h = table_from(rep_h)
d_h = max(max(abs(t_h[k]["eta"] - H2c[k]["eta"]), abs(t_h[k]["id_ratio"] - H2c[k]["id_ratio"])) for k in H2c)
check("C-i the replacement path with R500 := the header value (audit run() in this process) reproduces the committed numbers", f"max |diff| {d_h:.1e}", d_h <= 1e-9)
rep_m = run_with(R500H, scale=10 ** 0.2, skip_pressure=True)      # the stretched grid leaves the pressure diagnostic's 50-1000 kpc support
cg = orig_load("A85");
okm = abs(math.log10((cg["rg"] / cg["R500"] * cg["R500"] * 10 ** 0.2)[3] / cg["rg"][3]) - 0.2) < 1e-12
t_m = table_from(rep_m)
check("C-iii MUTATE: R500 x 10^0.2 moves the decoded gas radius grid by exactly 0.2 dex (and moves the identity ratio)", f"grid shift exact {okm}; identity can/nu_mono "
      f"{t_h['canonical|nu_mono']['id_ratio']:.3f} -> {t_m['canonical|nu_mono']['id_ratio']:.3f}", okm and abs(t_m["canonical|nu_mono"]["id_ratio"] - t_h["canonical|nu_mono"]["id_ratio"]) > 1e-3)

try:
    rep_f = run_with(R500F); P("  (R500,FORW run: the audit's pressure diagnostic ran normally)")
except ValueError as e:
    rep_f = run_with(R500F, skip_pressure=True); P(f"  (R500,FORW run: the audit's pressure diagnostic refused the grid ({e}); re-run with it skipped; it feeds no row)")
t_f = table_from(rep_f)
P("\nTHE IDENTITY READING AND eta AT THE OUTERMOST AUDITED RADIUS (median over the 12 clusters)")
for k in H2c:
    P(f"  {k:18s}: committed eta {H2c[k]['eta']:.3f}, identity/measured {H2c[k]['id_ratio']:.3f} +- {H2c[k]['id_sd']:.3f}  ->  R500,FORW: eta {t_f[k]['eta']:.3f}, "
      f"identity/measured {t_f[k]['id_ratio']:.3f} +- {t_f[k]['id_sd']:.3f} (r {t_f[k]['r_kpc']:.0f} kpc = {t_f[k]['frac_R500']:.2f} R500,FORW)")
npass = sum(CHK)
P(f"\n{npass}/{len(CHK)} checks pass   ({time.time() - T0:.0f} s)")
json.dump(dict(R500_header_kpc=R500H, R500_forward_kpc=R500F, committed=H2c, lcdmfree=t_f, identity_path=t_h, mutate=t_m, checks=dict(passed=npass, n=len(CHK))),
          open(os.path.join(LANE, "cfg303_xcop_LCDMFREE_results.json"), "w"), indent=1, default=float)
open(os.path.join(LANE, "cfg303_xcop_LCDMFREE.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == len(CHK) else 1)

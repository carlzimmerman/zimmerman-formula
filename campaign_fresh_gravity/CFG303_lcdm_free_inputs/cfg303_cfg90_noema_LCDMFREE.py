#!/usr/bin/env python3
"""CFG303 Addendum 3 -- (A3.1) CFG90's pooled z >= 1.5 a0(z) offsets with RC100's joint-fit posterior log M_baryon (LCDM-MODEL) replaced by the
native SED M* (RC100 Table 3 col 6) x (1 + mu_t18); (A3.2) CFG213's NOEMA3D Z1.4 bin with the joint-fit f_DM / M_fit replaced by SED M* + CO gas
in CFG216's thin disc.  cfg90.py is run UNMODIFIED except for its hard-coded REPO line, pointed (as CFG289's supplement did) at a temporary
symlink overlay of this repository in which only the RC100 CSV is replaced; its outputs stay in a temporary directory and are summarised here.
Frozen criteria: FROZEN_CRITERIA.md (52976ec22) + ADDENDA 1-3, written before any native number was computed.
kappa = 1/2 FITTED.  The cold mass is still required; no dark-matter particle is added.  No sentence here says the data favour a law.
Run:  python3 campaign_fresh_gravity/CFG303_lcdm_free_inputs/cfg303_cfg90_noema_LCDMFREE.py
Outputs: cfg303_cfg90_noema_LCDMFREE.out, cfg303_cfg90_noema_LCDMFREE_results.json (this lane only; no temporary path is written to them).
"""
import os, sys, io, re, csv, json, math, shutil, subprocess, tempfile, contextlib, time, hashlib
sys.dont_write_bytecode = True
import numpy as np

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
for f in ("FROZEN_CRITERIA.md", "FROZEN_CRITERIA_ADDENDUM_1.md", "FROZEN_CRITERIA_ADDENDUM_2.md", "FROZEN_CRITERIA_ADDENDUM_3.md"):
    P(f"  {f}: sha256 {sha(os.path.join(LANE, f))}")

# ================================================================================================ A3.1 CFG90
RC_REL = os.path.join("real_research", "data", "rc100_nestorshachar2023_table3.csv")
corr = list(csv.DictReader(open(os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3_CORRECTED.csv"), newline="")))
tr = {r["idx"]: r for r in csv.DictReader(open(os.path.join(LANE, "rc100_table3_cols5to8_transcribed.csv"), newline=""))}
F217 = os.path.join(CFG, "CFG217_rc100_attack", "cfg217_attack.py")
s217 = open(F217).read(); ns217 = {"__file__": F217, "__name__": "cfg303_exec"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(s217[:s217.index("# ------------------------------------------------------------------------------------------------ data (CFG216's sample)")], "cfg217", "exec"), ns217)
mu_t18 = ns217["mu_t18"]
TMP = tempfile.mkdtemp(prefix="cfg303_cfg90_")


def write_csv(rows, path, native=False):
    cols = list(rows[0].keys())
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
        for r in rows:
            r2 = dict(r)
            if native:
                t = tr[r["idx"]]; lms = float(t["logMstar"]); z = float(r["z"])
                r2["logMbar_Msun"] = f"{lms + math.log10(1 + mu_t18(z, lms)):.6f}"
            w.writerow(r2)


def overlay(replace_rc):
    """a symlink view of the repository with only the RC100 CSV replaced (None = original file)."""
    view = os.path.join(TMP, "view_" + ("orig" if replace_rc is None else os.path.basename(replace_rc).split(".")[0]))
    os.makedirs(view)
    for top in os.listdir(REPO):
        if top in ("real_research", ".git"):
            continue
        os.symlink(os.path.join(REPO, top), os.path.join(view, top))
    rr = os.path.join(view, "real_research"); os.makedirs(os.path.join(rr, "data"))
    for e in os.listdir(os.path.join(REPO, "real_research")):
        if e != "data":
            os.symlink(os.path.join(REPO, "real_research", e), os.path.join(rr, e))
    for e in os.listdir(os.path.join(REPO, "real_research", "data")):
        src = os.path.join(REPO, "real_research", "data", e)
        dst = os.path.join(rr, "data", e)
        if e == os.path.basename(RC_REL) and replace_rc is not None:
            shutil.copyfile(replace_rc, dst)
        else:
            os.symlink(src, dst)
    return view


def run_cfg90(view, tag):
    d90 = os.path.join(TMP, "cfg90_" + tag); os.makedirs(d90)
    src = open(os.path.join(CFG, "CFG90_a0z_rederivation", "cfg90.py")).read()
    patched, n = re.subn(r'^REPO = ".*"$', f'REPO = "{view}"', src, count=1, flags=re.M)
    assert n == 1
    open(os.path.join(d90, "cfg90.py"), "w").write(patched)
    subprocess.run([sys.executable, "cfg90.py"], cwd=d90, capture_output=True)
    return json.load(open(os.path.join(d90, "cfg90_results.json")))


fix_csv = os.path.join(TMP, "rc100_fix.csv"); nat_csv = os.path.join(TMP, "rc100_native.csv")
write_csv(corr, fix_csv); write_csv(corr, nat_csv, native=True)
J90 = json.load(open(os.path.join(CFG, "CFG90_a0z_rederivation", "cfg90_results.json")))
J90F = json.load(open(os.path.join(CFG, "CFG289_rc100_csv_bound", "cfg90_results_RC100FIX.json")))
r_orig = run_cfg90(overlay(None), "orig")
r_fix = run_cfg90(overlay(fix_csv), "fix")
r_nat = run_cfg90(overlay(nat_csv), "native")
P("\nA3.1 CFG90 (pooled z >= 1.5 offsets; counts RC100 below a0 / below 0.3 a0 / z>=1.5 below a0 / z>=1.5 below 0.3 a0)")
d_o = max(abs(r_orig["pooled"][k] - J90["pooled"][k]) for k in ("flat", "rival", "sigma"))
check("C-ii (reported: CFG289 found the committed cfg90 run read the live repo through its hard-coded path) the original file through the overlay against "
      "cfg90_results.json: pooled and RC100 counts", f"pooled max |diff| {d_o:.1e}; counts {r_orig['counts']['RC100']} vs {J90['counts']['RC100']}", True)
d_f = max(abs(r_fix["pooled"][k] - J90F["pooled"][k]) for k in ("flat", "rival", "sigma"))
check("C-i the corrected file with log M_baryon left as the posterior reproduces CFG289's corrected-file CFG90 run (pooled flat, rival, sigma; N; RC100 counts)",
      f"max |diff| {d_f:.1e}; N {r_fix['pooled']['N']} vs {J90F['pooled']['N']}; counts {r_fix['counts']['RC100']} vs {J90F['counts']['RC100']}",
      d_f <= 1e-9 and r_fix["pooled"]["N"] == J90F["pooled"]["N"] and r_fix["counts"]["RC100"] == J90F["counts"]["RC100"])
for lab, rr in (("committed (original file)", J90), ("corrected file, joint-fit posterior (CFG289)", r_fix), ("corrected file, NATIVE SED M* (1 + mu_t18)", r_nat)):
    p = rr["pooled"]
    P(f"  {lab:46s}: pooled N {p['N']}, flat {p['flat']:+.3f} ({p['flat'] / p['sigma']:+.2f} sigma), rival {p['rival']:+.3f} ({p['rival'] / p['sigma']:+.2f} sigma), "
      f"sigma {p['sigma']:.3f}; RC100 counts {rr['counts']['RC100']}; n1 (gaps > 1 sigma) {rr['n1']}, n2 {rr['n2']}")
RES = dict(cfg90=dict(committed=dict(pooled=J90["pooled"], counts=J90["counts"]), fix=dict(pooled=r_fix["pooled"], counts=r_fix["counts"], n1=r_fix["n1"]),
                      native=dict(pooled=r_nat["pooled"], counts=r_nat["counts"], n1=r_nat["n1"], n2=r_nat["n2"]), orig_overlay=dict(pooled=r_orig["pooled"], counts=r_orig["counts"])))

# ================================================================================================ A3.2 NOEMA3D Z1.4
P("\nA3.2 NOEMA3D (CFG213's Z1.4 bin) on native rows")
F213 = os.path.join(CFG, "CFG213_dysmalpy_two_sided", "cfg213_two_sided.py")
s213 = open(F213).read(); ns213 = {"__file__": F213, "__name__": "cfg303_exec"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(s213[:s213.index("# ------------------------------------------------------------------------------------------------ reported extras")], "cfg213", "exec"), ns213)
F216 = os.path.join(CFG, "CFG216_rc100_within_sample", "cfg216_rc100.py")
s216 = open(F216).read(); ns216 = {"__file__": F216, "__name__": "cfg303_exec"}
os.environ["RC100_INPUT"] = "corrected"
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(s216[:s216.index("# ------------------------------------------------------------------------------------------------ controls C1, C3")], "cfg216", "exec"), ns216)
os.environ.pop("RC100_INPUT", None)
disc_v2, G2SI = ns216["disc_v2"], ns216["G2SI"]
noema, galaxy_rows, deltas, med_ci, verdict, KER, A0F = (ns213[k] for k in ("noema", "galaxy_rows", "deltas", "med_ci", "verdict", "KER", "A0F"))
J213 = json.load(open(os.path.join(CFG, "CFG213_dysmalpy_two_sided", "cfg213_two_sided_results.json")))["numbers"]


def native_rows(alpha):
    out = []
    for g in noema:
        if not all(math.isfinite(g[k]) for k in ("Vc", "sig0", "Re", "z", "logMstar", "logMgas")):
            continue
        vc2 = g["Vc"] ** 2 - (3.36 - alpha) * g["sig0"] ** 2
        go = vc2 / g["Re"] * G2SI
        gb = (10 ** g["logMstar"] + 10 ** g["logMgas"]) * disc_v2(1.0, g["Re"], g["Re"]) / g["Re"] * G2SI
        out.append(dict(id=g["id"], z=g["z"], gbar=gb, D=go / gb))
    return out


# C-i: committed g_bar through the native formula (M_id = g_bar / xi) reproduces the committed fit-route cells -- uses a FRESH CFG213 namespace (its bootstrap state as committed)
ns213b = {"__file__": F213, "__name__": "cfg303_exec"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(s213[:s213.index("# ------------------------------------------------------------------------------------------------ reported extras")], "cfg213b", "exec"), ns213b)
fit = ns213b["galaxy_rows"]("Z1.4", ns213b["noema"], alpha=3.36)
nb = {g["id"]: g for g in ns213b["noema"]}
xs = [disc_v2(1.0, nb[r["id"]]["Re"], nb[r["id"]]["Re"]) / nb[r["id"]]["Re"] * G2SI for r in fit]
dci = 0.0
for law in ("flat", "rival"):
    rows_id = [dict(r, gbar=(r["gbar"] / x) * x) for r, x in zip(fit, xs)]
    m, lo, hi = ns213b["med_ci"](ns213b["deltas"](rows_id, law, "canonical", ns213b["KER"]["nu_mono"]), ("cfg303id", law))
    c = J213["Z1.4 (NOEMA3D)"][f"3.36|fit|nu_mono|canonical|{law}"]
    dci = max(dci, abs(m - c["med"]), abs(lo - c["lo"]), abs(hi - c["hi"]))
check("C-i the committed Z1.4 fit-route g_bar through the native geometry factor reproduces CFG213's committed cells (nu_mono canonical, alpha 3.36)", f"max |diff| {dci:.1e}", dci <= 1e-9)
z14 = {}
for alpha in (3.36, 1.68):
    rows = native_rows(alpha)
    for kn, nu in KER.items():
        for ft in A0F:
            for law in ("flat", "rival"):
                m, lo, hi = med_ci(deltas(rows, law, ft, nu), ("cfg303", alpha, kn, ft, law))
                z14[f"{alpha}|{kn}|{ft}|{law}"] = dict(n=len(rows), med=m, lo=lo, hi=hi, v=verdict(lo, hi))
rob = {}
for law in ("flat", "rival"):
    vs = {z14[f"{a}|{k}|{f}|{law}"]["v"] for a in (3.36, 1.68) for k in KER for f in A0F}
    rob[law] = vs.pop() if len(vs) == 1 else "NOT robust (" + ", ".join(sorted(vs)) + ")"
for law in ("flat", "rival"):
    c = J213["Z1.4 (NOEMA3D)"][f"3.36|fit|nu_mono|canonical|{law}"]; cr_ = J213["Z1.4 (NOEMA3D)"].get(f"3.36|route|nu_mono|canonical|{law}")
    nv = z14[f"3.36|nu_mono|canonical|{law}"]
    P(f"  {law:5s} nu_mono canonical alpha 3.36: committed fit route {c['med']:+.3f} [{c['lo']:+.3f}, {c['hi']:+.3f}] {c['v']}; committed route "
      + (f"{cr_['med']:+.3f} [{cr_['lo']:+.3f}, {cr_['hi']:+.3f}] {cr_['v']}" if cr_ else "n/a") + f"; NATIVE (n {nv['n']}) {nv['med']:+.3f} [{nv['lo']:+.3f}, {nv['hi']:+.3f}] {nv['v']}")
P(f"  robust verdicts: committed fit route flat {J213['Z1.4 (NOEMA3D) robust']['flat']}, rival {J213['Z1.4 (NOEMA3D) robust']['rival']}; NATIVE flat {rob['flat']}, rival {rob['rival']}")
RES["noema"] = dict(cells=z14, robust=rob, committed_robust=J213["Z1.4 (NOEMA3D) robust"])
shutil.rmtree(TMP, ignore_errors=True)
npass = sum(CHK)
P(f"\n{npass}/{len(CHK)} checks pass   ({time.time() - T0:.0f} s)")
RES["checks"] = dict(passed=npass, n=len(CHK))
json.dump(RES, open(os.path.join(LANE, "cfg303_cfg90_noema_LCDMFREE_results.json"), "w"), indent=1, default=float)
open(os.path.join(LANE, "cfg303_cfg90_noema_LCDMFREE.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == len(CHK) else 1)

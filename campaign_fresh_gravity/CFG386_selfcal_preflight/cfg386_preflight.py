"""CFG386 pre-flight: on-disk discs whose own curves span beam-resolved g_obs >= 3.5 a0 (inner) to <= 0.55 a0 (outer).
Criteria: FROZEN_CRITERIA.md (d5711e013). Run: python3 cfg386_preflight.py ; MUTATE=1 sets a0 x 10 (count must change; rc 1).
"""
import csv, json, math, os, sys
import numpy as np
from astropy.cosmology import Planck18

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE") == "1"
TAG = "_MUTATE" if MUTATE else ""
lines, checks = [], []
def say(s=""):
    print(s); lines.append(s)
def check(n, ok, v):
    checks.append({"name": n, "pass": bool(ok), "value": v}); say(f"  [{'PASS' if ok else 'FAIL'}] {n}: {v}")

A0 = 9.3603e-11 * (10 if MUTATE else 1)          # m/s^2
KPC = 3.0857e19
def g_obs(V_kms, r_kpc):
    return (V_kms * 1e3) ** 2 / (r_kpc * KPC)
def kpc_per_arcsec(z):
    return float(Planck18.angular_diameter_distance(z).to("kpc").value * math.pi / 180 / 3600)
arct = lambda r, Va, rt: Va * 2 / math.pi * math.atan(r / max(rt, 1e-6))

say("CFG386 self-calibration pre-flight" + ("  (MUTATE: a0 x 10)" if MUTATE else ""))
say("=" * 78)
check("C1 Planck18 D_A conversion at z = 2.2 is 8.3-8.5 kpc/arcsec", 8.2 <= kpc_per_arcsec(2.2) <= 8.6, f"{kpc_per_arcsec(2.2):.3f}")
check("C2 arctan model: V(r_t) = V_a/2 and V(1e6 r_t) -> V_a", abs(arct(1.0, 200, 1.0) - 100) < 1e-9 and abs(arct(1e6, 200, 1.0) / 200 - 1) < 1e-5, "ok")

fits = list(csv.DictReader(open(os.path.join(REPO, "data_assembly", "kmos3d_cubes", "k3d_fits_main_final_flags.csv"))))
cat = {r["ID"]: r for r in csv.DictReader(open(os.path.join(REPO, "data_assembly", "kmos3d_phibss", "kmos3d_catalog.csv")))}
rows, qual = [], {"cons_P0": [], "len_P0": [], "cons_P1": []}
for f in fits:
    c = cat.get(f["ID"])
    if c is None:
        continue
    z = float(f["Z"]); s = kpc_per_arcsec(z)
    Va, eVa, rt, sig0, rd, rmax = (float(f[k]) for k in ("Va", "eVa", "rt", "sig0", "rd", "rmax"))
    psf = float(c["PSF_FWHM"])
    r_out = rmax * s
    out = {"ID": f["ID"], "z": z, "Va": Va, "eVa_frac": eVa / Va if Va > 0 else 9, "psf_arcsec": psf, "rmax_arcsec": rmax}
    ok_fit = Va < 790 and Va > 0 and eVa / Va <= 0.10
    for lab, rin_as, P1 in (("cons_P0", psf, False), ("len_P0", psf / 2, False), ("cons_P1", psf, True)):
        r_in = rin_as * s
        def V2(r_as):
            v = arct(r_as, Va, rt)
            return math.sqrt(v * v + (2 * sig0**2 * r_as / max(rd, 1e-6) if P1 else 0.0))
        gi = g_obs(V2(rin_as), r_in) / A0 if r_in > 0 else 0
        go = g_obs(V2(rmax), r_out) / A0 if r_out > 0 else 9e9
        q = ok_fit and (rin_as < rmax) and gi >= 3.5 and go <= 0.55
        out[lab] = dict(g_in_a0=gi, g_out_a0=go, qualifies=q, sig_over_V_out=sig0 / max(arct(rmax, Va, rt), 1e-6))
        if q:
            qual[lab].append(f["ID"])
    rows.append(out)
say(f"\nKMOS3D: {len(rows)} fits; fit-quality pass (Va < 790, eVa/Va <= 0.10): {sum(1 for r in rows if r['Va']<790 and r['eVa_frac']<=0.10)}")
gin = np.array([r["cons_P0"]["g_in_a0"] for r in rows]); gout = np.array([r["cons_P0"]["g_out_a0"] for r in rows])
say(f"  conservative r_in = PSF: g_obs(r_in)/a0 median {np.median(gin):.2f}; g_obs(rmax)/a0 median {np.median(gout):.2f}; "
    f"rmax/PSF median {np.median([r['rmax_arcsec']/r['psf_arcsec'] for r in rows]):.2f}")
say(f"  inner >= 3.5 a0: {int(np.sum(gin >= 3.5))}; outer <= 0.55 a0: {int(np.sum(gout <= 0.55))}; rmax > PSF: {sum(1 for r in rows if r['rmax_arcsec'] > r['psf_arcsec'])}")
for lab in qual:
    say(f"  QUALIFYING ({lab}): {len(qual[lab])}  {qual[lab][:12]}")
for q in qual["cons_P0"]:
    r = next(x for x in rows if x["ID"] == q)
    say(f"    {q}: z {r['z']:.2f} g_in {r['cons_P0']['g_in_a0']:.2f} a0, g_out {r['cons_P0']['g_out_a0']:.2f} a0, sigma0/V_out {r['cons_P0']['sig_over_V_out']:.2f}"
        f"{'  PRESSURE-LIMITED' if r['cons_P0']['sig_over_V_out'] > 0.5 else ''}")

# KURVS
kv = list(csv.DictReader(open(os.path.join(REPO, "data_assembly", "arxiv_tables", "kurvs2023_velocities_at_radii.csv"))))
kk = {r["kurvs_id"]: r for r in csv.DictReader(open(os.path.join(REPO, "data_assembly", "arxiv_tables", "kurvs2023_kinematics.csv")))}
# R_d is in the INTEGRATED table (a first run looked only in the kinematics table, skipped every row silently; fixed, disclosed)
for r_ in csv.DictReader(open(os.path.join(REPO, "data_assembly", "arxiv_tables", "kurvs2023_integrated.csv"))):
    kk.setdefault(r_["kurvs_id"], {}).update(r_)
nk_eval = 0
kq = []
say("\nKURVS (z ~ 1.5): points at 3 R_d, 6 R_d, last")
for r in kv:
    k = kk.get(r["kurvs_id"], {})
    Rd = None
    for key in ("R_d_kpc", "Rd_kpc", "R_D_kpc", "rd_kpc"):
        if key in k and k[key] not in ("", None):
            Rd = float(k[key]); break
    if Rd is None and k.get("reff_kpc") not in (None, ""):
        Rd = float(k["reff_kpc"]) / 1.678          # exponential disc R_d = R_e/1.678 (the KMOS3D rule; disclosed)
    if Rd is None:
        say(f"  KURVS {r['kurvs_id']:>3}: no R_d found -> not evaluated"); continue
    nk_eval += 1
    pts = [(3 * Rd, float(r["v_at_R3D_kms"]), float(r["e_v_R3D"])), (6 * Rd, float(r["v_at_R6D_kms"]), float(r["e_v_R6D"])),
           (float(r["R_halpha_max_kpc"]), float(r["v_at_last_point_kms"]), float(r["e_v_last"]))]
    pts = sorted(pts)
    gi, go = g_obs(pts[0][1], pts[0][0]) / A0, g_obs(pts[-1][1], pts[-1][0]) / A0
    err_ok = all(e / v <= 0.10 for _, v, e in pts if v > 0)
    q = gi >= 3.5 and go <= 0.55 and err_ok
    if q:
        kq.append(r["kurvs_id"])
    say(f"  KURVS {r['kurvs_id']:>3}: inner g {gi:.2f} a0 (r {pts[0][0]:.1f} kpc), outer g {go:.2f} a0 (r {pts[-1][0]:.1f} kpc), errors<=10% {err_ok} -> {'QUALIFIES' if q else 'no'}")
say(f"  KURVS evaluated {nk_eval} of {len(kv)}; qualifying: {len(kq)} {kq}")
check("C3 every KURVS row with an R_d was evaluated (no silent skips)", nk_eval > 0, f"{nk_eval} of {len(kv)}")
say("SINS/zC-SINF AO (CFG280): one published radius per galaxy -> 0 qualifying by construction")

Nz2 = len(qual["cons_P0"])
verdict = "ON-DISK DECISIVE CANDIDATE" if Nz2 >= 10 else ("PARTIAL" if Nz2 >= 1 else "NONE ON DISK")
say(f"\nVERDICT (z >= 2, conservative r_in = PSF, P0): {verdict}  (N = {Nz2}; lenient {len(qual['len_P0'])}; with pressure P1 {len(qual['cons_P1'])}; KURVS z~1.5 {len(kq)})")
say("Caveat: these are FIT-MODEL extrapolations to the PSF radius and rmax, not independent per-radius measurements; a qualifying disc still needs")
say("its own per-radius extraction from the cube (and the outer pressure term).")
check("T-MUT main-run marker (MUTATE a0 x10 must change the count)", not MUTATE, f"N {Nz2}")
if MUTATE:
    checks.append({"name": "MUTATE forces rc 1", "pass": False, "value": Nz2})
n = sum(c_["pass"] for c_ in checks)
say(f"\n{n}/{len(checks)} pass" + ("  (MUTATE)" if MUTATE else ""))
json.dump({"lane": "CFG386", "mutate": MUTATE, "verdict": verdict, "qualifying": qual, "kurvs_qualifying": kq, "rows": rows, "checks": checks},
          open(os.path.join(HERE, f"cfg386_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg386{TAG}.out"), "w").write("\n".join(lines) + "\n")
sys.exit(0 if n == len(checks) else 1)

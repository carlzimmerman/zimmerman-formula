#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR11 (input lane) -- THE DARK FLUID'S VELOCITY STRUCTURE AROUND KiDS L* HOSTS, FROM L375's OWN SHELL MODEL.

WHY.  XR11 asks whether the dark fluid can carry the MOND-sector gate's stiffness in the edge layers.  That needs the
fluid's own stiffness there: its velocity dispersion along a perturbation's wavevector, and whether the fluid at a given
radius is phase-mixed (many streams) or a cold infall stream.  The record's infall model for these hosts is L375's
spherical shell model (secondary infall on a Wechsler accretion history, the bin's baryons, Newtonian only per L353,
L365's trigger and the isotropic kick).  Its halo() returns radial mass histograms only.  This lane loads L375's halo()
source UNEDITED except its return line, which also hands back the particles' final phase-space state (r, v_r, L, cold);
nothing else changes, so the Monte-Carlo sequence is L375's own.

WHAT IT WRITES (XR11_shell_model_velocities_results.json, read by XR11_dark_channel_gate.py):
  per run (KiDS bins 1 and 2 = M_200 8.97e11 / 1.91e12 Msun at z_l = 0.25 with L390's fitted baryonic masses 6.31e10 /
  1.00e11 Msun; the fiducial kicked carrier, v_k = 650 km/s, Gamma = 10 H, alpha = 0.75; and the same halo with the decay
  off), in 48 log radial bins from 5 kpc to 8 Mpc: the density of the undecayed (phi_H, 'cold') and decayed/kicked
  (phi_L, 'kicked') carrier; their mean radial velocity, radial dispersion about the mean, per-component tangential
  dispersion <v_t^2>/2; the share of cold elements moving outward; the outermost bin where inflow and outflow coexist
  (0.1 <= outgoing share <= 0.9, >= 20 elements: the model's multistream edge); and 2 r_200, where L375 injects its cold
  infall shells (v_r = -v_200, v_t = 0.4 v_200, a single velocity: zero intrinsic dispersion).  Bins holding only outgoing
  cold elements at large r are the initial Jeans-Gaussian tail escaping (densities <~1e-2 of the mean): an artefact of the
  initial condition, reported, not used.

CHECKS
  C1 CONTROL [load-bearing]: at N = 3000 the modified halo() returns L375's halo() histograms (all and cold) EXACTLY, for
     one decaying and one non-decaying configuration: the modification is the return line only.
  C2 CONTROL: the no-decay halo keeps the carrier (n_cold = n), and the fiducial halo's retained fraction inside
     0.5 Mpc/h lies in L375's committed range for its bin (0.15-0.45; L375 fid: 0.247 / 0.232 at N = 60000).
  R1 (reported) the dispersion profiles and the multistream marker, per run.
No MUTATE: this lane only produces inputs (as XR9_carrier_halos); the physics checks and their MUTATE are in
XR11_dark_channel_gate.py.

SCOPE.  L375's model and its limits: spherical, one smooth accretion history, cold shells injected at 2 r_200 (so the
model has NO cold carrier beyond ~2 r_200 at z = 0.25 except kicked products), static baryons.  N = 30000 per halo
(L375 used 60000) to keep the lane under two minutes single-threaded.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR11_shell_model_velocities.py
"""
import os, sys, json, math, time, inspect
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DS = os.path.join(REPO, "real_research", "dark_sector_2026")
sys.path.insert(0, DS)
sys.dont_write_bytecode = True                                          # write nothing outside this folder's XR11_ files
import L375_triggered_carrier_galaxy_retention as L375              # noqa: E402  (module import: its main is guarded)

SLUG = "XR11_shell_model_velocities"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "XR11_shell", "checks": {}, "numbers": {}}
NPART = 30000


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("CHECKS")[0].strip())

# ---------------------------------------------------------------------------------- L375's halo(), return line extended
_SRC = inspect.getsource(L375.halo)
_OLD = "return tag, dict(edges=edges,"
assert _SRC.count(_OLD) == 1
_NEW = "return tag, dict(r_fin=r, vr_fin=vr, L_fin=L, cold_fin=cold, edges=edges,"
_NS = dict(vars(L375))
exec(_SRC.replace(_OLD, _NEW), _NS)
halo_pv = _NS["halo"]
MB390 = json.load(open(os.path.join(DS, "L390_kids_resolved_linear_gate_results.json")))["numbers"]["M_b"]["p=1, x_c0=2.5"]
seed_of = lambda b, vk: 1200 + 10 * b + int(vk) // 25                  # DE10/XR9's seed rule

# ============================================================================================ C1 the modification
banner("C1  CONTROL: the extended halo() is L375's halo() (N = 3000, decaying and non-decaying)")
dev = []
for cfg in (("c1_fid", 2, MB390[2], 650.0, 10.0, 0.75, True, 3000, seed_of(2, 650)),
            ("c1_nod", 1, MB390[1], 650.0, 0.0, 0.75, True, 3000, seed_of(1, 650))):
    _, a = L375.halo(cfg)
    _, b = halo_pv(cfg)
    dev.append(int(np.max(np.abs(a["hist"] - b["hist"]))) + int(np.max(np.abs(a["hist_cold"] - b["hist_cold"]))))
check("C1 CONTROL: the extended halo() returns L375's histograms exactly (all and cold; decaying and non-decaying runs)",
      f"max |difference| in counts: {dev}", max(dev) == 0)

# ============================================================================================ the runs
banner("THE RUNS: KiDS bins 1 and 2, fiducial kick (650 km/s) and decay off, N = %d" % NPART)
EDGES = np.geomspace(5.0, 8000.0, 49)                                    # kpc
RM = np.sqrt(EDGES[1:] * EDGES[:-1]); VOL = 4 / 3 * math.pi * (EDGES[1:] ** 3 - EDGES[:-1] ** 3)


def moments(d, sel):
    r, vr, vt = d["r_fin"][sel], d["vr_fin"][sel], d["L_fin"][sel] / d["r_fin"][sel]
    idx = np.digitize(r, EDGES) - 1
    out = {k: np.full(len(RM), np.nan) for k in ("rho", "vr_mean", "sig_r", "sig_t1", "f_out", "n")}
    for i in range(len(RM)):
        m = idx == i
        out["n"][i] = m.sum()
        out["rho"][i] = m.sum() * d["m"] / VOL[i]                          # Msun/kpc^3
        if m.sum() >= 5:
            out["vr_mean"][i] = float(np.mean(vr[m]))
            out["sig_r"][i] = float(np.std(vr[m]))
            out["sig_t1"][i] = float(np.sqrt(np.mean(vt[m] ** 2) / 2))
            out["f_out"][i] = float(np.mean(vr[m] > 0))
    return {k: [None if not np.isfinite(x) else float(x) for x in v] for k, v in out.items()}


RUNS = {}
for b in (1, 2):
    for lab, gam in (("fid", 10.0), ("nodecay", 0.0)):
        cfg = (f"b{b}_{lab}", b, MB390[b], 650.0, gam, 0.75, True, NPART, seed_of(b, 650))
        _, d = halo_pv(cfg)
        cold = d["cold_fin"]
        mc = moments(d, cold); mk = moments(d, ~cold)
        # the multistream marker: outermost bin (>= 20 cold elements) where inflow and outflow coexist, 0.1 <= f_out <= 0.9.
        # (Bins with f_out = 1 at large r hold the initial Jeans-Gaussian tail escaping, at <~1e-2 of the mean density.)
        sp = [RM[i] for i in range(len(RM)) if mc["n"][i] and mc["n"][i] >= 20 and 0.10 <= (mc["f_out"][i] or 0) <= 0.90]
        r_sp = float(max(sp)) if sp else None
        z_l = L375.ZL
        r200 = float(L375.r200_of(L375.M200_BINS[b], z_l)); v200 = math.sqrt(L375.G * L375.M200_BINS[b] / r200)
        M_ap = float(np.sum(d["r_fin"] < L375.RAP)) * d["m"]
        RUNS[cfg[0]] = dict(b=b, Mb=MB390[b], M200=L375.M200_BINS[b], r200_kpc=r200, v200_kms=v200, r_splash_kpc=r_sp,
                            r_inject_kpc=2 * r200, n=int(d["n"]), n_cold=int(cold.sum()), M_ap=M_ap, cold=mc, kicked=mk)
        P(f"    {cfg[0]:11s}: M_b {MB390[b]:.2e}, r200 {r200:.0f} kpc, v200 {v200:.0f} km/s; n = {d['n']}, cold {int(cold.sum())}; "
          f"outermost multistream bin {r_sp if r_sp is None else round(r_sp)} kpc; cold shells injected at {2 * r200:.0f} kpc   "
          f"[{time.time() - T0:.0f}s]")
for b in (1, 2):
    RUNS[f"b{b}_fid"]["S_ap"] = RUNS[f"b{b}_fid"]["M_ap"] / RUNS[f"b{b}_nodecay"]["M_ap"]

banner("C2 R1  CONTROLS ON THE RUNS; THE DISPERSION PROFILES")
c2 = all(RUNS[f"b{b}_nodecay"]["n_cold"] == RUNS[f"b{b}_nodecay"]["n"] for b in (1, 2)) and \
    all(0.15 <= RUNS[f"b{b}_fid"]["S_ap"] <= 0.45 for b in (1, 2))
check("C2 CONTROL: decay off keeps every element cold; the fiducial retention inside 0.5 Mpc/h is in L375's range for its bin",
      {f"b{b}": round(RUNS[f"b{b}_fid"]["S_ap"], 3) for b in (1, 2)}, c2)
for key, R in RUNS.items():
    P(f"    {key}: r [kpc] | cold rho [Msun/kpc^3], <v_r>, sig_r, sig_t1 [km/s], f_out | kicked rho, sig_r")
    for i in range(0, len(RM), 3):
        c, k = R["cold"], R["kicked"]
        fmt = lambda x, f="%.0f": ("   -" if x is None else f % x)
        P(f"      {RM[i]:7.0f} | {fmt(c['rho'][i], '%.2e')} {fmt(c['vr_mean'][i])} {fmt(c['sig_r'][i])} {fmt(c['sig_t1'][i])} "
          f"{fmt(c['f_out'][i], '%.2f')} | {fmt(k['rho'][i], '%.2e')} {fmt(k['sig_r'][i])}")
check("R1 (reported) the cold and kicked carrier's velocity structure per run (see table)", "see table", True, load_bearing=False)

OUT["numbers"] = dict(edges_kpc=EDGES.tolist(), r_mid_kpc=RM.tolist(), N=NPART, runs=RUNS,
                      config=dict(alpha=0.75, gamma=10.0, v_k=650.0, grow_b=True, seed_rule="1200 + 10 b + int(v_k)//25",
                                  masses="L390 p=1, x_c0=2.5"))
nlb = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
fn = os.path.join(HERE, SLUG + "_results.json")
json.dump(OUT, open(fn, "w"), indent=1, default=float)
P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}   "
  f"[{time.time() - T0:.0f}s]")
sys.exit(1 if nlb else 0)

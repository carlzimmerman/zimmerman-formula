#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR12 (3/4) -- WHEN THE CONVERSION HAPPENS IN THE INFALL STREAMS, NOT THE HALO CENTRE: the flagship's clearing at r_F and
cluster retention, in the record's resolved shell model with FK1's own trigger.

WHY.  XR12_filament_trigger.py shows FK1's n^2 trigger (the fluid's own density, K-gated: rho_t(z) = delta_t0 rhobar_c0
E^4, delta_t0 = 5.31 nominal, 25 FK1's upper bracket) fires in the streams: every stream near r_vir (delta ~ 100) and the
densest filaments are above it at z = 2-3, and every clump the streams carry.  L375/L376 resolved galaxy hosts with a
shell model whose trigger reads the LOCAL TOTAL density, un-gated (x~ > 5).  This lane swaps in FK1's trigger and asks
where the carrier converts and what that does to (i) the flat-a0 flagship, which needs a retained fraction S <= 0.059 at
r_F (MS2), and (ii) cluster retention, which X-COP needs inside 0.286-0.768 (L366's two-sided gate, both footings).

MODEL.  L376's halo2() -- L375's spherical shell model (secondary infall on a Wechsler history, alpha = 0.75; Hernquist
baryons + an NFW-shaped CGM/ICM grown with the halo; a Newtonian, kernel-invisible carrier; the decay at Gamma = 10 H above
threshold; an isotropic kick) -- re-implemented with the trigger as a parameter.  Trigger variants:
  x5      L375/L376's own: x~ = 1.5 (rho_tot - rhobar_m)/rho_crit(z) > 5 (the local total density, un-gated)  [control]
  fk1     FK1: the COLD carrier's own shell density > delta_t0 rhobar_c0 E(z)^4;  delta_t0 = 5.31 or 25.
  +C_s    streams: outside r_200(z) the infalling carrier is concentrated into streams of local density C_s x the shell
          average (C_s = 10: a stream covering ~10% of the sphere), so it meets the threshold earlier.
  +up     upstream conversion: a fraction F_u(z) of newly accreted carrier arrives ALREADY converted -- the escaped
          daughters of the minihalos and galaxies that fired upstream (XR12_forest_halo_model H1's unweighted F_u(z),
          read from its results JSON), moving at w(z) = v_k <(1+z)/(1+z_c)> relative to the infall (their peculiar
          momentum decays as 1/a since conversion).
Hosts: the flagship (M_200 = 1e12, M_b = 1e11, z_obs = 2.5, from z = 5.25) and an X-COP-like cluster (M_200 = 8e14, BCG
1e12, ICM = f_b M - M_b, z_obs = 0, from z = 2.75).  Kick 600 km/s (L388's window centre).
CHECKS
  C1 CONTROL: with the x5 trigger the re-implementation reproduces L376's committed RC100 z = 2 numbers EXACTLY (N = 60000,
     seeds 2002/2102): carrier inside R_e / LCDM's = 3.9566e-4, f_DM,LCDM(<R_e) = 0.45303.
  R10 [the FIRST run's pre-declared claims, FALSIFIED, kept as run, not load-bearing] at the record's rate Gamma = 10 H:
     F1 "with streams >= 50% of the flagship's conversions fall outside r_200 at both delta_t0" and F2 "S(r_F) <= 0.059 for
     every FK1 variant on both footings".
  F1' [load-bearing, re-declared before the rerun] at FK1's own rate in its coherent (cold-stream) limit (Gamma = 1e3 H: the
     conversion time at twice the threshold, ~E_need/(2 G_t) ~ 3 Myr at z = 2.5; a stream with sigma = 20-60 km/s converts at
     ~25-75 H, XR12_filament_trigger E2, so the 10 H and 1e3 H rows bracket a real stream; I50 adds 50 H for the flagship)
     with streams >= 50% of the flagship's conversions fall outside r_200 at
     delta_t0 = 5.31, and without clumping <= 10% do (at both delta_t0): smooth spherical infall stays below n_t until
     inside r_200; streams cross it upstream.
  F2a [load-bearing, re-declared] THE OWN-DENSITY CAP: at FK1's rate the cold carrier inside r_F stays at or below the
     threshold, S_cold(r_F) <= 1.5 S_cap with S_cap = rho_t (4 pi/3) r_F^3 / M_c,LCDM(<r_F), for every FK1 variant.
  F2b [load-bearing, re-declared] the flagship at FK1's rate: S(r_F) <= 0.059 on both footings at delta_t0 = 5.31 (every
     variant), and S(r_F) > 0.059 on the canonical footing at delta_t0 = 25 (every variant).
  I50 [reported] the flagship at an intermediate, realistic-stream rate, 50 H.
  W2 [reported] the flagship's largest allowed normalisation from the shell model at FK1's rate against the forest's
     smallest (XR12_forest_halo_model W, read from its JSON): the band [zeta_forest, zeta_flagship], open or closed.
  X1 [reported] cluster retention eps(<1 Mpc/h), eps(<R_500) for every variant against its own no-decay run, and the
     implied shift of L388's pooled eps (0.374-0.607) -- inside or outside the two-sided X-COP gate.
MUTATE=1: v_k = 0 in every decaying run (the daughters stay): F2b must FAIL (rc = 1).

HISTORY (disclosed).  The first run (same seeds, Gamma = 10 H only) failed its pre-declared F1 (0.47/0.40 of conversions
outside r_200 at delta_t0 = 25) and F2 (S(r_F) = 0.075-0.30 canonical).  Diagnosis: at Gamma = 10 H the refilling carrier
overshoots n_t while it waits (S_cold(r_F) = 0.05-0.26, up to 3.4x the own-density cap rho_t/rho_bar(<r_F)), and a trigger
that reads the fluid's OWN density stops once a region is thin (re-seeding from vacuum needs n_t again), so late infall is
converted late and deep.  FK1's own rate was then added and F1', F2a, F2b were declared before the rerun; the Gamma = 10 H
rows and their original claims are kept (R10).  The rerun then showed that at FK1's rate the cold carrier sits well below
the cap and the retained S is mostly the daughters of conversions near r_F -- the readings below say so.

A0 FOOTINGS.  The shell model is Newtonian (the carrier is kernel-invisible; the baryons are static profiles), so a0 enters
only through r_F: canonical 9.3619e-11 -> 38.6 kpc, alt 1.1279e-10 -> 35.2 kpc.  X-COP's gate is two-sided on both
footings (canonical 0.286-0.835, alt 0.220-0.768; the pooled gate uses the tighter end of each side).

SCOPE.  Spherical and smooth (streams enter only through C_s; no substructure orbits, no mergers); static baryon profiles;
the trigger rate Gamma = 10 H as the record's (FK1's is faster, which only moves conversions outward); one seed per run.
Read-only on every other file: L375/L376 are imported for their helpers (import-safe, their main is guarded) and their
committed JSON is read; nothing outside this folder is written.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR12_stream_shells.py
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, json, math, time
import numpy as np
from scipy.integrate import cumulative_trapezoid

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DS = os.path.join(REPO, "real_research", "dark_sector_2026")
sys.path.insert(0, DS)
import L376_triggered_carrier_inner_galaxies as L76                 # noqa: E402  (import-safe: helpers only)
L5 = L76.L5
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR12_stream_shells"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "XR12", "part": "3/4 stream shells", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name.split(" ")[0]] = {"ok": ok, "claim": name, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 112); P(t); P("=" * 112)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: v_k = 0 in every decaying run; F2 must FAIL ***")

G, TU, Om, FB, H0, RHOC0, E, mfn = L5.G, L5.TU, L5.Om, L5.FB, L5.H0, L5.RHOC0, L5.E, L5.mfn
t_of_z, z_of_t, r200_of, h = L5.t_of_z, L5.z_of_t, L5.r200_of, L5.h
RS_L376 = np.geomspace(0.5, 100.0, 60)
RHOBAR_C0 = (1 - FB) * Om * RHOC0                                   # Msun/kpc^3


def halo2_trig(cfg, trig, rs_eval=RS_L376, track=False):
    """L376's halo2(), line for line, with the trigger (and optional upstream daughters) as a parameter.  With
    trig = {'kind': 'x5'} and no upstream it is L376's code path exactly (same arithmetic and random-number order)."""
    tag, M0, c0, Mb, vk, gam, alpha, grow_b, N, seed, zobs, zstart = cfg
    rng = np.random.default_rng(seed)
    r0 = r200_of(M0, zobs); rs0 = r0 / c0
    ab = 3.0 * (Mb / 1e11) ** 0.3; Mcgm = max(FB * M0 - Mb, 0.0)
    Mz = (lambda z: M0 * math.exp(-alpha * (z - zobs))) if alpha > 0 else (lambda z: M0)
    up = trig.get("upstream")
    rng_up = np.random.default_rng(seed + 7919) if up else None                 # separate stream: the control is untouched

    def Mst(r, z):
        f = Mz(z) / M0 if grow_b else 1.0
        return f * (Mb * r ** 2 / (r + ab) ** 2 + Mcgm * np.minimum(mfn(r / rs0) / mfn(c0), 1.0))

    def rho_st(r, z):
        f = Mz(z) / M0 if grow_b else 1.0
        return f * (Mb * ab / (2 * math.pi * r * (r + ab) ** 3) +
                    np.where(r < r0, Mcgm / (4 * math.pi * rs0 ** 3 * mfn(c0)) / ((r / rs0) * (1 + r / rs0) ** 2), 0.0))

    zs = zstart if alpha > 0 else zobs + 0.85
    m = (1 - FB) * M0 / N
    Mi = Mz(zs); ci = 4.0 if alpha > 0 else c0; ri = r200_of(Mi, zs) if alpha > 0 else r0; rsi = ri / ci
    Ni = int(round((1 - FB) * Mi / m))
    u = rng.random(Ni) * mfn(ci); xg = np.geomspace(1e-5, ci, 20000); r = np.interp(u, mfn(xg), xg) * rsi
    rg = np.geomspace(1e-3 * rsi, ri, 4000)
    rho_c = (1 - FB) * Mi / (4 * math.pi * rsi ** 3 * mfn(ci)) / ((rg / rsi) * (1 + rg / rsi) ** 2)
    Mc_r = (1 - FB) * Mi * mfn(rg / rsi) / mfn(ci)
    integ = rho_c * G * (Mst(rg, zs) + Mc_r) / rg ** 2
    tail = -np.concatenate([[0.0], cumulative_trapezoid(integ[::-1], rg[::-1])])[::-1]
    sg = np.sqrt(np.maximum(np.interp(r, rg, tail / rho_c), 0.0))
    v = rng.normal(size=(Ni, 3)) * sg[:, None]
    vr = v[:, 0].copy(); L = r * np.hypot(v[:, 1], v[:, 2]); cold = np.ones(Ni, bool)

    t0, t1 = t_of_z(zs), t_of_z(zobs)
    dt = 1.0e-3 / TU; nstep = int(math.ceil((t1 - t0) / dt)); dt = (t1 - t0) / nstep
    rmin = 0.05; edges = np.geomspace(0.05, 2e4, 240); rmid = np.sqrt(edges[1:] * edges[:-1])
    vol = 4 / 3 * math.pi * (edges[1:] ** 3 - edges[:-1] ** 3)
    carry = 0.0; t = t0; z = zs
    conv_r, conv_n = [], 0

    def acc(r, z):
        order = np.argsort(r); rank = np.empty(len(r), int); rank[order] = np.arange(len(r))
        return -G * (Mst(r, z) + m * (rank + 0.5)) / r ** 2 + L ** 2 / r ** 3

    a_ = acc(r, z)
    for i in range(nstep):
        vr += 0.5 * dt * a_
        r = r + dt * vr
        neg = r < rmin; r[neg] = 2 * rmin - r[neg]; vr[neg] = np.abs(vr[neg])
        t += dt; z = z_of_t(t)
        if alpha > 0:
            carry += (1 - FB) * (Mz(z) - Mz(z_of_t(t - dt))) / m
            k = int(carry); carry -= k
            if k > 0:
                Mnow = Mz(z); rn = 2 * r200_of(Mnow, z); v200 = math.sqrt(G * Mnow / r200_of(Mnow, z))
                r = np.concatenate([r, np.full(k, rn) * (1 + 0.05 * rng.random(k))])
                vr_new = np.full(k, -v200); L_new = rn * 0.4 * v200 * np.ones(k); cold_new = np.ones(k, bool)
                if up:
                    fu = float(np.interp(z, up["z"], up["Fu"])); w = float(np.interp(z, up["z"], up["w"]))
                    pre = rng_up.random(k) < fu
                    if pre.any():
                        nh = rng_up.normal(size=(int(pre.sum()), 3)); nh /= np.linalg.norm(nh, axis=1)[:, None]
                        vr_new[pre] += w * nh[:, 0]
                        L_new[pre] = rn * np.hypot(0.4 * v200 + w * nh[:, 1], w * nh[:, 2])
                        cold_new[pre] = False
                vr = np.concatenate([vr, vr_new]); L = np.concatenate([L, L_new]); cold = np.concatenate([cold, cold_new])
        a_ = acc(r, z)
        vr += 0.5 * dt * a_
        if gam > 0 and cold.any():
            if trig["kind"] == "x5":                                            # L375/L376's trigger, unchanged
                cnt, _ = np.histogram(r, edges)
                rho_tot = cnt * m / vol + rho_st(rmid, z)
                xt = 1.5 * (np.interp(r, rmid, rho_tot) - Om * RHOC0 * (1 + z) ** 3) / (RHOC0 * E(z) ** 2)
                idx = np.where(cold & (xt > 5.0))[0]
            else:                                                               # FK1: the cold carrier's own density, K-gated
                cntc, _ = np.histogram(r[cold], edges)
                loc = np.interp(r, rmid, cntc * m / vol)
                if trig.get("Cs", 1.0) > 1.0:
                    loc = np.where(r > r200_of(Mz(z), z), trig["Cs"] * loc, loc)
                idx = np.where(cold & (loc > trig["dt0"] * RHOBAR_C0 * E(z) ** 4))[0]
            hit = idx[rng.random(len(idx)) < 1 - math.exp(-gam * H0 * E(z) * dt)]
            if len(hit):
                nh = rng.normal(size=(len(hit), 3)); nh /= np.linalg.norm(nh, axis=1)[:, None]
                vt_old = L[hit] / r[hit]
                vr[hit] += vk * nh[:, 0]
                L[hit] = r[hit] * np.hypot(vt_old + vk * nh[:, 1], vk * nh[:, 2])
                cold[hit] = False
                if track:
                    conv_r.append(r[hit] / r200_of(Mz(z), z)); conv_n += len(hit)
    Menc = np.array([np.sum(r < x) for x in rs_eval]) * m
    Menc_cold = np.array([np.sum((r < x) & cold) for x in rs_eval]) * m
    Mb_enc = Mst(rs_eval, zobs)
    out = dict(r=rs_eval, Mc=Menc, Mc_cold=Menc_cold, Mbar=Mb_enc, ab=ab, M_ap=float(np.sum(r < L5.RAP)) * m)
    if track:
        cr = np.concatenate(conv_r) if conv_r else np.array([])
        out["conv"] = dict(n=int(conv_n), frac_outside_r200=float(np.mean(cr > 1.0)) if len(cr) else float("nan"),
                           median_r_over_r200=float(np.median(cr)) if len(cr) else float("nan"),
                           conv_over_accreted=float(conv_n) / max(len(r) - Ni, 1))
    return tag, out


# ============================================================================================ C1 control
banner("C1  CONTROL: the re-implementation with L375/L376's own trigger reproduces L376's committed RC100 z = 2 numbers")
R76 = json.load(open(os.path.join(DS, "L376_triggered_carrier_inner_galaxies_results.json")))["numbers"]["rc100"]["z2"]
c_z2 = L76.c200_dm(1e12, 2.0)
_, d_rc = halo2_trig(("rc_z2", 1e12, c_z2, 1e11, 650.0, 10.0, 0.75, True, 60000, 2002, 2.0, 4.75), {"kind": "x5"})
_, d_r0 = halo2_trig(("rc_z2_nodecay", 1e12, c_z2, 1e11, 650.0, 0.0, 0.75, True, 60000, 2102, 2.0, 4.75), {"kind": "x5"})
Re = 1.815 * d_rc["ab"]
mc = L76.interp_log(Re, d_rc["r"], np.maximum(d_rc["Mc"], 1e-30)); mc0 = L76.interp_log(Re, d_r0["r"], d_r0["Mc"])
mb = L76.interp_log(Re, d_rc["r"], d_rc["Mbar"])
gN = G * mb / Re ** 2 * L76.KMS2_KPC; gL = gN + G * mc0 / Re ** 2 * L76.KMS2_KPC
cr, fl = mc / mc0, float(1 - gN / gL)
_, d_small = halo2_trig(("eq", 1e12, c_z2, 1e11, 650.0, 10.0, 0.75, True, 3000, 77, 2.0, 4.75), {"kind": "x5"})
_, d_small76 = L76.halo2(("eq", 1e12, c_z2, 1e11, 650.0, 10.0, 0.75, True, 3000, 77, 2.0, 4.75))
eq = bool(np.array_equal(d_small["Mc"], d_small76["Mc"]) and np.array_equal(d_small["Mc_cold"], d_small76["Mc_cold"]))
P(f"    carrier inside R_e / LCDM's = {cr:.6e} (L376 {R76['carrier_ratio']:.6e});  f_DM,LCDM(<R_e) = {fl:.6f} "
  f"(L376 {R76['fDM']['canonical']['fDM_lcdm']:.6f});  a small-N run is bit-identical to L376's halo2(): {eq}   [{time.time() - T0:.0f}s]")
OUT["numbers"]["C1"] = dict(carrier_ratio=cr, fDM_lcdm=fl, identical_small_N=eq)
check("C1 CONTROL: with L375/L376's own trigger the re-implementation reproduces L376's committed RC100 z = 2 numbers exactly "
      "and is bit-identical to L376's halo2() on a fresh configuration",
      f"carrier ratio {cr:.6e} vs {R76['carrier_ratio']:.6e}; f_DM {fl:.6f} vs {R76['fDM']['canonical']['fDM_lcdm']:.6f}; identical {eq}",
      abs(cr / R76["carrier_ratio"] - 1) < 1e-9 and abs(fl - R76["fDM"]["canonical"]["fDM_lcdm"]) < 1e-12 and eq)

# ============================================================================================ inputs: the upstream daughters
banner("UPSTREAM  the converted-and-escaped fraction F_u(z) and the daughters' speed w(z), from XR12_forest_halo_model H1")
RF = os.path.join(HERE, "XR12_forest_halo_model_results.json")
UP = {}
if os.path.exists(RF):
    HM = json.load(open(RF))["numbers"]
    for lab, key in (("5.31", "Fu"), ("25", "Fu_upper25")):
        pairs = sorted((float(z_), float(v_)) for z_, v_ in HM["H1"][key].items())
        UP[lab] = (np.array([p_[0] for p_ in pairs]), np.array([p_[1] for p_ in pairs]))
else:
    P("    XR12_forest_halo_model_results.json not found: run XR12_forest_halo_model.py first"); sys.exit(2)


def upstream(zg, Fu, vk):
    """F_u(z) and w(z) = v_k <(1+z)/(1+z_c)> over the conversions before z (peculiar momentum ~ 1/a after conversion)."""
    zfine = np.linspace(0.0, 12.0, 1201); Ff = np.interp(zfine, zg, Fu)
    dF = -np.gradient(Ff, zfine)                                                # dF/d(-z): conversions per unit redshift
    w = []
    for z in zfine:
        sel = zfine >= z
        num = np.trapz(np.clip(dF[sel], 0, None) * (1 + z) / (1 + zfine[sel]), zfine[sel])
        den = np.trapz(np.clip(dF[sel], 0, None), zfine[sel])
        w.append(vk * num / den if den > 0 else vk)
    return dict(z=zfine, Fu=Ff, w=np.array(w))


UPS = {lab: upstream(*UP[lab], 600.0) for lab in UP}
for lab, U in UPS.items():
    P(f"    delta_t0 = {lab:5s}: F_u(z = 0/1/2/2.5/3) = " + "/".join(f"{float(np.interp(z_, U['z'], U['Fu'])):.3f}" for z_ in (0, 1, 2, 2.5, 3))
      + ";  w(z = 0/1/2/2.5) = " + "/".join(f"{float(np.interp(z_, U['z'], U['w'])):.0f}" for z_ in (0, 1, 2, 2.5)) + " km/s")
OUT["numbers"]["upstream"] = {lab: dict(z=[0, 1, 2, 2.5, 3], Fu=[float(np.interp(z_, U["z"], U["Fu"])) for z_ in (0, 1, 2, 2.5, 3)],
                                        w=[float(np.interp(z_, U["z"], U["w"])) for z_ in (0, 1, 2, 2.5, 3)]) for lab, U in UPS.items()}

VK = 0.0 if MUTATE else 600.0
GAM_REC, GAM_FK1 = 10.0, 1000.0
_BASE = {"FK1 5.31": {"kind": "fk1", "dt0": 5.311}, "FK1 5.31, streams C_s=10": {"kind": "fk1", "dt0": 5.311, "Cs": 10.0},
         "FK1 5.31, streams + upstream": {"kind": "fk1", "dt0": 5.311, "Cs": 10.0, "upstream": UPS["5.31"]},
         "FK1 25": {"kind": "fk1", "dt0": 25.0}, "FK1 25, streams C_s=10": {"kind": "fk1", "dt0": 25.0, "Cs": 10.0},
         "FK1 25, streams + upstream": {"kind": "fk1", "dt0": 25.0, "Cs": 10.0, "upstream": UPS["25"]}}
VARIANTS = {"nodecay": ({"kind": "x5"}, 0.0), "x5 (L375/L376 trigger)": ({"kind": "x5"}, GAM_REC)}
for lab, tr in _BASE.items():
    VARIANTS[f"{lab} @10H"] = (tr, GAM_REC)
for lab, tr in _BASE.items():
    VARIANTS[f"{lab} @FK1 rate"] = (tr, GAM_FK1)

# ============================================================================================ the flagship host, z = 2.5
banner("FLAGSHIP  M_200 = 1e12, M_b = 1e11, z = 2.5: where the carrier converts, and S(r_F)")
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
rF = {f_: math.sqrt(6.674e-11 * 1e11 * 1.989e30 / (0.1 * a0)) / 3.0857e19 for f_, a0 in A0.items()}
RS_F = np.array(sorted(set(np.round(np.geomspace(0.5, 400.0, 70), 6)) | {round(rF["canonical"], 6), round(rF["alt"], 6)}))
c_F = L76.c200_dm(1e12, 2.5)
FL = {}
for lab, (trig, gam) in VARIANTS.items():
    _, d = halo2_trig((lab, 1e12, c_F, 1e11, VK, gam, 0.75, True, 30000, 4001, 2.5, 5.25), trig, rs_eval=RS_F, track=(gam > 0))
    FL[lab] = d
M0F = {f_: float(np.interp(r_, RS_F, FL["nodecay"]["Mc"])) for f_, r_ in rF.items()}
FLr = {}
for lab, d in FL.items():
    if lab == "nodecay": continue
    S = {f_: float(np.interp(r_, RS_F, d["Mc"])) / M0F[f_] for f_, r_ in rF.items()}
    Sc = {f_: float(np.interp(r_, RS_F, d["Mc_cold"])) / M0F[f_] for f_, r_ in rF.items()}
    cv = d.get("conv", {})
    FLr[lab] = dict(S=S, S_cold=Sc, conv=cv)
    P(f"    {lab:40s}: S(r_F) canonical {S['canonical']:.4f} (cold {Sc['canonical']:.4f}), alt {S['alt']:.4f};  conversions outside r_200: "
      f"{cv.get('frac_outside_r200', float('nan')):.2f}, median r/r_200 {cv.get('median_r_over_r200', float('nan')):.2f}, "
      f"conversions / accreted particles {cv.get('conv_over_accreted', float('nan')):.2f}")
P(f"    r_F = {rF['canonical']:.1f} / {rF['alt']:.1f} kpc (canonical / alt);  gate S <= 0.059 (MS2)   [{time.time() - T0:.0f}s]")
OUT["numbers"]["flagship"] = dict(r_F=rF, results=FLr)
RHO_T = {5.311: 5.311 * RHOBAR_C0 * E(2.5) ** 4, 25.0: 25.0 * RHOBAR_C0 * E(2.5) ** 4}
S_cap = {dt: {f_: RHO_T[dt] * 4 / 3 * math.pi * r_ ** 3 / M0F[f_] for f_, r_ in rF.items()} for dt in RHO_T}
P("    the own-density cap S_cap = rho_t (4 pi/3) r_F^3 / M_c,LCDM(<r_F): " + "; ".join(
    f"delta_t0 = {dt:g}: {S_cap[dt]['canonical']:.4f} (canonical) / {S_cap[dt]['alt']:.4f} (alt)" for dt in S_cap))
OUT["numbers"]["flagship"]["S_cap"] = {str(k_): v for k_, v in S_cap.items()}
dt_of = lambda lab: 5.311 if "5.31" in lab else 25.0
rec = [k_ for k_ in FLr if k_.endswith("@10H")]; fast = [k_ for k_ in FLr if k_.endswith("@FK1 rate")]
# R10: the first run's claims on the Gamma = 10 H rows, kept as run
f1_rec = {k_: FLr[k_]["conv"].get("frac_outside_r200", 0.0) for k_ in rec if "streams" in k_}
check("R10 [first run's pre-declared F1 and F2, FALSIFIED, kept as run] at Gamma = 10 H: with streams >= 50% of conversions "
      "outside r_200 at both delta_t0, and S(r_F) <= 0.059 for every FK1 variant on both footings",
      "outside r_200: " + ", ".join(f"{k_.replace(' @10H', '')} {v:.2f}" for k_, v in f1_rec.items()) + "; S(r_F) can/alt: "
      + ", ".join(f"{k_.replace(' @10H', '')} {FLr[k_]['S']['canonical']:.3f}/{FLr[k_]['S']['alt']:.3f}" for k_ in rec),
      all(v >= 0.5 for v in f1_rec.values()) and max(max(FLr[k_]["S"].values()) for k_ in rec) <= 0.059,
      "at 10 H the refilling carrier overshoots the own-density cap while it waits to convert", load_bearing=False)
f1_str = {k_: FLr[k_]["conv"].get("frac_outside_r200", 0.0) for k_ in fast if "streams" in k_ and "5.31" in k_}
f1_smooth = {k_: FLr[k_]["conv"].get("frac_outside_r200", 0.0) for k_ in fast if "streams" not in k_}
check("F1' at FK1's rate, with streams >= 50% of the flagship's conversions fall outside r_200 at delta_t0 = 5.31, and without "
      "clumping <= 10% do (both delta_t0): the streams convert upstream, the smooth infall only inside r_200",
      "streams: " + ", ".join(f"{k_.replace(' @FK1 rate', '')} {v:.2f}" for k_, v in f1_str.items()) + "; smooth: "
      + ", ".join(f"{k_.replace(' @FK1 rate', '')} {v:.2f}" for k_, v in f1_smooth.items()),
      all(v >= 0.5 for v in f1_str.values()) and all(v <= 0.10 for v in f1_smooth.values()))
capok = {k_: max(FLr[k_]["S_cold"][f_] / S_cap[dt_of(k_)][f_] for f_ in rF) for k_ in fast}
dau = {k_: max(FLr[k_]["S"][f_] - FLr[k_]["S_cold"][f_] for f_ in rF) for k_ in fast}
check("F2a THE OWN-DENSITY CAP: at FK1's rate the cold carrier inside r_F stays at or below the threshold, S_cold(r_F) <= "
      "1.5 S_cap, for every FK1 variant and both footings",
      ", ".join(f"{k_.replace(' @FK1 rate', '')}: S_cold/S_cap {v:.2f} (daughters {dau[k_]:.3f})" for k_, v in capok.items()),
      all(v <= 1.5 for v in capok.values()),
      "at FK1's rate the cold carrier transits r_F thin and converts where it crosses n_t; what the flagship retains is mostly "
      "the daughters of conversions near r_F, not a carrier parked at the cap")
s531 = {k_: FLr[k_]["S"] for k_ in fast if "5.31" in k_}; s25 = {k_: FLr[k_]["S"] for k_ in fast if "25" in k_}
check("F2b the flagship at FK1's rate: S(r_F) <= 0.059 on both footings at delta_t0 = 5.31 (every variant), and S(r_F) > 0.059 "
      "on the canonical footing at delta_t0 = 25 (every variant)",
      "5.31: " + ", ".join(f"{k_.replace(' @FK1 rate', '')} {v['canonical']:.4f}/{v['alt']:.4f}" for k_, v in s531.items())
      + "; 25: " + ", ".join(f"{k_.replace(' @FK1 rate', '')} {v['canonical']:.4f}/{v['alt']:.4f}" for k_, v in s25.items()),
      all(max(v.values()) <= 0.059 for v in s531.values()) and all(v["canonical"] > 0.059 for v in s25.values()),
      "the flagship bounds FK1's normalisation from ABOVE: a higher threshold moves the conversion inward (median 0.40 r_200 "
      "at delta_t0 = 25 against 1.2-1.4 r_200 with streams at 5.31), so more of the cold carrier and of the daughters stay "
      "inside r_F: it holds at the linear cell's matter reading and fails at FK1's upper bracket")
# I50: an intermediate, realistic-stream rate for the flagship (sigma ~ 20-60 km/s streams: ~25-75 H, XR12_filament_trigger E2)
I50 = {}
for lab in ("FK1 5.31", "FK1 5.31, streams C_s=10", "FK1 5.31, streams + upstream", "FK1 25, streams C_s=10"):
    _, d = halo2_trig((lab + " @50H", 1e12, c_F, 1e11, VK, 50.0, 0.75, True, 30000, 4001, 2.5, 5.25), _BASE[lab], rs_eval=RS_F, track=True)
    I50[lab] = {f_: float(np.interp(r_, RS_F, d["Mc"])) / M0F[f_] for f_, r_ in rF.items()}
    P(f"    I50 {lab:32s} @50H: S(r_F) canonical {I50[lab]['canonical']:.4f}, alt {I50[lab]['alt']:.4f};  conversions outside r_200 "
      f"{d['conv'].get('frac_outside_r200', float('nan')):.2f}")
OUT["numbers"]["flagship"]["I50"] = I50
check("I50 (reported) at a realistic-stream rate (50 H) the flagship at delta_t0 = 5.31 with streams stays within S <= 0.059 on "
      "both footings", "; ".join(f"{k_}: {v['canonical']:.4f}/{v['alt']:.4f}" for k_, v in I50.items()),
      all(max(I50[k_].values()) <= 0.059 for k_ in ("FK1 5.31, streams C_s=10", "FK1 5.31, streams + upstream")),
      "between the record's 10 H (fails) and the cold limit (passes): where a real stream's rate puts the nominal cell",
      load_bearing=False)
# W2: the band in zeta
HMW = HM["W"]
zf_forest = {var: HMW["window"][var]["zeta_forest"] for var in ("plain", "sqrt_sigma")}
W2 = {}
for f_ in rF:
    for var in ("streams C_s=10", "streams + upstream"):
        a_ = FLr[f"FK1 5.31, {var} @FK1 rate"]["S"][f_]; b_ = FLr[f"FK1 25, {var} @FK1 rate"]["S"][f_]
        if a_ < 0.059 < b_:
            zmax = math.exp(math.log(25.0 / 5.311) * math.log(0.059 / a_) / math.log(b_ / a_))   # log-log between the brackets
        else:
            zmax = float("nan") if a_ >= 0.059 else float("inf")
        W2[f"{f_}/{var}"] = dict(S_531=a_, S_25=b_, zeta_flagship=zmax,
                                 open_plain=bool(zf_forest["plain"] < zmax), open_sqrt_sigma=bool(zf_forest["sqrt_sigma"] < zmax))
        P(f"    W2 {f_:9s} {var:20s}: S(r_F) = {a_:.4f} (5.31) / {b_:.4f} (25) -> the flagship allows zeta <= {zmax:.2f} (delta_t0 <= "
          f"{5.311 * zmax:.1f});  forest needs >= {zf_forest['plain']:.2f} (plain) / {zf_forest['sqrt_sigma']:.2f} (sqrt sigma) -> "
          f"{'OPEN' if W2[f'{f_}/{var}']['open_plain'] else 'CLOSED'} / {'OPEN' if W2[f'{f_}/{var}']['open_sqrt_sigma'] else 'CLOSED'}")
OUT["numbers"]["W2"] = dict(zeta_forest=zf_forest, cells=W2)
check("W2 (reported) the band between the forest's smallest and the flagship's largest normalisation of FK1's trigger, per "
      "footing and stream variant", "; ".join(f"{k_}: <= {v['zeta_flagship']:.2f} vs forest {zf_forest['plain']:.2f}/{zf_forest['sqrt_sigma']:.2f} "
                                             f"-> {'open' if v['open_plain'] else 'closed'}/{'open' if v['open_sqrt_sigma'] else 'closed'}" for k_, v in W2.items()),
      all(v["open_plain"] for v in W2.values()),
      "open on the plain forest proxy is a narrow band, not a window; with FK1's sqrt(sigma) modulation the minihalos convert "
      "more easily and the band's two ends meet or cross", load_bearing=False)

# ============================================================================================ the cluster, z = 0
banner("CLUSTER  M_200 = 8e14, BCG 1e12, z = 0: retention inside 1 Mpc/h and R_500, against the two-sided X-COP gate")
M_CL = 8e14
c_CL = L76.c200_dm(M_CL, 0.0)
r200_cl = r200_of(M_CL, 0.0)
from scipy.optimize import brentq
m_c = float(mfn(c_CL))
r500 = brentq(lambda rr: M_CL * float(mfn(rr / (r200_cl / c_CL))) / m_c / (4 / 3 * math.pi * rr ** 3) - 500 * RHOC0, 0.2 * r200_cl, r200_cl)
RAP1 = 1000.0 / h
RS_C = np.array(sorted(set(np.round(np.geomspace(10.0, 4000.0, 60), 6)) | {round(r500, 6), round(RAP1, 6)}))
CL = {}
for lab, (trig, gam) in VARIANTS.items():
    _, d = halo2_trig((lab, M_CL, c_CL, 1e12, VK, gam, 0.75, True, 16000, 5001, 0.0, 2.75), trig, rs_eval=RS_C, track=(gam > 0))
    CL[lab] = d
    P(f"    ... {lab} done   [{time.time() - T0:.0f}s]")
R366 = json.load(open(os.path.join(DS, "L366_triggered_carrier_cluster_retention_results.json")))["numbers"]["eps_bounds"]
lo_g = max(R366["canonical"][0], R366["alt"][0]); hi_g = min(R366["canonical"][1], R366["alt"][1])
L388 = json.load(open(os.path.join(DS, "L388_linear_gate_pooled_results.json")))["numbers"]["table"]["pooled"]
eps388 = {t: L388[t]["eps_cl"] for t in ("v575", "v600", "v625", "v650")}
CLr = {}
base1 = float(np.interp(RAP1, RS_C, CL["nodecay"]["Mc"])); base5 = float(np.interp(r500, RS_C, CL["nodecay"]["Mc"]))
for lab, d in CL.items():
    if lab == "nodecay": continue
    e1 = float(np.interp(RAP1, RS_C, d["Mc"])) / base1; e5 = float(np.interp(r500, RS_C, d["Mc"])) / base5
    CLr[lab] = dict(eps_1Mpch=e1, eps_R500=e5, conv=d.get("conv", {}))
ref = CLr["x5 (L375/L376 trigger)"]["eps_1Mpch"]
for lab, v in CLr.items():
    shift = v["eps_1Mpch"] / ref
    v["shift_vs_x5"] = shift
    v["L388_scaled"] = {t: e * shift for t, e in eps388.items()}
    inside = all(lo_g <= e <= hi_g for e in v["L388_scaled"].values())
    v["L388_scaled_inside_gate"] = inside
    cv = v["conv"]
    P(f"    {lab:40s}: eps(<1 Mpc/h) {v['eps_1Mpch']:.3f}, eps(<R_500) {v['eps_R500']:.3f}; x{shift:.2f} of the x5 trigger's -> L388 pooled "
      f"575-650 would read {min(v['L388_scaled'].values()):.3f}-{max(v['L388_scaled'].values()):.3f} "
      f"({'inside' if inside else 'OUTSIDE'} {lo_g:.3f}-{hi_g:.3f});  conversions outside r_200: {cv.get('frac_outside_r200', float('nan')):.2f}")
P(f"    r_200 = {r200_cl:.0f} kpc, R_500 = {r500:.0f} kpc, 1 Mpc/h = {RAP1:.0f} kpc (z = 0);  L388 pooled eps 575-650: "
  + ", ".join(f"{t} {e:.3f}" for t, e in eps388.items()))
OUT["numbers"]["cluster"] = dict(M200=M_CL, c=c_CL, r200=r200_cl, r500=r500, results=CLr, gate=[lo_g, hi_g], L388_pooled=eps388)
fk1c = [k_ for k_ in CLr if k_.startswith("FK1")]
fk1c_fast = [k_ for k_ in fk1c if k_.endswith("@FK1 rate")]
check("X1 (reported) cluster retention under FK1's trigger, scaled onto L388's pooled 575-650 km/s values by the shell model's "
      "shift against the record's x5 trigger, stays inside the two-sided X-COP gate for every variant",
      "; ".join(f"{k_}: x{CLr[k_]['shift_vs_x5']:.2f} -> {min(CLr[k_]['L388_scaled'].values()):.2f}-{max(CLr[k_]['L388_scaled'].values()):.2f}"
                for k_ in fk1c),
      all(CLr[k_]["L388_scaled_inside_gate"] for k_ in fk1c),
      "a shift estimate on a spherical, smooth model: the PM owners should re-run with FK1's trigger variable", load_bearing=False)

# ============================================================================================ summary
banner("SUMMARY")
P(f"""  Question (A), the flagship and clusters, in the record's resolved shell model with FK1's own trigger:
  - Where it converts (FK1's rate): with streams {min(f1_str.values()):.0%}-{max(f1_str.values()):.0%} of the flagship's conversions fall outside r_200
    (delta_t0 = 5.31); smooth spherical infall converts only inside it ({max(f1_smooth.values()):.0%} outside) (F1').
  - The own-density cap holds: the cold carrier inside r_F stays below n_t (S_cold/S_cap <= {max(capok.values()):.2f}); what r_F retains is
    mostly daughters of conversions near it (<= {max(dau.values()):.3f}) (F2a).  So the flagship holds at the linear cell's reading
    (S(r_F) <= {max(max(v.values()) for v in s531.values()):.4f}) and fails at FK1's upper bracket (S(r_F) >= {min(v['canonical'] for v in s25.values()):.3f} canonical) (F2b).
  - The band (W2): forest zeta >= {zf_forest['plain']:.2f} (plain) / {zf_forest['sqrt_sigma']:.2f} (sqrt sigma) against the flagship's zeta <= """
  + ", ".join(f"{v['zeta_flagship']:.2f}" for v in W2.values()) + f""".
  - Clusters at FK1's rate: shifts against the x5 trigger x{min(CLr[k_]['shift_vs_x5'] for k_ in fk1c_fast):.2f}-{max(CLr[k_]['shift_vs_x5'] for k_ in fk1c_fast):.2f} -> L388's pooled
    eps would read {min(min(CLr[k_]['L388_scaled'].values()) for k_ in fk1c_fast):.2f}-{max(max(CLr[k_]['L388_scaled'].values()) for k_ in fk1c_fast):.2f} against {lo_g:.3f}-{hi_g:.3f} (X1).""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["summary"] = dict(load_bearing_failed=n_fail, n_checks=len(CH), runtime_s=round(time.time() - T0, 1))
suffix = "_MUTATE" if MUTATE else ""
json.dump(OUT, open(os.path.join(HERE, f"{SLUG}_results{suffix}.json"), "w"), indent=1, default=str)
P(f"\n  checks: {sum(ok for _, ok, _ in CH)}/{len(CH)} pass; load-bearing failures: {n_fail}   [{time.time() - T0:.0f}s]")
sys.exit(1 if n_fail else 0)

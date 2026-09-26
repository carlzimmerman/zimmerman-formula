#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L376 -- THE TRIGGERED CARRIER INSIDE GALAXIES, RESOLVED: does the carrier that survives or is retained contaminate
rotation curves -- the radial acceleration relation at z ~ 0 and the dark fractions RC100 measures at z ~ 1-2.5?

WHY.  L365-L368's cosmological runs scored galaxy interiors only through a proxy: the carrier left in dense cells at z = 2
(halo clearing, G3 <= 0.30 of LCDM's) on a 0.39 Mpc/h mesh.  L375 resolved KiDS hosts and found the retained carrier is
mostly undecayed infalling material at r >~ r_200.  What is INSIDE, where rotation curves are measured, was not resolved.
In the construction the phantom (sourced by baryons only) supplies the rotation-curve "dark matter"; any carrier left inside
adds Newtonian acceleration ON TOP of the phantom and moves galaxies off the RAR.

MODEL: L375's shell model, unchanged and generalised to any host (M_200, M_b) and observing redshift z_obs (the accretion
history is started 2.75 in redshift earlier, as L375's; concentration from Dutton & Maccio 2014's z-dependent fit).  The
carrier is kernel-invisible (L353), so its acceleration adds as g_c = G M_c(<r)/r^2 to the phantom-inclusive
g_MOND = nu_RAR(g_N/a_0) g_N of the baryons (both footings of a_0).
PRE-DECLARED GATES (before the run):
  RAR (z = 0): for a dwarf (M_200 = 1e11, M_b = 3e9), a Milky-Way host (1e12, 6e10) and a massive spiral (5e12, 2e11),
     the carrier shifts log g_obs by Delta = log10(1 + g_c/g_MOND) <= 0.057 dex (the RAR's intrinsic-scatter bound,
     Lelli+17) at r = 2, 4, 8 R_d, both footings.
  RC100 (z = 1, 2): for a 1e12 host with M_b = 1e11, the carrier inside R_e is <= 0.30 of the LCDM carrier there (the
     record's halo-clearing threshold, now resolved); the resulting f_DM(<R_e) (phantom + carrier) is reported.
  H1: the RAR gate passes for all three hosts.  H2: the RC100 gate passes at z = 1 and 2.
CHECKS
  C1 CONTROL: the generalised code reproduces L375's committed fiducial S for KiDS bin 2 exactly (same seeds).
  C2 CONTROL: with the decay off (LCDM-like carrier) the RAR gate FAILS for the Milky-Way host (the gate has teeth).
  R1 = H1.  R2 = H2.  I (informational): Delta per host and radius, the RC100 f_DM(<R_e).
MUTATE=1: v_k = 0 in every decaying run: R1 must FAIL (rc = 1).

Run from the repository root:  python3 real_research/dark_sector_2026/L376_triggered_carrier_inner_galaxies.py
"""
import os, sys, json, math, time
import numpy as np
from multiprocessing import Pool
from scipy.integrate import cumulative_trapezoid

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import L375_triggered_carrier_galaxy_retention as L5            # noqa: E402  (L375's units, background and helpers)

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L376_triggered_carrier_inner_galaxies"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L376", "mutate": MUTATE, "checks": {}, "numbers": {}}
EXPECT_RAR, EXPECT_RC = True, True                               # H1, H2: set before the run

G, TU, Om, FB, H0, RHOC0, E, mfn = L5.G, L5.TU, L5.Om, L5.FB, L5.H0, L5.RHOC0, L5.E, L5.mfn
t_of_z, z_of_t, r200_of = L5.t_of_z, L5.z_of_t, L5.r200_of
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}                # m/s^2
KMS2_KPC = 1e6 / 3.0857e19                                       # (km/s)^2/kpc in m/s^2
nu_rar = lambda y: 1.0 / (1.0 - np.exp(-np.sqrt(y)))


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


def c200_dm(M, z):
    """Dutton & Maccio 2014, z-dependent (reduces to L360's z = 0 form)."""
    a = 0.520 + (0.905 - 0.520) * math.exp(-0.617 * z ** 1.21); b = -0.101 + 0.026 * z
    return 10 ** (a + b * math.log10(M / (1e12 / L5.h)))


def halo2(cfg):
    """L375's halo(), with the host (M0, c0), z_obs and z_start as inputs; identical arithmetic and random-number order."""
    tag, M0, c0, Mb, vk, gam, alpha, grow_b, N, seed, zobs, zstart = cfg
    rng = np.random.default_rng(seed)
    r0 = r200_of(M0, zobs); rs0 = r0 / c0
    ab = 3.0 * (Mb / 1e11) ** 0.3; Mcgm = max(FB * M0 - Mb, 0.0)
    Mz = (lambda z: M0 * math.exp(-alpha * (z - zobs))) if alpha > 0 else (lambda z: M0)

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
                vr = np.concatenate([vr, np.full(k, -v200)]); L = np.concatenate([L, rn * 0.4 * v200 * np.ones(k)])
                cold = np.concatenate([cold, np.ones(k, bool)])
        a_ = acc(r, z)
        vr += 0.5 * dt * a_
        if gam > 0 and cold.any():
            cnt, _ = np.histogram(r, edges)
            rho_tot = cnt * m / vol + rho_st(rmid, z)
            xt = 1.5 * (np.interp(r, rmid, rho_tot) - Om * RHOC0 * (1 + z) ** 3) / (RHOC0 * E(z) ** 2)
            idx = np.where(cold & (xt > 5.0))[0]
            hit = idx[rng.random(len(idx)) < 1 - math.exp(-gam * H0 * E(z) * dt)]
            if len(hit):
                nh = rng.normal(size=(len(hit), 3)); nh /= np.linalg.norm(nh, axis=1)[:, None]
                vt_old = L[hit] / r[hit]
                vr[hit] += vk * nh[:, 0]
                L[hit] = r[hit] * np.hypot(vt_old + vk * nh[:, 1], vk * nh[:, 2])
                cold[hit] = False
    rs_eval = np.geomspace(0.5, 100.0, 60)
    Menc = np.array([np.sum(r < x) for x in rs_eval]) * m
    Menc_cold = np.array([np.sum((r < x) & cold) for x in rs_eval]) * m
    Mb_enc = Mst(rs_eval, zobs)
    return tag, dict(r=rs_eval, Mc=Menc, Mc_cold=Menc_cold, Mbar=Mb_enc, ab=ab, M_ap=float(np.sum(r < L5.RAP)) * m)


def interp_log(x, xs, ys):
    return float(np.exp(np.interp(math.log(x), np.log(xs), np.log(np.maximum(ys, 1e-30)))))


if __name__ == "__main__":
    P(__doc__)
    N = int(os.environ.get("L376_N", "60000"))
    VK = 0.0 if MUTATE else 650.0
    HOSTS = {"dwarf": (1e11, 3e9), "milky_way": (1e12, 6e10), "massive": (5e12, 2e11)}
    cfgs = []
    # C1: L375's fiducial bin 2 (b = 1), exactly as L375 ran it (z_l = 0.25, z_start = 3, L360's z = 0 concentration)
    R75 = json.load(open(os.path.join(HERE, "L375_triggered_carrier_galaxy_retention_results.json")))["numbers"]
    Mb75 = R75["M_b"][1]; M75 = L5.M200_BINS[1]; c75 = L5.c200(M75)
    cfgs.append(("c1_nodecay", M75, c75, Mb75, 650.0, 0.0, 0.75, True, N, 101, 0.25, 3.0))
    cfgs.append(("c1_fid", M75, c75, Mb75, 650.0, 10.0, 0.75, True, N, 201, 0.25, 3.0))
    for i, (hn, (M0, Mb)) in enumerate(HOSTS.items()):
        c0 = c200_dm(M0, 0.0)
        cfgs.append((f"rar_{hn}", M0, c0, Mb, VK, 10.0, 0.75, True, N, 1000 + i, 0.0, 2.75))
        cfgs.append((f"rar_{hn}_nodecay", M0, c0, Mb, 650.0, 0.0, 0.75, True, N, 1100 + i, 0.0, 2.75))
    for zo in (1.0, 2.0):
        c0 = c200_dm(1e12, zo)
        cfgs.append((f"rc_z{zo:.0f}", 1e12, c0, 1e11, VK, 10.0, 0.75, True, N, 2000 + int(zo), zo, zo + 2.75))
        cfgs.append((f"rc_z{zo:.0f}_nodecay", 1e12, c0, 1e11, 650.0, 0.0, 0.75, True, N, 2100 + int(zo), zo, zo + 2.75))
    if MUTATE:
        P("  MUTATE: v_k = 0 in every decaying run")
    with Pool(int(os.environ.get("L376_POOL", "4"))) as pool:
        res = dict(pool.map(halo2, cfgs, chunksize=1))
    P(f"  {len(cfgs)} halos done   [{time.time() - T0:.0f}s]")

    banner("C1  CONTROL: the generalised shell code reproduces L375")
    S1 = res["c1_fid"]["M_ap"] / res["c1_nodecay"]["M_ap"]; S75 = R75["table"]["fid"]["S"][1]
    check("C1 L375's fiducial bin-2 retention reproduced exactly by the generalised code (same seeds, same arithmetic)",
          f"S = {S1:.6f} vs L375 {S75:.6f}", abs(S1 - S75) < 1e-9)

    def rar_table(tag):
        d = res[tag]; Rd = 1.08 * d["ab"]; rows = {}
        for f_, a0 in A0.items():
            for k in (2, 4, 8):
                rk = k * Rd
                gN = G * interp_log(rk, d["r"], d["Mbar"]) / rk ** 2 * KMS2_KPC
                gM = nu_rar(gN / a0) * gN
                gc = G * interp_log(rk, d["r"], np.maximum(d["Mc"], 1e-30)) / rk ** 2 * KMS2_KPC if np.any(d["Mc"] > 0) else 0.0
                rows[f"{f_}/{k}Rd"] = dict(r_kpc=rk, Delta_dex=float(math.log10(1 + gc / gM)))
        return rows

    banner("RAR AT z = 0: the carrier's shift of log g_obs at 2, 4, 8 R_d (gate <= 0.057 dex)")
    RAR = {}
    for hn in HOSTS:
        RAR[hn] = rar_table(f"rar_{hn}"); RAR[hn + "_nodecay"] = rar_table(f"rar_{hn}_nodecay")
        for suf in ("", "_nodecay"):
            rw = RAR[hn + suf]
            P(f"    {hn + suf:20s}: " + ", ".join(f"{k_}: {v['Delta_dex']:.3f} (r={v['r_kpc']:.1f})" for k_, v in rw.items() if k_.startswith("canonical")) +
              f"  | alt max {max(v['Delta_dex'] for k_, v in rw.items() if k_.startswith('alt')):.3f}")
    OUT["numbers"]["rar"] = RAR
    worst = {hn: max(v["Delta_dex"] for v in RAR[hn].values()) for hn in HOSTS}
    worst0 = max(v["Delta_dex"] for v in RAR["milky_way_nodecay"].values())
    check("C2 CONTROL: with the decay off the carrier moves the Milky-Way host off the RAR (> 0.057 dex): the gate has teeth",
          f"worst Delta (decay off) = {worst0:.3f} dex", worst0 > 0.057)

    banner("RC100 AT z = 1, 2: carrier inside R_e (gate <= 0.30 of LCDM's), and f_DM(<R_e)")
    RC = {}
    for zo in (1, 2):
        d, d0 = res[f"rc_z{zo}"], res[f"rc_z{zo}_nodecay"]; Re = 1.815 * d["ab"]
        mc, mc0 = interp_log(Re, d["r"], np.maximum(d["Mc"], 1e-30)), interp_log(Re, d0["r"], d0["Mc"])
        mb = interp_log(Re, d["r"], d["Mbar"]); fr = {}
        for f_, a0 in A0.items():
            gN = G * mb / Re ** 2 * KMS2_KPC; gM = nu_rar(gN / a0) * gN; gc = G * mc / Re ** 2 * KMS2_KPC
            gL = gN + G * mc0 / Re ** 2 * KMS2_KPC
            fr[f_] = dict(fDM_construction=float(1 - gN / (gM + gc)), fDM_lcdm=float(1 - gN / gL))
        RC[f"z{zo}"] = dict(Re_kpc=Re, carrier_ratio=mc / mc0, fDM=fr)
        P(f"    z = {zo}: R_e = {Re:.1f} kpc; carrier inside R_e / LCDM's = {mc / mc0:.3f};  f_DM(<R_e): construction "
          + ", ".join(f"{f_} {v['fDM_construction']:.2f}" for f_, v in fr.items()) + f"; LCDM carrier {fr['canonical']['fDM_lcdm']:.2f}")
    OUT["numbers"]["rc100"] = RC
    check("I (informational) RAR shifts per host and radius; RC100 f_DM(<R_e) for the construction and for the LCDM carrier",
          "see tables", True, "reported either way", load_bearing=False)

    banner("R1, R2  THE HYPOTHESES (set before the run)")
    check("R1 = H1: the retained carrier keeps all three z = 0 hosts on the RAR (Delta <= 0.057 dex at 2, 4, 8 R_d, both footings)",
          f"worst Delta by host: {worst}", all(v <= 0.057 for v in worst.values()) == EXPECT_RAR)
    check("R2 = H2: the carrier inside R_e at z = 1 and 2 is <= 0.30 of LCDM's (the halo-clearing gate, resolved)",
          f"{ {k_: round(v['carrier_ratio'], 3) for k_, v in RC.items()} }", all(v["carrier_ratio"] <= 0.30 for v in RC.values()) == EXPECT_RC)

    banner("VERDICT")
    P(f"""  Resolved galaxy interiors under the triggered carrier (v_k = {VK:.0f} km/s): RAR worst shifts {worst} dex (gate 0.057);
  carrier inside R_e at z = 1/2: {[round(RC[k_]['carrier_ratio'], 3) for k_ in ('z1', 'z2')]} of LCDM's (gate 0.30).
  LIMITS: spherical shells, smooth accretion history, static baryons, nu_RAR on the Hernquist baryons (no disc geometry), the
  trigger posited (no action).""")

    n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
    OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
    outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
    json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    P(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time() - T0:.0f}s]")
    sys.exit(0 if n_fail == 0 else 1)

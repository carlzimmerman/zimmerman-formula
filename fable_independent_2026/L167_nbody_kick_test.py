#!/usr/bin/env python3
"""
L167 -- THE N-BODY KICK TEST (L163 TEST 1).

Question. A MOND galaxy carries the CMB-required cold component (COSMIC = Omega_c/Omega_b times the baryons,
tracking the baryons initially). Each cold particle later receives an isotropic two-body decay kick v_k. What
fraction of that component's CONTRIBUTION TO g AT THE SPARC RADII is retained at z = 0, as a function of
v_k / v_flat?  The four analytic evacuation criteria of L162/L163 put the 0.582 crossing at v_k/v_flat = 2.81
(step, deep), 1.85 (step, shallow), 1.04 (orbit-averaged), 0.42 (isothermal). L163's stated rule: crossing
above ~2 closes the window; below ~1.5 the window is real.

Method. Spherical galaxy: baryons = exponential sphere M_b(<r) = M_b[1-(1+x)e^-x], M_b = v_flat^4/(G a0),
R_d from a SPARC-like scaling. Gravity from the baryons is MOND with the RAR nu-function and a 1-D external
field g_extN (EFE truncation, finite escape speed). Two kernel readings, as in L61/L162: eps=0 (kernel reads the
baryons only; cold component adds NEWTONIAN gravity) and eps=1 (kernel reads baryons + cold). Cold component:
N particles, self-gravity by spherical enclosed mass, Jeans-isotropic initial velocities, 2 Gyr relaxation, then
kicks: DELTA (all at cosmic t = 4 Gyr, z ~ 1.6) for the clean v_k/v_flat curve, and EXPONENTIAL (t_i ~ Exp(tau),
pre-assembly decays applied at t = 4 Gyr) for the cosmological window cells. Leapfrog, dt = 0.5 Myr, to 13.8 Gyr.
Retained fraction eta(r) = (g_cold,kicked / g_cold,control)(r), time-averaged over the last 1 Gyr, at r = 3 R_d
(~ the SPARC median radius) and 6 R_d. Control = identical run without kicks (removes IC imperfection).

Both a0 footings (canonical 9.36e-11, alt 1.13e-10). No pass condition is a literal True.
Limits stated in the output: spherical baryons; static baryons after t = 2 Gyr; no cosmological infall of
daughters; no redshifting of v_k inside the galaxy; S8/Lyman-alpha side of the window NOT recomputed (L160/L164).
"""
import numpy as np, time, sys, os
from multiprocessing import Pool

T0 = time.time()
G = 4.30091e-6                 # kpc (km/s)^2 / Msun
KM = 1.02271217                # kpc per (km/s * Gyr)  [1 km/s ~ 1 kpc/Gyr]
KPC_M = 3.0856775814913673e19
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
A0K = {k: v * KPC_M / 1e6 for k, v in A0.items()}     # (km/s)^2/kpc
COSMIC = 0.1200 / 0.02237
AGE = 13.8; T_START = 2.0; T_RELAX = 2.0; T_KICK = T_START + T_RELAX
DT = 5e-4; EPS_SOFT = 0.1; EPS_B = 0.05; NPART = 20000
ETA_CEIL = {"canon eps=0": 0.582, "alt eps=0": 0.486, "canon eps=1": 0.355, "alt eps=1": 0.276}
CHECKS = []
def check(n, ok, d=""):
    CHECKS.append((n, bool(ok))); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
def sec(t): print("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118, flush=True)

def nu_RAR(x): return 1.0 / (1.0 - np.exp(-np.sqrt(np.maximum(x, 1e-300))))

class Host:
    def __init__(self, vflat, foot="canonical", gext=0.01, eps=0, profile="tracks"):
        self.vflat, self.foot, self.gext, self.eps, self.profile = vflat, foot, gext, eps, profile
        self.a0 = A0K[foot]
        self.Mb = vflat ** 4 / (G * self.a0)
        self.Rd = 2.0 * (self.Mb / 1e10) ** 0.35
        self.gextN = gext * self.a0
    def Mb_enc(self, r):
        x = r / self.Rd; return self.Mb * (1.0 - (1.0 + x) * np.exp(-x))
    def rho_b(self, r):
        x = r / self.Rd; return self.Mb * x * np.exp(-x) / (4 * np.pi * self.Rd * r ** 2)
    def g_total(self, r, Md_enc):
        gNb = G * self.Mb_enc(r) / (r ** 2 + EPS_B ** 2)
        gNd = G * Md_enc / (r ** 2 + EPS_SOFT ** 2)
        if self.eps == 0:
            return nu_RAR((gNb + self.gextN) / self.a0) * gNb + gNd
        gN = gNb + gNd
        return nu_RAR((gN + self.gextN) / self.a0) * gN
    def g_baryon_only(self, r):
        gNb = G * self.Mb_enc(r) / (r ** 2 + EPS_B ** 2)
        return nu_RAR((gNb + self.gextN) / self.a0) * gNb
    def cold_target_density(self, r):
        if self.profile == "tracks":
            return COSMIC * self.rho_b(r)
        rs = 20.0; x = r / rs
        rho = 1.0 / (x * (1 + x) ** 2) * np.exp(-(r / 300.0) ** 2)
        # normalise: M(<3 R_d) = COSMIC * M_b(<3 R_d)
        rg = np.geomspace(1e-3, 3 * self.Rd, 2000)
        Mn = np.trapz(4 * np.pi * rg ** 2 * (1.0 / ((rg / rs) * (1 + rg / rs) ** 2)), rg)
        return rho * COSMIC * self.Mb_enc(3 * self.Rd) / Mn

def make_ics(h, seed):
    rng = np.random.default_rng(seed)
    rg = np.geomspace(1e-3, 400.0 if h.profile == "tracks" else 400.0, 4000)
    rho = h.cold_target_density(rg)
    dM = 4 * np.pi * rg ** 2 * rho
    Menc = np.concatenate([[0.0], np.cumsum(0.5 * (dM[1:] + dM[:-1]) * np.diff(rg))])
    Mtot = Menc[-1]
    u = rng.uniform(0, 1, NPART) * Mtot
    r = np.interp(u, Menc, rg)
    # Jeans isotropic dispersion in the total (baryon + self) potential
    Mdg = np.interp(rg, rg, Menc)
    gtot = h.g_total(rg, Mdg)
    integrand = rho * gtot
    I = np.concatenate([np.cumsum((0.5 * (integrand[1:] + integrand[:-1]) * np.diff(rg))[::-1])[::-1], [0.0]])
    sig2 = np.maximum(I / np.maximum(rho, 1e-300), 1e-6)
    sig = np.sqrt(np.interp(r, rg, sig2))
    # escape speed from the (finite) potential
    Phi = -np.concatenate([np.cumsum((0.5 * (gtot[1:] + gtot[:-1]) * np.diff(rg))[::-1])[::-1], [0.0]])
    vesc = np.sqrt(np.maximum(-2 * np.interp(r, rg, Phi), 0.0))
    v = rng.normal(0, 1, (NPART, 3)) * sig[:, None]
    vn = np.linalg.norm(v, axis=1); cap = 0.95 * vesc
    bad = vn > cap; v[bad] *= (cap[bad] / vn[bad])[:, None]
    dirs = rng.normal(0, 1, (NPART, 3)); dirs /= np.linalg.norm(dirs, axis=1)[:, None]
    x = dirs * r[:, None]
    mpart = Mtot / NPART
    return x, v, mpart

def accel(h, x, mpart):
    r = np.linalg.norm(x, axis=1)
    order = np.argsort(r)
    Menc = np.empty(NPART); Menc[order] = (np.arange(NPART)) * mpart   # mass strictly interior
    g = h.g_total(np.maximum(r, 1e-4), Menc)
    return -(g / np.maximum(r, 1e-4))[:, None] * x, r, order

def cold_g_at(h, r_eval, r, mpart):
    """g contributed by the cold component at r_eval (reading-dependent)."""
    Md = np.array([(r < re).sum() for re in r_eval]) * mpart
    return h.g_total(np.asarray(r_eval), Md) - h.g_baryon_only(np.asarray(r_eval))

def run(cfg):
    h = Host(cfg["vflat"], cfg["foot"], cfg["gext"], cfg["eps"], cfg["profile"])
    x, v, mpart = make_ics(h, 12345)
    rng = np.random.default_rng(777)
    mode, vk = cfg["mode"], cfg["vk"]
    if mode == "delta":
        tkick = np.full(NPART, T_KICK)
    elif mode == "none":
        tkick = np.full(NPART, np.inf)
    else:                                   # exponential, tau in Gyr, cosmic-time decay
        tkick = np.maximum(rng.exponential(cfg["tau"], NPART), T_KICK)
    r_eval = np.array([3 * h.Rd, 6 * h.Rd])
    a, r, _ = accel(h, x, mpart)
    t = T_START; nsteps = int(round((AGE - T_START) / DT))
    samples = []; m3_at_kick = None; kicked = np.zeros(NPART, bool)
    for i in range(nsteps):
        v += 0.5 * DT * KM * a
        x += DT * KM * v
        a, r, _ = accel(h, x, mpart)
        v += 0.5 * DT * KM * a
        t += DT
        due = (~kicked) & (tkick <= t)
        if due.any():
            d = rng.normal(0, 1, (due.sum(), 3)); d /= np.linalg.norm(d, axis=1)[:, None]
            v[due] += vk * d; kicked[due] = True
        if m3_at_kick is None and t >= T_KICK:
            m3_at_kick = (r < 3 * h.Rd).sum() * mpart
        if t >= AGE - 1.0 and i % 40 == 0:
            samples.append(cold_g_at(h, r_eval, r, mpart))
    gc = np.mean(samples, axis=0)
    m3_end = (r < 3 * h.Rd).sum() * mpart
    return dict(cfg=cfg, gcold=gc.tolist(), m3_kick=float(m3_at_kick), m3_end=float(m3_end),
                Rd=float(h.Rd), Mb=float(h.Mb), unbound=float((r > 50 * h.Rd).mean()))

def energy_test():
    """test particles in the fixed baryon-only MOND potential: leapfrog energy conservation over 2 Gyr."""
    h = Host(110.0); rng = np.random.default_rng(1)
    rg = np.geomspace(1e-3, 400, 4000); gb = h.g_baryon_only(rg)
    Phi = -np.concatenate([np.cumsum((0.5 * (gb[1:] + gb[:-1]) * np.diff(rg))[::-1])[::-1], [0.0]])
    n = 2000; r0 = np.geomspace(0.3, 10 * h.Rd, n)
    dirs = rng.normal(0, 1, (n, 3)); dirs /= np.linalg.norm(dirs, axis=1)[:, None]; x = dirs * r0[:, None]
    vc = np.sqrt(h.g_baryon_only(r0) * r0); tang = np.cross(dirs, rng.normal(0, 1, (n, 3)))
    tang /= np.linalg.norm(tang, axis=1)[:, None]; v = tang * (vc * rng.uniform(0.5, 1.2, n))[:, None]
    def E(x, v): r = np.linalg.norm(x, axis=1); return 0.5 * (v ** 2).sum(1) + np.interp(r, rg, Phi)
    E0 = E(x, v)
    def acc(x): r = np.linalg.norm(x, axis=1); return -(h.g_baryon_only(r) / r)[:, None] * x
    a = acc(x)
    for _ in range(int(2.0 / DT)):
        v += 0.5 * DT * KM * a; x += DT * KM * v; a = acc(x); v += 0.5 * DT * KM * a
    rel = np.abs((E(x, v) - E0) / E0)
    return float(np.median(rel)), float(np.max(rel))

if __name__ == "__main__":
    sec("L167  N-BODY KICK TEST -- retained cold contribution to g at the SPARC radii vs v_k / v_flat")
    print(f"  N = {NPART} cold particles, dt = {DT*1e3:.2f} Myr, t = {T_START}-{AGE} Gyr, relax {T_RELAX} Gyr, kick epoch (delta) "
          f"t = {T_KICK} Gyr; COSMIC = {COSMIC:.3f}; softening {EPS_SOFT} kpc")
    med, mx = energy_test()
    check("C1 integrator: test particles in the baryon-only MOND potential conserve energy over 2 Gyr",
          med < 5e-3 and mx < 5e-2, f"median |dE/E| = {med:.2e}, max = {mx:.2e}")
    HOSTS = [80.0, 110.0, 220.0]
    KR = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0]
    VK_ABS = [200.0, 300.0, 450.0, 600.0, 800.0, 994.0]
    base = dict(foot="canonical", gext=0.01, profile="tracks")
    cfgs = []
    def add(**kw):
        c = dict(base); c.update(kw); cfgs.append(c)
    for vf in HOSTS:
        for eps in (0, 1):
            add(vflat=vf, eps=eps, mode="none", vk=0.0)
            for k in KR: add(vflat=vf, eps=eps, mode="delta", vk=k * vf)
            for tau in (5.0, 20.0):
                for vk in VK_ABS: add(vflat=vf, eps=eps, mode="exp", tau=tau, vk=vk)
    # sensitivities on the median host, eps=0, delta
    for extra in (dict(foot="alt"), dict(gext=0.03), dict(profile="nfw")):
        add(vflat=110.0, eps=0, mode="none", vk=0.0, **extra)
        for k in KR: add(vflat=110.0, eps=0, mode="delta", vk=k * 110.0, **extra)
    print(f"  launching {len(cfgs)} runs on {os.cpu_count()} cores ...", flush=True)
    with Pool(max(1, os.cpu_count() - 2)) as pool:
        res = pool.map(run, cfgs)
    print(f"  done in {time.time()-T0:.0f}s", flush=True)

    def key(c): return (c["vflat"], c["eps"], c["foot"], c["gext"], c["profile"])
    ctrl = {key(r["cfg"]): r for r in res if r["cfg"]["mode"] == "none"}
    def eta(r):
        c = ctrl[key(r["cfg"])]
        return np.array(r["gcold"]) / np.array(c["gcold"])

    sec("CONTROL RUNS (no kick): equilibrium of the cold component")
    drift_ok = True
    for k, c in ctrl.items():
        d = c["m3_end"] / c["m3_kick"]
        drift_ok &= 0.7 < d < 1.3
        print(f"    v_flat {k[0]:5.0f} eps={k[1]} {k[2]:<9} gext={k[3]:.2f} {k[4]:<6}: M_cold(<3R_d) end/kick = {d:.3f}, "
              f"R_d = {c['Rd']:.2f} kpc, M_b = {c['Mb']:.2e}")
    check("C2 controls: cold mass inside 3 R_d drifts by < 30% between the kick epoch and z = 0 (relaxed ICs)", drift_ok)

    sec("DELTA KICK at t = 4 Gyr: eta(3 R_d), eta(6 R_d) vs v_k / v_flat   [canonical a0, g_extN = 0.01 a0, tracks-baryons]")
    cross = {}; mono_ok = True
    for vf in HOSTS:
        for eps in (0, 1):
            rows = sorted([r for r in res if r["cfg"]["mode"] == "delta" and key(r["cfg"]) == (vf, eps, "canonical", 0.01, "tracks")],
                          key=lambda r: r["cfg"]["vk"])
            ks = np.array([r["cfg"]["vk"] / vf for r in rows]); e3 = np.array([eta(r)[0] for r in rows]); e6 = np.array([eta(r)[1] for r in rows])
            mono_ok &= bool(np.all(np.diff(e3) < 0.02))
            ceil = ETA_CEIL["canon eps=%d" % eps]
            xc = np.interp(-ceil, -e3, ks) if e3.min() < ceil < e3.max() else np.nan
            cross[(vf, eps)] = xc
            print(f"    v_flat {vf:4.0f} km/s, eps={eps}: " + "  ".join(f"{k:.2f}:{a:.3f}/{b:.3f}" for k, a, b in zip(ks, e3, e6))
                  + f"\n        -> eta(3R_d) = {ceil} at v_k/v_flat = {xc:.2f}  (v_k = {xc*vf:.0f} km/s)")
    check("C3 eta(3 R_d) decreases monotonically with v_k in every delta-kick series (2% noise tolerance)", mono_ok)
    found = all(np.isfinite(v) for v in cross.values())
    check("C4 the ceiling crossing is bracketed by the scanned v_k/v_flat grid for every host and reading", found,
          ", ".join(f"({vf:.0f},eps{e})={c:.2f}" for (vf, e), c in cross.items()))
    xs0 = [cross[(vf, 0)] for vf in HOSTS]
    vabs = [cross[(vf, 0)] * vf for vf in HOSTS]
    check("C5 mass dependence: the absolute kick needed to reach the ceiling rises with v_flat (80 < 110 < 220 km/s hosts)",
          np.all(np.diff(vabs) > 0), "v_k needed = " + ", ".join(f"{v:.0f}" for v in vabs) + " km/s")
    env_ok = all(0.42 <= x <= 2.81 for x in xs0)
    check("C6 the N-body crossing lies inside the analytic envelope [0.42 (isothermal), 2.81 (step, deep)]", env_ok,
          "eps=0 crossings " + ", ".join(f"{x:.2f}" for x in xs0))

    sec("SENSITIVITIES on the median host (110 km/s, eps=0, delta kick)")
    sens = {}
    for extra, lab in ((("alt", 0.01, "tracks"), "alt a0 footing"), (("canonical", 0.03, "tracks"), "g_extN = 0.03 a0"),
                       (("canonical", 0.01, "nfw"), "NFW-shaped initial cold profile")):
        rows = sorted([r for r in res if r["cfg"]["mode"] == "delta" and key(r["cfg"]) == (110.0,) + (0,) + extra], key=lambda r: r["cfg"]["vk"])
        ks = np.array([r["cfg"]["vk"] / 110.0 for r in rows]); e3 = np.array([eta(r)[0] for r in rows])
        ceil = ETA_CEIL["alt eps=0"] if extra[0] == "alt" else ETA_CEIL["canon eps=0"]
        xc = np.interp(-ceil, -e3, ks) if e3.min() < ceil < e3.max() else np.nan
        sens[lab] = xc
        print(f"    {lab:<34}: " + "  ".join(f"{k:.2f}:{a:.3f}" for k, a in zip(ks, e3)) + f"   -> crossing {xc:.2f} (ceiling {ceil})")
    spread = np.nanmax(list(sens.values()) + [cross[(110.0, 0)]]) / np.nanmin(list(sens.values()) + [cross[(110.0, 0)]])
    check("C7 the crossing is robust: footing / external field / initial profile move it by less than a factor 1.6",
          np.isfinite(spread) and spread < 1.6, f"max/min crossing = {spread:.2f}")

    sec("EXPONENTIAL DECAY (cosmological cells of the L163 window): N-body f_gal = eta(3 R_d) vs L163's analytic criteria")
    print("    L163 live window: tau 5-20 Gyr, v_k 203-994 km/s, galaxy gate needs eta <= 0.582 (canon eps=0) / 0.355 (canon eps=1)")
    any_pass = {0: [], 1: []}
    for tau in (5.0, 20.0):
        for vf in HOSTS:
            for eps in (0, 1):
                rows = sorted([r for r in res if r["cfg"]["mode"] == "exp" and r["cfg"]["tau"] == tau and key(r["cfg"]) == (vf, eps, "canonical", 0.01, "tracks")],
                              key=lambda r: r["cfg"]["vk"])
                e3 = np.array([eta(r)[0] for r in rows]); vk = np.array([r["cfg"]["vk"] for r in rows])
                ceil = ETA_CEIL["canon eps=%d" % eps]
                ok = vk[e3 <= ceil]
                any_pass[eps].append((tau, vf, ok.min() if ok.size else np.nan))
                print(f"    tau {tau:4.0f} Gyr, v_flat {vf:4.0f}, eps={eps}: " + "  ".join(f"{k:.0f}:{a:.3f}" for k, a in zip(vk, e3))
                      + f"   -> gate passes for v_k >= {ok.min():.0f} km/s" if ok.size else
                      f"    tau {tau:4.0f} Gyr, v_flat {vf:4.0f}, eps={eps}: " + "  ".join(f"{k:.0f}:{a:.3f}" for k, a in zip(vk, e3)) + "   -> gate FAILS at every v_k <= 994")
    # the galaxy gate is a population statement: the MEDIAN SPARC host (110) must pass; the 220 host is the massive tail.
    vmin_med = {eps: [v for (tau, vf, v) in any_pass[eps] if vf == 110.0] for eps in (0, 1)}
    print(f"\n    median host: smallest passing v_k (tau 5, tau 20) = eps0 {vmin_med[0]}, eps1 {vmin_med[1]} km/s")
    # L160 triple scan: S_8 (generous bound) survives only for v_k <= ~600 km/s at tau <= 13.8 and <= ~1000 at tau 25-50.
    S8_CEIL_VK = 600.0
    gate_window = {eps: [v for v in vmin_med[eps] if np.isfinite(v) and v <= S8_CEIL_VK] for eps in (0, 1)}
    check("C8 [VERDICT INPUT] for the median host, is there a tau in {5,20} Gyr whose galaxy-gate kick v_k lies below the L160 "
          "S_8 ceiling (~600 km/s at tau <= 13.8 Gyr)?  (a FAIL here means the window is CLOSED by the N-body; a PASS means it stays open)",
          len(gate_window[0]) > 0, f"eps=0 passing kicks under 600 km/s: {gate_window[0]}; eps=1: {gate_window[1]}")

    sec("VERDICT")
    xmed = cross[(110.0, 0)]
    if xmed > 2.0: verdict = "WINDOW CLOSES (crossing above 2: the N-body sides with the step criterion; the galaxy gate needs a kick the S_8/Ly-alpha side forbids)"
    elif xmed < 1.5: verdict = "WINDOW REAL on the galaxy side (crossing below 1.5: orbit-averaged/soft evacuation confirmed) -- S_8/Ly-alpha still to be cleared (L160/L164)"
    else: verdict = "UNDETERMINED (crossing between 1.5 and 2)"
    print(f"    eta(3 R_d) = 0.582 crossing on the median host: v_k/v_flat = {xmed:.2f} ({xmed*110:.0f} km/s); L163 rule -> {verdict}")
    print(f"    all hosts eps=0: {[round(x,2) for x in xs0]};  eps=1: {[round(cross[(vf,1)],2) for vf in HOSTS]}")
    print("    LIMITS: spherical static baryons; cold tracks baryons initially (NFW sensitivity above); no daughter infall; no v_k redshift inside\n"
          "    the galaxy; S_8 / Lyman-alpha side taken from L160/L164, not recomputed. This test DERIVES nothing: it decides whether a\n"
          "    phenomenological decay patch is admissible at all.")
    npass = sum(ok for _, ok in CHECKS)
    print("\n" + "=" * 118 + f"\nL167 COMPLETE: {npass}/{len(CHECKS)} checks PASS.   [{time.time()-T0:.0f}s]\n" + "=" * 118)

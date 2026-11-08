#!/usr/bin/env python3
"""CMB2 / D4 (FROZEN_CRITERIA.md, 3274689858): the a0 law (QUMOND phantom, simple nu) at z ~ 1100 on the B2 footing
background of F1A, a0(z) = x a0, x in {1, 3, 10, 30, 100}, both footings never pooled.

Steps (subagent brief):
 1. rms physical gradient g_ac of the baryons-only linear potential at z 1100 per k band, and g_ac / (x a0).
 2. phantom share (nu - 1) at that gradient; field-level P_ph/P_N on a Gaussian realisation (160^3 box).
 3. time behaviour over one acoustic period per band: phantom vs its source (projected transfer c_X(t)).
 4. peak-ratio sign in a tight-coupling oscillator with G -> (1 + beta_k) G vs dust at R 5.41 (KA-dust incl. G4 numbers).
 5. MUTATE-phase: planted source = dust amplitude, phase-locked to delta_gamma: must read "follows" and fail.
 6. pre-screen per footing per x.
Inputs: F1A parts/fit_B2_{foot}_{cold,MB}.json (best fits) only. No LCDM input, no downloads. CAMB 1.6.6 for the linear
transfer (Weyl potential (Phi+Psi)/2; the symbolic Psi_N compile fails on this Mac: disclosed).
One thread, nice -n 15, RSS < 1 GB.  Usage: d4_law.py [canonical|alt] (one footing per process keeps RSS < 1 GB; the second call merges into d4_law.json)   kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, time, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
import scipy.fft as sfft
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../.."))
F1A = os.path.join(REPO, "closure_2026_11_07/F1A_primary_cmb_audit/parts")
NOTE = "kappa = 1/2 FITTED; not theory closed"
CL = 2.99792458e8; MPC = 3.0856775814913673e22; TCMB = 2.7255
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
XS = [1, 3, 10, 30, 100]
BANDS = [0.01, 0.03, 0.1, 0.3]
OMG = 2.4728e-5; OMR = OMG * (1 + 3.046 * 7 / 8 * (4 / 11) ** (4 / 3))
ZS = 1100.0
N, LBOX = int(os.environ.get("D4_N", "112")), 1078.0 * int(os.environ.get("D4_N", "112")) / 112   # Mpc; kf 0.0058, kNy 0.326
NT = int(os.environ.get("D4_NT", "100")); NSUB = 800; SEED = 20261107
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9   # macOS: bytes (peak, includes reusable freed pages)
def footprint():
    try:
        o = os.popen(f"footprint {os.getpid()} 2>/dev/null").read()
        for l in o.splitlines():
            if "phys_footprint:" in l: return l.split("phys_footprint:")[1].strip()
    except Exception: pass
    return None
def nu(y): return 0.5 + np.sqrt(0.25 + 1.0 / y)
LOG = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)

def pars(foot):
    c = json.load(open(os.path.join(F1A, f"fit_B2_{foot}_cold.json")))["pars"]
    m = json.load(open(os.path.join(F1A, f"fit_B2_{foot}_MB.json")))["pars"]
    return c, m

def camb_bg(h, ob, oc, As, ns):
    import camb
    p = camb.CAMBparams(); p.set_cosmology(H0=100 * h, ombh2=ob, omch2=max(oc, 1e-7), tau=0.07, mnu=0.0,
                                           num_massive_neutrinos=0, nnu=3.046, TCMB=TCMB)
    p.InitPower.set_params(As=As, ns=ns); p.WantCls = False
    return camb.get_background(p)

TRAPZ = getattr(np, "trapezoid", None) or np.trapz
def DR2(k, As, ns): return As * (k / 0.05) ** (ns - 1)

# ------------------------------------------------------------------ step 1: gradient table (analytic, CAMB transfer)
def transfer(r, ks, ts):
    ev = r.get_time_evolution(ks, ts, vars=["Weyl", "delta_photon", "a"])
    return ev[:, :, 0] / ks[:, None] ** 2, ev[:, :, 1], ev[0, :, 2]     # T_W(k,t), T_dg(k,t), a(t)

def grad_table(r, As, ns, a0):
    es = r.conformal_time(ZS)
    kk = np.exp(np.linspace(np.log(1e-4), np.log(1.0), 1500))
    TW, _, a = transfer(r, kk, np.array([es]))
    TW = TW[:, 0]; z1 = 1 / a[0]
    gk = CL ** 2 * z1 / MPC * kk * np.abs(TW) * np.sqrt(DR2(kk, As, ns))        # m/s^2 per unit ln k (rms)
    lnk = np.log(kk); out = {}
    for kc in BANDS:
        w = (kk > kc / 1.2) & (kk < kc * 1.2)
        out[str(kc)] = dict(g_per_lnk=float(np.sqrt(np.mean(gk[w] ** 2))), Weyl_rms_T=float(np.sqrt(np.mean(TW[w] ** 2))))
    def cum(lo, hi):
        w = (kk >= lo) & (kk <= hi); return float(np.sqrt(TRAPZ(gk[w] ** 2, lnk[w])))
    tot = dict(all_1e4_to_1=cum(1e-4, 1.0), box_kf_to_kNy=cum(2 * math.pi / LBOX, math.pi * N / LBOX),
               subhorizon_k_gt_pi_over_eta=cum(math.pi / es, 1.0), below_kf=cum(1e-4, 2 * math.pi / LBOX))
    for key, b in out.items():
        b["ratio_g_band_over_xa0"] = {str(x): b["g_per_lnk"] / (x * a0) for x in XS}
    tot["ratio_all_over_xa0"] = {str(x): tot["all_1e4_to_1"] / (x * a0) for x in XS}
    tot["nu_minus_1_at_g_all"] = {str(x): float(nu(tot["all_1e4_to_1"] / (x * a0)) - 1) for x in XS}
    tot["nu_minus_1_at_g_subhorizon"] = {str(x): float(nu(tot["subhorizon_k_gt_pi_over_eta"] / (x * a0)) - 1) for x in XS}
    for b in out.values():
        b["nu_minus_1_at_g_band"] = {str(x): float(nu(b["g_per_lnk"] / (x * a0)) - 1) for x in XS}
    return dict(eta_star=es, bands=out, totals=tot)

# ------------------------------------------------------------------ steps 2-3: field-level realisation over time
def box_run(foot, rMB, rC, As, ns, a0, ob):
    es = rMB.conformal_time(ZS); esC = rC.conformal_time(ZS)
    Rb = 3 * ob / (4 * OMG) / (1 + ZS); cs = 1 / math.sqrt(3 * (1 + Rb))
    P = {kc: 2 * math.pi / (kc * cs) for kc in BANDS}
    t0 = max(0.3 * es, es - P[0.03]); t1 = es + P[0.03] / 2
    ts = np.unique(np.concatenate([np.linspace(t0, t1, NT), [es]]))
    # transfer table on a fine k grid
    kk = np.unique(np.concatenate([np.exp(np.linspace(np.log(1e-4), np.log(0.01), 120)), np.arange(0.0102, 0.62, 0.0008)]))
    TW, TG, aa = transfer(rMB, kk, ts)
    kf = 2 * math.pi / LBOX
    kx = sfft.fftfreq(N, d=LBOX / N) * 2 * math.pi; kz = sfft.rfftfreq(N, d=LBOX / N) * 2 * math.pi
    KX, KY, KZ = np.meshgrid(kx, kx, kz, indexing="ij"); K = np.sqrt(KX ** 2 + KY ** 2 + KZ ** 2); K[0, 0, 0] = 1.0
    rng = np.random.default_rng(SEED)
    W = sfft.rfftn(rng.standard_normal((N, N, N)), workers=1)
    Rk = W * np.sqrt(2 * math.pi ** 2 * DR2(K, As, ns) / K ** 3 * N ** 3 / LBOX ** 3); Rk[0, 0, 0] = 0; del W
    HP = (K >= math.pi / es)
    # super-box uniform field (variant b): fixed random direction
    kl = kk[kk < kf]; ext_dir = rng.standard_normal(3); ext_dir /= np.linalg.norm(ext_dir)
    # shell subsamples
    shells = {}
    for kc in BANDS:
        idx = np.flatnonzero(((K > kc / 1.1) & (K < kc * 1.1)).ravel()); ntot = int(idx.size)
        if idx.size > 30000: idx = np.sort(rng.choice(idx, size=30000, replace=False))   # cap: projections on 30000 random shell modes
        sel = rng.choice(idx, size=min(NSUB, idx.size), replace=False) if idx.size > NSUB else idx
        shells[kc] = dict(all=idx, sub=sel, n=ntot, n_used=int(idx.size))
    VAR = ["a_box", "b_box_plus_superbox", "c_subhorizon_only"]
    store = {kc: dict(cN=[], cG=[], cph={v: {x: [] for x in XS} for v in VAR}, Pph={v: {x: [] for x in XS} for v in VAR},
                      PN=[], resf={v: {x: [] for x in XS} for v in VAR}, sub_res={v: {x: [] for x in XS} for v in VAR}) for kc in BANDS}
    snap = {}
    Kf = K.ravel(); Rf = Rk.ravel(); R2 = {kc: float(np.sum(np.abs(Rf[shells[kc]["all"]]) ** 2)) for kc in BANDS}
    lk = np.log(K)
    for it, t in enumerate(ts):
        a = aa[it]; conv = CL ** 2 / a / MPC          # dimensionless comoving grad (per Mpc) -> m/s^2
        Tw = np.interp(lk, np.log(kk), TW[:, it]); Psik = Tw * Rk; del Tw
        Tg_band = {kc: float(np.interp(kc, kk, TG[:, it])) for kc in BANDS}
        grads = [sfft.irfftn(1j * Kc * Psik, s=(N, N, N), workers=1).astype(np.float32) for Kc in (KX, KY, KZ)]
        gmag_a = (conv * np.sqrt(grads[0] ** 2 + grads[1] ** 2 + grads[2] ** 2)).astype(np.float32)
        sig_ext = math.sqrt(TRAPZ((kl * TW[kk < kf, it]) ** 2 * DR2(kl, As, ns), np.log(kl)))
        gext = sig_ext * ext_dir           # dimensionless comoving grad of the super-box modes, one realisation of |g|=sigma
        gmag_b = (conv * np.sqrt((grads[0] + gext[0]) ** 2 + (grads[1] + gext[1]) ** 2 + (grads[2] + gext[2]) ** 2)).astype(np.float32)
        PsiH = Psik * HP
        gh = [sfft.irfftn(1j * Kc * PsiH, s=(N, N, N), workers=1).astype(np.float32) for Kc in (KX, KY, KZ)]; del PsiH
        gmag_c = (conv * np.sqrt(gh[0] ** 2 + gh[1] ** 2 + gh[2] ** 2)).astype(np.float32)
        PsiNf = Psik.ravel(); psiNb = {}
        for kc in BANDS:
            psiNb[kc] = PsiNf[shells[kc]["all"]]
            s = shells[kc]; store[kc]["cN"].append(float(np.real(np.sum(PsiNf[s["all"]] * np.conj(Rf[s["all"]]))) / R2[kc]))
            store[kc]["cG"].append(Tg_band[kc]); store[kc]["PN"].append(float(np.mean(np.abs(PsiNf[s["all"]]) ** 2)))
        if abs(t - es) < 1e-9:
            snap["g_rms_box_a"] = float(np.sqrt(np.mean(gmag_a ** 2))); snap["g_rms_b"] = float(np.sqrt(np.mean(gmag_b ** 2)))
            snap["g_rms_c"] = float(np.sqrt(np.mean(gmag_c ** 2))); snap["g_median_a"] = float(np.median(gmag_a))
            snap["g_median_c"] = float(np.median(gmag_c)); snap["g_ext_sigma"] = float(conv * sig_ext)
        for v, gm, gv, off in (("a_box", gmag_a, grads, (0, 0, 0)), ("b_box_plus_superbox", gmag_b, grads, gext), ("c_subhorizon_only", gmag_c, gh, (0, 0, 0))):
            for x in XS:
                f = (nu(np.maximum(gm, 1e-30) / (x * a0)) - 1.0).astype(np.float32)
                div = 1j * KX * sfft.rfftn(f * (gv[0] + np.float32(off[0])), workers=1)
                div += 1j * KY * sfft.rfftn(f * (gv[1] + np.float32(off[1])), workers=1)
                div += 1j * KZ * sfft.rfftn(f * (gv[2] + np.float32(off[2])), workers=1)
                Pph = (-div / K ** 2).ravel(); Pph[0] = 0          # nabla^2 Psi_ph = div[(nu-1) nabla Psi]: -k^2 Psi_ph = i k.G
                for kc in BANDS:
                    s = shells[kc]; ph = Pph[s["all"]]; R_ = Rf[s["all"]]
                    c = float(np.real(np.sum(ph * np.conj(R_))) / R2[kc])
                    # residual = phantom minus its best linear (proportional-to-Psi_N) part, mode by mode
                    psiN = psiNb[kc]; den = np.sum(np.abs(psiN) ** 2)
                    bfit = np.real(np.sum(ph * np.conj(psiN))) / den if den > 0 else 0.0
                    res = ph - bfit * psiN
                    store[kc]["cph"][v][x].append(c); store[kc]["Pph"][v][x].append(float(np.mean(np.abs(ph) ** 2)))
                    store[kc]["resf"][v][x].append(float(np.sqrt(np.mean(np.abs(res) ** 2) / max(np.mean(np.abs(ph) ** 2), 1e-300))))
                    sub = np.searchsorted(s["all"], s["sub"])
                    store[kc]["sub_res"][v][x].append(res[sub].astype(np.complex64))
                del f, div, Pph
        del grads, gh, gmag_a, gmag_b, gmag_c, Psik
        if it % 10 == 0: say(f"  {foot} t {it+1}/{len(ts)} eta {t:.1f} z {1/a-1:.0f} peak rss {rss():.2f} GB, phys_footprint {footprint()}")
    # dust (cold model, same band centres; deterministic transfer) on its own time grid around its eta*
    tsC = np.maximum(esC + (ts - es), 1.0)
    TWC, TGC, aC = transfer(rC, np.array(BANDS), tsC)
    return dict(ts=ts, es=es, esC=esC, tsC=tsC, cs=cs, P=P, store=store, snap=snap, TWC=TWC, TGC=TGC, shells={k: v["n"] for k, v in shells.items()}, shells_used={k: v["n_used"] for k, v in shells.items()},
                Rsub={kc: Rf[shells[kc]["sub"]] for kc in BANDS})

def fit_slow_osc(t, c, om, tc, P):
    """c(t) = s0 + s1 (t - tc)/P + A cos(om t) + B sin(om t): s0 = slow (still) value at tc, amp = oscillating amplitude."""
    X = np.vstack([np.ones_like(t), (t - tc) / P, np.cos(om * t), np.sin(om * t)]).T
    co, *_ = np.linalg.lstsq(X, c, rcond=None)
    return dict(s0=float(co[0]), amp=float(math.hypot(co[2], co[3])), phase=float(math.atan2(-co[3], co[2])))

def pearson(a, b):
    a = np.asarray(a) - np.mean(a); b = np.asarray(b) - np.mean(b); d = math.sqrt(np.sum(a * a) * np.sum(b * b))
    return float(np.sum(a * b) / d) if d > 0 else 0.0

def classify(t, c, src, om, tc, P):
    """regress c = beta src + s (const) over the window: s = the still part not carried by the source."""
    X = np.vstack([src, np.ones_like(t)]).T; co, *_ = np.linalg.lstsq(X, c, rcond=None)
    r = pearson(c, src); so = fit_slow_osc(t, c, om, tc, P); ss = fit_slow_osc(t, src, om, tc, P)
    dph = (so["phase"] - ss["phase"] + math.pi) % (2 * math.pi) - math.pi
    lab = "follows" if abs(r) >= 0.8 else ("still" if abs(so["s0"]) >= so["amp"] else "mixed")
    return dict(r_src=r, beta=float(co[0]), still_after_source=float(co[1]), slow_s0=so["s0"], osc_amp=so["amp"], phase_minus_source_rad=float(dph), label=lab)

def analyse(foot, R):
    ts, es, P, st = R["ts"], R["es"], R["P"], R["store"]; out = {}
    for kc in BANDS:
        om = 2 * math.pi / P[kc]
        windows = {"centred": (es - P[kc] / 2, es + P[kc] / 2), "ending_at_z1100": (es - P[kc], es)}
        o = dict(n_modes=R["shells"][kc], n_modes_used=R["shells_used"][kc], period_Mpc=P[kc], windows={})
        it_s = int(np.argmin(np.abs(ts - es)))
        # field-level share at z 1100
        o["share_at_z1100"] = {v: {str(x): dict(Pph_over_PN=st[kc]["Pph"][v][x][it_s] / st[kc]["PN"][it_s],
                                                 c_ph_over_c_N=st[kc]["cph"][v][x][it_s] / st[kc]["cN"][it_s] if st[kc]["cN"][it_s] != 0 else None,
                                                 nonlinear_residual_frac=st[kc]["resf"][v][x][it_s]) for x in XS} for v in st[kc]["cph"]}
        o["Weyl_N_rms_z1100"] = math.sqrt(st[kc]["PN"][it_s])
        for wn, (lo, hi) in windows.items():
            lo = max(lo, ts[0]); w = (ts >= lo - 1e-9) & (ts <= hi + 1e-9); t = ts[w]
            cN = np.array(st[kc]["cN"])[w]; cG = np.array(st[kc]["cG"])[w]
            # dust Weyl in the cold model over the same window shifted to its eta*
            j = BANDS.index(kc); cD = R["TWC"][j][w]; cDG = R["TGC"][j][w]; tD = R["tsC"][w]
            dust = classify(tD, cD, cDG, om, R["esC"], P[kc]); Dst = abs(dust["still_after_source"]); Dslow = abs(dust["slow_s0"])
            src = dict(N_vs_dgamma=classify(t, cN, cG, om, es, P[kc]))
            rows = {}
            for v in st[kc]["cph"]:
                rows[v] = {}
                for x in XS:
                    cph = np.array(st[kc]["cph"][v][x])[w]
                    cl = classify(t, cph, cN, om, es, P[kc]); cl["r_dgamma"] = pearson(cph, cG)
                    sub = np.array(st[kc]["sub_res"][v][x])[w]                     # (nt, nsub) nonlinear residual modes
                    Rs = R["Rsub"][kc]; norm = math.sqrt(np.mean(np.abs(Rs) ** 2))
                    res_still = float(np.sqrt(np.mean(np.abs(sub.mean(axis=0)) ** 2)) / norm) if sub.size else 0.0
                    cl["nonlinear_residual_still_rms_per_unitR"] = res_still
                    still_total = abs(cl["still_after_source"]) + res_still
                    cl["prescreen_ratio_still_vs_dust"] = still_total / Dst if Dst > 0 else None
                    cl["generous_ratio_slow_s0_vs_dust"] = (abs(cl["slow_s0"]) + res_still) / Dslow if Dslow > 0 else None
                    cl["sign_slow_s0_same_as_dust"] = bool(np.sign(cl["slow_s0"]) == np.sign(dust["slow_s0"]))
                    rows[v][str(x)] = cl
            # MUTATE-phase: planted = dust's still amplitude x delta_gamma / rms(delta_gamma) (baryons-only), phase-locked
            m = Dst * cG / math.sqrt(np.mean(cG ** 2)); mc = classify(t, m, cG, om, es, P[kc])
            mc["prescreen_ratio_still_vs_dust"] = abs(mc["still_after_source"]) / Dst if Dst > 0 else None
            mc["fails_prescreen"] = bool(mc["prescreen_ratio_still_vs_dust"] < 0.5); mc["reads_follows"] = mc["label"] == "follows"
            dust["prescreen_ratio_self"] = 1.0
            o["windows"][wn] = dict(t_range=[float(t[0]), float(t[-1])], n_t=int(w.sum()), dust=dust, source=src, phantom=rows, MUTATE_phase=mc)
        out[str(kc)] = o
    return out

# ------------------------------------------------------------------ step 4: tight-coupling oscillator
def oscillator(h, ob, oc, k, beta=None, mode="tc", zend=ZS):
    """Newtonian gauge, Psi = Phi (no shear). fluids: photons (+baryons tight-coupled), neutrinos (fluid), baryons, dust.
    0i equation: Phi' = -H Phi + nu_eff (3/2) H^2/k^2 sum (rho_i/rho)(1+w_i) theta_i + (nu_eff'/nu_eff) Phi,
    nu_eff = 1 + beta s(k eta), s = u^2/(1+u^2) (subhorizon switch). mode 'g4': radiation one fluid, baryons uncoupled dust."""
    H0 = h / 2997.92458; Og = OMG / h ** 2; Onu = (OMR - OMG) / h ** 2; Ob = ob / h ** 2; Oc = oc / h ** 2; OL = 1 - Og - Onu - Ob - Oc
    def Hc(a): return a * H0 * math.sqrt((Og + Onu) / a ** 4 + (Ob + Oc) / a ** 3 + OL)
    ai = 1e-6; ti = ai / (H0 * math.sqrt(Og + Onu))
    def rhs(lna, y):
        a = math.exp(lna); H = Hc(a); eta = y[9]
        phi, dg, th, db, thb, dn, thn, dc, thc, _ = y
        rho_g, rho_n, rho_b, rho_c = Og / a ** 4, Onu / a ** 4, Ob / a ** 3, Oc / a ** 3; tot = rho_g + rho_n + rho_b + rho_c + OL
        u = k * eta; s = u * u / (1 + u * u); ds = 2 * u / (1 + u * u) ** 2 * k
        b, db = beta(eta) if beta is not None else (0.0, 0.0)
        nue = 1 + b * s; dnue = b * ds + db * s
        if mode == "g4":     # photons + neutrinos one fluid; baryons uncoupled
            src = (4 / 3) * (rho_g + rho_n) * th + rho_b * thb + rho_c * thc
        else:
            src = (4 / 3) * rho_g * th + rho_b * th + (4 / 3) * rho_n * thn + rho_c * thc
        dphi = -H * phi + nue * 1.5 * H ** 2 / k ** 2 * src / tot + dnue / nue * phi
        psi = phi
        if mode == "g4":
            ddg = -(4 / 3) * th + 4 * dphi; dth = k ** 2 * dg / 4 + k ** 2 * psi
            ddb = -thb + 3 * dphi; dthb = -H * thb + k ** 2 * psi
            ddn, dthn = 0.0, 0.0
        else:
            R = 3 * rho_b / (4 * rho_g)
            ddg = -(4 / 3) * th + 4 * dphi; dth = (-R * H * th + k ** 2 * dg / 4) / (1 + R) + k ** 2 * psi
            ddb = -th + 3 * dphi; dthb = 0.0
            ddn = -(4 / 3) * thn + 4 * dphi; dthn = k ** 2 * dn / 4 + k ** 2 * psi
        ddc = -thc + 3 * dphi; dthc = -H * thc + k ** 2 * psi
        return np.array([dphi, ddg, dth, ddb, dthb, ddn, dthn, ddc, dthc, 1.0]) / H
    p0 = 1.0; th0 = 0.5 * k ** 2 * ti * p0
    y0 = [p0, -2 * p0, th0, -1.5 * p0, th0, -2 * p0, th0, -1.5 * p0, th0, ti]
    s = solve_ivp(rhs, (math.log(ai), math.log(1 / (1 + zend))), y0, method="LSODA", rtol=1e-7, atol=1e-10)
    y = s.y[:, -1]
    return dict(phi=y[0], dg=y[1], db=y[3], dc=y[7], Theta_eff=y[1] / 4 + y[0])

def peaks(h, ob, oc, betafun, anchors=None):
    """Theta_eff = delta_gamma/4 + Psi at z 1100 vs k. Free detection (first extrema past k 0.012), or, with anchors
    (the baryons-only extrema), the signed extremum inside +- half a spacing of each anchor (G_eff runs)."""
    ks = np.linspace(0.004, 0.36, 220)
    Te = np.array([oscillator(h, ob, oc, k, beta=betafun(k) if betafun else None)["Theta_eff"] for k in ks])
    if anchors is None:
        d = np.diff(Te); ext = [i + 1 for i in range(len(d) - 1) if np.sign(d[i]) != np.sign(d[i + 1]) and ks[i + 1] > 0.012]
        H = [(float(ks[i]), float(Te[i])) for i in ext[:4]]
    else:
        sp = anchors[1][0] - anchors[0][0]; H = []
        for ka, va in anchors[:4]:
            w = np.flatnonzero(np.abs(ks - ka) <= sp / 2); i = w[np.argmax(np.sign(va) * Te[w])]; H.append((float(ks[i]), float(Te[i])))
    r = dict(extrema=H, finite=bool(np.all(np.isfinite(Te))))
    if len(H) >= 3:
        r["H1_over_H2"] = abs(H[0][1]) / abs(H[1][1]); r["H3_over_H2"] = abs(H[2][1]) / abs(H[1][1])
    return r

def main(foots):
    t0 = time.time(); J = os.path.join(HERE, "d4_law.json")
    RES = json.load(open(J)) if (os.path.exists(J) and len(foots) == 1) else dict(note=NOTE, criteria="FROZEN_CRITERIA.md (3274689858)", footings={})
    RES.setdefault("runs", []); LOG.extend(RES.pop("log", []))
    for foot in foots:
        a0 = FOOT[foot]
        c, m = pars(foot); As = math.exp(c["lnA"]) * 1e-10; ns = c["ns"]
        say(f"== {foot}: a0 {a0}; MB background h {m['h']:.4f} ob {m['ob']:.5f}; cold h {c['h']:.4f} ob {c['ob']:.5f} oc {c['oc']:.5f}; As {As:.4e} ns {ns:.4f}")
        rMB = camb_bg(m["h"], m["ob"], 0.0, As, ns); rC = camb_bg(c["h"], c["ob"], c["oc"], As, ns)
        F = dict(background=dict(MB=m, cold=c, As=As, ns=ns))
        F["step1_gradients"] = grad_table(rMB, As, ns, a0)
        # MB-fit amplitude variant (lnA, n_s at the MB best fit, n_s at bracket edge 1.3)
        F["step1_gradients_MBfit_amplitude"] = grad_table(rMB, math.exp(m["lnA"]) * 1e-10, m["ns"], a0)["totals"]
        say(json.dumps(F["step1_gradients"]["totals"], default=float))
        R = box_run(foot, rMB, rC, As, ns, a0, m["ob"])
        F["box"] = dict(N=N, L_Mpc=LBOX, kf=2 * math.pi / LBOX, kNy=math.pi * N / LBOX, seed=SEED, snapshot_z1100=R["snap"], eta_star_MB=R["es"],
                        eta_star_cold=R["esC"], cs_star=R["cs"], n_times=len(R["ts"]))
        F["steps2_3_5"] = analyse(foot, R)
        # step 4: oscillator. beta_k = regression slope of phantom on Psi_N (variant a, centred window), interpolated in log k
        osc = {}
        osc["KA_g4_mode_cold"] = {str(k): oscillator(c["h"], c["ob"], c["oc"], k, mode="g4")["db"] for k in (0.05, 0.3)}
        osc["baryons_only"] = peaks(m["h"], m["ob"], 0.0, None)
        osc["dust_R541"] = peaks(c["h"], c["ob"], c["oc"], None)
        # time history of the box-range rms gradient (variant a range kf..kNy), z 1e5 -> 1100, analytic from the transfer
        kk = np.exp(np.linspace(np.log(2 * math.pi / LBOX), np.log(math.pi * N / LBOX), 500))
        eh = np.exp(np.linspace(np.log(rMB.conformal_time(1e5)), np.log(R["es"]), 40))
        TWh, _, ah = transfer(rMB, kk, eh)
        gh = np.array([CL ** 2 / ah[j] / MPC * math.sqrt(TRAPZ((kk * TWh[:, j]) ** 2 * DR2(kk, As, ns), np.log(kk))) for j in range(len(eh))])
        gh *= R["snap"]["g_rms_box_a"] / gh[-1]          # tie to the realised box rms at z 1100
        osc["g_history"] = dict(eta=eh.tolist(), z=(1 / ah - 1).tolist(), g_rms=gh.tolist())
        for x in XS:
            bk = np.array([F["steps2_3_5"][str(kc)]["windows"]["centred"]["phantom"]["a_box"][str(x)]["beta"] for kc in BANDS])
            nm1 = float(nu(gh[-1] / (x * a0)) - 1); kap = bk / nm1      # beta_k = kappa_k (nu(g(eta)) - 1)
            # k 0.01 band (4 modes, near horizon) is not used: beta is clamped to the k 0.03 value below k 0.03
            kap = kap[1:]; lb = np.log(BANDS[1:]); le = np.log(eh); nh = nu(gh / (x * a0)) - 1
            def bfun(k, kap=kap, nh=nh, le=le, lb=lb):
                kp = float(np.interp(math.log(k), lb, kap))
                def f(eta):
                    l = min(max(math.log(eta), le[0]), le[-1]); v = np.interp(l, le, nh)
                    dv = (np.interp(min(l + 1e-3, le[-1]), le, nh) - np.interp(max(l - 1e-3, le[0]), le, nh)) / 2e-3 / eta
                    return kp * v, kp * dv
                return f
            osc[f"G_eff_x{x}"] = dict(beta_bands_z1100=bk.tolist(), nu_minus_1_box_rms_z1100=nm1, kappa_bands=kap.tolist(), **peaks(m["h"], m["ob"], 0.0, bfun, anchors=osc["baryons_only"]["extrema"]))
            say(f"  osc x {x}: {json.dumps(osc[f'G_eff_x{x}'], default=float)}")
        say("  osc baryons-only", json.dumps(osc["baryons_only"], default=float)); say("  osc dust", json.dumps(osc["dust_R541"], default=float))
        F["step4_oscillator"] = osc
        RES["footings"][foot] = F
        json.dump(RES, open(os.path.join(HERE, "d4_law.json"), "w"), indent=1, default=float)
    RES["runs"].append(dict(foots=foots, runtime_s=time.time() - t0, peak_rss_GB=rss(), phys_footprint_end=footprint(), N=N, L=LBOX, NT=NT)); RES["log"] = LOG
    json.dump(RES, open(os.path.join(HERE, "d4_law.json"), "w"), indent=1, default=float)
    say(f"done {foots} {time.time() - t0:.0f} s peak RSS {rss():.2f} GB phys_footprint {footprint()}")
    summary(RES)

def summary(RES):
    L = ["CMB2 / D4: the a0 law's phantom at z 1100 on B2 (baryons-only source), " + NOTE, ""]
    verdict = {}
    for foot, F in RES["footings"].items():
        a0 = FOOT[foot]; g = F["step1_gradients"]; sn = F["box"]["snapshot_z1100"]
        L.append(f"== {foot} (a0 {a0}); eta* MB {F['box']['eta_star_MB']:.1f} Mpc, cold {F['box']['eta_star_cold']:.1f}")
        L.append(f"step 1: g_rms all k {g['totals']['all_1e4_to_1']:.3e} m/s2; box rms {sn['g_rms_box_a']:.3e}; subhorizon-only rms {sn['g_rms_c']:.3e}; super-box sigma {sn['g_ext_sigma']:.3e}")
        L.append("  band g per ln k [m/s2] and g/(x a0) for x = " + str(XS))
        for kc, b in g["bands"].items():
            L.append(f"  k {kc}: g {b['g_per_lnk']:.3e}  ratios " + " ".join(f"{b['ratio_g_band_over_xa0'][str(x)]:.3g}" for x in XS)
                     + "  nu-1 " + " ".join(f"{b['nu_minus_1_at_g_band'][str(x)]:.3g}" for x in XS))
        L.append("  all-k ratio " + " ".join(f"{g['totals']['ratio_all_over_xa0'][str(x)]:.3g}" for x in XS) + "  nu-1 at all-k rms " + " ".join(f"{g['totals']['nu_minus_1_at_g_all'][str(x)]:.3g}" for x in XS))
        S = F["steps2_3_5"]; passes = []
        for kc in BANDS:
            o = S[str(kc)]; w = o["windows"]["centred"]
            L.append(f"step 2-3 k {kc} (n {o['n_modes']} modes, period {o['period_Mpc']:.0f} Mpc): dust still {w['dust']['still_after_source']:.4g} ({w['dust']['label']}); Psi_N vs dgamma r {w['source']['N_vs_dgamma']['r_src']:.3f}")
            for v in o["share_at_z1100"]:
                L.append(f"   {v}: Pph/PN " + " ".join(f"{o['share_at_z1100'][v][str(x)]['Pph_over_PN']:.3g}" for x in XS)
                         + " | beta " + " ".join(f"{w['phantom'][v][str(x)]['beta']:.3g}" for x in XS)
                         + " | r(ph,Psi_N) " + " ".join(f"{w['phantom'][v][str(x)]['r_src']:.3f}" for x in XS)
                         + " | label " + ",".join(w['phantom'][v][str(x)]['label'] for x in XS)
                         + " | prescreen still/dust " + " ".join(f"{w['phantom'][v][str(x)]['prescreen_ratio_still_vs_dust']:.3g}" for x in XS))
                for wn in o["windows"]:
                    for x in XS:
                        pr = o["windows"][wn]["phantom"][v][str(x)]
                        if kc in (0.03, 0.1, 0.3) and (pr["prescreen_ratio_still_vs_dust"] >= 0.5): passes.append((kc, v, wn, x, pr["prescreen_ratio_still_vs_dust"]))
            m = w["MUTATE_phase"]; L.append(f"   MUTATE-phase: label {m['label']}, still/dust {m['prescreen_ratio_still_vs_dust']:.2e}, fails {m['fails_prescreen']}")
        osc = F["step4_oscillator"]
        L.append(f"step 4 KA-g4 baryon contrast (cold, uncoupled-baryon G4 mode): k 0.05 {osc['KA_g4_mode_cold']['0.05']:.3f}, k 0.3 {osc['KA_g4_mode_cold']['0.3']:.3f} (F1A -26.8 / -108.1)")
        for key in ["baryons_only", "dust_R541"] + [f"G_eff_x{x}" for x in XS]:
            o = osc[key]; L.append(f"   {key}: H1/H2 {o.get('H1_over_H2', float('nan')):.3f}  H3/H2 {o.get('H3_over_H2', float('nan')):.3f}  finite {o.get('finite')}  extrema " + " ".join(f"{k_:.4f}:{v_:+.3f}" for k_, v_ in o["extrema"]))
        verdict[foot] = dict(passes=passes)
        L.append(f"PRE-SCREEN {foot}: " + ("PASS at " + str(passes) if passes else "FAIL at every x, k 0.03-0.3, all variants and windows"))
        L.append("")
    RES["prescreen"] = verdict
    open(os.path.join(HERE, "d4_law.out"), "w").write("\n".join(L + ["", "log:"] + RES.get("log", [])) + "\n")
    json.dump(RES, open(os.path.join(HERE, "d4_law.json"), "w"), indent=1, default=float)

if __name__ == "__main__":
    main(sys.argv[1:] or list(FOOT))

#!/usr/bin/env python3
"""CFG725: the condensate carrier's self-interaction window (sigma/m) against the record's merger and core data.
Criteria: FROZEN_CRITERIA.md (4f9022839), committed alone first.
Run:  nice -n 10 python3 cfg725.py              -> cfg725.out, cfg725_results.json (exit 0 iff controls K1-K4 pass)
      CFG725_MUTATE=1 nice -n 10 python3 cfg725.py -> cfg725_MUTATE.out, cfg725_results_MUTATE.json (exit 0 iff M1-M3 bite)
One process, < 1 GB, no downloads. kappa = 1/2 FITTED; footings never pooled; cold energy's mass required; not theory closed.
Literature numbers PROVISIONAL (Bullet lensing masses, Harvey beta, LITTLE THINGS mass-model subtraction)."""
import copy, hashlib, json, math, os, sys
import numpy as np
if not hasattr(np, "trapezoid"):
    np.trapezoid = np.trapz   # older numpy

MUT = os.environ.get("CFG725_MUTATE") == "1"
SUF = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
C623 = os.path.join(HERE, "..", "CFG623_merger_stopwatch_v5")
C723 = os.path.join(HERE, "..", "CFG723_carrier_mass_origin")
LT = os.path.join(HERE, "..", "..", "..", "_external_data", "little_things_oh2015")
sys.path.insert(0, C623)
import cfg623_main as M623  # noqa: E402  (read-only: estimator, window, stability, epoch)

OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

# ---------------------------------------------------------------- units: kpc, Gyr, Msun
G = 4.49850215e-6                 # kpc^3 Gyr^-2 Msun^-1 (CFG597 lib value)
KMS = 1.0227121650537077          # km/s -> kpc/Gyr
MSUN, KPC, PC = 1.98892e30, 3.0857e19, 3.0857e16
G_PC = 4.30091e-3                 # pc (km/s)^2 / Msun
CM2G_SI = 1e-4 / 1e-3             # 1 cm^2/g in m^2/kg  (CFG428 correction: 0.1)
CM2G = CM2G_SI * MSUN / KPC**2    # 1 cm^2/g in kpc^2/Msun
A0 = {"can": 9.3603e-11, "alt": 1.1312e-10}
SIGCAP = {k: a0 * PC / (math.pi * G_PC) / 1e6 for k, a0 in A0.items()}               # Msun/pc^2 (a0 in m/s^2 -> (km/s)^2/pc)
R_AP = 250.0                      # kpc
M_LENS = {"main": 2.5e14, "sub": 2.0e14}      # I1, PROVISIONAL
M_BAR = {"main": 4.85e13, "sub": 1.50e13}     # I1, CFG625 static
ERR_SIG = 0.15
RT = {"main": 1200.0, "sub": 990.944}
RC_SET, RC_PRI = (50.0, 100.0, 150.0), 100.0
F_OBS, SIG_F, HARV_B, HARV_S = 0.045, 0.125, -0.04, 0.07
GRID = np.concatenate([[0.0], np.logspace(-2, 2, 81)])
RUNS = {"can": "a0_can_v2666.7_eta1.132", "alt": "a0_alt_v2666.7_eta1.132"}
SEEDS = (603, 604, 605)
A_SET, T_SET, SV_SET, RE_SET = (1.0, 4.0), (5.0, 10.0), (1000.0, 1300.0), (50.0, 100.0, 200.0)

R = {"criteria": "4f9022839", "mutate": MUT}
checks = {}

# ================================================================= profiles
def piso(rc, rt, n=6000):
    r = np.concatenate([[0.0], np.logspace(-3, math.log10(rt), n)])
    rho = 1.0 / (1.0 + (r / rc) ** 2)
    m = np.concatenate([[0.0], np.cumsum(0.5 * (4 * np.pi * r[1:]**2 * rho[1:] + 4 * np.pi * r[:-1]**2 * rho[:-1]) * np.diff(r))])
    return r, rho, m

def mproj(r, rho, m, Rp):
    """projected mass inside Rp of a spherical profile truncated at r[-1]."""
    m3 = np.interp(Rp, r, m)
    s = r > Rp
    rr, dd = r[s], rho[s]
    integ = 4 * np.pi * rr**2 * dd * (1 - np.sqrt(1 - (Rp / rr) ** 2))
    return m3 + np.trapezoid(integ, rr)

def norm_piso(Mp, rc, rt):
    r, rho, m = piso(rc, rt)
    k = Mp / mproj(r, rho, m, R_AP)
    return r, rho * k, m * k

def phi0(r, rho):
    return -4 * np.pi * G * np.trapezoid(rho * r, r)

# ================================================================= K4 unit
checks["K4"] = abs(CM2G_SI - 0.1) < 1e-15
P(f"K4 unit: 1 cm^2/g = {CM2G_SI} m^2/kg = {CM2G:.4e} kpc^2/Msun -> {'PASS' if checks['K4'] else 'FAIL'}")
P(f"capacity a0/(pi G): can {SIGCAP['can']:.1f} / alt {SIGCAP['alt']:.1f} Msun/pc^2")

# ================================================================= K3: isotropic scattering kinematics
P("\n=== (a) kinematics: isotropic equal-mass scattering, retained momentum")
rng = np.random.default_rng(725)
k3 = {}
for x in (0.3, 0.6, 0.9):
    mu = rng.uniform(-1, 1, 1_000_000)               # cos(theta) of n_hat, isotropic in the CM frame
    dvz = 0.5 * (mu - 1.0)                            # (n - z)/2 . z, units of V
    dv = 0.5 * np.sqrt(2 - 2 * mu)
    ret = dv < x
    mc = float(np.sum(dvz[ret]) / mu.size)            # mean retained dv_z per scattering
    k3[x] = dict(mc=mc, analytic=-x**4 / 2, rel=abs(mc / (-x**4 / 2) - 1))
    P(f"  x = v_esc/V = {x}: MC retained <dv_z>/V = {mc:+.5f}, analytic -x^4/2 = {-x**4/2:+.5f} (rel {k3[x]['rel']:.2e})")
checks["K3"] = all(v["rel"] <= 0.01 for v in k3.values())
P(f"K3 -> {'PASS' if checks['K3'] else 'FAIL'}")

# ================================================================= K1: oscillator
def osc(t, a, w):
    """integrate d'' = a(t) - w^2 d, d(0)=d'(0)=0 on grid t (piecewise-linear a), RK4 with substeps."""
    d = np.zeros_like(t); v = 0.0; x = 0.0
    for i in range(1, t.size):
        h = t[i] - t[i - 1]; a0_, a1_ = a[i - 1], a[i]
        f = lambda s, x_, v_: (v_, a0_ + (a1_ - a0_) * s / h - w * w * x_)
        k1 = f(0, x, v); k2 = f(h / 2, x + h / 2 * k1[0], v + h / 2 * k1[1])
        k3_ = f(h / 2, x + h / 2 * k2[0], v + h / 2 * k2[1]); k4 = f(h, x + h * k3_[0], v + h * k3_[1])
        x += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3_[0] + k4[0]); v += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3_[1] + k4[1])
        d[i] = x
    return d
tt = np.linspace(0, 1.5, 15001); w_ = 20.0; aa = np.full_like(tt, 3.0)
dd = osc(tt, aa, w_); an = 3.0 / w_**2 * (1 - np.cos(w_ * tt))
k1err = float(np.max(np.abs(dd - an)) / np.max(np.abs(an)))
checks["K1"] = k1err <= 1e-6
P(f"K1 oscillator vs analytic constant drag: max rel err {k1err:.2e} -> {'PASS' if checks['K1'] else 'FAIL'}")

# ================================================================= (a) merger layer
P("\n=== (a) merger offset vs sigma/m (CFG623 alpha = 0 runs + isotropic-scattering drag layer)")
def fine_history(run):
    diag = run["diag"]
    t = np.array([d["t"] for d in diag])
    sg = np.array([d["sub"]["gal"] for d in diag]); mc = np.array([d["main"]["cold"] for d in diag])
    vs = np.array([d["sub"]["vgal"][:2] for d in diag]); vm = np.array([d["main"]["vgal"][:2] for d in diag])
    sep = np.hypot(*(sg - mc).T)
    vrel = vs - vm; V = np.hypot(*vrel.T) * KMS                # kpc/Gyr
    uhat = -(vrel / np.hypot(*vrel.T)[:, None])                # trailing direction
    return t, sep, V, uhat

def layer(run, foot, rc, branch="ALL", eta_mode="iso", sign=1.0):
    """returns per-epoch displacement vectors (kpc) for sigma/m = 1 cm^2/g, and the setup numbers."""
    t, sep, V, uhat = fine_history(run)
    Md = M_LENS["main"] - M_BAR["main"]
    rm, rhom, _ = norm_piso(Md, rc, RT["main"])
    rs, rhos, _ = norm_piso(M_LENS["sub"], rc, RT["sub"])
    w2 = 4 * np.pi / 3 * G * rhos[0]; om = math.sqrt(w2)
    vesc = math.sqrt(2 * abs(phi0(rs, rhos)))
    wgt = (M_LENS["sub"] - M_BAR["sub"]) / M_LENS["sub"]
    sig_dark = {k: (M_LENS[k] - M_BAR[k]) / (math.pi * (R_AP * 1e3) ** 2) for k in M_LENS}
    ffree = {k: max(0.0, 1 - SIGCAP[foot] / sig_dark[k]) for k in M_LENS}
    tgt = 1.0
    if branch == "FREE":
        wgt *= ffree["sub"]; tgt = ffree["main"]
    tf = np.linspace(t[0], t[-1], int((t[-1] - t[0]) / 2e-4) + 1)
    sepf = np.interp(tf, t, sep); Vf = np.interp(tf, t, V)
    x = np.minimum(vesc / Vf, 1.0)
    eta = x**4 / 2 if eta_mode == "iso" else np.full_like(x, 0.5)
    rho_t = np.interp(sepf, rm, rhom, right=0.0) * tgt
    a = sign * eta * CM2G * rho_t * Vf**2
    d = osc(tf, a, om)
    de = np.interp(t, tf, d)
    disp = (wgt * de)[:, None] * uhat
    info = dict(rc=rc, omega_per_Gyr=om, T_osc_Gyr=2 * math.pi / om, vesc_kms=vesc / KMS, w=wgt, f_free=ffree,
                Sigma_tgt_center_Msun_pc2=None, V_peri_kms=float(np.max(V) / KMS), eta_at_Vmax=float(np.min(x)**4 / 2),
                delta_max_kpc_per_cm2g=float(np.max(np.abs(d))), delta_end=float(d[-1]))
    # central column of the main target (for the impulse estimate)
    zz = np.linspace(-RT["main"], RT["main"], 20001)
    info["Sigma_tgt_center_Msun_pc2"] = float(np.trapezoid(np.interp(np.abs(zz), rm, rhom, right=0.0), zz) / 1e6) * tgt
    return disp, info

def shifted(diag, disp, s):
    out = []
    for d, dv in zip(diag, disp):
        e = copy.deepcopy(d); e["sub"]["lens"] = list(np.array(d["sub"]["lens"]) + s * dv); out.append(e)
    return out

def score(run, disp, s):
    diag0 = run["diag"]; tp = run["t_peri"]
    diag = shifted(diag0, disp, s) if s != 0 else diag0
    ep = M623.S.epoch(diag0, tp)
    i, w = ep["i_obs"], ep["w_obs"]
    b0 = M623.beta_of(diag[i - 1])[0]; b1 = M623.beta_of(diag[i])[0]
    f = b0 + w * (b1 - b0)
    stB = all(M623.stable(diag0[j]) for j in (i - 1, i))
    win_idx = [k for k, d in enumerate(diag0) if 0.1 - 1e-9 <= d["t"] - tp <= 0.6 + 1e-9 and M623.beta_of(d)[1] >= M623.DSG_H]
    good = [k for k in win_idx if M623.stable(diag0[k])]
    scH = len(good) >= 10 and len(good) >= 0.5 * len(win_idx)
    bb = float(np.mean([M623.beta_of(diag[k])[0] for k in good])) if good else float("nan")
    ZB, ZH = (f - F_OBS) / SIG_F, (bb - HARV_B) / HARV_S
    allowed = bool(stB and scH and abs(ZB) < 2 and abs(ZH) < 2)
    return dict(f=f, beta_bar=bb, Z_B=ZB, Z_H=ZH, scorable=bool(stB and scH), allowed=allowed, n_H=len(good))

def smax_of(rows):
    smax, first_ex, reentry = None, None, []
    for s, r in zip(GRID, rows):
        if s == 0: continue
        if not r["allowed"] and first_ex is None: first_ex = s
        if first_ex is not None and r["allowed"]: reentry.append(s)
        if first_ex is None: smax = s
    return (math.inf if first_ex is None else (smax if smax is not None else 0.0)), first_ex, reentry

runs = {f: json.load(open(os.path.join(C623, "runs", RUNS[f] + ".json"))) for f in RUNS}
MER = {}
for foot, run in runs.items():
    base = M623.score_run(run)
    MER[foot] = {"baseline_cfg623": dict(f=base["f"], beta_bar=base["beta_bar"])}
    for branch in ("ALL", "FREE"):
        for eta_mode in ("iso", "drag"):
            for rc in RC_SET:
                if eta_mode == "drag" and rc != RC_PRI: continue
                if branch == "FREE" and rc != RC_PRI: continue
                disp, info = layer(run, foot, rc, branch, eta_mode)
                rows = [score(run, disp, s) for s in GRID]
                sm, fe, re_ = smax_of(rows)
                key = f"{branch}_{eta_mode}_rc{int(rc)}"
                MER[foot][key] = dict(info=info, smax=sm, first_excluded=fe, reentry=re_,
                                      rows={f"{s:.4g}": rows[k] for k, s in enumerate(GRID)})
                P(f"  [{foot}] {key}: omega {info['omega_per_Gyr']:.1f}/Gyr (T {info['T_osc_Gyr']:.2f} Gyr), v_esc "
                  f"{info['vesc_kms']:.0f} km/s, V_max {info['V_peri_kms']:.0f} km/s, eta(V_max) {info['eta_at_Vmax']:.4f}, "
                  f"Sigma_tgt(0) {info['Sigma_tgt_center_Msun_pc2']:.0f} Msun/pc^2, w {info['w']:.3f}; "
                  f"max|delta| {info['delta_max_kpc_per_cm2g']:.2f} kpc per cm^2/g -> sigma/m_max = {sm:.3g} "
                  f"(first excluded {fe}; re-entry {re_[:3]})")
    # seed scatter (primary config)
    sc = {}
    for sd in SEEDS:
        fn = os.path.join(C623, "runs", f"{RUNS[foot]}_seed{sd}.json")
        if os.path.exists(fn):
            rr = json.load(open(fn))
            try:
                disp, _ = layer(rr, foot, RC_PRI)
                rows = [score(rr, disp, s) for s in GRID]
                sc[sd] = dict(smax=smax_of(rows)[0], f0=rows[0]["f"], b0=rows[0]["beta_bar"], scorable0=rows[0]["scorable"])
            except Exception as ex:  # noqa: BLE001
                sc[sd] = dict(error=str(ex))
    MER[foot]["seed_scatter_primary"] = sc
    P(f"  [{foot}] seeds (primary): " + "; ".join(f"{k}: smax {v.get('smax')}, f0 {v.get('f0', float('nan')):.3f}, "
                                                    f"b0 {v.get('b0', float('nan')):.3f}, scorable0 {v.get('scorable0')}" for k, v in sc.items()))
    pr = MER[foot]["ALL_iso_rc100"]["rows"]
    for s in ("0", "0.1", "1", "10", "100"):
        rr = pr[s]
        P(f"    primary sigma/m {s:>5}: f {rr['f']:+.4f} (Z_B {rr['Z_B']:+.2f}), beta_bar {rr['beta_bar']:+.4f} (Z_H {rr['Z_H']:+.2f}) "
          f"-> {'ALLOWED' if rr['allowed'] else 'EXCLUDED'}")
R["merger"] = MER

# ================================================================= (b) dwarfs: LITTLE THINGS capacity check
P("\n=== (b) dwarfs: tethered core is sigma/m-independent; is there a free population? (LITTLE THINGS DM-only curves)")
sums = {l.split()[1]: l.split()[0] for l in open(os.path.join(LT, "SHA256SUMS.txt")) if l.strip()}
h = hashlib.sha256(open(os.path.join(LT, "rotdm.dat"), "rb").read()).hexdigest()
lt_ok = sums.get("rotdm.dat") == h
P(f"  rotdm.dat sha256 {'matches' if lt_ok else 'DOES NOT MATCH'} the fetch manifest")
pts = []
for line in open(os.path.join(LT, "rotdm.dat")):
    if line[9:14].strip() != "Data": continue
    nm = line[0:8].strip(); R03 = float(line[15:23]); V03 = float(line[24:34]); Rs = float(line[35:44])
    Vs = float(line[45:54]); eV = float(line[55:63])
    pts.append((nm, R03 * Rs * 1e3, V03 * Vs, V03 * eV))
DW = {}
for foot in A0:
    n_above = 0; gal2 = set(); n = 0; sig_all = []
    for nm, Rpc, V, eVv in pts:
        if Rpc <= 0: continue
        n += 1
        Sg = max(V, 0) ** 2 / (math.pi * G_PC * Rpc); sig_all.append(Sg)
        if Sg > SIGCAP[foot]: n_above += 1
        if max(V - 2 * eVv, 0) ** 2 / (math.pi * G_PC * Rpc) > SIGCAP[foot]: gal2.add(nm)
    frac = n_above / n
    blind = frac <= 0.05 and len(gal2) <= 3
    DW[foot] = dict(n_points=n, n_gal=len({p[0] for p in pts}), frac_above=frac, gal_2sig_above=sorted(gal2),
                    median_Sigma=float(np.median(sig_all)), max_Sigma=float(np.max(sig_all)),
                    verdict="dwarfs below capacity -> dwarf cores sigma/m-blind (NOT DIAGNOSTIC)" if blind else
                    "free population in dwarfs possible; dwarf cores sigma/m-diagnostic (not evaluated here)")
    P(f"  [{foot}] {n} points / {DW[foot]['n_gal']} dwarfs: {100*frac:.1f}% above Sigma_cap {SIGCAP[foot]:.0f}; "
      f"galaxies > 2 sigma above: {sorted(gal2)}; median Sigma_dark(<R) {DW[foot]['median_Sigma']:.1f}, max "
      f"{DW[foot]['max_Sigma']:.1f} Msun/pc^2 -> {DW[foot]['verdict']}")
R["dwarfs"] = DW; R["little_things_checksum_ok"] = lt_ok

# ================================================================= (b) cluster free cores: isothermal model
P("\n=== (b) cluster cores: free population isothermal in (self + baryons + tethered-at-capacity), rho0 = A/((sigma/m)<v>t)")
def iso_solve(rho0, sv, rgrid, mext):
    """isothermal free component: d psi/dr = G (M_f + M_ext)/(sv^2 r^2), rho = rho0 exp(-psi). RK4 on rgrid (from ~0);
    M_ext is given on the nodes and linearly interpolated to the midpoints."""
    n = rgrid.size; psi = np.zeros(n); mf = np.zeros(n)
    mf[0] = 4 / 3 * np.pi * rgrid[0]**3 * rho0
    s2 = sv * sv; gs = G / s2; fp = 4 * np.pi * rho0
    mmid = 0.5 * (mext[1:] + mext[:-1]); ex = math.exp
    p, m = 0.0, mf[0]
    for i in range(1, n):
        a_, b_ = rgrid[i - 1], rgrid[i]; hh = b_ - a_; c_ = a_ + hh / 2
        ea, ec, eb = mext[i - 1], mmid[i - 1], mext[i]
        k1p = gs * (m + ea) / (a_ * a_); k1m = fp * a_ * a_ * ex(-min(p, 700.0))
        p2, m2 = p + hh / 2 * k1p, m + hh / 2 * k1m
        k2p = gs * (m2 + ec) / (c_ * c_); k2m = fp * c_ * c_ * ex(-min(p2, 700.0))
        p3, m3 = p + hh / 2 * k2p, m + hh / 2 * k2m
        k3p = gs * (m3 + ec) / (c_ * c_); k3m = fp * c_ * c_ * ex(-min(p3, 700.0))
        p4, m4 = p + hh * k3p, m + hh * k3m
        k4p = gs * (m4 + eb) / (b_ * b_); k4m = fp * b_ * b_ * ex(-min(p4, 700.0))
        p += hh / 6 * (k1p + 2 * k2p + 2 * k3p + k4p); m += hh / 6 * (k1m + 2 * k2m + 2 * k3m + k4m)
        psi[i], mf[i] = p, m
    return rho0 * np.exp(-np.minimum(psi, 700.0)), mf

def rgrid_of(rt, rmin=1e-2, n=1500):
    return np.logspace(math.log10(rmin), math.log10(rt), n)

# K2 controls
sv0 = 1000.0 * KMS; rho00 = 1e7
r0K = 3 * sv0 / math.sqrt(4 * np.pi * G * rho00)
rgK = rgrid_of(400 * r0K, rmin=1e-3 * r0K, n=4000)
rhoK, mK = iso_solve(rho00, sv0, rgK, np.zeros_like(rgK))
asym = sv0**2 / (2 * np.pi * G * (300 * r0K) ** 2)
k2a = abs(np.interp(300 * r0K, rgK, rhoK) / asym - 1)
rgP = rgrid_of(1200.0); rhoP, mP = iso_solve(rho00, sv0, rgP, np.zeros_like(rgP))
mprojP = mproj(np.concatenate([[0], rgP]), np.concatenate([[rhoP[0]], rhoP]), np.concatenate([[0], mP]), 1200.0 * (1 - 1e-12))
k2b = abs(mprojP / mP[-1] - 1)
Rq = np.linspace(0, 250.0, 501)[1:]
Sq = np.array([2 * np.trapezoid(np.interp(np.sqrt(Rr**2 + np.linspace(0, 1200, 6001)**2), rgP, rhoP, right=0.0), np.linspace(0, 1200, 6001)) for Rr in Rq])
m2d = np.trapezoid(np.concatenate([[0], 2 * np.pi * Rq * Sq]), np.concatenate([[0], Rq]))
m2f = mproj(np.concatenate([[0], rgP]), np.concatenate([[rhoP[0]], rhoP]), np.concatenate([[0], mP]), 250.0)
k2c = abs(m2f / m2d - 1)
R["K2_extra_projection_250kpc_relerr"] = k2c
P(f"   (reported, not frozen) projection formula vs direct 2-D integration at 250 kpc: rel err {k2c:.1e}")
checks["K2"] = k2a <= 0.10 and k2b <= 1e-3
P(f"K2 isothermal solver: rho(300 r0)/singular asymptote - 1 = {k2a:.3f} (<= 0.10); projected/3D mass at r_t - 1 = {k2b:.1e} "
  f"(<= 1e-3) -> {'PASS' if checks['K2'] else 'FAIL'}")

CORE = {}
sig_dark = {k: (M_LENS[k] - M_BAR[k]) / (math.pi * (R_AP * 1e3) ** 2) for k in M_LENS}
for foot in A0:
    CORE[foot] = {"corners": {}}
    obs_free = {k: sig_dark[k] - SIGCAP[foot] for k in M_LENS}
    CORE[foot]["Sigma_obs_free"] = obs_free
    # thermalisation threshold
    th = {}
    for k in M_LENS:
        Mpf = obs_free[k] * math.pi * (R_AP * 1e3) ** 2
        rb = Mpf / (4 / 3 * np.pi * R_AP**3)
        for t_ in T_SET:
            for sv in SV_SET:
                vr = 4 / math.sqrt(math.pi) * sv * KMS
                th[f"{k}_t{t_:g}_sv{sv:g}"] = [1 / (rb * vr * t_) / CM2G, 1 / (0.5 * rb * vr * t_) / CM2G]
    CORE[foot]["sigma_th_cm2g"] = th
    P(f"  [{foot}] observed free Sigma(<250 kpc): main {obs_free['main']:.0f}, sub {obs_free['sub']:.0f} Msun/pc^2; "
      f"thermalisation threshold sigma_th (rho_bar, 0.5 rho_bar): {min(min(v) for v in th.values()):.3f}-{max(max(v) for v in th.values()):.3f} cm^2/g")
    grid_core = [s for s in GRID if s > 0]
    for A_ in A_SET:
        for t_ in T_SET:
            for sv in SV_SET:
                for re_ in RE_SET:
                    ok_all = []; rows = {}
                    for s in grid_core:
                        ok = True; pr_ = {}
                        for k in M_LENS:
                            rg = rgrid_of(RT[k])
                            rr_, rhoe, me = piso(re_, RT[k])
                            kk = (M_BAR[k] + SIGCAP[foot] * math.pi * (R_AP * 1e3) ** 2) / mproj(rr_, rhoe, me, R_AP)
                            mext = np.interp(rg, rr_, me * kk)
                            vr = 4 / math.sqrt(math.pi) * sv * KMS
                            rho0 = A_ / (s * CM2G * vr * t_)
                            rhof, mf = iso_solve(rho0, sv * KMS, rg, mext)
                            rfull = np.concatenate([[0], rg]); dfull = np.concatenate([[rhof[0]], rhof]); mfull = np.concatenate([[0], mf])
                            Sp = mproj(rfull, dfull, mfull, R_AP) / (math.pi * (R_AP * 1e3) ** 2)
                            pr_[k] = Sp
                            if Sp < (1 - 2 * ERR_SIG) * obs_free[k]: ok = False
                        rows[f"{s:.4g}"] = dict(ok=ok, **{f"Sigma_{k}": v for k, v in pr_.items()})
                        ok_all.append(ok)
                        if not ok and len(ok_all) > 1 and not ok_all[-2]:
                            break   # two consecutive exclusions: Sigma_pred decreases monotonically with sigma/m (M2)
                    smax = math.inf
                    for s, ok in zip(grid_core, ok_all):
                        if not ok:
                            idx = grid_core.index(s); smax = grid_core[idx - 1] if idx > 0 else 0.0; break
                    key = f"A{A_:g}_t{t_:g}_sv{sv:g}_re{re_:g}"
                    CORE[foot]["corners"][key] = dict(smax=smax, rows=rows)
    sm = [v["smax"] for v in CORE[foot]["corners"].values()]
    CORE[foot]["smax_min"], CORE[foot]["smax_max"] = min(sm), max(sm)
    P(f"  [{foot}] core sigma/m_max over {len(sm)} bracket corners: {min(sm):.3g} - {max(sm):.3g} cm^2/g")
    for key in (f"A1_t10_sv1000_re100", f"A4_t5_sv1300_re100", f"A1_t5_sv1300_re200", f"A4_t10_sv1000_re50"):
        P(f"     corner {key}: sigma/m_max {CORE[foot]['corners'][key]['smax']:.3g}")

# derived scaling of the free core (pure self-gravitating, sigma_v 1000 km/s, t 10 Gyr, A 1)
P("  derived free-core relation (self-gravitating isothermal, sigma_v 1000 km/s, t 10 Gyr, A 1):")
rel = []
for s in (0.03, 0.1, 0.3, 1.0, 3.0):
    sv = 1000 * KMS; vr = 4 / math.sqrt(math.pi) * sv; rho0 = 1 / (s * CM2G * vr * 10.0)
    r0 = 3 * sv / math.sqrt(4 * np.pi * G * rho0)
    rg = rgrid_of(20 * r0, rmin=1e-3 * r0, n=3000); rhof, mf = iso_solve(rho0, sv, rg, np.zeros_like(rg))
    zz = np.linspace(0, rg[-1], 20001); S0 = 2 * np.trapezoid(np.interp(zz, rg, rhof), zz) / 1e6
    rel.append(dict(sigma_m=s, rho0_Msun_pc3=rho0 / 1e9, r0_kpc=r0, Sigma0_Msun_pc2=S0))
    P(f"     sigma/m {s:4g}: rho0 {rho0/1e9:.2e} Msun/pc^3, King radius r0 {r0:6.0f} kpc, Sigma0 (to 20 r0) {S0:7.0f} Msun/pc^2")
sl_r = np.polyfit(np.log([q["sigma_m"] for q in rel]), np.log([q["r0_kpc"] for q in rel]), 1)[0]
sl_S = np.polyfit(np.log([q["sigma_m"] for q in rel]), np.log([q["Sigma0_Msun_pc2"] for q in rel]), 1)[0]
P(f"     scaling: r0 ~ (sigma/m)^{sl_r:.3f}, Sigma0 ~ (sigma/m)^{sl_S:.3f}")
CORE["relation"] = dict(rows=rel, slope_r0=sl_r, slope_Sigma0=sl_S)
R["cores"] = CORE

# ================================================================= (c)/(d) combination and verdict
P("\n=== (c) combined window and (d) verdict (per footing)")
c723 = json.load(open(os.path.join(C723, "cfg723_results.json")))["B"]["rows"]
FK = {"can": "canonical", "alt": "alt"}
VER = {}
for foot in A0:
    smins = [r["sigma_over_m_min"] for r in c723[FK[foot]]]
    slo_min, slo_max = min(smins), max(smins)
    mer = MER[foot]["ALL_iso_rc100"]["smax"]
    cmin, cmax = CORE[foot]["smax_min"], CORE[foot]["smax_max"]
    core_diag = ((cmin < slo_min) == (cmax < slo_min)) and ((cmin < slo_max) == (cmax < slo_max))
    diag_bounds = [mer] + ([cmin] if core_diag else [])   # if diagnostic, all corners are on the same side; use the min
    S = min(diag_bounds)
    if math.isinf(S): v = "NOT DIAGNOSTIC"
    elif S < slo_min: v = "CLOSED"
    elif S >= slo_max: v = "OPEN"
    else:
        ok_m = [r["Mb"] for r in c723[FK[foot]] if r["sigma_over_m_min"] <= S]
        v = f"OPEN-PARTIAL (halos that can condense: M_b in {ok_m})"
    VER[foot] = dict(s_lo_min=slo_min, s_lo_max=slo_max, merger_smax=mer, core_range=[cmin, cmax], core_diagnostic=core_diag,
                     S_max=S, verdict=v, merger_drag_limit_smax=MER[foot]["ALL_drag_rc100"]["smax"],
                     merger_free_branch_smax=MER[foot]["FREE_iso_rc100"]["smax"],
                     merger_rc_range=[MER[foot][f"ALL_iso_rc{int(rc)}"]["smax"] for rc in RC_SET])
    P(f"  [{foot}] condensate needs sigma/m >= {slo_min:.3f} (M_b 1e9) ... {slo_max:.3f} (1e12)")
    P(f"  [{foot}] merger (primary ALL, iso, rc 100): sigma/m <= {mer:.3g}; r_c 50/100/150: {VER[foot]['merger_rc_range']}; "
      f"FREE branch {VER[foot]['merger_free_branch_smax']:.3g}; drag-limit (tight side, not a verdict input) {VER[foot]['merger_drag_limit_smax']:.3g}")
    P(f"  [{foot}] cluster cores: sigma/m_max {cmin:.3g}-{cmax:.3g} -> {'DIAGNOSTIC' if core_diag else 'NOT DIAGNOSTIC (bracket straddles the window)'}")
    P(f"  [{foot}] S_max = {S:.3g} cm^2/g -> VERDICT: {v}")
R["verdicts"] = VER
R["context_only"] = {"Sagunski21_cluster_limit_cm2g": 0.35, "label": "LCDM-halo Jeans modelling; context only, never a verdict input",
                     "Wittman18": "record row A09d: offsets consistent with zero, bound ~2 cm^2/g (no table on disk)"}
R["checks"] = checks

# ================================================================= MUTATE
if MUT:
    P("\n=== MUTATE")
    mut = {}
    m1 = True
    for foot, run in runs.items():
        base = MER[foot]["baseline_cfg623"]; r0_ = MER[foot]["ALL_iso_rc100"]["rows"]["0"]
        d1 = max(abs(r0_["f"] - base["f"]), abs(r0_["beta_bar"] - base["beta_bar"]))
        m1 &= d1 <= 1e-9
        P(f"  M1 [{foot}] sigma/m = 0 vs CFG623 alpha = 0: |delta| {d1:.1e}")
    # core: no bound at 1e-6
    for foot in A0:
        rg = rgrid_of(RT["sub"]); rr_, rhoe, me = piso(100.0, RT["sub"])
        kk = (M_BAR["sub"] + SIGCAP[foot] * math.pi * (R_AP * 1e3) ** 2) / mproj(rr_, rhoe, me, R_AP)
        vr = 4 / math.sqrt(math.pi) * 1000 * KMS
        rhof, mf = iso_solve(1.0 / (1e-6 * CM2G * vr * 10.0), 1000 * KMS, rg, np.interp(rg, rr_, me * kk))
        Sp = mproj(np.concatenate([[0], rg]), np.concatenate([[rhof[0]], rhof]), np.concatenate([[0], mf]), R_AP) / (math.pi * 6.25e10)
        ok = Sp >= (1 - 2 * ERR_SIG) * CORE[foot]["Sigma_obs_free"]["sub"]
        m1 &= bool(ok); P(f"  M1 [{foot}] core at sigma/m = 1e-6: Sigma_pred(sub) {Sp:.3g} -> no bound: {ok}")
    mut["M1"] = bool(m1)
    m2 = True
    for foot in A0:
        rw = MER[foot]["ALL_iso_rc100"]["rows"]
        disp, _ = layer(runs[foot], foot, RC_PRI)
        s03, s3 = score(runs[foot], disp, 0.3), score(runs[foot], disp, 3.0)
        # direct core evaluation at 0.3 and 3
        Ss = []
        for s in (0.3, 3.0):
            rg = rgrid_of(RT["sub"]); rr_, rhoe, me = piso(100.0, RT["sub"])
            kk = (M_BAR["sub"] + SIGCAP[foot] * math.pi * (R_AP * 1e3) ** 2) / mproj(rr_, rhoe, me, R_AP)
            vr = 4 / math.sqrt(math.pi) * 1000 * KMS
            rhof, mf = iso_solve(1.0 / (s * CM2G * vr * 10.0), 1000 * KMS, rg, np.interp(rg, rr_, me * kk))
            Ss.append(mproj(np.concatenate([[0], rg]), np.concatenate([[rhof[0]], rhof]), np.concatenate([[0], mf]), R_AP) / (math.pi * 6.25e10))
        ok = s3["f"] > s03["f"] and s3["beta_bar"] > s03["beta_bar"] and Ss[1] < Ss[0]
        m2 &= ok
        P(f"  M2 [{foot}] sigma/m 0.3 -> 3: f {s03['f']:.4f} -> {s3['f']:.4f}; beta_bar {s03['beta_bar']:.4f} -> {s3['beta_bar']:.4f}; "
          f"Sigma_free,pred(sub) {Ss[0]:.0f} -> {Ss[1]:.0f}: {'bites' if ok else 'DOES NOT BITE'}")
    mut["M2"] = bool(m2)
    m3 = True
    for foot in A0:
        disp, _ = layer(runs[foot], foot, RC_PRI, sign=-1.0)
        s3 = score(runs[foot], disp, 3.0); b0 = MER[foot]["baseline_cfg623"]["beta_bar"]
        ok = s3["beta_bar"] < b0; m3 &= ok
        P(f"  M3 [{foot}] flipped drag at sigma/m = 3: beta_bar {s3['beta_bar']:.4f} vs {b0:.4f}: {'bites' if ok else 'DOES NOT BITE'}")
    mut["M3"] = bool(m3)
    R["MUTATE"] = mut
    P(f"MUTATE: M1 {mut['M1']}, M2 {mut['M2']}, M3 {mut['M3']}")

P("\nchecks: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in checks.items()))
P("kappa = 1/2 FITTED; footings never pooled; cold energy's mass required; not theory closed; no LCDM/standard-MOND yardstick in a verdict.")
open(os.path.join(HERE, f"cfg725{SUF}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(R, open(os.path.join(HERE, f"cfg725_results{SUF}.json"), "w"), indent=1,
          default=lambda o: (None if (isinstance(o, float) and not math.isfinite(o)) else float(o) if isinstance(o, (np.floating,)) else bool(o) if isinstance(o, np.bool_) else str(o)))
if MUT:
    sys.exit(0 if all(R["MUTATE"].values()) else 1)
sys.exit(0 if all(checks.values()) else 1)

#!/usr/bin/env python3
"""SS5 (FROZEN_CRITERIA.md 12c42eef04): variant L's mechanism. The component feels g_N; baryons feel the law nu(|delta g_N|/a0)
delta g_N on the peculiar field (GR background). D1 two-fluid linear growth with nu(k, z) from the scale's own field; D2(a)
spherical two-species collapse; D2(b) 1D plane N-sheet with offset peaks; KA-L1-L3; MUTATE ML1 (planted v_stiff drift), ML2.
    SS1_FOOT=<f> python3 ss5.py   -> parts/ss5_<footing>.json
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, json, math, time
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from scipy.integrate import solve_ivp
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..")); os.makedirs(os.path.join(HERE, "parts"), exist_ok=True)
CRIT = "12c42eef04"; FOOT = os.environ.get("SS1_FOOT", "canonical"); T0 = time.time()
A0 = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}[FOOT]; VST = {"canonical": 265.8, "alt": 288.1}[FOOT]
Q15 = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX15_cmb_primary_likelihood", "qx15.json")))
th = Q15["footings"][FOOT]["main"]["theta"]; h = float(Q15["footings"][FOOT]["main"]["h"]); OB, OD = th["omega_b"], th["omega_d"]
Om = (OB + OD) / h ** 2; Orad = 2.469e-5 * (1 + 0.2271 * 3.046) / h ** 2; OL = 1 - Om - Orad; fb = OB / (OB + OD)
G = 6.6743e-11; MPC = 3.0857e22; KPC = 3.0857e19; MS = 1.98892e30; H0 = 100 * h * 1e3 / MPC; GYR = 3.15576e16
def H(a): return H0 * math.sqrt(Om / a ** 3 + Orad / a ** 4 + OL)
def acc_bg(a): return H0 ** 2 * (-0.5 * Om / a ** 3 - Orad / a ** 4 + OL)          # Friedmann a''/a (matter + radiation + Lambda)
def nu(y): y = np.maximum(np.asarray(y, float), 1e-30); return 0.5 + np.sqrt(0.25 + 1.0 / y)
def P(s): print(s, flush=True)
RES = dict(criteria=CRIT, footing=FOOT, a0=A0, v_stiff=VST, h=h, Omega_m=Om)
# ---------------- CLASS linear power (reference), for nu(k, z) in D1
from classy import Class
M = Class(); M.set({'output': 'mPk', 'h': h, 'omega_b': OB, 'omega_cdm': OD, 'A_s': math.exp(th["lnAs1e10"]) / 1e10, 'n_s': th["n_s"], 'tau_reio': th["tau"],
                    'N_ur': 3.046, 'T_cmb': 2.7255, 'P_k_max_1/Mpc': 10.0, 'z_max_pk': 20.0}); M.compute()
def drms(k_mpc, z):
    zz = min(z, 20.0); Pk = M.pk_lin(k_mpc, zz) * (((1 + 20.0) / (1 + z)) ** 2 if z > 20 else 1.0); return math.sqrt(k_mpc ** 3 * Pk / (2 * math.pi ** 2))
def gN_scale(k_mpc, z): a = 1 / (1 + z); return 1.5 * H0 ** 2 * Om * drms(k_mpc, z) / (a * a * (k_mpc / MPC))
# ================================================================ D1
def D1(newton=False):
    out = {}
    for kh in (0.1, 0.3, 1.0, 3.0):
        k = kh * h
        def rhs(lna, y):
            a = math.exp(lna); z = 1 / a - 1; Ha = H(a); dl = (-1.5 * Om / a ** 3 - 2 * Orad / a ** 4) * H0 ** 2 / Ha ** 2
            Oc = OD / h ** 2 / a ** 3 * H0 ** 2 / Ha ** 2; Obb = OB / h ** 2 / a ** 3 * H0 ** 2 / Ha ** 2; src = 1.5 * (Oc * y[0] + Obb * y[2])
            n_ = 1.0 if newton else float(nu(gN_scale(k, z) / A0))
            return [y[1], -(2 + dl) * y[1] + src, y[3], -(2 + dl) * y[3] + n_ * src]
        ai = 1 / 1091.0; zs = [3.0, 1.2, 0.0]; s = solve_ivp(rhs, (math.log(ai), 0.0), [ai, ai, 0.0, 0.0], t_eval=[math.log(1 / (1 + z)) for z in zs], rtol=1e-9, atol=1e-14, method="LSODA")
        rows = {}
        for j, z in enumerate(zs):
            dc, dcp, db, dbp = s.y[:, j]; ratio = db / dc; theta_rel = (dbp - dcp) / dcp; drift = (1 / (1 + z)) * H(1 / (1 + z)) / (k / MPC) * abs(dbp - dcp) / dc * drms(k, z) / 1e3
            rows[f"z {z}"] = dict(delta_b_over_delta_chi=ratio, r=1.0 if ratio > 0 else -1.0, theta_rel=theta_rel, drift_kms_if_chi_tracks_reference=drift,
                                  nu=float(nu(gN_scale(k, z) / A0)), y=gN_scale(k, z) / A0, delta_b_rms=abs(ratio) * drms(k, z))
        out[f"k {kh} h/Mpc"] = rows
    return out
d1 = D1(); d1n = D1(newton=True)
RES["D1"] = d1; RES["D1_newton_KA_L1"] = d1n
ka1 = all(abs(v["z 0.0"]["delta_b_over_delta_chi"] - 1) <= 1e-2 for v in d1n.values()); RES["KA_L1"] = bool(ka1)
r_ok = all(v[z]["r"] >= 0.99 for v in d1.values() for z in v); ratio_ok = all(v[z]["delta_b_over_delta_chi"] >= 1 for v in d1.values() for z in ("z 1.2", "z 0.0"))
P(f"[{FOOT}] D1: " + "; ".join(f"{k}: " + ", ".join(f"{z} b/chi {v[z]['delta_b_over_delta_chi']:.3g} (nu {v[z]['nu']:.1f}, delta_b,rms {v[z]['delta_b_rms']:.2g})" for z in v) for k, v in d1.items()) + f"; r = 1 everywhere: {r_ok}; KA-L1 (nu = 1) {ka1}  [{time.time()-T0:.0f}s]")
# ================================================================ background clock for D2
lna_g = np.linspace(math.log(1 / 1101.0), 0.0, 20001); tg = np.concatenate([[0.0], np.cumsum(np.diff(lna_g) / np.array([H(math.exp(0.5 * (lna_g[i] + lna_g[i + 1]))) for i in range(len(lna_g) - 1)]))])
def a_of_t(t): return math.exp(np.interp(t, tg, lna_g))
def t_of_z(z): return float(np.interp(math.log(1 / (1 + z)), lna_g, tg))
def Dlin(z):                                                          # linear growth (matter + Lambda), normalised to a at early times
    s = solve_ivp(lambda lna, y: [y[1], -(2 + (-1.5 * Om / math.exp(3 * lna) - 2 * Orad / math.exp(4 * lna)) * H0 ** 2 / H(math.exp(lna)) ** 2) * y[1] + 1.5 * (Om / math.exp(3 * lna)) * H0 ** 2 / H(math.exp(lna)) ** 2 * y[0]],
                  (math.log(1 / 1101.0), math.log(1 / (1 + z))), [1 / 1101.0, 1 / 1101.0], rtol=1e-9); return s.y[0, -1]
RHO_M0 = Om * 3 * H0 ** 2 / (8 * math.pi * G)                        # kg/m^3 comoving
# ================================================================ D2(a): spherical two-species collapse
NSTEP_A = int(os.environ.get("SS5_NSTEP_A", "400000"))
def D2a(nu_baryon=True, db_init=True, N=200, nstep=None):
    nstep = nstep or NSTEP_A
    zi = 200.0; ai = 1 / (1 + zi); Mtot = 1e12 * MS; qM = (3 * Mtot / (4 * math.pi * RHO_M0)) ** (1 / 3); sig = 0.55 * qM
    qe = np.linspace(0, 2.2 * qM, N + 1); qc = 0.5 * (qe[1:] + qe[:-1])
    prof = lambda q: np.exp(-0.5 * (q / sig) ** 2)
    # amplitude: mean linear delta inside qM equals 1.686 at z 1
    qq = np.linspace(1e-6, qM, 4000); mean_prof = np.trapz(prof(qq) * qq ** 2, qq) * 3 / qM ** 3
    A = D_I / mean_prof
    def dbar(q):
        qq_ = np.linspace(1e-9, q, 400); return A * np.trapz(prof(qq_) * qq_ ** 2, qq_) * 3 / q ** 3
    dmean = np.array([dbar(q) for q in qc]); dloc = A * prof(qc); m_shell = RHO_M0 * 4 / 3 * math.pi * (qe[1:] ** 3 - qe[:-1] ** 3) * (1 + dloc)
    mc = (1 - fb) * m_shell; mb = fb * m_shell
    Hi = H(ai); r0 = ai * qc * (1 - dmean / 3); v0 = Hi * r0 * (1 - dmean / 3)
    rb0 = r0.copy() if db_init else ai * qc; vb0 = v0.copy() if db_init else Hi * ai * qc
    eps = 1.0 * KPC; masses = np.concatenate([mc, mb]); isb = np.concatenate([np.zeros(N, bool), np.ones(N, bool)])
    def rhs(t, y):
        r = np.abs(y[:2 * N]); v = y[2 * N:]; a = a_of_t(t); o = np.argsort(r); Menc = np.empty(2 * N); Menc[o] = np.cumsum(masses[o]) - 0.5 * masses[o]
        Mbg = 4 / 3 * math.pi * RHO_M0 / a ** 3 * r ** 3; dM = Menc - Mbg; r2 = r * r + eps * eps
        gpec = -G * dM / r2; gbg = acc_bg(a) * r                                   # background part: (a''/a) r (fixed after the first run: radiation)
        F = np.where(isb & nu_baryon, nu(np.abs(gpec) / A0), 1.0)
        return np.concatenate([v, np.sign(y[:2 * N]) * (gbg + F * gpec)])        # radial orbits through the centre: the force points back (fixed after the first run)
    # integrator: fixed-step kick-drift-kick leapfrog uniform in t (the first, RK45 solve_ivp, run did not finish in 33 h of CPU on the
    # stiff centre crossings; swapped after it, disclosed); nstep and its 2x check are reported
    ti = t_of_z(zi); zs = [3.0, 1.2, 0.0]; te = [t_of_z(z) for z in zs]; y = np.concatenate([r0, rb0]); u = np.concatenate([v0, vb0])
    dt = (te[-1] - ti) / nstep; t = ti; snaps = {}; trk = []
    def acc(y, t): return rhs(t, np.concatenate([y, np.zeros_like(y)]))[2 * N:]
    g = acc(y, t)
    for n in range(nstep):
        u = u + 0.5 * dt * g; y = y + dt * u; t += dt; g = acc(y, t); u = u + 0.5 * dt * g
        if n % 200 == 0: trk.append((t, np.abs(y).copy()))
        for z_, tz in zip(zs, te):
            if z_ not in snaps and t >= tz - 0.5 * dt: snaps[z_] = np.abs(y).copy()
    class _S: pass
    s = _S(); s.t = np.array([x[0] for x in trk]); s.y = np.array([x[1] for x in trk]).T; s.status = 0; s.nfev = nstep
    def zcoll(idx):
        r = np.abs(s.y[idx]); cm = np.maximum.accumulate(r); j = np.where(r < 0.1 * cm)[0]; return (1 / a_of_t(s.t[j[0]]) - 1) if len(j) else -1.0   # first fall below 10 % of the first turnaround (running max; fixed after the leapfrog swap)
    ih = int(np.argmin(abs(qc - 0.5 ** (1 / 3) * qM)))                         # the shell enclosing about half of the 1e12 region
    colls = dict(z_coll_chi_half_shell=zcoll(ih), z_coll_b_half_shell=zcoll(N + ih), z_coll_chi_qM_shell=zcoll(int(np.argmin(abs(qc - qM)))), z_coll_b_qM_shell=zcoll(N + int(np.argmin(abs(qc - qM)))))
    s.y = np.stack([snaps[z_] for z_ in zs], axis=1)
    out = {}
    inner = qc <= qM
    for j, z in enumerate(zs):
        r = np.abs(s.y[:2 * N, j]); rc_, rb_ = r[:N][inner], r[N:][inner]; wc, wb = mc[inner], mb[inner]
        def rhalf(rr, ww): o = np.argsort(rr); c = np.cumsum(ww[o]); return float(rr[o][np.searchsorted(c, 0.5 * c[-1])])
        Rc, Rb = rhalf(rc_, wc), rhalf(rb_, wb); fin = float(np.sum(wb[rb_ <= Rc]) / np.sum(wb))
        out[f"z {z}"] = dict(R_half_chi_kpc=Rc / KPC, R_half_b_kpc=Rb / KPC, baryon_frac_inside_R_half_chi=fin, r_min_chi_kpc=float(rc_.min() / KPC), r_min_b_kpc=float(rb_.min() / KPC))
    # KA-L2: Newtonian collapse redshift of the shell at qM (first time its radius falls to < 5 % of turnaround) from a dedicated dense run
    return out, dict(A=A, sigma_q_Mpc=sig / MPC, qM_Mpc=qM / MPC, status=s.status, nfev=s.nfev, **colls)
def collapse_z_of(d, zi=200.0):
    ai = 1 / (1 + zi); qM = (3 * 1e12 * MS / (4 * math.pi * RHO_M0)) ** (1 / 3); r0 = ai * qM * (1 - d / 3); v0 = H(ai) * r0 * (1 - d / 3); Mq = 4 / 3 * math.pi * RHO_M0 * qM ** 3 * (1 + d)
    def rhs(t, y): a = a_of_t(t); return [y[1], acc_bg(a) * y[0] - G * (Mq - 4 / 3 * math.pi * RHO_M0 / a ** 3 * y[0] ** 3) / y[0] ** 2]
    s_ = solve_ivp(rhs, (t_of_z(zi), t_of_z(0.0)), [r0, v0], rtol=1e-9, atol=1.0, max_step=0.01 * GYR, dense_output=True)
    ts = np.linspace(s_.t[0], s_.t[-1], 4000); r = s_.sol(ts)[0]; i = int(np.argmax(r)); j = np.where(r[i:] < 0.1 * r[i])[0]
    return (1 / a_of_t(ts[i + j[0]]) - 1) if len(j) else -1.0
def calibrate():
    lo, hi = 1e-3, 0.05
    for _ in range(40):
        mid = math.sqrt(lo * hi); zc_ = collapse_z_of(mid); lo, hi = (lo, mid) if zc_ > 1.0 else (mid, hi)
    return math.sqrt(lo * hi)
D_I = calibrate()                                      # mean delta inside qM at z 200 for a Newtonian collapse at z 1 (frozen spec; fixes the first run's D-ratio, disclosed)
zc = collapse_z_of(D_I); RES["calibrated_mean_delta_i"] = D_I
P(f"[{FOOT}] calibrated mean delta_i (z 200, inside qM) {D_I:.5f}; single-shell Newtonian collapse z {zc:.3f}  [{time.time()-T0:.0f}s]")
d2a, info = D2a(); d2a0, info0 = D2a(db_init=False); d2aN, infoN = D2a(nu_baryon=False)
d2a2, info2 = D2a(nstep=2 * NSTEP_A)                                   # reported: 2x steps
RES["D2a"] = dict(convergence_2x_steps=d2a2, setup_2x=info2, nstep=NSTEP_A, main=d2a, bracket_delta_b_init_0=d2a0, newton_baryons=d2aN, setup=info, setup_db0=info0, setup_newton=infoN)
RES["KA_L2"] = dict(z_coll_newton_qM_shell=infoN["z_coll_chi_qM_shell"], pass_=bool(abs(infoN["z_coll_chi_qM_shell"] - 1.0) <= 0.1))
P(f"[{FOOT}] KA-L2 multi-shell Newtonian collapse z of the qM shell: {infoN['z_coll_chi_qM_shell']:.3f} -> {'PASS' if RES['KA_L2']['pass_'] else 'FAIL'}; collapse z of the half-mass shells (law baryons): chi {info['z_coll_chi_half_shell']:.2f}, b {info['z_coll_b_half_shell']:.2f}; qM shells chi {info['z_coll_chi_qM_shell']:.2f}, b {info['z_coll_b_qM_shell']:.2f}; delta_b,i 0: b half {info0['z_coll_b_half_shell']:.2f}")
conc_ok = (d2a["z 0.0"]["R_half_b_kpc"] <= d2a["z 0.0"]["R_half_chi_kpc"]) and (info["z_coll_b_half_shell"] >= info["z_coll_chi_half_shell"])   # baryons at least as concentrated AND collapse no later
P(f"[{FOOT}] D2(a) spherical: " + "; ".join(f"{z}: R_half chi {v['R_half_chi_kpc']:.0f} kpc, b {v['R_half_b_kpc']:.0f} kpc, baryons inside R_half_chi {v['baryon_frac_inside_R_half_chi']:.2f}" for z, v in d2a.items())
  + f"; Newton baryons z0: chi {d2aN['z 0.0']['R_half_chi_kpc']:.0f} b {d2aN['z 0.0']['R_half_b_kpc']:.0f}; delta_b,i 0: b {d2a0['z 0.0']['R_half_b_kpc']:.0f}  [{time.time()-T0:.0f}s]")
if os.environ.get("SS5_ONLY_A"): sys.exit(0)
# ================================================================ D2(b): 1D plane N-sheet, offset peaks
def D2b(nu_baryon=True, plant=False, N=2000, nstep=6000):
    L = 20.0 * MPC; zi = 200.0; ai = 1 / (1 + zi); q = (np.arange(N) + 0.5) * L / N
    g1 = lambda x, x0, w: np.exp(-0.5 * ((x - x0) / w) ** 2)
    A = 1.2 * Dlin(zi) / Dlin(1.0)
    dq = A * (g1(q, 7 * MPC, 0.8 * MPC) + 0.6 * g1(q, 12.5 * MPC, 1.2 * MPC)); dq = dq - dq.mean()
    Psi = -(np.cumsum(dq) * L / N); Psi -= Psi.mean()
    x0 = (q + Psi) % L; u0 = ai * H(ai) * Psi                                     # u = a dx/dt (peculiar, physical), growing mode f ~ 1
    X = np.concatenate([x0, x0.copy()]); U = np.concatenate([u0, u0.copy()]); wsp = np.concatenate([np.full(N, (1 - fb)), np.full(N, fb)]) * L / N; isb = np.concatenate([np.zeros(N, bool), np.ones(N, bool)])
    def gfield(Xc, a):
        o = np.argsort(Xc); cum = np.empty_like(Xc); cum[o] = np.cumsum(wsp[o]) - 0.5 * wsp[o]
        integ = cum - Xc; integ -= np.sum(wsp * integ) / np.sum(wsp)                 # int delta dx, zero mean (periodic)
        rho_bar = RHO_M0 / a ** 3; return -4 * math.pi * G * rho_bar * a * integ   # physical peculiar field
    t = t_of_z(zi); tend = t_of_z(0.0); dt = (tend - t) / nstep; out = {}; zs = {3.0: t_of_z(3.0), 1.2: t_of_z(1.2), 0.0: tend}; planted = False
    a = a_of_t(t); g = gfield(X, a); F = np.where(isb & nu_baryon, nu(np.abs(g) / A0), 1.0)
    for n in range(nstep):
        a = a_of_t(t)
        if plant and not planted and t >= zs[1.2]: U = U + np.where(isb, VST * 1e3, 0.0); planted = True
        U = U + 0.5 * dt * (-H(a) * U + F * g); X = (X + dt * U / a) % L; t += dt; a = a_of_t(t)
        g = gfield(X, a); F = np.where(isb & nu_baryon, nu(np.abs(g) / A0), 1.0); U = U + 0.5 * dt * (-H(a) * U + F * g)
        for z_, tz in zs.items():
            if f"z {z_}" not in out and t >= tz - 0.5 * dt:
                grid = np.linspace(0, L, 4000, endpoint=False); sm = 0.1 * MPC
                def dens(xs, w):
                    d = np.zeros_like(grid)
                    for sh in (-L, 0.0, L): d += np.sum(w[:, None] * np.exp(-0.5 * ((grid[None, :] - xs[:, None] - sh) / sm) ** 2), axis=0)
                    return d
                dc_, db_ = dens(X[:N], wsp[:N]), dens(X[N:], wsp[N:]); win = (grid > 4 * MPC) & (grid < 10 * MPC)
                pc, pb = grid[win][np.argmax(dc_[win])], grid[win][np.argmax(db_[win])]
                off = abs(pb - pc); off = min(off, L - off)
                out[f"z {z_}"] = dict(peak_chi_Mpc=pc / MPC, peak_b_Mpc=pb / MPC, offset_Mpc=off / MPC, max_nu=float(F[isb].max()) if nu_baryon else 1.0)
    return out
d2b = D2b(); d2bN = D2b(nu_baryon=False); d2bP = D2b(plant=True)
d2b_conv = D2b(nstep=24000); d2bPN = D2b(nu_baryon=False, plant=True)                 # reported: step convergence; planted drift with Newtonian baryons (power check, post-freeze)
RES["D2b"] = dict(main=d2b, ML2_newton=d2bN, ML1_planted=d2bP, convergence_4x_steps=d2b_conv, power_check_planted_newton_reported=d2bPN)
off_ok = all(v["offset_Mpc"] < 0.35 for v in d2b.values()); ka3 = all(v["offset_Mpc"] < 0.02 for v in d2bN.values()); ml1 = d2bP["z 0.0"]["offset_Mpc"] >= 0.35
RES["KA_L3"] = bool(ka3); RES["ML1_bites"] = bool(ml1)
P(f"[{FOOT}] D2(b) 1D: " + "; ".join(f"{z}: peaks chi {v['peak_chi_Mpc']:.2f} b {v['peak_b_Mpc']:.2f}, offset {v['offset_Mpc']:.3f} Mpc (max nu {v['max_nu']:.1f})" for z, v in d2b.items())
  + f"; ML2 Newton offsets " + ", ".join(f"{v['offset_Mpc']:.3f}" for v in d2bN.values()) + f"; ML1 planted v_stiff offsets " + ", ".join(f"{v['offset_Mpc']:.3f}" for v in d2bP.values()) + "; 4x steps " + ", ".join(f"{v['offset_Mpc']:.3f}" for v in d2b_conv.values()) + "; planted + Newton baryons " + ", ".join(f"{v['offset_Mpc']:.3f}" for v in d2bPN.values()) + f"  [{time.time()-T0:.0f}s]")
seg = (not r_ok) or (not off_ok) or (not conc_ok)
RES["mechanism"] = dict(r_ge_099=r_ok, baryons_ge_chi=ratio_ok, baryons_at_least_as_concentrated=bool(conc_ok), offset_lt_035=off_ok, segregation=bool(seg),
                        label=("NO VERDICT (KA or power failed)" if not (ka1 and ka3 and ml1 and RES['KA_L2']['pass_']) else ("D-SEP: run D3" if seg else "FAIL at the mechanism")))
P(f"[{FOOT}] mechanism: {RES['mechanism']}")
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.bool_): return bool(o)
    return o
json.dump(clean(RES), open(os.path.join(HERE, "parts", f"ss5_{FOOT}.json"), "w"), indent=1); M.struct_cleanup()

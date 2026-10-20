"""CFG939 main numerics: P as the exact Lagrangian displacement; shell crossing vs S4.
Criteria: FROZEN_CRITERIA.md (3524438b2) + AMENDMENT_A1_pre_result.md (7dace0a16). Symbolic checks: cfg939_sym.py.
Stages: K1c multi-stream identity; K3 Zel'dovich; N1 1-D tether crossing (exact single stream vs sheets); N2 1-D stiffness
(Lagrangian fluid); K4 NGC 3198 law; K5/K6/K7 + N3 spherical cold infall (C1, C2, energy) + Newtonian control; N4 sudden loss;
N5 per-class consequences (both footings, L* 24/100/300/1000 pc) and the alignment grade; S4 class.
Run:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg939.py                       -> cfg939.out, cfg939_results.json (exit 0 iff all K pass)
      CFG939_MUTATE=<gamma0|tetheroff|a0zero|losstooth|gradetooth> ...     -> cfg939_MUTATE_<name>.out/.json (exit 1 iff the tooth bites;
                                                                              a0zero is report-only and exits 1 by convention)
Units: 1-D runs K = rhobar = a0 = 1 (length a0/(K rhobar), time (K rhobar)^-1/2); spherical runs G = a0 = M_b = 1 (r_M = 1).
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed.
"""
import os, sys, json, math, time, resource, csv
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
MODE = os.environ.get("CFG939_MUTATE", "").strip()
A2 = os.environ.get("CFG939_A2", "0") == "1"                          # AMENDMENT A2 report-only robustness runs (92e2f0627)
if MODE not in ("", "gamma0", "tetheroff", "a0zero", "losstooth", "gradetooth"):
    print("unknown CFG939_MUTATE", MODE); sys.exit(2)
TAG = f"_MUTATE_{MODE}" if MODE else ("_A2" if A2 else "")
OUT, RESF = os.path.join(HERE, f"cfg939{TAG}.out"), os.path.join(HERE, f"cfg939_results{TAG}.json")
LINES, RES = [], {"lane": "CFG939", "criteria": "3524438b2", "amendment_A1": "7dace0a16", "mode": MODE or "normal"}
KOK = {}

def P(s=""):
    print(s, flush=True); LINES.append(s)
def rss_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024 if sys.platform == "darwin" else 1024)
def finish(code):
    RES["runtime_s"] = round(time.time() - T0, 1); RES["peak_rss_mb"] = round(rss_mb(), 1); RES["exit_code"] = code
    P(f"\ndone [{time.time() - T0:.0f} s, peak RSS {rss_mb():.0f} MB], exit {code}.  kappa = 1/2 FITTED; footings never pooled; not theory closed.")
    open(OUT, "w").write("\n".join(LINES) + "\n")
    json.dump(RES, open(RESF, "w"), indent=1, default=float)
    sys.exit(code)
def guard():
    if rss_mb() > 950:
        P(f"RSS GUARD: {rss_mb():.0f} MB > 950 MB -> abort"); finish(3)
def check(name, ok, detail=""):
    KOK[name] = bool(ok); P(f"  {name}: {'PASS' if ok else 'FAIL'}  {detail}"); return bool(ok)

P(__doc__.strip()); P(f"mode: {MODE or 'normal'}"); P()

# ============================================================================================ kernels
def Rk(u, a0=1.0):
    return u * u / (a0 - u)
def dRk(u, a0=1.0):
    return u * (2 * a0 - u) / (a0 - u) ** 2
def Wdiff(s2, s1):
    """What(s2) - What(s1), What(s) = -s^2/2 - s - ln(1 - s)  (a0 = 1)"""
    d = s2 - s1
    return -d * (s2 + s1) / 2 - d - np.log1p(-d / (1 - s1))
def Gant(s):
    """antiderivative of s^(-5/2) What(s): int_r^inf r'^2 What(M/r'^2) dr' = (1/2) M^(3/2) G(M/r^2)"""
    s = np.asarray(s, float); out = np.zeros_like(s)
    sm = s < 0.05
    if np.any(sm):
        x = s[sm]; acc = np.zeros_like(x)
        for n in range(3, 16):
            acc += x ** (n - 1.5) / (n * (n - 1.5))
        out[sm] = acc
    bg = ~sm
    if np.any(bg):
        x = s[bg]; rt = np.sqrt(x)
        out[bg] = -rt + (2 / 3) / rt + (2 / 3) * x ** -1.5 * np.log1p(-x) + (4 / 3) * np.arctanh(rt)
    return out
def Hpot(M, r):
    """int_r^inf R(M/r'^2) dr' = sqrt(M) [artanh sqrt(u) - sqrt(u)], u = M/r^2 (a0 = 1)"""
    tt = np.sqrt(np.asarray(M, float) / np.asarray(r, float) ** 2)
    small = tt < 0.05
    val = np.where(small, tt ** 3 / 3 + tt ** 5 / 5 + tt ** 7 / 7 + tt ** 9 / 9, np.arctanh(np.minimum(tt, 1 - 1e-16)) - tt)
    return np.sqrt(M) * val
def fcrit_x(x):
    x = np.asarray(x, float); rt = np.sqrt(x)
    return 1 - (1 - x) * (np.arctanh(rt) - rt) / x ** 1.5

# ============================================================================================ 1-D sheet code + exact single stream
def sheets_first_crossing(physics, eps=0.3, N=4000, dt=1e-3, tmax=2000.0, a0=1.0):
    """1-D sheets on q in (-pi, pi), Psi0 = -eps sin q, from rest; P_i = Q_rank - x_i (single stream: = -Psi_i, exact).
    physics: 'newton' (force -P: planar Newtonian self-gravity of the excess) or 'tether' (force R(|P|) sgn P, a0)."""
    dq = 2 * math.pi / N; q = -math.pi + (np.arange(N) + 0.5) * dq
    x = q - eps * np.sin(q); v = np.zeros(N)
    def acc(x):
        Pv = q - x                                  # single stream (checked every step: no crossing yet)
        if physics == "newton":
            return -Pv
        u = np.abs(Pv)
        if np.any(u >= a0): return None
        return Rk(u, a0) * np.sign(Pv)
    a = acc(x); t = 0.0; n = 0
    while t < tmax:
        v += 0.5 * dt * a; x += dt * v
        if np.any(x[1:] <= x[:-1]):
            return t + dt, n
        a = acc(x)
        if a is None: return float("nan"), n
        v += 0.5 * dt * a; t += dt; n += 1
        if n % 20000 == 0: guard()
    return float("inf"), n

def exact_single_stream_crossing(eps=0.3, Nq=4001, dt=5e-3, tmax=2000.0, a0=1.0, physics="tether"):
    """Each element is an independent oscillator Psi'' = F(Psi) (single stream, 1-D, exact); J = 1 + Psi0'(q) dPsi/dPsi0,
    with the variational equation integrated alongside (RK4). Returns first t with min_q J <= 0 and the J history."""
    q = np.linspace(-math.pi, math.pi, Nq)
    psi = -eps * np.sin(q); vel = np.zeros(Nq); dps = np.ones(Nq); dvel = np.zeros(Nq); psi0p = -eps * np.cos(q)
    def F(p):
        if physics == "newton": return p, np.ones_like(p)
        u = np.abs(p); return -Rk(u, a0) * np.sign(p), -dRk(u, a0)
    def rhs(y):
        p, w, dp, dw = y; f, fp = F(p); return (w, f, dw, fp * dp)
    y = (psi, vel, dps, dvel); t = 0.0; hist = []; Jprev = 1 + psi0p * dps
    nstep = int(round(tmax / dt))
    for n in range(nstep):
        k1 = rhs(y); y2 = tuple(a + 0.5 * dt * b for a, b in zip(y, k1)); k2 = rhs(y2)
        y3 = tuple(a + 0.5 * dt * b for a, b in zip(y, k2)); k3 = rhs(y3)
        y4 = tuple(a + dt * b for a, b in zip(y, k3)); k4 = rhs(y4)
        y = tuple(a + dt / 6 * (b1 + 2 * b2 + 2 * b3 + b4) for a, b1, b2, b3, b4 in zip(y, k1, k2, k3, k4))
        t += dt
        Jmin = float(np.min(1 + psi0p * y[2]))
        if n % 200 == 0: hist.append((t, Jmin))
        if Jmin <= 0:
            Jm_prev = hist[-1][1] if hist else 1.0
            return t, hist
        if n % 20000 == 0: guard()
    return float("inf"), hist

# ============================================================================================ 1-D Lagrangian fluid with stiffness
def fluid_run(lam, physics, gamma, eps=0.3, N=512, tend=40.0, a0=1.0):
    """periodic Lagrangian fluid over one wavelength; Psi0 = -(eps/k) sin kq; a = F(Psi) + (gamma/2)(J_{j-1/2}^-2 - J_{j+1/2}^-2)/dq.
    gamma = 0: integrate until J <= 0 and interpolate the crossing time ('CROSSING').
    gamma > 0: J -> 0 costs infinite stiffness energy; stop at J_min < 0.02 ('CROSSING-APPROACH') or at a grid-scale jump
    max|dJ| > 0.25 ('BROKE' = gradient catastrophe of the cold fluid with p = pi G L*^2 rho_c^2; S2 does not define the continuation)."""
    k = 2 * math.pi / lam; dq = lam / N; q = (np.arange(N)) * dq - lam / 2
    psi = -(eps / k) * np.sin(k * q); vel = np.zeros(N)
    def Jof(p): return 1 + (np.roll(p, -1) - p) / dq                 # J at j+1/2
    def acc(p):
        J = Jof(p)
        if np.min(J) <= 0: return None, J
        st = (gamma / 2) * (np.roll(J, 1) ** -2 - J ** -2) / dq if gamma > 0 else 0.0
        if physics == "newton": f = p
        else:
            u = np.abs(p)
            if np.any(u >= a0): return None, J
            f = -Rk(u, a0) * np.sign(p)
        return f + st, J
    a, J = acc(psi); t = 0.0; Jmin_hist = [(0.0, float(np.min(J)))]; status = "NO CROSSING"; tstat = None; n = 0
    dtmax = 2e-3; Jmin_run = float(np.min(J))
    while t < tend:
        Jm = float(np.min(J))
        dt = dtmax if gamma <= 0 else min(dtmax, 0.3 * dq * max(Jm, 1e-3) ** 1.5 / math.sqrt(gamma))
        vel += 0.5 * dt * a; psi += dt * vel
        a, J = acc(psi)
        if a is None:
            Jn = float(np.min(J)); status = "CROSSING"; tstat = t + dt * Jm / max(Jm - Jn, 1e-300); break
        vel += 0.5 * dt * a; t += dt; n += 1
        Jm = float(np.min(J)); Jmin_run = min(Jmin_run, Jm)
        if n % 100 == 0: Jmin_hist.append((round(t, 4), Jm))
        if gamma > 0 and Jm < 0.02:
            status, tstat = "CROSSING-APPROACH", t; break
        if float(np.max(np.abs(np.roll(J, -1) - J))) > 0.25:
            status, tstat = "BROKE", t; break
        if n % 20000 == 0: guard()
    return dict(lam=lam, physics=physics, gamma=gamma, N=N, status=status, t=tstat, Jmin_overall=Jmin_run, steps=n, t_reached=round(t, 3),
                Jmin_hist=Jmin_hist[::max(1, len(Jmin_hist) // 40)])

# ============================================================================================ spherical shells (G = a0 = M_b = 1)
RMIN, R0, NSH = 1.0, 50.0, 2000
DT_SPH, SAMP = 0.00125, 400          # spherical leapfrog step; sampling cadence (every 0.5 time units). First run used 0.005 (K5 failed: crossing-kink energy error)
UCORE = (math.sqrt(5) - 1) / 2                          # law at r = 1: u^2/(1-u) = 1
MCORE = UCORE * RMIN ** 2
def u_law(r, Mb=1.0):
    g = Mb / np.asarray(r, float) ** 2; return (-g + np.sqrt(g * g + 4 * g)) / 2
def m_law(r, Mb=1.0):
    return u_law(r, Mb) * np.asarray(r, float) ** 2

def sph_accel(r, dm, Mb, tether=True):
    order = np.argsort(r); rs = r[order]
    m_in = MCORE + dm * np.arange(r.size)
    if tether:
        s_in = m_in / rs ** 2; s_out = (m_in + dm) / rs ** 2
        if np.any(s_out >= 1): s_out = np.minimum(s_out, 1 - 1e-12); s_in = np.minimum(s_in, s_out - 1e-15)
        a_s = -Mb / rs ** 2 + rs ** 2 * Wdiff(s_out, s_in) / dm
    else:
        a_s = -(Mb + m_in + dm / 2) / rs ** 2
    a = np.empty_like(r); a[order] = a_s
    return a, order

def sph_accel_independent(r, dm, Mb):
    """independent implementation (explicit loop over sorted shells, closed-form What) for the A1 force identity check"""
    idx = sorted(range(r.size), key=lambda i: r[i]); a = np.empty(r.size)
    What = lambda s: -s * s / 2 - s - math.log1p(-s)
    for kk, i in enumerate(idx):
        mi = MCORE + kk * dm; mo = mi + dm; ri = r[i]
        a[i] = -Mb / ri ** 2 + ri ** 2 * (What(mo / ri ** 2) - What(mi / ri ** 2)) / dm
    return a

def sph_energy(r, v, dm, Mb, tether=True):
    rs = np.sort(r); N = r.size; m_in = MCORE + dm * np.arange(N); m_out = m_in + dm
    E = 0.5 * dm * float(np.sum(v * v)) - dm * Mb * float(np.sum(1 / rs))
    if tether:
        Et = 0.5 * MCORE ** 1.5 * (Gant(MCORE / RMIN ** 2) - Gant(MCORE / rs[0] ** 2))
        Et += float(np.sum(0.5 * m_out[:-1] ** 1.5 * (Gant(m_out[:-1] / rs[:-1] ** 2) - Gant(m_out[:-1] / rs[1:] ** 2))))
        Et += float(0.5 * m_out[-1] ** 1.5 * Gant(np.array([m_out[-1] / rs[-1] ** 2]))[0])
        E += Et
    else:
        E -= dm * float(np.sum((m_in + dm / 2) / rs))
    return E

def shell_energies(r, v, dm, Mb, order):
    """per-shell E_tf (frozen configuration, test element moving out through the others), E_q (own CURRENT enclosed mass,
    discrete-consistent co-moving single-stream invariant)."""
    rs = r[order]; N = r.size; m_in = MCORE + dm * np.arange(N); m_out = m_in + dm; m_mid = m_in + dm / 2
    rnext = np.append(rs[1:], np.inf)
    Tj = Hpot(m_mid, rs) - np.where(np.isfinite(rnext), Hpot(m_mid, np.where(np.isfinite(rnext), rnext, 1.0)), 0.0)
    Pi_frozen = np.cumsum(Tj[::-1])[::-1]
    Pi_q = 0.5 * (m_out ** 1.5 * Gant(m_out / rs ** 2) - m_in ** 1.5 * Gant(m_in / rs ** 2)) / dm
    vs = v[order]
    Etf_s = 0.5 * vs ** 2 - Mb / rs + Pi_frozen
    Eq_s = 0.5 * vs ** 2 - Mb / rs + Pi_q
    Etf = np.empty(N); Eq = np.empty(N); Etf[order] = Etf_s; Eq[order] = Eq_s
    return Etf, Eq

def law_ic(N=NSH, Rout=R0, Mb=1.0):
    """discrete equilibrium: each shell where its discrete tether force equals Mb/r^2 (exact zero force)"""
    mtot = float(m_law(Rout, Mb)) - MCORE; dm = mtot / N; r = np.empty(N)
    for i in range(N):
        mi = MCORE + i * dm; mo = mi + dm
        f = lambda rr: rr ** 2 * float(Wdiff(np.array(mo / rr ** 2), np.array(mi / rr ** 2))) / dm - Mb / rr ** 2
        lo = max(math.sqrt(mo) * 1.0000001, RMIN * 0.5); hi = Rout * 3
        r[i] = brentq(f, lo, hi, xtol=1e-15, rtol=1e-15, maxiter=500)
    return r, dm

def run_shells(r, v, dm, Mb_of_t, tether, dt, tend, sample_every, avg_from, label, track=True):
    N = r.size; rank0 = np.empty(N, int); o0 = np.argsort(r); rank0[o0] = np.arange(N)
    crossed = np.zeros(N, bool); t_cross = np.full(N, np.inf); t_tf = np.full(N, np.inf); t_q = np.full(N, np.inf)
    Mb = Mb_of_t(0.0); E0 = sph_energy(r, v, dm, Mb, tether)
    a, order = sph_accel(r, dm, Mb, tether); nst = int(round(tend / dt)); samples = []; first_cross = np.inf
    RAD = np.array([2.0, 5.0, 10.0, 20.0]); id_err = 0.0; id_rel = 0.0; t = 0.0
    if track and tether:
        Etf, Eq = shell_energies(r, v, dm, Mb, order)
        t_tf[Etf > 0] = 0.0; t_q[Eq > 0] = 0.0
    for n in range(nst):
        v += 0.5 * dt * a; r += dt * v
        low = r < RMIN; r[low] = 2 * RMIN - r[low]; v[low] = -v[low]
        t = (n + 1) * dt; Mb = Mb_of_t(t)
        a, order = sph_accel(r, dm, Mb, tether)
        v += 0.5 * dt * a
        rank = np.empty(N, int); rank[order] = np.arange(N)
        new = (rank != rank0) & ~crossed
        if np.any(new):
            crossed[new] = True; t_cross[new] = t
            if not np.isfinite(first_cross): first_cross = t
        if track and n % sample_every == 0:
            if tether:
                Etf, Eq = shell_energies(r, v, dm, Mb, order)
                t_tf[(Etf > 0) & ~np.isfinite(t_tf)] = t; t_q[(Eq > 0) & ~np.isfinite(t_q)] = t
            if t >= avg_from:
                rs = r[order]; samples.append((MCORE + dm * np.searchsorted(rs, RAD)) / m_law(RAD))
            if tether and n % (sample_every * 400) == 0:
                ai = sph_accel_independent(r, dm, Mb)
                id_err = max(id_err, float(np.max(np.abs(ai - a))))                 # absolute, a0 units (A1 gives no normalisation)
                id_rel = max(id_rel, float(np.max(np.abs(ai - a) / (Mb / r ** 2))))
        if n % 20000 == 0: guard()
    E1 = sph_energy(r, v, dm, Mb, tether)
    if tether: Etf, Eq = shell_energies(r, v, dm, Mb, order)
    else: Etf = Eq = np.full(N, np.nan)                     # tether energies undefined for the Newtonian control
    return dict(label=label, r=r, v=v, dm=dm, E0=E0, E1=E1, dE_rel=abs(E1 - E0) / abs(E0), crossed=crossed, t_cross=t_cross,
                first_cross=first_cross, t_tf=t_tf, t_q=t_q, Etf=Etf, Eq=Eq, samples=np.array(samples), RAD=RAD, id_err=id_err, id_rel=id_rel,
                Mb_end=Mb)

# ============================================================================================ A2 report-only runs (POST HOC, no class weight)
if A2:
    P("AMENDMENT A2 (POST HOC, 92e2f0627) report-only C1 robustness: N3 tether run (uniform sphere, full kernel) at other steps and a longer run")
    mtot = float(m_law(R0)) - MCORE; dm3 = mtot / NSH
    qq = (np.arange(NSH) + 0.5) / NSH; r_uni = (RMIN ** 3 + qq * (R0 ** 3 - RMIN ** 3)) ** (1 / 3)
    RES["A2"] = {}
    for lab, dtr, tend, avg in (("a dt 0.0025", 0.0025, 2000.0, 1000.0), ("b dt 0.000625", 0.000625, 2000.0, 1000.0),
                                ("c dt 0.00125 t_end 6000", 0.00125, 6000.0, 4000.0)):
        smp = int(round(0.5 / dtr))
        o = run_shells(r_uni.copy(), np.zeros(NSH), dm3, lambda t: 1.0, True, dtr, tend, smp, avg, lab, track=True)
        mr = o["samples"].mean(axis=0); ins = o["r"] <= 5.0
        c1 = "TETHERED AFTER CROSSING" if (np.mean(o["crossed"][ins]) >= 0.9 and abs(mr[0] - 1) <= 0.05 and abs(mr[1] - 1) <= 0.05) else "UNTETHERED"
        cr = o["crossed"]; c2a = float(np.mean((o["Etf"] > 0)[cr])) if cr.any() else float("nan")
        RES["A2"][lab] = dict(m_over_mlaw={str(R): float(x) for R, x in zip(o["RAD"], mr)}, crossed_inside5=float(np.mean(o["crossed"][ins])),
                              dE_rel=o["dE_rel"], C1_rule=c1, C2a_Etf=c2a)
        P(f"  [{lab}] m/m_law at 2/5/10/20 r_M: " + " / ".join(f"{x:.3f}" for x in mr) + f"; crossed inside 5 {np.mean(o['crossed'][ins]):.3f}; "
          f"dE/E {o['dE_rel']:.1e}; frozen C1 rule -> {c1}; C2(a) E_tf {c2a:.3f}")
    finish(0)

# ============================================================================================ MUTATE-only fast paths
if MODE == "tetheroff":
    P("M2 tether off (W_full -> 0): N1 start (eps 0.3) under planar Newtonian self-gravity; must collapse at the K3 time")
    tN, _ = sheets_first_crossing("newton", eps=0.3, dt=1e-4, tmax=50)
    tZ = math.acosh(1 / 0.3)
    tT, _ = sheets_first_crossing("tether", eps=0.3, dt=1e-3, tmax=50)
    RES["M2"] = dict(t_newton=tN, t_zeldovich=tZ, t_tether_same_window=tT)
    bite = abs(tN / tZ - 1) < 0.005 and not (abs(tT / tZ - 1) < 0.05)
    P(f"  Newtonian first crossing {tN:.5f} vs Zel'dovich {tZ:.5f} (rel {abs(tN / tZ - 1):.1e}); canonical tether in the same window: "
      f"{tT} -> {'BITES' if bite else 'DOES NOT BITE'}")
    finish(1 if bite else 0)

if MODE == "a0zero":
    P("M3 literal a0 -> 0 (a0 = 1e-6), REPORT ONLY. The frozen start (eps 0.3) is INADMISSIBLE: u = |P| up to 0.3 > a0 (capacity wall).")
    P("    Admissible start scaled to eps = 0.3 a0; exact single-stream oscillators; Newtonian crossing for that start = arccosh(1/(0.3 a0)).")
    a0m = 1e-6
    t3, h3 = exact_single_stream_crossing(eps=0.3 * a0m, a0=a0m, tmax=2000.0)
    tN3 = math.acosh(1 / (0.3 * a0m))
    Jm = min(h[1] for h in h3) if h3 else 1.0
    RES["M3"] = dict(a0=a0m, eps=0.3 * a0m, t_cross_tether=t3, min_J_by_tmax=Jm, one_minus_minJ=1 - Jm, t_cross_newton_same_start=tN3,
                     reading="no Newtonian collapse: J - 1 scales with a0, so the tether crossing time grows as 1/a0 (non-commuting limit)")
    P(f"  tether: first crossing {t3} by t = 2000 (1 - min J = {1 - Jm:.3e}); Newtonian same start: {tN3:.2f}. Literal a0 -> 0 does NOT give"
      f" Newtonian collapse (the wall pins the medium; J - 1 is O(a0)).")
    finish(1)

if MODE == "gamma0":
    P("M1 gamma -> 0: N2 tether-off run at lambda = 2 L* (< lambda_J = 4.443 L*): frozen gamma = L*^2/2 vs gamma = 0")
    rg = fluid_run(2.0, "newton", 0.5, tend=40.0); r0 = fluid_run(2.0, "newton", 0.0, tend=40.0)
    tZ = math.acosh(1 / 0.3)
    nocross_g = rg["status"] not in ("CROSSING", "CROSSING-APPROACH") and rg["Jmin_overall"] >= 0.1     # frozen: 'no crossing (J_min >= 0.1)'
    bite = nocross_g and (r0["status"] == "CROSSING" and abs(r0["t"] / tZ - 1) < 0.01)
    RES["M1"] = dict(with_gamma=rg, gamma0=r0, t_zeldovich=tZ)
    P(f"  gamma 0.5: {rg['status']} at t {rg['t']} (J_min over the integrated interval {rg['Jmin_overall']:.3f}; no J -> 0); gamma 0: {r0['status']} at t "
      f"{r0['t']:.5f} vs Zel'dovich {tZ:.5f} (rel {abs(r0['t'] / tZ - 1):.1e}) -> {'BITES' if bite else 'DOES NOT BITE'}")
    if rg["t"] is not None:
        P(f"  caveat: the gamma > 0 run is integrable only to its gradient catastrophe (t {rg['t']:.3f}); at that time the gamma = 0 run has "
          f"J_min = 1 - 0.3 cosh t = {1 - 0.3 * math.cosh(rg['t']):.3f} vs >= {rg['Jmin_overall']:.3f} with stiffness")
        RES["M1"]["Jmin_gamma0_at_tb"] = 1 - 0.3 * math.cosh(rg["t"])
    finish(1 if bite else 0)

# ============================================================================================ K1c: multi-stream 1-D identity
if MODE == "":
    P("=== K1c  multi-stream 1-D identity: folded map x(q) = q - 2 sin q on q in [-pi, pi] (rhobar = 1)")
    xmap = lambda qq: qq - 2 * np.sin(qq); Jmap = lambda qq: 1 - 2 * np.cos(qq)
    qext = [-math.pi, -math.pi / 3, math.pi / 3, math.pi]          # J = 0 at +-pi/3
    def streams(x0):
        roots = []
        for a_, b_ in zip(qext[:-1], qext[1:]):
            fa, fb = xmap(a_) - x0, xmap(b_) - x0
            if fa == 0: roots.append(a_)
            elif fa * fb < 0: roots.append(brentq(lambda qq: xmap(qq) - x0, a_, b_, xtol=1e-15))
        return sorted(roots)
    def PE(x0):                                                    # cumulative mass left of x0 minus background
        rt = streams(x0); pts = [-math.pi] + rt + [math.pi]; meas = 0.0
        for a_, b_ in zip(pts[:-1], pts[1:]):
            mid = 0.5 * (a_ + b_)
            if xmap(mid) < x0: meas += b_ - a_
        return meas - (x0 + math.pi)
    errP, errD, nmulti = 0.0, 0.0, 0
    for x0 in np.linspace(-2.9, 2.9, 59):
        rt = streams(x0)
        if any(abs(Jmap(qq)) < 0.05 for qq in rt): continue
        alt = -sum(np.sign(Jmap(qq)) * (x0 - qq) for qq in rt)
        errP = max(errP, abs(PE(x0) - alt))
        h = 1e-5; dPdx = (PE(x0 + h) - PE(x0 - h)) / (2 * h); rho = sum(1 / abs(Jmap(qq)) for qq in rt)
        errD = max(errD, abs(dPdx - (rho - 1)) / max(rho, 1.0)); nmulti += len(rt) > 1
    RES["K1c"] = dict(max_err_P=errP, max_rel_err_div=errD, n_multistream_points=nmulti)
    check("K1c P_E = -rhobar sum_s sign(J_s) Psi_s and d_x P_E = rho - rhobar through the fold", errP < 1e-6 and errD < 1e-6 and nmulti > 5,
          f"max |dP| {errP:.1e}, max rel div err {errD:.1e}, {nmulti} three-stream points")

# ============================================================================================ K3, N1, N2
if MODE == "":
    P("\n=== K3  Zel'dovich 1-D (Newtonian control: tether off, gamma 0, static background), eps 0.3, from rest")
    tZ = math.acosh(1 / 0.3)
    tN, _ = sheets_first_crossing("newton", eps=0.3, dt=1e-4, tmax=50)
    RES["K3"] = dict(t_zeldovich=tZ, t_sheets=tN)
    check("K3 sheet first crossing = arccosh(1/eps)/sqrt(K rhobar) within 0.5%", abs(tN / tZ - 1) < 0.005, f"{tN:.5f} vs {tZ:.5f}")

    P("\n=== N1  1-D canonical tether (S2+S3, gamma 0, no baryons): exact single stream (independent oscillators) vs sheets")
    tex, hex_ = exact_single_stream_crossing(eps=0.3, tmax=2000.0)
    tsh, _ = sheets_first_crossing("tether", eps=0.3, dt=5e-3, tmax=2000.0)
    # oscillation period at amplitude 0.3 (quadrature) for scale
    A = 0.3; Tosc = 4 * quad(lambda p: 1 / math.sqrt(2 * (float(Wdiff(np.array(A), np.array(0.0))) - float(Wdiff(np.array(p), np.array(0.0))))), 0, A, limit=200)[0]
    RES["N1"] = dict(t_cross_exact=tex, t_cross_sheets=tsh, T_osc_A03=Tosc, n_periods=tex / Tosc if np.isfinite(tex) else None,
                     Jmin_history=hex_[::50])
    ok_n1 = np.isfinite(tex) and np.isfinite(tsh) and abs(tsh / tex - 1) < 0.02
    P(f"  exact single stream: first crossing t = {tex:.3f} ({tex / Tosc:.2f} oscillation periods at amplitude 0.3, T = {Tosc:.3f}); "
      f"sheets: {tsh:.3f}; agreement {'WITHIN 2%' if ok_n1 else 'NOT within 2%'}")
    RES["N1"]["agree_2pct"] = bool(ok_n1)
    P("  (Newtonian collapse of the same start: t = 1.874; the canonical tether crosses only by anharmonic dephasing.)")

    P("\n=== N2  1-D stiffness (Lagrangian fluid, L* = 1, gamma = L*^2/2; predicted lambda_J = sqrt(2) pi L* = 4.443 for the Newtonian control)")
    n2 = []
    for lam in (2.0, 4.0, 8.0, 16.0):
        for phys in ("newton", "tether"):
            if phys == "tether" and 0.3 * lam / (2 * math.pi) >= 0.95: continue
            rr_ = fluid_run(lam, phys, 0.5, tend=40.0 if phys == "newton" else 300.0)
            n2.append(rr_)
            P(f"  lambda {lam:5.1f}  {phys:6s} gamma 0.5: {rr_['status']:12s} t {rr_['t']}  J_min {rr_['Jmin_overall']:.3f}  (reached t {rr_['t_reached']})")
    for lam in (2.0, 8.0):
        rr_ = fluid_run(lam, "tether", 0.0, tend=300.0); n2.append(rr_)
        P(f"  lambda {lam:5.1f}  tether gamma 0  : {rr_['status']:12s} t {rr_['t']}  J_min {rr_['Jmin_overall']:.3f}")
    res_chk = [fluid_run(2.0, "newton", 0.5, N=NN, tend=40.0) for NN in (512, 2048)]
    P(f"  resolution check (lambda 2, Newtonian+stiffness): gradient catastrophe at t {res_chk[0]['t']:.4f} (N 512) vs {res_chk[1]['t']:.4f} (N 2048)")
    RES["N2"] = dict(runs=n2, resolution=[dict(N=x["N"], status=x["status"], t=x["t"]) for x in res_chk])

# ============================================================================================ K4: NGC 3198
if MODE == "":
    P("\n=== K4  record galaxy NGC 3198 (SPARC rotmod; V_bar^2 = Vg|Vg| + 0.5 Vd|Vd| + 0.7 Vb|Vb|; spherical M_b(<R) = V_bar^2 R/G)")
    Gk = 4.30091e-6; KPC_M = 3.0857e19
    rows = []
    for l in open(os.path.join(REPO, "real_research", "data", "sparc_data", "NGC3198_rotmod.dat")):
        if l.startswith("#") or not l.strip(): continue
        Rr, V, eV, Vg, Vd, Vb = [float(z) for z in l.split()[:6]]; rows.append((Rr, V, eV, Vg, Vd, Vb))
    rows = np.array(rows); Rr = rows[:, 0]
    Vb2 = rows[:, 3] * np.abs(rows[:, 3]) + 0.5 * rows[:, 4] * np.abs(rows[:, 4]) + 0.7 * rows[:, 5] * np.abs(rows[:, 5])
    gN = Vb2 / Rr; Mb_ = Vb2 * Rr / Gk
    k4 = {}
    for fk, a0si in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
        a0k = a0si * KPC_M / 1e6
        # Lagrangian single-stream rest state: shells at rest with m_c(<r) such that F = -g_N + R(G m_c/r^2) = 0
        mc = np.array([brentq(lambda m: Rk(Gk * m / R_ ** 2, a0k) - g_, 0.0, a0k * R_ ** 2 / Gk * (1 - 1e-15), xtol=1e-30, rtol=1e-15)
                       for R_, g_ in zip(Rr, gN)])
        u_ = Gk * mc / Rr ** 2; g_ = gN + u_
        nu = 0.5 + np.sqrt(0.25 + a0k / gN)
        rel = float(np.max(np.abs(g_ / (nu * gN) - 1)))
        F = -gN + Rk(u_, a0k); relF = float(np.max(np.abs(F) / gN))
        Vp = np.sqrt(g_ * Rr); rms = float(np.sqrt(np.mean(((Vp - rows[:, 1]) / rows[:, 2]) ** 2)))
        k4[fk] = dict(max_rel_g_vs_nu_s=rel, max_rel_force=relF, V_pred_last=float(Vp[-1]), V_obs_last=float(rows[-1, 1]),
                      rms_pull_INFO=rms, M_c_over_M_b_last=float(mc[-1] / Mb_[-1]))
        check(f"K4 [{fk}] static single-stream shells reproduce g = nu_s g_N", rel <= 1e-10 and relF <= 1e-10,
              f"max rel {rel:.1e}; force {relF:.1e}; INFO V_pred/V_obs at {Rr[-1]:.1f} kpc {Vp[-1]:.1f}/{rows[-1, 1]:.1f} km/s, rms pull {rms:.2f}")
    RES["K4"] = k4

# ============================================================================================ K7 (CFG747 force identity), K5 control
if MODE == "":
    P("\n=== K7  deep-kernel force vs CFG747's (m_out^3 - m_in^3)/(3 dm r^4) (formula re-implemented from cfg747.py, read only)")
    rng = np.random.default_rng(939)
    rr = np.sort(rng.uniform(50.0, 400.0, 500)); dm7 = 0.01; mi = 0.5 + dm7 * np.arange(500); mo = mi + dm7
    s_o, s_i = mo / rr ** 2, mi / rr ** 2
    # deep cubic What_deep(s) = s^3/3  -> r^2 [s_o^3 - s_i^3]/(3 dm)
    mine = rr ** 2 * (s_o ** 3 - s_i ** 3) / (3 * dm7)
    rec = (mo ** 3 - mi ** 3) / (3 * dm7 * rr ** 4)
    e7 = float(np.max(np.abs(mine / rec - 1)))
    full = rr ** 2 * Wdiff(s_o, s_i) / dm7
    check("K7 deep-kernel discrete force == CFG747 formula", e7 <= 1e-12, f"max rel {e7:.1e}; full kernel / deep at these radii: "
          f"{float(np.min(full / rec)):.4f}-{float(np.max(full / rec)):.4f}")
    RES["K7"] = dict(max_rel=e7)

    P("\n=== K5  law control at rest (discrete equilibrium, point baryon mass, r_min 1, R0 50, N 2000)")
    rL, dmL = law_ic()
    aL, oL = sph_accel(rL.copy(), dmL, 1.0, True)
    relF = float(np.max(np.abs(aL) / (1.0 / rL ** 2)))
    out = run_shells(rL.copy(), np.zeros(NSH), dmL, lambda t: 1.0, True, 0.005, 100.0, 100, 1e9, "law control", track=False)
    check("K5a law control: |force| <= 1e-10 g_N and |dE/E| <= 1e-10 over t = 100", relF <= 1e-10 and out["dE_rel"] <= 1e-10,
          f"force {relF:.1e}, dE/E {out['dE_rel']:.1e}, crossings {int(out['crossed'].sum())}")
    RES["K5_control"] = dict(rel_force=relF, dE_rel=out["dE_rel"])
    # A1 row: flat frozen potential of the law state (finite edge R0): E_tf at rest should be ~ mu_edge = -(2/3)/R0 (deep)
    Etf0, Eq0 = shell_energies(rL, np.zeros(NSH), dmL, 1.0, np.argsort(rL))
    mu_edge_pred = -(1.0 / R0) + float(Hpot(np.array(m_law(R0)), np.array(R0)))
    RES["A1_flat_potential"] = dict(Etf_min=float(Etf0.min()), Etf_max=float(Etf0.max()), mu_edge_pred=mu_edge_pred,
                                     deep_formula=-(2 / 3) / R0, Eq_over_minus_two_thirds_Mb_over_r_at_r_gt_20=float(np.median(Eq0[rL > 20] / (-(2 / 3) / rL[rL > 20]))))
    P(f"  A1 report: frozen E_tf of the law state at rest spans [{Etf0.min():.5f}, {Etf0.max():.5f}] vs mu_edge {mu_edge_pred:.5f} "
      f"(deep -(2/3)/R0 = {-(2 / 3) / R0:.5f}); co-moving E_q / (-(2/3) M_b/r) at r > 20: {RES['A1_flat_potential']['Eq_over_minus_two_thirds_Mb_over_r_at_r_gt_20']:.4f}")

# ============================================================================================ N4 sudden loss (+ K6, M4)
def sudden_loss(f, tend=1500.0, dt=DT_SPH, track=True):
    rL, dmL = law_ic()
    Mb1 = 1.0 - f
    Etf0, Eq0 = shell_energies(rL, np.zeros(NSH), dmL, Mb1, np.argsort(rL))
    out = run_shells(rL.copy(), np.zeros(NSH), dmL, lambda t: Mb1, True, dt, tend, SAMP, 1e9, f"loss f={f}", track=track)
    out["Eq0"] = Eq0; out["Etf0"] = Etf0; out["r0"] = rL
    return out

if MODE == "losstooth":
    P("M4 sudden-loss tooth: f = 2/3 -+ 0.05 must flip deep shells (r >= 10 r_M) bound <-> unbound (co-moving E_q at t = 0+, and escape)")
    res4 = {}
    for f in (2 / 3 - 0.05, 2 / 3 + 0.05):
        o = sudden_loss(f, tend=1500.0)
        deep = o["r0"] >= 10
        unb0 = float(np.mean(o["Eq0"][deep] > 0)); esc = float(np.mean((o["r"][deep] > 10 * R0) & (o["v"][deep] > 0)))
        res4[f"{f:.4f}"] = dict(unbound_t0_deep=unb0, escaped_deep=esc, crossed_deep=float(np.mean(o["crossed"][deep])))
        P(f"  f = {f:.4f}: deep shells unbound at t=0+ {unb0:.3f}; escaped beyond 10 R0 by t=1500 {esc:.3f}; crossed {res4[f'{f:.4f}']['crossed_deep']:.3f}")
    RES["M4"] = res4
    vals = list(res4.values())
    bite = vals[0]["unbound_t0_deep"] < 0.05 and vals[1]["unbound_t0_deep"] > 0.95
    P(f"  -> {'BITES' if bite else 'DOES NOT BITE'}")
    finish(1 if bite else 0)

# ============================================================================================ N3 spherical cold infall (C1, C2, energy)
if MODE == "":
    P(f"\n=== N3  spherical cold infall (S2+S3 exact Lagrangian dynamics; full kernel; uniform sphere at rest from r_min 1 to R0 50; "
      "N 2000; dt {DT_SPH}; t_end 2000; time average over [1000, 2000])")
    mtot = float(m_law(R0)) - MCORE; dm3 = mtot / NSH
    qq = (np.arange(NSH) + 0.5) / NSH; r_uni = (RMIN ** 3 + qq * (R0 ** 3 - RMIN ** 3)) ** (1 / 3)
    n3 = {}
    for tether, lab in ((True, "tether"), (False, "newton_control")):
        dtr, smp = (DT_SPH, SAMP) if tether else (DT_SPH / 4, SAMP * 4)    # A2: control at dt/4 (reflection random walk, K5c)
        o = run_shells(r_uni.copy(), np.zeros(NSH), dm3, lambda t: 1.0, tether, dtr, 2000.0, smp, 1000.0, lab, track=True)
        mr = o["samples"].mean(axis=0) if len(o["samples"]) else np.full(4, np.nan)
        inside5 = o["r"] <= 5.0
        cr_in5 = float(np.mean(o["crossed"][inside5])) if np.any(inside5) else float("nan")
        esc = (o["r"] > 10 * R0) & (o["v"] > 0)
        outb = (o["r"] > R0) & (o["v"] > 0) & (o["Eq"] > 0)
        d = dict(m_over_mlaw={str(R): float(x) for R, x in zip(o["RAD"], mr)}, crossed_frac=float(o["crossed"].mean()),
                 crossed_frac_inside5=cr_in5, mass_inside5=float(dm3 * inside5.sum()), first_cross=float(o["first_cross"]), dE_rel=o["dE_rel"],
                 escaped_frac=float(esc.mean()), outbound_unbound_frac=float(outb.mean()), force_identity_max_abs=o["id_err"],
                 force_identity_max_rel_gN=o["id_rel"])
        if tether:
            cr = o["crossed"]
            for nm, unb, tfirst in (("E_tf", o["Etf"] > 0, o["t_tf"]), ("E_q", o["Eq"] > 0, o["t_q"]), ("ESC", esc, None)):
                a_ = float(np.mean(unb[cr] | esc[cr])) if np.any(cr) else float("nan")
                if tfirst is not None:
                    ever = np.isfinite(tfirst)
                    b_ = float(np.mean(o["t_cross"][ever] < tfirst[ever])) if np.any(ever) else float("nan")
                    nev = int(ever.sum())
                else:
                    b_ = float(np.mean(cr[esc])) if np.any(esc) else float("nan"); nev = int(esc.sum())
                d[f"C2a_{nm}"] = a_; d[f"C2b_{nm}"] = b_; d[f"n_ever_unbound_{nm}"] = nev
            ke = 0.5 * dm3 * o["v"] ** 2
            d["energy"] = dict(E0=o["E0"], E_end=o["E1"], KE_outbound_unbound=float(ke[outb].sum()), KE_rest=float(ke[~outb].sum()),
                               E_q_sum_outbound=float(dm3 * o["Eq"][outb].sum()), mass_outbound=float(dm3 * outb.sum()), mass_total=float(dm3 * NSH))
        n3[lab] = d
        P(f"  [{lab}] m/m_law at r = 2/5/10/20: " + " / ".join(f"{x:.3f}" for x in mr) +
          f"; crossed {d['crossed_frac']:.3f} (inside 5: {cr_in5:.3f}, mass inside 5 {d['mass_inside5']:.2f}); first crossing t {d['first_cross']:.2f}; "
          f"dE/E {o['dE_rel']:.1e}; escaped {d['escaped_frac']:.3f}; outbound unbound {d['outbound_unbound_frac']:.3f}")
        if tether:
            P("    C2 (crossing => positive binding) / (positive binding => crossed first): " +
              "; ".join(f"{nm}: {d[f'C2a_{nm}']:.3f} / {d[f'C2b_{nm}']:.3f} (n {d[f'n_ever_unbound_{nm}']})" for nm in ("E_tf", "E_q", "ESC")))
            P(f"    force identity (independent implementation): max |da| {o['id_err']:.1e} a0 (relative to g_N {o['id_rel']:.1e})")
            e = d["energy"]; P(f"    energy: E0 {e['E0']:.4f} -> {e['E_end']:.4f}; outbound unbound mass {e['mass_outbound']:.3f} of {e['mass_total']:.3f}, "
                               f"carrying KE {e['KE_outbound_unbound']:.4f} (sum E_q {e['E_q_sum_outbound']:.4f}); KE of the rest {e['KE_rest']:.4f}")
    RES["N3"] = n3
    check("K5b energy conservation with crossings (tether run) |dE/E| <= 1e-3", n3["tether"]["dE_rel"] <= 1e-3, f"{n3['tether']['dE_rel']:.1e}")
    check("K5c energy conservation with crossings (Newtonian control) |dE/E| <= 1e-3", n3["newton_control"]["dE_rel"] <= 1e-3, f"{n3['newton_control']['dE_rel']:.1e}")
    check("A1 force identity (independent implementation) <= 1e-12 a0", n3["tether"]["force_identity_max_abs"] <= 1e-12,
          f"{n3['tether']['force_identity_max_abs']:.1e} (relative to g_N {n3['tether']['force_identity_max_rel_gN']:.1e})")
    # C1
    t3 = n3["tether"]; mr2, mr5 = t3["m_over_mlaw"]["2.0"], t3["m_over_mlaw"]["5.0"]
    nc2, nc5 = n3["newton_control"]["m_over_mlaw"]["2.0"], n3["newton_control"]["m_over_mlaw"]["5.0"]
    ctrl_discriminates = not (abs(nc2 - 1) <= 0.05 and abs(nc5 - 1) <= 0.05)
    c1_teth = t3["crossed_frac_inside5"] >= 0.9 and abs(mr2 - 1) <= 0.05 and abs(mr5 - 1) <= 0.05
    C1 = ("TETHERED AFTER CROSSING" if c1_teth else "UNTETHERED") if ctrl_discriminates else "NOT DIAGNOSTIC"
    RES["C1"] = dict(class_=C1, crossed_inside5=t3["crossed_frac_inside5"], m2=mr2, m5=mr5, control_m2=nc2, control_m5=nc5,
                     control_discriminates=ctrl_discriminates)
    P(f"  C1: {C1}  (crossed inside 5 r_M {t3['crossed_frac_inside5']:.3f}; m/m_law 2: {mr2:.3f}, 5: {mr5:.3f}; Newtonian control {nc2:.3f} / {nc5:.3f})")

    P("\n=== K6 + N4  sudden baryon loss from the law at rest (point mass; M_b -> 1 - f at t = 0)")
    # K6: per-shell co-moving energy conserved before the first crossing (small dt)
    rL, dmL = law_ic(); fK = 0.5
    rK = rL.copy(); vK = np.zeros(NSH); MbK = 1 - fK
    _, oK = sph_accel(rK, dmL, MbK, True); Etf_, Eq_init = shell_energies(rK, vK, dmL, MbK, oK)
    aK, oK = sph_accel(rK, dmL, MbK, True); dtK = 5e-4; tK = 0.0; maxrel = 0.0; ncheck = 0
    while tK < 200.0:
        vK += 0.5 * dtK * aK; rK += dtK * vK
        low = rK < RMIN; rK[low] = 2 * RMIN - rK[low]; vK[low] = -vK[low]
        aK, oK = sph_accel(rK, dmL, MbK, True); vK += 0.5 * dtK * aK; tK += dtK
        if np.any(np.diff(rK) <= 0) or np.any(low): break               # rank = index while single stream
        if int(round(tK / dtK)) % 2000 == 0:
            _, Eq_now = shell_energies(rK, vK, dmL, MbK, oK)
            maxrel = max(maxrel, float(np.max(np.abs(Eq_now - Eq_init) / (MbK / rL)))); ncheck += 1
            guard()
    RES["K6"] = dict(t_first_cross_or_stop=tK, max_rel_dEq=maxrel, n_checks=ncheck)
    check("K6 single-stream per-shell E_q conserved to <= 1e-6 before the first crossing (f = 0.5)", maxrel <= 1e-6 and ncheck >= 3,
          f"max rel {maxrel:.1e} over {ncheck} checks up to t {tK:.2f}")
    n4 = {}
    for f in (0.5, 0.6, 0.7, 0.8, 0.9):
        o = sudden_loss(f)
        unb0 = o["Eq0"] > 0; esc = (o["r"] > 10 * R0) & (o["v"] > 0)
        outb = (o["r"] > R0) & (o["v"] > 0) & (o["Eq"] > 0)                 # report only (post hoc, no class weight): unbound and leaving
        xs = u_law(o["r0"]); fc = fcrit_x(xs)
        pred_unb = f > fc
        cr = o["crossed"]
        everq = np.isfinite(o["t_q"]); evertf = np.isfinite(o["t_tf"])
        d = dict(unbound_t0_Eq=float(unb0.mean()), unbound_t0_Etf=float((o["Etf0"] > 0).mean()), pred_unbound_fcrit=float(pred_unb.mean()),
                 agree_fcrit=float(np.mean(pred_unb == unb0)), escaped=float(esc.mean()), escaped_given_unbound_t0=float(esc[unb0].mean()) if unb0.any() else None,
                 escaped_given_bound_t0=float(esc[~unb0].mean()) if (~unb0).any() else None, crossed=float(cr.mean()),
                 C2b_Eq=float(np.mean(o["t_cross"][everq] < o["t_q"][everq])) if everq.any() else None,
                 C2b_Etf=float(np.mean(o["t_cross"][evertf] < o["t_tf"][evertf])) if evertf.any() else None,
                 C2b_ESC=float(np.mean(cr[esc])) if esc.any() else None, first_cross=float(o["first_cross"]), dE_rel=o["dE_rel"],
                 outbound_unbound_end=float(outb.mean()), bound_end_Eq_le_0=float(np.mean(o["Eq"] <= 0)))
        n4[f"{f}"] = d
        P(f"  f {f}: unbound at t=0+ E_q {d['unbound_t0_Eq']:.3f} (f_crit closed form predicts {d['pred_unbound_fcrit']:.3f}, agree {d['agree_fcrit']:.3f}), "
          f"E_tf {d['unbound_t0_Etf']:.3f}; escaped {d['escaped']:.3f} (of t0-unbound {d['escaped_given_unbound_t0']}, of t0-bound {d['escaped_given_bound_t0']}); "
          f"crossed {d['crossed']:.3f}; C2b E_q/E_tf/ESC {d['C2b_Eq']}/{d['C2b_Etf']}/{d['C2b_ESC']}; dE/E {d['dE_rel']:.1e}; "
          f"[report] outbound unbound at end {d['outbound_unbound_end']:.3f}, E_q <= 0 at end {d['bound_end_Eq_le_0']:.3f}")
    RES["N4"] = n4
    mx = max(v_["dE_rel"] for v_ in n4.values())
    check("K5d energy conservation with crossings (N4 sudden-loss runs) max |dE/E| <= 1e-3", mx <= 1e-3, f"{mx:.1e}")

# ============================================================================================ N5 consequences + grading
GK = 4.30091e-6; KPCM = 3.0857e19; GYR = 0.97779          # kpc (km/s)^2 / Msun ; kpc/(km/s) in Gyr
FOOT = {"canonical": 9.3603e-11 * KPCM / 1e6, "alt": 1.1312e-10 * KPCM / 1e6}
LSTARS = [0.024, 0.100, 0.300, 1.000]
def plummer(M, a): return (lambda r: M * r ** 3 / (r * r + a * a) ** 1.5, lambda r: 3 * M * a * a * r * r / (r * r + a * a) ** 2.5)
def hernquist(M, a): return (lambda r: M * r * r / (r + a) ** 2, lambda r: 2 * M * a * r / (r + a) ** 3)
def expsph(M, R): return (lambda r: M * (1 - (1 + r / R) * math.exp(-r / R)), lambda r: M * (r / R) * math.exp(-r / R) / R)
def beta23(Mnorm, rnorm, rc, rtr):
    Kn = Mnorm / (rnorm / rc - math.atan(rnorm / rc))
    return (lambda r: Kn * ((min(r, rtr) / rc) - math.atan(min(r, rtr) / rc)), lambda r: Kn * (r / rc) ** 2 / (1 + (r / rc) ** 2) / rc if r < rtr else 0.0)
def combo(parts): return (lambda r: sum(p[0](r) for p in parts), lambda r: sum(p[1](r) for p in parts))
def systems():
    S = []
    for nm, Ms, Re in (("UFD-c", 5e3, 0.030), ("UFD-e", 3e4, 0.240), ("Draco-like", 5e5, 0.220), ("Fornax-like", 4e7, 0.710)):
        S.append(dict(name=nm, cls="UFDs" if nm.startswith("UFD") else "classical dSphs", prof=plummer(Ms, Re), r_obs=1.305 * Re, collapsed=True))
    S.append(dict(name="SPARC-dwarf", cls="SPARC rotators", prof=combo([expsph(2.6e7, 0.6), expsph(3.66e8, 2.0)]), r_obs=5.0, collapsed=True))
    S.append(dict(name="MW-like", cls="MW-like", prof=hernquist(6e10, 2.5), r_obs=8.0, collapsed=True))
    g = beta23(1e14, 1200.0, 150.0, 2400.0); m = beta23(1e13, 1200.0, 150.0, 2400.0); mt = m[0](2400.0); sc = 1e13 / mt
    S.append(dict(name="cluster-core", cls="cluster cores", prof=combo([g, hernquist(1.5e12, 30.0), (lambda r: sc * m[0](r), lambda r: sc * m[1](r))]),
                  r_obs=500.0, collapsed=True))
    for r_ in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "tidal_dwarfs", "lelli2015_tdg.csv"))):
        Mbar = float(r_["M_bar_1e8"]) * 1e8; Ro = float(r_["R_out_kpc"]); age = float(r_["tmerg_over_torb"]) * float(r_["t_orb_Gyr"])
        S.append(dict(name=r_["object"].replace(" ", ""), cls="tidal dwarfs", prof=(lambda r, M=Mbar, R=Ro: M * min(1.0, (r / R) ** 2), lambda r, M=Mbar, R=Ro: (2 * M * r / R ** 2) if r < R else 0.0),
                      r_obs=Ro, collapsed=False, age=age))
    for nm, Ms, Re in (("NGC1052-DF2", 2.0e8, 2.0), ("NGC1052-DF4", 1.5e8, 1.6)):
        S.append(dict(name=nm, cls="DF2/DF4", prof=plummer(Ms, Re), r_obs=1.305 * Re, collapsed=False))
    return S
OBS = {"UFDs": "EXCESS", "classical dSphs": "EXCESS", "SPARC rotators": "ON LAW", "MW-like": "ON LAW", "cluster cores": "EXCESS",
       "tidal dwarfs": "BELOW", "DF2/DF4": "BELOW"}
CLASSES = list(OBS.keys())
VREL = 100.0                                             # km/s, declared lower bound for debris moving through a host's settled medium

PHI_CACHE = {}
def phi_grid(s):
    """baryonic potential on a grid r in [1e-3 r_half, r_half] (footing-independent), Phi(r) = -int_r^inf g_N dr"""
    if s["name"] in PHI_CACHE: return PHI_CACHE[s["name"]]
    Mf = s["prof"][0]; r = s["r_obs"]; gN = lambda rr: GK * Mf(rr) / rr ** 2
    big = 1e3 * max(r, 3000.0)
    seg = np.geomspace(r, big, 241)                       # log segments: robust across profile kinks (truncations)
    phi_h = -(sum(quad(gN, a_, b_, limit=100)[0] for a_, b_ in zip(seg[:-1], seg[1:])) + GK * Mf(big) / big)
    rr = np.geomspace(1e-3 * r, r, 121); ph = np.empty_like(rr); ph[-1] = phi_h
    for i in range(len(rr) - 2, -1, -1):
        ph[i] = ph[i + 1] - quad(gN, rr[i], rr[i + 1], limit=100)[0]
    PHI_CACHE[s["name"]] = (rr, ph); return rr, ph

def sys_numbers(s, a0k):
    Mf, dMf = s["prof"]; r = s["r_obs"]
    gN = lambda rr: GK * Mf(rr) / rr ** 2
    uf = lambda rr: (-gN(rr) + math.sqrt(gN(rr) ** 2 + 4 * gN(rr) * a0k)) / 2
    def rho_ph(rr):
        h = 1e-4 * rr
        return ((rr + h) ** 2 * uf(rr + h) - (rr - h) ** 2 * uf(rr - h)) / (2 * h) / (4 * math.pi * GK * rr * rr)
    rho_b = dMf(r) / (4 * math.pi * r * r)
    u = uf(r); g = gN(r)
    om2 = 4 * math.pi * GK * rho_b + (2 * g / r) * a0k / (a0k - u)
    Tc = 2 * math.pi / math.sqrt(om2) * GYR
    rr, ph = phi_grid(s)
    vin_g = np.sqrt(2 * np.abs(ph)); rho_g = np.array([rho_ph(x) for x in rr])
    vin = float(vin_g[-1]); rph = float(rho_g[-1])
    out = dict(r_half_kpc=r, M_b_in=Mf(r), gN_over_a0=g / a0k, x_u_over_a0=u / a0k, rho_ph_Msun_kpc3=rph, T_c_Gyr=Tc, v_in_kms=vin,
               fcrit_pointmass=float(fcrit_x(u / a0k)))
    for Ls in LSTARS:
        cs_g = np.sqrt(2 * math.pi * GK * Ls ** 2 * np.maximum(rho_g, 1e-300))
        mach_g = vin_g / cs_g
        out[f"Mach_L{int(Ls * 1000)}pc"] = float(mach_g[-1])
        sub = rr[mach_g < 1]
        out[f"r_sub_L{int(Ls * 1000)}pc_kpc"] = float(sub.max()) if sub.size else 0.0
    return out

def grade(pred):
    match = {c: (pred[c] == OBS[c]) for c in CLASSES}
    n = sum(match.values())
    if n == 7: cls = "ALIGNS"
    elif n >= 5 and match["SPARC rotators"] and match["MW-like"]: cls = "PARTIAL"
    else: cls = "MISALIGNS"
    return cls, n, match

def predicted_sides(rows, Ls_key, reading, vrel):
    side = {}
    for c in CLASSES:
        sides = set()
        for s in rows:
            if s["cls"] != c: continue
            present = s["collapsed"] or (s["v_in_kms"] >= vrel)
            if not present: sides.add("BELOW"); continue
            if reading == "derived":
                sides.add("ON LAW")
            elif reading == "HSC":
                ms = s["N_osc"] >= 1 and s[f"Mach_L{Ls_key}pc"] >= 1
                sides.add("EXCESS" if ms else "ON LAW")
            elif reading == "tooth":                      # hand-made: excess iff pressure-supported and medium present
                sides.add("ON LAW" if c in ("SPARC rotators", "MW-like") else "EXCESS")
        side[c] = sides.pop() if len(sides) == 1 else "MIXED"
    return side

AGE = {"UFDs": 13.0, "classical dSphs": 12.0, "SPARC rotators": 10.0, "MW-like": 10.0, "cluster cores": 6.0, "DF2/DF4": 9.0}
P("\n=== N5  consequences per class (record representative systems: CFG932 rows, Lelli+15 TDGs, CFG933 DF2/DF4); both footings")
P("    declared nominal ages (Gyr): " + ", ".join(f"{k} {v}" for k, v in AGE.items()) + "; TDGs: tmerg/t_orb x t_orb from the table."
  "  The crossing test needs only age >= T_c, so T_c is printed.")
N5 = {}
SYS = systems()
for fk, a0k in FOOT.items():
    rows = []
    for s in SYS:
        nb = sys_numbers(s, a0k); row = dict(name=s["name"], cls=s["cls"], collapsed=s["collapsed"], **nb)
        age = s.get("age", AGE.get(s["cls"], 10.0)); row["age_Gyr"] = age; row["N_osc"] = age / nb["T_c_Gyr"]
        rows.append(row)
    N5[fk] = rows
    P(f"\n  [{fk}] a0 = {a0k:.1f} (km/s)^2/kpc")
    P("  system          r_half   g_N/a0    T_c[Gyr]  N_osc   v_in   Mach@24pc  Mach@1kpc  r_sub@24pc  r_sub@1kpc  f_crit(r_half)")
    for r_ in rows:
        P(f"  {r_['name']:15s} {r_['r_half_kpc']:7.3f} {r_['gN_over_a0']:9.2e} {r_['T_c_Gyr']:9.3e} {r_['N_osc']:7.1f} {r_['v_in_kms']:6.1f} "
          f"{r_['Mach_L24pc']:9.2f} {r_['Mach_L1000pc']:9.3f}  {r_['r_sub_L24pc_kpc']:9.4f}  {r_['r_sub_L1000pc_kpc']:9.4f}  {r_['fcrit_pointmass']:.3f}")
RES["N5"] = N5

ALIGN = {}
readings = ("tooth",) if MODE == "gradetooth" else ("HSC", "derived")
for reading in readings:
    ALIGN[reading] = {}
    for fk in FOOT:
        for Ls in LSTARS:
            key = int(Ls * 1000)
            for vrel in ((VREL, VREL / 2) if reading != "tooth" else (VREL,)):
                pred = predicted_sides(N5[fk], key, reading, vrel)
                cls, n, match = grade(pred)
                ALIGN[reading][f"{fk}|L{key}pc|vrel{vrel:.0f}"] = dict(class_=cls, n_match=n, pred=pred, match=match)
    classes = sorted(set(v["class_"] for v in ALIGN[reading].values()))
    overall = classes[0] if len(classes) == 1 else "L*-DEPENDENT (" + ", ".join(classes) + ")"
    ALIGN[reading]["overall"] = overall
    P(f"\n  alignment [{reading}] overall: {overall}")
    for k_, v_ in ALIGN[reading].items():
        if k_ == "overall": continue
        P(f"    {k_:28s} {v_['class_']:10s} {v_['n_match']}/7   " + "; ".join(f"{c}: {v_['pred'][c]}" for c in CLASSES))
RES["alignment"] = ALIGN

if MODE == "gradetooth":
    bite = ALIGN["tooth"]["overall"] in ("ALIGNS", "PARTIAL")
    P(f"M5 grading tooth: hand-made criterion -> {ALIGN['tooth']['overall']} -> {'BITES (grader can return a non-MISALIGNS class)' if bite else 'DOES NOT BITE'}")
    finish(1 if bite else 0)

# ============================================================================================ S4 class
P("\n=== S4 class")
P("  C3 (analytic, DERIVATION.md section 3): with S3 as written (d_t P = -j, j the TOTAL current), P is a functional of the total density in 1-D and"
  " spherical symmetry, so every element feels -g_Nb + R(K|P|) P_hat - gamma grad rho_c whatever its stream: no stream-dependent coupling.")
C1 = RES["C1"]["class_"]; t3 = RES["N3"]["tether"]
c2a = {nm: t3[f"C2a_{nm}"] for nm in ("E_tf", "E_q", "ESC")}
c2a_frozen = c2a["E_tf"] >= 0.9
# frozen NOT DERIVABLE operational clause (printed, labelled ILL-POSED by A1)
frozen_clause = None
if t3["n_ever_unbound_E_tf"] > 0:
    frozen_clause = 1 - t3["escaped_frac"] * NSH / max(t3["n_ever_unbound_E_tf"], 1)
P(f"  C1 = {C1}; C2(a) crossing => E_tf > 0: {c2a['E_tf']:.3f} (E_q {c2a['E_q']:.3f}, ESC {c2a['ESC']:.3f}); frozen threshold 0.9 -> {'holds' if c2a_frozen else 'fails'}")
P(f"  frozen NOT-DERIVABLE clause (fraction of ever-E_tf>0 mass still in the box ~ {frozen_clause}) -> ILL-POSED (A1): moving elements of a tethered"
  " medium have E_tf > 0 by the flat-potential identity")
P(f"  A1 replacement: no >= 10% subset evolves under the tether-off force law (C3 analytic; force identity {t3['force_identity_max_abs']:.1e} a0)")
if C1 == "UNTETHERED" and c2a_frozen: S4 = "S4 DERIVED"
elif C1 == "TETHERED AFTER CROSSING": S4 = "S4 NOT DERIVABLE"
else: S4 = "UNDETERMINED (" + C1 + ")"
RES["S4_class"] = S4; RES["C2a"] = c2a; RES["frozen_clause_value"] = frozen_clause
P(f"  -> {S4}")
P(f"  alignment: H-SC {ALIGN['HSC']['overall']}; derived reading {ALIGN['derived']['overall']}")

nK = len(KOK); nP = sum(KOK.values())
RES["K"] = KOK; RES["K_pass"] = f"{nP}/{nK}"
P(f"\nK: {nP}/{nK} PASS")
finish(0 if nP == nK else 1)

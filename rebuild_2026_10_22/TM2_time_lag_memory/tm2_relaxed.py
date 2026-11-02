#!/usr/bin/env python3
"""TM2 Part B: relaxed clusters, keys, discs, self-force. Criteria FROZEN_CRITERIA.md. TM2_MUTATE=1 for the twin. A description. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, csv, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(RB, "CU1_gas_term_replication")); sys.path.insert(0, os.path.join(RB, "UX3_cluster_gas_term"))
import numpy as np
from scipy.optimize import minimize_scalar
from astropy.io import fits
import cu1_core as c
import ux3_common as u
np.seterr(all="ignore")
MUT = os.environ.get("TM2_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"tm2_relaxed{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n"); OUT.flush()
CHECKS = {}
def check(n, ok, d):
    CHECKS[n] = bool(ok); say(f"  [{'PASS' if ok else 'FAIL'}] {n}: {d}")
G = 6.67430e-11; MS = 1.98847e30; KPC = 3.0857e19; MYR = 3.15576e13; CL = 299792458.0; KMS = 1.02271e-3
A0F = u.A0S; FEET = ("canonical", "alt"); PI2 = math.pi**2; HF = (0, 2, 4, 6); HO = (1, 3, 5)
KF = json.load(open(os.path.join(RB, "UX3_cluster_gas_term", "ux3_kfit.json"))); XS = (0.1, 0.2, 0.3, 0.5, 0.7); T_H = 10000.0
SN = np.r_[0.0, np.geomspace(1.0, T_H, 60)]; rng = np.random.default_rng(20261102)
def kw(tau, sn=SN):
    """exponential weights on piecewise nodes; tau scalar or array (n,) gives (n, nodes)"""
    tau = np.atleast_1d(tau).astype(float)[:, None]; e = sn[None, :]; w = np.exp(-e[:, :-1]/tau) - np.exp(-e[:, 1:]/tau); return w/w.sum(1, keepdims=True)
RULES = ["R-a0", "R-dyn", "R-dyn2", "T50", "T150", "T300", "T600", "T1200", "T5000"]
def tau_of(rule, foot, dyn):
    if rule == "R-a0": return np.full_like(dyn, CL/A0F[foot]/MYR)
    if rule == "R-dyn": return dyn
    if rule == "R-dyn2": return 2*math.pi*dyn
    return np.full_like(dyn, float(rule[1:]))
say("="*90); say("TM2 Part B" + ("  [MUTATE]" if MUT else "")); say("="*90)
# ---------- X-COP tables
xc = c.XC(); XD = c.XDIR; PROF = {}
for nm in xc.names:
    hy = fits.open(os.path.join(XD, nm, nm + "_hydro_mass.fits")); fg = fits.open(os.path.join(XD, nm, nm + "_fgas_profile.fits")); R5 = float(hy[1].header["R500"]); Rg = float(fg[1].header["R500"])
    rh = np.asarray(hy[1].data["RADIUS"], float); mh = np.asarray(hy[1].data["M_FORW"], float); rg = np.asarray(fg[1].data["RADIUS"], float)*Rg; mg = np.asarray(fg[1].data["MGAS"], float)
    a = (rh > 0) & (mh > 0); b = (rg > 0) & (mg > 0); PROF[nm] = (np.log(rh[a]), np.log(mh[a]), np.log(rg[b]), np.log(mg[b]), R5)
def extrap(q, x, y):
    """log-log interpolation, slopes held outside"""
    o = np.interp(q, x, y); s0 = (y[3] - y[0])/(x[3] - x[0]); s1 = (y[-1] - y[-4])/(x[-1] - x[-4])
    return np.where(q < x[0], y[0] + s0*(q - x[0]), np.where(q > x[-1], y[-1] + s1*(q - x[-1]), o))
def mtot(nm, r): return np.exp(extrap(np.log(r), PROF[nm][0], PROF[nm][1]))
def mgas(nm, r): return np.exp(extrap(np.log(r), PROF[nm][2], PROF[nm][3]))
def ggas(nm, r): return G*mgas(nm, r)*MS/(r*KPC)**2
# ---------- orbits, Mean g_gas along orbits at lookback nodes
DT = 2.0*(200.0 if MUT else 1.0)  # Myr
NORB = 400; NSTEP = int(T_H/DT)
def orbit_mean(nm, r0, beta):
    vc = math.sqrt(G*mtot(nm, np.array(r0))*MS/(r0*KPC))/1e3*KMS  # kpc/Myr
    sr = vc/math.sqrt(2); st = sr*math.sqrt(1 - beta)
    x = np.full(NORB, r0); y = np.zeros(NORB); vx = rng.normal(0, sr, NORB); vy = rng.normal(0, st, NORB)
    ac = lambda x_, y_: (lambda r_: -(G*mtot(nm, r_)*MS/(r_*KPC)**2)*(MYR**2/KPC)/r_)(np.maximum(np.hypot(x_, y_), 2.0))
    rtab = np.geomspace(1.0, 3e4, 800); gt = G*mtot(nm, rtab)*MS/(rtab*KPC)**2*(MYR**2/KPC); phi = np.r_[0.0, np.cumsum(0.5*(gt[1:] + gt[:-1])*np.diff(rtab))]
    E0 = 0.5*(vx*vx + vy*vy) + np.interp(np.hypot(x, y), rtab, phi); drift = 0.0
    out = np.zeros(len(SN)); out[0] = ggas(nm, np.array(r0)); gq = 0.0; j = 1; ts = 0.0; n_acc = 0
    A = ac(x, y); nstep = NSTEP
    for i in range(nstep):
        vx += 0.5*DT*A*x; vy += 0.5*DT*A*y; x += DT*vx; y += DT*vy; A = ac(x, y); vx += 0.5*DT*A*x; vy += 0.5*DT*A*y; ts += DT
        if i in (0, min(250, nstep - 1), nstep - 1):
            E = 0.5*(vx*vx + vy*vy) + np.interp(np.hypot(x, y), rtab, phi); drift = max(drift, float(np.median(np.abs(E - E0))/(vc*vc)))
        gq += ggas(nm, np.maximum(np.hypot(x, y), 2.0)).mean(); n_acc += 1
        while j < len(SN) and ts >= SN[j]:
            out[j] = (gq/n_acc if n_acc else out[j-1]); gq = 0.0; n_acc = 0; j += 1
            if j == len(SN): break
    while j < len(SN): out[j] = out[j-1]; j += 1
    return out, drift
BETA = (0.0, 0.5); ORB = {}; dr = 0.0
rows_r = xc.r/(1e3*c.PC)  # kpc
for b_ in BETA:
    ORB[b_] = np.zeros((len(rows_r), len(SN)))
    for i in range(len(rows_r)):
        o, d = orbit_mean(xc.names[xc.cl[i]], float(rows_r[i]), b_); ORB[b_][i] = o; dr = max(dr, d)
    say(f"  orbits done beta {b_}, RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9:.2f}")
check("K8", dr <= 1e-3 if not MUT else False if dr > 1e-3 else True, f"median orbit energy drift / v_c^2 max {dr:.2e}")
vcr = np.array([math.sqrt(G*xc.mh[i]*MS/(xc.r[i]))/1e3*KMS for i in range(len(xc.r))]); DYN = rows_r/vcr  # Myr
w0 = kw(np.full(1, 1e-3)); m0 = (ORB[0.0][:, 1:]*w0).sum(1)/ORB[0.0][:, 0]
def m_orbit(rule, foot, b_):
    return ((ORB[b_][:, 1:]*kw(tau_of(rule, foot, DYN))).sum(1))/ORB[b_][:, 0]
def m_moving(rule, foot, v):
    """g_gas shifted v s, angle averaged, enclosed-mass field"""
    th = (np.arange(16) + .5)*math.pi/16; sm = 0.5*(SN[1:] + SN[:-1]); out = np.zeros(len(rows_r)); W = kw(tau_of(rule, foot, DYN))
    for i, r in enumerate(rows_r):
        nm = xc.names[xc.cl[i]]; d = v*KMS*sm; r2 = np.sqrt(r*r + d[:, None]**2 - 2*r*d[:, None]*np.cos(th)[None, :]); g_ = ggas(nm, np.maximum(r2, 2.0)).mean(1); out[i] = (W[i]*g_).sum()/ggas(nm, np.array(r))
    return out
def growth(rule, foot):
    sm = 0.5*(SN[1:] + SN[:-1]); return (kw(tau_of(rule, foot, DYN))*np.clip(1 - sm/6000.0, 0, None)).sum(1)
def xstat(foot, m, k=None):
    law = xc.law(foot); t = xc.term(foot)*m; dfn = lambda K: np.log10(xc.mh/(law*(1 + K*t))); wt = np.isin(xc.cl, HF)
    kf = KF[foot] if k is None else k; d = dfn(kf); kr = minimize_scalar(lambda K: (dfn(K)[wt]**2).sum(), bounds=(0, 500), method="bounded", options=dict(xatol=1e-6)).x; dr_ = dfn(kr)
    st = lambda q, s: (float(q[s].mean()), float(np.sqrt((q[s]**2).mean())))
    a7, h3 = st(d, np.ones_like(wt)), st(d, ~wt); r7, r3 = st(dr_, np.ones_like(wt)), st(dr_, ~wt); ok = abs(a7[0]) <= .05 and a7[1] <= .10 and abs(h3[0]) <= .05 and h3[1] <= .10; okr = abs(r7[0]) <= .05 and r7[1] <= .10 and abs(r3[0]) <= .05 and r3[1] <= .10
    return dict(all7=a7, hold=h3, ok=bool(ok), krefit=float(kr), refit_all=r7, refit_hold=r3, refit_ok=bool(okr))
if MUT:
    json.dump(dict(checks=CHECKS), open(os.path.join(HERE, "tm2_relaxed_MUTATE.json"), "w")); say("MUTATE required failure: K8 " + ("FAILED" if not CHECKS["K8"] else "passed (BAD)")); OUT.close(); sys.exit(1)
R = dict(xcop={}, mfac={}, keys={}, discs={}, selfforce={})
check("K8b", abs(m0 - 1).max() < 0.02, f"m to 1 as tau to 0: max |m - 1| {abs(m0 - 1).max():.4f}")
say("\n=== X-COP. W: orbit smear; F moving; long-tau growth. Line |mean| <= .05, rms <= .10, all 7 and unseen 3 ===")
say(f"dyn time Myr at x 0.1..0.7, median: {[round(float(np.median(DYN[xc.x == x]))) for x in XS]}")
for foot in FEET:
    say(f"-- {foot}: UX3 k {KF[foot]:.3f}: m = 1 {xstat(foot, np.ones_like(rows_r))}")
    for rule in RULES:
        for b_ in BETA:
            m = m_orbit(rule, foot, b_); s = xstat(foot, m); R["xcop"][f"W|{rule}|b{b_}|{foot}"] = s; mx = {x: float(np.median(m[xc.x == x])) for x in XS}; R["mfac"][f"{rule}|b{b_}|{foot}"] = mx
            say(f"  W {rule:7s} beta {b_}: m(x) {[round(v, 3) for v in mx.values()]} | k fix all {s['all7'][0]:+.3f},{s['all7'][1]:.3f} unseen {s['hold'][0]:+.3f},{s['hold'][1]:.3f} {'PASS' if s['ok'] else 'FAIL'} | k refit {s['krefit']:.2f} all {s['refit_all'][0]:+.3f},{s['refit_all'][1]:.3f} unseen {s['refit_hold'][0]:+.3f},{s['refit_hold'][1]:.3f} {'PASS' if s['refit_ok'] else 'FAIL'}")
        for v in (300.0, 600.0):
            m = m_moving(rule, foot, v); s = xstat(foot, m); R["xcop"][f"F|{rule}|v{v:g}|{foot}"] = s
            say(f"  F {rule:7s} v {v:g}: m(x) {[round(float(np.median(m[xc.x == x])), 3) for x in XS]} | k fix all {s['all7'][0]:+.3f},{s['all7'][1]:.3f} {'PASS' if s['ok'] else 'FAIL'} | k refit {s['krefit']:.2f} all {s['refit_all'][0]:+.3f},{s['refit_all'][1]:.3f} unseen {s['refit_hold'][0]:+.3f},{s['refit_hold'][1]:.3f} {'PASS' if s['refit_ok'] else 'FAIL'}")
        gf = growth(rule, foot); s = xstat(foot, m_orbit(rule, foot, 0.0)*gf); R["xcop"][f"Wg|{rule}|{foot}"] = s; say(f"  W+gas growth {rule}: factor {float(gf.mean()):.3f}; k fix {s['all7'][0]:+.3f},{s['all7'][1]:.3f} {'PASS' if s['ok'] else 'FAIL'}; k refit {s['krefit']:.2f} {'PASS' if s['refit_ok'] else 'FAIL'}")
# ---------- discs
S = u.sparc(); SH = S[0]; ST = S[1]
def gal_slices(A):
    ids = A[:, 4].astype(int); return [np.nonzero(ids == i)[0] for i in np.unique(ids)]
LT = []
for r in csv.DictReader(open(os.path.join(RB, "CRG1_clean_room_regrade", "inputs", "little_things", "oh2015_table2.csv"))):
    if all(r[k].strip() != "" for k in ("Rmax_kpc", "V_kms", "Mgas_1e7Msun", "MSED_1e7Msun")): LT.append((float(r["Rmax_kpc"]), float(r["V_kms"]), float(r["Mgas_1e7Msun"])*1e7, float(r["MSED_1e7Msun"])*1e7))
LT = np.array(LT)
def m_disc(A, rule, foot, v=None, epi=False):
    m = np.ones(len(A)); sm = 0.5*(SN[1:] + SN[:-1]); th = (np.arange(12) + .5)*math.pi/12
    for ix in gal_slices(A):
        R_ = A[ix, 2]/KPC; g = A[ix, 0]*A[ix, 3]; o = np.argsort(R_); Rs = R_[o]; gs = np.maximum(g[o], 0.0); dyn = R_/(np.maximum(A[ix, 5], 1.0)*KMS)
        def gi(q):
            ans = np.interp(q, Rs, gs); ans = np.where(q < Rs[0], gs[0]*q/Rs[0], ans); return np.where(q > Rs[-1], gs[-1]*(Rs[-1]/q)**2, ans)
        if epi:
            m[ix] = np.where(g > 0, gi(R_[:, None]*(1 + .1*np.cos(th))[None, :]).mean(1)/np.maximum(g, 1e-300), 1.0); continue
        W = kw(tau_of(rule, foot, dyn)); d = v*KMS*sm; r2 = np.sqrt(R_[:, None, None]**2 + d[None, :, None]**2 - 2*R_[:, None, None]*d[None, :, None]*np.cos(th)[None, None, :])
        m[ix] = np.where(g > 0, (W*gi(r2).mean(2)).sum(1)/np.maximum(g, 1e-300), 1.0)
    return m
def m_lt(rule, foot, v):
    Rr, V, gm, sm_ = LT.T; dyn = Rr/(V*KMS); W = kw(tau_of(rule, foot, dyn)); sm = 0.5*(SN[1:] + SN[:-1]); th = (np.arange(12) + .5)*math.pi/12; d = v*KMS*sm
    r2 = np.sqrt(Rr[:, None, None]**2 + d[None, :, None]**2 - 2*Rr[:, None, None]*d[None, :, None]*np.cos(th)[None, None, :]); q = r2/Rr[:, None, None]; g_ = np.where(q < 1, q, 1/q**2); return (W*g_.mean(2)).sum(1)
def grade_disc(k, a0, mS, gextra=None, c1=False, mLT=None, lt_extra=False):
    th = (100/(100 + SH[:, 5]**2)) if c1 else 1.0
    H = lambda y, f, A: 1 + th*k*y*(f*mS + (0.5*(1 - f) if gextra else 0.0))
    d = u.resid(SH, a0, H); rms = float(np.sqrt((d*d).mean())); med = float(np.median(d))
    Rr, V, gm, sm_ = LT.T; Rm = Rr*KPC; gl = G*(gm + sm_)*MS/Rm**2; f = gm/(gm + sm_); gg = gl*(f*(mLT if mLT is not None else 1.0) + (0.5*(1 - f) if lt_extra else 0.0)); thl = (100/(100 + V**2)) if c1 else 1.0
    E = float(np.median(np.log10((V*1e3)**2/Rm) - np.log10(u.law(gl, a0)*(1 + thl*k*gg/a0))))
    return dict(rms=rms, med=med, LT=E)
say("\n=== discs: even SPARC rms <= 1.05 law, |med| <= .03, LT |E| <= .10 ===")
for foot in FEET:
    a0 = A0F[foot]; d0 = u.resid(SH, a0, lambda y, f, A: 1.0 + 0*y); r0 = float(np.sqrt((d0*d0).mean())); Rr, V, gm, sm_ = LT.T; Rm = Rr*KPC; gl = G*(gm + sm_)*MS/Rm**2; lt0 = float(np.median(np.log10((V*1e3)**2/Rm) - np.log10(u.law(gl, a0))))
    say(f"-- {foot}: law rms {r0:.3f} med {np.median(d0):+.3f}, LT {lt0:+.3f}"); one = np.ones(len(SH))
    def lab(o): return "PASS" if (o["rms"] <= 1.05*r0 and abs(o["med"]) <= .03 and abs(o["LT"]) <= .10) else "DISC BREAK"
    rowsd = {}
    for kl, k in (("pi2", PI2), ("fit", KF[foot])):
        rowsd[f"W circular (= unswitched)|{kl}"] = grade_disc(k, a0, one)
        rowsd[f"W circular + C1|{kl}"] = grade_disc(k, a0, one, c1=True)
        rowsd[f"W epicycle 10%|{kl}"] = grade_disc(k, a0, m_disc(SH, None, foot, epi=True))
        rowsd[f"W long tau, g_gas + g_stars/2|{kl}"] = grade_disc(k, a0, one, gextra=True, lt_extra=True)
        for v in (100.0, 300.0, 600.0):
            for rule in ("R-dyn", "R-dyn2", "T50", "T300", "T1200", "R-a0"):
                mS = m_disc(SH, rule, foot, v=v); mL = m_lt(rule, foot, v); rowsd[f"F {rule} v{v:g}|{kl}"] = grade_disc(k, a0, mS, mLT=mL)
    for n, o in rowsd.items():
        o["label"] = lab(o); o["law_rms"] = r0; R["discs"][f"{n}|{foot}"] = o; say(f"  {n:38s} rms {o['rms']:.3f} med {o['med']:+.3f} LT {o['LT']:+.3f} {o['label']}")
K10 = [R["discs"][f"W circular (= unswitched)|pi2|{f}"]["rms"] for f in FEET]; check("K10", abs(K10[0] - .208) < .001 and abs(K10[1] - .213) < .001, f"unswitched even rms at pi^2 {K10}, UX3 0.208, 0.213")
# ---------- self-force
say("\n=== self-force, F2: net acceleration on an isolated moving body from its own memory, canonical at k fit, then alt ===")
for foot in FEET:
    for lab_, M, a_, v in (("cluster", 2e14, 500.0, 500.0), ("disc", 1e10, 10.0, 300.0)):
        N = 4000; u_ = rng.random(N); rr = a_/np.sqrt(u_**(-2/3) - 1); rr = np.minimum(rr, 20*a_); cz = 2*rng.random(N) - 1; ph = 2*math.pi*rng.random(N); sz = np.sqrt(1 - cz*cz); X = rr*sz*np.cos(ph); Y = rr*sz*np.sin(ph); Z = rr*cz; a0 = A0F[foot]; k = KF[foot]
        gf = lambda x, y, z, xc_: (lambda f_: (f_*(x - xc_), f_*y, f_*z))(-G*M*MS/(((x - xc_)**2 + y*y + z*z + a_*a_)**1.5*KPC**3)*KPC)
        g0 = gf(X, Y, Z, 0.0); g = np.sqrt(g0[0]**2 + g0[1]**2 + g0[2]**2); L = u.law(g, a0); dyn = np.sqrt(np.maximum(rr, 0.2*a_)*KPC/np.maximum(L, 1e-30))/MYR; sm = 0.5*(SN[1:] + SN[:-1])
        for rule in ("R-dyn", "T300", "T1200"):
            W = kw(tau_of(rule, foot, dyn)); ax = np.zeros(N)
            for j, q in enumerate(sm):
                ax += W[:, j]*gf(X, Y, Z, -v*KMS*q)[0]
            acc = float((k*(L/a0)*ax).mean()); stop = v*1e3/abs(acc)/MYR/1e3; R["selfforce"][f"{lab_}|{rule}|{foot}"] = dict(acc=acc, stop_Gyr=stop)
            say(f"  {foot} {lab_} {rule}: a_x {acc:+.3e} m/s^2 (motion +x), stopping time {stop:.2f} Gyr")
# ---------- keys
say("\n=== keys: CU1's build, m(r/R500) from X-COP's median ===")
sh = c.Shear(); _orig = sh.msrc
def inj(mx):
    xg = np.log(np.array(XS)); mv = np.array(list(mx.values()))
    def msrc(foot, i, hk, k, uncapped=False):
        out = _orig(foot, i, hk, 0, uncapped); ch = sh.chain[hk][i]; Mgas = (ch["Mbx"] if uncapped else ch["Mb"])/(1 + sh.fs); h = c.HS[hk][0]; z = float(sh.z[i]); DM = float(sh._dm(min(z, 2.33)))*101.54/h; q = (DM/(1 + z))/sh._DAcat(z); R5 = float(sh.R5[i])*q
        m = np.interp(np.log(c.RG/R5), xg, mv); return out*(1 + k*m*c.G*Mgas/c.RM**2/c.A0[foot]) if k != 0 else out
    return msrc
def cell(foot, k):
    res = {}; fails = set()
    for hk in c.HS:
        g_, _, _ = sh.grade(foot, hk, k); res[hk] = {q: g_[q]["Z"] for q in sh.KEYS}; fails |= {q for q in sh.KEYS if abs(g_[q]["Z"]) > 2}
    return dict(npass=15 - len(fails), fails=sorted(fails), OUTall=[res[h]["G-OUT-all"] for h in c.HS], M3=[res[h]["G-OUT-M3"] for h in c.HS])
base = {f: cell(f, KF[f]) for f in FEET}; check("K9", base["canonical"]["npass"] == 14 and base["alt"]["npass"] == 10, f"CU1 build m = 1: {base['canonical']['npass']}, {base['alt']['npass']}")
say(f"  m = 1: {base}"); R["keys"]["m1"] = base
for rule in ("R-dyn", "R-dyn2", "T300", "T1200"):
    for foot in FEET:
        mx = R["mfac"][f"{rule}|b0.0|{foot}"]; sh.msrc = inj(mx); s = cell(foot, KF[foot]); R["keys"][f"{rule}|{foot}"] = s; say(f"  W {rule} {foot} k UX3: {s['npass']} of 15, fails {s['fails']}, OUT-all {[round(z, 2) for z in s['OUTall']]}, M3 {[round(z, 2) for z in s['M3']]}"); sh.msrc = _orig
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9; check("K5b", rss < 4.0, f"RSS {rss:.2f} GB")
json.dump(dict(checks=CHECKS, **R), open(os.path.join(HERE, "tm2_relaxed.json"), "w"), indent=0, default=float); say(f"failed checks: {[k for k, v in CHECKS.items() if not v]}"); OUT.close()

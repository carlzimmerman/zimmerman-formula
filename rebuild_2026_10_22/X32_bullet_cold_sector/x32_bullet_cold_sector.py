#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
X32_bullet_cold_sector -- the Bullet Cluster: does a cold sector at the X26 sheet's sound speed end with the gas or with
the galaxies, as a perfect fluid (F) or as a collisionless component with sigma_1D = c_s (C)?

Criteria: FROZEN_CRITERIA.md (committed alone, before this script).  kappa = 1/2 FITTED.  Footings canonical 9.3603e-11 /
alt 1.1312e-10 m/s^2, never pooled.  The cold sector is gravitating field mass, never a particle.  Nothing is fitted.
Small job: one thread, numpy, < 1 GB.  MUTATE twin: X32_MUTATE=1 (m1 gas x2 in step 0 -> K0b; m2 plate scale -> K0c;
m3 well force sign -> K2), outputs *_MUTATE.*, exit 1 required.
"""
import os, sys, json, math, time, resource, hashlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq, fsolve
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
MUT = os.environ.get("X32_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"x32_bullet_cold_sector{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n"); OUT.flush()
CHECKS = {}
def check(name, ok, detail, tol=""):
    CHECKS[name] = bool(ok); say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}" + (f"  (tol {tol})" if tol else ""))
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1e9 if sys.platform == "darwin" else 1e6)
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
RES = {"lane": "X32_bullet_cold_sector", "criteria": "FROZEN_CRITERIA.md", "mutate": MUT}

# ============================================================== constants (h57 / hunt_lib values, for the step-0 reproduction)
G = 6.674e-11; KPC = 3.0857e19; MSUN = 1.989e30
MP, KEV = 1.67262192e-27, 1.602176634e-16
A0F = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
A0_H57 = {"canonical": 9.36e-11, "alt": 1.13e-10}
FEET = ("canonical", "alt")
SIG_CRIT = 1.827e9; Z_BOX = 18000.0
GAS = [(2.0e14, 565.0, 190.0, 90.0), (1.5e13, 505.0, 525.0, 120.0), (1.5e13, 90.0, 670.0, 170.0), (-6.8e12, 70.0, 670.0, 170.0)]
GAL = [(1.196e13, 470.0, 0.0, 0.0), (4.0e12, 245.0, 820.0, 220.0)]
ALLB = GAS + GAL
BCG1 = np.array([0.0, 0.0]); BCG3 = np.array([820.0, 220.0]); GASM = np.array([190.0, 90.0]); GASB = np.array([670.0, 170.0])
OBS300 = {"BCG1": 3.5e14, "BCG3": 2.3e14}
D_AX = float(np.hypot(*(BCG3 - BCG1))); UAX = (BCG3 - BCG1)/D_AX                      # 849 kpc model-frame axis
V_BULK, V_SHOCK = 2700.0, 4740.0
M_MAIN, M_SUB, M_SUB_FB = 1.5e15, 1.5e14, 2.3e14
B_REP = 150.0                                                                          # PROVISIONAL, reported only
OMEGA_C_B = 5.364
KBAR = {"main BCG": (0.36, 0.06), "main plasma": (0.05, 0.06), "sub BCG": (0.20, 0.05), "sub plasma": (0.02, 0.06)}
SIG_O3 = 0.15                                                                          # PROVISIONAL
SIG_DELTA = math.sqrt((1/8)**2 + 0.15**2)

# ============================================================== kernels and the field
def nut_routeA(y):
    y = np.maximum(np.asarray(y, float), 1e-300); return 1.0/np.expm1(np.sqrt(y))
def nut_v3(y):
    y = np.maximum(np.asarray(y, float), 1e-300); return 0.5*(np.sqrt(1.0 + 4.0/y) - 1.0)
def nut_deep(y): return np.asarray(y, float)**-0.5

class Cold:
    """spherical tabulated component: centre (x, y) kpc, mass A Msun, unit-mass tables r [kpc], m(<r), Sigma(R) [1/kpc^2]"""
    def __init__(self, x, y, A, tab):
        self.x, self.y, self.A, self.t = float(x), float(y), float(A), tab
    def menc(self, r):
        return self.A*np.interp(r, self.t["r"], self.t["m"], left=0.0, right=1.0)
    def sigma(self, R):
        return self.A*np.interp(R, self.t["R"], self.t["S"], left=self.t["S"][0], right=0.0)

def gN(X, Y, Z, plum, colds=(), gext=0.0):
    gx = np.zeros(np.shape(X)); gy = np.zeros(np.shape(X)); gz = np.zeros(np.shape(X))
    for M, a, xc, yc in plum:
        dx = X - xc; dy = Y - yc; dz = Z
        den = (dx*dx + dy*dy + dz*dz + a*a)**1.5
        f = -G*M*MSUN/(den*KPC**3)*KPC
        gx += f*dx; gy += f*dy; gz += f*dz
    for c in colds:
        dx = X - c.x; dy = Y - c.y; dz = Z
        r = np.sqrt(dx*dx + dy*dy + dz*dz); r = np.maximum(r, 1e-3)
        f = -G*c.menc(r)*MSUN/((r*KPC)**2)/r
        gx += f*dx; gy += f*dy; gz += f*dz
    gy = gy + gext
    return gx, gy, gz

def zgrid(Z, n_in=500, n_out=500, z_in=1500.0):
    a = np.linspace(0.0, z_in, n_in + 1); b = np.geomspace(z_in, Z, n_out + 1)[1:]; return np.concatenate([a, b])
ZS_SURF = zgrid(Z_BOX)

def Mph_cyl(x0, y0, R, plum, a0, nut, colds=(), nphi=360, nrho=200):
    zs = ZS_SURF; phi = (np.arange(nphi) + 0.5)*2*math.pi/nphi; CP, SP = np.cos(phi), np.sin(phi)
    X = (x0 + R*CP)[:, None]*np.ones((1, len(zs))); Y = (y0 + R*SP)[:, None]*np.ones((1, len(zs))); Zg = np.broadcast_to(zs[None, :], X.shape)
    gx, gy, gz = gN(X, Y, Zg, plum, colds, gext=a0/1000.0); g = np.sqrt(gx*gx + gy*gy + gz*gz)
    side = 2.0*np.trapz(np.sum(nut(g/a0)*(gx*CP[:, None] + gy*SP[:, None]), axis=0)*(2*math.pi/nphi)*R, zs)
    rho = np.linspace(0.0, R, nrho + 1); Xc = x0 + rho[:, None]*CP[None, :]; Yc = y0 + rho[:, None]*SP[None, :]
    gxc, gyc, gzc = gN(Xc, Yc, np.full_like(Xc, Z_BOX), plum, colds, gext=a0/1000.0); gc = np.sqrt(gxc*gxc + gyc*gyc + gzc*gzc)
    caps = 2.0*np.trapz(np.sum(nut(gc/a0)*gzc, axis=1)*(2*math.pi/nphi)*rho, rho)
    return -(side + caps)*KPC**2/(4*math.pi*G)/MSUN

def sig_plummer(D, M, a): return M*a*a/(math.pi*(D*D + a*a)**2)
def M2D(x0, y0, R, plum, colds=(), nrho=400, nphi=720):
    rho = np.linspace(0.0, R, nrho + 1); phi = (np.arange(nphi) + 0.5)*2*math.pi/nphi
    X = x0 + rho[:, None]*np.cos(phi)[None, :]; Y = y0 + rho[:, None]*np.sin(phi)[None, :]; S = np.zeros_like(X)
    for M, a, xc, yc in plum: S += sig_plummer(np.sqrt((X - xc)**2 + (Y - yc)**2), M, a)
    for c in colds: S += c.sigma(np.sqrt((X - c.x)**2 + (Y - c.y)**2))
    return float(np.trapz(np.sum(S, axis=1)*(2*math.pi/nphi)*rho, rho))

# ============================================================== STEP 0
say("=" * 110); say("X32_bullet_cold_sector" + ("   [MUTATE]" if MUT else "")); say("=" * 110)
say("\n=== STEP 0 ===")
X26J_P = os.path.join(REB, "X26_cold_sector_map", "x26_cold_sector_map_results.json"); X26J = json.load(open(X26J_P)); RES["x26_json_sha256"] = sha(X26J_P)
SHEET = {f: [p for p in X26J["A2_direct"][f] if p["allowed"]] for f in FEET}
CSR = {f: X26J["energy"][f]["KT cluster median"]["cs_kms"] for f in FEET}
k0a = True
for f in FEET:
    cs = [10**(p["log10_cstar"] + p["r"]*math.log10(517.1/100.0) + 0.5*p["q"]*math.log10(1.35e-5/1e-3)) for p in SHEET[f]]
    dev = max(abs(min(cs)/CSR[f][0] - 1), abs(max(cs)/CSR[f][1] - 1)); n_ok = len(SHEET[f]) == {"canonical": 19, "alt": 16}[f]
    say(f"  {f}: {len(SHEET[f])} sheet points; recomputed KT-median c_s {min(cs):.1f}-{max(cs):.1f} km/s vs JSON {CSR[f][0]:.1f}-{CSR[f][1]:.1f} (max dev {dev:.2e})")
    k0a &= n_ok and dev <= 0.01
check("K0a", k0a, "X26 sheet counts 19/16 and KT-median c_s range reproduced", "<= 1 %")
RES["sheet_cs_KTmedian"] = CSR
# K0b: h57 reproduction (Route A at h57's a0)
plum0 = ([(2*M, a, x, y) for M, a, x, y in GAS] if MUT else GAS) + GAL                 # m1
mb1 = M2D(*BCG1, 300.0, plum0); mb3 = M2D(*BCG3, 300.0, plum0)
H57 = {"canonical": (6.826e13, 4.934e13), "alt": (7.659e13, 5.508e13)}
devs = [abs(mb1/4.203e13 - 1), abs(mb3/2.359e13 - 1)]
for f in FEET:
    p1 = Mph_cyl(*BCG1, 300.0, plum0, A0_H57[f], nut_routeA); p3 = Mph_cyl(*BCG3, 300.0, plum0, A0_H57[f], nut_routeA)
    devs += [abs(p1/H57[f][0] - 1), abs(p3/H57[f][1] - 1)]
    say(f"  h57 reproduction {f} (a0 {A0_H57[f]:.3e}, Route A): M_bar {mb1:.4e} / {mb3:.4e} (h57 4.203e13 / 2.359e13); M_ph {p1:.4e} / {p3:.4e} (h57 {H57[f][0]:.3e} / {H57[f][1]:.3e})")
check("K0b", max(devs) <= 0.01, f"h57 M_bar and M_ph at BCG1/BCG3 reproduced, max dev {max(devs):.2e}", "<= 1 %")
# K0c: Clowe Table 2 offsets
SCALE = 3.413 if MUT else 4.413                                                        # m2
def hms(h, m, s): return 15.0*(h + m/60 + s/3600)
def dms(d, m, s): return -(abs(d) + m/60 + s/3600) if d < 0 else d + m/60 + s/3600
T2 = {"main BCG": (hms(6, 58, 35.3), dms(-55, 56, 56.3)), "main plasma": (hms(6, 58, 30.2), dms(-55, 56, 35.9)),
      "sub BCG": (hms(6, 58, 16.0), dms(-55, 56, 35.1)), "sub plasma": (hms(6, 58, 21.2), dms(-55, 56, 30.0))}
def sepk(a, b):
    (r1, d1), (r2, d2) = T2[a], T2[b]; d0 = math.radians(0.5*(d1 + d2))
    return math.hypot((r1 - r2)*math.cos(d0)*3600, (d1 - d2)*3600)*SCALE
OFF_OBS = {"main": sepk("main BCG", "main plasma"), "sub": sepk("sub BCG", "sub plasma")}; BB = sepk("main BCG", "sub BCG")
say(f"  Clowe Table 2: main BCG-plasma {OFF_OBS['main']:.1f} kpc, sub {OFF_OBS['sub']:.1f} kpc, BCG-BCG {BB:.1f} kpc")
check("K0c", abs(OFF_OBS["main"] - 209.4) <= 0.1 and abs(OFF_OBS["sub"] - 194.1) <= 0.1 and abs(BB - 721.5) <= 0.1, "209.4 / 194.1 / 721.5 kpc", "<= 0.1 kpc")
RES["offsets_obs_kpc"] = OFF_OBS
# K0d: transcribed numbers present in their record files
SRC = {os.path.join(REPO, "hunt_2026", "h57_bullet_peaks.py"): ["(2.0e14, 565.0, 190.0, 90.0), (1.5e13, 505.0, 525.0, 120.0)", "(1.5e13, 90.0, 670.0, 170.0), (-6.8e12, 70.0, 670.0, 170.0)",
          "(1.196e13, 470.0, 0.0, 0.0), (4.0e12, 245.0, 820.0, 220.0)", '{"BCG1": 3.5e14, "BCG3": 2.3e14}', "SIG_CRIT = 1.827e9"],
       os.path.join(REPO, "hunt_2026", "h57_bullet_peaks.out"): ["4.203e+13", "2.359e+13", "6.826e+13", "4.934e+13", "7.659e+13", "5.508e+13"],
       os.path.join(REPO, "opus_48_extended_research", "reviews", "bullet", "bullet_data_table.py"): ["KPC_PER_ARCSEC = 4.413", "(6,58,35.3), (-55,56,56.3)", "(6,58,30.2), (-55,56,35.9)",
          "(6,58,16.0), (-55,56,35.1)", "(6,58,21.2), (-55,56,30.0)", "0.36,0.06", "0.05,0.06", "0.20,0.05", "0.02,0.06", "4740 +710/-550 km/s", "~2700 km/s",
          "M200 main  ~1.5e15 ; M200 bullet ~1.5e14", "Subcluster (bullet) total~ 2.3e14", "~8 sigma", "Om=0.3, OL=0.7, H0=70", "T=14.1+-0.2 keV", "within 1 sigma of the galaxies"]}
miss = [(os.path.basename(p), s) for p, ss in SRC.items() for s in ss if s not in open(p).read()]
check("K0d", not miss, f"{sum(len(v) for v in SRC.values())} transcribed strings found in their record files; missing {miss}")
RES["record_sha256"] = {os.path.relpath(p, REPO): sha(p) for p in SRC}

# ---------------------------------------------- Hernquist wells, calibration (K0e)
def hq_X(s):
    s = np.asarray(s, float); out = np.ones_like(s)
    lo = s < 1 - 1e-6; hi = s > 1 + 1e-6
    out[lo] = np.arccosh(1/s[lo])/np.sqrt(1 - s[lo]**2); out[hi] = np.arccos(1/s[hi])/np.sqrt(s[hi]**2 - 1)
    return out
def hq_sigma(R, M, a):
    s = np.maximum(np.asarray(R, float)/a, 1e-6); X = hq_X(s); near = np.abs(s - 1) < 1e-3
    S = np.where(near, 4.0/15.0, ((2 + s*s)*X - 3)/np.where(near, 1.0, (1 - s*s)**2))
    return M/(2*math.pi*a*a)*S
def hq_ap(M, a, d, R=300.0, nrho=300, nphi=360):
    rho = np.linspace(0.0, R, nrho + 1); phi = (np.arange(nphi) + 0.5)*2*math.pi/nphi
    X = d + rho[:, None]*np.cos(phi)[None, :]; Y = rho[:, None]*np.sin(phi)[None, :]
    return float(np.trapz(np.sum(hq_sigma(np.hypot(X, Y), M, a), axis=1)*(2*math.pi/nphi)*rho, rho))
def calib(Mm, Ms):
    def F(la):
        am, as_ = np.exp(la)
        return [hq_ap(Mm, am, 0) + hq_ap(Ms, as_, D_AX) - OBS300["BCG1"], hq_ap(Ms, as_, 0) + hq_ap(Mm, am, D_AX) - OBS300["BCG3"]]
    best = None
    for g0 in ([math.log(400), math.log(100)], [math.log(800), math.log(30)], [math.log(250), math.log(200)], [math.log(1500), math.log(10)]):
        sol, info, ier, msg = fsolve(F, g0, full_output=True)
        r = max(abs(x) for x in F(sol))/2.3e14
        if ier == 1 and r < 1e-4 and np.all(np.exp(sol) > 1) and np.all(np.exp(sol) < 2e4): best = (float(np.exp(sol[0])), float(np.exp(sol[1])), r); break
    return best
WELL = calib(M_MAIN, M_SUB); WELL_FB = calib(M_MAIN, M_SUB_FB)
if WELL is None and WELL_FB is not None: WELLS = (M_MAIN, M_SUB_FB, WELL_FB, "fallback M_sub 2.3e14")
elif WELL is not None: WELLS = (M_MAIN, M_SUB, WELL, "M200 1.5e15 / 1.5e14")
else: WELLS = None
say(f"  Hernquist wells: M200 pair -> {WELL}; fallback pair -> {WELL_FB}")
check("K0e", WELLS is not None, f"well calibration solution: {WELLS[3] + ': a_main %.1f kpc, a_sub %.1f kpc' % (WELLS[2][0], WELLS[2][1]) if WELLS else 'none'}")
RES["wells"] = dict(primary=WELL, fallback=WELL_FB, used=WELLS[3] if WELLS else None)
STEP0 = all(CHECKS[k] for k in ("K0a", "K0b", "K0c", "K0d", "K0e"))
say(f"  STEP 0: {'PASS' if STEP0 else 'FAIL'}")

# K1 (estimator)
Mpt = 1e14; rho_ = np.linspace(1e-6, 300.0, 200001)
Man = math.sqrt(Mpt*MSUN*A0F["canonical"]/G)*np.trapz(np.arctan(Z_BOX/rho_), rho_)*KPC/MSUN
Mnu = Mph_cyl(0.0, 0.0, 300.0, [(Mpt, 0.001, 0.0, 0.0)], A0F["canonical"], nut_deep)
check("K1", abs(Mnu/Man - 1) < 0.01, f"deep-MOND cylinder quadrature {Mnu:.4e} vs analytic {Man:.4e} ({100*(Mnu/Man - 1):+.3f} %)", "<= 1 %")

# ============================================================== passage machinery
GK = 4.30091e-6                                     # kpc (km/s)^2 / Msun
KMS = 1.0227121650537077e-3                         # kpc/Myr per km/s
GI = GK*KMS**2                                      # kpc^3 / Myr^2 / Msun
FSIGN = -1.0 if MUT else 1.0                        # m3
def r200(M, z=0.296):
    Hz = 70.0*math.sqrt(0.3*(1 + z)**3 + 0.7)/1000.0                                    # km/s/kpc
    rhoc = 3*Hz**2/(8*math.pi*GK); return (M/(200*rhoc*4*math.pi/3))**(1/3)
def phiH(r, M, a): return -GK*M/(r + a)                                                  # (km/s)^2
def cold_table(M, a, cs, rt):
    r = np.concatenate([[0.0], np.geomspace(0.05, rt, 4000)])
    lr = -(phiH(r, M, a) - phiH(0.0, M, a))/cs**2; w = np.exp(lr - lr.max())
    dm = 4*math.pi*r*r*w; m = np.r_[0, np.cumsum(0.5*(dm[1:] + dm[:-1])*np.diff(r))]; mt = m[-1]
    rho3 = w/mt                                                                           # unit-mass density [1/kpc^3]
    R = np.concatenate([[0.0], np.geomspace(0.05, rt*0.999, 600)]); S = np.zeros_like(R)
    u = np.linspace(0.0, 1.0, 801)
    for i, Ri in enumerate(R):
        Rr = max(Ri, 1e-3); umax = math.acosh(rt/Rr); uu = u*umax; rr = Rr*np.cosh(uu)
        S[i] = 2*np.trapz(np.interp(rr, r, rho3)*rr, uu)
    return dict(r=r, m=m/mt, rho=rho3, R=R, S=S, rt=rt, cs=cs, M=M, a=a)
def sample(tab, n, sig, rng):
    M, a, rt = tab["M"], tab["a"], tab["rt"]
    rr = np.interp(rng.random(n), tab["m"], tab["r"])
    ct = 2*rng.random(n) - 1; ph = 2*math.pi*rng.random(n); st = np.sqrt(1 - ct*ct)
    pos = np.c_[rr*st*np.cos(ph), rr*st*np.sin(ph), rr*ct]
    vesc = np.sqrt(2*(phiH(rt, M, a) - phiH(rr, M, a))); vel = np.zeros((n, 3)); todo = np.arange(n)
    while len(todo):
        v = rng.normal(0.0, sig, (len(todo), 3)); ok = np.sqrt((v*v).sum(1)) < vesc[todo]
        vel[todo[ok]] = v[ok]; todo = todo[~ok]
    return pos, vel*KMS
def accH(p, c, M, a):
    d = p - c; r = np.sqrt((d*d).sum(1)); r = np.maximum(r, 1e-6)
    return FSIGN*(-GI*M/(r*(r + a)**2))[:, None]*d
def run_pass(Mm, am, Ms, as_, tm, ts, cs_m, cs_s, v, b, N=5000, dt=0.1, seed=32, partner=True):
    """rigid Hernquist wells, sub moves +x relative to main at speed v (km/s); returns f in 300 kpc and mean axial offset"""
    rng = np.random.default_rng(seed); vk = v*KMS; Mt = Mm + Ms
    t0 = -4000.0/vk; t1 = D_AX/vk; nst = int(math.ceil((t1 - t0)/dt)); dt = (t1 - t0)/nst
    def ctr(t):
        s = np.array([vk*t, 0.0, b]); return -Ms/Mt*s, Mm/Mt*s
    def cvel(): return np.array([-Ms/Mt*vk, 0, 0]), np.array([Mm/Mt*vk, 0, 0])
    cm0, cs0 = ctr(t0); vm, vs = cvel()
    pm, um = sample(tm, N, cs_m, rng); ps, us = sample(ts, N, cs_s, rng)
    P = np.r_[pm + cm0, ps + cs0]; U = np.r_[um + vm, us + vs]; t = t0
    if not partner:
        P = np.r_[pm, ps]; U = np.r_[um, us]
    def acc(P, t):
        if partner:
            cm, cs_ = ctr(t); A = accH(P, cm, Mm, am) + accH(P, cs_, Ms, as_)
        else:
            A = np.r_[accH(P[:N], np.zeros(3), Mm, am), accH(P[N:], np.zeros(3), Ms, as_)]
        return A
    def meas(P, t):
        cm, cs_ = ctr(t) if partner else (np.zeros(3), np.zeros(3))
        out = {}
        for k, sl, c, sgn in (("main", slice(0, N), cm, 1.0), ("sub", slice(N, 2*N), cs_, -1.0)):
            d = P[sl] - c; inn = np.hypot(d[:, 0], d[:, 1]) < 300.0
            out[k] = (float(inn.mean()), float(sgn*d[inn, 0].mean()) if inn.any() else float("nan"))
        return out
    m0 = meas(P, t); A = acc(P, t)
    for _ in range(nst):
        U += 0.5*dt*A; P += dt*U; t += dt; A = acc(P, t); U += 0.5*dt*A
    return m0, meas(P, t)
def passage(cs_m, cs_s, v, b=0.0, wells=None, dt=0.1, N=5000):
    Mm, Ms, (am, as_, _), _lab = wells if wells else WELLS
    tm = cold_table(Mm, am, cs_m, r200(Mm)); ts = cold_table(Ms, as_, cs_s, r200(Ms))
    m0, m1 = run_pass(Mm, am, Ms, as_, tm, ts, cs_m, cs_s, v, b, N=N, dt=dt, partner=True)
    c0, c1 = run_pass(Mm, am, Ms, as_, tm, ts, cs_m, cs_s, v, b, N=N, dt=dt, partner=False)
    out = {}
    for k in ("main", "sub"):
        out[k] = dict(f_ret=m1[k][0]/c1[k][0], dx=m1[k][1], frac_end=m1[k][0], ctrl_start=c0[k][0], ctrl_end=c1[k][0])
    return out, (tm, ts)

# ============================================================== physics (only after step 0)
def finish(V, code):
    RES["verdict"] = V; RES["checks"] = CHECKS; RES["runtime_s"] = time.time() - T0; RES["peak_rss_GB"] = rss()
    if "K5" not in CHECKS: check("K5", rss() < 1.0, f"peak RSS {rss():.3f} GB", "< 1 GB")
    RES["checks"] = CHECKS
    say(f"\nVERDICT: {V}")
    if MUT:
        must = ("K0b", "K0c", "K2"); RES["mutate_required_fail"] = {k: (k in CHECKS and not CHECKS[k]) for k in must}
        say("MUTATE: required failures " + ", ".join(f"{k} {'FAILED' if (k in CHECKS and not CHECKS[k]) else 'passed (BAD)'}" for k in must))
        code = 1
    json.dump(RES, open(os.path.join(HERE, f"x32_bullet_cold_sector_results{TAG}.json"), "w"), indent=1, default=float)
    say(f"runtime {time.time() - T0:.0f} s; peak RSS {rss():.3f} GB"); OUT.close(); sys.exit(code)

# K2 control equilibrium (run even if step 0 failed, so the MUTATE twin can show it)
W_ = WELLS if WELLS else (M_MAIN, M_SUB, (400.0, 100.0, 0), "dummy")
Mm, Ms, (am, as_, _), _ = W_
k2 = []
for f in FEET:
    for cs in CSR[f]:
        tm = cold_table(Mm, am, cs, r200(Mm)); ts = cold_table(Ms, as_, cs, r200(Ms))
        c0, c1 = run_pass(Mm, am, Ms, as_, tm, ts, cs, cs, V_BULK, 0.0, partner=False)
        for k in ("main", "sub"):
            k2.append(c1[k][0]/c0[k][0]); say(f"  control {f} c_s {cs:.0f} {k}: fraction in 300 kpc start {c0[k][0]:.4f} end {c1[k][0]:.4f}")
check("K2", min(k2) >= 0.95, f"isolated control end/start fraction in 300 kpc, min {min(k2):.4f}", ">= 0.95")
if not STEP0:
    finish("UNDECIDED (step 0)", 1)

say("\n=== REPORTED: c_s at the Bullet, Mach numbers ===")
Mm, Ms, (am, as_, _), wlab = WELLS
say(f"  wells ({wlab}): main M {Mm:.2e} a {am:.1f} kpc r200 {r200(Mm):.0f} kpc; sub M {Ms:.2e} a {as_:.1f} kpc r200 {r200(Ms):.0f} kpc")
def vc(M, a, r): return math.sqrt(GK*M*r/(r + a)**2)
VCM, VCS = vc(Mm, am, 300.0), vc(Ms, as_, 300.0)
say(f"  well V_c(300 kpc): main {VCM:.0f}, sub {VCS:.0f} km/s; FP3 bound if c_s <= sqrt(2/3) sigma_well with sigma_well = V_c/sqrt2: main {math.sqrt(2/3)*VCM/math.sqrt(2):.0f}, sub {math.sqrt(2/3)*VCS/math.sqrt(2):.0f} km/s")
sigB = math.sqrt(14.1*KEV/(0.6*MP))/1e3
def rho548(ctr):
    r = np.linspace(0, 548.0, 220)[1:]; th = np.linspace(0, math.pi, 61); ph = np.linspace(0, 2*math.pi, 121)[:-1]
    R_, T_, P_ = np.meshgrid(r, th, ph, indexing="ij"); X = ctr[0] + R_*np.sin(T_)*np.cos(P_); Y = ctr[1] + R_*np.sin(T_)*np.sin(P_); Zc = R_*np.cos(T_)
    rho = np.zeros_like(X)
    for M, a, xc, yc in ALLB: rho += 3*M/(4*math.pi*a**3)*(1 + ((X - xc)**2 + (Y - yc)**2 + Zc**2)/a**2)**-2.5
    w = R_**2*np.sin(T_); Mb = np.trapz(np.trapz(np.sum(rho*w, axis=2)*(2*math.pi/120), th, axis=1), r)
    return Mb/(4/3*math.pi*548.0**3)/1e9                                                   # Msun/pc^3
RHOB = {"main": rho548(BCG1), "sub": rho548(BCG3)}
REP = {"sigma_bullet_kms": sigB, "rho_b548": RHOB}
for f in FEET:
    for k in ("main", "sub"):
        cs = [10**(p["log10_cstar"] + p["r"]*math.log10(sigB/100) + 0.5*p["q"]*math.log10(RHOB[k]/1e-3)) for p in SHEET[f]]
        REP[f"{f}|{k}|cs_bullet_own"] = [min(cs), max(cs)]
        say(f"  {f} {k}: Bullet-own c_s (sigma {sigB:.0f} km/s from 14.1 keV, rho_b(<548 kpc) {RHOB[k]:.2e} Msun/pc^3): {min(cs):.0f}-{max(cs):.0f} km/s")
    for p in (3, 4, 6):
        fac = (1/1.296)**(p - 0.5); REP[f"{f}|z0296|p{p}"] = [CSR[f][0]*fac, CSR[f][1]*fac]
        say(f"  {f} z = 0.296, p = {p}: c_s x {fac:.3f} -> {CSR[f][0]*fac:.0f}-{CSR[f][1]*fac:.0f} km/s")
    for v in (V_BULK, V_SHOCK):
        say(f"  {f} Mach v/c_s at v {v:.0f}: {v/CSR[f][1]:.2f}-{v/CSR[f][0]:.2f} (gas: 3.0 +- 0.4, M06)")
RES["reported_cs"] = REP

# ============================================================== passages (C)
say("\n=== (C) COLLISIONLESS PASSAGES (rigid wells, sigma_1D = c_s) ===")
PASS = {}
for f in FEET:
    for cs in CSR[f]:
        for v in (V_BULK, V_SHOCK):
            o, tabs = passage(cs, cs, v); PASS[(f, cs, v)] = (o, tabs)
            say(f"  {f} c_s {cs:.0f} v {v:.0f} b 0: f_ret main {o['main']['f_ret']:.3f} (dx {o['main']['dx']:+.1f} kpc), sub {o['sub']['f_ret']:.3f} (dx {o['sub']['dx']:+.1f} kpc)")
RES["passages"] = {f"{f}|{cs:.1f}|{v:.0f}": PASS[(f, cs, v)][0] for (f, cs, v) in PASS}
f_, cs_, v_ = "canonical", CSR["canonical"][0], V_BULK
o_h, _ = passage(cs_, cs_, v_, dt=0.05)
d6 = max(abs(o_h[k]["f_ret"] - PASS[(f_, cs_, v_)][0][k]["f_ret"]) for k in ("main", "sub"))
check("K6", d6 <= 0.02, f"f_ret at dt 0.1 vs 0.05 Myr (A1.2) (canonical c_s {cs_:.0f}, v {v_:.0f}): max |diff| {d6:.4f}", "<= 0.02")
say("  reported: b = 150 kpc (PROVISIONAL), M_sub fallback, CDM-like comparator")
REPP = {}
for f in FEET:
    for cs in CSR[f]:
        for v in (V_BULK, V_SHOCK):
            o, _ = passage(cs, cs, v, b=B_REP); REPP[f"{f}|{cs:.1f}|{v:.0f}|b150"] = o
            say(f"  {f} c_s {cs:.0f} v {v:.0f} b 150: f_ret main {o['main']['f_ret']:.3f}, sub {o['sub']['f_ret']:.3f}; dx {o['main']['dx']:+.1f} / {o['sub']['dx']:+.1f} kpc")
if WELL_FB is not None and WELLS[3] != "fallback M_sub 2.3e14":
    o, _ = passage(CSR["canonical"][0], CSR["canonical"][0], V_BULK, wells=(M_MAIN, M_SUB_FB, WELL_FB, "fb")); REPP["fallback|canonical|cmin|2700"] = o
    say(f"  fallback wells (M_sub 2.3e14; a {WELL_FB[0]:.1f}/{WELL_FB[1]:.1f}) canonical c_s {CSR['canonical'][0]:.0f} v 2700: f_ret main {o['main']['f_ret']:.3f}, sub {o['sub']['f_ret']:.3f}")
for v in (V_BULK, V_SHOCK):
    o, _ = passage(VCM/math.sqrt(2), VCS/math.sqrt(2), v); REPP[f"CDMlike|{v:.0f}"] = o
    say(f"  CDM-like (sigma_1D main {VCM/math.sqrt(2):.0f}, sub {VCS/math.sqrt(2):.0f}) v {v:.0f}: f_ret main {o['main']['f_ret']:.3f}, sub {o['sub']['f_ret']:.3f}; dx {o['main']['dx']:+.1f} / {o['sub']['dx']:+.1f} kpc")
RES["passages_reported"] = REPP

# ============================================================== maps
XS = np.arange(-500.0, 1400.0 + 1e-9, 10.0); YS = np.arange(-400.0, 700.0 + 1e-9, 10.0); ZM = zgrid(6000.0, n_in=140, n_out=110, z_in=1200.0)
def sigma_ph_map(plum, colds, a0, h=2.0):
    S = np.zeros((len(XS), len(YS)))
    for j0 in range(0, len(YS), 6):
        ys = YS[j0:j0 + 6]; X, Y, Z = np.meshgrid(XS, ys, ZM, indexing="ij")
        def F(ax, dx_, dy_, dz_):
            gx, gy, gz = gN(X + dx_, Y + dy_, Z + dz_, plum, colds, gext=a0/1000.0); g = np.sqrt(gx*gx + gy*gy + gz*gz); nt = nut_v3(g/a0)
            return nt*(gx if ax == 0 else gy if ax == 1 else gz)
        div = ((F(0, h, 0, 0) - F(0, -h, 0, 0)) + (F(1, 0, h, 0) - F(1, 0, -h, 0)) + (F(2, 0, 0, h) - F(2, 0, 0, -h)))/(2*h)
        rho = -div/(4*math.pi*G)*KPC**2/MSUN
        S[:, j0:j0 + 6] = 2.0*np.trapz(rho, ZM, axis=2)
    return S
XX, YY = np.meshgrid(XS, YS, indexing="ij")
def sigma_direct(plum, colds):
    S = np.zeros_like(XX)
    for M, a, xc, yc in plum: S += sig_plummer(np.hypot(XX - xc, YY - yc), M, a)
    for c in colds: S += c.sigma(np.hypot(XX - c.x, YY - c.y))
    return S
def peak_in(S, A, Bp):
    mid = 0.5*(A + Bp); w = np.hypot(XX - mid[0], YY - mid[1]) <= 350.0
    i = np.argmax(np.where(w, S, -np.inf)); return np.array([XX.flat[i], YY.flat[i]])
PAIRS = {"main": (BCG1, GASM), "sub": (BCG3, GASB)}
def observe(colds, a0, label, want_map=True, extra=()):
    plum = ALLB + list(extra)
    out = {}
    if want_map:
        S = sigma_direct(plum, colds) + sigma_ph_map(plum, colds, a0)
        for k, (bc, gc) in PAIRS.items():
            pk = peak_in(S, bc, gc); dgas = float(np.hypot(*(pk - gc))); sep = float(np.hypot(*(bc - gc)))
            out[f"delta_{k}"] = dgas/sep; out[f"peak_{k}"] = pk.tolist(); out[f"peak_gas_kpc_{k}"] = dgas; out[f"peak_bcg_kpc_{k}"] = float(np.hypot(*(pk - bc)))
            out[f"Z_O1_{k}"] = (dgas/sep - 1)/SIG_DELTA
        out["kappa_max"] = float(S.max()/SIG_CRIT)
    for k, (bc, gc) in PAIRS.items():
        kb = (M2D(*bc, 100.0, plum, colds) + Mph_cyl(*bc, 100.0, plum, a0, nut_v3, colds))/(math.pi*1e4)/SIG_CRIT
        kg = (M2D(*gc, 100.0, plum, colds) + Mph_cyl(*gc, 100.0, plum, a0, nut_v3, colds))/(math.pi*1e4)/SIG_CRIT
        out[f"kbar_bcg_{k}"] = kb; out[f"kbar_gas_{k}"] = kg; out[f"dkappa_{k}"] = kb - kg
    for lab, bc in (("BCG1", BCG1), ("BCG3", BCG3)):
        out[f"M300_{lab}"] = M2D(*bc, 300.0, plum, colds) + Mph_cyl(*bc, 300.0, plum, a0, nut_v3, colds)
        out[f"Z_O3_{lab}"] = (out[f"M300_{lab}"]/OBS300[lab] - 1)/SIG_O3
    msg = "  " + label + ": "
    if want_map:
        msg += f"peaks main {out['peak_main']} (delta {out['delta_main']:.2f}, Z {out['Z_O1_main']:+.2f}; {out['peak_gas_kpc_main']:.0f} kpc from gas), sub {out['peak_sub']} (delta {out['delta_sub']:.2f}, Z {out['Z_O1_sub']:+.2f}; {out['peak_gas_kpc_sub']:.0f} kpc from gas); "
    msg += f"dkappa main {out['dkappa_main']:+.3f}, sub {out['dkappa_sub']:+.3f}; kbar sub BCG/gas {out['kbar_bcg_sub']:.3f}/{out['kbar_gas_sub']:.3f}; M300 {out['M300_BCG1']:.3e} / {out['M300_BCG3']:.3e} (Z_O3 {out['Z_O3_BCG1']:+.2f} / {out['Z_O3_BCG3']:+.2f})"
    say(msg); return out

say("\n=== THE LAW ALONE (baryons + v3 phantom, no cold; reported) ===")
LAW = {}
for f in FEET:
    LAW[f] = observe([], A0F[f], f"{f} law only")
    if f == "canonical":
        S = sigma_ph_map(ALLB, [], A0F[f]); m = np.hypot(XX - BCG1[0], YY - BCG1[1]) < 300.0
        mm = float(S[m].sum()*100.0); ms = Mph_cyl(*BCG1, 300.0, ALLB, A0F[f], nut_v3)
        check("K3", abs(mm/ms - 1) <= 0.08, f"phantom in the BCG1 300 kpc aperture: map {mm:.3e} vs surface integral {ms:.3e} ({100*(mm/ms - 1):+.1f} %)", "<= 8 %")
RES["law_only"] = LAW

# ---------------------------------------------- normalisation and readings
def colds_C(f, cs, v, A):
    o, (tm, ts) = PASS[(f, cs, v)]
    cm = BCG1 + o["main"]["dx"]*UAX; cs_ = BCG3 - o["sub"]["dx"]*UAX
    return [Cold(*cm, A[0]*o["main"]["f_ret"], tm), Cold(*cs_, A[1]*o["sub"]["f_ret"], ts)]
def solve_A(f, cs, v):
    a0 = A0F[f]
    def F(lA):
        A = np.exp(lA); cl = colds_C(f, cs, v, A)
        return [(M2D(*BCG1, 300.0, ALLB, cl) + Mph_cyl(*BCG1, 300.0, ALLB, a0, nut_v3, cl))/OBS300["BCG1"] - 1,
                (M2D(*BCG3, 300.0, ALLB, cl) + Mph_cyl(*BCG3, 300.0, ALLB, a0, nut_v3, cl))/OBS300["BCG3"] - 1]
    sol = fsolve(F, [math.log(4e14), math.log(2e14)], xtol=1e-8); res = max(abs(x) for x in F(sol))
    return np.exp(sol), res
MB_TOT = sum(m for m, *_ in ALLB); MB_MAIN = GAS[0][0] + GAL[0][0]; MB_SUB = MB_TOT - MB_MAIN
def placements_F(f, cs, v, A):
    o, (tm, ts) = PASS[(f, cs, v)]
    rho_m0 = A[0]*tm["rho"][0]; rho_s = A[1]*ts["rho"]
    thr = rho_m0*(v/cs)**2; inside = rho_s >= thr
    rs = float(ts["r"][inside].max()) if inside.any() else 0.0
    fcore = float(np.interp(rs, ts["r"], ts["m"])) if rs > 0 else 0.0
    ms = A[1]*(1 - fcore); mm = A[0]; dcm = D_AX*ms/(mm + ms)
    core = [Cold(*GASB, A[1]*fcore, ts)] if fcore > 0 else []
    Fa = [Cold(*GASM, mm + ms, tm)] + core
    Fb = [Cold(*(BCG1 + dcm*UAX), mm + ms, tm)] + core
    # A1.3 F-c: coaxial annuli merge inelastically; merged column at BCG1 + D_AX * Sig_sub/(Sig_sub + Sig_main)
    Re = np.concatenate([[0.0], np.geomspace(0.01, tm["rt"]*0.999, 60)]); Fc_pl = []
    for k in range(60):
        rr = np.linspace(Re[k], Re[k + 1], 41); Sm = A[0]*np.interp(rr, tm["R"], tm["S"], right=0.0); Ss = A[1]*np.interp(rr, ts["R"], ts["S"], right=0.0)
        mk = float(np.trapz(2*math.pi*rr*(Sm + Ss), rr)); ws = float(np.trapz(2*math.pi*rr*Ss, rr))
        if mk <= 0: continue
        xk = D_AX*ws/mk; c = BCG1 + xk*UAX; Fc_pl.append((mk, max(0.5*(Re[k] + Re[k + 1]), 1.0), float(c[0]), float(c[1])))
    Fc = Fc_pl
    sub_c = sum(m*((x - BCG1[0])*UAX[0] + (y - BCG1[1])*UAX[1]) for m, a, x, y in Fc_pl)/sum(m for m, *_ in Fc_pl)
    gg = dict(rho_main0=rho_m0, rho_sub0=float(rho_s[0]), GunnGott_ratio_at_sub_centre=float(thr/rho_s[0]), r_strip_kpc=rs, f_core=fcore, d_cm_kpc=dcm,
              Fc_fluid_centroid_from_BCG1_kpc=float(sub_c), Fc_ncomp=len(Fc_pl))
    return Fa, Fb, Fc, gg
def grade(obs, reading):
    fails, passes = [], []
    for k in ("main", "sub"):
        z = abs(obs[f"Z_O1_{k}"]); (fails if z > 3 else passes if z <= 2 else []).append(f"O1 {k} |Z| {z:.2f}")
        (passes if obs[f"dkappa_{k}"] > 0 else fails).append(f"O2 {k} dkappa {obs[f'dkappa_{k}']:+.3f}")
    if reading == "F":
        for lab in ("BCG1", "BCG3"):
            z = abs(obs[f"Z_O3_{lab}"]); (fails if z > 3 else passes if z <= 2 else []).append(f"O3 {lab} |Z| {z:.2f}")
    if reading == "C":
        (passes if obs["cap_ok"] else fails).append(f"cap A_tot {obs['A_tot']:.3e} vs {OMEGA_C_B*MB_TOT:.3e}")
    nobs = 4 + (2 if reading == "F" else 1)
    cls = "FAIL" if fails else ("PASS" if len(passes) == nobs else "TENSION")
    worst = max([abs(obs[f"Z_O1_{k}"]) for k in ("main", "sub")] + ([abs(obs[f"Z_O3_{l}"]) for l in ("BCG1", "BCG3")] if reading == "F" else [])
                + [99.0*(obs[f"dkappa_{k}"] <= 0) for k in ("main", "sub")])
    return cls, fails, worst

say("\n=== READINGS (graded combinations: 2 c_s x 2 v, b = 0) ===")
GR = {}; KRES = []
for f in FEET:
    GR[f] = {"C": [], "F": []}
    for cs in CSR[f]:
        for v in (V_BULK, V_SHOCK):
            A, res = solve_A(f, cs, v); KRES.append(res)
            say(f"\n  -- {f} c_s {cs:.1f} km/s, v {v:.0f} km/s: pre-merger cold A_main {A[0]:.3e}, A_sub {A[1]:.3e} (sum {A.sum():.3e}; cap 5.364 M_b {OMEGA_C_B*MB_TOT:.3e}; per-halo caps {OMEGA_C_B*MB_MAIN:.3e} / {OMEGA_C_B*MB_SUB:.3e}); residual {res:.1e}")
            oC = observe(colds_C(f, cs, v, A), A0F[f], f"{f} C"); oC["A"] = A.tolist(); oC["A_tot"] = float(A.sum()); oC["cap_ok"] = bool(A.sum() <= OMEGA_C_B*MB_TOT)
            cC = grade(oC, "C"); GR[f]["C"].append(dict(cs=cs, v=v, obs=oC, cls=cC[0], fails=cC[1]))
            say(f"     C: {cC[0]} {cC[1]}")
            Fa, Fb, Fc, gg = placements_F(f, cs, v, A)
            say(f"     F Gunn-Gott: ram/thermal at the sub centre {gg['GunnGott_ratio_at_sub_centre']:.1f}; r_strip {gg['r_strip_kpc']:.1f} kpc; f_core {gg['f_core']:.3f}; inelastic drift {gg['d_cm_kpc']:.0f} kpc")
            say(f"     F-c: merged fluid mass-weighted centroid {gg['Fc_fluid_centroid_from_BCG1_kpc']:.1f} kpc from BCG1 along the axis ({gg['Fc_ncomp']} annuli)")
            oa = observe(Fa, A0F[f], f"{f} F-a"); ob = observe(Fb, A0F[f], f"{f} F-b"); oc = observe([], A0F[f], f"{f} F-c", extra=Fc)
            ga, gb, gc = grade(oa, "F"), grade(ob, "F"), grade(oc, "F")
            use = min((("F-a", oa, ga), ("F-b", ob, gb), ("F-c", oc, gc)), key=lambda t: t[2][2])
            GR[f]["F"].append(dict(cs=cs, v=v, gunn_gott=gg, Fa=dict(obs=oa, cls=ga[0], fails=ga[1]), Fb=dict(obs=ob, cls=gb[0], fails=gb[1]),
                                   Fc=dict(obs=oc, cls=gc[0], fails=gc[1]), used=use[0], cls=use[2][0], fails=use[2][1]))
            say(f"     F-a: {ga[0]} {ga[1]}"); say(f"     F-b: {gb[0]} {gb[1]}"); say(f"     F-c: {gc[0]} {gc[1]}"); say(f"     F graded at {use[0]}: {use[2][0]}")
check("K4", max(KRES) <= 0.01, f"A normalisation residual max {max(KRES):.1e}", "<= 1 %")
RES["graded"] = GR

def rclass(lst):
    c = [x["cls"] for x in lst]
    return "ALLOWED" if all(x == "PASS" for x in c) else ("EXCLUDED" if all(x == "FAIL" for x in c) else "TENSION")
PER = {f: {r: rclass(GR[f][r]) for r in ("C", "F")} for f in FEET}
for f in FEET: say(f"  {f}: C {PER[f]['C']}, F {PER[f]['F']}")
RES["per_footing"] = PER
if all(PER[f]["F"] == "EXCLUDED" and PER[f]["C"] == "ALLOWED" for f in FEET): V = "FLUID EXCLUDED, COLLISIONLESS ALLOWED"
elif all(PER[f]["F"] == "EXCLUDED" and PER[f]["C"] == "EXCLUDED" for f in FEET): V = "BOTH EXCLUDED"
elif all(PER[f]["F"] == "ALLOWED" and PER[f]["C"] == "ALLOWED" for f in FEET): V = "BOTH ALLOWED"
else: V = "UNDECIDED"
check("K5", rss() < 1.0, f"peak RSS {rss():.3f} GB", "< 1 GB")
step_ok = all(CHECKS[k] for k in ("K1", "K2", "K3", "K4", "K6"))
if not step_ok: V = "UNDECIDED (check failure)"
finish(V, 0 if not MUT else 1)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR28 CONTROLS -- the machinery behind XR28's cluster-outskirts lane reproduces published and committed numbers before it is
used on the chain.

WHY.  XR28 asks whether the outskirts of galaxy clusters (the splashback radius and the outer slope) can measure the derivation
chain's band-pass length L.  Its answer rests on a spherical secondary-infall (shell) model, the chain's band-passed phantom,
a projection to Delta Sigma and a DK14 forward-fit.  Each piece is checked here first.

CHECKS (pre-declared; load-bearing unless marked)
  K1  BERTSCHINGER (1985): the self-similar collisionless secondary-infall solution (EdS, point-mass seed, M_ta ~ t^(2/3)),
      computed by iterating the similarity trajectory to a self-consistent mass profile, puts the first three caustics at
      0.364, 0.236 and 0.179 of the current turnaround radius (the published values, as quoted by Wang, Wang & Mo 2022,
      A&A 667, A99, sec. 3.2) -- each within 1%.
  K2  ADHIKARI, DALAL & CHAMBERLAIN (2014, JCAP 11, 019): their toy model (constant-mass collapse to r_ta/2, then a growing
      NFW halo M ~ a^s, R ~ a^(1+s/3), outer slope 3s/(3+s), with Lambda) reproduces their fitting function eq. (3),
      Delta_s = 38 Omega_M^(-0.57-0.02 s) e^(0.2 Omega_M + 0.52 s^(3/4)), within 10% (twice the fit's quoted ~5%) at
      s = 1, 2, 3 and Omega_M = 0.3, 0.5, 1.
  K3  XR19 (committed b55775ce0): its R table's comoving reach of a daughter born at z_e = 1 (4.945567068731957 Mpc, from its
      committed results JSON) is reproduced EXACTLY from XR19_common's own E(z) and H0 with its 4001-point trapezoid; an
      independent quadrature agrees to 1e-6 (reported).
  K4  THE PHANTOM: this lane's generalised band-passed phantom equals FP6's committed phantom() (exec'd read-only up to its
      CONTROLS banner) for point masses 1e11-1e14 Msun, L = 0.5-3 Mpc, both footings, to 1e-6; with L -> oo it is the
      unfiltered P2 phantom (FP6 K4's limit).
  K5  THE PROJECTION (the coordinator's instruction: not FP6's esd_of_M): the uniform-shell Delta Sigma equals Wright &
      Brainerd's analytic NFW to 0.5% at the 14 WL radii (0.2-20 h^-1 cMpc); the DK14 forward-fit recovers r_sp of a known
      DK14 profile to 2%.
  K5b THE PROJECTOR ON FP20's TEST CASES [added after FP20 (7a8c25321) listed XR28's model_esd among the projectors with its
      defect B, by name]: truncated SIS, NFW, a cored and a hollow template (at 35 kpc and the 14 WL radii) within 0.2% of an
      independent singularity-free quadrature (Sigma = 2 Int_0^U rho(sqrt(R^2 + u^2)) du; M_2D by its non-singular integral);
      a compact mass passed as extended kept exactly; the model's histogram profiles projected to 1e-6.
  K6  CONVERGENCE of the shell model (LCDM and the chain at H_Y's L, the ACT-DR5 sample's mass and z, t = 0 member): doubling
      the shells (600 -> 1200) and halving the late step (0.0015 -> 0.00075) moves the 3D lensing r_sp/r200m and the DK14
      WL r_sp/r200m by <= 5%.  [As first written.  It FELL in this lane's first run (the MUTATE run): the LCDM DK14 fit read an
      inner 1-D caustic as splashback (x_sp = 0.26) and the LCDM read-out moved with the step.  Kept as run, now reported.]
  K6b CONVERGENCE of the production configuration [declared after K6 fell, before any main run]: the 3-member ensemble, a
      lognormal apocentre scatter of 0.12 in r on the matter profiles (the triaxiality a spherical model lacks), the DK14
      read-out restricted to [0.5, 3] r200m, ds = 0.00075, 2 kick nodes: 1200 shells, ds = 0.0005 and 4 kick nodes move the
      DK14 WL and galaxy r_sp/r200m by <= 5% (LCDM; the chain at H_Y's L0 and at L0 = 0.75 Mpc).
  K7  (reported) REALISM of the LCDM shell model: its stacked r_sp/r200m against More, Diemer & Kravtsov (2015, ApJ 810,
      36, eq. 5) at the model's own accretion rate, and its DK14 WL r_sp/r200m against Shin et al. (2021)'s N-body value 1.07.
  K8  (reported) the committed inputs the lane reads: FP10's budget (A6) and XR19's F_tot(z), with file hashes.
MUTATE=1: K1's mass profile is frozen at the initial guess (no self-consistent shell crossing) and K2's halo stops growing
after the shell enters it: K1 and K2 must FAIL (rc = 1).

HISTORY (stated).  Scratch prototypes came first: the self-similar iteration (event-reflection versions failed to run; the
softened version with a point-mass closure gave 0.3600/0.2325/0.1756 at tau_max = 100, the envelope closure 0.3656/0.2373/
0.1800 at tau_max = 300, eps = 3e-4), the Adhikari toy model (ratios 0.90-1.09), the projection test (a first NFW check
used a wrong reference density; corrected: 7e-4), and the FP6 phantom comparison (5e-8).  These fixed the settings below;
the thresholds were set before this script's first run.  The first run (MUTATE) showed K6 failing for every mode; K6b
and the production settings were then added (disclosed above), and MUTATE was re-run before the main run.  K5b was added
after the first recorded main run, on the coordinator's relay of FP20's projector audit; MUTATE and main were then re-run
(these outputs), the projector itself unchanged.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR28_controls.py   (~12 min, one process)
"""
import os, sys, io, math, json, time, contextlib, subprocess, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
warnings.filterwarnings("ignore")
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import XR28_common as X

MUTATE = os.environ.get("MUTATE", "0") == "1"
R = X.Report("XR28 controls", "XR28_controls", MUTATE)
P, check = R.P, R.check
P(__doc__.split("CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: K1's mass profile frozen at the initial guess; K2's halo stops growing after entry -- K1 and K2 must FAIL ***")

# ============================================================================================ K1 Bertschinger
R.banner("K1  BERTSCHINGER (1985): self-similar collisionless secondary infall, EdS, point-mass seed")
TMAX, EPS = 300.0, 3e-4
LMIN, NL = math.log(1e-6), 3000
LGRID = np.linspace(LMIN, 0.0, NL); DLG = LGRID[1] - LGRID[0]; LAMG = np.exp(LGRID)


def bert_traj(Mg):
    Mg_l = Mg.tolist()

    def rhs(t, y):
        L = y[0]; lam = abs(L) * t ** (-8.0 / 9.0)
        if lam <= 1e-6:
            Mf = Mg_l[0] * (max(lam, 1e-30) / 1e-6) ** 0.75
        elif lam >= 1.0:
            Mf = 1.0
        else:
            u = (math.log(lam) - LMIN) / DLG; i = int(u); fr = u - i
            Mf = Mg_l[i] + fr * (Mg_l[i + 1] - Mg_l[i])
        return [y[1], -(math.pi ** 2 / 8.0) * t ** (2.0 / 3.0) * Mf * L / (L * L + EPS * EPS) ** 1.5]
    s = solve_ivp(rhs, (1.0, TMAX), [1.0, 0.0], method="DOP853", rtol=1e-8, atol=1e-10, dense_output=True)
    tau = np.exp(np.linspace(0.0, math.log(TMAX), 400000))
    return tau, np.abs(s.sol(tau)[0])


def bert_mass(tau, Lam):
    lam = Lam * tau ** (-8.0 / 9.0)
    w = (2.0 / 3.0) * tau ** (-2.0 / 3.0) * np.gradient(np.log(tau))
    o = np.argsort(lam); cum = np.cumsum(w[o])
    M = np.interp(LAMG, lam[o], cum, left=0.0)
    lenv = lam[tau > TMAX / 3.0].max()
    M = M + TMAX ** (-2.0 / 3.0) * np.minimum(LAMG / lenv, 1.0) ** 0.75       # the shells beyond tau_max, inside their envelope
    return np.minimum(M, 1.0), lam


def caustics(tau, lam):
    d = np.diff(lam); im = np.where((d[:-1] > 0) & (d[1:] <= 0))[0] + 1
    return [float(lam[i]) for i in im if tau[i] > 1.2][:3]


Mg = LAMG ** 0.75
hist = []
for it in range(30):
    tau, Lam = bert_traj(Mg)
    Mn, lam = bert_mass(tau, Lam)
    cs = caustics(tau, lam); dM = float(np.max(np.abs(Mn - Mg)))
    hist.append(dict(it=it, dM=dM, caustics=cs))
    P(f"    iteration {it}: max |dM| = {dM:.2e}; caustics = {np.round(cs, 4).tolist()}   {R.el()}")
    if MUTATE:
        break                                       # MUTATE: the profile is never updated (the initial guess's orbit)
    Mg = 0.5 * Mg + 0.5 * Mn
    if dM < 1e-3 and it >= 5:
        break
PUB = (0.364, 0.236, 0.179)
dev = [abs(c_ / p_ - 1) for c_, p_ in zip(cs, PUB)]
check("K1 BERTSCHINGER (1985): the self-consistent self-similar collisionless solution puts the first three caustics at 0.364, "
      "0.236, 0.179 r_ta (published) -- each within 1%",
      f"caustics {', '.join(f'{c_:.4f}' for c_ in cs)} (published {PUB}); deviations {', '.join(f'{d_:.2%}' for d_ in dev)}; "
      f"{len(hist)} iterations, tau_max {TMAX:.0f}, softening {EPS:g}", len(cs) == 3 and max(dev) <= 0.01)
R.numbers["K1"] = dict(caustics=cs, published=PUB, dev=dev, history=hist)

# ============================================================================================ K2 Adhikari
R.banner("K2  ADHIKARI, DALAL & CHAMBERLAIN (2014): the toy model against their fitting function eq. (3)")
GK = X.GMPC


def fit_A14(s, Om_):
    return 38.0 * Om_ ** (-0.57 - 0.02 * s) * math.exp(0.2 * Om_ + 0.52 * s ** 0.75)


def cosmo(Om0, H0=70.0):
    OL0 = 1 - Om0
    aa = np.geomspace(1e-6, 3.0, 40000)
    Ez = np.sqrt(Om0 / aa ** 3 + OL0)
    integ = 1.0 / (aa * H0 * Ez)
    tt = np.concatenate([[0.0], np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(aa))]) + (2 / 3) * aa[0] / (H0 * math.sqrt(Om0 / aa[0] ** 3))
    return dict(Om0=Om0, OL0=OL0, H0=H0, a_of_t=lambda t: float(np.interp(t, tt, aa)), t_of_a=lambda a: float(np.interp(a, aa, tt)),
                rhom=lambda a: Om0 * 3 * H0 ** 2 / (8 * math.pi * GK) / a ** 3, Omz=lambda a: Om0 / a ** 3 / (Om0 / a ** 3 + OL0))


def fnfw(x):
    return math.log1p(x) - x / (1 + x)


def c_of_s(s):
    tgt = 3 * s / (3 + s)
    return brentq(lambda c: c * c / ((1 + c) ** 2 * fnfw(c)) - tgt, 1e-3, 1e4)


def splash(s, C, t_ta, M=1e14, grow=True):
    lam = C["H0"] ** 2 * C["OL0"]
    def tta(rta):
        f = lambda u: rta / math.sqrt(max(2 * (GK * M / (u * rta) - GK * M / rta + lam * rta ** 2 * (u * u - 1) / 2), 1e-300))
        return quad(f, 0.0, 1.0, limit=400)[0]
    rta = brentq(lambda r: tta(r) - t_ta, 1e-3, 1e3)
    ev = lambda t, y: y[0] - rta / 2; ev.terminal = True; ev.direction = -1
    s1 = solve_ivp(lambda t, y: [y[1], -GK * M / y[0] ** 2 + lam * y[0]], (t_ta, t_ta * 20), [rta, 0.0], events=ev, rtol=1e-10, atol=1e-12)
    ti = s1.t_events[0][0]; ri, vi = s1.y_events[0][0]
    ai = C["a_of_t"](ti); c = c_of_s(s)

    def Menc(r, t):
        a = C["a_of_t"](t)
        Mt = M * (a / ai) ** s if grow else M
        Rh = ri * (a / ai) ** (1 + s / 3.0) if grow else ri
        return Mt * fnfw(min(abs(r), Rh) / (Rh / c)) / fnfw(c)
    s2 = solve_ivp(lambda t, y: [y[1], -GK * Menc(y[0], t) * np.sign(y[0]) / max(y[0] ** 2, 1e-12) + lam * y[0]],
                   (ti, ti * 30), [ri, vi], rtol=1e-9, atol=1e-11, dense_output=True, max_step=ti * 0.01)
    tt = np.linspace(ti, s2.t[-1], 200000); rr = s2.sol(tt)[0]
    j0 = np.where(np.sign(rr[:-1]) != np.sign(rr[1:]))[0][0]
    ar = np.abs(rr); k = j0 + 1 + int(np.argmax(np.diff(ar[j0 + 1:]) < 0))
    a_s = C["a_of_t"](tt[k])
    return Menc(ar[k], tt[k]) / (4 * math.pi / 3 * ar[k] ** 3 * C["rhom"](a_s)), C["Omz"](a_s)


K2 = {}
for s in (1.0, 2.0, 3.0):
    for Omt in (0.3, 0.5, 1.0):
        C = cosmo(0.3 if Omt < 0.99 else 1.0 - 1e-9)
        if Omt > 0.99:
            Ds, Omz = splash(s, C, C["t_of_a"](0.3), grow=not MUTATE)
        else:
            lt = brentq(lambda l_: splash(s, C, math.exp(l_), grow=not MUTATE)[1] - Omt, math.log(C["t_of_a"](0.02)),
                        math.log(C["t_of_a"](0.6)), xtol=1e-4)
            Ds, Omz = splash(s, C, math.exp(lt), grow=not MUTATE)
        K2[f"{s:.0f}|{Omt}"] = dict(model=Ds, fit=fit_A14(s, Omz), Om=Omz, ratio=Ds / fit_A14(s, Omz))
        P(f"    s = {s:.0f}, Omega_M = {Omz:.3f}: Delta_s = {Ds:.1f} (fit {fit_A14(s, Omz):.1f}), ratio {Ds / fit_A14(s, Omz):.3f}   {R.el()}")
rat = [v_["ratio"] for v_ in K2.values()]
check("K2 ADHIKARI et al. (2014): their toy model reproduces their eq. (3) within 10% over s = 1-3, Omega_M = 0.3-1 (a Lambda "
      "cosmology control of the orbit integration)", f"ratios {min(rat):.3f}-{max(rat):.3f}; s = 1: "
      + ", ".join(f"{v_['ratio']:.3f}" for k_, v_ in K2.items() if k_.startswith("1|")), max(abs(r_ - 1) for r_ in rat) <= 0.10)
R.numbers["K2"] = K2

# ============================================================================================ K3 XR19
R.banner("K3  XR19 (committed b55775ce0): a daughter's comoving reach from z_e = 1, reproduced exactly")
blob = subprocess.run(["git", "-C", X.REPO, "show", "HEAD:real_research/cross_thread_review_2026_09_26/XR19_front_physics_results.json"],
                      capture_output=True, text=True).stdout
committed = json.loads(blob)["numbers"]["R"]["1.0"]["chi_to_z0_Mpc"]
import XR19_common as X19                                  # read-only import of the committed module
ze = 1.0; ae = 1 / (1 + ze); aa = np.linspace(ae, 1.0, 4001)
integrand = 600.0 * ae / (aa ** 3 * X19.H0_KPC * 1e3 * X19.E(1 / aa - 1))
chi = np.concatenate([[0.0], np.cumsum(0.5 * (integrand[1:] + integrand[:-1]) * np.diff(aa))])
mine = float(chi[-1])
indep = quad(lambda a_: 600.0 * ae / (a_ ** 3 * 67.36 * math.sqrt(0.3138 / a_ ** 3 + 0.6862)), ae, 1.0, epsabs=1e-12, epsrel=1e-12)[0]
check("K3 XR19's committed R table: the comoving reach of a daughter born at z_e = 1 with v_k = 600 km/s (peculiar speed "
      "~ 1/a) is reproduced exactly from XR19_common's E(z) and H0 and its 4001-point trapezoid",
      f"this lane {mine!r} Mpc; XR19 committed {committed!r}; independent quadrature {indep:.9f} (|d| = {abs(indep - mine):.1e})",
      mine == committed)
check("K3b (reported) the same reach by adaptive quadrature agrees to 1e-6", f"{abs(indep - mine):.2e} Mpc", abs(indep - mine) < 1e-6,
      load_bearing=False)
R.numbers["K3"] = dict(mine=mine, committed=committed, quad=indep)

# ============================================================================================ K4 phantom vs FP6
R.banner("K4  THE PHANTOM: this lane's routine against FP6's committed phantom() (exec'd read-only)")
FP6 = os.path.join(X.REPO, "real_research", "derivation_chain_2026", "FP6_gate_survey.py")
src = open(FP6).read(); cut = src.index('banner("K  CONTROLS')
ns6 = {"__file__": FP6, "__name__": "fp6_machinery"}
old = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src[:cut], FP6, "exec"), ns6)
finally:
    if old is None:
        os.environ.pop("MUTATE", None)
    else:
        os.environ["MUTATE"] = old
RG6, MPCm, MS6, G6, PCm = ns6["RG"], ns6["MPCm"], ns6["MS6"], ns6["G6"], ns6["PCm"]
GM6 = G6 * MS6 / (PCm * 1e6) / 1e6
rg = RG6 / MPCm; worst = 0.0; worst_inf = 0.0
Gsave = X.GMPC; X.GMPC = GM6
try:
    for Mb in (1e11, 1e13, 1e14):
        for f in X.FOOTS:
            a0 = ns6["A0"][f] * (PCm * 1e6) / 1e6
            for L in (0.5, 1.3, 3.0):
                ref = ns6["phantom"](Mb * MS6, ns6["A0"][f], L * MPCm) / MS6
                mine_ = X.phantom_enclosed(rg, np.full_like(rg, Mb), a0, L, "p2", 0.0, X.Smoother(rg))
                sel = (rg > 0.01) & (rg < 30)
                worst = max(worst, float(np.max(np.abs(mine_[sel] - ref[sel])) / np.max(np.abs(ref[sel]))))
            unf = X.phantom_enclosed(rg, np.full_like(rg, Mb), a0, None, "p2", 0.0)
            gN = G6 * Mb * MS6 / RG6 ** 2
            ref_inf = (ns6["nu_p2"](gN / ns6["A0"][f]) - 1.0) * gN * RG6 ** 2 / G6 / MS6
            sel = (rg > 0.01) & (rg < 30)
            worst_inf = max(worst_inf, float(np.max(np.abs(unf[sel] / ref_inf[sel] - 1))))
finally:
    X.GMPC = Gsave
check("K4 THE PHANTOM: this lane's band-passed phantom equals FP6's committed phantom() (M_b 1e11-1e14 Msun, L 0.5-3 Mpc, both "
      "footings) to 1e-6, and its L -> oo limit is the unfiltered P2 phantom to 1e-9",
      f"max relative deviation {worst:.1e}; L -> oo {worst_inf:.1e} (FP6's S8_LCDM in its namespace: {ns6['S8_LCDM']:.4f})",
      worst < 1e-6 and worst_inf < 1e-9)
R.numbers["K4"] = dict(dev=worst, dev_inf=worst_inf)

# ============================================================================================ K5 projection and DK14
R.banner("K5  THE PROJECTION AND THE DK14 FORWARD-FIT")
rho_ref = 2.775e11 * 0.3
proj = X.shell_esd_kernel(X.R_WL, X.DK_FINE)[0]
devs = []
for M200, c in ((1.8e14, 4.0), (4.8e14, 4.0), (1.4e15, 3.0)):
    r200 = (3 * M200 / (4 * np.pi * 200 * rho_ref)) ** (1 / 3); rs = r200 / c
    dc = (200 / 3.) * c ** 3 / (math.log(1 + c) - c / (1 + c))
    rho = rho_ref * dc / ((X.DK_MID / rs) * (1 + X.DK_MID / rs) ** 2)
    devs.append(float(np.max(np.abs(proj @ (rho * X.DK_VOL) / X.nfw_esd_wb(X.R_WL, M200, c, rho_ref) - 1))))
ptrue = [math.log10(3e14), math.log10(0.2), math.log10(0.35), math.log10(1.4), math.log10(6), math.log10(4), math.log10(3e12), 1.5]
rr = np.geomspace(0.3, 8, 900); sl = X.dk14_slope(rr, ptrue); rsp_true = float(rr[np.argmin(sl)])
yt = proj @ (X.dk14_rho(X.DK_MID, ptrue) * X.DK_VOL) + 10 ** 12.5 / (math.pi * X.R_WL ** 2)
fit = X.dk14_fit(yt, "esd")
check("K5 THE PROJECTION: the uniform-shell Delta Sigma equals Wright & Brainerd's NFW to 0.5% (M200m 1.8e14-1.4e15 h^-1, "
      "c 3-4, 14 radii 0.2-20 h^-1 cMpc); the DK14 forward-fit recovers a known DK14 profile's r_sp to 2%",
      f"NFW max deviation {max(devs):.1e}; DK14 r_sp true {rsp_true:.3f}, fitted {fit['r_sp']:.3f} ({fit['r_sp'] / rsp_true - 1:+.2%}), "
      f"gamma {sl.min():.2f} -> {fit['gamma']:.2f}", max(devs) < 0.005 and abs(fit["r_sp"] / rsp_true - 1) < 0.02)
R.numbers["K5"] = dict(nfw_dev=devs, dk14=dict(true=rsp_true, fit=fit["r_sp"], g_true=float(sl.min()), g_fit=fit["gamma"]))

# K5b: FP20's test cases against an independent, singularity-free quadrature (added after FP20 listed this lane's projector
# among the defective ones by the NAME model_esd; the projector here is FP20's own exact uniform-shell formula)
def ref_esd(rho, R, rt=30.0, rin=None, Mpoint=0.0, breaks=None):
    """exact Delta Sigma and Sigma by quadrature: Sigma = 2 Int_0^U rho(sqrt(R^2 + u^2)) du (U = sqrt(rt^2 - R^2));
    M_2D(<R) = M(<R) + Int_R^rt 4 pi r^2 rho (1 - sqrt(1 - R^2/r^2)) dr; plus a central point mass.  breaks: radii where rho
    jumps (integrated piecewise)."""
    br = sorted(set(([rin] if rin else []) + (list(breaks) if breaks is not None else [])))
    U = math.sqrt(rt * rt - R * R)
    ub = [0.0] + [math.sqrt(b_ * b_ - R * R) for b_ in br if R < b_ < rt] + [U]
    Sig = 2 * sum(quad(lambda u_: rho(math.sqrt(R * R + u_ * u_)), a_, b_, limit=200, epsrel=1e-12, epsabs=0)[0] for a_, b_ in zip(ub[:-1], ub[1:]))
    ib = [1e-9] + [b_ for b_ in br if 1e-9 < b_ < R] + [R]
    Min = sum(quad(lambda r_: 4 * math.pi * r_ * r_ * rho(r_), a_, b_, limit=200, epsrel=1e-12, epsabs=0)[0] for a_, b_ in zip(ib[:-1], ib[1:]))
    ob = [R] + [b_ for b_ in br if R < b_ < rt] + [rt]
    Mout = sum(quad(lambda r_: 4 * math.pi * r_ * r_ * rho(r_) * (1 - math.sqrt(max(1 - R * R / (r_ * r_), 0.0))), a_, b_, limit=200,
                    epsrel=1e-12, epsabs=0)[0] for a_, b_ in zip(ob[:-1], ob[1:]))
    return (Mpoint + Min + Mout) / (math.pi * R * R) - Sig, Sig


def shell_masses(rho, e, rin=None):
    return np.array([quad(lambda r_: 4 * math.pi * r_ * r_ * rho(r_), a_, b_, points=([rin] if (rin and a_ < rin < b_) else None),
                          limit=200, epsrel=1e-11, epsabs=0)[0] for a_, b_ in zip(e[:-1], e[1:])])


RT = 30.0; RV = np.concatenate([[0.035], X.R_WL])
prof5 = {"SIS": (lambda r_: 1e13 / (r_ * r_) if r_ <= RT else 0.0, None),
         "NFW (r_s = 0.35)": (lambda r_: (rho_ref * (200 / 3.) * 64 / (math.log(5) - 0.8)) / ((r_ / 0.3524) * (1 + r_ / 0.3524) ** 2) if r_ <= RT else 0.0, None),
         "cored (r_c = 50 kpc)": (lambda r_: 1e15 / (1 + (r_ / 0.05) ** 2) if r_ <= RT else 0.0, None),
         "hollow (empty inside 50 kpc)": (lambda r_: (1e13 / (r_ * r_) if 0.05 <= r_ <= RT else 0.0), 0.05)}
K5b = {}
eF = X.DK_FINE[X.DK_FINE <= RT]; eF = np.concatenate([eF, [RT]]) if eF[-1] < RT else eF
KF_ = X.shell_esd_kernel(RV, eF)
for nm, (rho, rin) in prof5.items():
    ref = np.array([ref_esd(rho, R_, RT, rin)[0] for R_ in RV])
    m_ex = shell_masses(rho, eF, rin)
    Min0 = quad(lambda r_: 4 * math.pi * r_ * r_ * rho(r_), 1e-12, eF[0], limit=200)[0]
    mine = KF_[0] @ m_ex + Min0 / (math.pi * RV ** 2)
    K5b[nm] = float(np.max(np.abs(mine / ref - 1)))
    P(f"    [K5b] {nm:30s}: max |shell/quad - 1| = {K5b[nm]:.2e} over R = 35 kpc and the 14 WL radii")
# a compact mass passed as an extended mass (all of it as a uniform shell in the model grid's first bin): Gauss keeps it all
Mc = 1e14
cont = np.zeros(len(X.XBM)); cont[0] = Mc / (X.XVOL[0] * X.RHOM0)          # the whole mass in the first (0.030-0.032 cMpc) bin
st_c = dict(prof={"lens": cont}, inner={"lens": 0.0})
got = X.model_esd(st_c, "lens", mean=0.0)
K5b["compact mass (model_esd)"] = float(np.max(np.abs(got / (Mc / (math.pi * (X.R_WL / X.HD) ** 2)) - 1)))
# the model's own path: a piecewise-constant (histogram) profile is projected exactly
rng_ = np.random.default_rng(5); hist = rng_.uniform(0.5, 2.0, len(X.XBM)) * 1e12 / X.XBM ** 2
st_h = dict(prof={"lens": hist / X.RHOM0 + 1.0}, inner={"lens": 0.0})
got_h = X.model_esd(st_h, "lens", mean=1.0)
pc_rho = lambda r_: float(hist[min(max(np.searchsorted(X.XB, r_, side="right") - 1, 0), len(hist) - 1)]) if X.XB[0] <= r_ < X.XB[-1] else 0.0
ref_h = np.array([ref_esd(pc_rho, R_ / X.HD, X.XB[-1], None, breaks=X.XB)[0] for R_ in X.R_WL[:6]])
K5b["histogram (model_esd, exact)"] = float(np.max(np.abs(got_h[:6] / ref_h - 1)))
P(f"    [K5b] compact 1e14 Msun mass in the first bin: max |model_esd/(M/pi R^2) - 1| = {K5b['compact mass (model_esd)']:.1e}; "
  f"piecewise-constant profile through model_esd vs quadrature: {K5b['histogram (model_esd, exact)']:.1e}")
check("K5b THE PROJECTOR ON FP20's TEST CASES (FP20 listed this lane by the function name model_esd; the projector is FP20's own "
      "exact uniform-shell formula): truncated SIS, NFW, a cored and a hollow template (at 35 kpc and the 14 WL radii) within "
      "0.2% of an independent singularity-free quadrature; a compact mass passed as extended is kept exactly; the model's "
      "histogram profiles are projected to 1e-6",
      "; ".join(f"{k_}: {v_:.1e}" for k_, v_ in K5b.items()),
      all(v_ <= 2e-3 for k_, v_ in K5b.items() if "model_esd" not in k_) and K5b["compact mass (model_esd)"] < 1e-9
      and K5b["histogram (model_esd, exact)"] < 1e-6)
R.numbers["K5b"] = K5b

# ============================================================================================ K6 convergence, K7 realism
R.banner("K6  CONVERGENCE of the shell model (K6 as first written; K6b the production configuration); K7 (reported) realism")
S_B = X.DATA["ACT-DR5 x DES-Y3 (Shin+2021)"]
Mt = S_B["M200m"] * 1e14 / X.HD; zB = S_B["z"]
fp10 = X.fp10_budget(600.0, "185"); fweb = X.fweb_history(fp10)


def members(args):
    Mf, t, dark, L0, a0, Nq, ds, nmu = args
    ic = X.initial_profile(Mf, zB, Nq, t_env=t)
    parts = X.build_particles(ic, dark, vk=600.0, nmu=nmu, fp10=fp10, fweb=fweb, zobs=zB)
    res = X.run_shells(ic, parts, a0=a0, L0=L0, z_obs=zB, ds_late=ds)
    sp = res["sp"]
    return X.snapshot_profiles(res, {"all": np.ones_like(sp, bool), "bar": sp == 0, "dark": sp == 1})


def read(st, smooth=True, window=True):
    st = X.smooth_matter(st) if smooth else st
    r200h = st["r200m_lens"] * X.HD
    fw = X.dk14_fit(X.model_esd(st), "esd", r200h=r200h if window else None)
    fg = X.dk14_fit(X.model_sigma(st), "sigma", r200h=r200h if window else None)
    s3 = X.splashback3d(st["prof"]["lens"], st["r200m_lens"])
    return dict(x3=s3["x_sp"], g3=s3["gamma"], xwl=fw["r_sp"] / r200h, gwl=fw["gamma"], xgal=fg["r_sp"] / r200h, ggal=fg["gamma"],
                M=st["M200m_lens"])


def matched(dark, L0, a0, Nq, ds, nmu, guess):
    Mf = guess
    for _ in range(3):
        st = X.stack([(1.0, s_) for s_ in members((Mf, 0.0, dark, L0, a0, Nq, ds, nmu))])
        if abs(st["M200m_lens"] / Mt - 1) <= 0.03:
            break
        Mf *= Mt / st["M200m_lens"]
    return Mf


# K6 as first written: t = 0 member only, no apocentre scatter, unwindowed DK14 read-out, ds 0.0015 vs 0.00075, N_q 600 vs 1200
Mf0 = matched("lcdm", None, None, 600, 0.0015, 4, Mt * 1.3)
conv = {}
for lab, dark, L0, a0, g_ in (("LCDM", "lcdm", None, None, 1.0), ("chain H_Y", "nominal", X.L0_HY, X.A0["canonical"], 0.8)):
    Mf_ = matched(dark, L0, a0, 600, 0.0015, 4, Mf0 * g_)
    rows = {}
    for Nq, ds in ((600, 0.0015), (1200, 0.0015), (600, 0.00075)):
        o_ = read(X.stack([(1.0, s_) for s_ in members((Mf_, 0.0, dark, L0, a0, Nq, ds, 4))]), smooth=False, window=False)
        rows[f"{Nq}|{ds}"] = o_
        P(f"    [K6]  {lab:9s} N_q {Nq:4d}, ds {ds}: 3D lensing x_sp {o_['x3']:.3f}; DK14 WL x_sp {o_['xwl']:.3f}   {R.el()}")
    conv[lab] = rows
mv = max(abs(r_[k_] / rows_["600|0.0015"][k_] - 1) for rows_ in conv.values() for r_ in rows_.values() for k_ in ("x3", "xwl"))
check("K6 (reported; as first written -- it FELL in this lane's first run, the MUTATE run, and is kept as run) CONVERGENCE of the "
      "t = 0 member with no apocentre scatter and an unwindowed read-out: 1200 shells and a halved step move the 3D lensing and "
      "the DK14 WL r_sp/r200m by <= 5%", f"max change {mv:.1%}", mv <= 0.05, load_bearing=False)
R.numbers["K6"] = conv

# K6b: the production configuration (declared after K6 fell): the 3-member ensemble, apocentre scatter 0.12, the [0.5, 3] r200m
# read-out window, ds = 0.00075 and 2 kick nodes (XR28_outskirts_L), against 1200 shells, ds = 0.0005 and 4 kick nodes
cfgs = [("LCDM", "lcdm", None, None, 600, 0.00075, 2), ("LCDM", "lcdm", None, None, 1200, 0.00075, 2), ("LCDM", "lcdm", None, None, 600, 0.0005, 2),
        ("chain H_Y", "nominal", X.L0_HY, X.A0["canonical"], 600, 0.00075, 2), ("chain H_Y", "nominal", X.L0_HY, X.A0["canonical"], 1200, 0.00075, 2),
        ("chain H_Y", "nominal", X.L0_HY, X.A0["canonical"], 600, 0.0005, 2), ("chain H_Y", "nominal", X.L0_HY, X.A0["canonical"], 600, 0.00075, 4),
        ("chain 0.75", "nominal", 0.75, X.A0["canonical"], 600, 0.00075, 2), ("chain 0.75", "nominal", 0.75, X.A0["canonical"], 600, 0.0005, 2)]
convb = {}
if True:                                            # sequential (a module-level Pool would re-run this script under spawn)
    for lab, dark, L0, a0, Nq, ds, nmu in cfgs:
        Mf_ = matched(dark, L0, a0, Nq, ds, nmu, Mf0 * (1.0 if dark == "lcdm" else 0.8))
        sps = [members((Mf_, t, dark, L0, a0, Nq, ds, nmu)) for t, _ in X.GH3]
        o_ = read(X.stack([(w / 7.0, s_) for (t, w), ss in zip(X.GH3, sps) for s_ in ss]))
        convb[f"{lab}|{Nq}|{ds}|{nmu}"] = o_
        P(f"    [K6b] {lab:10s} N_q {Nq:4d}, ds {ds}, nodes {nmu}: DK14 WL x_sp {o_['xwl']:.3f} (gamma {o_['gwl']:.2f}); galaxies "
          f"{o_['xgal']:.3f} ({o_['ggal']:.2f}); 3D lensing {o_['x3']:.3f} ({o_['g3']:.2f}); M200m {o_['M']:.3e}   {R.el()}")
chg = {}
for k_, o_ in convb.items():
    lab = k_.split("|")[0]
    ref = convb[f"{lab}|600|0.00075|2"]
    chg[k_] = max(abs(o_["xwl"] / ref["xwl"] - 1), abs(o_["xgal"] / ref["xgal"] - 1))
check("K6b CONVERGENCE of the production configuration (3-member ensemble, apocentre scatter 0.12, [0.5, 3] r200m read-out, "
      "ds = 0.00075, 2 kick nodes): 1200 shells, ds = 0.0005 and 4 kick nodes move the DK14 WL and galaxy r_sp/r200m by <= 5% "
      "(LCDM; the chain at H_Y's L0 and at L0 = 0.75 Mpc, where the outskirts are LCDM-like)",
      "; ".join(f"{k_}: {v_:.1%}" for k_, v_ in chg.items()), max(chg.values()) <= 0.05)
R.numbers["K6b"] = dict(runs=convb, change=chg)

# K7 realism (reported), production configuration
o_l = convb["LCDM|600|0.00075|2"]
ic_ = X.initial_profile(matched("lcdm", None, None, 600, 0.00075, 2, Mf0), zB, 600)
res_ = X.run_shells(ic_, X.build_particles(ic_, "lcdm"), z_obs=zB)
sps_ = X.snapshot_profiles(res_, {"all": np.ones_like(res_["sp"], bool), "bar": res_["sp"] == 0, "dark": res_["sp"] == 1})
Gam = (math.log(sps_[-1]["M200m_newt"]) - math.log(sps_[0]["M200m_newt"])) / (math.log(sps_[-1]["a"]) - math.log(sps_[0]["a"]))
more15 = 0.54 * (1 + 0.53 * float(X.Omm_a(1 / (1 + zB)))) * (1 + 1.36 * math.exp(-Gam / 3.04))
check("K7 (reported) LCDM REALISM: the model's 3D r_sp/r200m against More, Diemer & Kravtsov (2015) eq. (5) at the model's own "
      "Gamma (Delta ln M200m/Delta ln a over the window), and its DK14 WL r_sp/r200m against Shin et al. (2021)'s N-body 1.07",
      f"Gamma {Gam:.2f}: model 3D {o_l['x3']:.3f} vs More+15 {more15:.3f}; DK14 WL {o_l['xwl']:.3f} vs N-body 1.07",
      abs(o_l["x3"] / more15 - 1) < 0.15 and abs(o_l["xwl"] / 1.07 - 1) < 0.15, load_bearing=False)
R.numbers["K7"] = dict(Gamma=Gam, x3=o_l["x3"], more15=more15, xwl=o_l["xwl"], sim=1.07)

# ============================================================================================ K8 inputs
R.banner("K8  (reported) THE COMMITTED INPUTS")
F, Fb = fp10
zw, Ft = X.xr19_ftot("nominal")
P(f"    FP10 A6 budget (600 km/s, K = 185): F(z = 0/1/2/4) = {F[0]:.3f}/{np.interp(1, X.ZG_FP10, F):.3f}/{np.interp(2, X.ZG_FP10, F):.3f}/"
  f"{np.interp(4, X.ZG_FP10, F):.3f}; F_b = {Fb[0]:.3f}/{np.interp(1, X.ZG_FP10, Fb):.3f}/{np.interp(2, X.ZG_FP10, Fb):.3f}/{np.interp(4, X.ZG_FP10, Fb):.3f}")
P(f"    XR19 nominal F_tot(z = 0/1/2/3) = {np.interp(0, zw, Ft):.3f}/{np.interp(1, zw, Ft):.3f}/{np.interp(2, zw, Ft):.3f}/{np.interp(3, zw, Ft):.3f}")
hashes = {os.path.basename(p_): X.sha256(p_) for p_ in (X.FP10_JSON, X.XR19_WEB_JSON, X.XR19_FRONT_JSON)}
check("K8 (reported) the inputs are the committed files (sha256 recorded)", hashes, True, load_bearing=False)
R.numbers["K8"] = dict(hashes=hashes, F=F.tolist(), Fb=Fb.tolist(), Ftot=dict(z=zw.tolist(), F=Ft.tolist()))

sys.exit(R.finish())

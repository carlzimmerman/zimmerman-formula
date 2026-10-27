#!/usr/bin/env python3
"""CFG658 G-EFE (FROZEN_CRITERIA.md, 12c5ab6b3): the one-action construction C* (nu_s law + CFG691 stiffness at L* = 5.75 pc +
CFG693 free-fall basins) on
  E1  wide binaries: CFG447's injection into the frozen DR4 pipeline (imported read-only, sha256 checked), same seeds / DR3 numbers;
      (i) basin only (EFE-blind nu_s, = CFG447's nu_P2 row), (ii) C*: per-pair stiff-screened boost;
  E2  cluster satellites: CFG478 harness (cm14b parsing), satellite phantom counted only inside its free-fall basin edge r_J;
  E3  every star a node: CFG694 G3 with the saturating nonlinearity in CFG691's reduced equation.
MUTATE in the same pass: M-B (basin off -> CFG478 Q1; no stiffness -> CFG447 nu_P2), M-S (eps = 0 -> CFG694 G3 0.0352).
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg658_efe.py   -> cfg658_efe.out, cfg658_efe_results.json
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed."""
import os, sys, io, json, math, time, hashlib, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.integrate import solve_bvp
from scipy.optimize import brentq
from scipy.stats import chi2 as CHI2

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
T0 = time.time(); OUT, RES, CHK = [], {"lane": "CFG658", "gate": "EFE", "criteria": "12c5ab6b3"}, {}
try:
    os.nice(10)
except OSError:
    pass


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def check(name, ok, msg):
    CHK[name] = dict(ok=bool(ok), msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}"); return bool(ok)


def nu_s(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


Gsi, MSUN, PC = 6.6743e-11, 1.98847e30, 3.0856775814913673e16
LSTAR = json.load(open(os.path.join(LANES, "CFG691_stiffness_window", "cfg691_results.json")))["numbers"]["G_SS"]["canonical"]["Lmin_pc"]
P(__doc__.split("Run:")[0].strip())
P(f"\nL* = {LSTAR:.4g} pc (CFG691 L*_min, both footings)")


# ============================================================================ the stiff profile, cubic (eps = 0) and saturating
def profile(eps=0.0):
    """-[q'' + 2q'/s - 2q/s^2] + q|q|/(1 - eps q) = 1/s^2 in t = ln s (CFG691/694 equation at eps = 0; CFG694's BCs)."""
    def f(t, y):
        s = np.exp(t)
        return np.vstack([y[1], -y[1] + 2.0 * y[0] + s ** 2 * y[0] * np.abs(y[0]) / (1 - eps * y[0]) - 1.0])

    def bc(ya, yb):
        return np.array([ya[1] - (ya[0] - 0.5), yb[0] - (1e-4 - 1e-8)])

    t = np.linspace(math.log(1e-4), math.log(1e4), 4001); s = np.exp(t)
    return solve_bvp(f, bc, t, np.vstack([1 / (s + 2), -s / (s + 2) ** 2]), tol=1e-8, max_nodes=200000)


def S_from(sol):
    def S(s):
        s = float(s)
        if s < 1e-4: return 0.5 * s
        if s > 1e4: return 1 - 1 / s
        return s * float(sol.sol(math.log(s))[0])
    return S


SOL0 = profile(0.0); S0 = S_from(SOL0)
c691 = json.load(open(os.path.join(LANES, "CFG691_stiffness_window", "cfg691_results.json")))["numbers"]["profile"]["S_table"]
dS = max(abs(S0(float(k)) - v) for k, v in c691.items())
check("CONTROL cubic profile reproduces CFG691's S table (1e-6)", SOL0.status == 0 and dS <= 1e-6, f"status {SOL0.status}, max |dS| {dS:.1e}")


def g_an(r, M, a0, S=S0):
    ell = (LSTAR * PC) ** 2 / (2 * math.sqrt(Gsi * M / a0))
    return math.sqrt(Gsi * M * a0) / r * S(r / ell)


# ============================================================================ E3 every star a node
P("\n== E3  a star's own phantom inside min(r_J, 1.08 pc) at L* (CFG694 G3 statistic), saturating vacuum ==")
FOOT_A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
T_gal = 2.146e-10 / (8.18e3 * PC)                                                 # = CFG694 G3
E3 = {}
d_ms = 0.0
for f, a0 in FOOT_A0.items():
    for m in (1.0, 0.3):
        M = m * MSUN; rM = math.sqrt(Gsi * M / a0); ell = (LSTAR * PC) ** 2 / (2 * rM); eps = rM / ell
        solE = profile(eps); SE = S_from(solE)
        rJ = (Gsi * M / T_gal) ** (1 / 3); rb = min(rJ, 1.08 * PC)
        f0 = g_an(rb, M, a0, S0) * rb ** 2 / Gsi / M
        fe = g_an(rb, M, a0, SE) * rb ** 2 / Gsi / M
        E3[f"{f}|{m}"] = dict(eps=eps, status=int(solE.status), frac_cubic=f0, frac_sat=fe, rel_change=fe / f0 - 1, rb_pc=rb / PC,
                              u_over_a0_inner=g_an(1e-3 * ell, M, a0, SE) / a0)
        d_ms = max(d_ms, abs(f0 - 0.0352))
        P(f"  {f:9s} M = {m} Msun: eps = r_M/l_gamma = {eps:.2e} (solve_bvp {solE.status}); M_ph/M cubic {f0:.5f} -> saturating {fe:.5f} "
          f"(rel {fe / f0 - 1:+.1e}); inner u/a0 {E3[f'{f}|{m}']['u_over_a0_inner']:.2e}")
check("M-S eps = 0 reproduces CFG694 G3 0.0352 (1e-4)", d_ms < 1e-4, f"max |d| {d_ms:.1e}")
e3ok = all(v["status"] == 0 for v in E3.values())
e3 = "PASS" if (e3ok and all(v["frac_sat"] <= 0.155 for v in E3.values())) else ("OPEN" if not e3ok else "FAIL")
P(f"  E3 verdict (M_ph/M <= 0.155): {e3}")
RES["E3"] = dict(rows=E3, verdict=e3)

# ============================================================================ E2 satellites
P("\n== E2  Sifon satellites (CFG478 harness): own phantom only inside the free-fall basin edge r_J ==")
P478 = os.path.join(LANES, "CFG478_satellites_qumond_efe", "cfg478_qumond_efe.py")
s478 = open(P478).read()
N8 = {"__file__": P478, "__name__": "cfg478_ro"}
argv0 = sys.argv; sys.argv = [P478]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(s478[:s478.index("# controls")], P478, "exec"), N8)
sys.argv = argv0
mstar, mbg, rsat, Mh, G8, Msun8, Mpc8 = (N8[k] for k in ("mstar", "mbg", "rsat", "Mh", "G", "Msun", "Mpc"))
rho_h, mph_exact, KER8 = N8["rho_h"], N8["mph_exact"], N8["KER"]
J478 = json.load(open(os.path.join(LANES, "CFG478_satellites_qumond_efe", "cfg478_qumond_efe_results.json")))["res"]


def sat_rows(foot, a0, nu, mode):
    """mode: 'Q1' basin off (host field as cm14b), 'iso' isolated (r_J -> inf), 'basin' C* rule."""
    pulls, boosts, need, info = [], [], [], []
    for lm, (lmb, elo, ehi), R in zip(mstar, mbg, rsat):
        Ms = 10 ** lm; Mb = 1.2 * Ms; ret = 0.13 * (0.1200 / 0.02237) * Mb; mb = 10 ** lmb
        rbg = (mb / (4 * math.pi * rho_h(R))) ** (1 / 3)                         # Mpc (harness)
        if mode == "Q1":
            ge = G8 * Mh(R) * Msun8 / (R * Mpc8) ** 2
            Mph = mph_exact(Mb * Msun8, rbg * Mpc8, ge, a0, nu) / Msun8; rJ = float("nan")
        else:
            dl = 1e-4
            slope = (math.log(Mh(R * (1 + dl))) - math.log(Mh(R * (1 - dl)))) / (math.log(1 + dl) - math.log(1 - dl))
            T = G8 * Mh(R) * Msun8 / (R * Mpc8) ** 3 * (2 - slope)
            gs = lambda r: float(nu(G8 * Mb * Msun8 / r ** 2 / a0)) * G8 * Mb * Msun8 / r ** 2
            rJ = math.exp(brentq(lambda lr: math.log(gs(math.exp(lr))) - math.log(T * math.exp(lr)), math.log(1e17), math.log(1e24))) / Mpc8
            reff = rbg if mode == "iso" else min(rbg, rJ)
            r_ = reff * Mpc8
            Mph = (float(nu(G8 * Mb * Msun8 / r_ ** 2 / a0)) - 1) * Mb
            info.append(dict(R=R, slope_alpha=3 - slope, rJ_kpc=rJ * 1e3, rbg_kpc=rbg * 1e3, rJ_over_rbg=rJ / rbg))
        Mtot = Mb + Mph + ret
        sig = 0.5 * (elo + ehi); pulls.append((lmb - math.log10(Mtot)) / sig)
        boosts.append((Mtot - ret) / Mb); need.append((mb - ret) / Mb)
    z = np.array(pulls); X2 = float((z ** 2).sum())
    return dict(chi2=X2, p=float(CHI2.sf(X2, 5)), pulls=z.tolist(), boost=boosts, need=need, info=info)


dq = 0.0
for foot, a0 in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
    for kn, nu in KER8.items():
        rr = sat_rows(foot, a0, nu, "Q1"); dq = max(dq, abs(rr["chi2"] - J478[f"{foot}|{kn}|Q1"]["chi2"]))
check("M-B basin off: CFG478 Q1 chi2 reproduced with its own kernels (P2, nu_mono; 0.05)", dq < 0.05, f"max |d| {dq:.1e}")
E2 = {}
for foot, a0 in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
    for mode in ("Q1", "iso", "basin"):
        rr = sat_rows(foot, a0, nu_s, mode); E2[f"{foot}|{mode}"] = rr
        P(f"  {foot:9s} nu_s {mode:5s}: chi2 {rr['chi2']:6.1f}/5 p {rr['p']:.2g} | boost {np.round(rr['boost'], 2).tolist()} vs needed "
          f"{np.round(rr['need'], 1).tolist()}")
        if mode == "basin":
            P("        r_J/r_bg " + str([round(x["rJ_over_rbg"], 2) for x in rr["info"]]) + "; host slope alpha "
              + str([round(x["slope_alpha"], 2) for x in rr["info"]]) + "; r_bg kpc " + str([round(x["rbg_kpc"]) for x in rr["info"]]))
# stiffness re-check (CFG694 G4 statistic at the satellites' own masses and r_bg)
Smin = 1.0
for foot, a0 in FOOT_A0.items():
    for lm, (lmb, elo, ehi), R in zip(mstar, mbg, rsat):
        Mb = 1.2 * 10 ** lm * MSUN; rbg = (10 ** lmb / (4 * math.pi * rho_h(R))) ** (1 / 3) * 3.0857e22
        ell = (LSTAR * PC) ** 2 / (2 * math.sqrt(Gsi * Mb / a0)); Smin = min(Smin, S0(rbg / ell))
check("stiffness leaves the satellites unscreened (S >= 0.99 at r_bg; CFG694 G4 re-check)", Smin >= 0.99, f"min S {Smin:.6f}")
e2 = "PASS" if all(E2[f"{f}|basin"]["p"] > 0.01 for f in FOOT_A0) else "FAIL"
P(f"  E2 verdict (basin rule, p > 0.01 both footings): {e2}")
RES["E2"] = dict(rows=E2, verdict=e2, S_min=Smin)

# ============================================================================ E1 wide binaries
P("\n== E1  wide binaries: CFG447 injections into the frozen DR4 pipeline (read-only) ==")
P447 = os.path.join(LANES, "CFG447_efe_blind_force_vs_dr3", "cfg447_efe_blind.py")
s447 = open(P447).read()
PIPE = os.path.join(REPO, "prep_2026", "gaia_dr4_prep", "wide_binary_pipeline.py")
sha_rec = "7c884e0e0a4cb9cb"
N7 = {"__file__": P447, "__name__": "cfg447_ro"}
argv0 = sys.argv; sys.argv = [P447]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(s447[:s447.index("seeds = list(range(47001, 47011)); res = {}")], P447, "exec"), N7)
sys.argv = argv0
Wp, recover, DR3 = N7["W"], N7["recover"], N7["DR3"]
seeds = list(range(47001, 47011))
check("K2 pipeline sha256 matches CFG447's record", N7["sha0"].startswith(sha_rec), N7["sha0"][:16])


def vt_gam(pop, gam):
    vX = (gam * pop["pmx"] + pop["npmx"]) * 4.74e3 * (pop["d_obs"] / 1000.)
    vY = (gam * pop["pmy"] + pop["npmy"]) * 4.74e3 * (pop["d_obs"] / 1000.)
    return np.hypot(vX, vY) / pop["vc_obs"]


def stiff_vt(pd, a0):
    M = pd["M_obs"] * Wp.MSUN; r = np.sqrt(Wp.G * M / pd["g_true"])
    ratio = np.array([g_an(ri, Mi, a0) for ri, Mi in zip(r, M)]) / pd["g_true"]
    stiff_vt.maxratio = max(getattr(stiff_vt, "maxratio", 0.0), float(ratio.max()))
    return vt_gam(pd, np.sqrt(1 + ratio))


J447 = json.load(open(os.path.join(LANES, "CFG447_efe_blind_force_vs_dr3", "cfg447_efe_blind_results.json")))["res"]
E1 = {}
dmb = 0.0
for foot in ("canonical", "alt"):
    for cell, fun in (("basin_only", lambda pd, a0: vt_gam(pd, np.sqrt(nu_s(pd["g_true"] / a0)))), ("Cstar", stiff_vt)):
        g = recover(fun, foot, seeds)
        med, spr = float(np.median(g)), float(np.std(g))
        _, gb, sb, gl, sl = DR3[foot]
        zb = (med - gb) / np.hypot(sb, spr); zl = (med - gl) / np.hypot(sl, spr)
        v = "EXCLUDED BY DR3" if zb > 5 else ("CONSISTENT" if abs(zb) < 2 else "NOT EXCLUDED")
        E1[f"{foot}|{cell}"] = dict(median=med, spread=spr, gammas=g.tolist(), z_builder=float(zb), z_literal=float(zl), label=v)
        if cell == "basin_only":
            dmb = max(dmb, abs(med - J447[f"nu_P2|{foot}"]["median"]), abs(zb - J447[f"nu_P2|{foot}"]["z_builder"]))
        P(f"  {foot:9s} {cell:10s}: gamma_hat median {med:.4f} (spread {spr:.4f}) | vs DR3 builder {gb} +- {sb}: {zb:+.2f} sigma "
          f"(literal {zl:+.2f}) -> {v}")
P(f"  C* per-pair anomaly/Newton max over all injected pairs: {getattr(stiff_vt, 'maxratio', float('nan')):.2e}")
check("M-B no stiffness (basin only) reproduces CFG447's nu_P2 rows (median and z, 0.05)", dmb < 0.05, f"max |d| {dmb:.1e}")
e1 = "CONSISTENT" if all(E1[f"{f}|Cstar"]["label"] == "CONSISTENT" for f in ("canonical", "alt")) else \
    ("EXCLUDED" if all(E1[f"{f}|Cstar"]["label"] == "EXCLUDED BY DR3" for f in ("canonical", "alt")) else "NOT EXCLUDED / MIXED")
P(f"  E1 verdict (C*: basin + stiffness): {e1}")
RES["E1"] = dict(rows=E1, verdict=e1, maxratio=getattr(stiff_vt, "maxratio", None))

RES["checks"] = CHK; RES["elapsed_s"] = time.time() - T0
json.dump(RES, open(os.path.join(HERE, "cfg658_efe_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg658_efe.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(v["ok"] for v in CHK.values()) else 1)

#!/usr/bin/env python3
"""C2b: AeST source verification (P1-P3) and a vanilla-CLASS emulation of G_cosmo = g G_N vs plik-lite + low-l (P4-P5).

Criteria: FROZEN_CRITERIA.md, AMENDMENT A2 (pre-result).  Run with:  OMP_NUM_THREADS=1 nice -n 10 python3 -I c2b_native_cmb.py
(C2B_MUTATE=1 for the mutation).  Reads downloaded data only with numpy; executes no downloaded code.
P4/P5 are an EMULATION of the background ratio g, NOT the AeST prediction.  kappa = 1/2 FITTED.
"""
import os, sys, json, re, math
import numpy as np
import sympy as sp
from scipy.io import FortranFile
from scipy.interpolate import InterpolatedUnivariateSpline
from classy import Class

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
MUT = os.environ.get("C2B_MUTATE", "") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"c2b_native_cmb{TAG}.out"), "w")
RES, CHK = {"mutate": MUT}, []


def P(s=""):
    print(s, flush=True); OUT.write(s + "\n"); OUT.flush()


def check(k, ok, val, thr):
    CHK.append((k, bool(ok)))
    P(f"{k} {'PASS' if ok else 'FAIL'} {val} {thr}")


def norm(s):
    return re.sub(r"\s+", "", s)


# ---------------------------------------------------------------- P1: verify against the sources
P("== P1: AeST source verification (arXiv:2007.00082 newRMONDLett.tex; arXiv:2304.05134 main.tex)")
PRL = norm(open(os.path.join(EXT, "aest_papers_2026_10_22", "src_2007.00082", "newRMONDLett.tex")).read())
VSZ = norm(open(os.path.join(EXT, "aest_papers_2026_10_22", "src_2304.05134", "main.tex")).read())
snip = {
    "action Eq.5: R - K_B/2 F^2 + 2(2-K_B) J.dphi - (2-K_B) Y - F(Y,Q) - lambda(A.A+1)":
        (PRL, r"R-\frac{\KB}{2}\Fh^{\mu\nu}\Fh_{\mu\nu}+2(2-\KB)\Jh^\mu\nabla_\mu\phi\nonumber\\&-(2-\KB)\Ycal-\Fcal(\Ycal,\Qcal)-\lambda(\Ah^\mu\Ah_\mu+1)"),
    "J_mu = A^alpha nabla_alpha A_mu (aether acceleration)": (PRL, r"\Jh_\mu=\Ah^\alpha\nabla_\alpha\Ah_\mu"),
    "Q = A^mu d_mu phi, Y = q^{mu nu} d phi d phi": (PRL, r"$\Qcal=\Ah^\mu\nabla_\mu\phi$and$\Ycal=q^{\mu\nu}\nabla_\mu\phi\nabla_\nu\phi$"),
    "K(Qbar) = -1/2 F(0,Qbar)": (PRL, r"\Kcal(\Qcalb)=-\frac{1}{2}\Fcal(0,\Qcalb)"),
    "J -> 2 lambda_s/(3(1+lambda_s) a0) Y^{3/2}": (PRL, r"\Jcal\rightarrow\frac{2\lambdas}{3(1+\lambdas)a_0}\Ycal^{3/2}"),
    "Gt = (1 - K_B/2) G_qs": (PRL, r"\Gt=(1-\frac{\KB}{2})\Gqs"),
    "G_N = (1 + 1/lambda_s) G_qs (tracking; screening = lambda_s -> inf)": (PRL, r"\GN=(1+1/\lambdas)\Gqs"),
    "mu = sqrt(2 K2/(2-K_B)) Q0": (PRL, r"\mu=\sqrt{\frac{2\Kcal_2}{2-\KB}}\Qcal_0"),
    "vectors healthy if 0<K_B<2 and lambda_s>-1": (PRL, r"healthyif$0<\KB<2$and$\lambdas>-1$"),
    "scalar requires K2>0": (PRL, r"werequirethat$\Kcal_2>0$"),
    "omega=0 mode requires lambda_s>0": (PRL, r"alsorequiringthat$\lambdas>0$"),
    "lambda_s influences the effective cosmological gravitational strength": (PRL, r"$\lambdas$(influencingtheeffectivecosmologicalgravitationalstrength)"),
    "VSZ: G_qs = G_N/(1+beta_0)": (VSZ, r"\frac{4\pi\GN}{1+\beta_0}\rho_b"),
    "VSZ: lambda_s = 1/beta_0": (VSZ, r"\lambdas\equiv1/\beta_0"),
    "VSZ: Minkowski stability lambda_s>0, mu^2>0": (VSZ, r"imposes$\lambdas>0$and$\mu^2>0$"),
}
p1 = {}
for k, (src, s) in snip.items():
    p1[k] = norm(s) in src
    P(f"  {'found  ' if p1[k] else 'MISSING'} {k}")
disc = [
    "real_research/bridge1_aest_equations.md: matches the source on every load-bearing item checked (action, lambda_s "
    "coefficient, Gt = (1-K_B/2) G_qs, mu, the E equation); it omits J_mu = A^a nabla_a A_mu and K = -F(0,Q)/2 (omissions, not errors).",
    "real_research/THE_NEXT_CALCULATION_aest_quasistatic.md: writes F(Y,Q) = -K(Q) + ...; the source has F(0,Q) = -2 K(Q) "
    "(K = -F(0,Q)/2, PRL text after Eq. 5).",
    "C1 (covariant_push_2026_10_22/C1_aest_embedding/README.md, point 1): takes the mass term as K2 Q0^2 Psi^2 in "
    "16 pi Gt L, m^2 = K2 Q0^2/(2-K_B), and calls the record's 2K2 'a convention'. With K = -F(0,Q)/2 the source fixes "
    "(2-K_B) mu^2 = 2 K2 Q0^2 (Eq. 6): C1's m^2 is mu^2/2 (a factor-2 slip in C1; it touches only the Mpc-scale mass "
    "term, not C1's verdict).",
    "C1 K2: G_N = 2 Gt/(2-K_B) at lambda_s -> inf agrees with the source; the 'Newtonian regime as a cap' is the screening "
    "limit lambda_s -> inf, which the source equates with screening.",
]
for d in disc:
    P("  discrepancy/note: " + d)
check("P1", all(p1.values()), f"{sum(p1.values())}/{len(p1)} found", "all found")
RES["P1"] = dict(found=p1, discrepancies=disc)

# ---------------------------------------------------------------- P2: g = Gt/G_N and the BBN bounds
P("== P2: G_cosmo/G_N in AeST and the A78 BBN line g > 0.9611")
KB, ls, Gq = sp.symbols("K_B lambda_s G_qs", positive=True)
Gt = (1 - KB / 2) * Gq
GN = Gq if MUT else (1 + 1 / ls) * Gq                                # mutation: drop the lambda_s factor
g_expr = sp.simplify(Gt / GN)
res2 = sp.simplify(g_expr - (1 - KB / 2) * ls / (1 + ls))
GMIN = 0.9611
g_inf = sp.limit(g_expr, ls, sp.oo)
kb_max = float(sp.solve(sp.Eq(g_inf, GMIN), KB)[0])
sol_ls = sp.solve(sp.Eq(g_expr.subs(KB, 0), GMIN), ls)
ls_min = float(sol_ls[0]) if sol_ls else float("nan")
P(f"  g = Gt/G_N = {g_expr};  residual vs (1-K_B/2) lambda_s/(1+lambda_s) = {res2}")
P(f"  BBN: K_B < {kb_max:.4f} (lambda_s -> inf), lambda_s > {ls_min:.3f} (K_B -> 0); jointly (1-K_B/2) lambda_s/(1+lambda_s) > {GMIN}")
gl = {lv: float((1 - 0) * lv / (1 + lv)) for lv in (1, 2, 10)}
P(f"  VSZ's plotted lambda_s = 1, 2, 10 give g <= {gl[1]:.3f}, {gl[2]:.3f}, {gl[10]:.3f} (Delta N_eff = "
  f"{7.4492 * (gl[1] - 1):.2f}, {7.4492 * (gl[2] - 1):.2f}, {7.4492 * (gl[10] - 1):.2f}; A78 line |Delta N_eff| < 0.30); "
  f"SZ's CMB 'MOND models' have lambda_s = inf")
ok2 = res2 == 0 and abs(kb_max - 0.0778) < 1e-3 and abs(ls_min - 24.71) < 1e-2
check("P2", ok2, f"res={res2},KB<{kb_max:.4f},ls>{ls_min:.3f}", "0, 0.0778, 24.71")
RES["P2"] = dict(g=str(g_expr), KB_max=kb_max, lambda_s_min=ls_min, g_at_lambda_s=gl,
                 dNeff_at_lambda_s={k: 7.4492 * (v - 1) for k, v in gl.items()},
                 H0_statement="H0_native = sqrt(g) H0_GR with g <= 1 always (0<K_B<2, lambda_s>0): AeST can only lower H0")

# ---------------------------------------------------------------- P3: growth feels Gt
P("== P3: which G does linear growth feel")
d_def = norm(r"\frac{1}{8\pi\Gt a^2\rhob}\grad^2\left[\KB\Ealp+\left(2-\KB\right)\chi\right]") in PRL
gr_form = norm(r"theEinsteinequationstakethesameformasinGR") in PRL
P(f"  delta normalised with Gt: {d_def};  Einstein equations in GR form: {gr_form}  (the PRL writes '8 pi G' there; with "
  f"the action normalised by 1/16 pi Gt and delta defined with Gt, that G is Gt)")
P("  => linear growth is sourced by Gt = G_cosmo; K7's G_N variant (+16 % sigma8) is NOT AeST's linear behaviour: withdrawn")
check("P3", d_def and gr_form, f"{d_def},{gr_form}", "True,True")
RES["P3"] = dict(delta_uses_Gt=d_def, einstein_GR_form=gr_form, K7_variant="withdrawn")

# ---------------------------------------------------------------- likelihoods (reimplemented; data read with numpy)
PK = os.path.join(EXT, "cobaya_2026_10_22", "packages", "data")
pl = os.path.join(PK, "planck_2018_pliklite_native")
dat = np.loadtxt(os.path.join(pl, "cl_cmb_plik_v22.dat"))
blmin = np.loadtxt(os.path.join(pl, "blmin.dat")).astype(int) + 30
blmax = np.loadtxt(os.path.join(pl, "blmax.dat")).astype(int) + 30
w = np.loadtxt(os.path.join(pl, "bweight.dat"))
lsw = np.arange(len(w)) + 30
w = np.hstack((np.zeros(30), w * 2 * np.pi / lsw / (lsw + 1)))
NB = (215, 199, 199)
cov = FortranFile(os.path.join(pl, "c_matrix_plik_v22.dat"), "r").read_reals(dtype=float).reshape((613, 613))
cov = np.tril(cov) + np.tril(cov, -1).T
Lc = np.linalg.cholesky(cov)
Xd = dat[:, 1]
lt = os.path.join(PK, "planck_2018_lowT_native")
covT = np.loadtxt(os.path.join(lt, "cov.txt"))[0:28, 0:28]
cinvT = np.linalg.inv(covT)
muT = np.loadtxt(os.path.join(lt, "mu.txt"))[0:28]
musig = np.zeros(30); musig[2:] = np.loadtxt(os.path.join(lt, "mu_sigma.txt"))[0:28]
s1 = np.loadtxt(os.path.join(lt, "cl2x_1.txt"))[:, 0:28]
s2 = np.loadtxt(os.path.join(lt, "cl2x_2.txt"))[:, 0:28]
spl, dspl, bnd = [], [], np.zeros((28, 2))
for i in range(28):
    j = 0
    while abs(s2[j, i] + 5) < 1e-4:
        j += 1
    bnd[i, 0] = s1[j + 2, i]
    j = s1.shape[0] - 1
    while abs(s2[j, i] - 5) < 1e-4:
        j -= 1
    bnd[i, 1] = s1[j - 2, i]
    spl.append(InterpolatedUnivariateSpline(s1[:, i], s2[:, i])); dspl.append(spl[-1].derivative())
probEE = np.loadtxt(os.path.join(PK, "planck_2018_lowE_native", "prob_table.txt"))


def lowTT_logl_raw(tt, A=1.0):
    th = tt[2:30] / A**2
    if np.any(th < bnd[:, 0]) or np.any(th > bnd[:, 1]):
        return -np.inf
    lg, x = 0.0, np.zeros(28)
    for i in range(28):
        dd = dspl[i](th[i])
        if dd < 0:
            return -np.inf
        lg += math.log(dd); x[i] = spl[i](th[i])
    dlt = x - muT
    return lg - 0.5 * dlt @ cinvT @ dlt


OFFT = lowTT_logl_raw(musig)


def chi2_lowTT(tt, A=1.0):
    return -2 * (lowTT_logl_raw(tt, A) - OFFT)


def chi2_lowEE(ee, A=1.0):
    idx = (ee[2:30] / (A**2 * 1e-4)).astype(int)
    if np.any(idx < 0) or np.any(idx >= probEE.shape[0]):
        return np.inf
    return -2 * float(np.take_along_axis(probEE, idx[np.newaxis, :], 0).sum())


def binned(tt, te, ee):
    out = []
    for cell, nb in zip((tt, te, ee), NB):
        for i in range(nb):
            out.append(np.dot(cell[blmin[i]:blmax[i] + 1], w[blmin[i]:blmax[i] + 1]))
    return np.array(out)


def chi2_plik(Tb, A=1.0):
    r = np.linalg.solve(Lc, Xd - Tb / A**2)
    return float(r @ r)


# ---------------------------------------------------------------- CLASS emulation of G_cosmo = g G_N
NG = 1 / 0.22711
RUNS = [0]


def run_class(p, g=1.0, lmax=2508, lens=True, theta=True, h=None):
    """p = (omega_b, omega_c, 100theta_s, lnAs, n_s, tau): physical densities. Emulation: baryons physical (microphysics),
    gravitating densities scaled by g via CDM and N_ur compensation (A2)."""
    wb, wc, th, lnA, ns, tau = p
    nur = 3.044 if MUT else g * (NG + 3.044) - NG
    pars = {"omega_b": wb, "omega_cdm": g * wc - (1 - g) * wb, "N_ur": nur, "T_cmb": 2.7255,
            "ln10^{10}A_s": lnA, "n_s": ns, "tau_reio": tau, "output": "tCl,pCl,lCl" if lens else "tCl,pCl",
            "l_max_scalars": lmax}
    if lens:
        pars["lensing"] = "yes"
    if theta:
        pars["100*theta_s"] = th
    else:
        pars["h"] = h
    c = Class(); c.set(pars); c.compute(); RUNS[0] += 1
    cl = c.lensed_cl(lmax) if lens else c.raw_cl(lmax)
    ell = cl["ell"]; f = ell * (ell + 1) / 2 / np.pi * (2.7255e6)**2
    out = dict(tt=cl["tt"] * f, te=cl["te"] * f, ee=cl["ee"] * f, h=c.h(),
               theta_s=c.get_current_derived_parameters(["100*theta_s"])["100*theta_s"],
               zstar=c.get_current_derived_parameters(["z_star"])["z_star"])
    c.struct_cleanup(); c.empty()
    return out


# ---------------------------------------------------------------- P4: acoustic scale vs g at fixed physical densities
P("== P4: acoustic scale under the emulated g (fixed physical densities, h = sqrt(g) h_1)  [EMULATION, not AeST]")
p0 = np.array([0.02237, 0.1200, 1.04110, 3.044, 0.9649, 0.0544])          # starting point only (Planck 2018 base values)
r1 = run_class(p0, 1.0, lmax=50, lens=False)
h1 = r1["h"]
rg = run_class(p0, 0.9611, lmax=50, lens=False, theta=False, h=math.sqrt(0.9611) * h1)
dth = rg["theta_s"] / r1["theta_s"] - 1
P(f"  g=1: 100theta_s={r1['theta_s']:.6f}, z*={r1['zstar']:.2f}, h={h1:.5f};  g=0.9611: 100theta_s={rg['theta_s']:.6f}, "
  f"z*={rg['zstar']:.2f}, h={math.sqrt(0.9611) * h1:.5f};  dtheta/theta = {dth:.2e}")
check("P4", abs(dth) < 1e-3, f"{dth:.2e}", "|dtheta/theta|<1e-3")
RES["P4"] = dict(theta1=r1["theta_s"], theta_g=rg["theta_s"], zstar1=r1["zstar"], zstar_g=rg["zstar"], dtheta=dth)

# ---------------------------------------------------------------- P5: plik-lite + low-l, refit, Fisher sigma(g), profile
P("== P5: plik-lite TTTEEE + low-l TT + low-l EE (reimplemented)  [EMULATION of g, NOT the AeST prediction]")
# native tau prior from low-l at fixed A_s e^{-2 tau}
taus = np.arange(0.035, 0.0801, 0.0075)
c2l = []
for t in taus:
    pp = p0.copy(); pp[5] = t; pp[3] = p0[3] + 2 * (t - p0[5])
    rr = run_class(pp, 1.0, lmax=40, lens=False)
    c2l.append(chi2_lowTT(rr["tt"]) + chi2_lowEE(rr["ee"]))
c2l = np.array(c2l)
cf = np.polyfit(taus, c2l, 2)
tau_hat, sig_tau = -cf[1] / (2 * cf[0]), 1 / math.sqrt(cf[0])
P(f"  low-l tau scan: tau_hat = {tau_hat:.4f} +- {sig_tau:.4f} (parabola over {len(taus)} points)")
STEP = np.array([1e-4, 1e-3, 2e-4, 0.01, 0.004, 0.004])


def theory(p, g):
    r = run_class(p, g)
    return binned(r["tt"], r["te"], r["ee"]), r


def resid(Tb, A, tau):
    return np.concatenate((np.linalg.solve(Lc, Xd - Tb / A**2), [(A - 1) / 0.0025, (tau - tau_hat) / sig_tau]))


def total_chi2(p, A, g):
    Tb, r = theory(p, g)
    c = dict(plik=chi2_plik(Tb, A), lowTT=chi2_lowTT(r["tt"], A), lowEE=chi2_lowEE(r["ee"], A), Aprior=((A - 1) / 0.0025)**2)
    c["total"] = sum(c.values()); c["H0"] = 100 * r["h"]
    return c


def jac(p, A, g, Tb):
    J = np.zeros((613 + 2, 7))
    for k in range(6):
        pp = p.copy(); pp[k] += STEP[k]
        Tk, _ = theory(pp, g)
        J[:613, k] = -np.linalg.solve(Lc, (Tk - Tb) / A**2) / STEP[k]
    J[613 + 1, 5] = 1 / sig_tau
    J[:613, 6] = np.linalg.solve(Lc, 2 * Tb / A**3)
    J[613, 6] = 1 / 0.0025
    return J


def gauss_newton(p, A, g, nit=4):
    for it in range(nit):
        Tb, _ = theory(p, g)
        r = resid(Tb, A, p[5]); c0 = r @ r
        J = jac(p, A, g, Tb)
        d = -np.linalg.lstsq(J, r, rcond=None)[0]
        lam = 1.0
        while lam > 1 / 16:
            pn, An = p + lam * d[:6], A + lam * d[6]
            Tn, _ = theory(pn, g)
            cn = resid(Tn, An, pn[5]) @ resid(Tn, An, pn[5])
            if cn <= c0:
                break
            lam /= 2
        p, A = pn, An
        P(f"    g={g}: GN it{it + 1}: steered chi2 {c0:.2f} -> {cn:.2f} (step {lam})")
    return p, A, J


pF, AF, JF = gauss_newton(p0.copy(), 1.0, 1.0)
cF = total_chi2(pF, AF, 1.0)
P(f"  LCDM refit (g=1): params {np.round(pF, 5).tolist()}, A_planck {AF:.5f}; chi2 {json.dumps({k: round(v, 2) for k, v in cF.items()})}")
# Fisher sigma(g)
Tp, _ = theory(pF, 1.01); Tm, _ = theory(pF, 0.99)
Jg = np.zeros(613 + 2); Jg[:613] = -np.linalg.solve(Lc, (Tp - Tm) / AF**2) / 0.02
Jfull = np.column_stack((JF, Jg))
Fm = Jfull.T @ Jfull
sig_g = math.sqrt(np.linalg.inv(Fm)[7, 7])
sig_g_fixed = 1 / math.sqrt(Fm[7, 7])
P(f"  Fisher (plik-lite + tau prior + A prior): sigma(g) = {sig_g:.4f} marginalised over 6 LCDM + A_planck "
  f"({sig_g_fixed:.4f} with the others fixed)")
prof = {}
for gv in (0.9611, 0.6845):
    pg, Ag, _ = gauss_newton(pF.copy(), AF, gv)
    cg = total_chi2(pg, Ag, gv)
    prof[str(gv)] = dict(params=pg.tolist(), A=Ag, chi2=cg, dchi2=cg["total"] - cF["total"])
    P(f"  g={gv}: refit {np.round(pg, 5).tolist()}, H0={cg['H0']:.2f}; chi2 {json.dumps({k: round(v, 2) for k, v in cg.items()})}; "
      f"Delta chi2 = {cg['total'] - cF['total']:+.2f}")
ok5 = 500 <= cF["plik"] <= 750
check("P5", ok5, f"chi2_plik={cF['plik']:.1f}", "in [500,750] for 613 bins")
d684, d961 = prof["0.6845"]["dchi2"], prof["0.9611"]["dchi2"]
P(f"  outcome: g=0.6845 {'DISFAVOURED (Delta chi2 > 25)' if d684 > 25 else 'not disfavoured at 5 sigma'} in this emulation; "
  f"BBN band edge g=0.9611 {'not distinguishable (Delta chi2 < 4)' if d961 < 4 else 'distinguishable'}; neither is an AeST verdict")
RES["P5"] = dict(tau_hat=tau_hat, sig_tau=sig_tau, lcdm_refit=dict(params=pF.tolist(), A=AF, chi2=cF), sigma_g=sig_g,
                 sigma_g_fixed=sig_g_fixed, profile=prof, class_runs=RUNS[0],
                 limits="emulation: background and recombination exact for G_cosmo = g G_N; per-species Poisson weights and "
                        "neutrino shear off by O(1-g) (about 6 % of nu shear at g = 0.961, about 45 % at 0.6845); "
                        "likelihoods reimplemented from data files, not validated against cobaya's own output")

npass = sum(ok for _, ok in CHK)
P(f"C2B_NATIVE_CMB COMPLETE: {npass}/{len(CHK)} checks PASS.  (CLASS runs: {RUNS[0]})")
RES["checks"] = dict(CHK)
json.dump(RES, open(os.path.join(HERE, f"c2b_native_cmb_results{TAG}.json"), "w"), indent=1, default=str)
OUT.close()
sys.exit(0 if npass == len(CHK) else 1)

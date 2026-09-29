# -*- coding: utf-8 -*-
"""CFG172 A4 -- G2 (growth) for 11C-a, -b, -c, cold component ON.  Frozen: sec. 2 (G2).
Around FRW the a-channel has mu(y -> 0) -> 0: the quadratic action for Phi vanishes (strong coupling), so linear growth is ILL-DEFINED for 11C-a/-c (and
for 11C-b where the branch is reached).  Declared scoring: the nonlinear quasi-static estimate G_eff/G = g/g_N = nu(y_lin) with y_lin = (3/2) Omega_m(z) H(z)^2 delta / (k_phys a0),
delta = 1 sigma / 3 sigma of the linear LCDM field (BBKS transfer, sigma_8 = 0.811 normalised; a crude reference, no Boltzmann code) capped at 1, and delta = 1.
Pass iff max |G_eff/G - 1| <= 5% over k in {0.1,0.3,1,3,10,30}/Mpc, z in {0,0.5,1,2,3,10,30,1000}.  The CMB part is UNDEFINED (no perturbation solver).
11C-b: F evaluated at the operating point t = K_bg/K_0 (declared Newtonian continuation below the branch point); background G_cos/G_N = (2-c14)/(2+3c2) added.
MUTATE = M2 (kernel -> GR): G2 must recover PASS (the flow then does nothing)."""
from scipy.integrate import quad
from cfg172_common import *

R = Run("CFG172_A4_growth")
mut = R.mut
Om, h, Ob = OM, HH, OB_H2 / HH ** 2
E2 = lambda z: Om * (1 + z) ** 3 + OL
def Dg(z):
    Ez = math.sqrt(E2(z))
    return 2.5 * Om * Ez * quad(lambda zz: (1 + zz) / E2(zz) ** 1.5, z, np.inf)[0]
D0 = Dg(0.0)
Gam = Om * h * math.exp(-Ob * (1 + math.sqrt(2 * h) / Om))
def T(k_mpc):
    q = k_mpc / h / Gam
    return np.log(1 + 2.34 * q) / (2.34 * q) * (1 + 3.89 * q + (16.1 * q) ** 2 + (5.46 * q) ** 3 + (6.71 * q) ** 4) ** -0.25
def Pk_unnorm(k): return k ** 0.9649 * T(k) ** 2
kk = np.logspace(-4, 2, 4000)
Rk = 8.0 / h
W = lambda kR: 3 * (np.sin(kR) - kR * np.cos(kR)) / kR ** 3
s8 = 0.811
sig2 = np.trapz(kk ** 2 * Pk_unnorm(kk) * W(kk * Rk) ** 2 / (2 * math.pi ** 2), kk)
Anorm = s8 ** 2 / sig2
delta_rms = lambda k: math.sqrt(Anorm * k ** 3 * Pk_unnorm(k) / (2 * math.pi ** 2))
R.check("G2.0 reference: sigma_8 normalisation reproduces 0.811; Delta_rms(k=1/Mpc) is O(1)", f"Delta(1/Mpc)={delta_rms(1.0):.2f}, Delta(0.1/Mpc)={delta_rms(0.1):.2f}, D0={D0:.3f}", 0.5 < delta_rms(1.0) < 3)

KS = [0.1, 0.3, 1, 3, 10, 30]
ZS = [0, 0.5, 1, 2, 3, 10, 30, 1000]
MPC = 3.0856775814913673e22
qP2 = lambda yv: 1.0 - (math.sqrt(1 + 4 * yv * yv) - 1) / (2 * yv)

def geff_over_G(yN, t_off=None, gr=False):
    """G_eff/G = y_g / y_N with mu_eff(y_g) y_g = y_N; mu_eff = 1 - q(sqrt(y_g^2 - t)) for y_g^2 > t else 1."""
    if gr:
        return 1.0
    if t_off is None:
        return float(nu_p2(yN))
    f = lambda ly: (1.0 - (qP2(math.sqrt(math.exp(2 * ly) - t_off)) if math.exp(2 * ly) > t_off else 0.0)) * math.exp(ly) - yN
    lo = math.log(yN) - 1e-12
    hi = math.log(yN) + 40
    if f(lo) >= 0:
        return 1.0
    return math.exp(brentq(f, lo, hi, xtol=1e-13)) / yN

def table(t_off=None, gr=False, a0=A0_SI["canonical"]):
    out = {}
    worst = 0.0
    for z in ZS:
        Ez2 = E2(z)
        for k in KS:
            kphys = k * (1 + z) / MPC
            Omz = Om * (1 + z) ** 3 / Ez2
            H2 = (H0_SI ** 2) * Ez2
            dl = min(1.0, delta_rms(k) * Dg(z) / D0)
            for nm, dv in (("1sigma", dl), ("3sigma", min(1.0, 3 * dl)), ("delta=1", 1.0)):
                yN = 1.5 * Omz * H2 * dv / (kphys * a0)
                ge = geff_over_G(yN, t_off, gr)
                out[f"z={z}/k={k}/{nm}"] = ge - 1.0
                if nm == "1sigma":
                    worst = max(worst, abs(ge - 1.0))
    return out, worst

res = {}
for nm, kw in (("11C-a/-c (P2)", {}), ("11C-b t=1.2e-6 (largest offset where G1 passes, A6)", {"t_off": 1.2e-6}), ("11C-b t=1 (rule-T tie)", {"t_off": 1.0}), ("11C-b t=4.0e6 (G6/G7-allowed corner)", {"t_off": 4.04e6}), ("GR control", {"gr": True})):
    if mut == "M2" and nm != "GR control":
        kw = dict(kw, gr=True)
    o, worst = table(**kw)
    res[nm] = {"worst_1sigma": worst, "worst_delta1_z0_k30": o["z=0/k=30/delta=1"], "at_z0_k30_1sigma": o["z=0/k=30/1sigma"], "z1000_k1_1sigma": o["z=1000/k=1/1sigma"]}
    P(f"  {nm:40s}: worst |G_eff/G - 1| over the grid (1 sigma) = {worst:.3e}; at z=0,k=30,delta=1: {o['z=0/k=30/delta=1']:.3e}; z=1000,k=1: {o['z=1000/k=1/1sigma']:.3e}")
R.out["numbers"]["G2"] = res
# background factor for 11C-b at the G6/G7 corner (c14 = t-fixed) and at the tie
Gc = lambda c2v, c14v: (2 - c14v) / (2 + 3 * c2v)
R.out["numbers"]["b_Gcos_over_GN"] = {"corner c2=2.7e-5,c14=8e-3": Gc(2.7e-5, 8.1e-3), "Planck-cap c2=6.3e-4, c14=0": Gc(6.3e-4, 0.0)}
ga = res["11C-a/-c (P2)"]["worst_1sigma"] <= 0.05
gb0 = res["11C-b t=1.2e-6 (largest offset where G1 passes, A6)"]["worst_1sigma"] <= 0.05
gb1 = res["11C-b t=1 (rule-T tie)"]["worst_1sigma"] <= 0.05
gb2 = res["11C-b t=4.0e6 (G6/G7-allowed corner)"]["worst_1sigma"] <= 0.05
R.verdict("G2 with cold fluid (11C-a, -c)", "PASS" if ga else "FAIL", f"quasi-static estimate: worst |G_eff/G-1| = {res['11C-a/-c (P2)']['worst_1sigma']:.2e} (line 0.05); linear theory ill-defined (mu -> 0); CMB part UNDEFINED")
R.verdict("G2 with cold fluid (11C-b at t=1.2e-6, where G1 passes)", "PASS" if gb0 else "FAIL", f"worst {res['11C-b t=1.2e-6 (largest offset where G1 passes, A6)']['worst_1sigma']:.2e}")
R.verdict("G2 with cold fluid (11C-b at t=1)", "PASS" if gb1 else "FAIL", f"worst {res['11C-b t=1 (rule-T tie)']['worst_1sigma']:.2e}")
R.verdict("G2 with cold fluid (11C-b at the G6/G7 corner t=4e6)", "PASS" if gb2 else "FAIL", f"worst {res['11C-b t=4.0e6 (G6/G7-allowed corner)']['worst_1sigma']:.2e}; background G_cos/G_N = {Gc(2.7e-5,8.1e-3):.4f}; CMB part UNDEFINED")
bite = (mut == "M2") and (res["11C-a/-c (P2)"]["worst_1sigma"] <= 0.05)
R.finish(bite=(mut != "" and bite))

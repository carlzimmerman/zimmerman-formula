#!/usr/bin/env python3
"""CFG654 part 1+2: independent cosmological inputs and initial conditions for the native PM pipeline.

Principle.  Before any bound system exists the switch is off (CFG649), so the framework's early universe is GR + photons +
massless neutrinos + baryons + cold energy (behaving as cold matter) + dark energy, with a0 irrelevant.  Linear perturbation
physics in that era (CAMB) is therefore the FRAMEWORK'S OWN linear physics, not a LCDM assumption.  What is NOT borrowed:
LCDM FIT RESULTS defined at late times (sigma8 at z = 0, Omega_m / H0 from late data) and LCDM late-time nonlinear or collapse
machinery (EH fitting shape, LCDM shell turnaround table, LCDM-backscaled growth).

Inputs (each with provenance; values read verbatim, see PROVENANCE):
  T_CMB   2.7255 K                      FIRAS (Fixsen 2009); the record's value (CFG642).
  omega_b 0.02193 +- 0.00022            BBN: Cooke, Pettini & Steidel 2018 D/H = (2.527 +- 0.030)e-5 inverted with CAMB 1.6.6's
                                        PRIMAT 2024 table (CFG642 gate d1, reproduced below). Independent of the CMB.
  omega_c 0.1202 +- 0.0014              Planck 2018 VI (arXiv 1807.06209, ms.tex Table 2 'LCDMcompare'), column TT,TE,EE+lowE
                                        (NO lensing reconstruction, NO BAO).  Fixed by the acoustic peaks (pre-switch-on).
  ln(1e10 A_s) 3.045 +- 0.016, n_s 0.9649 +- 0.0044, 100 theta_* 1.04109 +- 0.00030, tau 0.0544   same table / column.
  H0      DERIVED from theta_* in the framework's own background (flat, Lambda constant + CFG630 settling trickle, which is
          1e-6 and numerically irrelevant), with omega_b(BBN), omega_c, massless neutrinos (N_eff 3.044).  The framework does
          not predict H0; brackets: SH0ES 73.04 (Riess+22, on disk via CFG493/CFG642) and the inherited 67.36.
FLAG: the Planck chain that produced the column fits the full base-LCDM model, i.e. it assumes a Lambda-constant late
universe and integrates the late-time ISW and the lensing smoothing of the TT/TE/EE peaks (lensing RECONSTRUCTION is not in this
column).  A Lambda-constant late background is also the framework's own background, so this is not an extra assumption at the
background level; the late-time lensing smoothing of the peaks is computed with LCDM clustering, which is a residual
dependence (minimal raw product to remove it: see the README data list).

Run:  nice -n 10 python3 cfg654_ics.py   -> cfg654_ics.out, cfg654_ics_results.json, cfg654_ics_tables.npz (the engine loads this)
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, json, math, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
import numpy as np
from scipy.integrate import quad, solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
ZI = 49.0; AI = 1.0 / (1 + ZI)
C_KMS = 299792.458

# ---------------------------------------------------------------- provenance-tagged inputs
PROVENANCE = {
    "T_CMB": dict(value=2.7255, source="FIRAS, Fixsen 2009 ApJ 707 916; record value (CFG642 FROZEN_CRITERIA section 2)"),
    "DH_obs": dict(value=2.527e-5, sigma=0.030e-5, source="Cooke, Pettini & Steidel 2018 ApJ 855 102 (record value, CFG642 FROZEN_CRITERIA section 1)"),
    "omega_c": dict(value=0.1202, sigma=0.0014, source="Planck 2018 VI arXiv:1807.06209, ms.tex Table 2 (label LCDMcompare), column TT,TE,EE+lowE"),
    "omega_b_CMB": dict(value=0.02236, sigma=0.00015, source="same table/column (bracket only)"),
    "ln1e10As": dict(value=3.045, sigma=0.016, source="same table/column"),
    "As_e2tau_1e9": dict(value=1.884, sigma=0.012, source="same table/column (the combination the peaks fix)"),
    "n_s": dict(value=0.9649, sigma=0.0044, source="same table/column"),
    "theta_star_100": dict(value=1.04109, sigma=0.00030, source="same table/column (100 theta_*)"),
    "tau": dict(value=0.0544, source="same table/column (irrelevant for the matter spectrum)"),
    "H0_SH0ES": dict(value=73.04, sigma=1.04, source="Riess+22 (record value, CFG493 / CFG642)"),
    "trickle": dict(value="Delta rho_DE / rho_DE0 since z: 0.5 4.8e-7, 1 1.10e-6, 2 2.12e-6, 3 2.70e-6, 8 3.4e-6",
                    source="CFG630 README table (canonical, upper end of the alpha bracket); sign: rho_DE grows toward z = 0"),
}
INHERITED = dict(h=0.6736, omega_b=0.02237, omega_c=0.1200, n_s=0.965, sigma8=0.811)   # cfg596_pm.py / cfg650_pm.py constants

# CFG630 trickle: rho_DE(z) = rho_DE0 (1 - Dtr(z)), Dtr(0) = 0 (energy handed TO dark energy since z)
_TRZ = np.array([0.0, 0.5, 1.0, 2.0, 3.0, 8.0, 1e4]); _TRD = np.array([0.0, 4.8e-7, 1.10e-6, 2.12e-6, 2.70e-6, 3.4e-6, 3.4e-6])
def trickle(z):
    return np.interp(z, _TRZ, _TRD)

def bbn_omega_b():
    """CFG642 gate d1 reproduced: D/H (Cooke+18) inverted with CAMB's PRIMAT 2024 table (theory error in quadrature)."""
    import camb.bbn as cbbn
    from scipy.optimize import brentq
    D, sD = PROVENANCE["DH_obs"]["value"], PROVENANCE["DH_obs"]["sigma"]
    out = {}
    for name, tab in [("PRIMAT 2024", cbbn.BBN_table_interpolator("PRIMAT_Yp_DH_ErrorMC_2024.dat", function_of=("Ombh2", "DeltaN"))),
                      ("PArthENoPE 2017", cbbn.BBN_table_interpolator("PArthENoPE_880.2_standard.dat"))]:
        wb = brentq(lambda w: float(tab.DH(w, 0.0)) - D, 0.015, 0.03)
        dl = (math.log(float(tab.DH(wb * 1.001, 0.0))) - math.log(float(tab.DH(wb / 1.001, 0.0)))) / (2 * math.log(1.001))
        sth = float(tab.get("sig(D/H)", wb, 0.0)) if name.startswith("PRIMAT") else 0.0
        out[name] = dict(omega_b=wb, sigma=wb * math.hypot(sD / D, sth / D) / abs(dl))
    return out

# ---------------------------------------------------------------- the framework's own background and linear growth
class Background:
    """flat: photons + 3.044 massless neutrinos (radiation), cold matter (baryons + cold energy), dark energy = Lambda + trickle."""
    def __init__(self, h, omega_b, omega_c, Tcmb=2.7255, neff=3.044, trickle_on=True):
        self.h, self.ob, self.oc = h, omega_b, omega_c
        og = 2.4728e-5 * (Tcmb / 2.7255) ** 4                 # omega_gamma (record value, CFG642)
        self.Or = og * (1 + 0.2271 * neff) / h ** 2
        self.Om = (omega_b + omega_c) / h ** 2; self.OL = 1.0 - self.Om - self.Or; self.FB = omega_b / (omega_b + omega_c)
        self.tr = trickle_on
    def E(self, a):
        z = 1.0 / a - 1.0
        de = self.OL * ((1.0 - float(trickle(z))) if self.tr else 1.0)
        return math.sqrt(self.Om / a ** 3 + self.Or / a ** 4 + de)
    def growth(self):
        """sub-horizon growing mode of the cold matter (radiation and dark energy smooth), started on the exact Meszaros solution
        D = 1 + 3y/2, y = a/a_eq, at a = 1e-6; integrated in ln a.  Returns D(a) normalised D(1) = 1 and f(a) = dlnD/dlna."""
        aeq = self.Or / self.Om
        def Hl(a, e=1e-6):
            return (math.log(self.E(a * (1 + e))) - math.log(self.E(a * (1 - e)))) / (2 * e)
        def rhs(x, y):
            a = math.exp(x); D, Dp = y
            Oma = self.Om / a ** 3 / self.E(a) ** 2
            return [Dp, -(2.0 + Hl(a)) * Dp + 1.5 * Oma * D]
        a0 = 1e-6; y0 = a0 / aeq
        xs = np.linspace(math.log(a0), 0.0, 6001)
        s = solve_ivp(rhs, [xs[0], 0.0], [1 + 1.5 * y0, 1.5 * y0], t_eval=xs, rtol=1e-11, atol=1e-14, method="DOP853")
        D = s.y[0] / s.y[0][-1]; f = s.y[1] / s.y[0]
        self._lx, self._lD, self._f = xs, np.log(D), f
        return self
    def D(self, a): return float(math.exp(np.interp(math.log(a), self._lx, self._lD)))
    def f(self, a): return float(np.interp(math.log(a), self._lx, self._f))

# ---------------------------------------------------------------- CAMB in the pre-switch era (the framework's own linear physics)
def camb_results(h=None, theta=None, omega_b=None, omega_c=None, As=None, ns=None, mnu=0.0, zs=(ZI,), kmax=120.0):
    import camb
    p = camb.CAMBparams()
    kw = dict(ombh2=omega_b, omch2=omega_c, omk=0.0, mnu=mnu, num_massive_neutrinos=(1 if mnu > 0 else 0), nnu=3.044,
              TCMB=PROVENANCE["T_CMB"]["value"], tau=PROVENANCE["tau"]["value"])
    if theta is not None: kw["thetastar"] = theta
    else: kw["H0"] = 100 * h
    p.set_cosmology(**kw)
    p.InitPower.set_params(As=As, ns=ns, pivot_scalar=0.05)
    p.set_dark_energy(w=-1.0, wa=0.0)
    p.set_matter_power(redshifts=sorted(set(list(zs) + [0.0]), reverse=True), kmax=kmax, nonlinear=False, accurate_massive_neutrino_transfers=False)
    p.set_accuracy(AccuracyBoost=1.5, lAccuracyBoost=1.0)
    p.WantCls = False
    r = camb.get_results(p)
    return p, r

def Pk_cb(r, z, kh):
    """linear CDM+baryon ('delta_nonu') power at redshift z, (Mpc/h)^3, k in h/Mpc."""
    import camb
    pk = r.get_matter_power_interpolator(nonlinear=False, hubble_units=True, k_hunit=True, var1="delta_nonu", var2="delta_nonu",
                                         extrap_kmax=kh.max() * 1.01)
    return np.array(pk.P(z, kh))

# ---------------------------------------------------------------- inherited inputs (cfg596_pm.py verbatim) for the comparison
def inherited():
    h = INHERITED["h"]; om_b, om_c = INHERITED["omega_b"], INHERITED["omega_c"]; Om = (om_b + om_c) / h ** 2; OL = 1 - Om
    NS, SIG8 = INHERITED["n_s"], INHERITED["sigma8"]
    E = lambda a: math.sqrt(Om / a ** 3 + OL)
    def T_eh(k):
        OB = om_b / h ** 2; omh2, fb = Om * h * h, OB / Om
        s = 44.5 * math.log(9.83 / omh2) / math.sqrt(1 + 10 * (OB * h * h) ** 0.75)
        ag = 1 - 0.328 * math.log(431 * omh2) * fb + 0.38 * math.log(22.3 * omh2) * fb ** 2
        gam = Om * h * (ag + (1 - ag) / (1 + (0.43 * k * s) ** 4))
        q = k * (2.7255 / 2.7) ** 2 / (gam * h)
        L0 = np.log(2 * math.e + 1.8 * q); C0 = 14.2 + 731 / (1 + 62.5 * q)
        return L0 / (L0 + C0 * q * q)
    KG = np.geomspace(1e-5, 100, 40000); PK = KG ** NS * T_eh(KG * h) ** 2
    W8 = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
    PK *= SIG8 ** 2 / (np.trapz(PK * W8(KG * 8.0) ** 2 * KG ** 2, KG) / (2 * math.pi ** 2))
    P0 = lambda k: np.interp(np.log(np.maximum(k, 1e-5)), np.log(KG), PK, left=0, right=0)
    g = lambda x: quad(lambda u: 1.0 / (u * E(u)) ** 3, 0, x)[0] * E(x)
    Dg = lambda a: g(a) / g(1.0)
    Dmd = lambda a: 2.5 * Om * E(a) * quad(lambda u: 1.0 / (u * E(u)) ** 3, 0, a)[0]
    # CFG650 ic_amp() reproduced (A_s bracket, EH shape, matter-dominated D(a_i))
    As = math.exp(3.0448) * 1e-10; k = 0.1
    T = float(T_eh(np.array([k * h]))[0])
    pas = 2 * math.pi ** 2 / k ** 3 * (4.0 / 25.0) * As * (k * h / 0.05) ** (NS - 1) * (k * 2997.92458) ** 4 * T ** 2 * Dmd(AI) ** 2 / Om ** 2
    amp650 = math.sqrt(pas / (float(P0(np.array([k]))[0]) * Dg(AI) ** 2))
    return dict(h=h, Om=Om, P0=P0, Dg=Dg, E=E, amp650=amp650, KG=KG)

def sigR(kh, P, R):
    x = kh * R; W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
    return math.sqrt(np.trapz(P * W ** 2 * kh ** 3, np.log(kh)) / (2 * math.pi ** 2))

# ---------------------------------------------------------------- input sets
def input_sets(wbb):
    As = math.exp(PROVENANCE["ln1e10As"]["value"]) * 1e-10; ns = PROVENANCE["n_s"]["value"]; th = PROVENANCE["theta_star_100"]["value"] / 100
    oc = PROVENANCE["omega_c"]["value"]
    return {
        "NATIVE": dict(omega_b=wbb, omega_c=oc, As=As, ns=ns, theta=th, mnu=0.0, label="PRIMARY: BBN omega_b, CMB-primary omega_c/A_s/n_s, H0 from theta_* (framework background)"),
        "B_wbCMB": dict(omega_b=PROVENANCE["omega_b_CMB"]["value"], omega_c=oc, As=As, ns=ns, theta=th, mnu=0.0, label="bracket: CMB omega_b (no BBN)"),
        "B_H0loc": dict(omega_b=wbb, omega_c=oc, As=As, ns=ns, h=PROVENANCE["H0_SH0ES"]["value"] / 100, mnu=0.0, label="bracket: H0 = 73.04 local (theta_* not fitted)"),
        "B_H0inh": dict(omega_b=wbb, omega_c=oc, As=As, ns=ns, h=INHERITED["h"], mnu=0.0, label="bracket: H0 = 67.36 (inherited value)"),
        "B_mnu": dict(omega_b=wbb, omega_c=oc, As=As, ns=ns, theta=th, mnu=0.06, label="bracket: one massive neutrino 0.06 eV (oscillation minimum; PM has no neutrino component)"),
    }

def build(name, s, kh):
    p, r = camb_results(h=s.get("h"), theta=s.get("theta"), omega_b=s["omega_b"], omega_c=s["omega_c"], As=s["As"], ns=s["ns"], mnu=s["mnu"],
                        zs=(ZI, ZI + 1, ZI - 1, 1.0, 0.5))
    h = p.H0 / 100
    bg = Background(h, s["omega_b"], s["omega_c"]).growth()
    Pi = Pk_cb(r, ZI, kh); P0c = Pk_cb(r, 0.0, kh)
    Dp, Dm = Pk_cb(r, ZI - 1, kh), Pk_cb(r, ZI + 1, kh)
    fk = (1 + ZI) * 0.5 * (np.log(Dp) - np.log(Dm)) / 2.0          # f = -(1+z) dlnD/dz, dlnD = 0.5 dlnP
    Di = bg.D(AI)
    Plin0 = Pi / Di ** 2                                             # engine convention: P_lin0(k) D(a_i)^2 = P(k, z_i)
    sel = (kh > 0.05) & (kh < 2.0)
    gr = np.sqrt(P0c[sel] / Pi[sel]); ode = 1.0 / Di
    th = r.get_derived_params()
    return dict(name=name, label=s["label"], h=h, omega_b=s["omega_b"], omega_c=s["omega_c"], Om_cb=bg.Om, Or=bg.Or, OL=bg.OL, FB=bg.FB,
                ratio_c_b=s["omega_c"] / s["omega_b"], As=s["As"], ns=s["ns"], mnu=s["mnu"], theta_star_100=th["thetastar"], zstar=th["zstar"],
                rdrag=th["rdrag"], D_ai=Di, f_ai_ode=bg.f(AI), f_ai_camb_k=[float(np.interp(math.log(q), np.log(kh), fk)) for q in (0.1, 0.5, 2.0, 10.0)],
                growth_ratio_camb_over_ode=dict(min=float(gr.min() / ode), max=float(gr.max() / ode)),
                sigma8_lin_native_growth=sigR(kh, Plin0, 8.0), sigma8_lin_camb_z0=sigR(kh, P0c, 8.0),
                sig_zi=dict(R8=sigR(kh, Pi, 8.0), R2=sigR(kh, Pi, 2.0), R0p5=sigR(kh, Pi, 0.5)),
                _Plin0=Plin0, _Pi=Pi, _bg=bg)

def main():
    T0 = time.time(); OUT = []
    def P(*a):
        s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
    P("CFG654 part 1+2: independent inputs and ICs (CAMB in the pre-switch era = the framework's own linear physics; no sigma8, no EH, no LCDM backscaling)")
    P("kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")
    import camb
    P(f"CAMB {camb.__version__}")
    bbn = bbn_omega_b(); wbb = bbn["PRIMAT 2024"]["omega_b"]
    P(f"BBN omega_b (Cooke+18 D/H): PRIMAT 2024 {wbb:.5f} +- {bbn['PRIMAT 2024']['sigma']:.5f}; PArthENoPE 2017 {bbn['PArthENoPE 2017']['omega_b']:.5f} (reported)")
    kh = np.geomspace(1e-4, 110.0, 3000)
    inh = inherited()
    Pinh_i = inh["P0"](kh) * inh["Dg"](AI) ** 2
    P(f"inherited: h {inh['h']}, Om {inh['Om']:.5f}, sigma8 0.811 (EH no-wiggle, LCDM back-scaled D(a_i) = {inh['Dg'](AI):.6f}); CFG650 ic_amp reproduced = {inh['amp650']:.5f}")
    RES = dict(lane="CFG654", part="ics", camb=camb.__version__, provenance=PROVENANCE, bbn=bbn, inherited=dict(INHERITED, Om=inh["Om"], D_ai=inh["Dg"](AI),
               cfg650_ic_amp=inh["amp650"], sig_zi=dict(R8=sigR(kh, Pinh_i, 8.0), R2=sigR(kh, Pinh_i, 2.0), R0p5=sigR(kh, Pinh_i, 0.5))), sets={})
    KQ = (0.07, 0.1, 0.3, 0.5, 1.0, 2.0, 5.0, 10.0)
    for name, s in input_sets(wbb).items():
        b = build(name, s, kh)
        with np.errstate(divide="ignore"): amp = np.sqrt(b["_Pi"] / Pinh_i)       # (inherited table ends at k = 100)
        b["amp_vs_inherited_at_k"] = {str(q): float(np.interp(math.log(q), np.log(kh), amp)) for q in KQ}
        b["amp_sigma_ratio_zi"] = {R: b["sig_zi"][R] / RES["inherited"]["sig_zi"][R] for R in b["sig_zi"]}
        P(f"\n[{name}] {b['label']}")
        P(f"  h {b['h']:.5f} (100 theta_* {b['theta_star_100']:.5f}), Om_cb {b['Om_cb']:.5f}, Or {b['Or']:.3e}, OL {b['OL']:.5f}, f_b {b['FB']:.5f}, omega_c/omega_b {b['ratio_c_b']:.4f}, z* {b['zstar']:.2f}, r_drag {b['rdrag']:.2f} Mpc")
        P(f"  native growth D(a_i)/D(1) = {b['D_ai']:.6f} (inherited LCDM no-radiation {RES['inherited']['D_ai']:.6f}); f(a_i): ODE {b['f_ai_ode']:.5f}, CAMB at k 0.1/0.5/2/10 = " + "/".join(f"{x:.4f}" for x in b["f_ai_camb_k"]))
        P(f"  CAMB z_i->0 growth / ODE growth, k 0.05-2 h/Mpc: {b['growth_ratio_camb_over_ode']['min']:.4f} .. {b['growth_ratio_camb_over_ode']['max']:.4f}")
        P(f"  implied LINEAR sigma8 (A_s-normalised; native GR growth to z = 0, switch ignored, HYPOTHETICAL): {b['sigma8_lin_native_growth']:.4f}  (CAMB z = 0: {b['sigma8_lin_camb_z0']:.4f}; inherited 0.811)")
        P(f"  IC amplitude sqrt(P_native/P_inherited) at z_i, k [h/Mpc] " + ", ".join(f"{q}: {v:.4f}" for q, v in b["amp_vs_inherited_at_k"].items()))
        P(f"  sigma_R(z_i) ratio native/inherited: R8 {b['amp_sigma_ratio_zi']['R8']:.4f}, R2 {b['amp_sigma_ratio_zi']['R2']:.4f}, R0.5 {b['amp_sigma_ratio_zi']['R0p5']:.4f}  (CFG650 A_s bracket: 1.0265, k-independent)")
        RES["sets"][name] = {k: v for k, v in b.items() if not k.startswith("_")}
        if name == "NATIVE":
            bg = b["_bg"]
            np.savez(os.path.join(HERE, "cfg654_ics_tables.npz"), kh=kh, Plin0=b["_Plin0"], P_zi=b["_Pi"], lna=bg._lx, lnD=bg._lD, f=bg._f,
                     h=b["h"], omega_b=b["omega_b"], omega_c=b["omega_c"], Or=bg.Or, ns=b["ns"], As=b["As"], zi=ZI,
                     trz=_TRZ, trd=_TRD)
            # z = 0 linear shape for the scorer's k < k_lo continuation
            p, r = camb_results(theta=s["theta"], omega_b=s["omega_b"], omega_c=s["omega_c"], As=s["As"], ns=s["ns"], zs=(0.0,))
            np.savez(os.path.join(HERE, "cfg654_scorer_tables.npz"), kh=kh, Plin_z0=Pk_cb(r, 0.0, kh), lna=bg._lx, lnD=bg._lD, h=b["h"],
                     Om=bg.Om, Or=bg.Or, OL=bg.OL, trz=_TRZ, trd=_TRD)
    # footing disclosure: a0 = kappa c sqrt(G rho_DE) scales as sqrt(Omega_L h^2)
    nat = RES["sets"]["NATIVE"]; inhOLh2 = (1 - inh["Om"]) * inh["h"] ** 2
    RES["footing_disclosure"] = dict(rho_DE_ratio_native_over_inherited=nat["OL"] * nat["h"] ** 2 / inhOLh2,
                                     a0_canonical_if_rebuilt=9.3603e-11 * math.sqrt(nat["OL"] * nat["h"] ** 2 / inhOLh2),
                                     note="footings are the record's declared inputs and are NOT changed in the engine; reported only")
    P(f"\nfooting disclosure: rho_DE(native)/rho_DE(inherited) = {RES['footing_disclosure']['rho_DE_ratio_native_over_inherited']:.4f} -> canonical a0 if rebuilt "
      f"{RES['footing_disclosure']['a0_canonical_if_rebuilt']:.4e} (engine keeps 9.3603e-11 / 1.1312e-10; reported only)")
    P(f"trickle check: E(a=1) with/without CFG630 trickle differ by {abs(Background(nat['h'], nat['omega_b'], nat['omega_c']).E(0.5) / Background(nat['h'], nat['omega_b'], nat['omega_c'], trickle_on=False).E(0.5) - 1):.2e} at z = 1")
    P(f"\ndone in {time.time() - T0:.0f} s")
    json.dump(RES, open(os.path.join(HERE, "cfg654_ics_results.json"), "w"), indent=1)
    open(os.path.join(HERE, "cfg654_ics.out"), "w").write("\n".join(OUT) + "\n")

if __name__ == "__main__":
    main()

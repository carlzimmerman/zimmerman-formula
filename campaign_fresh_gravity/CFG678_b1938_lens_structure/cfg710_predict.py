#!/usr/bin/env python3
"""CFG710 (dir CFG678_b1938_lens_structure; criteria ef9d750d0): blind predictions for B1938+666's mass structure from the
stage-1 LIGHT + the law, sealed before the stage-2 fit is read. kappa = 1/2 FITTED; cold energy mass required; not theory closed.
Disclosed choice (made before stage 2): stars = the compact Sersic (R_e 0.227", n 5); the R_e = 30" component is a sky/arc
pedestal over the 1.2" mask (robustness variant V2 includes it)."""
import os, sys, io, json, math, hashlib, contextlib
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import gammaincinv
from astropy.cosmology import Planck18 as cosmo
import astropy.units as u
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4
MUT = os.environ.get("CFG710_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
G, MSUN, KPC, C = C4.G_SI, C4.MSUN, C4.KPC, 2.99792458e8
L1 = json.load(open(os.path.join(HERE, "cfg710_stage1_light.json")))
comp = {c["name"]: c for c in L1["components"]}
zl, zs, thE = 0.881, 2.059, L1["theta_E_stage1"]
Dl = cosmo.angular_diameter_distance(zl).to(u.m).value; Ds = cosmo.angular_diameter_distance(zs).to(u.m).value
Dls = cosmo.angular_diameter_distance_z1z2(zl, zs).to(u.m).value
ARC = Dl / 206264.806                                  # m per arcsec
Scr = C ** 2 / (4 * math.pi * G) * Ds / (Dl * Dls)     # kg/m^2
M_E = Scr * math.pi * (thE * ARC) ** 2

def h(y, a0name):
    return np.interp(np.log10(np.maximum(y, 1e-14)), C4._KNS["LYG"], C4._KNS["_HM"])

def model(comps, a0, Mstar):
    """circularised Sersic(s) -> Abel-deprojected rho* -> M*(r) -> law -> total M(r) -> projected kappa(R)"""
    rg = np.logspace(-3.5, 1.6, 700)                    # arcsec
    def Sig(R):
        s = 0.0
        for c_ in comps:
            n = c_["n"]; Re = c_["R_e"] * math.sqrt(c_["q"]); b = gammaincinv(2 * n, 0.5)
            s += c_["intensity"] * np.exp(-b * ((R / Re) ** (1 / n) - 1))
        return s
    dSig = lambda R: (Sig(R * 1.0001) - Sig(R * 0.9999)) / (0.0002 * R)
    rho = np.array([-1 / math.pi * quad(lambda t: dSig(math.sqrt(r * r + t * t)) / math.sqrt(r * r + t * t), 0, 60, limit=200)[0] for r in rg])
    rho = np.maximum(rho, 0)
    Mr = np.concatenate([[0], np.cumsum(0.5 * (4 * math.pi * rg[1:] ** 2 * rho[1:] + 4 * math.pi * rg[:-1] ** 2 * rho[:-1]) * np.diff(rg))])
    Mr = Mr / Mr[-1] * Mstar                            # stars normalised to total M*
    r_m = rg * ARC
    gN = G * Mr * MSUN / r_m ** 2
    g = gN + a0 * h(gN / a0, None) if a0 > 0 else gN
    Mt = g * r_m ** 2 / G / MSUN                         # total enclosed 3D mass (Msun)
    rho_t = np.gradient(Mt, rg) / (4 * math.pi * rg ** 2)
    def Mproj(R):                                       # projected mass inside R (arcsec)
        inner = np.interp(R, rg, Mt)
        f = lambda r: np.interp(r, rg, rho_t) * 4 * math.pi * r * r * (1 - math.sqrt(max(1 - R * R / (r * r), 0)))   # shell part inside the cylinder
        return inner + quad(f, R, rg[-1], limit=200)[0]
    return Mproj, g, gN, rg

def predict(comps, a0):
    Mp = lambda Ms: model(comps, a0, Ms)[0](thE) - M_E / MSUN
    Ms = 10 ** brentq(lambda lm: Mp(10 ** lm), 9, 13, xtol=1e-4)
    Mproj, g, gN, rg = model(comps, a0, Ms)
    # gamma_eff from kappa slope at theta_E: kappa_bar(R) = Mproj/(pi R^2); kappa = (1/2R) d(Mproj)/dR / (pi) ...
    R = np.array([0.9, 1.0, 1.1]) * thE; Mpr = np.array([Mproj(x) for x in R])
    dM = (Mpr[2] - Mpr[0]) / (R[2] - R[0]); kap = dM / (2 * math.pi * R[1])           # surface density (Msun/arcsec^2)
    Rk = np.array([0.95, 1.05]) * thE; kk = [(Mproj(x * 1.01) - Mproj(x * 0.99)) / (0.02 * x) / (2 * math.pi * x) for x in Rk]
    gam = 1 - (math.log(kk[1]) - math.log(kk[0])) / (math.log(Rk[1]) - math.log(Rk[0]))
    # mass-weighted 3D slope over 0.5-1.5 theta_E
    sel = (rg >= 0.5 * thE) & (rg <= 1.5 * thE); Mt = g * (rg * ARC) ** 2 / G / MSUN
    rho_t = np.gradient(Mt, rg) / (4 * math.pi * rg ** 2); s3 = -np.gradient(np.log(rho_t), np.log(rg))
    gam3 = float(np.average(s3[sel], weights=(rho_t * rg ** 3)[sel]))
    yE = float(np.interp(thE, rg, gN) / a0) if a0 > 0 else float("inf")
    return dict(M_star_Msun=Ms, gamma_eff_at_thetaE=gam, gamma3D_massweighted_0p5_1p5=gam3, gN_over_a0_at_thetaE=yE,
                cold_fraction_in_thetaE=1 - model(comps, 0.0, Ms)[0](thE) / (M_E / MSUN) if a0 > 0 else 0.0)

out = {"lane": "CFG710", "dir": "CFG678_b1938_lens_structure", "criteria": "ef9d750d0", "theta_E": thE,
       "M_E_Msun": M_E / MSUN, "Sigma_cr_Msun_pc2": Scr / (MSUN / (3.0857e16) ** 2), "mutate": MUT, "P1": {}}
L = []
for foot, a0 in C4.A0.items():
    a = 1e-30 if MUT else a0
    for var, comps in (("V1_compact", [comp["disk"]]), ("V2_both", [comp["disk"], comp["bulge"]])):
        p = predict(comps, a); out["P1"][f"{foot}_{var}"] = p
        L.append(f"P1 {foot} {var}: M* {p['M_star_Msun']:.3e}, gamma_eff(theta_E) {p['gamma_eff_at_thetaE']:.3f}, gamma3D(0.5-1.5) "
                 f"{p['gamma3D_massweighted_0p5_1p5']:.3f}, gN/a0(theta_E) {p['gN_over_a0_at_thetaE']:.1f}, cold fraction <theta_E {p['cold_fraction_in_thetaE']:.3f}")
d = comp["disk"]
out["P2"] = dict(light_PA_deg=d["phi_deg"], light_q=d["q"], rule="|PA_mass - PA_light| <= 10 deg (q_L <= 0.9); q_M in [q_L, q_L + 0.1]",
                 q_M_range=[d["q"], d["q"] + 0.1], PA_test_diagnostic=d["q"] <= 0.9)
out["P3"] = dict(m4_max=0.02, m3_max=0.02, note="theta_E-normalised multipole strength; light model has no a3/a4")
L.append(f"P2: light PA {d['phi_deg']:.1f} deg, q_L {d['q']:.3f} -> mass PA within 10 deg, q_M in [{d['q']:.3f}, {d['q']+0.1:.3f}]")
L.append("P3: m=3, m=4 mass multipole strengths <= 0.02")
if MUT:
    base = json.load(open(os.path.join(HERE, "cfg710_predictions.json")))["P1"]["canonical_V1_compact"]["gamma_eff_at_thetaE"]
    m = out["P1"]["canonical_V1_compact"]["gamma_eff_at_thetaE"]; bite = abs(m - base) > 0.05
    L.append(f"MUTATE a0->0: gamma_eff {base:.3f} -> {m:.3f}: {'BITES' if bite else 'DOES NOT BITE'}")
js = json.dumps(out, indent=1, sort_keys=True, default=float) + "\n"
open(os.path.join(HERE, f"cfg710_predictions{TAG}.json"), "w").write(js)
L.append(f"sha256(cfg710_predictions{TAG}.json) = {hashlib.sha256(js.encode()).hexdigest()}")
open(os.path.join(HERE, f"cfg710{TAG}.out"), "w").write("\n".join(L) + "\n"); print("\n".join(L))
if MUT: sys.exit(1 if bite else 0)

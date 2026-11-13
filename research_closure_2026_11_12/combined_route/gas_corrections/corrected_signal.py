"""Forward correction of FINAL5. Analytic gas toy profile, not a data likelihood.

Usage: python3 corrected_signal.py OUTPUT.json [--mutate]
The --mutate flag runs the same analytic verification; no frozen outputs are changed.
"""
import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.special import i0e

G, MSUN, MPC = 6.674e-11, 1.989e30, 3.0857e22
MP, MUE, XH = 1.6726e-27, 1.14, 0.76
SIGT, MEC2, KEV = 6.6524587e-29, 8.18711e-14, 1.602177e-16
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
XB2, MBST, ZREF = 34.6781, 8.42e10, 0.308


def Sigma(a0):
    """Enclosed mass / pi r^2 normalization [kg m^-2], NOT projected column."""
    return a0 / (math.pi * G * XB2)


def budget_radius(a0):
    return math.sqrt(MBST * MSUN / (math.pi * Sigma(a0)))


def M_req(R_m, a0):
    return max(0.0, math.pi * Sigma(a0) * R_m**2 - MBST * MSUN)


def rho_A(r, a0):
    """Gas shell saturation example: zero below Rbudget, Sigma/(2r) above."""
    a = np.asarray(r, dtype=float)
    return np.where(a >= budget_radius(a0), Sigma(a0) / (2 * np.maximum(a, 1e-100)), 0.0)


def column_factor(b, Rout, Rin=0.0):
    """Project rho=Sigma/(2r) on Rin<r<Rout. Input radii in any common unit."""
    if b < 0 or Rin < 0 or Rout <= Rin:
        raise ValueError("Require b>=0 and 0<=Rin<Rout")
    if b >= Rout:
        return 0.0
    if b == 0:
        return math.log(Rout / Rin) if Rin > 0 else math.inf
    return math.acosh(Rout / b) - (math.acosh(Rin / b) if b < Rin else 0.0)


def N_e_m(b, a0, Rout, Rin=None):
    if Rin is None:
        Rin = budget_radius(a0)
    return Sigma(a0) / (MUE * MP) * column_factor(b, Rout, Rin)


def N_e(b, a0, Rout, Rin=None):
    return N_e_m(b, a0, Rout, Rin) * 1e-4


def y_of(b, a0, kT, Rout, Rin=None):
    """Isothermal illustrative y. kT in keV; a temperature input is required."""
    return SIGT / MEC2 * (kT * KEV) * N_e_m(b, a0, Rout, Rin)


def EM(b, a0, Rout, Rin=None):
    """Integral ne nH dl [cm^-5] for the same shell profile."""
    if Rin is None:
        Rin = budget_radius(a0)
    if b >= Rout:
        return 0.0
    if b < 0 or not 0 <= Rin < Rout:
        raise ValueError("Invalid shell or impact radius")
    if b == 0:
        length = 2 * (1 / Rin - 1 / Rout) if Rin else math.inf
    else:
        length = 2 / b * (math.acos(b / Rout) - (math.acos(b / Rin) if b < Rin else 0))
    return (XH / MUE) * (Sigma(a0) / (2 * MP))**2 * length * 1e-10


def smear(b_arc, y_arc, fwhm_arc):
    """Circular 2D Gaussian convolution; zero outside supplied radial domain.

    K(R,b)=b/s^2 exp(-(R-b)^2/(2s^2)) i0e(Rb/s^2).
    No per-radius renormalization: beam flux outside the domain is real.
    """
    b, y = np.asarray(b_arc, float), np.asarray(y_arc, float)
    if b.ndim != 1 or y.shape != b.shape or np.any(np.diff(b) <= 0) or b[0] < 0:
        raise ValueError("Need matching profiles on an increasing nonnegative grid")
    s = fwhm_arc / math.sqrt(8 * math.log(2))
    if s <= 0:
        raise ValueError("Beam FWHM must be positive")
    return np.array([np.trapz(b / s**2 * np.exp(-0.5 * ((b - R) / s)**2)
                            * i0e(R * b / s**2) * y, b) for R in b])


def D_A(z):
    return 299792.458 / 67.4 / (1 + z) * MPC * quad(
        lambda v: 1 / math.sqrt(.315 * (1 + v)**3 + .685), 0, z)[0]


def xray_flux_cgs(luminosity_erg_s, luminosity_distance_m):
    return luminosity_erg_s / (4 * math.pi * (100 * luminosity_distance_m)**2)


def checks():
    """Independent LOS and volume integrals, analytic Gaussian beam and units."""
    a0, Rout, Rin = A0["canonical"], 2.6, budget_radius(A0["canonical"]) / MPC
    los_errors, em_errors = [], []
    for b in [0.0, Rin / 2, .3, 1, 2, 2.59]:
        lo = math.sqrt(max(0, Rin**2 - b**2))
        hi = math.sqrt(Rout**2 - b**2)
        direct = quad(lambda z: 1 / math.sqrt(b*b+z*z), lo, hi, epsabs=1e-11)[0]
        los_errors.append(abs(direct / column_factor(b, Rout, Rin) - 1))
        direct_em = 2 * quad(lambda z: 1 / (b*b+z*z), lo, hi, epsabs=1e-11)[0]
        norm = XH / MUE * (Sigma(a0)/(2*MP))**2 / MPC * 1e-10
        em_errors.append(abs(EM(b*MPC, a0, Rout*MPC) / (norm*direct_em) - 1))
    projected = 2 * quad(lambda b: b * column_factor(b, Rout, Rin), 0, Rout,
                          points=[Rin], epsabs=1e-10)[0]
    mass_error = abs(projected / (Rout**2 - Rin**2) - 1)
    projected_em = 2*math.pi*quad(lambda b: b*EM(b*MPC,a0,Rout*MPC), 0,Rout,
                                  points=[Rin],epsabs=1e7,epsrel=1e-9)[0] * MPC**2 * 1e4
    volume_em = 4*math.pi*(XH/MUE)*(Sigma(a0)/(2*MP))**2*(Rout-Rin)*MPC*1e-6
    em_mass_error = abs(projected_em/volume_em - 1)
    grid = np.linspace(0, 10, 2001)
    width, beam_sigma = 1.3, .7
    conv = smear(grid, np.exp(-grid**2/(2*width**2)), beam_sigma*math.sqrt(8*math.log(2)))
    expected = width**2/(width**2+beam_sigma**2)*np.exp(-grid**2/(2*(width**2+beam_sigma**2)))
    beam_error = float(np.max(np.abs(conv-expected)))
    flux_error = abs(xray_flux_cgs(4*math.pi*1e4, 1)-1)
    temp_ratio = y_of(MPC,a0,.4,2.6*MPC)/y_of(MPC,a0,.2,2.6*MPC)
    assert max(los_errors+em_errors+[mass_error,em_mass_error,flux_error]) < 2e-8
    assert beam_error < 5e-6
    assert temp_ratio == 2
    return dict(los_max_relative_error=max(los_errors),em_max_relative_error=max(em_errors),
                projected_mass_relative_error=mass_error,projected_em_relative_error=em_mass_error,
                gaussian_beam_max_absolute_error=beam_error,cgs_flux_error=flux_error,
                temperature_doubling_ratio=temp_ratio)


def result():
    verification = checks()
    out = {"status":"conditional toy forward model; no observational verdict", "checks":verification,
           "assumptions":["Saturated enclosed mass example, not a forced unique gas profile",
                          "Gas shell starts at Rbudget; compact central baryons counted once",
                          "Isothermal kT supplied per row; cooling coefficient illustrative, not calibrated",
                          "No ACT filtering/covariance or lens selection remeasurement"],"footings":{}}
    for name,a0 in A0.items():
        rows=[]
        for r in [.3,1,2,2.6]:
            rows.append(dict(b_Mpc=r,column_factor=column_factor(r,2.6,budget_radius(a0)/MPC),
                             Ne_cm2=N_e(r*MPC,a0,2.6*MPC),EM_cm5=EM(r*MPC,a0,2.6*MPC),
                             gas_mass_Msun=M_req(r*MPC,a0)/MSUN,
                             y_by_kT_keV={str(t):y_of(r*MPC,a0,t,2.6*MPC) for t in [.1,.2,.5]}))
        luminosity=3e-23*1e-6*4*math.pi*(Sigma(a0)/2)**2*(XH/MUE)/MP**2*(2.6*MPC-budget_radius(a0))
        out["footings"][name]=dict(Rin_Mpc=budget_radius(a0)/MPC,rows=rows,
                                      illustrative_Lx_erg_s=luminosity,
                                      illustrative_Fx_erg_s_cm2=xray_flux_cgs(luminosity,D_A(ZREF)*(1+ZREF)**2))
    return out


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    parser.add_argument("--mutate",action="store_true",help="Run the same analytic checks including factor-two T mutation")
    args=parser.parse_args()
    data=result()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(data,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"status":data["status"],"checks":data["checks"]},indent=2))


if __name__=="__main__":
    main()

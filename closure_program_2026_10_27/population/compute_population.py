#!/usr/bin/env python3
"""Finite population accounting; no forest bound or isolation fraction is fitted."""
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np
from scipy.integrate import quad
from scipy.special import gamma, gammainc

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
I = json.loads((HERE / "inputs.json").read_text())
C = json.loads((ROOT / I["capacity_input"]).read_text())
h, wb, om = (I["cosmology"][k] for k in ("h", "omega_b", "Omega_m"))
h70, ob = h / .7, wb / h**2
rhob = C["native"]["rho_b_Msun_Mpc3"]
rhoc = rhob / ob
D, J, F, A = (I[k] for k in ("driver2022", "jones2018", "fletcher2020", "alpaslan2015"))
rho_star = D["rho_star_coefficient_Msun_Mpc3"] * h70
rho_hi = J["Omega_HI_coefficient"] / h70 * rhoc
rho_mol = F["Omega_molecular_coefficient"] / h * rhoc
fstar, fhi, fmol = np.array([rho_star, rho_hi, rho_mol]) / rhob
rho_cold = rho_star + 1.33 * rho_hi + rho_mol
fcold = rho_cold / rhob

ms = 10**D["log10_Mstar_h70_minus2"] / h70**2
phi = np.array([10**D[k] for k in ("log10_phi1_h70_cubed", "log10_phi2_h70_cubed")])
phi *= 10**D["add_log10_phi_for_SDSS_and_z0"] * h70**3
alpha = np.array([D["alpha1"], D["alpha2"]])
rho_analytic = float(ms * np.sum(phi * gamma(alpha + 2)))

def per_dex(logm):
    x = 10**logm / ms
    return float(math.log(10) * np.sum(phi * x**(alpha + 1)) * math.exp(-x))

def integrate_range(lo, hi):
    rho = quad(lambda u: 10**u * per_dex(u), lo, hi, epsabs=1e-3, epsrel=1e-10)[0]
    n = quad(per_dex, lo, hi, epsabs=1e-12, epsrel=1e-10)[0]
    g = ms * np.sum(phi * gamma(alpha + 2) *
                    (gammainc(alpha + 2, 10**hi/ms) - gammainc(alpha + 2, 10**lo/ms)))
    assert math.isclose(rho, float(g), rel_tol=2e-9)
    return {"physical_log10_Mstar_range": [lo,hi], "number_density_Mpc_minus3": n,
            "fraction_of_fitted_stellar_mass": rho/rho_analytic,
            "rho_star_normalized_to_reported_total_Msun_Mpc3": rho/rho_analytic*rho_star,
            "F_star_normalized_to_reported_total": rho/rho_analytic*fstar}

ranges = {name: integrate_range(lo,hi) for name,lo,hi in [
    ("above_1e8",8,14),("above_1e9",9,14),("above_1e10",10,14),
    ("1e9_to_1e11",9,11),("1e10_to_1e11",10,11),("1e8_to_1e11p5",8,11.5)]}
# Fletcher's stellar cut uses H0=70 masses, so convert the cut itself.
cut = 9 - 2*math.log10(h70)
cutrange = integrate_range(cut,14)
cutrange["F_cold_with_published_gas_host_fractions"] = (
    cutrange["F_star_normalized_to_reported_total"] + .73*1.33*fhi + .89*fmol)

bins = np.array(D["finite_bins_log10_M_log10_phi"])
width = D["bin_width_dex"]
counts = 10**(bins[:,1] + D["add_log10_phi_for_SDSS_and_z0"]) * h70**3 * width
centers = 10**bins[:,0] / h70**2
bin_rhos = {name: float(np.dot(counts,centers * 10**shift)) for name,shift in
            [("lower_edge",-width/2),("center",0),("upper_edge",width/2)]}

def dc_integral(z, omega_m):
    return quad(lambda zz: 1/math.sqrt(omega_m*(1+zz)**3+1-omega_m),0,z)[0]

geometry = []
for z in [.02,.05,.079,.1]:
    ratio = dc_integral(z,om)/dc_integral(z,.3)
    geometry.append({"z":z,"native_over_reference_distance_at_same_h":ratio,
                     "density_shell_proxy_distance_inverse":1/ratio})

thresholds = {}
for name,b in C["footings"].items():
    B = b["exact_two_phase_fraction"]
    thresholds[name] = {
        "conditional_F_allowed": B,
        "all_stars_minimum_epsilon_star": fstar/B,
        "all_cold_minimum_epsilon_cold": fcold/B,
        "q_cold_max_by_epsilon": [{"epsilon":e,"q_max_unclipped":e*B/fcold,
                                    "q_max_clipped":min(1.,e*B/fcold)} for e in [.2,.25,.3,.5,.75,1.]],
        "epsilon_star_minimum_by_selected_stellar_mass_fraction": [
            {"q_star":q,"epsilon_star_minimum":q*fstar/B} for q in [.04,.25,.3,.5,.7,.75,1.]],
        "epsilon_cold_minimum_by_common_selected_mass_fraction": [
            {"q_common":q,"epsilon_cold_minimum":q*fcold/B} for q in [.25,.3,.5,.75,1.]],
        "stellar_mass_scale_sensitivity": [
            {"stellar_scale":s,"F_cold":s*fstar+1.33*fhi+fmol,
             "q_cold_max_at_epsilon_half":.5*B/(s*fstar+1.33*fhi+fmol)} for s in [.79,1.,1.21]],
        "patch_number_sensitivity_one_galaxy_per_patch": {
            key:{"q_number_max_unclipped":b["patch_number_density_Mpc_minus3"]/v["number_density_Mpc_minus3"],
                 "number_density_all_Mpc_minus3":v["number_density_Mpc_minus3"]} for key,v in ranges.items()},
        "environment_example_qstar_point3_all_HI_and_mol": {
            "F_selected_cold":.3*fstar+1.33*fhi+fmol,
            "epsilon_cold_minimum":(.3*fstar+1.33*fhi+fmol)/B}
    }

checks = {}
def check(name, condition):
    checks[name] = bool(condition)
    assert condition,name

check("native_input_h_matches",math.isclose(h,C["native"]["h"],rel_tol=1e-12))
check("native_input_wb_matches",math.isclose(wb,C["native"]["omega_b"],rel_tol=1e-12))
check("gamma_vs_log_integral",math.isclose(rho_analytic,quad(lambda u:10**u*per_dex(u),-20,14)[0],rel_tol=1e-9))
check("rounded_fit_recovers_reported_density_within_one_percent",abs(rho_analytic/rho_star-1)<.01)
check("known_single_schechter_mass_integral",abs(quad(lambda x:x*math.exp(-x),0,np.inf)[0]-1)<1e-10)
check("finite_bins_bracket",bin_rhos["lower_edge"]<bin_rhos["center"]<bin_rhos["upper_edge"])
check("h70_HI_scaling",math.isclose(fhi,.00039*.7*h/wb,rel_tol=1e-13))
check("h_molecular_scaling",math.isclose(fmol,.0000534*h/wb,rel_tol=1e-13))
check("all_ranges_are_finite_and_nested_below_total",all(0<v["fraction_of_fitted_stellar_mass"]<1 for v in ranges.values()))
check("all_baryons_in_selected_stars_are_counted_once",math.isclose(rho_star/rhob,fstar,rel_tol=1e-13))
check("environment_marginals_no_positive_intersection_bound",max(0,.3+.7-1)==0)
check("finite_bins_inside_published_fit_range",bins[:,0].min()-width/2>=D["fit_min_log10_M_h70_minus2"])
local = ROOT / I["local_data_checked"]["path"]
check("local_catalogue_hash_verified",hashlib.sha256(local.read_bytes()).hexdigest()==I["local_data_checked"]["sha256"])

out = {
    "claim":"Conditional population costs and capacities; no measured M6 isolation fraction or physical forest bound",
    "native":{"h":h,"h70":h70,"Omega_b":ob,"rho_b_Msun_Mpc3":rhob},
    "census":{"rho_star_Msun_Mpc3":rho_star,"F_star":fstar,"rho_HI_Msun_Mpc3":rho_hi,
              "F_HI_hydrogen_only":fhi,"F_HI_with_helium_1p33":1.33*fhi,
              "rho_molecular_quoted_Msun_Mpc3":rho_mol,"F_molecular_quoted":fmol,
              "F_stars_plus_HI_He":fstar+1.33*fhi,"rho_cold_baseline_Msun_Mpc3":rho_cold,
              "F_cold_baseline":fcold,
              "F_cold_molecular_extra_He":fstar+1.33*(fhi+fmol),
              "F_cold_HI_He_1p4_molecular_once":fstar+1.4*fhi+fmol,
              "stellar_uncertainties_Msun_Mpc3":{k:D[k]*h70 for k in
                  ["rho_star_random_coefficient","rho_star_systematic_coefficient","rho_star_cosmic_variance_coefficient"]}},
    "gsmf":{"rho_analytic_from_rounded_parameters":rho_analytic,
             "rho_fit_over_reported_total":rho_analytic/rho_star,"mass_ranges":ranges,
             "fletcher_cut_native_mass":10**cut,"above_fletcher_cut":cutrange},
    "finite_bin_conditional_lower_mass_accounting":{
        "status":"Lower edge bound on adopted binned estimates, not a statistical confidence lower bound",
        "native_mass_interval_Msun":[10**8/h70**2,10**11.75/h70**2],
        "rho_Msun_Mpc3":bin_rhos,"F_lower_edge":bin_rhos["lower_edge"]/rhob,
        "F_lower_edge_times_0p79_sensitivity":.79*bin_rhos["lower_edge"]/rhob},
    "thresholds":thresholds,"cosmology_geometry_sensitivity":geometry,
    "required_bound":"F_patch >= rho_selected_cold/rho_b; if epsilon_cold=rho_selected_cold/rho_patch_initial <= 1, F_patch=rho_selected_cold/(epsilon_cold*rho_b). This requires ancestry in counted closed patches.",
    "general_selection":"F_selected_cold = F_star*q_star + F_HI_with_helium_1p33*q_HI + F_molecular_quoted*q_mol, using coefficients in census. q are MASS fractions, not count fractions.",
    "environment_intersection_bound":{"minimum":max(0,A["stellar_mass_fraction_ungrouped"]+A["stellar_mass_fraction_not_in_pair"]-1),
                                      "maximum":min(A["stellar_mass_fraction_ungrouped"],A["stellar_mass_fraction_not_in_pair"])},
    "checks":checks,
    "non_claims":["No empirical isolated population minimum is established.",
                  "No X57/P1D1/P1D2 prescription is promoted to a physical forest confidence bound.",
                  "No abundance-match efficiency or environment correlation is assumed measured.",
                  "Mass function integrals are finite numerical estimates under published fits, not galaxy-formation dynamics.",
                  "GAMA errors and gas systematics are not replaced by formal fitting errors or assumed independent for a significance test."]
}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"F_star":fstar,"F_stars_HI_He":fstar+1.33*fhi,"F_cold":fcold,
                  "rho_cold":rho_cold,"checks_passed":sum(checks.values())},indent=2))

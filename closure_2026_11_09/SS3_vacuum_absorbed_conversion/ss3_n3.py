#!/usr/bin/env python3
"""SS3 N3 (FROZEN_CRITERIA.md 3a8a5a9fce): can a perturbation-free vacuum absorb a halo-local energy transfer?
Coupled equations: nabla_mu T^mu_nu(chi) = -Q_nu, nabla_mu T^mu_nu(vac) = +Q_nu, T^mu_nu(vac) = -rho_vac delta^mu_nu, so
-partial_nu rho_vac = Q_nu: Q must be a gradient, i.e. its curl partial_mu Q_nu - partial_nu Q_mu must vanish (integrability).
Q_nu = Gamma(r) rho_chi(r) u_nu with u_nu = (-1, 0, 0, 0) for a static halo (signature -+++). Checked symbolically.
KA: a spatially uniform Gamma rho_chi gives curl 0 (the cosmological, homogeneous case is consistent).
Reported: what local conservation forces, delta rho_vac(x, t) = int Gamma rho_chi dt, and the static-equilibrium check.
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, json
import sympy as sp
t, r = sp.symbols("t r", real=True); Gam = sp.Function("Gamma")(r); rho = sp.Function("rho_chi")(r)
u = [-1, 0, 0, 0]; X = [t, r]
Q = [Gam * rho * u[0], Gam * rho * u[1]]                                   # (t, r) components
curl_tr = sp.simplify(sp.diff(Q[1], t) - sp.diff(Q[0], r))                 # partial_t Q_r - partial_r Q_t
uniform = curl_tr.subs({Gam: sp.Symbol("G0"), rho: sp.Symbol("rho0")}).doit()
# energy equation (nu = t): -partial_t rho_vac = Q_t = -Gamma rho_chi  ->  partial_t rho_vac = Gamma rho_chi (local accumulation)
rv = sp.Function("rho_vac")(t, r)
energy = sp.Eq(sp.diff(rv, t), Gam * rho)
# momentum equation (nu = r): -partial_r rho_vac = Q_r = 0, but partial_r of the accumulated rho_vac = t * partial_r(Gamma rho_chi) != 0
mom_residual = sp.simplify(-sp.diff(t * Gam * rho, r) - Q[1])
out = dict(curl_t_r=str(curl_tr), curl_vanishes_generic=bool(curl_tr == 0), curl_uniform_case=str(uniform), KA_uniform_zero=bool(uniform == 0),
           energy_equation=str(energy), momentum_residual_if_vacuum_accumulates_locally=str(mom_residual),
           status="PASS" if curl_tr == 0 else "FAIL",
           reading=("A w = -1 recipient can absorb only a transfer that is a gradient. For a static halo the transfer Gamma rho_chi u_nu has curl "
                    "-d(Gamma rho_chi)/dr != 0, so no perturbation-free vacuum can take it (FAIL). Energy conservation alone gives "
                    "partial_t rho_vac = Gamma rho_chi: the vacuum would pile up where the halo converts, delta rho_vac = int Gamma rho_chi dt, "
                    "and the momentum equation then has residual -t d(Gamma rho_chi)/dr: a w = -1 gradient with nothing to balance it. "
                    "There is no static configuration (in linear GR a static source with delta p = -delta rho != 0 is inconsistent with Phi = Psi). "
                    "Either local energy-momentum conservation fails (the source's 'no perturbations') or the converted energy stays local and is "
                    "not vacuum. If it stays local, the halo's lensing mass is the pre-conversion halo's: the lane's full-retention KiDS reading "
                    "(SS1 MG3: 0.378 / 0.376 dex), a KiDS FAIL."))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "parts", "n3.json"), "w"), indent=1)
for k, v in out.items(): print(f"{k}: {v}")

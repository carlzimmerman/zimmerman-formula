import json
import numpy as np
import as204_curved_heat_force as m

leaf = m.S3(10)
runs = {}
rngs = np.random.default_rng(204)
m.run_s3(10, 0.05, 0.0, 2.3374, "probe", runs, rngs)
r = runs["probe"]
print("daph_max", r["daph_max"], "f2", r["f2"], "r_curved", r["r_curved_corrected"],
      "r_naive", r["r_naive_flat_transfer"])
print("b0_limit_residual", r["controls"]["b0_limit_residual"])
print("adj_rel", r["controls"]["adjoint_identity_relative_residual"])
print("hess_int_rel", r["controls"]["hessian_integrated_relative_residual"])
print("C0_sup_over_formula", r["constants"]["C0_sup_over_formula"],
      "Cg_sup_over_formula", r["constants"]["Cg_sup_over_formula"])
print("DS ratio", r["controls"]["DS_equals_SD_curved_sq_ratio"],
      "closed", r["controls"]["DS_equals_SD_curved_closed_form_sq"],
      "match", r["controls"]["DS_equals_SD_curved_closed_form_match"])
print("wz", [(w["mode"], round(w["rel_resid"], 4)) for w in r["controls"]["weitzenbock_modes"]])
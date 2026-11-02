#!/usr/bin/env python3
"""HF1 gate 1 numerics: ncdm precision at the m 11 eV FD point, RF5's parameters. Picks the fit's setting. kappa = 1/2 FITTED; not theory closed."""
import sys, json, time; sys.argv = ["x", "none"]; import os
exec(open(os.path.join(os.path.dirname(os.path.abspath("hf1_g1.py")), "hf1_g1.py")).read().split('if __name__ == "__main__":')[0])
L = R["Lik"](); p = np.array([RF1["params"][n] for n in NM])
V = {"tol5": {"tol_ncdm_synchronous": 1e-5,"tol_ncdm_bg": 1e-7},"tol6": {"tol_ncdm_synchronous": 1e-6,"tol_ncdm_bg": 1e-8},"tol7": {"tol_ncdm_synchronous": 1e-7,"tol_ncdm_bg": 1e-9},"tol6trig200": {"tol_ncdm_synchronous": 1e-6,"tol_ncdm_bg": 1e-8,"ncdm_fluid_trigger_tau_over_tau_k":200.0},"tol6trig1000l40": {"tol_ncdm_synchronous": 1e-6,"tol_ncdm_bg": 1e-8,"ncdm_fluid_trigger_tau_over_tau_k":1000.0,"l_max_ncdm":40},"tol7trig1000l60": {"tol_ncdm_synchronous": 1e-7,"tol_ncdm_bg": 1e-9,"ncdm_fluid_trigger_tau_over_tau_k":1000.0,"l_max_ncdm":60}}
out = {}
for k, pr in V.items():
    t = time.time(); c={"name": "kprec", "kind": "HF", "m": 11.0, "spec": "FD", "prec": pr}; o = R["run"]("pr", c, p);
    if o is None: print(k,"FAIL",c.get("class_fail")); continue
    q = L.parts(o, RF1["A"]); out[k] = dict(plik=q["plik"], lowTT=q["lowTT"], s=time.time() - t, h=o["h"]); print(k, out[k], flush=True)
json.dump(out, open("hf1_g1_prec.json", "w"), indent=1)

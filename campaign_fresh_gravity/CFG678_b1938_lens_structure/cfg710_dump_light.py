"""CFG710 (dir CFG678_b1938_lens_structure): dump the stage-1 LIGHT model (no mass info used) for the blind predictions."""
import sys, os, json, runpy, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(os.path.dirname(HERE), "CFG669_b1938_A_photometry", "cfg674_autolens.py")
sys.argv = ["x", "none"]; os.chdir(os.path.dirname(A))
g = runpy.run_path(A)
al = g["al"]; res1 = g["run_stage1"](); i1 = res1.max_log_likelihood_instance
fit = res1.max_log_likelihood_fit
lens = i1.galaxies.lens
ints = {}
for k, v in fit.linear_light_profile_intensity_dict.items():
    ints[str(k.effective_radius)] = float(v)
out = {"theta_E_stage1": float(lens.mass.einstein_radius), "components": []}
grid = al.Grid2D.uniform(shape_native=(801, 801), pixel_scales=0.01, origin=tuple(lens.bulge.centre))
tot = np.zeros(801 * 801)
for name in ("bulge", "disk"):
    lp = getattr(lens, name)
    q, phi = al.convert.axis_ratio_and_angle_from(ell_comps=lp.ell_comps)
    I = ints[str(lp.effective_radius)]
    prof = al.lp.Sersic(centre=lp.centre, ell_comps=lp.ell_comps, intensity=I, effective_radius=lp.effective_radius, sersic_index=lp.sersic_index)
    im = np.asarray(prof.image_2d_from(grid=grid))
    tot += im
    out["components"].append(dict(name=name, intensity=I, R_e=float(lp.effective_radius), n=float(lp.sersic_index), q=float(q), phi_deg=float(phi), centre=list(map(float, lp.centre))))
np.save(os.path.join(HERE, "cfg710_stage1_light_801x801_0p01.npy"), tot.reshape(801, 801))
json.dump(out, open(os.path.join(HERE, "cfg710_stage1_light.json"), "w"), indent=1); print(json.dumps(out, indent=1))

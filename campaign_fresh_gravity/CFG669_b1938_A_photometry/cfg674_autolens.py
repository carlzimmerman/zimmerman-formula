#!/usr/bin/env python3
"""CFG674 Part 4 (criteria c29c55493): PyAutoLens production model of GO 8281 F115W at perturber A.
Run with the isolated env: _external_data/pyautolens_env/venv/bin/python cfg674_autolens.py <stage>
kappa = 1/2 FITTED; cold energy mass required; not theory closed."""
import os, sys, json, math, warnings
warnings.filterwarnings("ignore")
import numpy as np
import autolens as al, autofit as af
HERE = os.path.dirname(os.path.abspath(__file__))
IN = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "_external_data", "cfg668_go8281", "pyautolens_inputs")
OUTP = os.path.join(os.path.dirname(IN), "pyautolens_output")
meta = json.load(open(os.path.join(IN, "f115w_meta.json")))
PS = meta["pixel_scale"]; NUC = tuple(meta["nucleus_arcsec_yx"]); AYX = tuple(meta["A_arcsec_yx"])
ds = al.Imaging.from_fits(pixel_scales=PS, data_path=os.path.join(IN, "f115w_data.fits"),
                          noise_map_path=os.path.join(IN, "f115w_noise.fits"), psf_path=os.path.join(IN, "f115w_psf.fits"))
mask = al.Mask2D.circular(shape_native=ds.shape_native, pixel_scales=PS, radius=1.2, centre=NUC)
ds = ds.apply_mask(mask=mask)
STAGE = (sys.argv[1] if len(sys.argv) > 1 else "smoke") if __name__ == "__main__" else "child"   # spawn-safe (macOS multiprocessing)

if STAGE == "smoke":
    lens = al.Galaxy(redshift=0.881, bulge=al.lp_linear.Sersic(centre=NUC, effective_radius=0.2, sersic_index=4.0),
                     mass=al.mp.Isothermal(centre=NUC, einstein_radius=0.46), shear=al.mp.ExternalShear())
    src = al.Galaxy(redshift=2.059, bulge=al.lp_linear.Sersic(centre=(0.0, 0.0), effective_radius=0.1))
    fit = al.FitImaging(dataset=ds, tracer=al.Tracer(galaxies=[lens, src]))
    print("smoke: figure_of_merit", float(fit.figure_of_merit), "chi2", float(fit.chi_squared), "N", int(mask.pixels_in_mask))
    print("data at A:", float(ds.data.native[int(round((meta['shape'][0]-1)/2 - AYX[0]/PS)), int(round((meta['shape'][1]-1)/2 + AYX[1]/PS))]))
    print("A yx", AYX, "nucleus yx", NUC)

def lens_light_model():
    b1 = af.Model(al.lp_linear.Sersic); b2 = af.Model(al.lp_linear.Sersic)
    b1.centre_0 = af.GaussianPrior(mean=NUC[0], sigma=0.03); b1.centre_1 = af.GaussianPrior(mean=NUC[1], sigma=0.03)
    b2.centre = b1.centre
    return b1, b2

def save_ml(result, name):
    inst = result.max_log_likelihood_instance
    json.dump({"log_likelihood": float(result.log_likelihood) if hasattr(result, "log_likelihood") else None,
               "instance": str(inst)}, open(os.path.join(OUTP, f"{name}_summary.json"), "w"), indent=1)

if STAGE == "1":
    os.makedirs(OUTP, exist_ok=True)
    b1, b2 = lens_light_model()
    mass = af.Model(al.mp.PowerLaw); mass.centre = b1.centre
    mass.einstein_radius = af.UniformPrior(lower_limit=0.3, upper_limit=0.7)
    lens = af.Model(al.Galaxy, redshift=0.881, bulge=b1, disk=b2, mass=mass, shear=af.Model(al.mp.ExternalShear))
    src = af.Model(al.Galaxy, redshift=2.059, bulge=af.Model(al.lp_linear.Sersic))
    model = af.Collection(galaxies=af.Collection(lens=lens, source=src))
    search = af.Nautilus(name="stage1", path_prefix=OUTP, n_live=150, number_of_cores=4, iterations_per_quick_update=5000)
    res = search.fit(model=model, analysis=al.AnalysisImaging(dataset=ds))
    print("STAGE1 max log likelihood:", res.max_log_likelihood_fit.log_likelihood)
    print(res.max_log_likelihood_instance.galaxies.lens.mass)
    print(res.max_log_likelihood_instance.galaxies.lens.shear)

def run_stage1():
    b1, b2 = lens_light_model()
    mass = af.Model(al.mp.PowerLaw); mass.centre = b1.centre
    mass.einstein_radius = af.UniformPrior(lower_limit=0.3, upper_limit=0.7)
    lens = af.Model(al.Galaxy, redshift=0.881, bulge=b1, disk=b2, mass=mass, shear=af.Model(al.mp.ExternalShear))
    src = af.Model(al.Galaxy, redshift=2.059, bulge=af.Model(al.lp_linear.Sersic))
    model = af.Collection(galaxies=af.Collection(lens=lens, source=src))
    search = af.Nautilus(name="stage1", path_prefix=OUTP, n_live=150, number_of_cores=4, iterations_per_quick_update=5000)
    return search.fit(model=model, analysis=al.AnalysisImaging(dataset=ds))

NPIX = int(os.environ.get('CFG674_NPIX', '1000'))
def adapt_from(res):
    """the library's own adapt images (keys = str(path)), converted to writable numpy arrays, plus a Hilbert image-plane mesh"""
    from autogalaxy.analysis.adapt_images import adapt_images as AI
    raw = AI.galaxy_name_image_dict_via_result_from(res)
    imgs = {k: al.Array2D(values=np.array(np.asarray(v.native), dtype=float, copy=True), mask=ds.mask) for k, v in raw.items()}
    SK = "('galaxies', 'source')"
    grid = al.image_mesh.Hilbert(pixels=NPIX, weight_floor=0.2, weight_power=1.0).image_plane_mesh_grid_from(
        mask=ds.mask, adapt_data=imgs[SK])
    return al.AdaptImages(galaxy_name_image_dict=imgs, galaxy_name_image_plane_mesh_grid_dict={SK: grid})

def pixelization():
    return af.Model(al.Pixelization, mesh=al.mesh.Delaunay(pixels=NPIX), regularization=af.Model(al.reg.Adapt))

if STAGE in ("2check", "2", "3", "time2", "2fast", "2nm", "2nm3", "5", "5profile", "5jitter"):
    res1 = run_stage1()
    i1 = res1.max_log_likelihood_instance
    adapt = adapt_from(res1)
if STAGE == "2check":
    src = al.Galaxy(redshift=2.059, pixelization=al.Pixelization(mesh=al.mesh.Delaunay(pixels=NPIX), regularization=al.reg.Adapt()))
    tr = al.Tracer(galaxies=[i1.galaxies.lens, src])
    an = al.AnalysisImaging(dataset=ds, adapt_images=adapt, use_jax=False)
    ad_obj = al.AdaptImages(galaxy_image_dict={src: adapt.galaxy_name_image_dict["('galaxies', 'source')"],
                                               i1.galaxies.lens: adapt.galaxy_name_image_dict["('galaxies', 'lens')"]},
                            galaxy_image_plane_mesh_grid_dict={src: adapt.galaxy_name_image_plane_mesh_grid_dict["('galaxies', 'source')"]})
    fit = al.FitImaging(dataset=ds, tracer=tr, adapt_images=ad_obj)
    print("2check: log_evidence", float(fit.log_evidence), "chi2", float(fit.chi_squared))

def stage2_model(i1, res1, multipoles=(3, 4)):
    lensm = res1.model.galaxies.lens
    mass = af.Model(al.mp.PowerLaw)
    mass.centre = lensm.mass.centre; mass.ell_comps = lensm.mass.ell_comps; mass.einstein_radius = lensm.mass.einstein_radius
    mass.slope = af.UniformPrior(lower_limit=1.5, upper_limit=3.0)
    kw = dict(redshift=0.881, bulge=i1.galaxies.lens.bulge, disk=i1.galaxies.lens.disk, mass=mass,
              shear=af.Model(al.mp.ExternalShear))
    for m in multipoles:
        mp = af.Model(al.mp.PowerLawMultipole, m=m)
        mp.centre = mass.centre; mp.einstein_radius = mass.einstein_radius; mp.slope = mass.slope
        kw[f"multipole_{m}"] = mp
    lens = af.Model(al.Galaxy, **kw)
    src = af.Model(al.Galaxy, redshift=2.059, pixelization=pixelization())
    return af.Collection(galaxies=af.Collection(lens=lens, source=src))

def run_stage2(i1, res1, adapt, multipoles=(3, 4), name="stage2"):
    # one core: the numpy-mode multiprocessing pool deadlocks on macOS spawn (disclosed); ~0.22 s per likelihood
    search = af.Nautilus(name=name, path_prefix=OUTP, n_live=150, number_of_cores=1, iterations_per_quick_update=5000)
    plh = res1.positions_likelihood_from(factor=3.0, minimum_threshold=0.2)   # standard guard vs demagnified sources
    return search.fit(model=stage2_model(i1, res1, multipoles),
                      analysis=al.AnalysisImaging(dataset=ds, adapt_images=adapt, positions_likelihood_list=[plh], use_jax=False))

if STAGE == "2":
    res2 = run_stage2(i1, res1, adapt)
    f2 = res2.max_log_likelihood_fit
    print("STAGE2 log_evidence", float(f2.log_evidence), "chi2", float(f2.chi_squared), "N", int(ds.mask.pixels_in_mask))
    print(res2.max_log_likelihood_instance.galaxies.lens.mass)

if STAGE == "time2":
    import time
    m = stage2_model(i1, res1)
    an = al.AnalysisImaging(dataset=ds, adapt_images=adapt, use_jax=False)
    inst = m.instance_from_prior_medians()
    t = time.time(); ll = an.log_likelihood_function(instance=inst); dt = time.time() - t
    t = time.time(); ll = an.log_likelihood_function(instance=inst); dt2 = time.time() - t
    print(f"TIME2: one stage-2 likelihood {dt:.2f}s (first) / {dt2:.2f}s (second); logL {float(ll):.1f}; free params {m.prior_count}")

EXTRA = []   # extra lens-plane galaxies (Part 5: A's own mass)
# ------------------------------------------------------------------ stage 3: measure A at the stage-2 maximum-likelihood model
def run_stage3(res2=None, tag="", i2=None, ad2=None):
    import autoarray as aa
    from scipy.ndimage import shift as ndshift
    from astropy.io import fits as _f
    i2 = i2 if i2 is not None else res2.max_log_likelihood_instance
    lens2, src2 = i2.galaxies.lens, i2.galaxies.source
    ad2 = ad2 if ad2 is not None else adapt_from(res2)
    SK = "('galaxies', 'source')"
    data0 = np.array(_f.getdata(os.path.join(IN, "f115w_data.fits")), float)
    noise = np.array(_f.getdata(os.path.join(IN, "f115w_noise.fits")), float)
    psf = np.array(_f.getdata(os.path.join(IN, "f115w_psf.fits")), float); psf /= psf.sum()
    n = data0.shape[0]; c = (n - 1) / 2
    pix = meta["pixar_sr"]; to_jy = 1e6 * pix                   # sum of MJy/sr pixels -> Jy
    PSF = al.Convolver.from_fits if False else None

    def point_img(yx, F):                                       # F in summed MJy/sr pixel units, at arcsec (y, x)
        r, col = c - yx[0] / PS, c + yx[1] / PS
        R, C = int(np.floor(r)), int(np.floor(col)); h = psf.shape[0] // 2
        st = ndshift(np.pad(psf, 2), (r - R, col - C), order=3); s0 = st.shape[0] // 2
        im = np.zeros_like(data0)
        for a in range(st.shape[0]):
            for b in range(st.shape[1]):
                j, k = R + a - s0, C + b - s0
                if 0 <= j < n and 0 <= k < n: im[j, k] += st[a, b]
        return im / st.sum() * F

    def amp(data, yx, npix=None):
        d = al.Imaging(data=al.Array2D.no_mask(values=data, pixel_scales=PS),
                       noise_map=al.Array2D.no_mask(values=noise, pixel_scales=PS), psf=ds.psf).apply_mask(mask=mask)
        src = al.Galaxy(redshift=2.059, pixelization=al.Pixelization(
            mesh=al.mesh.Delaunay(pixels=npix or NPIX), regularization=src2.pixelization.regularization))
        grid = ad2.galaxy_name_image_plane_mesh_grid_dict[SK] if not npix else al.image_mesh.Hilbert(
            pixels=npix, weight_floor=0.2, weight_power=1.0).image_plane_mesh_grid_from(mask=d.mask, adapt_data=ad2.galaxy_name_image_dict[SK])
        A = al.Galaxy(redshift=0.881, light=al.lp_linear.PointSource(centre=tuple(yx)))
        tr = al.Tracer(galaxies=[lens2, A, src] + list(EXTRA))
        ad = al.AdaptImages(galaxy_image_dict={src: ad2.galaxy_name_image_dict[SK]}, galaxy_image_plane_mesh_grid_dict={src: grid})
        fit = al.FitImaging(dataset=d, tracer=tr, adapt_images=ad, settings=aa.Settings(use_positive_only_solver=False))
        inv = fit.inversion
        iA = [k for k, o in enumerate(inv.linear_obj_list) if getattr(o, "light_profile_list", None) and
              any(type(lp).__name__ == "PointSource" for lp in o.light_profile_list)]
        kA = sum(getattr(o, "params", 1) for o in inv.linear_obj_list[:iA[0]])
        cov = np.linalg.inv(np.asarray(inv.curvature_reg_matrix))
        return float(inv.reconstruction[kA]), float(np.sqrt(cov[kA, kA])), float(fit.chi_squared), int(d.mask.pixels_in_mask)

    out = {"tag": tag}
    a0, s0, chi2, npx = amp(data0, AYX)
    # calibration: a bright (24 AB) injection fixes amplitude units -> summed-pixel flux
    Fcal = 3631 * 10 ** (-0.4 * 24.0) / to_jy
    acal = amp(data0 + point_img(AYX, Fcal), AYX)[0]; kcal = (acal - a0) / Fcal
    fA, sstat = a0 / kcal, s0 / abs(kcal) * math.sqrt(max(chi2 / npx, 1.0))
    # same-radius positions (12 x 30 deg), skipping within 0.25"
    rA = math.hypot(AYX[0] - NUC[0], AYX[1] - NUC[1]); ph = math.atan2(AYX[0] - NUC[0], AYX[1] - NUC[1]); amps = []
    for k in range(12):
        p = ph + math.radians(30 * k); yx = (NUC[0] + rA * math.sin(p), NUC[1] + rA * math.cos(p))
        if math.hypot(yx[0] - AYX[0], yx[1] - AYX[1]) < 0.25: continue
        amps.append(amp(data0, yx)[0] / kcal)
    amps = np.array(amps); spos = 1.4826 * np.median(np.abs(amps - np.median(amps)))
    sysv = [amp(data0, AYX, npix=int(NPIX * f))[0] / kcal for f in (0.7, 1.4)]
    ssys = 0.5 * (max(sysv + [fA]) - min(sysv + [fA]))
    stot = math.sqrt(sstat ** 2 + spos ** 2 + ssys ** 2)
    ab = lambda F: -2.5 * math.log10(F * to_jy / 3631) if F > 0 else float("inf")
    S = fA / stot
    out.update(chi2_nu=chi2 / npx, kcal=kcal, f_A_Jy=fA * to_jy, sig_stat_Jy=sstat * to_jy, sig_pos_Jy=spos * to_jy,
               sig_sys_Jy=ssys * to_jy, sig_tot_Jy=stot * to_jy, S=S, m_A=ab(fA), m_lim_2sig=ab(2 * stot),
               same_radius_Jy=(amps * to_jy).tolist(), floor_2sig_chi2nu1=ab(2 * s0 / abs(kcal)))
    # tooth: 29.0 AB injection
    Ft = 3631 * 10 ** (-0.4 * 29.0) / to_jy
    at = amp(data0 + point_img(AYX, Ft), AYX)[0] / kcal - fA
    out["tooth"] = dict(recovered_AB=ab(at), S=at / stot, bites=bool(abs(ab(at) - 29.0) <= 0.5 and at / stot >= 3))
    PRED = {"canonical": (30.88, 32.07), "alt": (31.02, 32.21)}
    for f, (faint, excl) in PRED.items():
        if not out["tooth"]["bites"]: v = "NOT DIAGNOSTIC (tooth fails)"
        elif S >= 3 and out["m_A"] < 25.7: v = "NOT DIAGNOSTIC (contamination)"
        elif S >= 3 and out["m_A"] <= faint: v = "SURVIVES"
        elif S < 2 and out["m_lim_2sig"] > excl: v = "EXCLUDED"
        elif out["m_lim_2sig"] < faint: v = "NOT DIAGNOSTIC"
        else: v = "TENSION"
        out[f"verdict_{f}"] = v
    json.dump(out, open(os.path.join(HERE, f"cfg674_stage3{tag}_results.json"), "w"), indent=1)
    print("STAGE3" + tag, json.dumps({k: v for k, v in out.items() if k != "same_radius_Jy"}, indent=1))
    return out

if STAGE == "3":
    res2 = run_stage2(i1, res1, adapt)
    run_stage3(res2)

if STAGE == "2fast":     # PREVIEW ONLY (no verdict weight): maximum-likelihood optimiser on the identical stage-2 model
    plh = res1.positions_likelihood_from(factor=3.0, minimum_threshold=0.2)
    search = af.LBFGS(name="stage2_lbfgs", path_prefix=OUTP, number_of_cores=1)
    resf = search.fit(model=stage2_model(i1, res1), analysis=al.AnalysisImaging(dataset=ds, adapt_images=adapt,
                                                                                 positions_likelihood_list=[plh], use_jax=False))
    inst = resf.max_log_likelihood_instance.galaxies.lens
    q, phi = al.convert.axis_ratio_and_angle_from(ell_comps=inst.mass.ell_comps)
    print("STAGE2FAST slope", inst.mass.slope, "theta_E", inst.mass.einstein_radius, "q_M", q, "PA_M", phi,
          "m3", inst.multipole_3.multipole_comps, "m4", inst.multipole_4.multipole_comps, "shear", inst.shear.gamma_1, inst.shear.gamma_2)
    print("STAGE2FAST chi2", float(resf.max_log_likelihood_fit.chi_squared))

if STAGE == "2nm":       # PREVIEW ONLY (no verdict weight): Nelder-Mead on the identical stage-2 likelihood; failures -> -inf
    from scipy.optimize import minimize
    plh = res1.positions_likelihood_from(factor=3.0, minimum_threshold=0.2)
    m = stage2_model(i1, res1)
    an = al.AnalysisImaging(dataset=ds, adapt_images=adapt, positions_likelihood_list=[plh], use_jax=False)
    names = m.model_component_and_parameter_names
    def neg(u):
        u = np.clip(u, 1e-6, 1 - 1e-6)
        try:
            inst = m.instance_from_unit_vector(list(u))
            v = float(an.log_likelihood_function(instance=inst))
            return -v if np.isfinite(v) else 1e30
        except Exception:
            return 1e30
    u0 = np.full(m.prior_count, 0.5)
    best = None
    for r in range(3):
        st = u0 if best is None else np.clip(best.x + np.random.default_rng(r).normal(0, 0.03, u0.size), 0.01, 0.99)
        o = minimize(neg, st, method="Nelder-Mead", options=dict(maxfev=2500, xatol=1e-4, fatol=0.5, adaptive=True))
        if best is None or o.fun < best.fun: best = o
        print(f"2nm restart {r}: -logL {o.fun:.1f}", flush=True)
    inst = m.instance_from_unit_vector(list(np.clip(best.x, 1e-6, 1 - 1e-6))).galaxies.lens
    q, phi = al.convert.axis_ratio_and_angle_from(ell_comps=inst.mass.ell_comps)
    print("STAGE2NM slope", inst.mass.slope, "theta_E", inst.mass.einstein_radius, "q_M", q, "PA_M", phi,
          "m3", inst.multipole_3.multipole_comps, "m4", inst.multipole_4.multipole_comps, "shear", inst.shear.gamma_1, inst.shear.gamma_2, flush=True)
    print("STAGE2NM -logL", best.fun, flush=True)


if STAGE == "2nm3":     # Nautilus stage 2 NOT RUN (12-h rule: 2000 evals in 11 h); ML model by Nelder-Mead (deterministic restart 0), then stage 3
    from scipy.optimize import minimize
    plh = res1.positions_likelihood_from(factor=3.0, minimum_threshold=0.2)
    m = stage2_model(i1, res1)
    an = al.AnalysisImaging(dataset=ds, adapt_images=adapt, positions_likelihood_list=[plh], use_jax=False)
    def neg(u):
        u = np.clip(u, 1e-6, 1 - 1e-6)
        try:
            v = float(an.log_likelihood_function(instance=m.instance_from_unit_vector(list(u))))
            return -v if np.isfinite(v) else 1e30
        except Exception:
            return 1e30
    UF = os.path.join(OUTP, "stage2_nm_best_u.npy")
    if os.path.exists(UF):
        ub = np.load(UF)
    else:
        o = minimize(neg, np.full(m.prior_count, 0.5), method="Nelder-Mead", options=dict(maxfev=2500, xatol=1e-4, fatol=0.5, adaptive=True))
        ub = np.clip(o.x, 1e-6, 1 - 1e-6); np.save(UF, ub); print(f"2nm3: -logL {o.fun:.1f}", flush=True)
    i2 = m.instance_from_unit_vector(list(ub))
    L2 = i2.galaxies.lens; q, phi = al.convert.axis_ratio_and_angle_from(ell_comps=L2.mass.ell_comps)
    print("2nm3 ML: slope", L2.mass.slope, "theta_E", L2.mass.einstein_radius, "q_M", q, "PA_M", phi, flush=True)
    json.dump({"u": ub.tolist(), "names": [str(n) for n in m.model_component_and_parameter_names]}, open(os.path.join(HERE, "cfg674_stage2_ml_nm.json"), "w"), indent=1)
    run_stage3(tag="_nmML", i2=i2, ad2=adapt)


if STAGE == "5":        # Part 5 (criteria 73fc35c96): A's own mass in the lens model
    import autoarray as aa
    from scipy.optimize import minimize_scalar
    plh = res1.positions_likelihood_from(factor=3.0, minimum_threshold=0.2)
    m = stage2_model(i1, res1)
    ub = np.array(json.load(open(os.path.join(HERE, "cfg674_stage2_ml_nm.json")))["u"])
    i2 = m.instance_from_unit_vector(list(ub))
    SK = "('galaxies', 'source')"; src2 = i2.galaxies.source
    def ll_sub(th, with_light=True):
        src = al.Galaxy(redshift=2.059, pixelization=al.Pixelization(mesh=al.mesh.Delaunay(pixels=NPIX), regularization=src2.pixelization.regularization))
        gals = [i2.galaxies.lens, src, al.Galaxy(redshift=0.881, mass=al.mp.IsothermalSph(centre=AYX, einstein_radius=max(th, 1e-6)))]
        if with_light: gals.append(al.Galaxy(redshift=0.881, light=al.lp_linear.PointSource(centre=AYX)))
        ad = al.AdaptImages(galaxy_image_dict={src: adapt.galaxy_name_image_dict[SK]},
                            galaxy_image_plane_mesh_grid_dict={src: adapt.galaxy_name_image_plane_mesh_grid_dict[SK]})
        f = al.FitImaging(dataset=ds, tracer=al.Tracer(galaxies=gals), adapt_images=ad, settings=aa.Settings(use_positive_only_solver=False))
        return float(f.log_likelihood)
    TH1 = 0.0050
    o = minimize_scalar(lambda t: -ll_sub(t), bounds=(0.0, 0.05), method="bounded", options=dict(xatol=2e-4))
    TH2 = float(o.x)
    dll = ll_sub(TH2, True) - ll_sub(TH2, False)
    print(f"PART5: theta_E,sub fixed {TH1}, free best {TH2:.4f}; M3 dlogL(light at A | M2 mass) = {dll:.2f}", flush=True)
    summary = {"theta_sub_M1": TH1, "theta_sub_M2": TH2, "dlogL_light_M3": dll}
    for tag, th in (("_P5M1", TH1), ("_P5M2", TH2)):
        EXTRA[:] = [al.Galaxy(redshift=0.881, mass=al.mp.IsothermalSph(centre=AYX, einstein_radius=th))]
        r = run_stage3(tag=tag, i2=i2, ad2=adapt)
        a = np.array(r["same_radius_Jy"]); med = np.median(a); mad = 1.4826 * np.median(np.abs(a - med))
        summary[tag] = dict(S=r["S"], m_A=r["m_A"], f_A_nJy=r["f_A_Jy"] * 1e9, vs_controls_sigma=(r["f_A_Jy"] - med) / mad,
                            rank=int((a < r["f_A_Jy"]).sum()), n=len(a), tooth=r["tooth"], verdict=r["verdict_canonical"])
    rob = all(summary[t]["vs_controls_sigma"] >= 3 for t in ("_P5M1", "_P5M2"))
    absb = any(summary[t]["vs_controls_sigma"] < 2 for t in ("_P5M1", "_P5M2"))
    summary["diagnostic"] = "ROBUST TO A'S MASS" if rob else ("ABSORBED BY A'S MASS" if absb else "IN BETWEEN")
    json.dump(summary, open(os.path.join(HERE, "cfg674_part5_results.json"), "w"), indent=1, default=float)
    print("PART5 SUMMARY", json.dumps(summary, indent=1, default=float), flush=True)

if STAGE == "5profile":   # diagnostic only: likelihood profile of A's mass (does the JWST arc itself prefer A's mass?)
    import autoarray as aa
    plh = res1.positions_likelihood_from(factor=3.0, minimum_threshold=0.2)
    m = stage2_model(i1, res1); ub = np.array(json.load(open(os.path.join(HERE, "cfg674_stage2_ml_nm.json")))["u"]); i2 = m.instance_from_unit_vector(list(ub))
    SK = "('galaxies', 'source')"; src2 = i2.galaxies.source
    def ll(th):
        src = al.Galaxy(redshift=2.059, pixelization=al.Pixelization(mesh=al.mesh.Delaunay(pixels=NPIX), regularization=src2.pixelization.regularization))
        gals = [i2.galaxies.lens, src, al.Galaxy(redshift=0.881, light=al.lp_linear.PointSource(centre=AYX))]
        if th > 0: gals.append(al.Galaxy(redshift=0.881, mass=al.mp.IsothermalSph(centre=AYX, einstein_radius=th)))
        ad = al.AdaptImages(galaxy_image_dict={src: adapt.galaxy_name_image_dict[SK]}, galaxy_image_plane_mesh_grid_dict={src: adapt.galaxy_name_image_plane_mesh_grid_dict[SK]})
        return float(al.FitImaging(dataset=ds, tracer=al.Tracer(galaxies=gals), adapt_images=ad, settings=aa.Settings(use_positive_only_solver=False)).log_likelihood)
    prof = {th: ll(th) for th in (0.0, 0.0025, 0.004, 0.005, 0.006, 0.0075, 0.01, 0.02)}
    b = max(prof.values()); print("PROFILE", {k: round(v - b, 2) for k, v in prof.items()}, flush=True)
    json.dump({str(k): v for k, v in prof.items()}, open(os.path.join(HERE, "cfg674_part5_massprofile.json"), "w"), indent=1)

if STAGE == "5jitter":    # diagnostic only: A's light amplitude under tiny lens perturbations (mesh re-triangulation systematic)
    import autoarray as aa
    plh = res1.positions_likelihood_from(factor=3.0, minimum_threshold=0.2)
    m = stage2_model(i1, res1); ub = np.array(json.load(open(os.path.join(HERE, "cfg674_stage2_ml_nm.json")))["u"]); i2 = m.instance_from_unit_vector(list(ub))
    SK = "('galaxies', 'source')"; src2 = i2.galaxies.source; to_jy = 1e6 * meta["pixar_sr"]; kcal = 0.9679391778396114
    def fa(th):
        src = al.Galaxy(redshift=2.059, pixelization=al.Pixelization(mesh=al.mesh.Delaunay(pixels=NPIX), regularization=src2.pixelization.regularization))
        A = al.Galaxy(redshift=0.881, light=al.lp_linear.PointSource(centre=AYX))
        gals = [i2.galaxies.lens, A, src] + ([al.Galaxy(redshift=0.881, mass=al.mp.IsothermalSph(centre=AYX, einstein_radius=th))] if th > 0 else [])
        ad = al.AdaptImages(galaxy_image_dict={src: adapt.galaxy_name_image_dict[SK]}, galaxy_image_plane_mesh_grid_dict={src: adapt.galaxy_name_image_plane_mesh_grid_dict[SK]})
        f = al.FitImaging(dataset=ds, tracer=al.Tracer(galaxies=gals), adapt_images=ad, settings=aa.Settings(use_positive_only_solver=False))
        inv = f.inversion
        k = sum(getattr(o, "params", 1) for o in inv.linear_obj_list[:[j for j, o in enumerate(inv.linear_obj_list) if getattr(o, "light_profile_list", None) and any(type(lp).__name__ == "PointSource" for lp in o.light_profile_list)][0]])
        return float(inv.reconstruction[k]) / kcal * to_jy * 1e9, float(f.log_likelihood)
    rows = {th: fa(th) for th in (0.0, 0.001, 0.002, 0.0025, 0.003, 0.004, 0.005, 0.006, 0.0075)}
    for th, (fA, l) in rows.items(): print(f"JITTER theta_sub {th:.4f}: f_A {fA:6.2f} nJy, logL {l:.1f}", flush=True)
    v = np.array([r[0] for r in rows.values()]); print(f"JITTER spread: min {v.min():.2f} max {v.max():.2f} std {v.std():.2f} nJy", flush=True)
    json.dump({str(k): v for k, v in rows.items()}, open(os.path.join(HERE, "cfg674_part5_jitter.json"), "w"), indent=1)

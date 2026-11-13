"""Independent finite image-matrix/evidence/profile checks, all inputs read-only."""
import hashlib
import json
import math
import sys
from pathlib import Path
import numpy as np
from scipy import linalg, signal
from astropy.io import fits

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
BASE = HERE.parent
sys.path[:0] = [str(BASE), str(BASE/"image_inversion")]
from inversion import setup as old_setup
from inversion_continuous import setup as continuous_setup
from lens_models import sie_parameters, sie_deflection, AqualLens


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    tracked = [Path(__file__).resolve(), BASE/"image_inversion/inversion.py",
        BASE/"image_inversion/inversion_continuous.py",BASE/"lens_models.py",
        BASE/"fit_images.py",BASE/"fit_images_v2.py",
        BASE/"image_fit_01/result.json", BASE/"image_fit_02/result.json",
        BASE/"library_01/library.npz"]
    before = {str(p):sha(p) for p in tracked}
    inv = old_setup(supersample=2)
    p = sie_parameters()
    inv.operator(lambda X,N:sie_deflection(X,N,**p))
    rng = np.random.default_rng(173)
    x = rng.normal(size=(100,100))
    direct = signal.convolve2d(x, inv.psf, mode="same", boundary="fill", fillvalue=0)
    convolution_error = float(np.max(np.abs((inv.P@x.ravel()).reshape(100,100)-direct)))
    keep = rng.choice(inv.mask.sum(),40,replace=False)
    D = inv.D[keep]
    noise = inv.noise[inv.mask][keep]
    delta = (inv.data-inv.lens)[inv.mask][keep]
    Q = linalg.block_diag(math.exp(6.4)*inv.R, np.diag([4.,100.]))
    WD,y = D/noise[:,None],delta/noise
    H,b = WD.T@WD+Q,WD.T@y
    coef = linalg.solve(H,b,assume_a="pos")
    res = y-WD@coef
    integrated = -.5*(res@res+coef@Q@coef+np.linalg.slogdet(H)[1]
        -np.linalg.slogdet(Q)[1]+np.log(2*np.pi*noise**2).sum())
    covariance = np.diag(noise**2)+D@linalg.solve(Q,D.T,assume_a="pos")
    covariance_form = -.5*(delta@linalg.solve(covariance,delta,assume_a="pos")
        +np.linalg.slogdet(covariance)[1]+40*np.log(2*np.pi))
    with fits.open(BASE/"inputs/results/deflections.fits") as h:
        Y,X = np.array(h[1].data),np.array(h[2].data)
    iy,ix = np.indices(X.shape)
    ax,an = sie_deflection((ix-50.5)*.1,(iy-50.5)*.1,**p)
    sie_error = float(np.sqrt(np.mean((ax-X)**2+(an+Y)**2)))
    eigen = np.linalg.eigvalsh(inv.R)
    result = {"assertion_tested":"PSF matrix versus direct convolution; Gaussian precision-form marginal likelihood versus direct covariance; released SIE+shear map; source-basis boundary continuity; local mass-profile step ladder",
        "non_claims":"No calibrated physical likelihood, final posterior, absolute field accuracy, or theory pass/fail",
        "rng_seed":173,"inputs_sha256_before":before,
        "PSF_convolution_max_absolute_error":convolution_error,
        "Gaussian_40pixel_precision_logevidence":float(integrated),
        "Gaussian_40pixel_covariance_logevidence":float(covariance_form),
        "Gaussian_evidence_difference":float(integrated-covariance_form),
        "SIE_released_map_vector_RMS_arcsec":sie_error,
        "source_prior_eigenvalue_range":[float(eigen[0]),float(eigen[-1])],
        "boundary_checks":[],"mass_profiles":[]}
    lens = AqualLens()
    for label,setup,folder in [("old_hard_window",old_setup,"image_fit_01"),
                               ("continuous_tents",continuous_setup,"image_fit_02")]:
        edge = setup(nsource=3,source_pixel=1.,source_center=(0.,0.))
        brightness = []
        for beta in [-1.-1e-7,-1.+1e-7]:
            edge.operator(lambda X,N:(X-beta,N))
            brightness.append(float((edge.fullB@np.ones(9)).reshape(100,100)[50,50]))
        result["boundary_checks"].append({"version":label,"brightness":brightness,
            "brightness_jump":brightness[1]-brightness[0]})
        obj = setup(supersample=2)
        rec = json.loads((BASE/folder/"result.json").read_text())
        m,g1,g2,z = rec["solutions"][-1]["parameters"]
        rows = []
        for h in [1e-6,1e-5,1e-4,4e-4,8e-4,1.6e-3,3.2e-3]:
            values = []
            for mm in [m-h,m,m+h]:
                r = obj.evaluate(lambda X,N,mm=mm:lens.deflection(X,N,mm,g1,g2),
                    log_regularization=z,return_arrays=False)
                values.append(r["score"])
            rows.append({"h_dex":h,"left_delta_logevidence":values[0]-values[1],
                "right_delta_logevidence":values[2]-values[1],
                "minus_log_curvature":-(values[2]-2*values[1]+values[0])/h**2})
        fit = obj.evaluate(lambda X,N:lens.deflection(X,N,m,g1,g2),
                          log_regularization=z,posterior_uncertainty=True)
        s,sd = fit["source"],fit["source_std"]
        border = np.zeros_like(s,dtype=bool)
        border[[0,-1],:]=True
        border[:,[0,-1]]=True
        result["mass_profiles"].append({"version":label,"parameters":[m,g1,g2,z],
            "fixed_other_parameter_mass_profile":rows,
            "edge_source_max_absolute_value":float(np.abs(s[border]).max()),
            "edge_source_max_absolute_mean_over_std":float((np.abs(s)/sd)[border].max()),
            "source_negative_count":int((s<0).sum()),
            "source_negative_gt3conditional_std_count":int(((s<0)&(-s/sd>3)).sum())})
    after = {str(p):sha(p) for p in tracked}
    assert before == after
    assert convolution_error < 1e-12
    assert abs(integrated-covariance_form) < 1e-8
    assert sie_error < 1e-12
    assert result["boundary_checks"][0]["brightness_jump"] > .9
    assert abs(result["boundary_checks"][1]["brightness_jump"]) < 1e-6
    result["inputs_sha256_after"] = after
    result["outcome"] = "Gaussian/convolution/shear checks passed; old boundary discontinuity reproduced; corrected basis continuous; local Gaussian curvature is not step stable in either version"
    (HERE/"image_numerics_check.json").write_text(json.dumps(result,indent=2)+"\n")
    text = json.dumps(result,indent=2)+"\n"
    (HERE/"raw_diagnostics.log").write_text(text)
    print(json.dumps({k:v for k,v in result.items() if k not in ["inputs_sha256_before","inputs_sha256_after","mass_profiles"]},indent=2))


if __name__ == "__main__":
    main()

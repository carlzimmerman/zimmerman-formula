"""Read-only comparison of canonical deflection library with a direct field.

Run using /private/tmp/forj0332-fit-venv/bin/python -B, one BLAS thread.
No model/input/library files are changed. Outputs stay in numerical_review.
This tests interpolation, not absolute PDE or physical theory accuracy.
"""
import hashlib
import json
import sys
from pathlib import Path
import numpy as np

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
BASE = HERE.parent
sys.path.insert(0, str(BASE))
from aqual_lensing import make_field, projected_deflection, geometry
from lens_models import AqualLens


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    paths = [Path(__file__).resolve(), BASE/"aqual_lensing.py", BASE/"lens_models.py",
             BASE/"library_01/library.npz", BASE/"inputs/results/coolest_sersic.json",
             BASE.parent/"closure_2026_11_06/QX4_udg/aqual.py"]
    before = {str(p): sha(p) for p in paths}
    lib = AqualLens()
    a = np.load(BASE/"library_01/library.npz")
    q, re, n, m = float(a["q"]), float(a["re_geom"]), float(a["n"]), 12.03
    field = make_field(10**m, re/np.sqrt(q)*geometry()[0], n, q,
                       nr=320, nt=64, tol=2e-8)
    rows = []
    for tag, radii, angles in [
        ("off_grid", [.5, 1., 1.5, 2., 3., 5., 7.], np.deg2rad([0, 22.5, 45, 67.5, 90])),
        ("on_map_grid", a["rad"][[70, 85, 100, 115, 130]], a["angle"][[0,16,32,48,64]]),
    ]:
        r,t = np.meshgrid(radii, angles, indexing="ij")
        u,v = r*np.cos(t), r*np.sin(t)
        co,si = np.cos(lib.angle),np.sin(lib.angle)
        X,N = lib.cx+co*u-si*v,lib.cn+si*u+co*v
        ax,an = lib.deflection(X,N,m)
        au,av = co*ax+si*an,-si*ax+co*an
        du,dv = projected_deflection(field,u,v,nlos=256)
        error = np.hypot(au-du,av-dv)
        relative = error/np.hypot(du,dv)
        rows.append({"kind":tag,"radius_arcsec":r.ravel().tolist(),
            "angle_degrees":np.rad2deg(t).ravel().tolist(),
            "vector_absolute_error_arcsec":error.ravel().tolist(),
            "vector_relative_error":relative.ravel().tolist(),
            "max_absolute_error_arcsec":float(error.max()),
            "max_relative_error":float(relative.max())})
    after = {str(p): sha(p) for p in paths}
    assert before == after
    result = {"assertion_tested":"At logM=12.03 and named positions, compare library interpolation with same-grid directly converged AQUAL field/projection",
        "non_claims":"Not an absolute AQUAL field accuracy bound, posterior error bound, or empirical theory test",
        "inputs_sha256_before":before,"inputs_sha256_after":after,
        "logmass":m,"field_residual":field["residual"],"nr":320,"nt":64,"nlos":256,
        "comparisons":rows,"status":"completed"}
    (HERE/"library_interpolation_check.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ["inputs_sha256_before","inputs_sha256_after","comparisons"]},indent=2))
    print(json.dumps([{k:r[k] for k in ["kind","max_absolute_error_arcsec","max_relative_error"]} for r in rows],indent=2))


if __name__ == "__main__":
    main()

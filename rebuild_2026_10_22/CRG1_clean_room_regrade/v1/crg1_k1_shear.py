"""K1 shear mock. --flip: sign of the excess flipped against the same target; must exit 1."""
from crg1_core import *
import sys
import crg1_clusters as C

def run(flip=False, out="k1_shear"):
    D = C.Data(); ST = C.stacks(); CSS = C.all_css(); h = 0.672
    d = C.load_or_build("C1_f0.034_g0.005_h0.672", C.fn_C1(D, ST, CSS, h, SC["fstar"]["primary"], SC["gas_dex"]["gs4"]))
    vC = d["vC_own_canonical"]; g = D.geo[h]
    Ainj = 1.30; Ause = (1 - (Ainj - 1)) if flip else Ainj
    den = g["W"] * g["Bst"]
    Dm = np.where(den > 0, Ause * vC / np.where(den > 0, den, 1.0), 0.0)
    M = C.Meas(D, h, Dov=Dm, leak0=True)
    t = C.keys_table(M, vC, vC, "canonical")
    k = t["G-OUT-all"]; target = (Ainj - 1) / k["sigma"]
    ok_deg = abs(k["Z"] - target) <= 0.10
    # As written the mock has no scatter: sigma is rounding error and the check is degenerate (NEW_AMBIGUITIES NA6).
    # Non-degenerate twin: real-E Gaussian scatter, with a common shift removing its OUTER sum over I so A stays exact.
    rng = np.random.default_rng(20261101)
    eps = rng.normal(size=vC.shape) * np.where(den > 0, D.c["E"][:, g["hi"]], 0.0)
    I = D.I; oo = C.BANDS["OUTER"]
    sh = (den[I][:, oo] * eps[I][:, oo]).sum() / den[I][:, oo].sum()
    eps[np.ix_(I, oo)] -= sh
    M2 = C.Meas(D, h, Dov=Dm + eps, leak0=True)
    k2 = C.keys_table(M2, vC, vC, "canonical")["G-OUT-all"]; target2 = (Ainj - 1) / k2["sigma"]
    ok_nd = abs(k2["Z"] - target2) <= 0.10
    ok = ok_deg and ok_nd
    r = dict(A_inj=Ainj, A_used=Ause, flip=flip, as_written=dict(A_rec=k["A"], sigma=k["sigma"], Z=k["Z"], target_Z=target, passed=bool(ok_deg), note="degenerate: zero scatter"),
             with_scatter=dict(A_rec=k2["A"], sigma=k2["sigma"], Z=k2["Z"], target_Z=target2, passed=bool(ok_nd)), passed=bool(ok), tol=0.10)
    save_part(out, r); log(str(r))
    return ok

if __name__ == "__main__":
    flip = "--flip" in sys.argv
    sys.exit(0 if run(flip, "k1_shear_FLIP" if flip else "k1_shear") else 1)

"""AS2 gate G-MAT: matter heat kernels (AS2_PREREGISTRATION.md).
Usage: python3 as2_gmat.py     (no MUTATE control is pre-registered for this gate; exit 0 iff every check passes)
(i)  S^4 traces (b0, b2/R, b4/R^2) of the bare Laplacians on scalars, Dirac spinors and 1-forms: Vassilevich hep-th/0306138 sec. 4.1
     (a0nobou, a2nobou, a4nobou) with E = 0 and the bundle curvature (spinor with explicit gamma matrices); scalar and 1-form also from the
     S^4 spectra (CPR table taba2) by Euler-Maclaurin.
(ii) assembled full operators (scalar Delta; Dirac Delta + R/4; vector Delta + Ric minus two scalar ghosts) = Vassilevich sec. 4.2.2 table
     (Christensen-Duff a, b, c, d) on S^4: a4/R^2 = (1/180)(d - b/12) in (4 pi)^-2 units; a0, a2 as frozen."""
import sys
sys.dont_write_bytecode = True
import sympy as sp
import as2_common as A

fails = []


def chk(tag, ok, msg):
    print(("  [PASS] " if ok else "  [FAIL] ") + tag + "  " + msg)
    if not ok:
        fails.append(tag)


def run(verbose=True):
    spec = A.spectra_heat_kernels()
    vb = {k: A.vassilevich_bare(k) for k in ("S", "V", "spinor")}
    if verbose:
        print("G-MAT (i)  bare Laplacians on S^4: (b0, b2/R, b4/R^2)")
        for k in ("S", "V"):
            print(f"    {k:7s} spectra (Euler-Maclaurin) {spec[k]}   Vassilevich {vb[k]}")
        print(f"    spinor  Vassilevich with explicit gamma matrices {vb['spinor']}")
    chk("G-MAT(i) scalar", tuple(spec["S"]) == tuple(vb["S"]), "spectra == Vassilevich (E = 0)")
    chk("G-MAT(i) 1-form", tuple(spec["V"]) == tuple(vb["V"]), "spectra (transverse + longitudinal) == Vassilevich (Omega = Riemann)")
    chk("G-MAT(i) spinor", vb["spinor"][0] == 4 and vb["spinor"][1] == sp.Rational(2, 3), f"spinor bundle dim 4, b2/R = 2/3; b4/R^2 = {vb['spinor'][2]}")
    # (ii) assembled full operators: Delta + E' with constant E' (E' = R/4 for Dirac and for Ric on vectors), a2 = b2 - E' b0, a4 = b4 - E' b2 + E'^2 b0/2
    def shift(b, Ep):
        return (b[0], b[1] - Ep * b[0], b[2] - Ep * b[1] + Ep**2 * b[0] / 2)
    sc = vb["S"]
    di = shift(vb["spinor"], sp.Rational(1, 4))
    vv = shift(vb["V"], sp.Rational(1, 4))
    ve = tuple(a - 2 * b for a, b in zip(vv, sc))
    CD = {"scalar": (1, 1, 30 * 0 - 6, sp.Rational(90) * sp.Rational(1, 36)), "Dirac": (-sp.Rational(7, 2), -11, 6, 0), "vector": (-13, 62, 18, 0)}
    target_a4 = {k: sp.Rational(1, 180) * (v[3] - sp.Rational(v[1], 12)) for k, v in CD.items()}
    frozen = {"scalar": (1, sp.Rational(1, 6), sp.Rational(29, 2160)), "Dirac": (4, -sp.Rational(1, 3), sp.Rational(11, 2160)),
              "vector": (2, -sp.Rational(2, 3), -sp.Rational(31, 1080))}
    if verbose:
        print("\nG-MAT (ii)  full one-loop operators assembled from the bare traces (a0, a2/R, a4/R^2) vs Christensen-Duff (Vassilevich table)")
    for nm, got in (("scalar", sc), ("Dirac", di), ("vector", ve)):
        if verbose:
            print(f"    {nm:7s} assembled {tuple(got)}  Christensen-Duff a4/R^2 = {target_a4[nm]}  frozen {frozen[nm]}")
        chk("G-MAT(ii) " + nm, tuple(got) == frozen[nm] and got[2] == target_a4[nm], "a0, a2, a4 exact")
    return not fails, spec, vb


if __name__ == "__main__":
    print("MODE: NORMAL")
    ok, _, _ = run()
    print("\nCHECKS FAILED:", fails if fails else "none")
    sys.exit(0 if ok else 1)

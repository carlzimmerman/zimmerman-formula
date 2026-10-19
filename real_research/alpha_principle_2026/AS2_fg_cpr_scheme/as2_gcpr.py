"""AS2 gates G-CPR-EH and G-CPR-R2 (pure gravity in the CPR f(R) scheme, AS2_PREREGISTRATION.md + Amendment 1).
Usage: python3 as2_gcpr.py [MUTATE_1 | MUTATE_2]
  MUTATE_1: sign of the graviton contribution (TT, xi, (h, sigma) blocks) flipped in the trace -> G-CPR-EH (i) must FAIL (exit 1).
  MUTATE_2: R^2 (f'') term removed from the spin-0 h Hessian only -> G-CPR-R2 must FAIL (exit 1).
Normal mode exits 0 iff all checks pass."""
import sys
sys.dont_write_bytecode = True
import numpy as np
import sympy as sp
import as2_common as A

MODE = sys.argv[1] if len(sys.argv) > 1 and __name__ == "__main__" else "NORMAL"
fails = []
N_FROZEN = 725760


def chk(tag, ok, msg):
    print(("  [PASS] " if ok else "  [FAIL] ") + tag + "  " + msg)
    if not ok:
        fails.append(tag)


def heat_kernels():
    spec = A.spectra_heat_kernels()
    spec["spinor"] = A.vassilevich_bare("spinor")
    return spec


def run(mode="NORMAL", verbose=True):
    m1, m2 = mode == "MUTATE_1", mode == "MUTATE_2"
    HK = heat_kernels()
    ok_tab = all(tuple(HK[k]) == tuple(A.HK_TABLE_CPR[k]) for k in ("S", "V", "VT", "TT"))
    chk("HK-CPR", ok_tab, "S^4 coefficients from the spectra equal CPR table taba6: " +
        ", ".join(f"{k} {tuple(HK[k])}" for k in ("S", "V", "VT", "TT")))
    X, det = A.X_gravity(HK, with_eta=True, mutate1=m1, mutate2=m2, order_f=2, detail=True)
    if verbose:
        print("\n  contributions to X(R) = (16 pi^2/V) d_t Gamma_k (pure gravity, n = 2 couplings, Taylor R^0..R^2):")
        for nm, c in det:
            print(f"    {nm:26s} R^0: {sp.factor(c.coeff(A.R, 0))}")
    chk("no-gdot0", sp.diff(X, A.gd0) == 0, "d_t f (the g_0 flow) does not enter, as CPR state")
    Y = A.george(order_f=2)
    tx, ty = A.taylor(X, 2), A.taylor(Y, 2)
    # normalisation fixed by the coupling-independent (ghost/Jacobian) terms
    const_x = sp.simplify(sum(c.coeff(A.R, 0) for nm, c in det if nm.startswith(("ghost", "third", "J_", "xi", "sigma"))))
    Rr = A.R
    const_y = sp.simplify(sp.series(-1008 * (511 * Rr**2 - 360 * Rr - 1080) / (Rr - 3) - 2016 * (607 * Rr**2 - 360 * Rr - 2160) / (Rr - 4), Rr, 0, 1).removeO())
    Nfit = sp.simplify(const_y / const_x)
    print(f"\n  normalisation N = Y_const/X_const = {Nfit}  (frozen: {N_FROZEN})")
    diffs = [sp.simplify(ty[i] - N_FROZEN * tx[i]) for i in range(3)]
    for i in range(3):
        print(f"    R^{i}: george - {N_FROZEN} X = {sp.factor(diffs[i])}")
    chk("G-CPR-EH(i)", Nfit == N_FROZEN and diffs[0] == 0 and diffs[1] == 0, "R^0 and R^1 coefficients equal CPR 'george' / 725760 exactly")
    chk("G-CPR-R2(i)", Nfit == N_FROZEN and diffs[2] == 0, "R^2 coefficient equals CPR 'george' / 725760 exactly")
    # (ii) fixed points of the pure-gravity truncations n = 1, 2 from MY derived X
    res = {}
    for n, tgt, tol in ((1, (0.1297, 0.9878), 1e-3), (2, (0.1294, 1.5633, 1.514e-3), 1e-2)):
        Xn = A.X_gravity(HK, with_eta=True, mutate1=m1, mutate2=m2, order_f=n)
        bet = A.beta_system(Xn, n)
        roots, f, J = A.find_roots(bet, n, grid=False,
                                   extra_starts=[A.from_glb([G_, L_] + ([B_] if n == 2 else []))
                                                 for G_ in (0.3, 0.7, 1.0, 1.5, 2.0, 3.0) for L_ in (-0.5, 0.0, 0.1, 0.13, 0.2, 0.3)
                                                 for B_ in ((0.0, 1e-3, 2e-3, 5e-3, -1e-3) if n == 2 else (None,))])
        rows = []
        for r in roots:
            glb = A.to_glb(r)
            th = A.crit_exponents(J, r)
            rows.append((r, glb, th))
        match = None
        for r, glb, th in rows:
            Lt, Gt = glb[1], glb[0]
            okm = abs(Lt / tgt[0] - 1) <= tol and abs(Gt / tgt[1] - 1) <= tol
            if n == 2:
                okm = okm and abs(r[2] / tgt[2] - 1) <= tol
            if okm:
                match = (r, glb, th)
        print(f"\n  n = {n} pure gravity: real roots (g~0, g~1{', g~2' if n == 2 else ''}) -> (Lambda~, G~):")
        for r, glb, th in rows:
            print(f"    g~ = {np.array2string(np.array(r), precision=6)}  Lambda~ = {glb[1]:.5f}  G~ = {glb[0]:.5f}  theta = {np.array2string(th, precision=3)}")
        tag = "G-CPR-EH(ii)" if n == 1 else "G-CPR-R2(ii)"
        if match is not None:
            r, glb, th = match
            msg = f"Lambda~* = {glb[1]:.5f}, G~* = {glb[0]:.5f}" + (f", g~2* = {r[2]:.6e}" if n == 2 else "") + \
                  f" vs CPR Table 1 {tgt} (tol {tol*100:g}%); theta = {np.array2string(th, precision=3)} (CPR Table 2: " + \
                  ("2.382 +- 2.168 i" if n == 1 else "1.376 +- 2.325 i, 26.862") + ", reported only)"
        else:
            msg = f"no root matches CPR Table 1 n = {n} {tgt} within {tol*100:g}%"
        chk(tag, match is not None, msg)
        res[n] = rows
    return not fails, res


if __name__ == "__main__":
    if MODE not in ("NORMAL", "MUTATE_1", "MUTATE_2"):
        sys.exit(f"unknown mode {MODE}")
    print("MODE:", MODE)
    ok, _ = run(MODE)
    print("\nCHECKS FAILED:", fails if fails else "none")
    sys.exit(0 if ok else 1)

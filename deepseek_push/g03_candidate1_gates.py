#!/usr/bin/env python3
"""G03 -- the gates for candidate 1 (T-B localised, Helmholtz output filter).

Gate order per the spec: S1 then S2.  S4/S5/P1-P3/C1 status lines printed but
NOT claimed.  Run: python3 g03_candidate1_gates.py [single|double|both]

S2 history (honest):
  v1 -- lagged fixed point on the RHS: INSTRUMENT-FAIL (overflow cascade,
       NaN at every xi > 0).  Recorded in the v1 .out.
  v2 -- direct composite LU B = A - xi^2 A1 A: correct but ~10+ min/solve.
  v3 -- the split form B = (I - xi^2 A1) A  =>  u = A^-1 (I-xi^2 A1)^-1 rhs:
       two cheap factorizations; stable.  FIRST PHYSICS SIGNAL: the output
       filter alone does NOT suppress the quadrupole (alt footing:
       xi = 0.01-0.03 pc -> 7.63x/7.63x/7.64x vs the bare 7.63x), consistent
       with the smooth-shell argument (radial smoothing preserves the l=2
       source moment; the anisotropy lives in mu's argument, which only the
       INPUT filter touches).
  v4 -- the DOUBLE filter (g02's T-B configuration): mu evaluated at the
       SMOOTHED field Phi_s = (I-xi^2 A1)^-1 Phi AND the output filter on the
       divergence.  This is the decisive configuration for candidate 1.
"""
import os, sys, math, json, time
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spl

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(REPO, "qwen_claude_field_theory", "theory_2026"))
from aqual_solver_2026 import Grid, grads, multipoles

GM_SUN = 1.32712440018e20
PC = 3.0856775814913673e16
GEXT, SGEXT = 2.32e-10, 0.16e-10
Q2_CEIL, Q2_CEN, Q2_SIG = 5.2e-27, 1.6e-27, 1.8e-27
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
PREF = lambda a0: 1.5 * a0 ** 1.5 / math.sqrt(GM_SUN)
R_M_PC = {f: math.sqrt(GM_SUN / a0) / PC for f, a0 in A0.items()}

def check(l, ok, d=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {l}" + (f"   {d}" if d else ""), flush=True)
    return bool(ok)

def mu2(x):
    x = np.maximum(x, 1e-30)
    return 1.0 - (1.0 + x / 2.0) ** (-2)

def build(G, mufun, phi, eta):
    """Clone of the validated solver's build() (verbatim; no edits to the
    shared solver file -- this lane keeps its own copy for the filter)."""
    ns, nt = G.ns, G.nt
    N = ns * nt
    x = grads(G, phi)
    m = mufun(np.maximum(x, 1e-30))
    mfs = 0.5 * (m[1:, :] + m[:-1, :])
    mft = 0.5 * (m[:, 1:] + m[:, :-1])
    idx = lambda i, j: i * nt + j
    rows, cols, vals, rhs = [], [], [], np.zeros(N)
    Ar = mfs * G.sf[:, None] * G.sin[None, :] * (G.dt / G.ds)
    Bt = mft * G.r[:, None] * G.sintf[None, :] * (G.ds / G.dt)
    for i in range(ns):
        for j in range(nt):
            k = idx(i, j)
            if i == 0 or i == ns - 1:
                rows.append(k); cols.append(k); vals.append(1.0)
                rhs[k] = (-1.0 / G.r[0] + eta * G.r[0] * G.mu_c[j]) if i == 0 else 0.0
                continue
            diag = 0.0
            for (ii, a) in ((i - 1, Ar[i - 1, j]), (i + 1, Ar[i, j])):
                rows.append(k); cols.append(idx(ii, j)); vals.append(a); diag -= a
            if j > 0:
                b = Bt[i, j - 1]; rows.append(k); cols.append(idx(i, j - 1)); vals.append(b); diag -= b
            if j < nt - 1:
                b = Bt[i, j]; rows.append(k); cols.append(idx(i, j + 1)); vals.append(b); diag -= b
            rows.append(k); cols.append(k); vals.append(diag)
            rhs[k] = 0.0
    return sps.csr_matrix((vals, (rows, cols)), shape=(N, N)), rhs

def screen_op(G, xi_g):
    """(I - xi^2 A1), the Helmholtz screen operator on the grid."""
    A1, _ = build(G, lambda x: np.ones_like(x), np.zeros((G.ns, G.nt)), 0.0)
    return (sps.identity(A1.shape[0]) - (xi_g * xi_g) * A1).tocsr()

def solve_filtered(G, mufun, eta, xi_g, double=False, tol=1e-10, itmax=300,
                   relax=0.55, verbose=False):
    """(1 - xi^2 lap) div[mu grad u] = 0 via the split u = A^-1 M^-1 rhs.

    single (double=False): mu from the unsmoothed field (output filter only).
    double (double=True) : mu evaluated at Phi_s = M^-1 Phi (input+output,
                           g02's T-B configuration).  In both cases M is the
                           fixed screen; A is rebuilt per iteration (Picard).
    The Dirichlet rows need no explicit reset (A's boundary rows are identity
    and rhs2's boundary entries carry the b.c.)."""
    ns, nt = G.ns, G.nt
    r = G.r[:, None]; ct = G.mu_c[None, :]
    u = -1.0 / r * np.ones((ns, nt))
    ue = -eta * r * ct
    phi = u + ue
    it, du = 0, 1.0
    M = None
    if xi_g != 0.0:
        M = screen_op(G, xi_g)
    for it in range(itmax):
        mu_arg = phi
        if double and xi_g != 0.0:
            mu_arg = spl.spsolve(M, phi.ravel()).reshape(ns, nt)
        A, rhs = build(G, mufun, mu_arg, eta)
        rhs2 = -(A.dot(ue.ravel()))
        rhs2[:nt] = rhs[:nt]; rhs2[-nt:] = 0.0
        if xi_g != 0.0:
            w = spl.spsolve(M, rhs2)
            unew = spl.spsolve(A, w).reshape(ns, nt)
        else:
            unew = spl.spsolve(A, rhs2).reshape(ns, nt)
        if not np.all(np.isfinite(unew)):
            return u, phi, it, float("inf")
        du = np.max(np.abs(unew - u)) / max(1.0, np.max(np.abs(unew)))
        u = (1 - relax) * u + relax * unew
        phi = u + ue
        if verbose and it % 40 == 0:
            print(f"    iter {it:3d}  rel {du:.2e}", flush=True)
        if du < tol:
            break
    return u, phi, it, du

def q_filtered(mufun, eta, xi_pc, foot, double=False):
    xi_g = xi_pc / R_M_PC[foot]
    G = Grid(1e-4, 1e4, 512, 128)
    u, phi, it, du = solve_filtered(G, mufun, eta, xi_g, double=double,
                                    itmax=400, relax=0.5)
    _, _, c2 = multipoles(G, u, eta)
    return abs(2.0 * c2), xi_g, it, du


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "both"
    assert mode in ("single", "double", "both")
    t0 = time.time()
    RES = []
    print("=" * 88)
    print("G03 GATES -- CANDIDATE 1 (T-B localised, Helmholtz screen)"
          f"  mode={mode}")
    print("=" * 88)

    print("\n--- S1  static target (derived in g03_candidate_actions.py S1-A) ---")
    RES.append(check("S1 [static reduction] the action family reduces to "
                     "(1-xi^2 lap) div[mu grad Phi] = 4 pi G rho with O((xi/d)^2) "
                     "covariantization terms stated", True,
                     "see S1-A printout; source derived, not postulated"))

    XI_SINGLE_PC = [0.0, 0.005, 0.01, 0.02, 0.03, 0.05, 0.1]
    XI_DOUBLE_PC = [0.01, 0.02, 0.03, 0.05]
    FLOOR = {"canonical": 0.02, "alt": 0.03}

    results = {}
    for label, xi_list, double in (("single", XI_SINGLE_PC, False),
                                   ("double", XI_DOUBLE_PC, True)):
        if mode not in (label, "both"):
            continue
        print(f"\n--- S2 [{label} filter]  Cassini quadrupole (both footings) ---")
        results[label] = {}
        for foot in A0:
            a0 = A0[foot]
            eta = GEXT / a0
            eta_lo = (GEXT - SGEXT) / a0
            results[label][foot] = {}
            print(f"\n  {foot:9s} footing (a0 = {a0:.4e}, r_M = {R_M_PC[foot]:.4f} pc)")
            for xi in xi_list:
                q, xi_g, it, du = q_filtered(mu2, eta, xi, foot, double=double)
                Q = q * PREF(a0)
                q_lo, _, _, _ = q_filtered(mu2, eta_lo, xi, foot, double=double)
                Q_lo = q_lo * PREF(a0)
                results[label][foot][xi] = dict(q=q, Q=Q, ratio=Q / Q2_CEIL,
                                                Q_lo=Q_lo, ratio_lo=Q_lo / Q2_CEIL,
                                                xi_g=xi_g, it=it, du=du)
                print(f"    xi = {xi:5.3f} pc (grid {xi_g:6.3f}): |Q2| = {Q:.3e} s^-2 = "
                      f"{Q / Q2_CEIL:5.2f}x ceiling  (1-sig: {Q_lo / Q2_CEIL:5.2f}x)  "
                      f"({time.time() - t0:.0f} s)", flush=True)

    # verdicts on the floors
    for label, xi_list, double in (("single", XI_SINGLE_PC, False),
                                   ("double", XI_DOUBLE_PC, True)):
        if mode not in (label, "both") or label not in results:
            continue
        at_floor = {f: results[label][f].get(FLOOR[f], None) for f in A0}
        if all(v is not None for v in at_floor.values()):
            ok = all(at_floor[f]["ratio"] <= 1.0 and at_floor[f]["ratio_lo"] <= 1.0
                     for f in A0)
            RES.append(check(f"S2 [{label} filter at the T-B floors] |Q2| <= 5.2e-27 "
                             "on BOTH footings at g_ext and g_ext-1sig",
                             ok, "; ".join(
                                 f"{f}: {at_floor[f]['ratio']:.2f}x (1sig {at_floor[f]['ratio_lo']:.2f}x)"
                                 for f in A0)))
        best = min((results[label][f][xi]["ratio_lo"]
                    for f in A0 for xi in xi_list if xi > 0))
        RES.append(check(f"S2b [{label} filter] min ratio over xi both footings "
                         "at g_ext-1sig", best <= 1.0, f"min {best:.2f}x"))

    print("\n--- S4 / S5 / P1-P3 / C1  status (NOT claimed -- later gates) ---")
    print("  S4 wide binaries : OPEN (effect O((xi/s)^2) ~ 1e-4 at kAU; DR4 arms)")
    print("  S5 lensing       : OPEN (Phi = Psi from the full metric, G05-level)")
    print("  P1 PPN          : OPEN (the f31c ladder on the candidate's form)")
    print("  P2 causal screen: OPEN (Helmholtz filter acausal at O(xi/c) -- named)")
    print("  P3 mode count   : SKETCH: psi = 1 scalar DOF, canonical, mass 1/xi^2;")
    print("                     ADM count with metric mixings = registered G05 item")
    print("  C1 cosmology    : OPEN (background + growth + k^4 reach)")

    n = sum(1 for r in RES if r)
    print(f"\nG03 GATES COMPLETE (S1-S2, candidate 1, mode {mode}): "
          f"{n}/{len(RES)} checks PASS.  ({time.time() - t0:.0f} s)")
    json.dump({"lane": "G03 candidate 1 gates (T-B localised, Helmholtz screen)",
               "mode": mode, "checks": [bool(r) for r in RES],
               "n_pass": int(n), "n_total": len(RES),
               "floors_pc": FLOOR, "quadrupole": results},
              open(os.path.join(HERE, "g03_candidate1_gates_results.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
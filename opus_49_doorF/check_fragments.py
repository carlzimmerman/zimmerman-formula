#!/usr/bin/env python3
"""
Door F certified-fragment checks (numeric, not proofs).

Fragment A -- Positive character expansion of the Wilson weight on SU(2).
  e^{beta cos(theta)} = sum_{n>=0} c_n(beta) chi_n(cos theta),  chi_n = Chebyshev U_n,
  c_n(beta) = (2/pi) int_0^pi e^{beta cos theta} sin theta sin((n+1) theta) dtheta.
  OS78 / Menotti-Pelissetto 87 need c_n(beta) >= 0 for beta >= 0. Checked here
  to mpmath precision on a grid; a rigorous proof exists (Bessel/positive-definite
  argument), this run is numerical evidence.

Fragment B -- 2D compact U(1) exact area-law constant.
  <U_ell> = (I_1(beta)/I_0(beta))^{area(ell)}  ==>  |<W_ell>| = e^{-c(beta) area},
  c(beta) = -ln(I_1(beta)/I_0(beta)) > 0 for every beta > 0. Numerically evaluated.

Fragment C -- 't Hooft-scaling obstruction of the repo's I15 gap bound.
  I15 (PROOF.md:173-189): gap >= 3x/16 for x >= X_d, X_d independent of N and volume.
  At fixed 't Hooft coupling lambda = N*x, the window x >= X_d needs N <= lambda/X_d:
  the bound is NOT N-uniform at fixed lambda, and gap >= 3 lambda/(16 N) -> 0 as N -> oo.
  Elementary arithmetic, evaluated here at X_d = 1 placeholder (X_d is unevaluated
  on the record; only the structural failure is being checked, no claim about X_d).
"""
import json
import mpmath as mp

mp.mp.dps = 40
results = {}

# ---------- Fragment A ----------
def su2_character_coeff_quad(beta, n):
    """c_n(beta) = (2/pi) int_0^pi e^{beta cos t} sin t sin((n+1) t) dt (quadrature)."""
    f = lambda t: mp.exp(beta * mp.cos(t)) * mp.sin(t) * mp.sin((n + 1) * t)
    return (2 / mp.pi) * mp.quad(f, [0, mp.pi])

def su2_character_coeff_exact(beta, n):
    """Closed form: c_n(beta) = I_n(beta) - I_{n+2}(beta), from
       e^{beta cos t} = I_0 + 2 sum I_k cos(kt)  and  sin t sin((n+1)t)
       = (cos(nt) - cos((n+2)t))/2.  Order-monotonicity of I_n in n (beta>=0
       fixed) gives c_n >= 0 exactly."""
    return mp.besseli(n, beta) - mp.besseli(n + 2, beta)

betas = [0.05, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0]
nmax = 60
mins = {}
max_qerr = mp.mpf(0)
for b in betas:
    mn = None
    for n in range(0, nmax + 1):
        v = su2_character_coeff_exact(b, n)
        if mn is None or v < mn:
            mn = v
        # validate closed form against quadrature for a sparse subsample
        if n % 7 == 0:
            q = su2_character_coeff_quad(b, n)
            err = abs(q - v)
            if err > max_qerr:
                max_qerr = err
    mins[str(b)] = float(mn)
all_nonneg = all(v >= 0 for v in mins.values())
mn_high = None
for n in range(0, 300):
    v = su2_character_coeff_exact(0.05, n)
    if mn_high is None or v < mn_high:
        mn_high = v
results["A_min_coeff_over_grid"] = mins
results["A_all_nonneg_on_grid"] = bool(all_nonneg)
results["A_min_coeff_beta005_n0_299"] = float(mn_high)
results["A_max_quadrature_vs_closedform_err"] = float(max_qerr)
results["A_note"] = ("EXACT lemma c_n(beta)=I_n(beta)-I_{n+2}(beta) >= 0 for all n, beta >= 0 "
                     "(I_n decreasing in order n at fixed beta: classical modified-Bessel monotonicity). "
                     "Quadrature vs closed form agree to the stated error; the grid check is exact arithmetic "
                     "on the closed form, the proof is the Bessel identity + order monotonicity.")

# ---------- Fragment B ----------
cs = {}
for b in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 100.0]:
    r = mp.besseli(1, b) / mp.besseli(0, b)
    c = -mp.log(r)
    cs[str(b)] = float(c)
results["B_area_law_constant_c_beta"] = cs
results["B_note"] = "2D U(1): |<W_ell>| = e^{-c(beta) area}; exact, all beta>0 (textbook, Migdal/2D gauge solvability)"

# ---------- Fragment C ----------
# gap(x,N) >= 3x/16 (I15, x>=X_d). At 't Hooft lambda = N x: gap >= 3 lambda/(16 N).
for lam in [1.0, 5.0]:
    g = lambda N: 3 * lam / (16 * N)
    results["C_tHooft_gap_at_" + str(lam)] = {
        "N=2": float(g(2)), "N=10": float(g(10)), "N=1000": float(g(1000)),
        "window_requires": "N <= lambda/X_d (uniformity in N fails at fixed lambda)",
    }
results["C_note"] = "structural check: I15 bound degrades to 0 at fixed 't Hooft coupling; no N-uniform strong-coupling window can exist at fixed lambda by this route (matches I15 PROOF.md:188-189)"

out = {"date": "2026-09-22", "dps": 40, "results": results}
with open("fragment_checks.json", "w") as fh:
    json.dump(out, fh, indent=2)
print(json.dumps(results, indent=2))
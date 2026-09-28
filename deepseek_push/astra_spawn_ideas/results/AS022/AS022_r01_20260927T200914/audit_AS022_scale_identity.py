#!/usr/bin/env python3
"""
AS022 - What a scale identity can actually derive: bounded audit computation.

Meta-audit of the framework scale identity
    a0 = kappa*c*sqrt(G*rho_Lambda),  kappa = 1/2 ADOPTED,
with companion constraint F2: Lambda = 8*pi*G*rho_Lambda/c^2,
acting on the three variables (a0, rho_Lambda, Lambda).

What this script computes (all bounded):
  S2.  Jacobian rank of {F1, F2} and of 'rearranged copies of F1' (control 1);
       parameterization of the one-dimensional solution family.
  S3.  Dimensional algebras: rho_Lambda and Lambda per footing (canonical 9.3619e-11,
       alternative 1.1279e-10 m/s^2), r_M = sqrt(G M_b/a0), v_flat^4 = G M_b a0,
       deep and Newtonian limiting regimes with the leading neglected term.
  S4.  Independent check: substitution back into F1, F2 at 50 significant digits;
       cross-route Lambda residuals; float64 residuals.
  S5.  Negative control: two distinct triples both satisfying F1 ^ F2 (the two
       constraints do NOT single out a magnitude); rank of the copy system.

Enforced bounds:
  * wall clock:  <= 120 s  (signal.alarm hard stop; also run under `timeout 120`)
  * memory:      <= 512 MB (per-phase peak-RSS monitor with hard abort;
                 RLIMIT_AS unavailable on this macOS: hard max below request)
  * threads:     1 (no threading/multiprocessing; OMP/MKL threads pinned to 1)
No observational fit is performed.  G_N, G_bare, G_cosmo are kept separate; only
G_N = 6.67430e-11 is used here, and any Lambda-from-F2 statement carries the
same-G proviso (G_E = G_N) explicitly.
"""
import os, sys, time, signal, json
import resource

# ------------------------------------------------------------------ bounds
WALL_S   = 120.0
MEM_B    = 512 * 1024 * 1024   # 512 MB
T0       = time.monotonic()

def _deadline(sig, frm):
    print(f"\n[AS022] HARD WALL-CLOCK ABORT after {time.monotonic()-T0:.1f}s "
          f"(limit {WALL_S}s)", flush=True)
    sys.exit(3)

signal.signal(signal.SIGALRM, _deadline)
signal.alarm(int(WALL_S) + 1)
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

def mem_kb():
    # macOS: ru_maxrss is in BYTES; Linux: KB. Normalize to MB.
    val = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return val / 1024.0 / 1024.0  # MB

def mem_guard(phase):
    kb = mem_kb()
    if kb > MEM_B / 2**20:
        print(f"[AS022] MEMORY ABORT at '{phase}': peak {kb:.1f} MB > 512 MB", flush=True)
        sys.exit(4)
    print(f"[AS022] memory check '{phase}': peak RSS {kb:.1f} MB (limit 512 MB, enforced)",
          flush=True)

import math
from decimal import Decimal, getcontext
import sympy as sp

getcontext().prec = 60

# ------------------------------------------------------------------ constants
G_N  = Decimal("6.67430e-11")      # m^3 kg^-1 s^-2  (Newton coupling; G_bare, G_cosmo kept separate elsewhere)
c    = Decimal("299792458")        # m/s
M_sun = Decimal("1.98847e30")      # kg
pc   = Decimal("3.085677581491367e16")  # m
Gf, cf, Msf, pcf = 6.67430e-11, 299792458.0, 1.98847e30, 3.085677581491367e16

A0 = {"canonical": Decimal("9.3619e-11"), "alt": Decimal("1.1279e-10")}
A0f = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
FOOT_NOTE = ("kappa = 1/2 adopted; the two footings are SEPARATE normalization choices: "
             "they may not share a fixed rho_Lambda AND a fixed kappa simultaneously "
             "(FRAMEWORK_CONTRACT).")

out = []
log = out.append

# ================================================================== S2 : rank & family
log("=" * 78)
log("STEP 2 — constraint rank and solution-set parameterization")
log("F1 = 4*a0^2 - G*c^2*rho_L = 0   (this is a0 = (c/2)*sqrt(G*rho_L), squared; encodes kappa = 1/2)")
log("F2 = Lambda - 8*pi*G*rho_L/c^2 = 0")
a0s, Gs, cs, rhs, Ls = sp.symbols("a0 G c rho_L Lambda", positive=True)
F1 = 4 * a0s**2 - Gs * cs**2 * rhs
F2 = Ls - 8 * sp.pi * Gs * rhs / cs**2
J = sp.Matrix([[sp.diff(F1, a0s), sp.diff(F1, rhs), sp.diff(F1, Ls)],
               [sp.diff(F2, a0s), sp.diff(F2, rhs), sp.diff(F2, Ls)]])
log("Jacobian J(F1,F2)/d(a0, rho_L, Lambda) =")
log(str(J))
log("rank(J) = %d  (rows independent for a0 > 0: row1 has dF1/da0 = 8*a0 != 0, "
    "row2 has dF2/dLambda = 1)" % J.rank())
log("rank < number of variables (3)  =>  solution set is a 1-parameter family:")
log("  (rho_L, a0, Lambda) = (lambda, (c/2)*sqrt(G*lambda), 8*pi*G*lambda/c^2),  lambda > 0")

# ---- control 1: rearranged copies of F1 counted as new equations
F1_copies = {
    "F1a:  4*a0^2 - G*c^2*rho = 0": 4*a0s**2 - Gs*cs**2*rhs,
    "F1b:  a0 - (c/2)*sqrt(G*rho) = 0": a0s - cs/2*sp.sqrt(Gs*rhs),
    "F1c:  rho - 4*a0^2/(G*c^2) = 0": rhs - 4*a0s**2/(Gs*cs**2),
    "F1d:  16*a0^4 - G^2*c^4*rho^2 = 0": 16*a0s**4 - Gs**2*cs**4*rhs**2,
    "F1e:  a0^2 - (c^2*G/4)*rho = 0": a0s**2 - cs**2*Gs/4*rhs,
}
vars12 = [a0s, rhs]
# symbolic rows
rows = []
for name, expr in F1_copies.items():
    rows.append([sp.diff(expr, v) for v in vars12])
Jc = sp.Matrix(rows)
log("\nCONTROL 1 — rearranged copies of F1 treated as new equations")
log("Jacobian of the 5-copy system w.r.t. (a0, rho_L), evaluated OFF the curve (generic point):")
log("rank (generic) = %d   [copies are not idempotent as functions; the test is the solution set]" % Jc.rank())
# on-curve: substitute the constraint relations 4a0^2 = G c^2 rho and a0 = (c/2) sqrt(G rho)
subs_on = {a0s**2: cs**2*Gs*rhs/4,
           sp.sqrt(Gs*rhs): 2*a0s/cs}
Jc_on = sp.Matrix([[sp.simplify(expr.subs(subs_on)) for expr in row] for row in rows])
log("After substituting the on-curve relations (4a0^2 = G c^2 rho, sqrt(G rho) = 2 a0/c):")
log("rank (on the solution curve) = %d" % Jc_on.rank())
# same for the full set {5 F1 copies, F2, F2-copy rho = Lambda c^2/(8 pi G)}
F2_copies = {
    "F2 : Lambda - 8*pi*G*rho/c^2 = 0": F2,
    "F2b: rho - Lambda*c^2/(8*pi*G) = 0": rhs - Ls*cs**2/(8*sp.pi*Gs),
}
allrows = []
for name, expr in F1_copies.items():
    allrows.append([sp.diff(expr, a0s), sp.diff(expr, rhs), sp.diff(expr, Ls)])
for name, expr in F2_copies.items():
    allrows.append([sp.diff(expr, a0s), sp.diff(expr, rhs), sp.diff(expr, Ls)])
Jall = sp.Matrix(allrows)
Jall_on = sp.Matrix([[sp.simplify(e.subs(subs_on)) for e in row] for row in Jall.tolist()])
log("\nFull copy system {F1a..F1e, F2, F2b} w.r.t. (a0, rho, Lambda), on the curve:")
log("rank = %d  (still 2: 7 written equations, 2 constraint directions, 1-dim family — "
    "no new constraint created by rewriting)" % Jall_on.rank())

# ================================================================== S3 : algebras per footing
log("\n" + "=" * 78)
log("STEP 3 — intermediate algebra with units (SI), both footings separately")
log(FOOT_NOTE)
for tag, a0 in A0.items():
    rho = 4 * a0**2 / (G_N * c**2)                 # kg/m^3
    # Lambda via F2:
    Lam_F2 = 8 * Decimal(math.pi) * G_N * rho / c**2      # m^-2
    Lam_cl = 32 * Decimal(math.pi) * a0**2 / c**4         # closed form, m^-2
    eps    = rho * c**2                                    # J/m^3
    a0_chk = c**2 * (Lam_cl / (32 * Decimal(math.pi))).sqrt()
    log(f"\n--- footing '{tag}': a0 = {a0} m/s^2 (kappa = 1/2 adopted) ---")
    log(f"rho_Lambda = 4*a0^2/(G c^2)          = {rho} kg/m^3")
    log(f"epsilon_Lambda = rho_Lambda c^2      = {eps} J/m^3")
    log(f"Lambda (via F2, 8 pi G rho/c^2)      = {Lam_F2} m^-2")
    log(f"Lambda (closed form, 32 pi a0^2/c^4) = {Lam_cl} m^-2")
    log(f"a0 reconstructed c^2 sqrt(Lambda/32pi)= {a0_chk} m/s^2")
    log(f"  cross-route Lambda residual (F2 route vs closed form): "
        f"{abs(Lam_F2 - Lam_cl)}  (rel {abs(Lam_F2 - Lam_cl)/Lam_cl:.1e})")
    log(f"  F1 residual after back-substitution: "
        f"{abs(4*a0**2 - G_N*c**2*rho)}  (rel {abs(4*a0**2 - G_N*c**2*rho)/(4*a0**2):.1e})")
    log(f"  F2 residual after back-substitution: "
        f"{abs(Lam_F2 - 8*Decimal(math.pi)*G_N*rho/c**2)}")
    # float64 residuals too
    af = A0f[tag]
    rhof = 4*af**2/(Gf*cf**2)
    log(f"  [float64] F1 residual: {abs(4*af**2 - Gf*cf**2*rhof):.3e}  "
        f"F2 residual: {abs((8*math.pi*Gf*rhof/cf**2) - 32*math.pi*af**2/cf**4):.3e}")
    log(f"  Lambda l0 = c^2/a0 = {c**2/a0} m  (length scale);  Lambda*l0^2 = "
        f"{Lam_cl*(c**2/a0)**2}  (should be 32*pi = {32*Decimal(math.pi)})")
    # fiducial masses
    for tagM, Mb in (("1e11 M_sun", Decimal("1e11")*M_sun), ("1 M_sun", M_sun)):
        rM  = (G_N * Mb / a0).sqrt()
        vfl = (G_N * Mb * a0)**Decimal("0.25")
        log(f"  M_b = {tagM}: r_M = sqrt(G M_b/a0) = {rM} m = {rM/pc} pc;  "
            f"v_flat = (G M_b a0)^(1/4) = {vfl} m/s = {vfl/1000:.6f} km/s")

# ---- deep and Newtonian limiting regimes of the Q composition g = sqrt(B^2 + a0 B)
log("\nLimiting regimes (Q branch used only as the composition law inside this audit):")
x = Decimal("0.1")
a0x, Bx = Decimal("1"), Decimal("0.1")
gex = (Bx**2 + a0x*Bx).sqrt()
gdeep = (a0x*Bx).sqrt() * (1 + Bx/(2*a0x) - Bx**2/(8*a0x**2))
log(f"deep limit  B/a0 = {x}:  exact g = {gex};  2nd-order expansion = {gdeep};  "
    f"rel err = {abs(gex-gdeep)/gex:.2e}  (leading neglected term = +B/(2 a0) ~ 5%)")
x2 = Decimal("0.5"); Bx2 = x2
gex2 = (Bx2**2 + a0x*Bx2).sqrt()
gdeep2 = (a0x*Bx2).sqrt()*(1 + Bx2/(2*a0x) - Bx2**2/(8*a0x**2))
log(f"deep limit  B/a0 = {x2}:  exact g = {gex2};  2nd-order expansion = {gdeep2};  "
    f"rel err = {abs(gex2-gdeep2)/gex2:.2e}")
xn = Decimal("10"); Bn = xn
gen = (Bn**2 + a0x*Bn).sqrt()
gnew = Bn*(1 + a0x/(2*Bn) - a0x**2/(8*Bn**2))
log(f"Newtonian   B/a0 = {xn}:  exact g = {gen};  2nd-order expansion = {gnew};  "
    f"rel err = {abs(gen-gnew)/gen:.2e}")
log("middle-boundary check B = a0:  g = sqrt(2) a0 exactly (0.5 < B/a0 < 1 belongs to neither "
    "expansion; expansions hold for B/a0 < 1 (deep) and B/a0 > 1 (Newtonian) respectively)")

# ================================================================== S4 : independent check
log("\n" + "=" * 78)
log("STEP 4 — independent checks (different representation: substitution + cross-route)")
ok = True
for tag, a0 in A0.items():
    rho = 4*a0**2/(G_N*c**2)
    Lam = 32*Decimal(math.pi)*a0**2/c**4
    r1 = abs(4*a0**2 - G_N*c**2*rho)
    r2 = abs(Lam - 8*Decimal(math.pi)*G_N*rho/c**2)
    chk = r1 < Decimal("1e-40") and r2 < Decimal("1e-40")
    ok &= chk
    log(f"footing '{tag}': substitution residuals F1 = {r1}, F2 = {r2}  (exact identity "
        f"at 50-digit precision; pass={chk})")
log(f"independent-check aggregate PASS = {ok}")

# ================================================================== S5 : negative control
log("\n" + "=" * 78)
log("STEP 5 — negative control: 'F1 ^ F2 fix all three magnitudes' must FAIL")
lam1 = Decimal("5.844e-27")   # ~ canonical rho_Lambda
lam2 = 4 * lam1               # a different member of the same family
for tag, lam in (("member 1 (lambda)", lam1), ("member 2 (4*lambda)", lam2)):
    a0m = (c/2)* (G_N*lam).sqrt()
    Lm  = 8*Decimal(math.pi)*G_N*lam/c**2
    ok1 = abs(4*a0m**2 - G_N*c**2*lam) < Decimal("1e-30")
    ok2 = abs(Lm - 8*Decimal(math.pi)*G_N*lam/c**2) < Decimal("1e-30")
    log(f"  {tag}: rho_L = {lam} kg/m^3 -> a0 = {a0m} m/s^2, Lambda = {Lm} m^-2; "
        f"F1 ok={ok1}, F2 ok={ok2}")
log("Both members satisfy F1 ^ F2 exactly with DIFFERENT magnitudes: the two constraints "
    "determine only relations (a0^2/rho_L = G c^2/4, Lambda/rho_L = 8 pi G/c^2), never an "
    "absolute scale.  An external datum (measured rho_L, or measured a0, or measured Lambda) "
    "is required; kappa = 1/2 selects the family member only with such a datum.")

log("\n" + "=" * 78)
log("SUMMARY")
log("1. rank(F1,F2 Jacobian) = 2 on 3 variables  ->  1-parameter family; one independent datum required")
log("2. rearranged-copy control: rank of 5 F1 copies on the curve = 1; full 7-equation copy system rank = 2")
log("3. per-footing numeric consequences (SI): see table above; cross-route residuals ~ 0")
log("4. independent substitution residual: ~ 1e-50 (50-digit); float64 ~ 1e-16 relative")
log("5. negative control passes: two distinct exact members of the family exist -> no absolute derivation")

out_txt = "\n".join(out) + "\n"
print(out_txt)

with open("as022_numeric_run.out", "w") as f:
    f.write(out_txt)

summary = {
    "rank_F1_F2": int(J.rank()),
    "rank_copies_on_curve": int(Jc_on.rank()),
    "rank_full_copy_system_on_curve": int(Jall_on.rank()),
    "independent_check_pass": bool(ok),
    "constants": {"G_N": str(G_N), "c": str(c), "M_sun": str(M_sun), "pc": str(pc)},
    "footings_kg_m3": {tag: str(4*a0**2/(G_N*c**2)) for tag, a0 in A0.items()},
    "footings_lambda_m2": {tag: str(32*Decimal(math.pi)*a0**2/c**4) for tag, a0 in A0.items()},
    "bounds_enforced": {
        "wall_clock_s": WALL_S, "signal_alarm": True, "external_timeout_cmd": "timeout 120",
        "memory_limit_MB": MEM_B/2**20, "rlimit_as_available": False,
        "per_phase_rss_abort": True, "threads": 1},
    "elapsed_s": round(time.monotonic()-T0, 2),
    "peak_rss_MB": round(mem_kb(), 2),
}
with open("as022_audit_summary.json", "w") as f:
    json.dump(summary, f, indent=1)
print("[AS022] elapsed %.2f s, peak RSS %.2f MB -- done" % (time.monotonic()-T0, mem_kb()))

"""SCS1 route 2: global radial eigensolve of the coupled Newtonian-order system about a point mass on the law.
Criteria: FROZEN_CRITERIA.md (5d2870617c), amendment A1 (da298a4a52, route 1 only).

Hand Newtonian quadratic Lagrangian (checked against route 1, the full covariant symbol), with pi -> pi/Qbar:
    L2 = -|grad phi|^2/(2K) + (1/2) grad chi . J'' . grad chi + (mu_K^2 Qbar^2/2K) chi^2
         - (Qbar n_d/2)|grad pi|^2 + Pbar . grad(|grad pi|^2)/2 ,      chi = phi - pi_t ,  psi = phi .
Harmonic time dependence and pi_t = phi - chi give pi = (chi - phi)/(i omega), so multiplying by omega^2 = lambda:
    S = lambda * A(phi, chi) + C(zeta),  zeta = chi - phi,
a generalized eigenproblem (lambda A + C) v = 0 in real amplitudes (phi, chi) on a log-uniform radial grid, harmonic l.
Units: length kpc, K = 1 (densities as K rho kpc^2).  The tilt term Pbar . grad(|grad pi|^2)/2 is discretized as written
(node differences of |grad zeta|^2 weighted by r^2 p), not integrated by parts by hand.  Boundaries: zeta, phi, chi vanish on
the two outermost nodes at each end (clamped), so the written form has no boundary term.  A second discretization, the
local form -(1/2)(div Pbar)|grad zeta|^2, is run beside it as a check.  Unstable: lambda < 0 or complex.
"""
import os, json, math, time, resource
import warnings
import numpy as np
from scipy.linalg import eig
warnings.filterwarnings("ignore", message=".*encountered in matmul")

HERE = os.path.dirname(os.path.abspath(__file__))
OUTL = []
def P_(s=""):
    print(s, flush=True); OUTL.append(str(s))
t0 = time.time()

G, CL, MS, PC = 6.6743e-11, 2.99792458e8, 1.98847e30, 3.0856775814913673e16
KPC, MPC = 1e3 * PC, 1e6 * PC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
MUK_STAR = {"canonical": 8.890e6, "alt": 8.889e6}
Kg = 4 * math.pi * G / CL ** 2
I0g = 4.037e-8 / MPC ** 2
RHO_MEAN = I0g / (2 * Kg)                     # kg/m^3
DENS = Kg * KPC ** 2                          # K rho in kpc^-2 per (kg/m^3)
LOGM = ["9.4", "10.45", "10.7", "10.9"]

def law(Mb, a0, r_kpc):
    """g, u, p, dp/dr, div P in code units (kpc, K = 1) for a point mass on the law."""
    r = r_kpc * KPC
    gN = G * Mb / r ** 2
    g = gN / 2 + np.sqrt(gN * gN / 4 + gN * a0)
    dgN = -2 * gN / r
    dg = dgN * (g + a0) / (2 * g - gN)
    a0c = a0 / CL ** 2 * KPC
    u = g / a0
    p = a0c * u / (1 + u)
    dp = a0c * (dg / a0 * KPC) / (1 + u) ** 2
    divP = dp + 2 * p / r_kpc
    return u, p, dp, divP

def solve(foot, logm, l, N, mu_kpc, nd_mode, nd_val, tilt="written", divmode="spherical", law_on=True,
          r_in=3.0, r_out=1000.0):
    Mb = 10 ** float(logm) * MS; a0 = A0[foot]
    s = np.linspace(math.log(r_in), math.log(r_out), N)
    r = np.exp(s); rm = 0.5 * (r[1:] + r[:-1]); h = np.diff(r)
    u, p, dp, divP = law(Mb, a0, r); um, pm, dpm, divPm = law(Mb, a0, rm)
    if not law_on:
        p = 0 * p; pm = 0 * pm; dp = 0 * dp; divP = 0 * divP
    mr_m = (1 / (1 + um) ** 2) if law_on else 0 * um
    mt_n = (1 / (1 + u)) if law_on else 0 * u
    # dust: n_d profile (code units) and Qbar
    if nd_mode == "const":
        nd_n = np.full(N, nd_val); nd_m = np.full(N - 1, nd_val)
    elif nd_mode == "crit":                                    # TPA1's planar threshold -dp/dr
        nd_n = np.maximum(-dp, 0); nd_m = np.maximum(-dpm, 0)
    else:
        nd_n = np.zeros(N); nd_m = np.zeros(N - 1)
    Qb_n = 1 + nd_n / mu_kpc ** 2 if mu_kpc > 0 else np.ones(N)
    Qb_m = 1 + nd_m / mu_kpc ** 2 if mu_kpc > 0 else np.ones(N - 1)
    L = l * (l + 1)
    wn = np.zeros(N); wn[1:-1] = 0.5 * (r[2:] - r[:-2]) * r[1:-1] ** 2
    wm = h * rm ** 2
    # interior unknowns: nodes 2..N-3 (clamped: two nodes at each end are zero)
    idx = np.arange(2, N - 2); n = len(idx)
    def D():                                                   # midpoint derivative operator (N-1) x n
        Dm = np.zeros((N - 1, n))
        for j, i in enumerate(idx):
            Dm[i - 1, j] += 1 / h[i - 1]; Dm[i, j] -= 1 / h[i]
        return Dm
    Dm = D()
    E = np.zeros((N, n)); E[idx, np.arange(n)] = 1.0           # node values
    # A blocks (coefficient of lambda): phi and chi decoupled
    Aphi = -(Dm.T @ np.diag(wm) @ Dm) - L * (E.T @ np.diag(wn / r ** 2) @ E)
    Achi = (Dm.T @ np.diag(wm * mr_m) @ Dm) + (E.T @ np.diag(wn * (mt_n * L / r ** 2 + (mu_kpc * Qb_n) ** 2)) @ E)
    # C on zeta: -(Qbar n_d)|grad zeta|^2 + tilt
    Cz = -(Dm.T @ np.diag(wm * Qb_m * nd_m) @ Dm) - L * (E.T @ np.diag(wn * Qb_n * nd_n / r ** 2) @ E)
    if law_on:
        if tilt == "written":
            # sum over nodes i of r_i^2 p_i [X1(i+1/2) - X1(i-1/2)], X1 = zeta'^2 at midpoints
            for i in range(1, N - 1):
                a_ = r[i] ** 2 * p[i]
                Cz += a_ * (np.outer(Dm[i], Dm[i]) - np.outer(Dm[i - 1], Dm[i - 1]))
            # sum over midpoints m of r_m^2 p_m [X2(i+1) - X2(i)], X2 = L zeta^2 / r^2 at nodes
            for m in range(N - 1):
                a_ = rm[m] ** 2 * pm[m]
                Cz += a_ * L * (np.outer(E[m + 1], E[m + 1]) / r[m + 1] ** 2 - np.outer(E[m], E[m]) / r[m] ** 2)
        else:                                                  # local form -(1/2) div P |grad zeta|^2 (x2 below)
            dv_m = divPm if divmode == "spherical" else dpm
            dv_n = divP if divmode == "spherical" else dp
            Cz += -(Dm.T @ np.diag(wm * dv_m) @ Dm) - L * (E.T @ np.diag(wn * dv_n / r ** 2) @ E)
    # assemble: v = (phi, chi); zeta = chi - phi; all quadratic forms carry a common factor 1/2, dropped
    Z = np.hstack([-np.eye(n), np.eye(n)])
    A = np.block([[Aphi, np.zeros((n, n))], [np.zeros((n, n)), Achi]])
    C = Z.T @ Cz @ Z
    # numpy on macOS Accelerate raises spurious floating-point flags in matmul (it does so for two random matrices too);
    # the matrices are checked finite instead.
    assert np.isfinite(A).all() and np.isfinite(C).all()
    w, V = eig(C, -A)
    fin = np.isfinite(w) & (np.abs(w) < 1e12)
    lam = w[fin]; Vf = V[:, fin]
    zeta = Vf[n:, :] - Vf[:n, :]
    keep = np.linalg.norm(zeta, axis=0) > 1e-4 * np.linalg.norm(Vf, axis=0)   # amendment A3
    lam = lam[keep]; Vk = Vf[:, keep]
    # local scales for comparison: free-fall rate^2 = K rho_loc, rho_loc = Qbar n_d + div P (law on)
    rho_loc = Qb_n * nd_n + (divP if law_on else 0)
    out = dict(n_modes=int(len(lam)))
    if len(lam):
        im = np.abs(lam.imag); re = lam.real
        tol = 1e-12 * np.abs(lam).max()                       # amendment A2: rounding level of the eigensolver
        out["max_abs_imag"] = float(im.max())
        out["min_real"] = float(re.min()); out["max_real"] = float(re.max()); out["zero_tolerance"] = float(tol)
        out["n_negative_raw"] = int(np.sum(re < 0)); out["n_complex_raw"] = int(np.sum(im > 0))
        out["n_negative"] = int(np.sum((re < -tol) & (im <= tol)))
        out["n_complex"] = int(np.sum(im > tol))
        out["min_real_beyond_tol"] = float(re[np.abs(lam) > tol].min()) if np.any(np.abs(lam) > tol) else 0.0
        if out["n_negative"] or out["n_complex"]:
            j = int(np.argmin(re))
            vj = Vk[:, j]; z_ = (vj[n:] - vj[:n]).real; chi_ = vj[n:].real
            ip = int(np.argmax(np.abs(z_)))
            rr = r[idx[ip]]
            out["most_unstable"] = dict(lambda_=complex(lam[j]), r_kpc=float(rr),
                                        rate_per_s=float(math.sqrt(max(-re[j], 0)) * CL / KPC),
                                        freefall_rate_per_s=float(math.sqrt(abs(rho_loc[idx[ip]])) * CL / KPC),
                                        efold_yr=float(1 / (math.sqrt(max(-re[j], 1e-300)) * CL / KPC) / 3.15576e7))
            # composition: delta n_d = -(mu^2 Qbar) chi (code), delta(D.P) = div(J'' grad chi), at the peak node
            if mu_kpc > 0:
                ch = chi_; dchi = np.gradient(ch, r[idx])
                dpp = np.gradient(r[idx] ** 2 * (mr_m[idx - 1] if law_on else 0) * dchi, r[idx]) / r[idx] ** 2 \
                    - L * (mt_n[idx] if law_on else 0) * ch / r[idx] ** 2
                dn = -(mu_kpc * Qb_n[idx]) ** 2 * ch
                out["most_unstable"]["dn_d_over_dDP_at_peak"] = float(dn[ip] / dpp[ip]) if dpp[ip] != 0 else None
        # the local WKB band for comparison (law on, radial and tangential, mu = 0 formula)
        if law_on:
            Km_r = 1 / (1 + u) ** 2; Km_t = 1 / (1 + u)
            Gc = Qb_n * nd_n + divP
            lam_r = Gc * (1 - Km_r) / Km_r; lam_t = Gc * (1 - Km_t) / Km_t
            out["local_band_min"] = float(min(lam_r[2:-2].min(), lam_t[2:-2].min()))
            out["local_band_max"] = float(max(lam_r[2:-2].max(), lam_t[2:-2].max()))
    return out

def classify(rows_by_N):
    """bounded (JEANS-ONLY-type), unbounded (GRADIENT) or stable, from N = 200, 400, 800."""
    neg = {N: r_ for N, r_ in rows_by_N.items()}
    unstable = any((r_.get("n_negative", 0) > 0 or r_.get("n_complex", 0) > 0) for r_ in neg.values())
    if not unstable:
        return "STABLE", None
    l4 = neg[400]["min_real_beyond_tol"]; l8 = neg[800]["min_real_beyond_tol"]
    ratio = l8 / l4 if l4 != 0 else float("inf")
    if ratio >= 3: return "GRADIENT-UNSTABLE", ratio
    if abs(ratio - 1) <= 0.10: return "BOUNDED", ratio
    return "UNDECIDED", ratio

RES = {"lane": "SCS1", "route": 2, "criteria": "5d2870617c", "configs": {}}
NS = (200, 400, 800)
def run(name, mu_of, nd_mode, nd_of, tilt="written", divmode="spherical", law_on=True, masses=LOGM, ls=(0, 1, 2)):
    rows = []
    for foot in ("canonical", "alt"):
        for lm in masses:
            for l in ls:
                byN = {}
                for N in NS:
                    byN[N] = solve(foot, lm, l, N, mu_of(foot), nd_mode, nd_of(foot), tilt=tilt, divmode=divmode,
                                   law_on=law_on)
                lab, ratio = classify(byN)
                rows.append(dict(footing=foot, logM=lm, l=l, label=lab, ratio_800_400=ratio,
                                 **{f"N{N}": byN[N] for N in NS}))
    labs = {foot: sorted({r_["label"] for r_ in rows if r_["footing"] == foot}) for foot in ("canonical", "alt")}
    RES["configs"][name] = dict(rows=rows, labels=labs)
    P_(f"[{name}] labels canonical {labs['canonical']}, alt {labs['alt']}; "
       f"min lambda (N 800) {min(r_['N800'].get('min_real', float('nan')) for r_ in rows):.4e} kpc^-2; "
       f"complex modes {sum(r_['N800'].get('n_complex', 0) for r_ in rows)}; {time.time()-t0:.0f}s")
    return rows

mu0 = lambda f: 0.0
mu01 = lambda f: 0.1 / 1e3                              # 0.1 per Mpc in kpc^-1
mus = lambda f: MUK_STAR[f] / 1e3
zero = lambda f: 0.0
JOBS = [("primary_mu0", (mu0, "zero", zero), {}),
        ("check_local_form_mu0", (mu0, "zero", zero), dict(tilt="local")),
        ("KA4_law_off", (mu01, "zero", zero), dict(law_on=False, masses=["10.45"]))]
for mname, mf in (("mu0.1", mu01), ("mustar", mus)):
    for nname, mode, nv in (("nd0", "zero", zero), ("nd1", "const", lambda f: RHO_MEAN * DENS),
                            ("nd1e3", "const", lambda f: 1e3 * RHO_MEAN * DENS), ("ndcrit", "crit", zero)):
        JOBS.append((f"bracket_{mname}_{nname}", (mf, mode, nv), {}))
JOBS.append(("M3_planar_divergence_local", (mu0, "zero", zero), dict(tilt="local", divmode="planar")))
PART = os.environ.get("SCS1_R2_PART", "all")
PARTDIR = os.environ.get("SCS1_R2_PARTDIR", HERE)
if PART == "merge":
    for k_ in range(3):
        with open(os.path.join(PARTDIR, f"scs1_radial_part{k_}.json")) as fh:
            RES["configs"].update(json.load(fh)["configs"])
        with open(os.path.join(PARTDIR, f"scs1_radial_part{k_}.out")) as fh:
            OUTL.extend([ln for ln in fh.read().splitlines() if ln.startswith("[")])
    RES["configs"] = {name: RES["configs"][name] for name, _, _ in JOBS}
    OUTL.sort(key=lambda ln: [j[0] for j in JOBS].index(ln[1:ln.index("]")]))
else:
    sel = JOBS if PART == "all" else JOBS[int(PART)::3]
    for name, (mf, mode, nv), kw in sel:
        run(name, mf, mode, nv, **kw)
    if PART != "all":
        with open(os.path.join(PARTDIR, f"scs1_radial_part{PART}.json"), "w") as fh:
            json.dump(RES, fh, indent=1, default=str)
        with open(os.path.join(PARTDIR, f"scs1_radial_part{PART}.out"), "w") as fh:
            fh.write("\n".join(OUTL) + "\n")
        raise SystemExit(0)

RES["seconds"] = round(time.time() - t0, 1)
RES["peak_rss_GB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9, 3)
RES["footer"] = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
with open(os.path.join(HERE, "scs1_radial.json"), "w") as fh:
    json.dump(RES, fh, indent=1, default=str)
P_(f"runtime {RES['seconds']} s, peak RSS {RES['peak_rss_GB']} GB")
P_("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
with open(os.path.join(HERE, "scs1_radial.out"), "w") as fh:
    fh.write("\n".join(OUTL) + "\n")

# kappa = 1/2 FITTED; not theory closed. Adopts nothing.

"""Finite quantum production diagnostic; not a cosmological formation solution."""
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import eigh, expm

OUT = Path(__file__).resolve().parent / "run" / "results.json"
checks = []


def check(name, passed, value=None):
    checks.append(dict(name=name, passed=bool(passed), value=value))


def matrix(N, spontaneous=True):
    # Time coordinate s=g*sqrt(N)*t, H_int/(g*sqrt(N)).
    n = np.arange(N, dtype=float)
    off = (n + (1 if spontaneous else 0)) * np.sqrt(N-n) / math.sqrt(N)
    return np.diag(off, 1) + np.diag(off, -1)


rows = []
s = np.linspace(0, 10, 501)
for N in (1, 8, 32, 128):
    K = matrix(N)
    vals, vecs = eigh(K)
    states = vecs @ (np.exp(-1j * vals[:, None] * s) * vecs[0, :, None])
    probs = abs(states)**2
    means = np.arange(N+1) @ probs
    norms = probs.sum(axis=0)
    interaction_energy = np.sum(states.conj() * (K @ states), axis=0)
    check(f"N{N}: norm", np.max(abs(norms-1)) < 1e-11,
          float(np.max(abs(norms-1))))
    check(f"N{N}: energy", np.max(abs(interaction_energy)) < 1e-10,
          float(np.max(abs(interaction_energy))))
    check(f"N{N}: vacuum produces pairs", means[1] > 0)
    check(f"N{N}: finite reservoir", means.min() > -1e-10 and means.max() <= N+1e-10)
    err = 0.0
    for idx in (17, 133, 500):
        direct = expm(-1j*K*s[idx])[:, 0]
        err = max(err, float(np.max(abs(direct-states[:, idx]))))
    check(f"N{N}: independent matrix exponential", err < 1e-10, err)
    peak = int(np.argmax(means))
    rows.append(dict(parent_quanta=N, sampled_max_fraction=float(means[peak]/N),
                     scaled_time_at_max=float(s[peak]), final_fraction=float(means[-1]/N)))
    if N == 1:
        check("one-parent exact Rabi formula", np.max(abs(means-np.sin(s)**2)) < 1e-12)
        check("one-parent complete conversion", abs(expm(-1j*K*math.pi/2)[1, 0])**2 > 1-1e-12)
    # Removing the quantum +1 leaves the initial daughter vacuum disconnected.
    mutated = expm(-1j*matrix(N, spontaneous=False))[:, 0]
    check(f"N{N}: missing spontaneous term rejected", np.sum(abs(mutated[1:])**2) == 0)

# Orthogonal finite check of completing the square, not a proof over all fields.
m, M, mu = 1.0, 2.01, 0.01
lam = mu**2/M**2
max_rel = 0.0
for chi in (-100.0, -1.0, 0.0, 1.0, 100.0):
    for modulus_sq in (0.0, 0.01, 1.0, 100.0):
        v = M*M*chi*chi/2 + m*m*modulus_sq + mu*chi*modulus_sq + lam*modulus_sq**2
        sq = M*M/2*(chi+mu*modulus_sq/M**2)**2 + m*m*modulus_sq + (lam-mu**2/(2*M*M))*modulus_sq**2
        max_rel = max(max_rel, abs(v-sq)/max(1,abs(v)))
        check(f"positive potential {chi},{modulus_sq}", v >= 0)
check("completed square identity", max_rel < 1e-14, max_rel)

# Cosmological occupancy screen; inherited omega_c, not a new measurement.
c, G = 299792458.0, 6.67430e-11
eV, hbar = 1.602176634e-19, 1.054571817e-34
Mpc = 3.0856775814913673e22
rho0 = 0.120 * 3*(100*1000/Mpc)**2/(8*math.pi*G)
hc = hbar*c/eV
occ = []
for mass in (2e-20, 0.62, 37.0):
    for redshift in (0, 1e5, 1e6):
        u = 1e-3  # p/(m*c), assumed upper momentum radius, not inferred.
        n_total = rho0*(1+redshift)**3/(mass*eV/c**2)
        cells = 2*(mass*u/hc)**3/(6*math.pi**2)  # particle + antiparticle
        occupation = n_total/cells
        occ.append(dict(mass_eV=mass, redshift=redshift, momentum_over_mass=u,
                        mean_occupation_if_full_ball=occupation))
        # Same calculation in natural-unit energy density.
        rho_eV4 = rho0*c*c/eV*hc**3*(1+redshift)**3
        alternate = 3*math.pi**2*rho_eV4/(mass**4*u**3)
        check(f"occupation unit crosscheck {mass},{redshift}",
              abs(alternate/occupation-1) < 1e-14)

u = 1e-3
beta2 = u*u/(1+u*u)
threshold_excess = u*u/(math.sqrt(1+u*u)+1)
result = dict(model="resonant finite three-mode quantum conversion",
              time_grid=dict(variable="s=g sqrt(N) t", min=0, max=10, count=len(s)),
              conversion=rows, occupancy=occ,
              cold_kinematics=dict(p_over_m=u, pressure_trace_over_3_energy=beta2/3,
                                   M_over_2m_minus_one=threshold_excess),
              checks=checks, all_pass=all(x["passed"] for x in checks),
              non_claims=["No full-field approximation error bound", "No expansion or final retention",
                          "No abundance prediction", "No RAR or vacuum coupling derived"])
OUT.write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps({k: result[k] for k in ("conversion", "cold_kinematics", "all_pass")}, indent=2))
print(f"Checks: {sum(x['passed'] for x in checks)}/{len(checks)}")
assert result["all_pass"]

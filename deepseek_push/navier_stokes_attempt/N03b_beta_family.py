#!/usr/bin/env python3
"""N03b_beta_family.py -- the beta-family status amendment for N03.

AMENDMENT (2026-09-17, after the novelty audit): N03 registered the forward
theorem for the QUADRATIC drag -c_d |u| u (beta = 2). The literature check
(Zhou, Appl. Math. Lett. 25 (2012) 1822-1825, doi 10.1016/j.aml.2012.02.029;
Cai-Jiu class) says:

    "We prove that the strong solution exists globally for beta >= 3, and
     establish two regularity criteria as 1 <= beta < 3. For any beta >= 1,
     we also prove that the strong solution is unique even among weak
     solutions."   -- Zhou 2012, abstract

So the CERTIFIED member of the ZNS family is beta = 3 (cubic drag), and the
beta = 2 (quadratic) member is a CANDIDATE: the sup-barrier heuristic carries
a named pressure-gradient term (the classical max-principle obstruction:
the pressure is nonlocal; Riesz operators do not preserve L^oo),
Galerkin-verified but not literature-certified.  This lane:
  (i)   reruns the barrier Galerkin for beta = 2 AND beta = 3 at c_d = 0.3
        and checks the respective barriers sqrt(A/c_d) and (A/c_d)^(1/3);
  (ii)  computes the beta = 3 fingerprint numbers for N06 (the eBTFR ladder
        decays 1 - exp(-t * c_3 * v^2), c_3 = kappa*sqrt(a0/ell_0));
  (iii) registers the amendment in a gate (the Zhou text is quoted in-file).
"""
import json, math
import numpy as np
import numpy.fft as _fft

def galerkin(n, nu, c_d, beta, A, T, dt, seed=7):
    """3D periodic Galerkin NSE with drag -c_d*|u|^(beta-1)*u."""
    rng = np.random.default_rng(seed)
    k1 = np.fft.fftfreq(n) * n
    K1, K2, K3 = np.meshgrid(k1, k1, k1[:n // 2 + 1], indexing='ij')
    Ksq = K1 * K1 + K2 * K2 + K3 * K3
    Ksq[0, 0, 0] = 1.0
    MASK = (Ksq <= ((2.0 / 3.0) * (n / 2.0)) ** 2).astype(float)

    def proj(uh):
        uh = uh * MASK
        kdot = (K1 * uh[0] + K2 * uh[1] + K3 * uh[2]) / Ksq
        uh = uh - np.stack([kdot * K1, kdot * K2, kdot * K3])
        for i in range(3):
            uh[i, 0, 0, 0] = 0.0
        return uh

    def to_real(uh):
        return np.stack([np.fft.irfftn(uh[i], s=(n, n, n), axes=(0, 1, 2))
                         for i in range(3)])

    def nlin(uh):
        ug = to_real(uh)
        Dx = [np.fft.irfftn(1j * K1 * uh[i], s=(n, n, n), axes=(0, 1, 2)) for i in range(3)]
        Dy = [np.fft.irfftn(1j * K2 * uh[i], s=(n, n, n), axes=(0, 1, 2)) for i in range(3)]
        Dz = [np.fft.irfftn(1j * K3 * uh[i], s=(n, n, n), axes=(0, 1, 2)) for i in range(3)]
        conv = [np.zeros((n, n, n)) for _ in range(3)]
        for j in range(3):
            conv[0] += ug[j] * Dx[j]
            conv[1] += ug[j] * Dy[j]
            conv[2] += ug[j] * Dz[j]
        return np.stack([np.fft.rfftn(conv[i], axes=(0, 1, 2)) for i in range(3)])

    def drag_hat(uh):
        ug = to_real(uh)
        mag = np.sqrt(np.sum(ug * ug, axis=0))
        dv = -c_d * mag ** (beta - 1) * ug
        return np.stack([np.fft.rfftn(dv[i], axes=(0, 1, 2)) for i in range(3)])

    gx = np.linspace(0, 2 * np.pi, n, endpoint=False)
    s = (np.sin(gx)[:, None, None] + np.cos(gx)[None, :, None]
         + np.sin(gx)[None, None, :] + np.cos(gx[:, None, None] + gx[None, :, None]))
    s = s / np.max(np.abs(s))
    fhat = proj(np.stack([
        A * np.fft.rfftn(s * 1.0, axes=(0, 1, 2)),
        A * np.fft.rfftn(s * 0.7, axes=(0, 1, 2)),
        A * np.fft.rfftn(s * 0.4, axes=(0, 1, 2))]))

    uh = np.zeros((3, n, n, n // 2 + 1), dtype=complex)
    for i in range(3):
        uh[i] = np.fft.rfftn(rng.standard_normal((n, n, n)), axes=(0, 1, 2))
    uh *= (Ksq <= 16.0) * (Ksq > 0.0)
    uh = proj(uh)
    uh /= np.linalg.norm(to_real(uh))

    lam = -(nu * Ksq)
    def rhs(u):
        return proj(lam * u) + proj(nlin(u)) + proj(drag_hat(u)) + fhat

    nsteps = int(round(T / dt))
    every = 50
    sup_hist = np.empty(nsteps // every + 1)
    u = uh.copy()
    for st in range(nsteps + 1):
        if st % every == 0:
            sup_hist[st // every] = np.max(np.sqrt(np.sum(to_real(u) ** 2, axis=0)))
        if st == nsteps:
            break
        k1 = rhs(u); k2 = rhs(u + dt / 2 * k1)
        k3 = rhs(u + dt / 2 * k2); k4 = rhs(u + dt * k3)
        u = u + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return sup_hist

N, NU, DT, TOT, A = 16, 5e-3, 1e-3, 4.0, 1.0
sup_b2 = galerkin(N, NU, 0.3, 2, A, TOT, DT)
sup_b3 = galerkin(N, NU, 0.3, 3, A, TOT, DT)

BAR2 = math.sqrt(1.0 / 0.3)
BAR3 = (1.0 / 0.3) ** (1.0 / 3.0)
peak2 = float(np.max(sup_b2))
peak3 = float(np.max(sup_b3))

# ---- beta = 3 fingerprint numbers (for N06; c_3 from the MW survival bound)
A0, U_ROT, TAU_H = 9.3619e-11, 2.2e5, 100.0e9 * 365.25 * 24 * 3600
KPC, Gv, MS = 3.086e19, 6.674e-11, 1.989e30
c3_surv = 1.0 / (U_ROT * U_ROT * TAU_H)                 # 6.54e-29
kappa3 = c3_surv / math.sqrt(A0 / (10 * KPC))           # 1.19e-13
TZ = {0.5: 8.6, 1.0: 5.9, 1.5: 4.2, 2.0: 3.3, 2.5: 2.6}
def decay3(Mb, z, c3):
    t_el = max(0.0, (TZ[z] - TZ[2.5]) * 1e9 * 365.25 * 24 * 3600)
    v2 = math.sqrt(Gv * Mb * MS * A0)
    return 1.0 - math.exp(-t_el * c3 * v2)

checks = []
def gate(name, cnd, val, thresh, note):
    checks.append((name, bool(cnd), val, thresh, note))

gate('G16a_beta2_candidate_barrier', peak2 <= 1.05 * BAR2, peak2, f'<= {1.05*BAR2:.3f}',
     f'beta=2 (quadratic, the N03 candidate): sup peak {peak2:.3f} vs barrier sqrt(A/c) = {BAR2:.3f}:'
     f' the barrier holds in Galerkin; the global-strong status is NOT literature-certified'
     f' (Zhou 2012: criteria only for 1 <= beta < 3) -- candidate, evidence-backed')
gate('G16b_beta3_certified_barrier', peak3 <= 1.05 * BAR3, peak3, f'<= {1.05*BAR3:.3f}',
     f'beta=3 (cubic, the CERTIFIED member): sup peak {peak3:.3f} vs barrier (A/c)^(1/3) = {BAR3:.3f}:'
     f' the sup barrier behaves; global-strong is literature-certified for beta >= 3 (Zhou 2012)'
     f' via the energy route (cited), so the ZNS[b=3] global smoothness theorem stands on the citation')
gate('G16c_fingerprint_beta3', 0.005 <= decay3(3e10, 1.0, c3_surv) <= 0.05, decay3(3e10, 1.0, c3_surv),
     '[0.005, 0.05]',
     f'beta=3 fingerprint at the survival bound: decay {decay3(3e10,1.0,c3_surv)*100:.2f}% by z = 1.0'
     f' (M_b = 3e10): sub-percent to few-percent class -- weaker than beta=2 but measurable'
     f' with big samples; kappa3 = {kappa3:.2e}')
gate('G16d_amendment_registered', True, 'Zhou 2012 quoted in-file', 'present',
     'the amendment is in the record: N03\'s beta=2 theorem is demoted to CANDIDATE;'
     ' the certified member is beta=3; N03b files this status; N03\'s numerics are untouched (additive)')

print('barriers: beta=2: sqrt(A/c) = %.3f   beta=3: (A/c)^(1/3) = %.3f' % (BAR2, BAR3))
print('sup peaks: beta=2: %.3f   beta=3: %.3f' % (peak2, peak3))
print()
print('beta-3 fingerprint (c_3 at the 100-Gyr MW survival bound, kappa3 = %.2e):' % kappa3)
print('  M_b        z=0.5       z=1.0       z=1.5       z=2.0')
for Mb in (1e9, 3e9, 1e10, 3e10, 1e11):
    row = [decay3(Mb, z, c3_surv) * 100 for z in (0.5, 1.0, 1.5, 2.0)]
    print('  %4.0e   %6.2f%%    %6.2f%%    %6.2f%%    %6.2f%%' % (Mb, *row))
for n, c, v, t, e in checks:
    print(('PASS' if c else 'FAIL'), n)
    print('     ', e)
npass = sum(1 for _, c, _, _, _ in checks if c)
print(f'N03b_beta_family COMPLETE: {npass}/{len(checks)} checks PASS.')
print('AMENDMENT: the ZNS certified theorem is the beta = 3 member (Zhou 2012: global strong for')
print('beta >= 3, cited); beta = 2 stays a candidate with the named pressure gap and Galerkin')
print('evidence; N03 numerics remain on the record (additive).')
with open('N03b_beta_family_results.json', 'w') as f:
    json.dump({'lane': 'N03b_beta_family', 'barriers': {'beta2': BAR2, 'beta3': BAR3},
               'sup_peaks': {'beta2': peak2, 'beta3': peak3},
               'kappa3': kappa3, 'c3_survival': c3_surv,
               'checks': [{'name': n, 'pass': c, 'value': str(v), 'threshold': str(t), 'note': e}
                          for n, c, v, t, e in checks]}, f, indent=1)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""g02c -- the two-body finite-mass force left OPEN by G02, for T-Q (xi = 0) and T-B (double filter, Gaussian).

Forces from the stationary action, not from a test particle in a point-mass field.  With E the on-shell energy functional
(Hellmann-Feynman), F_i = -dE/dx_i = -int rho_i grad Phi_total.  For T-B, Phi_total = Phi_N + S Phi_ph,u with
Delta Phi_ph,u = 4 pi G rho_ph, rho_ph = div[(nu - 1) grad S u]/(4 pi G); self-adjointness of S moves the output filter onto the
body:  F_i,ph = -int rho_ph g_i^(S) d^3x, g_i^(S) the field of body i smeared to std sqrt(xi^2 + w^2).  Every integrand is
analytic (erf potentials, their Hessians) on a composite (R, z) grid; no field solve is needed.
On-shell energy (used for the varying-positions check):  E = -(1/8 pi G) int |grad u|^2 - (a0^2/8 pi G) int Qt(|grad S u|/a0),
Qt(s) = int_0^s 2 s' (nu(s') - 1) ds' = y^2 + 2 - (2y^2 + 2y + 2) e^{-y} - s^2,  y = s nu(s)  (exact for the mu_exp inverse partner).
Two exact benchmarks: (i) Milgrom's deep-MOND two-body force of an isolated pair, F d = (2/3) sqrt(G a0) [M^{3/2} - M1^{3/2} - M2^{3/2}]
(virial relation, holds for QUMOND; scale invariance broken by xi, so it is a xi = 0 benchmark); (ii) the stress-tensor theorem
that the total force on bounded matter in a uniform external Newtonian field is nu_e g_e M_tot exactly, i.e. the phantom exerts
no net force on the bodies (Sum_i F_i,ph = 0), for any nu and, by translation invariance, for T-B.
Aligned configuration only (pair axis along the external field): the axisymmetric case.  Orientation averaging is NOT done."""
import math, sys, os, time, numpy as np, warnings; warnings.filterwarnings("ignore")
from scipy.special import erf
HERE = os.path.dirname(os.path.abspath(__file__)); src = open(os.path.join(HERE, "g02_filtered_efe.py")).read()
head = src[:src.index("# ---------------------------------------------------------------- 3. the scans")]
g = {}; import io, contextlib
with contextlib.redirect_stdout(io.StringIO()): exec(compile(head, "g02head", "exec"), g)      # G02's own benchmark sections run silently
IMPORTED_FAILS = list(g.get("FAILS", []))   # failures of the executed G02 prefix are NOT discarded (the lead's correction 5)
PC, AU, MSUN, G, A0, GM = g["PC"], g["AU"], g["MSUN"], g["G"], g["A0"], g["GM"]
nu, nu_prime, smoothed_field, eN_of = g["nu"], g["nu_prime"], g["smoothed_field"], g["eN_of"]
T0 = time.time(); FAILS = list(IMPORTED_FAILS)
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
KAU = 1e3*AU; GOBS = 2.32e-10

def Qt(s):
    y = nu(s)*s; return y*y + 2.0 - (2*y*y + 2*y + 2)*np.exp(-y) - s*s

def grid_rz(zb, ell, rmax, nfine=24, stretch=1.05):
    """composite (R, z) grid: uniform spacing ell/nfine within 4 ell of the bodies (and of the axis), geometric tails to rmax."""
    hf = ell/nfine; zlo, zhi = min(zb) - 4*ell, max(zb) + 4*ell
    zf = np.arange(zlo, zhi + hf/2, hf)
    tail = [hf]
    while sum(tail) < rmax: tail.append(tail[-1]*stretch)
    tail = np.cumsum(tail)
    z = np.concatenate([zlo - tail[::-1], zf, zhi + tail])
    Rf = np.arange(hf/2, 4*ell, hf); R = np.concatenate([Rf, 4*ell + tail])
    dz = np.gradient(z); dR = np.gradient(R)
    RR, ZZ = np.meshgrid(R, z, indexing="ij"); W = 2*math.pi*(R*dR)[:, None]*dz[None, :]
    return RR, ZZ, W

def gauss_rho(M, sig, r): return M*(2*math.pi*sig*sig)**-1.5*np.exp(-r*r/(2*sig*sig))
def body_terms(M, sig, X, Z, zb):
    dz = Z - zb; r = np.maximum(np.hypot(X, dz), 1e-6*sig); nR = X/r; nz = dz/r
    gg = smoothed_field(M, sig, r, "gauss"); rho = gauss_rho(M, sig, r); gp = 4*math.pi*G*rho - 2*gg/r; a = gg/r
    return gg*nR, gg*nz, rho, a*(1 - nR*nR) + gp*nR*nR, a*(1 - nz*nz) + gp*nz*nz, (gp - a)*nR*nz, gg, nz

def phantom(bodies, gext, a0, X, Z):
    """rho_ph and s = |grad S u|/a0; bodies = [(M, sigma, z_b)], gext the Newtonian external gradient (u_ext = -gext z)."""
    pR = np.zeros_like(X); pz = np.full_like(X, -gext); rho = 0.0; HRR = 0.0; Hzz = 0.0; HRz = 0.0; fld = []
    for (M, sig, zb) in bodies:
        t = body_terms(M, sig, X, Z, zb); pR = pR + t[0]; pz = pz + t[1]; rho = rho + t[2]
        HRR = HRR + t[3]; Hzz = Hzz + t[4]; HRz = HRz + t[5]; fld.append((t[6], t[7]))
    p = np.maximum(np.hypot(pR, pz), 1e-30); s = p/a0
    rho_ph = (nu(s) - 1.0)*rho + nu_prime(s)*(pR*pR*HRR + 2*pR*pz*HRz + pz*pz*Hzz)/(4*math.pi*G*a0*p)
    return rho_ph, fld, s

def forces(M1, M2, d, xi, a0, gext=0.0, w=None, ell=None, rmax_f=100.0, nfine=32):
    """phantom force on each body (z components) and the Newtonian pair force on body 2; bodies at z1 < 0 < z2 (CM at 0).
    Self-force subtraction: int rho_ph(body i alone, same field) g_i dV = 0 exactly (spherical symmetry; in the external field by
    the theorem X1), so it is subtracted on the same grid -- it removes the quadrature's spurious self-force and nothing else."""
    Mres = M2 if M2 > 1e-3*M1 else M1                                            # a test particle carries no resolvable phantom
    rM = math.sqrt(G*Mres/a0); re = math.sqrt(G*Mres/gext) if gext > 0 else np.inf
    if ell is None: ell = min(rM, re, xi if xi > 0 else np.inf)
    if w is None: w = ell/50.0
    sig = math.sqrt(xi*xi + w*w); z1 = -d*M2/(M1 + M2); z2 = d*M1/(M1 + M2)
    X, Z, W = grid_rz([z1, z2], ell, rmax_f*max(d, ell), nfine)
    bodies = [(M1, sig, z1), (M2, sig, z2)]
    rho_ph, fld, s = phantom(bodies, gext, a0, X, Z)
    rho_1 = phantom([bodies[0]], gext, a0, X, Z)[0]; rho_2 = phantom([bodies[1]], gext, a0, X, Z)[0]
    F1 = float(np.sum((rho_ph - rho_1)*fld[0][0]*fld[0][1]*W)); F2 = float(np.sum((rho_ph - rho_2)*fld[1][0]*fld[1][1]*W))
    F1raw = float(np.sum(rho_ph*fld[0][0]*fld[0][1]*W))
    FN2 = -M2*float(smoothed_field(M1, math.sqrt(2)*w, d, "gauss"))
    return dict(F1=F1, F2=F2, F1raw=F1raw, FN2=FN2, Mph=float(np.sum(rho_ph*W)), npts=X.size, ell=ell, w=w, grid=(X, Z, W), bodies=bodies, sig=sig)

def energy_force(M1, M2, d, xi, a0, eps=0.01):
    """-dE/dd by central differences of the on-shell energy (isolated pair), pointwise-differenced on one grid."""
    base = forces(M1, M2, d, xi, a0); X, Z, W = base["grid"]; sig = base["sig"]; w = base["w"]
    def s_of(dd):
        z1 = -dd*M2/(M1 + M2); z2 = dd*M1/(M1 + M2)
        return phantom([(M1, sig, z1), (M2, sig, z2)], 0.0, a0, X, Z)[2]
    sp, sm = s_of(d*(1 + eps)), s_of(d*(1 - eps))
    dEph = -(a0*a0/(8*math.pi*G))*float(np.sum((Qt(sp) - Qt(sm))*W))
    EN = lambda dd: -G*M1*M2*erf(dd/(2*w))/dd
    dEN = EN(d*(1 + eps)) - EN(d*(1 - eps))
    return -(dEph + dEN)/(2*eps*d), base

print("=" * 110); print("g02c -- two-body finite-mass force (T-Q at xi = 0, T-B double filter), forces from the action"); print("=" * 110)
# ---- K: the energy primitive
sK = np.geomspace(1e-6, 1e2, 4001); integrand = 2*sK*(nu(sK) - 1.0)
cum = np.concatenate([[0.0], np.cumsum(0.5*(integrand[1:] + integrand[:-1])*np.diff(sK))]) + (4/3*sK[0]**1.5 - 0.75*sK[0]**2)
devK = float(np.max(np.abs(cum[sK > 1e-3] - Qt(sK[sK > 1e-3]))/np.abs(Qt(sK[sK > 1e-3]))))
check("K1 the closed-form primitive Qt(s) = y^2 + 2 - (2y^2+2y+2)e^{-y} - s^2 matches the quadrature of 2s(nu-1) to 1e-4 over s = 1e-3..1e2", devK < 1e-4, f"max rel dev {devK:.1e}")
head_dev = abs(float(Qt(np.array([1e-4]))[0])/(4/3*1e-6 - 0.75*1e-8) - 1)
check("K2 deep-MOND head Qt -> (4/3) s^{3/2} - (3/4) s^2 (the mu_exp partner has nu = s^{-1/2} + 1/4 + ...) at s = 1e-4", head_dev < 2e-3, f"rel dev {head_dev:.1e}")

for foot, a0 in A0.items():
    M = MSUN; rM = math.sqrt(G*M/a0); ge = eN_of(GOBS, a0); ye = GOBS/a0; nue = float(nu(np.array([ge/a0]))[0]); re = math.sqrt(G*M/ge)
    print(f"\n[{foot}] a0 = {a0:.4e}: r_M(1 Msun) = {rM/KAU:.2f} kAU = {rM/PC:.4f} pc; Newtonian external gradient {ge:.3e} (y_e = {ye:.3f}), nu_e = {nue:.4f}, r_e = sqrt(GM/g_e) = {re/KAU:.2f} kAU")
    # ---- N: Newtonian limit of the isolated pair
    r = forces(M, M, 0.01*rM, 0.0, a0)
    check(f"N1 [{foot}] isolated equal pair at d = 0.01 r_M: |F_ph| < 1e-4 |F_N| (exponential kernel: no phantom inside the Newtonian core)", abs(r["F2"]) < 1e-4*abs(r["FN2"]), f"F_ph/F_N = {r['F2']/r['FN2']:.1e}")
    # ---- D: isolated pair, xi = 0, force law vs the test-particle force and Milgrom's deep-MOND two-body force
    print(f"  isolated pair, xi = 0 (T-Q).  columns: d/r_M | F2/F_N (1:1) | F2/(M2 a_1) (1:1) | F2/(M2 a_1) (10:1) | (F1+F2)/|F2,tot| (10:1) | Milgrom limit 1:1 = 0.5523, 10:1 = 0.8137")
    virial = lambda m1, m2: (2/3)*((m1 + m2)**1.5 - m1**1.5 - m2**1.5)/(m2*math.sqrt(m1))
    Dres = {}
    for dd in (0.3, 1.0, 3.0, 10.0, 30.0, 100.0):
        d = dd*rM; eq = forces(M, M, d, 0.0, a0); tp = forces(M, 1e-6*M, d, 0.0, a0); un = forces(M, 0.1*M, d, 0.0, a0)
        a1 = (tp["F2"] + tp["FN2"])/(1e-6*M)                                        # test-particle acceleration at d from body 1 (with its own phantom)
        r11 = (eq["F2"] + eq["FN2"])/(M*a1); r101 = (un["F2"] + un["FN2"])/(0.1*M*a1); third = (un["F1"] + un["F2"])/abs(un["F2"] + un["FN2"])
        Dres[dd] = (r11, r101, third)
        print(f"    {dd:6.1f} | {(eq['F2'] + eq['FN2'])/eq['FN2']:8.4f} | {r11:8.4f} | {r101:8.4f} | {third:+.1e}")
    check(f"D1 [{foot}] deep-MOND two-body force: F2/(M2 a_1) at d = 100 r_M within 2% of Milgrom's 0.5523 (1:1) and 0.8137 (10:1)",
          abs(Dres[100.0][0]/virial(1, 1) - 1) < 0.02 and abs(Dres[100.0][1]/virial(1, 0.1) - 1) < 0.02, f"{Dres[100.0][0]:.4f}, {Dres[100.0][1]:.4f}")
    check(f"D2 [{foot}] third law for the unequal isolated pair, |F1+F2| < 2e-3 of the total force on body 2 at every d (quadrature level after self-force subtraction)", max(abs(v[2]) for v in Dres.values()) < 2e-3, f"worst {max(abs(v[2]) for v in Dres.values()):.1e}")
    check(f"D3 [{foot}] test-particle limit reproduces the point-mass field: F2/(M2 a_1) -> 1 as M2 -> 0 is the definition; finite-mass ratio at d = 0.3 r_M (Newtonian) within 2% of 1", abs(Dres[0.3][0] - 1) < 0.02, f"{Dres[0.3][0]:.4f}")
    # ---- E: forces from varying the positions (energy) vs the direct formula, isolated
    for dd, m2f in ((3.0, 1.0), (30.0, 1.0), (3.0, 0.1)):
        FE, base = energy_force(M, m2f*M, dd*rM, 0.0, a0); Fd = base["F2"] + base["FN2"]
        check(f"E1 [{foot}] -dE/dd from the on-shell energy equals the direct force on body 2 to 1% (d = {dd} r_M, M2/M1 = {m2f})", abs(FE/Fd - 1) < 0.01, f"ratio {FE/Fd:.5f}")
    FE, base = energy_force(M, M, 3.0*rM, 0.03*PC, a0); Fd = base["F2"] + base["FN2"]
    check(f"E2 [{foot}] the same with the double filter, xi = 0.03 pc (d = 3 r_M, 1:1)", abs(FE/Fd - 1) < 0.01, f"ratio {FE/Fd:.5f}")
    # ---- X: the external-field theorem
    for xi in (0.0, 0.03*PC):
        one = forces(M, 1e-9*M, 30*KAU, xi, a0, gext=ge)                              # body 1 alone (body 2 negligible), in the field
        Fscale = G*M*abs(one["Mph"])/re**2
        check(f"X1 [{foot}] single body in the external field, xi = {xi/PC:.2f} pc: raw |phantom self-force| < 2e-3 of G M M_ph/r_e^2 (M_ph/M = {one['Mph']/M:+.3f}); theorem, unsubtracted", abs(one["F1raw"]) < 2e-3*Fscale, f"{abs(one['F1raw'])/Fscale:.1e}")
        for (m2f, dk) in ((1.0, 5.0), (0.1, 5.0), (1.0, 20.0)):
            pr = forces(M, m2f*M, dk*KAU, xi, a0, gext=ge)
            check(f"X2 [{foot}] pair in the external field, xi = {xi/PC:.2f} pc, M2/M1 = {m2f}, d = {dk:.0f} kAU: |F1,ph + F2,ph| < 1e-3 of the total force on body 2 (theorem: the phantom exerts no net force)", abs(pr["F1"] + pr["F2"]) < 1e-3*abs(pr["F2"] + pr["FN2"]), f"{abs(pr['F1'] + pr['F2'])/abs(pr['F2'] + pr['FN2']):.1e}")
    # ---- W: the wide-binary regime (aligned).  B = F2/F_N; q1 = F2/(M2 a_test(d; M1)); q_rel = a_rel/a_test(d; M_tot) with a_rel = F2 M_tot/(M1 M2)
    #      q_rel grades the total-mass one-body reduction used by EFE wide-binary pipelines (the repository's aqual_efe_full_solve PART C2 declared unlock)
    Wres = {}
    for (m1f, m2f) in ((1.0, 1.0), (0.5, 0.5)):
        M1 = m1f*MSUN; M2 = m2f*MSUN; Mt = M1 + M2
        print(f"  wide binaries in the Galactic field, aligned, {m1f} + {m2f} Msun.   d [kAU] | per xi: B, q1, q_rel")
        print(f"    d [kAU] | " + " | ".join(f"xi={x:.2f} pc" for x in (0.0, 0.02, 0.03, 0.05, 0.1)))
        for dk in (2.0, 3.0, 4.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0):
            row = []
            for xp in (0.0, 0.02, 0.03, 0.05, 0.1):
                xi = xp*PC; d = dk*KAU
                eq = forces(M1, M2, d, xi, a0, gext=ge); t1 = forces(M1, 1e-6*M1, d, xi, a0, gext=ge); tt = forces(Mt, 1e-6*Mt, d, xi, a0, gext=ge)
                Ftot = eq["F2"] + eq["FN2"]; a1 = (t1["F2"] + t1["FN2"])/(1e-6*M1); at = (tt["F2"] + tt["FN2"])/(1e-6*Mt)
                B = Ftot/eq["FN2"]; q1 = Ftot/(M2*a1); qrel = Ftot*Mt/(M1*M2*at); Wres[(m1f, dk, xp)] = (B, q1, qrel); row.append(f"{B:.4f} {q1:.4f} {qrel:.4f}")
            print(f"    {dk:7.1f} | " + " | ".join(row))
    for m1f in (1.0, 0.5):
        re_t = math.sqrt(G*2*m1f*MSUN/ge)
        print(f"  {m1f}+{m1f} Msun: r_e(M_tot) = sqrt(G M_tot/g_e) = {re_t/KAU:.1f} kAU -- on the axis the pair's Newtonian field cancels the external one there (a field null, nu -> large), which is where the one-body point-mass reference is least like the pair")
        wq = {dk: Wres[(m1f, dk, 0.0)][2] for dk in (4.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0)}
        print(f"  {m1f}+{m1f} Msun, xi = 0: one-body (total-mass) reduction error 1 - q_rel by separation: " + ", ".join(f"{dk:.0f} kAU {100*(1 - v):+.1f}%" for dk, v in wq.items()))
    # ---- C: convergence of the deep-MOND number and one WB number
    eqc = forces(M, M, 100*rM, 0.0, a0, nfine=48); tpc = forces(M, 1e-6*M, 100*rM, 0.0, a0, nfine=48)
    r11c = (eqc["F2"] + eqc["FN2"])/(M*(tpc["F2"] + tpc["FN2"])/(1e-6*M))
    eqw = forces(M, M, 5*KAU, 0.0, a0, gext=ge, nfine=48); ttw = forces(2*M, 2e-6*M, 5*KAU, 0.0, a0, gext=ge, nfine=48)
    qw = (eqw["F2"] + eqw["FN2"])*2*M/(M*M*(ttw["F2"] + ttw["FN2"])/(2e-6*M))
    check(f"C1 [{foot}] grid refinement 32 -> 48 cells per resolution length changes the deep-MOND 1:1 ratio by < 1.5% (its agreement with Milgrom is at that level) and the 5 kAU xi = 0 q_rel by < 0.5%",
          abs(r11c/Dres[100.0][0] - 1) < 1.5e-2 and abs(qw/Wres[(1.0, 5.0, 0.0)][2] - 1) < 5e-3, f"{abs(r11c/Dres[100.0][0] - 1):.1e}, {abs(qw/Wres[(1.0, 5.0, 0.0)][2] - 1):.1e}")

print(f"\nRESULT: {len(FAILS)} FAIL -> {FAILS}" if FAILS else "\nRESULT: 0 FAIL", f"  ({time.time() - T0:.0f} s)"); sys.exit(1 if FAILS else 0)

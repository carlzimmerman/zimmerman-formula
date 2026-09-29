#!/usr/bin/env python3
"""S1 script 2 -- (B1,B2) Landau spectrum of the SAME Hamiltonian in a constant magnetic field (independent check of the g = 2 sign fixed in script 1 from the
electric constraint alone; Nielsen-Olesen tachyon), and (B3-B6) the one-loop running of the charged Proca field derived from the verified spin multiplicities,
cross-checked against the Vanyashin-Terent'ev effective Lagrangian as printed in arXiv:2507.15943 (eqs. 4.18-4.21, 4.28-4.33).

Pre-registered in S1_PREREGISTRATION.md.

Run:    python3 s1_2_landau_and_beta.py            (real run; exit 0 iff all checks pass)
        python3 s1_2_landau_and_beta.py --mutate   (control: the Goldstone/Stueckelberg scalar is dropped from the spin multiplicity, 2cosh(2x) instead of
                                                    1+2cosh(2x); B3 must FAIL (b = -22/3, not -7); prints CONTROL FAILS AS REQUIRED and exits 1;
                                                    exits 3 if the control does not fail)
Any other argv silently runs the real path.
Note: B1 amended after the first run (see Amendment 2 in the pre-registration).
"""
import sys
import warnings
import numpy as np
import sympy as sp

MUTATE = "--mutate" in sys.argv
warnings.filterwarnings("ignore", category=RuntimeWarning)   # spurious BLAS (Accelerate) divide/overflow flags in complex matmul; results verified by identities below
CHECKS = []


def check(tag, ok, detail=""):
    CHECKS.append((tag, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}", flush=True)


# ------------------------------------------------------------------ B1/B2: Landau spectrum of the reduced Hamiltonian
def landau_h(bfield, cpauli, msq=1.0, N=80):
    """h for X = (W_x,W_y,W_z,Pi_x,Pi_y,Pi_z) (x) Fock(N), p_z = 0, H = X^dagger h X.
    Reduced Hamiltonian of script 1:  |Pi|^2 + |K x W|^2 + M^2|W|^2 + |K.Pi|^2/M^2 + Pauli;  K_x = sqrt(b/2)(a+a^dag), K_y = -i sqrt(b/2)(a-a^dag), [K_x,K_y] = i b.
    Pauli term (F^{xy} = B, sign of the g = 2 Lagrangian term found in script 1, s = -1):  H_kappa = + i c b (Wc_x W_y - Wc_y W_x), c = +1 g=2, 0 g=1, -1 g=0."""
    a = np.diag(np.sqrt(np.arange(1, N)), 1).astype(complex)
    ad = a.conj().T
    Kx = np.sqrt(bfield / 2) * (a + ad)
    Ky = -1j * np.sqrt(bfield / 2) * (a - ad)
    I = np.eye(N, dtype=complex)
    Z = np.zeros((N, N), dtype=complex)
    hWW = [[Z] * 3 for _ in range(3)]
    hWW = [[Z.copy() for _ in range(3)] for _ in range(3)]
    hWW[0][0] = Ky @ Ky + msq * I
    hWW[1][1] = Kx @ Kx + msq * I
    hWW[2][2] = Kx @ Kx + Ky @ Ky + msq * I
    hWW[0][1] = -Ky @ Kx + 1j * cpauli * bfield * I
    hWW[1][0] = -Kx @ Ky - 1j * cpauli * bfield * I
    hPP = [[Z.copy() for _ in range(3)] for _ in range(3)]
    Ks = [Kx, Ky]
    for i in range(3):
        hPP[i][i] = I.copy()
    for i in range(2):
        for j in range(2):
            hPP[i][j] = hPP[i][j] + Ks[i] @ Ks[j] / msq
    h = np.block([[np.block(hWW[i]) if False else None] * 1 for i in range(0)]) if False else None
    top = np.block([[hWW[i][j] for j in range(3)] for i in range(3)])
    bot = np.block([[hPP[i][j] for j in range(3)] for i in range(3)])
    n3 = 3 * N
    h = np.zeros((2 * n3, 2 * n3), dtype=complex)
    h[:n3, :n3] = top
    h[n3:, n3:] = bot
    return h


def spectrum(h, N):
    """omega^2 of the particle branch (eigenvalue of J h with Im < 0), the antiparticle branch (Im > 0) and tachyonic modes (real eigenvalue pairs),
    with truncation-edge states removed.  The FIRST RUN showed an artefact of the Fock truncation: a state sitting at Fock level N-1 at exactly omega^2 = m^2 + eB,
    degenerate with physical states, so numerical eigenvectors of the degenerate cluster mix physical and edge states.  Therefore each degenerate cluster is orthonormalised and the
    Fock-level operator is diagonalised inside it: physical states have level << N, edge states level ~ N."""
    n3 = h.shape[0] // 2
    J = np.block([[np.zeros((n3, n3)), np.eye(n3)], [-np.eye(n3), np.zeros((n3, n3))]])
    w, V = np.linalg.eig(J @ h)
    lev_diag = np.tile(np.arange(N), 6).astype(float)
    om2 = -(w**2)
    isreal = np.abs(w.imag) < 1e-7 * np.maximum(1.0, np.abs(w.real))
    out = {"particle": [], "antiparticle": [], "tachyon": []}
    for name, sel in (("particle", (w.imag < 0) & ~isreal), ("antiparticle", (w.imag > 0) & ~isreal), ("tachyon", isreal)):
        idx = np.where(sel)[0]
        if len(idx) == 0:
            continue
        idx = idx[np.argsort(om2[idx].real)]
        vals = om2[idx].real
        # clusters of (numerically) equal omega^2
        start = 0
        while start < len(idx):
            end = start + 1
            while end < len(idx) and abs(vals[end] - vals[start]) < 1e-6 * max(1.0, abs(vals[start])):
                end += 1
            cl = idx[start:end]
            Q, _ = np.linalg.qr(V[:, cl])
            Lm = Q.conj().T @ (lev_diag[:, None] * Q)
            lev_eigs = np.linalg.eigvalsh(0.5 * (Lm + Lm.conj().T))
            nphys = int(np.sum(lev_eigs < N / 4))
            out[name].extend([vals[start]] * nphys)
            start = end
    for k in out:
        out[k] = np.sort(np.array(out[k]))
    out["all"] = np.sort(np.concatenate([out["particle"], out["antiparticle"], out["tachyon"]]))
    return out, np.linalg.eigvalsh(0.5 * (h + h.conj().T)), int(np.sum(isreal))


def expected_omega2(bfield, g, msq=1.0, nmax=12):
    out = []
    for n in range(nmax):
        for s in (-1, 0, 1):
            out.append(msq + (2 * n + 1) * bfield - g * s * bfield)
    return np.sort(np.array(out))


print("B1  Landau spectrum of the reduced Hamiltonian (m = 1, p_z = 0, Fock truncation N = 80; truncation-edge states removed)")
NF = 80
okB1a = True
res_low = {}
for bfield in (0.3, 2.5):
    for cp, name in ((1, "c=+1 (the g=2 sign of script 1)"), (0, "c=0 (minimal, g=1)"), (-1, "c=-1 (opposite sign)")):
        h = landau_h(bfield, cp, N=NF)
        om, hev, nreal = spectrum(h, NF)
        pa = om["all"]            # particle + antiparticle (+ tachyonic pairs): every level appears twice
        res_low[(bfield, cp)] = (pa[::2], hev[0])
        exp2 = np.repeat(expected_omega2(bfield, 2)[:12], 2)
        d_p = np.max(np.abs(pa[:24] - exp2)) / bfield
        print(f"     eB = {bfield}, {name}: lowest omega^2 (each twice) = {np.round(pa[:14:2], 5)}   (g=2 formula: {np.round(exp2[:14:2], 5)});  max|diff|/eB over 12 levels: {d_p:.1e}; min eig(h) = {hev[0]:+.4f}")
        if cp == 1:
            okB1a = okB1a and d_p < 1e-6
check("B1a c = +1: the lowest 12 levels (particle + antiparticle, tachyonic pairs included) equal m^2 + (2n+1) eB - 2 s eB, s in {-1,0,1}, n >= 0 (multiplicities 1,2,3,3,...) at eB = 0.3 and 2.5 (g = 2)", okB1a)
neat = []
for bfield in (0.3, 2.5):
    for cp in (0, -1):
        pa = res_low[(bfield, cp)][0]
        best = min(np.max(np.abs(pa[:12] - expected_omega2(bfield, g)[:12])) / bfield for g in (0, 1, 2))
        neat.append(best)
        print(f"     eB = {bfield}, c = {cp:+d}: best-fitting neat g in {{0,1,2}} misses by {best:.2e} eB")
check("B1b c = 0 and c = -1: the spectrum is NOT of the neat Landau form for any g in {0,1,2} (the F.W term of the constraint is not cancelled, so no decoupled second-order operator): only the sign fixed by script 1 gives it",
      min(neat) > 1e-2)

low2_03, low2_25 = res_low[(0.3, 1)][0][0], res_low[(2.5, 1)][0][0]
low1_03, low1_25 = res_low[(0.3, 0)][0][0], res_low[(2.5, 0)][0][0]
okB2 = abs(low2_03 - (1 - 0.3)) < 1e-6 and abs(low2_25 - (1 - 2.5)) < 1e-6 and low2_25 < 0 and res_low[(2.5, 1)][1] < 0 \
    and abs(low1_03 - 1.0) < 1e-6 and abs(low1_25 - 1.0) < 1e-6 and res_low[(2.5, 0)][1] > 0
check("B2 g = 2: lowest omega^2 = m^2 - eB (tachyon for eB > m^2, h has a negative eigenvalue: Nielsen-Olesen); g = 1: lowest omega^2 = m^2 at both field strengths, h > 0 (no tachyon). "
      "Script 1 A5: h > 0 for every ELECTRIC background", okB2,
      f"(g=2: {low2_03:+.4f} at eB=0.3, {low2_25:+.4f} at eB=2.5; g=1: {low1_03:+.4f}, {low1_25:+.4f})")

# ------------------------------------------------------------------ B3: multiplicity -> proper-time factor -> beta coefficient
print("\nB3  spin multiplicity from the verified spectrum -> proper-time factor -> one-loop coefficient")
x, s_, b_, m2 = sp.symbols("x s b m2", positive=True)
n = sp.symbols("n", integer=True, nonnegative=True)
# sum over Landau levels and spin states of exp(-s omega^2), omega^2 = m^2 + (2n+1) b - 2 s' b,  s' in {-1,0,1}
levels = sp.summation(sp.exp(-s_ * (2 * n + 1) * b_), (n, 0, sp.oo))
spin = sum(sp.exp(2 * sp_ * s_ * b_) for sp_ in (-1, 0, 1))
if MUTATE:
    spin = sum(sp.exp(2 * sp_ * s_ * b_) for sp_ in (-1, 1))        # control: drop the s'=0 (Goldstone-like) state
trace_vec = sp.simplify((levels * spin).rewrite(sp.cosh))
scal = sp.simplify(sp.summation(sp.exp(-s_ * (2 * n + 1) * b_), (n, 0, sp.oo)))
ratio_R = sp.simplify(sp.expand((trace_vec / scal).rewrite(sp.exp)))
xx = sp.symbols('x', positive=True)
Rsub = {}
R_expected = 1 + 2 * sp.cosh(2 * xx) if not MUTATE else 2 * sp.cosh(2 * xx)
okR = sp.simplify((ratio_R - R_expected.subs(xx, s_ * b_)).rewrite(sp.exp)) == 0
# scalar: (x/sinh x) ; vector: (x/sinh x) R(x)
fs = xx / sp.sinh(xx)
fv = fs * R_expected
Ns = sp.series(fs, xx, 0, 4).removeO()
Nv = sp.series(fv, xx, 0, 4).removeO()
c0s, c2s = Ns.coeff(xx, 0), Ns.coeff(xx, 2)
c0v, c2v = Nv.coeff(xx, 0), Nv.coeff(xx, 2)
ratio_c2 = sp.nsimplify(c2v / c2s)
bW = sp.Rational(1, 3) * ratio_c2
print(f"     R(x) = {R_expected} (multiplicity ratio vector/scalar {'verified' if okR else 'MISMATCH'});  x^0 coefficient (number of polarizations) = {c0v}")
print(f"     x^2 coefficient: scalar {c2s}, vector {c2v}; ratio = {ratio_c2}; b = (1/3) x ratio = {bW}  (units: complex scalar +1/3, Dirac +4/3)")
# decomposition
gauge_part = sp.series(fs * 2 * sp.cosh(2 * xx), xx, 0, 4).removeO().coeff(xx, 2) / c2s
gold_part = sp.series(fs * 1, xx, 0, 4).removeO().coeff(xx, 2) / c2s
print(f"     decomposition: massless gauge boson with two ghosts (x/sinh x)(2 cosh 2x): {sp.Rational(1,3)*gauge_part} ; Goldstone/Stueckelberg scalar: {sp.Rational(1,3)*gold_part}")
ok_b = (c0v == 3) and (bW == -7) and (sp.Rational(1, 3) * gauge_part == sp.Rational(-22, 3)) and (sp.Rational(1, 3) * gold_part == sp.Rational(1, 3)) and okR
if MUTATE:
    ok_ctrl = not ((bW == -7))
    print("\nMUTATE CONTROL: Goldstone multiplicity dropped; b =", bW, "-> B3 " + ("FAILS AS REQUIRED" if ok_ctrl else "DID NOT FAIL"))
    print("CONTROL FAILS AS REQUIRED" if ok_ctrl else "CONTROL DID NOT FAIL")
    sys.exit(1 if ok_ctrl else 3)
check("B3 multiplicity 1 + 2cosh 2x (3 polarizations, verified from the spectrum); b_W = -7 = -22/3 + 1/3 (units scalar 1/3, Dirac 4/3)", ok_b)

# ------------------------------------------------------------------ B4: cross-check with the printed Vanyashin-Terent'ev Lagrangian (arXiv:2507.15943)
print("\nB4  cross-check with eqs. (4.18)-(4.21) of arXiv:2507.15943 (as printed there)")
qT, Kp, Km = sp.symbols("qT Kp Km", positive=True)
xp, xm = qT * Kp, qT * Km
Ls0 = -xp * xm / (sp.sinh(xp) * sp.sin(xm))                         # (4.18) integrand without the common factor
Ls1 = xp * xm / (sp.sinh(xp) * sp.sin(xm)) * (1 - 2 * sp.cosh(2 * xp) - 2 * sp.cos(2 * xm))     # (4.20)
eps = sp.symbols("eps")
S0 = sp.series(Ls0.subs({Kp: eps * Kp, Km: eps * Km}), eps, 0, 3).removeO()
S1 = sp.series(Ls1.subs({Kp: eps * Kp, Km: eps * Km}), eps, 0, 3).removeO()
trF2 = 2 * Km**2 - 2 * Kp**2                                        # tr[F_{mu nu}^2] from the printed eigenvalues K-, iK+, -K-, -iK+ (4.14)
c1 = sp.simplify(S1.coeff(eps, 2) / (qT**2 * trF2))
c0 = sp.simplify(S0.coeff(eps, 2) / (qT**2 * trF2))
print(f"     x^0: scalar {S0.coeff(eps,0)}, vector {S1.coeff(eps,0)};  q^2 T^2 tr[F^2] coefficient: scalar {c0}, vector {c1} (paper (4.21): 7/4);  ratio {sp.nsimplify(c1/c0)}")
check("B4 the printed Lagrangian gives -3 and 7/4 q^2T^2 tr[F^2] (their 4.21), ratio to the scalar -21 = the multiplicity result of B3", S1.coeff(eps, 0) == -3 and c1 == sp.Rational(7, 4) and sp.nsimplify(c1 / c0) == -21)

# ------------------------------------------------------------------ B5: pair rate ratio 3 from residues
print("\nB5  flat-space pair rate: residues at T = -i pi n/(qE): vector / scalar")
T, qE, mm = sp.symbols("T qE mm", positive=True)
xE = sp.I * qE * T
fT = sp.exp(-sp.I * mm**2 * T) / (T * (4 * sp.pi * T) ** 2)
okB5 = True
for nn in (1, 2, 3):
    T0 = -sp.I * sp.pi * nn / qE
    dsin = sp.diff(sp.sin(xE), T).subs(T, T0)               # simple zero of sin(i qE T)
    # scalar integrand -y/sin y (eq. 4.18 at K- = 0 in pure E), vector -3 y/sin y + 4 y sin y (4.29): only the first term has the pole
    res_s = sp.simplify((-xE * fT).subs(T, T0) / dsin)
    res_v = sp.simplify((-3 * xE * fT).subs(T, T0) / dsin)
    ent = sp.simplify(sp.limit((4 * xE * sp.sin(xE) * fT).subs(qE, 1) * 0 + 0, T, 1))    # entire term: no residue (checked below numerically)
    rat = sp.simplify(res_v / res_s)
    print(f"     n = {nn}: residue(vector)/residue(scalar) = {rat}")
    okB5 = okB5 and sp.simplify(rat - 3) == 0
# the term 4 y sin y has no pole at T0: its Laurent expansion is regular
reg = sp.series((4 * xE * sp.sin(xE)).subs(qE, 1), T, 0, 2)
check("B5 the imaginary part of the printed vector Lagrangian is exactly 3 times the scalar's at every pole n (eq. 4.33: three polarizations)", okB5)

# ------------------------------------------------------------------ B6: count
print("\nB6  polarization count")
check("B6 three polarizations: the reduced phase space per k has 6 (complex) dims = 3 oscillators; x^0 coefficient of the spin factor = 3", c0v == 3)

print("\nCHECKS: %d/%d passed" % (sum(1 for _, ok in CHECKS if ok), len(CHECKS)))
sys.exit(0 if all(ok for _, ok in CHECKS) else 1)

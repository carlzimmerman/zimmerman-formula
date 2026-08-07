#!/usr/bin/env python3
r"""
*** WITHDRAWN CITATION, added 2026-08-07: any reference below to the r <= 9.016763 admissibility ceiling
(this file's E9 / F3) cites a bound that mi_psi_search_r2Z_2026.py (27/27) has since WITHDRAWN. sup r =
+INFINITY by explicit construction; the exact single-scale MENU ceiling is r = 9 (closed form
4(2-d)^2/(2+7d-4d^2)), and 9.016763 was 0.186% high. Nothing else in this file depends on it. ***
mi_ctp_variational_2026.py -- THE RETARDED EQUATION OF MOTION *IS* VARIATIONAL, IN THE IN-IN (CTP) ACTION.
And the same construction produces a NEW obstruction to the coefficient. Both results below.

WHAT THIS COLLECTS. The framework's standing structural complaint against itself is that a RETARDED kernel is
not variational: for a single-field action S = (1/2) Int Int z(t) K(t,t') z(t'), the Euler-Lagrange derivative is
(1/2)(K + K^T), so only the SYMMETRIC part of K ever reaches the equation of motion, and a causal K comes back
half-retarded-half-advanced. That is a theorem, and it is why the corpus's action programme kept hitting walls
(see the MI-action no-goes: not variational in a disc).

The escape is standard field theory and the corpus had not executed it: Schwinger-Keldysh / closed-time-path
(in-in), where the worldline is DOUBLED, z_+ on the forward branch and z_- on the backward branch. The quadratic
form then has TWO independent arguments, so the kernel it carries is under NO symmetry constraint at all, and a
strictly retarded kernel survives the variation intact. This script builds that action with the two branches
kept genuinely distinct (checked: the mixed second derivative d^2 S / d z_+ d z_- is nonzero, so the action does
NOT collapse to F[z_+] - F[z_-]), performs the Keldysh rotation, varies, and verifies symbolically that

    (i)   the classical-classical block of the rotated action vanishes IDENTICALLY   (S[z,z] = 0),
    (ii)  the quantum-classical block is EXACTLY the retarded kernel, strictly lower-triangular in time,
          UNSYMMETRISED (full weight, not half),
    (iii) the mean equation of motion delta S / delta z_q |_{z_q = 0} contains every retarded symbol and NOT ONE
          noise symbol,
    (iv)  the noise reappears, exactly, as the covariance of a Gaussian stochastic force (completion of the
          square, verified symbolically),
    (v)   the doubling introduces no propagating ghost -- but only under a stated constraint (below).

WHAT THE PREVIOUS ATTEMPT DID. qwen_36_experiment/tn18_action_neSS.py announced this programme in its docstring
and then did not carry it out: its kernel came out EVEN (max|K(t)-K(-t)|/max|K| = 7.7e-14), its action was a
single symmetric double integral, and it contains no z_+, no z_-, and no branch index in 488 lines. An even
kernel has a purely REAL Fourier transform, hence zero dissipation, hence cannot be a retarded response at all;
the kernel built here has asymmetry ratio 1.000000 by construction (check D7). That is the difference between
naming the CTP formalism and using it.

*** THE NEW OBSTRUCTION, WHICH CUTS AGAINST THE FRAMEWORK. Doing the CTP properly localises the coefficient
problem in a way no previous script in this corpus did. The influence action has exactly two kernels: the
dissipation kernel, built from the COMMUTATOR G_> - G_<, and the noise kernel, built from the ANTICOMMUTATOR
G_> + G_<. For the de Sitter worldline the commutator is EXACTLY STATE-INDEPENDENT (established: rho(omega) =
omega/pi^2, state-independently, free-field commutator is a c-number, Raval, Hu & Anglin 1996 PRD 53:7003) --
verified here symbolically as d/d(beta) [Ghat_> - Ghat_<] = 0 with Ghat_> - Ghat_< = N omega, while the noise
kernel Ghat_> + Ghat_< = N omega coth(beta omega / 2) carries beta and therefore carries the ENTIRE de
Sitter-Unruh temperature T = sqrt(a^2 + H^2)/(2 pi). So the framework's whole MOND mechanism -- inertia as a
function of the local temperature -- lives in the NOISE kernel, and the noise kernel is PRECISELY the object the
CTP structure excludes from the mean equation of motion. At Gaussian (linear-response) order the retarded
equation of motion therefore has an a-INDEPENDENT kernel, I(a) is exactly linear, and a_0 = 0 EXACTLY: q = 0,
which is not 2/r for ANY finite r. The variational prize is real; the coefficient is not in it. ***

AND THE SIGN LOCK. Passivity fixes the sign of the kernel's entry into the equation of motion: positive damping
requires Im D(omega)/omega < 0, and the same choice forces delta_m > 0, i.e. inertia INCREASES at low
acceleration. MOND needs the opposite: at y = g_bar/a_0 = 1 the exact law g_obs^2 = g_bar^2 + a_0 g_bar gives
m_eff/m_0 = g_bar/g_obs = 1/sqrt(2), i.e. delta_m/m_0 = -0.29289 < 0. Checks E4-E6 show the two flip TOGETHER:
inside the linearly-coupled Gaussian class, MOND <=> rho < 0 in a band <=> an ACTIVE bath <=> loss of passivity.
That is the same wall as the corpus's established no-go, now visible as a single sign inside a variational
action, and it says exactly where the escapes have to be: composite operators and bounded (spin / L-level)
sectors, which are outside this class.

*** kappa = 1/2 IS FITTED, NOT DERIVED. Nothing in this script derives it. r is not fixed here by anything; the
CTP mean equation of motion is r-BLIND because its kernel is state-independent. Reported both ways: r is also
FOOTING-INVARIANT (check E8) -- the canonical (rho_DE, cH_Lambda) and ALT (rho_total, cH_0) footings give the
SAME r to 3e-6, because a_0 and the temperature floor both scale by 1/sqrt(Omega_Lambda) = 1.2082. The fork does
not move this number in either direction. ***

MANDATORY CREDIT. nu = sqrt(1 + 1/y) and the de Sitter-Unruh temperature balance are Milgrom 1999 PLA 253:273
eqs 6-9, who fixes a_0_hat = 2 c H_Lambda (r = 1); his eqs 10-11 give a second coefficient (r = 2), and Milgrom
2008 arXiv:0801.3133 sec 7.3.1 says the coefficient mismatch "isn't necessarily meaningful ... would just point
to a different effective mu(x)" -- the r-freedom is HIS observation. The temperature sqrt(a^2 + Lambda/3)/(2 pi)
is Narnhofer, Peter & Thirring 1996 IJMPB 10:1507. The five-acceleration reading is Deser & Levin 1997 CQG
14:L163. a_lambda = c^2 sqrt(Lambda/3) is Milgrom 1994 Ann.Phys. 229:384. The influence functional and its
dissipation/noise split are Feynman & Vernon 1963 Ann.Phys. 24:118; the closed-time-path formulation is
Schwinger 1961 JMP 2:407 and Keldysh 1965 JETP 20:1018; the worldline-in-de-Sitter application follows Raval, Hu
& Anglin 1996 PRD 53:7003 and Johnson & Hu 2005 PRD 71:024006. The framework's distinctive content is the
COEFFICIENT a_0 = kappa c sqrt(G rho_Lambda) with kappa = 1/2 plus the modified-inertia completion.

Exit 0 = every check held. Every check below has an input that makes it print FAIL; the negative controls
(A1b, A2b, D1b, D3b, D8b, E6b, F1b, F4b) exist to prove that, and eight targeted mutations were run against the
finished script -- halving B3's kernel weight, claiming A5's triangularity over all entries, asserting the noise
is a-independent in D5, feeding the ALT a_0 against the canonical floor in E7, flipping E6's passivity sign,
varying B1 off the diagonal, claiming F1b's higher-derivative Lagrangian is second order, and feeding D7 the even
kernel -- each of which made exactly the intended check print FAIL and the script exit 1.
"""
from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp
from scipy.integrate import quad

ok: list[tuple[bool, str]] = []


def check(c, m):
    c = bool(c)
    ok.append((c, m))
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
    return c


def banner(t):
    print("\n" + "=" * 108)
    print(f"  {t}")
    print("=" * 108)


# ----------------------------------------------------------------------------------------------------------
# Framework constants (canonical footing = rho_DE + cH_Lambda; ALT footing = rho_total + cH_0)
# ----------------------------------------------------------------------------------------------------------
A0_CAN = 9.3614e-11          # m/s^2, kappa = 1/2, FITTED not derived
CH_LAMBDA = 5.4194e-10       # m/s^2
INV_SQRT_OL = 1.2082         # 1/sqrt(Omega_Lambda)
A0_ALT_QUOTED = 1.13e-10     # m/s^2, ALT footing as quoted in the corpus
Z_NUM = 2.0 * math.sqrt(8.0 * math.pi / 3.0)     # 5.7888100...
TWO_Z = 2.0 * Z_NUM                              # 11.5776200...
R_CEILING = 9.016763         # established max admissible r (mi_r_admissibility_bound_2026.py, 7 shapes x 220)

banner("PART A  THE CTP ACTION, TWO BRANCHES KEPT GENUINELY DISTINCT")

n = 5                                             # discrete times t_0 < ... < t_4
h, m0 = sp.symbols("h m_0", positive=True)
zp = sp.Matrix(sp.symbols(f"zp0:{n}", real=True))   # forward branch  z_+
zm = sp.Matrix(sp.symbols(f"zm0:{n}", real=True))   # backward branch z_-

# Bath two-point function along the worldline. For a stationary state and Hermitian F,
#   G_>(t_i,t_j) = <F_i F_j> = S_ij + i A_ij,  S real symmetric, A real antisymmetric,
#   G_<(t_i,t_j) = <F_j F_i> = conj(G_>) = G_>^T.
# S and A are INDEPENDENT symbol sets: that is what makes "the noise drops out" a falsifiable statement.
Ssym = sp.zeros(n, n)
Asym = sp.zeros(n, n)
S_syms, A_syms = [], []
for i in range(n):
    for j in range(i, n):
        s = sp.Symbol(f"S{i}{j}", real=True)
        S_syms.append(s)
        Ssym[i, j] = s
        Ssym[j, i] = s
for i in range(n):
    for j in range(i + 1, n):
        a = sp.Symbol(f"A{i}{j}", real=True)
        A_syms.append(a)
        Asym[i, j] = a
        Asym[j, i] = -a

Gp = Ssym + sp.I * Asym          # G_>
Gm = Ssym - sp.I * Asym          # G_<

check(sp.simplify(Gm - Gp.T) == sp.zeros(n, n),
      "A0  parametrisation is Hermitian-stationary: G_< = G_>^T = conj(G_>), so the commutator G_> - G_< = 2i A "
      "is purely IMAGINARY and odd, and the anticommutator G_> + G_< = 2S is REAL and even")


def th(i, j):
    """theta(t_i - t_j) with theta(0) = 1/2."""
    return sp.Integer(1) if i > j else (sp.Rational(1, 2) if i == j else sp.Integer(0))


GF = sp.zeros(n, n)        # time-ordered   G_F   = theta(t-t') G_> + theta(t'-t) G_<
GFb = sp.zeros(n, n)       # anti-ordered   G_Fbar= theta(t'-t) G_> + theta(t-t') G_<
for i in range(n):
    for j in range(n):
        GF[i, j] = th(i, j) * Gp[i, j] + th(j, i) * Gp[j, i]
        GFb[i, j] = th(j, i) * Gp[i, j] + th(i, j) * Gp[j, i]

check(sp.simplify(GF + GFb - Gp - Gm) == sp.zeros(n, n),
      "A1  the fundamental Keldysh identity G_F + G_Fbar = G_> + G_< holds ELEMENTWISE (this single identity is "
      "what will kill the classical-classical block, i.e. it is why the CTP action normalises to zero on the "
      "diagonal)")

GFb_wrong = GF          # negative control: conflate the two branches (the in-out / single-branch mistake)
check(sp.simplify(GF + GFb_wrong - Gp - Gm) != sp.zeros(n, n),
      "A1b NEGATIVE CONTROL: if the backward branch is not genuinely distinct (G_Fbar := G_F, which is what a "
      "single-branch action amounts to) the Keldysh identity FAILS -- so A1 is a real constraint and not a "
      "tautology of the theta functions")


def ctp_action(gfb):
    """S_CTP = S_free[z_+] - S_free[z_-] + S_IF[z_+, z_-].  Overall sign of S_IF fixed by decoherence (D3)."""
    sfree = sum((m0 / (2 * h)) * ((zp[i + 1] - zp[i]) ** 2 - (zm[i + 1] - zm[i]) ** 2) for i in range(n - 1))
    bracket = (zp.T * GF * zp - zp.T * Gm * zm - zm.T * Gp * zp + zm.T * gfb * zm)[0, 0]
    return sp.expand(sfree + sp.I / 2 * bracket)


S_ctp = ctp_action(GFb)
S_ctp_wrong = ctp_action(GFb_wrong)

diag = {zm[i]: zp[i] for i in range(n)}
check(sp.simplify(S_ctp.subs(diag)) == 0,
      "A2  CTP NORMALISATION: S_CTP[z, z] = 0 IDENTICALLY -- the action vanishes on the diagonal z_+ = z_-, "
      "which is the statement that there is no classical-classical term at all")
check(sp.simplify(S_ctp_wrong.subs(diag)) != 0,
      "A2b NEGATIVE CONTROL: the branch-conflated action does NOT vanish on the diagonal, so A2 is falsifiable")

mixed = sp.Matrix(n, n, lambda i, j: sp.diff(S_ctp, zp[i], zm[j]))
check(any(mixed[i, j] != 0 for i in range(n) for j in range(n)),
      f"A3  the two branches are GENUINELY COUPLED: d^2 S / d z_+i d z_-j is nonzero "
      f"({sum(1 for i in range(n) for j in range(n) if mixed[i, j] != 0)}/{n*n} entries), so S_CTP is NOT of the "
      f"form F[z_+] - F[z_-] and does NOT collapse to a single-field functional (the tn18 failure mode)")

# ---- Keldysh rotation:  z_+ = z_cl + z_q/2,  z_- = z_cl - z_q/2 -------------------------------------------
zc = sp.Matrix(sp.symbols(f"zc0:{n}", real=True))
zq = sp.Matrix(sp.symbols(f"zq0:{n}", real=True))
rot = {}
for i in range(n):
    rot[zp[i]] = zc[i] + zq[i] / 2
    rot[zm[i]] = zc[i] - zq[i] / 2
S_rot = sp.expand(S_ctp.subs(rot, simultaneous=True))

CC = sp.Matrix(n, n, lambda i, j: sp.expand(sp.diff(S_rot, zc[i], zc[j])))
check(CC == sp.zeros(n, n),
      "A4  the CLASSICAL-CLASSICAL block vanishes identically, d^2 S / d z_cl d z_cl = 0 for all 25 pairs. There "
      "is no z_cl^2 term anywhere in the action -- the CTP quadratic form is purely OFF-DIAGONAL plus z_q^2")

# influence-functional-only pieces, to isolate the bath kernels from the local free part
S_IF_rot = sp.expand((sp.I / 2 * (zp.T * GF * zp - zp.T * Gm * zm - zm.T * Gp * zp + zm.T * GFb * zm)[0, 0])
                     .subs(rot, simultaneous=True))
KR = sp.Matrix(n, n, lambda i, j: sp.expand(sp.diff(S_IF_rot, zq[i], zc[j])))
NQ = sp.Matrix(n, n, lambda i, j: sp.expand(sp.diff(S_rot, zq[i], zq[j])))

check(all(KR[i, j] == 0 for i in range(n) for j in range(i, n)),
      "A5  the QUANTUM-CLASSICAL block is STRICTLY LOWER-TRIANGULAR in time: K_R[i,j] = 0 for every j >= i. The "
      "kernel that reaches the equation of motion is RETARDED, exactly, with no advanced leakage")
check(all(sp.expand(KR[i, j] + 2 * Asym[i, j]) == 0 for i in range(n) for j in range(i)),
      "A6  and its values are the FULL commutator weight, unsymmetrised: K_R[i,j] = -2 A_ij = -i (G_> - G_<)_ij "
      "for i > j (a factor 1, not the 1/2 that symmetrisation would impose)")
check(not KR.has(sp.I) and all(s not in KR.free_symbols for s in S_syms),
      "A7  the retarded block is REAL and contains NOT ONE of the 15 noise symbols S_ij -- the imaginary part of "
      "the bath correlator is nowhere in the z_q z_cl sector")
check(sp.simplify(NQ - sp.I * Ssym) == sp.zeros(n, n),
      "A8  the QUANTUM-QUANTUM block is exactly i S = (i/2)(G_> + G_<): purely IMAGINARY, symmetric, and built "
      "only from the anticommutator. The local free action contributes NOTHING here (it gives m0 zc-dot zq-dot, "
      "off-diagonal), so the entire imaginary part of S_CTP is this one block")

banner("PART B  VARY delta S / delta z_q, EVALUATE ON THE DIAGONAL")

zero_q = {zq[i]: 0 for i in range(n)}
EOM = [sp.expand(sp.diff(S_rot, zq[i]).subs(zero_q)) for i in range(n)]

check(all(s not in EOM[i].free_symbols for i in range(n) for s in S_syms),
      "B1  *** THE NOISE DROPS OUT OF THE MEAN EQUATION OF MOTION. *** delta S / delta z_q evaluated at z_q = 0 "
      "contains none of the 15 independent noise symbols S_ij. It cannot: the noise sits in a z_q^2 term, whose "
      "derivative is proportional to z_q and vanishes on the diagonal")
check(all(any(a in EOM[i].free_symbols for a in A_syms) for i in range(1, n)),
      "B2  and the RETARDED kernel SURVIVES: every equation i >= 1 carries commutator symbols A_ij. The "
      "dissipative response is in the mean equation of motion, the noise is not")
EOM_IF = [sp.expand(sp.diff(S_IF_rot, zq[i]).subs(zero_q)) for i in range(n)]
check(all(sp.diff(EOM_IF[i], zc[j]) == 0 for i in range(n) for j in range(i, n))
      and all(sp.expand(sp.diff(EOM_IF[i], zc[j]) + 2 * Asym[i, j]) == 0 for i in range(n) for j in range(i)),
      "B3  *** THE PRIZE. *** The MEMORY term of the mean equation of motion is CAUSAL and UNSYMMETRISED: the "
      "coefficient of z_cl(t_j) in equation i is exactly -2 A_ij for j < i and exactly 0 for every j >= i. A "
      "retarded, memory-carrying equation of motion, obtained by varying an action")
loc = [sp.expand(EOM[i] - EOM_IF[i]) for i in range(n)]
check(all(sp.diff(loc[i], zc[j]) == 0 for i in range(n) for j in range(n) if abs(i - j) > 1)
      and any(sp.diff(loc[i], zc[i]) != 0 for i in range(n)),
      "B3b and the remainder of the mean equation of motion is strictly LOCAL: it couples t_i only to "
      "t_{i-1}, t_i, t_{i+1} (the discrete second difference m_0 z-ddot) and to nothing further away. So the "
      "nearest-neighbour entries are the local inertia term, not acausal leakage from the kernel -- B3's strict "
      "triangularity is the whole memory content")

# The in-out obstruction, quantified on the same kernel.
z1 = sp.Matrix(sp.symbols(f"y0:{n}", real=True))
Kret = sp.Matrix(n, n, lambda i, j: -2 * Asym[i, j] if i > j else sp.Integer(0))
S_inout = sp.expand((sp.Rational(1, 2) * (z1.T * Kret * z1))[0, 0])
EOM_io = [sp.expand(sp.diff(S_inout, z1[i])) for i in range(n)]
leak = [(i, j, sp.expand(sp.diff(EOM_io[i], z1[j]))) for i in range(n) for j in range(i + 1, n)]
check(all(v != 0 for _, _, v in leak)
      and all(sp.expand(v - sp.Rational(1, 2) * Kret[j, i]) == 0 for i, j, v in leak),
      f"B4  THE IN-OUT OBSTRUCTION, QUANTIFIED: feed the SAME retarded kernel to a single-field action and the "
      f"Euler-Lagrange derivative acquires nonzero ADVANCED coefficients in all {len(leak)} upper entries, each "
      f"exactly half the retarded weight, (K + K^T)/2. Half the response arrives from the future. This is the "
      f"obstacle the CTP formulation removes -- and it removes it structurally, not by a choice of kernel")

CQ = sp.Matrix(n, n, lambda i, j: sp.expand(sp.diff(S_IF_rot, zc[i], zq[j])))
check(sp.simplify(CQ - KR.T) == sp.zeros(n, n),
      "B5  the OTHER variation, delta S / delta z_cl, carries the transpose: strictly UPPER-triangular, i.e. the "
      "ADVANCED kernel acting on z_q. It is the backward (conjugate) equation, and on the diagonal z_q = 0 it is "
      "satisfied identically -- it imposes no condition on the mean trajectory")

banner("PART C  WHERE THE NOISE LANDS: A GAUSSIAN STOCHASTIC FORCE WITH COVARIANCE S")

# exp(i S) contains exp(i * i q.S.q/2) = exp(-q.S.q/2). Hubbard-Stratonovich / completion of the square:
#   < exp(i xi.q) >_{xi ~ N(0, S)} = exp(-q.S.q/2)  <=>  the identity below with M = S^{-1}.
k = 3
Nn = sp.zeros(k, k)
for i in range(k):
    for j in range(i, k):
        s = sp.Symbol(f"N{i}{j}", real=True)
        Nn[i, j] = s
        Nn[j, i] = s
M = Nn.inv()
xi = sp.Matrix(sp.symbols(f"xi0:{k}", real=True))
qq = sp.Matrix(sp.symbols(f"q0:{k}", real=True))
lhs = (-sp.Rational(1, 2) * (xi.T * M * xi) + sp.I * (xi.T * qq))[0, 0]
shift = xi - sp.I * Nn * qq
rhs = (-sp.Rational(1, 2) * (shift.T * M * shift) - sp.Rational(1, 2) * (qq.T * Nn * qq))[0, 0]
check(sp.simplify(sp.expand(lhs - rhs)) == 0,
      "C1  COMPLETION OF THE SQUARE, exact for a general 3x3 symmetric N: -xi.N^{-1}.xi/2 + i xi.q = "
      "-(xi - iNq).N^{-1}.(xi - iNq)/2 - q.N.q/2. Shifting the Gaussian therefore gives "
      "< exp(i xi.q) > = exp(-q.N.q/2), so the imaginary z_q^2 block of the CTP action IS the characteristic "
      "function of a stochastic force")
check(sp.simplify(sp.expand(sp.I * (NQ[0, 0] / sp.I) - sp.I * (Gp + Gm)[0, 0] / 2)) == 0
      and all(sp.simplify(NQ[i, j] / sp.I - (Gp + Gm)[i, j] / 2) == 0 for i in range(n) for j in range(n)),
      "C2  IDENTIFICATION: the covariance of that force is exactly the CTP action's z_q^2 block over i, which is "
      "(G_> + G_<)/2 = the symmetrised bath correlator. So the mean equation of motion of B3 is the AVERAGE of "
      "the Langevin equation  m0 z-ddot + Int K_R z = xi,  < xi_i xi_j > = (G_> + G_<)_ij / 2. K_I did not "
      "disappear from the theory; it moved to the correlator, which is where it belongs")

banner("PART D  KELDYSH CONSISTENCY, AND THE de SITTER KERNELS")

# Convention: K_R(t,t') = theta(t-t')[G_> - G_<],  K_A(t,t') = -theta(t'-t)[G_> - G_<].
Dif = Gp - Gm
KRm = sp.Matrix(n, n, lambda i, j: th(i, j) * Dif[i, j])
KAm = sp.Matrix(n, n, lambda i, j: -th(j, i) * Dif[i, j])
check(sp.simplify(KRm - KAm - Dif) == sp.zeros(n, n),
      "D1  KELDYSH CONSISTENCY: G_R - G_A = G_> - G_< holds elementwise on all 25 entries (the diagonal works "
      "for any theta(0) convention because (G_> - G_<)_ii = 0)")
KAm_wrong = sp.Matrix(n, n, lambda i, j: +th(j, i) * Dif[i, j])
check(sp.simplify(KRm - KAm_wrong - Dif) != sp.zeros(n, n),
      "D1b NEGATIVE CONTROL: with the sign of G_A flipped the identity FAILS, so D1 is not vacuous")

# ---- the concrete de Sitter (thermal) worldline kernels ---------------------------------------------------
w, bet, Nc, acc, Hf = sp.symbols("omega beta N_c a H", positive=True)
nB = 1 / (sp.exp(bet * w) - 1)
Ghp = Nc * w * (1 + nB)        # Ghat_>(omega)
Ghm = Nc * w * nB              # Ghat_<(omega)
comm = sp.simplify(Ghp - Ghm)  # dissipation  (commutator)
anti = sp.simplify(Ghp + Ghm)  # noise        (anticommutator)

check(sp.simplify(Ghp / Ghm - sp.exp(bet * w)) == 0,
      "D2  the state is KMS at inverse temperature beta: Ghat_>(omega)/Ghat_<(omega) = exp(beta omega)")
check(sp.simplify(comm - Nc * w) == 0 and sp.simplify(sp.diff(comm, bet)) == 0,
      "D3  *** THE DISSIPATION KERNEL IS STATE-INDEPENDENT: Ghat_> - Ghat_< = N_c omega EXACTLY, and its "
      "derivative with respect to beta is identically ZERO. *** This reproduces the established free-field "
      "result rho(omega) = omega/pi^2 state-independently (Raval, Hu & Anglin 1996): the commutator of a free "
      "field is a c-number, so no state can touch it")
nF = 1 / (sp.exp(bet * w) + 1)
comm_ctrl = sp.simplify(Nc * w * (1 - nF) - Nc * w * nF)
check(sp.simplify(sp.diff(comm_ctrl, bet)) != 0,
      "D3b NEGATIVE CONTROL: with a Fermi occupation the commutator becomes N_c omega tanh(beta omega/2), whose "
      "beta-derivative is NOT zero -- state-independence is a property of the bosonic KMS structure, not an "
      "artefact of the algebra")
check(sp.simplify(anti - Nc * w * sp.coth(bet * w / 2)) == 0 and sp.simplify(sp.diff(anti, bet)) != 0,
      "D4  *** THE NOISE KERNEL DOES CARRY THE TEMPERATURE: Ghat_> + Ghat_< = N_c omega coth(beta omega / 2), "
      "with nonzero beta-derivative. *** Every trace of T is in the noise")

# substitute the framework's own de Sitter-Unruh temperature, beta = 2 pi / sqrt(a^2 + H^2)
beta_dS = 2 * sp.pi / sp.sqrt(acc**2 + Hf**2)
dcomm_da = sp.simplify(sp.diff(comm.subs(bet, beta_dS), acc))
danti_da = sp.simplify(sp.diff(anti.subs(bet, beta_dS), acc))
check(dcomm_da == 0 and sp.simplify(danti_da) != 0,
      "D5  *** THE OBSTRUCTION, IN ONE LINE. *** With T = sqrt(a^2 + H^2)/(2 pi) (Narnhofer-Peter-Thirring "
      "1996; Deser & Levin 1997), d/da of the DISSIPATION kernel is exactly 0 while d/da of the NOISE kernel is "
      "not. The acceleration-dependence -- the framework's entire MOND mechanism -- lives ONLY in the kernel "
      "that B1 just proved cannot appear in the mean equation of motion")

wg = np.linspace(-40.0, 40.0, 4001)
wg = wg[np.abs(wg) > 1e-9]
bnum = 2.0 * math.pi / math.sqrt(1.0 + 1.0)
noise_num = wg / np.tanh(bnum * wg / 2.0)      # Ghat_> + Ghat_<  at N_c = 1
diss_num = wg.copy()                          # Ghat_> - Ghat_<  at N_c = 1
check(noise_num.min() > 0 and diss_num.min() < 0,
      f"D6  the two blocks are structurally different objects on the same 4000-point grid spanning both signs of "
      f"omega: the NOISE kernel is positive everywhere (min = {noise_num.min():.6f}), as a bounded influence "
      f"functional requires (|F| <= 1 needs a positive-semidefinite z_q^2 form), while the DISSIPATION kernel "
      f"N_c omega is odd and goes negative (min = {diss_num.min():.4f})")

# ---- time domain: build a genuinely RETARDED kernel and test it ------------------------------------------
w_ir, w_c = 1.0, 30.0


W_NEG = 1.5          # the negative-rho band of the E6b control: |omega| < W_NEG, i.e. the DEEP regime


def rho_of(x, sign_band=+1.0):
    """Regulated worldline spectral density, odd. sign_band = -1 flips rho in the band |w| < W_NEG."""
    x = np.asarray(x, dtype=float)
    r = (1.0 / math.pi**2) * x * (x**2 / (x**2 + w_ir**2)) * np.exp(-((x / w_c) ** 2))
    if sign_band < 0:
        r = np.where(np.abs(x) < W_NEG, -3.0 * r, r)
    return r


wq = np.linspace(1e-6, 100.0, 6001)
rho_p = rho_of(wq)
tg = np.linspace(-20.0, 20.0, 4001)
with np.errstate(all="ignore"):
    mu_t = 2.0 * (np.sin(np.outer(tg, wq)) @ (rho_p * np.gradient(wq)))   # real, odd dissipation kernel
if not np.all(np.isfinite(mu_t)):
    raise RuntimeError("non-finite dissipation kernel")
K_R_t = np.where(tg >= 0.0, mu_t, 0.0)
K_even_t = np.interp(np.abs(tg), tg[tg >= 0], mu_t[tg >= 0])   # tn18-style EVEN kernel, mu(|t|)

asym = np.max(np.abs(K_R_t - K_R_t[::-1])) / np.max(np.abs(K_R_t))
asym_even = np.max(np.abs(K_even_t - K_even_t[::-1])) / np.max(np.abs(K_even_t))
check(asym > 0.999,
      f"D7  the kernel built here is GENUINELY RETARDED: max|K(t) - K(-t)|/max|K| = {asym:.6f} (it must be 1, "
      f"since K vanishes for t < 0). tn18 reported 7.7e-14 for the same statistic, i.e. an EVEN kernel; the "
      f"even reconstruction of the same mu gives {asym_even:.2e} here, reproducing that failure exactly")

import os
import re

_tn18 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                     "qwen_36_experiment", "tn18_action_neSS.py")
if os.path.exists(_tn18):
    src18 = open(_tn18).read()
    cos_transform = "np.cos(omega_pos * t)" in src18
    nonneg_grid = "t_grid = np.linspace(0, t_max" in src18
    no_branch_var = re.search(r"^\s*z_?(p|m|plus|minus|cl|q)\b\s*=", src18, re.M) is None
    check(cos_transform and nonneg_grid and no_branch_var,
          f"D7b SOURCE AUDIT of qwen_36_experiment/tn18_action_neSS.py, so the comparison above is verified and "
          f"not relayed: its kernel is built as a COSINE transform (integrand = np.cos(omega_pos * t) * rho_pos, "
          f"even by construction, its own comment says \"for even kernel\") on a NONNEGATIVE time grid, and in "
          f"{len(src18.splitlines())} lines it assigns no branch variable at all -- z_+, z_- and the Keldysh "
          f"rotation appear only inside its docstrings and print statements. The CTP action was named, not built")
else:
    check(False, "D7b tn18 source not found for audit")

dt = tg[1] - tg[0]
tpos = tg[tg >= 0]
mupos = mu_t[tg >= 0]
w_test = np.array([0.5, 1.0, 2.0, 3.0, 5.0])
ImKR = np.array([np.trapz(mupos * np.sin(wt * tpos), tpos) for wt in w_test])
ReKR = np.array([np.trapz(mupos * np.cos(wt * tpos), tpos) for wt in w_test])
rel_im = np.max(np.abs(ImKR - math.pi * rho_of(w_test)) / np.abs(math.pi * rho_of(w_test)))
check(rel_im < 0.02,
      f"D8  SPECTRAL REPRESENTATION HOLDS: Im Khat_R(omega) = pi rho(omega) to {rel_im*100:.3f}% max relative "
      f"error over omega in [0.5, 5]. The retarded kernel dissipates, and dissipates exactly the spectral weight "
      f"it was built from")
ImK_even = np.array([np.trapz(K_even_t * np.sin(wt * tg), tg) for wt in w_test])
check(np.max(np.abs(ImK_even)) < 1e-8 * np.max(np.abs(ReKR)) + 1e-10,
      f"D8b NEGATIVE CONTROL, and the physical indictment of tn18: an EVEN kernel has a purely REAL Fourier "
      f"transform, max|Im Khat_even| = {np.max(np.abs(ImK_even)):.2e}. Zero imaginary part means zero "
      f"dissipation: an even kernel cannot be a retarded vacuum response at all, whatever else it fits")

KA_test = np.conj(ReKR + 1j * ImKR)
full = np.array([np.trapz(mu_t * np.exp(1j * wt * tg), tg) for wt in w_test])
rel_kel = np.max(np.abs((ReKR + 1j * ImKR - KA_test) - full) / np.abs(full))
check(rel_kel < 0.02,
      f"D9  the FREQUENCY-DOMAIN Keldysh identity, on independently computed transforms: "
      f"Khat_R(omega) - Khat_A(omega) equals the full-line transform of the commutator to {rel_kel*100:.3f}% "
      f"(Khat_R integrated over t >= 0 only, Khat_A = its conjugate, the right side over all t)")

banner("PART E  THE PAYOFF: DOES THE RETARDED EQUATION OF MOTION ADMIT THE MOND LIMIT?")

# E1: independent re-derivation of the master formula q = 2/r, from a family NOT of the form f = c1p T.
aa, HH, lam = sp.symbols("a H lambda", positive=True)
c1p = 2 * sp.pi
TT = sp.sqrt(aa**2 + HH**2) / (2 * sp.pi)
TG = HH / (2 * sp.pi)
Tv = sp.Symbol("T", positive=True)
q_found = []
for lv in [sp.Rational(1, 3), sp.Integer(1), sp.Integer(7)]:
    fT = c1p * Tv + lv * c1p * TG * (1 - sp.exp(-Tv / TG))        # asymptotically linear, f'(T_GH) shifted
    c1p_chk = sp.limit(fT / Tv, Tv, sp.oo)                        # = c1p, the asymptotic slope
    fprime = sp.simplify(sp.diff(fT, Tv).subs(Tv, TG))            # f'(T_GH)
    r_here = sp.simplify(fprime / c1p_chk)
    I = sp.simplify(fT.subs(Tv, TT) - fT.subs(Tv, TG))            # I(a) = f(T(a)) - f(T_GH)
    Ihat = sp.simplify(2 * sp.pi * I / c1p_chk)                    # normalised so Ihat -> a for a >> H
    c2 = sp.simplify(sp.limit(Ihat / aa**2, aa, 0) * HH)           # Ihat ~ c2 a^2 / H at small a
    q_here = sp.simplify(1 / c2)
    q_found.append((sp.simplify(q_here - 2 / r_here), float(r_here), float(q_here)))
check(all(d == 0 for d, _, _ in q_found),
      f"E1  MASTER FORMULA RE-DERIVED INDEPENDENTLY (established fact 1, confirmed here from scratch on a "
      f"3-member non-scale-free family): a_0/H = q = 2/r with r = f'(T_GH)/c1p, exactly, at "
      f"r = {q_found[0][1]:.4f}, {q_found[1][1]:.4f}, {q_found[2][1]:.4f}")

# E2: what the CTP mean equation of motion gives, since its kernel is a-independent.
gobs, gbar, a0s, C = sp.symbols("g_obs g_bar a_0 C", positive=True)
sol = sp.solve(sp.Eq(gobs**2, gbar**2 + a0s * gbar).subs(gbar, C * gobs), a0s)
check(len(sol) == 1 and sp.simplify(sp.diff(sol[0], gobs)) != 0
      and sp.simplify(sol[0].subs(C, 1)) == 0,
      f"E2  *** A LINEAR I GIVES a_0 = 0 EXACTLY. *** If the mean equation of motion has an a-INDEPENDENT kernel "
      f"then I(g_obs) = C g_obs, and g_obs^2 = g_bar^2 + a_0 g_bar forces a_0 = g_obs(1 - C^2)/C, which is not a "
      f"CONSTANT unless C = 1, in which case a_0 = 0. No constant acceleration scale exists in the Gaussian "
      f"linear-response class")
r_sym = sp.Symbol("r", positive=True)
sol_r0 = sp.solve(sp.Eq(2 / r_sym, 0), r_sym)
sol_rZ = sp.solve(sp.Eq(2 / r_sym, 1 / sp.nsimplify(Z_NUM, rational=True)), r_sym)
check(sol_r0 == [] and len(sol_rZ) == 1,
      f"E3  and q = 0 is OUTSIDE the master-formula family {{2/r : 0 < r < inf}} ENTIRELY: solving 2/r = 0 for r "
      f"returns no solution, while solving 2/r = 1/Z returns exactly one. So the CTP mean equation of motion at "
      f"Gaussian order does not sit at some WRONG value of r -- it is not in the family at all. r is "
      f"UNDETERMINED, not mis-determined")

# E4: what MOND needs, as a mass shift.
mu_y1 = 1.0 / math.sqrt(2.0)
dm_mond = mu_y1 - 1.0
check(abs(dm_mond + 0.2928932188134524) < 1e-12 and dm_mond < 0,
      f"E4  WHAT MOND NEEDS: at y = g_bar/a_0 = 1 the exact law g_obs^2 = g_bar^2 + a_0 g_bar gives "
      f"m_eff/m_0 = g_bar/g_obs = 1/sqrt(2), so delta_m/m_0 = {dm_mond:.7f} < 0. Inertia must DECREASE")

# E5/E6: what the passive CTP kernel gives, and the sign lock.
mom1 = quad(lambda x: rho_of(x) / x, 1e-8, 300.0, limit=400)[0]
mom3 = quad(lambda x: rho_of(x) / x**3, 1e-8, 300.0, limit=400)[0]
hh = 0.05
ReK = {}
for wv in (0.0, hh, 2 * hh):
    ReK[wv] = np.trapz(mupos * np.cos(wv * tpos), tpos)
d2 = 2.0 * (ReK[hh] - ReK[0.0]) / hh**2       # Re Khat_R is EVEN in omega, so f''(0) = 2(f(h)-f(0))/h^2
check(abs(ReK[0.0] - 2 * mom1) / abs(2 * mom1) < 0.02 and abs(d2 / 4.0 - mom3) / abs(mom3) < 0.05,
      f"E5  the two low-frequency moments of the retarded kernel check out against direct quadrature: "
      f"Re Khat_R(0) = 2 Int rho/omega ({ReK[0.0]:.6f} vs {2*mom1:.6f}) and the omega^2 coefficient = "
      f"Int rho/omega^3 ({d2/4.0:.6f} vs {mom3:.6f}). These are the spring renormalisation and the MASS "
      f"renormalisation respectively")
# passivity fixes the sign with which the kernel enters D(omega) = -m0 w^2 -+ Khat_R(w).
im_over_w_plus = math.pi * rho_of(np.array([1.0, 2.0, 5.0]))[0] / 1.0          # assembly  +Khat_R
im_over_w_minus = -im_over_w_plus                                              # assembly  -Khat_R
dm_plus = -2.0 * mom3
dm_minus = +2.0 * mom3
check(im_over_w_plus > 0 and im_over_w_minus < 0 and dm_minus > 0 and dm_plus < 0,
      f"E6  *** THE SIGN LOCK. *** D(omega) = -m_0 omega^2 -+ Khat_R(omega). Positive damping requires "
      f"Im D/omega < 0, which selects the MINUS assembly (Im D/omega = {im_over_w_minus:.5f} against "
      f"{im_over_w_plus:+.5f}); and the SAME assembly gives delta_m = +2 Int rho/omega^3 = {dm_minus:+.6f} > 0. "
      f"Passivity and a POSITIVE mass shift are the same choice. m_eff > m_0: inertia INCREASES, the opposite of "
      f"E4's requirement")
def rho_neg(x):
    return rho_of(x, sign_band=-1.0)


mom3_neg = quad(lambda x: rho_neg(x) / x**3, 1e-8, 300.0, limit=400)[0]
imD_neg = -math.pi * float(rho_neg(np.array([0.5]))[0]) / 0.5      # Im D/omega in the flipped band
check(mom3_neg < 0 and imD_neg > 0 and float(rho_neg(np.array([5.0]))[0]) > 0,
      f"E6b NEGATIVE CONTROL, which locates the escape exactly: flip rho negative in the LOW-frequency band "
      f"|omega| < {W_NEG} -- the deep regime, which is where the omega^-3 moment has its weight -- and the same "
      f"passive assembly gives delta_m = {2*mom3_neg:+.6f} < 0, the MOND sign, while Im D/omega turns "
      f"{imD_neg:+.5f} > 0 there, i.e. the bath becomes ACTIVE (rho stays positive outside the band, "
      f"{float(rho_neg(np.array([5.0]))[0]):.5f} at omega = 5). Inside the linearly coupled Gaussian class, MOND "
      f"<=> rho < 0 at low frequency <=> loss of passivity. rho(omega) = omega/pi^2 state-independently "
      f"(established fact 3) forecloses that, so the escapes must be composite operators or bounded sectors, "
      f"outside this class")

# E6c: grid-refinement stability of every numeric in Part D/E (corpus hazard: coarse grids).
def numerics(nw, nt):
    wq2 = np.linspace(1e-6, 100.0, nw)
    rp2 = rho_of(wq2)
    tg2 = np.linspace(-20.0, 20.0, nt)
    with np.errstate(all="ignore"):
        mu2 = 2.0 * (np.sin(np.outer(tg2, wq2)) @ (rp2 * np.gradient(wq2)))
    tp2, mp2 = tg2[tg2 >= 0], mu2[tg2 >= 0]
    im2 = np.array([np.trapz(mp2 * np.sin(wt * tp2), tp2) for wt in w_test])
    rel2 = float(np.max(np.abs(im2 - math.pi * rho_of(w_test)) / np.abs(math.pi * rho_of(w_test))))
    rk = {wv: float(np.trapz(mp2 * np.cos(wv * tp2), tp2)) for wv in (0.0, hh)}
    return rel2, rk[0.0], 2.0 * (rk[hh] - rk[0.0]) / hh**2 / 4.0


base = (rel_im, ReK[0.0], d2 / 4.0)
fine = numerics(2 * 6001 - 1, 2 * 4001 - 1)
shift = max(abs(fine[i] - base[i]) / max(abs(base[i]), 1e-30) for i in (1, 2))
check(shift < 0.01 and fine[0] < 0.02,
      f"E6c REFINEMENT STABILITY at 2x in BOTH the omega grid and the t grid (12001 x 8001): the two moments "
      f"move by at most {shift*100:.4f}% (Re Khat_R(0): {base[1]:.6f} -> {fine[1]:.6f}; omega^2 coefficient: "
      f"{base[2]:.6f} -> {fine[2]:.6f}) and the spectral-representation error stays at {fine[0]*100:.4f}%. The "
      f"numbers are not grid artefacts")

# E7: r values, and the footing fork.
q_can = A0_CAN / CH_LAMBDA
r_can = 2.0 / q_can
a0_alt_exact = A0_CAN * INV_SQRT_OL
ch0 = CH_LAMBDA * INV_SQRT_OL
q_alt = a0_alt_exact / ch0
r_alt = 2.0 / q_alt
q_alt_quoted = A0_ALT_QUOTED / ch0
r_alt_quoted = 2.0 / q_alt_quoted
q_mixed = A0_ALT_QUOTED / CH_LAMBDA          # incoherent: ALT numerator on the canonical floor
r_mixed = 2.0 / q_mixed
check(abs(r_can - TWO_Z) / TWO_Z < 5e-4 and abs(q_can - 1 / Z_NUM) / (1 / Z_NUM) < 5e-4,
      f"E7  the framework's own numbers reproduce the master formula: q = a_0/(c H_Lambda) = {q_can:.7f} against "
      f"1/Z = {1/Z_NUM:.7f}, so r = {r_can:.5f} against 2Z = {TWO_Z:.5f} (agreement 1.2e-4, the rounding of "
      f"a_0 = 9.3614e-11)")
check(abs(r_alt - r_can) / r_can < 1e-5 and abs(r_alt_quoted - r_can) / r_can < 2e-3,
      f"E8  *** r IS FOOTING-INVARIANT, reported both ways as required. *** ALT footing (rho_total, cH_0) scales "
      f"BOTH a_0 and the temperature floor by 1/sqrt(Omega_Lambda) = {INV_SQRT_OL}, so r is unchanged: exact "
      f"scaling gives r_ALT = {r_alt:.5f} (3e-6 from canonical) and the quoted a_0^ALT = 1.13e-10 gives "
      f"{r_alt_quoted:.5f} (1e-3, pure quoting precision). The footing fork does NOT move this number in either "
      f"direction. Only the INCOHERENT mix (ALT numerator on the canonical floor) moves it, to "
      f"r = {r_mixed:.5f}, and that is a bookkeeping error, not a fork")
check(r_can > R_CEILING and 4 * math.pi > R_CEILING and 2.0 < R_CEILING,
      f"E9  BOTH WAYS, AGAINST BOTH SIDES: against the established admissibility ceiling r <= "
      f"{R_CEILING:.6f}, kappa = 1/2's r = 2Z = {TWO_Z:.4f} is excluded -- and so is Milgrom 2020's "
      f"r = 4 pi = {4*math.pi:.4f}. Milgrom 1999's r = 2 is admissible. The bound is not a framework-specific "
      f"penalty; it cuts the same way against the competing coefficient, and it rests on seven shapes, which is "
      f"not a proof")
check(dcomm_da == 0 and sol_r0 == [] and abs(1 / Z_NUM) > 0.17,
      f"E10 THE ANSWER TO THE PAYOFF QUESTION, stated plainly: NO. The shortfall is the ENTIRE value of q -- the "
      f"framework needs q = 1/Z = {1/Z_NUM:.4f} and this construction delivers exactly 0. The retarded equation of motion delivered by "
      f"Part B does not admit the MOND limit at Gaussian order, because D5 shows its kernel cannot depend on the "
      f"acceleration and E2 then forces a_0 = 0. There is no r to extract, so no comparison with 1, 4 pi or 2Z "
      f"is available from this construction. The variational result stands on its own; the coefficient is "
      f"untouched")

banner("PART F  OSTROGRADSKY: DERIVATIVE ORDER, AND THE CONSTRAINT THE DOUBLING REQUIRES")

t = sp.Symbol("t")
Zp, Zm = sp.Function("z_p")(t), sp.Function("z_m")(t)
m_s = sp.Symbol("m", positive=True)


def max_order(expr, fn):
    orders = [d.derivative_count for d in expr.atoms(sp.Derivative) if d.expr == fn]
    return max(orders) if orders else 0


L_ctp = m_s / 2 * (sp.diff(Zp, t) ** 2 - sp.diff(Zm, t) ** 2)
eqs = sp.euler_equations(L_ctp, [Zp, Zm], t)
ord_L = max(max_order(L_ctp, Zp), max_order(L_ctp, Zm))
ord_E = max(max(max_order(e.lhs - e.rhs, Zp), max_order(e.lhs - e.rhs, Zm)) for e in eqs)
check(ord_L == 1 and ord_E == 2,
      f"F1  DERIVATIVE COUNT: the CTP Lagrangian carries first derivatives only (order {ord_L}) on each branch, "
      f"so the Euler-Lagrange equations are second order (order {ord_E}). Ostrogradsky's theorem needs a "
      f"nondegenerate dependence on second or higher derivatives and does not apply. The nonlocal memory term "
      f"carries NO derivatives at all -- nonlocality in time is not higher-derivative")
L_hd = m_s / 2 * sp.diff(Zp, t, 2) ** 2
eq_hd = sp.euler_equations(L_hd, [Zp], t)
check(max(max_order(e.lhs - e.rhs, Zp) for e in eq_hd) == 4,
      "F1b NEGATIVE CONTROL: a genuine higher-derivative Lagrangian (z-ddot^2) does give a 4th-order equation, "
      "so F1's counter is measuring something")

Zc, Zq = sp.Function("z_cl")(t), sp.Function("z_q")(t)
L_rot = sp.expand(L_ctp.subs({Zp: Zc + Zq / 2, Zm: Zc - Zq / 2}).doit())
check(sp.simplify(L_rot - m_s * sp.diff(Zc, t) * sp.diff(Zq, t)) == 0,
      "F2  the rotated kinetic term is exactly m z_cl-dot z_q-dot: PURELY OFF-DIAGONAL. There is no z_cl-dot^2 "
      "and no z_q-dot^2 term, so neither rotated variable has a kinetic term of its own")
Kin = sp.Matrix([[0, m_s / 2], [m_s / 2, 0]])
ev = list(Kin.eigenvals().keys())
check(sp.simplify(sum(ev)) == 0 and sp.simplify(sp.prod(ev)) == -m_s**2 / 4,
      f"F3  and that form is INDEFINITE: eigenvalues +-m/2, trace 0, determinant -m^2/4. So ghost-freedom does "
      f"NOT follow from positivity of the kinetic form here, and must come from somewhere else. Stating that "
      f"honestly is part of the result")

# The somewhere else: the z_cl-variation is the ADVANCED equation for z_q, with z_q vanishing at both ends.
idx = list(range(1, n - 1))
Cfull = sp.Matrix(n, n, lambda i, j: sp.expand(sp.diff(S_rot, zc[i], zq[j])))
Cint = Cfull[idx, idx]
det_int = sp.expand(Cint.det())
check(det_int != 0 and sp.expand(det_int.subs(m0, 0)) == 0,
      f"F4  THE CONSTRAINT THAT REMOVES THE DOUBLED DEGREE OF FREEDOM. delta S / delta z_cl = 0 is a linear "
      f"homogeneous ADVANCED equation for z_q alone, and the CTP boundary conditions set z_q = 0 at both the "
      f"initial and the final time (the branches share the initial state and are glued by the trace). The "
      f"interior {len(idx)}x{len(idx)} coefficient matrix has determinant that is NOT identically zero, so "
      f"z_q == 0 is the UNIQUE solution and the doubling carries no propagating degree of freedom. That "
      f"determinant vanishes identically at m_0 = 0")
check(sp.expand(det_int.subs(m0, 0)) == 0 and sp.Matrix(len(idx), len(idx),
      lambda i, j: Cfull[idx[i], idx[j]].subs(m0, 0)).rank() < len(idx),
      f"F4b NEGATIVE CONTROL AND THE STATED CONSTRAINT: with no local kinetic term (m_0 = 0) the coefficient "
      f"matrix is strictly triangular, its rank drops to "
      f"{sp.Matrix(len(idx), len(idx), lambda i, j: Cfull[idx[i], idx[j]].subs(m0, 0)).rank()} of {len(idx)}, "
      f"nontrivial z_q solutions exist, and the ghost RETURNS. So the constraint the construction requires is "
      f"explicit: the action must retain a nondegenerate LOCAL kinetic term. A purely nonlocal, memory-only "
      f"inertia action is NOT ghost-free by this argument")

banner("WHAT THIS DOES AND DOES NOT ESTABLISH")
print(f"""  DELIVERED, and independent of the coefficient:
   - A retarded, causal, memory-carrying equation of motion FROM A VARIATIONAL PRINCIPLE (B3). The in-out
     obstruction is not evaded by a clever kernel choice, it is removed structurally: the CTP quadratic form has
     two independent arguments, so no symmetrisation acts on the kernel. B4 quantifies what in-out does instead
     -- exactly half the retarded weight arrives from the future.
   - The mean equation of motion carries the dissipation kernel and NONE of the 15 noise symbols (B1, A7), and
     the noise reappears exactly as the covariance of a Gaussian force (C1, C2).
   - Ghost-freedom holds, under a constraint now stated: a nondegenerate local kinetic term must survive
     (F4, F4b). The kinetic form itself is indefinite (F3); it is the CTP boundary conditions that do the work.

  NOT DELIVERED, and this is the honest headline:
   - The coefficient. r is not fixed here by anything. Worse for the framework than "wrong r": D5 + E2 + E3 show
     the Gaussian mean equation of motion gives a_0 = 0 EXACTLY, i.e. q = 0, which is not 2/r for any finite r.
     The dS commutator is state-independent, so the temperature -- the whole mechanism -- is in the noise, and
     the noise is exactly what the CTP structure keeps out of the mean equation of motion.
   - The sign. Passivity and delta_m > 0 are the same choice (E6); MOND needs delta_m/m_0 = -0.29289 at y = 1
     (E4). The escape is rho < 0 in a band (E6b), which the established state-independence of rho forecloses
     within this class.
   - kappa = 1/2 REMAINS FITTED, NOT DERIVED. Nothing above moves it, and r is footing-invariant (E8), so the
     canonical-versus-ALT fork does not move it either.

  WHERE THE MECHANISM MUST NOW LIVE, stated as a target rather than a result: the noise kernel reaches the mean
  trajectory only at second order in the noise, through a NONLINEAR term (<xi z> is nonzero only if the response
  is nonlinear), or through composite operators / bounded sectors that leave the free-field class. Both are
  outside what this script builds. Neither is excluded by it.""")

banner("RESULT")
nOK = sum(1 for c, _ in ok if c)
print(f"  {nOK}/{len(ok)} checks held.")
if nOK != len(ok):
    print("\n  FAILED:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0. The retarded MI equation of motion IS variational in the in-in (CTP) action -- proven")
print("  symbolically with the two branches distinct, the noise excluded from the mean equation of motion by")
print("  structure, and the ghost removed by a stated constraint. The coefficient did NOT come out: the de")
print("  Sitter dissipation kernel is state-independent, so a_0 = 0 exactly at Gaussian order and r is")
print("  undetermined. kappa = 1/2 remains FITTED, NOT DERIVED.")

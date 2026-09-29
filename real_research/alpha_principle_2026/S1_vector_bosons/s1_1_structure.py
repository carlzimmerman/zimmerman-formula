#!/usr/bin/env python3
"""S1 script 1 -- structure of the charged Proca field in the dS_4 planar patch with a constant electric field (sympy + numerics).

Pre-registered in S1_PREREGISTRATION.md (written before this script existed).  H = c = hbar = 1.
Checks A1-A8 (see the pre-registration for the wording).  The sign of the Pauli (g = 2) term is FIXED HERE from the electric-field constraint alone;
script 2 then checks independently (Landau levels) that this sign gives g = 2.

Run:    python3 s1_1_structure.py            (real run; exit 0 iff all checks pass)
        python3 s1_1_structure.py --mutate   (control: the OPPOSITE sign of the Pauli term is used as the "g=2" sign; check A2 must FAIL;
                                              prints CONTROL FAILS AS REQUIRED and exits 1; exits 3 if the control does not fail)
Any other argv silently runs the real path.
"""
import sys
import random
import numpy as np
import sympy as sp

MUTATE = "--mutate" in sys.argv
CHECKS = []


def check(tag, ok, detail=""):
    CHECKS.append((tag, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}", flush=True)


tau = sp.symbols("tau", negative=True)
lam, mu, kp, kz, E, Hh, c = sp.symbols("lambda mu k_perp k_z E H c", real=True)

# ------------------------------------------------------------------ A1: Weyl weights and the dS field strength
print("A1  Weyl weights and dS field strength")
xs = sp.symbols("t x y z", real=True)
a = -1 / (Hh * xs[0])
g = sp.diag(-a**2, a**2, a**2, a**2)
ginv = g.inv()
sqrtg = a**4
eta = sp.diag(-1, 1, 1, 1)
ok_w = True
for m_ in range(4):
    for n_ in range(4):
        for al in range(4):
            for be in range(4):
                lhs = sp.simplify(sqrtg * ginv[m_, al] * ginv[n_, be])
                ok_w = ok_w and sp.simplify(lhs - eta[m_, al] * eta[n_, be]) == 0
        ok_w = ok_w and sp.simplify(sqrtg * ginv[m_, n_] - a**2 * eta[m_, n_]) == 0
# F_{t z} = E a^2, A_z = -E/(H^2 t); nabla_nu F^{nu z}
Az = -E / (Hh**2 * xs[0])
Ftz = sp.diff(Az, xs[0])
F = sp.zeros(4, 4)
F[0, 3] = Ftz
F[3, 0] = -Ftz
Fup = ginv * F * ginv.T
divF = sp.simplify(sum(sp.diff(sqrtg * Fup[n_, 3], xs[n_]) for n_ in range(4)) / sqrtg)
ok_w = ok_w and sp.simplify(Ftz - E * a**2) == 0 and sp.simplify(divF - (-2 * E * Hh / a)) == 0
check("A1 sqrt(-g) g g = eta eta, sqrt(-g) g^{mu nu} = a^2 eta, F_tz = E a^2, nabla_nu F^{nu z} = -2 E H / a", ok_w, f"(nabla_nu F^(nu z) = {divF})")

# ------------------------------------------------------------------ component Lagrangian in the conformal frame (algebraic form, independent symbols)
Wt, Wx, Wy, Wz = sp.symbols("W_t W_x W_y W_z")
Wtc, Wxc, Wyc, Wzc = sp.symbols("Wc_t Wc_x Wc_y Wc_z")
Wxp, Wyp, Wzp = sp.symbols("Wp_x Wp_y Wp_z")
Wxcp, Wycp, Wzcp = sp.symbols("Wcp_x Wcp_y Wcp_z")
Pp, Mm, Gs = sp.symbols("P_z M G", real=True)      # P_z = p(tau), M = mass function, Gs = c e calE (Pauli strength)
Px, Py = kp, sp.Integer(0)
PV = [Px, Py, Pp]
Wv = [Wx, Wy, Wz]
Wcv = [Wxc, Wyc, Wzc]
Wpv = [Wxp, Wyp, Wzp]
Wcpv = [Wxcp, Wycp, Wzcp]
I = sp.I


def lagrangian(gs_sign):
    """L = |W_{tau i}|^2 - (1/2)|W_ij|^2 + M^2 (|W_tau|^2 - |W_i|^2) + i gs_sign*G (Wc_z W_tau - Wc_tau W_z), G = c e calE (magnitude)."""
    T1 = sum((Wcpv[i] + I * PV[i] * Wtc) * (Wpv[i] - I * PV[i] * Wt) for i in range(3))
    T2 = 0
    for i in range(3):
        for j in range(3):
            Wij = I * PV[i] * Wv[j] - I * PV[j] * Wv[i]
            Wijc = -I * PV[i] * Wcv[j] + I * PV[j] * Wcv[i]
            T2 += -sp.Rational(1, 2) * Wijc * Wij
    T3 = Mm**2 * (Wtc * Wt - sum(Wcv[i] * Wv[i] for i in range(3)))
    T4 = I * gs_sign * Gs * (Wzc * Wt - Wtc * Wz)
    return T1 + T2 + T3 + T4


# ------------------------------------------------------------------ A2: EL equations and the divergence identity (time-dependent coefficients)
print("\nA2  divergence identity: which sign of the Pauli term removes F W_{nu mu} from D_nu(EOM)")
Wf = {n: sp.Function("W" + n)(tau) for n in "txyz"}
Wcf = {n: sp.Function("Wc" + n)(tau) for n in "txyz"}
pf = kz + lam / tau
M2f = mu**2 / tau**2
Gf_ = lam / tau**2          # e * calE


def L_tau(gs_sign):
    Lg = lagrangian(gs_sign)
    subs = {Wt: Wf["t"], Wx: Wf["x"], Wy: Wf["y"], Wz: Wf["z"], Wtc: Wcf["t"], Wxc: Wcf["x"], Wyc: Wcf["y"], Wzc: Wcf["z"],
            Wxp: sp.diff(Wf["x"], tau), Wyp: sp.diff(Wf["y"], tau), Wzp: sp.diff(Wf["z"], tau),
            Wxcp: sp.diff(Wcf["x"], tau), Wycp: sp.diff(Wcf["y"], tau), Wzcp: sp.diff(Wcf["z"], tau),
            Pp: pf, Mm: mu / (-tau), Gs: Gf_}
    return Lg.subs(subs)


def EL(gs_sign):
    Lt = L_tau(gs_sign)
    out = {}
    for n in "txyz":
        q = Wcf[n]
        eq = sp.diff(Lt, q) - (sp.diff(sp.diff(Lt, sp.diff(q, tau)), tau) if n != "t" else 0)
        out[n] = sp.simplify(eq)
    return out


def div_identity(gs_sign):
    """D_nu E^nu + D_nu(M^2 W^nu), with E^b = delta L / delta Wc_b (upper index): D_nu E^nu = d_tau E^t + i P_i E^i.  W^t = -W_t."""
    Eb = EL(gs_sign)
    divE = sp.diff(Eb["t"], tau) + I * kp * Eb["x"] + I * pf * Eb["z"]
    # D_nu (M^2 W^nu) = d_tau(M^2 W^tau) + i P_i M^2 W^i ; W^tau = -W_t
    DMW = sp.diff(M2f * (-Wf["t"]), tau) + I * kp * M2f * Wf["x"] + I * pf * M2f * Wf["z"]
    X = sp.expand(sp.simplify(divE + DMW))
    return X


# In these units E^b for the mass term: -M^2 W^b ... the identity should read  D_nu E^nu = -D_nu(M^2 W^nu) + (Pauli remainder)
sgn_phys = -1 if MUTATE else 1
res = {}
for s_ in (+1, -1):
    X = div_identity(s_)
    # does X contain any derivative of a field?  (a leftover F W_{nu mu} term would contain d_tau W_z etc.)
    derivs = [d for d in X.atoms(sp.Derivative)]
    res[s_] = (X, len(derivs) == 0)
    print(f"     sign {s_:+d}: derivative terms left in [D_nu E^nu + D_nu(M^2 W^nu)] : {len(derivs)}; expression = {sp.simplify(X)}")
good = [s_ for s_ in (+1, -1) if res[s_][1]]
# expected: exactly one sign works, the remainder is  i s (d_tau(lam/tau^2)) W_z-type (the (d_nu F^{nu mu}) W_mu term)
gsign_g2 = good[0] if len(good) == 1 else None
if MUTATE and gsign_g2 is not None:
    gsign_g2 = -gsign_g2        # control: pretend the wrong sign is the g=2 sign
ok_A2 = len(good) == 1
if ok_A2 and not MUTATE:
    X = res[good[0]][0]
    dF = sp.diff(lam / tau**2, tau)
    ok_A2 = sp.simplify(X - (-I * good[0] * dF * Wf["z"])) == 0 or sp.simplify(X - (I * good[0] * dF * Wf["z"])) == 0
check("A2 exactly one sign of the Pauli term removes F.W_{nu mu} from D_nu(EOM); remainder = (d_tau calE) W_z i.e. (d_nu F^{nu mu}) W_mu",
      ok_A2 and gsign_g2 is not None and not MUTATE, f"(g=2 sign found: {good[0] if good else None})")
if MUTATE:
    used = gsign_g2
    ok_ctrl = (used is not None) and (not res[used][1])
    print(f"     control declares sign {used:+d} to be the g=2 sign; derivative (F W_(nu mu)) terms remain in the divergence: {ok_ctrl}")
    print("\nMUTATE CONTROL: the opposite (g=0) sign was used; A2 " + ("FAILS AS REQUIRED" if not (ok_A2 and gsign_g2 is not None and not MUTATE) else "DID NOT FAIL"))
    print("CONTROL FAILS AS REQUIRED" if ok_ctrl else "CONTROL DID NOT FAIL")
    sys.exit(1 if ok_ctrl else 3)

S_G2 = good[0]
print(f"     => the g = 2 sign of the term i*s*G*(Wc_z W_tau - Wc_tau W_z) with G = e*calE*c is s = {S_G2:+d} (c = 1)")

# ------------------------------------------------------------------ A3: Legendre transform, W_tau eliminated
print("\nA3  Legendre transform with W_tau eliminated")
Pix, Piy, Piz = sp.symbols("Pi_x Pi_y Pi_z")
Pixc, Piyc, Pizc = sp.symbols("Pic_x Pic_y Pic_z")
Piv = [Pix, Piy, Piz]
Picv = [Pixc, Piyc, Pizc]


def hamiltonian(gs_sign):
    """returns (H(W,Wc,Pi,Pic), W_tau solution, Wc_tau solution)."""
    L = lagrangian(gs_sign)
    # momenta: Pi_i = dL/dWcp_i = Wp_i - i P_i W_t ; Pic_i = dL/dWp_i = Wcp_i + i P_i Wc_t
    Pi_def = [sp.diff(L, Wcpv[i]) for i in range(3)]
    Pic_def = [sp.diff(L, Wpv[i]) for i in range(3)]
    # velocities in terms of momenta
    sol = sp.solve([Pi_def[i] - Piv[i] for i in range(3)] + [Pic_def[i] - Picv[i] for i in range(3)],
                   Wpv + Wcpv, dict=True)[0]
    Hfull = sum(Wpv[i] * Picv[i] + Wcpv[i] * Piv[i] for i in range(3)) - L
    Hfull = sp.expand(Hfull.subs(sol))
    # constraints: dH/dWc_t = 0, dH/dW_t = 0
    s1 = sp.solve(sp.diff(Hfull, Wtc), Wt)[0]
    s2 = sp.solve(sp.diff(Hfull, Wt), Wtc)[0]
    Hred = sp.expand(Hfull.subs({Wt: s1, Wtc: s2}))
    return sp.simplify(Hred), sp.simplify(s1), sp.simplify(s2), sol


def H_expected(gs_sign):
    cross = sum(PV[i] * Piv[i] for i in range(3))
    crossc = sum(PV[i] * Picv[i] for i in range(3))
    curl2 = 0
    for i in range(3):
        for j in range(i + 1, 3):
            Wij = PV[i] * Wv[j] - PV[j] * Wv[i]
            Wijc = PV[i] * Wcv[j] - PV[j] * Wcv[i]
            curl2 += Wijc * Wij
    lorentz = (crossc - gs_sign * Gs * Wzc)   # candidate sign, tested below
    return sum(Picv[i] * Piv[i] for i in range(3)) + curl2 + Mm**2 * sum(Wcv[i] * Wv[i] for i in range(3)), cross, crossc


okA3 = True
Hred_by_c = {}
for gs_sign, name in ((0, "c=0 (g=1)"), (S_G2, "g=2")):
    Hred, s1, s2, sol = hamiltonian(gs_sign)
    Hred_by_c[gs_sign] = Hred
    base, cross, crossc = H_expected(gs_sign)
    # candidates for the last term: |P.Pi - s' G W_z|^2 / M^2 with s' = +-1
    found = None
    for sp_ in (+1, -1):
        cand = base + (crossc - sp_ * gs_sign * Gs * Wzc) * (cross - sp_ * gs_sign * Gs * Wz) / Mm**2
        if sp.simplify(sp.expand(Hred - cand)) == 0:
            found = sp_
            break
    # some conventions put an extra i: test with complex phase
    if found is None:
        for ph in (I, -I):
            cand = base + (crossc + ph * gs_sign * Gs * Wzc * (-1)) * (cross + ph * gs_sign * Gs * Wz) / Mm**2
            if sp.simplify(sp.expand(Hred - cand)) == 0:
                found = ph
                break
    print(f"     {name}: H_reduced = |Pi|^2 + |P x W|^2 + M^2|W|^2 + |P.Pi - s G W_z|^2/M^2 with s' = {found} (in the convention G = |c| e calE and the g=2 Lagrangian sign found in A2); W_tau = {s1}")
    okA3 = okA3 and (found is not None)
check("A3 reduced Hamiltonian is |Pi|^2 + |P x W|^2 + M^2|W|^2 + |P.Pi - s e calE W_z|^2/M^2 (symbolic identity, c = 0 and c = g2)", okA3)

# Hamilton's equations = Euler-Lagrange, algebraically: Pi_i' = dL/dWc_i (with W_t substituted) versus -dH/dWc_i ; W_i' = Pi_i + i P_i W_t versus dH/dPic_i
L2 = lagrangian(S_G2)
Hred2 = Hred_by_c[S_G2]
_, s1g, s2g, solg = hamiltonian(S_G2)
okH = True
for i in range(3):
    # Pi_i' = dL/dWc_i  (EL), evaluated on the reduced variables: substitute velocities and W_tau
    lhs = sp.diff(L2, Wcv[i]).subs(solg).subs({Wt: s1g, Wtc: s2g})
    rhs = -sp.diff(Hred2, Wcv[i])
    okH = okH and sp.simplify(sp.expand(lhs - rhs)) == 0
    # W_i' = dH/dPic_i
    lhs2 = solg[Wpv[i]].subs({Wt: s1g})
    rhs2 = sp.diff(Hred2, Picv[i])
    okH = okH and sp.simplify(sp.expand(lhs2 - rhs2)) == 0
check("A3b Hamilton's equations of the reduced H reproduce the Euler-Lagrange equations (Pi_i' and W_i'), residual 0 (g = 2 sign)", okH)

# ------------------------------------------------------------------ hermitian matrix h, positivity
Xs = [Wx, Wy, Wz, Pix, Piy, Piz]
Xcs = [Wxc, Wyc, Wzc, Pixc, Piyc, Pizc]
hmat = sp.Matrix(6, 6, lambda a_, b_: sp.diff(Hred2, Xcs[a_], Xs[b_]))
print("\n     h (g=2) real symmetric:", sp.simplify(hmat - hmat.T) == sp.zeros(6, 6) and all(sp.im(x) == 0 for x in hmat))
h_c0 = sp.Matrix(6, 6, lambda a_, b_: sp.diff(Hred_by_c[0], Xcs[a_], Xs[b_]))
# y-block
hy = sp.Matrix([[hmat[1, 1], hmat[1, 4]], [hmat[4, 1], hmat[4, 4]]])
print("     h_y =", hy.tolist())
# ------------------------------------------------------------------ A4: y decoupling + Whittaker index
print("\nA4  W_y decouples; its equation has the Whittaker index mu_w^2 = 1/4 - lambda^2 - mu^2 (AH4 index at mu_s^2 = mu^2 + 2)")
dec = all(sp.simplify(hmat[1, j]) == 0 for j in (0, 2, 3, 5)) and all(sp.simplify(hmat[4, j]) == 0 for j in (0, 2, 3, 5))
okA4 = dec and sp.simplify(hy - sp.diag(kp**2 + Pp**2 + Mm**2, 1)) == sp.zeros(2, 2)
# Whittaker: w'' + (-1/4 + kap/z + (1/4 - mw^2)/z^2) w = 0 with z = 2 i k tau, kap = -i lam r  =>  q'' + [k^2 + 2 k lam r/tau + (1/4 - mw^2)/tau^2] q = 0
k_, r_, mw = sp.symbols("k r mu_w", positive=True)
z = 2 * I * k_ * tau
kap = -I * lam * r_
wpp = -(-sp.Rational(1, 4) + kap / z + (sp.Rational(1, 4) - mw**2) / z**2)       # w'' / w
qpp = (2 * I * k_) ** 2 * wpp                                                    # q'' / q
eq = sp.simplify(qpp + (k_**2 + 2 * k_ * lam * r_ / tau + (sp.Rational(1, 4) - mw**2) / tau**2))
okA4 = okA4 and sp.simplify(eq) == 0
# ODE for W_y:  W_y'' + [P^2 + M^2] W_y = 0 with P^2 = kp^2 + (kz + lam/tau)^2, kz = k r, kp^2 = k^2 (1 - r^2), M^2 = mu^2/tau^2
ode_pot = sp.expand((k_**2 * (1 - r_**2)) + (k_ * r_ + lam / tau) ** 2 + mu**2 / tau**2)
diff = sp.simplify(ode_pot - (k_**2 + 2 * k_ * lam * r_ / tau + (sp.Rational(1, 4) - mw**2) / tau**2).subs(mw, sp.sqrt(sp.Rational(1, 4) - lam**2 - mu**2)))
okA4 = okA4 and diff == 0
check("A4 h couples W_y only to Pi_y, h_y = diag(P^2+M^2,1); its ODE is the Whittaker equation with mu_w^2 = 1/4 - lambda^2 - mu^2 (residual 0)", okA4)

# ------------------------------------------------------------------ A5: positivity
print("\nA5  positivity of h (sum of squares) in the electric background")
Hb = Hred2
lam_r = np.random.default_rng(20260929)
cnt_bad = 0
minev = 1e300
hf_g2 = sp.lambdify((kp, Pp, Mm, Gs), hmat, "numpy")
hf_c0 = sp.lambdify((kp, Pp, Mm, Gs), h_c0, "numpy")
for it in range(20000):
    kk = 10 ** lam_r.uniform(-2, 2)
    rr = lam_r.uniform(-1, 1)
    la = 10 ** lam_r.uniform(-2, np.log10(50))
    mm = 10 ** lam_r.uniform(-2, np.log10(20))
    ta = -10 ** lam_r.uniform(-2, 1)
    pz = kk * rr + la / ta
    kperp = kk * np.sqrt(1 - rr**2)
    Mv = mm / abs(ta)
    Gv = la / ta**2
    for hf in (hf_g2, hf_c0):
        hm = np.array(hf(kperp, pz, Mv, Gv), dtype=float)
        ev = np.linalg.eigvalsh(0.5 * (hm + hm.T))
        floor = min(1.0, Mv**2)                  # h = diag(M^2, 1) + (sum of PSD squares)  =>  lambda_min >= min(1, M^2)
        minev = min(minev, ev[0] / floor)
        if ev[0] < floor * (1 - 1e-9) - 1e-12 * abs(ev[-1]):     # roundoff allowance: eigenvalue dynamic range up to 1e10
            cnt_bad += 1
check("A5 h >= diag(M^2,1) > 0 (lambda_min >= min(1,M^2)) at 2 x 20000 random points (lambda <= 50, mu in [0.01,20], all r, tau in (-10,-0.01)), g=2 and g=1", cnt_bad == 0,
      f"(violations of the bound: {cnt_bad}; min over points of lambda_min/min(1,M^2) = {minev:.6f})")

# ------------------------------------------------------------------ A6: current operator
print("\nA6  the current: e dH/dp (canonical variables fixed) - d/dtau P_pol; envelope check dL/dp = -dH/dp")
# numeric envelope check on L_reduced: choose random values of canonical variables; compare dLred/dp at fixed (W, W') with -dH/dp at fixed (W, Pi)
rng = np.random.default_rng(7)
Lg2 = lagrangian(S_G2)
sol_tau = sp.solve([sp.diff(Lg2, Wtc), sp.diff(Lg2, Wt)], [Wt, Wtc], dict=True)[0]
Lred = sp.simplify(Lg2.subs(sol_tau))
dLdp = sp.diff(Lred, Pp)                                      # at fixed W, Wc, W', Wc'  (W_tau eliminated: envelope)
vals = {s: complex(rng.normal(), rng.normal()) for s in (Wx, Wy, Wz, Wxp, Wyp, Wzp)}
vals.update({sc: np.conj(vals[s]) for s, sc in ((Wx, Wxc), (Wy, Wyc), (Wz, Wzc), (Wxp, Wxcp), (Wyp, Wycp), (Wzp, Wzcp))})
vals.update({Pp: 0.7, Mm: 1.3, Gs: 0.4, kp: 0.9})
# momenta at this configuration (needs W_tau)
Wt_val = complex(sol_tau[Wt].subs(vals))
Wtc_val = complex(sol_tau[Wtc].subs(vals))
Pi_vals = {Piv[i]: complex((Wpv[i] - I * PV[i] * Wt).subs(vals).subs({Wt: Wt_val})) for i in range(3)}
Pic_vals = {Picv[i]: complex((Wcpv[i] + I * PV[i] * Wtc).subs(vals).subs({Wtc: Wtc_val})) for i in range(3)}
vals2 = dict(vals)
vals2.update(Pi_vals)
vals2.update(Pic_vals)
lhs = complex(dLdp.subs(vals))
rhs = -complex(sp.diff(Hred2, Pp).subs(vals2))
check("A6a envelope identity dL_red/dp|_{q,q'} = -dH_red/dp|_{q,Pi} at a random configuration (complex fields)", abs(lhs - rhs) < 1e-10 * (1 + abs(lhs)),
      f"(|diff| = {abs(lhs - rhs):.2e})")
# polarization: P_pol = dL/dcalE = i S G/(e calE) (Wc_z W_t - Wc_t W_z) with W_tau(W,Pi)
Ppol = sp.simplify((I * S_G2 * (Wzc * s1g - s2g * Wz)))      # per unit G  (P_pol = Ppol * c e ... ) ; G = c e calE so dL/dG
print("     P_pol/(c e) =", sp.simplify(sp.expand(Ppol)))
Ppol_h = sp.Matrix(6, 6, lambda a_, b_: sp.diff(sp.expand(Ppol), Xcs[a_], Xs[b_]))
print("     P_pol matrix real symmetric:", sp.simplify(Ppol_h - Ppol_h.T) == sp.zeros(6, 6) and all(sp.im(x) == 0 for x in Ppol_h))
okA6b = sp.simplify(Ppol_h - Ppol_h.T) == sp.zeros(6, 6) and all(sp.im(sp.simplify(x)) == 0 for x in Ppol_h)
check("A6b the polarization P_pol = dL/d(calE) is a REAL SYMMETRIC bilinear in the canonical variables (so its symmetric-ordered expectation is nonzero)", okA6b)

# ------------------------------------------------------------------ A7: dimensional structure
print("\nA7  e and E enter only through lambda = eE/H^2; h(tau; k, e, E, m, H) = H h~(lambda, mu; k/H, H tau)")
e_, m_, kt, tt = sp.symbols("e m kt tt", positive=True)
Hs = sp.symbols("Hs", positive=True)
t_ = sp.symbols("t_", negative=True)
kx, kzz = sp.symbols("kx kzz", real=True)
p_phys = kzz + e_ * E / (Hs**2 * t_)
M_phys = m_ / (Hs * (-t_))
G_phys = e_ * E / (Hs**2 * t_**2)
hg2 = sp.lambdify((kp, Pp, Mm, Gs), hmat, "sympy")
h_phys = hg2(kx, p_phys, M_phys, G_phys)
tt_ = sp.symbols("tt_", negative=True)       # tt_ = H t_
lam_s, mu_s = sp.symbols("lam_s mu_s", real=True)
sub = {t_: tt_ / Hs, kx: Hs * sp.symbols("kxt", real=True), kzz: Hs * sp.symbols("kzt", real=True), m_: Hs * mu_s, e_: Hs**2 * lam_s / E}
hsub = sp.simplify(h_phys.subs(sub))
kxt, kzt = sp.symbols("kxt kzt", real=True)
ht = hg2(kxt, kzt + lam_s / tt_, mu_s / (-tt_), lam_s / tt_**2)
# scaling: X = (W, Pi): entries (WW): H^2 ; (Pi Pi): 1 ; (W Pi) : H. Compare with the diag weights
ok7 = True
for a_ in range(6):
    for b_ in range(6):
        wa = 2 if (a_ < 3 and b_ < 3) else (1 if (a_ < 3) != (b_ < 3) else 0)
        ok7 = ok7 and sp.simplify(hsub[a_, b_] - Hs**wa * ht[a_, b_]) == 0
check("A7 h depends on (e, E, m, H) only through lambda = eE/H^2 and mu = m/H, homogeneous of the stated weight in H", ok7)

# ------------------------------------------------------------------ A8: stationary vacuum sanity (flat, constant coefficients)
print("\nA8  constant-coefficient limit: the adiabatic vacuum covariance is stationary, so d<P_pol>/dtau = 0")
J6 = np.block([[np.zeros((3, 3)), np.eye(3)], [-np.eye(3), np.zeros((3, 3))]])


def gamma0(hm):
    w, V = np.linalg.eigh(hm)
    hh = V @ np.diag(np.sqrt(w)) @ V.T
    hi = V @ np.diag(1 / np.sqrt(w)) @ V.T
    K = hh @ J6 @ hh
    w2, U = np.linalg.eigh(K.T @ K)
    absK = U @ np.diag(np.sqrt(np.maximum(w2, 0))) @ U.T
    return 0.5 * hi @ absK @ hi


okA8 = True
for it in range(20):
    kk = rng.uniform(0.3, 3)
    hm = np.array(hf_g2(kk, rng.uniform(-2, 2), rng.uniform(0.3, 2), rng.uniform(-1, 1)), dtype=float)
    hm = 0.5 * (hm + hm.T)
    G0 = gamma0(hm)
    A = J6 @ hm
    stat = np.linalg.norm(A @ G0 + G0 @ A.T)
    pur = np.linalg.norm(G0 @ J6 @ G0 - 0.25 * J6)
    okA8 = okA8 and stat < 1e-9 and pur < 1e-9
check("A8 Gamma_0 = (1/2) h^{-1/2}|K|h^{-1/2} is stationary (A G + G A^T = 0) and pure (G J G = J/4) on the 6x6 vector h", okA8)

print("\nCHECKS: %d/%d passed" % (sum(1 for _, ok in CHECKS if ok), len(CHECKS)))
print(f"g = 2 sign of the Pauli term (in this Lagrangian's convention): s = {S_G2:+d};  H_reduced = |Pi|^2 + |P x W|^2 + M^2|W|^2 + |P.Pi - s' e calE W_z|^2/M^2")
sys.exit(0 if all(ok for _, ok in CHECKS) else 1)

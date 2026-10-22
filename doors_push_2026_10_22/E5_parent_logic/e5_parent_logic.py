"""E5_parent_logic: hostile audit of the "no covariant parent" no-gos against the SCREENED theory (PAPER49 action WITH
stiffness gamma = K L*^2/2).  Criteria: FROZEN_CRITERIA.md (committed alone first, 039c76d2f9).
Part A: NG1 saddle with the stiffness (linear response about AG6C's deep two-body AQUAL solution; solver copied verbatim
        from argon_push/AG6C_relativistic_completion/ag6c_s0_saddle.py lines 58-208, read-only reuse).
Part B: sympy checks E1, T1, N1, N2, G1-G4; G5 reads campaign_fresh_gravity/CFG944_*/cfg944_results.json.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 e5_parent_logic.py      (E5_MUTATE=1 for the mutate run)
kappa = 1/2 FITTED.  Not theory closed.
"""
import json
import math
import os
import sys
import time

import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla
import sympy as sp

MUT = os.environ.get("E5_MUTATE", "") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SUF = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"e5_parent_logic{SUF}.out"), "w")
RES = {"lane": "E5_parent_logic", "criteria_commit": "039c76d2f9", "mutate": MUT, "checks": {}, "numbers": {}}
T0 = time.time()
NPASS = [0, 0]


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.write(s + "\n")
    OUT.flush()


def check(name, ok, value, threshold):
    NPASS[1] += 1
    NPASS[0] += bool(ok)
    P(f"{name} {'PASS' if ok else 'FAIL'} {value} {threshold}")
    RES["checks"][name] = dict(ok=bool(ok), value=str(value), threshold=str(threshold))


# ------------------------------------------------------------------ constants (sources in FROZEN_CRITERIA / AG6C)
G = 6.6743e-11
MSUN = 1.98847e30
PC = 3.0856775814913673e16
MPC = 1e6 * PC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FID = {"F1_MW-M31": dict(M=8e10 * MSUN, d=0.77 * MPC), "F2_cluster_pair": dict(M=2e13 * MSUN, d=5.0 * MPC)}
LSTAR_PC = [24.0, 90.0, 1000.0]
LMUT = 1000.0 if MUT else 1.0          # mutate (i): L* x 1000 in S3/S4

# ------------------------------------------------------------------ grid
def make_faces(xmax, refs, rate=0.06):
    """faces from 0 to xmax; local spacing h(x) = min_k (h_k + rate |x - c_k|)."""
    xs = [0.0]
    while xs[-1] < xmax:
        x = xs[-1]
        h = min(hk + rate * abs(x - ck) for ck, hk in refs)
        xs.append(x + h)
    xs[-1] = xmax if xs[-1] - xmax < 0.5 * (xs[-1] - xs[-2]) else xs[-1]
    return np.array(xs)


class Grid:
    def __init__(self, Rf, zf):
        self.Rf, self.zf = Rf, zf
        self.Rc = 0.5 * (Rf[1:] + Rf[:-1])
        self.zc = 0.5 * (zf[1:] + zf[:-1])
        self.dR = np.diff(Rf)
        self.dz = np.diff(zf)
        self.NR, self.NZ = len(self.Rc), len(self.zc)
        self.N = self.NR * self.NZ
        self.RR, self.ZZ = np.meshgrid(self.Rc, self.zc, indexing="ij")
        self.V = np.outer(math.pi * (Rf[1:] ** 2 - Rf[:-1] ** 2), self.dz)
        self.idx = np.arange(self.N).reshape(self.NR, self.NZ)


def cell_grad(g, Phi, phib_R, phib_z):
    """central-difference gradient at cell centres (one-sided/BC-aware at the edges)."""
    NR, NZ = g.NR, g.NZ
    dPR = np.zeros_like(Phi)
    dPz = np.zeros_like(Phi)
    # R direction
    dPR[1:-1, :] = (Phi[2:, :] - Phi[:-2, :]) / (g.Rc[2:, None] - g.Rc[:-2, None])
    dPR[0, :] = (Phi[1, :] - Phi[0, :]) / (g.Rc[1] + g.Rc[0])   # mirror ghost (odd derivative); first run had a 2/3 error
    dPR[-1, :] = (phib_R - Phi[-2, :]) / (g.Rf[-1] - g.Rc[-2])
    # z direction
    dPz[:, 1:-1] = (Phi[:, 2:] - Phi[:, :-2]) / (g.zc[None, 2:] - g.zc[None, :-2])
    dPz[:, 0] = (Phi[:, 1] - Phi[:, 0]) / (g.zc[1] + g.zc[0])   # mirror ghost (odd derivative); first run had a 2/3 error
    dPz[:, -1] = (phib_z - Phi[:, -2]) / (g.zf[-1] - g.zc[-2])
    return dPR, dPz


def face_coeffs(g, Phi, phib_R, phib_z, mufun):
    """mu at R-faces (interior NR-1 x NZ, plus outer NZ) and z-faces (NR x NZ-1, plus outer NR)."""
    dPR, dPz = cell_grad(g, Phi, phib_R, phib_z)
    # interior R faces
    nR = (Phi[1:, :] - Phi[:-1, :]) / (g.Rc[1:, None] - g.Rc[:-1, None])
    tR = 0.5 * (dPz[1:, :] + dPz[:-1, :])
    muR = mufun(np.sqrt(nR ** 2 + tR ** 2))
    # outer R face (Dirichlet)
    nRo = (phib_R - Phi[-1, :]) / (g.Rf[-1] - g.Rc[-1])
    muRo = mufun(np.sqrt(nRo ** 2 + dPz[-1, :] ** 2))
    nz = (Phi[:, 1:] - Phi[:, :-1]) / (g.zc[None, 1:] - g.zc[None, :-1])
    tz = 0.5 * (dPR[:, 1:] + dPR[:, :-1])
    muz = mufun(np.sqrt(nz ** 2 + tz ** 2))
    nzo = (phib_z - Phi[:, -1]) / (g.zf[-1] - g.zc[-1])
    muzo = mufun(np.sqrt(nzo ** 2 + dPR[:, -1] ** 2))
    return muR, muRo, muz, muzo


def assemble(g, muR, muRo, muz, muzo, phib_R, phib_z):
    rows, cols, vals = [], [], []
    b = np.zeros(g.N)
    diag = np.zeros(g.N)
    I = g.idx
    # interior R faces
    AR = 2 * math.pi * g.Rf[1:-1, None] * g.dz[None, :]
    cR = muR * AR / (g.Rc[1:, None] - g.Rc[:-1, None])
    a, bb = I[:-1, :].ravel(), I[1:, :].ravel()
    c = cR.ravel()
    rows += [a, bb]
    cols += [bb, a]
    vals += [c, c]
    np.add.at(diag, a, -c)
    np.add.at(diag, bb, -c)
    # outer R boundary
    ARo = 2 * math.pi * g.Rf[-1] * g.dz
    cRo = muRo * ARo / (g.Rf[-1] - g.Rc[-1])
    ii = I[-1, :]
    np.add.at(diag, ii, -cRo)
    b[ii] -= cRo * phib_R
    # interior z faces
    Az = math.pi * (g.Rf[1:] ** 2 - g.Rf[:-1] ** 2)[:, None] * np.ones((1, g.NZ - 1))
    cz = muz * Az / (g.zc[None, 1:] - g.zc[None, :-1])
    a, bb = I[:, :-1].ravel(), I[:, 1:].ravel()
    c = cz.ravel()
    rows += [a, bb]
    cols += [bb, a]
    vals += [c, c]
    np.add.at(diag, a, -c)
    np.add.at(diag, bb, -c)
    # outer z boundary
    Azo = math.pi * (g.Rf[1:] ** 2 - g.Rf[:-1] ** 2)
    czo = muzo * Azo / (g.zf[-1] - g.zc[-1])
    ii = I[:, -1]
    np.add.at(diag, ii, -czo)
    b[ii] -= czo * phib_z
    rows.append(np.arange(g.N))
    cols.append(np.arange(g.N))
    vals.append(diag)
    A = sps.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(g.N, g.N))
    return A, b


def plummer_mass(g, zpos, b, mtot):
    """cell masses of Plummer spheres at (R=0, z=zpos) (list), normalised to mtot on the half-domain."""
    rho = np.zeros((g.NR, g.NZ))
    for zp in zpos:
        r2 = g.RR ** 2 + (g.ZZ - zp) ** 2
        rho += (3 / (4 * math.pi * b ** 3)) * (1 + r2 / b ** 2) ** (-2.5)
    m = rho * g.V
    m *= mtot / m.sum()
    return m


def solve(g, mcell, mufun, phib_fun, it_max=400, tol=1e-10, label=""):
    Rb = np.sqrt(g.Rf[-1] ** 2 + g.zc ** 2)
    zb = np.sqrt(g.Rc ** 2 + g.zf[-1] ** 2)
    phib_R, phib_z = phib_fun(Rb), phib_fun(zb)
    rhs = 4 * math.pi * mcell.ravel()                      # 4 pi G rho V, G = 1
    # initial guess: the far-field form evaluated at each cell (smooth, roughly right)
    r = np.sqrt(g.RR ** 2 + g.ZZ ** 2) + 1e-3
    Phi = phib_fun(r)
    muR, muRo, muz, muzo = face_coeffs(g, Phi, phib_R, phib_z, mufun)
    hist = []
    for it in range(it_max):
        A, b = assemble(g, muR, muRo, muz, muzo, phib_R, phib_z)
        Phin = spla.spsolve(A.tocsc(), rhs + b).reshape(g.NR, g.NZ)
        dphi = np.max(np.abs(Phin - Phi)) / (np.max(Phin) - np.min(Phin))
        Phi = Phin
        nmuR, nmuRo, nmuz, nmuzo = face_coeffs(g, Phi, phib_R, phib_z, mufun)
        muR, muRo, muz, muzo = (np.sqrt(muR * nmuR), np.sqrt(muRo * nmuRo), np.sqrt(muz * nmuz), np.sqrt(muzo * nmuzo))
        hist.append(dphi)
        if dphi < tol and it > 3:
            break
    # final consistency residual with mu evaluated on the final Phi
    muR, muRo, muz, muzo = face_coeffs(g, Phi, phib_R, phib_z, mufun)
    A, b = assemble(g, muR, muRo, muz, muzo, phib_R, phib_z)
    resid = np.max(np.abs(A @ Phi.ravel() - b - rhs)) / np.max(np.abs(rhs))
    P(f"  [{label}] N = {g.N} ({g.NR} x {g.NZ}), iterations {it + 1}, last dPhi {hist[-1]:.2e}, "
      f"residual/max(rhs) {resid:.2e}, t = {time.time() - T0:.1f} s")
    return Phi, phib_R, phib_z, resid, it + 1


def laplacian(g, Phi, phib_R, phib_z):
    """FV Laplacian (mu = 1) per unit volume."""
    one = lambda x: np.ones_like(x)
    muR, muRo, muz, muzo = face_coeffs(g, Phi, phib_R, phib_z, one)
    A, b = assemble(g, muR, muRo, muz, muzo, phib_R, phib_z)
    return ((A @ Phi.ravel() - b).reshape(g.NR, g.NZ)) / g.V



# ================================================================== PART A: saddle with stiffness
P("E5_parent_logic" + ("  [MUTATE: L* x 1000 in S3/S4; G2(b) stiffness sign flipped]" if MUT else ""))
P("\nPart A: NG1 at the two-body saddle WITH the stiffness (linear response about AG6C's deep AQUAL solution)")
deep_mu = lambda x: np.maximum(x, 1e-12)
HF, bsoft = 0.0025, 0.01
Rf = make_faces(60.0, [(0.0, HF)])
zf = make_faces(60.0, [(0.0, HF), (0.5, HF)])
g2 = Grid(Rf, zf)
m2 = plummer_mass(g2, [0.5, -0.5], bsoft, 1.0)
phib0 = lambda r: math.sqrt(2.0) * np.log(r)
Phi0, pbR0, pbz0, _, _ = solve(g2, m2, deep_mu, phib0, label="pair deep, gamma = 0")
C0 = laplacian(g2, Phi0, pbR0, pbz0) / (4 * math.pi) - m2 / g2.V
row0 = C0[:, 0]
Cref = {0.1: -0.40432, 0.2: -0.24012, 0.3: -0.11399}
Cfix = {R: float(np.interp(R, g2.Rc, row0)) for R in Cref}
mask20 = g2.Rc < 20
S_neg = 2 * np.sum(np.minimum(row0, 0) * g2.dR * mask20)
dev = max([abs(Cfix[R] / Cref[R] - 1) for R in Cref] + [abs(S_neg / -0.20640 - 1)])
check("K0", dev <= 0.01, f"maxdev={dev:.2e} (C(0.1,0.2,0.3)={Cfix[0.1]:+.5f},{Cfix[0.2]:+.5f},{Cfix[0.3]:+.5f}; col={S_neg:+.5f})",
      "<=0.01")
RES["numbers"]["C0_midplane"] = Cfix
RES["numbers"]["neg_column"] = S_neg

# Laplacian of C0 (source shape), Dirichlet 0 at the outer boundary (C0 ~ 1e-4 there; source masked to r < 20 anyway)
lapC = laplacian(g2, C0, np.zeros(g2.NZ), np.zeros(g2.NR))
r_up = np.sqrt(g2.RR ** 2 + (g2.ZZ - 0.5) ** 2)
r_dn = np.sqrt(g2.RR ** 2 + (g2.ZZ + 0.5) ** 2)
r_or = np.sqrt(g2.RR ** 2 + g2.ZZ ** 2)


def response(lam, rcut):
    """deep AQUAL with extra source (lam/2) lap C0 outside rcut of each mass; returns delta C on the mid-plane radii."""
    src = 0.5 * lam * lapC * ((r_up > rcut) & (r_dn > rcut) & (r_or < 20))
    madd = src * g2.V
    mtot_half = 1.0 + madd.sum()
    phib = lambda r: math.sqrt(2.0 * mtot_half) * np.log(r)
    Phi, pbR, pbz, _, _ = solve(g2, m2 + madd, deep_mu, phib, label=f"pair deep, stiff lam={lam:g} rcut={rcut}")
    C = laplacian(g2, Phi, pbR, pbz) / (4 * math.pi) - m2 / g2.V      # phantom = lap Phi / K - rho_b (added source excluded)
    d = C[:, 0] - row0
    out = {R: float(np.interp(R, g2.Rc, d)) / lam for R in Cref}
    out["col"] = float(2 * np.sum(np.minimum(C[:, 0], 0) * g2.dR * mask20) - S_neg) / lam
    return out, float(madd.sum())


C1 = {}
for lam_set in ([1e-5, 2e-5], [1e-6, 2e-6]):
    C1 = {}
    for rc in (0.05, 0.1):
        C1[rc] = [response(l, rc) for l in lam_set]
    lin = max(abs(C1[rc][0][0][R] / C1[rc][1][0][R] - 1) for rc in C1 for R in Cref)
    P(f"  lam_num {lam_set}: linearity max deviation {lin:.3e}")
    if lin <= 0.05:
        break
RES["numbers"]["lam_num"] = lam_set
for rc in C1:
    P(f"  r_cut {rc}: C1(R) = " + ", ".join(f"{R}: {C1[rc][0][0][R]:+.4e}" for R in Cref)
      + f";  net added half-mass at lam={lam_set[0]:g}: {C1[rc][0][1]:+.3e}")
RES["numbers"]["C1"] = {str(rc): {str(R): C1[rc][0][0][R] for R in list(Cref) + ["col"]} for rc in C1}
P(f"  [REPORTED, A1] negative-column response per unit lam (r_cut 0.1): {C1[0.1][0][0]['col']:+.4e} (column {S_neg:+.5f})")
check("S1", lin <= 0.05, f"{lin:.3e}", "<=0.05")
s2 = abs(C1[0.05][0][0][0.2] / C1[0.1][0][0][0.2] - 1)
check("S2", s2 <= 0.20, f"{s2:.3e}", "<=0.20")
C1_02 = C1[0.1][0][0][0.2]
sign_word = "reduces" if C1_02 > 0 else "deepens"
P(f"  stiffness {sign_word} the trough at R = 0.2 d (C1 = {C1_02:+.4e}, C0 = {Cfix[0.2]:+.5f})")

# mid-plane field for the core estimate
dPR, dPz = cell_grad(g2, Phi0, pbR0, pbz0)
ghat_mid = np.sqrt(dPR[:, 0] ** 2 + dPz[:, 0] ** 2)

s3_ok, s4_ok = True, True
fid_out = {}
for fname, fp in FID.items():
    for fo, a0 in A0.items():
        rM = math.sqrt(G * fp["M"] / a0)
        eps = rM / fp["d"]
        for Ls in LSTAR_PC:
            L = Ls * PC * LMUT
            lam = L ** 2 / (rM * fp["d"])
            rel = lam * C1_02 / Cfix[0.2]
            relcol = lam * C1[0.1][0][0]["col"] / S_neg
            Lhat = L / fp["d"]
            ell = Lhat / np.sqrt(2 * eps * np.maximum(ghat_mid, 1e-300))
            sel = (g2.Rc < 0.5) & (ell >= g2.Rc)
            Rcore = float(g2.Rc[sel].max()) if sel.any() else 0.0
            u_02 = eps * float(np.interp(0.2, g2.Rc, ghat_mid))
            ell02_kpc = L * math.sqrt(1 / (2 * u_02)) / (1e3 * PC)
            key = f"{fname}_{fo}_L{Ls:g}pc"
            fid_out[key] = dict(rM_kpc=rM / (1e3 * PC), eps=eps, lam=lam, dC_over_C_R02=rel, dcol_over_col=relcol, R_core_over_d=Rcore,
                                u_over_a0_R02=u_02, ell_perp_R02_kpc=ell02_kpc)
            P(f"  {key:32s}: r_M/d={eps:.4f} lam={lam:.3e} dC/C(0.2d)={rel:+.3e} dcol/col={relcol:+.3e} R_core/d={Rcore:.4f} "
              f"u/a0(0.2d)={u_02:.3e} ell_perp(0.2d)={ell02_kpc:.3g} kpc")
            if Ls <= 90:
                s3_ok &= abs(rel) <= 0.1
                s4_ok &= Rcore < 0.1
        Lcrit = math.sqrt(-Cfix[0.2] / C1_02 * rM * fp["d"]) / PC if C1_02 > 0 else float("nan")
        fid_out[f"{fname}_{fo}_Lcrit_pc"] = Lcrit
        ccol = C1[0.1][0][0]["col"]
        Lcol = math.sqrt(-S_neg / ccol * rM * fp["d"]) / PC if ccol > 0 else float("nan")
        fid_out[f"{fname}_{fo}_Lcrit_column_pc"] = Lcol
        P(f"  [REPORTED, A1] {fname}_{fo}: first-order L* at which the negative column would be filled = {Lcol:.4g} pc")
        P(f"  {fname}_{fo}: first-order L*_crit (trough at 0.2d removed) = {Lcrit:.4g} pc"
          + ("" if C1_02 > 0 else " (n/a: stiffness deepens)"))
RES["numbers"]["fiducials"] = fid_out
check("S3", s3_ok, "max|dC/C| at L*<=90pc = " + f"{max(abs(v['dC_over_C_R02']) for k, v in fid_out.items() if isinstance(v, dict) and ('L24pc' in k or 'L90pc' in k)):.3e}", "<=0.1 all 8")
check("S4", s4_ok, "max R_core/d at L*<=90pc = " + f"{max(v['R_core_over_d'] for k, v in fid_out.items() if isinstance(v, dict) and ('L24pc' in k or 'L90pc' in k)):.4f}", "<0.1")

# ================================================================== PART B: sympy
P("\nPart B: sympy")
# ---- E1: linearised stiffened static system
u, g, a0, K, k, L = sp.symbols("u g a0 K k L", positive=True)
Dfull = a0 * u / (a0 - u)
u_of_g = a0 * g / (a0 + g)
mu = g / (a0 + g)
Mpar = K * sp.diff(Dfull, u)
Mperp = K * Dfull / u
gam = K * L ** 2 / 2
Apar = sp.simplify((1 - K / Mpar).subs(u, u_of_g) - sp.diff(mu * g, g))
Aperp = sp.simplify((1 - K / Mperp).subs(u, u_of_g) - mu)
Apar_k = 1 - K / (Mpar + gam * k ** 2)
Aperp_k = 1 - K / (Mperp + gam * k ** 2)
ser_par = sp.simplify(sp.series(sp.series(Apar_k, u, 0, 2).removeO(), k, 0, 3).removeO() - (2 * u / a0 + L ** 2 * k ** 2 / 2))
ser_perp = sp.simplify(sp.series(sp.series(Aperp_k, u, 0, 2).removeO(), k, 0, 3).removeO() - (u / a0 + L ** 2 * k ** 2 / 2))
x, y, z = sp.symbols("x y z")
Pv = [sp.Function(f"P{i}")(x, y, z) for i in range(3)]
lapv = [sum(sp.diff(Pi, c, 2) for c in (x, y, z)) for Pi in Pv]
divlap = sum(sp.diff(lapv[i], c) for i, c in enumerate((x, y, z)))
lapdiv = sum(sp.diff(sum(sp.diff(Pv[i], c) for i, c in enumerate((x, y, z))), cc, 2) for cc in (x, y, z))
vec_id = sp.simplify(divlap - lapdiv)
e1 = [Apar, Aperp, ser_par, ser_perp, vec_id]
check("E1", all(sp.simplify(t) == 0 for t in e1), f"residuals={[str(sp.simplify(t)) for t in e1]}", "all 0")
e1b = [sp.simplify(ser_par + 2 * L ** 2 * k ** 2 * u / a0), sp.simplify(ser_perp + L ** 2 * k ** 2 * u / a0)]
check("E1b", all(t == 0 for t in e1b) and all(sp.simplify(t) == 0 for t in (Apar, Aperp, vec_id)),
      f"series residuals minus cross terms (-2,-1) L^2 k^2 u/a0: {e1b}; A_par, A_perp, vector identity 0  [A1, post hoc]",
      "all 0")

# ---- T1: D-T with stiffness
rho0, c2, om2, xi = sp.symbols("rho0 c2 omega2 xi")
drho = -rho0 * sp.I * k * xi
Phi_k = -K * drho / k ** 2
force = -sp.I * k * Phi_k * (1 - c2) - gam * sp.I * k * drho     # per unit mass: -grad Phi_self (1 - c2) - gamma grad(drho)
om2_sol = sp.simplify(-force / xi)
t1a = sp.simplify(om2_sol - (gam * rho0 * k ** 2 + (c2 - 1) * K * rho0))
gN = g ** 2 / (g + a0)
Fu = sp.simplify((g).subs(g, sp.solve(sp.Eq(g - u, gN), g)[0]))   # F(u) = g on the law with g = g_N + u
t1b = sp.simplify(Fu - Dfull)
t1c = sp.series(Fu, u, 0, 2).removeO().coeff(u, 1) - 1
check("T1", t1a == 0 and t1b == 0 and t1c == 0, f"om2-[gamma rho k^2+(c2-1)K rho]={t1a}; F(u)-D_full={t1b}; c2-1={t1c}",
      "all 0")

# ---- N1: NG2 = positivity sign
X, LX, LXX, s = sp.symbols("X L_X L_XX s", positive=True)
v2 = LX / (LX + 2 * X * LXX)
n1a = sp.simplify(v2 - 1 - (-2 * X * LXX / (LX + 2 * X * LXX)))
Xs = sp.symbols("Xs", positive=True)
sfun = sp.sqrt(2 * Xs) / a0
Ld = a0 ** 2 / K * (sfun - sp.log(1 + sfun))
LdX = sp.diff(Ld, Xs)
LdXX = sp.diff(Ld, Xs, 2)
LdXX_s = sp.simplify(LdXX.subs(Xs, a0 ** 2 * s ** 2 / 2))
v2_law = sp.simplify((LdX / (LdX + 2 * Xs * LdXX)).subs(Xs, a0 ** 2 * s ** 2 / 2))
n1b = sp.simplify(v2_law - (1 + s))
neg = sp.simplify(-LdXX_s)
neg_ok = all(float(neg.subs({s: sv, a0: 1, K: 1})) > 0 for sv in (1e-6, 1e-3, 0.1, 1, 10, 1e3, 1e6))
check("N1", n1a == 0 and n1b == 0 and neg_ok, f"v2-1 identity={n1a}; v2_law-(1+g/a0)={n1b}; L_XX(law)={LdXX_s} <0: {neg_ok}",
      "0, 0, True")
RES["numbers"]["L_XX_law"] = str(LdXX_s)

# ---- N2: dark-sector curl stiffness, X mode
epar, Nperp, gs, w = sp.symbols("epsilon_par N_perp gamma_s omega", positive=True)
# (i) canonical: H2 = 1/2 (1/epar + gs k^2) dD^2 + 1/2 Nperp k^2 dA^2 ; dA' = -dH/dD... frequency^2 = product of the two stiffnesses
Hmat = sp.Matrix([[1 / epar + gs * k ** 2, 0], [0, Nperp * k ** 2]])
w2_i = sp.simplify(Hmat[0, 0] * Hmat[1, 1])
v2_i = sp.simplify(w2_i / k ** 2)
n2a = sp.simplify(v2_i - Nperp * (1 / epar + gs * k ** 2))
# (ii) local Lagrangian: L2 = 1/2 epar w^2 A^2 - 1/2 Nperp k^2 A^2 - gs/2 k^2 (epar w A)^2
kin = sp.diff(sp.Rational(1, 2) * epar * w ** 2 - sp.Rational(1, 2) * gs * k ** 2 * epar ** 2 * w ** 2, w, 2)
n2b = sp.simplify(kin - epar * (1 - gs * epar * k ** 2))
v2_ii = sp.simplify(Nperp / (epar * (1 - gs * epar * k ** 2)))
lim_i = sp.limit(v2_i, k, 0) - Nperp / epar
lim_ii = sp.limit(v2_ii, k, 0) - Nperp / epar
mono = sp.simplify(sp.diff(v2_i, k)) , sp.simplify(sp.diff(v2_ii, k))
mono_ok = all(float(m.subs({epar: 0.5, Nperp: 1, gs: 0.3, k: 0.7})) > 0 for m in mono)
check("N2", n2a == 0 and n2b == 0 and lim_i == 0 and lim_ii == 0 and mono_ok,
      f"v2_i-N(1/e+gs k^2)={n2a}; kin-e(1-gs e k^2)={n2b}; k->0 limits {lim_i},{lim_ii}; dv2/dk>0 both: {mono_ok}",
      "0,0,0,0,True")

# ---- G1: kinetic coefficient independent of any xi-dot-free stiffness
tt, xx = sp.symbols("t x", real=True)
a_ = sp.Function("a")(tt)
Fthth, gst, c4 = sp.symbols("F_thth gamma_st c4", real=True)
xi_f = a_ * sp.cos(k * xx)
theta = sp.diff(xi_f, tt, xx)
Lag = sp.Rational(1, 2) * rho0 * sp.diff(xi_f, tt) ** 2 + sp.Rational(1, 2) * Fthth * theta ** 2 \
    - sp.Rational(1, 2) * gst * sp.diff(xi_f, xx, 2) ** 2 - sp.Rational(1, 2) * c4 * sp.diff(xi_f, xx, 3) ** 2
Lbar = sp.integrate(Lag, (xx, 0, 2 * sp.pi / k)) * k / (2 * sp.pi)
ad = sp.Symbol("adot")
Lbar = Lbar.subs(sp.Derivative(a_, tt), ad)
kincoef = sp.simplify(2 * sp.diff(Lbar, ad, 2))
g1 = sp.simplify(kincoef - (rho0 + Fthth * k ** 2))
check("G1", g1 == 0 and not kincoef.has(gst) and not kincoef.has(c4), f"kinetic coef={kincoef}", "rho0+F_thth k^2, no gamma")

# ---- G2: covariant tidal stiffness, Hessian vs iterated reading (flat space, linear order)
t, X1, X2, X3, ep, cdot = sp.symbols("t X1 X2 X3 epsilon chidot", real=True)
co = [t, X1, X2, X3]
eta = sp.diag(-1, 1, 1, 1)
dchi = sp.Function("dchi")(t, X1, X2, X3)
vv = [sp.Function(f"v{i}")(t, X1, X2, X3) for i in (1, 2, 3)]
chi = cdot * t + ep * dchi
uU = sp.Matrix([1] + [ep * vi for vi in vv])
uD = eta * uU
h_mixed = sp.Matrix(4, 4, lambda m, n: (1 if m == n else 0) + uD[m] * uU[n])   # h_m^n
dchi_v = [sp.diff(chi, c) for c in co]
hess = sp.Matrix(4, 4, lambda a, b: sp.diff(chi, co[a], co[b]))
tauA = sp.Matrix(3, 3, lambda i, j: sum(h_mixed[i + 1, a] * h_mixed[j + 1, b] * hess[a, b] for a in range(4) for b in range(4)))
proj_grad = [sum(h_mixed[m, n] * dchi_v[n] for n in range(4)) for m in range(4)]
tauB = sp.Matrix(3, 3, lambda i, j: sum(h_mixed[j + 1, a] * sp.diff(proj_grad[i + 1], co[a]) for a in range(4)))
lin = lambda M: M.applyfunc(lambda e: sp.expand(e).coeff(ep, 1))
tA, tB = lin(tauA), lin(tauB)
hessd = sp.Matrix(3, 3, lambda i, j: sp.diff(dchi, co[i + 1], co[j + 1]))
gA = sp.simplify(tA - hessd)
gB = sp.simplify(tB - hessd - cdot * sp.Matrix(3, 3, lambda i, j: sp.diff(vv[i], co[j + 1])))
# longitudinal plane wave: v = adot khat cos(k.x) along X1; traceless part squared, coefficient of adot^2 k^2
sgn = -1 if MUT else 1
kk = sp.symbols("kk", positive=True)
grad_v = sp.zeros(3, 3)
grad_v[0, 0] = 1                     # dv1/dX1 per unit (k adot); traceless projector of khat khat
TL = grad_v - sp.eye(3) * grad_v.trace() / 3
tau2_coef = sum(TL[i, j] ** 2 for i in range(3) for j in range(3))      # = 2/3
# L ⊃ -(3 gamma/4K^2) tau^2  with tau ⊃ chidot * sigma, sigma^2 = (2/3) theta^2  -> F_thth^stiff
Fst = sp.simplify(2 * (-sgn * sp.Rational(3, 4) * gam / K ** 2 * cdot ** 2 * tau2_coef))
H, rhob, Om = sp.symbols("H rhobar Omega_c", positive=True)
Fst_frw = sp.simplify(Fst.subs(cdot, -K * rhob / (3 * H)))
kg2L2 = sp.simplify((rhob / (-Fst_frw) * L ** 2).subs(rhob, sp.Rational(3, 2) * Om * H ** 2 / K)) if not MUT else sp.nan
kgL = {lab: float(sp.sqrt(kg2L2.subs(Om, val))) for lab, val in (("Omega_c=0.264 (today)", 0.264), ("EdS medium share 0.843", 5.3643 / 6.3643))} if not MUT else {}
g2ok = (gA == sp.zeros(3, 3)) and (gB == sp.zeros(3, 3)) and sp.simplify(tau2_coef - sp.Rational(2, 3)) == 0 and \
    bool((Fst.subs({K: 1, L: 1, cdot: 1})) <= 0)
check("G2", g2ok, f"(a) Hessian: tau-hess(dchi)={'0' if gA == sp.zeros(3, 3) else gA}; (b) iterated: tau-hess-chidot*grad v="
      f"{'0' if gB == sp.zeros(3, 3) else gB}; F_thth^stiff(b)={Fst}; FRW k_g L*^2={kg2L2}; k_g L*={kgL}", "(a) 0 (b) <=0")
RES["numbers"]["G2"] = dict(F_thth_stiff_b=str(Fst), F_thth_frw=str(Fst_frw), kg2_L2=str(kg2L2), kgL=kgL)

# ---- G3: Theorem G' (by construction; low weight)
th, thT, al, be, Wst, Sst, L00 = sp.symbols("theta theta_T alpha beta W_star S_star L00", real=True)
# convexity tangent inequality f(0) >= f(thT) - thT f'(thT) = T(0); static law f(0) = L00 - W* - S*
Bmin = sp.simplify(L00 - (L00 - Wst - Sst))     # B = L00 - T(0) >= L00 - f(0)
rng = np.random.default_rng(5)
viol = 0
for _ in range(200):
    c = rng.uniform(0.01, 3, 3)
    f = lambda q: c[0] * q ** 2 + c[1] * q ** 4 + c[2] * math.cosh(q) - 1.7 * q       # convex
    fp = lambda q: 2 * c[0] * q + 4 * c[1] * q ** 3 + c[2] * math.sinh(q) - 1.7
    qT = rng.uniform(0.1, 3)
    viol += f(0) < f(qT) - qT * fp(qT) - 1e-12
check("G3", sp.simplify(Bmin - (Wst + Sst)) == 0 and viol == 0, f"B_min=W*+S*: {Bmin}; tangent violations {viol}/200",
      "W*+S*, 0 (by construction)")

# ---- G4: gating the stiffness too
spp, Wg, Sg = sp.symbols("s2p W S", positive=True)
kg_only = sp.sqrt(rho0 / (spp * Wg))
kg_both = sp.sqrt(rho0 / (spp * (Wg + Sg)))
g4 = sp.simplify(kg_both / kg_only - sp.sqrt(Wg / (Wg + Sg)))
check("G4", g4 == 0, f"k_g ratio - sqrt(W/(W+S)) = {g4}", "0")

# ---- G5: parameter-free u-gate u_c = a0 vs CFG944 C4 window
cj = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG944_gated_tether_ghost_cure", "cfg944_results.json")))
g5 = {}
ok5 = True
for fo in ("canonical", "alt"):
    ue = cj["C4"][fo]["u_e"]
    ua = cj["C4"][fo]["u_amp"]
    outside = (1.0 > ue["1.0"]) and (1.0 < ua)
    g5[fo] = dict(slip_max_frozen=ue["5.0"], slip_max_abs=ue["1.0"], camp_min=ua, uc_a0_outside=outside)
    ok5 &= outside
RES["numbers"]["G5"] = g5
check("G5", ok5, json.dumps(g5), "u_c=a0 outside [c-amp min, slip max] both footings")

P(f"\nrun time {time.time() - T0:.1f} s")
try:
    import resource
    RES["peak_rss_GB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
except Exception:
    pass
P(f"E5_PARENT_LOGIC COMPLETE: {NPASS[0]}/{NPASS[1]} checks PASS.")
json.dump(RES, open(os.path.join(HERE, f"e5_parent_logic_results{SUF}.json"), "w"), indent=1, default=str)
OUT.close()
sys.exit(0 if NPASS[0] == NPASS[1] else 1)

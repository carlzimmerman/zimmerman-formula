#!/usr/bin/env python3
"""WT-09: stiffness terms with gravitational waves at exactly c that keep the static L* stiffness.

Criteria: FROZEN_CRITERIA.md (8812ac0477), committed alone before this script existed.
Run:      OMP_NUM_THREADS=1 nice -n 10 python3 wt09.py            -> wt09.out, wt09_results.json   (exit 0 iff K1-K6 pass)
          WT09_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 wt09.py -> *_MUTATE                   (exit 1 iff MU1-MU5 bite)
One process, sympy + numpy/scipy. In-script guard: exit 75 above 0.9 GB RSS; when a 1024^3 PM job is live, exit 75 if swap
grows > 1 GB or free+inactive < 8 GB. kappa = 1/2 FITTED; footings never pooled; not 'theory closed'.
Units: c = 1, K = 4 pi G, x^0 = t in the algebra; SI restored for numbers (geometric: lengths in m, chi/c^2).
"""
import os, sys, json, math, time, re, subprocess, threading, resource, random
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp
from scipy.interpolate import CubicSpline

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUT = os.environ.get("WT09_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUT else ""
OUT_PATH = os.path.join(HERE, f"wt09{SUF}.out")
JSON_PATH = os.path.join(HERE, f"wt09_results{SUF}.json")
_f = open(OUT_PATH, "w", encoding="utf-8")
_lock = threading.Lock()
T0 = time.time()


def P(*a):
    s = " ".join(str(v) for v in a)
    with _lock:
        print(s, flush=True)
        _f.write(s + "\n")
        _f.flush()


# ============================================================================================== guards (coordinator limits)
RSS_CAP = 0.9e9


def rss_bytes():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r if sys.platform == "darwin" else r * 1024


def _ps():
    try:
        return subprocess.run(["ps", "-axo", "command="], capture_output=True, text=True, timeout=10).stdout.splitlines()
    except Exception:
        return []


def pm_live():
    return any("_pm.py" in l and "grep" not in l for l in _ps())


def other_wt():
    return sum(1 for l in _ps() if re.search(r"python[0-9.]*\s+\S*wt0\d\S*\.py", l) and "wt09.py" not in l)


def swap_used():
    try:
        s = subprocess.run(["sysctl", "-n", "vm.swapusage"], capture_output=True, text=True, timeout=10).stdout
        m = re.search(r"used = ([0-9.]+)([MG])", s)
        return float(m.group(1)) * (1e6 if m.group(2) == "M" else 1e9)
    except Exception:
        return 0.0


def free_inactive():
    try:
        s = subprocess.run(["vm_stat"], capture_output=True, text=True, timeout=10).stdout
        ps = int(re.search(r"page size of (\d+)", s).group(1))
        fr = int(re.search(r"Pages free:\s+(\d+)", s).group(1))
        ina = int(re.search(r"Pages inactive:\s+(\d+)", s).group(1))
        return (fr + ina) * ps
    except Exception:
        return 1e12


SWAP0 = swap_used()


def _watch():
    while True:
        time.sleep(2.0)
        if rss_bytes() > RSS_CAP:
            P(f"GUARD: peak RSS {rss_bytes()/1e9:.2f} GB > 0.9 GB -> exit 75"); os._exit(75)
        if pm_live():
            su, fi = swap_used(), free_inactive()
            if su - SWAP0 > 1e9 or fi < 8e9:
                P(f"GUARD: 1024^3 PM job live and swap +{(su-SWAP0)/1e9:.2f} GB / free+inactive {fi/1e9:.1f} GB -> exit 75")
                os._exit(75)


if other_wt() >= 2:
    P("GUARD: two other wt0*.py processes are running; wait and rerun -> exit 75"); sys.exit(75)
if free_inactive() < 8e9:
    P("GUARD: free+inactive < 8 GB -> exit 75"); sys.exit(75)
threading.Thread(target=_watch, daemon=True).start()

P("=" * 118)
P("WT-09  stiffness terms with c_T = c exactly vs the static L* stiffness" + ("   [MUTATE: MU1-MU5]" if MUT else ""))
P("criteria FROZEN_CRITERIA.md 8812ac0477 | kappa = 1/2 FITTED | footings never pooled | Z = 5.7888 | not 'theory closed'")
P(f"guards: PM job live = {pm_live()}, other wt0*.py = {other_wt()}, free+inactive = {free_inactive()/1e9:.1f} GB, "
  f"swap used = {SWAP0/1e9:.2f} GB")
P("=" * 118)

RES = {"lane": "WT-09", "criteria": "8812ac0477", "mutate": MUT, "checks": {}, "numbers": {}, "labels": {}, "notes": []}


def chk(name, ok, msg=""):
    RES["checks"][name] = {"pass": bool(ok), "msg": msg}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")
    return bool(ok)


# ============================================================================================== constants (SI)
C_SI = 299792458.0
G_SI = 6.67430e-11
K_SI = 4 * math.pi * G_SI
PC = 3.0856775814913673e16
KPC = 1e3 * PC
MPC = 1e6 * PC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")
LSTAR = {"24pc": 24 * PC, "1kpc": 1 * KPC}
OMB, OMC_OVER_B, H0_KMS = 0.0493, 5.364, 67.4
OMC0 = OMB * OMC_OVER_B
OMM0 = OMB * (1 + OMC_OVER_B)
OML0 = 1 - OMM0
H0_SI = H0_KMS * 1e3 / MPC


def Ez(zz):
    return math.sqrt(OMM0 * (1 + zz) ** 3 + OML0)


def Omc_z(zz):
    return OMC0 * (1 + zz) ** 3 / Ez(zz) ** 2


# ============================================================================================== truncated-series toolkit
t, x, y, z = sp.symbols("t x y z", real=True)
XC = (t, x, y, z)
eps = sp.Symbol("eps")


def tr(e, n=2):
    e = sp.expand(e)
    if e == 0 or not e.has(eps):
        return e
    return sp.Add(*[e.coeff(eps, i) * eps ** i for i in range(n + 1)])


def _c012(e):
    e = tr(e)
    return [e.coeff(eps, i) if e.has(eps) or i == 0 else (e if i == 0 else 0) for i in range(3)]


def tsqrt(e):
    e = tr(e)
    c0, c1, c2 = e.coeff(eps, 0) if e.has(eps) else e, e.coeff(eps, 1), e.coeff(eps, 2)
    s0 = sp.sqrt(c0)
    return tr(s0 + c1 / (2 * s0) * eps + (c2 / (2 * s0) - c1 ** 2 / (8 * s0 ** 3)) * eps ** 2)


def tinv(e):
    e = tr(e)
    c0, c1, c2 = e.coeff(eps, 0) if e.has(eps) else e, e.coeff(eps, 1), e.coeff(eps, 2)
    return tr(1 / c0 - c1 / c0 ** 2 * eps + (c1 ** 2 / c0 ** 3 - c2 / c0 ** 2) * eps ** 2)


def mat(f):
    return [[f(i, j) for j in range(4)] for i in range(4)]


def sym(T):
    return mat(lambda i, j: tr((T[i][j] + T[j][i]) / 2))


class Kin:
    """All CFG938 building blocks for metric g = g0 + eps g1, scalar chi and comoving labels phis (to O(eps^2))."""

    def __init__(self, g0, g1, chi, phis, need_ricci=False):
        g0i = g0.inv()
        g = g0 + eps * g1
        gi = g0i - eps * g0i * g1 * g0i + eps ** 2 * g0i * g1 * g0i * g1 * g0i
        self.g = mat(lambda i, j: tr(g[i, j]))
        self.gi = mat(lambda i, j: tr(gi[i, j]))
        self.sqrtmg = tsqrt(-tr(g.det()))
        dg = [[[sp.diff(self.g[m][n], XC[l]) for l in range(4)] for n in range(4)] for m in range(4)]
        Gam = [[[0] * 4 for _ in range(4)] for _ in range(4)]
        for la in range(4):
            for mu in range(4):
                for nu in range(mu, 4):
                    s = 0
                    for si in range(4):
                        if self.gi[la][si] != 0:
                            s += self.gi[la][si] * (dg[nu][si][mu] + dg[mu][si][nu] - dg[mu][nu][si])
                    Gam[la][mu][nu] = Gam[la][nu][mu] = tr(s / 2)
        self.Gam = Gam
        if need_ricci:
            Ric = mat(lambda m, n: 0)
            for m in range(4):
                for n in range(m, 4):
                    s = 0
                    for l in range(4):
                        s += sp.diff(Gam[l][m][n], XC[l]) - sp.diff(Gam[l][m][l], XC[n])
                        for sg in range(4):
                            s += Gam[l][l][sg] * Gam[sg][m][n] - Gam[l][n][sg] * Gam[sg][m][l]
                    Ric[m][n] = Ric[n][m] = tr(s)
            self.R = tr(sum(self.gi[m][n] * Ric[m][n] for m in range(4) for n in range(4) if self.gi[m][n] != 0))
        # medium kinematics from labels
        dphi = [[sp.diff(ph, XC[a]) for a in range(4)] for ph in phis]
        Jt = []
        for mu in range(4):
            s = 0
            for a in range(4):
                for b in range(4):
                    for c in range(4):
                        if len({mu, a, b, c}) == 4:
                            s += sp.LeviCivita(mu, a, b, c) * dphi[0][a] * dphi[1][b] * dphi[2][c]
            Jt.append(tr(s))
        N2 = tr(-sum(self.g[m][n] * Jt[m] * Jt[n] for m in range(4) for n in range(4) if self.g[m][n] != 0))
        sN = tsqrt(N2)
        isN = tinv(sN)
        self.sN = sN
        self.n = tr(sN * tinv(self.sqrtmg))
        uU = [tr(Jt[m] * isN) for m in range(4)]
        uD = [tr(sum(self.g[m][n] * uU[n] for n in range(4))) for m in range(4)]
        self.uU, self.uD = uU, uD
        Pm = mat(lambda m, a: tr((1 if m == a else 0) + uD[m] * uU[a]))          # h_m^a
        self.Pm = Pm
        self.hup = mat(lambda m, n: tr(self.gi[m][n] + uU[m] * uU[n]))
        self.hlow = mat(lambda m, n: tr(self.g[m][n] + uD[m] * uD[n]))
        dchi = [sp.diff(chi, XC[m]) for m in range(4)]
        A = mat(lambda m, n: tr(sp.diff(chi, XC[m], XC[n]) - sum(Gam[l][m][n] * dchi[l] for l in range(4))))
        self.A = A
        self.DD = self.proj(A)
        self.D2 = tr(sum(self.hup[m][n] * A[m][n] for m in range(4) for n in range(4)))
        self.Box = tr(sum(self.gi[m][n] * A[m][n] for m in range(4) for n in range(4) if self.gi[m][n] != 0))
        Du = mat(lambda m, n: tr(sp.diff(uD[n], XC[m]) - sum(Gam[l][m][n] * uD[l] for l in range(4))))
        self.theta = tr(sum(self.gi[m][n] * Du[m][n] for m in range(4) for n in range(4) if self.gi[m][n] != 0))
        self.Kx = sym(self.proj(Du))
        self.Cs = tr(sum(uU[m] * dchi[m] for m in range(4)))
        Dchi = [tr(sum(Pm[b][c] * dchi[c] for c in range(4))) for b in range(4)]
        ND = mat(lambda a, b: tr(sp.diff(Dchi[b], XC[a]) - sum(Gam[l][a][b] * Dchi[l] for l in range(4))))
        self.Hc = sym(self.proj(ND))
        self.Dlap = tr(sum(self.hup[m][n] * self.Hc[m][n] for m in range(4) for n in range(4)))
        self.Ab0 = [A[0][i] for i in range(4)]

    def proj(self, T):
        Pm = self.Pm
        return mat(lambda m, n: tr(sum(Pm[m][a] * Pm[n][b] * T[a][b] for a in range(4) for b in range(4)
                                       if Pm[m][a] != 0 and Pm[n][b] != 0)))

    def TL(self, T):
        trT = tr(sum(self.hup[m][n] * T[m][n] for m in range(4) for n in range(4)))
        return mat(lambda m, n: tr(T[m][n] - sp.Rational(1, 3) * self.hlow[m][n] * trT))

    def norm2(self, T):
        gi = self.gi
        s = 0
        for m in range(4):
            for a in range(4):
                if gi[m][a] == 0:
                    continue
                for n in range(4):
                    for b in range(4):
                        if gi[n][b] == 0 or T[m][n] == 0 or T[a][b] == 0:
                            continue
                        s += T[m][n] * T[a][b] * gi[m][a] * gi[n][b]
        return tr(s)

    def lin(self, T1, T2, c):
        return mat(lambda m, n: tr(T1[m][n] + c * T2[m][n]))


# ============================================================================================== candidates
gam, Ksym = sp.symbols("gamma K", positive=True)
aF, bF, bsF = sp.symbols("a_f b_f beta_s", real=True)
rho0 = sp.Symbol("rho0", positive=True)


def S_cand(name, k):
    """Return S such that the candidate's Lagrangian density is -sqrt(-g) * S (coefficient included)."""
    c2 = gam / (2 * Ksym ** 2)
    c3 = 3 * gam / (4 * Ksym ** 2)
    if name == "i":
        return c3 * k.norm2(k.TL(k.DD))
    if name == "ii":
        return tr(c2 * k.Box ** 2)
    if name == "iii":
        return tr(c2 * k.D2 ** 2)
    if name == "iv":
        return c2 * k.norm2(k.Hc)
    if name == "iv_p":
        return c3 * k.norm2(k.TL(k.Hc))
    if name == "v":
        return tr(c2 * k.Dlap ** 2)
    if name == "vi_half":
        return c3 * k.norm2(k.TL(k.lin(k.DD, k.Kx, sp.Rational(1, 2) * k.Cs)))
    if name == "vi_b":
        return tr(c2 * k.Cs ** 2 * k.norm2(k.TL(k.Kx)))
    if name == "vii":
        return tr(c2 * (k.Box ** 2 - k.norm2(k.A)))
    if name == "viii":
        return tr(c2 * (k.Dlap ** 2 - k.norm2(k.Hc)))
    if name == "ix":
        return tr(gam / 2 * (rho0 * k.n) ** 2)
    if name == "fam":                                     # family (x): a (Delta_u chi)^2 + b |TL(DD + beta_s K C)|^2
        return tr(aF * k.Dlap ** 2 + bF * k.norm2(k.TL(k.lin(k.DD, k.Kx, bsF * k.Cs))))
    # ---- MUTATE variants of (v)
    if name == "v_MU1":
        return tr(c2 * k.Dlap ** 2 + sp.Rational(1, 100) * c3 * k.norm2(k.TL(k.DD)))
    if name == "v_MU2":
        return tr(c2 * (k.D2 + sp.Rational(9, 10) * k.theta * k.Cs) ** 2)
    if name == "v_MU3":
        return tr(2 * c2 * k.Dlap ** 2)
    if name == "v_MU4":
        return tr(c2 * k.Dlap ** 2 + c2 * k.Cs ** 2 * k.norm2(k.TL(k.Kx)))
    raise ValueError(name)


CANDS = ["i", "ii", "iii", "iv", "iv_p", "v", "vi_half", "vi_b", "vii", "viii", "ix"]
if MUT:
    CANDS = [c for c in CANDS if c != "v"] + ["v_MU1", "v_MU2", "v_MU3", "v_MU4"]
DESC = {"i": "-(3g/4K^2) tau.tau  [CFG938, projected traceless]", "ii": "-(g/2K^2)(Box chi)^2",
        "iii": "-(g/2K^2)(D^2 chi)^2", "iv": "-(g/2K^2) |H_int|^2  [full intrinsic Hessian]",
        "iv_p": "-(3g/4K^2)|TL H_int|^2  [= sol61 alpha=1]", "v": "-(g/2K^2)(Delta_u chi)^2  [intrinsic leaf Laplacian]",
        "vi_half": "-(3g/4K^2)|TL(DD + K C/2)|^2  [beta = 1/2]", "vi_b": "-(g/2K^2) C^2 sigma.sigma  [clock-weighted shear]",
        "vii": "-(g/2K^2)[(Box chi)^2 - A.A]  [Horndeski-L4 type]", "viii": "-(g/2K^2)[(Delta_u chi)^2 - |H_int|^2]  [leaf Galileon]",
        "ix": "-(g/2) m^2 n^2  [CFG938 local EoS]", "v_MU1": "(v) + 0.01 x (i)", "v_MU2": "-(g/2K^2)(D^2chi + 0.9 theta C)^2",
        "v_MU3": "(v) x 2", "v_MU4": "(v) + (vi-b)"}

# ============================================================================================== K4: EH normalisation
P("\n[K4] Einstein-Hilbert normalisation: <sqrt(-g) R>_{O(h^2)} for a TT plane wave (off shell)")
Aamp, kk, ww = sp.symbols("A k omega", positive=True)
phase = kk * z - ww * t
g1K4 = sp.zeros(4, 4)
g1K4[1, 1] = Aamp * sp.cos(phase)
g1K4[2, 2] = -Aamp * sp.cos(phase)
kinK4 = Kin(sp.diag(-1, 1, 1, 1), g1K4, sp.S(0), [x, y, z], need_ricci=True)
LK4 = tr(kinK4.sqrtmg * kinK4.R).coeff(eps, 2)
avgK4 = sp.simplify(sp.integrate(LK4.subs(t, 0), (z, 0, 2 * sp.pi / kk)) * kk / (2 * sp.pi))
k4 = sp.simplify(avgK4 - sp.Rational(1, 4) * (ww ** 2 - kk ** 2) * Aamp ** 2) == 0
chk("K4_EH_normalisation", k4, f"<sqrt(-g)R>_2 = {avgK4}  (frozen: (omega^2 - k^2) A^2 / 4)")

# ============================================================================================== K6: flat null Lagrangians
P("\n[K6] flat-space null Lagrangians (CFG938 S2d)")
chis = sp.Function("chis")(x, y, z)
Hs = sp.Matrix(3, 3, lambda i, j: sp.diff(chis, (x, y, z)[i], (x, y, z)[j]))
lap = Hs.trace()
L6a = sum(Hs[i, j] ** 2 for i in range(3) for j in range(3)) - lap ** 2
TLs = Hs - sp.eye(3) * lap / 3
L6b = sum(TLs[i, j] ** 2 for i in range(3) for j in range(3)) - sp.Rational(2, 3) * lap ** 2
e6a = sp.simplify(sp.euler_equations(L6a, [chis], [x, y, z])[0].lhs)
e6b = sp.simplify(sp.euler_equations(L6b, [chis], [x, y, z])[0].lhs)
chk("K6_null_Lagrangians", e6a == 0 and e6b == 0, f"EL[|dd chi|^2 - (Lap chi)^2] = {e6a}; EL[|TL|^2 - (2/3)(Lap chi)^2] = {e6b}")
P(f"  [{time.time()-T0:6.1f} s, peak RSS {rss_bytes()/1e9:.2f} GB]")

# ============================================================================================== C: static stiffness
P("\n[C] static stiffness: flat leaves, medium at rest, chi = chi(x,y,z) (theta = C = 0 by construction of 'static')")
kinS = Kin(sp.diag(-1, 1, 1, 1), sp.zeros(4, 4), chis, [x, y, z])
recS = gam / (2 * Ksym ** 2) * lap ** 2                              # record: (gamma/2) rho_c^2 = (gamma/2K^2)(Lap chi)^2
rr = sp.Symbol("r", positive=True)
uf = sp.Function("u")(rr)
qS, pS = sp.symbols("q p")


def spherical_density(expr):
    """Evaluate a static density on the z axis for chi(r): chi_xx = chi_yy = chi'/r = p, chi_zz = chi'' = q."""
    rep = {}
    for d in expr.atoms(sp.Derivative):
        vs = d.variables
        if len(vs) == 2:
            rep[d] = qS if vs == (z, z) else (pS if vs in ((x, x), (y, y)) else 0)
        elif len(vs) == 1:
            rep[d] = 0                                               # first derivatives enter no static candidate (checked)
    return sp.expand(expr.xreplace(rep))


def EL_u(dens_qp):
    Lr = 4 * sp.pi * rr ** 2 * dens_qp.subs({qS: sp.diff(uf, rr), pS: uf / rr})
    return sp.expand(sp.euler_equations(Lr, [uf], [rr])[0].lhs)


EL_rec = EL_u(spherical_density(recS))
P(f"  record EL_u [(gamma/2K^2) 4 pi r^2 (u' + 2u/r)^2] = {sp.factor(EL_rec)}")
STATIC = {}
for cn in CANDS + ["fam"]:
    Sst = S_cand(cn, kinS)
    has_first = any(len(d.variables) == 1 for d in Sst.atoms(sp.Derivative))
    e3 = sp.simplify(sp.euler_equations(Sst - recS, [chis], [x, y, z])[0].lhs) if cn != "fam" else None
    dqp = spherical_density(Sst)
    elc = EL_u(dqp)
    diff = sp.simplify(elc - EL_rec)
    ratio = sp.simplify(elc / EL_rec) if EL_rec != 0 else None
    if diff == 0:
        form = "IDENTICAL"
    elif ratio is not None and not ratio.has(rr) and not ratio.has(uf) and ratio.free_symbols <= {gam, Ksym, aF, bF, bsF}:
        form = f"MULTIPLE x {ratio}"
    else:
        form = "DIFFERENT FORM"
    STATIC[cn] = dict(form=form, ratio=str(ratio), first_derivs=has_first, null_lagrangian_3d=(e3 == 0) if e3 is not None else None,
                      density_qp=str(sp.factor(dqp)), EL=elc)
    P(f"  ({cn:8s}) static density(q=chi'', p=chi'/r) = {sp.factor(dqp)}")
    P(f"             spherical EL vs record: {form};  non-spherical C3 null-Lagrangian test: "
      f"{'n/a' if e3 is None else ('PASS (identical for all static chi)' if e3 == 0 else 'FAIL (differs off spherical symmetry)')}"
      f"{'  [first derivatives present]' if has_first else ''}")
fam_ratio = sp.simplify(STATIC["fam"]["EL"] / EL_rec)
P(f"  family (x): EL_fam / EL_rec = {fam_ratio}  -> S requires {sp.factor(fam_ratio)} = 1")
RES["static_family_condition"] = str(sp.factor(fam_ratio - 1))

# ---- K3 part 1: (i)'s static EL = record (symbolic)
k3sym = STATIC.get("i", {}).get("form") == "IDENTICAL"

# ---- C2 numeric NGC 3198 + K3 part 2 (law reduction)
P("\n[C2/K3] NGC 3198 (record SPARC file, Upsilon 0.61, 43 radii): gamma->0 law state, stiffness EL comparison")
d = np.genfromtxt(os.path.join(REPO, "real_research", "data", "sparc_data", "NGC3198_rotmod.dat"), comments="#")
Rm = d[:, 0] * KPC
Vg, Vd, Vb = d[:, 3] * 1e3, d[:, 4] * 1e3, d[:, 5] * 1e3
gNb = (Vg * np.abs(Vg) + 0.61 * Vd * np.abs(Vd) + 0.61 * Vb * np.abs(Vb)) / Rm
LAW = {}
k3num = True
for foot in FOOTS:
    a0 = A0[foot]
    uL = 0.5 * (-gNb + np.sqrt(gNb ** 2 + 4 * gNb * a0))               # R(u) = u^2/(a0 - u) = g_N
    resid = np.max(np.abs(uL ** 2 / (a0 - uL) / gNb - 1))
    glaw = 0.5 * (gNb + np.sqrt(gNb ** 2 + 4 * gNb * a0))
    relg = np.max(np.abs((gNb + uL) / glaw - 1))
    k3num &= relg <= 1e-12
    LAW[foot] = dict(u=uL, g=gNb + uL, a0=a0)
    P(f"  {foot:9s}: N = {len(Rm)}, max|R(u)/g_N - 1| = {resid:.2e}, max|g/g_law - 1| = {relg:.2e} (line 1e-12; CFG938 2.2e-16)")
chk("K3_static_EL_of_i_equals_CFG938_and_law_reduction", k3sym and k3num,
    f"(i) spherical EL {'IDENTICAL' if k3sym else 'DIFFERS'} to E[M_c]'s; law reduction <= 1e-12 both footings: {k3num}")

U, Up, Upp = sp.symbols("U Up Upp")


def EL_num(elexpr):
    e = elexpr.subs({sp.diff(uf, rr, 2): Upp}).subs({sp.diff(uf, rr): Up}).subs({uf: U})
    return sp.lambdify((rr, U, Up, Upp, gam, Ksym), e, "numpy")


fr = EL_num(EL_rec)
C2 = {}
for cn in CANDS:
    fc = EL_num(STATIC[cn]["EL"])
    worst = 0.0
    per = {}
    for foot in FOOTS:
        cs = CubicSpline(Rm, LAW[foot]["u"])
        u0, u1, u2 = cs(Rm), cs(Rm, 1), cs(Rm, 2)
        for lk, Ls in LSTAR.items():
            gv = K_SI * Ls ** 2 / 2
            er = fr(Rm, u0, u1, u2, gv, K_SI)
            ec = fc(Rm, u0, u1, u2, gv, K_SI) * np.ones_like(Rm)
            rel = float(np.max(np.abs(ec - er) / np.abs(er)))
            per[f"{foot}/{lk}"] = rel
            worst = max(worst, rel)
    C2[cn] = dict(max_rel=worst, per=per)
    STATIC[cn]["S"] = (STATIC[cn]["form"] == "IDENTICAL") and worst <= 1e-9
    P(f"  ({cn:8s}) max_r |EL_cand - EL_rec|/|EL_rec| over 4 footing x L* = {worst:.3e}  -> S = {STATIC[cn]['S']}")
RES["numbers"]["C2_static_rel_diff"] = {c: C2[c] for c in C2}
P(f"  [{time.time()-T0:6.1f} s, peak RSS {rss_bytes()/1e9:.2f} GB]")

# ---- C4 PN (Bochner) difference, report only
P("\n[C4] post-Newtonian (Bochner) difference (i) vs (v) on curved static leaves, report only: 1.5 R_rr u^2/(K^2 rho_c^2)")
C4 = {}
for foot in FOOTS:
    cs_u = CubicSpline(Rm, LAW[foot]["u"]); cs_g = CubicSpline(Rm, LAW[foot]["g"])
    u0, u1 = cs_u(Rm), cs_u(Rm, 1)
    g0v, g1v = cs_g(Rm), cs_g(Rm, 1)
    rhoc = (u1 + 2 * u0 / Rm) / K_SI
    Rrr = (2 * g1v + 2 * g0v / Rm) / C_SI ** 2
    ratio = np.abs(1.5 * Rrr * u0 ** 2 / (K_SI ** 2 * rhoc ** 2))
    ok = np.isfinite(ratio) & (rhoc > 0)
    C4[foot] = dict(max=float(np.max(ratio[ok])), median=float(np.median(ratio[ok])), n_used=int(ok.sum()),
                    n_rho_nonpositive=int((rhoc <= 0).sum()))
    P(f"  {foot:9s}: max {C4[foot]['max']:.2e}, median {C4[foot]['median']:.2e} (radii with rho_c > 0: {ok.sum()}/{len(Rm)})")
RES["numbers"]["C4_PN_bochner_ratio"] = C4

# ============================================================================================== B1: local uniform background
P("\n[B1] local uniform background (Minkowski, medium at rest, V = (C, u sin th, 0, u cos th), k || z), exact in V")
Cc = sp.Symbol("C", real=True)
uu = sp.Symbol("u", nonnegative=True)
ct, st = sp.symbols("ct st", real=True)
fn = ["hp", "hx", "xi1", "xi2", "xi3", "dchi", "dlam"]
F = [sp.Function(n)(t, z) for n in fn]
hp, hx, xi1, xi2, xi3, dchi, dlam = F
g1 = sp.zeros(4, 4)
g1[1, 1], g1[2, 2], g1[1, 2], g1[2, 1] = hp, -hp, hx, hx
chiB = Cc * t + uu * (st * x + ct * z) + eps * dchi
kinB = Kin(sp.diag(-1, 1, 1, 1), g1, chiB, [x - eps * xi1, y - eps * xi2, z - eps * xi3], need_ricci=True)
P(f"  kinematics built [{time.time()-T0:6.1f} s, peak RSS {rss_bytes()/1e9:.2f} GB]")
u1z = kinB.uU[3].coeff(eps, 1)
P(f"  sanity: u^z at O(eps) = {u1z}  (expected +d_t xi3: displacement +xi)")
P(f"  sanity: theta at O(eps) = {kinB.theta.coeff(eps, 1)};  Delta_u chi at O(eps) = {sp.factor(kinB.Dlap.coeff(eps, 1))}")
P(f"          D^2 chi at O(eps) = {sp.factor(kinB.D2.coeff(eps, 1))}")
wS, kS, vS = sp.symbols("omega k v", positive=True)
E, Ei = sp.symbols("E Ei")
Ps = sp.symbols("P0:7")
Qs = sp.symbols("Q0:7")


def fourier(L2):
    rep = {}
    for dd in L2.atoms(sp.Derivative):
        i = F.index(dd.expr)
        fp = fq = 1
        for v_ in dd.variables:
            fp *= (-sp.I * wS if v_ == t else sp.I * kS)
            fq *= (sp.I * wS if v_ == t else -sp.I * kS)
        rep[dd] = Ps[i] * E * fp + Qs[i] * Ei * fq
    L = L2.xreplace(rep).xreplace({f_: Ps[i] * E + Qs[i] * Ei for i, f_ in enumerate(F)})
    L = sp.expand(L)
    assert not (L.has(x) or L.has(y) or L.has(z) or L.has(t)), "explicit coordinates left: background not uniform"
    B = L.coeff(E, 1).coeff(Ei, 1)
    M = sp.Matrix(7, 7, lambda a, b: sp.expand(sp.diff(B, Ps[a], Qs[b])))
    return M.T                                                        # N: EOM N P = 0


L2_EH = tr(kinB.sqrtmg * kinB.R / (4 * Ksym)).coeff(eps, 2)
L2_dust = tr(-rho0 * kinB.sN).coeff(eps, 2)
L2_P938 = tr(kinB.sqrtmg * eps * dlam * (kinB.D2 - Ksym * rho0 * kinB.n)).coeff(eps, 2)
L2_Pint = tr(kinB.sqrtmg * eps * dlam * (kinB.Dlap - Ksym * rho0 * kinB.n + Ksym * rho0)).coeff(eps, 2)
N_EH, N_dust, N_938, N_int = [fourier(L) for L in (L2_EH, L2_dust, L2_P938, L2_Pint)]
P(f"  EH TT block (+,+) = {sp.factor(N_EH[0, 0])};  dust xi block diag = {[sp.factor(N_dust[i, i]) for i in (2, 3, 4)]}")
P(f"  P938 constraint row (dlam) = {[sp.factor(N_938[6, j]) for j in range(7)]}")
P(f"  P_int constraint row (dlam) = {[sp.factor(N_int[6, j]) for j in range(7)]}")
P(f"  [{time.time()-T0:6.1f} s, peak RSS {rss_bytes()/1e9:.2f} GB]")
NC = {}
for cn in CANDS + ["fam"]:
    NC[cn] = fourier(tr(-kinB.sqrtmg * S_cand(cn, kinB)).coeff(eps, 2))
P(f"  candidate quadratic forms built [{time.time()-T0:6.1f} s, peak RSS {rss_bytes()/1e9:.2f} GB]")

sub_trig = {st: sp.sqrt(1 - ct ** 2)}


def tt_first_order(Nc):
    """B1a: direct TT block (EH + candidate). Returns per-pol exact root and first-order d(v^2)/(L*^2) [L*^2 = 2 gamma/K]."""
    Nt = (N_EH + Nc)[:2, :2].subs(wS, vS * kS)
    off = sp.simplify(Nt[0, 1].subs(sub_trig))
    out = {}
    for p_, nm in ((0, "+"), (1, "x")):
        e = sp.expand(sp.simplify(Nt[p_, p_] / kS ** 2))
        # F(v, gamma) = 0, root v(0) = 1: d(v^2)/dgamma = -2 F_gamma / F_v at (1, 0)
        Fg = sp.diff(e, gam).subs({gam: 0, vS: 1})
        Fv = sp.diff(e, vS).subs({gam: 0, vS: 1})
        F0 = sp.simplify(e.subs({gam: 0, vS: 1}))
        dv2 = sp.simplify((-2 * Fg / Fv) * Ksym / 2)               # per L*^2
        dv2 = sp.simplify(sp.expand(dv2.subs(sub_trig)))
        # exact roots in v (positive branch)
        roots = sp.solve(sp.Eq(e, 0), vS)
        out[nm] = dict(F0=F0, dv2_per_L2=dv2, roots=roots, expr=e)
    return out, off


def principal_zero(Nc):
    """T at principal order, direct block: candidate's TT block identically zero."""
    return all(sp.simplify(Nc[i, j]) == 0 for i in range(2) for j in range(2))


def mixes(Nc):
    return any(sp.simplify(Nc[i, j]) != 0 for i in range(2) for j in range(2, 7))


B1 = {}
P("\n[B1a] direct TT block: d(c_T^2/c^2) per L*^2 at first order (c = 1; theta = angle(k, spatial grad chi); C = u.d chi)")
for cn in CANDS + ["fam"]:
    tt, off = tt_first_order(NC[cn])
    pz = principal_zero(NC[cn])
    mx = mixes(NC[cn])
    B1[cn] = dict(tt=tt, offdiag=str(off), principal_zero=pz, mixes=mx)
    P(f"  ({cn:8s}) {DESC.get(cn, 'family (x)')}")
    P(f"             TT block of the candidate identically zero: {pz};  h-(xi,dchi) mixing present: {mx};  +/x off-diagonal: {off}")
    for nm in ("+", "x"):
        P(f"             pol {nm}: d(v^2)/L*^2 = {sp.factor(tt[nm]['dv2_per_L2'])}")
    RES["labels"].setdefault(cn, {})["B1a_dv2_per_L2"] = {nm: str(sp.factor(tt[nm]["dv2_per_L2"])) for nm in ("+", "x")}
P(f"  [{time.time()-T0:6.1f} s, peak RSS {rss_bytes()/1e9:.2f} GB]")

# ---- K1, K2
th_grid = [sp.Rational(i, 12) * sp.pi for i in range(13)]
k1 = True
k1_vals = []
for th in th_grid:
    for nm in ("+", "x"):
        val = sp.simplify(B1["i"]["tt"][nm]["dv2_per_L2"].subs({Cc: 0, ct: sp.cos(th)}) - sp.Rational(3, 2) * uu ** 2) if "i" in B1 else 1
        k1 &= (val == 0)
        k1_vals.append(str(val))
chk("K1_tau_tau_reproduces_WT02", k1, "candidate (i): d(c_T^2/c^2) = +1.5 L*^2 u^2/c^4 at C = 0 for all 13 angles, both polarisations")
k2 = True
for cn in CANDS + ["fam"]:
    for nm in ("+", "x"):
        e0 = B1[cn]["tt"][nm]["expr"].subs({gam: 0, aF: 0, bF: 0})
        r0 = [sp.simplify(r_) for r_ in sp.solve(sp.Eq(e0, 0), vS)]
        k2 &= (r0 == [1])
chk("K2_gamma0_gives_cT_equal_c", k2, "gamma = 0 (and a = b = 0 for the family): every candidate's TT dispersion has the single positive root v = 1")

# ---- B1b mixing: Schur complement at leading order in k (exact rationals, high-precision roots)
import mpmath as mp
mp.mp.dps = 60
random.seed(909)


def mixing_dv2(Nc, Npar, params, gnum):
    """Leading-k Schur complement over (xi, dchi, dlam): returns d(v^2)/L*^2 near v = 1 (graviton branch)."""
    Ntot = (N_EH + N_dust + Npar + Nc).subs(params).subs(gam, gnum).subs(wS, vS * kS)
    hidx, xidx = [0, 1], [2, 3, 4, 5, 6]
    Nhh = Ntot.extract(hidx, hidx); NhX = Ntot.extract(hidx, xidx)
    NXh = Ntot.extract(xidx, hidx); NXX = Ntot.extract(xidx, xidx)
    sol = NXX.LUsolve(NXh)
    Neff = (Nhh - NhX * sol).applyfunc(sp.cancel)
    res = {}
    for p_, nm in ((0, "+"), (1, "x")):
        num, den = sp.fraction(sp.together(Neff[p_, p_]))
        pk = sp.Poly(sp.expand(num), kS)
        lead = sp.Poly(pk.LC(), vS)
        dk = sp.Poly(sp.expand(den), kS)
        coeffs = [mp.mpf(sp.Rational(cf).p) / mp.mpf(sp.Rational(cf).q) for cf in lead.all_coeffs()]
        rts = mp.polyroots(coeffs, maxsteps=200, extraprec=200)
        best = min(rts, key=lambda r_: abs(r_ - 1))
        res[nm] = float(mp.re(best) ** 2 - 1) / float(2 * gnum / params[Ksym])
    return res


P("\n[B1b] h-(xi,dchi,dlam) mixing at leading order in k (both parents; Schur complement; exact rationals + 60-digit roots)")
B1b = {}
for cn in CANDS:
    if not B1[cn]["mixes"]:
        B1b[cn] = {"P938": "no mixing (B1a exact)", "P_int": "no mixing (B1a exact)"}
        P(f"  ({cn:8s}) candidate does not couple TT h to (xi, dchi): B1a is the full principal symbol in both parents")
        continue
    out = {}
    for par, Np in (("P938", N_938), ("P_int", N_int)):
        vals = []
        for trial in range(5):
            tq = sp.Rational(random.randint(1, 9), 10)
            prm = {Cc: sp.Rational(random.randint(3, 15), 10) * random.choice([1, -1]), uu: sp.Rational(random.randint(3, 15), 10),
                   ct: (1 - tq ** 2) / (1 + tq ** 2), st: 2 * tq / (1 + tq ** 2), rho0: sp.Rational(random.randint(5, 20), 10),
                   Ksym: sp.Rational(1)}
            gnum = sp.Rational(1, 10 ** 9)
            mv = mixing_dv2(NC[cn], Np, prm, gnum)
            direct = {nm: float(B1[cn]["tt"][nm]["dv2_per_L2"].subs(st, sp.sqrt(1 - ct ** 2)).subs({Cc: prm[Cc], uu: prm[uu], ct: prm[ct], Ksym: 1}))
                      for nm in ("+", "x")}
            vals.append(dict(params={str(k_): str(v_) for k_, v_ in prm.items()}, mixed=mv, direct=direct))
        out[par] = vals
        P(f"  ({cn:8s}) {par}: d(v^2)/L*^2 mixed vs direct at 5 random points: " +
          "; ".join(f"[{v_['mixed']['+']:+.4f}/{v_['mixed']['x']:+.4f} vs {v_['direct']['+']:+.4f}/{v_['direct']['x']:+.4f}]" for v_ in vals))
    B1b[cn] = out
RES["numbers"]["B1b_mixing"] = B1b
P(f"  [{time.time()-T0:6.1f} s, peak RSS {rss_bytes()/1e9:.2f} GB]")

# ---- B1c Ostrogradsky and B1d clock health
P("\n[B1c/B1d] extra time derivatives and clock health (h = 0; dchi, dlam eliminated with the parent's constraint)")
Lsym = sp.Symbol("L", positive=True)
HLTH = {}
for cn in CANDS + ["fam"]:
    Ntot = N_dust + NC[cn]
    degs = [sp.degree(sp.expand(Ntot[i, i]), wS) if Ntot[i, i] != 0 else 0 for i in range(2, 6)]
    HLTH[cn] = {"diag_omega_degree(xi1,xi2,xi3,dchi)": degs}
    for par, Np in (("P938", N_938), ("P_int", N_int)):
        Nx = (Ntot + Np)
        idx_x, idx_c = [2, 3, 4], [5, 6]
        A_ = Nx.extract(idx_x, idx_x); B_ = Nx.extract(idx_x, idx_c); C_ = Nx.extract(idx_c, idx_x); D_ = Nx.extract(idx_c, idx_c)
        Nxi = (A_ - B_ * D_.LUsolve(C_)).applyfunc(lambda e_: sp.expand(sp.cancel(e_)))
        is_poly = all(sp.denom(sp.together(e_)).free_symbols.isdisjoint({wS}) for e_ in Nxi)
        degw = max(sp.degree(sp.numer(sp.together(e_)), wS) if e_ != 0 else 0 for e_ in Nxi)
        Tm = Nxi.applyfunc(lambda e_: sp.expand(sp.cancel(sp.diff(e_, wS, 2) / 2)).subs(wS, 0))
        # kinetic matrix at u = 0 (cosmic background): k^2 coefficient
        T_u0 = Tm.subs(uu, 0).applyfunc(sp.expand)
        T2 = T_u0.applyfunc(lambda e_: sp.expand(e_).coeff(kS, 2))
        T0m = T_u0.applyfunc(lambda e_: sp.expand(e_).coeff(kS, 0))
        HLTH[cn][par] = dict(omega_degree_after_constraint=int(degw), polynomial_in_omega=bool(is_poly),
                             T2_diag=[str(sp.factor(T2[i, i])) for i in range(3)], T0_diag=[str(sp.factor(T0m[i, i])) for i in range(3)],
                             T2_offdiag_zero=all(T2[i, j] == 0 for i in range(3) for j in range(3) if i != j),
                             T2=T2, T0=T0m, Tfull=Tm)
        P(f"  ({cn:8s}) {par}: omega-degree after constraint = {degw};  omega^2 k^2 coefficient (u = 0) diag "
          f"[xi1, xi2, xi3(L)] = {[sp.factor(T2[i, i]) for i in range(3)]}")
    P(f"             diagonal omega-degree before constraint (xi1, xi2, xi3, dchi) = {degs}")
P(f"  [{time.time()-T0:6.1f} s, peak RSS {rss_bytes()/1e9:.2f} GB]")

# thresholds (cosmic clock, S1d): H = 1 units, K rho0 = 1.5 Omega_c H^2, C = K rho0/(3H) (sign irrelevant), gamma = K L*^2/2
P("\n  clock-health thresholds on S1d's FRW (kinetic eigenvalue crosses zero): (k L*)^2 = -T0/T2 * L*^2")
THR = {}
for cn in CANDS:
    THR[cn] = {}
    for par in ("P938", "P_int"):
        T2m, T0m = HLTH[cn][par]["T2"], HLTH[cn][par]["T0"]
        row = {}
        for zz in (0.0, 10.0):
            oc = Omc_z(zz)
            sb = {Ksym: 1, rho0: sp.Float(1.5 * oc), Cc: sp.Float(0.5 * oc), gam: Lsym ** 2 / 2, uu: 0}
            vals = []
            for i in range(3):
                t2 = sp.N(T2m[i, i].subs(sb)); t0 = sp.N(T0m[i, i].subs(sb))
                if t2 == 0:
                    vals.append(None)
                else:
                    kl2 = sp.N((-t0 / t2) * Lsym ** 2)
                    vals.append(float(sp.sqrt(kl2)) if kl2 > 0 else None)
            row[f"z={zz:g}"] = vals
        THR[cn][par] = row
        neg = [str(sp.factor(HLTH[cn][par]["T2"][i, i])) for i in range(3)]
        P(f"  ({cn:8s}) {par}: k L* where the kinetic coefficient flips [xi1, xi2, xi3]: z=0 {row['z=0']}, z=10 {row['z=10']}")
RES["numbers"]["B1d_thresholds_kLstar"] = THR

# ============================================================================================== B2: exact FRW
P("\n[B2] exact FRW: g = -dt^2 + a(t)^2 (delta + h), comoving medium, chi = chibar(t), TT h(t,z), both polarisations")
aT = sp.Function("a", positive=True)(t)
chb = sp.Function("chibar")(t)
hF = sp.Function("hF")(t, z)
B2 = {}
KIN2 = {}
for pol in ("+", "x"):
    g0 = sp.diag(-1, aT ** 2, aT ** 2, aT ** 2)
    g1_ = sp.zeros(4, 4)
    if pol == "+":
        g1_[1, 1], g1_[2, 2] = aT ** 2 * hF, -aT ** 2 * hF
    else:
        g1_[1, 2] = g1_[2, 1] = aT ** 2 * hF
    KIN2[pol] = Kin(g0, g1_, chb, [x, y, z], need_ricci=True)
P(f"  FRW kinematics built [{time.time()-T0:6.1f} s, peak RSS {rss_bytes()/1e9:.2f} GB]")
Dtt, Dzz = sp.Derivative(hF, (t, 2)), sp.Derivative(hF, (z, 2))


def frw_coeffs(L2):
    el = sp.expand(sp.euler_equations(L2, [hF], [t, z])[0].lhs)
    high = [dd for dd in el.atoms(sp.Derivative) if dd.expr == hF and len(dd.variables) > 2]
    ctt = el.coeff(Dtt); czz = el.coeff(Dzz)
    rest = sp.expand(el - ctt * Dtt - czz * Dzz)
    mass = rest.coeff(hF)
    return ctt, czz, high, mass


EHc = {}
for pol in ("+", "x"):
    L2eh = tr(KIN2[pol].sqrtmg * KIN2[pol].R / (4 * Ksym)).coeff(eps, 2)
    EHc[pol] = frw_coeffs(L2eh)
    cT2 = sp.simplify(aT ** 2 * (-EHc[pol][1] / EHc[pol][0]))
    P(f"  EH {pol}: coeff(h_tt) = {sp.factor(EHc[pol][0])}, coeff(h_zz) = {sp.factor(EHc[pol][1])}, c_T^2 = {cT2}")
FRWV = {}
for cn in CANDS + ["fam"]:
    B2[cn] = {}
    for pol in ("+", "x"):
        kin = KIN2[pol]
        Sx = S_cand(cn, kin)
        bg = sp.simplify(Sx.coeff(eps, 0) if Sx.has(eps) else Sx)
        L2c = tr(-kin.sqrtmg * Sx).coeff(eps, 2)
        ctt, czz, high, mass = frw_coeffs(sp.expand(L2c + tr(kin.sqrtmg * kin.R / (4 * Ksym)).coeff(eps, 2)))
        QT = sp.simplify(ctt / EHc[pol][0])
        QG = sp.simplify(czz / EHc[pol][1])
        cT2 = sp.simplify(QG / QT)
        B2[cn][pol] = dict(QT=QT, QG=QG, cT2=cT2, high=[str(h_) for h_ in high], mass=sp.simplify(mass - EHc[pol][3]), bg=bg)
    FRWV[cn] = B2[cn]["+"]["bg"]
    P(f"  ({cn:8s}) background value on FRW = {sp.factor(B2[cn]['+']['bg'])}")
    for pol in ("+", "x"):
        b_ = B2[cn][pol]
        P(f"             pol {pol}: Q_T (kinetic/EH) = {sp.factor(b_['QT'])};  gradient/EH = {sp.factor(b_['QG'])};  "
          f"higher time derivs: {b_['high'] or 'none'}")
P(f"  [{time.time()-T0:6.1f} s, peak RSS {rss_bytes()/1e9:.2f} GB]")
k5 = ("i" in B2) and sp.simplify(B2["i"]["+"]["QT"] - (1 - 3 * gam * sp.diff(chb, t) ** 2 / Ksym)) == 0 and \
     sp.simplify(B2["i"]["x"]["QT"] - (1 - 3 * gam * sp.diff(chb, t) ** 2 / Ksym)) == 0 and \
     sp.simplify(B2["i"]["+"]["QG"] - 1) == 0
chk("K5_FRW_QT_of_i_equals_sol61", k5, "candidate (i) on exact FRW: Q_T = 1 - 3 gamma chibar'^2/K, gradient coefficient unchanged (both pols)")
k2b = all(sp.simplify(B2[cn][pol]["cT2"].subs({gam: 0, aF: 0, bF: 0}) - 1) == 0 for cn in B2 for pol in ("+", "x"))
chk("K2b_gamma0_FRW", k2b, "gamma = 0: c_T^2 = 1 exactly on FRW for every candidate")

# FRW numbers (geometric units: lengths in m; chibar' = -Omega_c H/(2c) per m, S1d)
P("\n  FRW numbers (S1d clock C = Omega_c(z) H(z) c/2): d(c_T/c) = (c_T^2/c^2 - 1)/2")
FRWN = {}
for cn in CANDS:
    FRWN[cn] = {}
    for zz in (0.0, 10.0):
        Hg = H0_SI * Ez(zz) / C_SI
        oc = Omc_z(zz)
        # chibar_g'(t_g) = -0.5 Omega_c(z) H_g; chibar'' from d/dt[-0.5 Omega_c0 H0g^2 a^-3 / H_g(a)], a' = a H_g
        aa = 1 / (1 + zz)
        H0g = H0_SI / C_SI

        def Hg_of(a_):
            return H0g * math.sqrt(OMM0 * a_ ** -3 + OML0)

        def c1_of(a_):
            return -0.5 * OMC0 * H0g ** 2 * a_ ** -3 / Hg_of(a_)
        da = 1e-6 * aa
        c2v = (c1_of(aa + da) - c1_of(aa - da)) / (2 * da) * aa * Hg_of(aa)
        Hdot = (Hg_of(aa + da) - Hg_of(aa - da)) / (2 * da) * aa * Hg_of(aa)
        row = {}
        for lk, Ls in LSTAR.items():
            sb = {gam: Ksym * Ls ** 2 / 2}
            e_ = B2[cn]["+"]["cT2"].subs(sb)
            e_ = e_.subs({sp.Derivative(chb, (t, 2)): c2v}).subs({sp.Derivative(chb, t): c1_of(aa)})
            e_ = e_.subs({sp.Derivative(aT, (t, 2)): aa * (Hdot + Hg_of(aa) ** 2)}).subs({sp.Derivative(aT, t): aa * Hg_of(aa)}).subs(aT, aa)
            e_ = e_.subs(Ksym, 1)
            val = float(sp.N(e_)) - 1.0
            row[lk] = val / 2
        FRWN[cn][f"z={zz:g}"] = row
    P(f"  ({cn:8s}) d(c_T/c): z=0 {FRWN[cn]['z=0']['24pc']:+.2e} / {FRWN[cn]['z=0']['1kpc']:+.2e};  "
      f"z=10 {FRWN[cn]['z=10']['24pc']:+.2e} / {FRWN[cn]['z=10']['1kpc']:+.2e}   (L* = 24 pc / 1 kpc; footing-free)")
RES["numbers"]["B2_FRW_dcT_over_c"] = FRWN

# ============================================================================================== wall numbers
P("\n[N] local c_T at the W wall (u = a0, C = 0): d(c_T/c) = (1/2) max_{theta,pol} d(v^2)/L*^2 x L*^2 a0^2/c^4")
WALL = {}
for cn in CANDS:
    mx = 0.0
    for th in th_grid:
        for nm in ("+", "x"):
            vv = float(B1[cn]["tt"][nm]["dv2_per_L2"].subs({Cc: 0, ct: sp.cos(th), uu: 1}))
            if abs(vv) > abs(mx):
                mx = vv
    WALL[cn] = {"coef_max_per_L2u2": mx}
    for foot in FOOTS:
        for lk, Ls in LSTAR.items():
            WALL[cn][f"{foot}/{lk}"] = 0.5 * mx * Ls ** 2 * A0[foot] ** 2 / C_SI ** 4
    P(f"  ({cn:8s}) coef {mx:+.4f};  can 24pc/1kpc {WALL[cn]['canonical/24pc']:+.2e} / {WALL[cn]['canonical/1kpc']:+.2e};"
      f"  alt {WALL[cn]['alt/24pc']:+.2e} / {WALL[cn]['alt/1kpc']:+.2e}")
RES["numbers"]["wall_dcT_over_c"] = WALL

# ============================================================================================== L1: theorem with n-dependent invariants
P("\n[L1] general quadratic form in the medium-frame Hessian blocks (TT image from B1, on the light cone, C = 0 then C != 0)")
cS = sp.symbols("c1:6", real=True)
dS = sp.symbols("d1:6", real=True)
sP = sp.Symbol("s_p", real=True)
# first-order h-images of the projected spatial Hessian and of b_i = A_0i (Fourier: P part), from kinB
Aimg = [[None] * 3 for _ in range(3)]


def img(e1):
    e1 = sp.expand(e1)
    rep = {}
    for dd in e1.atoms(sp.Derivative):
        i = F.index(dd.expr)
        fp = 1
        for v_ in dd.variables:
            fp *= (-sp.I * wS if v_ == t else sp.I * kS)
        rep[dd] = Ps[i] * fp
    e1 = e1.xreplace(rep).xreplace({f_: Ps[i] for i, f_ in enumerate(F)})
    return sp.expand(e1.subs({Ps[j]: 0 for j in range(2, 7)}))


for i in range(3):
    for j in range(3):
        Aimg[i][j] = img(kinB.DD[i + 1][j + 1].coeff(eps, 1))
bimg = [img(kinB.A[0][i + 1].coeff(eps, 1)) for i in range(3)]
nv = [st, 0, ct]


def cj(e_):
    return sp.conjugate(e_).subs({sp.conjugate(Ps[0]): Ps[0], sp.conjugate(Ps[1]): Ps[1]})


def invariants(Am, bv):
    trA = sum(Am[i][i] for i in range(3))
    nAn = sum(nv[i] * Am[i][j] * nv[j] for i in range(3) for j in range(3))
    An = [sum(Am[i][j] * nv[j] for j in range(3)) for i in range(3)]
    nb = sum(nv[i] * bv[i] for i in range(3))
    I = [trA * cj(trA), sum(Am[i][j] * cj(Am[i][j]) for i in range(3) for j in range(3)), nAn * cj(nAn),
         (nAn * cj(trA) + cj(nAn) * trA) / 2, sum(An[i] * cj(An[i]) for i in range(3))]
    J = [sum(bv[i] * cj(bv[i]) for i in range(3)), nb * cj(nb), (nb * cj(nAn) + cj(nb) * nAn) / 2,
         (nb * cj(trA) + cj(nb) * trA) / 2, sum((bv[i] * cj(An[i]) + cj(bv[i]) * An[i]) / 2 for i in range(3))]
    return I, J


Iv, Jv = invariants(Aimg, bimg)
Qgen = sum(cS[i] * Iv[i] for i in range(5)) + sum(dS[i] * Jv[i] for i in range(5))
eqsT = []
for Cval in (0, Cc):
    for pv in ((1, 0), (0, 1)):
        e_ = sp.expand(Qgen.subs({Ps[0]: pv[0], Ps[1]: pv[1]}).subs({wS: kS}).subs(Cc, Cval) / kS ** 2)
        e_ = sp.expand(e_.subs({ct: (1 - sP ** 2) / (1 + sP ** 2), st: 2 * sP / (1 + sP ** 2)}) * (1 + sP ** 2) ** 4)
        e_ = sp.expand(sp.simplify(e_))
        polyv = sp.Poly(e_, sP, uu, Cc) if Cval != 0 else sp.Poly(e_, sP, uu)
        eqsT_c = [cf for cf in polyv.coeffs()]
        eqsT += eqsT_c
    if Cval == 0:
        solT0 = sp.solve(eqsT, list(cS) + list(dS), dict=True)
        eqsT0 = list(eqsT)
# static S for the invariants: trA = q + 2p, |A|^2 = q^2 + 2p^2, nAn = q, |An|^2 = q^2; J = 0
dens_gen = (cS[0] * (qS + 2 * pS) ** 2 + cS[1] * (qS ** 2 + 2 * pS ** 2) + cS[2] * qS ** 2 + cS[3] * qS * (qS + 2 * pS) + cS[4] * qS ** 2)
elg = EL_u(dens_gen) - EL_rec
elg = sp.expand(elg.subs({sp.diff(uf, rr, 2): Upp}).subs({sp.diff(uf, rr): Up}).subs({uf: U}) * rr ** 2)
eqsS = sp.Poly(elg, Upp, Up, U, rr).coeffs()
solTS0 = sp.solve(eqsT0 + eqsS, list(cS) + list(dS), dict=True)
solTSC = sp.solve(eqsT + eqsS, list(cS) + list(dS), dict=True)
P(f"  T(C=0) alone: {solT0}")
P(f"  T(C=0) + S  : {solTS0}")
P(f"  T(C=0 and C!=0, projected Hessian) + S: {solTSC}")
iso_sub = {cS[2]: 0, cS[3]: 0, cS[4]: 0, dS[1]: 0, dS[2]: 0, dS[3]: 0, dS[4]: 0}
sol_iso = sp.solve([e_.subs(iso_sub) for e_ in eqsT0 + eqsS], [cS[0], cS[1], dS[0]], dict=True)
P(f"  n-independent (isotropic) subfamily under T(C=0) + S: {sol_iso}  "
  f"(record normalisation gamma/(2K^2) = {gam/(2*Ksym**2)})")
RES["L1"] = dict(T0=str(solT0), TS0=str(solTS0), TSC=str(solTSC), isotropic=str(sol_iso))

# ============================================================================================== L2: family (x), P938 floor
P("\n[L2] family (x): a (Delta_u chi)^2 + b |TL(DD + beta_s K C)|^2  [Lagrangian -(...)]")
Scond = sp.solve(sp.Eq(fam_ratio, 1), bF)
P(f"  S (static spherical = record): b = {Scond}")
dvf = sp.factor(B1["fam"]["tt"]["+"]["dv2_per_L2"])
P(f"  T (B1a, first order, per L*^2): d(v^2) = {dvf}  [x pol: {sp.factor(B1['fam']['tt']['x']['dv2_per_L2'])}]")
T2f = HLTH["fam"]["P938"]["T2"]
T2fi = HLTH["fam"]["P_int"]["T2"]
P(f"  H[P938]: omega^2 k^2 coefficients [xi1, xi2, xi3] = {[sp.factor(T2f[i, i]) for i in range(3)]}")
P(f"  H[P_int]: omega^2 k^2 coefficients [xi1, xi2, xi3] = {[sp.factor(T2fi[i, i]) for i in range(3)]}")
QTf = sp.factor(B2["fam"]["+"]["QT"])
P(f"  tensor Q_T on FRW: {QTf}")
# numerical scan for the P938 floor: minimise |d(v^2)| at C = 0 over (a, beta_s) with S and H[P938]
floor = None
grid_a = np.linspace(-2.0, 1.5, 351)
grid_b = np.linspace(-1.0, 2.0, 301)
gK = {gam: 1, Ksym: 1}
bexpr = Scond[0] if Scond else None
fT2 = [sp.lambdify((aF, bF, bsF, Cc, rho0), T2f[i, i].subs(gK), "numpy") for i in range(3)]
fdv = sp.lambdify((aF, bF, bsF, uu, ct), sp.expand(B1["fam"]["tt"]["+"]["dv2_per_L2"].subs(gK).subs(Cc, 0)), "numpy")
fdvx = sp.lambdify((aF, bF, bsF, uu, ct), sp.expand(B1["fam"]["tt"]["x"]["dv2_per_L2"].subs(gK).subs(Cc, 0)), "numpy")
fb = sp.lambdify(aF, bexpr.subs(gK), "numpy") if bexpr is not None else None
best = None
for a_ in grid_a * 0.5:                                          # units of gamma/(2K^2) = 0.5 here
    b_ = float(fb(a_))
    for bs_ in grid_b:
        h_ok = all(float(np.real(f_(a_, b_, bs_, 1.0, 1.0))) >= -1e-12 for f_ in fT2)
        if not h_ok:
            continue
        dv = max(abs(float(fdv(a_, b_, bs_, 1.0, c_))) for c_ in (1.0, 0.5, 0.0)) if True else 0
        dv = max(dv, max(abs(float(fdvx(a_, b_, bs_, 1.0, c_))) for c_ in (1.0, 0.5, 0.0)))
        if best is None or dv < best[0]:
            best = (dv, a_, b_, bs_)
if best:
    P(f"  P938 floor (grid a in [-1, 0.75] gamma/K^2, beta_s in [-1, 2]; S and H[P938] imposed): "
      f"min max|d(v^2)|/(L*^2 u^2) = {best[0]:.4f} at a = {best[1]:.3f}, b = {best[2]:.3f}, beta_s = {best[3]:.3f} (gamma = K = 1)")
RES["L2"] = dict(S=str(Scond), dv2=str(dvf), H938=[str(sp.factor(T2f[i, i])) for i in range(3)],
                 Hint=[str(sp.factor(T2fi[i, i])) for i in range(3)], QT=str(QTf),
                 floor_P938=None if best is None else dict(coef=best[0], a=best[1], b=best[2], beta_s=best[3]))
P(f"  [{time.time()-T0:6.1f} s, peak RSS {rss_bytes()/1e9:.2f} GB]")

# ============================================================================================== O(k^0) remainder bound for trace terms
fk = 2 * math.pi * 100.0 / C_SI
rem = {}
for foot in FOOTS:
    cs = CubicSpline(Rm, LAW[foot]["u"])
    rhoc = (cs(Rm, 1) + 2 * cs(Rm) / Rm) / K_SI
    rmax = float(np.max(np.abs(rhoc)))
    umax = float(np.max(LAW[foot]["u"]))
    rem[foot] = {lk: dict(stiff=Ls ** 2 * (K_SI * rmax) ** 2 / (fk ** 2 * C_SI ** 4), W=A0[foot] * umax / (fk ** 2 * C_SI ** 4))
                 for lk, Ls in LSTAR.items()}
P(f"\n[N] O(k^0) remainder at 100 Hz (order of magnitude, report only): stiffness L*^2(K rho_c)^2/(k^2 c^4) <= "
  f"{max(rem[f][l]['stiff'] for f in FOOTS for l in LSTAR):.1e}; W a0 u/(k^2 c^4) <= {max(rem[f][l]['W'] for f in FOOTS for l in LSTAR):.1e}")
RES["numbers"]["k0_remainder_100Hz"] = rem

# ============================================================================================== labels and verdict
P("\n" + "=" * 118)
P("LABELS per candidate  (T: principal d(c_T^2) == 0 in B1a, B1b (both parents) and B2;  S: static EL identical and "
  "C2 <= 1e-9;  F: square of a quantity vanishing on FRW;  O: omega-degree <= 2 and no h_ttt;  H[P])")
LAB = {}
for cn in CANDS:
    Tb1 = B1[cn]["principal_zero"] and not B1[cn]["mixes"]
    Tb2 = all(sp.simplify(B2[cn][pol]["cT2"] - 1) == 0 for pol in ("+", "x"))
    T_ = Tb1 and Tb2
    S_ = bool(STATIC[cn]["S"])
    bgv = sp.simplify(FRWV[cn])
    # F: value AND first variation vanish on FRW: background value zero and the quantity squared vanishes there
    F_ = (bgv == 0) and cn not in ("vii",)
    if cn == "vii":
        F_ = False
    O_ = all(HLTH[cn][p]["omega_degree_after_constraint"] <= 2 for p in ("P938", "P_int")) and \
         all(not B2[cn][pol]["high"] for pol in ("+", "x"))
    Hh = {}
    for par in ("P938", "P_int"):
        T2m = HLTH[cn][par]["T2"]
        sb = {Ksym: 1, gam: 1, rho0: 1, Cc: sp.Rational(1, 2), uu: 0}
        ev = [float(sp.N(T2m[i, i].subs(sb))) for i in range(3)]
        tens = True
        for zz in (0.0, 10.0):
            for lk, Ls in LSTAR.items():
                dct = FRWN[cn][f"z={zz:g}"][lk]
                tens &= (1 + 2 * dct) > 0
        Hh[par] = all(e_ >= -1e-12 for e_ in ev) and tens
    LAB[cn] = dict(T=T_, S=S_, F=F_, O=O_, H_P938=Hh["P938"], H_Pint=Hh["P_int"], FRW_background=str(bgv))
    P(f"  ({cn:8s}) T={T_!s:5s} S={S_!s:5s} F={F_!s:5s} O={O_!s:5s} H[P938]={Hh['P938']!s:5s} H[P_int]={Hh['P_int']!s:5s}"
      f"   FRW value = {sp.factor(bgv)}")
RES["labels_final"] = LAB
exists = [c for c in LAB if LAB[c]["T"] and LAB[c]["S"] and LAB[c]["F"] and LAB[c]["O"]]
sfo = [c for c in LAB if LAB[c]["S"] and LAB[c]["F"] and LAB[c]["O"]]
if exists:
    parts = []
    for c in exists:
        hp_ = [p for p in ("P938", "P_int") if LAB[c][f"H_{p}" if p == "P938" else "H_Pint"]]
        parts.append(f"{c} [{DESC[c]}] HEALTHY in {hp_ if hp_ else 'none'}")
    verdict = "EXISTS: " + "; ".join(parts)
    if not any(LAB[c]["H_P938"] for c in exists):
        fl = RES["L2"]["floor_P938"]
        verdict += f" | APPROXIMATE[P938]: floor max|d(c_T^2/c^2)| = {fl['coef']:.4f} L*^2 u^2/c^4 (family x, S+F+O+H[P938])" if fl else ""
elif sfo:
    flo = min(sfo, key=lambda c: abs(WALL[c]["coef_max_per_L2u2"]))
    verdict = f"APPROXIMATE: floor {abs(WALL[flo]['coef_max_per_L2u2']):.4f} L*^2 u^2/c^4 ({flo})"
else:
    verdict = "NO-GO (see L1/L2)"
P("\nVERDICT: " + verdict)
RES["verdict"] = verdict

# ============================================================================================== MUTATE teeth
if MUT:
    P("\nMUTATE teeth")
    mu1 = abs(float(B1["v_MU1"]["tt"]["+"]["dv2_per_L2"].subs({Cc: 0, uu: 1, ct: sp.Rational(1, 2)})) - 0.015) < 1e-12 and not LAB["v_MU1"]["T"]
    mu2 = sp.simplify(FRWV["v_MU2"]) != 0 and not LAB["v_MU2"]["F"]
    mu3 = abs(C2["v_MU3"]["max_rel"] - 1.0) < 1e-9 and not LAB["v_MU3"]["S"]
    mu4 = sp.simplify(B2["v_MU4"]["+"]["cT2"] - 1) != 0
    # MU5: (v)'s health with C = 0 (rebuild (v) only for the tooth)
    Nv = fourier(tr(-kinB.sqrtmg * S_cand("v", kinB)).coeff(eps, 2))
    Nx = (N_dust + Nv + N_938)
    A_ = Nx.extract([2, 3, 4], [2, 3, 4]); B_ = Nx.extract([2, 3, 4], [5, 6]); C_ = Nx.extract([5, 6], [2, 3, 4]); D_ = Nx.extract([5, 6], [5, 6])
    Nxi = (A_ - B_ * D_.LUsolve(C_)).applyfunc(lambda e_: sp.expand(sp.cancel(e_)))
    T2v = Nxi.applyfunc(lambda e_: sp.expand(sp.diff(e_, wS, 2) / 2).subs(wS, 0).coeff(kS, 2))
    ev_on = [float(sp.N(T2v[i, i].subs({Ksym: 1, gam: 1, rho0: 1, Cc: sp.Rational(1, 2), uu: 0}))) for i in range(3)]
    ev_off = [float(sp.N(T2v[i, i].subs({Ksym: 1, gam: 1, rho0: 1, Cc: 0, uu: 0}))) for i in range(3)]
    mu5 = min(ev_on) < 0 and min(ev_off) >= 0
    teeth = dict(MU1=mu1, MU2=mu2, MU3=mu3, MU4=mu4, MU5=mu5)
    for k_, v_ in teeth.items():
        chk(f"{k_}_bites", v_, {"MU1": "(v)+0.01(i): d(v^2) = 0.015 L*^2u^2 and T lost",
                                 "MU2": "D^2chi + 0.9 theta C: FRW value != 0 and F lost",
                                 "MU3": "(v) x 2: C2 relative difference 1.0 and S lost",
                                 "MU4": "(v)+(vi-b) on FRW: c_T != c",
                                 "MU5": f"(v) health: omega^2k^2 eig with C=1/2 {ev_on}, with C=0 {ev_off}"}[k_])
    RES["teeth"] = teeth
    code = 1 if all(teeth.values()) else 2
else:
    kall = all(RES["checks"][k_]["pass"] for k_ in RES["checks"] if k_.startswith("K"))
    code = 0 if kall else 1
    P(f"\ncontrols K1-K6 all pass: {kall}")

P(f"\nruntime {time.time()-T0:.1f} s, peak RSS {rss_bytes()/1e9:.3f} GB; exit {code}")
RES["runtime_s"] = time.time() - T0
RES["peak_rss_GB"] = rss_bytes() / 1e9


def _ser(o):
    if isinstance(o, dict):
        return {str(k_): _ser(v_) for k_, v_ in o.items()}
    if isinstance(o, (list, tuple)):
        return [_ser(v_) for v_ in o]
    if isinstance(o, (bool, int, float, str)) or o is None:
        return o
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    return str(o)


RES["static"] = {c: {k_: v_ for k_, v_ in STATIC[c].items() if k_ != "EL"} for c in STATIC}
RES["B1"] = {c: {"principal_zero": B1[c]["principal_zero"], "mixes": B1[c]["mixes"], "offdiag": B1[c]["offdiag"]} for c in B1}
RES["health"] = {c: {p: {k_: v_ for k_, v_ in HLTH[c][p].items() if k_ not in ("T2", "T0", "Tfull")} for p in ("P938", "P_int")}
                 for c in HLTH}
RES["B2"] = {c: {pol: {k_: str(v_) for k_, v_ in B2[c][pol].items()} for pol in B2[c]} for c in B2}
with open(JSON_PATH, "w") as fh:
    json.dump(_ser(RES), fh, indent=1)
_f.close()
sys.exit(code)

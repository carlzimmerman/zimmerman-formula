"""
mc_reduce_static.py -- REDUCTION A: static plane-symmetric quasistatic weak field.

Why plane symmetry:  in plane symmetry the exact vacuum MOND solution has CONSTANT
field gradients (a sheet of surface density Sigma gives g_N = 2 pi G Sigma independent of
z, and mu(g/a0) g = g_N still gives a constant g).  So the uniform-gradient jet is EXACT
for the vacuum region -- it is not a linearisation of the MOND nonlinearity, which is
retained in full.

Ansatz
------
    g_mn = diag( -(1+2 Phi), 1-2 Psi - E, 1-2 Psi - E, 1-2 Psi + 2 E )       (E = traceless probe)
    A_mu = (A0, 0, 0, Az)
    S_mn : S_00, S_zz, S_xx = S_yy = (S_00 - S_zz)/2   (flat tracelessness), S_0z = 0
    phi, chi, lam scalars ;  all fields functions of z only.

Bookkeeping
-----------
    * the Lagrangian density sqrt(-g) L is truncated at SECOND order in the metric
      potentials (Phi, Psi, E) and kept EXACT in the carrier.  This is the standard
      post-Newtonian counting: the MOND nonlinearity lives in the carrier sector
      (|grad phi| ~ a0), not in the metric potentials.
    * generalised momentum (operators contain up to two derivatives):
          P_f = dL/df' - d/dz( dL/df'' ),      Q_f = dL/df
      with d/dz acting by the chain rule on the first-order jet (f'' = 0).
    * VACUUM equations (rho = 0 outside the sheet):
          Q_f = 0                                  for every carrier field
          P_f = -(Sigma/2) d sqrt(-g~_00)/df       flux matching across the sheet
      This is EXACT for the archetype class (algebraic constitutive carrier: the
      neglected piece dP_f/dz vanishes identically there) and is reported as a
      DIAGNOSTIC residual otherwise -- never silently assumed.
    * the two Einstein equations EL_Phi = EL_Psi = 0 are NOT imposed: in vacuum they are
      the carrier's vacuum-energy (cosmological-constant) conditions, assumed separately
      tuned.  Their residuals are returned as diagnostics.

Outputs per operator (the columns of the reduction matrix M):
    eq 0..5   Q_chi, Q_A0, Q_Az, Q_S00, Q_Szz, Q_lam
    eq 6..12  P_phi, P_chi, P_A0, P_Az, P_S00, P_Szz, P_lam
    eq 13..14 P_Phi, P_Psi
    col 15    Sigma_P  =  EL_E  at E = 0   (the traceless metric stress: Part-I's object)
"""
import os
import pickle
import sympy as sp
from mc_core import Ctx, trunc_eps, EPS
from mc_basis import OPS, N_OPS

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache_static.pkl")

z = sp.Symbol('z')
COORDS = [sp.Symbol('t'), sp.Symbol('x'), sp.Symbol('y'), z]

# field name -> (function, jet symbols f0,f1,f2)
FIELDS = ["Phi", "Psi", "E", "phi", "chi", "A0", "Az", "S00", "Szz", "lam"]

# unknowns of the numeric solve (15)
UNKNOWNS = ["Phi1", "Psi1", "phi1", "chi0", "chi1", "A00", "A01", "Az0", "Az1",
            "S000", "S001", "Szz0", "Szz1", "lam0", "lam1"]
N_UNK = len(UNKNOWNS)

EQ_NAMES = ["Q_chi", "Q_A0", "Q_Az", "Q_S00", "Q_Szz", "Q_lam",
            "P_phi", "P_chi", "P_A0", "P_Az", "P_S00", "P_Szz", "P_lam",
            "P_Phi", "P_Psi"]
N_EQ = len(EQ_NAMES)
SIGP_COL = N_EQ            # column index of Sigma_P
N_COL = N_EQ + 1


def _jet(name):
    f = sp.Function(name)(z)
    return f, sp.Symbol(name + "0"), sp.Symbol(name + "1"), sp.Symbol(name + "2")


MPAR = sp.symbols('m1 m2 m3 m4 m5 m6 m7 m8')


def build_sources(s0):
    """Matter-frame source terms  d sqrt(-g~_00) / d f  (see mc_basis.MFRAME).

    g~_mn = e^{2(m1 phi + m2 chi)} [ g_mn + (m3+m5 phi) A_m A_n + (m4+m6 phi) S_mn
                                          + (m7+m8 phi) d_m phi d_n phi ]
    The d_m phi d_n phi piece has no 00-component for a STATIC configuration, so it does
    not enter the source; it does enter the spatial metric (handled in mc_gates).
    """
    m1, m2, m3, m4, m5, m6, m7, m8 = MPAR
    ph, ch = s0["phi"], s0["chi"]
    conf = 1 + 2 * (ph * m1 + ch * m2)
    base00 = -(1 + 2 * s0["Phi"]) + (m3 + m5 * ph) * s0["A0"]**2 + (m4 + m6 * ph) * s0["S00"]
    W = -conf * base00
    sqW = sp.sqrt(W)
    out = []
    for nm in ["phi", "chi", "A0", "Az", "S00", "Szz", "lam", "Phi", "Psi"]:
        out.append(sp.diff(sqW, s0[nm]))
    return [sp.simplify(e.subs({s0["Phi"]: 0, s0["phi"]: 0})) for e in out]


def build():
    fn, s0, s1, s2 = {}, {}, {}, {}
    for nm in FIELDS:
        f, a, b, c = _jet(nm)
        fn[nm], s0[nm], s1[nm], s2[nm] = f, a, b, c

    Phi, Psi, E = fn["Phi"], fn["Psi"], fn["E"]
    # the bookkeeping parameter is built INTO the ansatz -- never substituted in later
    # (subs() into Derivative objects silently destroys terms; see mc_core.trunc_eps)
    ep = EPS
    g = sp.diag(-(1 + 2 * ep * Phi), 1 - 2 * ep * Psi - ep * E,
                1 - 2 * ep * Psi - ep * E, 1 - 2 * ep * Psi + 2 * ep * E)

    A = [fn["A0"], sp.S.Zero, sp.S.Zero, fn["Az"]]
    S00f, Szzf = fn["S00"], fn["Szz"]
    Sxx = (S00f - Szzf) / 2
    S = sp.diag(S00f, Sxx, Sxx, Szzf)

    # truncate the inverse metric / sqrt(-g) at 3rd order so that products with one more
    # potential are still correct at 2nd order after the final truncation
    ctx = Ctx(COORDS, g, fn["phi"], fn["chi"], A, S, fn["lam"], build_curvature=True,
              trunc=lambda e: trunc_eps(e, 3))

    # ---- helper: expression -> jet symbols ----
    subs_map = []
    for nm in FIELDS:
        subs_map.append((sp.Derivative(fn[nm], (z, 2)), s2[nm]))
        subs_map.append((sp.Derivative(fn[nm], z), s1[nm]))
    for nm in FIELDS:
        subs_map.append((fn[nm], s0[nm]))

    def to_jet(expr):
        e = expr
        for a, b in subs_map:
            e = e.subs(a, b)
        e = sp.expand(e.doit())
        left = e.atoms(sp.Derivative) | e.atoms(sp.Function)
        if left:
            raise RuntimeError(f"unreduced objects survive the jet map: {left}")
        return e

    allsyms = ([s0[n] for n in FIELDS] + [s1[n] for n in FIELDS] + [s2[n] for n in FIELDS])

    def Dz(expr):
        """total d/dz on the first-order jet (second derivatives already set to zero)."""
        out = sp.S.Zero
        for nm in FIELDS:
            out += sp.diff(expr, s0[nm]) * s1[nm] + sp.diff(expr, s1[nm]) * s2[nm]
        return out

    ibp_passes = {}

    def to_first_order(J, tag=""):
        """Remove ALL second-derivative dependence by subtracting total derivatives.

        For a Lagrangian L(f, f', f'') that is linear in f'',
            L1 = L - d/dz[ (dL/df'') f' ]
        has the same Euler-Lagrange equations but is first order, so the momentum
        P_f = dL1/df' is the flux whose JUMP across a delta-function source gives the
        boundary condition (with the second-order form dL/df itself contains f'' and is
        delta-like -- the failure mode that made pure GR come out as Psi' = Phi'/4).
        """
        for npass in range(8):
            c2 = {nm: sp.diff(J, s2[nm]) for nm in FIELDS}
            if all(c == 0 for c in c2.values()):
                ibp_passes[tag] = npass
                return sp.expand(J)
            for nm in FIELDS:
                c = c2[nm]
                if c == 0:
                    continue
                J = sp.expand(J - (Dz(c) * s1[nm] + c * s2[nm]))
        # residual higher-derivative structure: drop it under the uniform-gradient
        # truncation and RECORD that this happened (never silent)
        left = {nm for nm in FIELDS if sp.diff(J, s2[nm]) != 0}
        ibp_passes[tag] = ("TRUNCATED", sorted(left))
        return sp.expand(J.subs({s2[nm]: 0 for nm in FIELDS}))

    # on-shell truncation applied AFTER all differentiations
    onshell = {}
    for nm in FIELDS:
        onshell[s2[nm]] = 0
    onshell[s0["Phi"]] = 0
    onshell[s0["Psi"]] = 0
    onshell[s0["E"]] = 0
    onshell[s1["E"]] = 0
    onshell[s0["phi"]] = 0       # shift symmetry: bare phi never appears (asserted below)

    def reduce_one(Lexpr, tag=""):
        """returns the N_COL outputs for one Lagrangian scalar L (density = sqrt(-g) L)."""
        dens = ctx.sqrtg * Lexpr
        dens = trunc_eps(dens, 2).subs(EPS, 1)
        J = to_first_order(to_jet(dens), tag)

        Q = {nm: sp.diff(J, s0[nm]) for nm in FIELDS}
        P = {nm: sp.diff(J, s1[nm]) for nm in FIELDS}

        out = [Q["chi"], Q["A0"], Q["Az"], Q["S00"], Q["Szz"], Q["lam"],
               P["phi"], P["chi"], P["A0"], P["Az"], P["S00"], P["Szz"], P["lam"],
               P["Phi"], P["Psi"]]
        # Sigma_P: the full E Euler-Lagrange residual at E = 0
        sigp = Q["E"] - Dz(P["E"])
        out.append(sigp)
        out = [sp.expand(o.subs(onshell)) for o in out]
        # sanity: no bare phi anywhere (shift symmetry of the phi slot)
        return out

    rows = []
    labels = []
    print("  reducing operators ...")
    for k, o in enumerate(OPS):
        Lexpr = o["fn"](ctx)
        rows.append(reduce_one(Lexpr, o['id']))
        labels.append(o["id"])
        print(f"    [{k+1:2d}/{N_OPS}] {o['id']:5s} {o['label'][:52]}")
    # gravity sector, fixed coefficient 1 (units 16 pi G = 1)
    print("    [EH ] R(g)   (fixed, coefficient 1)")
    rows.append(reduce_one(ctx.Rs, "EH"))
    labels.append("EH")

    srcr_syms = build_sources(s0)

    # ---------------- lambdify ----------------
    unk = [sp.Symbol(u) for u in UNKNOWNS]
    # map jet symbols -> unknown symbols
    ren = {
        s1["Phi"]: sp.Symbol("Phi1"), s1["Psi"]: sp.Symbol("Psi1"),
        s1["phi"]: sp.Symbol("phi1"),
        s0["chi"]: sp.Symbol("chi0"), s1["chi"]: sp.Symbol("chi1"),
        s0["A0"]: sp.Symbol("A00"), s1["A0"]: sp.Symbol("A01"),
        s0["Az"]: sp.Symbol("Az0"), s1["Az"]: sp.Symbol("Az1"),
        s0["S00"]: sp.Symbol("S000"), s1["S00"]: sp.Symbol("S001"),
        s0["Szz"]: sp.Symbol("Szz0"), s1["Szz"]: sp.Symbol("Szz1"),
        s0["lam"]: sp.Symbol("lam0"), s1["lam"]: sp.Symbol("lam1"),
    }
    Mrows = [[sp.expand(e.subs(ren)) for e in row] for row in rows]
    srcr = [sp.expand(e.subs(ren)) for e in srcr_syms]

    nontrivial = {k: v for k, v in ibp_passes.items() if v not in (0, 1)}
    print(f"  integration-by-parts passes (non-trivial): {nontrivial}")
    data = dict(labels=labels, ibp_passes={k: str(v) for k, v in ibp_passes.items()},
                Mrows_str=[[sp.srepr(e) for e in r] for r in Mrows],
                src_str=[sp.srepr(e) for e in srcr],
                unknowns=UNKNOWNS, eq_names=EQ_NAMES, n_col=N_COL)
    with open(CACHE, "wb") as fh:
        pickle.dump(data, fh)
    print(f"  symbolic reduction cached -> {CACHE}")
    return _lambdify(labels, Mrows, srcr)


def _lambdify(labels, Mrows, srcr):
    unk = [sp.Symbol(u) for u in UNKNOWNS]
    nrow, ncol = len(Mrows), len(Mrows[0])
    print("  lambdifying reduction matrix ...")
    flat = [Mrows[i][j] for i in range(nrow) for j in range(ncol)]
    Mfun = sp.lambdify(unk, flat, modules="numpy", cse=True)
    print("  lambdifying reduction jacobian ...")
    Jflat = [sp.diff(Mrows[i][j], u) for i in range(nrow) for j in range(ncol) for u in unk]
    Jfun = sp.lambdify(unk, Jflat, modules="numpy", cse=True)
    print("  lambdifying source terms ...")
    Sfun = sp.lambdify(unk + list(MPAR), srcr, modules="numpy", cse=True)
    SJfun = sp.lambdify(unk + list(MPAR),
                        [sp.diff(e, u) for e in srcr for u in unk],
                        modules="numpy", cse=True)
    return dict(labels=labels, Mfun=Mfun, Jfun=Jfun, Sfun=Sfun, SJfun=SJfun,
                shape=(nrow, ncol))


_CACHE_RUNTIME = {}


def load():
    """rebuild the lambdified functions (fast path uses the pickled srepr forms)."""
    if _CACHE_RUNTIME:
        return _CACHE_RUNTIME
    if not os.path.exists(CACHE):
        r = build()
        _CACHE_RUNTIME.update(r)
        return r
    with open(CACHE, "rb") as fh:
        data = pickle.load(fh)
    Mrows = [[sp.sympify(s) for s in r] for r in data["Mrows_str"]]
    # sources are rebuilt FRESH (cheap) so that extending the matter frame never requires
    # redoing the expensive operator reduction
    s0 = {nm: sp.Symbol(nm + "0") for nm in FIELDS}
    ren = {sp.Symbol("chi0"): sp.Symbol("chi0"), sp.Symbol("A00"): sp.Symbol("A00"),
           sp.Symbol("S000"): sp.Symbol("S000")}
    srcr = [sp.expand(e) for e in build_sources(s0)]
    r = _lambdify(data["labels"], Mrows, srcr)
    _CACHE_RUNTIME.update(r)
    return r


if __name__ == "__main__":
    import time
    t0 = time.time()
    build()
    print(f"built in {time.time()-t0:.1f} s -> {CACHE}")

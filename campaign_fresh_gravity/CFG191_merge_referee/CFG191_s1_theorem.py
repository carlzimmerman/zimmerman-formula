#!/usr/bin/env python3
"""CFG191_s1_theorem -- item (a): the no-EFE theorem.  F(z+ze)-F(ze)=F(z) for all z,ze>=0 forces F linear.
Own sympy/mpmath/numpy derivation and tests; no CFG179 file is opened.  MUTATE=1 runs M1 (composition replaced by ownership,
g_int=F(z)) and M2 (anisotropic linear law in the vector test; vector structure dropped) and must exit 1."""
import warnings; warnings.filterwarnings('ignore')
import numpy as np, sympy as sp, mpmath as mp
np.seterr(all='ignore')
from CFG191_common import Run
R = Run("CFG191_s1_theorem", "item (a): the linearity theorem, its premises and its escapes")
MUT = R.mutate
mp.mp.dps = 50

# ---- kernels (Newtonian field z in units of a0 -> observed field F(z) in units of a0)
Fp2  = lambda z: np.sqrt(z*z + z)
Frar = lambda z: z/(1 - np.exp(-np.sqrt(z)))
Fsim = lambda z: z*(1 + np.sqrt(1 + 4/z))/2
mFp2  = lambda z: mp.sqrt(z*z + z)
mFrar = lambda z: z/(1 - mp.exp(-mp.sqrt(z)))
mFsim = lambda z: z*(1 + mp.sqrt(1 + 4/z))/2
def comp(F, z, ze):
    """internal field of a subsystem (Newtonian z) in a uniform host field (Newtonian ze). Difference rule (P2 of the frozen file);
    M1 mutant: ownership rule g_int = F(z)."""
    return F(z) if MUT else F(z + ze) - F(ze)
def resid(F, z, ze):
    return comp(F, z, ze) - F(z)

R.sec("PREMISES (frozen before derivation)")
for s in ["P1 local single-argument law: observed field g = F(z_tot), z_tot the total Newtonian field (units a0)",
          "P2 difference rule (universal free fall): g_int = F(z+ze) - F(ze)",
          "P3 'no EFE' := g_int = F(z) for ALL z, ze >= 0",
          "P4 regularity: F monotone (or measurable, or bounded on an interval); differentiability NOT needed",
          "P5 aligned 1-D fields suffice for the scalar statement; the vector statement needs P3 for every direction pair",
          "P6 F(0)=0 (follows from z=ze=0)"]:
    R.p("  " + s)
if MUT:
    R.p("  MUTATE M1: composition rule replaced by ownership g_int = F(z)  (P2 dropped)")

R.sec("A1  symbolic derivation")
z, ze, c = sp.symbols("z z_e c", positive=True)
Fs = sp.sqrt(z**2 + z)
R.p("  step 0: z=ze=0 in P3 gives F(0)=F(0)+F(0), so F(0)=0 (P6).")
R.p("  step 1: P3 is Cauchy additivity F(x+y)=F(x)+F(y) on the half-line; by induction F(n x)=n F(x), then F(q x)=q F(x) for rational q>0.")
R.p("  step 2: with P4 (monotone, or bounded on an interval, or measurable), F(x)=F(1) x for every real x>0 (sandwich x between rationals for monotone F).")
R.p("          Without P4, Hamel-basis solutions exist (non-measurable; from memory, unverified as a citation); the observed field is monotone in the Newtonian field, so P4 holds.")
R.p("  step 3 (if C1): d/d ze of P3 gives F'(z+ze)=F'(ze); ze->0+ gives F' constant, the same result.")
Fl = c*z
lin_res = sp.simplify(Fl.subs(z, z+ze) - Fl.subs(z, ze) - Fl)
R.check("A1a F=c z satisfies P3 exactly (sympy)", lin_res == 0, f"residual = {lin_res}")
d1 = sp.simplify(sp.diff(Fs, z))
d2 = sp.simplify(sp.diff(Fs, z, 2))
R.p(f"  P2: F' = {d1};  F'' = {d2}")
R.p(f"  F'(0+) = {sp.limit(d1, z, 0, '+')}")
R.check("A1b P2 is strictly concave (F''<0 for z>0, sympy) and F'(0+)=infinity", sp.limit(d1, z, 0, '+') == sp.oo and sp.simplify(d2 + 1/(4*(z**2+z)**sp.Rational(3,2))) == 0,
        "F''=-1/(4 (z^2+z)^(3/2)); strict concavity with F(0)=0 gives STRICT sub-additivity, so the residual has one sign (suppression) for every strictly concave F")
# independence of the closed form: P2 is the inverse of M(x)=(sqrt(1+4x^2)-1)/2
Mfun = lambda x: (mp.sqrt(1 + 4*x*x) - 1)/2
chk_inv = max(abs(Mfun(mFp2(mp.mpf(v))) - mp.mpf(v)) for v in ("0.001", "0.01", "0.1", "1", "10", "100"))
R.check("A1c P2 = inverse of the framework mu-form M(x)=(sqrt(1+4x^2)-1)/2 to 1e-40", chk_inv < mp.mpf("1e-40"), f"max |M(F(z))-z| = {mp.nstr(chk_inv,3)}")
pts = [(a, b) for a in ("0.01", "0.1", "1") for b in ("0.1", "1")]
rows, ok6, agree = [], True, True
for a, b in pts:
    a_, b_ = mp.mpf(a), mp.mpf(b)
    rs = sp.N((Fs.subs(z, sp.Rational(a)+sp.Rational(b)) - Fs.subs(z, sp.Rational(b)) - Fs.subs(z, sp.Rational(a))), 40)
    # route 2: F evaluated by root-finding M(x)=z (independent of the sqrt closed form)
    Finv = lambda zz: mp.findroot(lambda x: Mfun(x) - zz, mp.sqrt(zz*zz+zz))
    rm = Finv(a_+b_) - Finv(b_) - Finv(a_)
    rc = resid(mFp2, a_, b_) if not MUT else mp.mpf(0)
    rows.append((a, b, rs, rm, rc))
    ok6 &= (rs < 0)
    agree &= abs(mp.mpf(str(rs)) - rm) < mp.mpf("1e-30")
R.p("  six declared points: r(z,ze)=F(z+ze)-F(ze)-F(z)   [sympy exact->40 digits | root-finding of M(x)=z | rule as run]")
for a, b, rs, rm, rc in rows:
    R.p(f"    z={a:>5} ze={b:>4}:  {sp.N(rs,14)!s:>22} | {mp.nstr(rm,14):>22} | {mp.nstr(rc,14):>22}")
R.check("A1d P2 residual is negative at all six declared points (sympy) and the two evaluations agree to 1e-30", ok6 and agree)
R.check("A1e [M1] merged P2 rivers interact under the composition rule as run: residual nonzero at all six points",
        all(abs(rc) > mp.mpf("1e-6") for *_, rc in rows), "under the ownership mutant the residual is identically 0")
R.data["six_points"] = [dict(z=a, ze=b, r_sympy=float(rs), r_root=float(rm), r_run=float(rc)) for a, b, rs, rm, rc in rows]

R.sec("A2  strict sub-additivity on a 200 x 200 log grid, mpmath 50 digits")
zg = [mp.mpf(10)**(mp.mpf(-3) + mp.mpf(6)*i/199) for i in range(200)]
res_tab = {}
for nm, Fm, cw in (("P2", mFp2, 1), ("nu_RAR z", mFrar, 1), ("nu_simple z", mFsim, 1), ("linear 2z (control)", lambda x: 2*x, 0)):
    Fz = [Fm(v) for v in zg]
    mx, mn = mp.mpf("-inf"), mp.mpf("inf")
    for i, a in enumerate(zg):
        for j, b in enumerate(zg):
            r = (Fm(a+b) - Fz[j]) - Fz[i] if not MUT else mp.mpf(0)
            mx = max(mx, r); mn = min(mn, r)
    # concavity by exact mp derivative at 200 points
    concave = all(mp.diff(Fm, v, 2) < 0 for v in zg[::4])
    res_tab[nm] = (mx, mn, concave)
    R.p(f"  {nm:22s}: max r = {mp.nstr(mx,4):>12}  min r = {mp.nstr(mn,4):>12}   F''<0 on the grid sample: {concave}")
R.check("A2a control: linear F=2z has |r|<1e-40 everywhere", max(abs(res_tab["linear 2z (control)"][0]), abs(res_tab["linear 2z (control)"][1])) < mp.mpf("1e-40"))
for nm in ("P2", "nu_RAR z", "nu_simple z"):
    mx, mn, cc = res_tab[nm]
    R.check(f"A2b {nm}: max r < 0 on the whole grid" + ("" if cc else "  (kernel is NOT concave on the sampled range; check is informational)"), mx < 0, f"max r = {mp.nstr(mx,4)}", lb=(nm == "P2") or cc)
R.data["A2"] = {k: dict(max=float(v[0]), min=float(v[1]), concave=bool(v[2])) for k, v in res_tab.items()}
R.p("  nu_mono: closed form not unambiguous from the documents I read; NOT RUN (declared).")

R.sec("A3  the 3D-vector form")
rng = np.random.default_rng(191)
def G_p2(x):
    n = np.linalg.norm(x, axis=-1, keepdims=True)
    return Fp2(n)*x/np.maximum(n, 1e-300)
Aan = np.array([[2.0, 0.5, 0.0], [0.5, 1.0, 0.3], [0.0, 0.3, 0.6]])
G_lin = lambda x: x @ Aan.T
def rand_dirs(n):
    v = rng.standard_normal((n, 3)); return v/np.linalg.norm(v, axis=1, keepdims=True)
def pair_sets(n, trivial=False):
    ma = 10**rng.uniform(-2, 1, n); mb = 10**rng.uniform(-2, 1, n)
    da = rand_dirs(n); db = rand_dirs(n)
    a = ma[:, None]*da; b = mb[:, None]*db
    k = n//10
    b[:k] = mb[:k, None]*da[:k]                       # parallel
    b[k:2*k] = -mb[k:2*k, None]*da[k:2*k]             # anti-parallel
    perp = np.cross(da[2*k:3*k], rand_dirs(k)); perp /= np.linalg.norm(perp, axis=1, keepdims=True)
    b[2*k:3*k] = mb[2*k:3*k, None]*perp               # perpendicular
    keep = (np.abs(np.log(ma/mb))[:, None] > 0.02).ravel() | (np.arange(n) < k) | (np.arange(n) >= 2*k)
    if trivial:
        b[:] = 0.0
    return a, b
def vec_resid(G, a, b):
    Rv = (G(a+b) - G(b) - G(a)) if not MUT or G is not G_p2 else G(a) - G(a)
    return np.linalg.norm(Rv, axis=1)/np.linalg.norm(G(a), axis=1)
a, b = pair_sets(200000)
ratio_b = np.linalg.norm(b, axis=1)/np.linalg.norm(a, axis=1)
sel = ratio_b >= 1e-2
if not MUT:
    rr = vec_resid(G_p2, a, b)
    R.p(f"  P2 vector law, {sel.sum()} pairs (|b|/|a|>=1e-2): min |R|/|G(a)| = {rr[sel].min():.3e}, median {np.median(rr[sel]):.3e}; fraction < 1e-6: {np.mean(rr[sel]<1e-6):.4f}")
    R.check("A3a P2: min |G(a+b)-G(b)-G(a)|/|G(a)| > 1e-6 over all sampled pairs (incl. parallel, anti-parallel, perpendicular)", rr[sel].min() > 1e-6)
    par = slice(0, 20000)
    z1 = np.linalg.norm(a[par], axis=1); z2 = np.linalg.norm(b[par], axis=1)
    one_d = np.abs(Fp2(z1+z2) - Fp2(z2) - Fp2(z1))
    vec = np.linalg.norm(G_p2(a[par]+b[par]) - G_p2(b[par]) - G_p2(a[par]), axis=1)
    R.check("A3b aligned pairs reproduce the 1-D residual exactly", np.max(np.abs(vec-one_d)) < 1e-12, f"max diff {np.max(np.abs(vec-one_d)):.2e}")
    # perpendicular set explicitly
    pk = slice(40000, 60000); rp = rr[pk]
    R.p(f"  perpendicular pairs: min ratio {rp.min():.3e}; anti-parallel pairs: min ratio {rr[20000:40000].min():.3e}")
else:
    # M2: (i) the law replaced by an anisotropic linear map; (ii) vector structure dropped (only trivial pairs)
    Rv = np.linalg.norm(G_lin(a+b) - G_lin(b) - G_lin(a), axis=1)/np.linalg.norm(G_lin(a), axis=1)
    R.p(f"  M2(i) anisotropic linear G=Ax: min |R|/|G(a)| = {Rv[sel].min():.3e} (additive: residual is rounding only)")
    R.check("A3a [M2 i] the vector test detects non-additivity (min ratio > 1e-6) -- must FAIL for the linear map", Rv[sel].min() > 1e-6)
    a0_, b0_ = pair_sets(20000, trivial=True)
    Rt = np.linalg.norm(G_p2(a0_+b0_) - G_p2(b0_) - G_p2(a0_), axis=1)/np.linalg.norm(G_p2(a0_), axis=1)
    R.p(f"  M2(ii) vector structure dropped (b=0 only): max ratio {Rt.max():.3e}")
    R.check("A3a' [M2 ii] the P2 residual is detected with the trivial pair set (min ratio > 1e-6) -- must FAIL", Rt.min() > 1e-6)
# isotropy step: a continuous additive G is R-linear (Cauchy on each component); rotational covariance then forces G=c*Id (Schur).
R.p("  symbolic step: additive+continuous G:R^3->R^3 => G(x)=A x (Cauchy applied along a basis); G(Rx)=R G(x) for all rotations R => A commutes with SO(3) => A=c*Id.")
R.p("  without the isotropy premise every linear map A survives (anisotropic linear laws); none is sqrt-like (V^2 ~ M).")

R.sec("A4  escape catalogue: residual test and deep-regime scaling (V^4 ~ M requires F ~ z^(1/2) at small z)")
zs, zes = np.array([0.01, 0.1, 1.0, 10.0]), np.array([0.1, 1.0, 10.0])
def slope(F, z0=1e-6): return (np.log(F(z0*1.01)) - np.log(F(z0)))/np.log(1.01)
def maxrel(Ffun, ownership=False):
    out = 0.0
    for zz in zs:
        for zz_e in zes:
            r = (Ffun(zz) if ownership else Ffun(zz+zz_e) - Ffun(zz_e)) - Ffun(zz)
            out = max(out, abs(r)/Ffun(zz))
    return out
cat = []
cat.append(("(i) ownership composition g_int=F(z), F=P2", maxrel(Fp2, True), slope(Fp2), "nonlocal (acts on the system's own field)"))
cat.append(("(ii) anisotropic linear G=Ax (scalar cut along x)", 0.0, 1.0, "local, linear, no BTFR"))
cat.append(("(iii) linear-in-source, non-Newtonian kernel, F=c z", maxrel(lambda x: 3*x), 1.0, "local, linear, V^2~M"))
def screened(u):
    s = u*u/(1+u*u)
    return lambda x: x*(1-s) + s*Fp2(x)
for u in (0.01, 0.3, 3.0, 100.0):
    cat.append((f"(iv) screened F=z+(P2-z)s(r/xi), r/xi={u:g}", maxrel(screened(u)), slope(screened(u)), "r-dependent (Arm B / chain class)"))
cat.append(("(vi) P2 difference rule (the law refereed)", maxrel(Fp2), slope(Fp2), "local; EFE present"))
R.p(f"  {'law':54s} {'max |r|/F(z)':>14s} {'small-z slope':>14s}  note")
for nm, mr, sl, note in cat:
    R.p(f"  {nm:54s} {mr:14.3e} {sl:14.3f}  {note}")
# E7 composition
def E7x(b, e7):
    rts = np.roots([1.0, e7, -b*(b+1), -b*b*e7]); pos = [r.real for r in rts if abs(r.imag) < 1e-12 and r.real > 0]
    assert len(pos) == 1
    return pos[0]
e7r = [(b, ge, E7x(b, np.sqrt(2)*ge)/Fp2(b)) for b in (0.01, 0.1, 1.0) for ge in (0.048, 0.845, 1.9)]
R.p("  (vi') E7 (MI worldline composition) x_E7(b,e7)/F_P2(b) with e7=sqrt2 g_ext: " + "; ".join(f"b={b} g={ge}: {v:.3f}" for b, ge, v in e7r))
R.data["catalogue"] = [dict(law=n, maxrel=m, slope=s, note=t) for n, m, s, t in cat]
zero_and_sqrt = [n for n, m, s, t in cat if m < 1e-12 and abs(s - 0.5) < 0.05]
zero_any = [n for n, m, s, t in cat if m < 1e-12]
R.p("  laws with residual 0 (no EFE): " + " | ".join(zero_any))
R.p("  laws with residual 0 AND a sqrt regime (slope 0.5) at the same scale: " + " | ".join(zero_and_sqrt))
R.check("A4a only the ownership composition has residual 0 together with a sqrt small-z regime", zero_and_sqrt == [cat[0][0]] , lb=True)
R.check("A4b at least two further escape classes pass the residual test (linear anisotropic; linear-kernel; screened at small r/xi) but have no sqrt regime at that scale", len([n for n, m, s, t in cat if m < 1e-3 and abs(s-0.5) > 0.2]) >= 2)
R.check("A4c the screened law's residual tends to 0 as r/xi->0 and to the P2 residual as r/xi->infinity", cat[3][1] < 0.1*cat[-2][1] and abs(cat[6][1] - cat[-1][1])/cat[-1][1] < 0.02)
R.check("A4d E7 also has an EFE (ratio<1 at all tested (b,g_ext))", all(v < 0.999 for *_, v in e7r))

R.sec("A5  size of the EFE for P2: survival x_merge/x_iso (1-D) and E7 -- README line T")
def zinv(g):   # Newtonian field with observed field g
    return (-1 + np.sqrt(1 + 4*g*g))/2
tgt = {("MW Sun 1.9", 0.01): (0.10, 0.12), ("MW Sun 1.9", 0.1): (0.31, 0.36), ("MW Sun 1.9", 1.0): (0.72, 0.81),
       ("Coma 0.845", 0.01): (0.12, 0.15), ("SPARC 0.048", 0.01): (0.63, 0.72)}
gext = {"MW Sun 1.9": 1.9, "Coma 0.845": 0.845, "SPARC 0.048": 0.048}
okA, okE = True, True
for (nm, b), (t1, t7) in tgt.items():
    zeq = zinv(gext[nm])
    r1 = comp(Fp2, b, zeq)/Fp2(b)
    r7 = E7x(b, np.sqrt(2)*gext[nm])/Fp2(b)
    okA &= abs(r1 - t1) <= 0.02; okE &= abs(r7 - t7) <= 0.02
    R.p(f"  {nm:12s} b={b:<5}: 1-D {r1:.3f} (README {t1:.2f})   E7 {r7:.3f} (README {t7:.2f})")
R.check("A5a 1-D survival ratios within 0.02 of the README values (five rows)", okA)
R.check("A5b E7 survival ratios within 0.02 of the README values (five rows)", okE, lb=False)

R.sec("VERDICT (frozen rule)")
a4 = all(c["ok"] for c in R.checks if c["label"].startswith("A4"))
R.finding("(a) theorem", "AGREES WITH QUALIFICATION" if (not MUT and a4) else "see checks",
          "Theorem reproduced with premises P1-P6. Within CFG179's own scope (a law that keeps a sqrt regime at the scale in question) only an ownership-type nonlocal composition escapes: A4a. "
          "The wording 'only B escapes' omits that laws which are Newtonian/linear at the scale (screened, r-dependent laws such as Arm B and the chain; linear-in-source laws) also have zero residual; they escape by not having the sqrt pull there. "
          "It also omits premise P2 (universal free fall / difference rule): E7 is a composition outside P2 and still has an EFE (A4d).")
R.finish()

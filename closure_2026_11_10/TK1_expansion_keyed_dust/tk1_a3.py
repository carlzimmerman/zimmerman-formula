"""TK1 A2 + A3: FRW limit and the top-hat through turnaround (criteria 98f2ab2b6e).

A3 model: closed FRW patch (homogeneous inside, so A = 0 and P = 0), baryons + clock charge in form B's cosmic ratio,
adiabatic, growing mode at z_i = 200. Friedmann constraint from the unitary-gauge N-equation (KA2):
    H^2 + k/a^2 = x_r + x_b + x_L + xK(3H, Om_n),  xK = Om_n + 0.75 Om_n^2/M_2 (1 + theta M_2'/M_2),
with the charge n a^3 conserved and Q - 1 = 1.5 Om_n / M_2 exactly (H0 = 1 units). H is the unique positive root.
Lines s1 (divergence), s2 (velocity Hessian degenerate: lambda_eff = -M_2'' (Q-1)^2 = -2/3), s3 (K4 kinetic sign; filled by
tk1_k4eval.py, which reads this file's track). Env TK1_MUTATE = MU1 (drop theta F_theta) or MU2 (key off, arm).
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, time
import mpmath as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tk1_lib as L

MUT = os.environ.get("TK1_MUTATE", "")
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
def say(*a):
    print(*a, flush=True)

class Dust:
    """GR reference: rho_K = n exactly."""
    def xK(self, th, Om_n):
        return Om_n
    def Qm1(self, th, Om_n):
        return mp.mpf(0)
    def lam_eff(self, th, Om_n):
        return mp.mpf(0)

# ------------------------------------------------------------------ background
def t_of_a_bg(key, a, foot):
    f = lambda la: 1 / L.background_H(key, mp.e**la, foot)[0]
    # from a = 1e-12 (radiation era; t ~ a^2/(2 sqrt(Or)) below)
    a_lo = mp.mpf("1e-8")
    t_lo = a_lo**2 / (2 * mp.sqrt(L.FOOT[foot]["Or"]))
    return t_lo + mp.quad(f, [mp.log(a_lo), mp.log(mp.mpf(a) / 100), mp.log(a)])

# ------------------------------------------------------------------ A2
def a2(foot, prm, out):
    key = L.Key(**prm)
    F = L.FOOT[foot]
    rows = {}
    for z in (3400, 1100, 10, 2, 1, 0.5, 0):
        a = mp.mpf(1) / (1 + z)
        H, On = L.background_H(key, a, foot)
        th = 3 * H
        # w from exact conservation: p = -rho - (d rho/d ln a)/3 along the background
        def xk_of_la(la):
            aa = mp.e**la
            HH, OO = L.background_H(key, aa, foot)
            return key.xK(3 * HH, OO)
        xk = xk_of_la(mp.log(a))
        dx = mp.diff(xk_of_la, mp.log(a))
        w = (-xk - dx / 3) / xk
        mu_eff = mp.sqrt(key.M2(th)) * L.H0_PER_MPC
        dlnM = th * key.dM2(th) / key.M2(th)
        rows[str(z)] = dict(H=float(H), theta=float(th), w=float(w), Qm1=float(key.Qm1(th, On)),
                            mu_eff_perMpc=float(mu_eff), dlnM2_dlntheta=float(dlnM),
                            lambda_eff=float(key.lam_eff(th, On)))
    # min of mu_eff over z in [0, 3400] (log grid)
    zs = [10**(mp.mpf(i) / 40) - 1 for i in range(0, int(40 * mp.log10(3401)) + 1)]
    mus = []
    for z in zs:
        H, On = L.background_H(key, 1 / (1 + z), foot)
        mus.append((float(mp.sqrt(key.M2(3 * H)) * L.H0_PER_MPC), float(z)))
    mmin = min(mus)
    out["rows"] = rows
    out["mu_eff_min"] = dict(mu=mmin[0], z=mmin[1], mu_J=F["mu_J"], ratio=mmin[0] / F["mu_J"])
    out["w3400_pass"] = rows["3400"]["w"] <= 0.01
    out["jeans_dominance_pass"] = mmin[0] >= F["mu_J"]
    if not out["jeans_dominance_pass"]:
        kmin = min((m / (1 + z), z) for m, z in mus)
        out["comoving_min"] = dict(k=kmin[0], z=kmin[1], line=F["mu_J"] / 3401)
    return out

# ------------------------------------------------------------------ A3 patch
class Patch:
    def __init__(self, key, foot, a_i, delta_i, Om=None):
        self.key = key
        F = dict(L.FOOT[foot]) if Om is None else Om
        self.F = F
        self.a_i = mp.mpf(a_i)
        self.d = mp.mpf(delta_i)
        Hbg = self.Hbg_i = (L.background_H(Dust(), a_i, foot)[0] if Om is None else
                            mp.sqrt(F["Or"] / self.a_i**4 + (F["Ob"] + F["Od"]) / self.a_i**3 + F["OL"]))
        self.H_i = Hbg * (1 - self.d / 3)
        x0 = self.rest_nok(self.a_i) + key.xK(3 * self.H_i, self.Om_n(self.a_i))
        self.kc = self.a_i**2 * (x0 - self.H_i**2)

    def Om_n(self, a):
        return self.F["Od"] * (1 + self.d) / a**3

    def rest_nok(self, a):
        return self.F["Or"] * (1 + 4 * self.d / 3) / a**4 + self.F["Ob"] * (1 + self.d) / a**3 + self.F["OL"]

    def rest(self, a):
        return self.rest_nok(a) - self.kc / a**2

    def H(self, a):
        a = mp.mpf(a)
        if isinstance(self.key, Dust):
            v = self.rest(a) + self.Om_n(a)
            return mp.sqrt(v) if v > 0 else mp.mpf("1e-60")
        return L.H_root(self.key, self.rest(a), self.Om_n(a))

    def G0(self, a):
        """value of rest + xK(0): turnaround (H = 0 allowed) where it reaches 0; -inf-like if the floor is off."""
        if isinstance(self.key, Dust):
            return self.rest(a) + self.Om_n(a)
        th = mp.mpf("1e-40")
        return self.rest(a) + self.key.xK(th, self.Om_n(a))

    def a_turn(self):
        """first a > a_i where G0 = 0 (H = 0 reachable); None if none below 1e3 a_i... scan in log a."""
        la = mp.log(self.a_i); step = mp.mpf("0.01")
        prev = self.G0(mp.e**la)
        while la < mp.log(self.a_i) + 12:
            la2 = la + step
            g = self.G0(mp.e**la2)
            if g <= 0 < prev or (prev > 0 and g <= 0):
                lo, hi = la, la2
                for _ in range(200):
                    mid = (lo + hi) / 2
                    if self.G0(mp.e**mid) > 0:
                        lo = mid
                    else:
                        hi = mid
                return mp.e**lo
            prev, la = g, la2
        return None

    def t_between(self, a1, a2, a_end=None):
        """proper time from a1 to a2 (expanding branch). If a_end (turnaround) is given and a2 is close to it,
        the sqrt endpoint is handled by a = a_end (1 - w^2)."""
        f = lambda la: 1 / self.H(mp.e**la)
        if a_end is None or a2 < a_end * (1 - mp.mpf("1e-3")):
            pts = [mp.log(a1)] + [mp.log(a1) + (mp.log(a2) - mp.log(a1)) * mp.mpf(j) / 8 for j in range(1, 9)]
            return mp.quad(f, pts)
        am = a_end * (1 - mp.mpf("1e-3"))
        t1 = self.t_between(a1, am)
        wmax = mp.sqrt(1 - am / a_end)
        wmin = mp.sqrt(max(1 - a2 / a_end, mp.mpf(0)))
        g = lambda w: 2 * a_end * w / ((a_end * (1 - w**2)) * self.H(a_end * (1 - w**2)))
        return t1 + mp.quad(g, [wmin, wmax / 4, wmax])


def calibrate(foot, z_ta, a_i):
    """delta_i such that the pure-dust patch turns around at the background's t(z_ta)."""
    t_target = t_of_a_bg(Dust(), mp.mpf(1) / (1 + z_ta), foot)
    t_ai = t_of_a_bg(Dust(), a_i, foot)
    def tta(d):
        P = Patch(Dust(), foot, a_i, d)
        at = P.a_turn()
        if at is None:
            return mp.inf
        return t_ai + P.t_between(a_i, at, at)
    lo, hi = mp.mpf("1e-4"), mp.mpf("0.2")
    for _ in range(60):
        mid = mp.sqrt(lo * hi)
        if tta(mid) > t_target:
            lo = mid
        else:
            hi = mid
    d = mp.sqrt(lo * hi)
    P = Patch(Dust(), foot, a_i, d)
    at = P.a_turn()
    t_actual = t_ai + P.t_between(a_i, at, at)   # the GR patch's own turnaround time (the reference used below)
    return d, at, t_ai, t_actual


def gmin(P, a):
    """local minimum of G(H; a) over H in [1e-9, 1e-2] (the floor-on dip); returns (Gmin, Hmin) or None if monotone."""
    key = P.key
    if isinstance(key, Dust) or key.mf == 0 or key.p == 0:
        return None
    rest, On = P.rest(a), P.Om_n(a)
    f = lambda lh: (mp.e**lh)**2 - rest - key.xK(3 * mp.e**lh, On)
    lhs = [mp.log(mp.mpf(10)**(mp.mpf(j) / 20 - 9)) for j in range(0, 141)]
    vals = [f(l) for l in lhs]
    j = min(range(1, len(vals) - 1), key=lambda i: vals[i])
    if not (vals[j] <= vals[j - 1] and vals[j] <= vals[j + 1]):
        return None
    lo, hi = lhs[j - 1], lhs[j + 1]
    for _ in range(80):   # golden section
        m1 = lo + (hi - lo) * mp.mpf(0.382); m2 = lo + (hi - lo) * mp.mpf(0.618)
        if f(m1) < f(m2):
            hi = m2
        else:
            lo = m1
    lm = (lo + hi) / 2
    return f(lm), mp.e**lm


def bisect_a(fn, alo, ahi, n=70):
    """fn(a) False at alo, True at ahi; returns the switching a."""
    for _ in range(n):
        am = mp.sqrt(alo * ahi)
        if fn(am):
            ahi = am
        else:
            alo = am
    return ahi


import sympy as _sp
_K4 = json.load(open(os.path.join(HERE, "tk1_k4.json")))
_ex = {k: eval(_K4["K4_sym_" + k], {**_sp.__dict__}) for k in ("Az", "g4")}
_sy = {}
for _e in _ex.values():
    for _s in _e.free_symbols:
        _sy[str(_s)] = _s
_ARGS = ["a", "a_d", "N0", "FQQ", "FQth", "Fthth", "K"]
assert set(_sy) <= set(_ARGS), _sy
_F = {k: _sp.lambdify([_sy.get(n, _sp.Symbol(n)) for n in _ARGS], v, "mpmath") for k, v in _ex.items()}
KC = mp.mpf(1.5)


def k4_alg(key, a, H, On):
    """A_z and g4 (closed forms, no time derivatives) on the local state; plus the dust c_s^2 = (Q-1)/Q (KA5)."""
    if isinstance(key, Dust):
        return None
    q = 1 + mp.mpf(1.5) * On / key.M2(3 * H)
    N0 = 1 / q
    th = 3 * H
    M = key.M2(th); Mp = key.dM2(th); Mpp = key.M2pp(th)
    args = [a, a * H * N0, N0, M / KC, Mp * (q - 1) / KC, Mpp * (q - 1)**2 / (2 * KC), KC]
    Az = _F["Az"](*args); g4 = _F["g4"](*args)
    return Az, g4, (q - 1) / q, N0


def H_hint(key, rest, On, Hprev):
    """largest root below Hprev*1.05 (continuation of the expanding branch)."""
    if isinstance(key, Dust):
        v = rest + On
        return mp.sqrt(v) if v > 0 else None
    G = lambda h: h**2 - rest - key.xK(3 * h, On)
    hi = Hprev * mp.mpf(1.05)
    if G(hi) <= 0:
        return L.H_root(key, rest, On)
    step = mp.mpf(10)**(mp.mpf(1) / 64)
    lo = hi / step
    while G(lo) > 0:
        hi = lo; lo = lo / step
        if lo < mp.mpf("1e-30"):
            return None
    for _ in range(90):
        mid = mp.sqrt(lo * hi)
        if G(mid) > 0:
            hi = mid
        else:
            lo = mid
        if hi / lo - 1 < mp.mpf("1e-26"):
            break
    return mp.sqrt(lo * hi)


def el_a_residual(key, P, a):
    """|d/dt L_v - L_a| / max(|terms|) for L = (-a v^2/N + kc N a) + N a^3 M_2(th)(1/N-1)^2/3 - N a^3 rest_nok(a)
    (units: 8 pi G/3 = 1, K = 1.5), on the constraint solution (clock time, v = adot). The true clock dust term is used
    (with theta F_theta), so a trajectory built from a wrong constraint (MU1) fails it."""
    import tk1_k4eval as E4
    keytrue = L.Key(mu0=float(key.m0 * L.H0_PER_MPC), th0=float(key.th0), p=key.p, Mf=float(key.mf * L.H0_PER_MPC))
    v = E4.background_funcs(key, a, P.rest, P.Om_n)
    N0, ad, add, Nd = v["N0"], v["a_d"], v["a_dd"], v["N0_d"]
    On_a3 = P.Om_n(a) * a**3     # conserved charge n a^3
    def Lf(N, aa, vv):
        th = 3 * vv / (N * aa)
        M = keytrue.M2(th)
        # the clock term at fixed tau-gauge: N a^3 M (1/N - 1)^2 / (2K), K = 1.5
        return (-aa * vv**2 / N + P.kc * N * aa) + N * aa**3 * M * (1 / N - 1)**2 / 3 - N * aa**3 * P.rest_nok(aa)
    Lv_N = mp.diff(Lf, (N0, a, ad), (1, 0, 1)); Lv_a = mp.diff(Lf, (N0, a, ad), (0, 1, 1))
    Lv_v = mp.diff(Lf, (N0, a, ad), (0, 0, 2)); La = mp.diff(Lf, (N0, a, ad), (0, 1, 0))
    terms = [Lv_N * Nd, Lv_a * ad, Lv_v * add, La]
    return abs(terms[0] + terms[1] + terms[2] - terms[3]) / max(abs(x) for x in terms)


def a3_one(foot, z_ta, key, a_i, cal):
    d, a_ta_gr, t_ai, t_ta_gr = cal
    t0 = t_of_a_bg(Dust(), 1, foot)
    P = Patch(key, foot, a_i, d)
    res = dict(z_ta=z_ta, delta_i=float(d), a_ta_GR=float(a_ta_gr), t_ta_GR_Gyr=float(t_ta_gr * L.GYR_PER_HUBBLE),
               t0_Gyr=float(t0 * L.GYR_PER_HUBBLE))
    PG = Patch(Dust(), foot, a_i, d)
    t_half_up = t_ai + PG.t_between(a_i, a_ta_gr / 2)
    res["t_coll_GR_Gyr"] = float((2 * t_ta_gr - t_half_up) * L.GYR_PER_HUBBLE)
    a_turn = P.a_turn()
    a_fold = None
    prev_a, prev_g = None, None
    for jj in range(0, 401):
        aa = a_ta_gr * mp.mpf(0.9) * (mp.mpf(60))**(mp.mpf(jj) / 400)
        gm = gmin(P, aa)
        if gm is None:
            prev_a, prev_g = aa, None
            continue
        if prev_g is not None and prev_g < 0 <= gm[0]:
            a_fold = bisect_a(lambda x: (gmin(P, x) or (mp.mpf(-1), 0))[0] >= 0, prev_a, aa)
            break
        prev_a, prev_g = aa, gm[0]
    # the expanding branch (largest root) ends at the fold if the dip exists; at H = 0 only when G has no dip
    a_end = a_fold if a_fold is not None else (a_turn if a_turn is not None else 60 * a_ta_gr)
    res["a_turn_over_aGR"] = None if a_turn is None else float(a_turn / a_ta_gr)
    res["a_fold_over_aGR"] = None if a_fold is None else float(a_fold / a_ta_gr)
    ends_at_turn = a_fold is None and a_turn is not None
    # grid in ln a
    la_i, la_e = mp.log(a_i), mp.log(a_end)
    g = [la_i + (la_e - la_i) * mp.mpf(jj) / 1500 for jj in range(1500)]
    if a_ta_gr < a_end:
        g += [mp.log(a_ta_gr * (1 - mp.mpf(10)**(-mp.mpf(jj) / 40))) for jj in range(20, 400)]
        g += [mp.log(a_ta_gr * (1 + mp.mpf(10)**(-mp.mpf(jj) / 40))) for jj in range(20, 400)]
    g += [mp.log(a_end * (1 - mp.mpf(10)**(-mp.mpf(jj) / 30))) for jj in range(10, 450)]
    g = sorted(set(x for x in g if la_i <= x < la_e))
    rows = []
    Hprev = None
    for la in g:
        aa = mp.e**la
        rest, On = P.rest(aa), P.Om_n(aa)
        H = L.H_root(key, rest, On) if Hprev is None or isinstance(key, Dust) else H_hint(key, rest, On, Hprev)
        if H is None:
            break
        Hprev = H
        rows.append([la, aa, H, On])
    # time: trapezoid in ln a of 1/H; end correction for a sqrt turnaround
    t = [t_ai]
    for r0, r1 in zip(rows[:-1], rows[1:]):
        t.append(t[-1] + (r1[0] - r0[0]) * (1 / r0[2] + 1 / r1[2]) / 2)
    t_end = t[-1]
    if ends_at_turn:
        aL, HL = rows[-1][1], rows[-1][2]
        c = HL / mp.sqrt(a_end - aL)
        t_end += 2 * mp.sqrt(a_end - aL) / (a_end * c)
    res["n_grid"] = len(rows)
    # quantities and events
    tr = []
    ev = {}
    prev = None
    maxq = mp.mpf(0)
    for (la, aa, H, On), tt in zip(rows, t):
        th = 3 * H
        lam = key.lam_eff(th, On) if not isinstance(key, Dust) else mp.mpf(0)
        qm1 = key.Qm1(th, On) if not isinstance(key, Dust) else mp.mpf(0)
        maxq = max(maxq, qm1)
        k4 = k4_alg(key, aa, H, On)
        row = dict(a=aa, t=tt, H=H, On=On, lam=lam, Qm1=qm1)
        if k4 is not None:
            Az, g4, cs2, N0 = k4
            row.update(Az=Az, g4=g4, cs2=cs2, N0=N0)
            # instability scale (physical k, H0 units) where rate = 1/t, if g4/Az < 0:
            # rate^2 = (|g4| k^4 - g2 k^2)/(Az N0^2), g2 = cs2 Az N0^2 / a^2, k comoving
            if g4 / Az < 0:
                A_ = -g4 / (Az * N0**2); B_ = cs2 / aa**2; C_ = 1 / tt**2
                k2 = (B_ + mp.sqrt(B_**2 + 4 * A_ * C_)) / (2 * A_)
                row["kstar_phys"] = mp.sqrt(k2) / aa
        tr.append(row)
        if prev is not None:
            if prev["lam"] >= 0 > lam and "lam_zero" not in ev:
                ev["lam_zero"] = row
            if prev["lam"] > mp.mpf(-2) / 3 >= lam and "s2" not in ev:
                ev["s2"] = row
            if "Az" in row and (prev["Az"] > 0) != (row["Az"] > 0) and "s3_ghost" not in ev:
                ev["s3_ghost"] = row
            if "kstar_phys" in row and "s3_grad" not in ev:
                ev["s3_grad"] = row
            for nm_, Lpc in (("kstar_1kpc", 1e3), ("kstar_1pc", 1.0)):
                # first point where the unstable band reaches wavelengths >= L (2 pi / k* >= L)
                if "kstar_phys" in row and nm_ not in ev:
                    lam_pc = 2 * mp.pi / (row["kstar_phys"] * L.H0_PER_MPC) * 1e6
                    if lam_pc >= Lpc:
                        ev[nm_] = row
        prev = row
    res["max_Qm1_branch"] = float(maxq)
    def pub(r):
        o = dict(a_over_aGR=float(r["a"] / a_ta_gr), one_minus=float(1 - r["a"] / a_ta_gr), t_Gyr=float(r["t"] * L.GYR_PER_HUBBLE),
                 minus_t_ta_GR_Myr=float((r["t"] - t_ta_gr) * L.GYR_PER_HUBBLE * 1e3), before_t0=bool(r["t"] < t0),
                 H=float(r["H"]), theta=float(3 * r["H"]), Qm1=float(r["Qm1"]), lam=float(r["lam"]))
        for k_ in ("Az", "g4", "cs2"):
            if k_ in r:
                o[k_] = float(r[k_])
        if "kstar_phys" in r:
            o["unstable_wavelength_pc"] = float(2 * mp.pi / (r["kstar_phys"] * L.H0_PER_MPC) * 1e6)
        if not isinstance(key, Dust):
            D = L.minisuper_D(key, r["a"], r["H"], r["On"], P.kc)
            o["minisuper_D"] = float(D[0])
        return o
    res["events"] = {k_: pub(v_) for k_, v_ in ev.items()}
    if a_fold is not None:
        res["events"]["fold"] = pub(tr[-1]); res["events"]["fold"]["a_fold_exact_over_aGR"] = float(a_fold / a_ta_gr)
        res["t_fold_Gyr"] = float(t_end * L.GYR_PER_HUBBLE)
    res["t_end_branch_Gyr"] = float(t_end * L.GYR_PER_HUBBLE)
    if ends_at_turn:
        res["t_turn_Gyr"] = float(t_end * L.GYR_PER_HUBBLE)
        res["Qm1_at_turn"] = float(key.Qm1(mp.mpf("1e-40"), P.Om_n(a_turn))) if not isinstance(key, Dust) else 0.0
        # time symmetry: collapse to a_turn/2
        jh = max(jj for jj, r in enumerate(tr) if r["a"] <= a_turn / 2)
        res["t_coll_Gyr"] = float((2 * t_end - tr[jh]["t"]) * L.GYR_PER_HUBBLE)
    # a(t0)
    if t_end > t0 and (res.get("t_coll_Gyr") is None or res["t_coll_Gyr"] > res["t0_Gyr"]):
        jj = min(jj for jj, r in enumerate(tr) if r["t"] >= t0) if any(r["t"] >= t0 for r in tr) else len(tr) - 1
        r = tr[jj]
        res["at_t0"] = dict(a_over_aGR=float(r["a"] / a_ta_gr), H=float(r["H"]), Qm1=float(r["Qm1"]), lam=float(r["lam"]))
    # a sparse public track
    step = max(1, len(tr) // 120)
    res["track"] = [dict(a_over_aGR=float(r["a"] / a_ta_gr), t_Gyr=float(r["t"] * L.GYR_PER_HUBBLE), H=float(r["H"]),
                         Qm1=float(r["Qm1"]), lam=float(r["lam"]), Az=float(r.get("Az", 0)), g4=float(r.get("g4", 0)),
                         unstable_wavelength_pc=(float(2 * mp.pi / (r["kstar_phys"] * L.H0_PER_MPC) * 1e6)
                                                 if "kstar_phys" in r else None))
                    for r in tr[::step] + tr[-30:]]
    t_stop = min(res.get("t_coll_Gyr") or 1e99, res["t0_Gyr"])
    def occurs(nm):
        e = res["events"].get(nm)
        return e is not None and e["t_Gyr"] <= t_stop
    collapsed = res.get("t_coll_Gyr") is not None and res["t_coll_Gyr"] <= res["t0_Gyr"]
    base = ("REGULAR" + (" STRONG FIELD" if res["max_Qm1_branch"] > 0.1 else "")) if collapsed else "STALLS"
    def first_of(names):
        occ = [(res["events"][n]["t_Gyr"], n) for n in names if occurs(n)]
        return ("SINGULAR (%s)" % min(occ)[1]) if occ else base
    res["label_frozen"] = first_of(["s2", "s3_ghost", "s3_grad"])
    res["label_A1"] = first_of(["fold", "s3_ghost", "s3_grad"])
    # reading with the gradient line restricted to wavelengths >= 1 pc / 1 kpc (reported, not label-setting)
    res["label_A1_if_grad_needs_1pc"] = first_of(["fold", "s3_ghost", "kstar_1pc"])
    res["label_A1_if_grad_needs_1kpc"] = first_of(["fold", "s3_ghost", "kstar_1kpc"])
    # a-equation residual (clock-time minisuperspace EL for a) at a few track points: the constraint solution must
    # satisfy it (MU1 must break it)
    if not isinstance(key, Dust):
        import tk1_k4eval as E4
        resid = []
        for r in [tr[len(tr) // 5], tr[len(tr) // 2], tr[(4 * len(tr)) // 5]]:
            resid.append(float(el_a_residual(key, P, r["a"])))
        res["EL_a_rel_residual"] = resid
    return res


AZ = None
def main():
    out = {"mutate": MUT}
    a_i = mp.mpf(1) / 201
    # KA6: EdS
    Om = dict(Or=0, Ob=0, Od=1, OL=0)
    d6 = mp.mpf("1e-5"); ai6 = mp.mpf("1e-5")
    P6 = Patch(Dust(), None, ai6, d6, Om=Om)
    at6 = P6.a_turn()
    t_ai6 = mp.mpf(2) / 3 * ai6**1.5
    tta6 = t_ai6 + P6.t_between(ai6, at6, at6)
    tcoll6 = 2 * tta6
    a_lin = (tcoll6 / (mp.mpf(2) / 3))**(mp.mpf(2) / 3)
    dlin = d6 * a_lin / ai6
    out["KA6"] = dict(delta_lin_coll=float(dlin), target=1.68647, rel=float(dlin / mp.mpf("1.686470") - 1),
                      pass_=bool(abs(dlin / mp.mpf("1.686470") - 1) < 1e-3))
    say("KA6 EdS delta_lin at collapse = %.6f (1.68647), rel %.1e" % (dlin, out["KA6"]["rel"]))
    keys = {"primary": L.PRIMARY}
    keys.update({k_: v_ for k_, v_ in L.BRACKETS.items() if k_ != "MU2_key_off"})
    if MUT == "MU2":
        keys = {"MU2_key_off": L.BRACKETS["MU2_key_off"]}
    if MUT == "MU1":
        keys = {"primary": L.PRIMARY}
    for foot in ("canonical", "alt"):
        out[foot] = {"A2": {}, "A3": {}}
        for nm, prm in keys.items():
            if nm == "MU2_key_off" and MUT != "MU2" and foot == "alt":
                pass
            key = L.Key(**prm, drop_thFth=(MUT == "MU1"))
            out[foot]["A2"][nm] = a2(foot, prm, {})
            r2 = out[foot]["A2"][nm]
            say("[%s %s] A2: w(3400) %.3e, mu_eff min %.4g at z %.3g (mu_J %.4g, ratio %.3f), dlnM2/dlnth(0) %.2e" % (
                foot, nm, r2["rows"]["3400"]["w"], r2["mu_eff_min"]["mu"], r2["mu_eff_min"]["z"], r2["mu_eff_min"]["mu_J"],
                r2["mu_eff_min"]["ratio"], r2["rows"]["0"]["dlnM2_dlntheta"]))
        for z_ta in (5, 2, 1, 0.5):
            cal = calibrate(foot, z_ta, a_i)
            for nm, prm in keys.items():
                key = L.Key(**prm, drop_thFth=(MUT == "MU1"))
                r = a3_one(foot, z_ta, key, a_i, cal)
                out[foot]["A3"]["%s_zta%s" % (nm, z_ta)] = r
                E = r["events"]
                def fe(n):
                    e = E.get(n)
                    return "-" if not isinstance(e, dict) else "a/aGR %.8g t %.5g Gyr (t-t_taGR %.4g Myr) th %.3g Q-1 %.3g lam %.3g Az %.3g D %.3g wl_pc %s" % (
                        e["a_over_aGR"], e["t_Gyr"], e["minus_t_ta_GR_Myr"], e["theta"], e["Qm1"], e["lam"], e.get("Az", 0), e.get("minisuper_D", 0), e.get("unstable_wavelength_pc"))
                say("[%s %s z_ta %s] frozen: %s | A1: %s | delta_i %.4g t_taGR %.3f t_collGR %.3f t_coll %s a_turn/aGR %s a_fold/aGR %s t_fold %s | a(t0)/aGR %s H(t0) %s Q-1(t0) %s lam(t0) %s | maxQ-1 %.3g [%.0f s]" % (
                    foot, nm, z_ta, r["label_frozen"], r["label_A1"], r["delta_i"], r["t_ta_GR_Gyr"], r["t_coll_GR_Gyr"],
                    r.get("t_coll_Gyr"), r["a_turn_over_aGR"], r["a_fold_over_aGR"], r.get("t_fold_Gyr"),
                    r.get("a_t0_over_aGR"), r.get("H_t0"), r.get("Qm1_t0"), r.get("lam_t0"), r["max_Qm1_branch"], time.time() - T0))
                for n in ("lam_zero", "s3_grad", "kstar_1kpc", "kstar_1pc", "s2", "s3_ghost", "fold"):
                    say("     %-10s %s" % (n, fe(n)))
                say("     at_t0 %s  t_turn %s  t_fold %s | if grad needs >= 1 pc: %s; >= 1 kpc: %s | EL_a residual %s" % (r.get("at_t0"), r.get("t_turn_Gyr"), r.get("t_fold_Gyr"), r["label_A1_if_grad_needs_1pc"], r["label_A1_if_grad_needs_1kpc"], r.get("EL_a_rel_residual")))
    fn = "tk1_a3%s.json" % ("_MUTATE_" + MUT if MUT else "")
    with open(os.path.join(HERE, fn), "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    say("done %.0f s" % (time.time() - T0))

if __name__ == "__main__":
    main()

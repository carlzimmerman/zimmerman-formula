#!/usr/bin/env python3
"""
agentM: Milgrom 2022 (arXiv:2208.07073, PRD 106, 064060) -- the explicit time-nonlocal MI construction --
run through the repo kill battery. Construction pinned from the LaTeX source (fetched 2026-06-10):
  EOM (his Eq. "law"):    m a^(w) I[{r^},w,a0] = F^(w)
  Special case (Eq. 5):   I = mu[A(w)/a0],  mu free interpolating function (mu->1 high x, mu->x low x)
  Heuristic A (Eq. "v"):  A(w) = (1/sqrt(2) pi) int_0^inf theta(w'/w) |a^(w')| dw'
  Discrete (Eq. shiluta): A(w_n) = w_n^2|rbar_n| + sum_{k!=n} w_k^2|rbar_k| theta(w_k/w_n)
  Normalization: theta(1) = 1  <- FIXED by requiring the standard a0/mu of rotation-curve analysis.
  Free choices: theta(y) (his examples 2/(1+y^2), e^(1-y), e^((1-y)/q)); mu(x) shape.
  EFE: mu[theta(0)<a_ex>/a0], theta(0) ~ few (his words). Circular orbits: a mu(a/a0) = a_N EXACTLY.
Battery: [1] agentE solar reflex (budget delta_a_sun <= 2.47e-15 strict / 3.38e-15 loose, = s<(0.34-0.40)a0);
[2] agentA eccentric-orbit precession (machinery validated against banked agentA numbers);
[3] N5 corridor mapping + SPARC scatter (locked conventions of mi_f4_sparc_shape_test.py, gate reproduced);
[4] wide-binary EFE fork (vs mi_f4_widebinary_efe.out) ; lensing wall cited (f4_lensing_wall.out, 40.5 sigma).
Working rule: both a0 footings (framework 9.36e-11, canonical 1.2e-10) + hostile bath s=cH_Lam=5.418e-10;
raw before comparison; 'fails' audited as hard as 'works'. 2026-06-10. No git.
"""
import numpy as np, glob, os

LINE = "=" * 100
print(LINE)
print("agentM MILGROM-2022 (2208.07073) TIME-NONLOCAL MI GAUNTLET -- run date 2026-06-10")
print(LINE)

# ---------------------------------------------------------------- [0] constants
GMsun = 1.32712440018e20  # m^3/s^2
AU    = 1.495978707e11
yr    = 3.15576e7
A0_FW, A0_CAN, S_HOST = 9.36e-11, 1.2e-10, 5.418e-10
BUDGET_STRICT, BUDGET_LOOSE = 2.47e-15, 3.38e-15   # agentE survival line, delta_a_sun [m/s^2]

# mu shapes (exact) + analytically STABLE c(x) = 1/mu(x) - 1 (naive form underflows for x >~ 1e8:
# 1/mu-1 ~ 1/2x^2 < eps_double; caught on first run -- Mercury physical-s rows printed 0; bug log in .md)
def mu_std(x):    return x / np.sqrt(1.0 + x * x)
def mu_simple(x): return x / (1.0 + x)
def mu_rar(x):    return -np.expm1(-np.sqrt(x))          # 1 - exp(-sqrt(x))
def c_std(x):     return 1.0 / (x * (np.sqrt(1.0 + x * x) + x))      # exact: sqrt(1+x^2)/x - 1
def c_simple(x):  return 1.0 / x                                      # exact: (1+x)/x - 1
def c_rar(x):     e = np.exp(-np.sqrt(x)); return e / (1.0 - e)       # exact: 1/(1-e) - 1
MUS = {"standard": (mu_std, c_std), "simple": (mu_simple, c_simple), "McGaugh-RAR": (mu_rar, c_rar)}
# stability self-check at moderate x where both forms are representable
for lab, (mu, cf) in MUS.items():
    xt = 50.0
    assert abs(cf(xt) - (1.0 / mu(xt) - 1.0)) < 1e-12 * cf(xt) + 1e-300, lab

# theta families -- his three named examples; theta(1)=1 for all (checked below)
def th_A(y): return 2.0 / (1.0 + y * y)            # theta(0)=2
def th_B(y): return np.exp(1.0 - y)                # theta(0)=e
def th_C(y): return np.exp((1.0 - y) / 2.0)        # theta(0)=e^0.5 = 1.649
THETAS = {"2/(1+y^2)": th_A, "exp(1-y)": th_B, "exp((1-y)/2)": th_C}
for lab, th in THETAS.items():
    assert abs(th(1.0) - 1.0) < 1e-14, lab
print("[0] theta(1)=1 verified for all theta families (the normalization his paper fixes to the")
print("    standard rotation-curve a0/mu -- the SAME constant that pins the own-frequency term below).\n")

# ---------------------------------------------------------------- [1] SOLAR REFLEX
print(LINE)
print("[1] SOLAR REFLEX (the agentE channel): A(Omega_J) on the Sun's CoM worldline")
print(LINE)
# Sun's barycentric-wobble Fourier inventory: one line per planet at its orbital frequency.
# wobble acceleration = GM_p / R_p^2 (Newton 3rd law); amplitude = R_p * (GM_p/GMsun); Omega = sqrt(GMsun/R^3)
planets = [  # name, GM [m^3/s^2], a_orb [AU]
    ("Mercury", 2.2032e13,      0.38710), ("Venus", 3.24859e14, 0.72333),
    ("EMB",     4.035032e14,    1.00000), ("Mars",  4.282837e13, 1.52366),
    ("Jupiter", 1.26686534e17,  5.20336), ("Saturn", 3.7931187e16, 9.53707),
    ("Uranus",  5.793939e15,   19.1913),  ("Neptune", 6.836529e15, 30.0690)]
inv = []
for name, gm, aau in planets:
    R = aau * AU
    om = np.sqrt(GMsun / R**3)
    acc = gm / R**2
    inv.append((name, om, acc))
a_gal, om_gal = 2.15e-10, 9.2e-16   # solar-neighbourhood galactic field (repo g_ext) and orbital frequency V/R
om_J = dict((n, o) for n, o, a in inv)["Jupiter"]
a_J  = dict((n, a) for n, o, a in inv)["Jupiter"]
print(f"    Sun worldline inventory (per-planet lines): Omega_J = {om_J:.4e} s^-1 ; a_J = {a_J:.4e} m/s^2")
print(f"    (agentE integrated mean |a_sun| = 2.091e-7; our Jupiter line = {a_J:.3e} -> inventory consistent)")
print(f"    galactic line: Omega_gal = {om_gal:.1e} s^-1, a_gal = {a_gal:.2e} m/s^2")

print("\n    A(Omega_J) per Eq. (shiluta): own term a_J*theta(1)=a_J  +  cross terms a_k*theta(Omega_k/Omega_J):")
results1 = {}
for tlab, th in THETAS.items():
    A = a_J  # own term, coefficient theta(1)=1 -- NOT a free choice (same normalization as RC analysis)
    cross = []
    for name, om, acc in inv:
        if name == "Jupiter":
            continue
        c = acc * th(om / om_J)
        A += c
        cross.append((name, c))
    cgal = a_gal * th(om_gal / om_J)
    A += cgal
    cross.append(("galactic", cgal))
    big = sorted(cross, key=lambda t: -t[1])[:3]
    results1[tlab] = A
    print(f"      theta={tlab:13s}: A = {A:.4e}  (A/a_J = {A/a_J:.3f}; top cross: "
          + ", ".join(f"{n} {c:.2e}" for n, c in big) + ")")
print("    -> the kernel's reflex 'suppression' factor (delta_a ratio vs magnitude-keyed, mu_std tail ~ (a_J/A)^2):")
for tlab, A in results1.items():
    print(f"       theta={tlab:13s}: (a_J/A)^2 = {(a_J/A)**2:.3f}")

print("\n    delta_a_sun = a_J * c(A/a0), c = 1/mu - 1 (stable form)  vs  budget strict 2.47e-15 / loose 3.38e-15:")
print(f"    {'mu shape':12s} {'theta':14s} {'a0/s':9s} {'x=A/a0':>10s} {'delta_a_sun':>12s} {'x over strict':>14s}  verdict")
for mlab, (mu, cf) in MUS.items():
    for tlab, A in results1.items():
        for slab, s in [("fw", A0_FW), ("canon", A0_CAN), ("cH(host)", S_HOST)]:
            x = A / s
            da = a_J * cf(x)
            over = da / BUDGET_STRICT
            v = "PASS" if da <= BUDGET_STRICT else ("PASS(loose)" if da <= BUDGET_LOOSE else "FAIL")
            print(f"    {mlab:12s} {tlab:14s} {slab:9s} {x:10.1f} {da:12.3e} {over:14.2f}  {v}")
    print()

# what WOULD rescue: required A, and the theta values that would deliver it
print("    RESCUE ARITHMETIC (mu_std tail): need A >= a0*sqrt(a_J/(2*budget)):")
for slab, s in [("fw", A0_FW), ("canon", A0_CAN)]:
    Areq = s * np.sqrt(a_J / (2.0 * BUDGET_STRICT))
    need = Areq - a_J
    th0_gal = need / a_gal                      # if supplied by the galactic line at theta(~0)
    a_sat = dict((n, a) for n, o, a in inv)["Saturn"]
    om_sat = dict((n, o) for n, o, a in inv)["Saturn"]
    th_sat = need / a_sat                       # if supplied by the Saturn line at theta(0.403)
    print(f"      {slab}: A_req = {Areq:.3e} ({Areq/a_J:.2f} x a_J); cross-terms must supply {need:.2e}")
    print(f"           via galactic line: theta(0) ~ {th0_gal:.0f}  | via Saturn line: theta({om_sat/om_J:.3f}) ~ {th_sat:.1f}")
    # EFE-quenching consequence of such a theta(0):
    for th0 in (th0_gal,):
        xq = th0 * 2.2  # WB/vertical: a_ex/a0 ~ 2.2
        print(f"           consequence: EFE argument theta(0)*a_ex/a0 ~ {xq:.0f} -> 1-mu_std = {1-mu_std(xq):.2e}"
              f" -> WB/vertical MOND boost quenched to ~{100*(1/np.sqrt(mu_std(xq))-1):.3f}% (vs observed-class ~10-20%)")
print("""
    NOTE (budget transfer): the agentE survival line was derived for the instantaneous-mu time template.
    Milgrom-22's per-frequency-constant mu is the FROZEN-mu template; agentE [3]/[4] ran that config:
    linearized post-fit Mars 269.8 m (frozen) vs 269.2 m (instantaneous) at hostile -> the budget transfers
    within ~2%. The frozen template's PRE-fit signal is actually LARGER (Mars 5417 vs 2303 m).""")

# ---------------------------------------------------------------- [2] ECCENTRIC ORBITS / PRECESSION
print(LINE)
print("[2] ECCENTRIC ORBITS: per-harmonic Milgrom-22 vs instantaneous-F4 (agentA machinery analog)")
print(LINE)

def kepler_orbit(e, N=16384):
    """One closed Kepler orbit, GM=1, a=1 (n=1, T=2pi), uniform-time sampling."""
    M = np.linspace(0.0, 2.0 * np.pi, N, endpoint=False)
    E = M.copy()
    for _ in range(60):
        E -= (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    x = np.cos(E) - e
    y = np.sqrt(1.0 - e * e) * np.sin(E)
    r = 1.0 - e * np.cos(E)
    ax, ay = -x / r**3, -y / r**3
    return x, y, r, ax, ay, E

def gauss_dpomega(x, y, r, dax, day, e):
    """Secular apsidal shift per orbit from perturbing accel (dax,day), Gauss form, n=a=1."""
    rx, ry = x / r, y / r
    tx, ty = -y / r, x / r
    aR = dax * rx + day * ry
    aT = dax * tx + day * ty
    cosf = x / r  # orbit constructed with pericenter on +x axis (pomega = 0)
    sinf = y / r
    integ = (np.sqrt(1 - e * e) / e) * (-cosf * aR + sinf * (2 + e * cosf) / (1 + e * cosf) * aT)
    return np.mean(integ) * 2.0 * np.pi   # integral over one period (dt = T/N, T=2pi)

def harmonics(ax, ay):
    """Acceleration harmonic amplitudes |a^_k| in Milgrom's convention (sqrt(2)|C_k|), plus raw rfft."""
    N = len(ax)
    CX, CY = np.fft.rfft(ax) / N, np.fft.rfft(ay) / N
    amp = np.sqrt(2.0) * np.sqrt(np.abs(CX) ** 2 + np.abs(CY) ** 2)
    return amp, CX, CY

def milgrom_dpomega(e, s_c, cf, th, K=80, N=16384):
    """First-order secular apsidal shift for Milgrom-22: per-harmonic constant c_k = 1/mu(A_k/s_c)-1."""
    x, y, r, ax, ay, E = kepler_orbit(e, N)
    amp, CX, CY = harmonics(ax, ay)
    K = min(K, len(amp) - 1)
    ks = np.arange(1, K + 1)
    Ak = np.array([np.sum(amp[1:K + 1] * th(ks / float(k))) for k in ks])   # Eq. (shiluta), theta(1)=1 own term
    ck = cf(Ak / s_c)                                                       # stable 1/mu - 1
    CXm, CYm = np.zeros_like(CX), np.zeros_like(CY)
    CXm[1:K + 1] = ck * CX[1:K + 1]
    CYm[1:K + 1] = ck * CY[1:K + 1]
    dax = np.fft.irfft(CXm * N, n=N)
    day = np.fft.irfft(CYm * N, n=N)
    return gauss_dpomega(x, y, r, dax, day, e), Ak, ck, amp

def instant_dpomega(e, s_c, cf, N=16384):
    """Validation arm: instantaneous magnitude-keyed MI through the SAME Gauss machinery."""
    x, y, r, ax, ay, E = kepler_orbit(e, N)
    amag = 1.0 / r**2
    c_t = cf(amag / s_c)
    return gauss_dpomega(x, y, r, c_t * ax, c_t * ay, e)

# --- unit test 1: constant c -> zero secular pomega (pure GM rescaling)
x, y, r, ax, ay, E = kepler_orbit(0.206)
z = gauss_dpomega(x, y, r, 1e-3 * ax, 1e-3 * ay, 0.206)
print(f"    [gate 1] constant-c (GM-rescaling) secular pomega: {z:+.3e} rad/orbit (expect ~0)  "
      + ("PASS" if abs(z) < 1e-9 else "FAIL"))

# --- unit test 2: instantaneous arm vs agentA banked closed form
print("    [gate 2] instantaneous mu_std arm vs agentA banked closed form "
      "(-pi(4+e^2)sqrt(1-e^2) s^2/2, GM=a=1):")
agentA_banked = {0.206: -6.213652e-06, 0.093: -6.269482e-06, 0.057: -6.278065e-06}
for e0, banked in agentA_banked.items():
    got = instant_dpomega(e0, 1e-3, c_std)
    closed = -np.pi * (4 + e0**2) * np.sqrt(1 - e0**2) * (1e-3) ** 2 / 2
    print(f"      e={e0}: measured {got:+.6e} | agentA closed {banked:+.6e} | ratio {got/banked:.4f}  "
          + ("PASS" if abs(got / banked - 1) < 0.02 else "FAIL"))

# --- Milgrom-22 per-harmonic result, amplified s_c (same convention as agentA [2])
print("\n    Milgrom-22 per-harmonic precession at amplified s_c=1e-3 (mu_std), ratio vs instantaneous:")
print(f"    {'e':>6s} {'theta':14s} {'dpomega [rad/orb]':>18s} {'instantaneous':>14s} {'ratio M22/inst':>15s}")
sup = {}
for e0 in (0.206, 0.093, 0.057):
    inst = instant_dpomega(e0, 1e-3, c_std)
    for tlab, th in THETAS.items():
        dp, Ak, ck, amp = milgrom_dpomega(e0, 1e-3, c_std, th)
        sup[(e0, tlab)] = dp / inst
        print(f"    {e0:6.3f} {tlab:14s} {dp:+18.3e} {inst:+14.3e} {dp/inst:15.3f}")
# s^2 scaling check
dp4, *_ = milgrom_dpomega(0.206, 1e-4, c_std, th_A)
dp3, *_ = milgrom_dpomega(0.206, 1e-3, c_std, th_A)
print(f"    s^2-scaling check (theta A, e=0.206): dp(1e-3)/dp(1e-4) = {dp3/dp4:.2f} (expect 100)")

# --- physical predictions, Standish J2000 elements (agentA's source)
print("\n    PHYSICAL predictions [mas/cy] (Standish J2000 a,e; T from Kepler):")
bodies = {"Mercury": (0.38709927, 0.20563593), "Mars": (1.52371034, 0.09339410),
          "Saturn": (9.53667594, 0.05386179)}
MASCY = 2.0626480624709636e8  # mas per rad
for blab, (aau, e0) in bodies.items():
    a_m = aau * AU
    T_yr = 2 * np.pi * np.sqrt(a_m**3 / GMsun) / yr
    g_a = GMsun / a_m**2
    inst_closed = lambda s: -np.pi * (4 + e0**2) * np.sqrt(1 - e0**2) * (s / g_a) ** 2 / 2
    for slab, s in [("cH(host)", S_HOST), ("fw a0", A0_FW), ("canon a0", A0_CAN)]:
        s_c = s / g_a
        row = []
        for tlab, th in THETAS.items():
            dp, *_ = milgrom_dpomega(e0, s_c, c_std, th)
            row.append((tlab, dp * MASCY * (100.0 / T_yr)))
        inst_mas = inst_closed(s) * MASCY * (100.0 / T_yr)
        print(f"      {blab:8s} {slab:9s}: inst(agentA) {inst_mas:+10.3e} | M22: "
              + " ; ".join(f"{t}: {v:+9.3e}" for t, v in row))
# explicit Saturn-hostile tension vs the tightest bound (the agentA binding case)
e0, aau = bodies["Saturn"][1], bodies["Saturn"][0]
a_m = aau * AU; g_a = GMsun / a_m**2; T_yr = 2 * np.pi * np.sqrt(a_m**3 / GMsun) / yr
print("\n    Saturn HOSTILE tension vs INPOP15a-C2 (+0.05 +/- 0.20 mas/cy), the agentA binding bound:")
for tlab, th in THETAS.items():
    dp, *_ = milgrom_dpomega(e0, S_HOST / g_a, c_std, th)
    v = dp * MASCY * (100.0 / T_yr)
    print(f"      theta={tlab:13s}: pred {v:+.4f} mas/cy -> tension {(v-0.05)/0.20:+.2f} sigma "
          f"(instantaneous agentA: -0.307 -> -1.79 sigma)")
print("""    bounds context (agentA [4]): Saturn tightest INPOP15a-C2 = +0.05 +/- 0.20 mas/cy (the 1.79-sigma
    binding case for instantaneous-hostile); EPM2011 -0.32 +/- 0.47; Mercury bounds are O(0.3-1) mas/cy.""")
print("    McGaugh-RAR mu: c_k ~ e^(-sqrt(x)) ~ 1e-21 at planetary x -> precession ~1e-25 mas/cy, zero. (all theta)")

# ---------------------------------------------------------------- [3] SPARC / N5 corridor
print(LINE)
print("[3] SPARC: circular orbits reduce EXACTLY to a mu(a/a0)=a_N (his Eq. mdar) -> p=0 acceleration-keyed")
print(LINE)
# mechanical check of the p=0 mapping through the same FFT pipeline: near-circular orbit
xc, yc, rc, axc, ayc, Ec = kepler_orbit(1e-8)
ampc, _, _ = harmonics(axc, ayc)
own = ampc[1]
for tlab, th in THETAS.items():
    ks = np.arange(1, 41)
    A1 = np.sum(ampc[1:41] * th(ks / 1.0))
    print(f"    circular-orbit check, theta={tlab:13s}: A(n)/|a| = {A1/own:.9f}  (=1 -> no dressing, p=0)")
print("    -> in N5's parametrization a0_eff = a0*[(1+Omega/H0)/...]^(-p): Milgrom-22 has p IDENTICALLY 0 on")
print("       single-frequency orbits; A is acceleration-valued ('Only ratios of frequencies enter' -- abstract).")
print("       It is NOT the pure-frequency class N5 killed at +0.023 dex / 5.2 sigma; it is the p=0 EDGE.\n")

# SPARC scatter gate: locked conventions of mi_f4_sparc_shape_test.py (the M22 prediction is EXACTLY this table)
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "sparc_data")
kpc = 3.0857e19
rows = []
for f in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
    try:
        d = np.genfromtxt(f, comments="#")
    except Exception:
        continue
    if d.ndim != 2 or d.shape[1] < 6:
        continue
    R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
    rows.append((R * kpc, Vobs, eV, Vgas, Vdisk, Vbul))
print(f"    SPARC galaxies loaded: {len(rows)}")
def nu_fw(yv):     return np.sqrt(1 + 1 / yv)
def nu_rar(yv):    return 1.0 / (1.0 - np.exp(-np.sqrt(yv)))
def nu_simple(yv): return 0.5 + np.sqrt(0.25 + 1 / yv)
def nu_std(yv):    return np.sqrt((yv + np.sqrt(yv * yv + 4)) / (2 * yv))
FUNCS = {"fw sqrt(1+1/y)": nu_fw, "McGaugh RAR": nu_rar, "simple": nu_simple, "F4 standard": nu_std}
def scatter(nu, Ud, a0):
    res, w = [], []
    for Rm, Vobs, eV, Vgas, Vdisk, Vbul in rows:
        Vbar2 = np.sign(Vgas) * Vgas**2 + Ud * Vdisk**2 + 1.4 * Ud * Vbul**2
        gb = Vbar2 * 1e6 / Rm
        go = (Vobs * 1e3) ** 2 / Rm
        ok = (gb > 0) & (go > 0) & np.isfinite(gb) & np.isfinite(go) & (Vobs > 0)
        rr = np.log10(go[ok]) - np.log10(nu(gb[ok] / a0) * gb[ok])
        fr = np.clip(eV[ok], 1, None) / np.clip(Vobs[ok], 1, None)
        res += list(rr); w += list(1 / fr**2)
    res, w = np.array(res), np.array(w)
    return np.sqrt(np.mean(res**2)), np.sqrt(np.sum(w * res**2) / np.sum(w))
Uds = np.linspace(0.3, 1.2, 46)
banked_fw = {"McGaugh RAR": 0.1950, "F4 standard": 0.1984, "fw sqrt(1+1/y)": 0.1969, "simple": 0.1951}
for a0v, a0lab in [(9.36e-11, "framework 9.36e-11"), (1.2e-10, "canonical 1.2e-10")]:
    print(f"\n    === Milgrom-22 SPARC RAR scatter (== acceleration-keyed table), a0 = {a0lab} ===")
    for lab, nu in FUNCS.items():
        su = [scatter(nu, U, a0v) for U in Uds]
        iu = int(np.argmin([sv[0] for sv in su]))
        gate = ""
        if a0lab.startswith("framework") and lab in banked_fw:
            gate = "  [gate vs banked {:.4f}: {}]".format(
                banked_fw[lab], "PASS" if abs(su[iu][0] - banked_fw[lab]) < 5e-4 else "FAIL")
        print(f"      {lab:16s} bestUd={Uds[iu]:.2f}  unweighted={su[iu][0]:.4f}  weighted={su[iu][1]:.4f}{gate}")

# ---------------------------------------------------------------- [4] WIDE BINARIES (EFE fork)
print("\n" + LINE)
print("[4] WIDE BINARIES: Milgrom-22's theta(0)-ENHANCED EFE vs the banked DR4 fork (mi_f4_widebinary_efe.out)")
print(LINE)
om_WB, g_ext = 4.2e-13, 2.15e-10
print(f"    Omega_WB = {om_WB:.1e} s^-1 ; Omega_gal/Omega_WB = {om_gal/om_WB:.2e} -> theta(Omega_ex/Omega_in) = theta(~0)")
print("    M22 EFE is SCALAR-additive across frequencies (|a^(w)| magnitudes; no vector angle-averaging) and")
print("    theta(0)-enhanced: A(w_in) = a_in + theta(0)*a_ex   [his Eq. exasa + WB paragraph, quoted in .md]")
rng = np.random.default_rng(20260610)
def boost_vector(nu, y_int, y_ext, n=200000):   # banked repo prescription (gate)
    u = rng.uniform(-1, 1, n)
    return np.mean(nu(np.sqrt(y_ext**2 + y_int**2 + 2 * y_ext * y_int * u)))
def boost_m22(mu, y_int, y_ext, th0):
    """self-consistent scalar M22: a*mu[(a+th0*y_ext)] = y_int (all in units of a0); boost = a/y_int."""
    lo, hi = y_int, 1e6
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid * mu(mid + th0 * y_ext) > y_int: hi = mid
        else: lo = mid
    return 0.5 * (lo + hi) / y_int
NUMU = {"F4/standard": mu_std, "simple": mu_simple, "McGaugh RAR": mu_rar}
NUNU = {"F4/standard": nu_std, "simple": nu_simple, "McGaugh RAR": nu_rar}
for a0v, lab in [(9.36e-11, "framework"), (1.2e-10, "canonical")]:
    y_ext = g_ext / a0v
    print(f"\n    === a0 {lab}: y_ext = {y_ext:.2f}; deep bin y_int = 0.18 ===  (VELOCITY boost %, sqrt(B)-1)")
    print(f"    {'shape':14s} {'banked vector-MI':>17s} {'M22 th0=1':>10s} {'M22 th0=2':>10s} {'M22 th0=e':>10s}")
    for shp in NUMU:
        bv = 100 * (np.sqrt(boost_vector(NUNU[shp], 0.18, y_ext)) - 1)
        b1 = 100 * (np.sqrt(boost_m22(NUMU[shp], 0.18, y_ext, 1.0)) - 1)
        b2 = 100 * (np.sqrt(boost_m22(NUMU[shp], 0.18, y_ext, 2.0)) - 1)
        be = 100 * (np.sqrt(boost_m22(NUMU[shp], 0.18, y_ext, np.e)) - 1)
        print(f"    {shp:14s} {bv:16.1f}% {b1:9.1f}% {b2:9.1f}% {be:9.1f}%")
print("""
    Reading: theta(0)~2-e cuts the soft-shape (simple/RAR) WB boost from the banked ~13-18% to ~4-10% --
    Milgrom-22 RESHAPES the DR4 fork: a clean DR4 null at ~3% kills soft-shape M22-MI only if theta(0)<~2;
    a +10-15% detection kills the theta(0)-enhanced EFE for ALL shapes (it cannot un-enhance);
    a +4-8% intermediate would SELECT M22-style enhanced-EFE MI over both AQUAL-EFE MOND and F4.""")

# ---------------------------------------------------------------- [5] verdict
print(LINE)
print("[5] VERDICT ASSEMBLY (numbers above; prose + quotes in agentM_milgrom2022_gauntlet.md)")
print(LINE)
print("""    1. SOLAR REFLEX: the frequency filter is STRUCTURALLY INERT on the Sun's own dominant line --
       theta(1)=1 (the rotation-curve normalization itself) pins A(Omega_J) >= a_J; cross-terms give
       A/a_J = 1.13-1.18 only -> delta_a suppression 0.72-0.78 vs required <=0.117 (fw) / 0.072 (canon).
       Milgrom-22 + power-law mu (standard: x6-11 over budget; simple: x3e4): DEAD at BOTH footings.
       Milgrom-22 + exponential mu (RAR): PASS by >10^13. The mu-tail, not the filter, decides.
    2. PRECESSION: the per-harmonic-constant structure SUPPRESSES the instantaneous signal x3.4-6.8
       and FLIPS ITS SIGN (prograde); Saturn-hostile lands at +0.06..+0.09 mas/cy = 0.0-0.2 sigma on
       INPOP15a-C2 (vs instantaneous -1.79 sigma): the channel is not just passed, it is RELAXED.
    3. SPARC: exactly the p=0 acceleration-keyed table (gate reproduced); NOT in N5's killed class;
       NOT dressed either -- the corridor escape is unavailable; survival rides on the mu-tail alone.
    4. WB: theta(0)-enhanced scalar EFE cuts the soft-shape boost from ~13-18% to ~4-10% -> DR4 fork
       reshaped (pre-registered above). LENSING: nonrelativistic pure MI by explicit self-restriction
       -> baryon-only metric -> the banked 40.5-sigma metric-passive wall stands unanswered.""")
print("[6] DONE.")

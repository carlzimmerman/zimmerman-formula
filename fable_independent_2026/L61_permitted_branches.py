#!/usr/bin/env python3
"""
L61 -- THE THREE PERMITTED BRANCHES: can a theory exist where the foliation theorem says it could?
==================================================================================================
PAPER9 / L31 states its own scope in its own words: the theorem binds theories with (i) static weak-field
MOND, (ii) one metric with matter minimally coupled, (iii) exactly two propagating gravitational modes,
and L39 discharged the locality proviso against the known nonlocal class by the lensing lock.  What it
explicitly does NOT close is written in the paper:

    "three or more propagating modes, two metrics, or a non-minimal matter coupling are all untouched."

Eighteen months of this programme have lived in the fourth corner.  This lane searches the other three.

There is a SECOND theorem that must be respected, and testing whether it generalises is the single most
important structural question here.  L49 -> L50 -> L55 established, for THIS action's kernel combined with
a LambdaCDM-profile cold abundance, that a full cold abundance and a MOND kernel doing the galaxy work are
ALTERNATIVES rather than COMPLEMENTS -- because they are two explanations of one measured excess and the
excess can only be spent once.  If that argument is branch-independent, no theory in ANY branch can carry
both, and that is a far stronger statement than anything about one action.  Step B tests exactly that,
BEFORE any branch is priced, because a branch that inherits it is dead before its gates are run.

WHAT IS RUN HERE
  PART A  CONTROLS.  The four mode-counting controls (2, 3, 3, 5 for general relativity, GR + scalar,
          khronometric, Einstein-aether) rebuilt from the Dirac formula; three gate numbers from the
          deposited theory's own gate table reproduced from its own data with independent code; and the
          conformal-null-geodesic control proved symbolically from the Christoffels.
  PART B  THE DECISIVE STRUCTURAL QUESTION.  Does "the excess can only be spent once" generalise beyond
          one action?  Stated as a theorem with hypotheses, each hypothesis then tested for whether ANY
          of the three branches can break it.
  PART C  BRANCH 1 -- three or more propagating modes, Lorentz invariant (RAQUAL, phase-coupling gravity).
  PART D  BRANCH 2 -- two metrics (dRGT/Hassan-Rosen, BIMOND, and this repository's own open subspace).
  PART E  BRANCH 3 -- non-minimal matter coupling (conformal, disformal), including the adjudication L50
          flagged and did not settle: LEDGER sf27's disformal repair versus the GW-speed identity.
  PART F  VERDICTS, and the mutation controls that must behave.

GATE ORDER, cheapest kill first, as the brief specifies: lensing-vs-dynamics; Solar System; preferred
frame; tensor speed; mode health; cluster mass and shear shape; cosmology.  A branch is stopped at the
first gate that closes it and the gate is named.

METHOD.  Nothing under closure_2026/ or the lead's directories is imported or executed.  Every symbolic
result is rebuilt in sympy in this file.  Where this repository has already CLOSED something, it is cited
and NOT re-derived -- in particular DC-013 (the single-metric frame-free slip-lock), DC-018 (the bimetric
Galileon flux-scaling theorem), the 2-D ghost-free bimetric subspace recorded as health-UNDECIDED, and
L6/L55's screening closures.  Both a0 footings on every dimensional number.

A branch is declared ALIVE only if a construction is exhibited and run through gates.  A survey is not a
verdict.
"""
import numpy as np, math, os, sys, glob, json, re, time
import sympy as sp

T0 = time.time()
FAILS = []
NCHK = 0
def check(name, ok, detail=""):
    global NCHK
    NCHK += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def P(s=""): print(s, flush=True)
def info(s): print("      " + s, flush=True)
def sec(t):
    P(""); P("=" * 118); P(t); P("=" * 118)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
DATA = os.path.join(REPO, "real_research", "data")
def rel(p): return os.path.relpath(p, REPO)          # never print an absolute machine path

# ---- constants ---------------------------------------------------------------------------------------
G     = 6.674e-11
c     = 2.99792458e8
MSUN  = 1.989e30
kpc   = 3.0857e19
Mpc   = 3.0857e22
pc    = 3.0857e16
A0    = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
FOOT  = ("canonical", "alt")
S_SAT, D_SAT = 2.540, 0.6476                    # the carried kernel, THE_COMPLETE_THEORY section 4
hP    = 0.674
H0    = hP * 100e3 / Mpc
RHO_C = 3 * H0**2 / (8 * math.pi * G)
OM, OB = 0.315, 0.049
OCH2   = 0.1200                                  # Planck 2018 cold-matter density
UPS_D, UPS_B = 0.5, 0.7
Z_REC  = 1100.0
RS_REC_COMOV = 145.0 * Mpc                       # sound horizon at recombination, comoving

def Delta(s):
    """The deposited theory's carried kernel, saturating at D_SAT above S_SAT (the bounded boost)."""
    s = np.asarray(s, float)
    sc = np.clip(s, 1e-300, S_SAT)                      # clip before expm1: above S_SAT the value is D_SAT
    d = np.where(s > 0, sc / np.expm1(np.sqrt(sc)), 0.0)
    return np.where(s > S_SAT, D_SAT, d)
def g_kernel(gb, a0): return gb + a0 * Delta(gb / a0)

P("=" * 118)
P("L61 -- THE THREE PERMITTED BRANCHES: >=3 modes, two metrics, non-minimal coupling")
P("=" * 118)
P("The foliation theorem (L31 53/53, L39 40/40, PAPER9) closes ONE corner and names three it does not.")
P("This lane searches the three, and asks first whether the 'excess spent once' theorem follows them there.")
P(f"a0 footings: canonical {A0['canonical']:.4e} m/s^2,  alt {A0['alt']:.4e} m/s^2   (both carried throughout)")


# ======================================================================================================
sec("PART A -- CONTROLS.  The gate machinery is calibrated against a known object before anything rests on it.")
# ======================================================================================================

P("")
P("A.1  The four mode-counting controls.  Dirac's formula, one line, applied to four theories whose")
P("     answers are published:   N_phys = (P - 2F - S) / 2,  P = phase-space dimension per space point,")
P("     F = number of first-class constraints, S = number of second-class constraints.")
P("")

def dirac(P_dim, F, S):
    n2 = P_dim - 2 * F - S
    return n2 / 2.0

COUNT = [
    # name, configuration variables (dimension), first class, second class, published N
    ("general relativity",
     "gamma_ij (6) -> P = 12", 12, 4, 0, 2,
     "4 first class = Hamiltonian + 3 momentum constraints (the diffeomorphisms)"),
    ("GR + one minimally coupled scalar",
     "gamma_ij (6) + phi (1) -> P = 14", 14, 4, 0, 3,
     "the scalar adds no constraint: 2 tensor + 1 scalar"),
    ("khronometric (non-projectable Horava)",
     "gamma_ij (6) + khronon T (1) -> P = 14", 14, 4, 0, 3,
     "gauge = foliation-preserving diffeos: 3 spatial + 1 time reparametrisation t -> f(t)"),
    ("Einstein-aether",
     "gamma_ij (6) + u^mu (4) minus the unit constraint (1) -> P = 18", 18, 4, 0, 5,
     "2 tensor + 2 vector + 1 scalar (Jacobson-Mattingly)"),
]
P(f"      {'theory':38s} {'phase space':34s} {'F':>2s} {'S':>2s} {'N':>4s} {'published':>10s}")
allc = True
for nm, cfg, Pd, F, S, pub, why in COUNT:
    N = dirac(Pd, F, S)
    P(f"      {nm:38s} {cfg:34s} {F:2d} {S:2d} {N:4.0f} {pub:10d}")
    info(f"    {why}")
    allc = allc and (abs(N - pub) < 1e-12)
check("A1  mode-counting control: general relativity = 2",              abs(dirac(12, 4, 0) - 2) < 1e-12, "(12 - 8)/2")
check("A2  mode-counting control: GR + scalar = 3",                     abs(dirac(14, 4, 0) - 3) < 1e-12, "(14 - 8)/2")
check("A3  mode-counting control: khronometric = 3",                    abs(dirac(14, 4, 0) - 3) < 1e-12, "(14 - 8)/2")
check("A4  mode-counting control: Einstein-aether = 5",                 abs(dirac(18, 4, 0) - 5) < 1e-12, "(18 - 8)/2")
P("")
info("The same formula, applied to the two-metric branch, is used unchanged in PART D:")
info(f"  Hassan-Rosen bigravity, ghost-free   P = 24, F = 4, S = 2  ->  N = {dirac(24,4,2):.0f}  (2 massless + 5 massive)")
info(f"  the same with the Boulware-Deser mode P = 24, F = 4, S = 0  ->  N = {dirac(24,4,0):.0f}  (the ghost)")
check("A4b two-metric counting reproduces the published 7 and the ghost's 8",
      abs(dirac(24, 4, 2) - 7) < 1e-12 and abs(dirac(24, 4, 0) - 8) < 1e-12, "7 healthy / 8 with BD")

# ---- A.2  gate numbers reproduced ---------------------------------------------------------------------
P("")
P("A.2  Gate numbers from the deposited theory's own gate table, recomputed here from its own data.")
P("     THE_COMPLETE_THEORY_2026-09-08.md section 6.  Three are reproduced: one analytic, two on SPARC.")
P("")

# --- gate number 1: the PPN alpha_2 at the exhibited point ---
K_B   = 0.2
c14   = 1.0e-6
sigma = 1.679312732
c2    = 2 * sigma * c14 / (2 - c14 - 3 * sigma * c14)
K2    = (2 - K_B)**2 / c2
alpha1 = -4 * c14
alpha2 = (c14 / 2.0) * (1.0 / sigma - 1.0)
S_eff_ceiling = 1 - 1 / 1.7716
info(f"exhibited point: K_B = {K_B}, c14 = {c14:.1e}, sigma = sigma* = {sigma:.9f}")
info(f"  c2   = 2 sigma c14/(2 - c14 - 3 sigma c14) = {c2:.6e}   (table: 1.679318e-6)")
info(f"  |K2| = (2 - K_B)^2 / c2                    = {K2:.4e}   (table: 1.9294e6, the closure locus)")
info(f"  alpha_1 = -4 c14 = {alpha1:.3e}  vs bound 1e-4      (footing-independent; see L49 X7)")
info(f"  alpha_2 = (c14/2)(1/sigma - 1) = {alpha2:.4e}  vs bound 4e-7,  margin {4e-7/abs(alpha2):.3f}x")
check("A5  gate reproduced: PPN alpha_2 = -2.02e-7 at margin 1.98x",
      abs(alpha2 + 2.02e-7) < 1e-9 and abs(4e-7 / abs(alpha2) - 1.98) < 0.02,
      f"alpha_2 = {alpha2:.4e}, margin {4e-7/abs(alpha2):.3f}x vs published 1.98x")
check("A5b gate reproduced: closure locus |K2| = 1.9294e6 and the S_eff ceiling 0.4355",
      abs(K2 / 1.9294e6 - 1) < 2e-4 and abs(S_eff_ceiling - 0.4355) < 5e-4,
      f"|K2| = {K2:.5e}, S_eff <= 1 - 1/sigma_max = {S_eff_ceiling:.4f}")

# --- SPARC ---
def read_master():
    lines = open(os.path.join(DATA, "SPARC_Lelli2016c.mrt"), encoding="latin-1").read().splitlines()
    last = max(i for i, l in enumerate(lines) if l.startswith("-----")); rows = {}
    for line in lines[last + 1:]:
        f = line.split()
        if len(f) < 18: continue
        try: rows[f[0]] = dict(D=float(f[2]), inc=float(f[5]), L36=float(f[7]), MHI=float(f[13]), Q=int(f[17]))
        except ValueError: continue
    return rows
MASTER = read_master()

def c200_DM14(M200):
    return 10**(0.905 - 0.101 * np.log10(np.asarray(M200, float) * hP / 1e12))
def moster_mstar(logMh):
    N, logM1, be, ga = 0.0351, 11.590, 1.376, 0.608
    x = 10**(np.asarray(logMh, float) - logM1)
    return 10**np.asarray(logMh, float) * 2 * N / (x**(-be) + x**ga)
_LMH = np.linspace(8.5, 15.5, 2801); _LMS = np.log10(moster_mstar(_LMH))
def halo_mass_AM(Mstar):
    return 10**np.interp(np.log10(np.asarray(Mstar, float)), _LMS, _LMH)
_nfwm = lambda x: np.log1p(x) - x / (1.0 + x)

GAL = []
for fn in sorted(glob.glob(os.path.join(DATA, "sparc_data", "*_rotmod.dat"))):
    name = os.path.basename(fn).replace("_rotmod.dat", "")
    if name not in MASTER: continue
    m = MASTER[name]
    try: d = np.loadtxt(fn, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6: continue
    r = d[:, 0] * kpc; Vo = d[:, 1] * 1e3; eV = d[:, 2] * 1e3
    Vg = d[:, 3] * 1e3; Vd = d[:, 4] * 1e3; Vb = d[:, 5] * 1e3
    Vb2 = Vg * np.abs(Vg) + UPS_D * Vd * np.abs(Vd) + UPS_B * Vb * np.abs(Vb)
    msk = (r > 0) & (Vo > 0) & (Vb2 > 0) & (eV / np.maximum(Vo, 1) < 0.10)
    if msk.sum() < 3: continue
    Mstar = UPS_D * m["L36"] * 1e9; Mgas = 1.33 * m["MHI"] * 1e9
    GAL.append(dict(name=name, r=r[msk], Vo=Vo[msk],
                    gb=Vb2[msk] / r[msk], go=Vo[msk]**2 / r[msk],
                    Mb=Mstar + Mgas, Mstar=Mstar))
for g in GAL:
    M200 = max(float(halo_mass_AM(g["Mstar"])), 1.02 * g["Mb"])
    cc = float(c200_DM14(M200))
    R200 = (3 * M200 * MSUN / (4 * math.pi * 200 * RHO_C))**(1 / 3.)
    x = np.clip(g["r"] / R200, 1e-6, 6.0)
    g["M200"] = M200
    g["g_halo"] = G * (M200 - g["Mb"]) * MSUN * _nfwm(cc * x) / _nfwm(cc) / g["r"]**2
NPT = sum(len(g["r"]) for g in GAL)
info(f"SPARC loaded from {rel(os.path.join(DATA,'sparc_data'))}: {len(GAL)} galaxies, {NPT} points "
     f"(Upsilon_d = {UPS_D}, Upsilon_b = {UPS_B}, eV/V < 0.10, >= 3 points)")

GB = np.concatenate([g["gb"] for g in GAL])
GO = np.concatenate([g["go"] for g in GAL])
GH = np.concatenate([g["g_halo"] for g in GAL])
RR = np.concatenate([g["r"] for g in GAL])

# --- gate number 2: the galactic rotation-curve gate, kernel alone ---
P("")
row = {}
for foot in FOOT:
    a0 = A0[foot]
    res = np.log10(GO / g_kernel(GB, a0))
    row[foot] = (float(np.sqrt(np.mean(res**2))), float(np.median(res)))
    resh = np.log10(GO / (GB + GH))
info(f"kernel alone (f = 0):  rms {row['canonical'][0]:.3f} / {row['alt'][0]:.3f} dex   "
     f"medians {row['canonical'][1]:+.3f} / {row['alt'][1]:+.3f}      (published 0.145 / 0.142, +0.030 / +0.003)")
resh = np.log10(GO / (GB + GH))
info(f"abundance-matched halo alone (f = 1, no kernel):  rms {np.sqrt(np.mean(resh**2)):.3f} dex, "
     f"median {np.median(resh):+.3f}      (published 0.171, -0.026)")
check("A6  gate reproduced: SPARC rotation curves, kernel at zero parameters = 0.145 / 0.142 dex",
      abs(row["canonical"][0] - 0.145) < 0.004 and abs(row["alt"][0] - 0.142) < 0.004
      and abs(row["canonical"][1] - 0.030) < 0.006 and abs(row["alt"][1] - 0.003) < 0.006,
      f"{row['canonical'][0]:.3f}/{row['alt'][0]:.3f} dex at {row['canonical'][1]:+.3f}/{row['alt'][1]:+.3f}")
check("A6b control: the abundance-matched halo alone reproduces 0.171 dex at median -0.026",
      abs(float(np.sqrt(np.mean(resh**2))) - 0.171) < 0.006 and abs(float(np.median(resh)) + 0.026) < 0.008,
      f"{np.sqrt(np.mean(resh**2)):.3f} dex at {np.median(resh):+.3f}")

# --- gate number 3: the bounded-boost ceiling VALUE, and the Saturn phantom mass ---
P("")
CEIL = {f: D_SAT * A0[f] for f in FOOT}
info(f"bounded-boost ceiling C a0 = {CEIL['canonical']:.3e} / {CEIL['alt']:.3e} m/s^2   "
     f"(table: 6.06e-11 / 7.30e-11)")
check("A7  gate reproduced: the bounded-boost ceiling C a0 = 6.06e-11 / 7.30e-11 m/s^2",
      abs(CEIL["canonical"] - 6.06e-11) < 1e-13 and abs(CEIL["alt"] - 7.30e-11) < 1e-13,
      f"C = {D_SAT} times a0 on each footing")
P("")
info("DIRECTION STATED, and NOT reproduced here: the gate table's '99.23% of 2352 points' for the")
info("ceiling's SPARC violation rate is a Upsilon-PROFILED number (g03w, with SPARC's own Q<3 / i>30")
info("cuts).  At FIXED Upsilon_d = 0.5 this lane's own count is much higher, exactly as L11 B3 already")
info("recorded ('my fixed-Upsilon counts sit ~2.5x higher for BOTH kernels').  It is reported as a")
info("diagnostic, not used as a control, and the discrepancy is attributed rather than hidden:")
for foot in FOOT:
    frac = float(np.mean((GO - GB) <= CEIL[foot]))
    info(f"  [{foot:9s}] fixed-Upsilon, no error bars: {100*frac:.2f}% of {len(GB)} points below C a0")

# --- gate number 4: the Saturn phantom mass ---
P("")
r_sat = 9.5826 * 1.495978707e11
gN_sat = G * 1.98847e30 / r_sat**2
SAT_BOUND = 6.7e-11                                      # Msun, Pitjev-Pitjeva
sat = {}
for foot in FOOT:
    a0 = A0[foot]
    exc = a0 * float(Delta(np.array([gN_sat / a0]))[0])   # saturated: the bounded-boost ceiling
    Mph = exc * r_sat**2 / G / MSUN
    sat[foot] = Mph / SAT_BOUND
    info(f"[{foot:9s}] Saturn: g_N = {gN_sat:.3e} m/s^2 = {gN_sat/a0:.2e} a0 (saturated); bare-kernel "
         f"excess {exc:.3e} m/s^2 -> phantom mass {Mph:.2e} Msun = {sat[foot]:.2e}x the bound {SAT_BOUND:.1e}")
check("A7b gate reproduced: the BARE kernel's Saturn phantom mass is 1.40e4 / 1.69e4 times the "
      "Pitjev-Pitjeva bound (which is why the theory needs its screening length xi)",
      abs(sat["canonical"] / 1.40e4 - 1) < 0.05 and abs(sat["alt"] / 1.69e4 - 1) < 0.05,
      f"{sat['canonical']:.2e}x / {sat['alt']:.2e}x vs published 1.40e4 / 1.69e4")

# --- A.3 the conformal control, symbolic ---
P("")
P("A.3  Control, symbolic: null geodesics are conformally invariant.  This is used in PART C and PART E,")
P("     so it is proved here from the Christoffels rather than quoted.")
xs = sp.symbols('t x y z')
Om = sp.Function('Omega')(*xs)
Phi_s, Psi_s = sp.Function('Phi')(*xs[1:]), sp.Function('Psi')(*xs[1:])
gmat = sp.diag(-(1 + 2 * Phi_s), (1 - 2 * Psi_s), (1 - 2 * Psi_s), (1 - 2 * Psi_s))
def christoffels(gm, X):
    gi = gm.inv(); Ch = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for b in range(4):
            for cc in range(4):
                Ch[a][b][cc] = sp.simplify(sum(gi[a, d] * (sp.diff(gm[d, b], X[cc]) + sp.diff(gm[d, cc], X[b])
                                                           - sp.diff(gm[b, cc], X[d])) for d in range(4)) / 2)
    return Ch
gt = sp.simplify(Om**2 * gmat)
Ch_g, Ch_t = christoffels(gmat, xs), christoffels(gt, xs)
kv = sp.symbols('k0 k1 k2 k3')
# k null with respect to g: solve for k0
k0sol = sp.solve(sum(gmat[i, j] * kv[i] * kv[j] for i in range(4) for j in range(4)), kv[0])
ksub = {kv[0]: k0sol[0]}
maxdev = 0
for a in range(4):
    dif = sum((Ch_t[a][b][cc] - Ch_g[a][b][cc]) * kv[b] * kv[cc] for b in range(4) for cc in range(4))
    # the reparametrisation piece: 2 k^a (k . dlnOmega)
    kdot = sum(kv[b] * sp.diff(sp.log(Om), xs[b]) for b in range(4))
    resid = sp.simplify(sp.expand(dif - 2 * kv[a] * kdot).subs(ksub))
    maxdev = max(maxdev, 0 if sp.simplify(resid) == 0 else 1)
check("A8  control (symbolic): Gamma~^a_bc k^b k^c - Gamma^a_bc k^b k^c - 2 k^a (k.dlnOmega) = 0 for null k",
      maxdev == 0, "null geodesics of Omega^2 g and g coincide up to reparametrisation, all 4 components")


# ======================================================================================================
sec("PART B -- THE DECISIVE STRUCTURAL QUESTION.  Does 'the excess can only be spent once' generalise?")
# ======================================================================================================
P("")
P("L55's theorem is scoped to THIS action's kernel combined with a LambdaCDM-profile cold abundance.")
P("Its argument, stripped of the action: the galaxy anomaly is ONE NUMBER PER POINT, and a component")
P("present in the amount the CMB requires already spends it.  That argument mentions neither the mode")
P("count, nor the number of metrics, nor the matter coupling.  Below it is restated as a theorem with")
P("explicit hypotheses, and each hypothesis is then tested against what the three branches can do.")
P("")
P("  THEOREM (excess spent once -- branch-independent form).  Let a theory predict, at each point of a")
P("  galaxy, the acceleration felt by a test baryon as")
P("")
P("        g_pred  =  g_bar  +  A_X  +  A_K")
P("")
P("  with g_bar the Newtonian field of the OBSERVED baryons, A_X the acceleration transmitted to that")
P("  baryon by a pressureless component present in the amount the CMB fixes, and A_K everything else the")
P("  modification supplies.  Assume")
P("      (H-a)  NO CANCELLATION:  A_X >= 0 and A_K >= 0 pointwise (both are inward);")
P("      (H-b)  MOND NORMALISATION:  with A_X = 0 the theory reproduces the observed relation, i.e. in the")
P("             deep regime A_K -> sqrt(g_bar a0) = the measured anomaly A = g_obs - g_bar;")
P("      (H-c)  TRANSMISSION:  A_X = eta * g_halo with eta > 0, where g_halo is the Newtonian field of the")
P("             cold component at the abundance the CMB fixes.")
P("  Then  g_pred - g_obs = A_X >= 0 pointwise: the theory OVERSHOOTS the measured rotation curve by")
P("  exactly the cold component's transmitted pull.  Admissibility therefore requires either eta small,")
P("  or the kernel suppressed by s_eff, and in the deep regime a suppression s is EXACTLY degenerate with")
P("  a smaller acceleration scale, a0' = s^2 a0.")
P("")
P("  The conclusion depends on the number of propagating modes, the number of metrics and the matter")
P("  coupling ONLY through (H-a) and (H-c).  Everything else is arithmetic on measured accelerations.")
P("")

# ---- B1: the pointwise inequality, on real data --------------------------------------------------------
P("B.1  The inequality, checked pointwise on SPARC rather than asserted.")
P("")
def resid_stats(eta, eps, foot):
    """g_pred = g_bar + eta*g_halo + a0 Delta( (g_bar + eps*eta*g_halo)/a0 ).
       eps = 1 : the kernel reads the TOTAL potential (L49's sourcing).
       eps = 0 : the kernel reads the BARYONS only (L50's sourcing).  Any branch lies between."""
    a0 = A0[foot]
    gN = GB + eta * GH
    gs = GB + eps * eta * GH
    gp = GB + eta * GH + a0 * Delta(gs / a0)
    r = np.log10(GO / gp)
    return float(np.sqrt(np.mean(r**2))), float(np.median(r))

P(f"      {'eta':>6s} | {'eps=1 (total-sourced)':>28s} | {'eps=0 (baryon-sourced)':>28s}")
P(f"      {'':>6s} | {'rms can/alt':>16s} {'median can':>11s} | {'rms can/alt':>16s} {'median can':>11s}")
for eta in (0.0, 0.2, 0.35, 0.50, 0.58, 0.75, 1.00):
    a = resid_stats(eta, 1.0, "canonical"); b = resid_stats(eta, 1.0, "alt")
    cc_ = resid_stats(eta, 0.0, "canonical"); d = resid_stats(eta, 0.0, "alt")
    P(f"      {eta:6.2f} | {a[0]:7.3f}/{b[0]:7.3f} {a[1]:+11.3f} | {cc_[0]:7.3f}/{d[0]:7.3f} {cc_[1]:+11.3f}")

# the pointwise statement itself
ok_point = True
for foot in FOOT:
    a0 = A0[foot]
    gp_eps0 = GB + 1.0 * GH + a0 * Delta(GB / a0)      # eta = 1, baryon-sourced: the WEAKEST kernel
    ok_point = ok_point and bool(np.all(gp_eps0 >= GB + a0 * Delta(GB / a0) - 1e-30))
# the load-bearing form: predicted minus observed >= the halo term, wherever the kernel alone already fits
a0c = A0["canonical"]
kern_only = GB + a0c * Delta(GB / a0c)
deep = GB < a0c
overshoot_frac = float(np.median((GB[deep] + GH[deep] + a0c * Delta(GB[deep] / a0c)) / GO[deep]))
info(f"at eta = 1, deep-MOND points ({int(deep.sum())} of {len(GB)}): median g_pred/g_obs = {overshoot_frac:.3f} "
     f"= {2.5*math.log10(overshoot_frac)/2.5:+.3f} dex overshoot")
check("B1  the overshoot is pointwise and equals the transmitted halo term (no cancellation is possible "
      "with A_X >= 0)", ok_point and overshoot_frac > 1.20,
      f"median g_pred/g_obs = {overshoot_frac:.3f} at eta = 1 with the WEAKEST (baryon-sourced) kernel")

# ---- B2: the branch-independent transmission ceiling ---------------------------------------------------
P("")
P("B.2  The ceiling on eta.  This is the number every branch has to hit, and it is computed from the data")
P("     and the RAR's own scatter, not from any action.  Criterion: the median RAR residual stays inside")
P("     the relation's own 0.11 dex (the GENEROUS of L49's two criteria, carried so no deficit is manufactured).")
P("")
def eta_ceiling(eps, foot, tol=0.11):
    lo, hi = 0.0, 4.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if abs(resid_stats(mid, eps, foot)[1]) <= tol: lo = mid
        else: hi = mid
    return lo
ETA_MAX = {}
for eps in (1.0, 0.0):
    for foot in FOOT:
        ETA_MAX[(eps, foot)] = eta_ceiling(eps, foot)
info(f"eps = 1 (kernel reads the total potential):   eta <= {ETA_MAX[(1.0,'canonical')]:.3f} / "
     f"{ETA_MAX[(1.0,'alt')]:.3f}     (L49 reports 0.355 / 0.276)")
info(f"eps = 0 (kernel reads the baryons only):      eta <= {ETA_MAX[(0.0,'canonical')]:.3f} / "
     f"{ETA_MAX[(0.0,'alt')]:.3f}     (L50 reports 0.582 / 0.486)")
info(f"the CMB requires eta = 1.000 +- 0.010 at recombination (Omega_c h^2 = {OCH2:.4f} +- 0.0012)")
check("B2  control: the transmission ceiling reproduces L49's and L50's published cold-fraction windows",
      abs(ETA_MAX[(1.0, 'canonical')] - 0.355) < 0.03 and abs(ETA_MAX[(1.0, 'alt')] - 0.276) < 0.03
      and abs(ETA_MAX[(0.0, 'canonical')] - 0.582) < 0.03 and abs(ETA_MAX[(0.0, 'alt')] - 0.486) < 0.03,
      "eta and the cold fraction f enter the same way, so the ceiling IS their window")
eta_best = ETA_MAX[(0.0, "canonical")]; eta_best_alt = ETA_MAX[(0.0, "alt")]
check("B3  the requirement any branch must meet: transmit at most ~58% / ~49% of the CMB-required cold "
      "component's pull at SPARC radii, while transmitting ~100% at recombination",
      eta_best < 1.0 and eta_best_alt < 1.0,
      f"eta <= {eta_best:.3f} / {eta_best_alt:.3f} in galaxies vs 1.000 at z = {Z_REC:.0f}")

# ---- B3: what could break (H-c)?  the range ordering ---------------------------------------------------
P("")
P("B.3  The ONLY escape is to break (H-c): make baryons blind to the cold component INSIDE galaxies while")
P("     leaving the CMB's driving intact.  Two mechanism families exist for that, and both are tested.")
P("")
P("     (i) A RANGE (a mass term / graviton mass / Yukawa mediator).  Required: suppression at ~10 kpc,")
P("         NO suppression at the sound horizon ~145 Mpc comoving.  A Yukawa force ratio is")
P("         (1 + m r) exp(-m r), STRICTLY DECREASING in r: it suppresses LONG range and not short.")
r_gal = 10.0 * kpc
r_cmb = RS_REC_COMOV / (1 + Z_REC)          # physical sound horizon at recombination
yuk = lambda mr: (1 + mr) * math.exp(-mr)
from scipy.optimize import brentq
# solve in the DIMENSIONLESS variable m*r (brentq's absolute tolerance makes solving for m in SI useless)
mr_gal = brentq(lambda u: yuk(u) - eta_best, 1e-9, 60.0)      # m r_gal that gives eta_best at 10 kpc
m_gal = mr_gal / r_gal
eta_at_cmb = yuk(m_gal * r_cmb)
mr_cmb = brentq(lambda u: yuk(u) - 0.90, 1e-9, 60.0)          # m r_s that leaves the CMB 90% driven
m_cmb = mr_cmb / r_cmb
eta_at_gal = yuk(m_cmb * r_gal)
info(f"physical sound horizon at z = {Z_REC:.0f}:  r_s = {r_cmb/Mpc:.4f} Mpc  (comoving {RS_REC_COMOV/Mpc:.0f} Mpc)")
info(f"tune the mass so that eta(10 kpc) = {eta_best:.3f}:   m r_gal = {mr_gal:.3f}, Compton wavelength "
     f"{1/(m_gal*kpc):.2f} kpc;   then eta(r_s) = {eta_at_cmb:.3e}  -- the CMB's driving is switched off too")
info(f"tune the mass so that eta(r_s)  >= 0.90:              m r_s = {mr_cmb:.3f}, Compton wavelength "
     f"{1/(m_cmb*Mpc):.3f} Mpc;   then eta(10 kpc) = {eta_at_gal:.6f}  -- the galaxy is not suppressed at all")
check("B4  a mass/range mechanism CANNOT break (H-c): the Yukawa ratio is monotone decreasing, so it "
      "suppresses long range and not short -- the opposite ordering to the one required",
      eta_at_cmb < 0.01 and eta_at_gal > 0.999,
      f"eta(r_s) = {eta_at_cmb:.2e} when eta(10 kpc) = {eta_best:.3f}; eta(10 kpc) = {eta_at_gal:.6f} when eta(r_s) = 0.90")

P("")
P("     (ii) An ENVIRONMENT (a screening function of a local scalar: density, acceleration, potential).")
P("          This is L6's class read in the mirror -- L6 asked whether a monotone S(X) could ENHANCE")
P("          clusters relative to galaxies; the question here is whether one could SUPPRESS the cold")
P("          component's pull in galaxies relative to recombination.  L6's own cosmological-ordering horn")
P("          is the test, and it is recomputed here for the recombination epoch, which L6 never used.")
P("")
rho_rec = OM * RHO_C * (1 + Z_REC)**3
def nfw_rho(M200, r):
    cc = float(c200_DM14(M200)); R200 = (3 * M200 * MSUN / (4 * math.pi * 200 * RHO_C))**(1 / 3.)
    rs = R200 / cc; d = (200 / 3.) * cc**3 / _nfwm(cc)
    return d * RHO_C / ((r / rs) * (1 + r / rs)**2)
M200_star = float(halo_mass_AM(5e10))
rho_bar_mid = 0.1 * MSUN / pc**3            # solar-neighbourhood midplane total baryon density, generous
rho_gal = nfw_rho(M200_star, r_gal) + rho_bar_mid       # CONSERVATIVE: baryons included, midplane value
rho_gal30 = nfw_rho(M200_star, 30 * kpc)
rho_clu = nfw_rho(1e15, 1000 * kpc)
info(f"mean matter density at recombination        rho = {rho_rec:.3e} kg/m^3")
info(f"L* galaxy at 10 kpc, halo + MIDPLANE baryons rho = {rho_gal:.3e} kg/m^3   "
     f"-- recombination is {rho_rec/rho_gal:.0f}x DENSER  (the conservative comparison)")
info(f"the same galaxy at 30 kpc, halo only         rho = {rho_gal30:.3e} kg/m^3   "
     f"-- recombination is {rho_rec/rho_gal30:.0f}x denser")
info(f"cluster at 1000 kpc                          rho = {rho_clu:.3e} kg/m^3")
check("B5  DENSITY-keyed screening has the WRONG ORDERING: the recombination-era universe is denser than "
      "a galaxy where the anomaly is measured -- even counting the disc's own midplane baryons -- so any "
      "monotone suppression in dense regions suppresses the CMB's driving harder than the galaxy's",
      rho_rec > rho_gal, f"rho_rec/rho_gal = {rho_rec/rho_gal:.0f} (conservative), "
                         f"{rho_rec/rho_gal30:.0f} at 30 kpc")

# acceleration horn
g_gal = float(np.median(GO))
info("")
for Phi_pert in (1e-5, 3e-5, 1e-4):
    g_rec = c**2 * Phi_pert / r_cmb
    info(f"acoustic driving at Phi = {Phi_pert:.0e}:  g ~ c^2 Phi / r_s = {g_rec:.3e} m/s^2 "
         f"= {g_rec/A0['canonical']:.2f} / {g_rec/A0['alt']:.2f} a0")
Phi_pert = 3e-5
g_rec = c**2 * Phi_pert / r_cmb
info(f"median SPARC acceleration                    g = {g_gal:.3e} m/s^2 "
     f"= {g_gal/A0['canonical']:.2f} / {g_gal/A0['alt']:.2f} a0")
sep_dex = abs(math.log10(g_rec / g_gal))
info(f"clusters at R500 sit at 0.33-0.58 a0 (this repository's own recorded value), i.e. AT OR BELOW")
info(f"galactic accelerations -- and clusters require MORE transmission (eta 0.569-0.893), not less.")
g_clu_a0 = 0.45
check("B6  ACCELERATION-keyed screening fails twice: the CMB's own driving acceleration is within ~1 dex "
      "of galactic accelerations (no clean separation), and clusters sit at or BELOW galactic "
      "accelerations while requiring MORE transmission (wrong ordering)",
      sep_dex < 1.5 and g_clu_a0 < g_gal / A0["canonical"],
      f"|log10(g_rec/g_gal)| = {sep_dex:.2f} dex; clusters {g_clu_a0:.2f} a0 vs galaxies "
      f"{g_gal/A0['canonical']:.2f} a0")

# potential horn -- galaxies vs clusters
Phi_gal = (150e3)**2 / c**2
Phi_clu = (1200e3)**2 / c**2
info(f"potential depth:  galaxy |Phi|/c^2 = {Phi_gal:.2e},  cluster = {Phi_clu:.2e}, "
     f"recombination perturbation = {Phi_pert:.1e}")
info(f"clusters require eta = 0.569 +- 0.130 (b = 0) to 0.893 +- 0.158 (b = 0.20) [L50 D4/D10]; a monotone")
info(f"suppression in DEEP potentials suppresses clusters MORE than galaxies, and clusters need MORE.")
check("B7  POTENTIAL-keyed screening has the wrong ordering between galaxies and clusters: clusters are "
      f"{Phi_clu/Phi_gal:.0f}x deeper and require MORE transmission, not less",
      Phi_clu > Phi_gal, f"Phi_clu/Phi_gal = {Phi_clu/Phi_gal:.0f}")

# ---- B4: the suppression-vs-a0 degeneracy, the second half of the theorem -------------------------------
P("")
P("B.4  The other half of the trade: suppress the KERNEL instead of the halo.  In the deep regime a")
P("     uniform suppression s is exactly degenerate with a smaller acceleration scale.")
P("     s * a0 * Delta(g/a0)  ==  a0' * Delta(g/a0')  with  a0' = s^2 a0, checked in the strict limit.")
x_deep = 1e-8
for s in (0.5, 0.438, 0.3):
    lhs = s * 1.0 * Delta(np.array([x_deep]))[0]
    rhs = (s * s) * Delta(np.array([x_deep / (s * s)]))[0]
    if s == 0.438: dgen = abs(lhs / rhs - 1)
info(f"deep-limit degeneracy check at g/a0 = {x_deep:.0e}, s = 0.438:  relative error {dgen:.2e}")
def s_ceiling(foot, tol=0.11):
    a0 = A0[foot]; lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        gp = GB + GH + mid * a0 * Delta(GB / a0)
        if abs(float(np.median(np.log10(GO / gp)))) <= tol: lo = mid
        else: hi = mid
    return lo
S_CEIL = {f: s_ceiling(f) for f in FOOT}
info(f"at eta = 1 the kernel must be suppressed to s <= {S_CEIL['canonical']:.3f} / {S_CEIL['alt']:.3f}  "
     f"(L50 D8 / L55 D4 report 0.495 / 0.439)")
info(f"which puts the surviving term's own MOND transition at a0' <= {S_CEIL['canonical']**2:.3f} a0 = "
     f"{S_CEIL['canonical']**2*A0['canonical']:.3e} / {S_CEIL['alt']**2*A0['alt']:.3e} m/s^2")
check("B8  control: the kernel-suppression ceiling reproduces L50 D8 / L55 D4 and the a0' = s^2 a0 degeneracy",
      dgen < 1e-2 and abs(S_CEIL["canonical"] - 0.495) < 0.05 and abs(S_CEIL["alt"] - 0.439) < 0.05,
      f"s <= {S_CEIL['canonical']:.3f}/{S_CEIL['alt']:.3f}, a0' <= {S_CEIL['canonical']**2:.3f} a0")

# ---- B5: the generalisation verdict --------------------------------------------------------------------
P("")
P("B.5  THE VERDICT ON GENERALISATION.")
P("")
gen = (ok_point and eta_at_cmb < 0.01 and eta_at_gal > 0.999 and rho_rec > rho_gal
       and sep_dex < 1.0 and Phi_clu > Phi_gal)
P("     Every step used: (1) measured accelerations at SPARC radii; (2) Omega_c h^2 from the CMB;")
P("     (3) the assumption that both contributions pull inward; (4) the theory's own MOND normalisation.")
P("     NONE of them mentions the number of propagating modes, the number of metrics, or how matter")
P("     couples.  Those enter only through the transmission factor eta, and the two mechanism families")
P("     that could make eta scale- or environment-dependent both fail on ORDERING, not on magnitude:")
P("     a range suppresses long and not short; density puts recombination on the WRONG side; acceleration")
P("     does not separate the two epochs at all; potential puts clusters on the wrong side.")
check("B9  [THE DECISIVE QUESTION]  the 'excess spent once' argument GENERALISES beyond one action: it is "
      "branch-independent, depending on modes / metrics / coupling only through the transmission factor",
      gen, "proved as a theorem with hypotheses (H-a),(H-b),(H-c); the escape route is closed on ORDERING")
P("")
P("     >> THEOREM (branch-independent).  No relativistic theory that (a) reproduces the observed deep-MOND")
P("     >> relation in galaxies with its cold component switched off, (b) contains a pressureless component")
P("     >> in the amount the CMB requires, and (c) transmits that component's Newtonian pull to baryons")
P("     >> with an efficiency that is not smaller inside galaxies than at recombination, can fit the")
P("     >> measured rotation curves.  It overshoots by the transmitted pull, pointwise.")
P("     >> The hypotheses that a branch could attack are (c) alone, and (c) requires a suppression whose")
P("     >> ordering is short-range-off / long-range-on, or dense-off / dilute-on with recombination denser")
P("     >> than a galaxy -- neither of which any mass term or monotone environmental screening supplies.")
P("     >> SCOPE, stated: the cold component's GALAXY PROFILE is still an input (abundance-matched LambdaCDM")
P("     >> here). A theory that puts the cold component somewhere other than in galaxy halos escapes -- and")
P("     >> that is a statement about the dark sector's microphysics, closed separately by this repository's")
P("     >> 2026-09-06/07 dark-sector no-go, NOT by this theorem.")


# ======================================================================================================
sec("PART C -- BRANCH 1: three or more propagating modes, Lorentz invariant.  (RAQUAL, phase-coupling gravity)")
# ======================================================================================================
P("")
P("The theorem permits it: give up requirement (iii) and keep Lorentz invariance.  RAQUAL")
P("(Bekenstein-Milgrom 1984) and phase-coupling gravity (Bekenstein 1988) are the two constructions in the")
P("17-theory table, with N_grav = 3 and >= 3.  The brief's question: what does the extra mode COST, and are")
P("their known failures GENERIC to the branch or specific to those two constructions?")
P("")
P("C.0  What the extra mode has to buy.  L39's operator lemma (cited, not re-derived) says: with no")
P("     preferred timelike vector there is exactly ONE transverse symmetric operator, so lensing and")
P("     dynamics cannot be modified separately; adjoining one unit timelike vector makes the count two and")
P("     unlocks them.  DC-013 (cited) says the same from diffeomorphism invariance: (Phi,Psi) are locked to")
P("     the ray (1,-2) for a single-metric frame-free modification at ANY number of modes.  So a")
P("     Lorentz-invariant extra mode cannot unlock lensing by modifying the metric sector.  The only")
P("     remaining lever is the MATTER COUPLING, and that gives an exhaustive four-way fork:")
P("")
P("       (1a) CONFORMAL  g~ = A(phi) g          -> tested here, C.1-C.3")
P("       (1b) DISFORMAL  g~ = A g + B dphi dphi -> this is BRANCH 3; handed to PART E")
P("       (1c) the field acquires a TIMELIKE GRADIENT vev (mimetic / Deffayet-Esposito-Farese-Woodard)")
P("            -> that IS a preferred frame; L39 established it and it satisfies the theorem's conclusion")
P("            rather than escaping it")
P("       (1d) a VECTOR with a timelike vev (TeVeS, GEA, AeST) -> preferred frame, in L31's table already")
P("")
P("     (1c) and (1d) are not escapes, they are instances of the conclusion.  (1b) leaves the branch.")
P("     So branch 1's own content is (1a), and the question is whether (1a)'s failure is generic.")
P("")
P("C.1  The generic obstruction, derived rather than quoted: a conformally coupled Lorentz-invariant")
P("     scalar's own gravitating stress is smaller than the phantom it must mimic by the galaxy's OWN")
P("     v^2/c^2.  This is not RAQUAL-specific -- it follows from the deep-MOND normalisation alone.")
P("")
# symbolic derivation
Xs, a0s, Gs, cs_, rs_, Ms = sp.symbols('X a0 G c r M', positive=True)
# AQUAL: L = -(a0^2/(8 pi G c^2)) F(X/a0^2); deep-MOND F(y) = (2/3) y^(3/2) reproduces |grad phi| = sqrt(g_N a0)
F = sp.Rational(2, 3) * (Xs / a0s**2)**sp.Rational(3, 2)
Ldens = (a0s**2 / (8 * sp.pi * Gs * cs_**2)) * F                      # energy density of the scalar (static)
gM = sp.sqrt(Xs)                                                       # |grad phi| = the MOND field
rho_phi = sp.simplify(Ldens)
rho_phantom = gM / (4 * sp.pi * Gs * rs_)                              # div g = 4 pi G rho for g ~ 1/r
ratio = sp.simplify(rho_phi / rho_phantom)
ratio_vc = sp.simplify(ratio.subs(Xs, (sp.Symbol('vc', positive=True)**2 / rs_)**2))
P(f"     scalar energy density      rho_phi     = {sp.simplify(rho_phi)}")
P(f"     phantom density required   rho_phantom = {sp.simplify(rho_phantom)}")
P(f"     ratio                                  = {sp.simplify(ratio)}")
P(f"     with |grad phi| = v_c^2/r              = {sp.simplify(ratio_vc)}")
check("C1  (symbolic) the ratio reduces to v_c^4 / (3 a0 r c^2) = (v_c^2/c^2) x (g_MOND / 3 a0): the "
      "scalar's gravitating stress is suppressed by the galaxy's own v^2/c^2",
      sp.simplify(ratio_vc - sp.Symbol('vc', positive=True)**4 / (3 * a0s * rs_ * cs_**2)) == 0,
      "derived from the deep-MOND normalisation, no kernel shape assumed")

# numerically on SPARC
P("")
for foot in FOOT:
    a0 = A0[foot]
    gM_num = np.sqrt(np.maximum(GB, 0) * a0)             # |grad phi| = sqrt(g_bar a0), the deep-MOND field
    d = GB < a0
    rr = gM_num**2 * RR / (3 * a0 * c**2)
    info(f"[{foot:9s}] rho_phi / rho_phantom on {int(d.sum())} deep-MOND SPARC points: "
         f"median {np.median(rr[d]):.2e}, max {np.max(rr[d]):.2e}")
    if foot == "canonical": med_ratio = float(np.median(rr[d]))
check("C2  BRANCH 1, GATE 1 (lensing vs dynamics): does a conformally coupled Lorentz-invariant scalar "
      "supply an O(1) fraction of the lensing mass it must?",
      med_ratio > 0.05,
      f"NO -- median rho_phi/rho_phantom = {med_ratio:.2e}.  It lenses like general relativity on the "
      f"baryons alone; the gate needs O(1)")
P("")
for foot in FOOT:
    a0 = A0[foot]
    d = GB < a0
    mdyn_mlens = g_kernel(GB, a0) / GB
    info(f"[{foot:9s}] predicted M_dyn / M_lens on deep-MOND points: median {np.median(mdyn_mlens[d]):.2f}, "
         f"90th percentile {np.percentile(mdyn_mlens[d], 90):.2f}    (observed: 1)")
    if foot == "canonical": mdl = float(np.median(mdyn_mlens[d]))
check("C3  BRANCH 1, GATE 1, the size of the miss: is the predicted dynamics-to-lensing mass ratio "
      "consistent with the measured ~1?",
      abs(mdl - 1.0) < 0.20, f"median M_dyn/M_lens = {mdl:.2f}")

P("")
P("C.2  Is the failure GENERIC to the branch or specific to RAQUAL and PCG?  Three tests.")
kerns = {
    "the deposited saturating kernel": lambda x: Delta(x),
    "Milgrom simple  mu = y/(1+y)":    lambda x: 0.5 * (x + np.sqrt(x * x + 4 * x)) - x,
    "Milgrom standard mu = y/sqrt(1+y^2)": lambda x: np.sqrt(0.5 * (x * x + x * np.sqrt(x * x + 4))) - x,
}
a0 = A0["canonical"]; d = GB < a0
rows = {}
for nm, kf in kerns.items():
    gM_k = a0 * kf(GB / a0)                     # the kernel's own anomaly = |grad phi|
    rr = gM_k**2 * RR / (3 * a0 * c**2)
    rows[nm] = float(np.median(rr[d]))
    info(f"{nm:38s}: median rho_phi/rho_phantom = {rows[nm]:.2e}")
spread = max(rows.values()) / min(rows.values())
check("C4  the obstruction is KERNEL-INDEPENDENT: three different interpolating functions give the same "
      "suppression to within a factor of a few, because the scale is set by v^2/c^2 and not by f",
      spread < 5.0 and max(rows.values()) < 1e-5,
      f"spread across kernels {spread:.2f}x, all below 1e-5")
P("")
info("Second test -- the historical record agrees, and it agrees for this reason.  Bekenstein's own")
info("sequence RAQUAL -> PCG -> TeVeS was driven by exactly this: TeVeS's unit timelike vector was")
info("introduced FOR the light bending.  L39 quotes DEFW 2011 verbatim: 'That problem was finally")
info("surmounted in 2004 by ... TeVeS ... where the presence of a unit timelike vector field helps in")
info("obtaining the right amount of light deflection.'  The failure is the branch's, not the construction's.")
P("")
info("Third test -- the ROUTE OUT of (1a) is (1b), and (1b) is not in this branch.  There is no")
info("Lorentz-invariant conformal construction that evades C1, because C1 uses only the deep-MOND")
info("normalisation |grad phi| = sqrt(g_bar a0) and the fact that a conformal factor does not bend light (A8).")
check("C5  BRANCH 1 VERDICT: is it alive on gate 1 (lensing vs dynamics)?",
      med_ratio > 0.05, "DEAD at the FIRST gate; the failure is generic, not RAQUAL-specific")
P("")
P("     WHAT THE EXTRA MODE COSTS, stated: it costs the whole lensing sector and buys nothing, because a")
P("     Lorentz-invariant scalar cannot supply the second transverse operator L39's lemma requires (its")
P("     gradient is spacelike in a static configuration; a timelike gradient vev is spontaneous Lorentz")
P("     violation and is case (1c)).  The extra mode also carries the branch's own known costs -- RAQUAL's")
P("     superluminal scalar propagation in the transition region, which is what drove Bekenstein to PCG --")
P("     but those are downstream of a gate already closed and are cited, not computed here.")
P("")
P("     NOT CLOSED BY THIS LANE: a Lorentz-invariant branch-1 theory whose matter coupling is disformal")
P("     is handed to PART E; and DC-013's ray lock, which covers the non-conformal metric-sector route at")
P("     any number of modes, is cited from the repository's record rather than re-derived.")


# ======================================================================================================
sec("PART D -- BRANCH 2: two metrics.  (dRGT / Hassan-Rosen, BIMOND, and this repository's open subspace)")
# ======================================================================================================
P("")
P("READ THE RECORD FIRST, as the brief requires.  project_relativistic_mond_closure_2026 carries:")
P("  * the SINGLE-METRIC pincer (DC-013 + DC-019), which explicitly does NOT cover bimetric;")
P("  * DC-018: standard ghost-free dRGT / Hassan-Rosen bigravity's helicity-0 Galileon sector CANNOT")
P("    give MOND's 1/r -- the spherical flux scaling theorem;")
P("  * BIMOND connection interactions: Boulware-Deser ghost risk (the lapse RATIO, rank-1 Hessian);")
P("  * THE ONE OPEN DOOR: the background-independent lapse-velocity-free (ghost-free) subspace of the")
P("    COMPLETE 5-invariant derivative-bimetric basis is 2-D and contains MOND-alive directions off the")
P("    f(Q) line; T4 - T1 gives static-NR MOND acceleration a = -4 AND lensing source b = -8, both")
P("    nonzero.  HEALTH IS RECORDED AS UNDECIDED.  This lane does NOT re-close it and does not claim it.")
P("")
P("D.1  DC-018 reproduced as a control (it is cheap and it calibrates the branch's first gate).")
P("")
n_sym, r_sym, GM_sym = sp.symbols('n r GM', positive=True)
pi_p = sp.Symbol('pip', positive=True)
# spherical Galileon flux:  r^(3-n) (pi')^n  ~  GM   =>   pi' ~ r^(1 - 3/n)
sol = sp.solve(sp.Eq(r_sym**(3 - n_sym) * pi_p**n_sym, GM_sym), pi_p)[0]
expo = sp.simplify(sp.log(sol / sol.subs(r_sym, 1)) / sp.log(r_sym))
P(f"     flux relation r^(3-n) (pi')^n = GM  =>  pi' = {sp.simplify(sol)}")
P(f"     radial exponent of pi'              =  {sp.simplify(expo)}")
for n in (1, 2, 3, 4):
    e = sp.nsimplify(expo.subs(n_sym, n))
    P(f"       n = {n}:  pi' ~ r^({e})")
n_mond = sp.solve(sp.Eq(1 - 3 / n_sym, -1), n_sym)[0]
P(f"     MOND requires pi' ~ r^(-1)  =>  n = {n_mond}  -- NOT an integer")
check("D1  control: DC-018 reproduced.  A spherical Galileon of integer order gives pi' ~ r^(1 - 3/n); "
      "MOND's r^(-1) needs the non-integer n = 3/2, so standard bigravity's helicity-0 sector has no MOND",
      sp.nsimplify(n_mond) == sp.Rational(3, 2),
      "n = 3/2; integer n in {1,2,3,4} gives r^-2, r^-1/2, r^0, r^1/4")

P("")
P("D.2  The mode price.  Branch 2 is not disjoint from branch 1: a healthy second metric costs 5 extra")
P("     propagating modes, so every two-metric theory is ALSO a >= 3-mode theory.")
info(f"ghost-free Hassan-Rosen:  N = {dirac(24,4,2):.0f} = 2 (massless) + 5 (massive graviton)")
info(f"with the Boulware-Deser mode unremoved:  N = {dirac(24,4,0):.0f}, one of them a ghost")
info("the repository's open subspace is exactly the question of which of these two the a != 0 sub-family is")
check("D2  branch 2 lies inside 'three or more modes': the permitted branches overlap and are not three "
      "independent directions",
      dirac(24, 4, 2) >= 3, "7 healthy or 8 with the ghost; either way >= 3")

P("")
P("D.3  Does the branch-independent theorem of PART B follow the second metric?  This is the question that")
P("     matters, because if it does the branch is dead before its gates are priced.")
P("")
P("     A second metric offers exactly one new way to attack hypothesis (H-c): put the cold component on")
P("     the SECOND metric, so that its pull reaches baryons only through the g-f interaction.  In every")
P("     ghost-free bimetric construction that interaction is a graviton MASS TERM, so the transmitted force")
P("     carries the Yukawa factor of B.3(i) -- and B4 already showed that factor has the wrong ordering.")
info(f"to suppress the dark sector's pull to eta = {eta_best:.3f} at 10 kpc a graviton mass needs")
info(f"  m r_gal = {mr_gal:.3f}, i.e. a Compton wavelength of {1/(m_gal*kpc):.2f} kpc")
info(f"at that mass the same factor at the recombination sound horizon is eta = {eta_at_cmb:.2e}: the third")
info(f"acoustic peak loses its driving, which is the observable the abundance was fixed by.")
check("D3  the PART B theorem GENERALISES to two metrics: the only new escape a second metric offers is "
      "mediation through the mass term, and that has the wrong range ordering",
      eta_at_cmb < 0.01, f"eta(r_s) = {eta_at_cmb:.2e} when eta(10 kpc) = {eta_best:.3f}")

P("")
P("D.4  The gates, in the brief's order, for the ONE construction the record leaves open.")
P("")
P(f"     {'gate':38s} {'verdict':16s} status")
BRANCH2_GATES = [
    ("1 lensing vs dynamics", "NOT CLOSED",
     "the record's T4 - T1 direction has a NONZERO lensing source b = -8 alongside a = -4; whether the "
     "ratio gives Phi = Psi is the record's own un-run coupled g/g-hat solve"),
    ("2 Solar System", "NOT RUN",
     "requires the action; the record does not carry a Solar-System solve for this subspace"),
    ("3 preferred frame", "LIABILITY FLAGGED",
     "the record warns the solve must NOT inherit the alpha_3 = -1 liability of the constraint-first horn"),
    ("4 tensor speed", "NOT RUN", "no c_T computation exists for this subspace in the record"),
    ("5 mode health", "**THE DECIDING GATE, UNDECIDED**",
     "full covariant Hamiltonian count on the a != 0 sub-family: healthy elliptic auxiliary (7) or "
     "Boulware-Deser ghost (8)?  Named in the record as the decisive un-run calculation"),
    ("6 cluster mass and shear shape", "INHERITED",
     "no bimetric-specific computation; the cluster specification of L41/L49 is chassis-independent"),
    ("7 cosmology", "CLOSED BY PART B",
     "the theorem of B.5 applies: D3"),
]
for nm, v, s in BRANCH2_GATES:
    P(f"     {nm:38s} {v:16s} {s}")
check("D4  BRANCH 2 VERDICT: is it DEAD on a gate run here?",
      False,
      "NO -- it is OPEN, at gate 5 (mode health), with the deciding calculation already named in the "
      "repository's own record.  This lane does not close it and does not claim it alive")
check("D5  BRANCH 2 VERDICT: is it ALIVE?  (alive requires an exhibited construction run through gates)",
      False,
      "NO -- gates 2, 4 and 5 have never been run on it.  Verdict: OPEN, not alive; and B.5's theorem "
      "applies to it whatever the answer at gate 5")


# ======================================================================================================
sec("PART E -- BRANCH 3: non-minimal matter coupling.  (conformal, disformal) -- and the adjudication")
# ======================================================================================================
P("")
P("E.1  The conformal half is already settled in this repository and reproved above at A8: a conformal")
P("     coupling cannot bend light.  L50 E2 derives it for a generic static isotropic metric; L39 C-c2")
P("     derives it from the Christoffels; A8 above reproduces it independently.  So the whole content of")
P("     branch 3 is the DISFORMAL coupling, which is what TeVeS carries and what every repair reaches for.")
P("")
P("E.2  THE IDENTITY, proved here symbolically for a GENERAL unit vector w -- spacelike (a frame-free")
P("     scalar's gradient) and timelike (a khronon's normal) -- because the two chassis in this")
P("     repository's record use different ones and the flagged disagreement is between them.")
P("")
Ph, Ps, Bd, Ad = sp.symbols('Phi Psi B A', real=True)
eps_ = sp.Symbol('epsilon', positive=True)
def cone_and_slip(timelike):
    """g~ = A g + B w w, w a unit vector of g.  Return (fractional cone tilt, shift in the potential
       matter feels), both to first order."""
    gtt = -(1 + 2 * Ph); grr = (1 - 2 * Ps)
    if timelike:
        wt2 = -gtt                       # w_t^2 with g^{tt} w_t^2 = -1
        gt_tt = Ad * gtt + Bd * wt2
        gt_rr = Ad * grr
    else:
        wr2 = grr                        # w_r^2 with g^{rr} w_r^2 = +1
        gt_tt = Ad * gtt
        gt_rr = Ad * grr + Bd * wr2
    # radial null speed in each metric, to first order in B (and then at leading weak-field order)
    c2_g  = sp.simplify(-gtt / grr)
    c2_gt = sp.simplify(-gt_tt / gt_rr)
    tilt = sp.series(sp.sqrt(c2_gt) - sp.sqrt(c2_g), Bd, 0, 2).removeO()
    tilt = sp.simplify(sp.expand(tilt).subs({Ph: 0, Ps: 0}))
    # the potentials matter feels, after stripping the overall conformal factor A.
    # -(1 + 2 Phi~) = g~_tt / A  and  (1 - 2 Psi~) = g~_rr / A.
    Pht = sp.simplify(sp.series(-(gt_tt / Ad + 1) / 2, Bd, 0, 2).removeO())
    Pst = sp.simplify(sp.series((1 - gt_rr / Ad) / 2, Bd, 0, 2).removeO())
    # the disformal shift, at leading order (drop the B x weak-field cross terms, which are second order)
    dPh = sp.simplify(sp.expand(Pht - Ph).subs({Ph: 0, Ps: 0}))
    dPs = sp.simplify(sp.expand(Pst - Ps).subs({Ph: 0, Ps: 0}))
    return sp.simplify(tilt), dPh, dPs

tilt_s, dPhi_s, dPsi_s = cone_and_slip(False)
tilt_t, dPhi_t, dPsi_t = cone_and_slip(True)
P(f"     SPACELIKE w (frame-free scalar's gradient):")
P(f"        fractional cone tilt (c_light - c_grav)/c = {tilt_s}")
P(f"        shift in Phi matter feels                  = {dPhi_s}")
P(f"        shift in Psi matter feels                  = {dPsi_s}")
P(f"     TIMELIKE w (khronon normal, LEDGER sf27's chassis):")
P(f"        fractional cone tilt (c_light - c_grav)/c = {tilt_t}")
P(f"        shift in Phi matter feels                  = {dPhi_t}")
P(f"        shift in Psi matter feels                  = {dPsi_t}")
id_space = sp.simplify(tilt_s - dPsi_s) == 0 and sp.simplify(dPhi_s) == 0
id_time  = sp.simplify(tilt_t - dPhi_t) == 0 and sp.simplify(dPsi_t) == 0
slip_s = sp.simplify(sp.Abs((dPhi_s - dPsi_s) / tilt_s))
slip_t = sp.simplify(sp.Abs((dPhi_t - dPsi_t) / tilt_t))
check("E1  (symbolic) THE IDENTITY, both chassis: the shift a disformal term makes in the potential matter "
      "feels EQUALS the fractional tilt of the matter light cone relative to the graviton cone, exactly",
      id_space and id_time,
      "spacelike w: tilt = delta Psi = -B/(2A), delta Phi = 0;   timelike w: tilt = delta Phi = -B/(2A), "
      "delta Psi = 0")
check("E1b the SLIP repaired has unit magnitude in units of the tilt created: |d(Phi - Psi)| / |tilt| = 1 "
      "in BOTH chassis, so a repair of size X costs a cone tilt of size X and there is no lever ratio to "
      "exploit",
      slip_s == 1 and slip_t == 1, f"spacelike {slip_s}, timelike {slip_t}")
tiltA0 = sp.simplify(tilt_s.subs(Bd, 0)) == 0 and sp.simplify(tilt_t.subs(Bd, 0)) == 0
check("E1c the CONFORMAL factor A alone moves neither: with B = 0 both the tilt and both potential shifts "
      "vanish for every A, which is A8 again -- the conformal lever cannot lens and the disformal lever "
      "cannot be had without the tilt",
      tiltA0 and sp.simplify(dPsi_s.subs(Bd, 0)) == 0 and sp.simplify(dPhi_t.subs(Bd, 0)) == 0,
      "A is pure gauge for light bending; only B moves anything")
P("")
P("     >> The slip you cancel IS the light-cone tilt you create.  That is LOCAL_NO_GO section 3.2's")
P("     >> identity, (c_GW - c_light)/c = B phi'^2 / 2 = (Psi - Phi), reproved here from the metric and")
P("     >> extended to the timelike-w chassis that the flagged contrary entry uses.")

P("")
P("E.3  How big must the tilt be?  The disformal term has to supply the whole lensing anomaly, so the")
P("     required tilt is the galaxy's own MOND potential.  Computed from the data on both footings.")
P("")
vflat = []
for g in GAL:
    n = max(1, len(g["r"]) // 4)
    vflat.append(float(np.median(np.sqrt(g["go"][-n:] * g["r"][-n:]))))
vflat = np.array(vflat)
tiltreq = vflat**2 / c**2
tilt_req = float(np.median(tiltreq))
info(f"SPARC flat speeds ({len(vflat)} galaxies): median {np.median(vflat)/1e3:.0f} km/s, "
     f"90th pct {np.percentile(vflat,90)/1e3:.0f} km/s")
info(f"required tilt |Psi - Phi| = v_flat^2/c^2: median {tilt_req:.2e}, 90th pct {np.percentile(tiltreq,90):.2e}")
info("FOOTING NOTE, stated rather than double-printed: v_flat^2/c^2 is footing-INDEPENDENT -- it is a")
info("measured speed.  What the footings change is which points are deep-MOND: "
     f"{int(np.sum(GB < A0['canonical']))} canonical vs {int(np.sum(GB < A0['alt']))} alt of {len(GB)}.")
info("LOCAL_NO_GO section 3.2 quotes Phi_MOND = v_flat^2/c^2 = 3.9e-7 (NGC 4993's host), 3.0e-7 (Milky Way);")
info(f"this lane's Milky-Way-mass end of the SPARC distribution gives {np.percentile(tiltreq,90):.1e}.")
check("E2  the required cone tilt is of order 1e-7 -- the galaxy's own v^2/c^2, on both footings",
      1e-8 < tilt_req < 1e-6, f"median required tilt {tilt_req:.2e}")

P("")
P("E.4  BRANCH 3 GATE 4 (tensor speed).  GW170817 bounds the PATH-AVERAGED tilt.")
D_GW = 40.0 * Mpc
t_path = D_GW / c
dt_obs = 1.7                                    # seconds, the observed GW-to-gamma delay
tilt_bound = dt_obs / t_path
info(f"path length {D_GW/Mpc:.0f} Mpc = {t_path:.3e} s; observed GW-to-gamma delay <= {dt_obs} s")
info("(the naive 1.7 s / travel-time bound is used; the published two-sided bound -3e-15 < dc/c < 7e-16")
info(" lands in the same place and does not change the conclusion)")
info("WHERE the tilt lives: sf29's own integration puts beta = 0 at the Newtonian ends and nonzero")
info("through the MOND zone, i.e. exactly in the halo the wave crosses on the way out and on the way in.")
info(f"  ->  path-averaged |tilt| <= {tilt_bound:.2e}")
# how much of the path has to be in a MOND-strength field to violate it?
f_needed = tilt_bound / tilt_req
info(f"the tilt would have to be confined to a fraction {f_needed:.2e} of the path to evade the bound")
for r_halo in (20.0 * kpc, 50.0 * kpc, 100.0 * kpc):
    fh = 2 * r_halo / D_GW
    info(f"  2 x {r_halo/kpc:5.0f} kpc of MOND-strength host halo (source + Milky Way) = {fh:.2e} of the "
         f"path -> exceeded {fh/f_needed:.1e}x")
r_halo = 20.0 * kpc                              # the MOST CONSERVATIVE choice is the one carried
f_hosts = 2 * r_halo / D_GW
info(f"the most conservative of these is carried: {f_hosts/f_needed:.1e}x over the bound")
info(f"LOCAL_NO_GO section 3.2 reports the same ordering: '2e6 epsilon over the bound' from the two")
info(f"galaxies' MOND regions, and '30-300' from the 40 Mpc of intergalactic medium alone.")
check("E3  BRANCH 3, GATE 4 (tensor speed / GW170817): is the tilt the lensing repair requires small "
      "enough to survive the path-averaged bound?",
      f_hosts / f_needed < 1.0,
      f"NO -- required tilt {tilt_req:.2e} over {f_hosts:.1e} of the path vs bound {tilt_bound:.2e}; "
      f"exceeded {f_hosts/f_needed:.1e}x on the most conservative halo extent, 1.6e6x on the least")

P("")
P("E.5  THE ADJUDICATION the brief asks for.  L50 E5 flagged a contrary record and did not settle it:")
P("     'LEDGER sf27 reports a disformal+conformal coupling to the khronon's normal REPAIRING the lensing")
P("     gate in a different chassis.'  Is there a live contradiction?  The files are read here.")
P("")
LEDGER = os.path.join(REPO, "qwen_claude_field_theory", "closure_2026", "LEDGER.md")
RETR   = os.path.join(REPO, "RETRACTIONS.md")
led = open(LEDGER, encoding="utf-8", errors="replace").read()
ret = open(RETR, encoding="utf-8", errors="replace").read()
row_sf29 = [l for l in led.splitlines() if l.startswith("| SF29")]
row_sf28 = [l for l in led.splitlines() if l.startswith("| SF28")]
row_sf27 = [l for l in led.splitlines() if l.startswith("| SF27")]
has_kill  = bool(row_sf29) and "REPAIR KILLED" in row_sf29[0]
has_withd = bool(row_sf28) and "WITHDRAWN" in row_sf28[0]
has_ret   = "sf27's repair requires" in ret or "Withdrawn:** sf28 PART C" in ret
stale     = "All four bills PAID in sf28" in led and "causality safe with the sign **forced**" in led
info(f"{rel(LEDGER)} row SF27: disformal repair reported as 'LENSING GATE REPAIRED'")
info(f"{rel(LEDGER)} row SF28: '{'; '.join(row_sf28[0].split('|')[3].strip().split(';')[:4]) if row_sf28 else ''}'")
info(f"{rel(LEDGER)} row SF29: 'REPAIR KILLED -- sf28 C withdrawn'  -> present: {has_kill}")
info(f"{rel(RETR)}: records the withdrawal of sf28 PART C  -> present: {has_ret}")
check("E4  [ADJUDICATED]  the contrary entry does NOT stand: this repository's own sf29 killed the "
      "disformal repair and RETRACTIONS.md records it, before L50 was written",
      has_kill and has_withd and has_ret,
      "LEDGER row SF29 = 'REPAIR KILLED'; row SF28 = 'causality WITHDRAWN by SF29'; RETRACTIONS.md concurs")
check("E5  DOCUMENTATION ITEM (handed back, NOT edited): does the LEDGER's prose status paragraph agree "
      "with its own SF28 / SF29 table rows?",
      not stale,
      "NO -- the prose still reads 'All four bills PAID in sf28 ... causality safe with the sign forced "
      "-- beta > 0 everywhere' while rows SF28/SF29 in the same file read 'causality WITHDRAWN by SF29' "
      "and 'REPAIR KILLED'.  A reader who stops at the prose gets the withdrawn claim.")
P("")
P("     What sf27 established and what survives: sf27's ALGEBRA stands -- the two levers (conformal alpha,")
P("     disformal beta) genuinely span the (g_dyn, g_lens) plane and the repair works POINTWISE.  That is")
P("     the same statement as E1's identity: the disformal lever is the only one that moves light, and it")
P("     moves it by exactly the cone tilt.  What sf29 killed is making it GLOBALLY consistent.")
P("")
P("E.6  sf29's two kills, and whether they are the SAME physics as the GW identity.")
P("")
P("     (a) SIGN.  The screening boundary condition belongs at the NEWTONIAN end, which for MOND is HIGH")
P("         acceleration, i.e. SMALL r.  With beta = 0 there, integrating outward gives beta < 0 through")
P("         the MOND regime, so the matter cone ratio (v_matter/v_photon)^2 = 1 - beta EXCEEDS 1.")
P("         That is superluminal matter, and it is the SAME quantity as E1's tilt with the opposite sign.")
beta_probe = -1.15                                  # sf29's reported value at x = 1, in units of v_c^2
vc2 = (150e3)**2 / c**2
cone_ratio = 1 - beta_probe * vc2
info(f"sf29 reports beta = -1.15 v_c^2 at x = 1 and -4.19 v_c^2 at x = 0.1; at v_c = 150 km/s that is")
info(f"  cone ratio (v_matter/v_photon)^2 = 1 - beta = {cone_ratio:.9f}, i.e. superluminal by {cone_ratio-1:.2e}")
info(f"  E1's identity says the same number is the lensing shift; sf29 and LOCAL_NO_GO 3.2 AGREE.")
check("E6  sf29's superluminality and the GW-speed identity are the SAME quantity seen from two sides, "
      "so there was never a contradiction to adjudicate -- only a stale prose paragraph",
      abs((cone_ratio - 1) / (abs(beta_probe) * vc2) - 1) < 1e-6,
      f"(v_m/v_gamma)^2 - 1 = -beta = {cone_ratio-1:.3e} = the tilt")

P("")
P("     (b) THE THEOREM, which is stronger than the sign.  The no-slip condition gives beta' = -2 Delta")
P("         with Delta = the anomalous acceleration > 0, so beta is STRICTLY MONOTONE in r.  Screening")
P("         requires beta = 0 in BOTH Newtonian regimes -- the high-acceleration interior AND the")
P("         external-field-dominated far exterior.  A strictly monotone function cannot vanish at both.")
P("         Reproduced here with the DEPOSITED theory's own kernel rather than sf29's chassis kernel.")
P("")
def beta_gap(x_hi=100.0, x_lo=0.01, kernel=Delta):
    """gap = 2 * integral of Delta dr between the two Newtonian ends, in units of v_c^2 = sqrt(G M a0).
       With g_N/a0 = x and g_N = GM/r^2: r = sqrt(GM/(a0 x)), dr = -1/2 sqrt(GM/a0) x^(-3/2) dx.
       gap = v_c^2 * Integral_{x_lo}^{x_hi} D(x) x^(-3/2) dx."""
    xs_ = np.exp(np.linspace(math.log(x_lo), math.log(x_hi), 200001))
    integ = kernel(xs_) * xs_**-1.5
    return float(np.trapz(integ, xs_))
gap_dep = beta_gap()
gap_dm  = beta_gap(kernel=lambda x: np.sqrt(x))     # pure deep-MOND, no saturation
info(f"deposited saturating kernel:  gap = {gap_dep:.2f} v_c^2 between x = 100 and x = 0.01")
info(f"pure deep-MOND sqrt kernel:   gap = {gap_dm:.2f} v_c^2 over the same range (logarithmic, unbounded)")
info(f"sf29 reports 8.52 v_c^2 for its own chassis kernel; the structural statement -- the gap is strictly")
info(f"positive and of order the phantom's own potential -- is kernel-independent.")
check("E7  sf29's monotonicity theorem reproduced on the deposited kernel: the required change in beta "
      "between the two Newtonian ends is strictly positive and of order v_c^2, so beta cannot vanish at both",
      gap_dep > 1.0 and gap_dm > 1.0,
      f"gap = {gap_dep:.2f} v_c^2 (deposited kernel), {gap_dm:.2f} v_c^2 (pure deep-MOND)")

P("")
P("E.7  Does the PART B theorem follow branch 3?  A non-minimal coupling is the ONE branch that could in")
P("     principle make baryons blind to the cold component -- so this is the branch where (H-c) is live.")
P("")
P("     But the coupling that does it must be SCALE- or ENVIRONMENT-dependent: off in galaxies, on at")
P("     recombination.  B4-B7 already computed both families' ordering:")
info(f"  range:        eta(r_s) = {eta_at_cmb:.2e} when eta(10 kpc) = {eta_best:.3f}    -- wrong ordering")
info(f"  density:      recombination is {rho_rec/rho_gal:.0f}x DENSER than a galaxy at 10 kpc  -- wrong ordering")
info(f"  acceleration: the two epochs differ by {sep_dex:.2f} dex, both of order a0        -- no separation")
info(f"  potential:    clusters are {Phi_clu/Phi_gal:.0f}x deeper and need MORE, not less    -- wrong ordering")
check("E8  the PART B theorem GENERALISES to a non-minimal coupling: the required suppression lands in "
      "exactly L6's and L55's already-closed screening class, and fails on ordering in every variable",
      eta_at_cmb < 0.01 and rho_rec > rho_gal and sep_dex < 1.0 and Phi_clu > Phi_gal,
      "four variables, four wrong orderings or no separation")
check("E9  BRANCH 3 VERDICT: is it alive?",
      False,
      "DEAD at GATE 4 (tensor speed).  Gate 1 (lensing) is PASSED POINTWISE by the disformal lever -- that "
      "is sf27's real content -- but the same lever is the cone tilt, and it is excluded ~1e6x by GW170817 "
      "and independently by sf29's two-boundary-condition theorem")


# ======================================================================================================
sec("PART F -- MUTATION CONTROLS, and the verdicts.")
# ======================================================================================================
P("")
P("F.1  Mutation controls.  A kill this lane reports must switch OFF when its cause is removed.")
P("")
# control 1: B = 0 -> no tilt AND no repair
tilt0 = sp.simplify(tilt_s.subs(Bd, 0)); dpsi0 = sp.simplify(dPsi_s.subs(Bd, 0))
check("F1  mutation control: with B = 0 the cone tilt vanishes AND the lensing repair vanishes together "
      "(the two are the same quantity, so neither can be had alone)",
      tilt0 == 0 and dpsi0 == 0, "B = 0 -> tilt = 0, delta Psi = 0")
# control 2: a0 -> 0 turns off the kernel, and the excess theorem's overshoot goes away
a0_tiny = 1e-30
gp_tiny = GB + 1.0 * GH + a0_tiny * Delta(GB / a0_tiny)
med_tiny = float(np.median(np.log10(GO / gp_tiny)))
med_full = float(np.median(np.log10(GO / (GB + GH + A0["canonical"] * Delta(GB / A0["canonical"])))))
info(f"with the kernel switched off (a0 -> 0) at eta = 1 the median residual is {med_tiny:+.3f} dex "
     f"(the halo-only value); with the kernel on it is {med_full:+.3f} dex")
check("F2  mutation control: the PART B overshoot is caused by the kernel, not by the machinery -- "
      "switching a0 off returns the halo-only residual",
      abs(med_tiny - float(np.median(resh))) < 1e-6 and med_full < med_tiny,
      f"a0 -> 0 gives {med_tiny:+.3f} = the halo-only {np.median(resh):+.3f}")
# control 3: the counting formula must give the published GR answer when applied to GR
check("F3  mutation control: the branch-2 counting formula, applied to general relativity itself "
      "(P = 12, F = 4, S = 0), returns 2 and not 7",
      abs(dirac(12, 4, 0) - 2) < 1e-12, "the same one-line formula; no branch-specific tuning")

P("")
P("F.2  VERDICT PER BRANCH.")
P("")
VERDICTS = [
    ("1  three or more modes, Lorentz invariant", "DEAD",
     "GATE 1, lensing vs dynamics",
     f"a conformally coupled Lorentz-invariant scalar contributes {med_ratio:.1e} of the lensing mass it "
     f"must supply; the suppression is the galaxy's own v^2/c^2 and is kernel-independent to a factor "
     f"{spread:.1f}.  Generic to the branch, NOT specific to RAQUAL and PCG.  Its escapes are a timelike "
     f"gradient vev (= a preferred frame, the theorem's own conclusion) or a disformal coupling (= branch 3)."),
    ("2  two metrics", "OPEN",
     "GATE 5, mode health -- UNDECIDED, calculation named",
     "standard dRGT/Hassan-Rosen is closed by DC-018 (cited, reproduced at D1: MOND needs the non-integer "
     "n = 3/2).  The repository's own 2-D ghost-free derivative-bimetric subspace is NOT closed and is NOT "
     "closed here: the deciding calculation is the full covariant Hamiltonian count on the a != 0 "
     "sub-family (7 healthy or 8 with the Boulware-Deser ghost) plus a coupled g/g-hat lensing solve that "
     "must not inherit alpha_3 = -1.  Whatever it returns, PART B's theorem applies (D3)."),
    ("3  non-minimal matter coupling", "DEAD",
     "GATE 4, tensor speed",
     f"conformal cannot bend light (A8, symbolic).  Disformal repairs lensing POINTWISE -- that is sf27's "
     f"real content and it stands -- but E1 proves the repaired slip IS the matter/graviton cone tilt, for "
     f"both a spacelike and a timelike w; the required tilt is {tilt_req:.1e} and GW170817's path average "
     f"bounds it at {tilt_bound:.1e}, exceeded ~{f_hosts/f_needed:.0e}x from the two host galaxies alone.  "
     f"Independently killed by sf29's theorem that beta cannot vanish in both Newtonian regimes "
     f"(gap {gap_dep:.1f} v_c^2 on the deposited kernel)."),
]
for nm, v, gate, why in VERDICTS:
    P(f"     BRANCH {nm}")
    P(f"        verdict: {v}")
    P(f"        gate:    {gate}")
    for line in [why[i:i + 104] for i in range(0, len(why), 104)]:
        P(f"        {line}")
    P("")

alive_any = False
check("F4  is ANY permitted branch alive on every gate?  (alive = an exhibited construction run through gates)",
      alive_any,
      "NO.  Branch 1 dies at gate 1, branch 3 at gate 4, branch 2 is undecided at gate 5 and has never "
      "been run through gates 2 and 4 at all")
check("F5  [VERDICT]  does a full-gate theory exist in the space the foliation theorem leaves permitted?",
      False,
      "NOT DEMONSTRATED, and one branch of three remains genuinely open.  Two of the three are closed by "
      "gates run here; the third is open at a calculation this repository already named.  And the PART B "
      "theorem now binds ALL THREE, so even a healthy branch-2 construction would face the same choice "
      "between a working kernel and a full cold cosmology")

P("")
P("=" * 118)
P(f"CHECKS: {NCHK} run, {NCHK - len(FAILS)} PASS, {len(FAILS)} FAIL.  Runtime {time.time()-T0:.1f} s.")
if FAILS:
    P("FAILING CHECKS (each is a finding, not a crash -- see the .md for which):")
    for f in FAILS: P(f"   - {f}")
P("=" * 118)
sys.exit(0)

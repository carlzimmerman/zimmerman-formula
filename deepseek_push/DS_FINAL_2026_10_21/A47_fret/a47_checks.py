"""A47 -- THE f_ret = 0.10 FACTOR: does the cold sector hold ten times the cosmic share?

Lane A47.  Reads only files already on disk:
  campaign_fresh_gravity/CFG416_supply_edge_confinement_512/FROZEN_CRITERIA.md   (the f_ret table)
  campaign_fresh_gravity/CFG804_catchment_supply_derived/README.md               (N = 1/f_ret, per bin)
  campaign_fresh_gravity/CFG801_settled_edge_vs_kids/README.md                   (+197 / +753 record)
  deepseek_push/DS_FINAL_2026_10_21/A18_two_ratios/a18_results.json              (N, f_ret, u, R_req)
  deepseek_push/DS_FINAL_2026_10_21/A44_no_edge/a44_results.json                 (Escan, N_required, CFG804)
  deepseek_push/DS_FINAL_2026_10_21/A29_u_radial/a29_results.json                (u per band)
  deepseek_push/DS_FINAL_2026_10_21/A43_cold_eos/a43_results.json                (f_ret = 2.195, the ceiling)

Question.  A44 buys the no-edge resolution with cold mass 5.364/f_ret = 53.64 M_b at f_ret = 0.10,
"ten times the cosmic share".  Two other lanes use the same symbol with a ceiling of 1: A18's
N = R_cosmic/f_ret with u = R_tot/N <= 1, and A43's f_ret <= 1 (the catchment ceiling).  Are these the
same object?  And is 53.64 M_b physically available for a 1e11 Msun galaxy?

Answer (this script).  There is ONE f_ret in CFG416 -- a retained *baryon fraction* -- and one derived
budget ratio N = R_cosmic/f_ret.  A43's f_ret is a second, different object (a cold-budget multiplier
against the catchment's cosmic share, f_c).  They coincide only on the cosmic-ratio locus.  A44's
model has f_c = 1.000 exactly: the factor 10 is *saturation* of the catchment's cold budget, not an
overdensity of 10.  The availability ceiling is not 10x the cosmic density; it is the catchment, and
the self-consistent CFG416 budget is N = 37.9-53.6 (>= 2.4x what the data require, N_req = 15.9).

Footings: a0 = 9.3603e-11 m/s^2 (canonical).  Deterministic, no network, stdlib only (sympy optional).
Exit 0 iff every check passes.  A47_MUTATE=<name> breaks one check group (see MUTATE.md).
"""
import json, math, os, re, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CFG = os.path.join(REPO, "campaign_fresh_gravity")
F416 = os.path.join(CFG, "CFG416_supply_edge_confinement_512", "FROZEN_CRITERIA.md")
F804 = os.path.join(CFG, "CFG804_catchment_supply_derived", "README.md")
F801 = os.path.join(CFG, "CFG801_settled_edge_vs_kids", "README.md")
DS = os.path.join(REPO, "deepseek_push", "DS_FINAL_2026_10_21")
MUT = os.environ.get("A47_MUTATE", "") or (sys.argv[1] if len(sys.argv) > 1 else "")
T0 = time.time()

OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))

# ------------------------------------------------------------------ constants (all from source files)
G      = 4.30091e-9        # Mpc (km/s)^2 / Msun
MPC_CM = 3.0856775814913673e24
MSUN_G = 1.98847e33
RHO_CRIT = 1.2607e11       # Msun/Mpc^3, h = 0.674 (A44 / CFG801)
OM, OL, H0 = 0.315, 0.685, 67.4
A0 = 9.3603e-11            # m/s^2 canonical
A0_MPC = A0 * 3.0856775814913673e22 / 1e6   # (km/s)^2 / Mpc
SUP = 5.364327223960661    # R_cosmic = (1-f_b)/f_b   (A18 numbers)
FB  = 0.15712579897450307  # f_b = omega_b/omega_m (A18 numbers)
H   = 0.674
SIG_C = 8.33               # km/s, THEORY 3.3 (cited by A43 K9)
DELTA_TA = (3 * math.pi / 4) ** 2   # 5.5517, spherical-collapse turnaround
RHO_COLD = (1 - FB) * OM * RHO_CRIT  # z=0 cosmic COLD density, Msun/Mpc^3
A47_MUT_SYSTEM = (MUT == "system")
FRET_A44 = 1.00 if A47_MUT_SYSTEM else 0.10      # the value A44 uses for the 53.64 M_b model
A47_MUT_DENSITY = (MUT == "density")
A47_MUT_FREEZE = (MUT == "freeze")

# ------------------------------------------------------------------ law profile
def s_edge(N):      return math.sqrt(N * (N + 1))          # r_e/r_M where m(x) = N
def m_law(x):       return 0.5 * (math.sqrt(1 + 4 * x * x) - 1)
def rM(Mb):         return math.sqrt(G * Mb / A0_MPC)      # Mpc
def r_of_delta(M, delta=200.0, rho=RHO_CRIT):
    return (3 * M / (4 * math.pi * delta * rho)) ** (1 / 3)
def r200(M):        return r_of_delta(M, 200.0, RHO_CRIT)
def r_ta(Mta):      return r_of_delta(Mta, DELTA_TA, OM * RHO_CRIT)
def r_zv(M):        return (G * M / H0 ** 2) ** (1 / 3)
def v_circ(M, r):   return math.sqrt(G * M / r)            # km/s
def M_bound(v, r):  return v * v * r / G                   # Msun
def vol(r):         return 4 * math.pi / 3 * r ** 3

# ------------------------------------------------------------------ CFG416 f_ret table
def fret416(logMta_h):
    """CFG416 FROZEN_CRITERIA 'declared f_ret(M_ta) (gas + stars fraction relative to cosmic)':
       0.10 below 1e12.5 Msun/h; log-linear to 0.55 at 1e13.5 and 0.85 at 1e14.5; capped at 0.90.
       M_ta is in Msun/h.  Returns a fraction in (0, 0.90]."""
    if A47_MUT_FREEZE:
        return 0.10
    if A47_MUT_SYSTEM:
        return 1.00
    if logMta_h < 12.5:
        f = 0.10
    elif logMta_h < 13.5:
        f = 0.10 + 0.45 * (logMta_h - 12.5)
    else:
        f = 0.55 + 0.30 * (logMta_h - 13.5)
    return min(f, 0.90)

def Mta_of(Mb, f):  return Mb * H / (f * FB)        # Msun/h, CFG416: M_b,now = f_ret f_b M_ta
def solve_fret(Mb):
    """A18's implicit solve M_ta = M_b h/(f_ret f_b), damped fixed point (A18 section 7 verbatim)."""
    f = 0.10
    for _ in range(400):
        fn = fret416(math.log10(Mta_of(Mb, f)))
        if abs(fn - f) < 1e-14:
            break
        f = 0.5 * (f + fn)
    return f

def hfun(f, Mb):    return fret416(math.log10(Mta_of(Mb, f))) - f

# ------------------------------------------------------------------ report of the record
P("=" * 118)
P("A47 -- THE f_ret = 0.10 FACTOR: does the cold sector hold ten times the cosmic share?" +
  (f"   [MUTATE {MUT}]" if MUT else ""))
P("=" * 118)
P(f"footing: a0 = {A0:.4e} m/s^2 (canonical);  R_cosmic = {SUP:.6f};  f_b = {FB:.6f};  h = {H}")
P(f"rho_crit = {RHO_CRIT:.4e} Msun/Mpc^3;  cosmic cold density = {RHO_COLD:.4e} Msun/Mpc^3;  "
  f"Delta_ta = {DELTA_TA:.4f}")

TXT416 = open(F416, errors="replace").read()
TXT804 = open(F804, errors="replace").read()
TXT801 = open(F801, errors="replace").read()
J18 = json.load(open(os.path.join(DS, "A18_two_ratios", "a18_results.json")))
J44 = json.load(open(os.path.join(DS, "A44_no_edge", "a44_results.json")))
J29 = json.load(open(os.path.join(DS, "A29_u_radial", "a29_results.json")))
J43 = json.load(open(os.path.join(DS, "A43_cold_eos", "a43_results.json")))
A18 = J18["numbers"]; A44C = J44["footings"]["canonical"]; A44A = J44["footings"]["alt"]
A29N = J29["numbers"]; A43N = J43["numbers"]

CK = []
def ck(cid, what, measured, ok):
    CK.append(dict(id=cid, what=what, measured=str(measured), pass_=bool(ok)))
    P(f"  [{cid}] {'PASS' if ok else 'FAIL'}  {what}: {measured}")

RES: dict = dict(lane="A47", generated=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), mutate=MUT or None,
           constants=dict(a0=A0, R_cosmic=SUP, f_b=FB, rho_crit=RHO_CRIT, rho_cold=RHO_COLD,
                          Delta_ta=DELTA_TA, H0=H0, h=H, sigma_c=SIG_C),
           sources=dict(cfg416=F416, cfg804=F804, cfg801=F801,
                        a18="A18_two_ratios/a18_results.json", a44="A44_no_edge/a44_results.json",
                        a29="A29_u_radial/a29_results.json", a43="A43_cold_eos/a43_results.json"))

# ================================================================== task 1 -- the two f_ret's
P("\n-- task 1: what the two f_ret's are (definitions parsed from the source files) --")
need = ["M_b,now = f_ret", "0.10 below 10^12.5", "0.55 at 10^13.5", "0.85 at 10^14.5",
        "capped at 0.90", "gas + stars fraction relative to cosmic"]
found = {s: (s in TXT416) for s in need}
ck("K1", "CFG416 FROZEN_CRITERIA.md defines f_ret as a retained BARYON fraction "
         "(M_b,now = f_ret f_b M_ta) with the three-segment table",
   f"{sum(found.values())}/6 definitional strings on disk; f_ret(12.0)={fret416(12.0):.2f}, "
   f"f_ret(13.5)={fret416(13.5):.2f}, f_ret(14.5)={fret416(14.5):.2f}, f_ret(15)={fret416(15):.2f}",
   all(found.values()))

shape = [fret416(x) for x in (12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 16.0)]
ck("K2", "the table is monotone non-decreasing and capped at 0.90 (it is a fraction, so the ceiling 1 is definitional)",
   "  ".join(f"{v:.2f}" for v in shape), all(b >= a for a, b in zip(shape, shape[1:])) and shape[-1] == 0.90)

# K3: the identity that resolves the apparent collision
try:
    import sympy as sp
    Rs, fb, fr, Mta, Mb = sp.symbols("R f_b f_ret M_ta M_b", positive=True)
    Mc = Rs * Mb / fr                     # A18/A44 budget: cold mass = R_cosmic * M_b/f_ret
    Mbnow = fr * fb * Mta                 # CFG416: retained baryons
    fc = sp.simplify((Mc.subs(Mb, Mbnow)) / (Rs * fb * Mta))   # / catchment's cosmic share
    resid = str(fc)
    exact = (fc == 1)
except Exception as e:                     # pragma: no cover
    resid, exact = f"sympy unavailable ({e})", None
num_resid = abs(SUP * (0.10 * FB * 6.37e12) / 0.10 / ((1 - FB) * 6.37e12) - 1.0)
ck("K3", "IDENTITY: with N = R_cosmic/f_ret and M_b = f_ret f_b M_ta, the cold mass is exactly "
         "the catchment's cosmic share, f_c = M_c/(R_cosmic f_b M_ta) = 1",
   f"sympy {resid if exact is not None else 'n/a'}; numeric residual {num_resid:.2e}",
   (exact if exact is not None else True) and num_resid < 1e-12)

# K4: THREE normalizations.  f_s = M_c/(R_cosmic M_b) = N/R_cosmic is A43's "f_ret" (cold mass in
# units of the SYSTEM's cosmic share; its ceiling f_s <= 1 is the system denominator, N <= 5.364).
# f_c = f_s * f_ret^b = M_c/(catchment cosmic share) is the physical availability fraction.
N_a44 = SUP / FRET_A44                                  # 53.643 at f_ret = 0.10
lam = A18["lambda_req"]; u_mid = A29N["u_MID"]; Rreq = A18["R_req"]; Rreq_e = A18["R_req_err"]
fs_system = SUP / SUP                                   # 1.000
fs_a44 = N_a44 / SUP                                    # 10.00
fs_a43 = (1.0 / u_mid) * (Rreq / SUP)                   # 2.195 = A43's f_ret
fs_a43_e = fs_a43 * math.hypot(A29N["u_MID_err"] / u_mid, Rreq_e / Rreq)
sig_above = (fs_a43 - 1.0) / 0.34                       # A43 quotes +-0.34
fc_a44 = fs_a44 * FRET_A44                              # 1.000
fc_a43 = fs_a43 * FRET_A44                              # 0.220
ck("K4", "three normalizations, two symbols: A43's f_ret is f_s = M_c/(R_cosmic M_b) = 2.195 (3.5 sigma "
         "above 1, the SYSTEM denominator); in catchment units that is f_c = f_s f_ret^b = 0.220, 4.6x "
         "below the physical ceiling; A44's model is f_s = 10.0 and f_c = 1.000",
   f"f_s: {fs_system:.3f} / {fs_a44:.2f} / {fs_a43:.3f} (+-{fs_a43_e:.2f}); "
   f"f_c: {fs_system*FRET_A44:.3f} / {fc_a44:.3f} / {fc_a43:.3f}",
   abs(fs_a44 - 10.0) < 1e-9 and abs(fs_a43 - 2.195) < 0.01 and abs(fc_a44 - 1.0) < 1e-9
   and abs(fc_a43 - 0.220) < 0.005 and sig_above > 3.0)

# K5: the symbol ledger -- N in CFG804 is 1/f_ret; N in A44/A18 is R_cosmic/f_ret
N804 = A44C["CFG804"]["N_per_bin"]                 # 10.0, 8.95, 7.35, 5.68  (units of 5.364 M_b)
coldmass = [n * SUP for n in N804]
ck("K5", "symbol ledger: CFG804's N = 1/f_ret (cold mass 5.364 N M_b) and A44's N = R_cosmic/f_ret "
         "(cold mass N M_b) are the SAME model, a factor 5.364 apart",
   f"CFG804 N={['%.2f' % n for n in N804]} -> cold masses {['%.1f' % m for m in coldmass]} M_b; "
   f"A44 N={N_a44:.2f} (= {N804[0]:.1f} x 5.364)",
   abs(N_a44 / N804[0] - SUP) < 1e-9 and all(abs(m - n * SUP) < 1e-9 for n, m in zip(N804, coldmass)))

# K6: reproduce A44's numbers from the definitions
er = [s_edge(N_a44) * rM(10 ** lm) for lm in A44C["N0"]["logMb_prim"]]
er804 = [s_edge(SUP * n) * rM(10 ** lm) for n, lm in zip(N804, A44C["CFG804"]["logMb_prim"])]
P(f"      r_e(53.64 M_b) per bin = {['%.0f' % (r*1e3) for r in er]} kpc;  "
  f"r_e(CFG804 per bin) = {['%.0f' % (r*1e3) for r in er804]} kpc")
ck("K6", "A44's two numbers reproduce from the definitions: 53.643 = 5.364/0.10, "
         "r_e = sqrt(N(N+1)) r_M = 54.14 r_M = 0.32-0.75 Mpc (A44 quotes 0.19-0.75; the 0.19 end "
         "belongs to its N=15.9 edge, not to 53.64)",
   f"{SUP:.6f}/{FRET_A44:.2f} = {SUP/FRET_A44:.3f}; s_edge = {s_edge(SUP/FRET_A44):.4f}; "
   f"r_e = {min(er)*1e3:.0f}-{max(er)*1e3:.0f} kpc; CFG804 per-bin table gives "
   f"{['%.0f' % (r*1e3) for r in er804]} kpc (file: 324/450/440/430)",
   abs(SUP / FRET_A44 - 53.64327223960661) < 1e-6 and abs(s_edge(SUP / FRET_A44) - 54.1377) < 5e-3
   and 300 < min(er) * 1e3 < 340 and 730 < max(er) * 1e3 < 770
   and max(abs(a - b) for a, b in zip([324, 450, 440, 430], [r * 1e3 for r in er804])) < 12)

# ================================================================== task 2 -- the physics
P("\n-- task 2: what 'ten times the cosmic share' does and does not mean --")
LM = 11.0
Mb1 = 10 ** LM
rM1 = rM(Mb1); re1 = s_edge(N_a44) * rM1
Mc1 = N_a44 * Mb1
Mtot1 = (1 + N_a44) * Mb1
r200_1 = r200(Mtot1)
d_e = Mc1 / (RHO_COLD * vol(re1))
d_200 = Mtot1 / (RHO_CRIT * vol(r200_1))
d_01 = m_law(0.1 / rM1) * Mb1 / (RHO_COLD * vol(0.1))
ck("K7", "the factor 10 is NOT a density: at r_e the cold medium is 133 x the cosmic cold density, "
         "at 0.1 Mpc ~6e3 x, and r200 is 200 x the mean matter density by definition",
   f"M_b=1e11: r_e={re1*1e3:.0f} kpc, 1+delta_cold(r_e)={d_e:.0f}; 1+delta(r200)={d_200:.0f}; "
   f"1+delta_cold(0.1 Mpc)={d_01:.0f}",
   100 < d_e < 200 and abs(d_200 / 200 - 1) < 0.02 and d_01 > 1000)

# K8: cosmic-share availability, computed from the cosmic mean density and the catchment volume
Mta1 = Mb1 / (0.10 * FB)
rta1 = r_ta(Mta1)
rneed1 = (3 * Mc1 / (4 * math.pi * RHO_COLD)) ** (1 / 3)
rzv1 = r_zv(Mtot1)
CAP10 = 10.0 if A47_MUT_DENSITY else 1.0     # MUTATION: read the factor 10 as a DENSITY ceiling
frac_ta = CAP10 * (RHO_COLD * vol(rta1)) / Mc1
frac_zv = CAP10 * (RHO_COLD * vol(rzv1)) / Mc1
P(f"      catchment: M_ta = M_b/(f_ret f_b) = {Mta1:.3e} Msun (M_ta/M_b = {Mta1/Mb1:.1f}); "
  f"r_ta(Delta={DELTA_TA:.2f}) = {rta1:.3f} Mpc")
P(f"      at the z=0 cosmic cold density {RHO_COLD:.2e}: r needed for {Mc1:.2e} Msun = {rneed1:.2f} Mpc; "
  f"zero-velocity radius = {rzv1:.2f} Mpc")
ck("K8", "cosmic-mean availability: only 18% (13.5% inside the zero-velocity sphere) of the budget "
         "is there at the present cosmic mean density; the other 82% is the catchment's turnaround "
         "overdensity (1/fraction = 5.55 = Delta_ta), i.e. the cold sector must trace the matter",
   f"mean-density cold mass inside r_ta = {frac_ta:.3f} of 53.64 M_b, inside r_ZV = {frac_zv:.3f}; "
   f"r_needed at mean density = {rneed1:.2f} Mpc = {rneed1/rzv1:.2f} r_ZV",
   0.15 < frac_ta < 0.20 and 0.12 < frac_zv < 0.15 and 1.8 < rneed1 / rzv1 < 2.1)

# K9: escape velocity
vc1 = v_circ(Mtot1, re1); vesc1 = math.sqrt(2) * vc1; vH1 = H0 * re1
ck("K9", "escape velocity: v_esc/v_H = 6 and v_esc/sigma_c = 32 at r_e, and the ambient-infall "
         "capacity v^2 r/G at r_e is 2.6x the budget -- this bound does not bite",
   f"v_c={vc1:.0f}, v_esc={vesc1:.0f}, v_H={vH1:.0f} km/s; M_bound(300 km/s, r_e)="
   f"{M_bound(300, re1):.2e} vs M_c={Mc1:.2e} (ratio {M_bound(300, re1)/Mc1:.2f})",
   vesc1 / vH1 > 3 and vesc1 / SIG_C > 20 and 2.0 < M_bound(300, re1) / Mc1 < 3.5)

# K10: tidal field
rre = re1 * (3 * Mtot1 / Mtot1) ** (1 / 3)   # equal-mass neighbour: d > r_e (3 M_env/M)^(1/3)
d_eq = re1 * (3.0) ** (1 / 3)                # M_env = M_tot, equal masses
d_10 = re1 * (3.0 * 10) ** (1 / 3)           # 10x heavier neighbour
re_small = s_edge(37.9) * rM1
d_eq_small = re_small * 3 ** (1 / 3)
ck("K10", "tidal field: an equal-mass neighbour must sit beyond 0.95 Mpc (53.64 model) or 0.68 Mpc "
          "(self-consistent N=38); a 10x neighbour beyond 2.0 Mpc",
   f"d_eq(53.64) = {d_eq:.2f} Mpc, d_eq(N=38) = {d_eq_small:.2f} Mpc, d_10 = {d_10:.2f} Mpc",
   0.85 < d_eq < 1.05 and 0.60 < d_eq_small < 0.75 and 1.9 < d_10 < 2.2)

# K11: phase space
rho_gcc = (Mc1 / vol(re1)) * MSUN_G / MPC_CM ** 3
Q = rho_gcc / (2 * math.pi * (SIG_C * 1e5) ** 2) ** 1.5
hbar = 1.054571817e-27
m_tg = (rho_gcc * (2 * math.pi * hbar) ** 3 / (2 * (4 * math.pi / 3) * (SIG_C * 1e5) ** 3)) ** 0.25
m_ev = m_tg / 1.78266192e-33
M_sigma = SIG_C ** 2 * re1 / G
ck("K11", "phase space: the coarse-grained density implies a Tremaine-Gunn floor m >= 37 eV (no new "
          "obstruction), and the sector's own sigma_c could hold only 0.2% of the mass at r_e -- the "
          "binding is the total mass, not the sector's dispersion",
   f"rho(r_e)={rho_gcc:.2e} g/cm^3, Q={Q:.2e}, m_TG={m_ev:.0f} eV, sigma_c^2 r_e/G={M_sigma:.1e} Msun "
   f"({M_sigma/Mtot1*100:.2f}% of M_tot)",
   25 < m_ev < 50 and M_sigma / Mtot1 < 0.005)

# ================================================================== task 3 -- the decisive number
P("\n-- task 3: is 53.64 M_b available?  the self-consistent CFG416 budget --")
rows = []
for b, lm in enumerate(A44C["N0"]["logMb_prim"]):
    Mb = 10 ** lm
    f = solve_fret(Mb)
    N = SUP / f
    rows.append(dict(bin=b + 1, logMb=lm, Mb=Mb, f_ret=f, Mta=Mta_of(Mb, f), logMta_h=math.log10(Mta_of(Mb, f)),
                     N=N, M_c=N * Mb, r_e=s_edge(N) * rM(Mb), r_e_53=s_edge(N_a44) * rM(Mb),
                     frac_of_5364=N / N_a44))
P("      bin  logM_b   f_ret   logM_ta[h]    N       M_c[M_b]   r_e[kpc]   r_e(53.64)[kpc]")
for r in rows:
    P(f"       {r['bin']}   {r['logMb']:5.2f}   {r['f_ret']:5.3f}   {r['logMta_h']:6.2f}     "
      f"{r['N']:6.2f}    {r['N']:6.2f}     {r['r_e']*1e3:6.0f}      {r['r_e_53']*1e3:6.0f}")
f11 = solve_fret(Mb1); N11 = SUP / f11
# uniqueness of the fixed point
scan = [hfun(0.02 + 0.001 * i, Mb1) for i in range(0, 950)]
sign_changes = sum(1 for a, b in zip(scan, scan[1:]) if a * b < 0)
ck("K12", "the CFG416 fixed point exists, is unique, and reproduces A18's grid (44.125 at 1e11, "
          "14.917 at 1e12); per bin N = 53.64, 53.64, 50.3, 37.9",
   f"1e11 -> f_ret {f11:.4f}, N {N11:.2f} (A18: 0.1216, 44.125); 1e12 -> N {SUP/solve_fret(1e12):.3f} "
   f"(A18: 14.917); sign changes {sign_changes}",
   abs(N11 - 44.125) < 0.2 and abs(SUP / solve_fret(1e12) - 14.917) < 0.1 and sign_changes == 1)

Nreq = A44C["N_required_primary"]
Nmin = min(r["N"] for r in rows)
N_cap_density = CAP10 * RHO_COLD * vol(re1) / Mb1     # the brief's premise as a ceiling, in units of M_b
N_cmp = N_cap_density if A47_MUT_DENSITY else Nmin
ck("K13", "AVAILABILITY vs REQUIREMENT: the smallest available budget (37.9 M_b at the top bin) is "
          "2.4x the N the data require (15.9), so availability does NOT cap below the requirement",
   f"N_avail = {['%.1f' % r['N'] for r in rows]}, min/N_req = {Nmin/Nreq:.2f}; "
   f"at 1e11 {N11:.1f}/{Nreq:.1f} = {N11/Nreq:.2f}"
   + (f"; MUTATED density ceiling -> N = {N_cap_density:.1f}" if A47_MUT_DENSITY else ""),
   N_cmp > Nreq)

def dchi2_at(N):
    esc = A44C["Escan"]; xs = sorted((float(k), v["dchi2_prim"]) for k, v in esc.items())
    for (x0, y0), (x1, y1) in zip(xs, xs[1:]):
        if x0 <= N <= x1:
            return y0 + (y1 - y0) * (N - x0) / (x1 - x0)
    return None
d44 = dchi2_at(N_a44); d11 = dchi2_at(N11); dreq = dchi2_at(Nreq)
ck("K14", "the available budget fits: dchi2(primary) at N=44.1 is <= +1 (A44's 53.64 gives +1.1, "
          "N_req=15.9 gives +4); the per-bin CFG804 model gives -0.3",
   f"dchi2(44.1) = {d11:+.1f}; dchi2(53.64) = {d44:+.1f}; dchi2(15.9) = {dreq:+.1f}; "
   f"CFG804 per-bin = {A44C['CFG804']['dchi2_prim']:+.1f}",
   d11 is not None and d11 < 2.0 and d44 < 2.0 and dreq <= 4.5)

# K15: where 53.64 stops being the table's value
lim = 10 ** 12.5 * 0.10 * FB / H
ck("K15", "the factor 10 is the LOW-MASS branch: f_ret = 0.10 is the table's value only while "
          "M_ta <= 1e12.5 Msun/h, i.e. M_b <= 7.4e10; at 1e11 it is 44.1 (82%), at the top bin 37.9 (71%)",
   f"M_b,lim = {lim:.2e}; f_ret(1e11) = {f11:.3f}; 53.64/44.1 = {N_a44/N11:.2f}; "
   f"53.64/37.9 = {N_a44/min(r['N'] for r in rows):.2f}",
   6e10 < lim < 9e10 and N_a44 / min(r["N"] for r in rows) > 1.3)

# K16: the u ledger
u18 = A18["u_MW"]; Rtot = A18["MW"]["R_tot"]
ck("K16", "u: A18's u = R_tot/N = 0.467 and A29's u_MID = 0.472 are numerically the same to 0.1 sigma "
          "but are different functionals (3D budget fraction vs projected band ratio); u <= 1 never "
          "constrained f_ret -- it bounds the law's share of the budget",
   f"R_tot/N = {Rtot/N_a44:.4f} vs A29 u_MID = {u_mid:.4f} +- {A29N['u_MID_err']:.4f} "
   f"({abs(Rtot/N_a44-u_mid)/math.hypot(A29N['u_MID_err'],0.0):.2f} sigma)",
   abs(Rtot / N_a44 - u_mid) / A29N["u_MID_err"] < 1.0)

# K17: geometry -- is the edge inside the catchment?
P("\n-- geometry: where the edge sits --")
GEO = []
for r in rows:
    Mt = (1 + r["N"]) * r["Mb"]; r2 = r200(Mt); rtab = r_ta(r["Mta"])
    GEO.append(dict(bin=r["bin"], r_e_kpc=r["r_e"] * 1e3, r200_kpc=r2 * 1e3, r_ta_kpc=rtab * 1e3,
                    over_r200=r["r_e"] / r2, over_rta=r["r_e"] / rtab, M_tot=Mt))
    P(f"      bin {r['bin']}: r_e = {r['r_e']*1e3:5.0f} kpc = {r['r_e']/r2:4.2f} r200c = "
      f"{r['r_e']/rtab:.2f} r_ta   (r200c {r2*1e3:.0f} kpc, r_ta {rtab*1e3:.0f} kpc, M_tot {Mt:.2e})")
x_ta = rta1 / rM1
N_geom = 0.5 * (-1 + math.sqrt(1 + 4 * x_ta * x_ta))
ck("K17", "geometry: the edge is 1.4-1.8 r200c and 0.3-0.4 r_ta -- inside the catchment; the geometric "
          "cap is N <= 155, three times the f_ret cap, so the baryon budget binds first",
   f"r_e/r200c {min(g['over_r200'] for g in GEO):.2f}-{max(g['over_r200'] for g in GEO):.2f}, "
   f"r_e/r_ta {min(g['over_rta'] for g in GEO):.2f}-{max(g['over_rta'] for g in GEO):.2f}, "
   f"N_max(geometry) = {N_geom:.0f}",
   1.3 < min(g["over_r200"] for g in GEO) and max(g["over_r200"] for g in GEO) < 2.0
   and max(g["over_rta"] for g in GEO) < 0.50 and N_geom > 100)

# K18: the alt footing (never pooled with canonical)
Nreq_alt = A44A["N_required_primary"]
ratio_alt = Nmin / Nreq_alt
ck("K18", "alt footing (a0 = 1.1312e-10) is not pooled: N_req = 19.85 there, and N_avail/N_req = 1.9 "
          "at the top bin (2.2 at 1e11), so the verdict is footing-independent; r_e scales by 0.910",
   f"N_req alt = {Nreq_alt:.2f}; {Nmin:.1f}/{Nreq_alt:.2f} = {ratio_alt:.2f}; "
   f"r_e(alt)/r_e(canonical) = {math.sqrt(9.3603/11.312):.3f}; dchi2(E_catch) alt = "
   f"{A44A['E_catch']['dchi2_prim']:+.1f}",
   ratio_alt > 1.5)

# ================================================================== summary
P("\n" + "=" * 118)
P("SUMMARY")
P("=" * 118)
P(f"  f_ret (CFG416)          = retained baryon fraction, M_b/(f_b M_ta) in (0, 0.90]  -> f_ret = 0.10 = 10% of the catchment's baryons")
P(f"  N = R_cosmic/f_ret      = cold mass / system baryons = 53.64 at f_ret = 0.10 (DERIVED, not a second f_ret)")
P(f"  f_s (A43's 'f_ret')     = cold mass / SYSTEM cosmic share = {fs_system:.2f} (system model), {fs_a44:.2f} (A44), {fs_a43:.2f} (A43) -- ceiling 1 is the system denominator")
P(f"  f_c = f_s f_ret^b       = cold mass / CATCHMENT cosmic share = {fc_a44:.3f} at A44's model, {fc_a43:.3f} at A43's EOS reading (ceiling 1)")
P(f"  factor 10               = 1/f_ret (baryon reservoir), NOT a density; 1+delta_cold(r_e) = {d_e:.0f}, 1+delta_cold(0.1 Mpc) = {d_01:.0f}")
P(f"  53.64 M_b available?    = {N11:.1f} M_b at 1e11 ({N11/N_a44*100:.0f}% of it), {Nmin:.1f} at the top bin; N_req = {Nreq:.1f}")
P(f"  decisive number         = N_avail/N_req = {Nmin/Nreq:.2f} > 1  -> not capped; tension does not return on the primary range")
P(f"  dchi2 at the available budget = {d11:+.1f} vs +1.1 at 53.64 (both <= 4)")

npass = sum(c["pass_"] for c in CK)
P(f"\n  {npass}/{len(CK)} checks pass.  runtime {time.time()-T0:.2f} s.")
RES["checks"] = CK; RES["n_pass"] = npass; RES["n_total"] = len(CK); RES["runtime_s"] = time.time() - T0
RES["definitions"] = dict(
    fret_416=dict(symbol="f_ret^b", meaning="retained baryon fraction M_b/(f_b M_ta)", range=[0.0, 0.90],
                  source="CFG416 FROZEN_CRITERIA.md", value_at_1e11=f11, value_low_branch=0.10),
    N=dict(symbol="N", meaning="cold mass per system baryon = R_cosmic/f_ret^b", value=SUP / 0.10,
           census_symbol="N_416 = 1/f_ret = 10.0 (CFG804), cold mass 5.364 N M_b"),
    f_s=dict(symbol="f_s", meaning="cold mass / SYSTEM cosmic share = N/R_cosmic (A43's 'f_ret')",
             at_system=fs_system, at_A44=fs_a44, at_A43=fs_a43, at_A43_err=0.34,
             ceiling=1.0, sigma_above_ceiling=sig_above),
    f_c=dict(symbol="f_c", meaning="cold mass / CATCHMENT cosmic share = f_s f_ret^b", at_A44=fc_a44,
             at_A43=fc_a43, ceiling=1.0))
RES["availability"] = dict(Mb=Mb1, rM_kpc=rM1 * 1e3, r_e_kpc=re1 * 1e3, M_c_Msun=Mc1, M_tot_Msun=Mtot1,
                           r200_Mpc=r200_1, delta_at_re=d_e, Mta_Msun=Mta1, r_ta_Mpc=rta1,
                           r_needed_cosmic_Mpc=rneed1, r_zv_Mpc=rzv1, frac_in_rta=frac_ta,
                           frac_in_rzv=frac_zv, v_c=vc1, v_esc=vesc1, v_H=vH1,
                           d_eq_Mpc=d_eq, d_10_Mpc=d_10, rho_gcc=rho_gcc, m_TG_eV=m_ev,
                           M_sigma_Msun=M_sigma, N_at_1e11=N11, N_req=Nreq, N_min_bins=Nmin,
                           dchi2_at_44=d11, dchi2_at_5364=d44, dchi2_at_req=dreq)
RES["per_bin"] = rows
RES["geometry"] = GEO
RES["M_b_lim_branch"] = lim
RES["N_geometric_cap"] = N_geom
RES["N_density_cap_literal"] = N_cap_density

with open(os.path.join(HERE, "a47" + (("_MUTATE_" + MUT) if MUT else "") + ".out"), "w") as fh:
    fh.write("\n".join(OUT) + "\n")
with open(os.path.join(HERE, "a47_results" + (("_MUTATE_" + MUT) if MUT else "") + ".json"), "w") as fh:
    json.dump(RES, fh, indent=1, default=float)
sys.exit(0 if npass == len(CK) else 1)

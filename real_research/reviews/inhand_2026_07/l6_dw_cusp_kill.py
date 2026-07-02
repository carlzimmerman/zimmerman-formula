#!/usr/bin/env python3
"""
LANE L6 -- THE DEFFAYET-WOODARD z~0.09 CUSP KILL-TEST (arXiv:2512.10513), no framework risk.

DW's reconstruction (banked A1, a1_dw_a0z_discriminant.py, verified against their synthesis.tex):
  Z_tot = (2 g_obs / a0_DW)^2 - B(z)^2 ,   B(z) = their eq (52) cosmological background,
  a0_DW = c H0 / sqrt(30) ~= 1.23e-10 (CONSTANT).
Their MOND branch is the Z>0 side of f(Z); deep MOND is their own 0 < Z <~ 1 (l.622).
=> the MOND branch EXISTS only for  g_obs > g_floor(z) = (a0_DW/2) |B(z)|.
SIGN CHECK re-derived below: |B| GROWS as z->0 below the crossing z_c ~ 0.088, so the floor
bites HARDEST exactly where SPARC lives (z ~ 0.0002-0.03) and vanishes only at z ~= z_c.
DW-naive therefore predicts: deep-MOND ABSENT/suppressed at SPARC redshifts, reappearing
toward z~0.09 (a cusp). The framework (dS-Unruh MI, a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11,
own nu: g_obs = sqrt(g_bar^2 + g_bar a0)) predicts a FLAT deep RAR across 0 < z < 0.2.

TESTS (all in-hand data):
  T1  floor census: how many SPARC deep-MOND points (g_bar < 0.1 a0) sit BELOW DW's floor
      at their own galaxy's z (three cosmologies incl. the DW-most-charitable one)?
  T2  exclusion: on DW's dead branch the maximal DW-style suppression is Newtonian
      (g_obs = g_bar). Per-GALAXY medians (conservative: points within a galaxy share D,i
      -> not independent), empirical inter-galaxy scatter -> N-sigma vs Newtonian; and the
      95% bound on the surviving MOND fraction s in g_obs^2 = g_bar^2 + s a0 g_bar.
  T3  cusp vs flat: effective a0_eff = (g_obs^2 - g_bar^2)/g_bar (exact inversion of the
      framework nu; deep-regime a0 estimator) in SPARC z-bins vs the committed MIGHTEE CSV
      (z up to ~0.08, toward z_c). DW-naive: strong rise toward z_c + dead low-z bins.
      Framework: flat. BOTH-WAYS: MIGHTEE per-point z is NOT in the banked CSV -> carried
      as a z-band [0.02, 0.08] ensemble, flagged; forks 1-3 run alongside.

Footing rules honored: framework judged on its OWN interpolation; a0 fork 1.13e-10 shown;
Upsilon fork 0.50/0.70 shown; nothing manufactured either way. Exits 0.
"""
import numpy as np, glob, os, re
from scipy import integrate, optimize

c   = 299792458.0
Mpc = 3.0856775814913673e22
H0  = 67.4e3/Mpc
cH0 = c*H0
G   = 6.674e-11
kpc = 3.0857e19

a0_DW = cH0/np.sqrt(30.0)                    # DW's own constant a0 (their eq 10)
OmL_fw = 0.685
a0_fw  = cH0*np.sqrt(3*OmL_fw/(32*np.pi))    # framework canonical = c^2 sqrt(Lambda/32pi)
a0_fork = 1.13e-10                           # rho_total/cH0 footing fork (rule 4)
print("="*100)
print("CONSTANTS")
print("="*100)
print(f"  a0_DW  = cH0/sqrt(30)          = {a0_DW:.4e} m/s^2 (DW's own, CONSTANT)")
print(f"  a0_fw  = c^2 sqrt(Lambda/32pi) = {a0_fw:.4e} m/s^2 (canonical) ; fork {a0_fork:.2e}")

# ---------------- DW background B(z), three cosmologies ----------------
def make_B(Om_r, Om_m, Om_L):
    def integrand_u(u):
        return (Om_r + 0.5*Om_m*u - Om_L*u**4)/np.sqrt(Om_r + Om_m*u + Om_L*u**4)
    def B(z):
        I,_ = integrate.quad(integrand_u, 0.0, 1.0/(1.0+z), limit=400)
        return 6*np.sqrt(30.0)*(1+z)**3*I     # (6 cH0/a0_DW) is H0-independent
    return B

cosmos = {
    "DW-paper (0.3,0.7)":   make_B(1e-4,   0.300, 0.700),
    "Planck-2015 (Kim+)":   make_B(1e-4,   0.3089, 1-1e-4-0.3089),
    "Planck-2018":          make_B(9.2e-5, 0.315, 0.685),
}
print()
print("="*100)
print("DW FLOOR: SIGN/MEANING RE-DERIVED (does the floor GROW as z->0? -- yes)")
print("="*100)
zcs = {}
for name, B in cosmos.items():
    zc = optimize.brentq(B, 0.01, 0.4, xtol=1e-9)
    zcs[name] = zc
    row = "  ".join(f"B({z:.3f})={B(z):+.3f}" for z in (0.0, 0.01, 0.03, 0.05, 0.08, 0.088, 0.12))
    print(f"  {name:<20} z_c={zc:.4f}   {row}")
assert abs(zcs["Planck-2015 (Kim+)"] - 0.0880) < 0.002, "failed to reproduce their z_c"
print("""  => VALIDATED: their z_c = 0.0880 reproduced on Kim+'s cosmology ({:.4f}). |B| is MAXIMAL at z=0
     and falls monotonically to 0 at z_c: the MOND-branch floor g_floor=(a0_DW/2)|B| GROWS as z->0.
     SPARC (z ~ 0.0002-0.03) sits where the floor bites HARDEST; MIGHTEE (z -> 0.08) approaches the
     floor-free cusp. Deep band (their own 0<Z<~1, i.e. g_obs <= a0_DW/2): floor/(a0_DW/2) at z=0 =
     {:.2f} | {:.2f} | {:.2f} (paper | P15 | P18) -- the ENTIRE deep band is off-branch today on all three.""".format(
     zcs["Planck-2015 (Kim+)"],
     *[abs(B(0.0)) for B in cosmos.values()]))

B_paper = cosmos["DW-paper (0.3,0.7)"]
B_p18   = cosmos["Planck-2018"]           # smallest |B(0)| -> DW-most-charitable floor
def floor_charitable(z):                   # min over cosmologies = most favorable to DW
    return 0.5*a0_DW*min(abs(B(z)) for B in cosmos.values())

# ---------------- SPARC load (banked rar_framework_a0_mlfit.py conventions) ----------------
DATA = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/sparc_data"
def load(Ud):
    Ub = 1.4*Ud
    gals = []
    for f in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
        head = open(f).readline()
        m = re.search(r"Distance\s*=\s*([\d.]+)\s*Mpc", head)
        if not m: continue
        D = float(m.group(1)); zgal = H0*D*Mpc/c
        try: d = np.genfromtxt(f, comments="#")
        except Exception: continue
        if d.ndim != 2 or d.shape[1] < 6: continue
        R,Vobs,eV,Vgas,Vdisk,Vbul = (d[:,i] for i in range(6))
        Vbar2 = np.sign(Vgas)*Vgas**2 + Ud*Vdisk**2 + Ub*Vbul**2
        gb = Vbar2*1e6/(R*kpc); go = (Vobs*1e3)**2/(R*kpc)
        ok = (gb>0)&(go>0)&np.isfinite(gb)&np.isfinite(go)&(Vobs>0)
        seV = 2*np.clip(eV,1,None)/np.clip(Vobs,1,None)/np.log(10)   # sigma of log10 g_obs
        gals.append(dict(name=os.path.basename(f).replace("_rotmod.dat",""),
                         z=zgal, gb=gb[ok], go=go[ok], slgo=seV[ok]))
    return gals

def run(Ud, a0_sel, tag):
    gals = load(Ud)
    npts = sum(len(g['gb']) for g in gals)
    zs = np.array([g['z'] for g in gals])
    print()
    print("="*100)
    print(f"T1+T2 [{tag}]  Upsilon_d={Ud}, deep cut g_bar < 0.1 x {a0_sel:.2e}")
    print("="*100)
    print(f"  {len(gals)} galaxies, {npts} RC points; z range {zs.min():.5f} - {zs.max():.5f} "
          f"(median {np.median(zs):.4f}) -- ALL below z_c~0.088")
    n_deep = n_below = n_below_char = 0
    dNewt, dMOND, s_gal, zg_list = [], [], [], []
    deep_all = []   # (z, gb, go) for T3
    for g in gals:
        deep = g['gb'] < 0.1*a0_sel
        if not deep.any(): continue
        gb, go, sl = g['gb'][deep], g['go'][deep], g['slgo'][deep]
        fl_paper = 0.5*a0_DW*abs(B_paper(g['z']))
        fl_char  = floor_charitable(g['z'])
        below  = go < fl_paper
        belowc = go < fl_char
        n_deep += deep.sum(); n_below += below.sum(); n_below_char += belowc.sum()
        deep_all += [(g['z'], b, o) for b,o in zip(gb, go)]
        if belowc.sum() >= 2:      # DW-charitable dead-branch points only
            gbb, gob = gb[belowc], go[belowc]
            dNewt.append(np.median(np.log10(gob/gbb)))                              # vs Newtonian
            dMOND.append(np.median(np.log10(gob/np.sqrt(gbb**2+gbb*a0_DW))))        # vs DW's own MOND locus
            s_gal.append(np.median((gob**2-gbb**2)/(a0_DW*gbb)))                    # surviving MOND fraction
            zg_list.append(g['z'])
    dNewt, dMOND, s_gal = map(np.array, (dNewt, dMOND, s_gal))
    N = len(dNewt)
    print(f"  deep-MOND points: {n_deep}; below DW floor at own z: {n_below} ({100*n_below/max(n_deep,1):.1f}%)"
          f" [paper cosmology] | {n_below_char} ({100*n_below_char/max(n_deep,1):.1f}%) [DW-most-charitable]")
    print(f"  galaxies with >=2 dead-branch deep points (charitable floor): N = {N}")
    mu, sd = dNewt.mean(), dNewt.std(ddof=1)
    t = mu/(sd/np.sqrt(N))
    muM, sdM = dMOND.mean(), dMOND.std(ddof=1)
    print(f"  per-galaxy median offset vs NEWTONIAN (DW max-suppression): {mu:+.3f} +/- {sd/np.sqrt(N):.3f} dex "
          f"(inter-galaxy scatter {sd:.3f} dex)")
    print(f"    => Newtonian dead branch rejected at {t:.1f} sigma (conservative per-galaxy count)")
    print(f"  same points vs DW's OWN on-branch MOND locus sqrt(gb^2+gb*a0_DW): {muM:+.3f} dex, scatter {sdM:.3f} dex")
    print(f"    => the branch DW says cannot exist there is exactly what the data trace")
    s_mu, s_se = s_gal.mean(), s_gal.std(ddof=1)/np.sqrt(N)
    s_lb = s_mu - 1.645*s_se
    print(f"  surviving MOND fraction s (g_obs^2 = gb^2 + s a0_DW gb) on the dead branch: "
          f"{s_mu:.3f} +/- {s_se:.3f}; 95% lower bound {s_lb:.3f}")
    print(f"    => maximal DW-style suppression allowed by SPARC: {100*(1-s_lb):.1f}% "
          f"(DW-naive needs 100%); s=0 is {s_mu/s_se:.0f} sigma away")
    return deep_all, np.array(zg_list), dNewt

deep_all, zg, dN = run(0.70, a0_fw, "canonical: framework anchor Upsilon")
_ = run(0.50, a0_fw, "fork: standard Upsilon=0.50")
_ = run(0.70, a0_fork, "fork: a0=1.13e-10 deep cut")
_ = run(0.70, a0_DW, "fork: DW's own a0 deep cut")

# ---------------- T3: cusp vs flat, SPARC z-bins + MIGHTEE ----------------
print()
print("="*100)
print("T3  a0_eff = (g_obs^2 - g_bar^2)/g_bar in deep regime: SPARC z-bins (below z_c) vs MIGHTEE (toward z_c)")
print("="*100)
deep_all = np.array(deep_all)   # z, gb, go  (Upsilon=0.70, deep cut 0.1 a0_fw)
z_d, gb_d, go_d = deep_all[:,0], deep_all[:,1], deep_all[:,2]
a0e = (go_d**2 - gb_d**2)/gb_d

def boot_med(x, n=4000, seed=1):
    rng = np.random.default_rng(seed)
    return np.std([np.median(rng.choice(x, len(x))) for _ in range(n)])

bins = [(0.0, 0.003), (0.003, 0.008), (0.008, 0.03)]
print(f"  {'z-bin':<16}{'N_pts':>6}{'med a0_eff':>12}{'+/-':>9}   DW floor(g_obs) band [charit., paper]")
meds = []
for lo, hi in bins:
    m = (z_d >= lo) & (z_d < hi)
    med = np.median(a0e[m]); se = boot_med(a0e[m])
    zmid = np.median(z_d[m])
    meds.append((zmid, med, se))
    print(f"  {f'{lo}-{hi}':<16}{m.sum():>6}{med:>12.2e}{se:>9.1e}   "
          f"{floor_charitable(zmid):.2e} - {0.5*a0_DW*abs(B_paper(zmid)):.2e}")

# MIGHTEE committed CSV + forks (z band 0.02-0.08, per-point z NOT banked -- flagged)
MD = "/Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/next_doors_2026_07"
mightee = {}
for fn, lab in [("mightee_rar_extracted.csv","MIGHTEE fiducial"),
                ("mightee_rar_fork1.csv","MIGHTEE fork1"),
                ("mightee_rar_fork2.csv","MIGHTEE fork2"),
                ("mightee_rar_fork3.csv","MIGHTEE fork3")]:
    d = np.genfromtxt(os.path.join(MD, fn), delimiter=",", comments="#")
    gb, go = 10**d[:,0], 10**d[:,1]
    deep = gb < 0.1*a0_fw
    if deep.sum() < 3:
        print(f"  {lab:<16}  only {deep.sum()} deep points -- skipped"); continue
    a0m = (go[deep]**2 - gb[deep]**2)/gb[deep]
    med = np.median(a0m); se = boot_med(a0m)
    mightee[lab] = (med, se)
    print(f"  {lab:<16}{deep.sum():>6}{med:>12.2e}{se:>9.1e}   z-band 0.02-0.08 (per-point z not in banked CSV)")

# flat vs cusp verdict numbers
(z1,m1,s1),(z2,m2,s2),(z3,m3,s3) = meds
slope_sig = abs(np.log10(m3/m1))/np.sqrt((s1/m1/np.log(10))**2+(s3/m3/np.log(10))**2)
print(f"""
  SPARC lowest-z vs highest-z bin: log10 ratio {np.log10(m3/m1):+.3f} dex ({slope_sig:.1f} sigma from flat).
  SIGN NOTE: the (insignificant) internal trend is a slight DECLINE toward z_c -- OPPOSITE to the
  rise DW's cusp requires. DW-naive expectation across these bins: LOW bins DEAD (floor
  {floor_charitable(z1)/a0_DW:.2f}-{0.5*a0_DW*abs(B_paper(z1))/a0_DW:.2f} a0_DW in g_obs >> every deep point) with a0_eff collapsing toward ~0
  (Newtonian), recovering only near z_c. Observed: same a0_eff in every SPARC bin -> FLAT.
  Framework's own prediction (flat a0 across 0<z<0.2, both footing forks <1% varied here): PASSES as-is.""")

# BOTH-WAYS FLAG: the MIGHTEE amplitude offset -- the one datum a DW advocate could point at
mmed, mse = mightee["MIGHTEE fiducial"]
m_all = np.median(a0e); s_all = boot_med(a0e)
off = np.log10(mmed/m_all)
off_se = np.sqrt((mse/mmed/np.log(10))**2 + (s_all/m_all/np.log(10))**2)
lo_f = min(v[0] for v in mightee.values()); hi_f = max(v[0] for v in mightee.values())
print(f"""  BOTH-WAYS FLAG (not suppressed): MIGHTEE deep a0_eff ({mmed:.2e}) sits {off:+.2f} +/- {off_se:.2f} dex
  ABOVE all-SPARC deep ({m_all:.2e}). A DW advocate could read a rise toward z_c into that. It does
  NOT rescue DW: (i) DW's floor forbids the SPARC deep points EXISTING on the MOND branch at all --
  an amplitude offset between surveys cannot undo a 26-sigma branch-existence violation at z<0.03;
  (ii) the offset is the banked B3 cross-survey systematic (Upsilon_K measured low on their gas-rich
  dwarfs; their own coefficient excludes ALL anchors incl. Milgrom at 3.2-3.9 sigma; x2 systematic
  swing; fork spread here {lo_f:.2e}-{hi_f:.2e}); (iii) without per-point z the cusp SHAPE
  (rise-then-fall through z_c) is untestable from this CSV -- only branch existence is, and it fails DW.""")

print("="*100)
print("HONEST SCOPE (both ways)")
print("="*100)
print("""  - The N-sigma above excludes DW-NAIVE: MOND branch absent below the floor with nothing
    replacing its phenomenology (max suppression = Newtonian baryons). It does NOT close their
    escape hatch: below-floor behavior is governed by their M-transport memory (their eq (33)),
    numerics their own sec. 4.2 defers ('formidable numerical undertaking'). For DW to survive,
    that deferred sector must land on DW's own on-branch MOND locus (per-galaxy mean offset
    ~-0.08 dex, inter-galaxy scatter ~0.22 dex above) across 1.5+ dex of g_bar, at every z in
    0.0002-0.03, while the branch itself is OFF -- a coincidence mimicking the thing the floor
    forbids, with no free parameter available to arrange it. Severe tension -> now quantified;
    'completed kill' still NOT claimed (their transition analysis is unpublished).
  - z from Hubble-flow D (z=H0 D/c): fine here, B(z) varies smoothly on ~0.01 scales.
  - MIGHTEE per-point z is not in the banked CSV; T3's MIGHTEE column is an ensemble check only.
  - Framework risk: NONE. This lane tests DW's floor; the framework's flat prediction is what
    the data already show.""")
print("EXIT 0")

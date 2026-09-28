#!/usr/bin/env python3
"""AS049 appendix -- PHANTOM DISK PROJECTED SURFACE DENSITY (dispatch-brief content).

Operative MONO log-phantom:  Phi_ph = C ln(r/r0)  =>  rho_ph = C/(4 pi G r^2),  C = sqrt(G M_b a0)
(Loan-certified Poisson inversion, AS047). This script derives:

  (A) face-on / edge-on projected surface density  Sigma_ph(R) = C/(4 G R)  (exact Abel),
  (B) capped regularization  Sigma_cap(Rp; R) = (C/(2 pi G Rp)) arccos(Rp/R)  (AS090 form),
  (C) column density through the disk plane + central column with inner cutoff,
  (D) implied column-density floor near the galaxy center, vs ZD07 slab ceiling
      Sigma_quad = a0/(4 pi G) on both footings (AS009 table),
  (E) honest domain: deep 1/r^2 law is the r >> r_M asymptote of RAR/MONO (AS047 S3);
      the inner MONO 'log phantom' profile replaces it for r < ~0.65 r_M.  Full-kernel
      numerical columns (exact MONO density) quantify the corrections.
  (F) leading correction to the nominal column from the RAR tail: -1/24 (r_M/R)^2.

Bounds: 1 process, 1 thread, wall <=120 s (caller timeout), maxrss asserted <512 MB.
"""
import json, math, os, resource, time
import mpmath as mp

mp.mp.dps = 50
t0 = time.time()

A0_CAN = mp.mpf("9.3619e-11"); A0_ALT = mp.mpf("1.1279e-10")
G = mp.mpf("6.67430e-11"); C_LIGHT = mp.mpf("299792458")
MSUN = mp.mpf("1.98847e30"); PC = mp.mpf("3.085677581491367e16")
MSUN_PC2 = MSUN/(PC*PC)                 # kg/m^2 per Msun/pc^2
KPC = 1000*PC
DELTA = mp.mpf("0.05")

# ---- MONO landmarks (same certified values as the main run)
y_p  = mp.findroot(lambda y: 2 - mp.sqrt(y) - 2*mp.exp(-mp.sqrt(y)), mp.mpf("2.54"))
h_p  = y_p/(mp.e**mp.sqrt(y_p) - 1)
c_mon = DELTA*h_p
y_star = mp.findroot(lambda y: (2*(mp.e**mp.sqrt(y)-1) - mp.sqrt(y)*mp.e**mp.sqrt(y))/(2*(mp.e**mp.sqrt(y)-1)**2) - c_mon/(y + y_p), mp.mpf("2.3374"))
h_star = y_star/(mp.e**mp.sqrt(y_star) - 1)

def h_mono(y):
    return h_star + c_mon*mp.log((y + y_p)/(y_star + y_p)) if y > y_star else y/(mp.e**mp.sqrt(y)-1)

def nu_mono(y): return 1 + h_mono(y)/y
def nu_RAR(y):  return 1/(1 - mp.e**(-mp.sqrt(y)))

# ---- exact phantom density from enclosed mass (spherical):  M_ph(r) = r^2 g_ph/G,  g_ph = a0 h(y)
def Mph_MONO(r, rM, a0):
    y = (rM/r)**2
    return r*r*a0*h_mono(y)/G

def rho_MONO(r, rM, a0, h=mp.mpf("1e-6")):
    """d/dr M_ph/(4 pi r^2), central difference in log-r (relative step 1e-6, 50 dps)."""
    rp, rm = r*(1+h), r/(1+h)
    Mp, Mm = Mph_MONO(rp, rM, a0), Mph_MONO(rm, rM, a0)
    return (Mp-Mm)/(rp-rm)/(4*mp.pi*r*r)

def Sigma_nominal(R, C):
    """exact Abel projection of rho_ph = C/(4 pi G r^2): C/(4 G R)"""
    return C/(4*G*R)

def Sigma_capped(Rp, R, C):
    """capped Abel: (C/2piG Rp) arccos(Rp/R), Rp<R (AS090), edge column -> 0"""
    return C/(2*mp.pi*G*Rp)*mp.acos(Rp/R)

def col_central(r_in, r_out, C):
    """central column through the plane with inner cap r_in and outer cap r_out:
       2 * C/(4piG) * (1/r_in - 1/r_out).  r_out -> inf gives C/(2 pi G r_in)."""
    return C/(2*mp.pi*G)*(1/r_in - 1/r_out)

def col_numeric(R, rM, a0, r_in, n=6000):
    """full-kernel vertical column at projected radius R using the exact MONO density:
       2 integral_{z_lo}^{inf} rho_MONO(sqrt(R^2+z^2)) dz,  z_lo = sqrt(max(r_in^2-R^2,0)).
       Substitution z = R*tan(theta), theta in [theta_lo, pi/2): dz = R dtheta/cos^2(theta),
       r = R/cos(theta).  Exact infinite range; midpoint rule, n points."""
    if R <= 0:
        return mp.inf
    th_lo = mp.atan(mp.sqrt(max(r_in*r_in - R*R, mp.mpf(0)))/R) if R < r_in else mp.mpf(0)
    th_hi = mp.pi/2
    s = 0
    for i in range(1, n+1):
        th = th_lo + (th_hi-th_lo)*(mp.mpf(i) - mp.mpf("0.5"))/n
        r = R/mp.cos(th)
        rho = rho_MONO(r, rM, a0)
        s += rho/mp.cos(th)**2
    return 2*R*(th_hi-th_lo)*s/n

checks = []
def check(name, ok, detail, tol):
    checks.append({"name": name, "pass": bool(ok), "detail": str(detail)[:150], "tolerance": tol})

C_scale = {}
floor_tab = {}
col_tab = {}
for a0, tag, M_b_Msun in [(A0_CAN, "canonical", mp.mpf("6e10")), (A0_ALT, "alternative", mp.mpf("6e10"))]:
    M_b = M_b_Msun*MSUN
    C = mp.sqrt(G*M_b*a0)
    rM = mp.sqrt(G*M_b/a0)
    C_scale[tag] = {"C": C, "rM_m": rM, "rM_kpc": rM/KPC, "v_flat_kms": C**mp.mpf("0.25")/1000}
    Sigma_quad = a0/(4*mp.pi*G)
    Sigma_m = a0/(2*mp.pi*G)
    R0 = mp.mpf("8.2")*KPC
    # (D) crossing radius where nominal Sigma(R) = Sigma_quad:
    R_crit = mp.pi*C/a0                      # = pi * r_M  (C = a0 r_M)
    # central floor with r_in = r_M/sqrt(y_star) (the MONO-splice radius) and r_out -> inf:
    r_in = rM/mp.sqrt(y_star)
    floor_c = col_central(mp.mpf("0.1")*rM, mp.mpf("1e6")*rM, C)   # cap at 0.1 r_M
    floor_nom = Sigma_nominal(r_in, C)
    # (E) full-MONO numeric column at R0 and at the splice radius; nominal at same R:
    col_R0_num = col_numeric(R0, rM, a0, mp.mpf("1e-3")*rM)
    col_R0_nom = Sigma_nominal(R0, C)
    col_R0_RAR_corr = col_R0_nom*(1 - (rM/R0)**2/mp.mpf("24"))     # leading RAR-tail correction
    col_splice_num = col_numeric(r_in, rM, a0, mp.mpf("1e-3")*rM)
    col_splice_nom = Sigma_nominal(r_in, C)
    floor_tab[tag] = {
        "Sigma_quad_Msun_pc2": Sigma_quad/MSUN_PC2, "Sigma_m_Msun_pc2": Sigma_m/MSUN_PC2,
        "R_crit_kpc": R_crit/KPC, "r_in_splice_kpc": r_in/KPC,
        "col_R0_nom_Msun_pc2": col_R0_nom/MSUN_PC2, "col_R0_fullMONO_Msun_pc2": col_R0_num/MSUN_PC2,
        "col_R0_RARcorr_Msun_pc2": col_R0_RAR_corr/MSUN_PC2,
        "col_splice_nom_Msun_pc2": col_splice_nom/MSUN_PC2, "col_splice_fullMONO_Msun_pc2": col_splice_num/MSUN_PC2,
        "floor_0.1rM_Msun_pc2": floor_c/MSUN_PC2,
    }
    # (A) exact integral identities vs numerical Abel (independent representation):
    #     deep asymptote R >> rM, tolerance set BEFORE evaluation; inner rows are domain table only
    col_table_row = {}
    for Rr in [mp.mpf("0.5"), mp.mpf("0.65"), mp.mpf("0.8"), mp.mpf("1"), mp.mpf("1.5"),
               mp.mpf("3"), mp.mpf("5"), mp.mpf("10"), mp.mpf("30")]:
        R = Rr*rM
        s_nom = Sigma_nominal(R, C)
        s_num = col_numeric(R, rM, a0, mp.mpf("1e-3")*rM)
        col_table_row[str(Rr)] = {"nominal_Msun_pc2": mp.nstr(s_nom/MSUN_PC2, 9),
                                  "fullMONO_Msun_pc2": mp.nstr(s_num/MSUN_PC2, 9),
                                  "ratio": mp.nstr(s_num/s_nom, 9)}
        if Rr in (mp.mpf("10"), mp.mpf("30")):
            check(f"A deep-asymptote {tag} R={Rr}rM", abs(s_num/s_nom - 1) < mp.mpf("1e-3"),
                  f"full-MONO/nominal - 1 = {mp.nstr(s_num/s_nom-1,6)}", "rel < 1e-3 for R >> rM")
    col_tab[tag] = col_table_row
    # (B) capped form: edge column -> 0 (gap 1e-30); infinite-cap limit -> nominal
    Rs = mp.mpf("10")*rM
    s_cap = Sigma_capped(mp.mpf("3")*rM, Rs, C)
    s_cap_inf = Sigma_capped(mp.mpf("3")*rM, mp.mpf("1e12")*rM, C)
    edge = Sigma_capped(Rs*(1 - mp.mpf("1e-30")), Rs, C)
    check(f"B cap-edge-zero {tag}", abs(edge) < mp.mpf("1e-9")*s_cap,
          f"Sig_cap at cap edge (gap 1e-30) ~ {mp.nstr(edge/MSUN_PC2,6)} Msun/pc2", "-> 0 as Rp -> R")
    check(f"B cap->nominal {tag}", abs(s_cap_inf - Sigma_nominal(mp.mpf("3")*rM, C))/Sigma_nominal(mp.mpf("3")*rM, C) < mp.mpf("1e-9"),
          f"cap(R=3rM; R_out=1e12 rM) = {mp.nstr(s_cap_inf/MSUN_PC2,8)} vs nominal {mp.nstr(Sigma_nominal(mp.mpf('3')*rM, C)/MSUN_PC2,8)} Msun/pc2", "-> 0")
    # (C) central column: 1/r_in law (outer cap at 1e30 r_M; exact infinite-cap limit)
    ci = col_central(mp.mpf("0.5")*rM, mp.mpf("1e30")*rM, C)
    ci_exact = C/(2*mp.pi*G*mp.mpf("0.5")*rM)
    check(f"C central-col 1/r_in {tag}", abs(ci - ci_exact)/ci_exact < mp.mpf("1e-28"),
          f"col(0.5rM; inf) = {mp.nstr(ci/MSUN_PC2,10)} Msun/pc2 = C/(2piG r_in) = Sigma_pi (a0/(piG)) exactly",
          "relative < 1e-28 (exact identity, outer cap 1e30 rM)")
    # (D) slab-ceiling violation floor: nominal floor at splice vs Sigma_quad (the ZD07 issue)
    check(f"D floor>ceil at splice {tag}", floor_nom > Sigma_quad,
          f"nominal col at splice = {mp.nstr(floor_nom/MSUN_PC2,8)} vs Sigma_quad = {mp.nstr(Sigma_quad/MSUN_PC2,8)} Msun/pc2",
          "floor > ZD07 slab ceiling (FK: MONO must cap or ceiling fails, cf. AS009/WAVE0)")
    check(f"D R_crit=pi rM {tag}", abs(R_crit - mp.pi*rM)/rM < mp.mpf("1e-25"),
          f"R_crit = {mp.nstr(R_crit/KPC,8)} kpc = pi r_M = {mp.nstr(mp.pi*rM/KPC,8)} kpc", "exact")

# (E) inner-side domain statement: at R = r_M the FULL-MONO column must differ from the nominal
#     1/r^2 law (the operative inner profile is the MONO log-phantom, not the deep 1/r^2 cell);
#     at R = 10, 30 r_M it must agree within 1e-3 (already checked in A).  Both can fail.
for tag, a0 in [("canonical", A0_CAN), ("alternative", A0_ALT)]:
    M_b = mp.mpf("6e10")*MSUN
    C = mp.sqrt(G*M_b*a0); rM = mp.sqrt(G*M_b/a0)
    R = rM
    s_nom = Sigma_nominal(R, C); s_num = col_numeric(R, rM, a0, mp.mpf("1e-3")*rM)
    check(f"E inner-side differs {tag}", abs(s_num/s_nom - 1) > mp.mpf("1e-2"),
          f"full-MONO/nominal - 1 at R=rM = {mp.nstr(s_num/s_nom-1,6)} (log-phantom inner side, not 1/r^2)",
          "inner side differs from the deep law (domain statement)")

npass = sum(1 for c in checks if c["pass"])
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print(f"AS049 phantom-disk appendix: {npass}/{len(checks)} checks PASS (wall {time.time()-t0:.2f}s, ru_maxrss raw={rss})")
assert rss < 512*1024*1024
for c in checks:
    print(f"  [{'PASS' if c['pass'] else 'FAIL'}] {c['name']}: {c['detail']}")
out = {
    "checks": checks,
    "constants": {"G": str(G), "c": str(C_LIGHT), "MSUN_PC2": str(MSUN_PC2)},
    "C_scale": {k: {kk: (str(vv) if not isinstance(vv, float) else vv) for kk, vv in v.items()} for k, v in C_scale.items()},
    "floor_tab": floor_tab,
    "col_tab": col_tab,
    "landmarks": {"y_p": mp.nstr(y_p, 15), "y_star": mp.nstr(y_star, 15), "c_mono": mp.nstr(c_mon, 15)},
}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "checks_phantom_disk.json"), "w") as f:
    json.dump(out, f, indent=1, default=str)
print(json.dumps({"C_scale": C_scale, "floor_tab": floor_tab, "col_tab": col_tab}, indent=1, default=str))
assert npass == len(checks)
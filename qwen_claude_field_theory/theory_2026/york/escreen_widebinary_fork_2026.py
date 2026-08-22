"""
HOSTILE REFEREE:  is the Cassini-passing region of the scalar e-screen a REAL escape
or the Cassini<->wide-binary lock in disguise?

Setup (frozen, same as escreen_Q2_map_2026.py):
    mu_eff(x, eps) = 1 - A(eps)*(1 - mu_gal(x)),   mu_gal(x)=x/sqrt(1+x^2)
    A(eps) = 1/(1 + (eps/eps_s)^m),   eps = e^2/a0^2
    e -> |g_ext| in an EMBEDDED subsystem (Solar System, wide binary),  e -> 0 isolated galaxy.
    Solar neighborhood external field g_e = Vc^2/R0 => eps = eps_e = eta^2.

The e-screen suppresses the Cassini EFE quadrupole because  Q2 ~ A(eps_e) * q_standard(eta)
(linear in A, verified in escreen_Q2_map).  The Cassini-PASSING region is A(eps_e) <~ 0.2.

Referee's four probes, all at the SAME (m,eps_s) that pass Cassini:
 (1) wide binaries in the solar neighborhood share eps_e -> same A -> boost 1/mu_eff(eta,eps_e)-1.
     Does it collapse to Newtonian (killing registered gamma_v=1.2139)?
 (2) is there an eps_s window: Solar System (eps_e~3-5) screened, but the systems where EFE is
     actually OBSERVED (dwarf satellites, Chae RAR-EFE; which eps_h?) UN-screened?
 (3) does a sharp A(eps) (large m) make an abrupt spatial screening boundary?
 (4) relabelling of the lock, or genuine daylight?

numpy for every number; both a0 footings; do not manufacture a pass or a deficit.
"""
import numpy as np

G, MSUN = 6.6743e-11, 1.98892e30
GM   = G*MSUN
KPC  = 3.0856775814913673e19
KMS  = 1.0e3
kAU  = 1.496e14

Vc, R0 = 229.0*KMS, 8.2*KPC
g_e = Vc**2/R0

A0_STD, A0_CAN, A0_ALT = 1.20e-10, 9.3619e-11, 1.1279e-10
CASSINI_95 = 5.1e-27

def mu_gal(x): return x/np.sqrt(1.0+x*x)
def mu_eff(x,A): return 1.0 - A*(1.0-mu_gal(x))
def A_screen(eps,m,eps_s): return 1.0/(1.0+(eps/eps_s)**m)
def head(t): print("\n"+"="*84+"\n"+t+"\n"+"="*84)
def line(t): print("  "+t)

head("(0) shared field: Solar System AND solar-neighborhood wide binaries see the SAME g_e")
line(f"g_e = Vc^2/R0 = {g_e:.4e} m/s^2  (Vc=229 km/s, R0=8.2 kpc)")
foot = []
for nm,a0 in (("standard  a0=1.20e-10",A0_STD),
              ("canonical a0=9.36e-11",A0_CAN),
              ("alt       a0=1.128e-10",A0_ALT)):
    eta=g_e/a0; eps_e=eta**2
    foot.append((nm,a0,eta,eps_e))
    line(f"{nm}:  eta={eta:.4f}  eps_e=eta^2={eps_e:.4f}  mu_gal(eta)={mu_gal(eta):.4f}  "
         f"full-MOND boost 1/mu_gal(eta)-1={1/mu_gal(eta)-1:+.4f}")

# ----------------------------------------------------------------------------------
# Cassini-passing (m,eps_s) cells, per footing, from Q2 ~ A * Q2_baseline.
# baseline Q2 (A=1) from Q2-map: standard 20.40e-27, canonical 14.66e-27, alt 18.87e-27.
# Passing needs A(eps_e) < CASSINI_95 / Q2_baseline.
# ----------------------------------------------------------------------------------
Q2base = {"standard  a0=1.20e-10":20.40e-27,
          "canonical a0=9.36e-11":14.66e-27,
          "alt       a0=1.128e-10":18.87e-27}
m_list   = [2,4,8,16]
eps_s_list = [0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0]

head("(1) WIDE-BINARY BOOST at the Cassini-passing cells  (same eps_e -> same A)")
line("boost(A) = 1/mu_eff(eta,eps_e) - 1 ;  full-MOND boost is boost(A=1).")
line("Q2 passes when A(eps_e) < A_pass := Cassini95 / Q2_baseline.\n")
for nm,a0,eta,eps_e in foot:
    Apass = CASSINI_95/Q2base[nm]
    b_full = 1.0/mu_eff(eta,1.0)-1.0
    head2 = f"footing {nm}: eta={eta:.3f}, eps_e={eps_e:.3f}, A_pass={Apass:.3f}, full-MOND boost={b_full:+.4f}"
    print("  "+head2)
    # enumerate passing cells and their A and resulting boost
    passing=[]
    for m in m_list:
        for es in eps_s_list:
            A=A_screen(eps_e,m,es)
            if A < Apass:
                passing.append((m,es,A))
    if not passing:
        line("   NO Cassini-passing cells on this grid.")
        continue
    # show the boost at the *largest* A that still passes (the least-screened passing cell -> most favorable to MOND)
    A_maxpass = max(p[2] for p in passing)
    b_maxpass = 1.0/mu_eff(eta,A_maxpass)-1.0
    m_mp,es_mp = [(m,es) for (m,es,A) in passing if A==A_maxpass][0]
    line(f"   #passing cells = {len(passing)}/{len(m_list)*len(eps_s_list)}")
    line(f"   least-screened PASSING cell: m={m_mp}, eps_s={es_mp}, A={A_maxpass:.4f}")
    line(f"   -> wide-binary boost there = {b_maxpass:+.4f}   "
         f"({b_maxpass/b_full:.1%} of full-MOND {b_full:+.4f})")
    # gamma_v: velocity ratio ~ sqrt(acceleration boost). registered full-MOND gamma_v=1.2139.
    # (gamma_v-1) scales ~ (1/2)(1/mu_eff-1) at small boost -> ~ A. Use the ratio to dilute it.
    gv_full = 1.2139
    gv_screened = 1.0 + (gv_full-1.0)*(b_maxpass/b_full)
    line(f"   registered gamma_v(full)=1.2139  ->  screened gamma_v ~ {gv_screened:.4f}  "
         f"(NOVERDICT edge >1.26; Newtonian=1.000)")

head("(1b) boost(A) collapse table (footing: alt, eta=1.838) -- boost is monotone in A, ->0 as A->0")
nm,a0,eta,eps_e = foot[2]
b1 = 1.0/mu_eff(eta,1.0)-1.0
line(f"{'A':>7}{'mu_eff(eta,A)':>16}{'boost=1/mu_eff-1':>20}{'boost/boost(1)':>16}")
for A in (1.0,0.5,0.3,0.2,0.1,0.05,0.02,0.0):
    b=1.0/mu_eff(eta,A)-1.0
    line(f"{A:>7.2f}{mu_eff(eta,A):>16.5f}{b:>20.5f}{(b/b1 if b1 else 0):>16.4f}")

# ----------------------------------------------------------------------------------
# (2) WHERE is EFE actually OBSERVED?  host-field eps_h of the canonical EFE systems.
# ----------------------------------------------------------------------------------
head("(2) eps_h of the systems where EFE is OBSERVED (do they sit BELOW eps_s?)")
line("host field g_h at the test system; eps_h=(g_h/a0)^2.  a0=1.2e-10 used for eps_h.")
a0ref=A0_MG = 1.20e-10
def eps_of_g(g): return (g/a0ref)**2

# (a) solar-neighborhood wide binaries: SAME g_e
line(f"(a) solar-nbhd WIDE BINARIES : g_h=g_e={g_e:.2e}  eps_h={eps_of_g(g_e):.3f}   "
     f"(== Solar System eps_e -> shares the screen)")

# (b) MW/M31 dwarf satellites (classic EFE systems): g_h = Vc_host^2 / d
for name,Vhost,d_kpc in (("Crater II (MW, d~117kpc)",229e3,117.0),
                         ("Antlia II (MW, d~130kpc)",229e3,130.0),
                         ("Fornax   (MW, d~140kpc)",229e3,140.0),
                         ("And XIX  (M31, d~110kpc)",225e3,110.0)):
    d=d_kpc*KPC; g_h=Vhost**2/d
    line(f"(b) {name:<26}: g_h={g_h:.2e}  eps_h={eps_of_g(g_h):.4f}   (g_h/a0={g_h/a0ref:.3f})")

# (c) Chae 2020/2022 external-field detection in SPARC rotation curves: e_N ~ 0.01-0.1 a0
for eN in (0.01,0.03,0.1):
    line(f"(c) Chae RAR-EFE field e_N={eN:.2f} a0        : eps_h={eN**2:.4f}")

line("")
line("=> dwarf-satellite & Chae EFE detections live at eps_h ~ 1e-4 .. 5e-2  <<  1.")
line("   Any eps_s that screens the Solar System (eps_e~3-5) satisfies eps_h << eps_s,")
line("   so A(eps_h)~1: those systems are UN-screened. GENUINE window for THAT EFE class.")
line("   BUT solar-nbhd wide binaries have eps_h = eps_e -> screened with the Solar System.")

# quantify: A at the dwarf/Chae fields for a representative screening (m=8, eps_s=3.0)
head("(2b) A(eps_h) at a representative Cassini-passing screen (m=8, eps_s=3.0)")
for label,eps_h in (("Solar System / wide binary (eps_e~3.4)",foot[2][3]),
                    ("Fornax dwarf (eps_h~0.010)",eps_of_g(229e3**2/(140*KPC))/1.0),
                    ("Crater II  (eps_h~0.015)",eps_of_g(229e3**2/(117*KPC))),
                    ("Chae field e_N=0.1a0 (eps_h=0.01)",0.01),
                    ("Chae field e_N=0.03a0 (eps_h=9e-4)",0.03**2)):
    A=A_screen(eps_h,8,3.0)
    line(f"{label:<42}: A={A:.5f}  -> {'SCREENED (MOND off)' if A<0.3 else 'UN-screened (MOND on)'}")

# ----------------------------------------------------------------------------------
# (3) abrupt spatial screening boundary from sharp m?
# ----------------------------------------------------------------------------------
head("(3) sharp-m spatial boundary: gamma_v of a wide binary vs GALACTOCENTRIC radius R")
line("external field along the MW disk g_e(R)=Vc^2/R (flat Vc) -> eps_e(R)=(Vc^2/(R a0))^2.")
line("screen m=16, eps_s=3.0, a0=1.2e-10. boost = 1/mu_eff(eta(R),eps_e(R))-1.")
line(f"{'R[kpc]':>8}{'g_e/a0':>9}{'eps_e':>9}{'A':>9}{'boost':>10}")
for Rk in (4,6,8,8.2,10,12,15,20):
    R=Rk*KPC; ge=Vc**2/R; eta=ge/a0ref; eps=eta**2
    A=A_screen(eps,16,3.0); b=1.0/mu_eff(eta,A)-1.0
    line(f"{Rk:>8.1f}{eta:>9.3f}{eps:>9.3f}{A:>9.4f}{b:>10.4f}")
line("")
line("Interpretation: the MW ROTATION CURVE itself is unaffected (galaxy interior e->0, A->1).")
line("The step lives in the EMBEDDED wide-binary population: a sharp-m screen predicts an")
line("abrupt gamma_v(R) step across the solar circle -- a testable but awkward DR4 signature,")
line("NOT a rotation-curve distortion.")

# ----------------------------------------------------------------------------------
# (4) verdict
# ----------------------------------------------------------------------------------
head("(4) VERDICT")
line("Two DISTINCT EFE classes resolve differently at the Cassini-passing (m,eps_s):")
line("")
line(" A. solar-neighborhood WIDE BINARIES  (framework's registered gamma_v=1.2139 DR4 target):")
line("    eps_h = eps_e ~ 3-5 = IDENTICAL to the Solar System.  The e-BC cannot tell a binary")
line("    from the planetary system in the same MW field.  boost collapses with A: at the")
line("    least-screened PASSING cell boost is ~15-25% of full-MOND, gamma_v -> ~1.03-1.05.")
line("    => FORK-IN-DISGUISE. Cassini-safe forces this wide-binary prediction toward Newton,")
line("       reproducing the DHF 'alpha_grav driven to ~0 by Cassini' standing result.")
line("")
line(" B. dwarf satellites + Chae RAR external-field detections:  eps_h ~ 1e-4 .. 5e-2 << eps_s.")
line("    A(eps_h) ~ 1 -> UN-screened, MOND+EFE fully alive.  => GENUINE DAYLIGHT: the e-screen")
line("    DOES separate the Solar System from the low-field systems where EFE is actually seen.")
line("")
line("NET: the scalar e-screen opens a real window for the LOW-FIELD EFE phenomenology, but it")
line("does NOT escape the specific Cassini<->wide-binary lock -- the two share eps_e by")
line("construction. The registered gamma_v=1.2139 DR4 prediction is the casualty; if DR4 sees")
line("gamma_v~1.2 the Cassini quadrupole is a real unresolved problem, if DR4 sees Newtonian it")
line("is consistent but the MOND-gravity wide-binary reading is dead. Either way the escape is")
line("PARTIAL: cluster/satellite EFE survives, the solar-neighborhood wide-binary prediction does not.")
print("\nDONE.")

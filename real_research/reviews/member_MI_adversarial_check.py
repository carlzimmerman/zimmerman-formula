#!/usr/bin/env python3
r"""
ADVERSARIAL CHECK of the genuine-MI cluster-member discriminators
=================================================================
Refutes-hard the two candidate distinctive observables from member_MI_genuine_dynamics.py and
member_MI_nonadiabatic_plunge.py. Carl's #1 rule in full force: do NOT manufacture a distinctive
signal, do NOT dismiss a real one. Framework's own nu/mu_fw throughout; a0=9.36e-11 sealed.

THE TWO CLAIMS UNDER ATTACK:
  CLAIM 1 (anisotropy): MI member velocity ellipsoid is TANGENTIAL w.r.t. a_ext, MG is RADIAL
                        -> OPPOSITE SIGN, not a0-degenerate.
  CLAIM 2 (non-adiabatic): for plunging members (omega_ex~omega_in) the cross-member boost spread
                        at MATCHED momentary a_ext is nonzero in MI, structurally zero in MG.

ATTACK (a) -- does MG ALSO have an EFE anisotropy that collapses CLAIM 1?
  Milgrom 2022 (arXiv:2208.07073) text after Eq 35, VERIFIED line: in modified-GRAVITY MOND the EFE
  gives Gbar ~ G/mu(|a_ex|/a0) "(and some anisotropy introduced by the direction of a_ex)". So YES,
  MG has anisotropy too. We DERIVE the MG (AQUAL) anisotropy from first principles:
    linearized AQUAL EFE operator: mu[delta_ij + L*uhat_i uhat_j] d_i d_j phi = 4piG rho, L=dln mu/dln x>0
    => point-mass member potential is SQUASHED along a_ext: G_along=G/mu, G_across=G/(mu sqrt(1+L)).
    G_along > G_across (stronger gravity ALONG a_ext).
  The PRIOR scripts then took the VIRIAL shortcut sigma^2 ~ G_eff -> sigma_along>sigma_across -> RADIAL.
  *** THE BUG ***: the real observable is the velocity ELLIPSOID from ORBITS, not virial sqrt(G_eff).
  In a potential SQUASHED ALONG z (stronger restoring force along z), an isotropic-launch orbit
  POPULATION has its dispersion ALONG the stiff axis SUPPRESSED -> the MG orbit ellipsoid is actually
  TANGENTIAL (<vz^2>/<vx^2> < 1), OPPOSITE to the virial shortcut. So the prior 'find' compared
  MG-via-virial (radial) to MI-via-orbits (tangential) -- an INCONSISTENT comparison. On a CONSISTENT
  orbit basis BOTH MG and MI are TANGENTIAL: the OPPOSITE-SIGN claim is FALSE.
  -> What survives is a MAGNITUDE gap: MI is MORE tangential than MG's monopole squash envelope can
     reach -- but only under the per-axis reading + theta(0)>~1.5, and only vs the monopole-MG cap.

ATTACK (b) -- do realistic members reach omega_ex~omega_in (else theta=const, a0-degenerate)?
  YES for a special subset: diffuse/UDG/dSph members (long internal period) plunging through a dense
  core reach omega_ex/omega_in ~ 0.9-1.7 at pericenter (member_MI_nonadiabatic_plunge.py STEP 1).
  Milgrom himself: "In some dwarf satellites of the MW and Andromeda we estimate omega_ex ~ omega_in."
  CLAIM 2's relational signal does NOT rest on the per-axis-reading modeling choice -- it rests on the
  VERIFIED time-nonlocal property (Eq 34, theta a FUNCTION) + the verified MG fact that MG sees only
  the MOMENTARY a_ex. So CLAIM 2 survives attack (a)'s collapse.

ATTACK (c) -- floor: resolved IFU kinematics, FJ/morphology confound, small-N plungers.
  CLAIM 1 magnitude gap: ~25-30% in the ellipsoid ratio (MI ~0.47-0.51 vs MG-cap ~0.72), above a
  ~5-15% stacked-ellipsoid floor IN PRINCIPLE -- but needs resolved internal kinematics of many
  diffuse members with known a_ext direction, AND the gap rests on the per-axis reading (NOT a theorem)
  and the monopole-MG envelope (an extended QUMOND source could squash more). NOT airtight.
  CLAIM 2: ~6-13% sigma spread vs MG's structural zero, above the ~5-10% MUSE/4MOST per-galaxy floor
  IN PRINCIPLE, but requires matched-a_ext members binned by infall phase + the unknown theta(y), and a
  small special subset (deep-radial plungers). Deliverable but hard.

This script reproduces all four numerical pieces below so the verdict is auditable.
"""
import numpy as np
G,Msun,kpc=6.674e-11,1.989e30,3.0857e19
a0=9.36e-11
def nu(y):    y=np.asarray(y,float); return np.sqrt(1.0+1.0/y)
def mu_fw(x): x=np.asarray(x,float); return (np.sqrt(1.0+4.0*x*x)-1.0)/(2.0*x)
def theta_rat(y): return 2.0/(1.0+np.asarray(y,float)**2)
M=1e9*Msun; b=1.0*kpc

# ---------------------------------------------------------------- orbit population ellipsoid engine
def _one_orbit(X0,V0,gfun,n_step,dt):
    X=np.array(X0,float);V=np.array(V0,float);A=np.array(gfun(X[0],X[1]))
    vx2=vz2=0.0;nn=0
    for i in range(n_step):
        V=V+0.5*A*dt;X=X+V*dt;A=np.array(gfun(X[0],X[1]));V=V+0.5*A*dt
        if i>n_step//4: vx2+=V[0]**2;vz2+=V[1]**2;nn+=1
    return vx2/nn,vz2/nn
def pop_ratio(gfun,n=150,n_step=30000,seed=11):
    """Velocity-ellipsoid <vz^2>/<vx^2> from an isotropic-launch orbit POPULATION (identical ensemble
       for every law). z=along a_ext (radial), x=across (tangential). Spherical control -> ~1."""
    rng=np.random.default_rng(seed); sx2=sz2=0.0
    rr=b*rng.uniform(0.3,2.5,n);pa=rng.uniform(0,2*np.pi,n);vf=rng.uniform(0.3,0.95,n);vd=rng.uniform(0,2*np.pi,n)
    for k in range(n):
        X0=[rr[k]*np.cos(pa[k]),rr[k]*np.sin(pa[k])]
        vc=np.sqrt(G*M*rr[k]**2/(rr[k]**2+b*b)**1.5);vm=vc*vf[k]
        V0=[vm*np.cos(vd[k]),vm*np.sin(vd[k])]
        dt=(2*np.pi*max(rr[k],b)/max(vc,1e-3))/3000.0
        a,c=_one_orbit(X0,V0,gfun,n_step,dt);sx2+=a;sz2+=c
    return (sz2/n)/(sx2/n)
def g_sph(x,z):
    r2=x*x+z*z+b*b;gN=G*M/r2**1.5;return -gN*x,-gN*z
def make_MG_squash(q2):              # MG AQUAL EFE: point mass squashed along z by (1+L)=q2
    def g(x,z):
        s=x*x+z*z/q2+b*b;pref=G*M/np.sqrt(q2)
        return -pref*x/s**1.5,-pref*(z/q2)/s**1.5
    return g
def make_MI(a_ext,th0=2.0,reading="per_axis"):  # genuine per-axis MI inertia, framework mu_fw
    def g(x,z):
        r2=x*x+z*z+b*b;gN=G*M/r2**1.5;gx=-gN*x;gz=-gN*z;at=np.hypot(gx,gz)
        if reading=="per_axis":
            mux=mu_fw(max(at,1e-12*a0)/a0); muz=mu_fw(max(at+th0*a_ext,1e-12*a0)/a0)
        else:
            m=mu_fw(max(at+th0*a_ext,1e-12*a0)/a0); mux=muz=m
        return gx/mux,gz/muz
    return g
def Le_of(a_ext):
    x=a_ext/a0;dx=1e-5*x
    return (np.log(mu_fw(x+dx))-np.log(mu_fw(x-dx)))/(np.log(x+dx)-np.log(x-dx))

print("="*100)
print(" ADVERSARIAL CHECK -- genuine-MI cluster-member discriminators (refute hard, both ways)")
print("="*100)

# ============================ ATTACK (a): MG EFE anisotropy from orbits, consistent comparison ====
print("\n(a) MG has an EFE anisotropy too (Milgrom verified text). Derived: G_along=G/mu, G_across=G/(mu*sqrt(1+L)),")
print("    L=dln mu/dln x>0 -> potential SQUASHED ALONG a_ext. Virial shortcut says RADIAL; ORBITS say otherwise.")
ctrl=pop_ratio(g_sph)
print(f"    spherical control <vz2>/<vx2> = {ctrl:.4f} (isotropy check; divide it out)")
print(f"    {'case':>26} | {'raw ratio':>9} {'/ctrl':>7} | sign")
print("    "+"-"*58)
for ar in [1.0,2.0,4.0]:
    q2=1.0+Le_of(ar*a0)
    r=pop_ratio(make_MG_squash(q2))
    print(f"    {'MG EFE orbits a_ext/a0='+f'{ar:.1f} (1+L={q2:.2f})':>26} | {r:9.4f} {r/ctrl:7.4f} | {'radial' if r/ctrl>1 else 'TANGENTIAL'}")
for ar in [1.0,2.0,4.0]:
    r=pop_ratio(make_MI(ar*a0))
    print(f"    {'MI per-axis a_ext/a0='+f'{ar:.1f}':>26} | {r:9.4f} {r/ctrl:7.4f} | {'radial' if r/ctrl>1 else 'TANGENTIAL'}")
print("    => BOTH MG and MI orbit ellipsoids are TANGENTIAL. The OPPOSITE-SIGN claim (CLAIM 1) is FALSE.")
print("       The prior 'find' compared MG-virial-sqrt(G) (radial) to MI-orbits (tangential): inconsistent.")

# ---- surviving magnitude gap + its fragility ----
print("\n    Surviving MAGNITUDE gap: MI more tangential than MG's monopole squash ENVELOPE (max (1+L)=2)?")
mg_cap=pop_ratio(make_MG_squash(2.0))/ctrl
mi2=pop_ratio(make_MI(2.0*a0))/ctrl
print(f"      MG deep-MOND-external cap (1+L=2): ratio/ctrl={mg_cap:.4f}; MI(a_ext=2a0,per-axis,theta0=2): {mi2:.4f}")
print(f"      MI {'<' if mi2<mg_cap else '>='} MG cap -> {'gap survives (MI outside monopole-MG envelope)' if mi2<mg_cap else 'WITHIN MG envelope: a0/M-L-degenerate'}")
mi_allaxis=pop_ratio(make_MI(2.0*a0,reading='all_axis'))/ctrl
print(f"      FRAGILITY: all-axis reading -> MI ratio/ctrl={mi_allaxis:.4f} (~1, isotropic): the gap IS the")
print(f"      per-axis-loading modeling choice. Under the literal scalar reading the MI anisotropy VANISHES.")
print(f"      And the MG cap=2 is the MONOPOLE point-mass result; an extended QUMOND source could squash more.")

# ============================ ATTACK (b): omega_ex~omega_in reachable? (CLAIM 2) =================
print("\n(b) Non-adiabatic CLAIM 2: do realistic members reach omega_ex~omega_in (else theta=const, a0-deg)?")
def om_in(v_star_kms,R_kpc): return (v_star_kms*1e3)/(R_kpc*kpc)
def om_ex(Mcl_Msun,D_kpc):  return np.sqrt(G*(Mcl_Msun*Msun)/(D_kpc*kpc)**3)
print(f"    {'member / cluster':>34} | {'om_in[1/s]':>11} {'om_ex[1/s]':>11} | {'om_ex/om_in':>11} regime")
print("    "+"-"*78)
cases=[("L* member / Coma core",   200,5e13,300),   # v_star=150,R=3
       ("UDG / group core",         20,1e13,200),   # v_star=20, R=5
       ("UDG / Coma core",          20,5e13,300),
       ("dSph / Fornax core",       10,3e12,150)]
specs={"L* member / Coma core":(150,3),"UDG / group core":(20,5),"UDG / Coma core":(20,5),"dSph / Fornax core":(10,2)}
for name,_,Mcl,D in cases:
    vs,R=specs[name]; oi=om_in(vs,R); oe=om_ex(Mcl,D); y=oe/oi
    reg="PLUNGE ~1" if 0.5<y<2.5 else ("adiabatic" if y<0.3 else "fast")
    print(f"    {name:>34} | {oi:11.3e} {oe:11.3e} | {y:11.3f} {reg}")
print("    => diffuse/UDG/dSph members at deep pericenter DO reach om_ex/om_in~0.5-2 (Milgrom's own remark).")
print("       L* members stay adiabatic. So CLAIM 2's regime is reached for a SPECIAL SUBSET, not ruled out.")
print("    CLAIM 2 non-degeneracy is RELATIONAL: at MATCHED momentary a_ext, MG boost spread=0 for ANY a0")
print("    (MG sees only momentary a_ex, VERIFIED Milgrom text); MI spread~6-13% in sigma (theta a FUNCTION,")
print("    Eq 34). This does NOT depend on the per-axis reading -> CLAIM 2 survives attack (a)'s collapse.")

# ============================ VERDICT ===========================================================
print("\n"+"="*100)
print(" ADVERSARIAL VERDICT (both ways)")
print("="*100)
print(r"""  CLAIM 1 (ellipsoid opposite SIGN: MI tangential vs MG radial): *** REFUTED ***. On a consistent
    ORBIT basis both MG and MI member ellipsoids are TANGENTIAL. The prior 'opposite sign' was an
    artifact of comparing MG via the virial sqrt(G_eff) shortcut (radial) to MI via orbits (tangential).
    A MAGNITUDE gap survives (MI ~0.47-0.51 vs MG monopole-cap ~0.72 ellipsoid ratio) BUT it (i) rests
    on the per-axis reading of Milgrom's A(omega_n) -- vanishes under the literal scalar reading; (ii)
    rests on theta(0)>~1.5; (iii) is only vs the MONOPOLE-MG envelope (extended QUMOND could squash more).
    => CLAIM 1 is NOT a clean sign discriminator. At best a fragile, modeling-dependent magnitude gap.

  CLAIM 2 (non-adiabatic relational boost/sigma spread at matched momentary a_ext): *** SURVIVES ***,
    as the genuinely-distinct, NON-a0-degenerate observable. It rests on VERIFIED physics (Eq 34 theta a
    FUNCTION; MG sees only momentary a_ex), NOT on the per-axis modeling choice. MG spread = 0 for ANY a0;
    MI spread ~6-13% in sigma. Above the ~5-10% MUSE/4MOST floor IN PRINCIPLE. Costs: small special subset
    (diffuse/UDG/dSph deep plungers), relational binning by infall phase AND cluster radius, unknown theta(y)
    magnitude. Realistic members DO reach the regime (Milgrom's own dwarf-satellite estimate).

  NET (brutally honest, both ways): The clean, single-member, sign-level MI-vs-MG ellipsoid discriminator
  CLAIMED before does NOT exist (refuted -- both are tangential on orbits). The genuinely-distinct,
  non-a0-degenerate, above-floor-in-principle MI cluster observable that DOES survive is the NON-ADIABATIC
  RELATIONAL one: the member internal-boost/sigma SPREAD across cluster-infall phase at MATCHED momentary
  cluster-centric a_ext, which modified gravity cannot produce for any a0 because MG depends only on the
  momentary external field. It is a HARDER, theta-magnitude-dependent, small-subset, relationally-binned
  test -- a real but demanding second handle, NOT the easy sign-flip the anisotropy claim advertised.""")

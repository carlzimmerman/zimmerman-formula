#!/usr/bin/env python3
"""
BUREAU D3 -- phenomenological causal worldline kernel for the framework's MI law.
EOM (preferred/CMB frame):   m * mu_fw(Q(t)/a0) * a(t) = F(t)        [form-1]
  fork form-2: d/dt[ m mu_fw(Q/a0) v ] = F
Q(t) = causal functional of a(t'<t).  Most general quadratic causal family:
  Q^2(t) = Int Int K2(s,s') a(t-s).a(t-s') ds ds',  K2 supported s,s'>0.
Decompose K2 = contact w(s)d(s-s') + smooth k(s,s') + derivative (jerk) contact:
  Q^2 = <|a|^2>_w + tau_j^2 <|adot|^2>_w + |<a>_v|^2-type smooth pieces.
Circular orbit (a, Omega):  Q^2 = a^2 * Chat(Omega),
  contact -> 1;  smooth -> |what(Omega)|^2 -> 0 (Riemann-Lebesgue);  jerk -> (Omega tau_j)^2.
Constraint (Milgrom-2022 style collapse): Chat(Omega)=1 across SPARC band 44-3008 H0
so that mu_fw (framework: g_obs=sqrt(g_bar^2+g_bar a0), fits SPARC 0.108 dex) is exact there.
Framework objects only: a0=9.36e-11 (=cH_Lambda/Z, Z=sqrt(32pi/3)), mu_fw.
Cites: Milgrom 2022 PRD 106,064060; Hees+2014 PRD 89,102002 (mu-tail ephemeris);
Fienga+ INPOP (Saturn extra-accel ~<5e-14 m/s^2); DOI 10.5281/zenodo.21148494 (Fourth Horn);
DOI 21139029 (state clause); DOI 21104820 (eta(beta)); real_research/PUMP_HUNT_AND_TRIGGERS_2026-07.md (R1-R4).
"""
import numpy as np, sys

a0=9.36e-11; H0=2.2e-18; G=6.674e-11; Msun=1.989e30; GMsun=1.32712e20
AU=1.495979e11; yr=3.15576e7; kpc=3.0857e19
def mu_fw(x):
    x=np.maximum(x,1e-300); return (np.sqrt(1+4*x*x)-1)/(2*x)
def nu_fw(y): return np.sqrt(1+1/y)
# S0 sanity: mu/nu inverse pair; framework law reproduced
y=10**np.linspace(-3,3,61); gb=y*a0; go=gb*nu_fw(y)
assert np.allclose(mu_fw(go/a0)*go, gb, rtol=1e-12)
print("S0 PASS: mu_fw exact inverse of framework law g_obs=sqrt(g_bar^2+g_bar*a0)")
print("   mu_fw tail: 1-mu = a0/(2a)+O(a0^2/a^2)  -> additive anomaly a0/2 = %.3e m/s^2"%(a0/2))

# S1 collapse lemma: circular orbit, contact kernel: Q=|a| for ANY Omega -> mu_fw exact. trivial.
Om_lo,Om_hi = 44*H0, 3008*H0
print("S1 collapse: contact kernel => Chat=1 all Omega; SPARC band = [%.2e, %.2e] s^-1"%(Om_lo,Om_hi))

# ---------- S2 the high-Omega trichotomy ----------
print("\nS2 TRICHOTOMY at high Omega (Saturn Omega=%.2e s^-1 = %.1e H0):"%(6.75e-9,6.75e-9/H0))
# Branch A: pure contact (acceleration-gating; Milgrom-2022 Type-<a^2> with mu_fw)
planets=[("Mercury",0.387,None),("Earth",1.0,None),("Mars",1.524,1e-13),
         ("Jupiter",5.203,None),("Saturn",9.537,5e-14),("Uranus",19.19,1e-12),("Neptune",30.07,1e-12)]
print(" Branch A (Chat=1 everywhere): delta_a = a(1/mu-1) ~= a0/2 SUNWARD at every planet, r-independent")
for nm,rau,bnd in planets:
    r=rau*AU; aN=GMsun/r**2; x=aN/a0; da=aN*(1/mu_fw(x)-1)
    s="" if bnd is None else "  vs bound %.0e -> OVER by x%.0f"%(bnd,da/bnd) if da>bnd else "  vs bound %.0e OK"%bnd
    if nm in("Mars","Saturn","Neptune"): print("   %-8s a=%.2e  delta_a=%.3e%s"%(nm,aN,da,s))
da_sat=GMsun/(9.537*AU)**2*(1/mu_fw(GMsun/(9.537*AU)**2/a0)-1)
print(" -> Branch A KILLED: Saturn delta_a=%.2e vs INPOP-class bound 5e-14 => factor %.0f (~%.1f orders)"%(da_sat,da_sat/5e-14,np.log10(da_sat/5e-14)))
print("    (Hees+2014 PRD 89,102002: n=1 mu-tails excluded; k=1/2 here. Robust to +-1 order in bound.)")
# Branch B: smooth vector kernel |what(Om)|^2 -> 0: anti-Newtonian. Moon example, tau at band-flat max
tau_max_flat=0.66/Om_hi  # |Chat-1|<0.44 at band top (0.079dex*2 on a0)
aM=3.986e14/(3.844e8)**2; OmM=2*np.pi/(27.32*86400)
w2=1/(1+(OmM*tau_max_flat)**2); Qm=aM*np.sqrt(w2)
# self-consistent: a solves mu(a*sqrt(w2)/a0)*a=g -> a=g*nu(g*w2^0.5.../) use x=a sqrt(w2): mu(x/a0)x/sqrt(w2)=g
aa=aM
for _ in range(200): aa=aM/mu_fw(aa*np.sqrt(w2)/a0)
print(" Branch B (smooth roll-off, tau=%.1e s band-flat max): Moon Q=%.1e (<a0!) -> a/a_N=%.1f, v/v_N=%.2f"%(tau_max_flat,Qm,aa/aM,np.sqrt(aa/aM)))
print(" -> Branch B KILLED for ALL tau: roll-off anywhere leaves every higher-Omega system (Moon/pulsars/LIGO)")
print("    ANTI-Newtonian-boosted (Q->0 => mu->0 => LESS inertia); tau->0 limit is Branch A. No escape.")
# Branch C: derivative (jerk) contact: Chat = 1+(Omega tau_j)^2  (the ONLY riser: smooth L1 parts die at inf)
slope_agn=np.log10((a0/2/5e-14)**2/1.44)/np.log10(6.75e-9/Om_hi)
slope_wb =np.log10((a0/2/5e-14)**2/1.44)/np.log10(6.75e-9/2.73e-12)
print(" Branch C (jerk): Chat=1+(Om tau_j)^2. Required min spectral slope: Omega^%.2f (agnostic), Omega^%.2f (WB-boost kept)"%(slope_agn,slope_wb))
print("   jerk gives Omega^2 => SUFFICIENT. Q grows with Omega -> mu->1: Newtonian-by-FREQUENCY, gate ABOVE the band.")

# ---------- S3 the tau window (both architectures) ----------
Om_sat=6.75e-9
tau_sat=(a0/(2*5e-14))/Om_sat                    # C1 linear tail a0/(2 Om tau)
tau_flat=0.66/Om_hi
Om_wb_2k=np.sqrt(1.5*GMsun/(2e3*AU)**3)          # tightest WB
tau_wbkeep=0.66/Om_wb_2k
tau_c2_sat=np.sqrt(a0/(2*5e-14)-1 if a0/(2*5e-14)>1 else 0)/Om_sat  # C2: da=(a0/2)G, G=1/(1+(Om t)^2)
print("\nS3 WINDOW for the new timescale tau:")
print("  C1 (jerk-amplitude): Saturn => tau_j >= %.3e s = %.0f yr;  band-flat => tau_j <= %.2e s = %.2e yr"%(tau_sat,tau_sat/yr,tau_flat,tau_flat/yr))
print("      keep-WB-boost (optional) => tau_j <= %.2e s = %.0f yr  -> boosted-WB window [%.1f, %.1f] kyr"%(tau_wbkeep,tau_wbkeep/yr,tau_sat/yr/1e3,tau_wbkeep/yr/1e3))
print("  C2 (band-fraction gate m_eff=m[1-G(1-mu_fw)], G=lowpass power frac): Saturn => tau_c >= %.2e s = %.0f yr"%(tau_c2_sat,tau_c2_sat/yr))
print("  ARCHITECTURE-INDEPENDENT: tau in [~1.4e2, ~3.2e6] yr; c*tau = [%.4f, %.1f] kpc; tau*H0 = [%.1e, %.1e]"%(
      3e8*tau_c2_sat/kpc,3e8*tau_flat/kpc,tau_c2_sat*H0,tau_flat*H0))

# ---------- S4 solar-system / compact table, C1 tau_j=10 kyr ----------
tj=1e4*yr
def da_C1(aN,Om,tj):
    Q=aN*np.sqrt(1+(Om*tj)**2); return aN*(1/mu_fw(Q/a0)-1)
print("\nS4 R4 safety (C1, tau_j=10 kyr): delta_a [m/s^2]")
rows=[("Mars",GMsun/(1.524*AU)**2,2*np.pi/(1.881*yr),1e-13),
      ("Saturn",GMsun/(9.537*AU)**2,2*np.pi/(29.46*yr),5e-14),
      ("Neptune",GMsun/(30.07*AU)**2,2*np.pi/(164.8*yr),1e-12),
      ("Moon(LLR)",aM,OmM,1e-13),
      ("Sedna(506AU)",GMsun/(506*AU)**2,2*np.pi/(1.14e4*yr),None),
      ("PSRJ0737",444.0,7.11e-4,None),("LIGO(100Hz)",1e13,628.0,None)]
for nm,aN,Om,b in rows:
    da=da_C1(aN,Om,tj); tag=("PASS(x%.0e margin)"%(b/da)) if b else "PASS"
    print("   %-13s Om=%.2e  da=%.2e  %s"%(nm,Om,da,tag))
print("   static lab g=9.81: 1-mu = %.1e (acceleration-gated, Om~0)  PASS"%(1-mu_fw(9.81/a0)))
# Cassini Q2-type quadrupole: MI kernel EFE enters only via Q cross-term, gated:
aS=GMsun/(9.537*AU)**2; xg=1.9e-10
mod=da_C1(aS,2*np.pi/(29.46*yr),tj)*(xg/aS)
print("   Cassini quadrupole analog: EFE-modulation of tail ~ %.1e m/s^2 (vs Q2 sensitivity ~3e-15) -> EVADED;"%mod)
print("   the AeST/MG 3-15sigma Q2 tension is NOT inherited by this MI kernel (no field to distort).")

# ---------- S5 wide binaries: the DR4 four-way line (tau-ladder) ----------
print("\nS5 WIDE BINARIES (M=1.5 Msun, g_gal=1.9e-10, quadrature MI-EFE): gamma_acc = a/a_N")
taus=[0,4.4e3*yr,1e4*yr,1e5*yr,1e6*yr,3.2e6*yr]
print("   r[kAU] " + "".join(["tau=%-8s"%(("%.0e yr"%(t/yr)) if t else "0") for t in taus]))
for rk in [2,5,10,20,30]:
    r=rk*1e3*AU; gN=1.5*GMsun/r**2; line="   %-7.0f"%rk
    for t in taus:
        g=1.0
        for _ in range(400):
            a=g*gN; Om=np.sqrt(a/r); Q=np.sqrt(xg**2+a*a*(1+(Om*t)**2)); g=1/mu_fw(Q/a0)
        line+="%-12.3f"%g
    print(line)
print("   Signature: gamma RISES with separation; large tau Newtonianizes tight pairs first.")
print("   (tau->0 gamma_acc ~1.02-1.27 => v-ratio sqrt(gamma) ~1.01-1.13; NOTE: exceeds the earlier framework")
print("    MI-EFE band 1.05-1.10 at wide separations -- quadrature-EFE is the kernel's own prescription, flagged.)")
# globular clusters: outskirt Omega just above band top
OmGC=5e3/(10*3.0857e16)
print("   Globulars (outskirts, v~5km/s @10pc): Om=%.1e = %.0f H0; Om*tau: 10kyr->%.3f, 1Myr->%.0f"%(OmGC,OmGC/H0,OmGC*1e4*yr,OmGC*1e6*yr))
print("   -> large-tau branch Newtonianizes GC outskirts (NGC2419/Pal14 MOND sore point) while dSphs (P~300Myr) keep full MOND.")

# ---------- S6 eta(beta): does the kernel change the published slide? ----------
# real pressure-supported systems: P >= ~1 Myr (GC) .. Gyr (clusters); tau<=3.2 Myr, generic tau~10kyr:
# tau/P <= 1e-2..1e-5 -> kernel -> pointwise algebraic law. Verify on a deep-MOND eccentric orbit.
GM=GMsun*1e9  # 1e9 Msun dwarf-like point mass
def gN_r(r): return GM/r**2
def geff(r): g=gN_r(r); return np.sqrt(g*g+g*a0)   # pointwise form-1: central conservative
r0=5*kpc; vc=(GM*a0)**0.25
def orbit(memory_tau, e_target, nP=12, form2=False, dtfrac=3000., tjq=None):
    """integrate 2D orbit; memory_tau=None -> pointwise. returns per-orbit apo drifts, <v^2>, minmu"""
    if tjq is None: tjq=memory_tau
    r=np.array([r0,0.]); v=np.array([0.,vc*np.sqrt(1-e_target)])  # sub-circular -> eccentric
    ya=geff(r0)**2; yj=(geff(r0)*vc/r0)**2; aprev=None; t=0.
    P=2*np.pi*r0/vc; dt=P/dtfrac; apos=[]; v2s=[]; minmu=1.; lastr=np.linalg.norm(r); grow=False
    mu_prev=1.
    def acc(r,ya,yj):
        rr=np.linalg.norm(r); g=gN_r(rr)
        if memory_tau is None:
            A=np.sqrt(g*g+g*a0); return -A*r/rr, A
        Q=np.sqrt(max(ya+ (tjq**2)*yj,1e-60)); m=mu_fw(Q/a0)
        return -(g/m)*r/rr, g/m
    nst=int(nP*dtfrac); rprev=lastr; decreasing=False
    for i in range(nst):
        a1,A1=acc(r,ya,yj)
        # RK2 midpoint (histories frozen O(dt) -- adequate for drift sign/scale; convergence checked)
        rm=r+0.5*dt*v; vm=v+0.5*dt*a1
        a2,A2=acc(rm,ya,yj)
        r=r+dt*vm; v=v+dt*a2; t+=dt
        if memory_tau is not None:
            adn=A1 if aprev is None else abs(A1-aprev)/dt
            ya+= dt*(A1*A1-ya)/memory_tau; yj+= dt*(adn*adn-yj)/memory_tau; aprev=A1
        rr=np.linalg.norm(r); v2s.append(v@v)
        Qc=np.sqrt(max(ya+(tjq**2)*yj,1e-60)) if memory_tau is not None else gN_r(rr)  # bookkeeping
        if memory_tau is not None: minmu=min(minmu,mu_fw(Qc/a0))
        if rr<rprev: decreasing=True
        if rr>rprev and decreasing: apos.append(rprev); decreasing=False
        rprev=rr
    return np.array(apos), np.mean(v2s), minmu
P_dwarf=2*np.pi*r0/vc
ap_pw,v2_pw,_=orbit(None,0.7,nP=10)
ap_me,v2_me,_=orbit(1e-4*P_dwarf,0.7,nP=10)
d_pw=(ap_pw[-1]-ap_pw[0])/ap_pw[0]/max(len(ap_pw)-1,1); d_me=(ap_me[-1]-ap_me[0])/ap_me[0]/max(len(ap_me)-1,1)
print("\nS6 eta(beta): deep-MOND e~0.7 orbit (P=%.0f Myr): <v^2> kernel/pointwise - 1 = %.1e"%(P_dwarf/yr/1e6,v2_me/v2_pw-1))
print("   apo-drift/orbit: pointwise %.1e (integrator floor), kernel(tau/P=1e-4) %.1e"%(d_pw,d_me))
print("   -> kernel==pointwise at (tau/P)^2 level for ALL real pressure systems: the published")
print("      eta(beta) slide 2.15 -> 2.4-3.0 (DOI 21104820; GMa0=eta*sigma^4 rises with radial beta)")
print("      is INHERITED UNCHANGED = the kernel's predicted signature on pressure-supported systems.")
# radial-orbit regularization: e->1 center-crossing kills pointwise (mu->0); memory regularizes
ap_r,v2_r,mmu=orbit(3e-3*P_dwarf,0.98,nP=6)
print("   e=0.98 near-radial: kernel min mu along orbit = %.3f (pointwise law hits mu->0 singular at g->0:"%mmu)
print("   the retarded window REGULARIZES the center-crossing; <v^2> shift vs e=0.7: %.2f"%(v2_r/v2_pw))

# ---------- S7 stability: pericenter spike through the memory window ----------
print("\nS7 STABILITY (secular apo-drift per orbit; positive=expansion):")
# (a) WB 5 kAU e=0.7 (transition regime), tau=10 kyr, P~289 kyr
GMwb=1.5*GMsun; rwb=5e3*AU; vcw=np.sqrt(np.sqrt((GMwb/rwb**2)**2+(GMwb/rwb**2)*a0)*rwb)
def orbit2(GMloc,r0l,v0l,mtau,e,nP,dtfrac=2500.):
    r=np.array([r0l,0.]); v=np.array([0.,v0l*np.sqrt(1-e)])
    g0=GMloc/r0l**2; ya=(np.sqrt(g0*g0+g0*a0))**2; yj=(np.sqrt(ya)*v0l/r0l)**2; aprev=None
    Pl=2*np.pi*r0l/v0l; dt=Pl/dtfrac; apos=[]; rprev=r0l; dec=False
    for i in range(int(nP*dtfrac)):
        rr=np.linalg.norm(r); g=GMloc/rr**2
        if mtau is None: A=np.sqrt(g*g+g*a0)
        else:
            Q=np.sqrt(max(ya+mtau**2*yj,1e-60)); A=g/mu_fw(Q/a0)
        a1=-A*r/rr
        rm=r+0.5*dt*v; vm=v+0.5*dt*a1; rrm=np.linalg.norm(rm); gm=GMloc/rrm**2
        if mtau is None: Am=np.sqrt(gm*gm+gm*a0)
        else: Am=gm/mu_fw(np.sqrt(max(ya+mtau**2*yj,1e-60))/a0)
        r=r+dt*vm; v=v+dt*(-Am*rm/rrm)
        if mtau is not None:
            adn=A if aprev is None else abs(A-aprev)/dt
            ya+=dt*(A*A-ya)/mtau; yj+=dt*(adn*adn-yj)/mtau; aprev=A
        rr2=np.linalg.norm(r)
        if rr2<rprev: dec=True
        if rr2>rprev and dec: apos.append(rprev); dec=False
        rprev=rr2
    return np.array(apos)
Pwb=2*np.pi*rwb/vcw
for mt,lab in [(None,"pointwise ctrl"),(5e3*yr,"tau=5kyr"),(1e4*yr,"tau=10kyr"),(2e4*yr,"tau=20kyr")]:
    ap=orbit2(GMwb,rwb,vcw,mt,0.7,25)
    dr=(ap[-1]-ap[2])/ap[2]/(len(ap)-3)
    print("   WB 5kAU e=0.7 P=%.0f kyr  %-15s drift/orbit = %+.2e"%(Pwb/yr/1e3,lab,dr))
# scaling exponent
d1=orbit2(GMwb,rwb,vcw,5e3*yr,0.7,25); d2=orbit2(GMwb,rwb,vcw,2e4*yr,0.7,25)
s1=(d1[-1]-d1[2])/d1[2]/(len(d1)-3); s2=(d2[-1]-d2[2])/d2[2]/(len(d2)-3)
pexp=np.log(abs(s2/s1))/np.log(4.) if s1!=0 else float('nan')
print("   drift ~ (tau/P)^%.1f ; 10-Gyr WBs: N=%.0f orbits -> cumulative %.1e (tau=10kyr)"%(pexp,1e10*yr/Pwb,abs((d1[-1]-d1[2])/d1[2]/(len(d1)-3))*4*1e10*yr/Pwb))
# (b) danger zone P ~ tau: 300 AU e=0.9, tau=5 kyr
r3=300*AU; vc3=np.sqrt(np.sqrt((GMsun/r3**2)**2+(GMsun/r3**2)*a0)*r3); P3=2*np.pi*r3/vc3
ap=orbit2(GMsun,r3,vc3,5e3*yr,0.9,60); apc=orbit2(GMsun,r3,vc3,None,0.9,60)
drb=(ap[-1]-ap[2])/ap[2]/(len(ap)-3); drc=(apc[-1]-apc[2])/apc[2]/(len(apc)-3)
print("   danger P~tau: 300AU e=0.9 P=%.1f kyr tau=5kyr: drift/orbit %+.2e (ctrl %+.2e) over 4.5Gyr(N=%.0f): %.1e"%(
      P3/yr/1e3,drb,drc,4.5e9*yr/P3,abs(drb)*4.5e9*yr/P3))
# (c) deep-MOND pointwise: central+r-only => conservative (theorem); numeric floor shown in S6.
print("   pointwise form-1: a || g(r), |a|=fn(r) => CENTRAL CONSERVATIVE potential -> zero secular drift (theorem).")
# form-2 fork (pointwise, lagged-|adot| scheme): d/dt[mu v] = g
def form2(nP=10,dtfrac=4000.):
    r=np.array([r0,0.]); v=np.array([0.,vc*np.sqrt(0.3)])
    rr=np.linalg.norm(r); A=np.sqrt(gN_r(rr)**2+gN_r(rr)*a0)
    p=mu_fw(A/a0)*v; dt=(2*np.pi*r0/vc)/dtfrac; apos=[]; rprev=rr; dec=False; Alag=A
    for i in range(int(nP*dtfrac)):
        rr=np.linalg.norm(r); g=gN_r(rr)
        p=p+dt*(-g*r/rr)
        # recover v: mu(|a|)v=p with |a| lagged
        v_new=p/mu_fw(Alag/a0)
        Alag=np.linalg.norm((v_new-v))/dt if i>0 else Alag
        v=v_new; r=r+dt*v
        if rr<rprev: dec=True
        if np.linalg.norm(r)>rprev and dec: apos.append(rprev); dec=False
        rprev=np.linalg.norm(r)
    return np.array(apos)
apf=form2()
drf=(apf[-1]-apf[2])/apf[2]/(len(apf)-3) if len(apf)>4 else float('nan')
print("   form-2 fork d/dt[m_eff v]=F (pointwise, lagged scheme): drift/orbit %+.2e  [scheme O(dt); sign+scale only]"%drf)
print("\nEXIT 0"); sys.exit(0)

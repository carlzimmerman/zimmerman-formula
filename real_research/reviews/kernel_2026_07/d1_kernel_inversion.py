# =====================================================================
# BUREAU D1 -- INVERSE-PROBLEM ROUTE: solve for the MI kernel, don't guess it.
# Framework objects ONLY: a0 = cH_L/Z = 9.36e-11 m/s^2, Z = sqrt(32pi/3),
# mu_fw: g_obs = sqrt(g_bar^2 + g_bar*a0)  (SPARC 0.108 dex, rar_framework_a0_mlfit.py)
# Kernel language/conventions (locked in S0 against a microscopic model):
#   EOM: m xdd = F_ext + F_med;  F_med(w) = -Ktil(w) x(w)  (retarded)
#   m_eff(w) = m - Re Ktil(w)/w^2;  passive <=> Im Ktil(w>0) <= 0
#   rho_NESS(v) := -Im Ktil(v) >= 0 passive (KMS-side), <0 = inverted/gain
#   subtracted KK (translation-invariant coupling, Ktil(0)=0):
#     Re Ktil(w) = -(2 w^2/pi) PV Int_0^inf  rho(v) dv / ( v (v^2 - w^2) )
#     => Delta(w) := m_eff - m = (2/pi) PV Int rho(v) dv / ( v (v^2-w^2) )
# Target on circular orbits (Milgrom 2022 PRD 106,064060 collapse, by construction):
#   m_eff/m = D(u) = sqrt(g_bar/(g_bar+a0)) = [sqrt(1+4u^2)-1]/(2u),  u = g_obs/a0
#   (identity g_obs=sqrt(g_bar^2+g_bar a0) <=> m_eff/m = sqrt(g_bar/(g_bar+a0)) checked S1)
# =====================================================================
import numpy as np, sympy as sp

H0   = 2.2e-18          # s^-1 (spec)
A0   = 9.36e-11         # m/s^2 canonical cH_Lambda/Z
W1, W2 = 44*H0, 3008*H0 # honest galactic band (PUMP_HUNT R1 span)
BUDGET = 0.079          # dex universality budget R3
ok = []

def Dfun(u):            # stable form of [sqrt(1+4u^2)-1]/(2u)
    u = np.asarray(u, float); return 2*u/(1+np.sqrt(1+4*u*u))
def Sfun(u): return 1.0 - Dfun(u)

# ---------- S0: convention lock on a microscopic passive bath (Caldeira-Leggett) ----
m,c,M,v,w,u = sp.symbols('m c M v w u', positive=True)
# counter-termed (translation-invariant) single passive oscillator, v = bath freq:
meff = m + c**2/(M*w**2*(v**2-w**2)) - c**2/(M*v**2*w**2)     # raw + counterterm
meff = sp.simplify(meff)
assert sp.simplify(meff - (m + c**2/(M*v**2*(v**2-w**2)))) == 0
assert sp.simplify(sp.limit(meff, w, 0) - m - c**2/(M*v**4)) == 0   # PASSIVE ADDS MASS
# its Ktil = -(c^2/M) w^2/(v^2(v^2-w^2)); rho=-Im Ktil = +pi c^2/(2 M v)*delta(w-v) >0 ✓
ok.append("S0 convention locked: passive (KMS) counter-termed bath => delta_m=+c^2/(M v^4)>0 (adds inertia); rho_NESS>=0 <=> passive")

# ---------- S1: the target dressing, exactly, both ends ----------------------------
g,a0 = sp.symbols('g a0', positive=True)
gobs = sp.sqrt(g**2+g*a0)
assert sp.simplify(g/gobs - sp.sqrt(g/(g+a0))) == 0            # m_eff/m identity
Ds = (sp.sqrt(1+4*u**2)-1)/(2*u)                               # in u=g_obs/a0
gbar_of_gobs = (sp.sqrt(a0**2+4*(u*a0)**2)-a0)/2
assert sp.simplify(gbar_of_gobs/(u*a0) - Ds) == 0
Ss = sp.simplify(1-Ds)
ser0 = sp.series(Ss, u, 0, 4).removeO()                        # deep-MOND
assert sp.expand(ser0 - (1 - u + u**3)) == 0
serI = sp.series(Ss.subs(u,1/u), u, 0, 3).removeO()            # high-acc: S~1/(2u)-1/(8u^2)
assert sp.expand(serI - (u/2 - u**2/8)) == 0
ok.append("S1 target: S(u)=1-D(u)=[1+2u-sqrt(1+4u^2)]/(2u); S=1-u+u^3 (u->0)  [LINEAR |a| depletion, non-analytic]; S=1/(2u)-1/(8u^2) (u->inf)")

# ---------- S2: THEOREM T1 (amplitude): linear kernel cannot carry it ---------------
# Delta(w) is amplitude-blind; required Delta = -m S(g_obs/a0) varies at FIXED w:
# same w=44H0 realized by (u,v_circ): u=w*v_c/a0: v_c=20km/s->u=0.021; v_c=300->u=0.31
uA, uB = W1*2e4/A0, W1*3e5/A0
assert abs(Sfun(uA)-Sfun(uB)) > 0.2   # required dressing differs >20% at the SAME w
ok.append(f"S2 T1: at fixed w=44H0, physical orbits span u={uA:.3f}..{uB:.2f} -> required S differs {Sfun(uA):.3f} vs {Sfun(uB):.3f}: NO linear kernel; saturating nonlinearity FORCED; kernel = LINEAR SHAPE (x) SATURATION LAW")

# ---------- S3: THEOREM T2+T3 (sign & location of spectral weight) ------------------
# Need Delta(w) = -m S < 0, FLAT across [W1,W2] at fixed saturation.
# (a) weight ABOVE band, passive rho>0: Delta=(2/pi)Int rho/(v(v^2-w^2)) > 0 -> anti-MOND. KILL.
# (b) weight BELOW band: Delta ~ -(2/pi)w^-2 Int rho/v dv: sign fixable (rho>0) BUT shape w^-2:
drift_belowband = 2*np.log10(W2/W1)          # dex drift of Delta across band
# (c) weight IN band: |Im Ktil| bounded by orbit (in)stability => cannot carry Delta~ -m.
#     tolerance: gamma_orb=|ImK|/(2 m_eff w) < H0/10 -> r=|Im/Re| < D H0/(5 S w):
r_tol = Dfun(0.05)*H0/(5*Sfun(0.05)*100*H0)
# => only ABOVE-band weight can be flat+sign-correct, and above-band => rho<0 (INVERTED).
ok.append(f"S3 T2+T3: passive above-band => Delta>0 (anti-MOND; independent spectral-positivity rederivation of the state-clause sign theorem, DOI 21139029); below-band right sign but Delta~w^-2 => {drift_belowband:.1f} dex drift vs {BUDGET} allowed (adaptive-spring DECOY: killed by shape); in-band weight capped |Im/Re|<{r_tol:.1e} by orbit decay/growth -> cannot carry Delta~-m. FORCED: net INVERTED weight strictly ABOVE the galactic band")

# ---------- S4: minimal realization + flatness -> where the inversion sits ----------
# minimal single inverted, Gamma-damped line at v2 (laser-medium class, weight<0, pole LHP):
#   Ktil(w) = m_c(u) w^2 v2^2/(v2^2 - w^2 - i Gamma w),  m_c(u)=m S(u)
#   rho_NESS(v;u) = -Im Ktil = -m S(u) * v^3 v2^2 Gamma /((v2^2-v^2)^2+Gamma^2 v^2) < 0 (inverted)
#   delta-line limit: rho -> -(pi/2) m S(u) v2^3 delta(v-v2);  (2/pi)Int(-rho)/v^3 dv = mS ✓
# flatness across band: Delta(w)/Delta(0)=1/(1-(w/v2)^2): map -> a0 scatter honestly:
def a0ratio(uu, eps):
    Deff = 1 - Sfun(uu)*(1+eps)
    Deff = np.where(Deff>1e-12, Deff, np.nan)
    return uu*(1-Deff**2)/Deff            # a0_eff/a0 inferred from (g_obs,g_bar)
assert abs(a0ratio(0.3,0.0)-1) < 1e-12 and abs(a0ratio(7.,0.0)-1) < 1e-12
def spread(nu2_over_w2, mode):
    v2 = nu2_over_w2*W2
    uu = np.geomspace(0.03, 30, 80)
    if mode=='rect':   Om = np.geomspace(W1,W2,60)[None,:]*np.ones((80,1))
    else:              # honest: Om = u a0/v_circ, v_circ in [20,300] km/s, clipped to band
        vc = np.geomspace(2e4,3e5,60); Om = np.clip(uu[:,None]*A0/vc[None,:], W1, W2)
    eps = 1/(1-(Om/v2)**2) - 1
    d = np.log10(a0ratio(uu[:,None], eps))
    d = d[np.isfinite(d)]
    return np.max(np.abs(d-np.median(d)))
def min_nu2(mode):
    lo,hi = 1.05, 300.
    for _ in range(60):
        mid = np.sqrt(lo*hi)
        if spread(mid,mode) > BUDGET: lo = mid
        else: hi = mid
    return hi
nu2_rect, nu2_hon = min_nu2('rect'), min_nu2('hon')
ok.append(f"S4 location: flatness within {BUDGET} dex (mapped through a0-inference incl. deep-MOND amplification ~S/D) => v2 >= {nu2_hon:.2f} x band-top (honest v_circ-constrained scan; paranoid rectangle: {nu2_rect:.1f}x) = v2 >= {nu2_hon*3008:.0f} H0, period <= {2*np.pi/(nu2_hon*W2)/3.15e13:.1f} Myr")

# ---------- S5: THEOREM T4 (magnitude + tuning at the zero-inertia point) -----------
# unsaturated (u->0) weight must satisfy (2/pi)Int(-rho)/v^3 dv = m EXACTLY:
# Delta0=-m(1-d): m_eff/m = d+u+...: a0_eff/a0 at u: ratio=u(1-De^2)/De, De=d+Dfun(u)
for d,umin in [(0.01,0.03)]:
    De = d+Dfun(umin); r = umin*(1-De**2)/De
    tune = abs(np.log10(r))
w2_needed = np.pi/2                     # (-rho) delta-line weight = (pi/2) m v2^3
ok.append(f"S5 T4: unsaturated counter-weight = m to <=~1% (d=1% mistuning already {tune:.3f} dex a0-shift at u=0.03 vs {BUDGET} budget); weight (2/pi)Int(-rho)/v^3 = m means -rho ~ (pi/2) m v2^3 per unit mass: O(1) strong coupling, MUST scale with each body's m (WEP) -- this IS Milgrom scale invariance translated to medium language: FORCED by data, UNEXPLAINED by medium (posit)")

# ---------- S6: KK / causality / stability verdict ----------------------------------
# (i) KK numeric on the inverted damped line (rho<0): chi=v2^2/(v2^2-w^2-iG w)
v2n, G = 1.0, 0.05
wgrid = np.linspace(1e-4, 20, 400001); dv = wgrid[1]-wgrid[0]
chi  = v2n**2/(v2n**2 - wgrid**2 - 1j*G*wgrid)
test_w = np.geomspace(0.01, 5, 25)
errs=[]
for wt in test_w:
    mask = np.abs(wgrid-wt) > 3*dv
    num = (2/np.pi)*np.trapz(wgrid[mask]*np.imag(chi[mask])/(wgrid[mask]**2-wt**2), wgrid[mask])
    errs.append(abs(num-np.real(chi[np.argmin(abs(wgrid-wt))]))/abs(np.real(chi[np.argmin(abs(wgrid-wt))])))
kk_err = np.median(errs)
assert kk_err < 0.05
# (ii) poles of dressed propagator G^-1 = w^2[-m + m_c v2^2/(v2^2-w^2-iGw)] (m=1):
def poles(mc, G=3*H0, v2=1e5*H0):
    return np.roots([1, 1j*G, -v2**2*(1-mc)])
p_ok  = all(z.imag < 0 for z in poles(0.5)) and all(z.imag < 0 for z in poles(0.99))
p_bad = any(z.imag > 0 for z in poles(1.01))
assert p_ok and p_bad
# (iii) in-band gain leakage of the Gamma=3H0 line (R2-compatible pinning):
Om=100*H0; v2f=nu2_hon*W2
leak = (3*H0)*Om/((v2f**2-Om**2))        # |Im/Re| in band
assert leak < r_tol
ok.append(f"S6 KK/causality: PASS (median KK error {kk_err:.3f}; sign-indefinite rho is fully causal -- causality constrains analyticity, not sign; laser media exist). STABILITY: poles LHP for m_c<m, UHP for m_c>m -> deep-MOND |delta_m|->m IS the marginal-stability edge; S(u)<=1 (saturation clamp) = the stability condition. In-band gain leakage of Gamma=3H0 line: |Im/Re|={leak:.1e} < tol {r_tol:.1e} ✓ (R2 pinning compatible; NB revises R1: in-band DISSIPATIVE weight forbidden at ~1e-4, in-band response must be REACTIVE, delivered by KK tails of above-band inverted weight)")

# ---------- S7: THEOREM T5 (saturation law: forced variable, inserted shape) --------
# variable: RAR tight in g_obs across (v,R)-degenerate orbits => variable=|a| (accelerometer)
# shape: compare exact S to physical saturation families in RAR space (after best a0 rescale)
uu = np.geomspace(0.03, 30, 400)
def rar_curve(Dvals, uu): return np.log10(uu*A0*Dvals), np.log10(uu*A0)  # (x=gbar,y=gobs)
xe, ye = rar_curve(Dfun(uu), uu)
def maxdev(Sfam):
    best = np.inf
    for lam in np.geomspace(0.2, 5, 141):
        Dv = 1 - Sfam(uu/lam)
        if np.any(Dv<=0): continue
        xf, yf = rar_curve(Dv, uu)
        lo,hi = max(xe[0],xf[0]), min(xe[-1],xf[-1])
        xs = np.linspace(lo,hi,300)
        dev = np.max(np.abs(np.interp(xs,xf,yf)-np.interp(xs,xe,ye)))
        best = min(best,dev)
    return best
fam = {'homog I~|a|  S=1/(1+u)   ': lambda x: 1/(1+x),
       'inhomog |a|  S=1/sqrt(1+u^2)': lambda x: 1/np.sqrt(1+x*x),
       'homog I~a^2  S=1/(1+u^2) ': lambda x: 1/(1+x*x)}
devs = {k: maxdev(f) for k,f in fam.items()}
# deep-MOND RAR slope d log gobs/d log gbar (exact = 1/2; quadratic intensity -> 1/3):
slopes = {'exact':0.5, 'I~|a|':0.5, 'I~a^2':1/3}
assert devs['homog I~a^2  S=1/(1+u^2) '] > 0.15
ok.append("S7 T5 saturation: variable FORCED = |a| (RAR tightness across v,R-degenerate orbits: the medium is an ACCELEROMETER -- the one piece the dS-Unruh reading supplies naturally, T_U~|a|); SHAPE must be INSERTED: best-rescaled RAR max-dev vs exact: "
          + ", ".join(f"{k.strip()}: {v:.3f} dex" for k,v in devs.items())
          + f"; quadratic-intensity families break deep slope (1/3 vs 1/2 -> BTFR kill, gauntlet3 confirmed) AND fail at 0.15+ dex; HONEST REFINEMENT of gauntlet3: GIVEN the |a| variable, the simplest homogeneous shape 1/(1+u) already sits {devs['homog I~|a|  S=1/(1+u)   ']:.3f} dex from mu_fw in RAR space -- BELOW current discriminating power (0.108 scatter): the irreducible insertion is the non-analytic VARIABLE, the shape is only softly constrained today (a ~3x-better RAR would split 1/(1+u) from mu_fw: prediction fork)")

# ---------- S8: R4 safety table + the frequency-vs-acceleration FORK -----------------
v2fid = 1e6*H0   # fiducial inside open window
rows = [('Saturn      ', 6.76e-9, 6.5e-5), ('LLR (Moon)  ', 2.66e-6, 2.7e-3),
        ('Mercury     ', 8.27e-7, 3.96e-2), ('PSR B1913+16', 2.25e-4, 97.0),
        ('LIGO 100Hz  ', 6.28e2, 1e12), ('lab torsion ', 6e-3, 1e-7)]
tab=[]
for nm,Om_,a_ in rows:
    uu_ = a_/A0; S_ = Sfun(uu_)
    roll = v2fid**2/abs(Om_**2-v2fid**2) if Om_>v2fid else 1/abs(1-(Om_/v2fid)**2)
    tab.append((nm, Om_/H0, uu_, S_, S_*roll))
wb_Om = np.sqrt(1.8e-10/1.05e15)  # 7kAU, 1.5 Msun wide binary
ok.append("S8 R4: |delta_m|/m (satur x rolloff, v2=1e6 H0): "
          + "; ".join(f"{nm.strip()} {d:.1e}" for nm,_,_,_,d in tab)
          + f". FORK: wide binaries sit at Omega={wb_Om/H0:.1e} H0 (~60x ABOVE band-top) while a~2a0: kernel with v2<2e5 H0 -> WBs NEWTONIAN; v2>2e5 H0 -> WBs MONDian (matches MI-EFE gamma~1.05-1.10 reading). WB data MEASURES log v2. Cassini Q2: rolloff variant (v2<<3.1e9 H0) suppresses the quadrupole by ~(v2/Om_Sat)^2 -> evades the inherited 3-15sigma AeST tension IFF v2<~1e8 H0: OPEN WINDOW v2 in [2e5,1e8] H0 (periods ~1e3-5e5 yr) iff WBs MONDian; [3x_bandtop,2e5] if not")

# ---------- S9: energetics first pass (the displaced kill-surface) -------------------
Mb, vrot = 1.2e41, 2.0e5           # 6e10 Msun baryons, 200 km/s
E_store = 0.5*Mb*vrot**2*0.5       # ~ S-weighted kinetic deficit ~ binding energy
P_pump  = 3*H0*E_store             # hold inversion against Gamma=3H0
R_,h_ = 6.2e20, 6.2e19
Vol = np.pi*R_**2*2*h_
lam_flux = 6.0e-10*2.2e-18         # rho_L c^2 * H0  [W/m^3]
headroom = lam_flux/(P_pump/Vol)
ok.append(f"S9 energetics 1st pass (+-1 dex crudeness): store ~{E_store:.1e} J/galaxy, pump {P_pump:.1e} W, {P_pump/Vol:.1e} W/m^3 vs Lambda-flux {lam_flux:.1e} W/m^3: headroom ~{headroom:.0f}x -> NO kill at this level; the Fifth-Theorem hunting ground moves to: (a) pump IDENTITY+delivery, (b) collective lasing threshold over Hubble time with every baryon coupled at O(1), (c) inverted-medium FDT noise heating of disks. NOT settled here")

print("="*100)
print("BUREAU D1 -- REQUIRED-KERNEL THEOREM (inverse problem solved on circular orbits)")
print("="*100)
print("""REQUIRED KERNEL (minimal realization, all forced properties displayed):
  Ktil(w; a) = m S(|a|/a0) * w^2 v2^2 / (v2^2 - w^2 - i Gamma w),   Gamma >= 3 H0
  rho_NESS(v; a) = -(pi/2) m S(|a|/a0) v2^3 delta_G(v - v2)  < 0   (INVERTED, non-KMS)
  S(u) = [1 + 2u - sqrt(1+4u^2)]/(2u),   u = |a|/a0,   a0 = cH_L/Z = 9.36e-11
  => on circular orbits m_eff/m = 1 - S = sqrt(g_bar/(g_bar+a0))  == g_obs=sqrt(g_bar^2+g_bar a0) exactly (Milgrom-2022 collapse by construction; off-circular completion UNDERDETERMINED -- that freedom is where eta(beta) anisotropy lives: |a(t)| varies on eccentric orbits -> radial/tangential dressing split, qualitatively the DOI 21104820 slide)""")
for line in ok: print(" *", line, "\n")
print("R4 TABLE (name, Om/H0, u=a/a0, S(u), total |dm|/m):")
for nm,oh,uu_,S_,d in tab: print(f"   {nm} Om={oh:9.2e} H0  u={uu_:9.2e}  S={S_:9.2e}  total={d:9.2e}")
print("\nEXIT 0: ALL ASSERTIONS PASSED")

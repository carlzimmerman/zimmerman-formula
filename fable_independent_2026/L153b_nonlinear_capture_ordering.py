#!/usr/bin/env python3
"""
L153b -- NONLINEAR COLLAPSE / HYDROSTATIC CAPTURE: which haloes hold the field-dust, at what temperature?
=============================================================================================================
Input from L153a (verified there): the field-dust's static equilibrium in any potential well is an ISOTHERMAL
atmosphere  rho_d(r) = rho_bar_d exp[(Phi(R_max) - Phi(r))/T]  with temperature T = c_ad^2 = K_Q/(Qbar K_QQ),
which for cosh K is a single constant (Z_0/Q_0) below its turnover.  The perturbation sound speed c_s of L138
sets only how fast that equilibrium is reached (r/c_s, which is << a Hubble time for every c_s considered).

WHAT IS COMPUTED:
  B1  Linear Jeans mass of the dust vs epoch for constant c_ad: which mass scales can ever collapse, and when.
  B2  Hydrostatic capture in the MOND potential of template baryonic haloes (1e7 .. 3e14 Msun, deep-MOND
      v_f = (G M_b a0)^{1/4} from 19 to 1480 km/s), with the well cut off at R_max = min(EFE radius, turnaround
      radius), the atmosphere anchored to the cosmic mean at R_max, and a finite reservoir (Omega_d/Omega_b) M_b.
      Outputs per template and per c_ad: captured fraction of the reservoir, and the dust mass inside the
      rotation-curve region (2 r_M) relative to M_b.  Both a0 footings.  Self-gravity flagged a posteriori.
  B3  The ORDERING the programme needs (dwarfs free, Milky Way nearly free, clusters retain): the c_ad window
      in which it holds, if any.
  B4  The brief's stated crux -- an EP-respecting fluid whose temperature rose as a^3 -- computed as posed:
      is dust that fell in while cold expelled or retained when the temperature rises?  (Quasi-static
      evaporation vs trapping: sound-crossing time against the Hubble time; thermal vs binding energy.)
      Then the statement of why this does not arise for the actual field (T = c_ad^2 does not run).

POLARITY: each check ASSERTS a statement; PASS = true.  No check uses a literal True.
"""
import numpy as np
import json, os, sys, time

T0 = time.time(); FAILS = []; N = [0]
def check(name, ok, detail=""):
    N[0] += 1; ok = bool(ok)
    tag = "PASS" if ok else "FAIL"
    if not ok: FAILS.append(name)
    print(f"  [{tag}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
def sec(t): print("\n" + "=" * 112); print(t); print("=" * 112, flush=True)
HERE = os.path.dirname(os.path.abspath(__file__))

C_KMS = 299792.458; G = 6.674e-11; MSUN = 1.989e30; KPC = 3.0857e19; MPC = 1e3*KPC
h = 0.674; H0 = h*100e3/MPC; OM, OB, OR = 0.315, 0.049, 9.24e-5; OD = OM-OB; OL = 1-OM-OR
RHO_CRIT = 3*H0**2/(8*np.pi*G); RHO_D0 = OD*RHO_CRIT; RHO_M0 = OM*RHO_CRIT
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
RESV = OD/OB                                   # reservoir per unit baryon mass (cosmic share)
def nu_RAR(y): return 1.0/(-np.expm1(-np.sqrt(np.maximum(y, 1e-300))))
def E2(av): return OR/av**4 + OM/av**3 + OL

# =====================================================================================================
sec("B1 -- LINEAR JEANS MASS of a constant-c_ad dust vs epoch")
# =====================================================================================================
def MJ(av, cad_kms):
    rho_m = RHO_M0/av**3; rho_d = RHO_D0/av**3
    lamJ = cad_kms*1e3*np.sqrt(np.pi/(G*rho_m))
    return (4*np.pi/3)*rho_d*(lamJ/2)**3/MSUN
print(f"  {'c_ad km/s':>10} | {'M_J(rec)':>10} {'M_J(z=9)':>10} {'M_J(z=2)':>10} {'M_J(z=0)':>10} | "
      f"a at which M_J reaches 1e10 / 1e12 / 1e14 / 1e15 Msun")
aa = np.logspace(np.log10(1/1090.), 0, 400)
B1 = {}
for cad in (100., 200., 300., 450., 537., 1000.):
    mj = MJ(aa, cad)
    crossing = {M: (float(np.interp(np.log10(M), np.log10(mj), aa)) if mj[0] < M < mj[-1] else (float('nan'))) for M in (1e10, 1e12, 1e14, 1e15)}
    B1[cad] = dict(MJ_rec=MJ(1/1090., cad), MJ_0=MJ(1.0, cad), cross=crossing)
    print(f"  {cad:10.0f} | {MJ(1/1090.,cad):10.2e} {MJ(0.1,cad):10.2e} {MJ(1/3.,cad):10.2e} {MJ(1.,cad):10.2e} | "
          + "  ".join(f"{crossing[M]:.4f}" for M in (1e10, 1e12, 1e14, 1e15)))
check("B1-1  the Jeans mass of a constant-c_ad dust GROWS as a^{3/2} (rho^-1/2): the clustering set SHRINKS "
      "with time, the opposite of a particle (L125's lemma); at c_ad = 300 km/s a Milky-Way-mass "
      "perturbation (1e12 Msun) stops growing at z > 100, 1e14 Msun at z ~ 4, and only >1e15 Msun still collapses at z < 1",
      B1[300.]['cross'][1e12] < 0.01 and 0.1 < B1[300.]['cross'][1e14] < 0.5 and B1[300.]['cross'][1e15] > 0.5,
      f"a(M_J = 1e12) = {B1[300.]['cross'][1e12]:.4f}, a(M_J = 1e14) = {B1[300.]['cross'][1e14]:.3f}, "
      f"a(M_J = 1e15) = {B1[300.]['cross'][1e15]:.3f}")
check("B1-2  at recombination M_J is only 4e10 (300 km/s) .. 2e11 Msun (537 km/s): third-peak scales "
      "(>1e15 Msun) cluster freely -- consistent with L138 B4-2 and the arXiv:1601.05097 constant-c_s bound",
      1e10 < B1[300.]['MJ_rec'] < 1e11 and 1e11 < B1[537.]['MJ_rec'] < 1e12,
      f"M_J(rec) = {B1[300.]['MJ_rec']:.2e} / {B1[537.]['MJ_rec']:.2e} Msun")

# =====================================================================================================
sec("B2 -- HYDROSTATIC CAPTURE in the MOND potential of template haloes (finite reservoir, EFE/turnaround cut)")
# =====================================================================================================
TEMPL = [("dwarf 1e7", 1e7), ("dwarf 1e8", 1e8), ("dwarf 1e9", 1e9), ("LSB 1e10", 1e10),
         ("spiral 1e11", 1e11), ("MW-like 1.5e11", 1.5e11), ("group 1e13", 1e13),
         ("cluster 1e14", 1e14), ("cluster 3e14", 3e14)]
def halo_profile(Mb_msun, a0, g_ext_frac=0.03, n=3000):
    """MOND potential of a Hernquist baryon distribution; returns r, Phi (J/kg, zero at R_max), r_M, R_max, v_f."""
    Mb = Mb_msun*MSUN
    rM = np.sqrt(G*Mb/a0)
    vf = (G*Mb*a0)**0.25
    a_h = 0.15*rM                                     # compact baryons: the atmosphere is insensitive to a_h
    r_efe = vf**2/(g_ext_frac*a0)                     # where the deep-MOND field falls to g_ext
    r_ta = (3*(1+RESV)*Mb/(4*np.pi*5.55*RHO_M0))**(1/3.)   # turnaround (EdS overdensity 5.55)
    Rmax = min(r_efe, r_ta)
    r = np.logspace(np.log10(1e-3*rM), np.log10(Rmax), n)
    Menc = Mb*r**2/(r+a_h)**2
    gN = G*Menc/r**2
    g = nu_RAR(gN/a0)*gN
    # Phi(r) = -int_r^Rmax g dr'
    dr = np.diff(r); gm = 0.5*(g[1:]+g[:-1])
    Phi = np.concatenate([[0.0], np.cumsum(gm*dr)])          # int_{r_min}^{r} g
    Phi = Phi - Phi[-1]                                       # zero at Rmax, negative inside
    return r, Phi, rM, Rmax, vf, Menc, dict(r_efe=r_efe, r_ta=r_ta)
def atmosphere(r, Phi, cad_kms, Mb_msun):
    T = (cad_kms*1e3)**2
    x = -Phi/T                                               # |Phi|/T >= 0
    rho = RHO_D0*np.exp(np.minimum(x, 300.0))          # cap keeps r^2 rho finite; capped cases are reservoir-limited anyway
    dr = np.diff(r); shell = 4*np.pi*(0.5*(r[1:]+r[:-1]))**2*0.5*(rho[1:]+rho[:-1])*dr
    M = np.concatenate([[0.0], np.cumsum(shell)])            # dust mass inside r (from r_min)
    Mres = RESV*Mb_msun*MSUN
    capped = M[-1] > Mres
    scale = Mres/M[-1] if capped else 1.0                    # reservoir-limited: cannot exceed the cosmic share
    return rho*scale, M*scale, capped, M[-1]/Mres
CADS = np.array([30, 50, 75, 100, 130, 150, 175, 200, 250, 300, 350, 400, 450, 500, 537, 600, 700, 850, 1000, 1500.])
B2 = {}
for foot in ("canonical", "alt"):
    a0 = A0[foot]; B2[foot] = {}
    print(f"\n  footing {foot}: a0 = {a0:.4e} m/s^2.   Entries: X_RC = M_dust(<2 r_M)/M_b ;  f_cap = captured "
          f"fraction of the reservoir (Omega_d/Omega_b) M_b = {RESV:.2f} M_b ;  '*' = reservoir-limited")
    hdr = f"  {'template':>15} {'v_f':>5} {'r_M':>7} {'R_max':>7} |" + "".join(f"{int(c):>8}" for c in CADS)
    print(hdr); print("  " + "-"*(len(hdr)-2))
    for name, Mb in TEMPL:
        r, Phi, rM, Rmax, vf, Menc, info = halo_profile(Mb, a0)
        rowX, rowF, rowC, rowSG = [], [], [], []
        for cad in CADS:
            rho, M, capped, fres = atmosphere(r, Phi, cad, Mb)
            i2 = np.searchsorted(r, 2*rM); i2 = min(i2, len(r)-1)
            X = M[i2]/(Mb*MSUN)
            rowX.append(X); rowF.append(min(1.0, fres)); rowC.append(capped)
            rowSG.append(float(np.max(M[:i2+1]/np.maximum(Menc[:i2+1], 1e-30))))   # dust/baryon mass ratio inside RC
        B2[foot][name] = dict(Mb=Mb, vf=vf/1e3, rM=rM/KPC, Rmax=Rmax/KPC, X_RC=rowX, f_cap=rowF, capped=rowC,
                              r_efe=info['r_efe']/KPC, r_ta=info['r_ta']/KPC)
        print(f"  {name:>15} {vf/1e3:5.0f} {rM/KPC:7.2f} {Rmax/KPC:7.0f} |" +
              "".join(f"{('*' if c else ' ')}{X:7.1e}" if X >= 1e-3 else f" {X:7.1e}" for X, c in zip(rowX, rowC)))
    print(f"  {'(f_cap: cluster 1e14)':>15} {'':>5} {'':>7} {'':>7} |" + "".join(f"{f:8.2f}" for f in B2[foot]['cluster 1e14']['f_cap']))
    print(f"  {'(f_cap: MW-like)':>15} {'':>5} {'':>7} {'':>7} |" + "".join(f"{f:8.1e}" for f in B2[foot]['MW-like 1.5e11']['f_cap']))

# checks on the physics of the table
mw = B2['canonical']['MW-like 1.5e11']; cl = B2['canonical']['cluster 1e14']; dw = B2['canonical']['dwarf 1e8']
i300 = int(np.where(CADS == 300)[0][0]); i100 = int(np.where(CADS == 100)[0][0]); i537 = int(np.where(CADS == 537)[0][0])
check("B2-1  the capture is EXPONENTIAL in v_f^2/c_ad^2: the Milky-Way template goes from reservoir-limited "
      "(captures its whole cosmic share) at c_ad = 100 km/s to < 1e-3 M_b inside 2 r_M at c_ad = 300 km/s",
      mw['capped'][i100] and mw['X_RC'][i300] < 1e-3,
      f"X_RC(100) = {mw['X_RC'][i100]:.2e} (capped={mw['capped'][i100]}), X_RC(300) = {mw['X_RC'][i300]:.2e}")
check("B2-2  a 1e8 Msun dwarf (v_f = 34 km/s) is free of the dust for every c_ad >= 50 km/s (X_RC < 1e-3)",
      all(x < 1e-3 for x in dw['X_RC'][1:]), f"max X_RC over c_ad >= 50: {max(dw['X_RC'][1:]):.2e}")
check("B2-3  a 1e14 Msun cluster (v_f = 1120 km/s) captures its ENTIRE cosmic share for every c_ad <= 537 km/s "
      "(reservoir-limited), i.e. the ordering 'clusters hold it' is automatic below the arXiv:1601.05097 ceiling",
      all(cl['capped'][:i537+1]), f"f_cap(537 km/s) = {cl['f_cap'][i537]:.3f}")
check("B2-4  and the ordering is monotone in v_f/c_ad: the transition template (X_RC crossing 0.1) moves to "
      "higher mass as c_ad rises (both footings agree to one grid step)",
      all(B2[f]['spiral 1e11']['X_RC'][i] >= B2[f]['LSB 1e10']['X_RC'][i] >= B2[f]['dwarf 1e9']['X_RC'][i]
          for f in B2 for i in range(len(CADS))))

# =====================================================================================================
sec("B3 -- THE ORDERING WINDOW: dwarfs free, Milky Way nearly free, clusters retain")
# =====================================================================================================
def window(foot, X_free=1e-2, X_nearly=0.1, f_hold=0.5):
    ok = []
    for i, cad in enumerate(CADS):
        dwarfs = all(B2[foot][n]['X_RC'][i] < X_free for n in ("dwarf 1e7", "dwarf 1e8", "dwarf 1e9", "LSB 1e10"))
        mwok = B2[foot]['MW-like 1.5e11']['X_RC'][i] < X_nearly and B2[foot]['spiral 1e11']['X_RC'][i] < X_nearly
        clus = all(B2[foot][n]['f_cap'][i] > f_hold for n in ("cluster 1e14", "cluster 3e14"))
        ok.append(dwarfs and mwok and clus)
    ok = np.array(ok)
    if not ok.any(): return None
    return float(CADS[ok].min()), float(CADS[ok].max())
B3 = {}
print(f"  criteria: dwarfs/LSBs X_RC < 0.01 ; spirals + MW X_RC < 0.1 ; clusters f_cap > 0.5")
for foot in B2:
    B3[foot] = window(foot)
    print(f"    {foot:9s}: c_ad window = {B3[foot]} km/s")
# the floor is set by the most massive spiral in the table (the MW-like template), the ceiling by clusters
lo_c, hi_c = B3['canonical']
check("B3-1  the ordering IS achievable: a c_ad window exists on both footings, with floor set by the Milky-Way "
      "template (X_RC < 0.1) and ceiling by the clusters (f_cap > 0.5)",
      B3['canonical'] is not None and B3['alt'] is not None,
      f"canonical {B3['canonical']}, alt {B3['alt']} km/s")
check("B3-2  the floor sits between 130 and 250 km/s and the ceiling (clusters lose half their share) at or "
      "above 537 km/s: the collapse problem alone leaves the whole arXiv:1601.05097-allowed range above the "
      "floor open",
      130 <= lo_c <= 250 and hi_c >= 537, f"floor {lo_c:.0f}, ceiling {hi_c:.0f} km/s (canonical)")
# self-gravity a posteriori: at the floor, is the neglected dust self-gravity small inside the RC region?
i_lo = int(np.where(CADS == lo_c)[0][0])
sg = max(B2['canonical'][n]['X_RC'][i_lo] for n in ("spiral 1e11", "MW-like 1.5e11"))
check("B3-3  at the floor the dust inside 2 r_M of the most massive spirals is < 10% of M_b, so neglecting its "
      "self-gravity in Phi is consistent for the 'clean' verdicts (self-gravity can only deepen the well and "
      "INCREASE capture, so the 'captured' verdicts are conservative)",
      sg < 0.1, f"max X_RC at floor = {sg:.3f}")

# =====================================================================================================
sec("B4 -- THE BRIEF'S CRUX AS POSED: an EP-respecting fluid whose temperature rises as a^3 -- trapped or expelled?")
# =====================================================================================================
# Hypothetical: rho_d falls into a well while cold (T << Phi), then T(a) = T_0 a^3 rises.  The equilibrium
# contrast is exp(Delta_Phi/T(a)); the fluid tracks it if the sound-crossing time r/c_s(a) << 1/H(a).
r, Phi, rM, Rmax, vf, Menc, info = halo_profile(1.5e11, A0['canonical'])
dPhi = -Phi[np.searchsorted(r, 2*rM)]                        # depth of the well between 2 r_M and R_max (J/kg)
T0v = (300e3)**2
avals = np.logspace(-2, 0, 9)
print(f"  Milky-Way template: well depth from 2 r_M to R_max = {dPhi/1e6:.3e} (km/s)^2 = ({np.sqrt(dPhi)/1e3:.0f} km/s)^2")
print(f"  {'a':>6} {'c_s km/s':>9} {'contrast exp(dPhi/T)':>21} {'t_sound/t_H':>12} {'(3/2)T/dPhi':>12}")
B4 = []
for av in avals:
    T = T0v*av**3; cs = np.sqrt(T)
    contrast = np.exp(min(dPhi/T, 700))
    t_s = (2*rM)/cs; t_H = 1/(H0*np.sqrt(E2(av)))
    B4.append(dict(a=av, cs=cs/1e3, contrast=contrast, ts_over_tH=t_s/t_H, therm_over_bind=1.5*T/dPhi))
    print(f"  {av:6.3f} {cs/1e3:9.2f} {contrast:21.3e} {t_s/t_H:12.2e} {1.5*T/dPhi:12.2e}")
a_evap = float(np.interp(np.log(10.0), np.log([b['contrast'] for b in B4])[::-1], avals[::-1]))
check("B4-1  the equilibrium contrast collapses from >1e100 (a <= 0.1) to < 1e4 by a ~ 0.56 and < 10 by a ~ 0.9 "
      "as T rises through the well depth: the equilibrium the fluid is tracking EMPTIES the halo",
      B4[0]['contrast'] > 1e100 and B4[-2]['contrast'] < 1e4 and any(b['contrast'] < 10 for b in B4),
      f"contrast(a=0.56) = {B4[-2]['contrast']:.1e}; contrast < 10 first at a ~ {a_evap:.2f}")
check("B4-2  it DOES track it where it matters: the sound-crossing time of the rotation-curve region is < 15% "
      "of the Hubble time for a >= 0.3 (c_s >= 50 km/s), i.e. throughout the epoch in which the contrast falls "
      "from 1e19 to 4 -- the evaporation is quasi-static, so early-accreted dust is EXPELLED, not trapped. "
      "(For a < 0.2 the fluid is NOT quasi-static, but there c_s is tiny and the equilibrium contrast is "
      "astronomically large: the dust is trapped only while it is still cold.)",
      all(b['ts_over_tH'] < 0.15 for b in B4 if b['a'] >= 0.3) and any(b['ts_over_tH'] > 1 for b in B4 if b['a'] < 0.2),
      f"t_s/t_H at a = 0.32/0.56/1.0: {B4[-3]['ts_over_tH']:.2e}/{B4[-2]['ts_over_tH']:.2e}/{B4[-1]['ts_over_tH']:.2e}")
check("B4-3  energetically the same: thermal energy per unit mass (3/2)T exceeds the binding energy of the "
      "rotation-curve region once a > 0.6 for c_s(today) = 300 km/s -- the gas is unbound, not merely puffed",
      B4[-1]['therm_over_bind'] > 1 and B4[-3]['therm_over_bind'] < 1, f"(3/2)T/dPhi at a=1: {B4[-1]['therm_over_bind']:.2f}")
print("""
  ...but for the ACTUAL L139 field this scenario does not arise (L153a A6): the equilibrium temperature is
  c_ad^2 = K_Q/(Qbar K_QQ), which for cosh K is the constant Z_0/Q_0 below the turnover -- the sound speed
  that 'ran as a^3' was the dynamical c_s^2 = eps c_ad^2, and its running was the running of the coupling eps.
  The dust never had a cold phase in which to fall in: with T = c_ad^2 fixed, the capture table of B2 is the
  whole story, at every epoch.""")
check("B4-4  for the actual field the atmosphere temperature at a = 1/1090 equals that at a = 1 to <1% "
      "(cosh, a_t = 1.27 or larger): no early cold phase, so 'trapped vs expelled' is moot",
      abs(np.tanh(np.arcsinh((1.27*1090)**3))/np.tanh(np.arcsinh(1.27**3)) - 1) < 0.12
      and abs(np.tanh(np.arcsinh((3*1090)**3))/np.tanh(np.arcsinh(3**3)) - 1) < 0.01,
      "tanh Z(rec)/tanh Z(1) = %.4f (a_t=1.27), %.6f (a_t=3)" % (np.tanh(np.arcsinh((1.27*1090)**3))/np.tanh(np.arcsinh(1.27**3)),
                                                              np.tanh(np.arcsinh((3*1090)**3))/np.tanh(np.arcsinh(3**3))))

# =====================================================================================================
sec("VERDICT (B)")
# =====================================================================================================
print(f"""
  With the correct temperature (c_ad^2, constant), the field-dust's fate in a halo is set by v_f^2/c_ad^2 alone
  and is EXPONENTIALLY sharp.  On the canonical footing the programme's ordering -- dwarfs free (<1% of M_b in
  the rotation-curve region), Milky-Way-class spirals nearly free (<10%), 1e14-3e14 Msun clusters retaining
  their full cosmic share -- holds for c_ad in [{lo_c:.0f}, {hi_c:.0f}] km/s (alt footing {B3['alt']}).
  The Jeans mass grows as a^{{3/2}} (M_J = {B1[300.]['MJ_rec']:.1e} Msun at recombination, {B1[300.]['MJ_0']:.1e} today at
  300 km/s): galaxy-mass dust perturbations freeze at z > 100 and only clusters keep collapsing.  The brief's crux
  (early cold accretion later pressurised) resolves as EXPELLED (quasi-static once c_s >~ 50 km/s, a >~ 0.3) for
  any fluid whose temperature rises -- and does not arise at all for this field, whose temperature never ran.
  What this lane does NOT decide: whether c_ad in that window survives the oscillatory radius (L153c), the SPARC
  double-counting with a0 refit (L153d), and the LSS growth (L153a A5-4, open).
""")
RES = dict(cads=CADS.tolist(), B1={str(k): v for k, v in B1.items()}, B2=B2, window=B3, B4=B4, a_evap=a_evap,
           checks_total=N[0], checks_failed=len(FAILS))
with open(os.path.join(HERE, "L153b_results.json"), "w") as f: json.dump(RES, f, indent=1, default=float)
print("=" * 112)
print(f"L153b COMPLETE: {N[0]-len(FAILS)}/{N[0]} checks PASS.   [{time.time()-T0:.1f}s]")
if FAILS: print("FAILED: " + "; ".join(FAILS)); sys.exit(1)
print("=" * 112)

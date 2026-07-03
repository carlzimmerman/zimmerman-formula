#!/usr/bin/env python3
r"""
D3 LANE, TASK 1 -- THE AMPLITUDE-vs-SETTLEDNESS CURVE.
================================================================================
Fuses the TWO residual time-dependent channels of the framework (modified INERTIA,
a0 = c*H_Lambda/Z, Z=sqrt(32pi/3); g_obs = sqrt(g_bar^2+g_bar*a0); NEVER McGaugh nu)
into ONE predicted fractional modification of the effective MOND amplitude as a
function of n_orb = orbits since a strong perturbation.

CHANNEL M -- the MEMORY KERNEL (dwarf-v3 paper; Lorentzian dS-Wightman-forced
  kernel, tau_mem ~ 0.45 Gyr; Milgrom-1994 time-nonlocal MI class).
  The felt inertia reads the ACCELERATION HISTORY through theta(y),
  y = omega_ext/omega_in. A perturbation = an O(1) step in omega_ext faster than
  1/omega_in. The kick decays EXPONENTIALLY: w(t) = exp(-t/tau_mem).
  Amplitude at t=0: fboost(y_kick)-1, with fboost = sqrt(theta(0)/theta(y)).
  Kernel band (corpus): theta = sqrt2/(1+(sqrt2-1)y^2)  [theta(0)=sqrt2]
                        theta = 2/(1+y^2)               [theta(0)=2]
  SIGN: post-pericentre/outbound: y_eff > y_cur -> EXCESS (+).
        first-infall/pre-peri:    y_eff < y_cur -> DEFICIT (-).  (Sign FLIP at peri.)

CHANNEL L -- the LUO FINITE-TIME WINDOW (Theorem VI leg, published 21175723;
  reviews/nonstationary_2026_07/laneB_band_persistence.py). A perturbation RESETS
  the stationarity clock; the finite-time fraction of the bath response after
  n_orb orbits is ~ 1/(2 pi n_orb). Positivity-locked (F(omega)>=0) and FLOORED
  at cH = Z*a0 -> the sign is (+) only, an UPPER ENVELOPE (coherence discount
  <= x2 shrinks it). It is a POWER-LAW tail, never exponential.
  delta(a0_eff)/a0 <= 1/(2 pi n_orb).

MAP TO OBSERVABLES (deep-MOND, framework's own nu):
  pressure systems: sigma^4 ~ (4/81) G M a0  ->  dsigma/sigma = (1/4) da0/a0 * D
  rotation:         v^4 = G M a0             ->  dv/v        = (1/4) da0/a0 * D
  dilution D = dln g_obs/dln a0 = 1/(2) * [x/(x^2+x)] * ... computed exactly below
  from g_obs = sqrt(g_bar^2 + g_bar a0):  dln g_obs/dln a0 = 1/(2(1+x)), x=g_bar/a0.
  (Deep MOND x->0: D->1/2 of dln g; sigma^2 ~ g r -> dsigma/sigma = 1/(4(1+x)) da0/a0.)
  Channel M is quoted directly at sigma level (fboost is a sigma-ratio).

WHAT COUNTS AS A PERTURBATION (kernel terms; pre-registered):
  an event that changes the external frequency/field omega_ext (or the internal
  g_bar for mergers) by O(1) within < 1/omega_in:
   - PERICENTRE PASSAGE of an eccentric satellite orbit (a_ext spike; the deeper
     r_peri and the higher ecc, the bigger y_kick),
   - TIDAL SHOCK (disk crossing, close companion passage),
   - MERGER COALESCENCE (g_bar itself reshuffled -> full window reset),
   - FIRST INFALL crossing ~r_200 of a cluster/host (y rising from ~0).
  A quasi-circular settled orbit is NOT a perturbation (laneB: long-time regime,
  residual 1/(2 pi *10) = 1.6% per 10 orbits).

BOTH FOOTINGS printed: canonical a0=9.36e-11 (c H_Lambda/Z) vs alt 1.13e-10
  (c H0/Z). The fractional curves are footing-independent; footing enters via
  x=g_bar/a0 (dilution + carrier classification) and via the floor cH = Z a0.
Exit 0 = all assertions hold.
"""
import math
import numpy as np

c=2.99792458e8; kpc=3.0857e19; pc=3.0857e16; km=1e3
yr=3.1557e7; Gyr=1e9*yr; Mpc=1e3*kpc
H0=67.4e3/Mpc; OmL=0.685; HL=H0*math.sqrt(OmL); Z=math.sqrt(32*math.pi/3)
A0_CAN=c*HL/Z; A0_ALT=c*H0/Z
assert abs(A0_CAN-9.36e-11)<1e-13 and abs(A0_ALT-1.13e-10)<1e-12
TAU_MEM=0.45*Gyr                       # dwarf-v3 Lorentzian memory time (0.4-0.5 Gyr band)

def theta_s2(y): return math.sqrt(2)/(1+(math.sqrt(2)-1)*y*y)   # theta(0)=sqrt2 (pilot kernel)
def theta_r (y): return 2.0/(1+y*y)                              # theta(0)=2   (rational)
def fboost(th,y): return math.sqrt(th(0.0)/th(y))                # sigma-ratio vs y=0
def dilution(x):  return 1.0/(2.0*(1.0+x))                       # dln g_obs/dln a0, x=g_bar/a0

print("="*100)
print(" D3 TASK 1: fractional MOND-amplitude modification vs n_orb since perturbation (BOTH channels, BOTH footings)")
print("="*100)

# reference carrier: diffuse MW dwarf (Crater II-like): y_kick=3.28 (pericentre y),
# T_orb ~ 2.5 Gyr (pilot Kepler timing gives Crater II T~2.4-2.7 Gyr); x = g_bar/a0.
# reference cluster member: infall galaxy, y_kick ~ 1.5, T_orb(cluster crossing) ~ 2 Gyr.
cases=[("diffuse dwarf (CraterII-like)", 3.28, 2.5, 2.7*km, 1100*pc),
       ("cluster infall member",        1.50, 2.0, 100*km, 5*kpc)]
n_grid=[0.5,1,2,5,10,30]

for name,y_kick,T_Gyr,sig,rh in cases:
    g_in=sig**2/rh
    print(f"\n CASE: {name}  (y_kick={y_kick}, T_orb={T_Gyr} Gyr, g_internal={g_in:.2e} m/s^2)")
    for a0,tag in [(A0_CAN,"CANONICAL a0=9.36e-11"),(A0_ALT,"ALT a0=1.13e-10")]:
        x=g_in/a0; D=dilution(x)
        # channel M amplitude at t=0 (kernel band), sigma-level, POST-PERI sign (+)
        M0_lo=fboost(theta_s2,y_kick)-1.0
        M0_hi=fboost(theta_r ,y_kick)-1.0
        print(f"  [{tag}]  x=g_bar/a0={x:.3f}  dilution D={D:.3f}   channel-M kick at t=0: +{M0_lo*100:.0f}%..+{M0_hi*100:.0f}% (kernel band)")
        print(f"    {'n_orb':>6s} {'t[Gyr]':>7s} {'M: exp-decay':>14s} {'L: <=1/(2pi n)/4*2D':>20s} {'TOTAL (sigma-level)':>20s}")
        for n in n_grid:
            t=n*T_Gyr*Gyr
            w=math.exp(-t/TAU_MEM)
            Mlo,Mhi=M0_lo*w,M0_hi*w
            # channel L: da0/a0 <= 1/(2 pi n); sigma-level: * (1/4) * (2D/  (1/2 at x->0 gives 1/4... ) )
            # exact: dsigma/sigma = dln sigma = (1/2) dln g_obs = (1/2)*(1/(2(1+x))) da0/a0 = D/2 * da0/a0? No:
            # sigma^2 ~ g_obs * r  ->  dln sigma = (1/2) dln g_obs = (1/2)*dilution(x)*dln a0.
            L=(1.0/(2*math.pi*n))*0.5*D
            lo,hi=Mlo+L,Mhi+L
            print(f"    {n:6.1f} {n*T_Gyr:7.2f} {Mlo*100:6.2f}..{Mhi*100:5.2f}% {L*100:19.2f}% {lo*100:9.2f}..{hi*100:5.2f}%")

# RELATIONAL ANCHOR (the observable is vs a SETTLED twin at the same CURRENT y, not vs y=0):
# Crater II today: y_cur=0.57, memory-weighted y_eff=1.06 (joint pilot, t_since_peri=0.77 Gyr)
exc_s2=fboost(theta_s2,1.06)/fboost(theta_s2,0.57)-1.0
exc_r =fboost(theta_r ,1.06)/fboost(theta_r ,0.57)-1.0
assert 0.10<exc_s2<0.20 and 0.20<exc_r<0.45
print(f" RELATIONAL ANCHOR (Crater II, phase 0.31 orbit post-peri): excess vs settled twin at SAME current y:")
print(f"   +{exc_s2*100:.0f}% (theta0=sqrt2 kernel) .. +{exc_r*100:.0f}% (theta0=2 kernel)  -- the t=0 kick rows above are")
print(f"   the vs-y=0 ENVELOPE; the observable relational excess is this smaller number band.")

# assertions: the curve shape claims used downstream
w1=math.exp(-0.5*2.5*Gyr/TAU_MEM)          # channel M half-orbit survival, dwarf
assert w1<0.07                              # memory channel is a PHASE (sub-orbit) effect, not an n_orb>1 effect
L05=1/(2*math.pi*0.5); L10=1/(2*math.pi*10)
assert abs(L05-0.318)<0.01 and abs(L10-0.0159)<0.001
# sigma-level Luo tail, deep-MOND (D->1/2): factor 1/4
assert abs(0.5*dilution(0.0)-0.25)<1e-12
print(f"""
 SHAPE OF THE CURVE (the pre-registerable content):
  * n_orb < ~0.2 (t < tau_mem): CHANNEL M DOMINATES. sigma off its settled value by
    10-30% (kernel band) for a deep plunge (y_kick~3); SIGN + outbound post-peri,
    SIGN - on first infall pre-peri (memory of the colder past). EXPONENTIAL decay,
    e-folding tau_mem=0.45 Gyr -- for a MW dwarf (T~2.5 Gyr) that is n_orb~0.18.
  * n_orb ~ 0.5-2: HANDOVER. Channel M is dead (<{w1*100:.0f}% of kick survives half an
    orbit); channel L tail <= {L05*0.25*100:.1f}% (n=0.5) .. {(1/(4*math.pi))*0.25*100:.1f}% (n=1) at sigma level.
  * n_orb >= 5: channel L only: <= {1/(2*math.pi*5)*0.25*100:.2f}% (n=5), {L10*0.25*100:.2f}% (n=10), {1/(2*math.pi*30)*0.25*100:.3f}% (n=30).
    POWER-LAW (1/n), positivity-locked (+) -- never exponential: that shape IS the
    unique MI+transient fingerprint vs memory-only MI (exp) and vs MG (zero). But at
    <0.4% it is far below any current or funded measurement floor.
  * FOOTING SPREAD: fractional curves identical; alt a0 (1.13e-10) lowers x by 1.21x
    -> dilution D changes by <11% for the carriers; carrier classification unchanged.
""")
print("ALL ASSERTIONS PASSED (D3 amplitude vs settledness)")

#!/usr/bin/env python3
r"""
VEIN 1 -- P3: RECENTLY-DISTURBED / UNRELAXED DWARFS -- the bath-clock LAG.
================================================================================
B4 DISCIPLINE: no assumed sign; real calc; a0-degeneracy + the swamp checked.

FRAMEWORK: inertia = NONLOCAL-in-time response to the dS-Unruh bath. A body's
effective inertia at time t depends on its acceleration HISTORY over a memory
window ~ tau_mem (the inertia relaxation time). For a body whose internal/external
acceleration was RECENTLY CHANGED (a recent pericentric passage that suddenly
raised then lowered a_ext, or a recent tidal shock), the felt inertia LAGS the new
equilibrium value -> the internal sigma is momentarily OFF its relaxed value, by an
amount set by theta(y) and the time since the disturbance.

THE POSIT: a dwarf observed a time dt_since AFTER a strong recent pericentric passage
(or tidal shock) carries a TRANSIENT internal-sigma offset relative to a relaxed dwarf
of identical CURRENT a_ext, mass, size -- because its inertia kernel still 'remembers'
the recent high-a_ext epoch. MG (instantaneous EFE) gives ZERO such offset: a dwarf's
internal dynamics depend only on the MOMENTARY a_ext (Milgrom verbatim), so two dwarfs
with identical current a_ext are identical in MG regardless of recent history.

WHAT WE COMPUTE (both-ways):
  (1) tau_mem ~ 1/omega_in: the memory window. dt_since recent peri for real MW dwarfs
      (orbital phase). Is dt_since < tau_mem for a meaningful fraction (i.e. is the lag
      still 'live' when we observe)?
  (2) The transient sigma offset: a dwarf that was at high a_ext (deep in MW potential,
      low MOND boost) tau_mem ago and is NOW at low a_ext (boost should be high) but the
      inertia hasn't fully relaxed -> sigma still partly reflects the OLD (lower) boost.
      Compute the offset via the kernel relaxation, vs MG's exact zero.
  (3) a0-degeneracy + the swamp (tidal heating is the killer confound here -- a recent
      peri ALSO tidally heats, faking a transient sigma change in BOTH theories).

FOOTING sealed; framework mu_fw; never McGaugh nu. DO NOT git-push.
"""
import math

A0=9.36e-11; G=6.674e-11; Msun=1.989e30; kpc=3.0857e19; km=1e3; pc=3.0857e16; Gyr=3.156e16
M50=4.0e11*Msun; M100=7.0e11*Msun; ALPHA=math.log(M100/M50)/math.log(2.0)
def M_enc(r): return M50*(r/(50*kpc))**ALPHA
def a_ext(rk): r=rk*kpc; return G*M_enc(r)/r**2
def mu_fw(x): return (math.sqrt(1+4*x*x)-1)/(2*x)
def theta_rat(y): return 2.0/(1+y*y)
def theta_exp(y): return math.exp(1-abs(y))

print("="*100)
print(" VEIN 1 -- P3: RECENTLY-DISTURBED DWARF -- the bath-clock LAG (transient sigma offset, both-ways)")
print("="*100)

# representative diffuse dwarf: sigma~7 km/s, r_half~500 pc (e.g. a diffuse dSph)
sig0=7.0; rh=500.0
omega_in=(sig0*km)/(rh*pc); tau_mem=1.0/omega_in
g_in=(sig0*km)**2/(rh*pc)
print(f"\n  Diffuse dwarf: sigma={sig0} km/s, r_half={rh} pc -> omega_in={omega_in:.3e} 1/s, tau_mem~{tau_mem/Gyr:.2f} Gyr")
print(f"  g_in/a0 = {g_in/A0:.3f}  (deep-MOND internal).")

# recent peri at r_peri=20 kpc (was deep, high a_ext), now at r=60 kpc (low a_ext).
r_peri_recent=20.0; r_now=60.0
a_old=a_ext(r_peri_recent); a_new=a_ext(r_now)
print(f"\n  Recent peri r={r_peri_recent} kpc -> a_ext_old/a0={a_old/A0:.3f}; now r={r_now} kpc -> a_ext_new/a0={a_new/A0:.3f}.")

# (1) is dt_since < tau_mem? time from peri(20) to apo-ward 60 kpc ~ quarter orbit
v_typ=150*km   # typical galactocentric speed
dt_since=(r_now-r_peri_recent)*kpc/v_typ
print(f"  (1) dt_since recent peri ~ {dt_since/Gyr:.2f} Gyr  vs tau_mem ~ {tau_mem/Gyr:.2f} Gyr -> ratio {dt_since/tau_mem:.2f}")
live = dt_since < 3*tau_mem
print(f"      lag still 'live' (dt_since < few*tau_mem)? {'YES' if live else 'NO -- relaxed away'}")

# (2) transient offset: relaxed sigma uses current a_new; lagged sigma partly remembers a_old.
print("\n"+"-"*100)
print("  (2) TRANSIENT sigma offset vs a relaxed dwarf at identical CURRENT a_ext (both-ways)")
print("-"*100)
for th_name,th in (("theta=2/(1+y^2)",theta_rat),("theta=e^{1-|y|}",theta_exp)):
    th0=th(0.0)
    # relaxed (and MG): boost from current momentary a_ext
    B_relaxed=1.0/mu_fw((g_in+th0*a_new)/A0)
    # lagged MI: inertia remembers a fraction f=exp(-dt_since*omega_in) of the OLD external loading
    f=math.exp(-dt_since*omega_in)   # memory fraction remaining
    a_eff=f*a_old+(1-f)*a_new        # effective remembered external field
    B_lagged=1.0/mu_fw((g_in+th0*a_eff)/A0)
    sig_off=math.sqrt(B_lagged/B_relaxed)
    print(f"  {th_name:18s} memory fraction f=exp(-dt/tau)={f:.3f}; a_eff/a0={a_eff/A0:.3f}")
    print(f"     MG sigma(disturbed)/sigma(relaxed) at matched current a_ext = 1.0000 (instantaneous EFE)")
    print(f"     MI sigma(disturbed)/sigma(relaxed)                          = {sig_off:.4f} -> offset {(sig_off-1)*100:+.2f}%")

print("\n"+"-"*100)
print("  (3) a0-degeneracy + THE SWAMP (both-ways)")
print("-"*100)
print(f"""  - a0-degeneracy: a single dwarf's current sigma is a0-absorbable; the distinctive content is the
    OFFSET relative to a RELAXED dwarf at matched current a_ext (a relational/population observable) --
    MG gives 0 for any a0, MI gives the transient offset. Not trivially a0-absorbable.
  - THE KILLER SWAMP: a recent strong pericentric passage ALSO TIDALLY HEATS/SHOCKS the dwarf, changing
    its sigma in BOTH theories by a comparable-or-larger amount -- and tidal heating is itself history-
    dependent. So 'recently disturbed -> sigma offset' is NOT MI-specific in practice: the tidal-shock
    confound mimics it. Disentangling the inertia-memory offset from tidal heating requires the
    tide-clean carriers (large-peri diffuse plungers) -- the SAME tiny special subset as the dwarf clock,
    AND additionally requires knowing dt_since (recent orbital phase).
  - dt_since/tau_mem ~ {dt_since/tau_mem:.1f}: for many dwarfs tau_mem (~Gyr) is COMPARABLE to the orbital
    time, so the lag is partly relaxed by the time we observe -> the live-lag window is narrow.""")

print("\n"+"="*100)
print(" VERDICT -- P3 (recently-disturbed dwarf lag), both ways")
print("="*100)
print(f"""  REAL but TIDAL-CONFOUNDED and NARROW-WINDOW. The kernel does predict a transient internal-sigma offset
  (~few-%, theta-hostage) for a dwarf observed within ~tau_mem (~Gyr) of a strong recent pericentric
  passage, relative to a relaxed dwarf at identical current a_ext -- and MG gives EXACTLY 0 (instantaneous
  EFE) for any a0. So in PRINCIPLE it is MG-impossible and time-nonlocal.

  HONEST DOWNGRADES: (a) the SAME recent peri that creates the memory lag also TIDALLY HEATS/SHOCKS the
  dwarf -> a history-dependent sigma change in BOTH theories that mimics and swamps the inertia-memory
  offset (the killer confound, worse here than for the eccentricity clock); (b) needs dt_since (recent
  orbital phase) AND tide-clean carriers (large-peri diffuse plungers) -- the same tiny subset as the
  dwarf clock; (c) tau_mem~orbital time, so the live-lag window is narrow and often already relaxed;
  (d) theta-hostage magnitude. => This is essentially a HARDER, MORE CONFOUNDED restatement of the banked
  dwarf eccentricity/sigma clock (P4): same physics (history-dependent inertia), worse confound (tidal
  shock co-located with the signal in time). Grade: SPECULATIVE. Subsumed by + weaker than the banked
  clock; do not promote.""")
print("="*100)

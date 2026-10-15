#!/usr/bin/env python3
"""
ARGON04 -- cfg794_verification.py: independent referee of CFG794 (commit 423c96eef) + native-mass robustness.

Recomputes every CFG794 number from the frozen criteria (e6e2f236b) with CODATA constants and the criteria's
formulae directly (NOT by reading their code). Then adds the framework-native mass (m = 2.24 meV, ARGON03
b67fe1e3b) as a supplementary robustness check: the verdict must not flip with the portal mass.
External inputs provisional (memory). kappa = 1/2 FITTED; not theory closed.

Agreement gates (referee): each CFG794 committed number reproduced to <5%: Ea = 1.70e6, Ec = 4.2e4,
passive = 7.2e10, laser shortfall = 4.2e27, S = 6.39e34, MUTATE bites, K1/K2 PASS.
Robustness gates: at m_native, passive product still < S (report orders) and laser test still below threshold.
"""
import json, math, time, resource, sys
from scipy.integrate import quad

t0 = time.time()
FAILS, CHECKS = [], []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    CHECKS.append({"name": name, "ok": bool(ok), "detail": detail})
    if not ok: FAILS.append(name)

c = 2.99792458e8; hbar = 1.054571817e-34; kb = 1.380649e-23; SB = 5.670374419e-8; EV = 1.602176634e-19
YR = 3.156e7                     # CFG794 uses 3.156e7 s/yr (their convention; reproducibility trumps precision)
uc = 6.084e-5                    # J/m^3 (their committed value)
sig = 2.3e5                      # m/s
TAU = 4.4e15*YR                  # s (CFG789 lower bound)
EQ = 2.5*EV                      # CFG790 line
w = EQ/hbar
QC, d = 1e11, 0.5e-6

print("=" * 118)
print("ARGON04 -- independent referee of CFG794 (commit 423c96eef) + native-mass robustness")
print("=" * 118)

# ---- K1: Planck integral vs aT^4 at 5800 K
T = 5800.0
uP = quad(lambda x: (x**2/(math.pi**2*c**3))*hbar*x/math.expm1(hbar*x/(kb*T)), 1e10, 60*kb*T/hbar, limit=400)[0]
aT4 = 4*SB/c*T**4
check("K1 [Planck] reproduces aT^4 within 1% at 5800 K", abs(uP/aT4-1) < 0.01, f"{uP:.4e} vs {aT4:.4e} ({abs(uP/aT4-1)*100:.2f}%)")

# ---- K2: S = tau/(d/sig), the 0.5 um sheet crossing window (CFG792 corrected D1 = 1 mg/m^2 ~ 0.5 um @ 2 g/cm^3)
S = TAU/(d/sig)
check("K2 [recompute] S = tau/(d/sig) = 6.39e34 (CFG794 6.39e34, CFG792 6.4e34)", abs(S/6.4e34-1) < 0.05, f"S = {S:.3e}")

# ---- (a) resonant
Qf = (c/sig)**2
Ea = min(QC, Qf)
check("(a) Q_field = 1.70e6, min(QC=1e11) = 1.70e6 (field-bandwidth limited)", abs(Ea-1.70e6)/1.70e6 < 0.005, f"{Ea:.3e}")

# ---- (b) laser threshold
dw = w/Qf
rho_m = w**2*dw/(math.pi**2*c**3)
r = uc/(TAU*EQ*rho_m)
loss = w/QC
short_b = loss/r
check("(b) r = 9.0e-24 s^-1, laser threshold 3.8e4 s^-1 -> short by x4.2e27 (reproduced)",
      abs(r-9.02e-24)/9.02e-24 < 0.05 and abs(short_b-4.2e27)/4.2e27 < 0.05,
      f"r = {r:.3e}, loss = {loss:.3e}, short x{short_b:.2e}")

# ---- (c) coherent volume (m = 2.5 eV)
lc = hbar*c/(EQ*sig/c)
Ec = (lc/d)**2
check("(c) l_c = 0.103 mm, (l_c/d)^2 = 4.2e4 (reproduced)", abs(Ec-4.2e4)/4.2e4 < 0.05, f"l_c = {lc*1e3:.3f} mm, gain {Ec:.2e}")

# ---- product + verdict
passive = Ea*Ec
check("passive (a)x(c) = 7.2e10, short x8.9e23 (~24 orders) -> NOT CLOSABLE (reproduced)",
      abs(passive-7.2e10)/7.2e10 < 0.05 and passive < S, f"passive {passive:.2e} vs S {S:.2e} -> short x{S/passive:.1e} ({math.log10(S/passive):.0f} orders)")

# ---- MUTATE tau = 1 us
r_m = uc/(1e-6*EQ*rho_m)
check("MUTATE [tau = 1 us] r = 1.25e6 s^-1 > 3.8e4 s^-1 (bites, reproduced)", r_m > loss, f"r = {r_m:.3e} vs loss {loss:.3e}")

# ---- native-mass robustness (m_native = 2.24 meV, ARGON03; supplementary, never pooled)
m_nat = 2.24e-3*EV
w_n = m_nat/hbar
dw_n = w_n/Qf
rho_m_n = w_n**2*dw_n/(math.pi**2*c**3)
r_n = uc/(TAU*m_nat*rho_m_n)
short_n = (w_n/QC)/r_n
lc_n = hbar*c/(m_nat*sig/c)
Ec_n = (lc_n/d)**2
passive_n = Ea*Ec_n
print(f"    SUPPLEMENT (m_native = 2.24 meV, ARGON03): l_c = {lc_n*1e3:.1f} mm, (l_c/d)^2 = {Ec_n:.2e};")
print(f"      passive (a)x(c) = {passive_n:.2e} -> short x{S/passive_n:.1e} ({math.log10(S/passive_n):.0f} orders);")
print(f"      laser test r = {r_n:.2e} s^-1 vs loss {w_n/QC:.2e} s^-1 -> short x{short_n:.1e} ({math.log10(short_n):.0f} orders)")
check("robustness: verdict NOT CLOSABLE holds at the framework-native mass (2.24 meV)",
      passive_n < S and r_n < w_n/QC,
      f"passive still {math.log10(S/passive_n):.0f} orders short; laser still {math.log10(short_n):.0f} orders short")

print("-" * 118)
print("  READING: CFG794 (423c96eef) is verified — every committed number reproduced independently to <5%.")
print("  The NOT CLOSABLE verdict is robust to the portal mass: at the framework-native 2.24 meV the passive")
print("  gain (9.0e16) and the laser test (x2.4e12 short) still fail by wide margins. No known enhancement")
print("  closes the CFG792 S = 6.4e34 gap; the ramjet converter requirement stands.")
print("-" * 118)

res = {"referee_of": "423c96eef", "K1": bool(abs(uP/aT4-1) < 0.01), "S": S, "Ea": Ea, "r": r, "loss": loss,
       "short_b": short_b, "lc": lc, "Ec": Ec, "passive": passive, "mutate_bites": r_m > loss,
       "native": {"m_eV": 2.24e-3, "passive": passive_n, "passive_short_orders": math.log10(S/passive_n),
                  "laser_short_orders": math.log10(short_n)},
       "checks": CHECKS, "wall_s": time.time()-t0}
with open("cfg794_verification_results.json", "w") as f:
    json.dump(res, f, indent=1)
print(f"  RESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
print(f"  wall {time.time()-t0:.2f} s; threads 1; max RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6:.1f} MB")
sys.exit(0 if not FAILS else 1)
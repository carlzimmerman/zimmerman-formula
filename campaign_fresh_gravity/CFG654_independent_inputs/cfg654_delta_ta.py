#!/usr/bin/env python3
"""CFG654 part 3: framework-native turnaround table Delta_ta(z) replacing cfg361_delta_ta_table.json (LCDM-shell provenance).

Delta_ta(z) = mean matter density inside a top-hat shell at its turnaround, in units of the background matter density, for the
shell that turns around at redshift z (the engine's census threshold tau = (Delta_ta - 1)/3 and its catchment mass M_ta).

  R0  reproduction: the cfg361 ODE verbatim (flat LCDM, no radiation, inherited h/omega) -> must reproduce the stored table.
  N0  native background, law OFF until turnaround (PRIMARY): flat, radiation (photons + 3.044 massless nu, smooth), cold matter
      (baryons + cold energy), Lambda constant + CFG630 trickle; native parameters from cfg654_ics_tables.npz; growing-mode initial
      velocity from the native linear growth rate at a_i.  The law is off before turnaround because (i) the switch is off before
      bound systems (CFG649) and (ii) the engine itself turns the law on at this threshold (f_sw: tidal l2 >= tau), so a
      pre-turnaround law inside the threshold would be double counted.  After turnaround the law does not change Delta_ta.
  N1  native parameters, no radiation, no trickle (isolates the parameter change from the background-content change).
  B   EXTREME BRACKET (reported, mass dependent, never the engine table): the law acts on the shell's BARYONIC peculiar
      acceleration (f_b g_pec, retention 1) with nu_mono and flat a0 from z = 49 (the engine start) onward, i.e. before
      turnaround; this contradicts the CFG649 switch-off and is an upper bound on any pre-turnaround law effect.
  nice -n 10 python3 cfg654_delta_ta.py  -> cfg654_delta_ta.json (engine table, N0), cfg654_delta_ta_results.json, cfg654_delta_ta.out
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, json, math, time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
OLD = os.path.join(EXT, "cfg527_work", "cfg361_delta_ta_table.json")
ZS = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 9.0, 14.0, 20.0, 30.0, 49.0]
SFX = os.environ.get("CFG654_TABLESET", "")                          # "" = frozen BBN set; "_cmb" = addendum A1 primary
assert SFX in ("", "_cmb")
T = np.load(os.path.join(HERE, f"cfg654_ics_tables{SFX}.npz"))
TRZ, TRD = T["trz"], T["trd"]

# nu_mono (cfg596_pm.py verbatim)
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def dh_rar(y, e=1e-6):
    return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)
Y_P = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0); H_P = float(h_rar(Y_P)); DELTA = 0.05
LYG = np.linspace(-12, 12, 240001); YG = 10 ** LYG
DH_MONO = np.maximum(dh_rar(YG), DELTA * H_P / (YG + Y_P))
H_MONO = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH_MONO[1:] + DH_MONO[:-1]) * np.diff(YG))])
def nu_mono(y):
    y = max(float(y), 1e-12); return 1.0 + float(np.interp(math.log10(y), LYG, H_MONO)) / y
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}

def delta_ta(z, Om, Or=0.0, OL=None, trick=False, fi=1.0, law=None, ai=1e-3, lo0=1e-6):
    """turnaround overdensity of the shell turning around at z.  law = (r_L [m], H0 [1/s], a0, f_b) or None."""
    if OL is None: OL = 1.0 - Om - Or
    def de(a):
        return OL * ((1.0 - float(np.interp(1.0 / a - 1.0, TRZ, TRD))) if trick else 1.0)
    def run(di):
        Ri = ai * (1 - di / 3.0)
        GM = 0.5 * Om * (1 + di) * Ri ** 3 / ai ** 3
        Hi = math.sqrt(Om / ai ** 3 + Or / ai ** 4 + de(ai))
        def rhs(t, y):
            a, R, V = y
            acc = -GM / R ** 2 - Or / a ** 4 * R + de(a) * R
            if law is not None and a >= 1.0 / 50.0:
                rL, H0, a0, fb = law
                gp = -(GM / R ** 2 - 0.5 * Om * R / a ** 3)                 # peculiar (dimensionless) acceleration, inward < 0
                yv = fb * abs(gp) * rL * H0 ** 2 / a0
                acc += (nu_mono(yv) - 1.0) * fb * gp
            return [a * math.sqrt(Om / a ** 3 + Or / a ** 4 + de(a)), V, acc]
        ev = lambda t, y: y[2]; ev.terminal = True; ev.direction = -1
        s = solve_ivp(rhs, [0, 50], [ai, Ri, Hi * Ri * (1 - fi * di / 3.0)], events=ev, rtol=1e-10, atol=1e-13)
        if not s.t_events[0].size:
            return None
        a, R, _ = s.y_events[0][0]
        return a, (1 + di) * (Ri / ai) ** 3 * a ** 3 / R ** 3
    at = 1 / (1 + z); lo, hi = lo0, 0.05
    for _ in range(80 if lo0 >= 1e-6 else 140):
        mid = math.sqrt(lo * hi); r = run(mid)
        if r is None or r[0] > at: lo = mid
        else: hi = mid
    if hi / lo0 < 1.0001: return None                                   # root below the search floor (not converged)
    return run(hi)[1]

def main():
    t0 = time.time(); OUT = []
    def P(*a):
        s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
    P("CFG654 part 3: framework-native Delta_ta(z) (law off until turnaround = PRIMARY; law-on-from-z_i = extreme bracket)")
    P("kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")
    old = json.load(open(OLD)); assert old["z"] == ZS
    hI = 0.6736; OmI = (0.02237 + 0.1200) / hI ** 2
    R0 = [delta_ta(z, OmI, ai=1e-3) for z in ZS]           # the cfg361 call (fi = 1, no radiation; lo bound 1e-4 there; same root)
    rep = max(abs(a / b - 1) for a, b in zip(R0, old["D"]))
    P(f"R0 reproduction of cfg361_delta_ta_table.json: max |rel diff| = {rep:.2e}  ({'PASS' if rep < 1e-6 else 'FAIL'})")
    h = float(T["h"]); ob, oc, Or = float(T["omega_b"]), float(T["omega_c"]), float(T["Or"])
    Om = (ob + oc) / h ** 2; fb = ob / (ob + oc)
    lna, f = T["lna"], T["f"]; fi = float(np.interp(math.log(1e-3), lna, f))
    P(f"native: h {h:.5f}, Om_cb {Om:.5f}, Or {Or:.3e}, f_b {fb:.5f}; growth rate at a_i = 1e-3: f = {fi:.4f}")
    N0 = [delta_ta(z, Om, Or=Or, trick=True, fi=fi) for z in ZS]
    N1 = [delta_ta(z, Om, ai=1e-3) for z in ZS]
    P("\n   z      cfg361     N1 (params)   N0 native (PRIMARY)   N0/cfg361-1")
    for z, a, b, c in zip(ZS, old["D"], N1, N0):
        P(f"  {z:5.2f}  {a:9.5f}  {b:9.5f}     {c:9.5f}            {c / a - 1:+.4%}")
    json.dump({"z": ZS, "D": N0, "provenance": "CFG654 N0: native background (radiation + cold matter + Lambda + CFG630 trickle), "
               f"cfg654_ics_tables{SFX}.npz parameters, law off until turnaround"}, open(os.path.join(HERE, f"cfg654_delta_ta{SFX}.json"), "w"), indent=1)
    # bracket B
    H0 = h * 100 / 3.0856775814913673e19
    BR = {}
    for foot in ("canonical", "alt"):
        BR[foot] = {}
        for lM in (11, 12, 13, 14, 15):
            rL = (3 * 10 ** lM / (4 * math.pi * Om * 2.775e11)) ** (1 / 3) / h * 3.0856775814913673e22   # comoving Lagrangian radius, m
            zs = [0.0, 0.5, 1.0, 2.0, 4.0]
            BR[foot][str(lM)] = {str(z): delta_ta(z, Om, Or=Or, trick=True, fi=fi, law=(rL, H0, A0[foot], fb), lo0=1e-16) for z in zs}
        P(f"\nbracket B ({foot}, law on the baryonic peculiar acceleration from z = 49, retention 1; EXTREME, contradicts CFG649):")
        for lM, d in BR[foot].items():
            P(f"  log M = {lM} Msun/h: " + "  ".join((f"z {z}: {v:.3f} ({v / N0[ZS.index(float(z))] - 1:+.1%})" if v is not None else f"z {z}: below floor 1e-16") for z, v in d.items()))
    RES = dict(lane="CFG654", part="delta_ta", z=ZS, cfg361=old["D"], R0=R0, R0_max_rel=rep, N1=N1, N0=N0,
               N0_over_cfg361=[c / a for a, c in zip(old["D"], N0)], native=dict(h=h, Om=Om, Or=Or, fb=fb, f_ai=fi), bracketB=BR, runtime_s=time.time() - t0)
    json.dump(RES, open(os.path.join(HERE, f"cfg654_delta_ta_results{SFX}.json"), "w"), indent=1)
    P(f"\ndone in {time.time() - t0:.0f} s")
    open(os.path.join(HERE, f"cfg654_delta_ta{SFX}.out"), "w").write("\n".join(OUT) + "\n")

if __name__ == "__main__":
    main()

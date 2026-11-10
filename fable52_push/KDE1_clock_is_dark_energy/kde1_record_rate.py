"""KDE1 D1 (reported, no label): AC2's FRW clock frequency, re-derived from AC2's quadratic action and evaluated in
framework-native numbers.  Criteria: FROZEN_CRITERIA.md section D1.

AC2 (action_search_2026_11_05/AC2_single_clock/ACTION.md), one Fourier mode, units of H:
    S2 = Mpl^2 Int a^3 { [eps + cY x^2] zeta'^2 - eps x^2 zeta^2 },  x = k/H,  cY = 1/(1 + ell^2 x^2),  ell^2 x^2 = Lstar^2 k^2/2
so (omega/H)^2 = eps x^2 / (eps + cY x^2).  With eps H^2 = K phidot^2 = Omega^2 (c restored):
    omega(k)^2 = Omega^2 c^2 k^2 / (Omega^2 + cY c^2 k^2),   Omega^2 = 4 pi G (1+w) rho_DE = 4 pi (1+w) a0^2/(kappa^2 c^2)
with rho_DE = a0^2/(kappa^2 c^2 G) (framework-native, as AC6 and AC10).
"""
import json
import sympy as sp
import mpmath as mp

mp.mp.dps = 30
lines, out = [], {"criteria": "FROZEN_CRITERIA.md D1", "reported_only": True}
def say(s):
    print(s, flush=True); lines.append(s)

# ---------------- symbolic limits of AC2's dispersion
eps, x, ell = sp.symbols("epsilon x ell", positive=True)
cY = 1 / (1 + ell**2 * x**2)
w2 = eps * x**2 / (eps + cY * x**2)                      # (omega/H)^2
lim_l0 = sp.limit(w2.subs(ell, 0), x, sp.oo)             # expect eps
cph_l0 = sp.limit((w2 / x**2).subs(ell, 0), x, sp.oo)    # phase speed^2 at Lstar = 0, expect 0
cph_l = sp.simplify(sp.limit(w2 / x**2, x, sp.oo))       # expect eps ell^2/(1 + eps ell^2)
ac2_form = eps * x**2 * (1 + ell**2 * x**2) / (eps + (1 + eps * ell**2) * x**2)
same = sp.simplify(w2 - ac2_form) == 0
ceiling = sp.simplify(sp.limit(w2 / (1 + ell**2 * x**2), x, sp.oo))   # omega^2/(H^2 (1 + Lstar^2 k^2/2)) -> eps
out["symbolic"] = {"omega2_matches_AC2_printed_form": bool(same), "lim_omega2_Lstar0": str(lim_l0),
                   "lim_phase_speed2_Lstar0": str(cph_l0), "lim_phase_speed2_Lstar": str(cph_l),
                   "lim_omega2_over_(1+Lstar^2k^2/2)": str(ceiling)}
say(f"AC2 dispersion re-derived from S2: equals AC2's printed (omega/H)^2 form: {same}")
say(f"  k -> oo at Lstar = 0: (omega/H)^2 -> {lim_l0}; phase speed^2 -> {cph_l0}")
say(f"  k -> oo at Lstar > 0: phase speed^2 -> {cph_l}; omega^2/(H^2 (1 + Lstar^2 k^2/2)) -> {ceiling}")

# ---------------- framework-native numbers
c = mp.mpf(299792458)
kpc = mp.mpf("3.0856775814913673e19")
Gyr = mp.mpf("3.15576e16")
kap = mp.mpf(1) / 2
foot = {"canonical": (mp.mpf("9.3603e-11"), mp.mpf("21.7")), "alt": (mp.mpf("1.1312e-10"), mp.mpf("22.9"))}
radii = [("10 kpc", 10), ("300 kpc", 300), ("1 Mpc", 1000), ("2 Mpc (cluster scale)", 2000)]
tauf = [mp.mpf("0.063"), mp.mpf("0.154")]
out["numbers"] = {}
for fname, (a0, Lpc) in foot.items():
    Lst = Lpc * kpc / 1000
    out["numbers"][fname] = {}
    say(f"[{fname}] a0 = {mp.nstr(a0, 5)} m/s^2, Lstar = {mp.nstr(Lpc, 3)} pc")
    for opw in (mp.mpf("0.1"), mp.mpf(1), mp.mpf(2)):
        Om2 = 4 * mp.pi * opw * a0**2 / (kap**2 * c**2)
        Om = mp.sqrt(Om2)
        row = {"1+w": float(opw), "Omega_per_s": mp.nstr(Om, 6), "1/Omega_Gyr": mp.nstr(1 / Om / Gyr, 5),
               "helmholtz_length_Gpc": mp.nstr(c / Om / (kpc * 1e6), 5), "radii": {}, "Omega_tau_f": {}}
        say(f"  1+w = {mp.nstr(opw, 2)}: Omega = {mp.nstr(Om, 5)} /s, 1/Omega = {mp.nstr(1/Om/Gyr, 4)} Gyr, "
            f"c/Omega = {mp.nstr(c/Om/(kpc*1e6), 4)} Gpc")
        for lab, rk in radii:
            k = 1 / (rk * kpc)
            cYv = 1 / (1 + Lst**2 * k**2 / 2)
            om = mp.sqrt(Om2 * c**2 * k**2 / (Om2 + cYv * c**2 * k**2))
            vph = om / k / 1000
            row["radii"][lab] = {"omega_per_s": mp.nstr(om, 6), "omega/Omega": mp.nstr(om / Om, 12),
                                 "phase_speed_km_s": mp.nstr(vph, 5)}
            say(f"     r = 1/k = {lab}: omega/Omega = {mp.nstr(om/Om, 10)}, clock phase speed omega/k = "
                f"{mp.nstr(vph, 4)} km/s")
        for tf in tauf:
            v = Om * tf * Gyr
            row["Omega_tau_f"][mp.nstr(tf, 3)] = mp.nstr(v, 5)
            say(f"     COL1 fold time {mp.nstr(tf, 3)} Gyr: Omega tau_f = {mp.nstr(v, 4)} "
                f"(restoring time / fold time = {mp.nstr(1/v, 4)})")
        out["numbers"][fname][mp.nstr(opw, 2)] = row
allv = [mp.mpf(r["Omega_tau_f"][k]) for f in out["numbers"].values() for r in f.values() for k in r["Omega_tau_f"]]
say(f"largest Omega tau_f over every case: {mp.nstr(max(allv), 4)}; smallest {mp.nstr(min(allv), 4)} "
    f"(AC10's planar fold criterion for a clock-only stream: folds iff Omega tau_f <= 1)")
out["Omega_tau_f_range"] = [mp.nstr(min(allv), 5), mp.nstr(max(allv), 5)]
# Lean input for theorem (v): the largest case, alt, 1+w = 2, tau_f = 0.154 Gyr: Omega^2 tau^2 = 8 pi (a0 tau/(kappa c))^2
a0, _ = foot["alt"]
z = a0 * mp.mpf("0.154") * Gyr / (kap * c)
say(f"Lean input (v): a0 tau_f/(kappa c) at alt, tau_f 0.154 Gyr = {mp.nstr(z, 10)}; 8 pi z^2 = {mp.nstr(8*mp.pi*z**2, 6)}")
out["lean_input_v"] = {"z": mp.nstr(z, 12), "8pi_z2": mp.nstr(8 * mp.pi * z**2, 8)}
with open("kde1_record_rate.json", "w") as f:
    json.dump(out, f, indent=1)
with open("kde1_record_rate.out", "w") as f:
    f.write("\n".join(lines) + "\nReported only; grades nothing.\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")

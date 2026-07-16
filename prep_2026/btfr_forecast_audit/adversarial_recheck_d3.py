#!/usr/bin/env python3
"""
ADVERSARIAL RECHECK, Door 3 (DESI DR2 + JWST BTFR forecast audit).

(1) Re-derives the canonical z=3 offset FROM THE BANKED RULE
    dlogV = (1/8) dlog10 rho_DE with the real DESI DR2 CPL (w0=-0.752,
    wa=-0.86), using plain math (no numpy broadcast, no shared code with
    btfr_forecast_check.py); plus the bump z/amplitude analytically.
(2) Audits Gemini's Task 5 (desi_jwst_btfr_forecast.py, byte-identical copy
    here) INDEPENDENTLY: greps it for hard-coded outputs / error treatment,
    imports its functions and reproduces its printed numbers, and computes
    what those numbers mean on the canonical footing.
Exit 0 <=> audit verdict confirmed by direct evidence.
"""
import math, re, sys, importlib.util

W0, WA = -0.752, -0.86            # banked DESI DR2 CPL
OM = 0.315; OL = 0.685

def f_DE(z, w0=W0, wa=WA):        # rho_DE(z)/rho_DE(0), CPL
    return (1 + z) ** (3 * (1 + w0 + wa)) * math.exp(-3 * wa * z / (1 + z))

# ---- (1) canonical re-derivation, banked rule dlogV = (1/8) dlog10 rho_DE ---
dlrho3 = math.log10(f_DE(3.0))
dlogV3 = dlrho3 / 8.0
a0r3 = math.sqrt(f_DE(3.0))
dlogM3 = -math.log10(a0r3)
z_bump = ((-(1 + W0) / WA)) / (1 + (1 + W0) / WA)   # w(z) = -1 crossing
bump = math.sqrt(f_DE(z_bump)) - 1
print(f"(1) dlog10 rho_DE(z=3) = {dlrho3:+.5f} -> dlogV = (1/8)*that = "
      f"{dlogV3:+.5f} dex  (banked -0.033, holding-script -0.0331)")
print(f"    a0(3)/a0(0) = {a0r3:.4f} (claimed 0.737); dlogM(3) = {dlogM3:+.4f}"
      f" (claimed +0.133)")
print(f"    bump: z = {z_bump:.4f} (claimed 0.4052), amplitude = "
      f"{100*bump:+.2f}% (claimed +6.15%)")
assert abs(dlogV3 - (-0.0331)) < 2e-4
assert abs(a0r3 - 0.737) < 1e-3 and abs(dlogM3 - 0.1325) < 1e-3
assert abs(z_bump - 0.4052) < 1e-3 and abs(bump - 0.0615) < 1e-3
# pure Lambda: exactly constant
assert all(abs(f_DE(z, -1.0, 0.0) - 1.0) < 1e-15 for z in (0.5, 1, 2, 3))
# alt footing spot check (rho_total/cH branch): E(3) with DR2 CPL
E3 = math.sqrt(OM * 4**3 + OL * f_DE(3.0))
print(f"    alt footing E(3) = {E3:.3f} -> dlogV = {0.25*math.log10(E3):+.4f} "
      f"(claimed +0.164), dlogM = {-math.log10(E3):+.4f} (claimed -0.656)")
assert abs(0.25 * math.log10(E3) - 0.1641) < 5e-4
# fork spread, opposite signs
spread = 0.25 * math.log10(E3) - dlogV3
print(f"    fork spread at z=3 = {spread:.4f} dex, signs OPPOSITE: "
      f"{0.25*math.log10(E3):+.3f} vs {dlogV3:+.3f}  (claimed 0.197)")
assert abs(spread - 0.197) < 1e-3 and dlogV3 < 0 < 0.25 * math.log10(E3)
# detectability spot checks
d35 = math.log10(f_DE(3.5)) / 8.0
N3 = math.ceil((3 * 0.05 / abs(dlogV3)) ** 2)
print(f"    |dlogV(3.5)| = {abs(d35):.4f} (claimed 0.041 max to z=3.5); "
      f"N_3sig(z=3, s=0.05) = {N3} (claimed ~21); coherent case: "
      f"{abs(d35):.3f} < 3*0.04 = 0.12 -> not detectable at any N")
assert abs(abs(d35) - 0.041) < 1e-3 and N3 == 21 and abs(d35) < 0.12

# ---- (2) independent audit of Gemini Task 5 ---------------------------------
SRC = "/Users/carlzimmerman/new_physics/prep_2026/btfr_forecast_audit/desi_jwst_btfr_forecast.py"
txt = open(SRC).read()
print("\n(2) Gemini Task 5 audit (independent):")
# (2a) hard-coded outputs? every printed number must come from a formula
hard = re.findall(r"-0\.259|-0\.482|-0\.659|4\.57|0\.737|-0\.033", txt)
print(f"    hard-coded headline numbers in source: {hard or 'NONE'}")
assert not hard, "found literal output values -> would contradict 'not hard-coded'"
# (2b) error treatment? scatter/floor/sigma/N anywhere?
err = re.findall(r"(?i)sigma|scatter|error|floor|noise|uncertain|N_gal|detect", txt)
print(f"    error/detectability treatment tokens: {err or 'NONE'}")
assert not err, "unexpected error treatment found"
# (2c) its DESI params vs the real DR2
w0g = float(re.search(r"w0_desi\s*=\s*(-?[\d.]+)", txt).group(1))
wag = float(re.search(r"wa_desi\s*=\s*(-?[\d.]+)", txt).group(1))
print(f"    its 'DESI DR2' params: w0={w0g}, wa={wag} "
      f"(comment: 'approximate representative') vs real DR2 w0={W0}, wa={WA}")
assert (w0g, wag) == (-0.8, -0.5) and (w0g, wag) != (W0, WA)
# (2d) its footing: import the module (main() is __main__-guarded) and test
spec = importlib.util.spec_from_file_location("gem5", SRC)
gem = importlib.util.module_from_spec(spec); spec.loader.exec_module(gem)
r_lcdm3 = gem.E_z_lcdm(3.0, OM, OL)
s_lcdm3 = gem.btfr_shift_dex(r_lcdm3)
r_desi3 = gem.E_z_desi(3.0, OM, OL, w0g, wag)
s_desi3 = gem.btfr_shift_dex(r_desi3)
print(f"    its formula reproduced: LCDM-basis a0 ratio at z=3 = {r_lcdm3:.3f} "
      f"(the '4.57x rising' -- canonical pure-Lambda a0 is EXACTLY constant)")
print(f"    its shifts at z=3: LCDM {s_lcdm3:+.3f} dex, 'DESI' {s_desi3:+.3f} dex"
      f" (its own DESI curve is {abs(s_desi3-s_lcdm3):.4f} dex from LCDM --")
print(f"     it misses the entire CPL signature; canonical dlogM(3) = "
      f"{dlogM3:+.3f} dex: WRONG SIGN, {abs(s_desi3/dlogM3):.1f}x magnitude)")
assert abs(r_lcdm3 - 4.57) < 0.01
assert abs(s_lcdm3 - (-0.660)) < 1e-3 and abs(s_desi3 - (-0.659)) < 1e-3
assert abs(s_desi3 - s_lcdm3) < 0.002          # indistinguishable from LCDM
assert s_desi3 * dlogM3 < 0                    # opposite sign vs canonical
assert 4.5 < abs(s_desi3 / dlogM3) < 5.5       # ~5x magnitude
# (2e) footing identification: E_z includes Omega_m (1+z)^3 -> rho_total branch
assert "Omega_m * (1+z)**3" in txt.replace(" ", "").replace("**3", "**3") or \
       re.search(r"Omega_m\s*\*\s*\(1\+z\)\s*\*\*\s*3", txt)
print("    footing: a0_ratio = E(z) = sqrt(Om(1+z)^3 + ...) -> the "
      "rho_total/cH0 ALT branch, mislabeled 'Zimmerman' (canonical is "
      "sqrt(rho_DE ratio))")
print("\nALL D3 ADVERSARIAL RECHECKS PASS -- audit verdict confirmed")

"""PAR1 KA-MD (AMENDMENT A2, a7cac068bf): independent SI recomputation of MEDIUM_DESIGN section 3's numbers.
Written without running or importing the note's script. Inputs are the note's stated ones.

Run: python3 par1_medium_ka.py -> par1_medium_ka.out/.json ; PAR1_MUTATE=MU5 (pi dropped) -> *_MUTATE_MU5.*
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json, math, os

MUT = os.environ.get("PAR1_MUTATE", "")
TAG = f"_MUTATE_{MUT}" if MUT else ""
G = 6.6743e-11            # m^3 kg^-1 s^-2
PC = 3.0857e16            # m
MPC = 3.0857e22           # m
h, Ob, Om, Orad = 0.674, 0.0493, 0.3147, 9.15e-5
H0 = h * 1.0e5 / MPC      # 100 h km/s/Mpc in 1/s
rho_c0 = 3.0 * H0 ** 2 / (8.0 * math.pi * G)
LINES = {"canonical": (22.4, 25.8, 0.73), "alt": (18.5, 31.1, 0.61)}
out, txt = {}, []
for foot, a0 in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
    kap = (G if MUT == "MU5" else math.pi * G) / a0          # m^2 per kg of baryons
    kap_cgs = kap * 1e4 / 1e3                                  # cm^2/g
    z = 1100.0
    a = 1.0 / (1.0 + z)
    rho_b = Ob * rho_c0 / a ** 3
    mfp_pc = 1.0 / (rho_b * kap) / PC
    Hz = H0 * math.sqrt(Om / a ** 3 + Orad / a ** 4 + (1.0 - Om - Orad))
    drag = 3.0e4 / (mfp_pc * PC) / Hz                          # (v / mean free path) / H at v = 30 km/s
    lk, lm, ld = LINES[foot]
    ok = {"opacity": abs(kap_cgs / lk - 1) <= 0.005, "mfp": abs(mfp_pc / lm - 1) <= 0.01, "drag": abs(drag - ld) <= 0.01}
    out[foot] = {"opacity_cm2_per_g": round(kap_cgs, 3), "mfp_z1100_pc": round(mfp_pc, 2),
                 "drag_over_H_30kms_z1100": round(drag, 3), "lines": ok, "PASS": all(ok.values())}
    txt.append(f"[{foot}] opacity {kap_cgs:.3f} cm^2/g (line {lk}); mean free path z 1100 {mfp_pc:.2f} pc (line {lm}); "
               f"drag/H at 30 km/s {drag:.3f} (line {ld}) -> {ok} -> {'PASS' if all(ok.values()) else 'FAIL'}")
out["KA_MD_PASS"] = all(out[f]["PASS"] for f in ("canonical", "alt"))
out["mutate"] = MUT
txt.append(f"KA-MD: {'PASS' if out['KA_MD_PASS'] else 'FAIL'} (mutate={MUT or 'none'})")
json.dump(out, open(f"par1_medium_ka{TAG}.json", "w"), indent=1)
open(f"par1_medium_ka{TAG}.out", "w").write("PAR1 KA-MD (A2 a7cac068bf)\n" + "\n".join(txt) +
                                            "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
print("\n".join(txt))

# Adopts nothing. kappa = 1/2 FITTED; not theory closed.

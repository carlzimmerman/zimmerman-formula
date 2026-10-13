"""CFG746: sealed hot-gas prediction of the CFG745 selector (criteria: FROZEN_CRITERIA.md). Deterministic JSON, no timestamps.
kappa = 1/2 FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed".
Run:  python3 cfg746_predict.py      (CFG746_MUTATE=1: k -> 2k; exit 1 iff P1 halves)
"""
import os, sys, json, math, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); sys.path.insert(0, LANES)
import CFG4_common as C4  # noqa: E402
MUT = os.environ.get("CFG746_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
G, MSUN, KPC, MPC, MP, ME, C, SIGT, KEV = 6.6743e-11, 1.98847e30, 3.0856775814913673e19, 3.0856775814913673e22, 1.67262192e-27, 9.1093837e-31, 2.99792458e8, 6.6524587e-29, 1.602176634e-16
c745 = json.load(open(os.path.join(LANES, "CFG745_hot_gas_selector", "cfg745_results.json")))
REQ = {"canonical": 0.8, "alt": 0.55}
L580 = {"0.1": (3.5e39, 1.1e40), "0.3": (9.8e39, 2.9e40), "1.0": (3.2e40, 9.5e40)}; M580 = 5.1e10
Mstar = 10 ** 10.8
out = {"lane": "CFG746", "Mstar_Msun": Mstar, "R_kpc": 100, "rows": {}}
lines = [__doc__.strip()]
for f in C4.FOOTS:
    a0 = C4.A0[f]
    for fh in ("0.85", "0.95"):
        k = c745[f][fh]["k"] * (2 if MUT else 1)
        Mh = REQ[f] * Mstar / k
        Mb = Mstar + Mh
        r = 100 * KPC
        gN = G * Mb * MSUN / r ** 2
        g = gN + math.sqrt(a0 * gN) + G * k * Mh * MSUN / r ** 2    # law on baryons + cold energy C = k M_hot (frozen P2)
        Vc2 = g * r
        kT = 0.6 * MP * Vc2 / 2 / KEV
        Ne = Mh * MSUN / (1.14 * MP)
        YD2 = SIGT * kT * KEV * Ne / (ME * C ** 2) / MPC ** 2
        Lx = {z: [round(v * (Mh / M580) ** 2, -36) for v in rng] for z, rng in L580.items()}
        key = f"{f}|{fh}"
        out["rows"][key] = dict(k=float(f"{k:.6g}"), M_hot_Msun=float(f"{Mh:.6g}"), M_hot_over_Mstar=float(f"{Mh / Mstar:.6g}"),
                                Vc_kms=float(f"{math.sqrt(Vc2) / 1e3:.6g}"), kT_keV=float(f"{kT:.6g}"), Y_DA2_Mpc2=float(f"{YD2:.6g}"), Lx_0p5_2_erg_s=Lx)
        lines.append(f"{key}: k {k:.3f}; M_hot(<100 kpc) {Mh:.3e} Msun ({Mh / Mstar:.3f} M*); V_c(100 kpc) {math.sqrt(Vc2) / 1e3:.0f} km/s (incl. cold energy); kT {kT:.3f} keV; "
                     f"Y D_A^2 {YD2:.3e} Mpc^2; L_X(Z 0.1/0.3/1) {Lx['0.1']}/{Lx['0.3']}/{Lx['1.0']} erg/s (eROSITA stack 1.1e40 +- 0.4e40)")
out["falsifier"] = "measured M_hot(<100 kpc) for log M* 10.5-11.0 quiescent galaxies below half of every M_hot_Msun row kills the selector as the C3 explanation"
blob = json.dumps(out, sort_keys=True, indent=1) + "\n"
open(os.path.join(HERE, f"cfg746_predictions{TAG}.json"), "w").write(blob)
h = hashlib.sha256(blob.encode()).hexdigest(); lines.append(f"SHA-256 cfg746_predictions{TAG}.json: {h}")
open(os.path.join(HERE, f"cfg746_predict{TAG}.out"), "w").write("\n".join(lines) + "\n"); print("\n".join(lines))
if MUT:
    base = json.load(open(os.path.join(HERE, "cfg746_predictions.json")))["rows"]["canonical|0.85"]["M_hot_Msun"]
    sys.exit(1 if abs(out["rows"]["canonical|0.85"]["M_hot_Msun"] / base - 0.5) < 1e-5 else 0)
open(os.path.join(HERE, "PREDICTIONS_HASH.txt"), "w").write(f"{h}  cfg746_predictions.json\n")

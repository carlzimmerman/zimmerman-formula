"""TK1 A1 on the FRW background (criteria 98f2ab2b6e): G_cosmo/G_N - 1, lambda_eff, the K4 kinetic coefficient A_z,
the k^4 gradient coefficient's sign (g4/A_z), the dust sound speed (Q-1)/Q (KA5 form), per footing, primary and brackets,
at z = 3400, 1100, 10, 2, 1, 0.5, 0 (and a log-z scan for the sign of g4 and A_z over [0, 3400]).
G_cosmo from the Friedmann equation's H^2 dependence at fixed charge: G_cosmo/G = 1/(1 - d xK/d(H^2)) (units 8 pi G/3 = 1).
G_N: static weak field, theta = 0: the term is M_f^2 (Q-1)^2/(2K) there (F_thth = 0 for p >= 2 at theta = 0), so G_N is
that of action (A) with mu_K = M_f. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json
import mpmath as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tk1_lib as L
import tk1_a3 as A3

HERE = os.path.dirname(os.path.abspath(__file__))
out = {}
keys = {"primary": L.PRIMARY}
keys.update({k: v for k, v in L.BRACKETS.items() if k != "MU2_key_off"})
for foot in ("canonical", "alt"):
    out[foot] = {}
    for nm, prm in keys.items():
        key = L.Key(**prm)
        rows = {}
        for z in (3400, 1100, 10, 2, 1, 0.5, 0):
            a = mp.mpf(1) / (1 + z)
            H, On = L.background_H(key, a, foot)
            dxdH = mp.diff(lambda h: key.xK(3 * h, On), H)
            Gc = 1 / (1 - dxdH / (2 * H))
            Az, g4, cs2, N0 = A3.k4_alg(key, a, H, On)
            M2pp = key.M2pp(3 * H)
            rows[str(z)] = dict(G_cosmo_over_G_minus_1=float(Gc - 1), lambda_eff=float(key.lam_eff(3 * H, On)),
                                Az=float(Az), g4=float(g4), g4_over_Az_sign=int(mp.sign(g4 / Az)),
                                cs2_dust=float(cs2), M2pp_sign=int(mp.sign(M2pp)), theta=float(3 * H))
        # scan
        neg_Az, neg_g4 = [], []
        for j in range(0, 141):
            z = mp.mpf(10)**(mp.mpf(j) / 40) - 1
            if z > 3400:
                break
            a = 1 / (1 + z)
            H, On = L.background_H(key, a, foot)
            Az, g4, cs2, N0 = A3.k4_alg(key, a, H, On)
            if Az <= 0:
                neg_Az.append(float(z))
            if g4 / Az < 0:
                neg_g4.append(float(z))
        out[foot][nm] = dict(rows=rows, z_with_Az_le_0=neg_Az, z_with_g4_over_Az_lt_0=neg_g4)
        mx = max(abs(r["G_cosmo_over_G_minus_1"]) for r in rows.values())
        print("[%s %s] max |G_cosmo/G - 1| %.3e; lambda_eff(0) %.3e; A_z > 0 everywhere: %s; g4/A_z < 0 at z: %s" % (
            foot, nm, mx, rows["0"]["lambda_eff"], not neg_Az,
            ("none" if not neg_g4 else "%.3g..%.3g (%d of grid)" % (min(neg_g4), max(neg_g4), len(neg_g4)))), flush=True)
        for z, r in rows.items():
            print("    z %-5s G-1 %+.3e lam %+.3e A_z %.3e g4 %+.3e cs2 %.3e theta %.4g" % (
                z, r["G_cosmo_over_G_minus_1"], r["lambda_eff"], r["Az"], r["g4"], r["cs2_dust"], r["theta"]), flush=True)
json.dump(out, open(os.path.join(HERE, "tk1_frw.json"), "w"), indent=1)
print("done")

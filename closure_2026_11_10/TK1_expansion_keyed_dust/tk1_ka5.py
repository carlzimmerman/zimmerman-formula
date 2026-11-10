"""TK1 KA5: K4's closed form on a background consistent with K4's own content (gravity + clock + Lambda, flat):
with M_2 constant (key off) the dust sound speed g2 a^2/(A_z N0^2) must equal (Q-1)/Q (k-essence dust). Primary beside.
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json
import mpmath as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tk1_lib as L, tk1_k4eval as E
OL = L.FOOT["canonical"]["OL"]; Od = 1 - OL
out = {}
for nm, prm in (("key_off", L.BRACKETS["MU2_key_off"]), ("primary", L.PRIMARY)):
    k = L.Key(**prm)
    rest = lambda a: mp.mpf(OL); On = lambda a: Od / a**3
    for z in (3400, 10, 0):
        a = mp.mpf(1) / (1 + z)
        r = E.evaluate(k, a, rest, On, OL=OL)
        q = r["Qm1"] / (1 + r["Qm1"])
        rel = r["cs2_dust"] / q - 1
        out["%s_z%s" % (nm, z)] = dict(cs2=float(r["cs2_dust"]), Qm1_over_Q=float(q), rel=float(rel), Az=float(r["Az"]), g4=float(r["g4"]))
        print("%-8s z %-5s A_z %.4e g4 %+.3e c_s^2 %s (Q-1)/Q %s rel %s" % (nm, z, r["Az"], r["g4"], mp.nstr(r["cs2_dust"], 10), mp.nstr(q, 10), mp.nstr(rel, 3)))
out["KA5_pass"] = all(abs(v["rel"]) < 1e-6 for k_, v in out.items() if k_.startswith("key_off"))
print("KA5 PASS" if out["KA5_pass"] else "KA5 FAIL")
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tk1_ka5.json"), "w"), indent=1)

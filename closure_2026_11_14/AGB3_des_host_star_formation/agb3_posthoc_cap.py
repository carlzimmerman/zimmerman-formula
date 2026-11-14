"""AGB3, POST HOC 3 (written after the shape post hoc was seen; no frozen word).

Part S grants the published slope a linear run up to the oldest hosts. The shape post hoc finds no trend among the
old low-redshift hosts. Here the sample's own drift template is rebuilt with each host's age capped at 6 Gyr (and at
4 Gyr), which is a law that stops running there, and Part S and Part J are repeated on the whole sample:
    T_cap(z) = 0.030 x [mean of min(age, cap) in the lowest redshift bin - mean of min(age, cap) at z].
Priors on the amplitude: D2 as frozen (0.389 +- 0.079) and the noise-corrected upper limit of the first post hoc
(U with stretch and mass as witnesses). Writes agb3_posthoc_cap.json; log to agb3_posthoc_cap.out."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = ["agb3_cosmo.py", "none"]; sys.path.insert(0, HERE)
import numpy as np
import agb3_cosmo as C

log = lambda s: print(s, flush=True); out = {}
d = C.R3.DES(); age = C.T2.age(d.lm, d.ls, d.z); bao = C.R1.BAO("all"); sn = C.R1.SN("full"); F = C.R1.Fitter("A", sn, bao)
N = json.load(open(os.path.join(HERE, "agb3_posthoc_noise.json")))["B"]["x1_mass"]["U"]
D = json.load(open(os.path.join(HERE, "agb3_D.json")))["fits"]["primary"]["D2"]
Af, An = np.array(C.GRID_F), np.array(C.GRID_N)
for cap in (6.0, 4.0):
    zc, ac = C.host_curve(d.z, np.minimum(age, cap)); name = f"cap{cap:.0f}"; sn.add_template(name, C.t_h(sn.z, zc, ac))
    log(f"cap {cap:.0f} Gyr: template at the sample's redshifts from {sn.T[name][0].min():+.4f} to {sn.T[name][0].max():+.4f} mag (uncapped: 0 to 0.105)")
    one = C.forks(F, name, 1.0, log, f"whole sample, cap {cap:.0f} Gyr, A_H = 1"); g = C.grids(F, name, log, f"cap {cap:.0f} Gyr")
    out[name] = dict(curve=dict(z=zc.tolist(), age=ac.tolist()), A1=one, grids=g, joint={})
    for pk, (ah, sh) in (("D2_as_frozen", (D["A"], D["sd_A"])), ("U_noise_corrected", (N["A_corrected"], N["sd_A_corrected"]))):
        r = C.J2.joint(Af, np.array(g["f"]), np.array(g["q0"]), An, np.array(g["n"]), np.array(g["t"]), ah, sh); out[name]["joint"][pk] = r
        log(f"  joint, prior {pk} ({ah:+.3f} +- {sh:.3f}): A_H {r['A']:+.3f}, q0 {r['q0']:+.3f}, q0 = 0: dchi2 {r['D_today']:.2f}; never accelerated: dchi2 {r['D_never']:.1f}")
json.dump(out, open(os.path.join(HERE, "agb3_posthoc_cap.json"), "w"), indent=1, default=float)
log("wrote agb3_posthoc_cap.json")

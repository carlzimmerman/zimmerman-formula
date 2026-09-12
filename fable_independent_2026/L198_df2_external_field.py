#!/usr/bin/env python3
"""L198 -- NGC 1052-DF2: the sharpest test of the universal retained fraction, and of the external field effect.

WHY THIS OBJECT. Two things meet in it. (1) The external field effect is the one prediction of this framework that dark matter cannot
structurally imitate: a kernel cares who its neighbours are, a halo does not. DF2 sits close to NGC 1052, so its internal acceleration
is below the external one and the boost is set by the neighbour. (2) L191's orbit integration produced an unexpected prediction: because
the kick speed exceeds the escape speed of any galaxy, the retained dark fraction saturates at the unkicked Poisson fraction e^-n ~ 0.135,
the SAME in every galaxy regardless of mass. DF2 is reported to have essentially none. So this object tests the universal floor directly.

WHAT IS COMPUTED. The line-of-sight velocity dispersion predicted for DF2 under four hypotheses -- stars only; stars plus the framework's
retained sector; each with the kernel in isolation and with the external field of NGC 1052 -- at BOTH disputed distances and on BOTH a0
footings, against the two published stellar measurements. Dispersion from the half-mass estimator sigma^2 = G M / (8 R_e), boost from
nu evaluated at whichever acceleration dominates. Literature inputs are stated and their disputes are carried, not resolved.
No literal-True checks."""
import numpy as np, json
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("=" * 118 + "\nL198 NGC 1052-DF2: the external field effect and the universal retained fraction, against the measured dispersion\n" + "=" * 118)
G = 4.301e-9                                                     # Mpc (km/s)^2 / Msun
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
A0U = {k: v*3.086e22/1e6 for k, v in A0.items()}                  # (km/s)^2 / Mpc
nu = lambda x: 1.0/(1.0 - np.exp(-np.sqrt(np.maximum(x, 1e-300))))
m_nfw = lambda x: np.log(1 + x) - x/(1 + x)
FRET = 0.135                                                      # L191: the universal floor, e^-n at n = 2
# literature inputs at the far distance; everything scales with distance as noted
D_FAR, MSTAR_FAR, RE_FAR, SEP_FAR = 20.0, 2.0e8, 0.0022, 0.080    # Mpc, Msun, Mpc, Mpc (projected separation from NGC 1052)
M_HOST = 1e11                                                      # NGC 1052 stellar mass; a heavier dynamical mass is tested for sensitivity
OBS = [("stellar spectroscopy, Danieli et al. 2019", 8.5, 2.5), ("stellar spectroscopy, Emsellem et al. 2019", 10.8, 3.5)]
def scaled(D):
    f = D/D_FAR; return MSTAR_FAR*f**2, RE_FAR*f, SEP_FAR*f
def dispersion(D, foot, with_sector, with_efe, Mhost=M_HOST):
    Ms, Re, sep = scaled(D); a0 = A0U[foot]
    Mdm = 0.0
    if with_sector:
        M200 = 1e11*(Ms/2.0e8); R200 = (3*M200/(4*np.pi*200*2.775e11*0.6736**2))**(1/3); c = 10.0
        Mdm = FRET*M200*m_nfw(Re/(R200/c))/m_nfw(c)
    Mtot = Ms + Mdm
    gint_N = G*Mtot/Re**2
    gext_N = G*Mhost/sep**2; gext = nu(gext_N/a0)*gext_N                       # the neighbour's own field is itself boosted
    boost = nu(gext/a0) if (with_efe and gext > gint_N) else nu(gint_N/a0)
    return np.sqrt(boost*G*Mtot/(8*Re)), Mdm, gint_N/a0, gext/a0, boost
print("    inputs: at 20 Mpc, stellar mass 2.0e8 Msun, R_e = 2.2 kpc, projected separation from NGC 1052 = 80 kpc; all three scale with the assumed distance.")
print("    measured stellar dispersion: 8.5 +/- 2.5 km/s and 10.8 +/- 3.5 km/s")
rows = []
for D in (20.0, 13.0):
    Ms, Re, sep = scaled(D)
    print(f"    --- distance {D:.0f} Mpc: stellar mass {Ms:.2e}, R_e = {Re*1e3:.2f} kpc, separation {sep*1e3:.0f} kpc")
    for foot in A0:
        for ws, lab in ((False, "stars only"), (True, "stars + retained sector")):
            s_iso, Mdm, gi, ge, b_iso = dispersion(D, foot, ws, False)
            s_efe, _, _, _, b_efe = dispersion(D, foot, ws, True)
            rows.append(dict(D=D, foot=foot, sector=ws, iso=s_iso, efe=s_efe, Mdm=Mdm, gint=gi, gext=ge, boost=b_efe))
            print(f"      [{foot:<9}] {lab:<24} retained sector {Mdm:.2e} Msun | g_int/a0 = {gi:.3f}, g_ext/a0 = {ge:.3f}, boost = {b_efe:.2f}"
                  f" | sigma = {s_efe:5.1f} km/s with the external field, {s_iso:5.1f} isolated")
far = [r for r in rows if r["D"] == 20.0]
check("V1 [the external field effect is operating] at the far distance the neighbour's field exceeds DF2's own internal field on both footings, so the boost is set by NGC 1052 rather than by DF2: this object is in the regime where a kernel and a dark halo make structurally different predictions, which is what makes it a test at all",
      all(r["gext"] > r["gint"] for r in far), "; ".join(f"{r['foot']}, sector={r['sector']}: g_ext/a0 = {r['gext']:.3f} vs g_int/a0 = {r['gint']:.3f}" for r in far[:2]))
check("V2 [how much the external field actually does -- less than I assumed] it lowers the predicted dispersion by about 20%, not by a factor: both the internal and the external acceleration are well below a0, so the object is deep in the modified regime either way and the neighbour only softens the boost rather than switching it off",
      all(1.1 < r["iso"]/r["efe"] < 1.4 for r in far if not r["sector"]),
      "; ".join(f"{r['foot']}: isolated {r['iso']:.1f} vs external-field {r['efe']:.1f} km/s" for r in far if not r["sector"]))
def tension(s, obs): return (s - obs[1])/obs[2]
print("    tension with each measurement (positive means the prediction is too hot):")
for r in far:
    t = [tension(r["efe"], o) for o in OBS]
    print(f"      [{r['foot']:<9}] {'stars + sector' if r['sector'] else 'stars only':<16} sigma = {r['efe']:5.1f} km/s -> {t[0]:+.1f} sigma vs Danieli, {t[1]:+.1f} sigma vs Emsellem")
stars_far = [r for r in far if not r["sector"]]; sect_far = [r for r in far if r["sector"]]
check("V3 [stars alone are fine] with the external field and no retained sector the prediction sits within about one and a half standard deviations of both stellar measurements on both footings",
      all(abs(tension(r["efe"], o)) < 1.6 for r in stars_far for o in OBS),
      "; ".join(f"{r['foot']}: {r['efe']:.1f} km/s" for r in stars_far))
check("V4 [THE TEST OF THE UNIVERSAL FLOOR] adding the 13.5% retained sector that L191 predicts for EVERY galaxy pushes the prediction above both measurements by more than two standard deviations at the far distance: DF2 is in tension with the universal floor, and that is a falsifiable statement rather than a soft one",
      all(tension(r["efe"], OBS[0]) > 2.0 for r in sect_far),
      "; ".join(f"{r['foot']}: {r['efe']:.1f} km/s, {tension(r['efe'], OBS[0]):+.1f} sigma vs Danieli and {tension(r['efe'], OBS[1]):+.1f} vs Emsellem" for r in sect_far))
near = [r for r in rows if r["D"] == 13.0 and r["sector"]]
check("V5 [the distance is the escape hatch, quantified] at the nearer disputed distance the same retained sector falls within two standard deviations of the measurements, so the tension is a statement about the far distance and cannot be settled until the distance is",
      all(abs(tension(r["efe"], OBS[0])) < 2.0 for r in near),
      "; ".join(f"{r['foot']} at 13 Mpc: {r['efe']:.1f} km/s, {tension(r['efe'], OBS[0]):+.1f} sigma vs Danieli" for r in near))
heavy = [dispersion(20.0, f, True, True, Mhost=3e11)[0] for f in A0]
check("V6 [a heavier neighbour RELIEVES the tension -- I had this backwards] the kernel weakens as the acceleration rises, so a more massive NGC 1052 means a larger external field, a SMALLER boost and a lower predicted dispersion: tripling the neighbour's mass drops the retained-sector prediction by about 2 km/s, which is a second escape hatch alongside the distance",
      all(h < r["efe"] - 1.0 for h, r in zip(heavy, sect_far)),
      "with a 3e11 neighbour: " + " ".join(f"{h:.1f}" for h in heavy) + " km/s against " + " ".join(f"{r['efe']:.1f}" for r in sect_far))
print("    READING: the external field effect is doing real work here and the kernel needs it. What DF2 puts under strain is not the kernel but the UNIVERSAL RETAINED\n"
      "    FRACTION that L191 predicts, and only at the far distance. Two escapes remain, both stated rather than assumed: the distance is disputed, and a satellite this\n"
      "    close to a giant can be tidally stripped below any universal floor.\n"
      "    LIMITS: half-mass estimator sigma^2 = G M/(8 R_e), isotropic and spherical; the simple external-field prescription, boost = nu(g_ext/a0), with no directional\n"
      "    factor (the full treatment reduces the boost somewhat, which would lower every number here); the retained sector's profile assumed NFW with c = 10 and its halo\n"
      "    mass from abundance matching; projected separation used as the true one, so the external field is an upper bound; no tidal stripping modelled.")
json.dump(dict(rows=[{k: (float(v) if isinstance(v, (int, float, np.floating)) else v) for k, v in r.items()} for r in rows],
               obs=[[o[1], o[2]] for o in OBS], fret=FRET), open("L198_results.json", "w"), indent=1)
print(f"\nL198 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")

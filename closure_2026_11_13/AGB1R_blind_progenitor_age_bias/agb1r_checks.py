"""AGB1R known-answer checks for Part A: counts, K1 (BAO-only LCDM), K2 (SN-only LCDM, full), K4 (integrator vs CAMB),
K3 mutation twins (exit 3 if both twins pass, 4 otherwise). KT is in agb1r_template.py; KA in agb1r_partA.py.
Usage: python3 agb1r_checks.py [counts|k1|k2|k4|k3|all]"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agb1r_common import (load_des, sample_keep, SN, BAO, PartA, Dist, E2, build_template, fit_A, nm_polished,
                          C_KMS, dump, HERE)

what = sys.argv[1] if len(sys.argv) > 1 else "all"
out = {}

def lcdm_fit(model):
    f = lambda x: model.eval(x[0], -1.0, 0.0, 0.0)["chi2"] if 0.05 < x[0] < 0.7 else 1e10
    x, v = nm_polished(f, [0.31], [0.02])
    r = model.eval(x[0], -1.0, 0.0, 0.0)
    return float(x[0]), r

if what in ("counts", "all"):
    D = load_des(); ids = D["ids"]; z = D["zhd"]; des = ids == 10
    c = dict(n=len(ids), n_des=int(des.sum()), des_zmin=float(z[des].min()), des_zmax=float(z[des].max()),
             des_zmed=float(np.median(z[des])), n_leg=int((~des).sum()), leg_zmin=float(z[~des].min()),
             leg_zmax=float(z[~des].max()))
    c["pass"] = bool(c["n"] == 1820 and c["n_des"] == 1623 and c["n_leg"] == 197)
    print(f"counts: {c['n']} SNe; DES {c['n_des']} (z {c['des_zmin']:.4f}-{c['des_zmax']:.4f}, median {c['des_zmed']:.3f});"
          f" legacy {c['n_leg']} (z {c['leg_zmin']:.4f}-{c['leg_zmax']:.4f}) -> {'PASS' if c['pass'] else 'FAIL'}")
    out["counts"] = c

if what in ("k1", "all"):
    m = PartA(None, BAO("all"))
    Om, r = lcdm_fit(m)
    hrd = C_KMS/(100*r["s"])
    k1 = dict(Om=Om, hrd=hrd, chi2=r["chi2"], pass_=bool(abs(Om - 0.2975) <= 0.003 and abs(hrd - 101.54) <= 0.3))
    print(f"K1 BAO-only flat LCDM: Om {Om:.4f} (target 0.2975, tol 0.003)  h r_d {hrd:.2f} Mpc (target 101.54, tol 0.3)"
          f"  chi2 {r['chi2']:.3f} -> {'PASS' if k1['pass_'] else 'FAIL'}")
    out["K1"] = k1

if what in ("k2", "all"):
    D = load_des(); keep = sample_keep(D, "full")
    S = build_template("S"); sn = SN(D, keep, S["spline"](D["zhd"][keep]))
    m = PartA(sn, None)
    Om, r = lcdm_fit(m)
    k2 = dict(Om=Om, chi2=r["chi2"], pass_=bool(abs(Om - 0.330) <= 0.0075))
    print(f"K2 SN-only (full) flat LCDM, A = 0: Om {Om:.4f} (target 0.330, tol 0.0075)  chi2 {r['chi2']:.3f}"
          f" (N = {len(keep)}) -> {'PASS' if k2['pass_'] else 'FAIL'}")
    out["K2"] = k2

if what in ("k4", "all"):
    import camb
    Om, w0, wa, h = 0.32, -0.8, -0.7, 0.68
    ob = 0.0224; oc = Om*h*h - ob
    P = camb.CAMBparams(); P.set_dark_energy(w=w0, wa=wa, dark_energy_model="ppf")
    P.set_cosmology(H0=100*h, ombh2=ob, omch2=oc, mnu=0.0, num_massive_neutrinos=0, nnu=3.044, omk=0)
    P.WantTransfer = False; P.WantCls = False
    R = camb.get_background(P)
    zz = np.array([0.5, 1.0, 2.33])
    dm_c = R.comoving_radial_distance(zz); dh_c = C_KMS/R.hubble_parameter(zz)
    d = Dist(zz); dm = d.DM(Om, w0, wa)*C_KMS/(100*h); dh = C_KMS/(100*h)/np.sqrt(E2(zz, Om, w0, wa))
    rel = np.r_[dm/dm_c - 1, dh/dh_c - 1]
    k4 = dict(z=zz, DM_mine=dm, DM_camb=dm_c, DH_mine=dh, DH_camb=dh_c, rel=rel, max_rel=float(np.abs(rel).max()))
    k4["pass_"] = bool(k4["max_rel"] <= 1e-3)
    for i, z in enumerate(zz):
        print(f"K4 z {z:4.2f}: D_M {dm[i]:.3f} vs CAMB {dm_c[i]:.3f} ({rel[i]:+.2e});  D_H {dh[i]:.3f} vs CAMB {dh_c[i]:.3f}"
              f" ({rel[3+i]:+.2e})")
    print(f"K4 max |rel| {k4['max_rel']:.2e} (tol 1e-3) -> {'PASS' if k4['pass_'] else 'FAIL'}")
    out["K4"] = k4

if what in ("k3", "all"):
    D = load_des(); keep = sample_keep(D, "full")
    S = build_template("S"); T = S["spline"](D["zhd"])
    Om0, w00, wa0, hrd0 = 0.31, -0.8, -0.6, 101.6
    s0 = C_KMS/(100*hrd0)
    zb_model = PartA(None, BAO("all"))
    dmb = zb_model.dist.DM(Om0, w00, wa0); zb = zb_model.bao.zall
    dhb = 1/np.sqrt(E2(zb, Om0, w00, wa0))
    bao_vec = s0*zb_model.bao.model_vec(dmb[:-1], dhb[:-1], dmb[-1], dhb[-1])
    dsn = Dist(D["zhd"]).DM(Om0, w00, wa0)
    mu_base = 5*np.log10((1 + D["zhel"])*dsn*C_KMS/70.0) + 25
    allpass = True; tw = {}
    for At, Awrong in ((1.0, 0.0), (0.0, 1.0)):
        sn = SN(D, keep, T[keep], mu_override=mu_base + At*T)
        m = PartA(sn, BAO("all", override=bao_vec))
        fr = fit_A(m, None, "free")
        wr = fit_A(m, Awrong, "free")
        dwrong = wr["chi2"] - fr["chi2"]
        ok = (abs(fr["A"] - At) <= 0.01 and abs(fr["w0"] + 0.8) <= 0.01 and abs(fr["wa"] + 0.6) <= 0.05
              and fr["chi2"] <= 1e-3 and dwrong > 0)
        allpass &= ok
        print(f"K3 twin A_true {At:.0f}: A_free {fr['A']:+.5f}  Om {fr['Om']:.5f}  w0 {fr['w0']:+.5f}  wa {fr['wa']:+.5f}"
              f"  h r_d {fr['hrd']:.3f}  chi2_min {fr['chi2']:.2e}  dchi2 at A = {Awrong:.0f}: {dwrong:.2f} -> "
              f"{'PASS' if ok else 'FAIL'}")
        tw[f"A_true_{At:.0f}"] = dict(free=fr, wrong=wr, dchi2_wrong=dwrong, pass_=bool(ok))
    out["K3"] = dict(twins=tw, pass_=bool(allpass))
    print(f"K3 -> {'PASS (exit 3)' if allpass else 'FAIL (exit 4)'}")

dump(out, os.path.join(HERE, f"agb1r_checks_{what}.json"))
if what == "k3": sys.exit(3 if out["K3"]["pass_"] else 4)

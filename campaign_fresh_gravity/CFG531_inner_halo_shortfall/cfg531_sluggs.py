#!/usr/bin/env python3
"""CFG531 SLUGGS arm (FROZEN_CRITERIA.md, criteria commit 750fa1f55): the four centrals' residual as eps = Delta M(<r)/M_pred(<r).
Machinery: CFG528b's cfg528b_measured_tracers.py exec'd read-only up to its header print (it execs CFG528, which execs CFG331).
eps_i = 10^(2 o_i) - 1 (Jeans is linear in g); radii and r/r_M of the outer GC bins; (a) the same M* shifts on the JAM-law
ceiling with CFG528's admissibility rule; (d) kernel swap (nu_simple / nu_standard, a0 x CFG468 SPARC ratio) in both the JAM
calibration and the field; mechanism M-a (stars collapsed to a point = maximal contraction).  MUTATE (CFG531_MUTATE=1): MU5.
Run: nice -n 10 python3 cfg531_sluggs.py ; CFG531_MUTATE=1 nice -n 10 python3 cfg531_sluggs.py
"""
import os, sys, io, math, json, time, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "2"
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
MUTATE = os.environ.get("CFG531_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
LOG, CHK = [], {}
RES = {"lane": "CFG531", "script": "cfg531_sluggs", "mutate": MUTATE, "criteria_commit": "750fa1f55",
       "settings": "kappa = 1/2 FITTED; footings never pooled; nu_mono; cold energy mass still required; not theory closed"}
try:
    os.nice(10)
except OSError:
    pass


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}]{'' if lb else ' (reported)'} {name}: {msg}")


D528 = os.path.join(LANES, "CFG528_sluggs_centrals_mechanism")
_p = os.path.join(D528, "cfg528b_measured_tracers.py")
_src = open(_p).read()
for k in ("CFG528B_MUTATE", "CFG528_MUTATE", "CFG528_POSTFREEZE"):
    os.environ.pop(k, None)
NS = {"__file__": _p, "__name__": "cfg528b_ro"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_src[:_src.index('\nP("=" * 124)')], "cfg528b", "exec"), NS)
B, GAL, A0, CEN, RG, LR, G, KPC = (NS[k] for k in ("B", "GAL", "A0", "CEN", "RG", "LR", "G", "KPC"))
build, off_pops, measured_pops, sig_multi, READ = NS["build"], NS["off_pops"], NS["measured_pops"], NS["sig_multi"], NS["READ"]
NS28 = NS["NS"]; NS331 = NS28["NS"]; KERN = NS331["KERN"]; MSUN = NS331["MSUN"]; SIG = NS28["SIG"]
NU0 = KERN["nu_mono"]
FOOTS = ("canonical", "alt")
J28b = json.load(open(os.path.join(D528, "cfg528b_measured_tracers_results.json")))
J28 = json.load(open(os.path.join(D528, "cfg528_mechanism_results.json")))
J468 = json.load(open(os.path.join(LANES, "CFG468_kernel_family", "cfg468_kernel_family_results.json")))
P(f"CFG528b machinery exec'd read-only; centrals {CEN}; footings {A0}")


def own_off(n, a0, mmult=1.0, g_scale=1.0):
    r = build(n, a0, **READ["own"], mmult=mmult)
    return off_pops(n, r[0] * g_scale, measured_pops(n)), r


# ------------------------------------------------------------------ K3: row M own reproduced
k3 = max(abs(own_off(n, A0[ft])[0] - J28b["rows"]["M own"][ft]["per"][f"NGC{n}"]) for ft in FOOTS for n in CEN)
check("K3 CFG528b machinery reproduces its committed row M own offsets (both footings) to 1e-6", k3 <= 1e-6, f"max |d| {k3:.1e}")
# K4: kernel-swap path with nu_mono itself is an identity
KERN["nu_mono"] = lambda y: NU0(y)
k4 = max(abs(own_off(n, A0[ft])[0] - J28b["rows"]["M own"][ft]["per"][f"NGC{n}"]) for ft in FOOTS for n in CEN)
KERN["nu_mono"] = NU0
check("K4 kernel swap with nu_mono itself reproduces row M own exactly", k4 == 0.0, f"max |d| {k4:.1e}")


def eps_of(o):
    return 10 ** (2 * o) - 1


def sig_eps(o, s):
    return 2 * math.log(10) * 10 ** (2 * o) * s


if not MUTATE:
    # ------------------------------------------------------------------ geometry and the common quantity
    P("\n== geometry: outer GC bins, r_M from the K0 stellar mass (stars only) ==")
    GEO = {}
    for ft in FOOTS:
        for n in CEN:
            g, gN, M, eps_in = build(n, A0[ft])
            rM = math.sqrt(G * M * MSUN / A0[ft]) / KPC
            Ro = B[n]["Rb"][B[n]["outer"]]
            GEO[f"NGC{n}|{ft}"] = dict(logMs_table=GAL[n]["lMs"], logM_K0=math.log10(M), rM_kpc=rM, R_outer_kpc=Ro.tolist(),
                                      R_min=float(Ro.min()), R_max=float(Ro.max()), R_mean=float(Ro.mean()),
                                      r_over_rM=[float(Ro.min() / rM), float(Ro.max() / rM)])
            P(f"  NGC{n} [{ft:9s}] log M* (table) {GAL[n]['lMs']:.2f}, K0 {math.log10(M):.2f}; r_M {rM:.1f} kpc; outer R {Ro.min():.1f}-{Ro.max():.1f} kpc "
              f"(mean {Ro.mean():.1f}); r/r_M {Ro.min() / rM:.2f}-{Ro.max() / rM:.2f}")
    RES["geometry"] = GEO

    P("\n== common quantity eps = 10^(2 o) - 1 (per galaxy, class) ==")
    EPS = {}
    for row in ("J joint best case", "M own", "M K0"):
        for ft in FOOTS:
            r = J28b["rows"][row][ft]
            per = {n: dict(o=r["per"][f"NGC{n}"], sig_o=SIG[(n, ft)], eps=eps_of(r["per"][f"NGC{n}"]),
                           sig_eps=sig_eps(r["per"][f"NGC{n}"], SIG[(n, ft)])) for n in CEN}
            cls = dict(o=r["mean"], sig_o=r["err"], eps=eps_of(r["mean"]), sig_eps=sig_eps(r["mean"], r["err"]))
            cls["Z"] = cls["eps"] / cls["sig_eps"]
            three = [n for n in CEN if n != 4374]
            o3 = float(np.mean([r["per"][f"NGC{n}"] for n in three])); s3 = math.sqrt(sum(SIG[(n, ft)] ** 2 for n in three)) / 3
            cls3 = dict(o=o3, sig_o=s3, eps=eps_of(o3), sig_eps=sig_eps(o3, s3)); cls3["Z"] = cls3["eps"] / cls3["sig_eps"]
            ssys = math.sqrt(sum(SIG[(n, ft)] ** 2 + 0.05 ** 2 for n in CEN)) / 4
            clsS = dict(o=r["mean"], sig_o=ssys, eps=eps_of(r["mean"]), sig_eps=sig_eps(r["mean"], ssys)); clsS["Z"] = clsS["eps"] / clsS["sig_eps"]
            EPS[f"{row}|{ft}"] = dict(per={f"NGC{n}": v for n, v in per.items()}, class4=cls, class3_no4374=cls3, class4_sys005=clsS)
            P(f"  {row:18s} [{ft:9s}] " + "; ".join(f"{n}: {v['eps']:+.3f}+-{v['sig_eps']:.3f}" for n, v in per.items())
              + f" | class {cls['eps']:+.3f}+-{cls['sig_eps']:.3f} (Z {cls['Z']:+.1f}); 3-gal {cls3['eps']:+.3f}+-{cls3['sig_eps']:.3f}; "
              f"with 0.05 dex sys {clsS['eps']:+.3f}+-{clsS['sig_eps']:.3f} (Z {clsS['Z']:+.1f})")
    RES["eps"] = EPS
    RES["SS"] = {ft: EPS[f"J joint best case|{ft}"]["class4"]["Z"] >= 2 for ft in FOOTS}
    P(f"  SS (J class eps >= 2 sigma): {RES['SS']}")

    P("\n== per outer bin, row M own: eps_bin = (sigma_obs / sigma_pred)^2 - 1 ==")
    PB = {}
    for ft in FOOTS:
        for n in CEN:
            g = build(n, A0[ft], **READ["own"])[0]
            s = sig_multi(B[n]["Rb"], g, measured_pops(n)); o = B[n]["outer"]
            e = (B[n]["Sb"][o] / s[o]) ** 2 - 1
            PB[f"NGC{n}|{ft}"] = dict(R=B[n]["Rb"][o].tolist(), eps=e.tolist())
            P(f"  NGC{n} [{ft:9s}] " + " ".join(f"{R:.0f}kpc:{x:+.2f}" for R, x in zip(B[n]["Rb"][o], e)))
    RES["per_bin_M_own"] = PB

    # ------------------------------------------------------------------ (a) the same M* shifts on the JAM-law ceiling
    P("\n== (a) M* x 10^delta on the JAM-law ceiling, row M own (admissible if inner JAM excess eps_in <= 0.06 dex, CFG528) ==")
    Aa = {}
    imf = lambda lms: 0.25 * min(max((lms - 10.3) / 1.0, 0.0), 1.0)
    for ft in FOOTS:
        for dl in (0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, "IMF"):
            row = {}
            for n in CEN:
                d_ = imf(GAL[n]["lMs"]) if dl == "IMF" else dl
                o0 = own_off(n, A0[ft])[0]; o1, r1 = own_off(n, A0[ft], mmult=10 ** d_)
                row[f"NGC{n}"] = dict(delta=d_, offset=o1, d_offset=o1 - o0, eps_in=r1[3], admissible=bool(r1[3] <= 0.06))
            Aa[f"{dl}|{ft}"] = row
            P(f"  delta {str(dl):5s} [{ft:9s}] " + "; ".join(f"{k[3:]}: d_off {v['d_offset']:+.3f}, eps_in {v['eps_in']:+.3f} "
                                                         f"{'adm' if v['admissible'] else 'INADM'}" for k, v in row.items()))
    RES["a"] = Aa

    # ------------------------------------------------------------------ (d) kernel swap
    P("\n== (d) kernel swap in calibration + field, a0 x CFG468 SPARC ratio; row M own; delta added to J (declared approximation) ==")
    Dk = {}
    for k, fn in (("simple", lambda y: 0.5 + np.sqrt(0.25 + 1.0 / np.maximum(np.asarray(y, float), 1e-300))),
                  ("standard", lambda y: np.exp(0.5 * np.arcsinh(0.5 * np.asarray(y, float))) / np.sqrt(np.maximum(np.asarray(y, float), 1e-300)))):
        for t in ("T-free", "T-fix"):
            rat = J468["sparc"]["kernels"][f"nu_{k}"][t]["a0"] / J468["sparc"]["kernels"]["nu_mono"][t]["a0"]
            for ft in FOOTS:
                KERN["nu_mono"] = fn
                try:
                    o1 = {n: own_off(n, A0[ft] * rat)[0] for n in CEN}
                finally:
                    KERN["nu_mono"] = NU0
                o0 = {n: J28b["rows"]["M own"][ft]["per"][f"NGC{n}"] for n in CEN}
                dmean = float(np.mean([o1[n] - o0[n] for n in CEN]))
                Jm = J28b["rows"]["J joint best case"][ft]["mean"] + dmean
                Dk[f"{k}|{t}|{ft}"] = dict(a0_ratio=rat, d_offset={f"NGC{n}": o1[n] - o0[n] for n in CEN}, d_mean=dmean, J_mean_shifted=Jm,
                                           eps_J=eps_of(Jm), sig_eps_J=sig_eps(Jm, J28b["rows"]["J joint best case"][ft]["err"]))
                P(f"  nu_{k:8s} {t:6s} (a0 x {rat:.4f}) [{ft:9s}] d_off " + " ".join(f"{n}:{o1[n] - o0[n]:+.3f}" for n in CEN)
                  + f" -> J class eps {eps_of(Jm):+.3f}+-{Dk[f'{k}|{t}|{ft}']['sig_eps_J']:.3f}")
    RES["d"] = Dk

    # ------------------------------------------------------------------ mechanism M-a: maximal contraction (stars as a point)
    P("\n== mechanism M-a: stars collapsed to a point (maximal contraction; JAM calibration unchanged), row M own ==")
    Ma = {}
    for ft in FOOTS:
        for n in CEN:
            ah = B[n]["ah"]
            o0 = own_off(n, A0[ft])[0]
            B[n]["ah"] = 1e-6
            try:
                o1 = own_off(n, A0[ft])[0]
            finally:
                B[n]["ah"] = ah
            eJ = eps_of(J28b["rows"]["J joint best case"][ft]["per"][f"NGC{n}"])
            sup = 10 ** (-2 * (o1 - o0)) - 1
            Ma[f"NGC{n}|{ft}"] = dict(d_offset=o1 - o0, eps_supplied=sup, eps_required_J=eJ, fraction=(sup / eJ if eJ > 0 else None))
            P(f"  NGC{n} [{ft:9s}] d_offset {o1 - o0:+.4f} -> eps supplied {sup:+.4f} vs required (J) {eJ:+.3f}")
    RES["mech_Ma"] = Ma
    RES["mech_Mc_census_CFG528"] = {k: dict(r_edge_kpc=v["r_edge_kpc"], R_out_kpc=v["R_out_kpc"], binds=v["binds"]) for k, v in J28["census"].items()}
    RES["template_gas_multiplier_CFG528"] = J28["null_gas"]
    P("  M-c (CFG528 census): r_edge " + ", ".join(f"{k}: {v['r_edge_kpc']:.0f} kpc (R_out {v['R_out_kpc']:.0f}, binds {v['binds']})"
                                                   for k, v in J28["census"].items() if k.endswith("|own")))
else:
    P("\n== MUTATE ==")
    mu = 0.0; me = 0.0
    for ft in FOOTS:
        for n in CEN:
            o0, _ = own_off(n, A0[ft]); o1, _ = own_off(n, A0[ft], g_scale=1.5)
            mu = max(mu, abs((o0 - o1) - 0.5 * math.log10(1.5)))
            me = max(me, abs((10 ** (2 * (o0 - o1)) - 1) - 0.5))
    check("MU5 g -> 1.5 g: every row-M-own offset drops by 0.5 log10 1.5 and the eps mapping returns 0.5, to 1e-6", mu < 1e-6 and me < 1e-6,
          f"max |d offset| {mu:.1e}; max |d eps| {me:.1e}")

RES["checks"] = CHK
RES["elapsed_s"] = round(time.time() - T0, 1)
nlb = sum(1 for c_ in CHK.values() if c_["load_bearing"] and not c_["ok"])
P(f"\n{sum(c_['ok'] for c_ in CHK.values())}/{len(CHK)} checks pass; elapsed {RES['elapsed_s']} s")
json.dump(RES, open(os.path.join(HERE, f"cfg531_sluggs_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg531_sluggs{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nlb else 0)

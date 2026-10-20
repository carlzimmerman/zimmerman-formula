#!/usr/bin/env python3
"""CFG915: population-label (history) mobility H-POP against the merger (M), galaxy (G) and dwarf-clump (D) constraints.
Criteria: FROZEN_CRITERIA.md (014b7ba1d, committed alone before this script).  HYPOTHESIS TEST.

H-POP: two labels of one cold medium.  t = bound into a structure at its formation (alpha_t = 0, collisionless, retained);
f = arrived later via catchment inflow (alpha_f in {0.5, 1.0}).  Rules: L0 (half-mass formation snapshot; primary) and
LC (capture on settling).  NOTE the naming clash with the record (FROZEN_CRITERIA.md section 1): H-POP's t is the record's
untethered/collisionless class, H-POP's f the record's settling class.

Run:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg915.py                 -> cfg915.out, cfg915_results.json        (exit 0)
      CFG915_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg915.py  -> cfg915_MUTATE.out, cfg915_results_MUTATE.json
                                                                          (exit 1 when the tooth bites)
Read-only: CFG598 cfg598_lib (P0 drift PDE, MW and grid hosts; flux step copied with one cell-mass array per label);
result JSONs of CFG623, 641, 598, 542, 882, 889 (parts), 726, 777, 827, 829, 843, 845, 860, 880, 883, 890.
Nothing downloaded; no other lane edited.  One core; each process < 1 GB.
kappa = 1/2 FITTED; footings never pooled; cold energy is real gravitating mass; no particle species; not theory closed."""
import os, sys, json, math, time, io, contextlib
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
MUT = os.environ.get("CFG915_MUTATE", "") == "1"; SUF = "_MUTATE" if MUT else ""
OUT = []


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


sys.path.insert(0, os.path.join(LANES, "CFG598_settling_front_partial"))
with contextlib.redirect_stdout(io.StringIO()):
    import cfg598_lib as C                                   # noqa: E402  (read-only)

T0 = time.time()
FOOTS = ("can", "alt"); FL = {"can": "canonical", "alt": "alt"}
GK, A0K, TU = C.GK, C.A0K, C.TU_GYR
ALPHAS_F = (0.5, 1.0)
X_FORM = 0.5                                                  # L0 formation convention (flagged)
R_CORE = 200.0                                                # kpc, CFG623 window scale
WALL = 290.0                                                  # s per PDE run (guard; < 5 min)
rd = lambda p: json.load(open(os.path.join(LANES, p)))
CACHE_F = os.path.join(HERE, "cfg915_runs_cache.json")
CACHE = json.load(open(CACHE_F)) if os.path.exists(CACHE_F) else {}
RES = dict(lane="CFG915", criteria="014b7ba1d", mutate=MUT, label="HYPOTHESIS TEST",
           settings=dict(kappa="1/2 FITTED", footings=C.A0SI, alpha_f=ALPHAS_F, alpha_t=0.0, X_form=X_FORM, R_core_kpc=R_CORE))

P("CFG915  population-label (history) mobility H-POP vs mergers / galaxies / dwarf clumps   criteria 014b7ba1d   HYPOTHESIS TEST")
P("  kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; cold energy real mass; no species; not theory closed.")
P("  naming: t = H-POP 'tethered' (bound at formation, alpha_t = 0) = the record's untethered/collisionless class;")
P("          f = H-POP 'free' (later arrival, alpha_f 0.5/1.0) = the record's settling class.")
P()

# ================================================================================================= 1. K-tests (record numbers)
K = {}


def kline(name, ok, msg):
    K[name] = dict(pass_=ok if isinstance(ok, str) else bool(ok), msg=msg)
    P(f"{name}: {msg} -> {ok if isinstance(ok, str) else ('PASS' if ok else 'FAIL')}")


R623 = rd("CFG623_merger_stopwatch_v5/cfg623_results.json")["cells"]
bobs = {}
for f in FOOTS:
    vals = []
    for a in ("0", "0.1", "0.3", "inf"):
        c = R623[f"{a}_{f}"]
        if c.get("beta_bar") is not None and c.get("Z_H") is not None:
            vals.append(c["beta_bar"] - 0.07 * c["Z_H"])
    bobs[f] = vals
k = (all(R623[f"0_{f}"]["status"] == "ALLOWED" for f in FOOTS)
     and all(R623[f"{a}_{f}"]["status"] == "EXCLUDED" for a in ("0.1", "0.3", "inf") for f in FOOTS)
     and abs(R623["0.03_can"]["Z_B"] - 3.12) <= 0.01 and abs(R623["0.03_alt"]["Z_B"] - 2.65) <= 0.01
     and all(max(v) - min(v) <= 0.005 for v in bobs.values()))
kline("K-M1", k, f"CFG623 alpha 0 ALLOWED both, 0.1/0.3/inf EXCLUDED both, Z_B(0.03) {R623['0.03_can']['Z_B']:+.2f}/"
      f"{R623['0.03_alt']['Z_B']:+.2f}; beta_obs = beta_bar - 0.07 Z_H over scorable nodes: "
      + "; ".join(f"{f} {min(v):+.4f}..{max(v):+.4f}" for f, v in bobs.items()))
R641 = rd("CFG641_hcb_gate_merger/cfg641_results.json")
pr = R641["progenitors"]["RN_can_main"]; res_share = pr["reservoir"] / (pr["reservoir"] + pr["settled"])
k = (all(s == "ALLOWED" for s in R641["arms"]["S"]["status"].values())
     and all(s == "EXCLUDED" for s in R641["arms"]["P"]["status"].values())
     and abs(R641["T_G"]["gated_off_frac_window"] - 0.9996) <= 1e-4 and abs(res_share - 0.87) <= 0.01
     and len(R641["arms"]["S"]["status"]) == len(R641["arms"]["P"]["status"]))
kline("K-M2", k, f"CFG641 arm S {sorted(set(R641['arms']['S']['status'].values()))} over {len(R641['arms']['S']['status'])} cells, "
      f"arm P {sorted(set(R641['arms']['P']['status'].values()))}; gated off {R641['T_G']['gated_off_frac_window']:.4f}; "
      f"RN main reservoir share {res_share:.3f}")
R598 = rd("CFG598_settling_front_partial/cfg598_results.json")
M598 = R598["MW"]
k = (abs(M598["P0|can|0.25"]["min_q"] - 0.9842) <= 1e-4 and abs(M598["P0|alt|0.25"]["min_q"] - 0.9849) <= 1e-4
     and abs(M598["P0|can|0.5"]["min_q"] - 0.9928) <= 1e-4 and abs(M598["P0|alt|0.5"]["min_q"] - 0.9930) <= 1e-4)
kline("K-G1", k, f"CFG598 MW P0 min q 0.25: {M598['P0|can|0.25']['min_q']:.4f}/{M598['P0|alt|0.25']['min_q']:.4f}, "
      f"0.5: {M598['P0|can|0.5']['min_q']:.4f}/{M598['P0|alt|0.5']['min_q']:.4f}")
R542 = rd("CFG542_dissipative_action/cfg542_results.json")["K9_dispersion"]
am1, amc = R542["alpha_max_beta1_q1"]["Pb"], R542["alpha_max_beta1_q_cosmic"]["Pb"]
kline("K-C", abs(am1 - 1.0) <= 1e-3 and abs(amc - 1.1864) <= 1e-3, f"CFG542 alpha_max {am1:.4f} (q = 1), {amc:.4f} (q = 1 - f_b)")
R882 = rd("CFG882_clump_retention_equations/cfg882_results.json")["V1"]
ac = [R882[f][h]["alpha_c"] for f in R882 for h in ("H1", "H2", "H3")]
a50 = [R882[f][h]["alpha50"] for f in R882 for h in ("H1", "H2", "H3")]
ALPHA_C = max(ac)
kline("K-D1", abs(max(ac) - 1.37e-3) <= 0.01e-3 and abs(min(a50) - 6.2e-4) <= 0.1e-4 and abs(max(a50) - 1.02e-3) <= 0.01e-3,
      f"CFG882 alpha_c max {max(ac):.3e}; alpha_50 {min(a50):.2e}..{max(a50):.2e}")
at50 = {}
for part in ("G1a", "G1b", "G2a", "G2b"):
    for key, v in rd(f"CFG889_gated_kinetic_stability/parts/part_{part}.json").items():
        if key.startswith("G|") and key.endswith("|clump"):
            at50[key] = float(key.split("|")[3][1:]) * v["t50"]
ALPHA_DG = min(at50.values()) / 12000.0
kline("K-D2", len(at50) == 8 and abs(min(at50.values()) - 105.5) <= 1 and abs(max(at50.values()) - 147.5) <= 1,
      f"CFG889 alpha*t50 {min(at50.values()):.1f}..{max(at50.values()):.1f} Myr over {len(at50)} cells -> alpha_D,gated "
      f"{min(at50.values()) / 12000:.2e}..{max(at50.values()) / 12000:.2e}")
# record numbers used in D and the corollaries
R827 = rd("CFG827_dwarf_age_sfh_ml/cfg827_results.json")
E827 = np.array([v["E_SFH"] for v in R827["rows"].values() if not v["train"]])
rho827 = R827["scores"]["-1.31"]["rho"]
kline("K-R827", len(E827) == 28 and int((E827 > 0).sum()) == 25 and abs(E827.mean() - 0.375) <= 0.005 and abs(rho827 - 0.089) <= 0.005,
      f"CFG827 OOS N {len(E827)}, above {int((E827 > 0).sum())}, mean E {E827.mean():+.4f}, rho {rho827:+.3f}")
R880 = rd("CFG880_clump_sigma_universality/cfg880_results.json")
kline("K-R880", all(abs(R880[f]["primary"]["s_hat"] - 0.38) <= 1e-9 for f in ("canonical", "alt")),
      f"CFG880 s_hat {R880['canonical']['primary']['s_hat']}/{R880['alt']['primary']['s_hat']} ({R880['cls']})")
R843 = rd("CFG843_mw_vs_m31_satellites/cfg843_results.json")["all"]
kline("K-R843", abs(R843["c"] - 0.055) <= 0.001 and abs(R843["sc"] - 0.117) <= 0.001, f"CFG843 c {R843['c']:+.4f} +- {R843['sc']:.4f} ({R843['cls']})")
R845 = rd("CFG845_hprim_vs_sparc_dwarfs/cfg845_results.json")
kline("K-R845", abs(R845["D"] + 0.273) <= 0.001 and abs(R845["sD"] - 0.026) <= 0.001, f"CFG845 D {R845['D']:+.4f} +- {R845['sD']:.4f} ({R845['cls']})")
R860 = rd("CFG860_stripping_vs_isolated_dwarfs/cfg860_results.json")
if "canonical|base" in R860["variants"]:
    b = R860["variants"]["canonical|base"]
    kline("K-R860", abs(b["ac0"] - 0.285) <= 0.005 and abs(b["acG"] - 0.370) <= 0.005, f"CFG860 base a+c0 {b['ac0']:+.3f}, a+cG {b['acG']:+.3f}")
else:
    near = R860["variants"]["canonical|cut 350 kpc"]
    kline("K-R860", "PARTIAL", f"CFG860 canonical base not stored (README +0.285 +- 0.108 / +0.370 +- 0.073); nearest stored "
          f"'canonical|cut 350 kpc' a+c0 {near['ac0']:+.3f} +- {near['sac0']:.3f}, a+cG {near['acG']:+.3f} +- {near['sacG']:.3f}; "
          f"class {R860['cls']}")
R829 = rd("CFG829_lensing_low_g_vs_dwarf_excess/cfg829_results.json")
Ab, Ar = R829["canonical|nu_e|blue (u-r<2.5)"]["window"], R829["canonical|nu_e|red (u-r>2.5)"]["window"]
kline("K-R829", abs(Ab["A"] - 1.016) <= 0.001 and abs(Ab["sA"] - 0.086) <= 0.001 and abs(Ar["A"] - 1.587) <= 0.001,
      f"CFG829 blue A {Ab['A']:.3f} +- {Ab['sA']:.3f}, red A {Ar['A']:.3f} +- {Ar['sA']:.3f}")
R883 = rd("CFG883_no_cooling_systems/cfg883_results.json")["T1"]["summary"]["foot"]
kline("K-R883", all(R883[f]["n_NC"] == 6 and R883[f]["n_CP_robust"] == 1 for f in ("canonical", "alt")),
      f"CFG883 NO CLUMP {R883['canonical']['n_NC']}/{R883['alt']['n_NC']}, robust CLUMP PRESENT {R883['canonical']['n_CP_robust']}/"
      f"{R883['alt']['n_CP_robust']} ({R883['canonical']['CP'][0]})")
R890 = rd("CFG890_dwarf_description_comparison/cfg890_results.json")
VX = {f: R890[FL[f]]["models"]["M5"]["phys"]["V_x"] for f in FOOTS}
kline("K-R890", abs(VX["can"] - 6.48) <= 0.01 and abs(VX["alt"] - 6.29) <= 0.01, f"CFG890 M5 V_x {VX['can']:.3f}/{VX['alt']:.3f} km/s")
R726 = rd("CFG726_merger_memory/cfg726_results.json")
z726 = {f"{t}|{f}|{b}": R726[t][f"s|{FL[f]}|{b}"]["Z_outer"] for t in ("T_R", "T_A") for f in FOOTS for b in ("primary", "Nx0.5")}
want = {"T_R|can|primary": -3.63, "T_R|alt|primary": -4.05, "T_A|can|primary": -4.83, "T_A|alt|primary": -5.19,
        "T_R|can|Nx0.5": -2.50, "T_R|alt|Nx0.5": -3.19, "T_A|can|Nx0.5": -3.13, "T_A|alt|Nx0.5": -3.59}
k = all(abs(z726[x] - want[x]) <= 0.01 for x in want) and all(v.startswith("H-MM FAILS") for v in R726["verdict"].values())
kline("K-R726", k, "CFG726 Z_outer " + ", ".join(f"{x} {z726[x]:+.2f}" for x in want) + f"; verdict {R726['verdict']['s'][:12]}")
R777 = rd("CFG777_relic_clusters/cfg777_results.json")
P(f"(report) CFG777 frozen relic verdict s/mono: {R777['verdict']['s']}/{R777['verdict']['mono']} (condensed-baryon framework)")
P()


# ================================================================================================= 2. two-population G model
class Run2(C.Run):
    """CFG598 P0 drift PDE with one cell-mass array per label (t, f).  Deficit, D(<r) and tau use the TOTAL cold mass; each
    label drifts with its own alpha; flux / dt / last-trace rules copied from cfg598_lib.Run.flux_step per label."""

    def flux2(self, mt, mf, at, af, rta, dtmax):
        N, V, A, rf = self.N, self.V, self.A, self.rf
        cellB = rf[:-1] < rta
        m = mt + mf
        rho = m / V
        d = np.where(cellB, np.maximum(self.mph / V - rho, 0.0), 0.0)
        Md = np.concatenate([[0.0], np.cumsum(d * V)])
        dpsi = GK * Md / rf ** 2
        don = slice(1, N)
        pops = []; dtc = np.inf; gam = 0.0
        for X, mX, aX in (("f", mf, af), ("t", mt, at)):
            if not (aX > 0 and np.isfinite(aX)):
                continue
            live = mX > self.thr
            tau = np.where(live, 1.0 / np.sqrt(4 * math.pi * GK * np.maximum(rho + self.rhob, 1e-300)), 0.0)
            ok = live[don] & cellB[don]
            v = aX * tau[don] * dpsi[1:N]
            rhoX = mX / V
            flux = rhoX[don] * v * A[1:N]
            with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
                dtcX = np.where(ok & (v > 0), 0.4 * V[don] / np.maximum(A[1:N] * v, 1e-300), np.inf).min()
            sel = live & cellB
            gX = float((4 * math.pi * GK * rho * tau * aX)[sel].max()) if sel.any() else 0.0
            dtc = min(dtc, dtcX); gam = max(gam, gX)
            pops.append((X, mX, ok, flux, v))
        dt = min(dtc, 0.2 / gam if gam > 0 else np.inf, dtmax)
        new = {"t": mt, "f": mf}; vm = 0.0
        for X, mX, ok, flux, v in pops:
            tr = np.where(ok, np.minimum(flux * dt, mX[don]), 0.0)
            tr = np.where(ok & (mX[don] - tr < self.thr[don]) & (tr > 0), mX[don], tr)
            m2 = mX.copy(); m2[1:] -= tr; m2[:-1] += tr
            new[X] = m2
        mtot = new["t"] + new["f"]
        for X, mX, ok, flux, v in pops:
            sig = ok & (mtot[don] >= 1e-3 * self.mph[don])
            vm = max(vm, float(np.max(np.where(sig, v, 0.0))) if sig.any() else 0.0)
        return new["t"], new["f"], dt, vm

    def settle_inf_X(self, mO, mX, rta):
        """alpha_X -> inf for one label (other label mO fixed): CFG598 settle_inf with need_X = max(mph, mO + mX) - mO."""
        cellB = self.rf[:-1] < rta; nB = int(cellB.sum())
        m = mO + mX
        q_ok = m[:nB] >= self.mph[:nB] * (1 - 1e-12)
        i0 = int(np.argmin(q_ok)) if not q_ok.all() else nB
        if i0 >= nB:
            return mX
        Mmob = float(mX[i0:nB].sum())
        need = np.maximum(self.mph[i0:nB], m[i0:nB]) - mO[i0:nB]
        cum = np.cumsum(need)
        new = mX.copy(); new[i0:nB] = 0.0
        j = int(np.searchsorted(cum, Mmob))
        if j >= len(need):
            new[i0:nB] = need; new[nB - 1] += Mmob - cum[-1]
        else:
            new[i0:i0 + j] = need[:j]
            new[i0 + j] = Mmob - (cum[j - 1] if j > 0 else 0.0)
        return new

    def capture(self, mt, mf, rta, tol):
        """LC: f -> t in cells inside B that are settled and have no deficit inside.  tol = relative settled tolerance
        (frozen: 1e-12, the record's settle_inf test; post-freeze variant LC-tol: 0.01 locally and in the inner cumulative)."""
        cellB = self.rf[:-1] < rta
        m = mt + mf
        short = np.maximum(self.mph - m, 0.0)
        cellset = m >= self.mph * (1 - tol)
        if tol <= 1e-9:
            inner = np.concatenate([[0.0], np.cumsum(np.where(cellset, 0.0, short))])[:-1]
            noinner = inner == 0.0
        else:
            inner = np.concatenate([[0.0], np.cumsum(short)])[:-1]
            Mph_in = np.concatenate([[0.0], np.cumsum(self.mph)])[:-1]
            noinner = inner <= tol * np.maximum(Mph_in, 1e-300)
        cap = cellB & cellset & noinner & (mf > 0)
        if cap.any():
            mt = mt.copy(); mf = mf.copy(); mt[cap] += mf[cap]; mf[cap] = 0.0
        return mt, mf

    def run2(self, af, at=0.0, rule="REF", t_form=None, cap_tol=1e-12, maxsteps=4_000_000, dtcap_gyr=0.01):
        H = self.H; tend = H.t0
        mf = self.initial(); mt = np.zeros(self.N)
        self.thr = 1e-14 * H.Mcat / self.N * np.ones(self.N)
        t = H.t_s; k = 0; ndep = len(self.dep_t); n = 0; vmax = 0.0
        dtcap = dtcap_gyr / TU; wall0 = time.time(); walled = False
        inf_f = not np.isfinite(af); inf_t = not np.isfinite(at)
        snapped = rule not in ("L0", "L0S")
        self.snap_info = None
        def snap(mt, mf):
            cB = self.rf[:-1] < H.r_ta(t_form)
            m = mt + mf
            with np.errstate(divide="ignore", invalid="ignore"):
                q = np.where(self.mph > 0, m / self.mph, np.inf)
            low = np.where(cB & (q < 0.99))[0]
            j = int(low[0]) if low.size else int(cB.sum())
            interior = np.zeros(self.N, bool); interior[:j] = True; interior &= cB
            # POST HOC diagnostic: where the formation snapshot's mass sits (settled interior vs unsettled, in transit)
            self.snap_info = dict(t_form_gyr=float(t * TU), rta_form_kpc=float(H.r_ta(t_form)), r_settled_edge_kpc=float(self.rf[j]),
                                  M_snap=float(m[cB].sum()), M_snap_interior=float(m[interior].sum()),
                                  frac_in_transit=float(1 - m[interior].sum() / max(m[cB].sum(), 1e-300)))
            sel = cB if rule == "L0" else interior          # L0S (POST HOC variant): only the settled interior is relabelled t
            mt = mt.copy(); mf = mf.copy(); mt[sel] += mf[sel]; mf[sel] = 0.0
            return mt, mf
        if not snapped and t_form <= t + 1e-12:
            mt, mf = snap(mt, mf); snapped = True
        moving = (af > 0 and np.isfinite(af)) or (at > 0 and np.isfinite(at))
        while t < tend - 1e-12:
            xb = H.X_ta(t)
            if abs(xb / self.xb - 1) > 2e-3:
                self.set_baryons(xb)
            rta = H.r_ta(t)
            nxt = self.dep_t[k] if k < ndep else np.inf
            dtmax = min(dtcap, tend - t, max(nxt - t, 1e-9))
            if not snapped:
                dtmax = min(dtmax, max(t_form - t, 1e-9))
            if not moving:
                dt = dtmax
            else:
                mt, mf, dt, vm = self.flux2(mt, mf, at, af, rta, dtmax); vmax = max(vmax, vm)
            if rule == "LC":
                mt, mf = self.capture(mt, mf, rta, cap_tol)
            t += dt; n += 1
            while k < ndep and self.dep_t[k] <= t + 1e-12:
                mf = mf + self.deposit_profile(self.dep_R[k], self.dep_m[k]); k += 1
            if inf_f:
                mf = self.settle_inf_X(mt, mf, H.r_ta(t))
            if inf_t:
                mt = self.settle_inf_X(mf, mt, H.r_ta(t))
            if not snapped and t >= t_form - 1e-12:
                mt, mf = snap(mt, mf); snapped = True
            if rule == "LC":
                mt, mf = self.capture(mt, mf, H.r_ta(t), cap_tol)
            if n >= maxsteps:
                break
            if (n & 1023) == 0 and time.time() - wall0 > WALL:
                walled = True; break
        transit = float(self.dep_m[k:].sum())
        self.set_baryons(H.X_ta(t))
        m = mt + mf
        return dict(mt=mt, mf=mf, m=m, t=t, n=n, hit_cap=bool(n >= maxsteps and t < tend - 1e-9), walled=walled,
                    mass_err=abs(m.sum() + transit - H.Mcat) / H.Mcat, vmax_over_Vf=vmax / self.Vf0, wall_s=time.time() - wall0)


HOSTS = {}


def host(key):
    if key not in HOSTS:
        with contextlib.redirect_stdout(io.StringIO()):
            HOSTS[key] = C.Host(None, mw=True) if key == "MW" else C.Host(float(key))
    return HOSTS[key]


def akey(a):
    return "inf" if not np.isfinite(a) else f"{a:g}"


def gt(hkey, foot, rule, af, at=0.0, tform="X05", cap_tol=1e-12):
    """one PDE run, cached by its full setting; returns small diagnostics."""
    key = f"{hkey}|{foot}|{rule}|af{akey(af)}|at{akey(at)}|{tform}|tol{cap_tol:g}"
    if key in CACHE:
        return CACHE[key]
    H = host(hkey)
    R = Run2(H, foot, "P0", N=300)
    tf = None
    if rule in ("L0", "L0S"):
        tf = float(np.interp(X_FORM, H.X, H.t_ta)) if tform == "X05" else H.t_s
    o = R.run2(af, at, rule, tf, cap_tol)
    m, mt, mf = o["m"], o["mt"], o["mf"]
    rf = R.rf
    with np.errstate(divide="ignore", invalid="ignore"):
        q = np.where(R.mph > 0, m / R.mph, np.inf)
    out = dict(n=o["n"], hit_cap=o["hit_cap"], walled=o["walled"], mass_err=o["mass_err"], wall_s=round(o["wall_s"], 2),
               vmax_over_Vf=o["vmax_over_Vf"], t_form_gyr=None if tf is None else tf * TU, rta0_kpc=H.rta0,
               t_frac=float(mt.sum() / m.sum()), snap_info=R.snap_info)
    if hkey == "MW":
        sel = rf[1:] <= 30.0
        mph = R.mph[sel]
        out.update(min_q=float(np.min(q[sel][mph > 0])), max_q=float(np.max(q[sel][mph > 0])),
                   Mc_over_Mph=float(m[sel].sum() / R.mph[sel].sum()), f_share_30=float(mf[sel].sum() / m[sel].sum()))
        out["settled"] = out["min_q"] >= 0.99; out["overfilled"] = out["Mc_over_Mph"] - 1 > 0.01
        out["i_holds"] = bool(out["settled"] and not out["overfilled"])
        ov = np.maximum(m - R.mph, 0.0); ovt = np.minimum(np.maximum(mt - R.mph, 0.0), ov)
        out["overfill_30"] = float(ov[sel].sum() / R.mph[sel].sum())               # POST HOC: excess mass inside 30 kpc / M_ph
        out["overfill_t_share_30"] = float(ovt[sel].sum() / max(ov[sel].sum(), 1e-300))   # share of that excess carried by t
        bad = np.where(sel & (R.mph > 0) & (q < 0.99))[0]
        out["r_minq_kpc"] = float(R.rc[sel][np.argmin(np.where(mph > 0, q[sel], np.inf))])
        out["n_cells_q_lt_099"] = int(bad.size)
    else:
        d = R.diag(m)
        out.update(S01=d["S"]["0.1"], S05=d["S"]["0.5"], Mc01=d["Mc"]["0.1"], Mc05=d["Mc"]["0.5"])
        for lab, Rr in (("200", R_CORE), ("500", 500.0), ("0.1rta", 0.1 * H.rta0), ("0.05rta", 0.05 * H.rta0)):
            s = rf[1:] <= Rr
            out[f"phi_f_{lab}"] = float(mf[s].sum() / max(m[s].sum(), 1e-300))
            out[f"Mc_{lab}"] = float(m[s].sum()); out[f"q_{lab}"] = float(m[s].sum() / max(R.mph[s].sum(), 1e-300))
    out = {kk: (bool(v) if isinstance(v, (bool, np.bool_)) else v) for kk, v in out.items()}
    CACHE[key] = out
    json.dump(CACHE, open(CACHE_F, "w"), indent=0, sort_keys=True)
    P(f"    run {key}: {o['wall_s']:.1f} s, n {o['n']}" + (" [WALL]" if o["walled"] else "") + (" [CAP]" if o["hit_cap"] else ""))
    return out


def gline(tag, o):
    return (f"{tag}: min q {o['min_q']:.4f} (at {o['r_minq_kpc']:.1f} kpc, {o['n_cells_q_lt_099']} cells < 0.99), "
            f"max q {o['max_q']:.3g}, M_c/M_ph(<30) {o['Mc_over_Mph']:.4f}, f share(<30) {o['f_share_30']:.3f}, "
            f"t share(all) {o['t_frac']:.3f} -> {'(i) holds' if o['i_holds'] else '(i) FAILS'}"
            + (" [WALL-STOPPED]" if o["walled"] else "") + (" [STEP CAP]" if o["hit_cap"] else ""))


# ------------------------------------------------------------------------------------------------ K-G2 / K-G3
P("K-G2 / K-G3: the two-population code with no t (rule REF, all f) against CFG598")
kg2 = []
for f in FOOTS:
    for a in (0.5, 1.0, np.inf):
        o = gt("MW", f, "REF", a)
        ref = M598[f"P0|{f}|{akey(a)}"]
        rel = max(abs(o["min_q"] / ref["min_q"] - 1), abs(o["max_q"] / ref["max_q"] - 1), abs(o["Mc_over_Mph"] / ref["Mc_over_Mph"] - 1))
        kg2.append(rel)
        P(f"  MW {f} alpha {akey(a)}: min q {o['min_q']:.6f} vs {ref['min_q']:.6f}, M_c/M_ph {o['Mc_over_Mph']:.6f} vs "
          f"{ref['Mc_over_Mph']:.6f}; max rel {rel:.2e}")
kline("K-G2", max(kg2) <= 1e-9, f"two-population code (REF) vs CFG598 MW P0 at 0.5, 1, inf, both footings: max rel {max(kg2):.2e}")
kg3 = []
for hk in ("15.0", "14.0"):
    for f in FOOTS:
        o = gt(hk, f, "REF", 0.5)
        ref = R598["runs"][f"{hk}|{f}|P0"]["0.5"]
        rel = max(abs(o["S01"] / ref["S"]["0.1"] - 1), abs(o["S05"] / ref["S"]["0.5"] - 1), abs(o["Mc01"] / ref["Mc"]["0.1"] - 1),
                  abs(o["Mc05"] / ref["Mc"]["0.5"] - 1))
        kg3.append(rel)
        P(f"  host {hk} {f} alpha 0.5: S(0.5 r_ta) {o['S05']:.6e} vs {ref['S']['0.5']:.6e}; max rel {rel:.2e}")
kline("K-G3", max(kg3) <= 1e-9, f"two-population code (REF) vs CFG598 grid hosts log 15, 14 (P0, alpha 0.5): max rel {max(kg3):.2e}")
P()
RES["K"] = K
KALL = all(v["pass_"] is True or v["pass_"] == "PARTIAL" for v in K.values())

# ================================================================================================= 3. G-tests (MW)
AT_SW = 0.0
if not MUT:
    P("G-tests: CFG598 MW P0 with labels (pass = CFG598 (i) on both footings at the same alpha_f in {0.5, 1.0})")
    G = {}
    for rule in ("L0", "LC"):
        for a in (0.5, 1.0, np.inf):
            for f in FOOTS:
                o = gt("MW", f, rule, a)
                G[f"{rule}|{f}|{akey(a)}"] = o
                P("  " + gline(f"{rule} {f} alpha_f {akey(a)}" + (" [bracket]" if not np.isfinite(a) else ""), o))
    for a in (0.5, 1.0):
        for f in FOOTS:
            o = gt("MW", f, "L0", a, tform="X0")
            G[f"L0early|{f}|{akey(a)}"] = o
            P("  " + gline(f"L0-early (t = initial content only) {f} alpha_f {akey(a)} [bracket]", o))
    P("  POST-FREEZE, PRE-RUN variant (no class weight): LC-tol, capture at q >= 0.99 locally with inner cumulative deficit <= 1%")
    for a in (0.5, 1.0):
        for f in FOOTS:
            o = gt("MW", f, "LC", a, cap_tol=0.01)
            G[f"LCtol|{f}|{akey(a)}"] = o
            P("  " + gline(f"LC-tol {f} alpha_f {akey(a)}", o))
    P("  POST HOC diagnostics (added after the first full run; no class weight):")
    for f in FOOTS:
        for a in ALPHAS_F:
            lc, le = G[f"LC|{f}|{akey(a)}"], G[f"L0early|{f}|{akey(a)}"]
            P(f"   PH1 LC (exact capture) vs L0-early {f} alpha_f {akey(a)}: t share {lc['t_frac']:.3f} vs {le['t_frac']:.3f}; min q "
              f"{lc['min_q']:.5f} vs {le['min_q']:.5f}; f share(<30) {lc['f_share_30']:.3f} vs {le['f_share_30']:.3f} "
              "-> exact capture latches only overfilled cells in a growing host")
    for f in FOOTS:
        for a in ALPHAS_F:
            si = G[f"L0|{f}|{akey(a)}"]["snap_info"]
            P(f"   PH2 L0 snapshot {f} alpha_f {akey(a)}: t_form {si['t_form_gyr']:.2f} Gyr, r_ta(t_form) {si['rta_form_kpc']:.0f} kpc, "
              f"settled (q >= 0.99) interior to {si['r_settled_edge_kpc']:.1f} kpc; {si['frac_in_transit']:.3f} of the snapshot mass "
              f"({si['M_snap']:.3e} Msun) is unsettled, in transit, and is frozen")
    for a in ALPHAS_F:
        for f in FOOTS:
            o = gt("MW", f, "L0S", a)
            G[f"L0S|{f}|{akey(a)}"] = o
            P("   PH3 " + gline(f"L0-settled (only the q >= 0.99 interior at t_form becomes t) {f} alpha_f {akey(a)}", o))
    for f in FOOTS:
        for a in ALPHAS_F:
            P(f"   PH4 overfill inside 30 kpc (sum of max(m - m_ph, 0) / M_ph(<30); share carried by t) {f} alpha_f {akey(a)}: "
              + "; ".join(f"{lab} {G[f'{lab}|{f}|{akey(a)}']['overfill_30']:.4f} (t {G[f'{lab}|{f}|{akey(a)}']['overfill_t_share_30']:.2f})"
                          for lab in ("L0", "LC", "L0S", "L0early")))
    GPASS = {}
    for rule in ("L0", "LC"):
        ok_a = [a for a in ALPHAS_F if all(G[f"{rule}|{f}|{akey(a)}"]["i_holds"] and not G[f"{rule}|{f}|{akey(a)}"]["walled"]
                                         for f in FOOTS)]
        GPASS[rule] = ok_a
        P(f"  G({rule}): " + (f"PASS at alpha_f {ok_a}" if ok_a else "FAIL (no alpha_f in {0.5, 1.0} holds (i) on both footings)"))
    RES["G"] = G; RES["G_pass_alpha"] = GPASS
    P()

    # ============================================================================================= 4. M: host label splits + first order
    P("M (a) mapping: CFG623 alpha = 0 ALLOWED and CFG641 arm S (gate off 99.96%) = effectively all cold energy immobile.")
    PHI = {}
    for f in FOOTS:
        c0, ci, c3 = R623[f"0_{f}"], R623[f"inf_{f}"], R623[f"0.3_{f}"]
        bo = float(np.mean(bobs[f])); bmax = bo + 0.14
        PHI[f] = dict(B=(0.295 - c0["f"]) / (ci["f"] - c0["f"]), H=(bmax - c0["beta_bar"]) / (ci["beta_bar"] - c0["beta_bar"]),
                      B03=(0.295 - c0["f"]) / (c3["f"] - c0["f"]), H03=(bmax - c0["beta_bar"]) / (c3["beta_bar"] - c0["beta_bar"]),
                      beta_obs=bo, beta_max=bmax, f0=c0["f"], finf=ci["f"], b0=c0["beta_bar"], binf=ci["beta_bar"])
        P(f"M (b) first-order mixture tolerance {f}: f(0) {c0['f']:+.3f}, f(inf) {ci['f']:+.3f}, beta(0) {c0['beta_bar']:+.3f}, "
          f"beta(inf) {ci['beta_bar']:+.3f}, beta_obs {bo:+.4f} -> phi_lin,B {PHI[f]['B']:.3f}, phi_lin,H {PHI[f]['H']:.3f} "
          f"(with the 0.3 node: {PHI[f]['B03']:.3f}, {PHI[f]['H03']:.3f})")
    RES["phi_lin"] = PHI
    P("M (c) H-POP's mobile fraction in cluster cores (CFG598 grid hosts, P0, t0; point-mass baryons, inherited EPS history):")
    HS = {}
    for rule in ("L0", "LC"):
        for a in ALPHAS_F:
            for hk in ("15.0", "14.0"):
                for f in FOOTS:
                    o = gt(hk, f, rule, a)
                    HS[f"{rule}|{hk}|{f}|{akey(a)}"] = o
                    P(f"  {rule} log {hk} {f} alpha_f {akey(a)}: phi_f(<200 kpc) {o['phi_f_200']:.4f}, (<500 kpc) {o['phi_f_500']:.4f}, "
                      f"(<0.1 r_ta = {0.1 * o['rta0_kpc']:.0f} kpc) {o['phi_f_0.1rta']:.4f}; M_c/M_ph(<200) {o['q_200']:.3f}; "
                      f"t share(all) {o['t_frac']:.3f}" + (" [WALL]" if o["walled"] else ""))
    MCLS = {}
    for rule in ("L0", "LC"):
        use = GPASS[rule] if GPASS[rule] else list(ALPHAS_F)
        per_a = {}
        for a in use:
            per_a[akey(a)] = {f: max(HS[f"{rule}|{hk}|{f}|{akey(a)}"]["phi_f_200"] for hk in ("15.0", "14.0")) for f in FOOTS}
        if GPASS[rule]:
            okc = [a for a in per_a if all(per_a[a][f] <= PHI[f]["H"] for f in FOOTS)]
            lab = "CONSISTENT (first order)" if okc else "UNDERDETERMINED"
        else:
            worst = {f: max(per_a[a][f] for a in per_a) for f in FOOTS}
            lab = "CONSISTENT (first order)" if all(worst[f] <= PHI[f]["H"] for f in FOOTS) else "UNDERDETERMINED"
        MCLS[rule] = dict(label=lab, phi_core=per_a, note="LC t = law-settled profile (direct map to CFG623 alpha 0)" if rule == "LC"
                          else "L0 t = formation snapshot (profile differs from CFG623's progenitors; approximate)")
        P(f"  M({rule}) = {lab}; max phi_f(<200) per alpha_f: " + "; ".join(f"{a}: " + "/".join(f"{per_a[a][f]:.4f}" for f in FOOTS) for a in per_a)
          + f" vs phi_lin,H {PHI['can']['H']:.3f}/{PHI['alt']['H']:.3f}  ({MCLS[rule]['note']})")
    P("M (d) CFG641 (report only): any collisionless t reservoir in the merging cores must trace the baryons (RI allowed, RN "
      "excluded) in the stars-only branch; H-POP does not fix that profile.")
    RES["hosts"] = HS; RES["M"] = MCLS
    P()

    # ============================================================================================= 5. D mapping
    sGa = {f: math.sqrt(GK * A0K[f]) for f in FOOTS}
    L = np.exp(4 * E827)
    D = dict(alpha_t=0.0, alpha_c=ALPHA_C, alpha_D_gated=ALPHA_DG, retention="Gamma_t = alpha_t q/tau = 0 (CFG882 exact law); CFG889 erosion "
             "was drift-driven -> off for t",
             loss_factor=dict(median=float(np.median(L)), p16=float(np.percentile(L, 16)), p84=float(np.percentile(L, 84)),
                              n_le1=int((L <= 1).sum()), N=int(L.size)))
    P(f"D retention: alpha_t = 0 <= alpha_c {ALPHA_C:.2e} and <= alpha_D,gated {ALPHA_DG:.2e}: CFG882 Gamma_t = 0; CFG889's erosion "
      "acted through the drift -> no erosion channel for t in the record's equations (tides aside, CFG838 rho 0.00).")
    P(f"D amount (D-i, deep regime, t-dominated, order of magnitude): loss factor M_b,form/M_b,now = e^(4E) from CFG827's 28 "
      f"out-of-sample dwarfs: median {D['loss_factor']['median']:.2f}, 16-84% {D['loss_factor']['p16']:.2f}-{D['loss_factor']['p84']:.2f}, "
      f"{D['loss_factor']['n_le1']} dwarfs need none (E <= 0); mean E {E827.mean():+.3f} -> e^(4 Ebar) {math.exp(4 * E827.mean()):.2f}")
    MF = {}
    for f in FOOTS:
        inc = VX[f] ** 2 / sGa[f]
        MF[f] = {f"{mn:.0e}": float((math.sqrt(mn) + inc) ** 2) for mn in (1e3, 1e5, 1e7)}
        P(f"D amount from CFG890 M5 V_x {VX[f]:.2f} km/s ({f}): sqrt(M_form) - sqrt(M_now) = {inc:.0f} Msun^1/2 -> M_b,form = "
          + ", ".join(f"{float(mn):.0e}: {MF[f][mn]:.2e} (x{MF[f][mn] / float(mn):.3g})" for mn in MF[f]))
    D["M_form_from_Vx"] = MF
    readings = [
        ("CFG880 per-dwarf scatter (s_hat 0.38)", "needs per-dwarf loss variation: allowed, unmeasured input", "no contradiction"),
        ("CFG827 age independence (rho +0.09)", "no age dependence unless loss tracks age", "no contradiction"),
        ("CFG843 host independence (c +0.055 +- 0.117)", "loss internal / early", "no contradiction"),
        ("CFG883 no clump in 6 globulars (1 robust clump, NGC 1851)", "t ~ 0 for systems formed at g >> a0 or in a host field", "no contradiction (NGC 1851 unexplained)"),
        ("CFG845 SPARC rotating dwarfs on the law (D -0.273 +- 0.026 vs H-PRIM)", "no net loss in gas-rich rotators; excludes D-ii (collapse amount)", "no contradiction for D-i; D-ii EXCLUDED"),
        ("CFG860/873 gas-bearing isolated dwarfs above the law", "requires early loss there too", "prediction (no removed-baryon measure, CFG846)"),
        ("CFG829 blue lenses on the law (A 1.016 +- 0.086), red A 1.587", "loss in red only", "no contradiction"),
    ]
    for r_, need, verdict in readings:
        P(f"  D-i vs {r_}: {need} -> {verdict}")
    D["readings"] = readings
    D["release_variants"] = ("gas-expulsion or stripping release of t frees the overfill, which then drifts at alpha_f >= 0.5 >> alpha_c "
                             f"{ALPHA_C:.2e}: the D-i clump is erased; release is incompatible with H-POP's own D route")
    D["label"] = "CONSISTENT (conditional on alpha_t = 0 and unmeasured formation-epoch baryon masses)"
    P(f"  D(L0) = D(LC) = {D['label']}; release variants: {D['release_variants']}")
    RES["D"] = D
    P()

    # ============================================================================================= 6. corollaries
    C1 = dict(LC=dict(mapping="identity with H-MM: M_b + max(sum T_i, T_rem), T_i = settled progenitor halo to its supply edge",
                      record=f"CFG726 FAILS: T-R OUTER Z {z726['T_R|can|primary']:+.2f}/{z726['T_R|alt|primary']:+.2f}, T-A OUTER Z "
                             f"{z726['T_A|can|primary']:+.2f}/{z726['T_A|alt|primary']:+.2f}, T-E eFEDS (both kernels)",
                      label="CONTRADICTED" if all(v.startswith("H-MM FAILS") for v in R726["verdict"].values()) else "NOT CONTRADICTED"),
              L0=dict(mapping="deep regime, edges beyond r: phi_t = sqrt(X_form) = 0.707 times sum sqrt f_i = CFG726's N_mem x 0.5 bracket",
                      record=f"N x 0.5 fails T-R OUTER Z {z726['T_R|can|Nx0.5']:+.2f}/{z726['T_R|alt|Nx0.5']:+.2f}, T-A OUTER Z "
                             f"{z726['T_A|can|Nx0.5']:+.2f}/{z726['T_A|alt|Nx0.5']:+.2f}", label="AT RISK (approximate mapping)"))
    P(f"C1 merger memory: LC {C1['LC']['label']} ({C1['LC']['mapping']}; {C1['LC']['record']})")
    P(f"                  L0 {C1['L0']['label']} ({C1['L0']['mapping']}; {C1['L0']['record']})")
    ts2 = {k_: R726["T_S2"][k_] for k_ in R726["T_S2"] if k_.startswith("s|canonical")}
    P("C1b minor accretion (CFG726 T-S2, declared vulnerability, unscored): accreted pieces keep their t under both rules -> AT RISK "
      "(disc V x1.04 / x1.12 / x1.37 for 1% / 3% / 10% in 1% pieces, CFG726 README)")
    P(f"C2 frozen relic (CFG777, condensed-baryon framework) {R777['verdict']['s']}: report only (source-dependent).")
    P("C4 CFG747/776: the record's push expels surplus; alpha_t = 0 is the posit that it does not act on t (new assumption).")
    P("C5 CFG722 Q1 (conditional): a ballistic collisionless carrier is a particle species in the identified-carrier dictionary; "
      "H-POP's t inherits this open issue (flagged; no species added here).")
    RES["corollaries"] = dict(C1=C1, C1b="AT RISK", C2=f"report only ({R777['verdict']['s']})", C4="new assumption", C5="flagged")
    P()

    # ============================================================================================= 7. classes
    CLS = {}
    rank = {"CONSISTENT WITH ALL THREE": 0, "UNDERDETERMINED": 1, "CONTRADICTED": 2}
    for rule in ("L0", "LC"):
        why = []
        if not GPASS[rule]:
            gs = "; ".join(f"{f} alpha_f {akey(a)} min q {G[f'{rule}|{f}|{akey(a)}']['min_q']:.4f}, M_c/M_ph {G[f'{rule}|{f}|{akey(a)}']['Mc_over_Mph']:.4f}"
                           for a in ALPHAS_F for f in FOOTS)
            why.append(f"G: breaks CFG598 MW (i) ({gs})")
        if C1[rule]["label"] == "CONTRADICTED":
            why.append(f"C1: breaks CFG726 ({C1[rule]['record']})")
        if why:
            lab = "CONTRADICTED"
        elif MCLS[rule]["label"] == "UNDERDETERMINED":
            lab = "UNDERDETERMINED"
        else:
            lab = "CONSISTENT WITH ALL THREE"
        CLS[rule] = dict(label=lab, why=why, M=MCLS[rule]["label"], G="PASS at " + str(GPASS[rule]) if GPASS[rule] else "FAIL",
                         D=D["label"], C1=C1[rule]["label"], at_risk=["C1b minor accretion"] + (["C1 merger memory"] if rule == "L0" else []))
        P(f"CLASS {rule}: {lab}" + ("".join(f"\n   - {w}" for w in why)) + f"\n   M {CLS[rule]['M']}; G {CLS[rule]['G']}; D {CLS[rule]['D']}; "
          f"C1 {CLS[rule]['C1']}; at risk: {', '.join(CLS[rule]['at_risk'])}")
    overall = min((CLS[r_]["label"] for r_ in CLS), key=lambda x: rank[x])
    RES["classes"] = CLS; RES["overall"] = overall
    P(f"OVERALL H-POP (best over the two declared rules): {overall}")
    P("POST HOC reading notes (no class weight):")
    P("  - LC with exact capture latches only overfilled cells while a host grows (PH1): its t is the OVERFILL population, i.e. a")
    P("    history-latched form of CFG639's deficit gate. C1 is unaffected (argument, not computed): on merging, a remnant of settled")
    P("    pieces is overfilled by exactly H-MM's sub-additive excess with no deficit inside it (H-MM's mass is max(sum T_i, T_rem)")
    P("    >= T_rem everywhere), so LC latches that excess at once whatever the pieces' earlier labels; the remnant is H-MM's formula.")
    P("  - For LC the static host label split over-states the merger's mobile fraction (argument: latching continues during the")
    P("    merger wherever the phantom leaves with the gas), so M(LC) stays UNDERDETERMINED; it does not change LC's class (C1).")
    P("  - L0 fails G because the formation snapshot freezes the unsettled, in-transit cold energy inside r_ta(t_form) (PH2); the")
    P("    20-30 kpc shell must then be filled by deposits arriving after X = 0.5, which at alpha_f <= 1 do not arrive by t0")
    P("    (the alpha_f -> inf bracket passes). PH3 shows what a settled-only snapshot (a different, unfrozen rule) would do.")
    P("New assumptions / constants: alpha_t = 0 for t (posit against the record's universal drift/push); label rule L0 with "
      "X_form = 0.5 (convention) or LC capture (rule, no rate constant; finite rate would add Gamma_cap); no release; per-dwarf "
      "formation-epoch baryon masses (unmeasured history input).  alpha_f is the record's existing coefficient.")
    P()
else:
    # ============================================================================================= MUTATE: swap alpha_t <-> alpha_f
    MAIN = json.load(open(os.path.join(HERE, "cfg915_results.json")))
    P("MUTATE: swap the labels' mobilities (alpha_t in {0.5, 1.0}, alpha_f = 0)")
    GS = {}
    for rule in ("L0", "LC"):
        for a in ALPHAS_F:
            for f in FOOTS:
                o = gt("MW", f, rule, 0.0, at=a)
                GS[f"{rule}|{f}|{akey(a)}"] = o
                P("  " + gline(f"SWAPPED {rule} {f} alpha_t {akey(a)}", o))
    TOOTH = {}
    for rule in ("L0", "LC"):
        gsw = [a for a in ALPHAS_F if all(GS[f"{rule}|{f}|{akey(a)}"]["i_holds"] for f in FOOTS)]
        g_un = bool(MAIN["G_pass_alpha"][rule])
        phim = {f: min(1 - MAIN["hosts"][f"{rule}|{hk}|{f}|{akey(a)}"]["phi_f_200"] for hk in ("15.0", "14.0") for a in ALPHAS_F) for f in FOOTS}
        if all(phim[f] >= 0.9 for f in FOOTS):
            msw = "FAILS (mobile fraction >= 0.9 -> CFG623 nodes alpha >= 0.3 EXCLUDED both footings)"
        elif all(phim[f] > MAIN["phi_lin"][f]["B"] for f in FOOTS):
            msw = "FAILS at first order"
        else:
            msw = "not failed"
        dsw = f"FAILS (clump drifts at alpha >= 0.5 >> alpha_c {ALPHA_C:.2e}, CFG882)"
        failed_new = []
        if g_un and not gsw:
            failed_new.append("G")
        if msw.startswith("FAILS"):
            failed_new.append("M")
        failed_new.append("D")
        TOOTH[rule] = dict(G_swapped="PASS at " + str(gsw) if gsw else "FAIL", G_unswapped="PASS" if g_un else "FAIL",
                           M_swapped=msw, min_mobile_fraction=phim, D_swapped=dsw, newly_failed=failed_new, bites=bool(failed_new))
        P(f"  {rule}: G swapped {TOOTH[rule]['G_swapped']} (unswapped {TOOTH[rule]['G_unswapped']}); M swapped {msw} "
          f"(min mobile fraction {phim['can']:.3f}/{phim['alt']:.3f}); D swapped {dsw} -> newly failed {failed_new} -> "
          f"{'BITES' if failed_new else 'does not bite'}")
    bites = all(TOOTH[r_]["bites"] for r_ in TOOTH)
    RES["G_swapped"] = GS; RES["tooth"] = TOOTH; RES["bites"] = bites
    P(f"TOOTH: {'BITES' if bites else 'DOES NOT BITE'} (per rule: " + ", ".join(f"{r_} {'bites' if TOOTH[r_]['bites'] else 'no'}" for r_ in TOOTH) + ")")
    P()

P(f"K-tests: {'all PASS' if KALL else 'SOME FAIL'} ({sum(1 for v in K.values() if v['pass_'] is True)}/{len(K)} PASS, "
  f"{sum(1 for v in K.values() if v['pass_'] == 'PARTIAL')} PARTIAL)")
P(f"elapsed {time.time() - T0:.0f} s")


def jclean(o):
    if isinstance(o, dict):
        return {str(k_): jclean(v) for k_, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jclean(v) for v in o]
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, float) and not np.isfinite(o):
        return str(o)
    return o


json.dump(jclean(RES), open(os.path.join(HERE, f"cfg915_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg915{SUF}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if (MUT and RES.get("bites")) else 0)

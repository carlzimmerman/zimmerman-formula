#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG243_common -- shared machinery for lane CFG243 (a conserved dust created once, at turnaround, by a local causal source).
Frozen criteria: campaign_fresh_gravity/CFG243_FROZEN_CRITERIA.md (committed 7cc93bdef, sha256 ee6df5b2...).  Nothing in the repository
is edited; committed lanes (CFG44 Bcommon, CFG7_common, CFG70's JSON) are read READ-ONLY.  Repo root: ZF_REPO, else walk up from
__file__ to the directory that holds campaign_fresh_gravity/.  Every printed path is <repo>/... or <lane>/...; no absolute home path is
printed or stored.

Units: kpc, km/s, Msun (G = 4.30091727e-6 kpc (km/s)^2/Msun as in Bcommon).  Canonical a0 = 9.3603e-11 m/s^2 and alt 1.1312e-10 (both
footings, never pooled).  kappa = 1/2 is FITTED.  Nothing here says the theory is closed; there is no dark-matter particle and the cold
MASS is still required.

Exit convention (as CFG242): a main run exits 0 iff every 'control' check passes (a gate FAIL is a 'result', not an error); a MUTATE run
exits 1 iff the control BITES (every claim handed to finish() is True), else 0 (a declared control failure, kept as run).
"""
import os, sys, json, math, time, importlib.util
import numpy as np

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))


def find_repo():
    env = os.environ.get("ZF_REPO")
    if env and os.path.isdir(os.path.join(env, "campaign_fresh_gravity")):
        return os.path.abspath(env)
    d = HERE
    for _ in range(8):
        if os.path.isdir(os.path.join(d, "campaign_fresh_gravity")):
            return d
        d = os.path.dirname(d)
    raise SystemExit("CFG243: set ZF_REPO to the repository root (walk-up from __file__ found none)")


REPO = find_repo()


def scrub(s):
    s = str(s).replace(REPO, "<repo>")
    s = s.replace(os.path.expanduser("~"), "~")
    return s.replace(HERE, "<lane>")


def _load(name, relpath):
    p = os.path.join(REPO, relpath)
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


B = _load("Bcommon", "campaign_fresh_gravity/CFG44_fluid_target/Bcommon.py")          # read-only
G, KPC_M, C_KMS = B.G, B.KPC_M, B.C_KMS
A0_SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
A0K = {k: v * KPC_M / 1e6 for k, v in A0_SI.items()}          # (km/s)^2/kpc
A0 = A0K["canonical"]
FOOTS = ("canonical", "alt")
KAPPA = 0.5
GYR_PER_KPC_KMS = KPC_M / 1e3 / (3.15576e7 * 1e9)             # 1 kpc/(km/s) in Gyr
MASSES = (1e9, 1e10, 1e11, 1e12)
OMEGA_C_OVER_B = 0.1200 / 0.02237                              # as Bcommon

# the Planck 2018 best fit as CFG4_cosmology.py uses it (XR26's CLASS inputs; typed here with that source)
P18 = {"h": 0.673317, "omega_b": 0.022383, "omega_cdm": 0.12011, "tau_reio": 0.0543, "ln10^{10}A_s": 3.0448, "n_s": 0.96605,
       "N_ur": 2.0328, "N_ncdm": 1, "m_ncdm": 0.06, "YHe": 0.24543}
OMC_H2_COMPARE = 0.1200        # Planck 2018 Omega_c h^2 = 0.1200 +- 0.0012 (the FITTED comparison value)
COSMIC_LINE_FRAC = 0.5         # frozen: >= 0.5 of the Omega_c h^2 needed at z = 1100
DELTA_TA_FROZEN = {1100: 1.0624, 10: 1.0624, 2.5: 1.076, 0: 1.276}      # frozen thresholds (CFG4_README; EdS value for z >= 10)
RHO_L_CAN = (A0 / (KAPPA * C_KMS)) ** 2 / G                    # Msun/kpc^3 from the tie read backwards (CFG242_common's value)
RHOC0_KPC = 2.77536627e11 * P18["h"] ** 2 / 1e9                # Msun/kpc^3
OMEGA_M = 0.3157               # CFG4's committed value, = CLASS total matter at these parameters (checked in CFG243_controls)
OMEGA_B = P18["omega_b"] / P18["h"] ** 2
OMEGA_C = P18["omega_cdm"] / P18["h"] ** 2


def load_c7():
    sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
    import CFG7_common as C7                                    # read-only import (LCDM growth, committed turnaround thresholds)
    return C7


class Run:
    def __init__(self, slug):
        self.slug = slug
        self.mutate = os.environ.get("MUTATE", "").strip()
        self.robust = os.environ.get("ROBUST", "").strip()
        mode = (f"_MUTATE_{self.mutate}" if self.mutate else "") + (f"_ROBUST_{self.robust}" if self.robust else "")
        self.tag = slug + mode
        self.lines, self.checks, self.nums = [], [], {}
        self.t0 = time.time()
        self.P(f"# {self.tag}   repo = <repo>   mode = {self.mutate or self.robust or 'main'}")

    def P(self, s=""):
        s = scrub(s)
        print(s, flush=True)
        self.lines.append(s)

    def banner(self, s):
        self.P("\n" + "=" * 100 + f"\n{s}\n" + "=" * 100)

    def check(self, name, ok, detail="", kind="control"):
        ok = bool(ok)
        self.checks.append(dict(name=name, ok=ok, detail=scrub(detail), kind=kind))
        self.P(f"  [{'PASS' if ok else 'FAIL'}] ({kind}) {name}" + (f"   ({scrub(detail)})" if detail else ""))
        return ok

    def num(self, k, v):
        self.nums[k] = v

    def verdict(self, gate, status, why):
        self.nums.setdefault("verdicts", {})[gate] = dict(status=status, why=scrub(why))
        self.P(f"  >>> {gate}: {status} -- {scrub(why)}")

    def main_cells(self):
        p = os.path.join(HERE, f"{self.slug}_results.json")
        if not os.path.exists(p):
            return {}
        return {c["name"]: c["ok"] for c in json.load(open(p))["checks"]}

    def finish(self, bite_claims=None):
        ctrl_fail = [c for c in self.checks if c["kind"] == "control" and not c["ok"]]
        out = dict(slug=self.tag, mutate=self.mutate, robust=self.robust, runtime_s=round(time.time() - self.t0, 2),
                   checks=self.checks, numbers=self.nums)
        if self.mutate:
            bit = bool(bite_claims) and all(bite_claims)
            out["control_bites"] = bit
            self.P(f"\nMUTATE {self.mutate}: control {'BITES (exit 1)' if bit else 'DOES NOT BITE (declared control failure, exit 0)'}")
            code = 1 if bit else 0
        elif self.robust:
            bit = bool(bite_claims) and all(bite_claims)
            out["robust_bites"] = bit
            self.P(f"\nROBUST {self.robust}: the check {'BITES (the headline is fragile; exit 1)' if bit else 'does NOT bite (the headline is robust; exit 0, as frozen)'}")
            code = 1 if bit else 0
        else:
            self.P(f"\nRESULT: {len(self.checks)} checks, {len(ctrl_fail)} control failure(s): "
                   + ("; ".join(c['name'] for c in ctrl_fail) if ctrl_fail else "none") + f"   ({time.time() - self.t0:.0f} s)")
            code = 1 if ctrl_fail else 0

        def clean(o):
            if isinstance(o, dict):
                return {str(k): clean(v) for k, v in o.items()}
            if isinstance(o, (list, tuple)):
                return [clean(v) for v in o]
            if isinstance(o, (np.floating, np.integer)):
                return o.item()
            if isinstance(o, np.ndarray):
                return clean(o.tolist())
            if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
                return str(o)
            return o

        open(os.path.join(HERE, f"{self.tag}.out"), "w").write("\n".join(self.lines) + "\n")
        json.dump(clean(out), open(os.path.join(HERE, f"{self.tag}_results.json"), "w"), indent=1)
        sys.exit(code)


# ------------------------------------------------------------------------------------------------ CLASS (a Boltzmann code is available)
def class_cosmo(zs, newtonian=False, baryon_only=False, kmax=1500.0):
    """CLASS 3.x transfer functions at the Planck 2018 parameters (CFG4_cosmology's inputs).  matter_source_in_current_gauge is
    needed for z_pk above z_rec.  baryon_only: omega_cdm -> 1e-7 (the frozen C4 reading; flat, Omega_Lambda adjusts)."""
    from classy import Class
    par = dict(P18, output="mTk,vTk", **{"P_k_max_h/Mpc": kmax}, z_pk=",".join(str(z) for z in zs),
               matter_source_in_current_gauge="yes", gauge=("newtonian" if newtonian else "synchronous"))
    if baryon_only:
        par["omega_cdm"] = 1e-7
    c = Class()
    c.set(par)
    c.compute()
    return c


def PR_k(k_mpc):
    As = math.exp(P18["ln10^{10}A_s"]) * 1e-10
    return As * (k_mpc / 0.05) ** (P18["n_s"] - 1.0)


def delta2(c, z, key="d_m"):
    """dimensionless power per ln k: Delta^2(k, z) = P_R(k) T(k, z)^2, k in 1/Mpc."""
    tr = c.get_transfer(z)
    k = tr["k (h/Mpc)"] * c.h()
    return k, PR_k(k) * tr[key] ** 2


def sigma_R(k, D2, R_mpc):
    x = k * R_mpc
    W = 3.0 * (np.sin(x) - x * np.cos(x)) / x ** 3
    return float(np.sqrt(np.trapz(D2 * W ** 2, np.log(k))))


def R_of_M(M, omega_m=OMEGA_M):
    """comoving top-hat radius [Mpc] enclosing mass M [Msun] at the mean matter density Omega_m rho_crit,0."""
    rhom = omega_m * 2.77536627e11 * P18["h"] ** 2
    return (3.0 * M / (4.0 * math.pi * rhom)) ** (1.0 / 3.0)


def erfc(x):
    from scipy.special import erfc as _e
    return float(_e(x))


def ps_F(delta_ta, sigma):
    """Press-Schechter turned-around mass fraction F = erfc(delta_ta / (sqrt2 sigma)); log10 returned too (no underflow)."""
    from scipy.special import erfc, log_ndtr
    x = delta_ta / (math.sqrt(2.0) * sigma)
    F = float(erfc(x))
    # log10 F via the normal tail: erfc(x) = 2 Phi(-sqrt2 x)
    log10F = float((math.log(2.0) + log_ndtr(-math.sqrt(2.0) * x)) / math.log(10.0))
    return F, log10F


# ------------------------------------------------------------------------------------------------ small helpers used by several scripts
def r_M_kpc(Mb, a0=A0):
    return math.sqrt(G * Mb / a0)


def nu_p2_scalar(y):
    return math.sqrt(1.0 + 1.0 / y)


def dust_ratio_point(x):
    """target M_c / M_b for a point mass (CFG44, P2): sqrt(1 + x^2) - 1."""
    return math.sqrt(1.0 + x * x) - 1.0


def cfg70_rta():
    """B's committed (nu_mono and P2) and CFG48's r_ta, r_e from CFG70's results JSON, read-only (kpc)."""
    p = os.path.join(REPO, "campaign_fresh_gravity", "CFG70_memory_kernel_exchange", "cfg70_memory_kernel_exchange_results.json")
    d = json.load(open(p))["numbers"]["E1"]
    out = {}
    for M, v in d.items():
        out[float(M)] = {"CFG48": (v["CFG48"]["r_ta"], v["CFG48"]["r_e"]), "B_P2": (v["committed_P2"]["r_ta"], v["committed_P2"]["r_e"]),
                         "B_nu_mono": (v["committed_nu_mono"]["r_ta"], v["committed_nu_mono"]["r_e"])}
    return out

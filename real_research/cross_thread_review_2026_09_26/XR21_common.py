#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR21_common -- shared plumbing for the XR21 stage scripts: output tee (<name>.out / <name>_MUTATE.out), the record's check()
convention, results JSON (<name>_results.json / <name>_results_MUTATE.json), thread pinning, and read-only loaders of the
record's machinery (L362's CLASS P_lin, L346's CLASS settings, FP9's exec'd machinery).  Nothing outside this folder is edited.
"""
import os, sys, io, json, time, math, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
G03 = os.path.join(REPO, "real_research", "g03_audit_2026")
DSEC = os.path.join(REPO, "real_research", "dark_sector_2026")
CHAIN = os.path.join(REPO, "real_research", "derivation_chain_2026")


def pin_threads(n):
    for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
        os.environ[v] = str(n)


class Tee:
    def __init__(self, path):
        self.f = open(path, "w"); self.o = sys.stdout

    def write(self, s):
        self.o.write(s); self.f.write(s)

    def flush(self):
        self.o.flush(); self.f.flush()


class Lane:
    """one stage script's bookkeeping: its .out tee, its checks, its JSON."""

    def __init__(self, slug, mutate):
        self.slug, self.mutate = slug, mutate
        self.t0 = time.time()
        self.checks, self.out = [], {"lane": slug, "mutate": mutate, "checks": {}, "numbers": {}, "runs": {}}
        self.dir = os.environ.get("XR21_OUTDIR", HERE)                  # smoke tests write elsewhere, never for the record
        os.makedirs(self.dir, exist_ok=True)
        self.tee = Tee(os.path.join(self.dir, f"{slug}{'_MUTATE' if mutate else ''}.out"))
        sys.stdout = self.tee

    def P(self, *a):
        print(*a, flush=True)

    def banner(self, t):
        self.P("\n" + "=" * 116 + "\n" + t + "\n" + "=" * 116)

    def check(self, name, measured, ok, reading="", load_bearing=True):
        ok = bool(ok)
        self.checks.append((name, ok, load_bearing))
        self.out["checks"][name.split(" ")[0]] = {"title": name, "ok": ok, "measured": str(measured), "load_bearing": load_bearing}
        self.P(f"  [{'PASS' if ok else 'FAIL'}] {name}{'' if load_bearing else '  (reported, not load-bearing)'}")
        self.P(f"         measured: {measured}")
        if reading:
            self.P(f"         reading:  {reading}")
        return ok

    def el(self):
        return f"[{time.time() - self.t0:.0f} s]"

    def finish(self):
        n_fail = sum(1 for _, ok, lb in self.checks if lb and not ok)
        self.out["n_checks"] = len(self.checks)
        self.out["n_pass"] = sum(1 for _, ok, _ in self.checks if ok)
        self.out["n_fail_load_bearing"] = n_fail
        self.out["wall_s"] = time.time() - self.t0
        name = f"{self.slug}_results{'_MUTATE' if self.mutate else ''}.json"
        with open(os.path.join(self.dir, name), "w") as f:
            json.dump(self.out, f, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
        self.P(f"\n  {self.out['n_pass']}/{len(self.checks)} checks pass; load-bearing failures: {n_fail}; wrote {name}   {self.el()}")
        self.tee.flush()
        return 0 if n_fail == 0 else 1


# ---------------------------------------------------------------------------------------------- record loaders (read-only)
def l362_plin():
    """L362's CLASS instance (P_k_max 60 h/Mpc, z_max 60): its P_lin(k [h/Mpc], z) [(Mpc/h)^3]."""
    if G03 not in sys.path:
        sys.path.insert(0, G03)
    import L362_forest_pincer_convergence as L2
    return L2.P_lin


_L346 = {}


def l346_plin():
    """a CLASS instance with L346's own settings (P_k_max 20 h/Mpc), as L346's make_ics used."""
    if not _L346:
        from classy import Class
        h = 0.6736
        cl = Class()
        cl.set({"h": h, "omega_b": 0.02237, "omega_cdm": 0.12, "A_s": 2.1e-9, "n_s": 0.9649, "tau_reio": 0.0544,
                "N_ur": 3.046, "N_ncdm": 0, "YHe": 0.2454, "output": "mPk", "P_k_max_h/Mpc": 20, "z_max_pk": 60,
                "non_linear": "halofit"})
        cl.compute()
        _L346["P"] = lambda kh, z: cl.pk_lin(kh * h, z) * h ** 3
        _L346["cl"] = cl
    return _L346["P"]


def load_fp9():
    """FP9's committed script exec'd read-only up to its 'K  CONTROLS' banner (FP9 execs FP6's machinery the same way):
    FP6's growth yardstick, kernels, phantom(), FP9's yield hook (cut_hook, CQ_yield, x_P2), growth_aq, LL_of."""
    path = os.path.join(CHAIN, "FP9_web_galaxy_separator.py")
    src = open(path).read()
    cut = src.index('\nbanner("K  CONTROLS') + 1
    ns = {"__file__": path, "__name__": "fp9_machinery"}
    old = os.environ.get("MUTATE")
    os.environ["MUTATE"] = "0"
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src[:cut], path, "exec"), ns)
    finally:
        if old is None:
            os.environ.pop("MUTATE", None)
        else:
            os.environ["MUTATE"] = old
    M6 = ns["M6"]
    YIELD = ns["YIELD"]

    def hy_model(n, L25, pp, y25, floor=True):                       # FP9 lines 633-638 (floor_of, hy_model), FLOOR_ON = floor
        return M6["bandpass_model"](ns["LL_of"](L25, n), n, yr=0.0, floor=((y25, pp, YIELD) if floor else None))
    ns["hy_model"] = hy_model
    return ns


def fp0_footings():
    """FP0's committed footings (FP9 reads the same JSON)."""
    p = os.path.join(CHAIN, "FP0_core_postulates_results.json")
    n0 = json.load(open(p))["numbers"]
    return {"canonical": n0["a0_canonical"], "alt": n0["a0_rho_total"]}


def load_fp13_state():
    """FP13's committed state machinery, exec'd read-only: its module head (up to def main) and the body of main() up to its
    'the general separator model + gates' block (dedented): the growth, halofit (Takahashi+12), L_table, gbp_rms_phys, the
    switches, yth_state, fun_of, on FP13's own ln a grid.  Returns the namespace plus the headline tables (H_S: delta_c, NL,
    ramp, c_y = 1) and FP13's MUTATE yield (no onset switch)."""
    import textwrap
    path = os.path.join(CHAIN, "FP13_separator_from_state.py")
    src = open(path).read()
    head = src[:src.index("\ndef main():")]
    b0 = src.index("\ndef main():") + len("\ndef main():\n")
    b1 = src.index("    # --------------------------------------------------------------------------------------------- the general separator model + gates")
    body = textwrap.dedent(src[b0:b1])
    ns = {"__file__": path, "__name__": "fp13_machinery"}
    old = os.environ.get("MUTATE")
    os.environ["MUTATE"] = "0"
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(head, path, "exec"), ns)
            exec(compile(body, path + ":main", "exec"), ns)
    finally:
        if old is None:
            os.environ.pop("MUTATE", None)
        else:
            os.environ["MUTATE"] = old
    LH = ns["L_table"](ns["DELTA_C"], "NL")
    yh, yh_tab, rms = ns["yth_state"](LH, "NL", "ramp", 1.0)
    ym, ym_tab, _ = ns["yth_state"](LH, "NL", "none", 1.0)
    ns.update(HS_LH=LH, HS_Lh=ns["fun_of"](LH), HS_yh=yh, HS_ytab=yh_tab, HS_rms=rms, HS_ytab_mutate=ym_tab, HS_yh_mutate=ym)

    def model_of(Lf, yf):                                          # FP13's model_of (its gates block), verbatim
        M6 = ns["M6"]; h = M6["h"]
        return {"hfac": lambda a, k: 1.0 - np.exp(-0.5 * (k * h * Lf(a) / a) ** 2),
                "cut": lambda y, a: M6["cutfac"](y, yf(a), ns["YIELD"]), "yr": 0.0}
    import numpy as np
    ns["model_of"] = model_of
    return ns

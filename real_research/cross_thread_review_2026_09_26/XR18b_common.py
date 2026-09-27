#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR18b_common -- shared machinery for the XR18b re-audit of FP19's repaired separator H_K1 (nothing here runs a lane).

It supplies:
  * Lane: the review folder's conventions (the script tees its own .out, writes a results JSON, prints PASS/FAIL checks,
    exits rc = 0 only when no load-bearing check fails; MUTATE=1 writes the _MUTATE versions and never touches the main ones).
  * load_fp19(): FP19's committed module and slices of its main() body (up to its K banner; its K4 block, which defines
    XR18 C1's <K>_h-channel formula; its H3 block, which defines the symbol table), exec'd READ-ONLY in a private namespace
    (FP19 in turn execs FP13 -> FP9 -> FP6 read-only).  Nothing of FP19 that writes a file is executed.
  * extract_defs(): the text of named top-level functions of a committed script, so that XR18's own functions can be re-run
    without executing (or overwriting) anything of XR18.
  * load_base(): FP9 (FP6 inside) up to its CONTROLS banner and DE12's host/transition definitions -- XR18's recipe.
  * H_K1's separator as closed forms: L(z) = L_Lambda Omega_L(z) (n = 2) and the tied yield
    y_th(z) = c_y max(0, 2q) 4 pi G rho_bar L/a0 (c_y = 2), identical to FP19's L_K / y_tied.
Run nothing from here; the lanes import it.  kappa = 1/2 is FITTED (Z = 5.7888); nothing here derives it.
"""
import os, sys, io, json, math, time, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CHAIN = os.path.join(REPO, "real_research", "derivation_chain_2026")
DE = os.path.join(REPO, "real_research", "dark_energy_2026")

HEAD_LL, HEAD_N, HEAD_CY = 2.9, 2.0, 2.0          # FP19's headline H_K1: L_Lambda [Mpc], n, c_y
XI_PC = {"canonical": 0.0243, "alt": 0.0268}       # FP7's AQUAL Solar-System floors on xi (pc), as XR18 uses them
HBARC_EVM, MP_EV = 1.973269804e-7, 2.435e27        # FP7 B6's strong-coupling constants (hbar c [eV m], reduced Planck mass [eV])


# ================================================================================================ the Lane helper
class _Tee:
    def __init__(self, path):
        self._f = open(path, "w", encoding="utf-8")
        self._s = sys.__stdout__

    def write(self, t):
        self._s.write(t)
        self._f.write(t)

    def flush(self):
        self._s.flush()
        self._f.flush()

    def close(self):
        self._f.close()


def _js_default(o):
    try:
        import numpy as np
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, (np.floating, np.integer)):
            return float(o)
        if isinstance(o, np.bool_):
            return bool(o)
    except Exception:
        pass
    return str(o)


class Lane:
    def __init__(self, name, tag):
        self.mutate = os.environ.get("MUTATE", "0") == "1"
        self.name = name
        self.txt = os.path.join(HERE, name + ("_MUTATE.out" if self.mutate else ".out"))
        self.jsn = os.path.join(HERE, name + ("_results_MUTATE.json" if self.mutate else "_results.json"))
        self.t0 = time.time()
        self.tee = _Tee(self.txt)
        sys.stdout = self.tee
        self.out = {"lane": tag, "mutate": self.mutate, "checks": {}, "numbers": {}, "ledger": []}
        self.ch = []

    def P(self, *a):
        print(*a, flush=True)

    def banner(self, t):
        self.P("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118)

    def el(self):
        return f"[{time.time() - self.t0:.0f} s]"

    def check(self, name, measured, ok, reading="", load_bearing=True):
        ok = bool(ok)
        self.ch.append((name, ok, load_bearing))
        self.out["checks"][name.split()[0]] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing, "name": name}
        self.P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")
        if reading:
            self.P(f"         reading:  {reading}" if (ok or not self.mutate) else
                   f"         reading (written for the unmutated theory; this MUTATE run fails the check):  {reading}")
        return ok

    def finish(self):
        n_fail = sum(1 for _, ok, lb in self.ch if lb and not ok)
        self.out["n_checks"] = len(self.ch)
        self.out["n_fail_load_bearing"] = n_fail
        self.out["n_fail_reported"] = sum(1 for _, ok, lb in self.ch if (not lb) and (not ok))
        self.out["elapsed_s"] = round(time.time() - self.t0)
        json.dump(self.out, open(self.jsn, "w"), indent=1, default=_js_default)
        rc = 0 if n_fail == 0 else 1
        self.P(f"\n  {sum(1 for _, ok, _l in self.ch if ok)}/{len(self.ch)} checks pass; load-bearing failures: {n_fail}; wrote "
               f"{os.path.basename(self.jsn)}  ({time.time() - self.t0:.0f} s)")
        self.P(f"rc = {rc}")
        self.tee.flush()
        sys.stdout = sys.__stdout__
        self.tee.close()
        sys.exit(rc)


# ================================================================================================ read-only loaders
def _with_mutate_off(fn):
    old = os.environ.get("MUTATE")
    os.environ["MUTATE"] = "0"
    try:
        return fn()
    finally:
        if old is None:
            os.environ.pop("MUTATE", None)
        else:
            os.environ["MUTATE"] = old


def load_fp19():
    """FP19's module + main() body slices exec'd read-only.  Returns the namespace: FP13's machinery (NS, M6, ns9, the state,
    L_table, yth_state, model_of, gates, growth_aq, ...), FP19's gates2, L_K, y_tied, I_of, halo_rate, rms_bp_L,
    maxwell_x_mean, halo_x_mean, chord_modes, RB_of, RB_fine, D2_at, stein_score, the K4 block (K_channel, x_mean_halo_c,
    x_mean_gauss_c, y_rms_bp_c), and FP19's symbol_table (with eps_K recomputed by FP19's own K_channel)."""
    path = os.path.join(CHAIN, "FP19_hs_repair.py")
    src = open(path).read()
    mod = src[:src.index("\ndef main():")]
    body = src[src.index("\ndef main():") + len("\ndef main():"): src.index('\nif __name__ == "__main__":')]
    ded = "\n".join(l_[4:] if l_.startswith("    ") else l_ for l_ in body.split("\n"))
    part1 = ded[:ded.index('banner("K  CONTROLS: FP13')]
    partK4 = ded[ded.index("# K4: XR18 C1's <K>_h channel"): ded.index('Lx = lambda a: M6["L_phys"](LL9, 2.0, a)')]
    partS = ded[ded.index("ZSYM = (0.0, 0.25, 0.5, Z_Q0"): ded.index("sym_head = symbol_table(")]
    ns = {"__file__": path, "__name__": "fp19_machinery"}

    def run():
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(mod, path, "exec"), ns)
            exec(compile(part1, path, "exec"), ns)
            exec(compile(partK4, path, "exec"), ns)
            LK = ns["L_K"](HEAD_LL, HEAD_N)
            ns["LK_head"], ns["yK_head"] = LK, ns["y_tied"](LK, HEAD_CY)
            ns["b4"] = ns["K_channel"](LK, ns["yK_head"])
            exec(compile(partS, path, "exec"), ns)
    _with_mutate_off(run)
    return ns


def extract_defs(path, names):
    """the source text of the named TOP-LEVEL functions of a committed script (from 'def name(' to the next top-level line)."""
    lines = open(path).read().split("\n")
    out = []
    for nm in names:
        start = next(i for i, l_ in enumerate(lines) if l_.startswith(f"def {nm}("))
        j = start + 1
        while j < len(lines) and (lines[j].startswith((" ", "\t")) or lines[j].strip() == ""):
            j += 1
        blk = lines[start:j]
        while blk and blk[-1].strip() == "":
            blk.pop()
        out.append("\n".join(blk))
    return "\n\n\n".join(out)


def load_base():
    """FP9 (FP6 inside) exec'd read-only up to its CONTROLS banner, and DE12's host/transition definitions (XR18's recipe)."""
    FP9 = os.path.join(CHAIN, "FP9_web_galaxy_separator.py")
    s9 = open(FP9).read()
    NS9 = {"__file__": FP9, "__name__": "fp9_machinery"}
    P12 = os.path.join(DE, "DE12_mond_sector_gate_stiffness.py")
    D12 = {"__name__": "de12", "__file__": P12}
    s12 = open(P12).read()
    head = s12.split("# ============================================================================================ C1 the amplification")[0]
    trans = s12.split("# ============================================================================================ the transitions")[1].split(
        "# ============================================================================================ G1 G2 the budget")[0].split('banner("C2')[0]

    def run():
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(s9[:s9.index('\nbanner("K  CONTROLS')], FP9, "exec"), NS9)
            exec((head + trans).replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), D12)
    _with_mutate_off(run)
    return NS9, D12


# ================================================================================================ H_K1 as closed forms
def hk1_forms(M6, A0, LL=HEAD_LL, n=HEAD_N, cy=HEAD_CY):
    """H_K1's separator on FRW (FP19's L_K and y_tied, closed forms): L(z) [physical Mpc] and y_th(z, footing); two_q(a);
    fourpiGrho(a) = <K>^2/6 - Lambda/2 = 4 pi G rho_bar [1/s^2]."""
    Om, OL, Or, H0, Mpc = M6["Om"], M6["OL"], M6["Or"], M6["H0"], M6["Mpc"]
    OmL_a = M6["OmL_a"]

    def two_q(a):
        E2 = Om / a ** 3 + OL + Or / a ** 4
        return 1.0 + (Or / a ** 4) / E2 - 3.0 * OL / E2

    def fourpiGrho(a):
        return 1.5 * H0 ** 2 * (Om / a ** 3 + Or / a ** 4)

    def L_of(z):
        return LL * OmL_a(1.0 / (1.0 + z)) ** (n / 2.0)

    def yth_of(z, foot, ramp=None):
        a = 1.0 / (1.0 + z)
        r_ = max(0.0, two_q(a)) if ramp is None else ramp(a)
        return cy * r_ * fourpiGrho(a) * L_of(z) * Mpc / A0[foot]

    return dict(two_q=two_q, fourpiGrho=fourpiGrho, L_of=L_of, yth_of=yth_of)


def ell_sc(a0, Cphi, lam_eff, cc=299792458.0):
    """FP7 B6's tree-level strong-coupling length: Lambda_sc = c_s^(9/4) [(3/2) alpha M_P (2 lambda_eff)^(3/2)]^(1/2), alpha = a0/c^2
    in eV, c_s^2 = C_phi/lambda_eff, ell_sc = c_s hbar c/Lambda_sc [m] (the copy XR25 K3 verified against FP7's committed rows)."""
    alpha_eV = a0 / cc ** 2 * HBARC_EVM
    cs = math.sqrt(Cphi / lam_eff)
    Lsc = cs ** 2.25 * math.sqrt(alpha_eV * MP_EV * (2 * lam_eff) ** 1.5 * 1.5)
    return cs, Lsc, cs * HBARC_EVM / Lsc

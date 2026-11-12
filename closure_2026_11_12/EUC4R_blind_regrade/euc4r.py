#!/usr/bin/env python3
"""EUC4R: blind re-grade of EUC4 Part A (wide grade-B lenses vs the law's saturation ceiling).

Written from the text of EUC4's and EUC1's FROZEN_CRITERIA.md and this lane's PROTOCOL.md only; imports nothing from
EUC1, EUC4, A55 or A70. kappa = 1/2 FITTED. Footings never pooled. One-sided test. Does not relabel EUC4.

Run (main first, then the twin):
    python3 -I euc4r.py
    EUC4R_MUTATE=newton python3 -I euc4r.py      # must exit 1
"""
import hashlib
import json
import os
import sys

import numpy as np
import pandas as pd
from scipy.integrate import quad
from scipy.special import gammainc, gammaincinv

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "_external_data", "euclid_dr1_eclipse")
KEY = "eclipse_dr1_catalogue_key_v20261103.csv"
OBJ = "ECLIPSE_object_catalogue.csv"
SHA256 = {  # EUC1 FROZEN_CRITERIA §1
    KEY: "65338917534c9c767c4f45732d29937d2dfb7fd68083cdfd05aec994ee4fa9ab",
    OBJ: "8247a4d5f23513b83be6db5a8244234f0cc1e1ac66e4de1a54983ae5984786b2",
}

MUTATE = os.environ.get("EUC4R_MUTATE", "")
if MUTATE not in ("", "newton"):
    sys.exit("unknown EUC4R_MUTATE")
SUFFIX = "_mutate_newton" if MUTATE == "newton" else ""

FOOTINGS = {"canonical": 9.3603e-11, "alt": 1.132e-10}  # m/s^2
A0 = {k: (1e-30 if MUTATE == "newton" else v) for k, v in FOOTINGS.items()}
LAWS = ("S", "B")

# constants (PROTOCOL §3.3)
G = 6.67430e-11
C = 299792458.0
MSUN = 1.98841e30
KPC = 3.0856775814913673e19
MPC = 1e3 * KPC
ARCSEC = np.pi / 648000.0
# cosmology (EUC1 §3)
H0 = 67.74e3 / MPC  # s^-1
OM = 0.3089
ZS_INF = 1100.0
RMAX = 1e6 * KPC

SEED = 20261112
NBOOT = 2000
BSTAR = 0.25

LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ---------------------------------------------------------------- distances
def chi(z):
    """Comoving distance (m), flat, no radiation."""
    f = lambda x: 1.0 / np.sqrt(OM * (1 + x) ** 3 + 1 - OM)
    val, _ = quad(f, 0.0, z, epsabs=0.0, epsrel=1e-11, limit=1000)
    return C / H0 * val


_CHI_CACHE = {}


def chi_c(z):
    z = float(z)
    if z not in _CHI_CACHE:
        _CHI_CACHE[z] = chi(z)
    return _CHI_CACHE[z]


def sigma_cr_inf(zl, zs=ZS_INF):
    """Sigma_cr(z_l, z_s) in kg/m^2; D_s/D_ls = chi_s/(chi_s - chi_l) in flat space."""
    cl = np.array([chi_c(z) for z in zl])
    cs = chi_c(zs)
    dl = cl / (1 + zl)
    return C ** 2 / (4 * np.pi * G * dl) * cs / (cs - cl), dl


# ---------------------------------------------------------------- Sersic / Prugniel-Simien
def ps_enclosed_fraction(r, re, n):
    """M(<r)/M_tot for the Prugniel-Simien deprojection (PROTOCOL §3.1)."""
    p = 1.0 - 0.6097 / n + 0.05463 / n ** 2
    bn = gammaincinv(2.0 * n, 0.5)
    return gammainc(n * (3.0 - p), bn * (r / re) ** (1.0 / n))


# ---------------------------------------------------------------- projection nodes
def gl_nodes(U, nper=128, split=4.0):
    """Gauss-Legendre nodes/weights in u on [0, split] and [split, U] per lens (U > split)."""
    x, w = np.polynomial.legendre.leggauss(nper)
    U = np.asarray(U, dtype=float)
    assert np.all(U > split), "U must exceed the panel split"
    a1, b1 = 0.0, split
    u1 = 0.5 * (b1 - a1) * x + 0.5 * (b1 + a1)
    w1 = 0.5 * (b1 - a1) * w
    u1 = np.broadcast_to(u1, (U.size, nper))
    w1 = np.broadcast_to(w1, (U.size, nper))
    u2 = 0.5 * (U[:, None] - split) * x[None, :] + 0.5 * (U[:, None] + split)
    w2 = 0.5 * (U[:, None] - split) * w[None, :]
    return np.hstack([u1, u2]), np.hstack([w1, w2])


def law_g(gN, a0, law):
    if law == "S":
        return 0.5 * gN * (1.0 + np.sqrt(1.0 + 4.0 * a0 / gN))
    if law == "B":
        return np.sqrt(gN * gN + a0 * gN)
    raise ValueError(law)


class Lenses:
    """Per-lens projection set-up: g_N at unit mass factor on the nodes."""

    def __init__(self, RE, Re, n, Mstar, nper=128):
        self.RE = RE
        U = np.arccosh(RMAX / RE)
        u, w = gl_nodes(U, nper=nper)
        r = RE[:, None] * np.cosh(u)
        frac = ps_enclosed_fraction(r, Re[:, None], n[:, None])
        self.gN1 = G * Mstar[:, None] * frac / r ** 2
        self.w = w

    def m2d(self, logB, a0, law):
        g = law_g(self.gN1 * 10.0 ** logB[:, None], a0, law)
        return self.RE ** 2 / G * np.sum(self.w * g, axis=1)

    def solve_b(self, Mmin, a0, law, lo=-4.0, hi=4.0, iters=60):
        lo = np.full(Mmin.shape, lo)
        hi = np.full(Mmin.shape, hi)
        for _ in range(iters):
            mid = 0.5 * (lo + hi)
            above = self.m2d(mid, a0, law) > Mmin
            hi = np.where(above, mid, hi)
            lo = np.where(above, lo, mid)
        return 0.5 * (lo + hi)


# ---------------------------------------------------------------- statistics
def boot_stats(b, gen="default"):
    N = b.size
    if gen == "default":
        idx = np.random.default_rng(SEED).integers(0, N, size=(NBOOT, N))
    else:
        idx = np.random.RandomState(SEED).randint(0, N, size=(NBOOT, N))
    bb = b[idx]
    out = {}
    for name, arr, full in (
        ("f25", (bb > BSTAR).mean(axis=1), float((b > BSTAR).mean())),
        ("f0", (bb > 0).mean(axis=1), float((b > 0).mean())),
        ("b_med", np.median(bb, axis=1), float(np.median(b))),
    ):
        lo, hi = np.percentile(arr, [2.5, 97.5])
        out[name] = [full, float(lo), float(hi)]
    return out


def word(f25, N, checks_ok):
    if N < 30 or not checks_ok:
        return "NOT EVALUABLE"
    if f25[1] >= 0.25:
        return "WIDE LENSES BREAK THE CEILING"
    if f25[2] <= 0.10:
        return "NOT CONFIRMED"
    return "NO VERDICT"


# ---------------------------------------------------------------- main
def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    say(f"EUC4R blind re-grade, Part A. MUTATE={MUTATE or 'none'}. kappa = 1/2 FITTED. Footings never pooled.")
    say("a0 used:", A0)
    for f, h in SHA256.items():
        got = sha(os.path.join(DATA, f))
        say(f"sha256 {f}: {'OK' if got == h else 'MISMATCH ' + got}")
        if got != h:
            sys.exit(2)

    key = pd.read_csv(os.path.join(DATA, KEY), low_memory=False)
    obj = pd.read_csv(os.path.join(DATA, OBJ), low_memory=False)
    df = key.merge(obj[["Unique_Identifier", "large_system_warning", "Expert_Grade"]],
                   left_on="unique_identifier", right_on="Unique_Identifier", how="left")
    assert len(df) == len(key)
    say(f"rows: key {len(key)}, object {len(obj)}, unmatched after join {int(df.Unique_Identifier.isna().sum())}")

    # ---- E2
    ida = set(key.loc[key.lens_grade == "A", "unique_identifier"])
    idb = set(key.loc[key.lens_grade == "B", "unique_identifier"])
    shared = len(ida & idb)
    grade_agree = int((df.lens_grade == df.Expert_Grade).sum())
    e2_ok = shared == 0 and not key.unique_identifier.duplicated().any()
    say(f"E2: grade A ids {len(ida)}, grade B ids {len(idb)}, shared {shared}, duplicates "
        f"{int(key.unique_identifier.duplicated().sum())} -> {'PASS' if e2_ok else 'FAIL'}; "
        f"key lens_grade == object Expert_Grade on {grade_agree}/{len(df)} rows")

    # ---- machinery checks
    checks = {}
    # point mass, a0 -> 0: M_2D/M = tanh(U) -> 1
    R = np.array([1.0, 5.0, 20.0, 100.0]) * KPC
    u, w = gl_nodes(np.arccosh(RMAX / R))
    M = 1e11 * MSUN
    m2 = R ** 2 / G * np.sum(w * law_g(G * M / (R[:, None] * np.cosh(u)) ** 2, 1e-30, "S"), axis=1)
    err = float(np.max(np.abs(m2 / M - 1)))
    checks["point_mass"] = (err < 1e-6, err)
    # g = v^2/r: M_2D/R constant (-> pi v^2 / 2G)
    R = np.array([0.5, 2.0, 8.0, 30.0]) * KPC
    u, w = gl_nodes(np.arccosh(RMAX / R))
    v2 = (250e3) ** 2
    m2 = R ** 2 / G * np.sum(w * v2 / (R[:, None] * np.cosh(u)), axis=1)
    ratio = m2 / R / (np.pi * v2 / (2 * G))
    err = float(np.max(np.abs(ratio - 1)))
    checks["sis_constant"] = (err < 1e-4, err)
    # Sersic mass fraction at r -> large
    nn = np.array([0.6, 1.0, 4.0, 10.0])
    fr = ps_enclosed_fraction(np.full(4, 1e6), np.ones(4), nn)
    err = float(np.max(np.abs(fr - 1)))
    checks["sersic_total"] = (err < 1e-10, err)
    # diagnostic only: projected Newtonian mass inside R_e for the PS body (Sersic: 0.5)
    nn = np.array([1.0, 2.0, 4.0, 6.0, 10.0])
    Re1 = np.full(nn.size, 5.0 * KPC)
    Ldiag = Lenses(Re1, Re1, nn, np.full(nn.size, 1e11 * MSUN))
    half = Ldiag.m2d(np.zeros(nn.size), 1e-30, "S") / (1e11 * MSUN)
    say("diagnostic (no gate): PS projected Newtonian mass inside R_e / M* for n =", nn.tolist(), "->",
        np.round(half, 4).tolist())

    # ---- distance convergence
    zt = np.array([0.3, 0.6, 1.0, 1.5])
    s1100, _ = sigma_cr_inf(zt, 1100.0)
    s1e4, _ = sigma_cr_inf(zt, 1e4)
    say("Sigma_cr(z_s=1100)/Sigma_cr(z_s=1e4) at z_l", zt.tolist(), "->", np.round(s1100 / s1e4, 5).tolist())

    # ---- samples
    base_cols = dict(
        te="eclipse_effective_einstein_radius", re="eclipse_effective_radius", n="eclipse_sersic_index",
        z="eclipse_median_phz", lm="eclipse_log_survived_mass_med")
    flags = (df.lens_model_success == True) & (df.final_sample == True) & (df.large_system_warning == False)  # noqa: E712
    valid_conds = {
        "theta_E > 0": df[base_cols["te"]] > 0,
        "R_eff > 0": df[base_cols["re"]] > 0,
        "0.6 <= n <= 10": (df[base_cols["n"]] >= 0.6) & (df[base_cols["n"]] <= 10),
        "z_phot > 0": df[base_cols["z"]] > 0,
        "logM > 0": df[base_cols["lm"]] > 0,
    }
    valid = np.logical_and.reduce(list(valid_conds.values()))
    samples = {}
    for grade in ("A", "B"):
        g0 = (df.lens_grade == grade) & flags
        say(f"grade {grade}: flags pass {int(g0.sum())}; removed by each validity condition (individually): "
            + ", ".join(f"{k} {int((g0 & ~v).sum())}" for k, v in valid_conds.items())
            + f"; after all five {int((g0 & valid).sum())}")
        samples[grade] = g0 & valid
    te = df[base_cols["te"]]
    sel = {
        "P_gradeA": samples["A"],
        "W_B": samples["B"] & (te >= 1.7),
        "secondary_B": samples["B"] & (te >= 1.3) & (te < 1.7),
        "complement_B": samples["B"] & (te < 1.0),
    }
    use = np.logical_or.reduce(list(sel.values()))
    d = df.loc[use].copy()

    # ---- per-lens physics
    zl = d[base_cols["z"]].to_numpy(float)
    sig, dl = sigma_cr_inf(zl)
    RE = d[base_cols["te"]].to_numpy(float) * ARCSEC * dl
    Re = d[base_cols["re"]].to_numpy(float) * ARCSEC * dl
    n = d[base_cols["n"]].to_numpy(float)
    Ms = 10.0 ** d[base_cols["lm"]].to_numpy(float) * MSUN
    Mmin = np.pi * RE ** 2 * sig
    L = Lenses(RE, Re, n, Ms)
    L2 = Lenses(RE, Re, n, Ms, nper=256)
    bcol = {}
    worst_nodes = 0.0
    n_edge = 0
    for law in LAWS:
        for ft, a0 in A0.items():
            b = L.solve_b(Mmin, a0, law)
            b2 = L2.solve_b(Mmin, a0, law)
            worst_nodes = max(worst_nodes, float(np.max(np.abs(b - b2))))
            n_edge += int(np.sum(np.abs(np.abs(b) - 4.0) < 1e-6))
            bcol[f"b_{law}_{ft}"] = b
    checks["node_doubling"] = (worst_nodes < 1e-4, worst_nodes)
    say(f"lenses at a bisection bracket edge: {n_edge}")
    for k, (ok, val) in checks.items():
        say(f"check {k}: {'PASS' if ok else 'FAIL'} ({val:.3e})")
    checks_ok = e2_ok and all(ok for ok, _ in checks.values())

    out = {"mutate": MUTATE or None, "a0": A0, "E2": {"shared": shared, "pass": e2_ok},
           "checks": {k: {"pass": bool(ok), "value": v} for k, (ok, v) in checks.items()},
           "samples": {}}
    lens_rows = d[["unique_identifier"] + list(base_cols.values())].copy()
    for k, v in bcol.items():
        lens_rows[k] = v
    for sname, m in sel.items():
        lens_rows[sname] = m.loc[use].to_numpy()
    for sname in sel:
        mk = lens_rows[sname].to_numpy(bool)
        N = int(mk.sum())
        say(f"\n== {sname}: N = {N}; theta_E range "
            f"{lens_rows.loc[mk, base_cols['te']].min():.3f}-{lens_rows.loc[mk, base_cols['te']].max():.3f} arcsec")
        so = {"N": N}
        for law in LAWS:
            for ft in A0:
                b = lens_rows.loc[mk, f"b_{law}_{ft}"].to_numpy()
                st = boot_stats(b)
                st_rs = boot_stats(b, gen="randomstate")
                rec = {"default_rng": st, "RandomState_f25": st_rs["f25"]}
                line = (f"  law {law} {ft:9s}: f25 {st['f25'][0]:.4f} [{st['f25'][1]:.4f}, {st['f25'][2]:.4f}]"
                        f" (RandomState [{st_rs['f25'][1]:.4f}, {st_rs['f25'][2]:.4f}])"
                        f"  f0 {st['f0'][0]:.4f}  b_med {st['b_med'][0]:+.4f} [{st['b_med'][1]:+.4f}, {st['b_med'][2]:+.4f}]")
                if law == "S" and sname in ("W_B", "secondary_B"):
                    w_ = word(st["f25"], N, checks_ok)
                    w_rs = word(st_rs["f25"], N, checks_ok)
                    rec["word"] = w_
                    rec["word_RandomState"] = w_rs
                    line += f"  -> {w_ if sname == 'W_B' else w_ + ' (secondary)'}"
                    if w_rs != w_:
                        line += f"  [RandomState gives {w_rs}]"
                say(line)
                so[f"{law}_{ft}"] = rec
        out["samples"][sname] = so

    say("\nE1' (comparison, not a gate): f25 law S on P = "
        f"{out['samples']['P_gradeA']['S_canonical']['default_rng']['f25'][0]:.4f} canonical / "
        f"{out['samples']['P_gradeA']['S_alt']['default_rng']['f25'][0]:.4f} alt; EUC1 quoted 0.156 / 0.139")
    words = {ft: out["samples"]["W_B"][f"S_{ft}"].get("word") for ft in A0}
    say(f"\nWORD on W_B (law S): canonical {words['canonical']} / alt {words['alt']}"
        + ("   [MUTATED RUN: not a verdict]" if MUTATE else ""))
    out["words_W_B"] = words

    exit_code = 0
    if MUTATE == "newton":
        main_json = os.path.join(HERE, "euc4r.json")
        ref = json.load(open(main_json))
        rises = {}
        for ft in A0:
            f_mut = out["samples"]["W_B"][f"S_{ft}"]["default_rng"]["f25"][0]
            f_ref = ref["samples"]["W_B"][f"S_{ft}"]["default_rng"]["f25"][0]
            rises[ft] = f_mut > f_ref
            say(f"MUTATE newton, W_B law S {ft}: f25 {f_ref:.4f} -> {f_mut:.4f}: {'RISES' if rises[ft] else 'DOES NOT RISE'}")
        out["mutation_rises"] = rises
        exit_code = 1 if all(rises.values()) else 3
        say(f"mutation twin exit code {exit_code} (1 = the twin bit as required)")

    with open(os.path.join(HERE, f"euc4r{SUFFIX}.json"), "w") as f:
        json.dump(out, f, indent=1)
    lens_rows.to_csv(os.path.join(HERE, f"euc4r_lenses{SUFFIX}.csv"), index=False, float_format="%.6g")
    with open(os.path.join(HERE, f"euc4r{SUFFIX}.out"), "w") as f:
        f.write("\n".join(LOG) + "\n")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())

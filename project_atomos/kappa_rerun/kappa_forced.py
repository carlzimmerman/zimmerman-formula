#!/usr/bin/env python3
"""kappa_forced.py -- register kappa = 1/2 as a FORCED constant and switch the forced PAIR
                      from the published {3, sqrt(8pi/3)} to {3, kappa}, NON-DESTRUCTIVELY.

WHY
---
reviews/mi_kappa_spectral_reduction_2026.py (sibling repo) proved

        a0 = kappa * c * sqrt(G rho_Lambda)        EXACTLY,   kappa = 1/2

with every pi, the 32 and the 3 cancelling.  So sqrt(8pi/3) = sqrt(8pi)[Einstein] x sqrt(1/3)
[Friedmann] is GR + FRW -- it is NOT the framework's own distinctive number.  The framework's
distinctive input is kappa = 1/2, and gate/registry.py's FORCED_CONSTRAINTS has no entry for it.

WHAT THIS MODULE DOES *NOT* DO
------------------------------
It does not edit a single committed file.  The published configuration stays bit-identical:
  * the default of the switch is "published";
  * every mutation happens inside a context manager that snapshots and restores;
  * the registry dict is mutated IN PLACE (never rebound), because exhaust.py line 81 does
    `from gate.registry import FORCED_CONSTRAINTS` -- exhaust._germ_provenance iterates the SAME
    dict object, so rebinding would be invisible to it and clear()/update() is the only correct
    restore.  This is the established pattern from overnight_pair_search.candidate_pair_registered.

THE KEY-SPACE MAPPING (worked out, not guessed)
----------------------------------------------
Two different key spaces are in play and they are NOT the same strings:

  gate/registry.py  FORCED_CONSTRAINTS  is keyed by PROVENANCE NAME
        'einstein_8pi', 'friedmann_third', 'a0_kernel_8pi3', 'Ngen_3', 'A4_dim_3',
        'S3_doublet_amp_sqrt2'

  exhaust_depth5_forced._FORCED_KEYS   holds GERM KEYS (keys of exhaust.Alphabet.atoms)
        ('3', 'sqrt(8pi/3)')

  exhaust_depth4_forced.FORCED_PROVS   holds PROVENANCE NAMES again
        frozenset({'Ngen_3', 'a0_kernel_8pi3'})

The BRIDGE between them is exhaust._germ_provenance(value): it scans FORCED_CONSTRAINTS in
insertion order and returns the first provenance whose registered value matches the germ's value
to rel-tol 1e-9.  Verified empirically on build_alphabet(None, None) (25 germs):

        germ key '3'            value 3.0                -> 'Ngen_3'
              (NOT 'A4_dim_3', which is also 3.0: insertion order puts Ngen_3 first)
        germ key 'sqrt(8pi/3)'  value 2.8944050182330705 -> 'a0_kernel_8pi3'
        every other germ                                 -> None  (free O(1))

so  _FORCED_KEYS = ('3','sqrt(8pi/3)')  <->  FORCED_PROVS = {'Ngen_3','a0_kernel_8pi3'}
and 'einstein_8pi' (5.0133), 'friedmann_third' (0.5774), 'S3_doublet_amp_sqrt2' (1.4142) are
registered but UNREACHABLE in this germ pool -- no germ has those values.

HOW THE KAPPA MODE FLIPS IT
---------------------------
  1. ADD    'kappa_half' -> 0.5   to FORCED_CONSTRAINTS.
  2. REMOVE 'einstein_8pi', 'friedmann_third', 'a0_kernel_8pi3'  (the GR+FRW kernel).  Removing
     a0_kernel_8pi3 is MANDATORY, not cosmetic: exhaust_depthN_forced._germ_recipes does
     `keys = (forced[0], forced[1], free)` and would silently keep only 2 of 3 forced germs while
     the third leaked out of the free pool.  Also, gate.forced_kernel passes on
     |distinct forced provenances| >= 2, so leaving a0_kernel_8pi3 in would let the OLD pair keep
     passing and the "re-run" would not be a different search.
  3. Re-key the germ that carries the value 1/2.  The pool ALREADY contains exactly one 0.5 germ
     ('flv_koide_cos2_angle', from targets.geometric_primitives).  We replace it IN PLACE with a
     germ literally keyed 'kappa' so formulas and Gate-B tells read honestly.  The germ pool's
     VALUE MULTISET is unchanged (asserted in assert_pool_value_identical) -- only one key's NAME
     moves, so no value is added or lost.  Set rename_germ=False to skip even that.

RESULT under kappa mode, on build_alphabet(None, None):
        _forced_keys_present -> ['3', 'kappa']        (germ keys)
        provenances          -> {'Ngen_3','kappa_half'}
        n_free germs         -> 23   (identical count to published; 'sqrt(8pi/3)' is now FREE)

SWITCH
------
  env  ATOMOS_FORCED_PAIR = published | kappa        (default: published)
  or   forced_pair(mode="kappa")  explicitly.

Exit 0 = every self-check ran.  Run this file directly for the self-report.
"""
from __future__ import annotations

import os
import sys
from typing import Dict, List, Optional

import mpmath as mp

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import exhaust as EX                       # noqa: E402
from gate import registry as REG           # noqa: E402

# --------------------------------------------------------------------------------------------
# 1. THE FORCED CONSTANT ITSELF
# --------------------------------------------------------------------------------------------
KAPPA_REGISTRY_KEY = "kappa_half"
KAPPA_GERM_KEY = "kappa"
KAPPA_GERM_SYMBOL = "kappa"
KAPPA_VALUE = 0.5

KAPPA_ENTRY = dict(
    value=KAPPA_VALUE,
    desc="kappa = 1/2, the framework's own coefficient in a0 = kappa*c*sqrt(G rho_Lambda)",
    law=("MI spectral reduction (reviews/mi_kappa_spectral_reduction_2026.py): the de Sitter "
         "response kernel reduces the acceleration scale EXACTLY to a0 = kappa c sqrt(G rho_Lambda) "
         "with kappa = 1/2 -- every pi, the 32 and the 3 cancel, so sqrt(8pi/3) = sqrt(8pi)"
         "[Einstein] x sqrt(1/3)[Friedmann] is GR+FRW bookkeeping and 1/2 is the framework's "
         "distinctive input. NOTE (honesty, per the kappa-forcing-door closure 2026-06-17): "
         "kappa=1/2 is FORCED-BY-CONSTRUCTION in the reduction, it is NOT derived from "
         "ghost-freedom/unitarity/holography -- it is registered here as a pre-fit DECLARED "
         "constraint, which is exactly what Gate B demands, and nothing more."),
)

# The GR+FRW kernel entries that the kappa mode retires (see docstring step 2).
GR_KERNEL_KEYS = ("einstein_8pi", "friedmann_third", "a0_kernel_8pi3")

# The published forced GERM keys / PROVENANCE names, for assertions.
PUBLISHED_FORCED_GERM_KEYS = ("3", "sqrt(8pi/3)")
PUBLISHED_FORCED_PROVS = ("Ngen_3", "a0_kernel_8pi3")
KAPPA_FORCED_GERM_KEYS = ("3", KAPPA_GERM_KEY)
KAPPA_FORCED_PROVS = ("Ngen_3", KAPPA_REGISTRY_KEY)

VALID_MODES = ("published", "kappa")
ENV_VAR = "ATOMOS_FORCED_PAIR"


def mode_from_env() -> str:
    """The switch. DEFAULTS TO THE PUBLISHED PAIR when the env var is absent or empty."""
    raw = (os.environ.get(ENV_VAR) or "published").strip().lower()
    if raw not in VALID_MODES:
        raise SystemExit(f"{ENV_VAR}={raw!r} invalid; use one of {VALID_MODES} "
                         f"(absent => 'published', the committed default)")
    return raw


# --------------------------------------------------------------------------------------------
# 2. THE GERM-POOL RE-KEY  (value-preserving)
# --------------------------------------------------------------------------------------------
_ORIG_DEFAULT_GERMS = EX._default_germs


def _kappa_default_germs() -> List["EX.Atom"]:
    """exhaust._default_germs with the single 0.5-valued germ RE-KEYED to 'kappa'.

    Value-preserving by construction: we swap one list element for another with the SAME value,
    so the germ VALUE multiset (and len) is untouched.  If (contrary to the audited pool) no
    0.5 germ exists, we append one and say so loudly -- but assert_pool_value_identical then
    fails, which is the intended tripwire.
    """
    base = _ORIG_DEFAULT_GERMS()
    kappa_atom = EX._make_germ(KAPPA_GERM_KEY, KAPPA_GERM_SYMBOL, KAPPA_VALUE)
    hits = [i for i, a in enumerate(base) if EX._value_key(a.value) == EX._value_key(mp.mpf("0.5"))]
    if len(hits) == 1:
        base[hits[0]] = kappa_atom
        return base
    if len(hits) == 0:
        base.append(kappa_atom)
        return base
    raise SystemExit(f"germ pool has {len(hits)} germs with value 1/2 -- ambiguous re-key, refusing")


# --------------------------------------------------------------------------------------------
# 3. THE CONTEXT MANAGER
# --------------------------------------------------------------------------------------------
class forced_pair:
    """Context manager: run the enclosed block with forced = {3, sqrt(8pi/3)} (published, the
    default and a strict no-op) or forced = {3, kappa}.

    Restores the EXACT original registry dict object contents and the original
    exhaust._default_germs function on exit, including on exception.
    """

    def __init__(self, mode: Optional[str] = None, rename_germ: bool = True):
        self.mode = (mode or mode_from_env()).strip().lower()
        if self.mode not in VALID_MODES:
            raise SystemExit(f"mode {self.mode!r} invalid; use one of {VALID_MODES}")
        self.rename_germ = rename_germ
        self._orig_registry: Optional[Dict] = None
        self._orig_germs = None

    def __enter__(self):
        # ---- guard: the published registry must look the way we documented, or bail out
        missing = [k for k in PUBLISHED_FORCED_PROVS if k not in REG.FORCED_CONSTRAINTS]
        if missing:
            raise SystemExit(f"registry is not in its published state (missing {missing}); refusing")
        if KAPPA_REGISTRY_KEY in REG.FORCED_CONSTRAINTS:
            raise SystemExit(f"{KAPPA_REGISTRY_KEY!r} is ALREADY registered -- refusing to "
                             f"overwrite (this is the refuse-overwrite rule from "
                             f"overnight_pair_search.candidate_pair_registered)")
        if self.mode == "published":
            return self                      # strict no-op: the committed configuration

        self._orig_registry = dict(REG.FORCED_CONSTRAINTS)   # shallow snapshot of the REAL dict
        self._orig_germs = EX._default_germs

        # mutate IN PLACE -- exhaust holds the same dict object by reference
        for k in GR_KERNEL_KEYS:
            REG.FORCED_CONSTRAINTS.pop(k, None)
        REG.FORCED_CONSTRAINTS[KAPPA_REGISTRY_KEY] = dict(KAPPA_ENTRY)

        if self.rename_germ:
            EX._default_germs = _kappa_default_germs
        return self

    def __exit__(self, *exc):
        if self._orig_registry is not None:
            REG.FORCED_CONSTRAINTS.clear()
            REG.FORCED_CONSTRAINTS.update(self._orig_registry)
            self._orig_registry = None
        if self._orig_germs is not None:
            EX._default_germs = self._orig_germs
            self._orig_germs = None
        return False


# --------------------------------------------------------------------------------------------
# 4. GUARDS  (each one exists because this project already shipped the corresponding bug)
# --------------------------------------------------------------------------------------------
def germ_provenance_map(alpha) -> Dict[str, Optional[str]]:
    """germ key -> provenance, computed by the REAL exhaust._germ_provenance."""
    return {g: EX._germ_provenance(float(alpha.value(g))) for g in alpha.germs}


def forced_germ_keys(alpha) -> List[str]:
    return [g for g, p in germ_provenance_map(alpha).items() if p is not None]


def free_germ_keys(alpha) -> List[str]:
    return [g for g, p in germ_provenance_map(alpha).items() if p is None]


def pool_value_multiset(alpha) -> List[str]:
    """The germ pool as a sorted list of exact value keys (mpmath 30-dps strings, NOT float64 --
    guard against bug #4, value-key precision loss)."""
    return sorted(EX._value_key(alpha.value(g)) for g in alpha.germs)


def assert_field_exists(obj, field: str, what: str):
    """Guard against bug #1 (a filter on a field that does not exist silently passes everything)."""
    ok = (field in obj) if isinstance(obj, dict) else hasattr(obj, field)
    if not ok:
        avail = sorted(obj.keys()) if isinstance(obj, dict) else sorted(vars(obj))
        raise SystemExit(f"FIELD GUARD: {what} has no field {field!r}; available: {avail}")
    return True


def assert_no_holdout(keys, what: str):
    """Guard against bug #3 (a hard-coded list re-adding a held-back holdout target by name)."""
    from targets.pdg_constants import HOLDOUT_KEYS
    leak = sorted(set(keys) & set(HOLDOUT_KEYS))
    if leak:
        raise SystemExit(f"HOLDOUT GUARD: {what} contains held-back target(s) {leak}")
    return True


# --------------------------------------------------------------------------------------------
# 5. SELF-REPORT
# --------------------------------------------------------------------------------------------
_ok = True


def _check(cond: bool, msg: str) -> bool:
    global _ok
    if not cond:
        _ok = False
    print(f"  [{'OK  ' if cond else 'FAIL'}] {msg}")
    return bool(cond)


def _banner(s: str):
    print("\n" + "=" * 98)
    print(s)
    print("=" * 98)


def main() -> int:
    import exhaust_depth5_forced as D5
    import exhaust_depth4_forced as D4

    _banner("kappa_forced -- register kappa=1/2 as forced, non-destructively")
    print(f"  switch env var      : {ENV_VAR} (absent => 'published')")
    print(f"  env currently says  : {mode_from_env()!r}")
    print(f"  registry key        : {KAPPA_REGISTRY_KEY} = {KAPPA_VALUE}")
    print(f"  germ key            : {KAPPA_GERM_KEY}")

    _banner("A. the PUBLISHED state (switch OFF) -- must be untouched")
    alpha0 = EX.build_alphabet(None, None)
    pm0 = germ_provenance_map(alpha0)
    pool0 = pool_value_multiset(alpha0)
    _check(sorted(forced_germ_keys(alpha0)) == sorted(PUBLISHED_FORCED_GERM_KEYS),
           f"forced GERM keys = {sorted(forced_germ_keys(alpha0))}")
    _check(sorted({pm0[g] for g in forced_germ_keys(alpha0)}) == sorted(PUBLISHED_FORCED_PROVS),
           f"forced PROVENANCES = {sorted({pm0[g] for g in forced_germ_keys(alpha0)})}")
    _check(tuple(D5._FORCED_KEYS) == PUBLISHED_FORCED_GERM_KEYS,
           f"exhaust_depth5_forced._FORCED_KEYS (germ keys) = {D5._FORCED_KEYS}")
    _check(set(D4.FORCED_PROVS) == set(PUBLISHED_FORCED_PROVS),
           f"exhaust_depth4_forced.FORCED_PROVS (provenance names) = {sorted(D4.FORCED_PROVS)}")
    _check(D5._forced_keys_present(alpha0) == list(PUBLISHED_FORCED_GERM_KEYS),
           f"_forced_keys_present(alpha) = {D5._forced_keys_present(alpha0)}")
    n_free0 = len(D5._free_germ_keys(alpha0))
    _check(n_free0 == 23, f"n_free germs = {n_free0}")
    _check(KAPPA_REGISTRY_KEY not in REG.FORCED_CONSTRAINTS,
           f"{KAPPA_REGISTRY_KEY!r} absent from the committed registry (as documented)")
    print("  the MAPPING, stated: germ key -> provenance")
    for g in ("3", "sqrt(8pi/3)"):
        print(f"    {g:<14} value={float(alpha0.value(g))!r:<24} -> {pm0[g]}")
    print("  registry entries that are REGISTERED but germ-UNREACHABLE in this pool:")
    for k in ("einstein_8pi", "friedmann_third", "S3_doublet_amp_sqrt2", "A4_dim_3"):
        e = REG.FORCED_CONSTRAINTS[k]
        reach = [g for g in alpha0.germs
                 if abs(float(alpha0.value(g)) - float(e["value"])) / abs(float(e["value"])) < 1e-9]
        print(f"    {k:<22} value={float(e['value']):.10g}  germs matching: {reach or 'NONE'}")

    _banner("B. a strict-no-op 'published' context")
    with forced_pair(mode="published"):
        alphaP = EX.build_alphabet(None, None)
        _check(pool_value_multiset(alphaP) == pool0, "germ pool value multiset unchanged")
        _check(D5._forced_keys_present(alphaP) == list(PUBLISHED_FORCED_GERM_KEYS),
               f"_forced_keys_present = {D5._forced_keys_present(alphaP)}")
    _check(KAPPA_REGISTRY_KEY not in REG.FORCED_CONSTRAINTS, "registry restored after exit")

    _banner("C. the KAPPA state (switch ON)")
    with forced_pair(mode="kappa"):
        alpha1 = EX.build_alphabet(None, None)
        pm1 = germ_provenance_map(alpha1)
        _check(KAPPA_REGISTRY_KEY in REG.FORCED_CONSTRAINTS,
               f"{KAPPA_REGISTRY_KEY!r} registered, value={REG.forced_value(KAPPA_REGISTRY_KEY)}")
        _check(all(k not in REG.FORCED_CONSTRAINTS for k in GR_KERNEL_KEYS),
               f"GR+FRW kernel keys retired: {GR_KERNEL_KEYS}")
        _check(len(alpha1.germs) == len(alpha0.germs),
               f"germ POOL SIZE unchanged: {len(alpha1.germs)} == {len(alpha0.germs)}")
        _check(pool_value_multiset(alpha1) == pool0,
               "germ pool VALUE MULTISET identical to published (mpmath 30-dps keys, not float64)")
        _check(sorted(forced_germ_keys(alpha1)) == sorted(KAPPA_FORCED_GERM_KEYS),
               f"forced GERM keys = {sorted(forced_germ_keys(alpha1))}")
        _check(sorted({pm1[g] for g in forced_germ_keys(alpha1)}) == sorted(KAPPA_FORCED_PROVS),
               f"forced PROVENANCES = {sorted({pm1[g] for g in forced_germ_keys(alpha1)})}")
        _check(D5._forced_keys_present(alpha1) == ["3", KAPPA_GERM_KEY],
               f"_forced_keys_present = {D5._forced_keys_present(alpha1)}  "
               f"(exactly 2 -- _germ_recipes' keys=(forced[0],forced[1],free) stays well-posed)")
        _check(pm1["sqrt(8pi/3)"] is None,
               "germ 'sqrt(8pi/3)' is now a FREE O(1) (GR+FRW, not the framework's number)")
        _check(pm1["2"] is None,
               "germ '2' is still FREE -- kappa is NOT credited to it by value")
        n_free1 = len(D5._free_germ_keys(alpha1))
        _check(n_free1 == n_free0, f"n_free germs = {n_free1} == published {n_free0}")
        _check("flv_koide_cos2_angle" not in alpha1.germs and KAPPA_GERM_KEY in alpha1.germs,
               "the single 0.5 germ was RE-KEYED flv_koide_cos2_angle -> kappa (no value added/lost)")

    _banner("D. restoration")
    alpha2 = EX.build_alphabet(None, None)
    _check(KAPPA_REGISTRY_KEY not in REG.FORCED_CONSTRAINTS, "kappa_half removed from registry")
    _check(all(k in REG.FORCED_CONSTRAINTS for k in GR_KERNEL_KEYS), "GR+FRW kernel keys restored")
    _check(EX._default_germs is _ORIG_DEFAULT_GERMS, "exhaust._default_germs restored")
    _check(pool_value_multiset(alpha2) == pool0, "germ pool value multiset restored")
    _check(D5._forced_keys_present(alpha2) == list(PUBLISHED_FORCED_GERM_KEYS),
           f"_forced_keys_present = {D5._forced_keys_present(alpha2)}")

    _banner("E. restoration survives an EXCEPTION inside the block")
    try:
        with forced_pair(mode="kappa"):
            raise RuntimeError("deliberate")
    except RuntimeError:
        pass
    _check(KAPPA_REGISTRY_KEY not in REG.FORCED_CONSTRAINTS, "registry restored after exception")
    _check(EX._default_germs is _ORIG_DEFAULT_GERMS, "_default_germs restored after exception")

    _banner("F. holdout guard (bug #3)")
    from exhaust_parallel import sm_target_keys
    from targets.pdg_constants import HOLDOUT_KEYS
    srch = sm_target_keys()
    assert_no_holdout(srch, "sm_target_keys()")
    _check(True, f"sm_target_keys() = {len(srch)} targets, HOLDOUT_KEYS={sorted(HOLDOUT_KEYS)}, "
                 f"leak=NONE")

    _banner("VERDICT")
    print("  " + ("ALL CHECKS PASS" if _ok else "** SOME CHECKS FAILED **"))
    print("=" * 98)
    return 0 if _ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

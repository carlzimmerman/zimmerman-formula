#!/usr/bin/env python3
"""Opt-in X48 launcher; no changes to the historical module or live jobs.

Example (first inspect with --dry-run):
  python3 x48_zoom_common.py --common-kmax 4 --work NEW_DIR --dry-run \
      --mass 1e12 --seed 1 --ng 48

kmax is in inverse physical-comoving Mpc, not a grid index. It is an experimental
choice, not a validated convergence setting. Remove --dry-run only when the new
simulation is authorized. All other arguments go to historical x48_zoom.main.
"""
import argparse
import ast
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "x48_zoom.py"
GENERATOR = "X48common-v1"


def transformed_initial_conditions(source):
    """Mask Pk consistently for the draw and HR conditioning, then replace dk."""
    function = next(n for n in ast.parse(source).body
                    if isinstance(n, ast.FunctionDef) and n.name == "constrained_field")
    targets = [n for n in function.body if isinstance(n, ast.Assign)
               and any(isinstance(t, ast.Name) and t.id == "dk" for t in n.targets)]
    if len(targets) != 1:
        raise RuntimeError("Expected exactly one initial dk assignment; review upstream changes")
    draws = [n for n in ast.walk(targets[0].value) if isinstance(n, ast.Call)
             and isinstance(n.func, ast.Attribute) and n.func.attr == "standard_normal"]
    if len(draws) != 2:
        raise RuntimeError("Unexpected historical Gaussian-draw construction; review upstream changes")
    # Insert immediately before the draw: the original Pk normalization is
    # retained on support. All subsequent corr(), s0/s1/s2 and CC see this Pk.
    mask = ast.parse("Pk = np.where(_common_support(ng, L, _common_kmax), Pk, 0.0)").body[0]
    function.body.insert(function.body.index(targets[0]), mask)
    replacement = ast.parse("_common_gaussian(ng, L, seed, lambda k: Pk, kmax=_common_kmax)", mode="eval").body
    targets[0].value = ast.copy_location(replacement, targets[0].value)
    return function


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--common-kmax", type=float, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    opts, legacy_args = parser.parse_known_args(argv)
    if not math.isfinite(opts.common_kmax) or opts.common_kmax <= 0:
        parser.error("--common-kmax must be finite and positive")
    identity_parser = argparse.ArgumentParser(add_help=False)
    identity_parser.add_argument("--mass", type=float, required=True)
    identity_parser.add_argument("--seed", type=int, default=1)
    identity_parser.add_argument("--ng", type=int, default=48)
    identity_parser.add_argument("--resume", action="store_true")
    identity, _ = identity_parser.parse_known_args(legacy_args)
    source = SOURCE.read_text()
    source_hash = hashlib.sha256(source.encode()).hexdigest()
    helper_hash = hashlib.sha256((HERE / "x48_common_modes.py").read_bytes()).hexdigest()
    stamps = {"ic_generator": GENERATOR, "common_kmax_Mpc_inv": opts.common_kmax,
              "common_source_sha256": source_hash, "common_helper_sha256": helper_hash}
    if opts.work.exists():
        if not identity.resume:
            parser.error("New common-mode runs require a new --work directory")
        checkpoint = opts.work / "ckpt.npz"
        if not checkpoint.is_file():
            checkpoint = opts.work / "snap_zf.npz"
        if not checkpoint.is_file():
            parser.error("No marked common-mode checkpoint/snapshot to resume")
        with np.load(checkpoint, allow_pickle=False) as saved:
            meta = json.loads(str(saved["meta"]))
        required = dict(stamps, M=identity.mass, seed=identity.seed, ng=identity.ng)
        if any(meta.get(key) != value for key, value in required.items()):
            parser.error("Checkpoint identity differs: legacy or different mode/cutoff/source/grid/seed/mass")
    elif identity.resume:
        parser.error("--resume requires a marked existing common-mode checkpoint")
    function = transformed_initial_conditions(source)  # validate even for dry-run
    if opts.dry_run:
        print(json.dumps(dict(stamps, mode="dry-run: no simulation started", work=str(opts.work),
                              mass=identity.mass, seed=identity.seed, ng=identity.ng), indent=2))
        return 0
    legacy = _load(SOURCE, "x48_historical_for_common_run")
    helper = _load(HERE / "x48_common_modes.py", "x48_common_modes_for_run")
    namespace = dict(vars(legacy), _common_gaussian=helper.gaussian_rfft,
                     _common_support=helper.support_mask, _common_kmax=opts.common_kmax)
    tree = ast.Module(body=[function], type_ignores=[])
    ast.fix_missing_locations(tree)
    exec(compile(tree, str(SOURCE), "exec"), namespace)
    common_field = namespace["constrained_field"]
    def marked_field(*args):
        q, displacement, meta = common_field(*args)
        meta.update(stamps)
        return q, displacement, meta
    legacy.constrained_field = marked_field
    prior = sys.argv
    try:
        sys.argv = [str(SOURCE), "--work", str(opts.work), *legacy_args]
        return legacy.main()
    finally:
        sys.argv = prior


if __name__ == "__main__":
    raise SystemExit(main())

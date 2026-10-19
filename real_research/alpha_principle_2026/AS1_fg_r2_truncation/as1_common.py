"""Lane AS1 shared code (see AS1_PREREGISTRATION.md).

Everything downstream of f_g is lane B's code, used BY IMPORT:
  * rg_common.py (measured inputs) is imported directly;
  * b3_forced_vs_required.py has no importable function for trial C5 (it is a script that runs and calls sys.exit),
    so it is executed once as a module with its stdout captured, and its own objects (aY_inv_at, a2_mz, fg, c5, f_needed, c6)
    are taken from the module namespace.  Nothing of the C5 chain is retyped here.
  * b1_reproduce_literature.py is executed the same way to obtain its numeric Eichhorn-Versteegen beta functions betas(x).
Lane B is not modified.  Bytecode writing is disabled so that no __pycache__ appears in lane B's directory.
"""
import sys
sys.dont_write_bytecode = True
import io
import contextlib
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE_B = HERE.parent / "B_rg_asymptotic_safety"
if str(LANE_B) not in sys.path:
    sys.path.insert(0, str(LANE_B))

import rg_common as RG  # noqa: E402  (lane B measured inputs)


def _exec_lane_b_script(name):
    """Execute a lane-B script as a module (argv cleared so its own MUTATE switch is off), capture its stdout,
    require that it exits 0, and return the module object with its namespace."""
    path = LANE_B / name
    spec = importlib.util.spec_from_file_location("laneB_" + name.replace(".py", ""), str(path))
    mod = importlib.util.module_from_spec(spec)
    saved_argv = sys.argv
    sys.argv = [str(path)]
    buf = io.StringIO()
    code = None
    try:
        with contextlib.redirect_stdout(buf):
            spec.loader.exec_module(mod)
    except SystemExit as e:
        code = e.code
    finally:
        sys.argv = saved_argv
    if code not in (0, None):
        raise RuntimeError(f"lane B script {name} exited {code}; its output:\n{buf.getvalue()}")
    mod._captured_stdout = buf.getvalue()
    return mod


_B3 = None
_B1 = None


def laneB_b3():
    global _B3
    if _B3 is None:
        _B3 = _exec_lane_b_script("b3_forced_vs_required.py")
    return _B3


def laneB_b1():
    global _B1
    if _B1 is None:
        _B1 = _exec_lane_b_script("b1_reproduce_literature.py")
    return _B1


ALPHA_INV0 = RG.ALPHA_INV0          # 137.035999177 (CODATA 2022)
FG_EH_QUOTED = 0.04795              # lane B EH value as quoted in the pre-registration (context only)
FG_REQ_QUOTED = 0.009805            # lane B C6 value as quoted in the pre-registration (context only)
EH_MISS_QUOTED = 44.12              # lane B EH miss in units of alpha^-1, as frozen in the pre-registration


def gY_star_from_fg(fg):
    """g_Y* = 4 pi sqrt(6 f_g / 41) (Eichhorn-Versteegen eq. for the interacting hypercharge fixed point)."""
    import numpy as np
    if fg <= 0:
        return None
    return 4 * np.pi * np.sqrt(6 * fg / 41)


def downstream_P(fg):
    """alpha_em^-1(0) from f_g by lane B's C5 chain (imported objects): alpha_Y^-1(M_Z) = b3.aY_inv_at(M_Z, g_Y*),
    + alpha_2^-1(M_Z) (MEASURED, b3.a2_mz) + the MEASURED hadronic-inclusive offset rg_common.DELTA_0_MZ."""
    b3 = laneB_b3()
    gs = gY_star_from_fg(fg)
    if gs is None:
        return None
    return b3.aY_inv_at(RG.MZ, gs) + b3.a2_mz + RG.DELTA_0_MZ


def classify(P, miss_threshold, labels=("AGREES", "CLOSER", "NO IMPROVEMENT")):
    """Frozen classification of AS1_PREREGISTRATION.md.  labels are passed in so that MUTATE_3 can swap two of them."""
    agrees, closer, noimp = labels
    delta = (P - ALPHA_INV0) / ALPHA_INV0
    if abs(delta) <= 0.02:
        return agrees, delta
    if abs(P - ALPHA_INV0) < miss_threshold:
        return closer, delta
    return noimp, delta

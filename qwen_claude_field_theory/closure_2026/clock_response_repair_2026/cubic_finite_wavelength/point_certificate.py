#!/usr/bin/env python3
"""Exact selected-epoch interval certificate and bridge to actual Lean definitions.

No sampling or float arithmetic decides a sign. This certifies one reconstructed
epoch only, and does not establish finite-wavelength dynamics or history-wide
regularity. The symbolic-source-to-Lean bridge is checked here, not inside Lean.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import signal
import sympy as s

HERE = Path(__file__).resolve().parent


def interval_mul(left, right):
    products = [x*y for x in left for y in right]
    return min(products), max(products)


def polynomial_interval(expression, variable, bounds):
    result = (s.S.Zero, s.S.Zero)
    for coefficient in s.Poly(expression, variable).all_coeffs():
        product = interval_mul(result, bounds)
        result = product[0]+coefficient, product[1]+coefficient
    return result


def ratio_interval(expression, variable, bounds):
    numerator, denominator = s.fraction(s.cancel(expression))
    ni = polynomial_interval(numerator, variable, bounds)
    di = polynomial_interval(denominator, variable, bounds)
    assert di[1] < 0 or di[0] > 0, "Denominator interval contains zero"
    return interval_mul(ni, (1/di[1], 1/di[0]))


def main():
    signal.alarm(180)
    source = HERE / "derive.py"
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    spec = importlib.util.spec_from_file_location("selected_epoch_source", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _, context = module.derive()
    constant_constraint = context["constraint"].subs(context["k"], 0)
    assert s.cancel(context["constraint"] - constant_constraint
                    - context["constraint_k2"]*context["k"]**2) == 0
    H = context["H"]
    point = {
        context["a"]: 1, context["gamma"]: s.Rational(1, 10**6),
        context["M"]: 1, context["A"]: s.Rational(1, 10),
        context["q"]: s.Rational(10, 11), context["U"]: s.Rational(1, 110),
        context["B0"]: s.Rational(231, 100),
        context["qd"]: -5*H/77-1/(242*H),
    }
    bounds = (s.Rational(51639, 100000), s.Rational(51640, 100000))
    assert 0 < bounds[0] and bounds[0]**2 < s.Rational(4, 15) < bounds[1]**2
    expressions = {
        "D0": constant_constraint,
        "D2": context["constraint_k2"],
        "A0": context["pre_zeta_kinetic"],
    }
    lean = HERE / "PointSigns.lean"
    text = lean.read_text()
    rows = []
    for name, expression in expressions.items():
        actual = s.cancel(expression.subs(point))
        match = re.search(r"noncomputable def point" + name
                          + r" \(H : ℝ\) : ℝ :=\s*([^\n]+)", text)
        assert match, "Missing actual Lean coefficient definition: " + name
        explicit = s.sympify(match.group(1).replace("^", "**"), locals={"H": H})
        an, ad = s.fraction(actual)
        en, ed = s.fraction(s.cancel(explicit))
        remainder = s.rem(an*ed-en*ad, H**2-s.Rational(4, 15), H)
        assert remainder == 0, "Actual-source / Lean-expression bridge failed: " + name
        original_denominator = polynomial_interval(ad, H, bounds)
        assert original_denominator[1] < 0 or original_denominator[0] > 0
        interval = ratio_interval(explicit, H, bounds)
        if name in ("D0", "D2"):
            assert interval[1] < 0, "Strict negative sign not certified: " + name
        else:
            assert interval[0] > 0, "Strict positive sign not certified: " + name
        rows.append(dict(coefficient=name, lean_expression=str(explicit),
                         exact_interval=[str(v) for v in interval],
                         exact_bridge_remainder=str(remainder),
                         original_denominator_interval=[str(v) for v in original_denominator]))
    signal.alarm(0)
    assert hashlib.sha256(source.read_bytes()).hexdigest() == source_hash, "Source changed during run"
    return dict(status="exact selected-epoch sign certificate passed", cases=rows,
                H_bounds=[str(v) for v in bounds], H_squared="4/15", H_positive=True,
                exact_constraint_affine_in_k_squared=True,
                source_sha256=source_hash,
                lean_sha256=hashlib.sha256(lean.read_bytes()).hexdigest(),
                sympy_version=s.__version__, arithmetic="exact rational interval and polynomial remainder",
                limitations=["One prescribed epoch and coupling only", "Physical k=0 auxiliary elimination is excluded",
                             "Source-to-Lean bridge is symbolic Python, not formalized GR in Lean",
                             "No gradient, mass, evolution, observational, or global-history conclusion"])


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))

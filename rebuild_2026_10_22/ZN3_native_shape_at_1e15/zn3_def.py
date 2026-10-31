# ZN3 (FROZEN_CRITERIA.md): ZN1's rule with tags at 1e13, 1e14, 1e15. Appended after ZN1's definitions; replaces zn1_shape only.
_Z3M = ("1e13", "1e14") if os.environ.get("ZN3_TWO") else ("1e13", "1e14", "1e15")
def zn1_shape(lgM, z):
    k = ZN1_SNAP if ZN1_SNAP != "nearest" else ("0.00" if z < 0.125 else "0.25" if z < 0.375 else "0.50"); T_ = [_ZS[m_][k] for m_ in _Z3M]; i_ = 0
    while i_ < len(T_) - 2 and lgM > T_[i_ + 1]["lgM"]: i_ += 1
    a, b = T_[i_], T_[i_ + 1]; w = float(np.clip((lgM - a["lgM"]) / (b["lgM"] - a["lgM"]), 0.0, 1.0))
    if lgM > T_[-1]["lgM"]: ZN1_STAT["above_top"] = ZN1_STAT.get("above_top", 0) + 1
    return (1 - w) * np.array(a["lnm"]) + w * np.array(b["lnm"]), min(a["x_edge"], b["x_edge"])

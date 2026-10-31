# ZN2 (FROZEN_CRITERIA.md): the native z = 0 shape on SPARC and the groups. Injected before sparc in FC1's grader text.
ZN2 = dict(on=not os.environ.get("ZN2_K1"), below=0, n=0, map=os.environ.get("ZN2_MAP", "tot"), rx=float(os.environ.get("ZN2_RX", "1")))
_Z2J = json.load(open(os.environ["ZN2_SHAPES"])) if not os.environ.get("ZN2_K1") else None
_Z2X = np.log(np.array(_Z2J["x"])) if _Z2J else None
_Z2T = sorted(((float(_Z2J[m_]["0.00"]["lgM"]), np.array(_Z2J[m_]["0.00"]["lnm"])) for m_ in ("1e12", "1e13", "1e14")), key=lambda t_: t_[0]) if _Z2J else []
def zn2_lnm(lg, count):
    T_ = _Z2T
    if lg <= T_[0][0]:
        if count: ZN2["below"] += 1
        return T_[0][1]
    if lg >= T_[-1][0]: return T_[-1][1]
    k_ = next(i_ for i_ in range(len(T_) - 1) if T_[i_][0] <= lg <= T_[i_ + 1][0]); w_ = (lg - T_[k_][0]) / (T_[k_ + 1][0] - T_[k_][0]); return (1 - w_) * T_[k_][1] + w_ * T_[k_ + 1][1]
def zn2_mass(Mc, rc_, r, q_):
    fc_ = NAT_RRAT / (1 + NAT_RRAT); Mt_ = Mc / fc_; lg_ = math.log10(Mt_ / MSUNE); M_, R_ = (fc_ * Mt_, (3 * Mt_ / (4 * math.pi * 200 * rc_)) ** (1 / 3)) if ZN2["map"] == "tot" else (Mc, (3 * Mc / (4 * math.pi * 200 * rc_)) ** (1 / 3))
    if q_ is not None: ZN2["n"] += 1
    ln_ = zn2_lnm(lg_, q_ is not None); x_ = np.minimum(np.asarray(r, float), R_) / (R_ * ZN2["rx"]); lx_ = np.log(np.maximum(x_, 1e-300))
    return M_ * np.exp(np.where(lx_ >= _Z2X[0], np.interp(lx_, _Z2X, ln_), ln_[0] + 2 * (lx_ - _Z2X[0])))

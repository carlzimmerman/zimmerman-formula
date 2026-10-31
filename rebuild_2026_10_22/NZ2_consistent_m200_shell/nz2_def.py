# NZ2 (FROZEN_CRITERIA.md): NZ1's core inside r_f, a uniform shell to f_c M200 at R200, then a gamma_o tail to M_fair at r_ta. Appended after NZ1's definitions.
NZ2_ON = os.environ.get("NZ2_ON") == "1"; NZ2_GO = float(os.environ.get("NZ2_GO", "2.65")); NZ2_STAT = dict(cells=0, fallback=0, flat=0, k2a=0.0, k2b=0.0); _nz1_fn0 = nz1_fn
def nz1_fn(tag, M, s, active, Mfair, rta):
    if (not NZ2_ON) or NZ1_MODE == "off" or SHAPE["s"] != "S" or ETA_USE["v"] != ETA or not active: return _nz1_fn0(tag, M, s, active, Mfair, rta)
    rf, r0_, a = nz1_core(tag, M); Mcf = math.pi * s * r0_ ** 2 * float(B(rf / r0_)); bg_ = BGS[tag]; rc_ = 3 * (100 * bg_["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); thr_ = 200 * rc_ * globals().get("ZOBS", dict(E2=1.0))["E2"]; R2_ = (3 * M * MSUNE / (4 * math.pi * thr_)) ** (1 / 3); Mc2 = FC1_F * M * MSUNE; St = NZ2_STAT; St["cells"] += 1
    if R2_ <= rf or Mc2 <= Mcf or R2_ >= rta: St["fallback"] += 1; return _nz1_fn0(tag, M, s, active, Mfair, rta)
    p_ = 3 - NZ2_GO; flat_ = Mc2 >= Mfair; St["flat"] += 1 if flat_ else 0
    def f(r):
        r = np.minimum(np.asarray(r, float), rta); core = math.pi * s * r0_ ** 2 * B(r / r0_); shell = Mcf + (Mc2 - Mcf) * (r ** 3 - rf ** 3) / (R2_ ** 3 - rf ** 3); outer = np.full_like(r, Mc2) if flat_ else Mc2 + (Mfair - Mc2) * ((np.maximum(r, R2_) / R2_) ** p_ - 1) / ((rta / R2_) ** p_ - 1)
        return np.where(r <= rf, core, np.where(r <= R2_, shell, outer))
    St["k2a"] = max(St["k2a"], abs(float(f(np.array([R2_]))[0]) / Mc2 - 1)); St["k2b"] = max(St["k2b"], 0.0 if flat_ else abs(float(f(np.array([rta]))[0]) / Mfair - 1)); return f

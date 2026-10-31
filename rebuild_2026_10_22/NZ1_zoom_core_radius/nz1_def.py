# NZ1 (criteria in FROZEN_CRITERIA.md): r0 from the zooms. Injected before grade_clusters in FC1's grader text, after MA1's definition.
NZ1_MODE = os.environ.get("NZ1_MODE", "all"); NZ1_R0X = float(os.environ.get("NZ1_R0X", "1")); NZ1_STAT = dict(cells=0, no_tail=0, k1a=0.0, k1b=0.0, k2a=0.0, k2b=0.0, gam=[], a_seen=[]); NZ1_LAST = {}
def nz1_core(tag, M):
    Sc = sigma_coll(tag, M)[0]; rf = math.sqrt(3 * (M / 2) / (4 * math.pi * Sc)) * 3.0857e16; eta = eta_of(cf_of(M))
    a = brentq(lambda a_: 4 / 3 * a_ * a_ / float(B(a_)) - eta, 1.01, 1e4, xtol=1e-12); NZ1_STAT["k1a"] = max(NZ1_STAT["k1a"], abs(4 / 3 * a * a / float(B(a)) / eta - 1)); NZ1_STAT["a_seen"].append(a)
    return rf, rf / a * NZ1_R0X, a
def nz1_r0(tag, M, active, budget):
    if NZ1_MODE != "all" or SHAPE["s"] != "S" or ETA_USE["v"] != ETA or not active: return budget()
    return nz1_core(tag, M)[1]
def nz1_fn(tag, M, s, active, Mfair, rta):
    if NZ1_MODE == "off" or SHAPE["s"] != "S" or ETA_USE["v"] != ETA or not active:
        r0_ = solve_r0(Mfair, rta, s); return lambda r: math.pi * s * r0_ ** 2 * B(np.minimum(r, rta) / r0_)
    rf, r0_, a = nz1_core(tag, M); Mcf = math.pi * s * r0_ ** 2 * float(B(rf / r0_)); St = NZ1_STAT; St["cells"] += 1
    if NZ1_R0X == 1: St["k1b"] = max(St["k1b"], abs(Mcf / (FC1_F * M * MSUNE / 2) - 1))
    rhof = s / r0_ * (1 + (rf / r0_) ** 2) ** -1.5; St["k2b"] = max(St["k2b"], abs(rhof / float(rho_shape(rf, r0_, s / r0_)) - 1)); NZ1_LAST.update(rf_kpc=rf / 3.0857e19, r0_kpc=r0_ / 3.0857e19, a=a, gamma=None)
    if rta <= rf or Mcf >= Mfair:
        St["no_tail"] += 1; return lambda r: np.minimum(math.pi * s * r0_ ** 2 * B(np.minimum(r, rta) / r0_), Mfair)
    L = math.log(rta / rf); tgt = (Mfair - Mcf) / (4 * math.pi * rhof * rf ** 3)
    I_ = lambda g: L if abs(3 - g) < 1e-9 else (math.exp((3 - g) * L) - 1) / (3 - g)
    gam = brentq(lambda g: I_(g) - tgt, -20.0, 60.0, xtol=1e-12); St["gam"].append(gam); St["k2a"] = max(St["k2a"], abs((Mcf + 4 * math.pi * rhof * rf ** 3 * I_(gam)) / Mfair - 1)); NZ1_LAST["gamma"] = gam
    def f(r):
        r = np.minimum(np.asarray(r, float), rta); y = np.maximum(r / rf, 1.0); t_ = np.log(y) if abs(3 - gam) < 1e-9 else (y ** (3 - gam) - 1) / (3 - gam)
        return np.where(r <= rf, math.pi * s * r0_ ** 2 * B(r / r0_), Mcf + 4 * math.pi * rhof * rf ** 3 * t_)
    return f

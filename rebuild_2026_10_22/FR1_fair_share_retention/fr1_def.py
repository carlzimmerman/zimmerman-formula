# FR1 (FROZEN_CRITERIA.md): measured Y500(M500) map, injected before zn1_fn through ZN1_XFILE. Native shape, tail and grader unchanged. No eRASS1 M500, no shear.
_FRL = json.loads(os.environ["FR1_LINE"]); _FRF = float(os.environ["X73_FSTAR"]); _FRH = dict(h=None, foot=None, tag=None); _FRI = dict(i=None); _FRD = {}; _FRS_ = json.load(open(os.environ["ZN1_SHAPES"]))
def _fr_x500(lgM):
    def one(key):
        a = _FRS_[key]["0.25"]; x = np.array(_FRS_["x"]); q = np.array(a["lnm"]) - 3 * np.log(x) - math.log(2.5); j = np.where(q >= 0)[0].max(); return math.exp(np.interp(0.0, [q[j + 1], q[j]], [math.log(x[j + 1]), math.log(x[j])]))
    a, b = one("1e14"), one("1e15"); w = float(np.clip((lgM - _FRS_["1e14"]["0.25"]["lgM"]) / (_FRS_["1e15"]["0.25"]["lgM"] - _FRS_["1e14"]["0.25"]["lgM"]), 0.0, 1.0)); return (1 - w) * a + w * b
def _fr_y500(lgM_h, Mb_h, h):
    q = 0.7 / h; x = (np.log10(np.maximum(Mb_h, 1e-200) / MSUNE) - math.log10(1 + _FRF) - 2.5 * math.log10(q)) if _FRL["x"] == "G" else (lgM_h - math.log10(q)); return _FRL["a"] + _FRL["b"] * (x - _FRL["piv"]) + math.log10(1 + _FRF) + 1.5 * math.log10(q)
def zn1_m200_fs(Mb, z):
    bg = BGS["A_c2b_refit"]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); thr = 200 * rc * (NAT_OM * (1 + z) ** 3 + 1 - NAT_OM); h = BGS[_FRH["tag"]]["h"] if _FRH["tag"] else bg["h"]
    if _FRL["mode"] == "one":
        d = (1 + NAT_RRAT) * Mb / (4 / 3 * math.pi * RM ** 3); i = np.where(d >= thr)[0]
        if len(i) == 0: _FRH["F"] = 1.0; return None, None, thr
        i = int(i.max()); lr = math.log(RM[i]) + (math.log(thr) - math.log(d[i])) / (math.log(d[i + 1]) - math.log(d[i])) * (math.log(RM[i + 1]) - math.log(RM[i])); R = math.exp(lr); _FRH["F"] = 1.0; return thr * 4 / 3 * math.pi * R ** 3, R, thr
    if _FRL.get("carry") is not None:  # POST-RESULT row only: Y200 = line(M500) x 10^carry at R200, X-COP's measured carry in place of GS1's slope + ZN4's shape
        V = 4 / 3 * math.pi * RM ** 3; lgM2 = np.log10(thr * V / MSUNE); lgM5 = lgM2 + math.log10(2.5 * _fr_x500(14.5) ** 3); lgF = _fr_y500(lgM5, Mb, h) + _FRL["carry"]; d = (1 + NAT_RRAT) * Mb / 10 ** lgF / V; i = np.where(d >= thr)[0]
        if len(i) == 0 or i.max() + 1 >= len(RM): _FRH["F"] = 1.0; return None, None, thr
        i = int(i.max()); lr = math.log(RM[i]) + (math.log(thr) - math.log(d[i])) / (math.log(d[i + 1]) - math.log(d[i])) * (math.log(RM[i + 1]) - math.log(RM[i])); R2 = math.exp(lr); M2 = thr * 4 / 3 * math.pi * R2 ** 3; F = (1 + NAT_RRAT) * float(np.interp(R2, RM, Mb)) / M2; x5 = _fr_x500(14.5); R5 = x5 * R2; _FRH.update(F=F, M5=M2 * 2.5 * x5 ** 3, R5=R5, Mb5=float(np.interp(R5, RM, Mb)), Mb2=float(np.interp(R2, RM, Mb))); return M2, R2, thr
    t5 = 2.5 * thr; V = 4 / 3 * math.pi * RM ** 3; lgM = np.log10(t5 * V / MSUNE); lgY = _fr_y500(lgM, Mb, h); d = (1 + NAT_RRAT) * Mb / 10 ** lgY / V; i = np.where(d >= t5)[0]
    if len(i) == 0: _FRH["F"] = 1.0; return None, None, thr
    i = int(i.max())
    if i + 1 >= len(RM): _FRH["F"] = 1.0; return None, None, thr
    lr = math.log(RM[i]) + (math.log(t5) - math.log(d[i])) / (math.log(d[i + 1]) - math.log(d[i])) * (math.log(RM[i + 1]) - math.log(RM[i])); R5 = math.exp(lr); M5 = t5 * 4 / 3 * math.pi * R5 ** 3; M2 = M5 / 0.7
    for _ in range(12): x = _fr_x500(math.log10(M2 / MSUNE)); M2 = M5 / (2.5 * x ** 3)
    R2 = (3 * M2 / (4 * math.pi * thr)) ** (1 / 3); Mb2 = float(np.interp(R2, RM, Mb)); Mb5 = float(np.interp(R5, RM, Mb)); F = (1 + NAT_RRAT) * Mb2 / M2; _FRH.update(F=F, M5=M5, R5=R5, Mb5=Mb5, Mb2=Mb2); return M2, R2, thr
def _fr_rec(foot, tag, pp, z, fn, M2, R2):
    if _FRL["mode"] == "one" or M2 is None: return
    i = _FRI["i"]; k = f"{foot}|{tag}|{i if i is not None else 'x%.5f' % z}"; R5 = _FRH["R5"]; Mc5 = float(np.asarray(fn(np.array([R5])))[0]); y5m = (1 + NAT_RRAT) * _FRH["Mb5"] / (Mc5 + _FRH["Mb5"]); yl = 10 ** float(_fr_y500(math.log10(_FRH["M5"] / MSUNE), _FRH["Mb5"], BGS[tag]["h"]))
    _FRD[k] = dict(i=i, z=z, lgM200=math.log10(M2 / MSUNE), lgM500=math.log10(_FRH["M5"] / MSUNE), R200=R2, R500=R5, Y200=_FRH["F"], Y500_line=yl, Y500_model=y5m, carry=_FRH["F"] / yl, Mbt=float(pp["Mb"][-1]) / MSUNE, Mb200=_FRH["Mb2"] / MSUNE, Mfair=pp["Mfair"] / MSUNE, rta=pp["rta"], Mc200=float(np.asarray(fn(np.array([R2])))[0]) / MSUNE, Mcta=float(np.asarray(fn(np.array([pp["rta"]])))[0]) / MSUNE)
import atexit
atexit.register(lambda: json.dump(_FRD, open(os.environ["FR1_DUMP"], "w")) if os.environ.get("FR1_DUMP") else None)

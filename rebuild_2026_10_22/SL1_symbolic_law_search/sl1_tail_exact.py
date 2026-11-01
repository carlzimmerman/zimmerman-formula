# SL1 tail: regrades trees through the grader's own dvecN. Trees come from SL1_TREES (JSON list of [A, B] as nested lists), results to SL1_OUT. Reads only.
import time as _tm
os.environ["SL1_HERE"] = os.environ["SL1_LANE"]; _NS = {"__name__": "sl1_lib"}; _SRC = open(os.path.join(os.environ["SL1_LANE"], "discover_law.py")).read().split('if __name__ == "__main__" and "--sweep"')[0]; exec(compile(_SRC, "discover_law", "exec"), _NS)
_D = _NS["Data"](); _ev, _Bf, _kc, _KEYS = _NS["ev"], _NS["Bf"], _NS["keys_core"], _NS["KEYS"]; _FX = lambda t: t if isinstance(t, str) else tuple(_FX(c) if i else c for i, c in enumerate(t))
_L = json.load(open(os.environ["SL1_TREES"])); _RES = []; _t0 = _tm.time()
def _exact(At, Bt, foot):
    a0 = A0[foot]; o = {}
    for hk in HK:
        s_ = _D.cl[hk]["s"]; Ar = s_.rho(At) if not isinstance(At, float) else np.full(N, At); V = np.zeros((N, 8))
        for i in ALLI:
            i = int(i); pp = prep(i, "canonical", hk); rr = np.minimum(RM, pp["rta"]); M0 = s_.Mout[i] * _Bf(rr / s_.r0[i]) / _Bf(s_.R[i] / s_.r0[i]); re = Ar[i] * s_.r0[i]; Mc = s_.Mout[i] * _Bf(rr / re) / _Bf(s_.R[i] / re)
            if Bt != "1":
                x = dict(xb=GE * pp["Mb"] / RM ** 2 / a0, xc=GE * M0 / RM ** 2 / a0, fl=pp["Mb"] / M0, q=s_.V["q"][i]); Mc = Mc * np.broadcast_to(_ev(Bt, x), RM.shape)
            V[i] = dvecN(i, "canonical", hk, pp["Mb"] + Mc)
        PREP.clear(); o[hk] = _kc(_D.C["clusters"], V, foot, hk).tolist()
    return o
for a_, b_, feet_ in _L:
    a_ = a_ if isinstance(a_, float) else _FX(a_); b_ = _FX(b_); _RES.append(dict(A=_NS["to_s"](a_) if not isinstance(a_, float) else a_, B=_NS["to_s"](b_), Z={f_: _exact(a_, b_, f_) for f_ in feet_})); print(f"exact {len(_RES)}/{len(_L)} {_tm.time()-_t0:.0f} s", flush=True)
json.dump(dict(keys=_KEYS, res=_RES), open(os.environ["SL1_OUT"], "w"), default=float); sys.exit(0)

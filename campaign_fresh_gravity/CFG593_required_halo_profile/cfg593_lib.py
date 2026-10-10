"""CFG593 library (FROZEN_CRITERIA.md section 2): the declared total-profile family and its CFG556 halo-model evaluation.

Family (x_e, f, y), the same for every halo:
  settled   S_set(r) = S(min(r, r_in)) + f [S(min(r, r_e)) - S(min(r, r_in))],  r_e = x_e r_ta, r_in = y r_M  (r_in >= r_e: S(min(r, r_e)))
  supply cap: S_set(r_e) <= (1 - f_b) M_ta, else the edge is pulled in to where S_set reaches the supply
  unsettled density ~ rho_L(r) h(r), h = 0 inside min(r_in, r_e), 1 - f on [r_in, r_e], 1 beyond r_e; normalised by M(<r_ta) = M_ta
  baryons inside r_e follow the declared shape; any baryons beyond r_e are carried in the conserved remainder (CFG556's convention)
Read-only reuse: CFG556's halo model (exec'd up to its run block).
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, io, math, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg593_work"))

XE_GRID = [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.70, 0.85, 1.00]
F_GRID = [round(0.1 * i, 1) for i in range(11)]
Y_GRID = [0, 1, 3, 10]


def family_points():
    pts = []
    for xe in XE_GRID:
        for f in F_GRID:
            for y in (Y_GRID if f < 1.0 else [0]):
                pts.append((xe, f, y))
    return pts


def family_cum(r, mb, S, ML, Mta, re, rin, f, supply=None, cap=True):
    """Total M(<r) on grid r (increasing; r[-1] = r_ta).  mb, S, ML: cumulative arrays on r (ML(r_ta) = M_ta).
    re, rin: radii (should be grid nodes for exactness).  Returns (M, info).  cap=False only for the K1 control."""
    def at(arr, x):
        return float(np.interp(x, r, arr))
    rin_ = min(rin, re)
    S_in = np.interp(np.minimum(r, rin_), r, S)
    S_e = np.interp(np.minimum(r, re), r, S)
    Sset = S_in + f * (S_e - S_in)
    capped_supply = False
    if cap and supply is not None and Sset[-1] > supply * (1 + 1e-12):
        # edge pulled in to where S_set reaches the supply (linear interpolation on the grid, as CFG556 emg)
        i = int(np.nonzero(Sset >= supply)[0][0])
        if i == 0:
            re_new = r[0]
        else:
            re_new = r[i - 1] + (supply - Sset[i - 1]) * (r[i] - r[i - 1]) / (Sset[i] - Sset[i - 1])
        return None, dict(re_new=float(re_new))           # caller rebuilds the grid with re_new as a node and calls again with re = re_new
    mb_e = np.interp(np.minimum(r, re), r, mb)
    ML_e, ML_in = at(ML, re), at(ML, rin_)
    if rin < re:
        Uc = (1 - f) * (np.interp(np.clip(r, rin_, re), r, ML) - ML_in) + (np.interp(np.maximum(r, re), r, ML) - ML_e)
    else:
        Uc = np.interp(np.maximum(r, re), r, ML) - ML_e
    Utot = Mta - mb_e[-1] - Sset[-1]
    Uend = Uc[-1]
    if Uend <= Mta * 1e-14:
        rem = max(Utot, 0.0)
        M = mb_e + Sset + rem * ML / Mta
        q = 0.0; A = float("nan")
    else:
        A = Utot / Uend
        M = mb_e + Sset + Utot * Uc / Uend
        q = 1.0 - A
    return M, dict(re=float(re), rin=float(rin_), q=float(q), A=float(A), Sset_e=float(Sset[-1]), Utot=float(Utot), capped_supply=capped_supply)


# ---------------------------------------------------------------------------------------------------------------- CFG556 machinery
_H = None


def H556():
    global _H
    if _H is None:
        P556 = os.path.join(LANES, "CFG556_halo_model_matter_power", "cfg556_halo_model.py")
        src = open(P556).read(); cut = src.index("# ------------------------------------------------------------------ run")
        H = {"__file__": P556, "__name__": "cfg556_ro"}
        e = os.environ.pop("CFG556_MUTATE", None)
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src[:cut], "cfg556_ro", "exec"), H)
        if e is not None:
            os.environ["CFG556_MUTATE"] = e
        _H = H
    return _H


def hm_profile(hb, foot, xe, f, y, baryons="cen", mode="family"):
    """family profile for one CFG556 halo.  mode 'family' (x_e constant), 'census' (census edge, cap off; K1), 'emg' (supply edge; K1)."""
    H = H556()
    rgrid, M_L, baryon_cum, nu_k, fret_of = H["rgrid"], H["M_L"], H["baryon_cum"], H["nu_k"], H["fret_of"]
    G, h, FB, A0MPC = H["G"], H["h"], H["FB"], H["A0MPC"]
    rta, Mta = hb["rta"], hb["Mta"]
    fr = fret_of(math.log10(Mta))
    Mb = fr * FB * Mta; supply = (1 - FB) * Mta; a0 = A0MPC[foot]
    rM = math.sqrt(G * Mb * h / a0)
    cap = True
    if mode == "census":
        re = min(rM / math.log1p(fr * FB / (1 - FB)), rta); f, rin = 1.0, 0.0; cap = False; baryons = "cen"
    elif mode == "emg":
        re = rta; f, rin = 1.0, 0.0; baryons = "emg"
    else:
        re = min(xe * rta, rta); rin = y * rM
    Rt = re if baryons == "cen" else rta
    r0 = rgrid(hb, rta)

    def build(re_, rin_):
        nodes = [x for x in (re_, rin_) if 0 < x < rta]
        r = np.unique(np.concatenate([r0, nodes]))
        mb = baryon_cum(hb, Mb, r, Rt)
        yv = G * mb * h / (np.maximum(r, 1e-30) ** 2 * a0)
        S = np.where(r > 0, mb * nu_k(yv), 0.0) - mb
        return r, mb, S, M_L(hb, r)
    r, mb, S, ML = build(re, rin)
    M, inf = family_cum(r, mb, S, ML, Mta, re, rin, f, supply, cap)
    if M is None:
        re2 = inf["re_new"]
        r, mb, S, ML = build(re2, rin)
        M, inf = family_cum(r, mb, S, ML, Mta, re2, rin, f, supply, cap=False)
        inf["capped_supply"] = True
    inf.update(fret=fr, rM=rM, re_over_rta=inf["re"] / rta)
    return r, M, inf


def hm_R(foot, xe, f, y, baryons="cen", mode="family", U_only=False):
    """R(k) = 1 + (P_F,ta - P_L,ta) / P_L,std (CFG556 PRIMARY scope) for the family point; also K5 conservation and diagnostics."""
    H = H556()
    HB = H["HB"]; U_set = H["U_set"]
    cons = [0.0]; infos = []

    def fn(hb):
        r, M, inf = hm_profile(hb, foot, xe, f, y, baryons, mode)
        cons[0] = max(cons[0], abs(M[-1] - hb["Mta"]) / hb["Mta"])
        infos.append(inf)
        return r, M, inf
    U, _ = U_set(fn)
    return U, infos, cons[0]


_REF = {}


def hm_refs():
    """P_L,std and P_L,ta (CFG556 exactly)."""
    if not _REF:
        H = H556()
        Ustd = H["U_std"](); Pstd, _, _ = H["spectra_std"](Ustd)
        Ulta, _ = H["U_set"](lambda hb: (lambda r: (r, H["M_L"](hb, r), {}))(H["rgrid"](hb, hb["rta"])))
        Plta, _, _ = H["spectra_ta"](Ulta)
        _REF.update(Pstd=Pstd, Plta=Plta)
    return _REF


def R_of_U(U):
    H = H556(); ref = hm_refs()
    PF, _, _ = H["spectra_ta"](U)
    return 1 + (PF - ref["Plta"]) / ref["Pstd"]


def ML_shape(lMta_h):
    """x -> M_L(x r_ta) / M_ta for a CFG556 NFW halo of catchment mass 10**lMta_h [Msun/h] (z = 0 shape)."""
    H = H556()
    lm = float(np.interp(lMta_h, np.log10(H["MTA"]), np.log10(H["MM"])))
    hb = H["halo_basics"](10 ** lm)
    return lambda x: H["M_L"](hb, np.asarray(x) * hb["rta"]) / hb["Mta"], hb

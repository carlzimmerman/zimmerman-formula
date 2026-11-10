"""SCS3 maps: SCS2's backgrounds (scs2_aqual.py, copied unchanged into this folder) solved at more resolutions, with the
quantities of FROZEN_CRITERIA.md (eff0ae1861) section 2 per background and resolution:
  - SCS2's map summary (Q_neg/Q_pos, min D.P, where);
  - route L: Gamma_loc^2 = -4 pi G D.P u (2 + u) (exact symbol along the field), its maximum over off-plane unmasked cells,
    location and e-folding time; route L-tilde with route 2's discrete symbol (1 - mt)/mt, mt = min(J_rr, J_tt[, J_perp]);
  - the region (D.P < 0 by SCS2's threshold; Gamma_loc > 1/t_H) in r_e and R_d; whether it reaches the disc;
  - the sheet's surface phantom density Sigma_ph(R) (thin discs);
  - MUTATE M1 (G -> -D.P) and M2 (grid-artefact spike) route-L values on the same backgrounds (separate keys);
  - the far-field closed-form comparison (reported) and orbital times.
Resolutions: AX R0-R3 (base (48,24), (72,36), (108,54), (162,81)); PL R0-R1 ((48,16,16), (72,24,24)); R2 (108,36,36) only
via SCS3_PL_R2=1 after the memory probe.  Solver caches go to $SCS3_CACHE (scratchpad), never the repo.
Preemptible: results are written to scs3_maps_partial.json after every background; SIGTERM writes and exits; a rerun
resumes.  SCS3_SET selects: 'AX' (axial + isolated primaries), 'PL', 'DOMAIN', 'THICK_AX', 'THICK_PL'.
TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, math, time, resource, signal
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scs2_aqual as S

G = S.G
KPCKMS_TO_S = 3.0857e16          # 1 / (km/s/kpc) in s
GYR = 3.15576e16                 # s
T_H = 13.8                       # Gyr, age of the universe (criteria section 2)
AX_BASE = [(48, 24), (72, 36), (108, 54), (162, 81), (243, 121), (364, 182), (546, 273)]  # R4, R5: A1; R6: A4
A4 = os.environ.get("SCS3_A4") == "1"          # amendment A4 (b34295ebcd): axial R6
A1 = os.environ.get("SCS3_A1") == "1" or os.environ.get("SCS3_A2") == "1" or A4
A2 = os.environ.get("SCS3_A2") == "1"          # amendment A2 (63ed365df0): PL / THICK_PL polar-axis row excluded
ITER = os.environ.get("SCS3_ITER") == "1"      # amendments A2/A3: the PL R2 solver (MMD-ordered direct LU)
PL_BASE = [(48, 16, 16), (72, 24, 24), (108, 36, 36)]
CACHE = os.environ.get("SCS3_CACHE", os.path.join(HERE, "_cache"))
os.makedirs(CACHE, exist_ok=True)
SET = os.environ.get("SCS3_SET", "AX")
RMAX_FAC = float(os.environ.get("SCS3_RMAX_FAC", "10"))


def make_grid_res(kind, M, Rd, a0, ge, axis, res):
    """SCS2's make_grid with resolutions R0..R3 (R0, R1 identical to SCS2's coarse / fine and 3D grids)."""
    re = (math.sqrt(G * M * a0) / (ge * a0)) if ge > 0 else 0.0
    r_max = max(1e3 * Rd, RMAX_FAC * re)
    r_min = 1e-4 * Rd
    scale = math.log(r_max / r_min) / math.log(r_max / (0.02 * Rd))
    if ge > 0 and axis == "x":
        nr0, nt, np_ = PL_BASE[res]
        return S.Grid(r_min, r_max, int(round(nr0 * scale)), nt, np_, "half")
    nr, nt = AX_BASE[res]
    nr = int(round(nr * scale))
    if ge > 0 and axis == "z":
        return S.Grid(r_min, r_max, nr, 2 * nt, 1, "full")
    return S.Grid(r_min, r_max, nr, nt, 1, "half")


S.make_grid = make_grid_res      # background() looks make_grid up in its module at call time


def a1_mask(bg, spec):
    """amendment A1: also mask every cell below the R0 grid's 20-shell edge (in place on bg['dp'])."""
    g0 = make_grid_res(spec["kind"], bg["M"], bg["Rd"], bg["a0"], spec["ge"], spec["axis"], 0)
    r_edge = g0.rf[20]
    g = bg["g"]
    bg["dp"][g.rc < r_edge] = np.nan
    return r_edge


def sheet_mask(g, kind):
    m = np.zeros(g.shape, bool)
    if kind in ("expo", "kuzmin", "expo+bulge"):
        if g.tmode == "half":
            m[:, -1, :] = True
        else:
            m[:, g.nt // 2 - 1, :] = True; m[:, g.nt // 2, :] = True
    return m


def excl_mask(g, kind):
    """cells excluded from route L / L-tilde / region: the sheet, and under A2 the 3D grid's first theta row."""
    m = sheet_mask(g, kind)
    if A2 and g.np_ > 1:
        m[:, 0, :] = True
    return m


if ITER:
    # amendment A3 (fe9811fe03): A2's CG fallback replaced by the same direct LU with the MMD_AT_PLUS_A ordering
    import scipy.sparse.linalg as _spla

    class _Shim:
        def __getattr__(self, k):
            return getattr(_spla, k)
        def spsolve(self, A, b):
            lu = _spla.splu(A.tocsc(), permc_spec="MMD_AT_PLUS_A")
            x = lu.solve(b)
            del lu
            return x
    S.spla = _Shim()


def gamma_maps(bg, dp=None):
    """Gamma_loc^2 (s^-2) by the exact symbol and by route 2's discrete symbol, per cell (NaN where masked)."""
    g = bg["g"]
    dp = bg["dp"] if dp is None else dp
    gr, gt, gp = bg["grads"]; gm = np.sqrt(gr ** 2 + gt ** 2 + gp ** 2)
    u = gm / bg["a0"]
    fourpiGrho = 4 * np.pi * G * dp                        # (km/s/kpc)^2
    Gam2 = -fourpiGrho * u * (2 + u) / KPCKMS_TO_S ** 2    # s^-2
    Jpar = 1 / (1 + u) ** 2; Jperp = 1 / (1 + u)
    ghr = gr / np.maximum(gm, 1e-300); ght = gt / np.maximum(gm, 1e-300)
    Jrr = Jperp + (Jpar - Jperp) * ghr ** 2; Jtt = Jperp + (Jpar - Jperp) * ght ** 2
    mt = np.minimum(Jrr, Jtt)
    if g.np_ > 1:
        mt = np.minimum(mt, Jperp)
    Gam2t = -fourpiGrho * (1 - mt) / mt / KPCKMS_TO_S ** 2
    return Gam2, Gam2t, u


def efold_gyr(G2):
    return float(1 / (math.sqrt(G2) * GYR)) if G2 > 0 else None


def where_of(g, sel, Rd, re):
    r = g.rc[:, None, None] * np.ones(g.shape)
    R = g.R; Z = g.Z
    th = np.degrees(np.arctan2(R, Z))
    if not sel.any():
        return None
    return dict(n=int(sel.sum()), r_over_re=[float(r[sel].min() / re), float(r[sel].max() / re)] if re > 0 else None,
                r_over_Rd=[float(r[sel].min() / Rd), float(r[sel].max() / Rd)],
                theta_deg=[float(th[sel].min()), float(th[sel].max())],
                reaches_disc=bool(np.any(sel & (r < 5 * Rd) & (np.abs(Z) < Rd))))


def route_L(bg, kind, dp=None):
    g = bg["g"]
    Gam2, Gam2t, u = gamma_maps(bg, dp)
    dpu = bg["dp"] if dp is None else dp
    ok = np.isfinite(dpu)
    off = ok & ~excl_mask(g, kind)
    re = math.sqrt(G * bg["M"] * bg["a0"]) / (bg["ge"] * bg["a0"]) if bg["ge"] > 0 else 0.0
    out = {}
    for lab, A in (("L", Gam2), ("Lt", Gam2t)):
        Aoff = np.where(off, A, -np.inf)
        k = int(np.argmax(Aoff)); idx = np.unravel_index(k, g.shape)
        G2 = float(Aoff[idx])
        r = float(g.rc[idx[0]]); th = float(np.degrees(g.tc[idx[1]])); ph = float(np.degrees(g.pc[idx[2]]))
        out[lab] = dict(Gamma2_max_s2=G2, efold_gyr=efold_gyr(G2), r_kpc=r, r_over_re=r / re if re > 0 else None,
                        r_over_Rd=r / bg["Rd"], theta_deg=th, phi_deg=ph, u_there=float(u[idx]),
                        dp_there=float(dpu[idx]))
    # region where at least one e-fold in t_H
    fast = off & (Gam2 > (1 / (T_H * GYR)) ** 2)
    out["region_fast"] = where_of(g, fast, bg["Rd"], re)
    # all cells (sheet included) for the record: what route 2 sees
    Aall = np.where(ok, Gam2t, -np.inf)
    out["Lt_all_cells_Gamma2_max_s2"] = float(np.max(Aall))
    return out


def sheet_stats(bg, kind):
    g = bg["g"]
    if kind not in ("expo", "kuzmin", "expo+bulge"):
        return None
    sm = sheet_mask(g, kind)
    dth = np.diff(g.tf)
    thick = g.rc[:, None, None] * dth[None, :, None] * np.ones(g.shape)
    col = np.where(sm & np.isfinite(bg["dp"]), bg["dp"] * thick, 0.0).sum(axis=1)        # (nr, np_) Msun/kpc^2
    valid = np.isfinite(bg["dp"][:, 0, 0])
    col = col[valid]; rr = g.rc[valid]
    neg = col < 0
    res = dict(Sigma_ph_min=float(col.min()), Sigma_ph_max=float(col.max()), n_negative_columns=int(neg.sum()))
    if neg.any():
        ii = np.where(neg.any(axis=1))[0]
        res["negative_R_over_Rd"] = [float(rr[ii].min() / bg["Rd"]), float(rr[ii].max() / bg["Rd"])]
        # baryonic surface density there, for scale
        Rn = rr[ii]
        if kind == "kuzmin":
            Sb = bg["M"] * bg["Rd"] / (2 * np.pi * (Rn ** 2 + bg["Rd"] ** 2) ** 1.5)
        else:
            Sb = bg["M"] / (2 * np.pi * bg["Rd"] ** 2) * np.exp(-Rn / bg["Rd"])
        res["Sigma_b_range_there"] = [float(Sb.min()), float(Sb.max())]
        res["Sigma_ph_min_over_Sigma_b"] = float(np.min(col[ii].min(axis=-1) / Sb))
    return res


def farfield_compare(bg, kind):
    """reported: route L against Gamma_ff^2 = -K D.P_ff x(2+x) on negative band cells at 4-8 r_e (0.1 a0)."""
    if bg["ge"] <= 0:
        return None
    g = bg["g"]; M = bg["M"]; a0 = bg["a0"]; x = bg["ge"]
    re = math.sqrt(G * M * a0) / (x * a0)
    mue = x / (1 + x); Le = 1 / (1 + x); A = G * M / (mue * math.sqrt(1 + Le))
    par = g.Z if bg["axis"] == "z" else g.X
    r = np.sqrt(g.R ** 2 + g.Z ** 2)
    perp2 = r ** 2 - par ** 2
    s = np.sqrt(perp2 + par ** 2 / (1 + Le))
    KDP = -Le * A * (perp2 - 2 * par ** 2 / (1 + Le)) / ((1 + Le) * s ** 5)       # (km/s/kpc)^2
    Gff2 = -KDP * x * (2 + x) / KPCKMS_TO_S ** 2
    Gam2, _, _ = gamma_maps(bg)
    sel = np.isfinite(bg["dp"]) & ~excl_mask(g, kind) & (r >= 4 * re) & (r <= 8 * re) & (Gff2 > 0) & (Gam2 > 0)
    # band cells only: within 20 deg of the plane perpendicular to g_e
    sel &= np.abs(par) < np.tan(np.radians(20)) * np.sqrt(perp2)
    if not sel.any():
        return dict(n=0)
    ratio = Gam2[sel] / Gff2[sel]
    # the plane identity itself at the cells: Gamma_ff^2 (x_par = 0) = G M (2 + x)/(s^3 r^3)
    s1 = math.sqrt(1 + Le)
    return dict(n=int(sel.sum()), ratio_median=float(np.median(ratio)), ratio_range=[float(ratio.min()), float(ratio.max())],
                Gamma_ff_efold_at_re_gyr=efold_gyr(G * M * (2 + x) / (s1 ** 3 * re ** 3) / KPCKMS_TO_S ** 2))


def orbital(bg, r_star):
    """orbital time at R = 2.2 R_d in the plane (from the in-plane radial field) and the dynamical / Kepler times at r_star."""
    g = bg["g"]; gr, gt, gp = bg["grads"]
    R = 2.2 * bg["Rd"]
    i = int(np.argmin(np.abs(g.rc - R)))
    j = int(np.argmin(np.abs(g.tc - np.pi / 2)))
    gR = abs(gr[i, j, 0])
    vc = math.sqrt(g.rc[i] * gR)
    T_disc = 2 * np.pi * g.rc[i] / vc * KPCKMS_TO_S / GYR
    T_kep = 2 * np.pi * math.sqrt(r_star ** 3 / (G * bg["M"])) * KPCKMS_TO_S / GYR
    return dict(R_kpc=float(g.rc[i]), vc_kms=vc, T_orb_disc_gyr=T_disc, T_kepler_at_rstar_gyr=T_kep)


def m2_spike(bg, res, min_dp_R0):
    """MUTATE M2: a negative spike in the axis cell at r = r_e with the larger |grad Phi|, 10 (h_R0/h)^2 |min D.P(R0)|."""
    g = bg["g"]
    re = math.sqrt(G * bg["M"] * bg["a0"]) / (bg["ge"] * bg["a0"])
    i = int(np.argmin(np.abs(g.rc - re)))
    gr, gt, gp = bg["grads"]; gm = np.sqrt(gr ** 2 + gt ** 2 + gp ** 2)
    j = 0 if gm[i, 0, 0] >= gm[i, -1, 0] else g.nt - 1
    dp = bg["dp"].copy()
    dp[i, j, 0] -= 10 * (1.5 ** res) ** 2 * abs(min_dp_R0)
    return dp, (i, j)


# ------------------------------------------------------------------ backgrounds of each set
def set_list():
    L = []
    for foot in ("canonical", "alt"):
        if SET == "AX":
            for lm in S.LOGM:
                for kind in ("expo", "kuzmin"):
                    RR = (0, 1, 2, 3, 4, 5, 6) if A4 else (0, 1, 2, 3, 4, 5) if A1 else (0, 1, 2, 3)
                    L.append(dict(group="primary", foot=foot, kind=kind, logm=lm, ge=0.0, axis="z", res=RR))
                    for ge in (0.01, 0.1):
                        L.append(dict(group="AX", foot=foot, kind=kind, logm=lm, ge=ge, axis="z", res=RR))
        elif SET == "PL":
            rr = (0, 1, 2) if os.environ.get("SCS3_PL_R2") == "1" else (0, 1)
            rr = tuple(int(x) for x in os.environ["SCS3_PL_RES"].split(",")) if os.environ.get("SCS3_PL_RES") else rr
            for lm in ("9.4", "10.9"):
                for kind in ("expo", "kuzmin"):
                    for ge in (0.01, 0.1):
                        L.append(dict(group="PL", foot=foot, kind=kind, logm=lm, ge=ge, axis="x", res=rr))
        elif SET == "DOMAIN":
            L.append(dict(group="DOMAIN", foot=foot, kind="expo", logm="10.45", ge=0.1, axis="z", res=(1,)))
        elif SET == "DOMAIN01":       # reported addition: at 0.01 a0 the edge is 10 r_e (at 0.1 a0 it is 1e3 R_d ~ 31 r_e)
            L.append(dict(group="DOMAIN01", foot=foot, kind="expo", logm="10.45", ge=0.01, axis="z", res=(1,)))
        elif SET == "THICK_AX":
            for lm in S.LOGM:
                for ge in (0.01, 0.1):
                    L.append(dict(group="THICK_AX", foot=foot, kind="thick", logm=lm, ge=ge, axis="z",
                                  res=(0, 1, 2, 3, 4, 5, 6) if A4 else (0, 1, 2, 3, 4, 5) if A1 else (0, 1, 2, 3)))
        elif SET == "THICK_PL":
            for lm in ("9.4", "10.9"):
                for ge in (0.01, 0.1):
                    L.append(dict(group="THICK_PL", foot=foot, kind="thick", logm=lm, ge=ge, axis="x", res=(0, 1)))
    return L


def tag_of(d, res):
    t = "_".join(str(d[k]) for k in ("group", "foot", "kind", "logm", "ge", "axis")).replace(".", "p")
    return f"{t}_R{res}" + (f"_rmax{RMAX_FAC:g}" if RMAX_FAC != 10 else "")


PART = os.environ.get("SCS3_PART", "")
OUTNAME = os.path.join(HERE, f"scs3_maps_{SET}" + ("_A4" if A4 else "_A2" if A2 else "_A1" if A1 else "") + ("_mmd" if ITER else "") + (f"_rmax{RMAX_FAC:g}" if RMAX_FAC != 10 else "")
                       + (f"_p{PART.split('/')[0]}" if PART else "") + ".json")
PARTIAL = OUTNAME.replace(".json", "_partial.json")
RES = {"lane": "SCS3", "script": "scs3_maps.py", "criteria": "eff0ae1861", "amendment_A1": "f51866c8d4" if A1 else None, "amendment_A2": "63ed365df0" if A2 else None, "amendment_A4": "b34295ebcd" if A4 else None, "iterative": ITER, "set": SET, "rmax_fac": RMAX_FAC, "rows": {}}
if os.path.exists(PARTIAL):
    RES = json.load(open(PARTIAL))


def dump(path):
    RES["peak_rss_GB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9, 3)   # macOS: bytes
    RES["footer"] = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    os.replace(tmp, path)


def on_term(sig, frm):
    dump(PARTIAL); print("SIGTERM: partial written", flush=True); sys.exit(0)


signal.signal(signal.SIGTERM, on_term)

if __name__ == "__main__":
    t0 = time.time()
    todo = set_list()
    if PART:
        k, n = map(int, PART.split("/")); todo = todo[k::n]
    for d in todo:
        for res in d["res"]:
            tg = tag_of(d, res)
            if tg in RES["rows"]:
                continue
            t1 = time.time()
            cpath = os.path.join(CACHE, tg + ("_mmd" if ITER else "") + ".npz")
            if os.path.exists(cpath):
                bg = S.load_cache(cpath); bg.update(kind=d["kind"], foot=d["foot"], logm=d["logm"])
                bg["residual"] = None; bg["iterations"] = None
            else:
                bg = S.background(d["foot"], d["kind"], d["logm"], ge=d["ge"], axis=d["axis"], res=res)
                S.save_cache(bg, cpath)
            g = bg["g"]
            r_edge = a1_mask(bg, d) if A1 else None
            smap = S.summarize_map(bg)
            row = dict(spec={k: v for k, v in d.items() if k != "res"}, res=res, grid=list(g.shape), n_cells=g.n,
                       Rd_kpc=bg["Rd"], residual=bg["residual"], iterations=bg["iterations"], map=smap, a1_mask_edge_kpc=r_edge)
            # SCS2's KA4 / resolution comparison radius: the map over the whole domain is SCS2's maps.json quantity;
            # scs2_resolution.py used crop = min of the two grids' r_max, which is the same r_max here.
            if d["ge"] > 0:
                re = math.sqrt(G * bg["M"] * bg["a0"]) / (d["ge"] * bg["a0"]); row["r_e_kpc"] = re
                row["routeL"] = route_L(bg, d["kind"])
                neg_sel = np.isfinite(bg["dp"]) & ~excl_mask(g, d["kind"])
                scale = np.nanmax(np.abs(np.where(neg_sel, bg["dp"], np.nan)))
                negm = neg_sel & (bg["dp"] < -1e-6 * scale)
                row["region_negative"] = where_of(g, negm, bg["Rd"], re)
                row["farfield"] = farfield_compare(bg, d["kind"])
                row["orbital"] = orbital(bg, row["routeL"]["L"]["r_kpc"])
                # MUTATE M1: G -> -D.P
                m1 = route_L(bg, d["kind"], dp=-bg["dp"])
                row["M1"] = dict(Gamma2_max_s2=m1["L"]["Gamma2_max_s2"], r_over_re=m1["L"]["r_over_re"],
                                 theta_deg=m1["L"]["theta_deg"], dp_there_original=float(-m1["L"]["dp_there"]))
                # MUTATE M2 (AX only): spike scaled with resolution
                if d["axis"] == "z" and d["group"] == "AX":
                    t0r = tag_of(d, 0)
                    mdp0 = smap["min_dp_offplane"] if res == 0 else RES["rows"][t0r]["map"]["min_dp_offplane"]
                    dpm, ij = m2_spike(bg, res, mdp0)
                    m2 = route_L(bg, d["kind"], dp=dpm)
                    row["M2"] = dict(Gamma2_max_s2=m2["L"]["Gamma2_max_s2"], r_over_re=m2["L"]["r_over_re"],
                                     theta_deg=m2["L"]["theta_deg"], spike_cell=list(map(int, ij)))
            else:
                row["routeL"] = route_L(bg, d["kind"])
                ok = np.isfinite(bg["dp"])
                row["all_unmasked_positive"] = bool(np.all(bg["dp"][ok] > 0))
                row["min_dp_all_unmasked"] = float(np.min(bg["dp"][ok]))
                m1 = route_L(bg, d["kind"], dp=-bg["dp"])
                row["M1"] = dict(Gamma2_max_s2=m1["L"]["Gamma2_max_s2"])
            row["sheet"] = sheet_stats(bg, d["kind"])
            row["seconds"] = round(time.time() - t1, 1)
            RES["rows"][tg] = row
            dump(PARTIAL)
            rl = row["routeL"]["L"]
            print(f"[{tg}] grid {g.shape} res {row['residual']}; neg cells {smap['n_negative_offplane']}; "
                  f"Q-/Q+ {smap['frac_neg_over_pos']}; min D.P {smap['min_dp_offplane']:.4e}; Gamma_L e-fold {rl['efold_gyr']} Gyr "
                  f"at r/r_e {rl['r_over_re']} th {rl['theta_deg']:.1f}; sheet {row['sheet'] and row['sheet']['Sigma_ph_min']}; "
                  f"{row['seconds']}s", flush=True)
    RES["seconds_total"] = round(time.time() - t0, 1)
    dump(OUTNAME)
    if os.path.exists(PARTIAL):
        os.remove(PARTIAL)
    print("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")

# kappa = 1/2 FITTED; not theory closed. Adopts nothing.

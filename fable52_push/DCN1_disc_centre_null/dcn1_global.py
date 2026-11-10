"""DCN1 B1 (FROZEN_CRITERIA.md d603f1703c, section 2): global backgrounds on SCS3's grids with the copied SCS2 solver.

Modes (DCN1_MODE):
  KA1   thick 9.4 / 0.1 a0 axial, as frozen, at DCN1_RES (default 4): route L and min D.P under SCS3's A1 mask, compared
        with SCS3's stored scs3_maps_THICK_AX_A4.json rows (1e-6).  Also reports where the maximum sits (axis cells?).
  BC    variant C (thick mass inside r_min = rho_0 (4/3) pi r_min^3) at R4 for P1's 16 axial backgrounds; caches Phi for the
        local boundary data; reports the null on the axis.  Also the 8 isolated thick backgrounds (P2) at R4, variant C.
  KA2   SCS2's isolated thick / primary / bulge at R1 as frozen (20-shell mask): min D.P against SCS2's scs2_maps.json (1e-6).
  P2G   every SCS2 isolated family at R0-R3, both treatments, mask removed (shell 0 only): min D.P, negative cells, route L.
Caches (npz) go to $DCN1_CACHE (the scratchpad).  Preemptible: partial json after every background; SIGTERM writes and exits.
TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, math, time, resource, signal
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scs2_aqual as S

G = S.G
KPCKMS_TO_S = 3.0857e16
GYR = 3.15576e16
MYR = GYR / 1e3
AX_BASE = [(48, 24), (72, 36), (108, 54), (162, 81), (243, 121), (364, 182), (546, 273)]   # SCS3 R0-R6
CACHE = os.environ.get("DCN1_CACHE", os.path.join(HERE, "_cache"))
os.makedirs(CACHE, exist_ok=True)
MODE = os.environ.get("DCN1_MODE", "KA1")
RMIN_FAC = float(os.environ.get("DCN1_RMIN_FAC", "1e-4"))
VARIANT = {"C": False}


def make_grid_res(kind, M, Rd, a0, ge, axis, res):          # copied from SCS3's scs3_maps.py (RMAX_FAC 10)
    re = (math.sqrt(G * M * a0) / (ge * a0)) if ge > 0 else 0.0
    r_max = max(1e3 * Rd, 10 * re)
    r_min = RMIN_FAC * Rd                                     # 1e-4 as SCS2/SCS3; A3's check uses 1e-6
    scale = math.log(r_max / r_min) / math.log(r_max / (0.02 * Rd))
    nr, nt = AX_BASE[res]
    nr = int(round(nr * scale))
    if ge > 0 and axis == "z":
        return S.Grid(r_min, r_max, nr, 2 * nt, 1, "full")
    return S.Grid(r_min, r_max, nr, nt, 1, "half")


S.make_grid = make_grid_res
_deposit_frozen = S.deposit


def deposit_variant(g, kind, M, Rd):
    Mc, Min = _deposit_frozen(g, kind, M, Rd)
    if VARIANT["C"] and kind == "thick":
        hz = S.h_z_bershady(Rd); rho0 = M / (4 * np.pi * Rd ** 2 * hz)
        Min = rho0 * 4.0 / 3.0 * np.pi * g.rf[0] ** 3
    return Mc, Min


S.deposit = deposit_variant


def a1_edge(spec, M, Rd, a0):
    g0 = make_grid_res(spec["kind"], M, Rd, a0, spec["ge"], spec["axis"], 0)
    return g0.rf[20]


def gamma_map(bg, dp):
    gr, gt, gp = bg["grads"]; gm = np.sqrt(gr ** 2 + gt ** 2 + gp ** 2)
    u = gm / bg["a0"]
    return -4 * np.pi * G * dp * u * (2 + u) / KPCKMS_TO_S ** 2, u


def sheet_mask(g, kind):
    m = np.zeros(g.shape, bool)
    if kind in ("expo", "kuzmin", "expo+bulge"):
        if g.tmode == "half":
            m[:, -1, :] = True
        else:
            m[:, g.nt // 2 - 1, :] = True; m[:, g.nt // 2, :] = True
    return m


def routeL(bg, dp, kind):
    g = bg["g"]
    Gam2, u = gamma_map(bg, dp)
    ok = np.isfinite(dp) & ~sheet_mask(g, kind)
    A = np.where(ok, Gam2, -np.inf)
    k = int(np.argmax(A)); i, j, l = np.unravel_index(k, g.shape)
    G2 = float(A[i, j, l])
    th = float(g.tc[j])
    axis_cell = bool(j == 0 or j == g.nt - 1)
    return dict(Gamma2_max_s2=G2, efold_myr=(1 / math.sqrt(G2) / MYR) if G2 > 0 else None, r_kpc=float(g.rc[i]),
                r_over_Rd=float(g.rc[i] / bg["Rd"]), theta_deg=math.degrees(th), on_axis_cell=axis_cell,
                theta_cells_from_axis=int(min(j, g.nt - 1 - j)), u_there=float(u[i, j, l]), dp_there=float(dp[i, j, l]))


def axis_null(bg):
    """the null on the axis below the disc (theta = pi side for g_e along +z with the disc's pull opposing it), from the
    cell gradient on the axis cells: the cell with min |grad Phi| between 1e-3 and 0.3 R_d, on either axis."""
    g = bg["g"]; gr, gt, gp = bg["grads"]; gm = np.sqrt(gr ** 2 + gt ** 2 + gp ** 2)
    sel = (g.rc > 1e-3 * bg["Rd"]) & (g.rc < 0.3 * bg["Rd"])
    best = None
    for j in (0, g.nt - 1):
        ii = np.where(sel)[0]
        k = ii[int(np.argmin(gm[ii, j, 0]))]
        cand = (float(gm[k, j, 0]), int(k), int(j))
        if best is None or cand[0] < best[0]:
            best = cand
    gmin, i, j = best
    z = float(g.rc[i] * math.cos(g.tc[j]))
    return dict(z_null_kpc=z, z_null_over_Rd=z / bg["Rd"], u_min=gmin / bg["a0"], shell=i, theta_cell=j)


def load_or_solve(spec, res, variant):
    tag = (f"{spec['foot']}_{spec['kind']}_{spec['logm']}_{spec['ge']}_{spec['axis']}_R{res}_{variant}").replace(".", "p") + (f"_rmin{RMIN_FAC:g}" if RMIN_FAC != 1e-4 else "")
    cpath = os.path.join(CACHE, tag + ".npz")
    VARIANT["C"] = (variant == "C")
    if os.path.exists(cpath):
        bg = S.load_cache(cpath); bg.update(kind=spec["kind"], foot=spec["foot"], logm=spec["logm"])
        bg["residual"] = None; bg["iterations"] = None
    else:
        bg = S.background(spec["foot"], spec["kind"], spec["logm"], ge=spec["ge"], axis=spec["axis"], res=res)
        S.save_cache(bg, cpath)
    # the unmasked D.P (shell 0 only masked): recompute from the solution
    dp_all, _ = phantom_unmasked(bg)
    bg["dp_unmasked"] = dp_all
    return bg, tag, cpath


def phantom_unmasked(bg):
    g = bg["g"]
    F = S.faces(g)
    gr, gt, gp = bg["grads"]
    mu = S.face_mu(g, F, bg["Phi"], bg["Phib"], bg["a0"], False, gr, gt, gp)
    coef = {k_: 1 - v for k_, v in mu.items()}
    A, cout, kout = S.operator(g, F, coef)
    rhs = np.zeros(g.n); np.add.at(rhs, kout, -cout * bg["Phib"].ravel())
    flux = (A @ bg["Phi"].ravel() - rhs).reshape(g.shape)
    dp = flux / (4 * np.pi * G * g.V)
    dp[0] = np.nan                                  # shell 0: its inner face carries the enclosed-mass flux
    return dp, None


def specs():
    L = []
    if MODE == "KA1":
        for foot in ("canonical", "alt"):
            L.append((dict(foot=foot, kind="thick", logm="9.4", ge=0.1, axis="z"), int(os.environ.get("DCN1_RES", "4")), "frozen"))
    elif MODE == "BC":
        for foot in ("canonical", "alt"):
            for lm in S.LOGM:
                for ge in (0.1, 0.01):
                    L.append((dict(foot=foot, kind="thick", logm=lm, ge=ge, axis="z"), 4, "C"))
                L.append((dict(foot=foot, kind="thick", logm=lm, ge=0.0, axis="z"), 4, "C"))
    elif MODE == "KA2":
        for foot in ("canonical", "alt"):
            for lm in S.LOGM:
                for kind in ("thick", "expo", "kuzmin", "expo+bulge"):
                    L.append((dict(foot=foot, kind=kind, logm=lm, ge=0.0, axis="z"), 1, "frozen"))
    elif MODE == "P2R":                     # amendment A3 item 5 (reported): r_min = 1e-6 R_d
        for foot in ("canonical", "alt"):
            for lm in ("9.4", "10.9"):
                for kind in ("thick", "expo", "kuzmin"):
                    for res in (1, 2, 3):
                        for var in (("frozen", "C") if kind == "thick" else ("frozen",)):
                            L.append((dict(foot=foot, kind=kind, logm=lm, ge=0.0, axis="z"), res, var))
    elif MODE == "P2G":
        for foot in ("canonical", "alt"):
            for lm in S.LOGM:
                for kind in ("thick", "expo", "kuzmin", "expo+bulge"):
                    for res in (0, 1, 2, 3):
                        for var in (("frozen", "C") if kind == "thick" else ("frozen",)):
                            L.append((dict(foot=foot, kind=kind, logm=lm, ge=0.0, axis="z"), res, var))
    return L


OUTNAME = os.path.join(HERE, f"dcn1_global_{MODE}" + (f"_R{os.environ['DCN1_RES']}" if MODE == "KA1" and os.environ.get("DCN1_RES") else "") + ".json")
PARTIAL = OUTNAME.replace(".json", "_partial.json")
RES = {"lane": "DCN1", "script": "dcn1_global.py", "criteria": "d603f1703c", "mode": MODE, "rows": {}}
if os.path.exists(PARTIAL):
    RES = json.load(open(PARTIAL))


def dump(path):
    RES["peak_rss_GB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9, 3)
    RES["footer"] = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
    tmp = path + ".tmp"
    json.dump(RES, open(tmp, "w"), indent=1, default=str); os.replace(tmp, path)


def on_term(sig, frm):
    dump(PARTIAL); print("SIGTERM: partial written", flush=True); sys.exit(0)


signal.signal(signal.SIGTERM, on_term)

if __name__ == "__main__":
    t0 = time.time()
    ref3 = json.load(open(os.path.join(HERE, "..", "SCS3_external_field_stability", "scs3_maps_THICK_AX_A4.json")))["rows"]
    ref2 = json.load(open(os.path.join(HERE, "..", "SCS2_static_clock_stability_discs", "scs2_maps.json")))["maps"]
    for spec, res, var in specs():
        key = (f"{spec['foot']}_{spec['kind']}_{spec['logm']}_{spec['ge']}_R{res}_{var}").replace(".", "p")
        if key in RES["rows"]:
            continue
        t1 = time.time()
        bg, tag, cpath = load_or_solve(spec, res, var)
        g = bg["g"]; M = bg["M"]; Rd = bg["Rd"]
        row = dict(spec=spec, res=res, variant=var, grid=list(g.shape), residual=bg["residual"], iterations=bg["iterations"],
                   cache=os.path.basename(cpath), Rd_kpc=Rd, Min_Msun=float(bg["Min"]) if "Min" in bg else None)
        if spec["kind"] == "thick":
            hz = S.h_z_bershady(Rd); rho0 = M / (4 * np.pi * Rd ** 2 * hz)
            row["rho0_Msun_kpc3"] = rho0; row["hz_kpc"] = hz
            row["freefall_efold_myr"] = 1 / math.sqrt(4 * np.pi * G * rho0 / KPCKMS_TO_S ** 2) / MYR
            row["bubble_kpc"] = bg["a0"] / (4 * np.pi * G * rho0)
        if MODE == "KA1":
            dpA = bg["dp"].copy(); dpA[g.rc < a1_edge(spec, M, Rd, bg["a0"])] = np.nan       # SCS3's A1 mask
            row["routeL_A1mask"] = routeL(bg, dpA, spec["kind"])
            row["min_dp_A1mask"] = float(np.nanmin(dpA))
            t3 = f"THICK_AX_{spec['foot']}_thick_9p4_0p1_z_R{res}"
            if t3 in ref3:
                r3 = ref3[t3]
                row["SCS3_Gamma2"] = r3["routeL"]["L"]["Gamma2_max_s2"]; row["SCS3_min_dp"] = r3["map"]["min_dp_offplane"]
                row["rel_Gamma2"] = abs(row["routeL_A1mask"]["Gamma2_max_s2"] / row["SCS3_Gamma2"] - 1)
                row["rel_min_dp"] = abs(row["min_dp_A1mask"] / row["SCS3_min_dp"] - 1)
                row["KA1_pass"] = bool(row["rel_Gamma2"] <= 1e-6 and row["rel_min_dp"] <= 1e-6)
            row["null"] = axis_null(bg)
        elif MODE == "KA2":
            smap = S.summarize_map(bg)
            k2 = f"{'primary' if spec['kind'] in ('expo','kuzmin') else 'bracket_thick' if spec['kind']=='thick' else 'bracket_bulge'}_{spec['foot']}_{spec['kind']}_{spec['logm']}___".replace(".", "p")
            row["min_dp_offplane"] = smap["min_dp_offplane"]; row["n_negative_offplane"] = smap["n_negative_offplane"]
            ok = np.isfinite(bg["dp"]); row["all_masked_in_positive"] = bool(np.all(bg["dp"][ok] > 0))
            if k2 in ref2:
                row["SCS2_min_dp"] = ref2[k2]["map"]["min_dp_offplane"]
                row["rel_min_dp"] = abs(row["min_dp_offplane"] / row["SCS2_min_dp"] - 1)
                row["KA2_pass"] = bool(row["rel_min_dp"] <= 1e-6 and row["all_masked_in_positive"])
            else:
                row["KA2_pass"] = bool(row["all_masked_in_positive"]); row["SCS2_min_dp"] = None
        elif MODE in ("BC", "P2G", "P2R"):
            dpu = bg["dp_unmasked"]
            off = np.isfinite(dpu) & ~sheet_mask(g, spec["kind"])
            row["routeL_unmasked"] = routeL(bg, dpu, spec["kind"])
            row["min_dp_unmasked_offplane"] = float(np.nanmin(np.where(off, dpu, np.nan)))
            row["n_negative_unmasked_offplane"] = int(np.sum(off & (dpu < 0)))
            inner = off & (g.rc[:, None, None] < g.rf[20])
            row["n_negative_in_old_mask"] = int(np.sum(inner & (dpu < 0)))
            row["min_dp_in_old_mask"] = float(np.nanmin(np.where(inner, dpu, np.nan))) if inner.any() else None
            negc = off & (dpu < 0)
            row["negative_r_over_Rd"] = [float(g.rc[np.where(negc)[0]].min() / Rd), float(g.rc[np.where(negc)[0]].max() / Rd)] if negc.any() else None
            row["negative_shells"] = sorted(set(int(x) for x in np.where(negc)[0]))[:10] if negc.any() else []
            row["r_min_over_Rd"] = float(g.rf[0] / Rd)
            if spec["ge"] > 0:
                row["null"] = axis_null(bg)
                dpA = bg["dp"].copy(); dpA[g.rc < a1_edge(spec, M, Rd, bg["a0"])] = np.nan
                row["routeL_A1mask"] = routeL(bg, dpA, spec["kind"])
            # D.P and u along the inner shells (the centre's scaling), off-plane, theta nearest 45 deg
            j45 = int(np.argmin(np.abs(g.tc - np.pi / 4)))
            gr, gt, gp = bg["grads"]; um = np.sqrt(gr ** 2 + gt ** 2 + gp ** 2)[:, j45, 0] / bg["a0"]
            row["profile_45deg"] = dict(r_over_Rd=[float(v) for v in g.rc[1:25] / Rd], dp=[float(v) for v in dpu[1:25, j45, 0]],
                                        u=[float(v) for v in um[1:25]])
        row["seconds"] = round(time.time() - t1, 1)
        RES["rows"][key] = row
        dump(PARTIAL)
        rl = row.get("routeL_A1mask") or row.get("routeL_unmasked") or {}
        print(f"[{key}] grid {g.shape} {row['seconds']}s; L max {rl.get('Gamma2_max_s2')} e-fold {rl.get('efold_myr')} Myr at "
              f"r/Rd {rl.get('r_over_Rd')} th {rl.get('theta_deg')} axis {rl.get('on_axis_cell')} u {rl.get('u_there')}; "
              f"KA {row.get('KA1_pass', row.get('KA2_pass'))}; minDP unmasked {row.get('min_dp_unmasked_offplane')}; "
              f"null {row.get('null')}", flush=True)
    RES["seconds_total"] = round(time.time() - t0, 1)
    dump(OUTNAME)
    if os.path.exists(PARTIAL):
        os.remove(PARTIAL)
    print("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")

# kappa = 1/2 FITTED; not theory closed. Adopts nothing.

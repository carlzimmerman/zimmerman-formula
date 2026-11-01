# DR6 (FROZEN_CRITERIA.md): the term, injected before grade_clusters. Text between the markers goes through the grader's sub(). Read only of other lanes.
_DR6 = json.load(open(DR6_PK)); _DRX = np.log(np.array(_DR6["rx"])); _DRXI = np.array(_DR6["xi"]); DR6_ROWS = []
def dr6_m2(i, pp, Mh, foot, hk):
    if DR6_VAR == "OFF": return 0.0
    z = float(NX["CL"][i]["z"]); M2, R2, _thr = zn1_m200_fs(pp["Mb"], z)
    if M2 is None: DR6_NOFS["n"] += 1; return 0.0
    M2s = M2 / MSUNE; D = float(np.interp(z, _DR6["z"], _DR6["D"])); s = float(np.interp(math.log10(M2s), _DR6["lM"], _DR6["sig"])) * D; nu = 1.686 / s; b = 1 + (nu * nu - 1) / 1.686
    rmpc = RM / MPCE; xi = np.interp(np.log(np.maximum(rmpc * (1 + z), 1e-3)), _DRX, _DRXI) * D * D; rhob = _DR6["rhom"] * (1 + z) ** 3 * MSUNE / MPCE ** 3; rta = pp["rta"]
    rho_mod = np.gradient(pp["Mb"] + Mh, RM) / (4 * np.pi * RM ** 2); rho_lin = rhob * (1 + b * xi)
    if DR6_VAR == "C1": rho = np.where(RM > rta, b * rhob * xi, 0.0)
    elif DR6_VAR == "C2": rho = np.where(RM > R2, DR6_SIGN * b * rhob * xi, 0.0)
    else: rho = np.where(RM > rta, b * rhob * xi, np.where(RM > R2, np.maximum(0.0, rho_lin - rho_mod), 0.0))
    dm = 4 * np.pi * RM ** 2 * rho; M = np.r_[0, np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(RM))]
    if foot == "canonical" and hk == "h0672":
        xs = (1.5, 2.0, 3.0, 5.0); rr = lambda r_: float(np.interp(r_, RM, rho_mod) / np.interp(r_, RM, rho_lin))
        DR6_ROWS.append(dict(i=int(i), t=int(T3M[i]), z=z, lgM200=math.log10(M2s), R200=R2 / MPCE, rta=rta / MPCE, b=b, nu=nu, Mfair=pp["Mfair"] / MSUNE, Mb=float(pp["Mb"][-1]) / MSUNE, add_in_rta=float(np.interp(rta, RM, M)) / MSUNE, ratio={str(x): rr(x * R2) for x in xs if x * R2 < rta} | {"0.9rta": rr(0.9 * rta)}))
        json.dump(DR6_ROWS, open(DR6_ROWF, "w"))
    return M
DR6_NOFS = dict(n=0)

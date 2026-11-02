"""AS2 engine: second variation of a covariant action on a locally flat, frozen background, by plane waves.
Metric in Newtonian gauge (h_tt=-2Phi, h_xx=-2Psi+hp, h_yy=-2Psi-hp, h_zz=-2Psi, h_xy=hc, h_tx=Bx, h_ty=By), complete at k != 0.
L = wb R[g] + wa R[ghat] + sum(quadratic terms) - C f(I) + matter. Everything is first-order tensors contracted at leading WKB order.
MUTATE (AS2_MUTATE=1) flips the Einstein-Hilbert sign and the carrier coupling. kappa = 1/2 FITTED; not theory closed."""
import os
import numpy as np, scipy.linalg as sl
MUT = os.environ.get("AS2_MUTATE") == "1"
ETA = np.array([-1.0, 1, 1, 1])

class Fields:
    """names, and for each the first-order pieces it contributes."""
    def __init__(self, content):
        self.content = content
        names = ["Phi", "Psi", "hp", "hc", "Bx", "By"]
        self.has_A = content in ("Ae", "Kh", "SAe", "SKh", "KhP", "AeP", "EA", "AeK")
        self.twist = content in ("Ae", "SAe", "AeP", "EA", "AeK")
        self.has_S = content in ("S", "SX", "SAe", "SKh", "BMS", "M")
        self.has_X = content == "SX"
        self.has_P = content in ("KhP", "AeP")
        self.has_tau = content in ("Kh", "SKh", "KhP")
        self.has_B = content in ("BM", "BMS")
        if self.twist:
            names += ["Ax", "Ay", "Az"]
        if self.has_tau:
            names += ["tau"]
        if self.has_S:
            names += ["pi"]
        if self.has_X:
            names += ["chi"]
        if self.has_P:
            names += ["Px", "Py", "Pz"]
        if self.has_B:
            names += ["ht_tt", "ht_tz", "ht_tx", "ht_ty", "ht_xx", "ht_yy", "ht_zz", "ht_xy", "ht_xz", "ht_yz"]
        self.names = names
        self.n = len(names)
        self.ix = {k: i for i, k in enumerate(names)}
        n = self.n
        h = np.zeros((n, 4, 4)); ht = np.zeros((n, 4, 4))
        i = self.ix
        h[i["Phi"], 0, 0] = -2
        h[i["Psi"], 1, 1] = h[i["Psi"], 2, 2] = h[i["Psi"], 3, 3] = -2
        h[i["hp"], 1, 1] = 1; h[i["hp"], 2, 2] = -1
        h[i["hc"], 1, 2] = h[i["hc"], 2, 1] = 1
        h[i["Bx"], 0, 1] = h[i["Bx"], 1, 0] = 1
        h[i["By"], 0, 2] = h[i["By"], 2, 0] = 1
        if self.has_B:
            for nm, a, b in (("tt", 0, 0), ("tz", 0, 3), ("tx", 0, 1), ("ty", 0, 2), ("xx", 1, 1), ("yy", 2, 2), ("zz", 3, 3), ("xy", 1, 2), ("xz", 1, 3), ("yz", 2, 3)):
                ht[i["ht_" + nm], a, b] = ht[i["ht_" + nm], b, a] = 1
        self.h, self.ht = h, ht

class Pieces:
    """First-order tensors at derivative vector d = (dt, dx, dy, dz). Rows are fields."""
    def __init__(self, fl, d, Q0=0.0):
        self.fl, self.d = fl, d
        n, h, ix = fl.n, fl.h, fl.ix
        self.Gam = self.gamma(h, d)
        self.Gamt = self.gamma(fl.ht, d)
        # lower aether: A_t = -1 + h_tt/2 from the unit constraint; A_i from the field; khronon A_i = -d_i tau
        Al = np.zeros((n, 4), complex)
        Al[:, 0] = h[:, 0, 0] / 2
        if fl.twist:
            Al[ix["Ax"], 1] = Al[ix["Ay"], 2] = Al[ix["Az"], 3] = 1
        if fl.has_tau:
            Al[ix["tau"], 1:] = -d[1:]
        self.Al = Al
        self.D = np.einsum("a,nb->nab", d, Al) + self.Gam[:, 0, :, :]
        self.a = self.D[:, 0, 1:]
        self.Fab = self.D - self.D.transpose(0, 2, 1)
        self.theta = np.einsum("nii->n", self.D[:, 1:, 1:])
        self.Fti = self.Fab[:, 0, 1:]
        self.Fij = np.stack([self.Fab[:, 1, 2], self.Fab[:, 2, 3], self.Fab[:, 3, 1]], 1)
        Vv = np.zeros((n, 3), complex); dQ = np.zeros(n, complex); dt = np.zeros(n, complex); Xt = np.zeros(n, complex)
        if fl.has_S:
            Vv[ix["pi"], :] = d[1:]
            dt[ix["pi"]] = d[0]
        self.gradpi = Vv.copy()
        self.dtpi = dt.copy()
        self.V = Vv + Q0 * Al[:, 1:]
        self.dQ = dt + Q0 * h[:, 0, 0] / 2
        self.dQtau = np.zeros(n, complex)
        if fl.has_tau:
            self.dQtau[ix["tau"]] = d[0]
            self.dQtau = self.dQtau + h[:, 0, 0] / 2
        self.Pv = np.zeros((n, 3), complex)
        if fl.has_P:
            self.Pv[ix["Px"], 0] = self.Pv[ix["Py"], 1] = self.Pv[ix["Pz"], 2] = 1
        self.gradchi = np.zeros((n, 3), complex)
        if fl.has_X:
            self.gradchi[ix["chi"], :] = d[1:]
        if fl.has_B:
            self.C = self.Gam - self.Gamt  # (n, c, a, b)

    @staticmethod
    def gamma(h, d):
        # Gamma^c_ab = eta^cc/2 (d_a h_bc + d_b h_ac - d_c h_ab)
        t1 = np.einsum("a,nbc->nabc", d, h)
        G = 0.5 * (t1 + np.einsum("nabc->nbac", t1) - np.einsum("nabc->nbca", t1))  # index order n,a,b,c(lower)
        return np.einsum("c,nabc->ncab", ETA, G)

    def dG(self, h):
        # delta G_ab of h, from delta R_ab = (d_c d_a h^c_b + d_c d_b h^c_a - box h_ab - d_a d_b h)/2
        d = self.d
        du = ETA * d
        box = np.sum(du * d)
        hup = np.einsum("c,ncb->ncb", ETA, h)              # h^c_b
        tr = np.einsum("nii->n", hup)
        dd = np.einsum("a,b->ab", d, d)
        dch = np.einsum("c,ncb->nb", d, hup)               # d_c h^c_b
        R = 0.5 * (np.einsum("a,nb->nab", d, dch) + np.einsum("b,na->nab", d, dch) - box * h - np.einsum("n,ab->nab", tr, dd))
        Rs = np.einsum("c,ncc->n", ETA, R)
        return R - 0.5 * np.einsum("n,ab->nab", Rs, np.diag(ETA))

def bil3(A, B):
    return np.einsum("im,jm->ij", A, B)

def YB_form(C1, C2):
    # I = -Y/2, Y = eta^mn (C^g_ml C^l_ng - C^g_mn C^l_lg), symmetrised
    t1 = np.einsum("igml,jlmg,m->ij", C1, C2, ETA)
    t2 = np.einsum("igmm,jllg,m->ij", C1, C2, ETA) if False else np.einsum("igmn,mn,jllg->ij", C1, np.diag(ETA), C2)
    t2s = np.einsum("igmn,mn,jllg->ij", C2, np.diag(ETA), C1).T
    return -0.5 * (t1 - 0.5 * (t2 + t2s))

class Theory:
    """terms: dict of quadratic coefficients. carrier: name of I. C_F, C_FF: -C f'(I0), f''(I0) values set per background."""
    def __init__(self, content, Q0=0.0, terms=None, carrier=None, wb=1.0, wa=0.0, L=0.0, stiff=None, muK2=0.0, matter="min", phibar=0.1):
        self.fl = Fields(content); self.Q0 = Q0; self.terms = terms or {}; self.carrier = carrier
        self.wb, self.wa, self.L, self.stiff, self.muK2, self.matter = wb, wa, L, stiff, muK2, matter
        self.phibar = phibar

    def pieces(self, d):
        return Pieces(self.fl, np.asarray(d, complex), self.Q0)

    def carrier_form(self, P, Pr):
        c = self.carrier
        if c == "Y":
            return bil3(P.V, Pr.V)
        if c == "X":
            return bil3(P.gradpi, Pr.gradpi) - np.outer(P.dtpi, Pr.dtpi)
        if c == "a2":
            return bil3(P.a, Pr.a)
        if c == "Fti2":
            return bil3(P.Fti, Pr.Fti)
        if c == "KJS":
            return np.einsum("iab,a,b,jab->ij", P.D, ETA, ETA, Pr.D)
        if c == "P2":
            return bil3(P.Pv, Pr.Pv)
        if c == "chi2":
            return bil3(P.gradchi, Pr.gradchi)
        if c == "YB":
            return YB_form(P.C, Pr.C)
        raise ValueError(c)

    def quad(self, Pm, Pp):
        """Quadratic matrix from everything except the carrier: L2 = 1/2 f^dag M f, left derivative -d, right d."""
        fl = self.fl; T = self.terms
        sgn = -1.0 if MUT else 1.0
        M = sgn * self.wb * -np.einsum("iab,a,b,jab->ij", fl.h + 0j, ETA, ETA, Pp.dG(fl.h))
        if fl.has_B:
            M = M + self.wa * -np.einsum("iab,a,b,jab->ij", fl.ht + 0j, ETA, ETA, Pp.dG(fl.ht))
        def add(c, A, B):
            nonlocal M
            M = M + 2 * c * A
        # F^2 = -2 Fti^2 + 2 Fij^2 , L = -(KB/2) F^2
        if T.get("KB"):
            M = M + 2 * (T["KB"] / 2) * (2 * bil3(Pm.Fti, Pp.Fti) - 2 * bil3(Pm.Fij, Pp.Fij))
        if T.get("tw"):
            M = M - 2 * T["tw"] * bil3(Pm.Fij, Pp.Fij)
        if T.get("aV"):
            M = M + T["aV"] * (bil3(Pm.a, Pp.V) + bil3(Pm.V, Pp.a))
        if T.get("aP"):
            M = M + T["aP"] * (bil3(Pm.a, Pp.Pv) + bil3(Pm.Pv, Pp.a))
        if T.get("Y"):
            M = M - 2 * T["Y"] * bil3(Pm.V, Pp.V)
        if T.get("Ypi"):
            M = M - 2 * T["Ypi"] * bil3(Pm.gradpi, Pp.gradpi)
        if T.get("P2"):
            M = M - 2 * T["P2"] * bil3(Pm.Pv, Pp.Pv)
        if T.get("a2"):
            M = M + 2 * T["a2"] * bil3(Pm.a, Pp.a)
        if T.get("gradcross"):   # QUMOND parent: 2 grad pi . grad chi  (pi auxiliary-Newton field)
            M = M + T["gradcross"] * (bil3(Pm.gradpi, Pp.gradchi) + bil3(Pm.gradchi, Pp.gradpi))
        if T.get("Phipi"):       # 2 grad Phi . grad pi style, used by SX and BMS twin
            i = fl.ix["Phi"]; g = np.zeros_like(Pp.gradpi); g[i, :] = Pp.d[1:]; gm = np.zeros_like(Pm.gradpi); gm[i, :] = Pm.d[1:]
            M = M + T["Phipi"] * (bil3(gm, Pp.gradchi) + bil3(Pm.gradchi, g))
        if T.get("ea"):
            c1, c2, c3, c4 = T["ea"]
            M = M - 2 * (c1 * np.einsum("iab,a,b,jab->ij", Pm.D, ETA, ETA, Pp.D) + c2 * np.outer(Pm.theta, Pp.theta)
                         + c3 * np.einsum("iab,a,b,jba->ij", Pm.D, ETA, ETA, Pp.D) - c4 * bil3(Pm.a, Pp.a))
        if self.muK2:
            dq = Pp.dQtau if fl.has_tau and not fl.has_S else Pp.dQ
            dqm = Pm.dQtau if fl.has_tau and not fl.has_S else Pm.dQ
            M = M + 2 * 2 * self.muK2 * np.outer(dqm, dq)
        if self.stiff and self.L:
            s = self.stiff; L2 = self.L ** 2
            def lap(P):
                d = P.d[1:]
                if s == "DP":
                    return P.Pv @ d
                if s == "DV":
                    return P.V @ d
                if s == "Da":
                    return P.a @ d
                if s == "boxpi":
                    return P.gradpi @ d - P.dtpi * P.d[0]
                raise ValueError(s)
            M = M - 2 * L2 * np.outer(lap(Pm), lap(Pp))
        return M

    def M(self, omega, kz=1.0, kx=0.0, F=0.0, F2=0.0, T0=None):
        dp = np.array([-1j * omega, 1j * kx, 0, 1j * kz], complex)
        Pp, Pm = self.pieces(dp), self.pieces(-dp)
        M = self.quad(Pm, Pp)
        if self.carrier:
            sg = -1.0 if MUT else 1.0
            M = M - sg * 2 * F * self.carrier_form(Pm, Pp)
            if F2 and T0 is not None:
                dIm = 2 * self.bg_cross(Pm, T0); dIp = 2 * self.bg_cross(Pp, T0)
                M = M - sg * F2 * np.outer(dIm, dIp)
        return M

    def bg_cross(self, P, T0):
        """B(T0, T) for the carrier: T0 is a background 'Pieces' evaluated on the bg field vector."""
        c = self.carrier
        P0, f0 = T0
        def contr(A, A0):
            return A @ (f0 @ A0)
        if c == "Y":
            return contr(P.V, P0.V)
        if c == "X":
            return contr(P.gradpi, P0.gradpi)
        if c == "a2":
            return contr(P.a, P0.a)
        if c == "Fti2":
            return contr(P.Fti, P0.Fti)
        if c == "P2":
            return contr(P.Pv, P0.Pv)
        if c == "chi2":
            return contr(P.gradchi, P0.gradchi)
        if c == "KJS":
            return np.einsum("iab,a,b,ab->i", P.D, ETA, ETA, np.einsum("i,iab->ab", f0, P0.D))
        if c == "YB":
            C0 = np.einsum("i,igml->gml", f0, P0.C)[None]
            return YB_form(P.C, C0)[:, 0]
        raise ValueError(c)

# ---------- static reduction ----------
def static_fields(th):
    fl = th.fl
    out = ["Phi", "Psi"]
    if fl.twist:
        out.append("Az")
    if fl.has_S:
        out.append("pi")
    if fl.has_X:
        out.append("chi")
    if fl.has_P:
        out.append("Pz")
    if fl.has_B:
        out = ["f", "fh"] + [n for n in out if n not in ("Phi", "Psi")]
    return out

def static_reduce(th):
    """Real gradient Lagrangian L = 1/2 v^T Mq v - C f(s (c.v)^2), with matter -16 pi G rho e.f. Returns (names, A=-Mq, c, s, e, e_psi)."""
    fl = th.fl
    names = static_fields(th)
    # ht_xx stands for the isotropic spatial part of ghat
    fl2 = fl
    T = np.zeros((len(names), fl.n))  # rows: static vars
    for r, nm in enumerate(names):
        if nm == "f":             # Milgrom's branch Phi = Psi on each metric: consistent, since both the EH form and Y are q = 2 Phi Psi - Psi^2 in the two potentials
            T[r, fl.ix["Phi"]] = T[r, fl.ix["Psi"]] = 1
        elif nm == "fh":
            T[r, fl.ix["ht_tt"]] = -2
            for k in ("ht_xx", "ht_yy", "ht_zz"):
                T[r, fl.ix[k]] = -2
        else:
            T[r, fl.ix[nm]] = 1
    dre = np.array([0, 0, 0, 1.0], complex)
    Pr = th.pieces(dre)
    # EH part: use d = i, then k^2 coefficient
    di = np.array([0, 0, 0, 1j], complex)
    Pip, Pim = th.pieces(di), th.pieces(-di)
    th0 = Theory(fl.content, th.Q0, {}, None, th.wb, th.wa)
    Meh = th0.quad(Pim, Pip)
    tt = dict(th.terms)
    thq = Theory(fl.content, th.Q0, tt, None, 0.0, 0.0)
    Mq = thq.quad(Pr, Pr)            # real gradient forms, no d sign flip
    Mtot = T @ (Meh + Mq) @ T.T
    A = -np.real_if_close(Mtot); A = np.real(A)
    # carrier as a rank-one form
    if th.carrier:
        B = T @ th.carrier_form(Pr, Pr) @ T.T
        B = np.real(B)
        w, U = np.linalg.eigh(0.5 * (B + B.T))
        i = int(np.argmax(np.abs(w)))
        s = float(np.sign(w[i])) if abs(w[i]) > 1e-12 else 0.0
        c = U[:, i] * np.sqrt(abs(w[i]))
        rank = int(np.sum(np.abs(w) > 1e-9))
    else:
        s, c, rank = 0.0, np.zeros(len(names)), 0
    if c.sum() < 0:
        c = -c
    e, ep = matter_vectors(th, names, T)
    return dict(names=names, A=A, c=c, s=s, rank=rank, e=e, ep=ep)

def matter_vectors(th, names, T):
    """Matter-frame potentials as linear forms: Phi_m = e.f, Psi_m = ep.f, read from the first-order matter metric."""
    fl = th.fl
    hm = matter_h(th)
    a = -0.5 * hm[:, 0, 0]
    b = -0.5 * hm[:, 1, 1]
    return T @ a, T @ b

def matter_h(th):
    fl = th.fl; h = fl.h.copy(); ix = fl.ix
    if th.matter == "min":
        return h
    i = ix["pi"]
    if th.matter == "conf":      # e^{2 pi} g
        h[i] = h[i] + 2 * np.diag(ETA)
        return h
    if th.matter == "tev":       # e^{-2 pi}(g + AA) - e^{2 pi} AA at pi-bar = 0
        h[i] = h[i] + np.diag([-2.0, -2, -2, -2])
        return h
    if th.matter == "dsc":       # g + phi_a phi_b / M^2 ; adds no static force at Q0=0 at first order
        return h
    raise ValueError(th.matter)

# ---------- modes ----------
def modes(th, F=0.0, F2=0.0, T0=None, kz=1.0, kx=0.0, deg=None):
    pts = np.array([0.0, 1, -1, 2, -2])
    Ms = [th.M(w, kz, kx, F, F2, T0) for w in pts]
    V = np.vander(pts, 5, increasing=True)
    C = np.linalg.solve(V, np.array(Ms).reshape(5, -1)).reshape(5, *Ms[0].shape)
    scale = max(np.abs(c).max() for c in C)
    tol = 1e-9 * scale
    d = 4
    while d > 0 and np.abs(C[d]).max() < tol:
        d -= 1
    n = C[0].shape[0]
    def Mw(w):
        return sum(C[j] * w ** j for j in range(d + 1))
    def dMw(w):
        return sum(j * C[j] * w ** (j - 1) for j in range(1, d + 1))
    # singular pencil?
    sv = []
    for w in (0.613 + 0.271j, -1.37 + 0.77j, 2.11 - 0.53j):
        s = np.linalg.svd(Mw(w), compute_uv=False); sv.append(s[-1] / s[0])
    if max(sv) < 1e-11:
        return dict(degenerate=True, deg=d, roots=[], n=n)
    # companion
    A = np.zeros((d * n, d * n), complex); B = np.eye(d * n, dtype=complex)
    for j in range(d - 1):
        A[j * n:(j + 1) * n, (j + 1) * n:(j + 2) * n] = np.eye(n)
    for j in range(d):
        A[(d - 1) * n:, j * n:(j + 1) * n] = -C[j]
    B[(d - 1) * n:, (d - 1) * n:] = C[d]
    ev = sl.eig(A, B, right=False, homogeneous_eigvals=True)
    al, be = ev
    roots = []
    for a_, b_ in zip(al, be):
        if abs(b_) < 1e-10 * abs(a_) or abs(a_) / max(abs(b_), 1e-300) > 1e5:
            continue
        w = a_ / b_
        s = np.linalg.svd(Mw(w), compute_uv=False)
        roots.append(w)
    out = []
    for w in roots:
        U, s, Vh = np.linalg.svd(Mw(w))
        v = Vh[-1].conj()
        if abs(w) < 1e-4:
            out.append(dict(w=complex(w), kind="zero", E=None)); continue
        E = (v.conj() @ dMw(w) @ v) / (2 * w)
        kind = "ok" if abs(w.imag) < 1e-5 * max(abs(w), 1) else "complex"
        out.append(dict(w=complex(w), kind=kind, E=complex(E), kin=(v.conj() @ v).real))
    return dict(degenerate=False, deg=d, roots=out, n=n)

def speeds(res, k=1.0):
    """Unique positive omega^2/k^2 and the sign of the residue for physical roots."""
    rows = []
    for r in res["roots"]:
        w = r["w"]
        if r["kind"] == "zero":
            rows.append(("zero", 0.0, 0)); continue
        if r["kind"] == "complex":
            rows.append(("complex", complex(w * w), 0)); continue
        if w.real < 0:
            continue
        rows.append(("wave", (w.real ** 2) / k ** 2, float(np.sign(r["E"].real))))
    return rows

def health_label(res):
    if res["degenerate"]:
        return "ND", "degenerate determinant"
    if res["deg"] > 2:
        return "FAIL", f"higher time derivative, degree {res['deg']}"
    rows = speeds(res)
    if any(r[0] == "complex" for r in rows):
        return "FAIL", "complex omega: gradient or tachyonic instability"
    if any(r[0] == "wave" and r[2] < 0 for r in rows):
        return "FAIL", f"negative residue, c^2 {[round(r[1], 5) for r in rows if r[0] == 'wave' and r[2] < 0]}"
    if any(r[0] == "zero" for r in rows):
        return "ND", f"{sum(r[0] == 'zero' for r in rows)} zero-speed roots"
    return "PASS", f"c^2 {sorted(set(round(r[1], 6) for r in rows))}"

# ---------- moving source ----------
def source_vector(th, vx=0.0, vz=0.0, w_norm=4.0):
    hm = matter_h(th)
    T = np.zeros((4, 4)); T[0, 0] = 1
    T[0, 1] = T[1, 0] = vx; T[0, 3] = T[3, 0] = vz
    T[1, 1] = vx ** 2; T[3, 3] = vz ** 2; T[1, 3] = T[3, 1] = vx * vz
    # L_m = (16 pi G)/2 h_ab T^ab ; with k=1, U=1: 16 pi G rho = 4
    return 0.5 * w_norm * np.einsum("nab,ab->n", hm, T)

def esolve(M, S):
    d = np.sqrt(np.maximum(np.abs(np.diag(M)), 1e-30))
    d = np.where(np.abs(np.diag(M)) < 1e-20, np.maximum(np.abs(M).max(1), 1.0) ** 0.5, d)
    Mq = M / np.outer(d, d)
    try:
        x = np.linalg.solve(Mq, S / d)
    except np.linalg.LinAlgError:
        x = np.linalg.lstsq(Mq, S / d, rcond=1e-14)[0]
    return x / d

def alpha1(th, F=0.0, v=1.0):
    """g_0x in the vector sector with velocity along x, k along z, omega = 0. GR: h_tx = -4 U v."""
    fl = th.fl
    names = [n for n in ("Bx", "Ax", "Px", "ht_tx", "ht_xz") if n in fl.ix]
    idx = [fl.ix[n] for n in names]
    M = th.M(0.0, 1.0, 0.0, F)[np.ix_(idx, idx)]
    S = source_vector(th, vx=v)[idx]
    f = esolve(M, -S)
    b = f[0].real
    U = abs(phi_beta(th, F)[1])       # physical U: the rest-frame Newtonian potential, so G_N is whatever this theory gives
    return -2 * b / (v * U) - 8, b / (v * U)

def phi_beta(th, F=0.0, vs=(0.004, 0.008, 0.012, 0.016, 0.02)):
    """Scalar sector, source moving along k: Phi = -U(1 + beta v^2) in Newtonian gauge. Returns beta and Psi ratio at rest."""
    fl = th.fl
    names = [n for n in ("Phi", "Psi", "Az", "tau", "pi", "chi", "Pz", "ht_tt", "ht_tz", "ht_zz", "ht_xx", "ht_yy") if n in fl.ix]
    idx = [fl.ix[n] for n in names]
    out = []
    for v in vs:
        M = th.M(v, 1.0, 0.0, F)[np.ix_(idx, idx)]
        S = source_vector(th, vz=v)[idx]
        f = esolve(M, -S)
        out.append(f[0].real)
    vs = np.array(vs)
    co = np.polyfit(vs ** 2, np.array(out), 2)
    return co[1] / co[2], co[2]

def alpha2(th, F=0.0):
    """Readout calibrated in KA3 on Einstein-aether: beta = -2 - alpha1/2 + alpha2."""
    a1 = alpha1(th, F)[0]
    b, U = phi_beta(th, F)
    return b + 2 + a1 / 2, a1, U

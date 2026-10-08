/*
 * cfg489_core.c -- the 1-D spherical Lagrangian hydro integrator of lane CFG489 (NC1: GR + Lambda chassis, MOND only in
 * the cold fluid). Compiled at run time by cfg489_nc1.py into a temporary directory and called through ctypes.
 *
 * Units: G = M_b = a0 (true footing) = 1, so r_M = 1 and V_f = 1.
 *
 * Nodes i = 0..N sit at the shell interfaces r_i; node 0 is a fixed reflecting wall at r_w. Shell j = 1..N lies between
 * nodes j-1 and j and carries mass dm_j, specific internal energy e_j and a settling stress ps_j. Node masses
 * mb_i = (dm_i + dm_{i+1})/2 (mb_N = dm_N/2, mb_0 = dm_1/2). The fluid mass that node i feels is the node-consistent
 *     Menc_i = mb_0 + sum_{1<=k<i} mb_k + mb_i/2,
 * so that the gravity force is exactly -dW/dr_i with
 *     W = sum_i mb_i Phi_host(r_i) - G sum_i mb_i (Menc_i)/r_i   (i >= 1; the wall node is fixed).
 * The host (static baryons) enters through tables of M_host(<r),
 * rho_host(r) and Phi_host(r) on a uniform ln r grid.
 *
 * Forces on node i: F_i = -4 pi r_i^2 (Ptot_{i+1} - Ptot_i), Ptot = P + q + ps (Ptot_{N+1} = 0). The fluid's 4-acceleration
 * (Newtonian limit) is the non-gravitational acceleration A_i = F_i / mb_i (+ the M3 force), which is exactly
 * Dv/Dt + grad Phi.
 *
 * Target (A-kin): M_t,i = r_i^2 sgn(A_i) F(|A_i|) / G, F(g) = g - g_N(g) with the kernel inverted (a0_eff in F);
 * at the wall M_t,0 = 0 (wall_mode 0, the frozen text) or r_w^2 F(g_wall) (wall_mode 1: the wall's own 4-acceleration is
 * the host gravity there). rho_t,j = (M_t,j - M_t,j-1)/V_j.
 *
 * Members: mode 0 = M1 (tau Dps/Dt = -(ps - peq), peq = s (P/rho)(rho - rho_t), tau = 1/sqrt(4 pi G rho_m));
 *          mode 1 = M2 (tau -> 0); mode 2 = M3 (F-H force f = s(G (Menc + M_t,0)/r^2 - sgn(A)F(|A|)), A implicit
 *          pointwise). s = 0 switches the settling off (pure hydro).
 * The dependence of peq on ps through A is linearised and solved implicitly (tridiagonal) each step.
 * ec = 1: the settling stress's work is drawn from e (energy-conserving form); ec = 0: from an external reservoir.
 *
 * Time stepping: staggered leapfrog (v at half steps), e updated with the time-centred thermal pressure (implicit in
 * e^{n+1}), shock viscosity q = rho (C2 dv^2 + C1 c_s |dv|) for compression.
 */
#include <math.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int N;              /* shells */
    int mode;           /* 0 M1, 1 M2, 2 M3 */
    int ec;             /* energy-conserving form */
    int kernel;         /* 0 nu_mono table, 1 P2 */
    double s;           /* settling sign/strength */
    double a0eff;       /* a0 inside the target's F (true a0 = 1) */
    double gamma, C2, C1, cfl;
    double rw;          /* wall radius */
    double t_end;
    double t_samp0, dt_samp;
    int n_samp;
    long max_steps;
    double e_floor;
    /* host table */
    int nh; double lnr0, dlnr;
    /* kernel table (nu_mono) */
    int nz; double lnz0, dlnz;
    int wall_mode;      /* 0: M_t at the wall = 0 (frozen text); 1: M_t,0 = r_w^2 F(g_wall) (the wall's own A) */
    int point_host;     /* 1: point-mass host (M = 1 + Mcore, rho = 0, Phi = -(1 + Mcore)/r), no table lookups */
    double Mcore;       /* inert core inside the wall (the law's target phantom there); already in the host tables */
} Params;

typedef struct {
    long steps;
    int crashed;        /* 0 ok, 1 inversion, 2 nan, 3 dt too small, 4 max steps */
    double t_final;
    long n_floor;       /* e floor hits */
    int n_samp_done;
} Stats;

static const double PI4 = 4.0 * M_PI;

static double interp_tab(const double *tab, int n, double x0, double dx, double x) {
    double u = (x - x0) / dx;
    if (u <= 0.0) return tab[0];
    if (u >= n - 1) return tab[n - 1];
    int k = (int)u;
    double w = u - k;
    return tab[k] * (1.0 - w) + tab[k + 1] * w;
}

/* host: M(<r), rho(r), Phi(r); beyond the table use point-mass forms with the last M */
static void host_eval(const Params *p, const double *HM, const double *HR, const double *HP, double r,
                      double *M, double *rho, double *Phi) {
    double lr = log(r);
    double umax = p->lnr0 + p->dlnr * (p->nh - 1);
    if (lr >= umax) {
        double Ml = HM[p->nh - 1];
        *M = Ml; *rho = 0.0; *Phi = -Ml / r; return;
    }
    if (lr <= p->lnr0) {
        *M = HM[0]; *rho = HR[0]; *Phi = HP[0]; return;
    }
    *M = interp_tab(HM, p->nh, p->lnr0, p->dlnr, lr);
    *rho = interp_tab(HR, p->nh, p->lnr0, p->dlnr, lr);
    *Phi = interp_tab(HP, p->nh, p->lnr0, p->dlnr, lr);
}

/* F(g) = g - g_N(g) and F'(g) for g >= 0, with a0 = a0eff */
static void Ffun(const Params *p, const double *LY, const double *DY, double g, double *F, double *Fp) {
    double a0 = p->a0eff;
    if (g <= 0.0) { *F = 0.0; *Fp = 1.0; return; }
    double z = g / a0;
    if (p->kernel == 1) {                 /* P2: g = sqrt(gN^2 + a0 gN) */
        double sq = sqrt(1.0 + 4.0 * z * z);
        double y = 0.5 * (-1.0 + sq);
        *F = a0 * (z - y);
        *Fp = 1.0 - 2.0 * z / sq;
        return;
    }
    double lz = log(z);
    double zmin = p->lnz0, zmax = p->lnz0 + p->dlnz * (p->nz - 1);
    if (lz <= zmin) {                     /* deep: y = z^2 */
        *F = a0 * (z - z * z);
        *Fp = 1.0 - 2.0 * z;
        return;
    }
    if (lz >= zmax) {                     /* Newtonian: y = z - c, dy/dz = 1 */
        double ylast = exp(LY[p->nz - 1]);
        double zlast = exp(zmax);
        *F = a0 * (zlast - ylast);
        *Fp = 1.0 - DY[p->nz - 1];
        return;
    }
    double y = exp(interp_tab(LY, p->nz, p->lnz0, p->dlnz, lz));
    double dy = interp_tab(DY, p->nz, p->lnz0, p->dlnz, lz);
    *F = a0 * (z - y);
    *Fp = 1.0 - dy;
}

/* Thomas algorithm: a sub, b diag, c super, d rhs (overwritten), n */
static int thomas(int n, double *a, double *b, double *c, double *d, double *x) {
    for (int i = 1; i < n; i++) {
        if (b[i - 1] == 0.0) return 1;
        double w = a[i] / b[i - 1];
        b[i] -= w * c[i - 1];
        d[i] -= w * d[i - 1];
    }
    if (b[n - 1] == 0.0) return 1;
    x[n - 1] = d[n - 1] / b[n - 1];
    for (int i = n - 2; i >= 0; i--) x[i] = (d[i] - c[i] * x[i + 1]) / b[i];
    return 0;
}

int run_nc1(const Params *p, const double *HM, const double *HR, const double *HP, const double *LY, const double *DY,
            const double *dm, double *r, double *v, double *e, double *ps,
            double *samp_r, double *samp_e, double *samp_v, double *samp_E, Stats *st) {
    int N = p->N;
    double g = p->gamma;
    /* work arrays, index 0..N (nodes) or 1..N (shells; index 0 unused) */
    double *mb = calloc(N + 1, sizeof(double)), *Menc = calloc(N + 1, sizeof(double));
    double *V = calloc(N + 1, sizeof(double)), *rho = calloc(N + 1, sizeof(double)), *P = calloc(N + 2, sizeof(double));
    double *q = calloc(N + 2, sizeof(double)), *rt = calloc(N + 1, sizeof(double)), *A = calloc(N + 1, sizeof(double));
    double *Mt = calloc(N + 1, sizeof(double)), *dMt = calloc(N + 1, sizeof(double)), *cc = calloc(N + 1, sizeof(double));
    double *acc = calloc(N + 1, sizeof(double)), *Vnew = calloc(N + 1, sizeof(double)), *fM3 = calloc(N + 1, sizeof(double));
    double *ta = calloc(N + 2, sizeof(double)), *tb = calloc(N + 2, sizeof(double)), *tc = calloc(N + 2, sizeof(double));
    double *td = calloc(N + 2, sizeof(double)), *tx = calloc(N + 2, sizeof(double)), *peq = calloc(N + 1, sizeof(double));
    double *taus = calloc(N + 1, sizeof(double));
    double *Mh = calloc(N + 1, sizeof(double)), *Rh = calloc(N + 1, sizeof(double)), *Ph = calloc(N + 1, sizeof(double));

    for (int i = 1; i <= N; i++) mb[i] = (i < N) ? 0.5 * (dm[i] + dm[i + 1]) : 0.5 * dm[N];
    mb[0] = 0.5 * dm[1];
    {
        double cum = mb[0];
        for (int i = 1; i <= N; i++) { Menc[i] = cum + 0.5 * mb[i]; cum += mb[i]; }
    }
    double t = 0.0, dt_old = 0.0;
    double Wres = 0.0, Sps = 0.0, Sq = 0.0;
    int ks = 0;
    st->crashed = 0; st->n_floor = 0; st->steps = 0;
    double Mw, rhow, Phw;
    host_eval(p, HM, HR, HP, p->rw, &Mw, &rhow, &Phw);
    double gwall = Mw / (p->rw * p->rw);   /* no fluid inside the wall: gravity there is the host's */
    double Fw, Fpw;
    Ffun(p, LY, DY, gwall, &Fw, &Fpw);
    double Mt0 = (p->wall_mode == 1) ? p->rw * p->rw * Fw : 0.0;
    int first = 1;

    for (long step = 0; ; step++) {
        /* --- geometry, density, pressure */
        for (int j = 1; j <= N; j++) {
            V[j] = (PI4 / 3.0) * (r[j] * r[j] * r[j] - r[j - 1] * r[j - 1] * r[j - 1]);
            if (!(r[j] > r[j - 1]) || !(V[j] > 0.0)) { st->crashed = 1; goto done; }
            rho[j] = dm[j] / V[j];
            if (e[j] < p->e_floor) { e[j] = p->e_floor; st->n_floor++; }
            P[j] = (g - 1.0) * rho[j] * e[j];
            if (!isfinite(P[j]) || !isfinite(r[j]) || !isfinite(v[j]) || !isfinite(ps[j])) { st->crashed = 2; goto done; }
        }
        P[N + 1] = 0.0; q[N + 1] = 0.0;
        for (int j = 1; j <= N; j++) {
            double dv = v[j] - v[j - 1];
            double cs = sqrt(g * P[j] / rho[j]);
            q[j] = (dv < 0.0) ? rho[j] * (p->C2 * dv * dv + p->C1 * cs * (-dv)) : 0.0;
        }
        if (p->point_host) {
            for (int i = 1; i <= N; i++) { Mh[i] = 1.0 + p->Mcore; Rh[i] = 0.0; Ph[i] = -(1.0 + p->Mcore) / r[i]; }
            Rh[0] = 0.0;
        } else {
            for (int i = 1; i <= N; i++) host_eval(p, HM, HR, HP, r[i], &Mh[i], &Rh[i], &Ph[i]);
            Rh[0] = rhow;
        }
        for (int j = 1; j <= N; j++) {
            /* local matter density at the shell: cold fluid + host baryons (mean of the shell's two nodes) */
            taus[j] = 1.0 / sqrt(PI4 * (rho[j] + 0.5 * (Rh[j] + Rh[j - 1])));
        }
        for (int i = 1; i <= N; i++) cc[i] = PI4 * r[i] * r[i] / mb[i];

        /* --- time step */
        double dt = 1e30;
        for (int j = 1; j <= N; j++) {
            double s2 = P[j] / rho[j];
            double ce2 = g * s2;
            if (p->mode == 0 || p->mode == 1) ce2 += fabs(p->s) * s2 * (1.0 + fabs(rt[j]) / rho[j]);
            double dv = v[j] - v[j - 1];
            double sig = sqrt(ce2) + ((dv < 0.0) ? 4.0 * p->C2 * (-dv) : 0.0);
            double dr = r[j] - r[j - 1];
            double dtj = dr / (sig + 1e-300);
            if (dtj < dt) dt = dtj;
        }
        dt *= p->cfl;
        for (int i = 1; i <= N; i++) {
            double Mtot = Mh[i] + Menc[i];
            double tff = sqrt(r[i] * r[i] * r[i] / Mtot);
            if (0.1 * tff < dt) dt = 0.1 * tff;
            if (fabs(v[i]) > 0 && 0.02 * r[i] / fabs(v[i]) < dt) dt = 0.02 * r[i] / fabs(v[i]);
        }
        if (dt < 1e-9) { st->crashed = 3; goto done; }
        if (first) { dt_old = dt; first = 0; }
        double dtk = 0.5 * (dt_old + dt);    /* kick interval for v at half steps */

        /* --- settling stress update (M1/M2): implicit in ps through A-kin */
        if ((p->mode == 0 || p->mode == 1) && p->s != 0.0) {
            for (int i = 1; i <= N; i++) {
                double Ptot_i = P[i] + q[i] + ps[i];
                double Ptot_ip = (i < N) ? (P[i + 1] + q[i + 1] + ps[i + 1]) : 0.0;
                A[i] = -cc[i] * (Ptot_ip - Ptot_i);
                double F, Fp;
                Ffun(p, LY, DY, fabs(A[i]), &F, &Fp);
                Mt[i] = r[i] * r[i] * ((A[i] >= 0.0) ? F : -F);
                dMt[i] = r[i] * r[i] * Fp;          /* dM_t/dA */
            }
            Mt[0] = Mt0; dMt[0] = 0.0;
            for (int j = 1; j <= N; j++) {
                rt[j] = (Mt[j] - Mt[j - 1]) / V[j];
                double s2 = P[j] / rho[j];
                peq[j] = p->s * s2 * (rho[j] - rt[j]);
            }
            for (int j = 1; j <= N; j++) {
                double Ej = (p->mode == 1) ? 0.0 : exp(-dt / taus[j]);
                double s2 = P[j] / rho[j];
                double k = -p->s * s2 / V[j];        /* J_jk = k * d rho_t,j... with sign: J = -s s2 d rho_t/d ps */
                /* d rho_t,j / d ps_{j+1} = -dMt_j cc_j / V_j ; d/d ps_j = (dMt_j cc_j + dMt_{j-1} cc_{j-1}) / V_j ;
                   d/d ps_{j-1} = -dMt_{j-1} cc_{j-1} / V_j  (cc_0 unused since dMt_0 = 0) */
                double cjm1 = (j >= 2) ? dMt[j - 1] * cc[j - 1] : 0.0;
                double cj = dMt[j] * cc[j];
                double Jjm = k * (-cjm1);
                double Jjj = k * (cj + cjm1);
                double Jjp = (j < N) ? k * (-cj) : 0.0;
                double w = 1.0 - Ej;
                tb[j - 1] = 1.0 - w * Jjj;
                ta[j - 1] = -w * Jjm;
                tc[j - 1] = -w * Jjp;
                double Jps = Jjj * ps[j] + ((j >= 2) ? Jjm * ps[j - 1] : 0.0) + ((j < N) ? Jjp * ps[j + 1] : 0.0);
                td[j - 1] = Ej * ps[j] + w * (peq[j] - Jps);
            }
            ta[0] = 0.0; tc[N - 1] = 0.0;
            if (thomas(N, ta, tb, tc, td, tx)) { st->crashed = 2; goto done; }
            for (int j = 1; j <= N; j++) ps[j] = tx[j - 1];
        } else if (p->s == 0.0) {
            for (int j = 1; j <= N; j++) ps[j] = 0.0;
        }

        /* --- accelerations */
        for (int i = 1; i <= N; i++) {
            double Ptot_i = P[i] + q[i] + ps[i];
            double Ptot_ip = (i < N) ? (P[i + 1] + q[i + 1] + ps[i + 1]) : 0.0;
            double AP = -cc[i] * (Ptot_ip - Ptot_i);
            double gg = (Mh[i] + Menc[i]) / (r[i] * r[i]);
            fM3[i] = 0.0;
            if (p->mode == 2 && p->s != 0.0) {
                /* solve A + s sgn(A) F(|A|) = AP + s Menc/r^2 for A (monotone) */
                double R = AP + p->s * (Menc[i] + Mt0) / (r[i] * r[i]);
                double x = R / (1.0 + p->s);
                for (int it = 0; it < 60; it++) {
                    double F, Fp;
                    Ffun(p, LY, DY, fabs(x), &F, &Fp);
                    double h = x + p->s * ((x >= 0.0) ? F : -F) - R;
                    double hp = 1.0 + p->s * Fp;
                    double dx = h / hp;
                    x -= dx;
                    if (fabs(dx) <= 1e-14 * (fabs(x) + 1e-300)) break;
                }
                fM3[i] = x - AP;
                A[i] = x;
            } else {
                A[i] = AP;
            }
            acc[i] = A[i] - gg;
        }

        /* --- sampling (state at integer time t) */
        while (ks < p->n_samp && t >= p->t_samp0 + ks * p->dt_samp) {
            double K = 0.0, U = 0.0, W = 0.0;
            for (int i = 1; i <= N; i++) {
                double vh = v[i] + 0.5 * dt_old * acc[i];   /* integer-time velocity estimate */
                K += 0.5 * mb[i] * vh * vh;
                W += mb[i] * Ph[i] - mb[i] * Menc[i] / r[i];
            }
            for (int j = 1; j <= N; j++) U += dm[j] * e[j];
            for (int i = 0; i <= N; i++) { samp_r[(long)ks * (N + 1) + i] = r[i]; samp_v[(long)ks * (N + 1) + i] = v[i]; }
            for (int j = 1; j <= N; j++) samp_e[(long)ks * (N + 1) + j] = e[j];
            samp_e[(long)ks * (N + 1)] = 0.0;
            double *E8 = samp_E + (long)ks * 8;
            E8[0] = t; E8[1] = K; E8[2] = U; E8[3] = W; E8[4] = Wres; E8[5] = Sps; E8[6] = Sq; E8[7] = (double)st->n_floor;
            ks++;
        }
        if (t >= p->t_end) break;
        if (step >= p->max_steps) { st->crashed = 4; goto done; }

        /* --- kick (v at half step), drift */
        for (int i = 1; i <= N; i++) v[i] += dtk * acc[i];
        v[0] = 0.0;
        double rold0 = r[0];
        for (int i = 1; i <= N; i++) r[i] += dt * v[i];
        r[0] = rold0;

        /* --- energy: time-centred thermal pressure (implicit in e^{n+1}); q and ps at time n */
        for (int j = 1; j <= N; j++) {
            Vnew[j] = (PI4 / 3.0) * (r[j] * r[j] * r[j] - r[j - 1] * r[j - 1] * r[j - 1]);
            if (!(Vnew[j] > 0.0)) { st->crashed = 1; goto done; }
            double dV = Vnew[j] - V[j];
            double Pext = q[j] + (p->ec ? ps[j] : 0.0);
            double enew = (e[j] - (0.5 * P[j] + Pext) * dV / dm[j]) / (1.0 + 0.5 * (g - 1.0) * dV / Vnew[j]);
            double Tm = (g - 1.0) * 0.5 * (e[j] + enew);
            if (Tm > 0.0) {
                Sq += (-q[j] * dV) / Tm;
                if (p->ec) Sps += (-ps[j] * dV) / Tm;
            }
            e[j] = enew;
            if (p->mode == 0 || p->mode == 1) Wres += ps[j] * dV;
        }
        if (p->mode == 2) for (int i = 1; i <= N; i++) Wres += mb[i] * fM3[i] * v[i] * dt;
        t += dt;
        dt_old = dt;
        st->steps = step + 1;
    }
done:
    st->t_final = t;
    st->n_samp_done = ks;
    free(mb); free(Menc); free(V); free(rho); free(P); free(q); free(rt); free(A); free(Mt); free(dMt); free(cc);
    free(acc); free(Vnew); free(fM3); free(ta); free(tb); free(tc); free(td); free(tx); free(peq); free(taus);
    free(Mh); free(Rh); free(Ph);
    return st->crashed;
}

/* the target routine alone (control K4): M_t(r) = r^2 sgn(A) F(|A|) for given r, A arrays */
void target_mass(const Params *p, const double *LY, const double *DY, int n, const double *rr, const double *AA,
                 double *Mt) {
    for (int i = 0; i < n; i++) {
        double F, Fp;
        Ffun(p, LY, DY, fabs(AA[i]), &F, &Fp);
        Mt[i] = rr[i] * rr[i] * ((AA[i] >= 0.0) ? F : -F);
    }
}

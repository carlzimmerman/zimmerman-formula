/* FS1 scheme S core (CRITERIA.md, f716e2f98f): AC10's planar label system with conservative Lagrangian pressure
 * p = K/(2 J^2), Christensen-limited shock viscosity on pressure cells, SSP-RK3, interior + all-cell J_thr events.
 * Compiled by fs1.py (cc -O2 -shared). kappa = 1/2 FITTED; not theory closed. */
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef struct {
    int N, i0, i1, press;
    double dq, M1, s2, sheet, cq, cl, pg, s2q, Mtot;
    double *mnode, *K, *minv;
    int *order;
    double *left, *J, *dv, *P, *psi, *Qv, *sig;
} Ctx;

static void sort_order(Ctx *c, const double *x) {
    int n = c->N + 1, *o = c->order;
    for (int i = 1; i < n; i++) {           /* insertion sort from previous order (nearly sorted); stable by index */
        int a = o[i], j = i - 1;
        while (j >= 0 && (x[o[j]] > x[a] || (x[o[j]] == x[a] && o[j] > a))) { o[j + 1] = o[j]; j--; }
        o[j + 1] = a;
    }
}

/* acceleration; returns max signal speed sigma (0 if no pressure) */
static double acc(Ctx *c, const double *x, const double *v, double *a) {
    int N = c->N, n = N + 1;
    sort_order(c, x);
    double cs = 0.0;
    for (int k = 0; k < n; k++) { int i = c->order[k]; double m = c->mnode[i]; cs += m; c->left[i] = cs - m / 2; }
    double xmin = x[c->order[0]], xmax = x[c->order[n - 1]];
    double half = (c->Mtot - c->s2 * (xmax - xmin)) / 2;
    for (int i = 0; i < n; i++)
        a[i] = c->M1 * (c->left[i] - c->s2 * (x[i] - xmin) - half) - 0.5 * c->sheet * erf(x[i] / c->s2q);
    double smax = 0.0;
    if (!c->press) return 0.0;
    for (int i = 0; i < N; i++) { c->J[i] = (x[i + 1] - x[i]) / c->dq; c->dv[i] = v[i + 1] - v[i]; }
    for (int i = 0; i < N; i++) {
        double Ki = c->K[i], Ji = c->J[i], dvi = c->dv[i];
        c->P[i] = 0.0; c->Qv[i] = 0.0; c->psi[i] = 1.0; c->sig[i] = 0.0;
        if (!(Ji > 0 && Ki > 0)) continue;
        double p = Ki / (2 * Ji * Ji), C = sqrt(Ki / (Ji * Ji * Ji));
        double dvl = (i > 0) ? c->dv[i - 1] : dvi, dvr = (i < N - 1) ? c->dv[i + 1] : dvi;
        double rl = (dvi != 0) ? dvl / dvi : 1.0, rr = (dvi != 0) ? dvr / dvi : 1.0;
        double ps = 0.5 * (rl + rr); if (2 * rl < ps) ps = 2 * rl; if (2 * rr < ps) ps = 2 * rr;
        if (ps < 0) ps = 0; if (ps > 1) ps = 1;
        double Q = 0.0;
        if (dvi < 0) Q = (1 - ps) * (c->cq * dvi * dvi / Ji + c->cl * C * fabs(dvi));
        c->P[i] = p + Q; c->Qv[i] = Q; c->psi[i] = ps;
        double s = C + 2 * c->cq * (1 - ps) * ((dvi < 0) ? -dvi : 0.0) / Ji;
        c->sig[i] = s; if (s > smax) smax = s;
    }
    for (int i = 0; i < n; i++) {
        double Pl = (i == 0) ? c->pg : c->P[i - 1], Pr = (i == N) ? c->pg : c->P[i];
        a[i] -= (Pr - Pl) * c->minv[i];
    }
    return smax;
}

static double herm(double s, double J0, double d0, double J1, double d1, double dt) {
    double s2 = s * s, s3 = s2 * s;
    return (2 * s3 - 3 * s2 + 1) * J0 + (s3 - 2 * s2 + s) * dt * d0 + (-2 * s3 + 3 * s2) * J1 + (s3 - s2) * dt * d1;
}

/* first s in (0,1] with herm(s) <= thr; -1 if none (64-interval scan + 60 bisections) */
static double hroot(double J0, double d0, double J1, double d1, double dt, double thr) {
    double sp = 0.0, fp = J0 - thr;
    if (fp <= 0) return 0.0;
    for (int k = 1; k <= 64; k++) {
        double s = k / 64.0, f = herm(s, J0, d0, J1, d1, dt) - thr;
        if (f <= 0) {
            double lo = sp, hi = s;
            for (int it = 0; it < 60; it++) { double m = 0.5 * (lo + hi); if (herm(m, J0, d0, J1, d1, dt) - thr <= 0) hi = m; else lo = m; }
            return hi;
        }
        sp = s; fp = f;
    }
    return -1.0;
}

/* out[0] t_fold (-1 none), [1] t_fold_all (-1), [2] J_min interior, [3] v_max, [4] nstep, [5] status
 * (0 ok, 1 fold, -2 nonfinite, -3 maxsteps, -4 walltime), [6] fold cell, [7] shock flag at fold (Q>0 within 3 cells),
 * [8] all-cell event cell, [9] t_end, [10] J_min all cells
 * rec: if rec_cap>0, per step-end record of (t, x[rc], x[rc+1], v[rc], v[rc+1]) for node rc; rec_n returned in out[11] */
int fs1_run(int N, double M1, double Pi0, double s2, double gam, double sheet, double cq, double cl, double cfl,
            double fsheet, double tmax, double jthr, int edge_b, double WB, double X0a, double X0b, double EDGE,
            long maxsteps, double walltime, double *out, int rc, int rec_cap, double *rec) {
    Ctx c; memset(&c, 0, sizeof c);
    int n = N + 1;
    c.N = N; c.M1 = M1; c.s2 = s2; c.sheet = sheet; c.cq = cq; c.cl = cl;
    c.dq = (X0b - X0a) / N;
    c.i0 = (int)(EDGE * N); c.i1 = (int)((1 - EDGE) * N);
    double *q = malloc(sizeof(double) * n);
    double stp = (X0b - X0a) / N;
    for (int i = 0; i < n; i++) q[i] = (double)i * stp + X0a;                  /* numpy linspace */
    q[N] = X0b;
    c.dq = q[1] - q[0];
    c.mnode = calloc(n, sizeof(double)); c.K = calloc(N, sizeof(double)); c.minv = malloc(sizeof(double) * n);
    c.order = malloc(sizeof(int) * n); c.left = malloc(sizeof(double) * n);
    c.J = malloc(sizeof(double) * N); c.dv = malloc(sizeof(double) * N); c.P = malloc(sizeof(double) * N);
    c.psi = malloc(sizeof(double) * N); c.Qv = malloc(sizeof(double) * N); c.sig = malloc(sizeof(double) * N);
    double span = q[N] - q[0], e = EDGE * span; double Kmax = 0;
    for (int i = 0; i < N; i++) {
        double qc = 0.5 * (q[i + 1] + q[i]);
        double T = 0.5 * (tanh((qc - q[0] - 0.5 * e) / (0.1 * e)) - tanh((qc - q[N] + 0.5 * e) / (0.1 * e)));
        double Pic = s2 + (Pi0 - s2) * T;
        c.mnode[i] += Pic * c.dq / 2; c.mnode[i + 1] += Pic * c.dq / 2;
        c.K[i] = gam * (Pic > 0 ? Pic : 0.0);
        if (edge_b && (i < c.i0 || i >= c.i1)) c.K[i] = 0.0;
        if (c.K[i] > Kmax) Kmax = c.K[i];
    }
    c.Mtot = 0; for (int i = 0; i < n; i++) c.Mtot += c.mnode[i];
    for (int i = 0; i < n; i++) c.minv[i] = 1.0 / c.dq;
    c.minv[0] = c.minv[N] = 2.0 / c.dq;
    c.pg = gam * (s2 > 0 ? s2 : 0.0) / 2;
    c.press = (gam > 0 && Kmax > 0);
    c.s2q = sqrt(2.0) * WB;
    for (int i = 0; i < n; i++) c.order[i] = i;

    double *x = malloc(sizeof(double) * n), *v = malloc(sizeof(double) * n), *a = malloc(sizeof(double) * n);
    double *x1 = malloc(sizeof(double) * n), *v1 = malloc(sizeof(double) * n), *a1 = malloc(sizeof(double) * n);
    double *x2 = malloc(sizeof(double) * n), *v2 = malloc(sizeof(double) * n);
    double *xn = malloc(sizeof(double) * n), *vn = malloc(sizeof(double) * n);
    for (int i = 0; i < n; i++) { x[i] = q[i]; v[i] = 1.0; }
    double t = 0.0, tf = -1, tfa = -1, jmin = 1.0, vmax = 1.0; long ns = 0; double jmina = 1.0; int status = 0, icell = -1, acell = -1, sflag = 0;
    int nrec = 0;
    clock_t c0 = clock();
    double smax = acc(&c, x, v, a);
    if (rec_cap > 0) { rec[0] = 0; rec[1] = x[rc]; rec[2] = x[rc + 1]; rec[3] = v[rc]; rec[4] = v[rc + 1]; nrec = 1; }
    while (t < tmax) {
        double vm = 0; for (int i = 0; i < n; i++) { double av = fabs(v[i]); if (av > vm) vm = av; }
        if (vm > vmax) vmax = vm;
        double dt = fsheet * WB / vm;
        if (smax > 0 && cfl * c.dq / smax < dt) dt = cfl * c.dq / smax;
        if (tmax - t < dt) dt = tmax - t;
        for (int i = 0; i < n; i++) { x1[i] = x[i] + dt * v[i]; v1[i] = v[i] + dt * a[i]; }
        acc(&c, x1, v1, a1);
        for (int i = 0; i < n; i++) { x2[i] = 0.75 * x[i] + 0.25 * (x1[i] + dt * v1[i]); v2[i] = 0.75 * v[i] + 0.25 * (v1[i] + dt * a1[i]); }
        acc(&c, x2, v2, a1);
        for (int i = 0; i < n; i++) { xn[i] = x[i] / 3 + 2.0 / 3 * (x2[i] + dt * v2[i]); vn[i] = v[i] / 3 + 2.0 / 3 * (v2[i] + dt * a1[i]); }
        int bad = 0;
        for (int i = 0; i < n; i++) if (!isfinite(xn[i]) || !isfinite(vn[i])) { bad = 1; break; }
        if (bad) { status = -2; break; }
        /* events: per cell cubic Hermite in time */
        double best = 2.0, besta = 2.0; int bcell = -1, bacell = -1;
        for (int i = 0; i < N; i++) {
            double J0 = (x[i + 1] - x[i]) / c.dq, J1 = (xn[i + 1] - xn[i]) / c.dq;
            double d0 = (v[i + 1] - v[i]) / c.dq, d1 = (vn[i + 1] - vn[i]) / c.dq;
            int interior = (i >= c.i0 && i < c.i1);
            if (J0 <= jthr) continue;            /* already below at step start (edge cell after its fold) */
            double lo = (J0 < J1 ? J0 : J1) - dt * (fabs(d0) > fabs(d1) ? fabs(d0) : fabs(d1));
            if (lo > jthr) continue;
            double s = hroot(J0, d0, J1, d1, dt, jthr);
            if (s < 0) continue;
            if (interior && s < best) { best = s; bcell = i; }
            if (s < besta) { besta = s; bacell = i; }
        }
        if (tfa < 0 && bacell >= 0) { tfa = t + besta * dt; acell = bacell; }
        if (bcell >= 0) {
            tf = t + best * dt; icell = bcell; jmin = jthr; status = 1; ns++;
            acc(&c, xn, vn, a);                      /* shock flag at the fold state */
            if (c.press) for (int k = icell - 3; k <= icell + 3; k++) if (k >= 0 && k < N && c.Qv[k] > 0) sflag = 1;
            t = tf;
            break;
        }
        for (int i = c.i0; i < c.i1; i++) { double Jn = (xn[i + 1] - xn[i]) / c.dq; if (Jn < jmin) jmin = Jn; }
        for (int i = 0; i < N; i++) { double Jn = (xn[i + 1] - xn[i]) / c.dq; if (Jn < jmina) jmina = Jn; }
        memcpy(x, xn, sizeof(double) * n); memcpy(v, vn, sizeof(double) * n); t += dt; ns++;
        smax = acc(&c, x, v, a);
        if (rec_cap > 0 && nrec < rec_cap) { double *r = rec + 5 * nrec; r[0] = t; r[1] = x[rc]; r[2] = x[rc + 1]; r[3] = v[rc]; r[4] = v[rc + 1]; nrec++; }
        if (ns >= maxsteps) { status = -3; break; }
        if ((ns & 1023) == 0 && (double)(clock() - c0) / CLOCKS_PER_SEC > walltime) { status = -4; break; }
    }
    if (status == 1 && rec_cap > 0 && nrec < rec_cap) { double *r = rec + 5 * nrec; r[0] = t; r[1] = xn[rc]; r[2] = xn[rc + 1]; r[3] = vn[rc]; r[4] = vn[rc + 1]; nrec++; }
    out[0] = tf; out[1] = tfa; out[2] = jmin; out[3] = vmax; out[4] = (double)ns; out[5] = status; out[6] = icell;
    out[7] = sflag; out[8] = acell; out[9] = t; out[10] = jmina; out[11] = nrec;
    free(q); free(c.mnode); free(c.K); free(c.minv); free(c.order); free(c.left); free(c.J); free(c.dv); free(c.P);
    free(c.psi); free(c.Qv); free(c.sig); free(x); free(v); free(a); free(x1); free(v1); free(a1); free(x2); free(v2); free(xn); free(vn);
    return status;
}

/* X12_caustics_3d compiled kernels (FROZEN_CRITERIA §3). Built by x12_core.py with the system C compiler into work/.
 *
 * Arrays are C-ordered (ix, iy, iz), iz fastest. dx[NX-1], dy[NY-1], dz[NZ-1] are the node spacings.
 * Variational finite differences: for a cell c, g_c^2 = 1/4 sum over its 4 x-edges (du/dx)^2 + the same for y and z;
 * E[u] = sum_c V_c F(g_c); R(u)_n = dE/du_n. With F'(g)/g = coef, each edge e of c carries the flux
 * q = V_c coef_c (du_e) / (4 d_e^2), added to its upper node and subtracted from its lower node.
 */
#include <math.h>
#include <stdlib.h>
#include <string.h>

#define IDX(i, j, k) (((size_t)(i) * NY + (size_t)(j)) * NZ + (size_t)(k))

static double coef_of(int kind, double g, double a0)
{
    double x;
    switch (kind) {
    case 0: return 1.0;                                  /* Poisson */
    case 1: x = g / a0; return x / (1.0 + x);             /* mu (AQUAL) */
    case 2: x = g / a0; return 1.0 / (1.0 + x);           /* 1 - mu (hold law) */
    case 3: x = g / a0; if (x < 1e-300) x = 1e-300;       /* nu (QUMOND-like start only) */
        return 0.5 * (1.0 + sqrt(1.0 + 4.0 / x));
    }
    return 1.0;
}

/* R = dE/du on all nodes (zeroed first). Returns max g/a0 over cells in *xmax (if a0 > 0). */
void residual(const double *u, int NX, int NY, int NZ, const double *dx, const double *dy, const double *dz,
              int kind, double a0, double *R, double *xmax)
{
    memset(R, 0, sizeof(double) * (size_t)NX * NY * NZ);
    double xm = 0.0;
    for (int i = 0; i < NX - 1; i++) {
        double ax = 1.0 / dx[i];
        for (int j = 0; j < NY - 1; j++) {
            double ay = 1.0 / dy[j];
            for (int k = 0; k < NZ - 1; k++) {
                double az = 1.0 / dz[k];
                double u000 = u[IDX(i, j, k)], u100 = u[IDX(i + 1, j, k)], u010 = u[IDX(i, j + 1, k)];
                double u110 = u[IDX(i + 1, j + 1, k)], u001 = u[IDX(i, j, k + 1)], u101 = u[IDX(i + 1, j, k + 1)];
                double u011 = u[IDX(i, j + 1, k + 1)], u111 = u[IDX(i + 1, j + 1, k + 1)];
                double ex0 = u100 - u000, ex1 = u110 - u010, ex2 = u101 - u001, ex3 = u111 - u011;
                double ey0 = u010 - u000, ey1 = u110 - u100, ey2 = u011 - u001, ey3 = u111 - u101;
                double ez0 = u001 - u000, ez1 = u101 - u100, ez2 = u011 - u010, ez3 = u111 - u110;
                double g2 = 0.25 * ((ex0 * ex0 + ex1 * ex1 + ex2 * ex2 + ex3 * ex3) * ax * ax
                                    + (ey0 * ey0 + ey1 * ey1 + ey2 * ey2 + ey3 * ey3) * ay * ay
                                    + (ez0 * ez0 + ez1 * ez1 + ez2 * ez2 + ez3 * ez3) * az * az);
                double g = sqrt(g2);
                if (a0 > 0 && g / a0 > xm) xm = g / a0;
                double V = dx[i] * dy[j] * dz[k];
                double w = 0.25 * V * coef_of(kind, g, a0);
                double wx = w * ax * ax, wy = w * ay * ay, wz = w * az * az;
                double q;
                q = wx * ex0; R[IDX(i + 1, j, k)] += q; R[IDX(i, j, k)] -= q;
                q = wx * ex1; R[IDX(i + 1, j + 1, k)] += q; R[IDX(i, j + 1, k)] -= q;
                q = wx * ex2; R[IDX(i + 1, j, k + 1)] += q; R[IDX(i, j, k + 1)] -= q;
                q = wx * ex3; R[IDX(i + 1, j + 1, k + 1)] += q; R[IDX(i, j + 1, k + 1)] -= q;
                q = wy * ey0; R[IDX(i, j + 1, k)] += q; R[IDX(i, j, k)] -= q;
                q = wy * ey1; R[IDX(i + 1, j + 1, k)] += q; R[IDX(i + 1, j, k)] -= q;
                q = wy * ey2; R[IDX(i, j + 1, k + 1)] += q; R[IDX(i, j, k + 1)] -= q;
                q = wy * ey3; R[IDX(i + 1, j + 1, k + 1)] += q; R[IDX(i + 1, j, k + 1)] -= q;
                q = wz * ez0; R[IDX(i, j, k + 1)] += q; R[IDX(i, j, k)] -= q;
                q = wz * ez1; R[IDX(i + 1, j, k + 1)] += q; R[IDX(i + 1, j, k)] -= q;
                q = wz * ez2; R[IDX(i, j + 1, k + 1)] += q; R[IDX(i, j + 1, k)] -= q;
                q = wz * ez3; R[IDX(i + 1, j + 1, k + 1)] += q; R[IDX(i + 1, j + 1, k)] -= q;
            }
        }
    }
    if (xmax) *xmax = xm;
}

/* Hessian-vector product of E_mu (AQUAL, F'(g)/g = mu = x/(1+x), F'' = mu_L = (2x+x^2)/(1+x)^2) at u, applied to v.
 * H_c v = V [mu_c sum_e a_e dv_e s + beta_c t_c sum_e a_e du_e s], a_e = 1/(4 d_e^2), t_c = sum_e a_e du_e dv_e,
 * beta_c = (mu_L - mu)/g^2. mu is floored at 1e-14 (X8). Also returns the per-node diagonal-ish coefficient
 * (volume-weighted mean of mu + (mu_L - mu)/3 over adjacent cells, numerator and weights) if dnum/dden are non-null. */
void hessvec(const double *u, const double *v, int NX, int NY, int NZ, const double *dx, const double *dy,
             const double *dz, double a0, double *out, double *dnum, double *dden)
{
    memset(out, 0, sizeof(double) * (size_t)NX * NY * NZ);
    if (dnum) memset(dnum, 0, sizeof(double) * (size_t)NX * NY * NZ);
    if (dden) memset(dden, 0, sizeof(double) * (size_t)NX * NY * NZ);
    for (int i = 0; i < NX - 1; i++) {
        double ax = 1.0 / dx[i];
        for (int j = 0; j < NY - 1; j++) {
            double ay = 1.0 / dy[j];
            for (int k = 0; k < NZ - 1; k++) {
                double az = 1.0 / dz[k];
                size_t n[8] = {IDX(i, j, k), IDX(i + 1, j, k), IDX(i, j + 1, k), IDX(i + 1, j + 1, k),
                               IDX(i, j, k + 1), IDX(i + 1, j, k + 1), IDX(i, j + 1, k + 1), IDX(i + 1, j + 1, k + 1)};
                /* edges: (lower, upper) corner numbers and direction 0/1/2 */
                static const int lo[12] = {0, 2, 4, 6, 0, 1, 4, 5, 0, 1, 2, 3};
                static const int up[12] = {1, 3, 5, 7, 2, 3, 6, 7, 4, 5, 6, 7};
                double du[12], dv[12], a[12];
                double g2 = 0.0, t = 0.0;
                for (int e = 0; e < 12; e++) {
                    double s = (e < 4) ? ax : ((e < 8) ? ay : az);
                    a[e] = 0.25 * s * s;
                    du[e] = u[n[up[e]]] - u[n[lo[e]]];
                    dv[e] = v ? (v[n[up[e]]] - v[n[lo[e]]]) : 0.0;
                    g2 += a[e] * du[e] * du[e];
                    t += a[e] * du[e] * dv[e];
                }
                double g = sqrt(g2), x = g / a0;
                double mu = x / (1.0 + x), muL = (2.0 * x + x * x) / ((1.0 + x) * (1.0 + x));
                double beta = (g > 1e-300) ? (muL - mu) / g2 : 0.0;
                double muf = mu > 1e-14 ? mu : 1e-14;
                double V = dx[i] * dy[j] * dz[k];
                if (v) {
                    for (int e = 0; e < 12; e++) {
                        double q = V * a[e] * (muf * dv[e] + beta * t * du[e]);
                        out[n[up[e]]] += q;
                        out[n[lo[e]]] -= q;
                    }
                }
                if (dnum) {
                    double cd = muf + (muL - mu) / 3.0;
                    for (int c = 0; c < 8; c++) {
                        dnum[n[c]] += V * cd;
                        dden[n[c]] += V;
                    }
                }
            }
        }
    }
}

/* Batched tridiagonal solves along z: for each of nab rows, (Ld + lam[ab] Md) w = y (in place), off-diagonal Le. */
void tridiag(double *y, long nab, int nz, const double *lam, const double *Ld, const double *Le, const double *Md)
{
    double *cp = (double *)malloc(sizeof(double) * nz);
    for (long r = 0; r < nab; r++) {
        double *yr = y + r * (long)nz;
        double l = lam[r];
        double den = Ld[0] + l * Md[0];
        cp[0] = (nz > 1) ? Le[0] / den : 0.0;
        yr[0] /= den;
        for (int k = 1; k < nz; k++) {
            den = Ld[k] + l * Md[k] - Le[k - 1] * cp[k - 1];
            if (k < nz - 1) cp[k] = Le[k] / den;
            yr[k] = (yr[k] - Le[k - 1] * yr[k - 1]) / den;
        }
        for (int k = nz - 2; k >= 0; k--) yr[k] -= cp[k] * yr[k + 1];
    }
    free(cp);
}

/* Index-space quadratic B-spline weights for one coordinate. */
static inline void b2w(double c, const double *X, int N, int mir, int *nodes, double *W, double *D, double *flip)
{
    *flip = 1.0;
    if (mir && c < 0) { c = -c; *flip = -1.0; }
    int lo = 0, hi = N - 1;
    if (c <= X[0]) lo = 0;
    else if (c >= X[N - 1]) lo = N - 2;
    else {
        while (hi - lo > 1) { int m = (lo + hi) >> 1; if (X[m] <= c) lo = m; else hi = m; }
        if (lo > N - 2) lo = N - 2;
    }
    double d = X[lo + 1] - X[lo];
    double f = (c - X[lo]) / d;
    if (f < 0) f = 0;
    if (f > 1) f = 1;
    double s = lo + f;
    int n0 = (int)floor(s + 0.5);
    double uu = s - n0;
    W[0] = 0.5 * (0.5 - uu) * (0.5 - uu);
    W[1] = 0.75 - uu * uu;
    W[2] = 0.5 * (0.5 + uu) * (0.5 + uu);
    D[0] = -(0.5 - uu) / d;
    D[1] = -2.0 * uu / d;
    D[2] = (0.5 + uu) / d;
    for (int a = 0; a < 3; a++) {
        int nn = n0 - 1 + a;
        if (nn < 0) nn = mir ? -nn : 0;
        if (nn > N - 1) nn = N - 1;
        nodes[a] = nn;
    }
}

void tsc_deposit(long np, const double *px, const double *py, const double *pz, const double *m,
                 const double *X, const double *Y, const double *Z, int NX, int NY, int NZ,
                 int mx, int my, int mz, double *out)
{
    memset(out, 0, sizeof(double) * (size_t)NX * NY * NZ);
    for (long p = 0; p < np; p++) {
        int ni[3], nj[3], nk[3];
        double Wx[3], Wy[3], Wz[3], Dx[3], Dy[3], Dz[3], fx, fy, fz;
        b2w(px[p], X, NX, mx, ni, Wx, Dx, &fx);
        b2w(py[p], Y, NY, my, nj, Wy, Dy, &fy);
        b2w(pz[p], Z, NZ, mz, nk, Wz, Dz, &fz);
        double mp = m[p];
        for (int a = 0; a < 3; a++)
            for (int b = 0; b < 3; b++) {
                double wab = mp * Wx[a] * Wy[b];
                size_t base = ((size_t)ni[a] * NY + (size_t)nj[b]) * NZ;
                for (int c = 0; c < 3; c++) out[base + nk[c]] += wab * Wz[c];
            }
    }
}

/* Gradient of sum_n f_n S_n(x_p) at the particles (energy-conserving force); mirrored components sign-flipped. */
void tsc_grad(long np, const double *px, const double *py, const double *pz, const double *X, const double *Y,
              const double *Z, int NX, int NY, int NZ, int mx, int my, int mz, const double *f,
              double *gx, double *gy, double *gz)
{
    for (long p = 0; p < np; p++) {
        int ni[3], nj[3], nk[3];
        double Wx[3], Wy[3], Wz[3], Dx[3], Dy[3], Dz[3], fx, fy, fz;
        b2w(px[p], X, NX, mx, ni, Wx, Dx, &fx);
        b2w(py[p], Y, NY, my, nj, Wy, Dy, &fy);
        b2w(pz[p], Z, NZ, mz, nk, Wz, Dz, &fz);
        double sx = 0, sy = 0, sz = 0;
        for (int a = 0; a < 3; a++)
            for (int b = 0; b < 3; b++) {
                size_t base = ((size_t)ni[a] * NY + (size_t)nj[b]) * NZ;
                double f0 = f[base + nk[0]], f1 = f[base + nk[1]], f2 = f[base + nk[2]];
                double fw = f0 * Wz[0] + f1 * Wz[1] + f2 * Wz[2];
                double fd = f0 * Dz[0] + f1 * Dz[1] + f2 * Dz[2];
                sx += Dx[a] * Wy[b] * fw;
                sy += Wx[a] * Dy[b] * fw;
                sz += Wx[a] * Wy[b] * fd;
            }
        gx[p] = fx * sx;
        gy[p] = fy * sy;
        gz[p] = fz * sz;
    }
}

/* J = det dx/dq on a block [i0,i1) x [j0,j1) x [k0,k1) of the label lattice (LX, LY, LZ), label coordinates qx, qy, qz.
 * Centred differences over +-1 labels; across a mirror (index -1 on a mirrored axis) the ghost of label 1 is used with
 * that coordinate negated; otherwise one-sided at the lattice ends. Also returns the 9 derivatives if F != NULL. */
static inline void getpos(const double *px, const double *py, const double *pz, int LX, int LY, int LZ,
                          int a, int b, int c, int mx, int my, int mz, double *r)
{
    double sx = 1, sy = 1, sz = 1;
    if (a < 0) { a = -a; sx = mx ? -1 : 1; }
    if (b < 0) { b = -b; sy = my ? -1 : 1; }
    if (c < 0) { c = -c; sz = mz ? -1 : 1; }
    size_t q = ((size_t)a * LY + (size_t)b) * LZ + (size_t)c;
    r[0] = sx * px[q];
    r[1] = sy * py[q];
    r[2] = sz * pz[q];
}

void jacobian(const double *px, const double *py, const double *pz, int LX, int LY, int LZ,
              const double *qx, const double *qy, const double *qz, int mx, int my, int mz,
              int i0, int i1, int j0, int j1, int k0, int k1, double *J, double *F)
{
    long cnt = 0;
    for (int a = i0; a < i1; a++)
        for (int b = j0; b < j1; b++)
            for (int c = k0; c < k1; c++) {
                double d[3][3];
                int idx[3] = {a, b, c};
                int L[3] = {LX, LY, LZ};
                int mir[3] = {mx, my, mz};
                const double *qq[3] = {qx, qy, qz};
                for (int dir = 0; dir < 3; dir++) {
                    int lo = idx[dir] - 1, hi = idx[dir] + 1;
                    double qlo, qhi;
                    if (lo < 0 && !mir[dir]) lo = idx[dir];
                    if (hi > L[dir] - 1) hi = idx[dir];
                    qlo = (lo < 0) ? -qq[dir][-lo] : qq[dir][lo];
                    qhi = qq[dir][hi];
                    int al[3] = {a, b, c}, ah[3] = {a, b, c};
                    al[dir] = lo;
                    ah[dir] = hi;
                    double rl[3], rh[3];
                    getpos(px, py, pz, LX, LY, LZ, al[0], al[1], al[2], mx, my, mz, rl);
                    getpos(px, py, pz, LX, LY, LZ, ah[0], ah[1], ah[2], mx, my, mz, rh);
                    double inv = 1.0 / (qhi - qlo);
                    for (int comp = 0; comp < 3; comp++) d[comp][dir] = (rh[comp] - rl[comp]) * inv;
                }
                double det = d[0][0] * (d[1][1] * d[2][2] - d[1][2] * d[2][1])
                           - d[0][1] * (d[1][0] * d[2][2] - d[1][2] * d[2][0])
                           + d[0][2] * (d[1][0] * d[2][1] - d[1][1] * d[2][0]);
                J[cnt] = det;
                if (F) for (int r = 0; r < 9; r++) F[cnt * 9 + r] = d[r / 3][r % 3];
                cnt++;
            }
}

/* max over unknown nodes of K |rho_n| ((1 + x_n)^2 - 1), x_n = |grad u|/a0 by centred differences (0 across mirrors). */
double omega2_max(const double *u, const double *rho_abs, int NX, int NY, int NZ, const double *X, const double *Y,
                  const double *Z, int mx, int my, int mz, double a0, double K)
{
    double best = 0.0;
    int ilo = mx ? 0 : 1, jlo = my ? 0 : 1, klo = mz ? 0 : 1;
    for (int i = ilo; i < NX - 1; i++)
        for (int j = jlo; j < NY - 1; j++)
            for (int k = klo; k < NZ - 1; k++) {
                size_t n = IDX(i, j, k);
                double r = rho_abs[n];
                if (r == 0.0) continue;
                double gx = (i == 0) ? 0.0 : (u[IDX(i + 1, j, k)] - u[IDX(i - 1, j, k)]) / (X[i + 1] - X[i - 1]);
                double gy = (j == 0) ? 0.0 : (u[IDX(i, j + 1, k)] - u[IDX(i, j - 1, k)]) / (Y[j + 1] - Y[j - 1]);
                double gz = (k == 0) ? 0.0 : (u[IDX(i, j, k + 1)] - u[IDX(i, j, k - 1)]) / (Z[k + 1] - Z[k - 1]);
                double x = sqrt(gx * gx + gy * gy + gz * gz) / a0;
                double w = K * r * ((1.0 + x) * (1.0 + x) - 1.0);
                if (w > best) best = w;
            }
    return best;
}

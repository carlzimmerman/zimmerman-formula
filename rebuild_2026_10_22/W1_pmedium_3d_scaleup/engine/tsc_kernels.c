/* W1 engine kernels: TSC deposition, TSC force gather, pairwise isolated potential energy.
 * Arithmetic mirrors sol61_push/fragment_radiation_2026_10_22/model.py Model.deposit and the gather in
 * sol61_push/spatial_expansion_2026_10_23/model.py evaluate():
 *   u = x/dx + n/2, j = floor(u + .5), dist = u - (j+o), ad = |dist|,
 *   w  = ad < .5 ? .75 - dist*dist : .5*((1.5-ad)*(1.5-ad)),
 *   dw = (ad < .5 ? -2*dist : -(1.5-ad)*sign(dist)) / dx,
 *   weight = (wx*wy)*wz, der_i = (dw_i*w_{i+1})*w_{i+2},
 *   rho[flat] += (m/vol)*weight in particle order (np.bincount order),
 *   force_p = -(sum_k F[flat_k]*der_k) with NumPy's pairwise order over the 27 offsets (see pairwise27).
 * Compile with -ffp-contract=off (no FMA) and without fast-math.
 * Threading: deposition splits the grid into x-slabs (each cell still accumulates in particle order), the gather and the
 * pair sums split particles; results are independent of the thread count. */
#include <math.h>
#include <pthread.h>
#include <stdint.h>
#include <stdlib.h>

/* Python-style modulo; wrapped particles give a in [-1, n+1], so the branch path avoids the integer division. */
static inline int64_t pmod(int64_t a, int64_t n) {
    if (a >= 0 && a < n) return a;
    if (a < 0 && a >= -n) return a + n;
    if (a >= n && a < 2 * n) return a - n;
    int64_t r = a % n; return r < 0 ? r + n : r;
}

static inline void weights1d(double u, int64_t j, double dx, double w[3], double dw[3]) {
    for (int o = -1; o <= 1; o++) {
        double dist = u - (double)(j + o);
        double ad = fabs(dist);
        double sg = (dist > 0) ? 1.0 : ((dist < 0) ? -1.0 : 0.0);
        if (ad < .5) { w[o + 1] = .75 - dist * dist; dw[o + 1] = (-2 * dist) / dx; }
        else { double t = 1.5 - ad; w[o + 1] = .5 * (t * t); dw[o + 1] = ((-t) * sg) / dx; }
    }
}

typedef struct {
    int64_t n, np, x0, x1, p0, p1;
    double dx, val, eps2;
    const double *x, *F, *m;
    double *out;
} job_t;

static void *deposit_worker(void *arg) {
    job_t *J = (job_t *)arg;
    const int64_t n = J->n; const double dx = J->dx, half = (double)n / 2.0;
    for (int64_t p = 0; p < J->np; p++) {
        double u[3]; int64_t j[3];
        for (int a = 0; a < 3; a++) { u[a] = J->x[3 * p + a] / dx + half; j[a] = (int64_t)floor(u[a] + .5); }
        int any = 0; int64_t ix[3];
        for (int o = 0; o < 3; o++) { ix[o] = pmod(j[0] + o - 1, n); if (ix[o] >= J->x0 && ix[o] < J->x1) any = 1; }
        if (!any) continue;
        double w[3][3], dw[3][3];
        for (int a = 0; a < 3; a++) weights1d(u[a], j[a], dx, w[a], dw[a]);
        int64_t iy[3], iz[3];
        for (int o = 0; o < 3; o++) { iy[o] = pmod(j[1] + o - 1, n) * n; iz[o] = pmod(j[2] + o - 1, n); }
        for (int ox = 0; ox < 3; ox++) {
            if (ix[ox] < J->x0 || ix[ox] >= J->x1) continue;
            double *row = J->out + ix[ox] * n * n;
            for (int oy = 0; oy < 3; oy++) {
                const double a0 = w[0][ox] * w[1][oy];
                for (int oz = 0; oz < 3; oz++) row[iy[oy] + iz[oz]] += J->val * (a0 * w[2][oz]);
            }
        }
    }
    return NULL;
}

/* NumPy 1.26 pairwise sum for 8 <= n <= 128 (8 accumulators), as used by np.sum along a contiguous axis:
 * the gather product array F[flat][:,:,None]*der inherits der's layout, whose 27-offset axis is contiguous,
 * so np.sum(axis=1) returns 0.0 + pairwise(t[0..26]). */
static inline double pairwise27(const double *t) {
    double r[8];
    for (int j = 0; j < 8; j++) r[j] = t[j];
    for (int i = 8; i < 24; i += 8) for (int j = 0; j < 8; j++) r[j] += t[i + j];
    double res = ((r[0] + r[1]) + (r[2] + r[3])) + ((r[4] + r[5]) + (r[6] + r[7]));
    for (int i = 24; i < 27; i++) res += t[i];
    return 0.0 + res;
}

static void *gather_worker(void *arg) {
    job_t *J = (job_t *)arg;
    const int64_t n = J->n; const double dx = J->dx, half = (double)n / 2.0;
    for (int64_t p = J->p0; p < J->p1; p++) {
        double u[3]; int64_t j[3];
        for (int a = 0; a < 3; a++) { u[a] = J->x[3 * p + a] / dx + half; j[a] = (int64_t)floor(u[a] + .5); }
        double w[3][3], dw[3][3];
        for (int a = 0; a < 3; a++) weights1d(u[a], j[a], dx, w[a], dw[a]);
        int64_t ix[3], iy[3], iz[3];
        for (int o = 0; o < 3; o++) { ix[o] = pmod(j[0] + o - 1, n) * n * n; iy[o] = pmod(j[1] + o - 1, n) * n; iz[o] = pmod(j[2] + o - 1, n); }
        double t0[27], t1[27], t2[27]; int k = 0;
        for (int ox = 0; ox < 3; ox++) {
            for (int oy = 0; oy < 3; oy++) {
                const double *Frow = J->F + ix[ox] + iy[oy];
                const double a0 = dw[0][ox] * w[1][oy];
                for (int oz = 0; oz < 3; oz++, k++) {
                    double f = Frow[iz[oz]];
                    t0[k] = f * (a0 * w[2][oz]);
                    t1[k] = f * ((dw[1][oy] * w[2][oz]) * w[0][ox]);
                    t2[k] = f * ((dw[2][oz] * w[0][ox]) * w[1][oy]);
                }
            }
        }
        J->out[3 * p] = -pairwise27(t0); J->out[3 * p + 1] = -pairwise27(t1); J->out[3 * p + 2] = -pairwise27(t2);
    }
    return NULL;
}

static void *pair_worker(void *arg) {
    job_t *J = (job_t *)arg;
    for (int64_t i = J->p0; i < J->p1; i++) {
        double s = 0; const double *ri = J->x + 3 * i;
        for (int64_t k = i + 1; k < J->np; k++) {
            const double *rk = J->x + 3 * k;
            double a = ri[0] - rk[0], b = ri[1] - rk[1], c = ri[2] - rk[2];
            s += J->m[k] / sqrt(a * a + b * b + c * c + J->eps2);
        }
        J->out[i] = J->m[i] * s;
    }
    return NULL;
}

static void run_threads(void *(*fn)(void *), job_t *jobs, int nt) {
    if (nt <= 1) { fn(&jobs[0]); return; }
    pthread_t *th = (pthread_t *)malloc(sizeof(pthread_t) * nt);
    for (int t = 0; t < nt; t++) pthread_create(&th[t], NULL, fn, &jobs[t]);
    for (int t = 0; t < nt; t++) pthread_join(th[t], NULL);
    free(th);
}

/* rho must be zero-filled by the caller (n^3 doubles). */
void tsc_deposit(int64_t n, double dx, int64_t np, const double *x, double val, double *rho, int nthreads) {
    int nt = nthreads < 1 ? 1 : nthreads; if (nt > n) nt = (int)n;
    job_t *jobs = (job_t *)calloc(nt, sizeof(job_t));
    for (int t = 0; t < nt; t++) {
        jobs[t].n = n; jobs[t].np = np; jobs[t].dx = dx; jobs[t].val = val; jobs[t].x = x; jobs[t].out = rho;
        jobs[t].x0 = (n * t) / nt; jobs[t].x1 = (n * (t + 1)) / nt;
    }
    run_threads(deposit_worker, jobs, nt);
    free(jobs);
}

void tsc_gather(int64_t n, double dx, int64_t np, const double *x, const double *F, double *out, int nthreads) {
    int nt = nthreads < 1 ? 1 : nthreads;
    job_t *jobs = (job_t *)calloc(nt, sizeof(job_t));
    for (int t = 0; t < nt; t++) {
        jobs[t].n = n; jobs[t].np = np; jobs[t].dx = dx; jobs[t].x = x; jobs[t].F = F; jobs[t].out = out;
        jobs[t].p0 = (np * t) / nt; jobs[t].p1 = (np * (t + 1)) / nt;
    }
    run_threads(gather_worker, jobs, nt);
    free(jobs);
}

/* rowsum[i] = m_i * sum_{k>i} m_k / sqrt(|r_i-r_k|^2 + eps2); r physical positions (np x 3). */
void pair_rows(int64_t np, const double *r, const double *m, double eps2, double *rowsum, int nthreads) {
    int nt = nthreads < 1 ? 1 : nthreads;
    job_t *jobs = (job_t *)calloc(nt, sizeof(job_t));
    /* balance the triangular work: split so each thread gets ~equal pair counts */
    double total = (double)np * (double)(np - 1) / 2.0; int64_t start = 0;
    for (int t = 0; t < nt; t++) {
        jobs[t].np = np; jobs[t].x = r; jobs[t].m = m; jobs[t].eps2 = eps2; jobs[t].out = rowsum; jobs[t].p0 = start;
        int64_t end = start; double acc = 0, goal = total / nt;
        if (t == nt - 1) end = np; else { while (end < np && acc < goal) { acc += (double)(np - 1 - end); end++; } }
        jobs[t].p1 = end; start = end;
    }
    run_threads(pair_worker, jobs, nt);
    free(jobs);
}

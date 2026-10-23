/* X1 E1 truncated-Wigner lattice kernel: one velocity-Verlet step of the conformal equations of the action.
 *   phi'' = Lap phi - mp2 phi - 2 ga x conj(phi) - 2 lam (|phi|^2 - 2c) phi
 *   x''   = Lap x   - mx2 x   - ga phi^2
 * mp2 = (m/H)^2 a^2 - (1-6xi) a''/a,  mx2 = (M/H)^2 a^2 - (1-6xi) a''/a,  ga = (g/H) a.
 * Per-site arithmetic only (no reductions), so results are identical for any thread count.
 * Build: cc -O2 -fcx-limited-range -fPIC -shared -o x1_lattice_kernel.so x1_lattice_kernel.c -lpthread   (no -ffast-math: bitwise resume)
 */
#include <complex.h>
#include <pthread.h>
#include <stdlib.h>

typedef double complex cplx;

typedef struct {
    int N, z0, z1; double idx2, dt, mp2, mx2, ga, lam, c;
    cplx *phi, *pphi, *x, *px, *fphi, *fx; int mode;   /* mode 0: force only; 1: half-kick+drift; 2: half-kick */
} job_t;

static inline long IDX(int N, int i, int j, int k) { return ((long)i*N + j)*N + k; }

static void force_slab(job_t *J) {
    int N = J->N;
    for (int i = J->z0; i < J->z1; i++) {
        int ip = (i+1)%N, im = (i+N-1)%N;
        for (int j = 0; j < N; j++) {
            int jp = (j+1)%N, jm = (j+N-1)%N;
            for (int k = 0; k < N; k++) {
                int kp = (k+1)%N, km = (k+N-1)%N;
                long s = IDX(N,i,j,k);
                cplx p = J->phi[s], xx = J->x[s];
                cplx lp = (J->phi[IDX(N,ip,j,k)] + J->phi[IDX(N,im,j,k)] + J->phi[IDX(N,i,jp,k)] + J->phi[IDX(N,i,jm,k)]
                         + J->phi[IDX(N,i,j,kp)] + J->phi[IDX(N,i,j,km)] - 6.0*p) * J->idx2;
                cplx lx = (J->x[IDX(N,ip,j,k)] + J->x[IDX(N,im,j,k)] + J->x[IDX(N,i,jp,k)] + J->x[IDX(N,i,jm,k)]
                         + J->x[IDX(N,i,j,kp)] + J->x[IDX(N,i,j,km)] - 6.0*xx) * J->idx2;
                double r2 = creal(p)*creal(p) + cimag(p)*cimag(p);
                J->fphi[s] = lp - J->mp2*p - 2.0*J->ga*xx*conj(p) - 2.0*J->lam*(r2 - 2.0*J->c)*p;
                J->fx[s]   = lx - J->mx2*xx - J->ga*p*p;
            }
        }
    }
}

static void *worker(void *arg) {
    job_t *J = (job_t *)arg; int N = J->N;
    long a = (long)J->z0*N*N, b = (long)J->z1*N*N;
    if (J->mode == 0) { force_slab(J); return NULL; }
    double h = 0.5*J->dt;
    for (long s = a; s < b; s++) { J->pphi[s] += h*J->fphi[s]; J->px[s] += h*J->fx[s]; }
    if (J->mode == 1) for (long s = a; s < b; s++) { J->phi[s] += J->dt*J->pphi[s]; J->x[s] += J->dt*J->px[s]; }
    return NULL;
}

static void run(int nth, job_t *base) {
    int N = base->N; if (nth < 1) nth = 1; if (nth > N) nth = N;
    pthread_t *th = malloc(sizeof(pthread_t)*nth); job_t *jb = malloc(sizeof(job_t)*nth);
    for (int t = 0; t < nth; t++) {
        jb[t] = *base; jb[t].z0 = (int)((long)N*t/nth); jb[t].z1 = (int)((long)N*(t+1)/nth);
        if (nth == 1) worker(&jb[t]); else pthread_create(&th[t], NULL, worker, &jb[t]);
    }
    if (nth > 1) for (int t = 0; t < nth; t++) pthread_join(th[t], NULL);
    free(th); free(jb);
}

/* Compute forces at the given parameters into fphi, fx. */
void x1_force(int N, double dx, cplx *phi, cplx *x, cplx *fphi, cplx *fx,
              double mp2, double mx2, double ga, double lam, double c, int nth) {
    job_t J = {N, 0, N, 1.0/(dx*dx), 0.0, mp2, mx2, ga, lam, c, phi, NULL, x, NULL, fphi, fx, 0};
    run(nth, &J);
}

/* nsteps velocity-Verlet steps. On entry fphi/fx hold forces at (phi,x) with params p0; params for the end of each step
 * are given in arrays mp2[s], mx2[s], ga[s] (s = 0..nsteps-1). On exit fphi/fx hold forces at the final state. */
void x1_steps(int N, double dx, double dt, int nsteps, cplx *phi, cplx *pphi, cplx *x, cplx *px, cplx *fphi, cplx *fx,
              const double *mp2, const double *mx2, const double *ga, double lam, double c, int nth) {
    for (int s = 0; s < nsteps; s++) {
        job_t J = {N, 0, N, 1.0/(dx*dx), dt, 0, 0, 0, lam, c, phi, pphi, x, px, fphi, fx, 1};
        run(nth, &J);                                   /* half kick with old force + drift */
        job_t F = {N, 0, N, 1.0/(dx*dx), dt, mp2[s], mx2[s], ga[s], lam, c, phi, NULL, x, NULL, fphi, fx, 0};
        run(nth, &F);                                   /* force at new time */
        job_t K = {N, 0, N, 1.0/(dx*dx), dt, 0, 0, 0, lam, c, phi, pphi, x, px, fphi, fx, 2};
        run(nth, &K);                                   /* second half kick */
    }
}

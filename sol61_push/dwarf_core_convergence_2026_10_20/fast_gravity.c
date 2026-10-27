/* Full 3-D Plummer pair Hamiltonian, double precision, symmetric pair updates.
 * Explicit build (macOS):
 * clang -O3 -ffp-contract=off -dynamiclib -pthread fast_gravity.c -o fast_gravity.dylib
 * Add -DFAST_GRAVITY_SCALAR for an independently selectable scalar build.
 * Never compile with fast-math. There is no approximate reciprocal/square root.
 *
 * Each call owns all scratch and pthread state. Each unordered pair appears
 * once; both endpoints use the same central pair factor. Thread-local SoA
 * force/potential arrays are merged in a fixed thread order. This changes
 * floating summation order, not the Hamiltonian, and is not bitwise equivalent
 * to the historical serial trajectory. Collisions/integration are not here.
 */
#include <math.h>
#include <pthread.h>
#include <stddef.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#ifdef __FAST_MATH__
#error "fast-math is forbidden for the conservative gravity backend"
#endif
#pragma STDC FP_CONTRACT OFF

#if defined(__aarch64__) && !defined(FAST_GRAVITY_SCALAR)
#include <arm_neon.h>
#define FG_VECTOR 1
#endif

struct worker {
    const double *px, *py, *pz, *mass;
    double *ax, *ay, *az, *phi;
    size_t count, index, workers;
    double eps2, G;
    int status;
};

static void *calculate_pairs(void *pointer) {
    struct worker *w = (struct worker *)pointer;
    const size_t count = w->count;
    for (size_t i = w->index; i < count; i += w->workers) {
        const double xi = w->px[i], yi = w->py[i], zi = w->pz[i], mi = w->mass[i];
        size_t j = i + 1;
#ifdef FG_VECTOR
        const float64x2_t vi_x = vdupq_n_f64(xi), vi_y = vdupq_n_f64(yi), vi_z = vdupq_n_f64(zi);
        const float64x2_t vone = vdupq_n_f64(1.0), veps = vdupq_n_f64(w->eps2);
        const float64x2_t vG = vdupq_n_f64(w->G), vmi = vdupq_n_f64(mi);
        float64x2_t sum_x = vdupq_n_f64(0.0), sum_y = vdupq_n_f64(0.0);
        float64x2_t sum_z = vdupq_n_f64(0.0), sum_phi = vdupq_n_f64(0.0);
        for (; j + 1 < count; j += 2) {
            const float64x2_t dx = vsubq_f64(vld1q_f64(w->px + j), vi_x);
            const float64x2_t dy = vsubq_f64(vld1q_f64(w->py + j), vi_y);
            const float64x2_t dz = vsubq_f64(vld1q_f64(w->pz + j), vi_z);
            float64x2_t r2 = vaddq_f64(vmulq_f64(dx, dx), vmulq_f64(dy, dy));
            r2 = vaddq_f64(r2, vmulq_f64(dz, dz));
            r2 = vaddq_f64(r2, veps);
            if (vminvq_f64(r2) <= 0.0) { w->status = 1; return NULL; }
            const float64x2_t inverse = vdivq_f64(vone, vsqrtq_f64(r2));
            const float64x2_t gravity_inverse = vmulq_f64(vG, inverse);
            const float64x2_t factor = vmulq_f64(vmulq_f64(gravity_inverse, inverse), inverse);
            const float64x2_t mass_j = vld1q_f64(w->mass + j);
            const float64x2_t factor_i = vmulq_f64(mass_j, factor);
            const float64x2_t factor_j = vmulq_f64(vmi, factor);
            sum_x = vaddq_f64(sum_x, vmulq_f64(factor_i, dx));
            sum_y = vaddq_f64(sum_y, vmulq_f64(factor_i, dy));
            sum_z = vaddq_f64(sum_z, vmulq_f64(factor_i, dz));
            vst1q_f64(w->ax + j, vsubq_f64(vld1q_f64(w->ax + j), vmulq_f64(factor_j, dx)));
            vst1q_f64(w->ay + j, vsubq_f64(vld1q_f64(w->ay + j), vmulq_f64(factor_j, dy)));
            vst1q_f64(w->az + j, vsubq_f64(vld1q_f64(w->az + j), vmulq_f64(factor_j, dz)));
            sum_phi = vsubq_f64(sum_phi, vmulq_f64(gravity_inverse, mass_j));
            vst1q_f64(w->phi + j, vsubq_f64(vld1q_f64(w->phi + j), vmulq_f64(gravity_inverse, vmi)));
        }
        w->ax[i] += vaddvq_f64(sum_x);
        w->ay[i] += vaddvq_f64(sum_y);
        w->az[i] += vaddvq_f64(sum_z);
        w->phi[i] += vaddvq_f64(sum_phi);
#endif
        for (; j < count; ++j) {
            const double dx = w->px[j] - xi, dy = w->py[j] - yi, dz = w->pz[j] - zi;
            const double r2 = dx*dx + dy*dy + dz*dz + w->eps2;
            if (r2 <= 0.0) { w->status = 1; return NULL; }
            const double inverse = 1.0 / sqrt(r2);
            const double gravity_inverse = w->G * inverse;
            const double factor = gravity_inverse * inverse * inverse;
            const double factor_i = w->mass[j] * factor, factor_j = mi * factor;
            w->ax[i] += factor_i * dx; w->ay[i] += factor_i * dy; w->az[i] += factor_i * dz;
            w->ax[j] -= factor_j * dx; w->ay[j] -= factor_j * dy; w->az[j] -= factor_j * dz;
            w->phi[i] -= gravity_inverse * w->mass[j];
            w->phi[j] -= gravity_inverse * mi;
        }
    }
    return NULL;
}

int fast_gravity_simd_enabled(void) {
#ifdef FG_VECTOR
    return 1;
#else
    return 0;
#endif
}

/* Status: 0 success; 1 singular unsoftened pair; 2 allocation/size failure;
 * 3 pthread launch failure; 4 invalid scalar parameters. Caller validates data.
 */
int fast_gravity_kernel(const double *x, const double *mass, size_t count,
                        double eps, double G, size_t requested_threads,
                        double *acceleration, double *phi) {
    if (requested_threads == 0 || requested_threads > 64 || eps < 0.0 || !isfinite(eps) || !isfinite(G)) return 4;
    if (count > SIZE_MAX / (4 * sizeof(double) * requested_threads)) return 2;
    memset(acceleration, 0, 3 * count * sizeof(double));
    memset(phi, 0, count * sizeof(double));
    if (count < 2) return 0;
    const size_t workers = requested_threads < count ? requested_threads : count;
    double *position = (double *)malloc(3 * count * sizeof(double));
    double *scratch = (double *)calloc(4 * workers * count, sizeof(double));
    struct worker *tasks = (struct worker *)calloc(workers, sizeof(struct worker));
    pthread_t *threads = (pthread_t *)malloc(workers * sizeof(pthread_t));
    if (!position || !scratch || !tasks || !threads) {
        free(position); free(scratch); free(tasks); free(threads); return 2;
    }
    for (size_t i = 0; i < count; ++i) {
        position[i] = x[3*i]; position[count+i] = x[3*i+1]; position[2*count+i] = x[3*i+2];
    }
    for (size_t index = 0; index < workers; ++index) {
        tasks[index].px = position; tasks[index].py = position + count;
        tasks[index].pz = position + 2*count; tasks[index].mass = mass;
        double *buffer = scratch + 4*index*count;
        tasks[index].ax = buffer; tasks[index].ay = buffer + count;
        tasks[index].az = buffer + 2*count; tasks[index].phi = buffer + 3*count;
        tasks[index].count = count; tasks[index].index = index; tasks[index].workers = workers;
        tasks[index].eps2 = eps * eps; tasks[index].G = G;
    }
    size_t launched = 0;
    int status = 0;
    for (size_t index = 1; index < workers; ++index) {
        if (pthread_create(threads + index, NULL, calculate_pairs, tasks + index)) {
            status = 3; break;
        }
        launched = index;
    }
    if (status == 0) calculate_pairs(tasks);
    for (size_t index = 1; index <= launched; ++index) pthread_join(threads[index], NULL);
    if (status == 0) {
        for (size_t index = 0; index < workers; ++index) {
            if (tasks[index].status) { status = tasks[index].status; break; }
            for (size_t i = 0; i < count; ++i) {
                acceleration[3*i] += tasks[index].ax[i];
                acceleration[3*i+1] += tasks[index].ay[i];
                acceleration[3*i+2] += tasks[index].az[i];
                phi[i] += tasks[index].phi[i];
            }
        }
    }
    free(position); free(scratch); free(tasks); free(threads);
    return status;
}

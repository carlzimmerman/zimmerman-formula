// ZK1: direct-summation softened gravity, the same sum as x48_zoom.accel. a_i = G m sum_j (x_j - x_i) / (|x_j - x_i|^2 + eps^2)^(3/2) + OLH2 x_i.
// Split arrays so the inner loop vectorises. Range form so a caller can thread it.
#include <math.h>
void x48_accel(const double *restrict x, const double *restrict y, const double *restrict z, long N, double Gm, double eps2, double OLH2,
               long i0, long i1, double *restrict ax, double *restrict ay, double *restrict az) {
    for (long i = i0; i < i1; i++) {
        const double xi = x[i], yi = y[i], zi = z[i]; double sx = 0.0, sy = 0.0, sz = 0.0;
        #pragma clang loop vectorize(enable) interleave(enable)
        for (long j = 0; j < N; j++) {
            const double dx = x[j] - xi, dy = y[j] - yi, dz = z[j] - zi, r2 = dx * dx + dy * dy + dz * dz + eps2, inv = 1.0 / (r2 * sqrt(r2));
            sx += dx * inv; sy += dy * inv; sz += dz * inv;
        }
        ax[i] = Gm * sx + OLH2 * xi; ay[i] = Gm * sy + OLH2 * yi; az[i] = Gm * sz + OLH2 * zi;
    }
}

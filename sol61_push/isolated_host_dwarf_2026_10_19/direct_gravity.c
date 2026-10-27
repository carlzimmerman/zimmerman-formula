/* Exact softened pair Hamiltonian, one CPU thread, no fast-math flags.
 * Build explicitly on macOS:
 * cc -O3 -dynamiclib direct_gravity.c -o direct_gravity.dylib
 * No runtime compilation is performed by the Python module.
 */
#include <math.h>
#include <stddef.h>
#include <stdint.h>
#include <string.h>

int gravity_kernel(const double *x, const double *m, size_t count,
                   double epsilon, double grav_constant,
                   double *acceleration, double *potential) {
    memset(acceleration, 0, 3 * count * sizeof(double));
    double energy = 0.0;
    const double epsilon2 = epsilon * epsilon;
    for (size_t i = 0; i < count; ++i) {
        for (size_t j = i + 1; j < count; ++j) {
            const double dx = x[3*j] - x[3*i];
            const double dy = x[3*j+1] - x[3*i+1];
            const double dz = x[3*j+2] - x[3*i+2];
            const double radius2 = dx*dx + dy*dy + dz*dz + epsilon2;
            if (radius2 <= 0.0) return 1;
            const double inverse_r = 1.0 / sqrt(radius2);
            const double factor = grav_constant * inverse_r * inverse_r * inverse_r;
            const double factor_i = m[j] * factor;
            const double factor_j = m[i] * factor;
            acceleration[3*i] += factor_i * dx;
            acceleration[3*i+1] += factor_i * dy;
            acceleration[3*i+2] += factor_i * dz;
            acceleration[3*j] -= factor_j * dx;
            acceleration[3*j+1] -= factor_j * dy;
            acceleration[3*j+2] -= factor_j * dz;
            energy -= grav_constant * m[i] * m[j] * inverse_r;
        }
    }
    *potential = energy;
    return 0;
}

/* Python supplies all unordered neighbors in randomized sequential order and
 * one uniform variate per candidate. No threads or RNG state live in C.
 * stats = max_probability, delta_K, delta_J_x/y/z, max_resonance_z.
 */
int scatter_kernel(const double *x, double *v, const double *m,
                   const int64_t *pairs, const double *uniforms, size_t count,
                   double coefficient, double h, double resonance_u,
                   double light_speed, double *stats, int64_t *hits) {
    memset(stats, 0, 6 * sizeof(double));
    *hits = 0;
    const double resonance_scale = 2.0 * resonance_u * light_speed;
    for (size_t pair = 0; pair < count; ++pair) {
        const size_t i = (size_t)pairs[2*pair];
        const size_t j = (size_t)pairs[2*pair+1];
        double n[3], relative[3], radius2 = 0.0, speed2 = 0.0;
        for (size_t axis = 0; axis < 3; ++axis) {
            n[axis] = x[3*i+axis] - x[3*j+axis];
            relative[axis] = v[3*i+axis] - v[3*j+axis];
            radius2 += n[axis] * n[axis];
            speed2 += relative[axis] * relative[axis];
        }
        if (radius2 == 0.0 || radius2 >= h*h) continue;
        const double z = speed2 / (resonance_scale * resonance_scale);
        if (z > stats[5]) stats[5] = z;
        if (z >= 0.1) return 1;
        const double inverse_radius = 1.0 / sqrt(radius2);
        double incoming = 0.0;
        for (size_t axis = 0; axis < 3; ++axis) {
            n[axis] *= inverse_radius;
            incoming -= relative[axis] * n[axis];
        }
        if (incoming <= 0.0) continue;
        const double amplitude_ratio = (2.0 - z / (1.0 - z)) / 2.0;
        const double ratio = amplitude_ratio * amplitude_ratio / (1.0 + resonance_u*resonance_u*z);
        const double probability = coefficient * ratio * incoming;
        if (probability > stats[0]) stats[0] = probability;
        if (probability > 0.05) return 2;
        if (uniforms[pair] >= probability) continue;
        double delta_p_i[3], delta_p_j[3];
        double before_energy = 0.0, after_energy = 0.0;
        for (size_t axis = 0; axis < 3; ++axis) {
            const double before_i = v[3*i+axis];
            const double before_j = v[3*j+axis];
            before_energy += before_i*before_i + before_j*before_j;
            v[3*i+axis] += incoming * n[axis];
            v[3*j+axis] -= incoming * n[axis];
            after_energy += v[3*i+axis]*v[3*i+axis] + v[3*j+axis]*v[3*j+axis];
            delta_p_i[axis] = m[i] * (v[3*i+axis] - before_i);
            delta_p_j[axis] = m[j] * (v[3*j+axis] - before_j);
        }
        stats[1] += 0.5 * m[i] * (after_energy - before_energy);
        for (size_t axis = 0; axis < 3; ++axis) {
            const size_t first = (axis + 1) % 3, second = (axis + 2) % 3;
            stats[2+axis] += x[3*i+first]*delta_p_i[second] - x[3*i+second]*delta_p_i[first]
                           + x[3*j+first]*delta_p_j[second] - x[3*j+second]*delta_p_j[first];
        }
        ++*hits;
    }
    return 0;
}

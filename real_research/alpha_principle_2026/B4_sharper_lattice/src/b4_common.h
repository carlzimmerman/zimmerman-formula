/* shared helpers for the B4 lattice programs (copied from the B2 lane, unchanged apart from the include guard): RNG (xoshiro256**), lattice indexing */
#ifndef B4_COMMON_H
#define B4_COMMON_H
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <string.h>

typedef struct { uint64_t s[4]; } rng_t;
static inline uint64_t rotl64(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
static uint64_t splitmix64(uint64_t *x) {
  uint64_t z = (*x += 0x9e3779b97f4a7c15ULL);
  z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
  z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
  return z ^ (z >> 31);
}
static void rng_seed(rng_t *r, uint64_t seed) {
  uint64_t x = seed * 0x2545F4914F6CDD1DULL + 12345ULL;
  for (int i = 0; i < 4; i++) r->s[i] = splitmix64(&x);
}
static inline uint64_t rng_u64(rng_t *r) {
  uint64_t *s = r->s;
  uint64_t result = rotl64(s[1] * 5, 7) * 9;
  uint64_t t = s[1] << 17;
  s[2] ^= s[0]; s[3] ^= s[1]; s[1] ^= s[2]; s[0] ^= s[3];
  s[2] ^= t; s[3] = rotl64(s[3], 45);
  return result;
}
static inline double rng_u(rng_t *r) { return (rng_u64(r) >> 11) * (1.0 / 9007199254740992.0); } /* [0,1) */
static double rng_gauss(rng_t *r) {
  double u1 = 1.0 - rng_u(r), u2 = rng_u(r);
  return sqrt(-2.0 * log(u1)) * cos(6.283185307179586 * u2);
}

/* hypercubic periodic lattice */
typedef struct { int L, V; int *nbp, *nbm; } lat_t; /* nbp[s*4+mu] = site s+mu ; nbm = s-mu */
static void lat_init(lat_t *l, int L) {
  l->L = L; l->V = L * L * L * L;
  l->nbp = (int *)malloc(sizeof(int) * 4 * l->V); l->nbm = (int *)malloc(sizeof(int) * 4 * l->V);
  for (int s = 0; s < l->V; s++) {
    int c[4]; int t = s;
    for (int m = 0; m < 4; m++) { c[m] = t % L; t /= L; }
    for (int m = 0; m < 4; m++) {
      int cp[4] = {c[0], c[1], c[2], c[3]}, cm[4] = {c[0], c[1], c[2], c[3]};
      cp[m] = (c[m] + 1) % L; cm[m] = (c[m] + L - 1) % L;
      int sp = 0, sm = 0;
      for (int k = 3; k >= 0; k--) { sp = sp * L + cp[k]; sm = sm * L + cm[k]; }
      l->nbp[s * 4 + m] = sp; l->nbm[s * 4 + m] = sm;
    }
  }
}
#endif

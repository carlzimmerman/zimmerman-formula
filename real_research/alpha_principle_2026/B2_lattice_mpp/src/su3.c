/* B2 lane: SU(3) 4D fundamental-adjoint lattice gauge theory, Metropolis multi-hit with a fixed pool of near-identity SU(3) matrices closed under inversion.
   S = beta_F sum_p (1 - ReTr U_p/3) + beta_A sum_p (1 - Tr_adj U_p/8),  Tr_adj = |Tr U|^2 - 1
   usage: su3 L betaF betaA nsweep ntherm seed start(0 hot,1 cold) hits mutate outfile [every]
   output: binary float64 pairs per measured sweep: (mean ReTr/3 = X_F, mean (|Tr|^2-1)/8 = X_A)
   mutate=1 (control): update-side adjoint normalisation 1/9 instead of 1/8 (measured X_A unchanged) */
#include "b2_common.h"
typedef struct { double r[9], i[9]; } m3;
static inline void mm(const m3 *a, const m3 *b, m3 *c) {
  for (int x = 0; x < 3; x++) for (int y = 0; y < 3; y++) {
    double sr = 0, si = 0;
    for (int k = 0; k < 3; k++) { double ar = a->r[x*3+k], ai = a->i[x*3+k], br = b->r[k*3+y], bi = b->i[k*3+y]; sr += ar*br - ai*bi; si += ar*bi + ai*br; }
    c->r[x*3+y] = sr; c->i[x*3+y] = si;
  }
}
static inline void dag(const m3 *a, m3 *c) { for (int x = 0; x < 3; x++) for (int y = 0; y < 3; y++) { c->r[x*3+y] = a->r[y*3+x]; c->i[x*3+y] = -a->i[y*3+x]; } }
static void ident(m3 *a) { memset(a, 0, sizeof(m3)); a->r[0] = a->r[4] = a->r[8] = 1.0; }
static void reunit(m3 *a) { /* Gram-Schmidt rows 0,1, row 2 = conj(row0 x row1) */
  double n = 0; for (int k = 0; k < 3; k++) n += a->r[k]*a->r[k] + a->i[k]*a->i[k]; n = 1.0/sqrt(n); for (int k = 0; k < 3; k++) { a->r[k] *= n; a->i[k] *= n; }
  double pr = 0, pi = 0; for (int k = 0; k < 3; k++) { pr += a->r[k]*a->r[3+k] + a->i[k]*a->i[3+k]; pi += a->r[k]*a->i[3+k] - a->i[k]*a->r[3+k]; }
  for (int k = 0; k < 3; k++) { double xr = a->r[3+k] - (pr*a->r[k] - pi*a->i[k]), xi = a->i[3+k] - (pr*a->i[k] + pi*a->r[k]); a->r[3+k] = xr; a->i[3+k] = xi; }
  n = 0; for (int k = 0; k < 3; k++) n += a->r[3+k]*a->r[3+k] + a->i[3+k]*a->i[3+k]; n = 1.0/sqrt(n); for (int k = 0; k < 3; k++) { a->r[3+k] *= n; a->i[3+k] *= n; }
  /* row2 = conj(row0 x row1) */
  for (int k = 0; k < 3; k++) { int k1 = (k+1)%3, k2 = (k+2)%3;
    double cr = a->r[k1]*a->r[3+k2] - a->i[k1]*a->i[3+k2] - (a->r[k2]*a->r[3+k1] - a->i[k2]*a->i[3+k1]);
    double ci = a->r[k1]*a->i[3+k2] + a->i[k1]*a->r[3+k2] - (a->r[k2]*a->i[3+k1] + a->i[k2]*a->r[3+k1]);
    a->r[6+k] = cr; a->i[6+k] = -ci; }
}
static void rand_su3(rng_t *R, double eps, m3 *out) { /* product of three SU(2) subgroup rotations near identity */
  m3 acc; ident(&acc);
  for (int sub = 0; sub < 3; sub++) {
    int p = (sub == 0) ? 0 : (sub == 1) ? 1 : 0, q = (sub == 0) ? 1 : (sub == 1) ? 2 : 2;
    double v[4]; double n = 0; for (int i = 1; i < 4; i++) { v[i] = rng_gauss(R); n += v[i]*v[i]; }
    double al = eps * (2*rng_u(R) - 1) * 3.141592653589793; n = sin(al)/sqrt(n); v[0] = cos(al); for (int i = 1; i < 4; i++) v[i] *= n;
    m3 t; ident(&t);
    t.r[p*3+p] = v[0]; t.i[p*3+p] = v[3]; t.r[q*3+q] = v[0]; t.i[q*3+q] = -v[3];
    t.r[p*3+q] = v[2]; t.i[p*3+q] = v[1]; t.r[q*3+p] = -v[2]; t.i[q*3+p] = v[1];
    m3 c; mm(&t, &acc, &c); acc = c;
  }
  reunit(&acc); *out = acc;
}
int main(int argc, char **argv) {
  if (argc < 11) { fprintf(stderr, "usage\n"); return 2; }
  int L = atoi(argv[1]); double bF = atof(argv[2]), bA = atof(argv[3]); long nsw = atol(argv[4]), nth = atol(argv[5]);
  uint64_t seed = strtoull(argv[6], 0, 10); int cold = atoi(argv[7]), hits = atoi(argv[8]), mut = atoi(argv[9]);
  FILE *fo = fopen(argv[10], "wb"); if (!fo) return 3; int every = (argc > 11) ? atoi(argv[11]) : 1;
  double cA = mut ? (1.0/9.0) : (1.0/8.0);
  rng_t R; rng_seed(&R, seed); lat_t lt; lat_init(&lt, L); int V = lt.V;
  m3 *U = (m3 *)malloc(sizeof(m3) * 4 * V);
  for (int i = 0; i < 4 * V; i++) { if (cold) ident(&U[i]); else { m3 t; ident(&t); for (int k = 0; k < 6; k++) { m3 r, c; rand_su3(&R, 1.0, &r); mm(&r, &t, &c); t = c; } reunit(&t); U[i] = t; } }
  double eps = 0.25; const int NP = 100; m3 pool[200]; double poolEps = -1;
  double np = 6.0 * V;
  for (long sw = 0; sw < nsw; sw++) {
    if (sw < nth || poolEps < 0) { /* (re)build the pool with current eps: pairs (R, R^dagger) */
      for (int k = 0; k < NP; k++) { rand_su3(&R, eps, &pool[2*k]); dag(&pool[2*k], &pool[2*k+1]); } poolEps = eps; }
    long acc = 0, tot = 0;
    for (int s = 0; s < V; s++) for (int mu = 0; mu < 4; mu++) {
      int sp = lt.nbp[s * 4 + mu]; m3 St[6]; int ns = 0;
      for (int nu = 0; nu < 4; nu++) if (nu != mu) {
        int spn = lt.nbp[s * 4 + nu], smn = lt.nbm[s * 4 + nu];
        m3 a, b, c, d;
        dag(&U[spn * 4 + mu], &a); mm(&U[sp * 4 + nu], &a, &b); dag(&U[s * 4 + nu], &c); mm(&b, &c, &St[ns++]);
        int spm = lt.nbm[sp * 4 + nu];
        dag(&U[spm * 4 + nu], &a); dag(&U[smn * 4 + mu], &b); mm(&a, &b, &c); mm(&c, &U[smn * 4 + nu], &St[ns++]);
      }
      m3 u = U[s * 4 + mu];
      /* action of link as function of u: sum_i bF(1 - Re Tr(u V_i)/3) + bA(1 - cA(|Tr(u V_i)|^2 - 1)) ; only u-dependent part */
      double Su = 0;
      for (int i = 0; i < 6; i++) { double tr = 0, ti = 0; for (int x = 0; x < 3; x++) for (int y = 0; y < 3; y++) { tr += u.r[x*3+y]*St[i].r[y*3+x] - u.i[x*3+y]*St[i].i[y*3+x]; ti += u.r[x*3+y]*St[i].i[y*3+x] + u.i[x*3+y]*St[i].r[y*3+x]; }
        Su += -bF*tr/3.0 - bA*cA*(tr*tr + ti*ti); }
      for (int h = 0; h < hits; h++) {
        m3 un;
#ifdef ZFLIP
        if (h == hits - 1) { /* center-flip proposal U -> omega^{+-1} U (Z3 center; the pair omega, omega^2 is chosen with equal probability, so the proposal is symmetric) */
          double c = (rng_u(&R) < 0.5) ? -0.5 : -0.5, sn = (rng_u(&R) < 0.5) ? 0.8660254037844386 : -0.8660254037844386;
          for (int k = 0; k < 9; k++) { un.r[k] = c * u.r[k] - sn * u.i[k]; un.i[k] = c * u.i[k] + sn * u.r[k]; }
        } else
#endif
        mm(&pool[(int)(rng_u(&R) * 2 * NP)], &u, &un);
        double Sn = 0;
        for (int i = 0; i < 6; i++) { double tr = 0, ti = 0; for (int x = 0; x < 3; x++) for (int y = 0; y < 3; y++) { tr += un.r[x*3+y]*St[i].r[y*3+x] - un.i[x*3+y]*St[i].i[y*3+x]; ti += un.r[x*3+y]*St[i].i[y*3+x] + un.i[x*3+y]*St[i].r[y*3+x]; }
          Sn += -bF*tr/3.0 - bA*cA*(tr*tr + ti*ti); }
        double dS = Sn - Su; tot++;
        if (dS <= 0 || rng_u(&R) < exp(-dS)) { u = un; Su = Sn; acc++; }
      }
      reunit(&u); U[s * 4 + mu] = u;
    }
    if (sw < nth && tot > 0) { double a = (double)acc / tot; eps *= (a > 0.5) ? 1.05 : 0.95; if (eps > 1.0) eps = 1.0; if (eps < 0.02) eps = 0.02; }
    if (sw >= nth && ((sw - nth) % every == 0)) {
      double sx = 0, sa = 0;
      for (int s = 0; s < V; s++) for (int mu = 0; mu < 4; mu++) for (int nu = mu + 1; nu < 4; nu++) {
        int spm = lt.nbp[s * 4 + mu], spn = lt.nbp[s * 4 + nu];
        m3 a, b, c, d;
        mm(&U[s * 4 + mu], &U[spm * 4 + nu], &a); dag(&U[spn * 4 + mu], &b); dag(&U[s * 4 + nu], &c); mm(&b, &c, &d); 
        double tr = 0, ti = 0; for (int x = 0; x < 3; x++) for (int y = 0; y < 3; y++) { tr += a.r[x*3+y]*d.r[y*3+x] - a.i[x*3+y]*d.i[y*3+x]; ti += a.r[x*3+y]*d.i[y*3+x] + a.i[x*3+y]*d.r[y*3+x]; }
        sx += tr/3.0; sa += (tr*tr + ti*ti - 1.0)/8.0;
      }
      double o[2] = {sx / np, sa / np}; fwrite(o, sizeof(double), 2, fo);
    }
  }
  fclose(fo); fprintf(stderr, "su3 done L=%d bF=%g bA=%g eps=%g\n", L, bF, bA, eps); return 0;
}

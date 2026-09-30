/* B2 lane: SU(2) 4D fundamental-adjoint lattice gauge theory, Metropolis multi-hit (or Creutz heat bath when mode=1 and beta_A=0).
   S = beta_F sum_p (1 - x_p) + beta_A sum_p (1 - Tr_adj/3),  x_p = (1/2) Tr U_p,  Tr_adj = 4 x^2 - 1   => adjoint term = beta_A (4/3)(1 - x^2)
   usage: su2 L betaF betaA nsweep ntherm seed start(0 hot,1 cold) hits mode(0 metro,1 heatbath) mutate outfile [every]
   output: binary float64 pairs per measured sweep: (mean x_p = X_F, mean (4x^2-1)/3 = X_A)
   mutate=1 (control): the update uses adjoint normalisation 1/2 instead of 1/3, i.e. (2 - ... ) coupling (1 - Tr_adj/2) while the measured X_A is unchanged */
#include "b2_common.h"
typedef struct { double a[4]; } q_t;
static inline q_t qm(q_t p, q_t q) { /* quaternion product = SU(2) product */
  q_t r;
  r.a[0] = p.a[0]*q.a[0] - p.a[1]*q.a[1] - p.a[2]*q.a[2] - p.a[3]*q.a[3];
  r.a[1] = p.a[0]*q.a[1] + p.a[1]*q.a[0] + p.a[2]*q.a[3] - p.a[3]*q.a[2];
  r.a[2] = p.a[0]*q.a[2] - p.a[1]*q.a[3] + p.a[2]*q.a[0] + p.a[3]*q.a[1];
  r.a[3] = p.a[0]*q.a[3] + p.a[1]*q.a[2] - p.a[2]*q.a[1] + p.a[3]*q.a[0];
  return r;
}
static inline q_t qc(q_t p) { q_t r = {{p.a[0], -p.a[1], -p.a[2], -p.a[3]}}; return r; }
static inline void qn(q_t *p) { double n = 1.0 / sqrt(p->a[0]*p->a[0] + p->a[1]*p->a[1] + p->a[2]*p->a[2] + p->a[3]*p->a[3]); for (int i = 0; i < 4; i++) p->a[i] *= n; }
static void randq(rng_t *R, q_t *q) { double s = 0; for (int i = 0; i < 4; i++) { q->a[i] = rng_gauss(R); s += q->a[i]*q->a[i]; } s = 1.0/sqrt(s); for (int i = 0; i < 4; i++) q->a[i] *= s; }
int main(int argc, char **argv) {
  if (argc < 12) { fprintf(stderr, "usage\n"); return 2; }
  int L = atoi(argv[1]); double bF = atof(argv[2]), bA = atof(argv[3]); long nsw = atol(argv[4]), nth = atol(argv[5]);
  uint64_t seed = strtoull(argv[6], 0, 10); int cold = atoi(argv[7]), hits = atoi(argv[8]), mode = atoi(argv[9]), mut = atoi(argv[10]);
  FILE *fo = fopen(argv[11], "wb"); if (!fo) return 3; int every = (argc > 12) ? atoi(argv[12]) : 1;
  double cA = mut ? 0.5 : (1.0/3.0); /* update-side adjoint normalisation; correct value 1/3 */
  /* adjoint term (update side): beta_A (1 - Tr_adj*cA) with Tr_adj = 4x^2-1: = beta_A(1 + cA - 4 cA x^2) */
  double kA = bA * 4.0 * cA; /* coefficient of -x^2 */
  rng_t R; rng_seed(&R, seed); lat_t lt; lat_init(&lt, L); int V = lt.V;
  q_t *U = (q_t *)malloc(sizeof(q_t) * 4 * V);
  for (int i = 0; i < 4 * V; i++) { if (cold) { U[i].a[0] = 1; U[i].a[1] = U[i].a[2] = U[i].a[3] = 0; } else randq(&R, &U[i]); }
  double eps = 0.5; double np = 6.0 * V;
  for (long sw = 0; sw < nsw; sw++) {
    long acc = 0, tot = 0;
    for (int s = 0; s < V; s++) for (int mu = 0; mu < 4; mu++) {
      int sp = lt.nbp[s * 4 + mu]; double W[4] = {0,0,0,0}; double M[4][4]; memset(M, 0, sizeof(M));
      for (int nu = 0; nu < 4; nu++) if (nu != mu) {
        int spn = lt.nbp[s * 4 + nu], smn = lt.nbm[s * 4 + nu];
        q_t v1 = qm(qm(U[sp * 4 + nu], qc(U[spn * 4 + mu])), qc(U[s * 4 + nu]));
        int spm = lt.nbm[sp * 4 + nu];
        q_t v2 = qm(qm(qc(U[spm * 4 + nu]), qc(U[smn * 4 + mu])), U[smn * 4 + nu]);
        q_t vs[2] = {v1, v2};
        for (int k = 0; k < 2; k++) {
          /* x = (1/2)Tr(U V) = u . conj(V) as 4-vectors */
          double w[4] = {vs[k].a[0], -vs[k].a[1], -vs[k].a[2], -vs[k].a[3]};
          for (int i = 0; i < 4; i++) { W[i] += w[i]; for (int j = 0; j < 4; j++) M[i][j] += w[i]*w[j]; }
        }
      }
      q_t u = U[s * 4 + mu];
      if (mode == 1 && bA == 0.0) { /* Creutz heat bath for pure fundamental */
        double k = sqrt(W[0]*W[0] + W[1]*W[1] + W[2]*W[2] + W[3]*W[3]); double al = bF * k;
        /* sample a0 in [-1,1] with density sqrt(1-a0^2) exp(al a0) */
        double a0;
        for (;;) { double r1 = 1.0 - rng_u(&R), r2 = 1.0 - rng_u(&R), r3 = rng_u(&R);
          double x = -(log(r1) + cos(6.283185307179586*r3)*cos(6.283185307179586*r3)*log(r2)) / al;
          double r4 = rng_u(&R); if (r4*r4 <= 1.0 - 0.5*x) { a0 = 1.0 - x; break; } }
        double sn = sqrt(1.0 - a0*a0), c = 2.0*rng_u(&R) - 1.0, ph = 6.283185307179586*rng_u(&R), st = sqrt(1.0 - c*c);
        /* new x-variable y = u . W/k = a0 ; build u_new as quaternion with u.What = a0; u = a0*What + sn*(perp) */
        double Wh[4] = {W[0]/k, W[1]/k, W[2]/k, W[3]/k};
        /* random unit perpendicular to Wh: gram-schmidt */
        double p[4]; for (int i = 0; i < 4; i++) p[i] = rng_gauss(&R);
        double d = 0; for (int i = 0; i < 4; i++) d += p[i]*Wh[i]; for (int i = 0; i < 4; i++) p[i] -= d*Wh[i];
        double n = 0; for (int i = 0; i < 4; i++) n += p[i]*p[i]; n = 1.0/sqrt(n);
        (void)c; (void)ph; (void)st;
        for (int i = 0; i < 4; i++) u.a[i] = a0*Wh[i] + sn*p[i]*n;
        qn(&u); U[s * 4 + mu] = u; continue;
      }
      /* Metropolis: S(u) = -bF u.W - (kA/4)*... : dS = -bF (u'-u).W - kA (u'^T M u' - u^T M u)/... ; adjoint per plaquette -kA x^2 => -kA u^T M u */
      double uv[4] = {u.a[0], u.a[1], u.a[2], u.a[3]};
      double Su; { double q = 0; for (int i = 0; i < 4; i++) for (int j = 0; j < 4; j++) q += uv[i]*M[i][j]*uv[j]; double l = 0; for (int i = 0; i < 4; i++) l += uv[i]*W[i]; Su = -bF*l - kA*q; }
      for (int h = 0; h < hits; h++) {
#ifdef ZFLIP
        if (h == hits - 1) { /* center-flip proposal U -> -U (an involution, so the proposal is symmetric): equilibrates the Z2 sector */
          double nv[4] = {-uv[0], -uv[1], -uv[2], -uv[3]};
          double q = 0; for (int i = 0; i < 4; i++) for (int j = 0; j < 4; j++) q += nv[i]*M[i][j]*nv[j]; double l = 0; for (int i = 0; i < 4; i++) l += nv[i]*W[i];
          double Sn = -bF*l - kA*q, dS = Sn - Su; tot++;
          if (dS <= 0 || rng_u(&R) < exp(-dS)) { for (int i = 0; i < 4; i++) { u.a[i] = nv[i]; uv[i] = nv[i]; } Su = Sn; acc++; }
          continue;
        }
#endif
        q_t r; { double al = eps * (2.0*rng_u(&R) - 1.0) * 3.141592653589793; double vv[3]; double n = 0; for (int i = 0; i < 3; i++) { vv[i] = rng_gauss(&R); n += vv[i]*vv[i]; } n = sin(al)/sqrt(n);
          r.a[0] = cos(al); for (int i = 0; i < 3; i++) r.a[i+1] = vv[i]*n; }
        q_t un = qm(r, u); qn(&un);
        double nv[4] = {un.a[0], un.a[1], un.a[2], un.a[3]};
        double Sn; { double q = 0; for (int i = 0; i < 4; i++) for (int j = 0; j < 4; j++) q += nv[i]*M[i][j]*nv[j]; double l = 0; for (int i = 0; i < 4; i++) l += nv[i]*W[i]; Sn = -bF*l - kA*q; }
        double dS = Sn - Su; tot++;
        if (dS <= 0 || rng_u(&R) < exp(-dS)) { u = un; for (int i = 0; i < 4; i++) uv[i] = nv[i]; Su = Sn; acc++; }
      }
      qn(&u); U[s * 4 + mu] = u;
    }
    if (sw < nth && tot > 0) { double a = (double)acc / tot; eps *= (a > 0.5) ? 1.03 : 0.97; if (eps > 1.0) eps = 1.0; if (eps < 0.02) eps = 0.02; }
    if (sw >= nth && ((sw - nth) % every == 0)) {
      double sx = 0, sa = 0;
      for (int s = 0; s < V; s++) for (int mu = 0; mu < 4; mu++) for (int nu = mu + 1; nu < 4; nu++) {
        int spm = lt.nbp[s * 4 + mu], spn = lt.nbp[s * 4 + nu];
        q_t P = qm(qm(U[s * 4 + mu], U[spm * 4 + nu]), qm(qc(U[spn * 4 + mu]), qc(U[s * 4 + nu])));
        double x = P.a[0]; sx += x; sa += (4.0*x*x - 1.0) / 3.0;
      }
      double o[2] = {sx / np, sa / np}; fwrite(o, sizeof(double), 2, fo);
    }
  }
  fclose(fo); fprintf(stderr, "su2 done L=%d bF=%g bA=%g eps=%g\n", L, bF, bA, eps); return 0;
}

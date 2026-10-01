/* B4 lane: SU(2) 4D fundamental-adjoint lattice gauge theory, flat-histogram (multicanonical, Wang-Landau built, then frozen) sampling.
   S = beta_F sum_p (1 - x_p) + beta_A sum_p (1 - Tr_adj/3), x_p = Tr U_p/2, Tr_adj = 4x^2 - 1.
   Sampled order variable O = A + bw*F, A = sum_p (4x^2-1)/3, F = sum_p x.   Weight exp(-S - W(O)).
   Link update = hits of: near-identity rotation (nhit of them), Metropolis-corrected reflection about the fundamental staple (refl=1), center flip U->-U (always last).
   keys (key=value): mode (0 canonical, 1 Wang-Landau build, 2 production) L bF bA seed cold nhit refl bw nth nsw every out
        mode 1: lo hi nb wlmax lnf_end flat_int flat_frac table(out)      mode 2: table(in) mut
   mode 0 / 2 output: float64 pairs per measurement (A, F) totals;  mode 1 output: the table file.  Summary on stderr. */
#include "muca.h"
typedef struct { double a[4]; } q_t;
static inline q_t qm(q_t p, q_t q) {
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
static double getd(int argc, char **argv, const char *k, double d) { size_t n = strlen(k); for (int i = 1; i < argc; i++) if (!strncmp(argv[i], k, n) && argv[i][n] == '=') return atof(argv[i] + n + 1); return d; }
static const char *gets_(int argc, char **argv, const char *k) { size_t n = strlen(k); for (int i = 1; i < argc; i++) if (!strncmp(argv[i], k, n) && argv[i][n] == '=') return argv[i] + n + 1; return NULL; }
static void totals(const lat_t *lt, const q_t *U, double *A, double *F) {
  double sx = 0, sa = 0; int V = lt->V;
  for (int s = 0; s < V; s++) for (int mu = 0; mu < 4; mu++) for (int nu = mu + 1; nu < 4; nu++) {
    int spm = lt->nbp[s * 4 + mu], spn = lt->nbp[s * 4 + nu];
    q_t P = qm(qm(U[s * 4 + mu], U[spm * 4 + nu]), qm(qc(U[spn * 4 + mu]), qc(U[s * 4 + nu])));
    double x = P.a[0]; sx += x; sa += (4.0*x*x - 1.0) / 3.0;
  }
  *A = sa; *F = sx;
}
int main(int argc, char **argv) {
  int mode = (int)getd(argc, argv, "mode", 0), L = (int)getd(argc, argv, "L", 4);
  double bF = getd(argc, argv, "bF", 0.0), bA = getd(argc, argv, "bA", 0.0), bw = getd(argc, argv, "bw", 0.0);
  uint64_t seed = (uint64_t)getd(argc, argv, "seed", 1); int cold = (int)getd(argc, argv, "cold", 0);
  int nhit = (int)getd(argc, argv, "nhit", 4), refl = (int)getd(argc, argv, "refl", 1), mut = (int)getd(argc, argv, "mut", 0);
  long nth = (long)getd(argc, argv, "nth", 1000), nsw = (long)getd(argc, argv, "nsw", 1000), every = (long)getd(argc, argv, "every", 1);
  const char *outf = gets_(argc, argv, "out"), *tabf = gets_(argc, argv, "table");
  double kA = bA * 4.0 / 3.0;
  rng_t R; rng_seed(&R, seed); lat_t lt; lat_init(&lt, L); int V = lt.V; double np = 6.0 * V;
  q_t *U = (q_t *)malloc(sizeof(q_t) * 4 * V);
  for (int i = 0; i < 4 * V; i++) { if (cold) { U[i].a[0] = 1; U[i].a[1] = U[i].a[2] = U[i].a[3] = 0; } else randq(&R, &U[i]); }
  double eps = 0.5;
  muca_t m; memset(&m, 0, sizeof(m)); long wlmax = 0, flat_int = 200; double lnf = 1.0, lnf_end = 1e-3, flat_frac = 0.5; int learn = 0; int tlo = 0, thi = 0;
  if (mode == 1) {
    mu_alloc(&m, (int)getd(argc, argv, "nb", 400), getd(argc, argv, "lo", 0), getd(argc, argv, "hi", 1));
    wlmax = (long)getd(argc, argv, "wlmax", 100000); lnf_end = getd(argc, argv, "lnf_end", 1e-3); flat_int = (long)getd(argc, argv, "flat_int", 200); flat_frac = getd(argc, argv, "flat_frac", 0.5);
    m.mode = 1;
  } else if (mode == 2) {
    if (!tabf || mu_load(&m, tabf, &eps)) { fprintf(stderr, "cannot load table\n"); return 3; }
    m.mode = 2; m.mut = mut;
  } else m.mode = 0;
  FILE *fo = NULL; if (mode != 1) { fo = fopen(outf, "wb"); if (!fo) return 3; }
  double A, F; totals(&lt, U, &A, &F); double Ocur = A + bw * F, Wc = 0; mu_W(&m, Ocur, &Wc); if (mu_bin(&m, Ocur) >= 0) m.inside = 1;
  long ntravers = 0; int side = 0; double zlo = m.lo + 0.15 * (m.hi - m.lo), zhi = m.hi - 0.15 * (m.hi - m.lo);
  double *Hp = (double *)calloc(m.nb > 0 ? m.nb : 1, sizeof(double)); long nrec = 0;
  long total = nth + (mode == 1 ? wlmax : nsw); long wl_sw = 0; int wl_done = 0; long nflat = 0;
  for (long sw = 0; sw < total; sw++) {
    int adapt = (sw < nth) && mode != 2;
    if (mode == 1 && sw == nth) learn = 1;
    long acc = 0, tot = 0;
    for (int s = 0; s < V; s++) for (int mu = 0; mu < 4; mu++) {
      int sp = lt.nbp[s * 4 + mu]; double W[4] = {0,0,0,0}; double M[4][4]; memset(M, 0, sizeof(M));
      for (int nu = 0; nu < 4; nu++) if (nu != mu) {
        int spn = lt.nbp[s * 4 + nu], smn = lt.nbm[s * 4 + nu];
        q_t v1 = qm(qm(U[sp * 4 + nu], qc(U[spn * 4 + mu])), qc(U[s * 4 + nu]));
        int spm = lt.nbm[sp * 4 + nu];
        q_t v2 = qm(qm(qc(U[spm * 4 + nu]), qc(U[smn * 4 + mu])), U[smn * 4 + nu]);
        q_t vs[2] = {v1, v2};
        for (int k = 0; k < 2; k++) { double w[4] = {vs[k].a[0], -vs[k].a[1], -vs[k].a[2], -vs[k].a[3]};
          for (int i = 0; i < 4; i++) { W[i] += w[i]; for (int j = 0; j < 4; j++) M[i][j] += w[i]*w[j]; } }
      }
      q_t u = U[s * 4 + mu]; double uv[4] = {u.a[0], u.a[1], u.a[2], u.a[3]};
      double l = 0, q = 0; for (int i = 0; i < 4; i++) { l += uv[i]*W[i]; for (int j = 0; j < 4; j++) q += uv[i]*M[i][j]*uv[j]; }
      double Wn2 = W[0]*W[0] + W[1]*W[1] + W[2]*W[2] + W[3]*W[3], Wn1 = sqrt(Wn2);
      int nprop = nhit + ((refl && Wn1 > 1e-9) ? 1 : 0) + 1;
      for (int h = 0; h < nprop; h++) {
        double nv[4]; int kind;   /* 0 near-identity, 1 reflection, 2 center flip */
        if (h < nhit) kind = 0; else if (h == nprop - 1) kind = 2; else kind = 1;
        if (kind == 0) {
          q_t r; double al = eps * (2.0*rng_u(&R) - 1.0) * 3.141592653589793; double vv[3]; double n = 0; for (int i = 0; i < 3; i++) { vv[i] = rng_gauss(&R); n += vv[i]*vv[i]; } n = sin(al)/sqrt(n);
          r.a[0] = cos(al); for (int i = 0; i < 3; i++) r.a[i+1] = vv[i]*n;
          q_t uu = {{uv[0], uv[1], uv[2], uv[3]}}; q_t un = qm(r, uu); qn(&un); for (int i = 0; i < 4; i++) nv[i] = un.a[i];
        } else if (kind == 1) {
          double d = 0; for (int i = 0; i < 4; i++) d += uv[i]*W[i]/Wn1; for (int i = 0; i < 4; i++) nv[i] = 2.0*d*W[i]/Wn1 - uv[i];
        } else { for (int i = 0; i < 4; i++) nv[i] = -uv[i]; }
        double ln = 0, qq = 0; for (int i = 0; i < 4; i++) { ln += nv[i]*W[i]; for (int j = 0; j < 4; j++) qq += nv[i]*M[i][j]*nv[j]; }
        double dS = -bF*(ln - l) - kA*(qq - q);
        double On = Ocur + (4.0/3.0)*(qq - q) + bw*(ln - l);
        double Wn; int ok = mu_W(&m, On, &Wn);
        if (kind == 0) tot++;
        if (!ok) continue;
        double dW = (m.mut) ? 0.0 : (Wn - Wc);
        double x = dS + dW;
        if (x <= 0 || rng_u(&R) < exp(-x)) { for (int i = 0; i < 4; i++) uv[i] = nv[i]; l = ln; q = qq; Ocur = On; Wc = Wn; if (kind == 0) acc++; if (!m.inside && mu_bin(&m, Ocur) >= 0) m.inside = 1; }
      }
      u.a[0] = uv[0]; u.a[1] = uv[1]; u.a[2] = uv[2]; u.a[3] = uv[3]; qn(&u); U[s * 4 + mu] = u;
      if (learn && m.inside) { int b = mu_bin(&m, Ocur); if (b >= 0) { m.lnG[b] += lnf / (4.0 * V); m.H[b] += 1.0; m.vst[b] = 1; if (Ocur < m.lo + 0.1 * (m.hi - m.lo)) tlo = 1; if (Ocur > m.hi - 0.1 * (m.hi - m.lo)) thi = 1; mu_W(&m, Ocur, &Wc); } }
    }
    if (adapt && tot > 0) { double a = (double)acc / tot; eps *= (a > 0.5) ? 1.03 : 0.97; if (eps > 1.0) eps = 1.0; if (eps < 0.02) eps = 0.02; }
    if (sw % 50 == 0) { totals(&lt, U, &A, &F); Ocur = A + bw * F; mu_W(&m, Ocur, &Wc); }
    if (mode == 1 && learn) {
      wl_sw++;
      if (wl_sw % flat_int == 0) {
        double mn = 1e300, mean = 0; int nv = 0; for (int b = 0; b < m.nb; b++) if (m.vst[b]) { if (m.H[b] < mn) mn = m.H[b]; mean += m.H[b]; nv++; } mean /= (nv > 0 ? nv : 1);
        if (mean > 0 && mn >= flat_frac * mean && tlo && thi) { lnf *= 0.5; nflat++; tlo = thi = 0; memset(m.H, 0, sizeof(double) * m.nb); if (lnf < lnf_end) { wl_done = 1; break; } }
      }
      continue;
    }
    if (mode != 1 && sw >= nth) {
      long k = sw - nth;
      if (k % every == 0) {
        totals(&lt, U, &A, &F); double o[2] = {A, F}; fwrite(o, sizeof(double), 2, fo); nrec++;
        if (mode == 2) { Ocur = A + bw * F; int b = mu_bin(&m, Ocur); if (b >= 0) Hp[b] += 1.0; int ns = (Ocur < zlo) ? -1 : (Ocur > zhi ? 1 : 0); if (ns != 0) { if (side != 0 && ns != side) ntravers++; side = ns; } }
      }
    }
  }
  if (mode == 1) { mu_save(&m, tabf, eps); fprintf(stderr, "su2m WL L=%d bF=%g bA=%g wl_sweeps=%ld lnf=%g nflat=%ld done=%d eps=%g\n", L, bF, bA, wl_sw, lnf, nflat, wl_done, eps); return 0; }
  fclose(fo);
  double mn = 1e300, mean = 0; for (int b = 0; b < m.nb; b++) { if (Hp[b] < mn) mn = Hp[b]; mean += Hp[b]; } if (m.nb > 0) mean /= m.nb;
  fprintf(stderr, "su2m mode=%d L=%d bF=%g bA=%g rec=%ld traversals=%ld flat_min/mean=%g eps=%g\n", mode, L, bF, bA, nrec, ntravers, mean > 0 ? mn / mean : 0.0, eps);
  return 0;
}

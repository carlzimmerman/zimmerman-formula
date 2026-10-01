/* B4 lane: SU(3) 4D fundamental-adjoint lattice gauge theory, flat-histogram (multicanonical, Wang-Landau built, then frozen) sampling.
   S = beta_F sum_p (1 - ReTr U_p/3) + beta_A sum_p (1 - Tr_adj/8), Tr_adj = |Tr U|^2 - 1.  O = A + bw*F, A = sum_p (|Tr|^2-1)/8, F = sum_p ReTr/3.  Weight exp(-S - W(O)).
   Link update: nhit near-identity multiplications from a fixed pool closed under inversion (width eps, frozen after the thermalisation stage) and a center-flip U -> omega^{+-1} U last.
   (no overrelaxation for SU(3) in this version: disclosed.)   keys as su2m.c */
#include "muca.h"
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

static double getd(int argc, char **argv, const char *k, double d) { size_t n = strlen(k); for (int i = 1; i < argc; i++) if (!strncmp(argv[i], k, n) && argv[i][n] == '=') return atof(argv[i] + n + 1); return d; }
static const char *gets_(int argc, char **argv, const char *k) { size_t n = strlen(k); for (int i = 1; i < argc; i++) if (!strncmp(argv[i], k, n) && argv[i][n] == '=') return argv[i] + n + 1; return NULL; }
static void plaq_tr(const lat_t *lt, const m3 *U, int s, int mu, int nu, double *tr, double *ti) {
  int spm = lt->nbp[s * 4 + mu], spn = lt->nbp[s * 4 + nu]; m3 a, b, c, d;
  mm(&U[s * 4 + mu], &U[spm * 4 + nu], &a); dag(&U[spn * 4 + mu], &b); dag(&U[s * 4 + nu], &c); mm(&b, &c, &d);
  double r = 0, i = 0; for (int x = 0; x < 3; x++) for (int y = 0; y < 3; y++) { r += a.r[x*3+y]*d.r[y*3+x] - a.i[x*3+y]*d.i[y*3+x]; i += a.r[x*3+y]*d.i[y*3+x] + a.i[x*3+y]*d.r[y*3+x]; }
  *tr = r; *ti = i;
}
static void totals(const lat_t *lt, const m3 *U, double *A, double *F) {
  double sx = 0, sa = 0;
  for (int s = 0; s < lt->V; s++) for (int mu = 0; mu < 4; mu++) for (int nu = mu + 1; nu < 4; nu++) { double tr, ti; plaq_tr(lt, U, s, mu, nu, &tr, &ti); sx += tr / 3.0; sa += (tr*tr + ti*ti - 1.0) / 8.0; }
  *A = sa; *F = sx;
}
int main(int argc, char **argv) {
  int mode = (int)getd(argc, argv, "mode", 0), L = (int)getd(argc, argv, "L", 4);
  double bF = getd(argc, argv, "bF", 0.0), bA = getd(argc, argv, "bA", 0.0), bw = getd(argc, argv, "bw", 0.0);
  uint64_t seed = (uint64_t)getd(argc, argv, "seed", 1); int cold = (int)getd(argc, argv, "cold", 0);
  int nhit = (int)getd(argc, argv, "nhit", 4), mut = (int)getd(argc, argv, "mut", 0);
  long nth = (long)getd(argc, argv, "nth", 1000), nsw = (long)getd(argc, argv, "nsw", 1000), every = (long)getd(argc, argv, "every", 1);
  const char *outf = gets_(argc, argv, "out"), *tabf = gets_(argc, argv, "table");
  rng_t R; rng_seed(&R, seed); lat_t lt; lat_init(&lt, L); int V = lt.V;
  m3 *U = (m3 *)malloc(sizeof(m3) * 4 * V);
  for (int i = 0; i < 4 * V; i++) { if (cold) ident(&U[i]); else { m3 t; ident(&t); for (int k = 0; k < 6; k++) { m3 r, c; rand_su3(&R, 1.0, &r); mm(&r, &t, &c); t = c; } reunit(&t); U[i] = t; } }
  double eps = 0.25; const int NP = 100; m3 pool[200]; int pool_built = 0;
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
    if (adapt || !pool_built) { for (int k = 0; k < NP; k++) { rand_su3(&R, eps, &pool[2*k]); dag(&pool[2*k], &pool[2*k+1]); } pool_built = 1; }
    long acc = 0, tot = 0;
    for (int s = 0; s < V; s++) for (int mu = 0; mu < 4; mu++) {
      int sp = lt.nbp[s * 4 + mu]; m3 St[6]; int ns = 0;
      for (int nu = 0; nu < 4; nu++) if (nu != mu) {
        int spn = lt.nbp[s * 4 + nu], smn = lt.nbm[s * 4 + nu];
        m3 a, b, c;
        dag(&U[spn * 4 + mu], &a); mm(&U[sp * 4 + nu], &a, &b); dag(&U[s * 4 + nu], &c); mm(&b, &c, &St[ns++]);
        int spm = lt.nbm[sp * 4 + nu];
        dag(&U[spm * 4 + nu], &a); dag(&U[smn * 4 + mu], &b); mm(&a, &b, &c); mm(&c, &U[smn * 4 + nu], &St[ns++]);
      }
      m3 u = U[s * 4 + mu];
      /* sums over the 6 plaquettes: SF = sum Re Tr(u St)/3 ; SA = sum |Tr(u St)|^2/8 */
      double SF = 0, SA = 0;
      for (int i = 0; i < 6; i++) { double tr = 0, ti = 0; for (int x = 0; x < 3; x++) for (int y = 0; y < 3; y++) { tr += u.r[x*3+y]*St[i].r[y*3+x] - u.i[x*3+y]*St[i].i[y*3+x]; ti += u.r[x*3+y]*St[i].i[y*3+x] + u.i[x*3+y]*St[i].r[y*3+x]; } SF += tr / 3.0; SA += (tr*tr + ti*ti) / 8.0; }
      int nprop = nhit + 1;
      for (int h = 0; h < nprop; h++) {
        m3 un;
        if (h == nprop - 1) { double sn = (rng_u(&R) < 0.5) ? 0.8660254037844386 : -0.8660254037844386; for (int k = 0; k < 9; k++) { un.r[k] = -0.5 * u.r[k] - sn * u.i[k]; un.i[k] = -0.5 * u.i[k] + sn * u.r[k]; } }
        else mm(&pool[(int)(rng_u(&R) * 2 * NP)], &u, &un);
        double nF = 0, nA = 0;
        for (int i = 0; i < 6; i++) { double tr = 0, ti = 0; for (int x = 0; x < 3; x++) for (int y = 0; y < 3; y++) { tr += un.r[x*3+y]*St[i].r[y*3+x] - un.i[x*3+y]*St[i].i[y*3+x]; ti += un.r[x*3+y]*St[i].i[y*3+x] + un.i[x*3+y]*St[i].r[y*3+x]; } nF += tr / 3.0; nA += (tr*tr + ti*ti) / 8.0; }
        double dS = -bF*(nF - SF) - bA*(nA - SA);
        double On = Ocur + (nA - SA) + bw*(nF - SF);
        double Wn; int ok = mu_W(&m, On, &Wn);
        if (h < nhit) tot++;
        if (!ok) continue;
        double dW = (m.mut) ? 0.0 : (Wn - Wc);
        double x = dS + dW;
        if (x <= 0 || rng_u(&R) < exp(-x)) { u = un; SF = nF; SA = nA; Ocur = On; Wc = Wn; if (h < nhit) acc++; if (!m.inside && mu_bin(&m, Ocur) >= 0) m.inside = 1; }
      }
      reunit(&u); U[s * 4 + mu] = u;
      if (learn && m.inside) { int b = mu_bin(&m, Ocur); if (b >= 0) { m.lnG[b] += lnf / (4.0 * V); m.H[b] += 1.0; m.vst[b] = 1; if (Ocur < m.lo + 0.1 * (m.hi - m.lo)) tlo = 1; if (Ocur > m.hi - 0.1 * (m.hi - m.lo)) thi = 1; mu_W(&m, Ocur, &Wc); } }
    }
    if (adapt && tot > 0) { double a = (double)acc / tot; eps *= (a > 0.5) ? 1.05 : 0.95; if (eps > 1.0) eps = 1.0; if (eps < 0.02) eps = 0.02; }
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
  if (mode == 1) { mu_save(&m, tabf, eps); fprintf(stderr, "su3m WL L=%d bF=%g bA=%g wl_sweeps=%ld lnf=%g nflat=%ld done=%d eps=%g\n", L, bF, bA, wl_sw, lnf, nflat, wl_done, eps); return 0; }
  fclose(fo);
  double mn = 1e300, mean = 0; for (int b = 0; b < m.nb; b++) { if (Hp[b] < mn) mn = Hp[b]; mean += Hp[b]; } if (m.nb > 0) mean /= m.nb;
  fprintf(stderr, "su3m mode=%d L=%d bF=%g bA=%g rec=%ld traversals=%ld flat_min/mean=%g eps=%g\n", mode, L, bF, bA, nrec, ntravers, mean > 0 ? mn / mean : 0.0, eps);
  return 0;
}

/* B4 lane: 2D q-state Potts model, flat-histogram sampling of N = number of aligned nearest-neighbour bonds (weight exp(beta N - W(N))).
   Used ONLY as the exactly-known first-order check of the machinery (beta_c = ln(1+sqrt(q)) for q > 4).  keys as su2m.c plus q, beta. */
#include "muca.h"
static double getd(int argc, char **argv, const char *k, double d) { size_t n = strlen(k); for (int i = 1; i < argc; i++) if (!strncmp(argv[i], k, n) && argv[i][n] == '=') return atof(argv[i] + n + 1); return d; }
static const char *gets_(int argc, char **argv, const char *k) { size_t n = strlen(k); for (int i = 1; i < argc; i++) if (!strncmp(argv[i], k, n) && argv[i][n] == '=') return argv[i] + n + 1; return NULL; }
int main(int argc, char **argv) {
  int mode = (int)getd(argc, argv, "mode", 0), L = (int)getd(argc, argv, "L", 12), q = (int)getd(argc, argv, "q", 20);
  double beta = getd(argc, argv, "beta", 1.7); uint64_t seed = (uint64_t)getd(argc, argv, "seed", 1); int cold = (int)getd(argc, argv, "cold", 0), mut = (int)getd(argc, argv, "mut", 0);
  long nth = (long)getd(argc, argv, "nth", 1000), nsw = (long)getd(argc, argv, "nsw", 1000), every = (long)getd(argc, argv, "every", 1);
  const char *outf = gets_(argc, argv, "out"), *tabf = gets_(argc, argv, "table");
  int V = L * L; rng_t R; rng_seed(&R, seed);
  int *sp = (int *)malloc(sizeof(int) * V), *nb4 = (int *)malloc(sizeof(int) * V * 4);
  for (int y = 0; y < L; y++) for (int x = 0; x < L; x++) { int s = y * L + x; nb4[s*4+0] = y*L + (x+1)%L; nb4[s*4+1] = y*L + (x+L-1)%L; nb4[s*4+2] = ((y+1)%L)*L + x; nb4[s*4+3] = ((y+L-1)%L)*L + x; }
  for (int s = 0; s < V; s++) sp[s] = cold ? 0 : (int)(rng_u(&R) * q);
  muca_t m; memset(&m, 0, sizeof(m)); long wlmax = 0, flat_int = 200; double lnf = 1.0, lnf_end = 1e-3, flat_frac = 0.5; int learn = 0, wl_done = 0, tlo = 0, thi = 0; long nflat = 0, wl_sw = 0; double eps = 0;
  if (mode == 1) { mu_alloc(&m, (int)getd(argc, argv, "nb", 400), getd(argc, argv, "lo", 0), getd(argc, argv, "hi", 1)); wlmax = (long)getd(argc, argv, "wlmax", 100000); lnf_end = getd(argc, argv, "lnf_end", 1e-3); flat_int = (long)getd(argc, argv, "flat_int", 200); flat_frac = getd(argc, argv, "flat_frac", 0.5); m.mode = 1; }
  else if (mode == 2) { if (!tabf || mu_load(&m, tabf, &eps)) return 3; m.mode = 2; m.mut = mut; } else m.mode = 0;
  FILE *fo = NULL; if (mode != 1) { fo = fopen(outf, "wb"); if (!fo) return 3; }
  double Ocur = 0; for (int s = 0; s < V; s++) { if (sp[nb4[s*4]] == sp[s]) Ocur += 1; if (sp[nb4[s*4+2]] == sp[s]) Ocur += 1; }
  double Wc = 0; mu_W(&m, Ocur, &Wc); if (mu_bin(&m, Ocur) >= 0) m.inside = 1;
  long ntravers = 0; int side = 0; double zlo = m.lo + 0.15 * (m.hi - m.lo), zhi = m.hi - 0.15 * (m.hi - m.lo); double *Hp = (double *)calloc(m.nb > 0 ? m.nb : 1, sizeof(double)); long nrec = 0;
  long total = nth + (mode == 1 ? wlmax : nsw);
  for (long sw = 0; sw < total; sw++) {
    if (mode == 1 && sw == nth) learn = 1;
    for (int k = 0; k < V; k++) {
      int s = (int)(rng_u(&R) * V); int old = sp[s]; int nw = (int)(rng_u(&R) * (q - 1)); if (nw >= old) nw++;
      int d = 0; for (int j = 0; j < 4; j++) { int t = sp[nb4[s*4+j]]; if (t == nw) d++; if (t == old) d--; }
      double On = Ocur + d, Wn; int ok = mu_W(&m, On, &Wn);
      if (ok) { double x = -beta * d + (m.mut ? 0.0 : (Wn - Wc)); if (x <= 0 || rng_u(&R) < exp(-x)) { sp[s] = nw; Ocur = On; Wc = Wn; if (!m.inside && mu_bin(&m, Ocur) >= 0) m.inside = 1; } }
      if (learn && m.inside) { int b = mu_bin(&m, Ocur); if (b >= 0) { m.lnG[b] += lnf / ((double)V); m.H[b] += 1.0; m.vst[b] = 1; if (Ocur < m.lo + 0.1 * (m.hi - m.lo)) tlo = 1; if (Ocur > m.hi - 0.1 * (m.hi - m.lo)) thi = 1; mu_W(&m, Ocur, &Wc); } }
    }
    if (mode == 1 && learn) { wl_sw++; if (wl_sw % flat_int == 0) { double mn = 1e300, mean = 0; int nv = 0; for (int b = 0; b < m.nb; b++) if (m.vst[b]) { if (m.H[b] < mn) mn = m.H[b]; mean += m.H[b]; nv++; } mean /= (nv > 0 ? nv : 1);
        if (mean > 0 && mn >= flat_frac * mean && tlo && thi) { lnf *= 0.5; nflat++; tlo = thi = 0; memset(m.H, 0, sizeof(double) * m.nb); if (lnf < lnf_end) { wl_done = 1; break; } } } continue; }
    if (mode != 1 && sw >= nth && ((sw - nth) % every == 0)) { double o[2] = {Ocur, 0.0}; fwrite(o, sizeof(double), 2, fo); nrec++;
      if (mode == 2) { int b = mu_bin(&m, Ocur); if (b >= 0) Hp[b] += 1.0; int ns = (Ocur < zlo) ? -1 : (Ocur > zhi ? 1 : 0); if (ns != 0) { if (side != 0 && ns != side) ntravers++; side = ns; } } }
  }
  if (mode == 1) { mu_save(&m, tabf, 0.0); fprintf(stderr, "potts WL L=%d q=%d wl_sweeps=%ld lnf=%g nflat=%ld done=%d\n", L, q, wl_sw, lnf, nflat, wl_done); return 0; }
  fclose(fo); double mn = 1e300, mean = 0; for (int b = 0; b < m.nb; b++) { if (Hp[b] < mn) mn = Hp[b]; mean += Hp[b]; } if (m.nb > 0) mean /= m.nb;
  fprintf(stderr, "potts mode=%d L=%d q=%d beta=%g rec=%ld traversals=%ld flat_min/mean=%g\n", mode, L, q, beta, nrec, ntravers, mean > 0 ? mn / mean : 0.0); return 0;
}

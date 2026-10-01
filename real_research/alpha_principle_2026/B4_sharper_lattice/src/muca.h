/* B4 lane: flat-histogram helper shared by the gauge programs and the Potts check.
   Sampled weight exp(-S - W(O)); O = the total of the chosen order variable, W = piecewise-constant table lnG over nb bins on [lo,hi].
   mode 0 canonical (W = 0), mode 1 Wang-Landau (W = lnG, updated), mode 2 production (W = frozen lnG).
   mut = 1: the acceptance ignores the W-difference in production (detailed balance of the flat-histogram chain violated): CONTROL ONLY. */
#ifndef B4_MUCA_H
#define B4_MUCA_H
#include "b4_common.h"
typedef struct {
  int mode, nb, mut; double lo, hi, dw, ramp; double *lnG; double *H; char *vst;
  int inside;      /* set once the configuration has entered [lo,hi]; afterwards moves leaving the range are rejected */
} muca_t;
static void mu_alloc(muca_t *m, int nb, double lo, double hi) {
  m->nb = nb; m->lo = lo; m->hi = hi; m->dw = (hi - lo) / nb; m->ramp = 2.0; m->inside = 0;
  m->lnG = (double *)calloc(nb, sizeof(double)); m->H = (double *)calloc(nb, sizeof(double)); m->vst = (char *)calloc(nb, 1);
}
/* returns 0 if the move to O must be rejected, else sets *W */
static inline int mu_W(const muca_t *m, double O, double *W) {
  if (m->mode == 0) { *W = 0.0; return 1; }
  double t = (O - m->lo) / m->dw;
  if (t >= 0 && t < m->nb) { *W = m->lnG[(int)t]; return 1; }
  if (m->inside) return 0;
  double d = (t < 0) ? -t : (t - m->nb); int e = (t < 0) ? 0 : m->nb - 1;
  *W = m->lnG[e] + m->ramp * d; return 1;
}
static inline int mu_bin(const muca_t *m, double O) { double t = (O - m->lo) / m->dw; if (t >= 0 && t < m->nb) return (int)t; return -1; }
/* weight-table file: doubles [eps, lo, hi, nb, lnG[0..nb-1]] */
static int mu_save(const muca_t *m, const char *fn, double eps) {
  FILE *f = fopen(fn, "wb"); if (!f) return 1; double h[4] = {eps, m->lo, m->hi, (double)m->nb};
  fwrite(h, sizeof(double), 4, f); fwrite(m->lnG, sizeof(double), m->nb, f); fclose(f); return 0;
}
static int mu_load(muca_t *m, const char *fn, double *eps) {
  FILE *f = fopen(fn, "rb"); if (!f) return 1; double h[4]; if (fread(h, sizeof(double), 4, f) != 4) return 2;
  mu_alloc(m, (int)h[3], h[1], h[2]); *eps = h[0];
  if (fread(m->lnG, sizeof(double), m->nb, f) != (size_t)m->nb) return 3; fclose(f); return 0;
}
#endif

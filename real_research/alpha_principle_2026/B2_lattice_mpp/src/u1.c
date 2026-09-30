/* B2 lane: compact U(1) 4D lattice gauge theory, Wilson (action 0) or Villain (action 1), Metropolis multi-hit.
   usage: u1 L beta nsweep ntherm seed start(0 hot,1 cold) action hits mutate outfile
   output: binary float64 pairs per measured sweep: (mean cos theta_p, mean action density per plaquette)
   Wilson S = -beta sum cos(theta_p);  Villain S = sum -ln sum_{n=-1,0,1} exp(-(beta/2)(theta_p+2 pi n)^2)
   mutate=1: accepts with min(1, exp(-dS/2)) (wrong rule, control only) */
#include "b2_common.h"
static double sv(double a, double beta) {
  double e0 = exp(-0.5 * beta * a * a), t1 = a + 6.283185307179586, t2 = a - 6.283185307179586;
  return -log(e0 + exp(-0.5 * beta * t1 * t1) + exp(-0.5 * beta * t2 * t2));
}
int main(int argc, char **argv) {
  if (argc < 11) { fprintf(stderr, "usage\n"); return 2; }
  int L = atoi(argv[1]); double beta = atof(argv[2]); long nsw = atol(argv[3]), nth = atol(argv[4]);
  uint64_t seed = strtoull(argv[5], 0, 10); int cold = atoi(argv[6]), act = atoi(argv[7]), hits = atoi(argv[8]), mut = atoi(argv[9]);
  FILE *fo = fopen(argv[10], "wb"); if (!fo) return 3;
  rng_t R; rng_seed(&R, seed); lat_t lt; lat_init(&lt, L); int V = lt.V;
  double *cx = (double *)malloc(sizeof(double) * 4 * V), *cy = (double *)malloc(sizeof(double) * 4 * V);
  for (int i = 0; i < 4 * V; i++) { double th = cold ? 0.0 : 6.283185307179586 * rng_u(&R); cx[i] = cos(th); cy[i] = sin(th); }
  double w = 1.0; double np = 6.0 * V;
  for (long sw = 0; sw < nsw; sw++) {
    long acc = 0, tot = 0;
    for (int s = 0; s < V; s++) for (int mu = 0; mu < 4; mu++) {
      double zx[12], zy[12]; int nz = 0; double Zx = 0, Zy = 0;
      int sp = lt.nbp[s * 4 + mu];
      for (int nu = 0; nu < 4; nu++) if (nu != mu) {
        int spn = lt.nbp[s * 4 + nu], smn = lt.nbm[s * 4 + nu];
        /* forward: U_nu(s+mu) conj(U_mu(s+nu)) conj(U_nu(s)) */
        double ax = cx[sp * 4 + nu], ay = cy[sp * 4 + nu];
        double bx = cx[spn * 4 + mu], by = -cy[spn * 4 + mu];
        double px = ax * bx - ay * by, py = ax * by + ay * bx;
        double dx = cx[s * 4 + nu], dy = -cy[s * 4 + nu];
        double ex = px * dx - py * dy, ey = px * dy + py * dx;
        zx[nz] = ex; zy[nz] = ey; nz++; Zx += ex; Zy += ey;
        /* backward: conj(U_nu(s+mu-nu)) conj(U_mu(s-nu)) U_nu(s-nu) */
        int spm = lt.nbm[sp * 4 + nu];
        ax = cx[spm * 4 + nu]; ay = -cy[spm * 4 + nu];
        bx = cx[smn * 4 + mu]; by = -cy[smn * 4 + mu];
        px = ax * bx - ay * by; py = ax * by + ay * bx;
        dx = cx[smn * 4 + nu]; dy = cy[smn * 4 + nu];
        ex = px * dx - py * dy; ey = px * dy + py * dx;
        zx[nz] = ex; zy[nz] = ey; nz++; Zx += ex; Zy += ey;
      }
      double ux = cx[s * 4 + mu], uy = cy[s * 4 + mu];
      for (int h = 0; h < hits; h++) {
        double d = w * (2.0 * rng_u(&R) - 1.0), cd = cos(d), sd = sin(d);
        double nx = ux * cd - uy * sd, ny = ux * sd + uy * cd; double dS;
        if (act == 0) dS = -beta * ((nx - ux) * Zx - (ny - uy) * Zy);
        else {
          dS = 0;
          for (int i = 0; i < 12; i++) {
            double ao = atan2(uy * zx[i] + ux * zy[i], ux * zx[i] - uy * zy[i]);
            double an = atan2(ny * zx[i] + nx * zy[i], nx * zx[i] - ny * zy[i]);
            dS += sv(an, beta) - sv(ao, beta);
          }
        }
        if (mut) dS *= 0.5;
        tot++;
        if (dS <= 0 || rng_u(&R) < exp(-dS)) { ux = nx; uy = ny; acc++; }
      }
      double nrm = 1.0 / sqrt(ux * ux + uy * uy); cx[s * 4 + mu] = ux * nrm; cy[s * 4 + mu] = uy * nrm;
    }
    if (sw < nth) { double a = (double)acc / tot; w *= (a > 0.5) ? 1.03 : 0.97; if (w > 3.1) w = 3.1; if (w < 0.02) w = 0.02; }
    if (sw >= nth) {
      double sc = 0, sa = 0;
      for (int s = 0; s < V; s++) for (int mu = 0; mu < 4; mu++) for (int nu = mu + 1; nu < 4; nu++) {
        int spm = lt.nbp[s * 4 + mu], spn = lt.nbp[s * 4 + nu];
        double ax = cx[s * 4 + mu], ay = cy[s * 4 + mu];
        double bx = cx[spm * 4 + nu], by = cy[spm * 4 + nu];
        double px = ax * bx - ay * by, py = ax * by + ay * bx;
        double cxx = cx[spn * 4 + mu], cyy = -cy[spn * 4 + mu];
        double qx = px * cxx - py * cyy, qy = px * cyy + py * cxx;
        double dx = cx[s * 4 + nu], dy = -cy[s * 4 + nu];
        double rx = qx * dx - qy * dy, ry = qx * dy + qy * dx;
        sc += rx; sa += (act == 0) ? -rx : sv(atan2(ry, rx), beta);
      }
      double o[2] = {sc / np, sa / np}; fwrite(o, sizeof(double), 2, fo);
    }
  }
  fclose(fo); fprintf(stderr, "u1 done L=%d beta=%g w=%g\n", L, beta, w); return 0;
}

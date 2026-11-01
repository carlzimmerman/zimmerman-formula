/* HB1: spherical hydrostatic barotrope in a fixed baryon mass profile, scaled units, no G.
   dH/dx = -(m + mb)/(4 x^2), dm/dx = 4 x^2 rho(H). RK4 in t = ln x. Shoot on H_c so m(xe) = mt.
   kappa = 1/2 FITTED, unused; not theory closed. */
#include <math.h>
#include <stdlib.h>
typedef struct { int n; double dH; const double *tab; double Htop, rtop, slope; int ext; double wall; } Eos;
static int wallhit;
static inline double rho(const Eos *e, double H) {
    if (H <= 0.0) return 0.0;
    if (H < e->Htop) { double u = H / e->dH; int i = (int)u; if (i >= e->n - 1) i = e->n - 2; double w = u - i; return e->tab[i] * (1 - w) + e->tab[i + 1] * w; }
    double d = H - e->Htop;
    if (e->ext == 1) return e->rtop + e->slope * d;                    /* C1 tangent */
    if (e->ext == 3) { double a = e->slope / e->rtop * d; if (a > 500) { a = 500; wallhit = 1; } return e->rtop * exp(a); }  /* isothermal */
    wallhit = 1; return e->wall;                                       /* analytic wall */
}
/* integrate; returns m(xe). If out != NULL fills m on grid (m[i] for x[i] <= xe, m_e beyond); Hout likewise */
static double shoot(int n, const double *x, const double *mb, double xe, double Hc, const Eos *e, int nsub, double *out, double *Hout) {
    double xs = x[0] * 0.01, b = mb[0] / (x[0] * x[0]);
    double r0 = rho(e, Hc), H = Hc - b * xs / 4.0 - r0 * xs * xs / 6.0, m = 4.0 / 3.0 * r0 * xs * xs * xs;
    /* inner piece, mb = b x^2 */
    int ns = 40; double t = log(xs), dt = (log(x[0]) - t) / ns;
    for (int k = 0; k < ns; k++) {
        double X = exp(t), Xh = exp(t + 0.5 * dt), Xe = exp(t + dt);
        double r1 = rho(e, H), k1H = -(m + b * X * X) / (4 * X), k1m = 4 * X * X * X * r1;
        double H2 = H + 0.5 * dt * k1H, m2 = m + 0.5 * dt * k1m, k2H = -(m2 + b * Xh * Xh) / (4 * Xh), k2m = 4 * Xh * Xh * Xh * rho(e, H2);
        double H3 = H + 0.5 * dt * k2H, m3 = m + 0.5 * dt * k2m, k3H = -(m3 + b * Xh * Xh) / (4 * Xh), k3m = 4 * Xh * Xh * Xh * rho(e, H3);
        double H4 = H + dt * k3H, m4 = m + dt * k3m, k4H = -(m4 + b * Xe * Xe) / (4 * Xe), k4m = 4 * Xe * Xe * Xe * rho(e, H4);
        H += dt / 6 * (k1H + 2 * k2H + 2 * k3H + k4H); m += dt / 6 * (k1m + 2 * k2m + 2 * k3m + k4m); t += dt;
    }
    if (out) { out[0] = m; if (Hout) Hout[0] = H; }
    int last = 0;
    for (int i = 0; i < n - 1; i++) {
        double xa = x[i], xb = x[i + 1]; int done = 0;
        if (xb >= xe) { xb = xe; done = 1; }
        if (xb > xa) {
            double ta = log(xa), tb = log(xb), lx = log(x[i + 1]) - ta, h = (tb - ta) / nsub, ma = mb[i], dm_ = (mb[i + 1] - mb[i]) / lx;
            for (int k = 0; k < nsub; k++) {
                double tt = ta + k * h, Xa = exp(tt), Xh = exp(tt + 0.5 * h), Xe = exp(tt + h);
                double ba = ma + dm_ * (tt - ta), bh = ba + dm_ * 0.5 * h, be = ba + dm_ * h;
                double k1H = -(m + ba) / (4 * Xa), k1m = 4 * Xa * Xa * Xa * rho(e, H);
                double H2 = H + 0.5 * h * k1H, m2 = m + 0.5 * h * k1m, k2H = -(m2 + bh) / (4 * Xh), k2m = 4 * Xh * Xh * Xh * rho(e, H2);
                double H3 = H + 0.5 * h * k2H, m3 = m + 0.5 * h * k2m, k3H = -(m3 + bh) / (4 * Xh), k3m = 4 * Xh * Xh * Xh * rho(e, H3);
                double H4 = H + h * k3H, m4 = m + h * k3m, k4H = -(m4 + be) / (4 * Xe), k4m = 4 * Xe * Xe * Xe * rho(e, H4);
                H += h / 6 * (k1H + 2 * k2H + 2 * k3H + k4H); m += h / 6 * (k1m + 2 * k2m + 2 * k3m + k4m);
            }
        }
        if (out && !done) { out[i + 1] = m; if (Hout) Hout[i + 1] = H; last = i + 1; }
        if (done) { if (out) { for (int j = i + 1; j < n; j++) { out[j] = m; if (Hout) Hout[j] = H; } } return m; }
    }
    (void)last; return m;
}
double hb_mass(int n, const double *x, const double *mb, double xe, double Hc, int tn, double dH, const double *tab, double Htop, double rtop, double slope, int ext, double wall, int nsub) {
    Eos e = { tn, dH, tab, Htop, rtop, slope, ext, wall }; return shoot(n, x, mb, xe, Hc, &e, nsub, NULL, NULL);
}
/* returns H_c; status: 0 ok, 1 no root, 2 wall touched at the root. branch: 0 nearest Href in ln H_c, 1 lowest, 2 highest (scan 1e-3 Href to 3e3 Href). nroots: sign changes seen by the wide scan (branch > 0) */
double hb_solve(int n, const double *x, const double *mb, double xe, double mt, double Href, int tn, double dH, const double *tab, double Htop, double rtop, double slope, int ext, double wall, int nsub, double *out, double *Hout, int *status, int *nshots, int branch, int *nroots) {
    Eos e = { tn, dH, tab, Htop, rtop, slope, ext, wall }; *nshots = 0; wallhit = 0; *nroots = -1;
    double a = 0, b = 0, fa = 0, fb = 0; int ok = 0; const double g = 1.02;
    if (branch == 0) {
        double fr = shoot(n, x, mb, xe, Href, &e, nsub, NULL, NULL) / mt - 1; (*nshots)++;
        if (fabs(fr) < 1e-7) { a = b = Href; ok = 2; }
        else {
            double up = Href, dn = Href, fu = fr, fd = fr;
            for (int k = 0; k < 700 && !ok; k++) {
                double u2 = up * g, fu2 = shoot(n, x, mb, xe, u2, &e, nsub, NULL, NULL) / mt - 1; (*nshots)++;
                if (fu * fu2 <= 0) { a = up; b = u2; fa = fu; fb = fu2; ok = 1; break; }
                up = u2; fu = fu2;
                double d2 = dn / g, fd2 = shoot(n, x, mb, xe, d2, &e, nsub, NULL, NULL) / mt - 1; (*nshots)++;
                if (fd * fd2 <= 0) { a = d2; b = dn; fa = fd2; fb = fd; ok = 1; break; }
                dn = d2; fd = fd2;
            }
        }
    } else {
        double h = Href * 1e-3, f0 = shoot(n, x, mb, xe, h, &e, nsub, NULL, NULL) / mt - 1; int nr = 0; (*nshots)++;
        while (h < Href * 3e3) {
            double h2 = h * g, f2 = shoot(n, x, mb, xe, h2, &e, nsub, NULL, NULL) / mt - 1; (*nshots)++;
            if (f0 * f2 <= 0) { nr++; if (branch == 2 || !ok) { a = h; b = h2; fa = f0; fb = f2; ok = 1; } }
            h = h2; f0 = f2;
        }
        *nroots = nr;
    }
    if (!ok) { *status = 1; return NAN; }
    double c = a;
    if (ok == 1) {   /* Illinois */
        for (int it = 0; it < 80; it++) {
            c = (a * fb - b * fa) / (fb - fa); if (!(c > a && c < b)) c = 0.5 * (a + b);
            double fc = shoot(n, x, mb, xe, c, &e, nsub, NULL, NULL) / mt - 1; (*nshots)++;
            if (fabs(fc) < 1e-10 || (b - a) < 1e-13 * b) break;
            if (fc * fb < 0) { a = b; fa = fb; } else fa *= 0.5;
            b = c; fb = fc; if (a > b) { double t = a; a = b; b = t; t = fa; fa = fb; fb = t; }
        }
    }
    wallhit = 0; shoot(n, x, mb, xe, c, &e, nsub, out, Hout); *status = wallhit ? 2 : 0; return c;
}

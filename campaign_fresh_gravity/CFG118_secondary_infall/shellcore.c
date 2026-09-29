/*
 * shellcore.c -- the integrator of lane CFG118 (door 6: spherical secondary infall of cold shells onto a static baryon core).
 * Compiled at run time by CFG118_secondary_infall.py (into a temporary directory) and called through ctypes.
 *
 * A 1-D spherical Lagrangian shell code in physical coordinates.  Shell i feels
 *
 *     a_i = -G [M_core(<r_i) + M_c(<r_i)] / r_i^2  -  (f_sm H0^2 / 2) a(t)^-3 r_i  +  Omega_L H0^2 r_i  +  j_i^2 / r_i^3
 *
 *   M_c(<r_i) = m (n_i + 1/2): n_i = number of other shells inside r_i (equal-mass shells; a shell feels half its own mass),
 *   recomputed by sorting at every step, so shells cross freely;
 *   the second term is a smooth, non-clustering background of density f_sm rho_crit0 a^-3 (the cosmic baryons outside the core);
 *   the third is Lambda c^2 r / 3 = Omega_L H0^2 r;  a(t) is the exact flat-LCDM (or Einstein-de Sitter) scale factor.
 *
 * Integrator: kick-drift-kick leapfrog with individual power-of-two ("block") steps.  Level k has the step T / 2^k (T = t1 - t0).
 * A shell's step is min(eta t_loc, etaH / H(t)) with t_loc = min( sqrt(r / g_pull), r / |v|, r^2 / j ), rounded down to a level;
 * a shell may move to a coarser level only when the current time is a multiple of that level's step (block synchronisation).
 * Between its kicks a shell drifts linearly, so its position is known exactly at any time.
 *
 * Enclosed masses (exact).  Shells at levels >= KF (the "fast tier") are drifted and insertion-sorted at every tick; all shells
 * are drifted and sorted together at every multiple of the level-(KF-1) step (a "slow tick").  Slow-tier shells are kicked only at
 * slow ticks, so between two slow ticks a slow shell j moves by at most D r_j, D = max_j |v_j| S / r_j (S = the slow-tick
 * interval).  A fast shell counts the slow shells inside its radius by binary search on the slow tier's sorted positions and
 * checks the few inside the +-D window at their exact current positions.  No approximation is made in the count.
 *
 * Angular momentum.  A shell is radial until its first turnaround (its synchronised velocity changes sign from + to -).  There
 *     j^2 = 2 [Phi(r_ta) - Phi(q r_ta)] / ( (q r_ta)^-2 - r_ta^-2 ),
 * the energy/pericentre relation for apocentre r_ta and pericentre q r_ta in the potential of the mass enclosed at that moment
 * (the shells inside r_ta at their current radii, the shell's own half mass, the core, the smooth background and Lambda), held
 * fixed; j stays fixed afterwards.  (If that potential drop were not positive the point-mass form 2 G M(<r_ta) r_ta q/(1+q)
 * would be used and counted; it never is in the committed runs.)  q <= 0 keeps every shell radial.
 *
 * Units: kpc, km/s, Msun; time in kpc/(km/s).
 */
#include <math.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int32_t eds;                /* 1: Einstein-de Sitter a(t) = (1.5 H0 t)^(2/3);  0: flat LCDM */
    double  H0, Om, OL, fsm, G; /* H0 in km/s/kpc; fsm = density parameter of the smooth non-clustering background */
    int32_t core;               /* 0 none, 1 Plummer-softened point mass, 2 exponential sphere */
    double  Mb, eps, h;
    int32_t N;
    double  m, q, t0, t1;
    int32_t kmax, kf;
    double  eta, etaH;
    int32_t nsnap;
} Params;

typedef struct {
    int64_t nticks, nkicks, nslowticks, nfloor, nrefl, nlazy, nfallback, nturn, njfb;
    double  maxD;
} Stats;

typedef struct {
    const Params *P;
    Stats *S;
    int64_t TT;
    double T, dtick;
    double *rr, *vv, *tref, *vsp, *j2;
    int32_t *lvl;
    char *turned;
    double *t_ta, *r_ta, *r_p1;
    int32_t *nperi;
    int64_t cnt[64];
} Ctx;

static inline double mcore(const Params *P, double r)
{
    if (P->core == 1) {
        double d = r * r + P->eps * P->eps;
        return P->Mb * r * r * r / (d * sqrt(d));
    }
    if (P->core == 2) {
        double s = r / P->h;
        if (s < 1e-3) return P->Mb * s * s * s / 6.0 * (1.0 - 0.75 * s + 0.3 * s * s);
        return P->Mb * (1.0 - exp(-s) * (1.0 + s + 0.5 * s * s));
    }
    return 0.0;
}

static inline double phi_core(const Params *P, double r)
{
    if (P->core == 1) return -P->G * P->Mb / sqrt(r * r + P->eps * P->eps);
    if (P->core == 2) {
        double s = r / P->h;
        double Pm = (s < 1e-3) ? s * s * s / 6.0 * (1.0 - 0.75 * s + 0.3 * s * s) : 1.0 - exp(-s) * (1.0 + s + 0.5 * s * s);
        return -P->G * P->Mb * (Pm / r + (1.0 + s) * exp(-s) / (2.0 * P->h));
    }
    return 0.0;
}

static inline double a_of_t(const Params *P, double t)
{
    if (P->eds) return pow(1.5 * P->H0 * t, 2.0 / 3.0);
    return pow(P->Om / P->OL, 1.0 / 3.0) * pow(sinh(1.5 * sqrt(P->OL) * P->H0 * t), 2.0 / 3.0);
}

static inline double accel(const Params *P, double r, double Menc, double j2, double ia3)
{
    double H02 = P->H0 * P->H0;
    return -P->G * (mcore(P, r) + Menc) / (r * r) - 0.5 * P->fsm * H02 * ia3 * r + P->OL * H02 * r + j2 / (r * r * r);
}

static inline double tloc(const Params *P, double r, double v, double Menc, double j2, double ia3)
{
    double gp = P->G * (mcore(P, r) + Menc) / (r * r) + 0.5 * P->fsm * P->H0 * P->H0 * ia3 * r;
    double t = sqrt(r / gp);
    double av = fabs(v);
    if (av > 0.0) { double tv = r / av; if (tv < t) t = tv; }
    if (j2 > 0.0) { double tj = r * r / sqrt(j2); if (tj < t) t = tj; }
    return t;
}

static inline int level_for(const Ctx *c, double dtw)
{
    double x = c->T / dtw;
    if (!(x > 1.0)) return 0;
    int k = (int)ceil(log2(x));
    if (k < 0) k = 0;
    while (k <= c->P->kmax && ldexp(c->T, -k) > dtw) k++;
    if (k > c->P->kmax) { k = c->P->kmax; c->S->nfloor++; }
    return k;
}

/* closing half-kick of shell id's current step at time t, and the pericentre/turnaround events.  Returns 1 when the shell has
   just turned around (the caller then assigns j^2 from the enclosed potential and calls kick_open). */
static int kick_close(Ctx *c, int id, double Menc, double t, double ia3)
{
    const Params *P = c->P;
    double r = c->rr[id];
    double dto = ldexp(c->T, -c->lvl[id]);
    double vs = c->vv[id] + 0.5 * dto * accel(P, r, Menc, c->j2[id], ia3);
    int turn = 0;
    if (!c->turned[id] && c->vsp[id] > 0.0 && vs <= 0.0) {
        c->turned[id] = 1; c->t_ta[id] = t; c->r_ta[id] = r; c->S->nturn++;
        turn = (P->q > 0.0);
    } else if (c->turned[id] && c->vsp[id] < 0.0 && vs >= 0.0) {
        c->nperi[id]++;
        if (c->nperi[id] == 1) c->r_p1[id] = r;
    }
    c->vsp[id] = vs;
    c->vv[id] = vs;                     /* synchronised velocity until kick_open */
    c->S->nkicks++;
    return turn;
}

/* j^2 at turnaround from the potential drop between r_ta and q r_ta; dphi_sh = G sum_j m (1/max(r_j, q r_ta) - 1/r_ta) over the
   OTHER shells inside r_ta at their current radii */
static void assign_j(Ctx *c, int id, double Menc, double dphi_sh, double ia3)
{
    const Params *P = c->P;
    double rta = c->rr[id], rp = P->q * rta, H02 = P->H0 * P->H0;
    double dphi = dphi_sh + P->G * 0.5 * P->m * (1.0 / rp - 1.0 / rta) + phi_core(P, rta) - phi_core(P, rp)
                + 0.25 * P->fsm * H02 * ia3 * (rta * rta - rp * rp) - 0.5 * P->OL * H02 * (rta * rta - rp * rp);
    if (dphi > 0.0) {
        c->j2[id] = 2.0 * dphi / (1.0 / (rp * rp) - 1.0 / (rta * rta));
    } else {
        double Mt = mcore(P, rta) + Menc + P->fsm * H02 * ia3 * rta * rta * rta / (2.0 * P->G);
        c->j2[id] = 2.0 * P->G * Mt * rta * P->q / (1.0 + P->q);
        c->S->njfb++;
    }
}

/* new level (block-synchronised) and the opening half-kick of the next step */
static void kick_open(Ctx *c, int id, double Menc, int64_t tau, double ia3, double Ht)
{
    const Params *P = c->P;
    double r = c->rr[id], vs = c->vv[id];
    double acc = accel(P, r, Menc, c->j2[id], ia3);
    double dtw = P->eta * tloc(P, r, vs, Menc, c->j2[id], ia3);
    double dth = P->etaH / Ht;
    if (dth < dtw) dtw = dth;
    int k = level_for(c, dtw);
    while (k < P->kmax && (tau & ((((int64_t)1) << (P->kmax - k)) - 1)) != 0) k++;   /* block synchronisation */
    c->cnt[c->lvl[id]]--; c->cnt[k]++;
    c->lvl[id] = k;
    c->vv[id] = vs + 0.5 * ldexp(c->T, -k) * acc;
}

static void isort(int32_t *ord, int n, const double *key)
{
    for (int p = 1; p < n; p++) {
        int32_t id = ord[p];
        double x = key[id];
        int q = p - 1;
        while (q >= 0 && key[ord[q]] > x) { ord[q + 1] = ord[q]; q--; }
        ord[q + 1] = id;
    }
}

static inline int lower_bound(const double *a, int n, double x)
{
    int lo = 0, hi = n;
    while (lo < hi) { int mid = (lo + hi) >> 1; if (a[mid] < x) lo = mid + 1; else hi = mid; }
    return lo;
}

int run_shells(const Params *P, const double *r_init, const double *v_init, const double *tsnap, double *snap,
               double *r_out, double *v_out, double *j2_out, double *t_ta, double *r_ta, double *r_p1, int32_t *nperi,
               Stats *S)
{
    const int N = P->N, KMAX = P->kmax, KF = P->kf;
    if (KMAX > 62 || KF < 1 || KF > KMAX) return -1;
    Ctx c;
    memset(&c, 0, sizeof(c));
    memset(S, 0, sizeof(*S));
    c.P = P; c.S = S;
    c.TT = ((int64_t)1) << KMAX;
    c.T = P->t1 - P->t0;
    c.dtick = c.T / (double)c.TT;
    const double Ssync = ldexp(c.T, -(KF - 1));
    c.rr = malloc(N * sizeof(double)); c.vv = malloc(N * sizeof(double)); c.tref = malloc(N * sizeof(double));
    c.vsp = malloc(N * sizeof(double)); c.j2 = malloc(N * sizeof(double));
    c.lvl = malloc(N * sizeof(int32_t)); c.turned = malloc(N);
    int32_t *all = malloc(N * sizeof(int32_t)), *fast = malloc(N * sizeof(int32_t)), *slow = malloc(N * sizeof(int32_t));
    double *slow_r = malloc(N * sizeof(double));
    if (!c.rr || !c.vv || !c.tref || !c.vsp || !c.j2 || !c.lvl || !c.turned || !all || !fast || !slow || !slow_r) return -2;
    c.t_ta = t_ta; c.r_ta = r_ta; c.r_p1 = r_p1; c.nperi = nperi;

    for (int i = 0; i < N; i++) {
        c.rr[i] = r_init[i]; c.vv[i] = v_init[i]; c.tref[i] = P->t0; c.vsp[i] = v_init[i]; c.j2[i] = 0.0;
        c.turned[i] = 0; c.lvl[i] = 0; t_ta[i] = NAN; r_ta[i] = NAN; r_p1[i] = NAN; nperi[i] = 0; all[i] = i;
    }
    isort(all, N, c.rr);
    const double m = P->m;
    double t = P->t0, a = a_of_t(P, t), ia3 = 1.0 / (a * a * a), Ht = P->H0 * sqrt(P->Om * ia3 + P->OL);
    c.cnt[0] = N;
    /* the opening half-kick of every shell at t0 */
    for (int p = 0; p < N; p++) {
        int id = all[p];
        double Menc = m * (p + 0.5), r = c.rr[id];
        double acc = accel(P, r, Menc, 0.0, ia3);
        double dtw = P->eta * tloc(P, r, c.vv[id], Menc, 0.0, ia3), dth = P->etaH / Ht;
        if (dth < dtw) dtw = dth;
        int k = level_for(&c, dtw);
        c.cnt[0]--; c.cnt[k]++; c.lvl[id] = k;
        c.vv[id] = c.vv[id] + 0.5 * ldexp(c.T, -k) * acc;
    }
    int nf = 0, ns = 0;
    double D = 0.0;
#define REBUILD_TIERS()                                                                                  \
    do {                                                                                                 \
        nf = 0; ns = 0; D = 0.0;                                                                         \
        for (int p_ = 0; p_ < N; p_++) {                                                                 \
            int id_ = all[p_];                                                                           \
            if (c.lvl[id_] >= KF) fast[nf++] = id_;                                                      \
            else { slow[ns] = id_; slow_r[ns++] = c.rr[id_];                                              \
                   double d_ = fabs(c.vv[id_]) * Ssync / c.rr[id_]; if (d_ > D) D = d_; }                 \
        }                                                                                                \
        if (D > S->maxD) S->maxD = D;                                                                    \
    } while (0)
    REBUILD_TIERS();

    int64_t tau = 0;
    int isnap = 0;
    for (;;) {
        int kfin = 0;
        for (int k = KMAX; k >= 0; k--) if (c.cnt[k] > 0) { kfin = k; break; }
        int64_t st = ((int64_t)1) << (KMAX - kfin);
        int64_t tn = (tau / st + 1) * st;
        if (tn > c.TT) tn = c.TT;
        double tnext = (tn == c.TT) ? P->t1 : P->t0 + (double)tn * c.dtick;
        while (isnap < P->nsnap && tsnap[isnap] <= tnext) {
            double ts = tsnap[isnap];
            double *row = snap + (size_t)isnap * (size_t)N;
            for (int i = 0; i < N; i++) row[i] = c.rr[i] + c.vv[i] * (ts - c.tref[i]);
            isnap++;
        }
        tau = tn; t = tnext;
        int kact = KMAX - __builtin_ctzll((unsigned long long)tau);
        if (kact < 0) kact = 0;
        int final = (tau == c.TT);
        a = a_of_t(P, t); ia3 = 1.0 / (a * a * a); Ht = P->H0 * sqrt(P->Om * ia3 + P->OL);
        if (kact <= KF - 1) {                                                   /* slow tick: everything */
            for (int i = 0; i < N; i++) {
                c.rr[i] += c.vv[i] * (t - c.tref[i]); c.tref[i] = t;
                if (c.rr[i] < 0.0) { c.rr[i] = -c.rr[i]; c.vv[i] = -c.vv[i]; S->nrefl++; }
            }
            isort(all, N, c.rr);
            for (int p = 0; p < N; p++) {
                int id = all[p];
                if (c.lvl[id] < kact) continue;
                double Menc = m * (p + 0.5);
                if (kick_close(&c, id, Menc, t, ia3)) {
                    double rta = c.rr[id], rp = P->q * rta, sh = 0.0;
                    for (int s = 0; s < p; s++) { double rj = c.rr[all[s]]; sh += 1.0 / (rj > rp ? rj : rp) - 1.0 / rta; }
                    assign_j(&c, id, Menc, P->G * m * sh, ia3);
                }
                if (!final) kick_open(&c, id, Menc, tau, ia3, Ht);
            }
            REBUILD_TIERS();
            S->nslowticks++;
        } else {                                                                /* fast tick: the fast tier only */
            for (int f = 0; f < nf; f++) {
                int id = fast[f];
                c.rr[id] += c.vv[id] * (t - c.tref[id]); c.tref[id] = t;
                if (c.rr[id] < 0.0) { c.rr[id] = -c.rr[id]; c.vv[id] = -c.vv[id]; S->nrefl++; }
            }
            isort(fast, nf, c.rr);
            for (int f = 0; f < nf; f++) {
                int id = fast[f];
                if (c.lvl[id] < kact) continue;
                double r = c.rr[id];
                int64_t nin = f;
                if (ns > 0) {
                    if (D >= 0.5) {
                        for (int s = 0; s < ns; s++) {
                            int js = slow[s];
                            if (c.rr[js] + c.vv[js] * (t - c.tref[js]) < r) nin++;
                        }
                        S->nfallback++;
                    } else {
                        int lo = lower_bound(slow_r, ns, r / (1.0 + D));
                        int hi = lower_bound(slow_r, ns, r / (1.0 - D));
                        nin += lo;
                        for (int s = lo; s < hi; s++) {
                            int js = slow[s];
                            if (c.rr[js] + c.vv[js] * (t - c.tref[js]) < r) nin++;
                        }
                        S->nlazy += hi - lo;
                    }
                }
                double Menc = m * ((double)nin + 0.5);
                if (kick_close(&c, id, Menc, t, ia3)) {
                    double rta = r, rp = P->q * rta, sh = 0.0;
                    for (int g = 0; g < f; g++) { double rj = c.rr[fast[g]]; sh += 1.0 / (rj > rp ? rj : rp) - 1.0 / rta; }
                    int hi = (D >= 0.5) ? ns : lower_bound(slow_r, ns, rta / (1.0 - D));
                    for (int s = 0; s < hi; s++) {
                        int js = slow[s];
                        double rj = c.rr[js] + c.vv[js] * (t - c.tref[js]);
                        if (rj < rta) sh += 1.0 / (rj > rp ? rj : rp) - 1.0 / rta;
                    }
                    assign_j(&c, id, Menc, P->G * m * sh, ia3);
                }
                if (!final) kick_open(&c, id, Menc, tau, ia3, Ht);
            }
        }
        S->nticks++;
        if (final) break;
    }
    for (int i = 0; i < N; i++) { r_out[i] = c.rr[i]; v_out[i] = c.vv[i]; j2_out[i] = c.j2[i]; }
    free(c.rr); free(c.vv); free(c.tref); free(c.vsp); free(c.j2); free(c.lvl); free(c.turned);
    free(all); free(fast); free(slow); free(slow_r);
    return isnap;
}

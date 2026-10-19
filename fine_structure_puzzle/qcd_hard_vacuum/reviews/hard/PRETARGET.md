# Independent hard review: pretarget critical derivation

Written 2026-10-19T17:52:14Z by fresh subagent `/root/hard_independent_review`.
Exposure before this record: task instructions, package filenames, FSP-010
CONTRACT/BASELINE, the three required unchanged parent derivations, installed
mathbox instructions, root status and exact-version cache misses. No new
hard_proton/hard_bridge derivation, report, code, input or result was opened.
This is source-first relative to the new author arguments, not ignorance of the
parent Dirac and OPE benchmarks. Parent content hashes:

- proton_kernel/DERIVATION.md: `8cb49cb40f449a13a6443978e8281df6327622d6a364efc42f6e607d4b52af7e`
- proton_kernel/DIRAC_MSBAR_MATCHING.md: `eeaa5cbfc08956a2005ceeeddbc5e2505b979b3ffb5244b8a1513c62d078fe6a`
- sea_ope/DERIVATION.md: `3e11521b73f007ef775cd31c71e2842319e12ab157141a9f5b681316681e6cb6`

## Quark matching and the hadron insertion

Set u=e². For an elementary on-shell Dirac line, Feynman parameter x on the
photon gives numerator d+(2-d)x = 4-2x+epsilon(2x-2), and denominator
Delta=(1-x)²m²+x s for a photon mass squared s. Thus

    f_D(s)=D_D(s)/m
      =1/(16pi²) integral_0^1 [(4-2x) log(mu²/Delta)+(2x-2)] dx.

This is the MSbar mass held fixed convention. The epsilon numerator has
integral -1; its product with the pole is a finite local contact and cannot
be dropped. At s=0, -2 integral(4-2x)log(1-x)=5, so
f_D(0)=[3log(mu²/m²)+4]/(16pi²).

Independently, the parent full radial Dirac kernel has primitive
F(z)~(3/4)log(2z)+3/16, z=Q/(2m). A sharp O(4) photon cutoff therefore gives
f_cut=[3log(Lambda²/m²)+3/2]/(16pi²)+o(1). Subtracting yields the *added*
cutoff-to-fixed-MSbar insertion

    (dm_cut/du)_fixedMSbar
       = Q_f² m_f [3log(mu²/Lambda²)+5/2]/(16pi²),

at leading order in strong coupling. The plus 5/2 is fixed, not fitted. For
sigma_f=m_f partial M_p/partial m_f, Feynman--Hellmann makes its proton
contribution

    (D_p^massct)/M_p
      = sum_f Q_f² (sigma_f/M_p)
            [3log(mu²/Lambda²)+5/2]/(16pi²).

There is no extra m_f or M_p and no factor 4pi. If source delta-m denotes the
subtracted parameter rather than the actual bare-path increment its sign is
opposite. This calculation fixes the e² alpha_s^0 *quark mass conversion*.
It does not fix the e² alpha_s gluon/coupling conversion. The latter can survive
at order one in the proton response because canonical <G²> scales as
M_p²/alpha_s by the anomaly. Consequently neither a small perturbative gluon
coefficient nor the finite 5/2 above licenses a full hard-QCD endpoint.

## Recovering an integration constant from all mass scales

For n>=1, integrating by parts at *finite* L gives

    f(0)=sum_(k=0)^(n-1) (-L)^k f^(k)(L)/k!
         +(-1)^n/(n-1)! integral_0^L s^(n-1) f^(n)(s) ds.

This is a boundary-value reconstruction, not a determination from derivatives
alone: adding a constant to f leaves every derivative unchanged. The lower
endpoint terms require s^k f^(k)(s)->0 for k>=1 and finite f(0). If
f(s)=A log(s/s0)+B+r(s), and L^k r^(k)(L)->0 for k<n, the boundary polynomial
is A log(L/s0)+B-A H_(n-1)+o(1). Therefore

    f(0)=B-A H_(n-1)
       +lim_(L->infty){(-1)^n/(n-1)! integral_0^L
                          s^(n-1)f^(n)(s)ds + A log(L/s0)}.

The log cannot be dropped. For n=2, f(0)=f(L)-L f'(L)+integral_0^L s f''.
For n=3, f(0)=f(L)-L f'(L)+L²f''(L)/2-integral_0^L s²f'''/2.

For the Dirac parameter integral, take s0=m². At large s the integral of
(4-2x) is 3, its log-x integral is -7/2, and the evanescent term is -1:

    f_D(s)=[-3log(s/m²)+3log(mu²/m²)+5/2]/(16pi²)+o(1).

Thus A=-3/(16pi²), B=[3log(mu²/m²)+5/2]/(16pi²). For n=2 the endpoint
constant is [3log(mu²/m²)+11/2]/(16pi²), not 4/(16pi²).
The subtracted curvature integral must supply -3/(32pi²). The large-s
Dirac contact constant 5/2 equals the sharp-cutoff conversion constant here;
this equality does not establish the corresponding interacting gluon constant.

## Full radial normalization and sign

With t=Q² and spin-averaged parent conventions,

    f_D,cut(s)=1/(2pi²) integral dz B_D(z) 4m²z²/(4m²z²+s),
    B_D(z)=[sqrt(1+z²)+2z]/[sqrt(1+z²)+z]².

Equivalently the t-density is B_D(sqrt(t)/(2m))/(8pi² m sqrt(t)), approaching
3/(16pi² t). Differentiating n>=1 times before integrating is UV convergent:

    f_D^(n)(s)=(-1)^n n!/(2pi²)
        integral_0^infty dz B_D(z) 4m²z²/(4m²z²+s)^(n+1).

The same derivative from parameters is

    (-1)^n (n-1)!/(16pi²)
       integral_0^1 (4-2x) x^n/[(1-x)²m²+x s]^n dx.

Hence f'<0, f''>0. They provide independent representations suitable for
bounded checks of the normalization. Massive-photon derivatives annihilate
s-independent local contacts; matching must restore those contacts. All-scale
derivatives in QCD additionally require the full individual-proton current,
all connected-to-proton contractions and the declared current/action contacts.
No finite collection of slopes, no Born-only tensor and no quark-only finite
matching determines that full observable.

This record is frozen before new author exposure. Subsequent corrections, if
any, will be explicit in REVIEW.md rather than replacing this pretarget record.

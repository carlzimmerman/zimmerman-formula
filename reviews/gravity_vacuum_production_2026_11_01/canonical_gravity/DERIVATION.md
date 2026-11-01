# Canonical SU5+W0: discriminating derivation

Use canonical K and the standard N=1 F potential exp(K/P²)[sum|Wi+zi*W/P²|²-3|W|²/P²], plus D terms. Gauge kinetic data are constant. Along X real,A=i aD,B=bD,D=diag(2,2,2,-3,-3), all gauge D terms vanish. In f=1 mass units let p=Mp/mu,w0=W0/mu³. Then

    K=X²+30a²+30b²,
    w=X-15hXa²+15lambda a²b+w0,
    Vsg=exp(K/p²){(1-15ha²+Xw/p²)²
             +30a²(hX-lambda b-w/p²)²
             +30(lambda a²/2+bw/p²)²-3w²/p²}.

This is the full real D-flat canonical microscopic tree potential, not a singlet ansatz. The rigid valley is a0²=2h/(30h²+lambda²),b0=hX/lambda. Its normalized flat coordinate T=sqrt(30h²+lambda²)X/lambda and F_eff=1/sqrt31 when h=lambda=e; Wraw=F_eff T and K=|T|²+30a0². Heavy normal Hessians are raw Haa=120h,Hbb=60lambda²a0². They are not canonical light masses.

Expanding the full microscopic potential to first order in w0/p² gives

    deltaV=2w0 Re[sum zi Wi-3Wraw]/p²
          =-4w0 ReX/p².

Euler homogeneity cancels every cubic contribution exactly; only the linear fX survives. There is therefore no O(w0/p²) a/b tadpole. Heavy SUGRA relaxation starts at the subsequent gravity order. This is stronger than assuming it is small because v/Mp is small. On the valley, deltaV=-J R cos(theta),J=4F_eff W0/Mp², R=|T|. Vacuum cancellation gives W0≈F_eff Mp/sqrt3, requiring a fractional residual tuning of orderrhoDE/(2F_eff²) in W0. Exact tuning uses the full potential and the chosen subtraction, not an independently shifted rigid vacuum.

Let U(R) be the rigid reduced loop potential. At the aligned phase the leading light stationarity is U_R=J. With canonical real sigma=sqrt2 deltaR and phase a=sqrt2 Rtheta,

    m_sigma²=U_RR/2, m_a²=J/(2R),
    g_sigma_aa=(m_sigma²-m_a²)/(sqrt2 R),
    Gamma_sigma_aa=m_sigma³/(64pi R²)
       *(1-m_a²/m_sigma²)² sqrt(1-4m_a²/m_sigma²).

The cubic follows by expanding U(sqrt[(R+sigma/sqrt2)²+a²/2])-J(R+sigma/sqrt2). In polar coordinates the potential cubic and derivative cubic must both be included. Merely multiplying the old massless-phase width by phase space is wrong. For finite distinct A,F, use the actual normalized derivatives rather than silently transplanting this tree metric.

In t=R/R0,R0=z0/sqrt(e), define psi(t)=CW(R0t)/e². The chosen critical g/e makes this one-loop shape independent of e. The tilt is e²L with

    L=4z0 mu/[31sqrt3 Mp e^(5/2)].

Stable local branch: psi'(t)=L>0 and psi''(t)>0. The first fold is psi''=0; phase-pair closure is t psi''=4psi'. The phase/radial ratio is psi'/(tpsi''). Parameterizing the branch by t is preferable to assuming a displaced minimum still exists for a target mass. It gives

    mu(t)=31sqrt3 Mp e^(5/2) psi'(t)/(4z0),
    mchi(t)=mu(t) e^(5/2) cchi(t),
    m_sigma²=mu² e³ psi''/(2z0²),
    m_a²=mu² e³ psi'/(2z0²t).

The physical mchi curve need not attain its maximum at the fixed-mu fold because cchi changes with t. Actual threshold masses/current slopes will be evaluated at the resulting points. W0 corrections to the simple tilt and quantum/metric corrections are a separate finite stage, not hidden in this first profile.

At radii comparable with Mp the canonical reduced model is the Polonyi potential, with an exact-K Minkowski stationary point R/Mp=sqrt3-1,W0/(F_eff Mp)=2-sqrt3. This follows by direct stationarity, not an assumed continuation of the sub-Planckian CW vacuum. Its full microscopic normal reduction and sensitivity to unspecified Planck operators must be distinguished from the small-field branch.

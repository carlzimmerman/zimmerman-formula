# CFG158 referee kernel (Julia). Spherical cold shells with shell crossing, static baryon core.
# Independent of CFG118's C code: each shell is a test body integrated by an adaptive Dormand-Prince 5(4) in a potential whose
# enclosed cold mass is rebuilt from sorted shell positions every dt_s and interpolated linearly in time by a predictor-corrector.
# Units: kpc, km/s, Msun; time unit kpc/(km/s).  Usage: julia cfg158_shells.jl <task file>   (one spec per line, key=value ...)
using Printf

const G = 4.30091727e-6
const MYR = 977.79222         # Myr per (kpc/(km/s))

mutable struct Ctx
    geom::Int; Mb::Float64; eps2::Float64; h::Float64
    H0::Float64; Om::Float64; OL::Float64; Ob::Float64
    rn::Vector{Float64}; rp::Vector{Float64}; Ms::Vector{Float64}; n::Int
    tn::Float64; dt::Float64; usep::Bool; jform::Int
end

mutable struct State
    R::Vector{Float64}; V::Vector{Float64}; J2::Vector{Float64}; TU::Vector{Int8}
    H::Vector{Float64}; RTA::Vector{Float64}; RP::Vector{Float64}
end
State(n) = State(zeros(n), zeros(n), zeros(n), zeros(Int8, n), zeros(n), zeros(n), zeros(n))
function copystate!(B::State, A::State)
    copyto!(B.R, A.R); copyto!(B.V, A.V); copyto!(B.J2, A.J2); copyto!(B.TU, A.TU)
    copyto!(B.H, A.H); copyto!(B.RTA, A.RTA); copyto!(B.RP, A.RP)
end

const STAT = zeros(Int64, 5)   # steps, rejects, refines, resort fallbacks, tangential-scale fallback accepts

@inline function mcp(rs::Vector{Float64}, Ms::Vector{Float64}, n::Int, r::Float64)
    n == 0 && return 0.0
    k = searchsortedlast(rs, r)
    if k == 0
        return Ms[1] * r / rs[1]
    elseif k >= n
        return Ms[n]
    else
        d = rs[k+1] - rs[k]
        return d > 0 ? Ms[k] + (Ms[k+1] - Ms[k]) * (r - rs[k]) / d : Ms[k]
    end
end

@inline function P3(s::Float64)   # regularised lower incomplete gamma(3, s)
    if s < 0.5
        t = s * s * s / 6.0; sm = t
        for k in 4:14
            t *= s / k; sm += t
        end
        return exp(-s) * sm
    else
        return 1.0 - (1.0 + s + 0.5 * s * s) * exp(-s)
    end
end

@inline function a3inv(c::Ctx, t::Float64)
    if c.OL > 0
        s = sinh(1.5 * sqrt(c.OL) * c.H0 * t)
        return (c.OL / c.Om) / (s * s)
    else
        x = 1.5 * c.H0 * t
        return 1.0 / (x * x)
    end
end

@inline function coreacc(c::Ctx, r::Float64)   # inward acceleration from the static core
    c.Mb == 0.0 && return 0.0
    if c.geom == 1
        return G * c.Mb * r / (r * r + c.eps2)^1.5
    else
        return G * c.Mb * P3(r / c.h) / (r * r)
    end
end

@inline function coremass(c::Ctx, r::Float64)
    c.Mb == 0.0 && return 0.0
    c.geom == 1 ? c.Mb * r^3 / (r * r + c.eps2)^1.5 : c.Mb * P3(r / c.h)
end

@inline function mcold(c::Ctx, r::Float64, t::Float64)
    c.n == 0 && return 0.0
    m1 = mcp(c.rn, c.Ms, c.n, r)
    if c.usep
        th = (t - c.tn) / c.dt
        m2 = mcp(c.rp, c.Ms, c.n, r)
        return (1 - th) * m1 + th * m2
    end
    return m1
end

@inline function gin(c::Ctx, r::Float64, t::Float64)   # inward acceleration without centrifugal term
    g = coreacc(c, r) + G * mcold(c, r, t) / (r * r)
    if c.Ob > 0
        g += 0.5 * c.H0^2 * c.Ob * a3inv(c, t) * r
    end
    g -= c.OL * c.H0^2 * r
    return g
end

@inline f2(c::Ctx, r::Float64, t::Float64, j2::Float64) = -gin(c, r, t) + j2 / (r * r * r)

# specific angular momentum squared at first turnaround (README/frozen energy-pericentre relation)
function jsq(c::Ctx, rta::Float64, q::Float64, t::Float64)
    if c.jform == 1
        return 2 * G * (coremass(c, rta) + mcold(c, rta, t)) * rta * q / (1 + q)
    end
    rp = q * rta
    nint = 400
    a = log(rp); b = log(rta); hh = (b - a) / nint
    s = 0.0
    for k in 0:nint
        x = exp(a + k * hh)
        w = (k == 0 || k == nint) ? 1.0 : (isodd(k) ? 4.0 : 2.0)
        s += w * gin(c, x, t) * x
    end
    s *= hh / 3
    return 2 * s / (1 / (rp * rp) - 1 / (rta * rta))
end

# one Dormand-Prince 5(4) step
@inline function dp_step(c::Ctx, r, v, t, h, j2, k1v)
    kr1 = v
    r2 = r + h * (0.2 * kr1); v2 = v + h * (0.2 * k1v)
    kr2 = v2; kv2 = f2(c, r2, t + 0.2h, j2)
    r3 = r + h * (3 / 40 * kr1 + 9 / 40 * kr2); v3 = v + h * (3 / 40 * k1v + 9 / 40 * kv2)
    kr3 = v3; kv3 = f2(c, r3, t + 0.3h, j2)
    r4 = r + h * (44 / 45 * kr1 - 56 / 15 * kr2 + 32 / 9 * kr3); v4 = v + h * (44 / 45 * k1v - 56 / 15 * kv2 + 32 / 9 * kv3)
    kr4 = v4; kv4 = f2(c, r4, t + 0.8h, j2)
    r5 = r + h * (19372 / 6561 * kr1 - 25360 / 2187 * kr2 + 64448 / 6561 * kr3 - 212 / 729 * kr4)
    v5 = v + h * (19372 / 6561 * k1v - 25360 / 2187 * kv2 + 64448 / 6561 * kv3 - 212 / 729 * kv4)
    kr5 = v5; kv5 = f2(c, r5, t + 8 / 9 * h, j2)
    r6 = r + h * (9017 / 3168 * kr1 - 355 / 33 * kr2 + 46732 / 5247 * kr3 + 49 / 176 * kr4 - 5103 / 18656 * kr5)
    v6 = v + h * (9017 / 3168 * k1v - 355 / 33 * kv2 + 46732 / 5247 * kv3 + 49 / 176 * kv4 - 5103 / 18656 * kv5)
    kr6 = v6; kv6 = f2(c, r6, t + h, j2)
    r7 = r + h * (35 / 384 * kr1 + 500 / 1113 * kr3 + 125 / 192 * kr4 - 2187 / 6784 * kr5 + 11 / 84 * kr6)
    v7 = v + h * (35 / 384 * k1v + 500 / 1113 * kv3 + 125 / 192 * kv4 - 2187 / 6784 * kv5 + 11 / 84 * kv6)
    kr7 = v7; kv7 = f2(c, r7, t + h, j2)
    er = h * (71 / 57600 * kr1 - 71 / 16695 * kr3 + 71 / 1920 * kr4 - 17253 / 339200 * kr5 + 22 / 525 * kr6 - 1 / 40 * kr7)
    ev = h * (71 / 57600 * k1v - 71 / 16695 * kv3 + 71 / 1920 * kv4 - 17253 / 339200 * kv5 + 22 / 525 * kv6 - 1 / 40 * kv7)
    return r7, v7, er, ev, kv7
end

# find hh in (0,h] with v(hh) ~ 0 (v changes sign over the step): regula falsi (Illinois) on the step
function refine_zero(c::Ctx, r, v, t, h, j2, k1v, vend, tol)
    lo = 0.0; flo = v; hi = h; fhi = vend
    hh = h; rr = r; vv = vend
    side = 0
    for it in 1:60
        hh = (lo * fhi - hi * flo) / (fhi - flo)
        rr, vv, _, _, _ = dp_step(c, r, v, t, hh, j2, k1v)
        if abs(vv) <= tol * (sqrt(abs(k1v) * r) + abs(v) + 1e-30) || (hi - lo) < 1e-14 * h
            break
        end
        if sign(vv) == sign(flo)
            lo = hh; flo = vv
            side == -1 && (fhi /= 2); side = -1
        else
            hi = hh; fhi = vv
            side == 1 && (flo /= 2); side = 1
        end
        STAT[3] += 1
    end
    return hh, rr, vv
end

function advance!(c::Ctx, S::State, i::Int, t::Float64, tend::Float64, q::Float64, rtol::Float64)
    r = S.R[i]; v = S.V[i]; j2 = S.J2[i]; tu = S.TU[i]; h = S.H[i]
    if !(h > 0); h = 1e-3 * (tend - t); end
    k1v = f2(c, r, t, j2)
    while t < tend - 1e-13 * abs(tend)
        h = min(h, tend - t)
        r7, v7, er, ev, kv7 = dp_step(c, r, v, t, h, j2, k1v)
        vc = max(abs(v), abs(v7), sqrt(abs(k1v) * r))
        err = max(abs(er) / (rtol * max(abs(r), abs(r7)) + 1e-300), abs(ev) / (rtol * vc + 1e-300))
        if !(err <= 1.0) && h < 1e-10 && j2 > 0
            # last-resort branch (only reached below h = 1e-10 kpc/(km/s), far below any physical step): a shell on a
            # circular orbit has v_r ~ 0 and no radial acceleration, so the relative v_r tolerance is unattainable; use the
            # shell's tangential speed j/r as the velocity scale.  Never reached by a step in the runs that completed under v1.
            vc2 = max(vc, sqrt(j2) / r)
            err = max(abs(er) / (rtol * max(abs(r), abs(r7)) + 1e-300), abs(ev) / (rtol * vc2 + 1e-300))
            err <= 1.0 && (STAT[5] += 1)
        end
        if !(err <= 1.0)
            STAT[2] += 1
            h *= max(0.2, 0.9 * (isfinite(err) ? err : 1e10)^(-0.2))
            if h < 1e-15 * abs(t); error("step underflow shell $i t=$t"); end
            continue
        end
        STAT[1] += 1
        if tu == 0 && v7 <= 0 && v > 0
            hh, r7, v7 = refine_zero(c, r, v, t, h, j2, k1v, v7, 1e-9)
            t += hh; r = r7; v = v7
            j2 = jsq(c, r, q, t); tu = 1; S.RTA[i] = r
            k1v = f2(c, r, t, j2)
            continue
        elseif tu == 1 && v7 >= 0 && v < 0
            hh, r7, v7 = refine_zero(c, r, v, t, h, j2, k1v, v7, 1e-9)
            t += hh; r = r7; v = v7; tu = 2; S.RP[i] = r
            k1v = f2(c, r, t, j2)
            continue
        end
        t += h; r = r7; v = v7; k1v = kv7
        h *= min(5.0, max(0.2, 0.9 * (err > 1e-30 ? err : 1e-30)^(-0.2)))
    end
    S.R[i] = r; S.V[i] = v; S.J2[i] = j2; S.TU[i] = tu; S.H[i] = h
end

function resort!(sr::Vector{Float64}, p::Vector{Int}, R::Vector{Float64})
    n = length(p)
    @inbounds for k in 1:n
        sr[k] = R[p[k]]
    end
    shifts = 0
    @inbounds for k in 2:n
        x = sr[k]; pk = p[k]; j = k - 1
        while j >= 1 && sr[j] > x
            sr[j+1] = sr[j]; p[j+1] = p[j]; j -= 1; shifts += 1
        end
        sr[j+1] = x; p[j+1] = pk
        if shifts > 40 * n
            STAT[4] += 1
            pp = sortperm(R); p .= pp
            for kk in 1:n; sr[kk] = R[p[kk]]; end
            return
        end
    end
end

function parseargs(line)
    d = Dict{String,String}()
    for tok in split(strip(line))
        kv = split(tok, "="; limit=2)
        length(kv) == 2 && (d[kv[1]] = kv[2])
    end
    return d
end
gf(d, k, def) = haskey(d, k) ? parse(Float64, d[k]) : def
gi(d, k, def) = haskey(d, k) ? parse(Int, d[k]) : def

function age(Om, OL, H0, a)
    OL > 0 ? 2 / (3 * sqrt(OL) * H0) * asinh(sqrt(OL / Om) * a^1.5) : 2 / (3 * H0) * a^1.5
end

function run_orbit(d)
    Mb = gf(d, "Mb", 1e10); eps = gf(d, "eps", 1e-3); rta = gf(d, "rta", 0.7); q = gf(d, "q", 0.1)
    norb = gf(d, "norb", 2000); rtol = gf(d, "rtol", 1e-10)
    c = Ctx(1, Mb, eps^2, 1.0, 0.0674, 1.0, 0.0, 0.0, Float64[], Float64[], Float64[], 0, 0.0, 1.0, false, 0)
    j2 = jsq(c, rta, q, 1.0)
    S = State(1); S.R[1] = rta; S.V[1] = 0.0; S.J2[1] = j2; S.TU[1] = 1; S.H[1] = 1e-6
    Phi(r) = -G * Mb / sqrt(r * r + eps^2)
    E(S) = 0.5 * S.V[1]^2 + 0.5 * S.J2[1] / S.R[1]^2 + Phi(S.R[1])
    E0 = E(S)
    a = 0.5 * (rta + q * rta)
    P = 2pi * sqrt(a^3 / (G * Mb))
    T = norb * P
    nchunk = 20; t = 0.0; maxdrift = 0.0
    for k in 1:nchunk
        advance!(c, S, 1, t, t + T / nchunk, q, rtol)
        t += T / nchunk
        maxdrift = max(maxdrift, abs(E(S) / E0 - 1))
    end
    return Dict("rp_over_rta" => S.RP[1] / rta, "drift_end" => E(S) / E0 - 1, "drift_max" => maxdrift,
                "steps" => STAT[1], "norb" => norb, "P_myr" => P * MYR)
end

function run_sim(d)
    t_start = time()
    fill!(STAT, 0)
    geom = d["geom"] == "exp" ? 2 : 1
    Mb = gf(d, "Mb", 1e10) * gf(d, "core", 1.0)
    h = gf(d, "h", 1.0); eps = gf(d, "eps", 1e-3)
    q = gf(d, "q", 0.1); N = gi(d, "N", 5000); Mout = gf(d, "Mout", 1e11)
    H0 = gf(d, "H0", 0.0674); Om = gf(d, "Om", 0.315); OL = gf(d, "OL", 0.685); Oc = gf(d, "Oc", 0.2655)
    Ob = gf(d, "Ob", Om - Oc)
    zi = gf(d, "zi", 100.0); dts = gf(d, "dt_myr", 1.0) / MYR; rtol = gf(d, "rtol", 1e-10)
    icf = gf(d, "icf", 1.0); jform = gi(d, "jform", 0)
    rlo = gf(d, "rlo", 0.1); rhi = gf(d, "rhi", 100.0); ng = gi(d, "ng", 155)
    out = d["out"]
    ai = 1 / (1 + zi)
    ti = age(Om, OL, H0, ai); t0 = age(Om, OL, H0, 1.0)
    etah = gf(d, "eta_h", 3e-4)
    aoft(t) = OL > 0 ? (Om / OL)^(1 / 3) * sinh(1.5 * sqrt(OL) * H0 * t)^(2 / 3) : (1.5 * H0 * t)^(2 / 3)
    Hoft(t) = (a = aoft(t); H0 * sqrt(Om / a^3 + OL))
    tb = [ti]
    let t = ti
        while etah / Hoft(t) < dts
            t += etah / Hoft(t); push!(tb, t)
        end
        nlate = ceil(Int, (t0 - t) / dts); dtl = (t0 - t) / nlate
        for k in 1:nlate
            push!(tb, t + k * dtl)
        end
        tb[end] = t0
    end
    nint = length(tb) - 1
    dtl = tb[end] - tb[end-1]
    cad2 = max(1, round(Int, 2.0 / MYR / dtl)); cad20 = max(1, round(Int, 20.0 / MYR / dtl))
    k400 = round(Int, 400.0 / MYR / dtl); k8000 = round(Int, 8000.0 / MYR / dtl)
    m = Mout / N
    rhoc0 = Oc * 3 * H0^2 / (8pi * G)
    Hai = H0 * sqrt(Om / ai^3 + OL)
    S = State(N)
    for i in 1:N
        Mi = (i - 0.5) * m
        r = ai * cbrt(3 * Mi / (4pi * rhoc0))
        S.R[i] = r; S.V[i] = icf * Hai * r; S.H[i] = 1e-3 * (tb[2] - tb[1])
    end
    B = State(N)
    Ms = [(k - 0.5) * m for k in 1:N]
    p = collect(1:N); sr = zeros(N); p2 = collect(1:N); sr2 = zeros(N)
    c = Ctx(geom, Mb, eps^2, h, H0, Om, OL, Ob, sr, sr2, Ms, N, ti, dtl, false, jform)
    resort!(sr, p, S.R)
    rg = [rlo * (rhi / rlo)^((j - 1) / (ng - 1)) for j in 1:ng]
    times = Float64[]; samp = Float64[]
    function do_sample(t)
        push!(times, t)
        for j in 1:ng
            push!(samp, mcp(c.rn, Ms, N, rg[j]))
        end
    end
    tlog = stderr
    for n in 0:nint-1
        tn = tb[n+1]; dt = tb[n+2] - tb[n+1]
        c.tn = tn; c.dt = dt
        # predictor: profile frozen at t_n
        c.usep = false
        copystate!(B, S)
        for i in 1:N
            advance!(c, B, i, tn, tn + dt, q, rtol)
        end
        copyto!(p2, p)
        resort!(sr2, p2, B.R)
        # corrector: linear interpolation in time between the profile at t_n and the predicted profile
        c.usep = true
        for i in 1:N
            advance!(c, S, i, tn, tn + dt, q, rtol)
        end
        c.usep = false
        resort!(sr, p, S.R)
        k = nint - (n + 1)
        if (k <= k400 && k % cad2 == 0) || (k <= k8000 && k % cad20 == 0)
            do_sample(tb[n+2])
        end
        if (n + 1) % 2000 == 0
            @printf(tlog, "  [%s] %d/%d intervals, %.0f s\n", d["out"], n + 1, nint, time() - t_start)
        end
    end
    open(out * ".final.bin", "w") do io
        write(io, S.R); write(io, S.V); write(io, S.J2); write(io, Float64.(S.TU)); write(io, S.RTA); write(io, S.RP)
    end
    open(out * ".times.bin", "w") do io; write(io, times); end
    open(out * ".samples.bin", "w") do io; write(io, samp); end
    open(out * ".rgrid.bin", "w") do io; write(io, rg); end
    open(out * ".meta.txt", "w") do io
        println(io, "N ", N); println(io, "m ", m); println(io, "Mout ", Mout); println(io, "nint ", nint)
        println(io, "t0 ", t0); println(io, "ti ", ti); println(io, "nsamp ", length(times)); println(io, "ng ", ng)
        println(io, "steps ", STAT[1]); println(io, "rejects ", STAT[2]); println(io, "refines ", STAT[3]); println(io, "resort_fallbacks ", STAT[4]); println(io, "vscale_fallbacks ", STAT[5])
        println(io, "seconds ", time() - t_start)
    end
end

function main()
    for line in eachline(ARGS[1])
        isempty(strip(line)) && continue
        d = parseargs(line)
        if get(d, "mode", "sim") == "orbit"
            res = run_orbit(d)
            open(d["out"] * ".orbit.txt", "w") do io
                for (k, v) in res; println(io, k, " ", v); end
            end
        else
            run_sim(d)
        end
    end
end
main()

// Live thin-disk N-body for one SPARC galaxy. Pure TypeScript, no DOM, so it can be tested headless.
//
// Physics (and its limits):
//  * The stellar disk is N particles sampled from Sigma_* = Upsilon_disk * SBdisk (SPARC); the gas is NOT live: SPARC's own tabulated gas contribution
//    Vgas(R) is used as a fixed axisymmetric Newtonian field.
//  * The Newtonian in-plane field of the live stars is computed on a grid by FFT convolution (zero-padded, so the box is isolated) with the kernel of a
//    layer of exponential vertical profile, scale height 0.196 R_d (SPARC's own thickness choice).
//  * 'law': the record's kernel is applied to the total Newtonian field, g = nu(gbar(R)/a0) g_N, with a0 fixed, where gbar(R) is the AZIMUTHALLY AVERAGED
//    magnitude of the Newtonian field at the particle's radius (recomputed every step). For an axisymmetric disc this is exactly the algebraic law the record fits
//    to SPARC. A pointwise nu(|g_N|) was tried first: it amplifies particle shot noise and is not curl-free, and it pumped angular momentum (+12% in 1 Gyr).
//    Even this radial form is not QUMOND (which solves a curl-free phantom field in 3D), so any bar/spiral behaviour here is indicative, not a result.
//  * 'halo': the Newtonian field plus a RIGID spherical halo whose in-plane field is fitted point by point to Vobs^2 - Vbar^2 (the standard picture).
//  * 'newton': baryons only.
// Units: kpc, km/s, Msun; time unit kpc/(km/s) = 0.9778 Gyr; G = 4.30091e-6 kpc (km/s)^2 / Msun.

export interface GalaxyData {
  name: string; D: number; Q: number; T: number; Rd: number; Vflat: number; Inc: number; L36: number; MHI: number; Mstar: number
  R: number[]; Vobs: number[]; eV: number[]; Vgas: number[]; Vdisk: number[]; Rf: number[]; ss: number[]
  chk: { star_frac_rms: number; law_rms_dex: number; law_tab_rms_dex: number }
}
export interface Kernel { log10y: number[]; nu: number[] }
export type Mode = 'law' | 'newton' | 'halo'
export const GYR_PER_UNIT = 0.9778

// ---------------------------------------------------------------- FFT
class FFT2 {
  M: number; rev: Uint32Array; cos: Float32Array; sin: Float32Array; tr: Float32Array; ti: Float32Array
  constructor(M: number) {
    this.M = M
    this.rev = new Uint32Array(M)
    const bits = Math.log2(M)
    for (let i = 0; i < M; i++) { let r = 0; for (let b = 0; b < bits; b++) if (i & (1 << b)) r |= 1 << (bits - 1 - b); this.rev[i] = r }
    this.cos = new Float32Array(M / 2); this.sin = new Float32Array(M / 2)
    for (let i = 0; i < M / 2; i++) { this.cos[i] = Math.cos((2 * Math.PI * i) / M); this.sin[i] = -Math.sin((2 * Math.PI * i) / M) }
    this.tr = new Float32Array(M); this.ti = new Float32Array(M)
  }
  /** in-place 1D transform of M complex values read with `stride` from offset `off` */
  private line(re: Float32Array, im: Float32Array, off: number, stride: number, inv: boolean) {
    const { M, rev, cos, sin, tr, ti } = this
    for (let i = 0; i < M; i++) { const j = off + rev[i] * stride; tr[i] = re[j]; ti[i] = im[j] }
    for (let len = 2; len <= M; len <<= 1) {
      const half = len >> 1, step = M / len
      for (let s = 0; s < M; s += len) {
        for (let k = 0, w = 0; k < half; k++, w += step) {
          const wr = cos[w], wi = inv ? -sin[w] : sin[w]
          const a = s + k, b = a + half
          const xr = tr[b] * wr - ti[b] * wi, xi = tr[b] * wi + ti[b] * wr
          tr[b] = tr[a] - xr; ti[b] = ti[a] - xi; tr[a] += xr; ti[a] += xi
        }
      }
    }
    for (let i = 0; i < M; i++) { const j = off + i * stride; re[j] = tr[i]; im[j] = ti[i] }
  }
  transform(re: Float32Array, im: Float32Array, inv: boolean) {
    const M = this.M
    for (let r = 0; r < M; r++) this.line(re, im, r * M, 1, inv)
    for (let c = 0; c < M; c++) this.line(re, im, c, M, inv)
    if (inv) { const s = 1 / (M * M); for (let i = 0; i < re.length; i++) { re[i] *= s; im[i] *= s } }
  }
}

// ---------------------------------------------------------------- helpers
const G = 4.30091e-6
function interp(xs: number[] | Float32Array | Float64Array, ys: number[] | Float32Array | Float64Array, x: number) {
  const n = xs.length
  if (x <= xs[0]) return ys[0]
  if (x >= xs[n - 1]) return ys[n - 1]
  let lo = 0, hi = n - 1
  while (hi - lo > 1) { const m = (lo + hi) >> 1; if (xs[m] > x) hi = m; else lo = m }
  const u = (x - xs[lo]) / (xs[hi] - xs[lo]); return ys[lo] * (1 - u) + ys[hi] * u
}
function mulberry32(a: number) { return () => { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296 } }
function gauss(rnd: () => number) { let u = 0; while (u < 1e-12) u = rnd(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * rnd()) }

export interface Options { N?: number; np?: number; Q?: number; seed?: number }

export class DiskSim {
  gal: GalaxyData; mode: Mode; N: number; M: number; L: number; h: number; np: number; Q: number
  a0: number; nuLogY: Float64Array; nuVal: Float64Array
  x: Float32Array; y: Float32Array; vx: Float32Array; vy: Float32Array; mp: number; x0: Float32Array; y0: Float32Array
  t = 0; steps = 0
  // grid fields
  private fft: FFT2; private kxr: Float32Array; private kxi: Float32Array; private kyr: Float32Array; private kyi: Float32Array
  private re: Float32Array; private im: Float32Array
  private gsx: Float32Array; private gsy: Float32Array        // live-star Newtonian field on the N x N grid
  private gx: Float32Array; private gy: Float32Array          // total field felt by the stars
  private fixX: Float32Array; private fixY: Float32Array      // fixed gas field (Newtonian)
  private hx: Float32Array; private hy: Float32Array          // rigid halo field (halo mode)
  vc0: { R: number[]; V: number[] } = { R: [], V: [] }        // initial equilibrium circular speed
  dt = 0.002
  R99 = 0

  constructor(gal: GalaxyData, kernel: Kernel, a0: number, mode: Mode, opt: Options = {}) {
    this.gal = gal; this.mode = mode; this.N = opt.N ?? 128; this.M = 2 * this.N; this.np = opt.np ?? 60000; this.Q = opt.Q ?? 1.8
    this.a0 = a0
    this.nuLogY = Float64Array.from(kernel.log10y); this.nuVal = Float64Array.from(kernel.nu)
    const { N, M } = this
    // stellar radius containing 99% of the mass sets the box
    const Rf = gal.Rf, ss = gal.ss
    const cum = new Float64Array(Rf.length); let acc = 0
    for (let i = 0; i < Rf.length; i++) { acc += ss[i] * Rf[i] * (i ? Rf[i] - Rf[i - 1] : Rf[0]); cum[i] = acc }
    let k99 = 0; while (k99 < Rf.length - 1 && cum[k99] < 0.99 * acc) k99++
    this.R99 = Rf[k99]
    this.L = Math.max(2.7 * this.R99, 4 * gal.Rd); this.h = this.L / N
    this.fft = new FFT2(M)
    const MM = M * M
    this.re = new Float32Array(MM); this.im = new Float32Array(MM)
    this.kxr = new Float32Array(MM); this.kxi = new Float32Array(MM); this.kyr = new Float32Array(MM); this.kyi = new Float32Array(MM)
    this.gsx = new Float32Array(N * N); this.gsy = new Float32Array(N * N); this.gx = new Float32Array(N * N); this.gy = new Float32Array(N * N)
    this.fixX = new Float32Array(N * N); this.fixY = new Float32Array(N * N); this.hx = new Float32Array(N * N); this.hy = new Float32Array(N * N)
    this.x = new Float32Array(this.np); this.y = new Float32Array(this.np); this.vx = new Float32Array(this.np); this.vy = new Float32Array(this.np)
    this.mp = gal.Mstar / this.np
    this.x0 = new Float32Array(this.np); this.y0 = new Float32Array(this.np)
    this.buildKernel()
    this.buildFixedFields()
    this.initParticles(opt.seed ?? 1)
  }

  nu(y: number) { return interp(this.nuLogY, this.nuVal, Math.log10(Math.max(y, 1e-6))) }

  private buildKernel() {
    const { N, M, h } = this, z0 = Math.max(0.196 * this.gal.Rd, 0.4 * h)
    // Fq(r) = int_0^inf e^-t (r^2 + z0^2 t^2)^(-3/2) dt  (in-plane force from an exponential-vertical-profile layer, per unit G m dx)
    const nt = 600, tmax = 30, ts = new Float64Array(nt), wt = new Float64Array(nt)
    for (let i = 0; i < nt; i++) { ts[i] = (i / (nt - 1)) * tmax; wt[i] = Math.exp(-ts[i]) * (tmax / (nt - 1)) * (i === 0 || i === nt - 1 ? 0.5 : 1) }
    const nr = 1600, rmin = h / 60, rmax = h * Math.SQRT2 * N * 1.05, lr0 = Math.log(rmin), lr1 = Math.log(rmax)
    const rs = new Float64Array(nr), fq = new Float64Array(nr)
    for (let i = 0; i < nr; i++) {
      const r = Math.exp(lr0 + (i / (nr - 1)) * (lr1 - lr0)); rs[i] = r; let s = 0
      for (let j = 0; j < nt; j++) s += wt[j] * Math.pow(r * r + z0 * z0 * ts[j] * ts[j], -1.5)
      fq[i] = s
    }
    const Fq = (r: number) => { const u = (Math.log(Math.max(r, rmin)) - lr0) / (lr1 - lr0) * (nr - 1); const i = Math.min(nr - 2, Math.max(0, Math.floor(u))); const f = u - i; return fq[i] * (1 - f) + fq[i + 1] * f }
    for (let dy = -(N - 1); dy <= N - 1; dy++) {
      for (let dx = -(N - 1); dx <= N - 1; dx++) {
        if (dx === 0 && dy === 0) continue
        const r = h * Math.hypot(dx, dy), f = -G * Fq(r), idx = ((dy + M) % M) * M + ((dx + M) % M)
        this.kxr[idx] = f * h * dx; this.kyr[idx] = f * h * dy       // g = m (x_target - x_source) * (-G Fq)
      }
    }
    this.fft.transform(this.kxr, this.kxi, false); this.fft.transform(this.kyr, this.kyi, false)
  }

  private cellXY(i: number) { return -this.L / 2 + (i + 0.5) * this.h }

  /** fixed axisymmetric gas field from SPARC's tabulated Vgas(R) */
  private buildFixedFields() {
    const { N, gal } = this, R = gal.R, g2 = gal.Vgas.map((v, i) => (Math.sign(v) * v * v) / R[i])        // signed inward magnitude
    const Rl = R[R.length - 1]
    for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) {
      const x = this.cellXY(i), y = this.cellXY(j), r = Math.hypot(x, y) + 1e-9
      let g: number
      if (r <= R[0]) g = g2[0] * (r / R[0]); else if (r >= Rl) g = g2[R.length - 1] * (Rl / r) ** 2; else g = interp(R, g2, r)
      this.fixX[j * N + i] = -g * (x / r); this.fixY[j * N + i] = -g * (y / r)
    }
  }

  /** Newtonian field of a mass grid (Msun per cell) on the N x N grid, into (ox, oy) */
  private poisson(mass: Float32Array, ox: Float32Array, oy: Float32Array) {
    const { N, M, re, im, kxr, kxi, kyr, kyi } = this
    re.fill(0); im.fill(0)
    for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) re[j * M + i] = mass[j * N + i]
    this.fft.transform(re, im, false)
    // pack gx + i gy: ghat = mhat * (Kxhat + i Kyhat)
    for (let k = 0; k < M * M; k++) {
      const a = re[k], b = im[k]
      const px = a * kxr[k] - b * kxi[k], qx = a * kxi[k] + b * kxr[k]
      const py = a * kyr[k] - b * kyi[k], qy = a * kyi[k] + b * kyr[k]
      re[k] = px - qy; im[k] = qx + py
    }
    this.fft.transform(re, im, true)
    for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) { ox[j * N + i] = re[j * M + i]; oy[j * N + i] = im[j * M + i] }
  }

  private mass = new Float32Array(0)
  private depositParticles() {
    const { N, h, L } = this
    if (this.mass.length !== N * N) this.mass = new Float32Array(N * N)
    const m = this.mass; m.fill(0)
    for (let p = 0; p < this.np; p++) {
      const u = (this.x[p] + L / 2) / h - 0.5, v = (this.y[p] + L / 2) / h - 0.5
      const i = Math.floor(u), j = Math.floor(v)
      if (i < 0 || j < 0 || i >= N - 1 || j >= N - 1) continue
      const fx = u - i, fy = v - j, mp = this.mp
      m[j * N + i] += mp * (1 - fx) * (1 - fy); m[j * N + i + 1] += mp * fx * (1 - fy)
      m[(j + 1) * N + i] += mp * (1 - fx) * fy; m[(j + 1) * N + i + 1] += mp * fx * fy
    }
    return m
  }

  /** total field (vector) from live-star field + fixed gas, with the chosen law */
  private nuBin = new Float64Array(96)
  private totalField() {
    const { N, a0, mode } = this
    const nb = this.nuBin.length, rmax = this.L / 2
    if (mode === 'law') {                                              // radial boost from the azimuthally averaged inward Newtonian field
      const sum = new Float64Array(nb), cnt = new Float64Array(nb)
      for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) {
        const x = this.cellXY(i), y = this.cellXY(j), r = Math.hypot(x, y); if (r >= rmax || r < 1e-9) continue
        const k = j * N + i, b = Math.floor((r / rmax) * nb)
        sum[b] += Math.hypot(this.gsx[k] + this.fixX[k], this.gsy[k] + this.fixY[k]); cnt[b]++
      }
      for (let b = 0; b < nb; b++) this.nuBin[b] = this.nu(Math.max(cnt[b] ? sum[b] / cnt[b] : 0, 1e-12) / a0)
    }
    for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) {
      const k = j * N + i
      let ax = this.gsx[k] + this.fixX[k], ay = this.gsy[k] + this.fixY[k]
      if (mode === 'law') {
        const r = Math.hypot(this.cellXY(i), this.cellXY(j)), f = this.nuBin[Math.min(nb - 1, Math.floor((r / rmax) * nb))]
        ax *= f; ay *= f
      } else if (mode === 'halo') { ax += this.hx[k]; ay += this.hy[k] }
      this.gx[k] = ax; this.gy[k] = ay
    }
  }

  private force() {
    this.poisson(this.depositParticles(), this.gsx, this.gsy)
    this.totalField()
  }

  /** azimuthally averaged inward acceleration profile of a grid field on nb radial bins */
  private radialProfile(ax: Float32Array, ay: Float32Array, nb: number, rmax: number) {
    const { N } = this, sum = new Float64Array(nb), cnt = new Float64Array(nb)
    for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) {
      const x = this.cellXY(i), y = this.cellXY(j), r = Math.hypot(x, y); if (r >= rmax || r < 1e-9) continue
      const b = Math.floor((r / rmax) * nb), gin = -(x * ax[j * N + i] + y * ay[j * N + i]) / r
      sum[b] += gin; cnt[b]++
    }
    const R: number[] = [], g: number[] = []
    for (let b = 0; b < nb; b++) if (cnt[b] > 0) { R.push(((b + 0.5) / nb) * rmax); g.push(sum[b] / cnt[b]) }
    return { R, g }
  }

  private initParticles(seed: number) {
    const { N, L, h, gal } = this, rnd = mulberry32(seed)
    // 1. smooth-disk Newtonian field -> equilibrium circular speed
    const smooth = new Float32Array(N * N)
    for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) {
      const r = Math.hypot(this.cellXY(i), this.cellXY(j)); smooth[j * N + i] = r > gal.Rf[gal.Rf.length - 1] ? 0 : interp(gal.Rf, gal.ss, r) * 1e6 * h * h
    }
    const sx = new Float32Array(N * N), sy = new Float32Array(N * N)
    this.poisson(smooth, sx, sy)
    const rmax = L / 2, nb = 64
    const star = this.radialProfile(sx, sy, nb, rmax)
    const gasP = this.radialProfile(this.fixX, this.fixY, nb, rmax)
    const nbR = star.R.length
    const gN = star.g.map((g, i) => g + gasP.g[i])
    // rigid halo for halo mode: fitted point by point so the equilibrium curve equals the observed one
    const Vh2 = new Float64Array(gal.R.length)
    for (let i = 0; i < gal.R.length; i++) {
      const gb = interp(star.R, gN, gal.R[i]); Vh2[i] = Math.max(gal.Vobs[i] ** 2 - gal.R[i] * gb, 0)
    }
    const gh = (r: number) => { const R = gal.R, Rl = R[R.length - 1]; if (r <= R[0]) return (Vh2[0] / R[0]) * (r / R[0]); if (r >= Rl) return Vh2[R.length - 1] / r; return interp(R, Array.from(Vh2).map((v, i) => v / R[i]), r) }
    if (this.mode === 'halo') {
      const ghTab = gal.R.map((_, i) => Vh2[i] / gal.R[i])
      for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) {
        const x = this.cellXY(i), y = this.cellXY(j), r = Math.hypot(x, y) + 1e-9, R = gal.R, Rl = R[R.length - 1]
        const g = r <= R[0] ? ghTab[0] * (r / R[0]) : r >= Rl ? Vh2[R.length - 1] / r : interp(R, ghTab, r)
        this.hx[j * N + i] = -g * (x / r); this.hy[j * N + i] = -g * (y / r)
      }
    }
    void gh
    const vc2 = star.R.map((R, i) => {
      const g = gN[i]
      if (this.mode === 'law') return R * this.nu(g / this.a0) * g
      if (this.mode === 'halo') { const gg = interp(gal.R, Array.from(Vh2).map((v, k) => v / gal.R[k]), R); return R * (g + (R <= gal.R[gal.R.length - 1] ? gg : Vh2[gal.R.length - 1] / R)) }
      return R * g
    })
    const Vc = vc2.map(v => Math.sqrt(Math.max(v, 0)))
    this.vc0 = { R: star.R.slice(), V: Vc.slice() }
    // 2. epicyclic frequency, Toomre-set dispersion
    const kappa = new Float64Array(nbR), boost = new Float64Array(nbR)
    for (let i = 0; i < nbR; i++) {
      const a = Math.max(0, i - 2), b = Math.min(nbR - 1, i + 2), R = star.R[i]
      const dV = (Vc[b] - Vc[a]) / (star.R[b] - star.R[a])
      kappa[i] = Math.sqrt(Math.max(2 * (Vc[i] / R) * (Vc[i] / R + dV), 0.1 * (Vc[i] / R) ** 2))
      boost[i] = this.mode === 'law' ? Math.max(1, vc2[i] / Math.max(R * star.g[i], 1e-9)) : 1
    }
    // 3. sample radii from the stellar mass profile
    const Rf = gal.Rf, cum = new Float64Array(Rf.length); let acc = 0
    for (let i = 0; i < Rf.length; i++) { acc += gal.ss[i] * Rf[i] * (i ? Rf[i] - Rf[i - 1] : Rf[0]); cum[i] = acc }
    for (let p = 0; p < this.np; p++) {
      const u = rnd() * acc; let lo = 0, hi = Rf.length - 1
      while (hi - lo > 1) { const m = (lo + hi) >> 1; if (cum[m] > u) hi = m; else lo = m }
      const f = (u - cum[lo]) / Math.max(cum[hi] - cum[lo], 1e-30), R = Math.min(Rf[lo] + f * (Rf[hi] - Rf[lo]), this.R99 * 1.6)
      const th = 2 * Math.PI * rnd()
      const bin = Math.min(nbR - 1, Math.max(0, Math.floor((R / rmax) * nb))), vc = interp(star.R, Vc, R), kap = interp(star.R, Array.from(kappa), R)
      const sigS = interp(Rf, gal.ss, R) * 1e6                                                   // Msun/kpc^2
      let sR = (this.Q * 3.36 * G * sigS * interp(star.R, Array.from(boost), R)) / Math.max(kap, 1e-6)
      sR = Math.min(Math.max(sR, 5), 0.5 * vc)
      const sP = (sR * kap) / Math.max(2 * vc / R, 1e-6)
      const vR = sR * gauss(rnd), vT = vc + Math.min(sP, 0.5 * vc) * gauss(rnd) * 0.7 - (sR * sR) / (2 * Math.max(vc, 1))
      const c = Math.cos(th), s = Math.sin(th)
      this.x[p] = R * c; this.y[p] = R * s
      this.vx[p] = vR * c - vT * s; this.vy[p] = vR * s + vT * c
      void bin
    }
    this.x0.set(this.x); this.y0.set(this.y)
    // timestep from the fastest orbit outside the softening scale
    let wmax = 0
    for (let i = 0; i < nbR; i++) if (star.R[i] > 1.5 * h) wmax = Math.max(wmax, Vc[i] / star.R[i])
    this.dt = Math.min(0.006, 0.045 / Math.max(wmax, 1e-3))
    this.force()
  }

  /** one kick-drift-kick leapfrog step */
  step() {
    const { N, h, L, np, dt } = this
    const kick = (f: number) => {
      for (let p = 0; p < np; p++) {
        const u = (this.x[p] + L / 2) / h - 0.5, v = (this.y[p] + L / 2) / h - 0.5
        let i = Math.floor(u), j = Math.floor(v)
        if (i < 0 || j < 0 || i >= N - 1 || j >= N - 1) { this.vx[p] *= 0.9999; continue }
        const fx = u - i, fy = v - j, a = (1 - fx) * (1 - fy), b = fx * (1 - fy), c = (1 - fx) * fy, d = fx * fy
        const k0 = j * N + i, k1 = k0 + 1, k2 = k0 + N, k3 = k2 + 1
        this.vx[p] += f * (a * this.gx[k0] + b * this.gx[k1] + c * this.gx[k2] + d * this.gx[k3])
        this.vy[p] += f * (a * this.gy[k0] + b * this.gy[k1] + c * this.gy[k2] + d * this.gy[k3])
      }
    }
    kick(0.5 * dt)
    for (let p = 0; p < np; p++) { this.x[p] += this.vx[p] * dt; this.y[p] += this.vy[p] * dt }
    this.force()
    kick(0.5 * dt)
    this.t += dt; this.steps++
  }

  /** current azimuthal-mean circular speed from the field the stars feel (law applied) */
  curve(nb = 28) {
    const rmax = Math.min(this.L / 2, this.gal.Rf[this.gal.Rf.length - 1] * 1.1), p = this.radialProfile(this.gx, this.gy, nb, rmax)
    return { R: p.R, V: p.R.map((R, i) => Math.sqrt(Math.max(R * p.g[i], 0))) }
  }
  /** the Newtonian curve of the current stars plus gas (no law, no halo) */
  newtonianCurve(nb = 28) {
    const { N } = this, ax = new Float32Array(N * N), ay = new Float32Array(N * N)
    for (let k = 0; k < N * N; k++) { ax[k] = this.gsx[k] + this.fixX[k]; ay[k] = this.gsy[k] + this.fixY[k] }
    const rmax = Math.min(this.L / 2, this.gal.Rf[this.gal.Rf.length - 1] * 1.1), p = this.radialProfile(ax, ay, nb, rmax)
    return { R: p.R, V: p.R.map((R, i) => Math.sqrt(Math.max(R * p.g[i], 0))) }
  }
  angularMomentum() { let s = 0; for (let p = 0; p < this.np; p++) s += this.x[p] * this.vy[p] - this.y[p] * this.vx[p]; return s * this.mp }
  halfMassRadius() { const r = new Float32Array(this.np); for (let p = 0; p < this.np; p++) r[p] = Math.hypot(this.x[p], this.y[p]); r.sort(); return r[this.np >> 1] }
}

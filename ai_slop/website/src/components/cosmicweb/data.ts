import { useEffect, useState } from 'react'

export interface RunRecord {
  tag: string
  sigma8: number
  k: number[]
  P: number[]
  runtime_s: number
  nsteps: number
  z_i: number
  vol_on?: number
  mass_on?: number
  vol_on_knot?: number
  vol_on_fil?: number
  mass_on_knot?: number
  mass_on_fil?: number
}

export interface HaloInfo {
  id: string
  rank: number
  centre: number[]
  n: number
  n_control_sphere: number
  mass_msun_h: number
  mass_control_msun_h: number
  moved_median_kpc_h: number
  moved_rms_kpc_h: number
  frac_switch_on: number
  n_shown: number
  bytes: number
  centre_s0: number[]
  centre_offset_kpc_h: number
  prof_edges: number[]
  prof_fw: number[]
  prof_s0: number[]
}

export interface CosmicMeta {
  N: number
  L: number
  log_lo: number
  log_hi: number
  halo_r: number
  halo_scale: number
  halo_stride: number
  layers: number[]
  m_particle_msun_h: number
  rec: { res: RunRecord; s0: RunRecord }
  checks: Record<string, { mass: number; mean: number; sigma8_grid: number; sigma8_record: number; rel: number; count_sum: number; count_max: number; frac_cells_empty: number; frac_particles_in_cells_gt_127: number }>
  stats: {
    corr_log_density_128: number
    rms_dlog10_128: number
    frac_cells_within_0p1dex_128: number
    s8_ratio: number
    pk_max_dev: number
    by_density_128: Record<string, { frac_cells: number; mean_dlog10: number; rms_dlog10: number }>
    frac_volume_rho_gt_100_512: Record<string, number>
    frac_mass_rho_gt_100_512: Record<string, number>
  }
  particle_cmp: {
    n: number
    median_mpc_h: number
    p90_mpc_h: number
    p99_mpc_h: number
    p999_mpc_h: number
    frac_gt_cell: number
    cell_mpc_h: number
    by_framework_cell_count: Record<string, { n: number; frac: number; median_mpc_h: number; p90_mpc_h: number }>
  }
  halos: HaloInfo[]
  bytes: Record<string, number>
}

export const BASE = '/data/cosmic512'
export const NC = 512

/** decoded particles-per-cell for each uint8 code (c for c <= 127, else 127 * 2^((code - 127) / 16)) */
export const COUNT_DECODE = (() => {
  const t = new Float32Array(256)
  for (let k = 0; k < 256; k++) t[k] = k <= 127 ? k : 127 * Math.pow(2, (k - 127) / 16)
  return t
})()

async function fetchGz(name: string, len: number): Promise<Uint8Array> {
  const buf = await (await fetch(`${BASE}/${name}`)).arrayBuffer()
  const raw = new Uint8Array(buf)
  if (raw.length === len) return raw
  if (raw.length > 2 && raw[0] === 0x1f && raw[1] === 0x8b) {
    if (typeof DecompressionStream === 'undefined') throw new Error('This browser cannot unpack the data (needs DecompressionStream).')
    const stream = new Blob([raw]).stream().pipeThrough(new DecompressionStream('gzip'))
    const out = new Uint8Array(await new Response(stream).arrayBuffer())
    if (out.length === len) return out
  }
  throw new Error(`Unexpected size for ${name}`)
}

/** 128^3 volume (log10 density, 0..255 over [log_lo, log_hi]) */
export const fetchPreview = (name: string) => fetchGz(name, 128 ** 3)

/** an 8-bit grayscale PNG atlas decoded to one byte per pixel (the red channel) */
export function loadAtlas(name: string, w: number, h: number): Promise<Uint8Array> {
  return new Promise((resolve, reject) => {
    const img = new Image()
    img.onload = () => {
      const c = document.createElement('canvas'); c.width = w; c.height = h
      const g = c.getContext('2d', { willReadFrequently: true })!
      g.drawImage(img, 0, 0)
      const px = g.getImageData(0, 0, w, h).data
      const out = new Uint8Array(w * h)
      for (let i = 0; i < out.length; i++) out[i] = px[i * 4]
      resolve(out)
    }
    img.onerror = () => reject(new Error(`could not load ${name}`))
    img.src = `${BASE}/${name}`
  })
}

export interface TimelineMeta {
  frames: number
  n: number
  cols: number
  a: number[]
  z: number[]
  k: number[]
  sigma8: { res: number[]; s0: number[] }
  P: { res: number[][]; s0: number[][] }
  range: { res: number[][]; s0: number[][] }
  diag: { vol_on: number[]; mass_on: number[] }
  slab_mpc_h: number[]
  runtime_s: { res: number; s0: number }
  validation: { name: string; value: number; limit: number; ok: boolean; note: string }[]
  halo: { n: number; scale: number; centre: number[]; n_sphere_res: number; n_sphere_s0: number; mass_msun_h: number; particle_mass_msun_h: number }
  bytes: Record<string, number>
}

const INFERNO = ['#000004', '#160b39', '#420a68', '#6a176e', '#932667', '#bc3754', '#dd513a', '#f37819', '#fca50a', '#f6d746', '#fcffa4']
const hex = (h: string) => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)]

/** 256 x RGBA lookup table: density colour map (inferno-like) */
export function densityLut(): Uint8Array {
  const out = new Uint8Array(256 * 4)
  const st = INFERNO.map(hex)
  for (let i = 0; i < 256; i++) {
    const t = (i / 255) * (st.length - 1), j = Math.min(Math.floor(t), st.length - 2), u = t - j
    for (let c = 0; c < 3; c++) out[i * 4 + c] = Math.round(st[j][c] * (1 - u) + st[j + 1][c] * u)
    out[i * 4 + 3] = 255
  }
  return out
}

/** 256 x RGBA diverging table for a signed quantity in [-1, 1]: blue (control denser) - dark - orange (framework denser) */
export function divergingLut(): Uint8Array {
  const out = new Uint8Array(256 * 4)
  const neg = hex('#4aa3ff'), mid = hex('#101420'), pos = hex('#ff7a3d')
  for (let i = 0; i < 256; i++) {
    const s = (i / 255) * 2 - 1, a = Math.abs(s), end = s < 0 ? neg : pos
    for (let c = 0; c < 3; c++) out[i * 4 + c] = Math.round(mid[c] * (1 - a) + end[c] * a)
    out[i * 4 + 3] = 255
  }
  return out
}

export const fmtBytes = (b: number) => (b >= 1e6 ? `${(b / 1e6).toFixed(b >= 1e7 ? 0 : 1)} MB` : `${Math.round(b / 1e3)} kB`)
export const sumBytes = (b: Record<string, number>, prefix: string) => Object.entries(b).filter(([k]) => k.startsWith(prefix)).reduce((s, [, v]) => s + v, 0)
export const fmtMass = (m: number) => { const e = Math.floor(Math.log10(m)); return `${(m / 10 ** e).toFixed(1)}×10${String(e).split('').map(c => '⁰¹²³⁴⁵⁶⁷⁸⁹'[+c] ?? '⁻').join('')}` }

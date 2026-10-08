// What the visitor's machine can reasonably be asked to do. Used by the heavy visualisations to pick light defaults and to avoid autoplay.
// Browsers expose only coarse hints (deviceMemory is missing in Safari and Firefox, hardwareConcurrency is often capped), so this errs on the cautious side.
export interface Device { low: boolean; reduce: boolean; coarse: boolean; saveData: boolean; cores: number; mem: number }

export function getDevice(): Device {
  if (typeof window === 'undefined') return { low: false, reduce: false, coarse: false, saveData: false, cores: 8, mem: 8 }
  const nav = navigator as Navigator & { deviceMemory?: number; connection?: { saveData?: boolean } }
  const cores = nav.hardwareConcurrency ?? 4, mem = nav.deviceMemory ?? 8
  const coarse = window.matchMedia?.('(pointer: coarse)').matches ?? false
  const reduce = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false
  const saveData = !!nav.connection?.saveData
  return { low: coarse || cores <= 4 || mem <= 4 || saveData, reduce, coarse, saveData, cores, mem }
}

/** pixel ratio cap for a canvas: 1 on weak devices, 1.5 otherwise (2x costs 1.8x the pixels for little visible gain on these plots) */
export const maxPixelRatio = (d: Device) => Math.min(window.devicePixelRatio || 1, d.low ? 1 : 1.5)

/** decorative motion (auto-rotation, autoplay) is off for weak devices and for people who ask for reduced motion */
export const allowAutoMotion = (d: Device) => !d.low && !d.reduce

/** lose-context handling shared by every WebGL canvas: stop the page from hanging on to a dead context and say so */
export function guardContext(canvas: HTMLCanvasElement, onLost: () => void) {
  const h = (e: Event) => { e.preventDefault(); onLost() }
  canvas.addEventListener('webglcontextlost', h)
  return () => canvas.removeEventListener('webglcontextlost', h)
}

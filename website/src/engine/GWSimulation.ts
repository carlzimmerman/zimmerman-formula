/**
 * =============================================================================
 * GWSimulation.ts - GRAVITATIONAL WAVE SIMULATION ENGINE
 * =============================================================================
 *
 * Directive QQQ: 3D Lattice Wave Shader
 * Directive RRR: Wave-Rider Camera Sequence
 * Directive SSS: Simulation UI Trigger
 *
 * Features:
 * - GW190521: Most massive BBH merger (85 + 66 M☉ → 142 M☉)
 * - Real-time lattice displacement visualization
 * - "Ride the wave" camera from merger site to Earth
 * - Physics-accurate strain and propagation
 *
 * Z² Framework v11.1.0
 * =============================================================================
 */

import * as THREE from 'three';
import { MPC, GPC, celestialToCartesian } from './CosmicConstants';

// =============================================================================
// GW190521 EVENT DATA
// =============================================================================

export interface GWEvent {
  id: string;
  name: string;

  // Location (celestial coordinates)
  ra_deg: number;           // Right Ascension
  dec_deg: number;          // Declination
  distance_Mpc: number;     // Luminosity distance

  // Source parameters
  mass1_solar: number;      // Primary black hole mass
  mass2_solar: number;      // Secondary black hole mass
  finalMass_solar: number;  // Remnant mass

  // Wave parameters
  peakFrequency_Hz: number; // Peak GW frequency
  peakStrain: number;       // Peak dimensionless strain at Earth
  duration_s: number;       // Ring-down duration

  // Position in km (computed)
  position_km: [number, number, number];
}

export const GW190521: GWEvent = {
  id: 'GW190521',
  name: 'GW190521 (IMBH Merger)',

  // Location - LIGO/Virgo localization
  ra_deg: 102.5,            // ~6h 50m
  dec_deg: 34.0,            // +34°
  distance_Mpc: 5300,       // 5.3 Gpc luminosity distance

  // Masses (most massive BBH merger detected)
  mass1_solar: 85,
  mass2_solar: 66,
  finalMass_solar: 142,     // First intermediate-mass black hole

  // Wave properties at Earth
  peakFrequency_Hz: 60,     // Peak frequency
  peakStrain: 2.4e-22,      // Peak strain h
  duration_s: 0.1,          // Very short merger

  // Position computed from celestial coords
  position_km: celestialToCartesian(102.5, 34.0, 5300 * MPC),
};

// Other notable events for future expansion
export const GW_EVENTS: GWEvent[] = [
  GW190521,
  {
    id: 'GW150914',
    name: 'GW150914 (First Detection)',
    ra_deg: 123.5,
    dec_deg: -30.0,
    distance_Mpc: 440,
    mass1_solar: 36,
    mass2_solar: 29,
    finalMass_solar: 62,
    peakFrequency_Hz: 150,
    peakStrain: 1.0e-21,
    duration_s: 0.2,
    position_km: celestialToCartesian(123.5, -30.0, 440 * MPC),
  },
  {
    id: 'GW170817',
    name: 'GW170817 (BNS + Kilonova)',
    ra_deg: 197.5,
    dec_deg: -23.4,
    distance_Mpc: 40,
    mass1_solar: 1.46,
    mass2_solar: 1.27,
    finalMass_solar: 2.7,
    peakFrequency_Hz: 1500,
    peakStrain: 5.0e-22,
    duration_s: 100,
    position_km: celestialToCartesian(197.5, -23.4, 40 * MPC),
  },
];

// =============================================================================
// LATTICE WAVE SHADER UNIFORMS
// =============================================================================

export interface GWShaderUniforms {
  time: { value: number };
  epicenter: { value: THREE.Vector3 };
  waveSpeed: { value: number };        // c in scene units
  waveRadius: { value: number };       // Current wave front radius
  strain: { value: number };           // Dimensionless strain amplitude
  frequency: { value: number };        // Wave frequency
  decayLength: { value: number };      // 1/r decay scale
  latticeScale: { value: number };     // Grid cell size
  showPolarization: { value: boolean }; // Show + and × modes
}

export function createGWShaderUniforms(): GWShaderUniforms {
  return {
    time: { value: 0 },
    epicenter: { value: new THREE.Vector3(0, 0, 0) },
    waveSpeed: { value: 1.0 },
    waveRadius: { value: 0 },
    strain: { value: 0.3 },            // Exaggerated for visibility
    frequency: { value: 0.5 },
    decayLength: { value: 100 },
    latticeScale: { value: 0.5 },
    showPolarization: { value: true },
  };
}

// =============================================================================
// VERTEX SHADER - LATTICE DISPLACEMENT
// =============================================================================

export const gwVertexShader = /* glsl */`
  uniform float time;
  uniform vec3 epicenter;
  uniform float waveSpeed;
  uniform float waveRadius;
  uniform float strain;
  uniform float frequency;
  uniform float decayLength;
  uniform float latticeScale;
  uniform bool showPolarization;

  varying vec3 vPosition;
  varying vec3 vNormal;
  varying float vStrain;
  varying float vDistFromWave;

  // Plus (+) polarization displacement
  vec3 plusMode(vec3 pos, float r, float phase) {
    float h = strain * sin(phase) / (1.0 + r / decayLength);

    // h+ stretches x, compresses y (or vice versa)
    vec3 displacement = vec3(
      pos.x * h,
      -pos.y * h,
      0.0
    );
    return displacement;
  }

  // Cross (×) polarization displacement
  vec3 crossMode(vec3 pos, float r, float phase) {
    float h = strain * cos(phase) / (1.0 + r / decayLength);

    // h× stretches along x=y diagonal
    vec3 displacement = vec3(
      pos.y * h * 0.5,
      pos.x * h * 0.5,
      0.0
    );
    return displacement;
  }

  void main() {
    vPosition = position;
    vNormal = normal;

    // Distance from epicenter
    vec3 toEpicenter = position - epicenter;
    float r = length(toEpicenter);

    // Distance from current wave front
    float distFromWave = r - waveRadius;
    vDistFromWave = distFromWave;

    // Wave packet envelope (Gaussian pulse)
    float waveWidth = 5.0;
    float envelope = exp(-distFromWave * distFromWave / (2.0 * waveWidth * waveWidth));

    // Only show strain near the wave front
    vStrain = envelope * strain / (1.0 + r / decayLength);

    // Phase at this point
    float phase = 2.0 * 3.14159 * frequency * (r - waveRadius);

    // Combined polarization displacement
    vec3 displacement = vec3(0.0);

    if (showPolarization) {
      displacement += plusMode(position, r, phase);
      displacement += crossMode(position, r, phase + 1.5708); // 90° offset
    }

    // Apply displacement scaled by envelope
    vec3 displaced = position + displacement * envelope;

    gl_Position = projectionMatrix * modelViewMatrix * vec4(displaced, 1.0);
  }
`;

// =============================================================================
// FRAGMENT SHADER - STRAIN VISUALIZATION
// =============================================================================

export const gwFragmentShader = /* glsl */`
  uniform float time;
  uniform float waveRadius;

  varying vec3 vPosition;
  varying vec3 vNormal;
  varying float vStrain;
  varying float vDistFromWave;

  void main() {
    // Base lattice color
    vec3 baseColor = vec3(0.1, 0.2, 0.3);

    // Strain visualization - blue for compression, red for expansion
    vec3 strainColor;
    if (vStrain > 0.0) {
      strainColor = mix(baseColor, vec3(0.0, 0.8, 1.0), vStrain * 3.0); // Cyan for expansion
    } else {
      strainColor = mix(baseColor, vec3(1.0, 0.2, 0.5), -vStrain * 3.0); // Magenta for compression
    }

    // Wave front highlight
    float waveFrontGlow = exp(-abs(vDistFromWave) * 2.0);
    vec3 waveColor = vec3(1.0, 0.9, 0.3); // Golden wave front

    // Combine
    vec3 finalColor = mix(strainColor, waveColor, waveFrontGlow * 0.5);

    // Grid lines
    float gridLine = 0.0;
    vec3 gridPos = fract(vPosition * 2.0);
    float lineWidth = 0.05;
    if (gridPos.x < lineWidth || gridPos.y < lineWidth || gridPos.z < lineWidth) {
      gridLine = 0.3;
    }

    finalColor += vec3(gridLine);

    // Alpha based on distance from wave
    float alpha = 0.3 + waveFrontGlow * 0.7;

    gl_FragColor = vec4(finalColor, alpha);
  }
`;

// =============================================================================
// WAVE RIDER CAMERA SEQUENCE (Directive RRR)
// =============================================================================

export interface WaveRiderPhase {
  name: string;
  description: string;
  duration_s: number;

  // Camera position relative to wave front
  cameraPosition: 'merger' | 'behind_wave' | 'with_wave' | 'earth';
  cameraOffset_km?: [number, number, number];

  // What to show
  showLattice: boolean;
  showStrainHUD: boolean;
  timeScale: number;  // Real seconds per simulation second
}

export const WAVE_RIDER_SEQUENCE: WaveRiderPhase[] = [
  {
    name: 'Merger',
    description: 'GW190521: 85 + 66 M☉ black holes spiral and merge at 5.3 Gpc',
    duration_s: 3,
    cameraPosition: 'merger',
    showLattice: true,
    showStrainHUD: true,
    timeScale: 1e-3, // Slow-mo the merger
  },
  {
    name: 'Wave Launch',
    description: 'Gravitational waves expand at c, carrying 8 M☉ of pure energy',
    duration_s: 4,
    cameraPosition: 'behind_wave',
    cameraOffset_km: [0, 0, -1000 * MPC],
    showLattice: true,
    showStrainHUD: true,
    timeScale: 1e12, // Time-lapse cosmic scale
  },
  {
    name: 'Cosmic Propagation',
    description: 'Riding with the wave through intergalactic space...',
    duration_s: 6,
    cameraPosition: 'with_wave',
    cameraOffset_km: [100 * MPC, 0, 0],
    showLattice: true,
    showStrainHUD: true,
    timeScale: 1e15, // Extreme time-lapse
  },
  {
    name: 'Earth Arrival',
    description: 'After 7 billion years, LIGO detects strain h = 2.4×10⁻²² on May 21, 2019',
    duration_s: 4,
    cameraPosition: 'earth',
    showLattice: true,
    showStrainHUD: true,
    timeScale: 1, // Real-time at Earth
  },
];

// =============================================================================
// SIMULATION STATE
// =============================================================================

export interface GWSimulationState {
  isRunning: boolean;
  currentEvent: GWEvent | null;
  currentPhase: number;
  phaseProgress: number;  // 0-1
  elapsedTime_s: number;  // Simulation time
  waveRadius_km: number;  // Current wave front distance from source

  // Camera state
  cameraPosition_km: [number, number, number];
  cameraTarget_km: [number, number, number];

  // HUD data
  currentStrain: number;
  distanceToEarth_km: number;
  lightYearsRemaining: number;
}

export const INITIAL_GW_STATE: GWSimulationState = {
  isRunning: false,
  currentEvent: null,
  currentPhase: 0,
  phaseProgress: 0,
  elapsedTime_s: 0,
  waveRadius_km: 0,
  cameraPosition_km: [0, 0, 0],
  cameraTarget_km: [0, 0, 0],
  currentStrain: 0,
  distanceToEarth_km: 0,
  lightYearsRemaining: 0,
};

// =============================================================================
// PHYSICS UTILITIES
// =============================================================================

const C_KM_PER_S = 299792.458;           // Speed of light in km/s
const YEAR_S = 365.25 * 24 * 3600;       // Seconds per year
const LY_KM = C_KM_PER_S * YEAR_S;       // Light year in km

/**
 * Calculate GW strain at distance from source.
 * h ~ M * (G/c²) / r for quadrupole radiation
 */
export function calculateStrain(event: GWEvent, distance_km: number): number {
  // Strain scales as 1/r
  const sourceDistance = event.distance_Mpc * MPC;
  const ratio = sourceDistance / Math.max(distance_km, 1);
  return event.peakStrain * ratio;
}

/**
 * Calculate time for wave to reach Earth from source.
 */
export function travelTimeToEarth(event: GWEvent): number {
  const distance_km = event.distance_Mpc * MPC;
  return distance_km / C_KM_PER_S; // seconds
}

/**
 * Convert simulation time to wave front position.
 */
export function waveRadiusAtTime(elapsedTime_s: number): number {
  return elapsedTime_s * C_KM_PER_S;
}

/**
 * Calculate camera position for "wave riding" effect.
 */
export function getWaveRiderCamera(
  event: GWEvent,
  phase: WaveRiderPhase,
  waveRadius_km: number,
  progress: number
): { position: [number, number, number]; target: [number, number, number] } {
  const [ex, ey, ez] = event.position_km;
  const earthPos: [number, number, number] = [0, 0, 0];

  // Direction from event to Earth
  const dx = -ex;
  const dy = -ey;
  const dz = -ez;
  const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
  const dirX = dx / dist;
  const dirY = dy / dist;
  const dirZ = dz / dist;

  switch (phase.cameraPosition) {
    case 'merger':
      // Near the merger site, looking at it
      return {
        position: [ex + 500 * MPC, ey + 300 * MPC, ez + 400 * MPC],
        target: event.position_km,
      };

    case 'behind_wave':
      // Behind the expanding wave, looking toward Earth
      const behindDist = waveRadius_km * 0.8;
      return {
        position: [
          ex + dirX * behindDist + 200 * MPC,
          ey + dirY * behindDist + 100 * MPC,
          ez + dirZ * behindDist,
        ],
        target: earthPos,
      };

    case 'with_wave':
      // Riding alongside the wave front
      const perpX = -dirY;
      const perpY = dirX;
      const waveFrontDist = waveRadius_km;
      return {
        position: [
          ex + dirX * waveFrontDist + perpX * 500 * MPC,
          ey + dirY * waveFrontDist + perpY * 500 * MPC,
          ez + dirZ * waveFrontDist + 300 * MPC,
        ],
        target: [
          ex + dirX * waveFrontDist,
          ey + dirY * waveFrontDist,
          ez + dirZ * waveFrontDist,
        ],
      };

    case 'earth':
      // At Earth, wave approaching
      const earthViewDist = Math.max(dist - waveRadius_km, 10 * MPC);
      return {
        position: [1 * MPC, 0.5 * MPC, 0.8 * MPC],
        target: [ex + dirX * (dist - earthViewDist), ey + dirY * (dist - earthViewDist), ez + dirZ * (dist - earthViewDist)],
      };

    default:
      return { position: [0, 0, 0], target: [0, 0, 0] };
  }
}

// =============================================================================
// THREE.JS SHADER MATERIAL FACTORY
// =============================================================================

export function createGWShaderMaterial(): THREE.ShaderMaterial {
  // Type assertion needed for THREE.ShaderMaterial uniforms
  const uniforms = createGWShaderUniforms() as unknown as { [uniform: string]: THREE.IUniform };

  return new THREE.ShaderMaterial({
    uniforms,
    vertexShader: gwVertexShader,
    fragmentShader: gwFragmentShader,
    transparent: true,
    side: THREE.DoubleSide,
    depthWrite: false,
  });
}

// =============================================================================
// LATTICE GEOMETRY FACTORY
// =============================================================================

export function createLatticeGeometry(
  size: number,
  resolution: number
): THREE.BufferGeometry {
  const geometry = new THREE.BoxGeometry(size, size, size, resolution, resolution, resolution);

  // Convert to wireframe for lattice effect
  const edges = new THREE.EdgesGeometry(geometry);

  return edges;
}

/**
 * Create a 3D grid of points for lattice visualization.
 */
export function createLatticePointCloud(
  size: number,
  pointsPerAxis: number
): THREE.BufferGeometry {
  const count = pointsPerAxis ** 3;
  const positions = new Float32Array(count * 3);
  const colors = new Float32Array(count * 3);

  const step = size / (pointsPerAxis - 1);
  const offset = size / 2;

  let i = 0;
  for (let x = 0; x < pointsPerAxis; x++) {
    for (let y = 0; y < pointsPerAxis; y++) {
      for (let z = 0; z < pointsPerAxis; z++) {
        positions[i * 3] = x * step - offset;
        positions[i * 3 + 1] = y * step - offset;
        positions[i * 3 + 2] = z * step - offset;

        // Neutral blue-white color
        colors[i * 3] = 0.6;
        colors[i * 3 + 1] = 0.7;
        colors[i * 3 + 2] = 0.9;

        i++;
      }
    }
  }

  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

  return geometry;
}

// =============================================================================
// EXPORT
// =============================================================================

export default {
  GW190521,
  GW_EVENTS,
  WAVE_RIDER_SEQUENCE,
  createGWShaderMaterial,
  createLatticeGeometry,
  createLatticePointCloud,
  calculateStrain,
  travelTimeToEarth,
  waveRadiusAtTime,
  getWaveRiderCamera,
};

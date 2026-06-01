/**
 * =============================================================================
 * Z² Digital Twin Engine - Main Export
 * =============================================================================
 *
 * Work-Order HHH: Float64 Camera-Relative Engine
 *
 * This module provides a complete multi-scale rendering engine capable of
 * smoothly visualizing from planetary surfaces (10³ km) to the cosmic
 * horizon (10²³ km) - a span of 20 orders of magnitude.
 *
 * KEY ARCHITECTURE:
 * - All positions stored in Float64 (JavaScript Number) on CPU
 * - Camera-relative transformation to Float32 for GPU
 * - Dynamic LOD with geometry ↔ label swapping
 * - Adaptive near/far planes per scale
 *
 * Z² Framework v11.1.0
 * =============================================================================
 */

// Core engine
export {
  FloatingOriginController,
  Vector3_F64,
  getFloatingOrigin,
  resetFloatingOrigin,
} from './FloatingOrigin';

// Constants and conversions
export {
  // Distance units (all in km)
  KM, M, AU, LY, PC, KPC, MPC, GPC,

  // Z² locked parameters
  Z2,

  // Solar System data
  SUN,
  PLANETS,

  // Milky Way data
  MILKY_WAY,

  // Local Group
  LOCAL_GROUP,

  // Z² Vertices
  Z2_VERTICES,

  // Major structures
  MAJOR_STRUCTURES,

  // LOD thresholds
  LOD_THRESHOLDS,

  // Utilities
  getLODLevel,
  celestialToCartesian,
  formatDistance,
} from './CosmicConstants';

export type { LODLevel } from './CosmicConstants';

// State management
export {
  useUniverseStore,
  useCameraState,
  useVisibility,
  useTourState,
  useLODLevel,
  useSceneScale,
  useGWSimulation,
  TOUR_WAYPOINTS,
} from './UniverseState';

export type { CameraState, VisibilityFlags, TourState, UniverseStore } from './UniverseState';

// LOD system
export {
  LODManager,
  RenderMode,
  LOD_CONFIGS,
  aggregateLabels,
} from './LODManager';

export type { CosmicObjectType, AggregatedLabel } from './LODManager';

// React hooks
export {
  useFloatingOrigin,
  useFloatingCamera,
  useFloatingOrbitControls,
  useCinematicTour,
} from './useFloatingOrigin';

export type { UseFloatingOriginResult } from './useFloatingOrigin';

// GW Simulation (Directives QQQ, RRR, SSS)
export {
  GW190521,
  GW_EVENTS,
  WAVE_RIDER_SEQUENCE,
  INITIAL_GW_STATE,
  createGWShaderMaterial,
  createLatticeGeometry,
  createLatticePointCloud,
  calculateStrain,
  travelTimeToEarth,
  waveRadiusAtTime,
  getWaveRiderCamera,
  gwVertexShader,
  gwFragmentShader,
  createGWShaderUniforms,
} from './GWSimulation';

export type {
  GWEvent,
  GWShaderUniforms,
  WaveRiderPhase,
  GWSimulationState,
} from './GWSimulation';

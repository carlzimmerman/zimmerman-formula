/**
 * =============================================================================
 * UniverseState.ts - ZUSTAND STORE FOR UNIVERSE STATE
 * =============================================================================
 *
 * Global state management for the Digital Twin.
 * Stores camera position, LOD level, visible objects, and UI state.
 *
 * All positions are stored in Float64 (km) for precision.
 *
 * Z² Framework v11.1.0
 * Work-Order HHH: Float64 Camera-Relative Engine
 * =============================================================================
 */

import { create } from 'zustand';
import { subscribeWithSelector } from 'zustand/middleware';
import {
  AU, KPC, MPC, GPC,
  getLODLevel,
  LOD_THRESHOLDS,
  type LODLevel,
  PLANETS,
  Z2_VERTICES,
  MILKY_WAY,
  formatDistance,
} from './CosmicConstants';
import { Vector3_F64, FloatingOriginController } from './FloatingOrigin';
import {
  GW190521,
  WAVE_RIDER_SEQUENCE,
  INITIAL_GW_STATE,
  waveRadiusAtTime,
  getWaveRiderCamera,
  type GWEvent,
  type GWSimulationState,
} from './GWSimulation';

// =============================================================================
// TYPES
// =============================================================================

export interface CameraState {
  // Absolute position in km (Float64 precision via JavaScript Number)
  position: [number, number, number];
  target: [number, number, number];

  // Derived values
  distanceFromOrigin: number;
  lodLevel: LODLevel;
  sceneScale: number;
  nearPlane: number;
  farPlane: number;
}

export interface VisibilityFlags {
  solarSystem: boolean;
  milkyWay: boolean;
  localGroup: boolean;
  clusters: boolean;
  cosmicWeb: boolean;
  z2Vertices: boolean;
  z2Domain: boolean;
  labels: boolean;
}

export interface TourState {
  isRunning: boolean;
  currentWaypoint: number;
  waypointText: string;
  progress: number;
}

export interface UniverseStore {
  // Core state
  camera: CameraState;
  visibility: VisibilityFlags;
  tour: TourState;

  // GW Simulation state (Directives QQQ, RRR, SSS)
  gwSimulation: GWSimulationState;

  // UI state
  isRotating: boolean;
  showDebug: boolean;

  // Floating origin controller reference
  floatingOrigin: FloatingOriginController | null;

  // Actions
  initFloatingOrigin: (initialPos?: [number, number, number]) => void;
  setCameraPosition: (pos: [number, number, number]) => void;
  setCameraTarget: (target: [number, number, number]) => void;
  zoom: (factor: number) => void;
  setVisibility: (flags: Partial<VisibilityFlags>) => void;
  toggleVisibility: (key: keyof VisibilityFlags) => void;
  setRotating: (rotating: boolean) => void;
  setShowDebug: (show: boolean) => void;

  // Tour actions
  startTour: () => void;
  stopTour: () => void;
  setTourWaypoint: (index: number, text: string) => void;
  setTourProgress: (progress: number) => void;

  // GW Simulation actions
  startGWSimulation: (event?: GWEvent) => void;
  stopGWSimulation: () => void;
  updateGWSimulation: (deltaTime: number) => void;
  setGWPhase: (phase: number) => void;

  // Computed getters
  getScenePosition: (absolutePos: [number, number, number]) => [number, number, number];
  getSceneSize: (size_km: number) => number;
  shouldRenderGeometry: (objectType: string) => boolean;
}

// =============================================================================
// INITIAL STATE
// =============================================================================

// Start at COSMIC scale to show the full 20.6 Gpc fundamental domain
const INITIAL_CAMERA_POSITION: [number, number, number] = [
  22 * GPC,  // 22 Gpc from origin - sees entire Z² box
  16 * GPC,
  22 * GPC,
];

const INITIAL_CAMERA_TARGET: [number, number, number] = [0, 0, 0];

const initialDistance = Math.sqrt(
  INITIAL_CAMERA_POSITION[0] ** 2 +
  INITIAL_CAMERA_POSITION[1] ** 2 +
  INITIAL_CAMERA_POSITION[2] ** 2
);

const initialLOD = getLODLevel(initialDistance);

const INITIAL_CAMERA_STATE: CameraState = {
  position: INITIAL_CAMERA_POSITION,
  target: INITIAL_CAMERA_TARGET,
  distanceFromOrigin: initialDistance,
  lodLevel: initialLOD,
  sceneScale: LOD_THRESHOLDS[initialLOD].sceneScale_km,
  nearPlane: LOD_THRESHOLDS[initialLOD].nearPlane,
  farPlane: LOD_THRESHOLDS[initialLOD].farPlane,
};

const INITIAL_VISIBILITY: VisibilityFlags = {
  solarSystem: true,
  milkyWay: true,
  localGroup: true,
  clusters: true,
  cosmicWeb: true,
  z2Vertices: true,
  z2Domain: true,
  labels: true,
};

const INITIAL_TOUR: TourState = {
  isRunning: false,
  currentWaypoint: 0,
  waypointText: '',
  progress: 0,
};

// =============================================================================
// STORE CREATION
// =============================================================================

export const useUniverseStore = create<UniverseStore>()(
  subscribeWithSelector((set, get) => ({
    // Initial state
    camera: INITIAL_CAMERA_STATE,
    visibility: INITIAL_VISIBILITY,
    tour: INITIAL_TOUR,
    gwSimulation: INITIAL_GW_STATE,
    isRotating: false,
    showDebug: false,
    floatingOrigin: null,

    // Initialize floating origin controller
    initFloatingOrigin: (initialPos) => {
      const controller = new FloatingOriginController(initialPos || INITIAL_CAMERA_POSITION);
      set({ floatingOrigin: controller });

      // Sync camera state
      const state = controller.getDebugState();
      set({
        camera: {
          position: state.position_km,
          target: state.target_km,
          distanceFromOrigin: state.distance_km,
          lodLevel: state.lodLevel,
          sceneScale: controller.sceneScale,
          nearPlane: controller.nearPlane,
          farPlane: controller.farPlane,
        },
      });
    },

    // Set camera position
    setCameraPosition: (pos) => {
      const { floatingOrigin } = get();
      if (!floatingOrigin) return;

      floatingOrigin.setCameraPosition(pos[0], pos[1], pos[2]);

      const distance = Math.sqrt(pos[0] ** 2 + pos[1] ** 2 + pos[2] ** 2);
      const lodLevel = getLODLevel(distance);

      set({
        camera: {
          ...get().camera,
          position: pos,
          distanceFromOrigin: distance,
          lodLevel,
          sceneScale: LOD_THRESHOLDS[lodLevel].sceneScale_km,
          nearPlane: LOD_THRESHOLDS[lodLevel].nearPlane,
          farPlane: LOD_THRESHOLDS[lodLevel].farPlane,
        },
      });
    },

    // Set camera target
    setCameraTarget: (target) => {
      const { floatingOrigin } = get();
      if (!floatingOrigin) return;

      floatingOrigin.setCameraTarget(target[0], target[1], target[2]);
      set({
        camera: {
          ...get().camera,
          target,
        },
      });
    },

    // Zoom in/out
    zoom: (factor) => {
      const { floatingOrigin } = get();
      if (!floatingOrigin) return;

      floatingOrigin.zoom(factor);

      const state = floatingOrigin.getDebugState();
      set({
        camera: {
          position: state.position_km,
          target: state.target_km,
          distanceFromOrigin: state.distance_km,
          lodLevel: state.lodLevel,
          sceneScale: floatingOrigin.sceneScale,
          nearPlane: floatingOrigin.nearPlane,
          farPlane: floatingOrigin.farPlane,
        },
      });
    },

    // Visibility controls
    setVisibility: (flags) => {
      set({
        visibility: {
          ...get().visibility,
          ...flags,
        },
      });
    },

    toggleVisibility: (key) => {
      set({
        visibility: {
          ...get().visibility,
          [key]: !get().visibility[key],
        },
      });
    },

    // UI state
    setRotating: (rotating) => set({ isRotating: rotating }),
    setShowDebug: (show) => set({ showDebug: show }),

    // Tour controls
    startTour: () => set({ tour: { ...get().tour, isRunning: true, currentWaypoint: 0, progress: 0 } }),
    stopTour: () => set({ tour: { ...get().tour, isRunning: false, waypointText: '' } }),
    setTourWaypoint: (index, text) => set({ tour: { ...get().tour, currentWaypoint: index, waypointText: text } }),
    setTourProgress: (progress) => set({ tour: { ...get().tour, progress } }),

    // GW Simulation controls (Directives QQQ, RRR, SSS)
    startGWSimulation: (event = GW190521) => {
      const distance_km = Math.sqrt(
        event.position_km[0] ** 2 +
        event.position_km[1] ** 2 +
        event.position_km[2] ** 2
      );

      set({
        gwSimulation: {
          isRunning: true,
          currentEvent: event,
          currentPhase: 0,
          phaseProgress: 0,
          elapsedTime_s: 0,
          waveRadius_km: 0,
          cameraPosition_km: [...event.position_km] as [number, number, number],
          cameraTarget_km: [0, 0, 0],
          currentStrain: event.peakStrain,
          distanceToEarth_km: distance_km,
          lightYearsRemaining: distance_km / 9.461e12, // km per light year
        },
      });
    },

    stopGWSimulation: () => set({ gwSimulation: INITIAL_GW_STATE }),

    updateGWSimulation: (deltaTime: number) => {
      const { gwSimulation, floatingOrigin } = get();
      if (!gwSimulation.isRunning || !gwSimulation.currentEvent) return;

      const phase = WAVE_RIDER_SEQUENCE[gwSimulation.currentPhase];
      if (!phase) {
        // Simulation complete
        set({ gwSimulation: INITIAL_GW_STATE });
        return;
      }

      // Update progress within current phase
      const newPhaseProgress = gwSimulation.phaseProgress + deltaTime / phase.duration_s;

      if (newPhaseProgress >= 1) {
        // Move to next phase
        const nextPhase = gwSimulation.currentPhase + 1;
        if (nextPhase >= WAVE_RIDER_SEQUENCE.length) {
          // Simulation complete
          set({ gwSimulation: INITIAL_GW_STATE });
          return;
        }

        set({
          gwSimulation: {
            ...gwSimulation,
            currentPhase: nextPhase,
            phaseProgress: 0,
          },
        });
      } else {
        // Update within current phase
        const newElapsedTime = gwSimulation.elapsedTime_s + deltaTime * phase.timeScale;
        const newWaveRadius = waveRadiusAtTime(newElapsedTime);

        // Get camera position for this phase
        const cameraInfo = getWaveRiderCamera(
          gwSimulation.currentEvent,
          phase,
          newWaveRadius,
          newPhaseProgress
        );

        // Calculate distance remaining to Earth
        const distanceToEarth = Math.sqrt(
          gwSimulation.currentEvent.position_km[0] ** 2 +
          gwSimulation.currentEvent.position_km[1] ** 2 +
          gwSimulation.currentEvent.position_km[2] ** 2
        ) - newWaveRadius;

        set({
          gwSimulation: {
            ...gwSimulation,
            phaseProgress: newPhaseProgress,
            elapsedTime_s: newElapsedTime,
            waveRadius_km: newWaveRadius,
            cameraPosition_km: cameraInfo.position,
            cameraTarget_km: cameraInfo.target,
            distanceToEarth_km: Math.max(0, distanceToEarth),
            lightYearsRemaining: Math.max(0, distanceToEarth / 9.461e12),
          },
        });

        // Update the floating origin camera if available
        if (floatingOrigin) {
          floatingOrigin.setCameraPosition(cameraInfo.position[0], cameraInfo.position[1], cameraInfo.position[2]);
          floatingOrigin.setCameraTarget(cameraInfo.target[0], cameraInfo.target[1], cameraInfo.target[2]);
        }
      }
    },

    setGWPhase: (phase) => set({
      gwSimulation: {
        ...get().gwSimulation,
        currentPhase: phase,
        phaseProgress: 0,
      },
    }),

    // Computed: Transform absolute position to scene coordinates
    getScenePosition: (absolutePos) => {
      const { floatingOrigin } = get();
      if (!floatingOrigin) {
        return [0, 0, 0];
      }

      const scenePos = floatingOrigin.toSceneCoordinatesArray(absolutePos);
      return [scenePos.x, scenePos.y, scenePos.z];
    },

    // Computed: Transform size to scene units
    getSceneSize: (size_km) => {
      const { floatingOrigin } = get();
      if (!floatingOrigin) return 0;
      return floatingOrigin.toSceneSize(size_km);
    },

    // Computed: Should we render 3D geometry for this object type?
    shouldRenderGeometry: (objectType) => {
      const { camera } = get();

      switch (objectType) {
        case 'planet':
          // Only render planet geometry when within 100 AU
          return camera.lodLevel === 'PLANETARY';

        case 'star':
          // Render star geometry within stellar range
          return camera.lodLevel === 'PLANETARY' || camera.lodLevel === 'STELLAR';

        case 'galaxy':
          // Render galaxy geometry within galactic/cluster range
          return camera.lodLevel === 'GALACTIC' || camera.lodLevel === 'CLUSTER';

        case 'cluster':
        case 'supercluster':
          // Render at cluster/cosmic scale
          return camera.lodLevel === 'CLUSTER' || camera.lodLevel === 'COSMIC';

        case 'z2_vertex':
        case 'z2_domain':
          // Always render Z² framework elements (as geometry or labels)
          return true;

        default:
          return true;
      }
    },
  }))
);

// =============================================================================
// SELECTOR HOOKS
// =============================================================================

export const useCameraState = () => useUniverseStore((state) => state.camera);
export const useVisibility = () => useUniverseStore((state) => state.visibility);
export const useTourState = () => useUniverseStore((state) => state.tour);
export const useLODLevel = () => useUniverseStore((state) => state.camera.lodLevel);
export const useSceneScale = () => useUniverseStore((state) => state.camera.sceneScale);
export const useGWSimulation = () => useUniverseStore((state) => state.gwSimulation);

// Re-export GW types
export type { GWEvent, GWSimulationState } from './GWSimulation';

// =============================================================================
// TOUR WAYPOINTS (in km)
// =============================================================================

export const TOUR_WAYPOINTS = [
  {
    name: 'Sun',
    position: [3 * AU, 2 * AU, 3 * AU] as [number, number, number],
    target: [0, 0, 0] as [number, number, number],
    duration: 5,
    text: 'The Sun — Our star, 4.6 billion years old',
  },
  {
    name: 'Inner Solar System',
    position: [15 * AU, 8 * AU, 12 * AU] as [number, number, number],
    target: [0, 0, 0] as [number, number, number],
    duration: 5,
    text: 'Inner Solar System — Mercury, Venus, Earth, Mars',
  },
  {
    name: 'Outer Solar System',
    position: [60 * AU, 30 * AU, 50 * AU] as [number, number, number],
    target: [0, 0, 0] as [number, number, number],
    duration: 5,
    text: 'Outer Solar System — Jupiter, Saturn, Uranus, Neptune, Pluto',
  },
  {
    name: 'Milky Way',
    position: [50 * KPC, 25 * KPC, 40 * KPC] as [number, number, number],
    target: [0, 0, 0] as [number, number, number],
    duration: 6,
    text: 'The Milky Way — 200 billion stars, 26.8 kpc radius',
  },
  {
    name: 'Local Group',
    position: [2 * MPC, 1 * MPC, 1.5 * MPC] as [number, number, number],
    target: [0, 0, 0] as [number, number, number],
    duration: 5,
    text: 'Local Group — 80+ galaxies including Andromeda',
  },
  {
    name: 'Cosmic Web',
    position: [500 * MPC, 300 * MPC, 400 * MPC] as [number, number, number],
    target: [100 * MPC, 50 * MPC, 100 * MPC] as [number, number, number],
    duration: 6,
    text: 'Cosmic Web — Filaments, clusters, and voids emerge',
  },
  {
    name: 'DESI Survey',
    position: [3 * GPC, 2 * GPC, -2 * GPC] as [number, number, number],
    target: [0, 0, 0] as [number, number, number],
    duration: 7,
    text: 'DESI DR1 — 5.7M galaxies, r = 0.9986 NGC-SGC correlation',
  },
  {
    name: 'V1 Shapley',
    position: [10 * GPC, 6 * GPC, 7 * GPC] as [number, number, number],
    target: Z2_VERTICES[0].position_km,
    duration: 8,
    text: 'V1: Shapley Supercluster — Topological vertex',
  },
  {
    name: 'V3 CMB Cold Spot',
    position: [-4 * GPC, 8 * GPC, 9 * GPC] as [number, number, number],
    target: Z2_VERTICES[2].position_km,
    duration: 8,
    text: 'V3: CMB Cold Spot — Matched circles at 5.7σ',
  },
  {
    name: 'Full Domain',
    position: [22 * GPC, 16 * GPC, 22 * GPC] as [number, number, number],
    target: [0, 0, 0] as [number, number, number],
    duration: 8,
    text: 'T³/Z₂ Fundamental Domain — L_c = 20.6 Gpc, Ω_m = 6/19',
  },
];

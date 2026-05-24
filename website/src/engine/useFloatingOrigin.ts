/**
 * =============================================================================
 * useFloatingOrigin.ts - REACT HOOK FOR FLOATING ORIGIN SYSTEM
 * =============================================================================
 *
 * This hook bridges the FloatingOriginController with React-Three-Fiber.
 * It handles:
 * - Initializing the controller
 * - Syncing camera state with Zustand
 * - Providing camera-relative transform functions
 * - Managing orbit controls in Float64 space
 *
 * Z² Framework v11.1.0
 * Work-Order HHH: Float64 Camera-Relative Engine
 * =============================================================================
 */

import { useEffect, useRef, useCallback, useMemo } from 'react';
import { useThree, useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { useUniverseStore, useCameraState, TOUR_WAYPOINTS } from './UniverseState';
import { FloatingOriginController, Vector3_F64 } from './FloatingOrigin';
import { LOD_THRESHOLDS, formatDistance, type LODLevel } from './CosmicConstants';
import { LODManager, RenderMode, type CosmicObjectType } from './LODManager';

// =============================================================================
// HOOK RETURN TYPE
// =============================================================================

export interface UseFloatingOriginResult {
  // Transform functions
  toScenePosition: (pos_km: [number, number, number]) => THREE.Vector3;
  toSceneSize: (size_km: number) => number;

  // LOD helpers
  getRenderMode: (type: CosmicObjectType, pos_km: [number, number, number], size_km: number) => RenderMode;
  shouldShowLabel: (type: CosmicObjectType, pos_km: [number, number, number]) => boolean;
  getTransitionOpacity: (type: CosmicObjectType, pos_km: [number, number, number], mode: RenderMode) => number;

  // Camera state
  cameraDistance_km: number;
  lodLevel: LODLevel;
  sceneScale: number;
  formattedDistance: string;

  // Near/far planes for dynamic camera
  nearPlane: number;
  farPlane: number;

  // Controller reference (for advanced usage)
  controller: FloatingOriginController | null;
}

// =============================================================================
// MAIN HOOK
// =============================================================================

export function useFloatingOrigin(): UseFloatingOriginResult {
  const { camera } = useThree();
  const controllerRef = useRef<FloatingOriginController | null>(null);

  // Zustand state
  const cameraState = useCameraState();
  const initFloatingOrigin = useUniverseStore((s) => s.initFloatingOrigin);
  const setCameraPosition = useUniverseStore((s) => s.setCameraPosition);
  const floatingOrigin = useUniverseStore((s) => s.floatingOrigin);

  // Initialize controller on mount
  useEffect(() => {
    initFloatingOrigin();
  }, [initFloatingOrigin]);

  // Keep ref in sync
  useEffect(() => {
    controllerRef.current = floatingOrigin;
  }, [floatingOrigin]);

  // ==========================================================================
  // TRANSFORM FUNCTIONS
  // ==========================================================================

  const toScenePosition = useCallback(
    (pos_km: [number, number, number]): THREE.Vector3 => {
      if (!controllerRef.current) {
        return new THREE.Vector3(0, 0, 0);
      }
      return controllerRef.current.toSceneCoordinatesArray(pos_km);
    },
    []
  );

  const toSceneSize = useCallback(
    (size_km: number): number => {
      if (!controllerRef.current) return 0;
      return controllerRef.current.toSceneSize(size_km);
    },
    []
  );

  // ==========================================================================
  // LOD HELPERS
  // ==========================================================================

  const getRenderMode = useCallback(
    (type: CosmicObjectType, pos_km: [number, number, number], size_km: number): RenderMode => {
      if (!controllerRef.current) return RenderMode.HIDDEN;

      const camPos = controllerRef.current.cameraPosition;
      const objPos = Vector3_F64.fromArray(pos_km);
      const distance = camPos.distanceTo(objPos);

      // Calculate approximate screen size
      const sceneSize = size_km / controllerRef.current.sceneScale;
      const sceneDistance = distance / controllerRef.current.sceneScale;
      const angularSize = sceneSize / Math.max(sceneDistance, 0.001);
      const screenPixels = angularSize * 500; // Approximate based on FOV

      return LODManager.getRenderMode(type, distance, size_km, screenPixels);
    },
    []
  );

  const shouldShowLabel = useCallback(
    (type: CosmicObjectType, pos_km: [number, number, number]): boolean => {
      if (!controllerRef.current) return false;

      const camPos = controllerRef.current.cameraPosition;
      const objPos = Vector3_F64.fromArray(pos_km);
      const distance = camPos.distanceTo(objPos);

      return LODManager.shouldShowLabel(type, distance);
    },
    []
  );

  const getTransitionOpacity = useCallback(
    (type: CosmicObjectType, pos_km: [number, number, number], mode: RenderMode): number => {
      if (!controllerRef.current) return 0;

      const camPos = controllerRef.current.cameraPosition;
      const objPos = Vector3_F64.fromArray(pos_km);
      const distance = camPos.distanceTo(objPos);

      return LODManager.getTransitionOpacity(type, distance, mode);
    },
    []
  );

  // ==========================================================================
  // MEMOIZED VALUES
  // ==========================================================================

  const formattedDistance = useMemo(
    () => formatDistance(cameraState.distanceFromOrigin),
    [cameraState.distanceFromOrigin]
  );

  // ==========================================================================
  // RETURN
  // ==========================================================================

  return {
    toScenePosition,
    toSceneSize,
    getRenderMode,
    shouldShowLabel,
    getTransitionOpacity,
    cameraDistance_km: cameraState.distanceFromOrigin,
    lodLevel: cameraState.lodLevel,
    sceneScale: cameraState.sceneScale,
    formattedDistance,
    nearPlane: cameraState.nearPlane,
    farPlane: cameraState.farPlane,
    controller: floatingOrigin,
  };
}

// =============================================================================
// CAMERA SYNC HOOK
// =============================================================================

/**
 * Hook to sync Three.js camera with floating origin system.
 * Must be used inside Canvas.
 */
export function useFloatingCamera() {
  const { camera } = useThree();
  const floatingOrigin = useUniverseStore((s) => s.floatingOrigin);
  const cameraState = useCameraState();

  // Update Three.js camera near/far based on LOD
  useEffect(() => {
    if (camera instanceof THREE.PerspectiveCamera) {
      camera.near = cameraState.nearPlane;
      camera.far = cameraState.farPlane;
      camera.updateProjectionMatrix();
    }
  }, [camera, cameraState.nearPlane, cameraState.farPlane]);

  // In floating origin system, camera is always near origin looking at target
  useFrame(() => {
    if (!floatingOrigin) return;

    // Camera position in scene coordinates (always small numbers)
    const scenePos = floatingOrigin.getCameraScenePosition();
    camera.position.set(scenePos.x, scenePos.y, scenePos.z);

    // Look at origin (target in scene space)
    camera.lookAt(0, 0, 0);
  });
}

// =============================================================================
// ORBIT CONTROLS ADAPTER HOOK
// =============================================================================

/**
 * Adapts standard OrbitControls to work with the floating origin system.
 * Intercepts control changes and converts them to Float64 camera movements.
 */
export function useFloatingOrbitControls(
  controlsRef: React.RefObject<any>,
  enabled: boolean = true
) {
  const floatingOrigin = useUniverseStore((s) => s.floatingOrigin);
  const setCameraPosition = useUniverseStore((s) => s.setCameraPosition);
  const zoom = useUniverseStore((s) => s.zoom);

  const lastPosition = useRef(new THREE.Vector3());
  const lastTarget = useRef(new THREE.Vector3());

  useFrame(() => {
    if (!controlsRef.current || !floatingOrigin || !enabled) return;

    const controls = controlsRef.current;
    const currentPosition = controls.object.position.clone();
    const currentTarget = controls.target.clone();

    // Detect if controls have moved
    if (!currentPosition.equals(lastPosition.current)) {
      // Calculate delta in scene space
      const delta = currentPosition.clone().sub(lastPosition.current);

      // Convert to km and apply to floating origin
      floatingOrigin.handleOrbitDelta(delta);

      // Update Zustand state
      const state = floatingOrigin.getDebugState();
      setCameraPosition(state.position_km);

      // Reset Three.js camera to origin-relative position
      // (The floating origin system keeps camera near origin)
      const newScenePos = floatingOrigin.getCameraScenePosition();
      controls.object.position.copy(newScenePos);
      controls.target.set(0, 0, 0);
    }

    lastPosition.current.copy(controls.object.position);
    lastTarget.current.copy(controls.target);
  });

  // Handle zoom separately via wheel events
  useEffect(() => {
    const handleWheel = (e: WheelEvent) => {
      if (!enabled) return;

      e.preventDefault();
      const zoomFactor = e.deltaY > 0 ? 0.9 : 1.1;
      zoom(zoomFactor);
    };

    window.addEventListener('wheel', handleWheel, { passive: false });
    return () => window.removeEventListener('wheel', handleWheel);
  }, [enabled, zoom]);
}

// =============================================================================
// CINEMATIC TOUR HOOK
// =============================================================================

export function useCinematicTour() {
  const floatingOrigin = useUniverseStore((s) => s.floatingOrigin);
  const tour = useUniverseStore((s) => s.tour);
  const startTour = useUniverseStore((s) => s.startTour);
  const stopTour = useUniverseStore((s) => s.stopTour);
  const setTourWaypoint = useUniverseStore((s) => s.setTourWaypoint);
  const setTourProgress = useUniverseStore((s) => s.setTourProgress);
  const setCameraPosition = useUniverseStore((s) => s.setCameraPosition);

  const animationRef = useRef<number | null>(null);
  const startTimeRef = useRef<number>(0);
  const currentWaypointRef = useRef<number>(0);
  const lerpFnRef = useRef<((progress: number) => void) | null>(null);

  // Start tour
  const start = useCallback(() => {
    if (!floatingOrigin) return;

    startTour();
    currentWaypointRef.current = 0;
    startTimeRef.current = performance.now();

    // Set up first waypoint
    const wp = TOUR_WAYPOINTS[0];
    setTourWaypoint(0, wp.text);
    lerpFnRef.current = floatingOrigin.createTourLerp(wp.position, wp.target);

    // Start animation loop
    const animate = (time: number) => {
      const waypoint = TOUR_WAYPOINTS[currentWaypointRef.current];
      const elapsed = (time - startTimeRef.current) / 1000;
      const progress = Math.min(elapsed / waypoint.duration, 1);

      // Apply lerp
      if (lerpFnRef.current) {
        lerpFnRef.current(progress);

        // Sync state
        const state = floatingOrigin.getDebugState();
        setCameraPosition(state.position_km);
        setTourProgress(progress);
      }

      // Move to next waypoint
      if (progress >= 1) {
        currentWaypointRef.current++;

        if (currentWaypointRef.current >= TOUR_WAYPOINTS.length) {
          // Tour complete
          stopTour();
          return;
        }

        // Set up next waypoint
        const nextWp = TOUR_WAYPOINTS[currentWaypointRef.current];
        setTourWaypoint(currentWaypointRef.current, nextWp.text);
        lerpFnRef.current = floatingOrigin.createTourLerp(nextWp.position, nextWp.target);
        startTimeRef.current = time;
      }

      animationRef.current = requestAnimationFrame(animate);
    };

    animationRef.current = requestAnimationFrame(animate);
  }, [floatingOrigin, startTour, stopTour, setTourWaypoint, setTourProgress, setCameraPosition]);

  // Stop tour
  const stop = useCallback(() => {
    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current);
      animationRef.current = null;
    }
    stopTour();
  }, [stopTour]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, []);

  return {
    isRunning: tour.isRunning,
    currentWaypoint: tour.currentWaypoint,
    waypointText: tour.waypointText,
    progress: tour.progress,
    start,
    stop,
  };
}

// =============================================================================
// EXPORT ALL
// =============================================================================

export {
  Vector3_F64,
  FloatingOriginController,
  LODManager,
  RenderMode,
};

export type { CosmicObjectType };

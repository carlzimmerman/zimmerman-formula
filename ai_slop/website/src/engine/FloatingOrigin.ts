/**
 * =============================================================================
 * FloatingOrigin.ts - 64-BIT CAMERA-RELATIVE RENDERING ENGINE
 * =============================================================================
 *
 * THE MAGIC TRICK:
 * ----------------
 * All positions are stored in Float64 (JavaScript Number) on the CPU.
 * On every frame, we compute: relative_pos = object_pos - camera_pos
 * This small, local number is then safely cast to Float32 for WebGL.
 *
 * In the GPU shader, the camera is effectively always at (0, 0, 0).
 * This completely bypasses the WebGL vertex jitter problem.
 *
 * PRECISION ANALYSIS:
 * - Float64 mantissa: 52 bits → ~15-16 significant decimal digits
 * - At cosmic scale (10^23 km), precision = 10^23 / 10^15 = 10^8 km = 0.01 ly
 * - At solar scale, precision is sub-millimeter
 *
 * Z² Framework v11.1.0
 * Work-Order HHH: Float64 Camera-Relative Engine
 * =============================================================================
 */

import * as THREE from 'three';
import { LOD_THRESHOLDS, getLODLevel, type LODLevel } from './CosmicConstants';

// =============================================================================
// FLOAT64 VECTOR CLASS
// =============================================================================

/**
 * High-precision 3D vector using JavaScript's native Float64.
 * Used for all CPU-side position calculations.
 */
export class Vector3_F64 {
  constructor(
    public x: number = 0,
    public y: number = 0,
    public z: number = 0
  ) {}

  set(x: number, y: number, z: number): this {
    this.x = x;
    this.y = y;
    this.z = z;
    return this;
  }

  copy(v: Vector3_F64): this {
    this.x = v.x;
    this.y = v.y;
    this.z = v.z;
    return this;
  }

  clone(): Vector3_F64 {
    return new Vector3_F64(this.x, this.y, this.z);
  }

  add(v: Vector3_F64): this {
    this.x += v.x;
    this.y += v.y;
    this.z += v.z;
    return this;
  }

  sub(v: Vector3_F64): this {
    this.x -= v.x;
    this.y -= v.y;
    this.z -= v.z;
    return this;
  }

  multiplyScalar(s: number): this {
    this.x *= s;
    this.y *= s;
    this.z *= s;
    return this;
  }

  divideScalar(s: number): this {
    return this.multiplyScalar(1 / s);
  }

  length(): number {
    return Math.sqrt(this.x * this.x + this.y * this.y + this.z * this.z);
  }

  lengthSq(): number {
    return this.x * this.x + this.y * this.y + this.z * this.z;
  }

  normalize(): this {
    const len = this.length();
    if (len > 0) this.divideScalar(len);
    return this;
  }

  distanceTo(v: Vector3_F64): number {
    const dx = this.x - v.x;
    const dy = this.y - v.y;
    const dz = this.z - v.z;
    return Math.sqrt(dx * dx + dy * dy + dz * dz);
  }

  /**
   * Convert to camera-relative Float32 for GPU.
   * This is THE critical operation that enables multi-scale rendering.
   */
  toCameraRelative(cameraPos: Vector3_F64, sceneScale: number): THREE.Vector3 {
    return new THREE.Vector3(
      (this.x - cameraPos.x) / sceneScale,
      (this.y - cameraPos.y) / sceneScale,
      (this.z - cameraPos.z) / sceneScale
    );
  }

  /**
   * Convert to array (for serialization/storage)
   */
  toArray(): [number, number, number] {
    return [this.x, this.y, this.z];
  }

  /**
   * Create from array
   */
  static fromArray(arr: [number, number, number]): Vector3_F64 {
    return new Vector3_F64(arr[0], arr[1], arr[2]);
  }
}

// =============================================================================
// FLOATING ORIGIN CONTROLLER
// =============================================================================

export interface FloatingOriginState {
  // Camera position in absolute km (Float64)
  cameraPosition: Vector3_F64;

  // Camera look-at target in absolute km
  cameraTarget: Vector3_F64;

  // Current LOD level
  lodLevel: LODLevel;

  // Current scene scale (km per scene unit)
  sceneScale: number;

  // Camera near/far planes
  nearPlane: number;
  farPlane: number;

  // Distance from camera to origin (for LOD decisions)
  cameraDistanceFromOrigin: number;
}

export class FloatingOriginController {
  private state: FloatingOriginState;

  // Velocity for smooth movement (km/s equivalent, scaled by deltaTime)
  private velocity: Vector3_F64 = new Vector3_F64();

  constructor(initialPosition?: [number, number, number]) {
    const pos = initialPosition
      ? Vector3_F64.fromArray(initialPosition)
      : new Vector3_F64(0, 0, 1e10); // Default: 100 AU from origin

    this.state = {
      cameraPosition: pos,
      cameraTarget: new Vector3_F64(0, 0, 0),
      lodLevel: getLODLevel(pos.length()),
      sceneScale: this.computeSceneScale(pos.length()),
      nearPlane: 0.01,
      farPlane: 100,
      cameraDistanceFromOrigin: pos.length(),
    };

    this.updateLOD();
  }

  // ===========================================================================
  // GETTERS
  // ===========================================================================

  get cameraPosition(): Vector3_F64 {
    return this.state.cameraPosition;
  }

  get cameraTarget(): Vector3_F64 {
    return this.state.cameraTarget;
  }

  get lodLevel(): LODLevel {
    return this.state.lodLevel;
  }

  get sceneScale(): number {
    return this.state.sceneScale;
  }

  get nearPlane(): number {
    return this.state.nearPlane;
  }

  get farPlane(): number {
    return this.state.farPlane;
  }

  get cameraDistanceFromOrigin(): number {
    return this.state.cameraDistanceFromOrigin;
  }

  // ===========================================================================
  // POSITION UPDATES
  // ===========================================================================

  /**
   * Set camera position directly (in km)
   */
  setCameraPosition(x: number, y: number, z: number): void {
    this.state.cameraPosition.set(x, y, z);
    this.updateLOD();
  }

  /**
   * Set camera position from Vector3_F64
   */
  setCameraPositionVector(pos: Vector3_F64): void {
    this.state.cameraPosition.copy(pos);
    this.updateLOD();
  }

  /**
   * Move camera by delta (in km)
   */
  moveCamera(dx: number, dy: number, dz: number): void {
    this.state.cameraPosition.x += dx;
    this.state.cameraPosition.y += dy;
    this.state.cameraPosition.z += dz;
    this.updateLOD();
  }

  /**
   * Set camera target (look-at point in km)
   */
  setCameraTarget(x: number, y: number, z: number): void {
    this.state.cameraTarget.set(x, y, z);
  }

  /**
   * Zoom toward/away from target
   * factor > 1 = zoom in, factor < 1 = zoom out
   */
  zoom(factor: number): void {
    const direction = this.state.cameraTarget.clone()
      .sub(this.state.cameraPosition);

    const distance = direction.length();
    const newDistance = distance / factor;

    // Clamp to reasonable bounds
    const minDistance = 1000; // 1000 km minimum
    const maxDistance = 30 * 3.086e22; // 30 Gpc maximum

    const clampedDistance = Math.max(minDistance, Math.min(maxDistance, newDistance));

    if (clampedDistance !== distance) {
      direction.normalize().multiplyScalar(clampedDistance);
      this.state.cameraPosition.copy(this.state.cameraTarget).sub(direction);
      this.updateLOD();
    }
  }

  // ===========================================================================
  // LOD MANAGEMENT
  // ===========================================================================

  /**
   * Update LOD level and scene scale based on camera distance
   */
  private updateLOD(): void {
    const distance = this.state.cameraPosition.distanceTo(this.state.cameraTarget);
    this.state.cameraDistanceFromOrigin = distance;

    const newLOD = getLODLevel(distance);
    const lodConfig = LOD_THRESHOLDS[newLOD];

    this.state.lodLevel = newLOD;
    this.state.sceneScale = lodConfig.sceneScale_km;
    this.state.nearPlane = lodConfig.nearPlane;
    this.state.farPlane = lodConfig.farPlane;
  }

  /**
   * Compute appropriate scene scale for given distance
   */
  private computeSceneScale(distance_km: number): number {
    const lod = getLODLevel(distance_km);
    return LOD_THRESHOLDS[lod].sceneScale_km;
  }

  // ===========================================================================
  // COORDINATE TRANSFORMATION (THE MAGIC)
  // ===========================================================================

  /**
   * Transform an absolute position (km) to camera-relative scene coordinates.
   * This is called for every visible object on every frame.
   *
   * The result is a THREE.Vector3 (Float32) that can be sent to the GPU.
   */
  toSceneCoordinates(absolutePos_km: Vector3_F64): THREE.Vector3 {
    return absolutePos_km.toCameraRelative(
      this.state.cameraPosition,
      this.state.sceneScale
    );
  }

  /**
   * Transform an absolute position array to scene coordinates
   */
  toSceneCoordinatesArray(pos_km: [number, number, number]): THREE.Vector3 {
    return new THREE.Vector3(
      (pos_km[0] - this.state.cameraPosition.x) / this.state.sceneScale,
      (pos_km[1] - this.state.cameraPosition.y) / this.state.sceneScale,
      (pos_km[2] - this.state.cameraPosition.z) / this.state.sceneScale
    );
  }

  /**
   * Transform a size/radius from km to scene units
   */
  toSceneSize(size_km: number): number {
    return size_km / this.state.sceneScale;
  }

  /**
   * Get camera position in scene coordinates (always near origin)
   */
  getCameraScenePosition(): THREE.Vector3 {
    // In camera-relative rendering, camera is always at a small offset
    // We return the look direction scaled appropriately
    const toTarget = this.state.cameraTarget.clone()
      .sub(this.state.cameraPosition);
    const distance = toTarget.length();

    // Camera is positioned looking at origin from `distance` away
    toTarget.normalize().multiplyScalar(-distance / this.state.sceneScale);

    return new THREE.Vector3(toTarget.x, toTarget.y, toTarget.z);
  }

  // ===========================================================================
  // ORBIT CONTROLS INTEGRATION
  // ===========================================================================

  /**
   * Handle orbit controls movement.
   * Converts scene-space delta to absolute km delta.
   */
  handleOrbitDelta(sceneDelta: THREE.Vector3): void {
    const kmDelta = new Vector3_F64(
      sceneDelta.x * this.state.sceneScale,
      sceneDelta.y * this.state.sceneScale,
      sceneDelta.z * this.state.sceneScale
    );
    this.state.cameraPosition.add(kmDelta);
    this.updateLOD();
  }

  /**
   * Handle zoom from scroll wheel.
   * deltaY > 0 = zoom out, deltaY < 0 = zoom in
   */
  handleZoom(deltaY: number): void {
    const zoomFactor = deltaY > 0 ? 0.9 : 1.1;
    this.zoom(zoomFactor);
  }

  // ===========================================================================
  // CINEMATIC TOUR SUPPORT
  // ===========================================================================

  /**
   * Smoothly interpolate camera to a new position over time.
   * Returns a function that should be called each frame with progress [0,1].
   */
  createTourLerp(
    targetPos_km: [number, number, number],
    targetLookAt_km: [number, number, number]
  ): (progress: number) => void {
    const startPos = this.state.cameraPosition.clone();
    const startTarget = this.state.cameraTarget.clone();
    const endPos = Vector3_F64.fromArray(targetPos_km);
    const endTarget = Vector3_F64.fromArray(targetLookAt_km);

    return (progress: number) => {
      // Use smoothstep for easing
      const t = progress * progress * (3 - 2 * progress);

      this.state.cameraPosition.set(
        startPos.x + (endPos.x - startPos.x) * t,
        startPos.y + (endPos.y - startPos.y) * t,
        startPos.z + (endPos.z - startPos.z) * t
      );

      this.state.cameraTarget.set(
        startTarget.x + (endTarget.x - startTarget.x) * t,
        startTarget.y + (endTarget.y - startTarget.y) * t,
        startTarget.z + (endTarget.z - startTarget.z) * t
      );

      this.updateLOD();
    };
  }

  // ===========================================================================
  // DEBUG / STATE EXPORT
  // ===========================================================================

  getDebugState(): {
    position_km: [number, number, number];
    target_km: [number, number, number];
    distance_km: number;
    lodLevel: LODLevel;
    sceneScale: string;
  } {
    return {
      position_km: this.state.cameraPosition.toArray(),
      target_km: this.state.cameraTarget.toArray(),
      distance_km: this.state.cameraDistanceFromOrigin,
      lodLevel: this.state.lodLevel,
      sceneScale: `${this.state.sceneScale.toExponential(2)} km/unit`,
    };
  }
}

// =============================================================================
// SINGLETON INSTANCE
// =============================================================================

let _instance: FloatingOriginController | null = null;

export function getFloatingOrigin(): FloatingOriginController {
  if (!_instance) {
    _instance = new FloatingOriginController();
  }
  return _instance;
}

export function resetFloatingOrigin(initialPosition?: [number, number, number]): FloatingOriginController {
  _instance = new FloatingOriginController(initialPosition);
  return _instance;
}

// =============================================================================
// Z² TOPOLOGICAL PROPULSION SYSTEM (Directive XXX)
// =============================================================================
// Handles player movement through the T³/Z₂ orbifold topology
// - Sub-light movement for local exploration
// - Topological warp for Gpc-scale travel
// - Automatic T³ boundary wrapping
// - Z₂ parity tracking
// =============================================================================

import * as THREE from 'three';
import { PlayerPosition, VESSEL_CONFIGS, VesselType } from '../store/playerStore';

// Fundamental domain parameters
const L_C = 20.6; // Fundamental domain size in Gpc
const HALF_L = L_C / 2; // ±10.3 Gpc boundaries

// Speed of light in our units (Gpc/s) - for reference
// In reality c ≈ 3e5 km/s ≈ 9.7e-15 Gpc/year ≈ 3e-22 Gpc/s
// We use scaled speeds for gameplay
const C_SCALED = 0.001; // Scaled "speed of light" for sub-light movement

export interface PropulsionInput {
  // WASD movement (-1 to 1)
  forward: number;
  right: number;
  up: number;

  // Mouse look (radians/frame)
  yaw: number;
  pitch: number;

  // Warp engaged
  warp: boolean;

  // Delta time
  delta: number;
}

export interface PropulsionResult {
  newPosition: PlayerPosition;
  newVelocity: THREE.Vector3;
  newRotation: THREE.Euler;

  // T³/Z₂ events
  didCrossBoundary: boolean;
  crossedAxis: 'x' | 'y' | 'z' | null;
  didFlipParity: boolean;
}

export interface WrapResult {
  position: PlayerPosition;
  didWrap: boolean;
  axis: 'x' | 'y' | 'z' | null;
}

/**
 * Apply T³ modulo wrapping to a position
 * When position exceeds ±HALF_L, wrap to opposite side
 */
export function wrapPositionT3(pos: PlayerPosition): WrapResult {
  const wrapped: PlayerPosition = { ...pos };
  let didWrap = false;
  let axis: 'x' | 'y' | 'z' | null = null;

  if (wrapped.x > HALF_L) {
    wrapped.x -= L_C;
    didWrap = true;
    axis = 'x';
  } else if (wrapped.x < -HALF_L) {
    wrapped.x += L_C;
    didWrap = true;
    axis = 'x';
  }

  if (wrapped.y > HALF_L) {
    wrapped.y -= L_C;
    didWrap = true;
    axis = axis || 'y';
  } else if (wrapped.y < -HALF_L) {
    wrapped.y += L_C;
    didWrap = true;
    axis = axis || 'y';
  }

  if (wrapped.z > HALF_L) {
    wrapped.z -= L_C;
    didWrap = true;
    axis = axis || 'z';
  } else if (wrapped.z < -HALF_L) {
    wrapped.z += L_C;
    didWrap = true;
    axis = axis || 'z';
  }

  return { position: wrapped, didWrap, axis };
}

/**
 * Calculate the shortest geodesic direction on T³
 * Returns a direction vector that accounts for wrapping
 */
export function geodesicDirection(from: PlayerPosition, to: PlayerPosition): THREE.Vector3 {
  let dx = to.x - from.x;
  let dy = to.y - from.y;
  let dz = to.z - from.z;

  // Check if wrapping is shorter
  if (Math.abs(dx) > HALF_L) dx = dx > 0 ? dx - L_C : dx + L_C;
  if (Math.abs(dy) > HALF_L) dy = dy > 0 ? dy - L_C : dy + L_C;
  if (Math.abs(dz) > HALF_L) dz = dz > 0 ? dz - L_C : dz + L_C;

  return new THREE.Vector3(dx, dy, dz).normalize();
}

/**
 * Apply Z₂ parity inversion to position and rotation
 */
export function applyZ2Inversion(
  pos: PlayerPosition,
  rot: THREE.Euler
): { position: PlayerPosition; rotation: THREE.Euler } {
  return {
    position: { x: -pos.x, y: -pos.y, z: -pos.z },
    rotation: new THREE.Euler(rot.x, rot.y + Math.PI, rot.z),
  };
}

/**
 * Main propulsion update function
 * Called every frame to update player position/velocity
 */
export function updatePropulsion(
  currentPosition: PlayerPosition,
  currentVelocity: THREE.Vector3 | { x: number; y: number; z: number },
  currentRotation: THREE.Euler | { x: number; y: number; z: number },
  vesselType: VesselType,
  input: PropulsionInput
): PropulsionResult {
  const config = VESSEL_CONFIGS[vesselType];

  // Ensure we have proper THREE objects (Zustand may serialize to plain objects)
  const velocity = currentVelocity instanceof THREE.Vector3
    ? currentVelocity
    : new THREE.Vector3(currentVelocity.x, currentVelocity.y, currentVelocity.z);

  const rotation = currentRotation instanceof THREE.Euler
    ? currentRotation
    : new THREE.Euler(currentRotation.x, currentRotation.y, currentRotation.z);

  // Create rotation matrix from current orientation
  const rotationMatrix = new THREE.Matrix4().makeRotationFromEuler(rotation);

  // Calculate movement direction in world space
  const forward = new THREE.Vector3(0, 0, -1).applyMatrix4(rotationMatrix);
  const right = new THREE.Vector3(1, 0, 0).applyMatrix4(rotationMatrix);
  const up = new THREE.Vector3(0, 1, 0).applyMatrix4(rotationMatrix);

  // Apply rotation from mouse input
  const newRotation = new THREE.Euler(
    rotation.x + input.pitch,
    rotation.y + input.yaw,
    rotation.z
  );

  // Clamp pitch to prevent flipping
  newRotation.x = Math.max(-Math.PI / 2 + 0.1, Math.min(Math.PI / 2 - 0.1, newRotation.x));

  // Calculate thrust
  const thrust = new THREE.Vector3()
    .addScaledVector(forward, input.forward)
    .addScaledVector(right, input.right)
    .addScaledVector(up, input.up);

  // Determine speed based on warp state
  let speedMultiplier: number;
  if (input.warp) {
    // Warp speed: Gpc-scale movement
    speedMultiplier = config.maxSpeed;
  } else {
    // Sub-light: Very slow, for local exploration
    speedMultiplier = C_SCALED;
  }

  // Apply acceleration
  const acceleration = thrust.multiplyScalar(config.acceleration * speedMultiplier * input.delta);
  const newVelocity = velocity.clone().add(acceleration);

  // Apply drag (more drag at sub-light to feel responsive)
  const drag = input.warp ? 0.98 : 0.9;
  newVelocity.multiplyScalar(drag);

  // Clamp velocity to max speed
  const maxVel = speedMultiplier * 2;
  if (newVelocity.length() > maxVel) {
    newVelocity.normalize().multiplyScalar(maxVel);
  }

  // Update position
  const newPosition: PlayerPosition = {
    x: currentPosition.x + newVelocity.x * input.delta,
    y: currentPosition.y + newVelocity.y * input.delta,
    z: currentPosition.z + newVelocity.z * input.delta,
  };

  // Apply T³ wrapping
  const wrapResult = wrapPositionT3(newPosition);

  return {
    newPosition: wrapResult.position,
    newVelocity,
    newRotation,
    didCrossBoundary: wrapResult.didWrap,
    crossedAxis: wrapResult.axis,
    didFlipParity: false, // Z₂ flip is triggered separately
  };
}

/**
 * Calculate distance to nearest boundary
 */
export function distanceToNearestBoundary(pos: PlayerPosition): {
  distance: number;
  axis: 'x' | 'y' | 'z';
  direction: 1 | -1;
} {
  const distances = [
    { axis: 'x' as const, dist: HALF_L - pos.x, dir: 1 as const },
    { axis: 'x' as const, dist: HALF_L + pos.x, dir: -1 as const },
    { axis: 'y' as const, dist: HALF_L - pos.y, dir: 1 as const },
    { axis: 'y' as const, dist: HALF_L + pos.y, dir: -1 as const },
    { axis: 'z' as const, dist: HALF_L - pos.z, dir: 1 as const },
    { axis: 'z' as const, dist: HALF_L + pos.z, dir: -1 as const },
  ];

  const nearest = distances.reduce((min, curr) =>
    curr.dist < min.dist ? curr : min
  );

  return {
    distance: nearest.dist,
    axis: nearest.axis,
    direction: nearest.dir,
  };
}

/**
 * Get current "quadrant" of the fundamental domain (for HUD display)
 */
export function getQuadrantInfo(pos: PlayerPosition): {
  octant: string;
  distanceFromOrigin: number;
  nearestVertex: string;
} {
  const signs = [
    pos.x >= 0 ? '+' : '-',
    pos.y >= 0 ? '+' : '-',
    pos.z >= 0 ? '+' : '-',
  ];
  const octant = `(${signs[0]}X, ${signs[1]}Y, ${signs[2]}Z)`;

  const distanceFromOrigin = Math.sqrt(pos.x ** 2 + pos.y ** 2 + pos.z ** 2);

  // Nearest Z₂ vertex (corners of the fundamental domain)
  const vertexIndex =
    (pos.x >= 0 ? 0 : 1) +
    (pos.y >= 0 ? 0 : 2) +
    (pos.z >= 0 ? 0 : 4);
  const vertexNames = ['V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8'];
  const nearestVertex = vertexNames[vertexIndex];

  return { octant, distanceFromOrigin, nearestVertex };
}

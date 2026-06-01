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

// =============================================================================
// BLACK HOLE DATA - Cosmic hazards with geometric lock
// =============================================================================
// Real Schwarzschild radii are ~km scale, but we scale up for gameplay
// Event horizon = zone where geodesics lock onto singularity

export interface BlackHole {
  id: string;
  name: string;
  position: { x: number; y: number; z: number };
  mass_solar: number;
  // Gameplay-scaled event horizon (real r_s would be ~0 in Gpc)
  eventHorizon_gpc: number;
  // Gravitational influence zone (tidal effects start here)
  influenceRadius_gpc: number;
}

export const COSMIC_BLACK_HOLES: BlackHole[] = [
  {
    id: 'GW190521',
    name: 'GW190521 Remnant',
    position: { x: 4.2, y: 1.8, z: -2.5 },
    mass_solar: 142,
    eventHorizon_gpc: 0.005, // 5 Mpc - gameplay scale
    influenceRadius_gpc: 0.05, // 50 Mpc - tidal effects zone
  },
  {
    id: 'M87',
    name: 'M87* Supermassive',
    position: { x: 0.016, y: 0.005, z: 0.01 }, // ~16 Mpc away
    mass_solar: 6.5e9, // 6.5 billion solar masses
    eventHorizon_gpc: 0.01, // 10 Mpc
    influenceRadius_gpc: 0.1, // 100 Mpc
  },
  {
    id: 'SagA',
    name: 'Sagittarius A*',
    position: { x: -0.05, y: 0, z: -0.05 }, // Galactic center (~50 Mpc offset for gameplay)
    mass_solar: 4e6,
    eventHorizon_gpc: 0.002, // 2 Mpc
    influenceRadius_gpc: 0.02, // 20 Mpc
  },
];

export interface PropulsionInput {
  // Left hand - Thrust controls (-1 to 1)
  forward: number;  // W/S throttle
  right: number;    // Q/E strafe
  up: number;       // R/F vertical

  // Arrow keys - Steering (radians/frame, continuous while held)
  yaw: number;      // Left/Right arrow
  pitch: number;    // Up/Down arrow
  roll?: number;    // A/D roll (optional)

  // Warp engaged (Shift/Space)
  warp: boolean;

  // Delta time
  delta: number;
}

export interface BlackHoleLockState {
  isLocked: boolean;
  lockedToHole: BlackHole | null;
  distanceToSingularity: number;
  isInInfluenceZone: boolean;
  nearestHole: BlackHole | null;
}

export interface PropulsionResult {
  newPosition: PlayerPosition;
  newVelocity: THREE.Vector3;
  newRotation: THREE.Euler;

  // T³/Z₂ events
  didCrossBoundary: boolean;
  crossedAxis: 'x' | 'y' | 'z' | null;
  didFlipParity: boolean;

  // Black hole state
  blackHoleState: BlackHoleLockState;
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
 * Calculate geodesic correction factor
 * In T³ topology, geodesics curve near boundaries to wrap smoothly
 * This creates a subtle "pull" effect as you approach a boundary
 */
function calculateGeodesicCorrection(
  position: PlayerPosition,
  velocity: THREE.Vector3
): THREE.Vector3 {
  const correction = new THREE.Vector3(0, 0, 0);
  const boundaryThreshold = 3.0; // Start curving within 3 Gpc of boundary

  // Check each axis for proximity to boundary
  const axes: ('x' | 'y' | 'z')[] = ['x', 'y', 'z'];

  for (const axis of axes) {
    const pos = position[axis];
    const vel = velocity[axis];

    // Distance to nearest boundary on this axis
    const distToPos = HALF_L - pos;
    const distToNeg = HALF_L + pos;

    // Approaching positive boundary
    if (distToPos < boundaryThreshold && vel > 0) {
      // Geodesic curves smoothly - velocity bends to wrap
      const curvature = 1 - (distToPos / boundaryThreshold);
      // Don't resist, just prepare for wrap - subtle effect
      correction[axis] -= vel * curvature * 0.1;
    }
    // Approaching negative boundary
    else if (distToNeg < boundaryThreshold && vel < 0) {
      const curvature = 1 - (distToNeg / boundaryThreshold);
      correction[axis] -= vel * curvature * 0.1;
    }
  }

  return correction;
}

/**
 * Check black hole proximity and apply geometric effects
 * Inside event horizon: ALL geodesics point to singularity (locked)
 * Inside influence zone: Gravitational pull toward black hole
 */
function checkBlackHoles(
  position: PlayerPosition,
  velocity: THREE.Vector3
): { state: BlackHoleLockState; modifiedVelocity: THREE.Vector3 } {
  const modifiedVelocity = velocity.clone();
  let state: BlackHoleLockState = {
    isLocked: false,
    lockedToHole: null,
    distanceToSingularity: Infinity,
    isInInfluenceZone: false,
    nearestHole: null,
  };

  let nearestDist = Infinity;

  for (const hole of COSMIC_BLACK_HOLES) {
    // Calculate distance to black hole
    const dx = position.x - hole.position.x;
    const dy = position.y - hole.position.y;
    const dz = position.z - hole.position.z;
    const distance = Math.sqrt(dx * dx + dy * dy + dz * dz);

    // Track nearest hole
    if (distance < nearestDist) {
      nearestDist = distance;
      state.nearestHole = hole;
      state.distanceToSingularity = distance;
    }

    // Check if INSIDE event horizon - GEOMETRIC LOCK
    if (distance < hole.eventHorizon_gpc) {
      state.isLocked = true;
      state.lockedToHole = hole;
      state.distanceToSingularity = distance;

      // ALL geodesics point toward singularity!
      // Player input is ignored - velocity forced inward
      const dirToSingularity = new THREE.Vector3(
        hole.position.x - position.x,
        hole.position.y - position.y,
        hole.position.z - position.z
      ).normalize();

      // Inward velocity increases as you approach (tidal acceleration)
      const fallSpeed = Math.max(velocity.length(), 0.1);
      modifiedVelocity.copy(dirToSingularity.multiplyScalar(fallSpeed * 1.5));

      break; // Can only be locked to one hole
    }

    // Check if in influence zone - gravitational pull
    if (distance < hole.influenceRadius_gpc) {
      state.isInInfluenceZone = true;

      // Direction toward black hole
      const dirToHole = new THREE.Vector3(
        hole.position.x - position.x,
        hole.position.y - position.y,
        hole.position.z - position.z
      ).normalize();

      // Gravitational pull strength (inverse square, scaled for gameplay)
      const pullStrength = (hole.influenceRadius_gpc - distance) / hole.influenceRadius_gpc;
      const gravPull = pullStrength * pullStrength * 0.3; // Max 30% velocity modification

      // Add gravitational pull to velocity
      modifiedVelocity.addScaledVector(dirToHole, gravPull * velocity.length());
    }
  }

  return { state, modifiedVelocity };
}

/**
 * Main propulsion update function
 * Called every frame to update player position/velocity
 * Movement follows T³/Z₂ geodesics - straight lines that wrap at boundaries
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

  // Apply rotation from arrow keys (yaw, pitch) and roll (A/D)
  const rollAmount = input.roll || 0;
  const newRotation = new THREE.Euler(
    rotation.x + input.pitch,
    rotation.y + input.yaw,
    rotation.z + rollAmount * 0.02  // Roll is slower for stability
  );

  // Clamp pitch to prevent flipping
  newRotation.x = Math.max(-Math.PI / 2 + 0.1, Math.min(Math.PI / 2 - 0.1, newRotation.x));

  // Calculate thrust from input
  const thrust = new THREE.Vector3()
    .addScaledVector(forward, input.forward)
    .addScaledVector(right, input.right)
    .addScaledVector(up, input.up);

  // Determine speed based on warp state
  let speedMultiplier: number;
  if (input.warp) {
    // Warp speed: Gpc-scale movement - following T³ geodesics
    speedMultiplier = config.maxSpeed;
  } else {
    // Sub-light: Very slow, for local exploration
    speedMultiplier = C_SCALED;
  }

  // Apply acceleration
  const acceleration = thrust.multiplyScalar(config.acceleration * speedMultiplier * input.delta);
  const newVelocity = velocity.clone().add(acceleration);

  // Apply geodesic correction - velocity curves smoothly near boundaries
  // This is the T³ topology affecting the path!
  const geodesicAdj = calculateGeodesicCorrection(currentPosition, newVelocity);
  newVelocity.add(geodesicAdj);

  // Check for black hole proximity and geometric lock
  const blackHoleCheck = checkBlackHoles(currentPosition, newVelocity);
  const finalVelocity = blackHoleCheck.state.isLocked
    ? blackHoleCheck.modifiedVelocity  // LOCKED - velocity forced toward singularity
    : blackHoleCheck.modifiedVelocity; // May have gravitational pull applied

  // Apply drag (more drag at sub-light to feel responsive)
  // No drag when locked in black hole - pure geodesic fall
  const drag = blackHoleCheck.state.isLocked ? 1.0 : (input.warp ? 0.98 : 0.9);
  finalVelocity.multiplyScalar(drag);

  // Clamp velocity to max speed (unless locked in black hole)
  if (!blackHoleCheck.state.isLocked) {
    const maxVel = speedMultiplier * 2;
    if (finalVelocity.length() > maxVel) {
      finalVelocity.normalize().multiplyScalar(maxVel);
    }
  }

  // Update position along geodesic
  const newPosition: PlayerPosition = {
    x: currentPosition.x + finalVelocity.x * input.delta,
    y: currentPosition.y + finalVelocity.y * input.delta,
    z: currentPosition.z + finalVelocity.z * input.delta,
  };

  // Apply T³ wrapping - this IS the geodesic behavior
  // In T³, a straight line that exits one face enters the opposite face
  // Note: Black holes don't wrap - they're absolute positions
  const wrapResult = wrapPositionT3(newPosition);

  return {
    newPosition: wrapResult.position,
    newVelocity: finalVelocity,
    newRotation,
    didCrossBoundary: wrapResult.didWrap,
    crossedAxis: wrapResult.axis,
    didFlipParity: false, // Z₂ flip is triggered separately
    blackHoleState: blackHoleCheck.state,
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

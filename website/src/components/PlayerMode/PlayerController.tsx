// =============================================================================
// PLAYER CONTROLLER (Directives XXX, YYY)
// =============================================================================
// Handles player input, movement, and T³/Z₂ boundary interactions
// =============================================================================

'use client';

import React, { useRef, useEffect, useCallback } from 'react';
import { useFrame, useThree } from '@react-three/fiber';
import * as THREE from 'three';
import { usePlayerStore, PlayerPosition } from '../../store/playerStore';
import { updatePropulsion, distanceToNearestBoundary, getQuadrantInfo } from '../../physics/Z2Propulsion';
import { VesselMesh } from './VesselMesh';

const L_C = 20.6;
const HALF_L = L_C / 2;

interface PlayerControllerProps {
  onBoundaryCross: (axis: string) => void;
  onParityFlip: () => void;
}

const PlayerController: React.FC<PlayerControllerProps> = ({
  onBoundaryCross,
  onParityFlip,
}) => {
  const { camera } = useThree();
  const {
    isPlayerMode,
    activeVessel,
    position,
    velocity,
    rotation,
    isWarping,
    currentParity,
    setPosition,
    setVelocity,
    setRotation,
    startWarp,
    stopWarp,
    recordBoundaryCross,
    flipParity,
  } = usePlayerStore();

  // Input state
  const inputRef = useRef({
    forward: 0,
    right: 0,
    up: 0,
    yaw: 0,
    pitch: 0,
    warp: false,
  });

  // Mouse state
  const isPointerLocked = useRef(false);

  // Handle keyboard input
  useEffect(() => {
    if (!isPlayerMode) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      switch (e.code) {
        case 'KeyW': inputRef.current.forward = 1; break;
        case 'KeyS': inputRef.current.forward = -1; break;
        case 'KeyA': inputRef.current.right = -1; break;
        case 'KeyD': inputRef.current.right = 1; break;
        case 'Space': inputRef.current.up = 1; break;
        case 'ControlLeft': inputRef.current.up = -1; break;
        case 'ShiftLeft':
          inputRef.current.warp = true;
          startWarp();
          break;
      }
    };

    const handleKeyUp = (e: KeyboardEvent) => {
      switch (e.code) {
        case 'KeyW': if (inputRef.current.forward > 0) inputRef.current.forward = 0; break;
        case 'KeyS': if (inputRef.current.forward < 0) inputRef.current.forward = 0; break;
        case 'KeyA': if (inputRef.current.right < 0) inputRef.current.right = 0; break;
        case 'KeyD': if (inputRef.current.right > 0) inputRef.current.right = 0; break;
        case 'Space': if (inputRef.current.up > 0) inputRef.current.up = 0; break;
        case 'ControlLeft': if (inputRef.current.up < 0) inputRef.current.up = 0; break;
        case 'ShiftLeft':
          inputRef.current.warp = false;
          stopWarp();
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, [isPlayerMode, startWarp, stopWarp]);

  // Handle mouse look
  useEffect(() => {
    if (!isPlayerMode) return;

    const handleMouseMove = (e: MouseEvent) => {
      if (!isPointerLocked.current) return;

      const sensitivity = 0.002;
      inputRef.current.yaw -= e.movementX * sensitivity;
      inputRef.current.pitch -= e.movementY * sensitivity;
    };

    const handlePointerLockChange = () => {
      isPointerLocked.current = document.pointerLockElement !== null;
    };

    const handleClick = () => {
      if (isPlayerMode && !isPointerLocked.current) {
        document.body.requestPointerLock();
      }
    };

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('pointerlockchange', handlePointerLockChange);
    document.addEventListener('click', handleClick);

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('pointerlockchange', handlePointerLockChange);
      document.removeEventListener('click', handleClick);
      if (document.pointerLockElement) {
        document.exitPointerLock();
      }
    };
  }, [isPlayerMode]);

  // Main update loop
  useFrame((state, delta) => {
    if (!isPlayerMode) return;

    // Clamp delta to prevent huge jumps
    const clampedDelta = Math.min(delta, 0.1);

    // Get propulsion result
    const result = updatePropulsion(
      position,
      velocity,
      rotation,
      activeVessel,
      {
        forward: inputRef.current.forward,
        right: inputRef.current.right,
        up: inputRef.current.up,
        yaw: inputRef.current.yaw,
        pitch: inputRef.current.pitch,
        warp: inputRef.current.warp,
        delta: clampedDelta,
      }
    );

    // Reset mouse deltas after applying
    inputRef.current.yaw = 0;
    inputRef.current.pitch = 0;

    // Update store
    setPosition(result.newPosition);
    setVelocity(result.newVelocity);
    setRotation(result.newRotation);

    // Handle boundary crossing
    if (result.didCrossBoundary && result.crossedAxis) {
      recordBoundaryCross();
      onBoundaryCross(result.crossedAxis);
    }

    // Update camera to follow player
    // Camera is positioned behind and above the vessel
    const cameraOffset = new THREE.Vector3(0, 0.5, 2);
    cameraOffset.applyEuler(result.newRotation);

    camera.position.set(
      result.newPosition.x + cameraOffset.x,
      result.newPosition.y + cameraOffset.y,
      result.newPosition.z + cameraOffset.z
    );

    // Camera looks at vessel position
    camera.lookAt(
      result.newPosition.x,
      result.newPosition.y,
      result.newPosition.z
    );
  });

  if (!isPlayerMode) return null;

  return (
    <group
      position={[position.x, position.y, position.z]}
      rotation={[rotation.x, rotation.y, rotation.z]}
    >
      <VesselMesh
        vesselType={activeVessel}
        isWarping={isWarping}
        parity={currentParity}
      />

      {/* Vessel lighting */}
      <pointLight position={[0, 1, 0]} intensity={0.5} color="#ffffff" />

      {/* Warp trail effect */}
      {isWarping && (
        <mesh position={[0, 0, 1]}>
          <coneGeometry args={[0.3, 2, 8]} />
          <meshBasicMaterial
            color="#00ffff"
            transparent
            opacity={0.3}
            side={THREE.DoubleSide}
          />
        </mesh>
      )}
    </group>
  );
};

// HUD component for player mode
export const PlayerHUD: React.FC = () => {
  const {
    isPlayerMode,
    activeVessel,
    position,
    velocity,
    isWarping,
    boundariesCrossed,
    parityFlips,
    currentParity,
    stopPlayerMode,
  } = usePlayerStore();

  if (!isPlayerMode) return null;

  const speed = Math.sqrt(velocity.x ** 2 + velocity.y ** 2 + velocity.z ** 2);
  const quadrant = getQuadrantInfo(position);
  const boundary = distanceToNearestBoundary(position);

  return (
    <div className="absolute inset-0 pointer-events-none z-40">
      {/* Top bar */}
      <div className="absolute top-4 left-1/2 -translate-x-1/2 bg-black/80 border border-cyan-500/50 rounded-lg px-6 py-2 flex items-center gap-6 pointer-events-auto">
        <div className="text-cyan-400 font-mono text-sm">
          <span className="text-slate-500">VESSEL:</span> {activeVessel.toUpperCase()}
        </div>
        <div className={`font-mono text-sm ${isWarping ? 'text-orange-400 animate-pulse' : 'text-slate-400'}`}>
          {isWarping ? '⚡ WARP ACTIVE' : 'SUB-LIGHT'}
        </div>
        <button
          onClick={stopPlayerMode}
          className="text-red-400 hover:text-red-300 text-sm font-bold"
        >
          [ESC] EXIT
        </button>
      </div>

      {/* Left panel - Position */}
      <div className="absolute left-4 top-1/2 -translate-y-1/2 bg-black/80 border border-slate-600 rounded-lg p-4 font-mono text-xs space-y-2">
        <div className="text-slate-500 mb-2">POSITION (Gpc)</div>
        <div className="text-cyan-400">X: {position.x.toFixed(3)}</div>
        <div className="text-cyan-400">Y: {position.y.toFixed(3)}</div>
        <div className="text-cyan-400">Z: {position.z.toFixed(3)}</div>
        <div className="border-t border-slate-700 pt-2 mt-2">
          <div className="text-slate-500">OCTANT</div>
          <div className="text-white">{quadrant.octant}</div>
        </div>
        <div>
          <div className="text-slate-500">NEAREST VERTEX</div>
          <div className="text-purple-400">{quadrant.nearestVertex}</div>
        </div>
      </div>

      {/* Right panel - Stats */}
      <div className="absolute right-4 top-1/2 -translate-y-1/2 bg-black/80 border border-slate-600 rounded-lg p-4 font-mono text-xs space-y-2">
        <div className="text-slate-500 mb-2">TELEMETRY</div>
        <div>
          <span className="text-slate-500">SPEED:</span>
          <span className="text-green-400 ml-2">{speed.toFixed(4)} Gpc/s</span>
        </div>
        <div>
          <span className="text-slate-500">FROM ORIGIN:</span>
          <span className="text-white ml-2">{quadrant.distanceFromOrigin.toFixed(2)} Gpc</span>
        </div>
        <div className="border-t border-slate-700 pt-2 mt-2">
          <div className="text-slate-500">TO BOUNDARY</div>
          <div className={boundary.distance < 1 ? 'text-orange-400' : 'text-white'}>
            {boundary.distance.toFixed(2)} Gpc ({boundary.axis.toUpperCase()})
          </div>
        </div>
        <div className="border-t border-slate-700 pt-2 mt-2">
          <div className="text-slate-500">TOPOLOGY</div>
          <div className="text-cyan-400">T³ Wraps: {boundariesCrossed}</div>
          <div className="text-purple-400">Z₂ Flips: {parityFlips}</div>
          <div className={currentParity === 1 ? 'text-green-400' : 'text-red-400'}>
            Parity: {currentParity === 1 ? '+1' : '-1'}
          </div>
        </div>
      </div>

      {/* Bottom - Controls reminder */}
      <div className="absolute bottom-4 left-1/2 -translate-x-1/2 bg-black/60 rounded-lg px-4 py-2 text-xs text-slate-500 font-mono">
        WASD: Move | Mouse: Look | SHIFT: Warp | Click to capture mouse
      </div>

      {/* Boundary proximity warning */}
      {boundary.distance < 1 && (
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-center">
          <div className="text-2xl font-bold text-orange-400 animate-pulse">
            ⚠️ APPROACHING {boundary.axis.toUpperCase()} BOUNDARY
          </div>
          <div className="text-orange-300 text-sm">
            {boundary.distance.toFixed(2)} Gpc to T³ wrap
          </div>
        </div>
      )}
    </div>
  );
};

export default PlayerController;

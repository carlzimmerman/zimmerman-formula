// =============================================================================
// PLAYER CONTROLLER (Directives XXX, YYY)
// =============================================================================
// Handles player input, movement, and T³/Z₂ boundary interactions
// =============================================================================

'use client';

import React, { useRef, useEffect, useCallback, useState } from 'react';
import { useFrame, useThree } from '@react-three/fiber';
import * as THREE from 'three';
import { usePlayerStore, PlayerPosition } from '../../store/playerStore';
import { updatePropulsion, distanceToNearestBoundary, getQuadrantInfo, BlackHoleLockState, COSMIC_BLACK_HOLES } from '../../physics/Z2Propulsion';
import { VesselMesh } from './VesselMesh';

const L_C = 20.6;
const HALF_L = L_C / 2;

interface PlayerControllerProps {
  onBoundaryCross: (axis: string) => void;
  onParityFlip: () => void;
  onBlackHoleLock?: (holeName: string) => void;
}

const PlayerController: React.FC<PlayerControllerProps> = ({
  onBoundaryCross,
  onParityFlip,
  onBlackHoleLock,
}) => {
  const { camera } = useThree();

  // Black hole state for visual effects
  const blackHoleStateRef = useRef<BlackHoleLockState>({
    isLocked: false,
    lockedToHole: null,
    distanceToSingularity: Infinity,
    isInInfluenceZone: false,
    nearestHole: null,
  });
  const wasLockedRef = useRef(false);
  const {
    isPlayerMode,
    activeVessel,
    playerName,
    position,
    velocity,
    rotation,
    isWarping,
    currentParity,
    touchInput,
    setPosition,
    setVelocity,
    setRotation,
    startWarp,
    stopWarp,
    recordBoundaryCross,
    flipParity,
  } = usePlayerStore();

  // Input state - Flight Sim style (no pointer lock!)
  // Works with both keyboard (desktop) and touch (mobile)
  const inputRef = useRef({
    forward: 0,    // W/S = throttle / Left joystick Y
    right: 0,      // Q/E = strafe / Left joystick X
    up: 0,         // R/F = vertical
    yaw: 0,        // Arrow Left/Right = turn / Right joystick X
    pitch: 0,      // Arrow Up/Down = pitch / Right joystick Y
    roll: 0,       // A/D = roll
    warp: false,   // Shift = warp drive / Warp button
  });

  // Touch state for mobile controls
  const leftTouchRef = useRef<{ id: number; startX: number; startY: number } | null>(null);
  const rightTouchRef = useRef<{ id: number; startX: number; startY: number } | null>(null);

  // Handle keyboard input - FLIGHT SIM CONTROLS (no mouse capture!)
  // Left hand: WASD + QE + RF for thrust
  // Right hand: Arrow keys for steering
  useEffect(() => {
    if (!isPlayerMode) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      // Prevent default for game keys
      if (['KeyW', 'KeyS', 'KeyA', 'KeyD', 'KeyQ', 'KeyE', 'KeyR', 'KeyF',
           'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ShiftLeft', 'Space'].includes(e.code)) {
        e.preventDefault();
      }

      switch (e.code) {
        // LEFT HAND - Thrust controls
        case 'KeyW': inputRef.current.forward = 1; break;      // Throttle forward
        case 'KeyS': inputRef.current.forward = -1; break;     // Throttle reverse
        case 'KeyQ': inputRef.current.right = -1; break;       // Strafe left
        case 'KeyE': inputRef.current.right = 1; break;        // Strafe right
        case 'KeyR': inputRef.current.up = 1; break;           // Thrust up
        case 'KeyF': inputRef.current.up = -1; break;          // Thrust down
        case 'KeyA': inputRef.current.roll = -1; break;        // Roll left
        case 'KeyD': inputRef.current.roll = 1; break;         // Roll right

        // RIGHT HAND - Steering (Arrow keys)
        case 'ArrowLeft': inputRef.current.yaw = 0.03; break;  // Yaw left
        case 'ArrowRight': inputRef.current.yaw = -0.03; break; // Yaw right
        case 'ArrowUp': inputRef.current.pitch = 0.03; break;  // Pitch up
        case 'ArrowDown': inputRef.current.pitch = -0.03; break; // Pitch down

        // Warp drive
        case 'ShiftLeft':
        case 'Space':
          inputRef.current.warp = true;
          startWarp();
          break;
      }
    };

    const handleKeyUp = (e: KeyboardEvent) => {
      switch (e.code) {
        // Thrust
        case 'KeyW': if (inputRef.current.forward > 0) inputRef.current.forward = 0; break;
        case 'KeyS': if (inputRef.current.forward < 0) inputRef.current.forward = 0; break;
        case 'KeyQ': if (inputRef.current.right < 0) inputRef.current.right = 0; break;
        case 'KeyE': if (inputRef.current.right > 0) inputRef.current.right = 0; break;
        case 'KeyR': if (inputRef.current.up > 0) inputRef.current.up = 0; break;
        case 'KeyF': if (inputRef.current.up < 0) inputRef.current.up = 0; break;
        case 'KeyA': if (inputRef.current.roll < 0) inputRef.current.roll = 0; break;
        case 'KeyD': if (inputRef.current.roll > 0) inputRef.current.roll = 0; break;

        // Steering
        case 'ArrowLeft': if (inputRef.current.yaw > 0) inputRef.current.yaw = 0; break;
        case 'ArrowRight': if (inputRef.current.yaw < 0) inputRef.current.yaw = 0; break;
        case 'ArrowUp': if (inputRef.current.pitch > 0) inputRef.current.pitch = 0; break;
        case 'ArrowDown': if (inputRef.current.pitch < 0) inputRef.current.pitch = 0; break;

        // Warp
        case 'ShiftLeft':
        case 'Space':
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

  // NO POINTER LOCK - Mouse stays free for UI!

  // Main update loop - Flight Sim physics
  useFrame((state, delta) => {
    if (!isPlayerMode) return;

    // Clamp delta to prevent huge jumps
    const clampedDelta = Math.min(delta, 0.1);

    // Combine keyboard and touch input (touch overrides if non-zero)
    const combinedForward = touchInput.forward !== 0 ? touchInput.forward : inputRef.current.forward;
    const combinedRight = touchInput.right !== 0 ? touchInput.right : inputRef.current.right;
    const combinedYaw = touchInput.yaw !== 0 ? touchInput.yaw * 0.03 : inputRef.current.yaw;
    const combinedPitch = touchInput.pitch !== 0 ? touchInput.pitch * 0.03 : inputRef.current.pitch;

    // Combine keyboard warp (inputRef) with store warp (mobile button)
    const combinedWarp = inputRef.current.warp || isWarping;

    // Get propulsion result - steering is continuous (not reset like mouse)
    const result = updatePropulsion(
      position,
      velocity,
      rotation,
      activeVessel,
      {
        forward: combinedForward,
        right: combinedRight,
        up: inputRef.current.up,
        yaw: combinedYaw,
        pitch: combinedPitch,
        roll: inputRef.current.roll,
        warp: combinedWarp,
        delta: clampedDelta,
      }
    );

    // DON'T reset yaw/pitch - they stay active while arrow keys held

    // Update store
    setPosition(result.newPosition);
    setVelocity(result.newVelocity);
    setRotation(result.newRotation);

    // Handle boundary crossing
    if (result.didCrossBoundary && result.crossedAxis) {
      recordBoundaryCross();
      onBoundaryCross(result.crossedAxis);
    }

    // Track black hole state
    blackHoleStateRef.current = result.blackHoleState;

    // Trigger callback when first locked
    if (result.blackHoleState.isLocked && !wasLockedRef.current) {
      wasLockedRef.current = true;
      if (onBlackHoleLock && result.blackHoleState.lockedToHole) {
        onBlackHoleLock(result.blackHoleState.lockedToHole.name);
      }
    }
    if (!result.blackHoleState.isLocked) {
      wasLockedRef.current = false;
    }

    // Update camera to follow player
    // Camera positioned behind and above vessel (scaled for 0.001 Gpc vessels)
    // At 0.005 Gpc (5 Mpc) behind, vessel remains visible against cosmic backdrop
    const cameraOffset = new THREE.Vector3(0, 0.002, 0.005);
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
        playerName={playerName}
        showLabel={true}
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

      {/* Black hole influence zone effect - red tint */}
      {blackHoleStateRef.current.isInInfluenceZone && !blackHoleStateRef.current.isLocked && (
        <mesh>
          <sphereGeometry args={[500, 16, 16]} />
          <meshBasicMaterial
            color="#ff0000"
            transparent
            opacity={0.1}
            side={THREE.BackSide}
          />
        </mesh>
      )}

      {/* GEOMETRIC LOCK effect - intense red/black vortex */}
      {blackHoleStateRef.current.isLocked && (
        <>
          <mesh>
            <sphereGeometry args={[800, 16, 16]} />
            <meshBasicMaterial
              color="#220000"
              transparent
              opacity={0.5}
              side={THREE.BackSide}
            />
          </mesh>
          <mesh rotation={[0, Date.now() * 0.001, 0]}>
            <torusGeometry args={[300, 50, 8, 32]} />
            <meshBasicMaterial color="#ff0000" transparent opacity={0.3} />
          </mesh>
        </>
      )}
    </group>
  );
};

// =============================================================================
// MOBILE CONTROLS - Virtual Joysticks for Touch Devices
// =============================================================================

interface VirtualJoystickProps {
  side: 'left' | 'right';
  onMove: (x: number, y: number) => void;
  onEnd: () => void;
  label: string;
}

const VirtualJoystick: React.FC<VirtualJoystickProps> = ({ side, onMove, onEnd, label }) => {
  const joystickRef = useRef<HTMLDivElement>(null);
  const knobRef = useRef<HTMLDivElement>(null);
  const touchIdRef = useRef<number | null>(null);
  const centerRef = useRef({ x: 0, y: 0 });

  const handleTouchStart = useCallback((e: React.TouchEvent) => {
    if (touchIdRef.current !== null) return;
    const touch = e.touches[0];
    touchIdRef.current = touch.identifier;

    const rect = joystickRef.current?.getBoundingClientRect();
    if (rect) {
      centerRef.current = {
        x: rect.left + rect.width / 2,
        y: rect.top + rect.height / 2,
      };
    }
  }, []);

  const handleTouchMove = useCallback((e: React.TouchEvent) => {
    e.preventDefault();
    const touch = Array.from(e.touches).find(t => t.identifier === touchIdRef.current);
    if (!touch || !joystickRef.current) return;

    const rect = joystickRef.current.getBoundingClientRect();
    const maxDist = rect.width / 2 - 20;

    let dx = touch.clientX - centerRef.current.x;
    let dy = touch.clientY - centerRef.current.y;

    // Clamp to circle
    const dist = Math.sqrt(dx * dx + dy * dy);
    if (dist > maxDist) {
      dx = (dx / dist) * maxDist;
      dy = (dy / dist) * maxDist;
    }

    // Move knob visually
    if (knobRef.current) {
      knobRef.current.style.transform = `translate(${dx}px, ${dy}px)`;
    }

    // Normalize to -1 to 1
    onMove(dx / maxDist, dy / maxDist);
  }, [onMove]);

  const handleTouchEnd = useCallback((e: React.TouchEvent) => {
    const touch = Array.from(e.changedTouches).find(t => t.identifier === touchIdRef.current);
    if (touch) {
      touchIdRef.current = null;
      if (knobRef.current) {
        knobRef.current.style.transform = 'translate(0px, 0px)';
      }
      onEnd();
    }
  }, [onEnd]);

  return (
    <div
      ref={joystickRef}
      className={`absolute bottom-24 ${side === 'left' ? 'left-4' : 'right-4'} w-28 h-28 sm:w-32 sm:h-32 rounded-full bg-black/40 border-2 border-cyan-500/50 flex items-center justify-center touch-none`}
      onTouchStart={handleTouchStart}
      onTouchMove={handleTouchMove}
      onTouchEnd={handleTouchEnd}
    >
      {/* Label */}
      <div className="absolute -top-6 text-cyan-400 text-xs font-mono">{label}</div>
      {/* Knob */}
      <div
        ref={knobRef}
        className="w-12 h-12 sm:w-14 sm:h-14 rounded-full bg-cyan-500/60 border-2 border-cyan-400 transition-transform duration-75"
      />
    </div>
  );
};

// Mobile controls overlay
export const MobileControls: React.FC<{
  onLeftJoystick: (x: number, y: number) => void;
  onRightJoystick: (x: number, y: number) => void;
  onLeftEnd: () => void;
  onRightEnd: () => void;
  onWarpStart: () => void;
  onWarpEnd: () => void;
  isWarping: boolean;
}> = ({ onLeftJoystick, onRightJoystick, onLeftEnd, onRightEnd, onWarpStart, onWarpEnd, isWarping }) => {
  return (
    <div className="absolute inset-0 pointer-events-none z-30 md:hidden">
      {/* Left joystick - Thrust */}
      <div className="pointer-events-auto">
        <VirtualJoystick
          side="left"
          onMove={onLeftJoystick}
          onEnd={onLeftEnd}
          label="THRUST"
        />
      </div>

      {/* Right joystick - Steering */}
      <div className="pointer-events-auto">
        <VirtualJoystick
          side="right"
          onMove={onRightJoystick}
          onEnd={onRightEnd}
          label="STEER"
        />
      </div>

      {/* Warp button */}
      <div className="pointer-events-auto absolute bottom-28 left-1/2 -translate-x-1/2">
        <button
          onTouchStart={onWarpStart}
          onTouchEnd={onWarpEnd}
          className={`px-6 py-3 rounded-full font-bold text-sm transition-all ${
            isWarping
              ? 'bg-orange-500 text-white animate-pulse'
              : 'bg-black/60 text-orange-400 border-2 border-orange-500/50'
          }`}
        >
          {isWarping ? '⚡ WARPING' : '🚀 WARP'}
        </button>
      </div>

      {/* Up/Down buttons */}
      <div className="pointer-events-auto absolute right-4 top-1/2 -translate-y-1/2 flex flex-col gap-2">
        <button
          onTouchStart={(e) => { e.preventDefault(); }}
          className="w-12 h-12 rounded-full bg-black/60 border-2 border-slate-500/50 text-slate-400 font-bold"
        >
          ↑
        </button>
        <button
          onTouchStart={(e) => { e.preventDefault(); }}
          className="w-12 h-12 rounded-full bg-black/60 border-2 border-slate-500/50 text-slate-400 font-bold"
        >
          ↓
        </button>
      </div>
    </div>
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
    startWarp,
    stopWarp,
    setTouchInput,
  } = usePlayerStore();

  // Mobile control handlers
  const handleLeftJoystick = useCallback((x: number, y: number) => {
    setTouchInput({ right: x, forward: -y }); // Y inverted for intuitive control
  }, [setTouchInput]);

  const handleRightJoystick = useCallback((x: number, y: number) => {
    setTouchInput({ yaw: -x, pitch: -y }); // Inverted for intuitive control
  }, [setTouchInput]);

  const handleLeftEnd = useCallback(() => {
    setTouchInput({ forward: 0, right: 0 });
  }, [setTouchInput]);

  const handleRightEnd = useCallback(() => {
    setTouchInput({ yaw: 0, pitch: 0 });
  }, [setTouchInput]);

  if (!isPlayerMode) return null;

  const speed = Math.sqrt(velocity.x ** 2 + velocity.y ** 2 + velocity.z ** 2);
  const quadrant = getQuadrantInfo(position);
  const boundary = distanceToNearestBoundary(position);

  // Find nearest black hole
  const nearestBlackHole = COSMIC_BLACK_HOLES.reduce((nearest, hole) => {
    const dx = position.x - hole.position.x;
    const dy = position.y - hole.position.y;
    const dz = position.z - hole.position.z;
    const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
    if (!nearest || dist < nearest.distance) {
      return { hole, distance: dist };
    }
    return nearest;
  }, null as { hole: typeof COSMIC_BLACK_HOLES[0]; distance: number } | null);

  const isNearBlackHole = nearestBlackHole && nearestBlackHole.distance < nearestBlackHole.hole.influenceRadius_gpc;
  const isLockedInBlackHole = nearestBlackHole && nearestBlackHole.distance < nearestBlackHole.hole.eventHorizon_gpc;

  return (
    <div className="absolute inset-0 pointer-events-none z-40">
      {/* Mobile Controls - Only visible on small screens */}
      <MobileControls
        onLeftJoystick={handleLeftJoystick}
        onRightJoystick={handleRightJoystick}
        onLeftEnd={handleLeftEnd}
        onRightEnd={handleRightEnd}
        onWarpStart={startWarp}
        onWarpEnd={stopWarp}
        isWarping={isWarping}
      />

      {/* Top bar - Responsive */}
      <div className="absolute top-2 sm:top-4 left-1/2 -translate-x-1/2 bg-black/80 border border-cyan-500/50 rounded-lg px-3 sm:px-6 py-1 sm:py-2 flex items-center gap-2 sm:gap-6 pointer-events-auto">
        <div className="text-cyan-400 font-mono text-xs sm:text-sm">
          <span className="text-slate-500 hidden sm:inline">VESSEL:</span> {activeVessel.toUpperCase()}
        </div>
        <div className={`font-mono text-xs sm:text-sm ${isWarping ? 'text-orange-400 animate-pulse' : 'text-slate-400'}`}>
          {isWarping ? '⚡ WARP' : 'SUB-LIGHT'}
        </div>
        <button
          onClick={stopPlayerMode}
          className="text-red-400 hover:text-red-300 text-xs sm:text-sm font-bold"
        >
          EXIT
        </button>
      </div>

      {/* Left panel - Position (hidden on mobile) */}
      <div className="hidden md:block absolute left-4 top-1/2 -translate-y-1/2 bg-black/80 border border-slate-600 rounded-lg p-4 font-mono text-xs space-y-2">
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

      {/* Right panel - Stats (hidden on mobile, compact on tablet) */}
      <div className="hidden sm:block absolute right-2 sm:right-4 top-16 sm:top-1/2 sm:-translate-y-1/2 bg-black/80 border border-slate-600 rounded-lg p-2 sm:p-4 font-mono text-[10px] sm:text-xs space-y-1 sm:space-y-2">
        <div className="text-slate-500 mb-1 sm:mb-2">TELEMETRY</div>
        <div>
          <span className="text-slate-500">SPEED:</span>
          <span className="text-green-400 ml-1 sm:ml-2">{speed.toFixed(4)}</span>
        </div>
        <div className="hidden sm:block">
          <span className="text-slate-500">FROM ORIGIN:</span>
          <span className="text-white ml-2">{quadrant.distanceFromOrigin.toFixed(2)} Gpc</span>
        </div>
        <div className="border-t border-slate-700 pt-1 sm:pt-2 mt-1 sm:mt-2">
          <div className="text-slate-500">TO BOUNDARY</div>
          <div className={boundary.distance < 1 ? 'text-orange-400' : 'text-white'}>
            {boundary.distance.toFixed(2)} ({boundary.axis.toUpperCase()})
          </div>
        </div>
        <div className="border-t border-slate-700 pt-1 sm:pt-2 mt-1 sm:mt-2">
          <div className="text-slate-500">TOPOLOGY</div>
          <div className="text-cyan-400">T³: {boundariesCrossed}</div>
          <div className="text-purple-400">Z₂: {parityFlips}</div>
          <div className={currentParity === 1 ? 'text-green-400' : 'text-red-400'}>
            P: {currentParity === 1 ? '+1' : '-1'}
          </div>
        </div>
        {nearestBlackHole && (
          <div className="border-t border-slate-700 pt-1 sm:pt-2 mt-1 sm:mt-2">
            <div className="text-slate-500">BLACK HOLE</div>
            <div className={isLockedInBlackHole ? 'text-red-500' : isNearBlackHole ? 'text-orange-400' : 'text-white'}>
              {nearestBlackHole.hole.name.split(' ')[0]}
            </div>
            <div className={isNearBlackHole ? 'text-red-400' : 'text-slate-400'}>
              {nearestBlackHole.distance.toFixed(3)}
            </div>
          </div>
        )}
      </div>

      {/* Mobile mini-stats - Top right corner on small screens */}
      <div className="sm:hidden absolute top-12 right-2 bg-black/70 border border-slate-600 rounded px-2 py-1 font-mono text-[9px]">
        <div className="text-green-400">{speed.toFixed(3)} Gpc/s</div>
        <div className={boundary.distance < 1 ? 'text-orange-400' : 'text-slate-400'}>
          {boundary.axis.toUpperCase()}: {boundary.distance.toFixed(1)}
        </div>
      </div>

      {/* Bottom - Controls reminder - Desktop only */}
      <div className="hidden md:block absolute bottom-4 left-1/2 -translate-x-1/2 bg-black/80 border border-slate-700 rounded-lg px-6 py-3 font-mono">
        <div className="flex gap-8 text-xs">
          <div className="text-slate-400">
            <div className="text-cyan-400 font-bold mb-1">LEFT HAND</div>
            <div>W/S: Throttle</div>
            <div>Q/E: Strafe</div>
            <div>R/F: Up/Down</div>
            <div>A/D: Roll</div>
          </div>
          <div className="text-slate-400">
            <div className="text-orange-400 font-bold mb-1">RIGHT HAND</div>
            <div>← →: Turn</div>
            <div>↑ ↓: Pitch</div>
            <div className="text-yellow-400 mt-1">SHIFT/SPACE: Warp</div>
          </div>
        </div>
      </div>

      {/* Boundary proximity warning */}
      {boundary.distance < 1 && !isLockedInBlackHole && (
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-center">
          <div className="text-2xl font-bold text-orange-400 animate-pulse">
            ⚠️ APPROACHING {boundary.axis.toUpperCase()} BOUNDARY
          </div>
          <div className="text-orange-300 text-sm">
            {boundary.distance.toFixed(2)} Gpc to T³ wrap
          </div>
        </div>
      )}

      {/* Black hole gravitational influence warning */}
      {isNearBlackHole && !isLockedInBlackHole && nearestBlackHole && (
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-center">
          <div className="text-2xl font-bold text-red-400 animate-pulse">
            ⚠️ GRAVITATIONAL INFLUENCE: {nearestBlackHole.hole.name}
          </div>
          <div className="text-red-300 text-sm">
            {nearestBlackHole.distance.toFixed(4)} Gpc to event horizon
          </div>
          <div className="text-yellow-400 text-xs mt-1">
            WARNING: Geodesics bending toward singularity
          </div>
        </div>
      )}

      {/* GEOMETRIC LOCK - No escape! */}
      {isLockedInBlackHole && nearestBlackHole && (
        <div className="absolute inset-0 flex items-center justify-center bg-red-900/30">
          <div className="text-center">
            <div className="text-4xl font-bold text-red-500 animate-pulse mb-2">
              ⛔ GEOMETRIC LOCK ⛔
            </div>
            <div className="text-2xl text-red-400">
              {nearestBlackHole.hole.name}
            </div>
            <div className="text-red-300 text-lg mt-2">
              All geodesics lead to the singularity
            </div>
            <div className="text-white/60 text-sm mt-4 font-mono">
              Distance: {nearestBlackHole.distance.toFixed(6)} Gpc
            </div>
            <div className="text-red-200/80 text-xs mt-2">
              No escape possible - T³/Z₂ topology cannot save you here
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PlayerController;

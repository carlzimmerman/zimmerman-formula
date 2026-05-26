/**
 * =============================================================================
 * OTHER PLAYERS RENDERER - Multiplayer Vessel Visualization
 * =============================================================================
 *
 * Renders other players' vessels in the 3D scene with:
 * - Position interpolation for smooth movement
 * - Vessel type matching
 * - Player name labels
 * - Warp trail effects
 * - Parity indicator (Z₂ state)
 *
 * =============================================================================
 */

'use client';

import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Html } from '@react-three/drei';
import * as THREE from 'three';
import { useMultiplayerStore, OtherPlayer } from '@/store/multiplayerStore';
import { VESSEL_CONFIGS, VesselType } from '@/store/playerStore';

// =============================================================================
// INTERPOLATION HELPER
// =============================================================================

function lerp(a: number, b: number, t: number): number {
  return a + (b - a) * t;
}

function lerpVector3(
  current: THREE.Vector3,
  target: { x: number; y: number; z: number },
  t: number
): void {
  current.x = lerp(current.x, target.x, t);
  current.y = lerp(current.y, target.y, t);
  current.z = lerp(current.z, target.z, t);
}

// =============================================================================
// OTHER PLAYER VESSEL COMPONENT
// =============================================================================

interface OtherPlayerVesselProps {
  player: OtherPlayer;
}

function OtherPlayerVessel({ player }: OtherPlayerVesselProps) {
  const groupRef = useRef<THREE.Group>(null);
  const currentPosition = useRef(new THREE.Vector3(
    player.position.x,
    player.position.y,
    player.position.z
  ));
  const currentRotation = useRef(new THREE.Euler(
    player.rotation.x,
    player.rotation.y,
    player.rotation.z
  ));

  const vesselConfig = VESSEL_CONFIGS[player.vessel] || VESSEL_CONFIGS.ufo;
  const scale = vesselConfig.scale;

  // Interpolate position smoothly
  useFrame((_, delta) => {
    if (!groupRef.current) return;

    // Interpolation factor (adjust for smoother/snappier movement)
    const lerpFactor = Math.min(1, delta * 8);

    // Interpolate position
    lerpVector3(currentPosition.current, player.position, lerpFactor);
    groupRef.current.position.copy(currentPosition.current);

    // Interpolate rotation
    currentRotation.current.x = lerp(currentRotation.current.x, player.rotation.x, lerpFactor);
    currentRotation.current.y = lerp(currentRotation.current.y, player.rotation.y, lerpFactor);
    currentRotation.current.z = lerp(currentRotation.current.z, player.rotation.z, lerpFactor);
    groupRef.current.rotation.copy(currentRotation.current);
  });

  // Vessel geometry based on type
  const vesselGeometry = useMemo(() => {
    switch (player.vessel) {
      case 'ufo':
        return <capsuleGeometry args={[scale * 0.5, scale * 0.3, 8, 16]} />;
      case 'truck':
        return <boxGeometry args={[scale * 1.5, scale * 0.8, scale * 0.8]} />;
      case 'sedan':
        return <capsuleGeometry args={[scale * 0.4, scale * 0.6, 4, 12]} />;
      case 'plane':
        return <coneGeometry args={[scale * 0.3, scale * 1.2, 6]} />;
      case 'donut':
        return <torusGeometry args={[scale * 0.5, scale * 0.2, 16, 32]} />;
      default:
        return <sphereGeometry args={[scale * 0.5, 16, 16]} />;
    }
  }, [player.vessel, scale]);

  return (
    <group ref={groupRef}>
      {/* Main vessel mesh */}
      <mesh castShadow>
        {vesselGeometry}
        <meshStandardMaterial
          color={player.color}
          emissive={player.color}
          emissiveIntensity={player.isWarping ? 0.5 : 0.2}
          metalness={0.7}
          roughness={0.3}
        />
      </mesh>

      {/* Warp glow when warping */}
      {player.isWarping && (
        <mesh scale={1.3}>
          {vesselGeometry}
          <meshBasicMaterial
            color={player.color}
            transparent
            opacity={0.3}
            side={THREE.BackSide}
          />
        </mesh>
      )}

      {/* Parity indicator ring */}
      <mesh rotation={[Math.PI / 2, 0, 0]} position={[0, scale * 0.6, 0]}>
        <ringGeometry args={[scale * 0.15, scale * 0.2, 16]} />
        <meshBasicMaterial
          color={player.currentParity === 1 ? '#00ff00' : '#ff0000'}
          transparent
          opacity={0.8}
          side={THREE.DoubleSide}
        />
      </mesh>

      {/* Player name label - small but visible */}
      <Html
        position={[0, scale * 1.5, 0]}
        center
        distanceFactor={8}
        occlude={false}
        style={{
          pointerEvents: 'none',
          userSelect: 'none',
        }}
      >
        <div
          style={{
            position: 'relative',
            display: 'flex',
            alignItems: 'center',
            gap: '4px',
            background: 'rgba(0, 0, 0, 0.9)',
            color: player.color,
            padding: '3px 8px',
            borderRadius: '12px',
            fontSize: '9px',
            fontWeight: 'bold',
            whiteSpace: 'nowrap',
            border: `1.5px solid ${player.color}`,
            boxShadow: `0 0 10px ${player.color}50, 0 2px 6px rgba(0,0,0,0.6)`,
            textShadow: `0 0 4px ${player.color}`,
            letterSpacing: '0.3px',
          }}
        >
          {/* Vessel icon */}
          <span style={{ fontSize: '10px' }}>
            {player.vessel === 'ufo' && '🛸'}
            {player.vessel === 'truck' && '🚛'}
            {player.vessel === 'sedan' && '🚗'}
            {player.vessel === 'plane' && '✈️'}
            {player.vessel === 'donut' && '🍩'}
          </span>
          {player.name}
          {/* Warp indicator - inline */}
          {player.isWarping && (
            <span
              style={{
                background: '#00ffff',
                color: '#000',
                padding: '1px 3px',
                borderRadius: '4px',
                fontSize: '6px',
                fontWeight: 'bold',
                marginLeft: '2px',
              }}
            >
              ⚡
            </span>
          )}
        </div>
      </Html>

      {/* Direction indicator (velocity arrow) */}
      {(Math.abs(player.velocity.x) > 0.001 ||
        Math.abs(player.velocity.y) > 0.001 ||
        Math.abs(player.velocity.z) > 0.001) && (
        <arrowHelper
          args={[
            new THREE.Vector3(
              player.velocity.x,
              player.velocity.y,
              player.velocity.z
            ).normalize(),
            new THREE.Vector3(0, 0, 0),
            scale * 2,
            player.isWarping ? 0x00ffff : 0xffff00,
            scale * 0.3,
            scale * 0.15,
          ]}
        />
      )}
    </group>
  );
}

// =============================================================================
// MAIN COMPONENT
// =============================================================================

export function OtherPlayersRenderer() {
  const { otherPlayers, isConnected, isMultiplayerEnabled } = useMultiplayerStore();

  // Don't render if multiplayer is disabled
  if (!isMultiplayerEnabled || !isConnected) {
    return null;
  }

  // Convert Map to array for rendering
  const playersArray = Array.from(otherPlayers.values());

  // Filter out stale players (no update in 10 seconds)
  const activePlayers = playersArray.filter(
    (player) => Date.now() - player.lastUpdate < 10000
  );

  return (
    <group name="other-players">
      {activePlayers.map((player) => (
        <OtherPlayerVessel key={player.id} player={player} />
      ))}
    </group>
  );
}

// =============================================================================
// MULTIPLAYER HUD COMPONENT
// =============================================================================

export function MultiplayerHUD() {
  const {
    isConnected,
    isMultiplayerEnabled,
    playerCount,
    otherPlayers,
  } = useMultiplayerStore();

  if (!isMultiplayerEnabled) return null;

  const activePlayers = Array.from(otherPlayers.values()).filter(
    (p) => Date.now() - p.lastUpdate < 10000
  );

  return (
    <div className="absolute top-20 right-4 bg-black/80 border border-cyan-500/50 rounded-lg p-3 text-xs backdrop-blur-sm">
      <div className="flex items-center gap-2 mb-2">
        <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
        <span className="text-cyan-400 font-bold">MULTIPLAYER</span>
      </div>

      <div className="space-y-1 text-gray-300">
        <div className="flex justify-between gap-4">
          <span className="text-gray-500">Status:</span>
          <span className={isConnected ? 'text-green-400' : 'text-red-400'}>
            {isConnected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
        <div className="flex justify-between gap-4">
          <span className="text-gray-500">Players:</span>
          <span className="text-white font-mono">{activePlayers.length + 1}</span>
        </div>
      </div>

      {/* Player list */}
      {activePlayers.length > 0 && (
        <div className="mt-2 pt-2 border-t border-cyan-500/30">
          <div className="text-gray-500 mb-1">Nearby Pilots:</div>
          <div className="space-y-1 max-h-32 overflow-y-auto">
            {activePlayers.slice(0, 8).map((player) => (
              <div
                key={player.id}
                className="flex items-center gap-2 text-xs"
              >
                <div
                  className="w-2 h-2 rounded-full"
                  style={{ backgroundColor: player.color }}
                />
                <span style={{ color: player.color }}>{player.name}</span>
                <span className="text-gray-600 text-[10px]">
                  [{player.vessel}]
                </span>
              </div>
            ))}
            {activePlayers.length > 8 && (
              <div className="text-gray-500">
                +{activePlayers.length - 8} more...
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default OtherPlayersRenderer;

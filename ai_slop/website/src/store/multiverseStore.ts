// =============================================================================
// MULTIVERSE STORE (Directive ZZZ)
// =============================================================================
// Prepared for future multiplayer support
// Stores other players' positions and vessel types for instanced rendering
// =============================================================================

import { create } from 'zustand';
import * as THREE from 'three';
import { VesselType } from './playerStore';

// Other player state (received from server)
export interface OtherPlayerState {
  id: string;
  position: Float64Array; // [x, y, z] in Gpc
  velocity: THREE.Vector3;
  rotation: THREE.Euler;
  vesselType: VesselType;
  isWarping: boolean;
  parity: 1 | -1;
  lastUpdate: number; // Timestamp for interpolation
}

interface MultiverseState {
  // Connected players
  otherPlayers: Map<string, OtherPlayerState>;

  // Connection state
  isConnected: boolean;
  playerId: string | null;

  // Actions
  setConnected: (connected: boolean, playerId?: string) => void;
  updatePlayer: (id: string, state: Partial<OtherPlayerState>) => void;
  removePlayer: (id: string) => void;
  clearPlayers: () => void;

  // For instanced rendering
  getPlayersByVessel: (vesselType: VesselType) => OtherPlayerState[];
  getAllPlayers: () => OtherPlayerState[];
}

export const useMultiverseStore = create<MultiverseState>((set, get) => ({
  otherPlayers: new Map(),
  isConnected: false,
  playerId: null,

  setConnected: (connected, playerId) => set({
    isConnected: connected,
    playerId: playerId || null,
  }),

  updatePlayer: (id, state) => set((prev) => {
    const players = new Map(prev.otherPlayers);
    const existing = players.get(id);

    if (existing) {
      players.set(id, { ...existing, ...state, lastUpdate: Date.now() });
    } else {
      // New player - create full state
      players.set(id, {
        id,
        position: state.position || new Float64Array([0, 0, 0]),
        velocity: state.velocity || new THREE.Vector3(),
        rotation: state.rotation || new THREE.Euler(),
        vesselType: state.vesselType || 'ufo',
        isWarping: state.isWarping || false,
        parity: state.parity || 1,
        lastUpdate: Date.now(),
      });
    }

    return { otherPlayers: players };
  }),

  removePlayer: (id) => set((prev) => {
    const players = new Map(prev.otherPlayers);
    players.delete(id);
    return { otherPlayers: players };
  }),

  clearPlayers: () => set({ otherPlayers: new Map() }),

  getPlayersByVessel: (vesselType) => {
    return Array.from(get().otherPlayers.values())
      .filter((p) => p.vesselType === vesselType);
  },

  getAllPlayers: () => Array.from(get().otherPlayers.values()),
}));

// =============================================================================
// INSTANCED MESH HELPER
// =============================================================================
// For efficient rendering of many players using GPU instancing
// Each vessel type gets its own InstancedMesh

export interface InstanceData {
  vesselType: VesselType;
  matrices: THREE.Matrix4[];
  colors: THREE.Color[];
  count: number;
}

/**
 * Generate instance matrices for all players of a given vessel type
 * To be called each frame for updating InstancedMesh
 */
export function generateInstanceData(
  players: OtherPlayerState[],
  localPlayerPosition: Float64Array
): InstanceData[] {
  const vesselTypes: VesselType[] = ['ufo', 'truck', 'sedan', 'plane', 'donut'];
  const instanceData: InstanceData[] = [];

  for (const vesselType of vesselTypes) {
    const playersOfType = players.filter((p) => p.vesselType === vesselType);

    if (playersOfType.length === 0) {
      instanceData.push({
        vesselType,
        matrices: [],
        colors: [],
        count: 0,
      });
      continue;
    }

    const matrices: THREE.Matrix4[] = [];
    const colors: THREE.Color[] = [];

    for (const player of playersOfType) {
      // Calculate position relative to local player (floating origin)
      const relativePos = new THREE.Vector3(
        player.position[0] - localPlayerPosition[0],
        player.position[1] - localPlayerPosition[1],
        player.position[2] - localPlayerPosition[2]
      );

      // Create transformation matrix
      const matrix = new THREE.Matrix4();
      matrix.compose(
        relativePos,
        new THREE.Quaternion().setFromEuler(player.rotation),
        new THREE.Vector3(1, 1, 1).multiplyScalar(player.parity)
      );

      matrices.push(matrix);
      colors.push(new THREE.Color(player.isWarping ? 0x00ffff : 0xffffff));
    }

    instanceData.push({
      vesselType,
      matrices,
      colors,
      count: playersOfType.length,
    });
  }

  return instanceData;
}

// =============================================================================
// NETWORK MESSAGE TYPES (for future WebSocket integration)
// =============================================================================

export interface NetworkMessage {
  type: 'join' | 'leave' | 'update' | 'sync';
  playerId: string;
  data?: Partial<OtherPlayerState>;
  timestamp: number;
}

/**
 * Serialize local player state for network transmission
 */
export function serializePlayerState(
  position: Float64Array,
  velocity: THREE.Vector3,
  rotation: THREE.Euler,
  vesselType: VesselType,
  isWarping: boolean,
  parity: 1 | -1
): NetworkMessage {
  return {
    type: 'update',
    playerId: '', // Will be set by server
    data: {
      position,
      velocity,
      rotation,
      vesselType,
      isWarping,
      parity,
    },
    timestamp: Date.now(),
  };
}

/**
 * Interpolate player position for smooth rendering between updates
 */
export function interpolatePlayer(
  player: OtherPlayerState,
  currentTime: number,
  interpolationTime: number = 100 // ms
): THREE.Vector3 {
  const timeSinceUpdate = currentTime - player.lastUpdate;
  const t = Math.min(timeSinceUpdate / interpolationTime, 1);

  // Simple linear extrapolation based on velocity
  return new THREE.Vector3(
    player.position[0] + player.velocity.x * t * 0.001,
    player.position[1] + player.velocity.y * t * 0.001,
    player.position[2] + player.velocity.z * t * 0.001
  );
}

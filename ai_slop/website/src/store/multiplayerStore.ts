/**
 * =============================================================================
 * MULTIPLAYER STORE - Z² Universe Player Synchronization
 * =============================================================================
 *
 * Zustand store for managing multiplayer state:
 * - Other players' positions, rotations, and vessel types
 * - Connection status
 * - Room/session management
 *
 * Uses Firebase Realtime Database for synchronization.
 * =============================================================================
 */

import { create } from 'zustand';
import { VesselType } from './playerStore';

// =============================================================================
// TYPES
// =============================================================================

export interface OtherPlayer {
  id: string;
  name: string;
  vessel: VesselType;
  position: { x: number; y: number; z: number };
  rotation: { x: number; y: number; z: number };
  velocity: { x: number; y: number; z: number };
  isWarping: boolean;
  currentParity: 1 | -1;
  lastUpdate: number;
  color: string;
}

export interface MultiplayerState {
  // Connection
  isConnected: boolean;
  isMultiplayerEnabled: boolean;
  playerId: string | null;

  // Other players
  otherPlayers: Map<string, OtherPlayer>;

  // Settings
  updateRate: number; // Updates per second to send
  interpolationDelay: number; // ms delay for smooth interpolation
  maxPlayers: number;

  // Stats
  playerCount: number;
  latency: number;

  // Actions
  setConnected: (connected: boolean) => void;
  setMultiplayerEnabled: (enabled: boolean) => void;
  setPlayerId: (id: string | null) => void;

  updateOtherPlayer: (player: OtherPlayer) => void;
  removeOtherPlayer: (id: string) => void;
  clearOtherPlayers: () => void;

  setPlayerCount: (count: number) => void;
  setLatency: (latency: number) => void;
}

// =============================================================================
// STORE
// =============================================================================

export const useMultiplayerStore = create<MultiplayerState>((set, get) => ({
  // Initial state
  isConnected: false,
  isMultiplayerEnabled: false,
  playerId: null,

  otherPlayers: new Map(),

  updateRate: 10, // 10 updates per second
  interpolationDelay: 100, // 100ms interpolation delay
  maxPlayers: 50,

  playerCount: 0,
  latency: 0,

  // Actions
  setConnected: (connected) => set({ isConnected: connected }),
  setMultiplayerEnabled: (enabled) => set({ isMultiplayerEnabled: enabled }),
  setPlayerId: (id) => set({ playerId: id }),

  updateOtherPlayer: (player) => set((state) => {
    const newPlayers = new Map(state.otherPlayers);
    newPlayers.set(player.id, player);
    return { otherPlayers: newPlayers, playerCount: newPlayers.size };
  }),

  removeOtherPlayer: (id) => set((state) => {
    const newPlayers = new Map(state.otherPlayers);
    newPlayers.delete(id);
    return { otherPlayers: newPlayers, playerCount: newPlayers.size };
  }),

  clearOtherPlayers: () => set({ otherPlayers: new Map(), playerCount: 0 }),

  setPlayerCount: (count) => set({ playerCount: count }),
  setLatency: (latency) => set({ latency }),
}));

// =============================================================================
// HELPER: Generate random player color
// =============================================================================

export function generatePlayerColor(): string {
  const hue = Math.random() * 360;
  return `hsl(${hue}, 70%, 60%)`;
}

// =============================================================================
// HELPER: Generate unique player ID
// =============================================================================

export function generatePlayerId(): string {
  return `player_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

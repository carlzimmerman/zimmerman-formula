// =============================================================================
// PLAYER STORE - Z² Orbifold Flight Simulator State
// =============================================================================
// Manages player vessel, position, and propulsion state using Zustand
// Architected for future multiplayer support (Directive ZZZ)
// =============================================================================

import { create } from 'zustand';

// Plain object types for SSR-safe state (THREE objects created at runtime)
interface Vector3Like {
  x: number;
  y: number;
  z: number;
}

interface EulerLike {
  x: number;
  y: number;
  z: number;
}

// Vessel types available to players
export type VesselType = 'ufo' | 'truck' | 'sedan' | 'plane' | 'donut';

export interface VesselConfig {
  id: VesselType;
  name: string;
  description: string;
  color: string;
  scale: number;
  maxSpeed: number; // Gpc per second at warp
  acceleration: number;
}

// Vessel scale factor: 0.001 Gpc = 1 Mpc (roughly galaxy-cluster scale for visibility)
// The Sun is ~4.5×10⁻¹⁷ Gpc - we use larger for gameplay visibility
const VESSEL_SCALE_BASE = 0.001; // Base scale in Gpc

export const VESSEL_CONFIGS: Record<VesselType, VesselConfig> = {
  ufo: {
    id: 'ufo',
    name: 'Classic Saucer',
    description: 'Retro flying saucer with smooth handling',
    color: '#00ff88',
    scale: VESSEL_SCALE_BASE * 1.0,
    maxSpeed: 2.0,
    acceleration: 0.5,
  },
  truck: {
    id: 'truck',
    name: 'Space Trucker',
    description: 'Heavy hauler - slow but steady',
    color: '#ff6600',
    scale: VESSEL_SCALE_BASE * 1.5,
    maxSpeed: 1.0,
    acceleration: 0.2,
  },
  sedan: {
    id: 'sedan',
    name: 'Cosmic Taxi',
    description: 'Nimble space sedan for quick trips',
    color: '#ffcc00',
    scale: VESSEL_SCALE_BASE * 0.8,
    maxSpeed: 3.0,
    acceleration: 0.8,
  },
  plane: {
    id: 'plane',
    name: 'Starfighter',
    description: 'Fast and agile spacecraft',
    color: '#0088ff',
    scale: VESSEL_SCALE_BASE * 1.2,
    maxSpeed: 4.0,
    acceleration: 1.0,
  },
  donut: {
    id: 'donut',
    name: 'The Cosmic Donut',
    description: 'A giant space donut. Why not?',
    color: '#ff88cc',
    scale: VESSEL_SCALE_BASE * 2.0,
    maxSpeed: 1.5,
    acceleration: 0.3,
  },
};

// Float64 position for cosmic-scale precision
export interface PlayerPosition {
  // High precision position in Gpc
  x: number;
  y: number;
  z: number;
}

// Player state
export interface PlayerState {
  // Mode
  isPlayerMode: boolean;
  isSelectingVessel: boolean;

  // Player identity (for labels/multiplayer)
  playerName: string;

  // Vessel
  activeVessel: VesselType;

  // Position (Float64 precision in Gpc)
  position: PlayerPosition;

  // Velocity vector (Gpc per second)
  velocity: Vector3Like;

  // Rotation (Euler angles)
  rotation: EulerLike;

  // Propulsion state
  isWarping: boolean;
  warpFactor: number; // 0-1, multiplier for speed

  // T³/Z₂ state
  boundariesCrossed: number;
  parityFlips: number;
  currentParity: 1 | -1; // +1 or -1 for Z₂

  // Actions
  setVessel: (vessel: VesselType) => void;
  startPlayerMode: () => void;
  stopPlayerMode: () => void;
  openVesselSelector: () => void;
  closeVesselSelector: () => void;
  setPlayerName: (name: string) => void;

  // Movement
  setPosition: (pos: PlayerPosition) => void;
  setVelocity: (vel: Vector3Like) => void;
  setRotation: (rot: EulerLike) => void;

  // Propulsion
  startWarp: () => void;
  stopWarp: () => void;
  setWarpFactor: (factor: number) => void;

  // T³/Z₂ events
  recordBoundaryCross: () => void;
  recordParityFlip: () => void;
  flipParity: () => void;

  // Reset
  resetToOrigin: () => void;
}

// Initial position: Earth orbit (origin of the fundamental domain)
const INITIAL_POSITION: PlayerPosition = { x: 0, y: 0, z: 0 };

export const usePlayerStore = create<PlayerState>((set, get) => ({
  // Initial state
  isPlayerMode: false,
  isSelectingVessel: false,
  playerName: 'Pilot', // Default name, can be customized
  activeVessel: 'ufo',
  position: { ...INITIAL_POSITION },
  velocity: { x: 0, y: 0, z: 0 },
  rotation: { x: 0, y: 0, z: 0 },
  isWarping: false,
  warpFactor: 0,
  boundariesCrossed: 0,
  parityFlips: 0,
  currentParity: 1,

  // Actions
  setVessel: (vessel) => set({ activeVessel: vessel }),

  startPlayerMode: () => set({
    isPlayerMode: true,
    isSelectingVessel: false,
    position: { ...INITIAL_POSITION },
    velocity: { x: 0, y: 0, z: 0 },
    boundariesCrossed: 0,
    parityFlips: 0,
    currentParity: 1,
  }),

  stopPlayerMode: () => set({
    isPlayerMode: false,
    isWarping: false,
    warpFactor: 0,
  }),

  openVesselSelector: () => set({ isSelectingVessel: true }),
  closeVesselSelector: () => set({ isSelectingVessel: false }),
  setPlayerName: (name) => set({ playerName: name }),

  // Movement
  setPosition: (pos) => set({ position: pos }),
  setVelocity: (vel) => set({ velocity: { x: vel.x, y: vel.y, z: vel.z } }),
  setRotation: (rot) => set({ rotation: { x: rot.x, y: rot.y, z: rot.z } }),

  // Propulsion
  startWarp: () => set({ isWarping: true }),
  stopWarp: () => set({ isWarping: false, warpFactor: 0 }),
  setWarpFactor: (factor) => set({ warpFactor: Math.max(0, Math.min(1, factor)) }),

  // T³/Z₂ events
  recordBoundaryCross: () => set((state) => ({
    boundariesCrossed: state.boundariesCrossed + 1,
  })),
  recordParityFlip: () => set((state) => ({
    parityFlips: state.parityFlips + 1,
  })),
  flipParity: () => set((state) => ({
    currentParity: state.currentParity === 1 ? -1 : 1,
  })),

  // Reset
  resetToOrigin: () => set({
    position: { ...INITIAL_POSITION },
    velocity: { x: 0, y: 0, z: 0 },
    rotation: { x: 0, y: 0, z: 0 },
    isWarping: false,
    warpFactor: 0,
    boundariesCrossed: 0,
    parityFlips: 0,
    currentParity: 1,
  }),
}));

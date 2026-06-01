/**
 * =============================================================================
 * USE MULTIPLAYER HOOK - Firebase Realtime Synchronization
 * =============================================================================
 *
 * Hook for managing multiplayer synchronization:
 * - Connects to Firebase Realtime Database
 * - Broadcasts local player position
 * - Subscribes to other players' positions
 * - Handles player join/leave with onDisconnect
 * - Throttles updates for performance
 *
 * =============================================================================
 */

import { useEffect, useRef, useCallback } from 'react';
import {
  ref,
  set,
  onValue,
  onDisconnect,
  remove,
  serverTimestamp,
  off,
  DataSnapshot,
} from 'firebase/database';
import { getFirebaseDatabase } from '@/lib/firebase';
import { useMultiplayerStore, generatePlayerId, generatePlayerColor, OtherPlayer } from '@/store/multiplayerStore';
import { usePlayerStore, VesselType } from '@/store/playerStore';

// =============================================================================
// TYPES
// =============================================================================

interface PlayerData {
  name: string;
  vessel: VesselType;
  position: { x: number; y: number; z: number };
  rotation: { x: number; y: number; z: number };
  velocity: { x: number; y: number; z: number };
  isWarping: boolean;
  currentParity: 1 | -1;
  color: string;
  lastUpdate: number;
}

// =============================================================================
// HOOK
// =============================================================================

export function useMultiplayer() {
  const {
    isMultiplayerEnabled,
    playerId,
    setConnected,
    setPlayerId,
    updateOtherPlayer,
    removeOtherPlayer,
    clearOtherPlayers,
    updateRate,
  } = useMultiplayerStore();

  const {
    isPlayerMode,
    playerName,
    activeVessel,
    position,
    rotation,
    velocity,
    isWarping,
    currentParity,
  } = usePlayerStore();

  const lastUpdateRef = useRef<number>(0);
  const playerColorRef = useRef<string>(generatePlayerColor());
  const unsubscribeRef = useRef<(() => void) | null>(null);

  // ==========================================================================
  // BROADCAST LOCAL PLAYER POSITION
  // ==========================================================================

  const broadcastPosition = useCallback(() => {
    if (!isMultiplayerEnabled || !playerId || !isPlayerMode) return;

    const db = getFirebaseDatabase();
    if (!db) return;

    const now = Date.now();
    const minInterval = 1000 / updateRate;

    // Throttle updates
    if (now - lastUpdateRef.current < minInterval) return;
    lastUpdateRef.current = now;

    const playerRef = ref(db, `players/${playerId}`);
    const playerData: PlayerData = {
      name: playerName,
      vessel: activeVessel,
      position: { x: position.x, y: position.y, z: position.z },
      rotation: { x: rotation.x, y: rotation.y, z: rotation.z },
      velocity: { x: velocity.x, y: velocity.y, z: velocity.z },
      isWarping,
      currentParity,
      color: playerColorRef.current,
      lastUpdate: now,
    };

    set(playerRef, playerData).catch(console.error);
  }, [
    isMultiplayerEnabled,
    playerId,
    isPlayerMode,
    playerName,
    activeVessel,
    position,
    rotation,
    velocity,
    isWarping,
    currentParity,
    updateRate,
  ]);

  // ==========================================================================
  // CONNECT TO MULTIPLAYER
  // ==========================================================================

  const connect = useCallback(() => {
    const db = getFirebaseDatabase();
    if (!db) {
      console.warn('Firebase database not available');
      return;
    }

    // Generate player ID
    const newPlayerId = generatePlayerId();
    setPlayerId(newPlayerId);

    // Reference to this player's data
    const playerRef = ref(db, `players/${newPlayerId}`);

    // Set initial player data
    const initialData: PlayerData = {
      name: playerName,
      vessel: activeVessel,
      position: { x: position.x, y: position.y, z: position.z },
      rotation: { x: 0, y: 0, z: 0 },
      velocity: { x: 0, y: 0, z: 0 },
      isWarping: false,
      currentParity: 1,
      color: playerColorRef.current,
      lastUpdate: Date.now(),
    };

    set(playerRef, initialData)
      .then(() => {
        setConnected(true);
        console.log('Connected to multiplayer as', newPlayerId);
      })
      .catch((error) => {
        console.error('Failed to connect:', error);
        setConnected(false);
      });

    // Set up onDisconnect to clean up when player leaves
    onDisconnect(playerRef).remove();

    // Subscribe to all players
    const playersRef = ref(db, 'players');
    const handlePlayersUpdate = (snapshot: DataSnapshot) => {
      const players = snapshot.val();
      if (!players) {
        clearOtherPlayers();
        return;
      }

      // Get current player IDs from Firebase
      const currentPlayerIds = new Set(Object.keys(players));

      // Update or add players
      Object.entries(players).forEach(([id, data]) => {
        // Skip self
        if (id === newPlayerId) return;

        const playerData = data as PlayerData;
        const otherPlayer: OtherPlayer = {
          id,
          name: playerData.name || 'Unknown',
          vessel: playerData.vessel || 'ufo',
          position: playerData.position || { x: 0, y: 0, z: 0 },
          rotation: playerData.rotation || { x: 0, y: 0, z: 0 },
          velocity: playerData.velocity || { x: 0, y: 0, z: 0 },
          isWarping: playerData.isWarping || false,
          currentParity: playerData.currentParity || 1,
          lastUpdate: playerData.lastUpdate || Date.now(),
          color: playerData.color || '#ffffff',
        };

        updateOtherPlayer(otherPlayer);
      });

      // Remove players that are no longer in Firebase
      const { otherPlayers } = useMultiplayerStore.getState();
      otherPlayers.forEach((_, id) => {
        if (!currentPlayerIds.has(id)) {
          removeOtherPlayer(id);
        }
      });
    };

    onValue(playersRef, handlePlayersUpdate);

    // Store unsubscribe function
    unsubscribeRef.current = () => {
      off(playersRef);
      remove(playerRef);
    };
  }, [
    playerName,
    activeVessel,
    position,
    setPlayerId,
    setConnected,
    updateOtherPlayer,
    removeOtherPlayer,
    clearOtherPlayers,
  ]);

  // ==========================================================================
  // DISCONNECT FROM MULTIPLAYER
  // ==========================================================================

  const disconnect = useCallback(() => {
    const db = getFirebaseDatabase();

    if (unsubscribeRef.current) {
      unsubscribeRef.current();
      unsubscribeRef.current = null;
    }

    if (db && playerId) {
      const playerRef = ref(db, `players/${playerId}`);
      remove(playerRef).catch(console.error);
    }

    setPlayerId(null);
    setConnected(false);
    clearOtherPlayers();
    console.log('Disconnected from multiplayer');
  }, [playerId, setPlayerId, setConnected, clearOtherPlayers]);

  // ==========================================================================
  // AUTO-CONNECT/DISCONNECT BASED ON STATE
  // ==========================================================================

  useEffect(() => {
    if (isMultiplayerEnabled && isPlayerMode && !playerId) {
      connect();
    } else if (!isMultiplayerEnabled && playerId) {
      disconnect();
    }
  }, [isMultiplayerEnabled, isPlayerMode, playerId, connect, disconnect]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (playerId) {
        disconnect();
      }
    };
  }, []);

  // ==========================================================================
  // RETURN INTERFACE
  // ==========================================================================

  return {
    connect,
    disconnect,
    broadcastPosition,
  };
}

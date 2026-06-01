/**
 * ================================================================================
 * TimeManager.ts - UNIFIED SIMULATION CLOCK
 * ================================================================================
 *
 * Synchronizes all time-dependent phenomena in the Digital Twin:
 * - Gravitational wave events
 * - GRB transient flashes
 * - Orbital dynamics (planets, galaxies, binaries)
 * - CMB fluctuation animations
 * - kSZ void outflows
 *
 * Supports multiple time scales:
 * - Real-time (1:1 with wall clock)
 * - Orbital time (years compressed to seconds)
 * - Cosmological time (billions of years compressed)
 *
 * Z² Framework v11.1.0
 * Author: Carl Zimmerman + Claude
 * Date: May 2026
 * ================================================================================
 */

import { useCallback, useEffect, useRef, useState } from 'react';

// =============================================================================
// TIME SCALE DEFINITIONS
// =============================================================================

export type TimeScale =
  | 'REALTIME'        // 1:1 with wall clock
  | 'ORBITAL'         // 1 second = 1 Earth year
  | 'GALACTIC'        // 1 second = 1 million years
  | 'COSMOLOGICAL';   // 1 second = 1 billion years

export interface TimeScaleConfig {
  name: TimeScale;
  label: string;
  secondsPerUnit: number;  // Real seconds per simulation unit
  unitName: string;        // "seconds" | "years" | "Myr" | "Gyr"
}

export const TIME_SCALES: Record<TimeScale, TimeScaleConfig> = {
  REALTIME: {
    name: 'REALTIME',
    label: 'Real Time',
    secondsPerUnit: 1,
    unitName: 'seconds',
  },
  ORBITAL: {
    name: 'ORBITAL',
    label: 'Orbital (1s = 1yr)',
    secondsPerUnit: 1 / 31557600,  // 1 second = 1 year (in seconds)
    unitName: 'years',
  },
  GALACTIC: {
    name: 'GALACTIC',
    label: 'Galactic (1s = 1Myr)',
    secondsPerUnit: 1 / 3.1557e13,  // 1 second = 1 million years
    unitName: 'Myr',
  },
  COSMOLOGICAL: {
    name: 'COSMOLOGICAL',
    label: 'Cosmic (1s = 1Gyr)',
    secondsPerUnit: 1 / 3.1557e16,  // 1 second = 1 billion years
    unitName: 'Gyr',
  },
};

// =============================================================================
// TRANSIENT EVENT TYPES
// =============================================================================

export interface TransientEvent {
  id: string;
  type: 'GW' | 'GRB' | 'SN' | 'FLARE' | 'QUASAR_VARIABILITY';
  position: { x: number; y: number; z: number };  // Scene coordinates
  startTime: number;     // Simulation time when event starts
  duration: number;      // Duration in simulation time
  peakTime: number;      // Time of peak intensity
  intensity: number;     // 0-1 normalized intensity
  metadata?: {
    name?: string;
    strain?: number;     // For GW events
    energy?: number;     // ergs for GRB/SN
    redshift?: number;
  };
}

// =============================================================================
// TIME MANAGER STATE
// =============================================================================

export interface TimeState {
  // Current simulation time (in the current scale's units)
  simulationTime: number;

  // Wall clock elapsed time (seconds)
  elapsedRealTime: number;

  // Current time scale
  timeScale: TimeScale;

  // Playback state
  isPlaying: boolean;
  playbackSpeed: number;  // Multiplier (0.1x, 1x, 2x, 10x, etc.)

  // Active transient events
  activeEvents: TransientEvent[];

  // Epoch reference (simulation time at start)
  epochOffset: number;
}

// =============================================================================
// TIME MANAGER HOOK
// =============================================================================

export interface UseTimeManagerOptions {
  initialScale?: TimeScale;
  initialSpeed?: number;
  autoStart?: boolean;
  onEventStart?: (event: TransientEvent) => void;
  onEventEnd?: (event: TransientEvent) => void;
}

export interface TimeManagerActions {
  play: () => void;
  pause: () => void;
  togglePlayback: () => void;
  setSpeed: (speed: number) => void;
  setTimeScale: (scale: TimeScale) => void;
  seekTo: (time: number) => void;
  reset: () => void;
  addEvent: (event: Omit<TransientEvent, 'id'>) => string;
  removeEvent: (id: string) => void;
  clearEvents: () => void;
  getTimeInScale: (targetScale: TimeScale) => number;
}

export function useTimeManager(
  options: UseTimeManagerOptions = {}
): [TimeState, TimeManagerActions] {
  const {
    initialScale = 'ORBITAL',
    initialSpeed = 1,
    autoStart = false,
    onEventStart,
    onEventEnd,
  } = options;

  // State
  const [state, setState] = useState<TimeState>({
    simulationTime: 0,
    elapsedRealTime: 0,
    timeScale: initialScale,
    isPlaying: autoStart,
    playbackSpeed: initialSpeed,
    activeEvents: [],
    epochOffset: 0,
  });

  // Refs for animation loop
  const frameRef = useRef<number | null>(null);
  const lastTimeRef = useRef<number | null>(null);
  const eventsRef = useRef<TransientEvent[]>([]);

  // Event ID counter
  const eventIdRef = useRef(0);

  // Animation loop
  useEffect(() => {
    if (!state.isPlaying) {
      if (frameRef.current) {
        cancelAnimationFrame(frameRef.current);
        frameRef.current = null;
      }
      lastTimeRef.current = null;
      return;
    }

    const animate = (currentTime: number) => {
      if (lastTimeRef.current === null) {
        lastTimeRef.current = currentTime;
      }

      const deltaMs = currentTime - lastTimeRef.current;
      const deltaSec = deltaMs / 1000;
      lastTimeRef.current = currentTime;

      // Update times
      const scaleConfig = TIME_SCALES[state.timeScale];
      const simDelta = deltaSec * state.playbackSpeed / scaleConfig.secondsPerUnit;

      setState(prev => {
        const newSimTime = prev.simulationTime + simDelta;
        const newRealTime = prev.elapsedRealTime + deltaSec;

        // Check for event state changes
        const activeEvents = eventsRef.current.filter(evt => {
          const elapsed = newSimTime - evt.startTime;
          return elapsed >= 0 && elapsed <= evt.duration;
        });

        // Trigger callbacks for newly started events
        if (onEventStart) {
          for (const evt of activeEvents) {
            const wasActive = prev.activeEvents.some(e => e.id === evt.id);
            if (!wasActive) {
              onEventStart(evt);
            }
          }
        }

        // Trigger callbacks for ended events
        if (onEventEnd) {
          for (const evt of prev.activeEvents) {
            const stillActive = activeEvents.some(e => e.id === evt.id);
            if (!stillActive) {
              onEventEnd(evt);
            }
          }
        }

        return {
          ...prev,
          simulationTime: newSimTime,
          elapsedRealTime: newRealTime,
          activeEvents,
        };
      });

      frameRef.current = requestAnimationFrame(animate);
    };

    frameRef.current = requestAnimationFrame(animate);

    return () => {
      if (frameRef.current) {
        cancelAnimationFrame(frameRef.current);
      }
    };
  }, [state.isPlaying, state.timeScale, state.playbackSpeed, onEventStart, onEventEnd]);

  // Actions
  const play = useCallback(() => {
    setState(prev => ({ ...prev, isPlaying: true }));
  }, []);

  const pause = useCallback(() => {
    setState(prev => ({ ...prev, isPlaying: false }));
  }, []);

  const togglePlayback = useCallback(() => {
    setState(prev => ({ ...prev, isPlaying: !prev.isPlaying }));
  }, []);

  const setSpeed = useCallback((speed: number) => {
    setState(prev => ({ ...prev, playbackSpeed: Math.max(0.01, speed) }));
  }, []);

  const setTimeScale = useCallback((scale: TimeScale) => {
    setState(prev => {
      // Convert current time to new scale
      const oldConfig = TIME_SCALES[prev.timeScale];
      const newConfig = TIME_SCALES[scale];

      // Convert simulation time: first to real seconds, then to new scale
      const realSeconds = prev.simulationTime * oldConfig.secondsPerUnit;
      const newSimTime = realSeconds / newConfig.secondsPerUnit;

      return {
        ...prev,
        timeScale: scale,
        simulationTime: newSimTime,
      };
    });
  }, []);

  const seekTo = useCallback((time: number) => {
    setState(prev => ({ ...prev, simulationTime: time }));
  }, []);

  const reset = useCallback(() => {
    setState(prev => ({
      ...prev,
      simulationTime: 0,
      elapsedRealTime: 0,
      isPlaying: false,
      activeEvents: [],
    }));
  }, []);

  const addEvent = useCallback((event: Omit<TransientEvent, 'id'>): string => {
    const id = `evt_${eventIdRef.current++}`;
    const fullEvent: TransientEvent = { ...event, id };
    eventsRef.current.push(fullEvent);
    return id;
  }, []);

  const removeEvent = useCallback((id: string) => {
    eventsRef.current = eventsRef.current.filter(e => e.id !== id);
    setState(prev => ({
      ...prev,
      activeEvents: prev.activeEvents.filter(e => e.id !== id),
    }));
  }, []);

  const clearEvents = useCallback(() => {
    eventsRef.current = [];
    setState(prev => ({ ...prev, activeEvents: [] }));
  }, []);

  const getTimeInScale = useCallback((targetScale: TimeScale): number => {
    const currentConfig = TIME_SCALES[state.timeScale];
    const targetConfig = TIME_SCALES[targetScale];

    const realSeconds = state.simulationTime * currentConfig.secondsPerUnit;
    return realSeconds / targetConfig.secondsPerUnit;
  }, [state.simulationTime, state.timeScale]);

  const actions: TimeManagerActions = {
    play,
    pause,
    togglePlayback,
    setSpeed,
    setTimeScale,
    seekTo,
    reset,
    addEvent,
    removeEvent,
    clearEvents,
    getTimeInScale,
  };

  return [state, actions];
}

// =============================================================================
// UTILITY FUNCTIONS
// =============================================================================

/**
 * Calculate event intensity at current time (for rendering)
 */
export function getEventIntensity(event: TransientEvent, currentTime: number): number {
  const elapsed = currentTime - event.startTime;

  if (elapsed < 0 || elapsed > event.duration) {
    return 0;
  }

  // Light curve model: fast rise, exponential decay
  const timeToPeak = event.peakTime - event.startTime;
  const decayTime = event.duration - timeToPeak;

  if (elapsed <= timeToPeak) {
    // Rising phase (quadratic)
    const progress = elapsed / timeToPeak;
    return event.intensity * progress * progress;
  } else {
    // Decay phase (exponential)
    const decayProgress = (elapsed - timeToPeak) / decayTime;
    return event.intensity * Math.exp(-3 * decayProgress);
  }
}

/**
 * Format simulation time for display
 */
export function formatSimulationTime(time: number, scale: TimeScale): string {
  const config = TIME_SCALES[scale];

  switch (scale) {
    case 'REALTIME':
      const hours = Math.floor(time / 3600);
      const minutes = Math.floor((time % 3600) / 60);
      const seconds = Math.floor(time % 60);
      return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

    case 'ORBITAL':
      if (Math.abs(time) < 1) {
        return `${(time * 365.25).toFixed(1)} days`;
      }
      return `${time.toFixed(2)} years`;

    case 'GALACTIC':
      if (Math.abs(time) < 1000) {
        return `${time.toFixed(1)} Myr`;
      }
      return `${(time / 1000).toFixed(2)} Gyr`;

    case 'COSMOLOGICAL':
      return `${time.toFixed(3)} Gyr`;

    default:
      return `${time.toFixed(2)} ${config.unitName}`;
  }
}

/**
 * Calculate orbital phase for a body
 */
export function getOrbitalPhase(
  orbitalPeriod: number,  // In current time scale units
  simulationTime: number,
  initialPhase: number = 0
): number {
  return (initialPhase + (2 * Math.PI * simulationTime) / orbitalPeriod) % (2 * Math.PI);
}

/**
 * Synchronize multiple orbital bodies to the same time
 */
export interface OrbitalBody {
  id: string;
  orbitalPeriod: number;
  orbitalRadius: number;
  initialPhase: number;
  inclination?: number;
}

export function getOrbitalPositions(
  bodies: OrbitalBody[],
  simulationTime: number
): Map<string, { x: number; y: number; z: number; phase: number }> {
  const positions = new Map();

  for (const body of bodies) {
    const phase = getOrbitalPhase(body.orbitalPeriod, simulationTime, body.initialPhase);
    const incl = body.inclination ?? 0;

    positions.set(body.id, {
      x: body.orbitalRadius * Math.cos(phase),
      y: body.orbitalRadius * Math.sin(phase) * Math.cos(incl),
      z: body.orbitalRadius * Math.sin(phase) * Math.sin(incl),
      phase,
    });
  }

  return positions;
}

// =============================================================================
// GRAVITATIONAL WAVE HELPER
// =============================================================================

/**
 * Generate GW event with proper ringdown
 */
export function createGWEvent(
  position: { x: number; y: number; z: number },
  strain: number,  // Peak strain (dimensionless)
  startTime: number,
  name?: string
): Omit<TransientEvent, 'id'> {
  // GW events have ~100ms merger, ~1s ringdown
  const duration = 2.0;  // seconds in REALTIME
  const peakTime = startTime + 0.5;  // Peak at merger

  return {
    type: 'GW',
    position,
    startTime,
    duration,
    peakTime,
    intensity: Math.min(strain * 1e21, 1),  // Normalize strain to 0-1
    metadata: { name, strain },
  };
}

/**
 * Generate GRB event
 */
export function createGRBEvent(
  position: { x: number; y: number; z: number },
  energy_ergs: number,
  startTime: number,
  name?: string
): Omit<TransientEvent, 'id'> {
  // Long GRBs: 2-100 seconds
  // Short GRBs: 0.1-2 seconds
  const isShort = energy_ergs < 1e50;
  const duration = isShort ? 0.5 : 30;
  const peakTime = startTime + duration * 0.1;

  return {
    type: 'GRB',
    position,
    startTime,
    duration,
    peakTime,
    intensity: Math.min(Math.log10(energy_ergs) / 54, 1),  // Log scale to 0-1
    metadata: { name, energy: energy_ergs },
  };
}

// =============================================================================
// EXPORT
// =============================================================================

export default useTimeManager;

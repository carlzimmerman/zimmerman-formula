// =============================================================================
// VESSEL SELECTOR UI (Directive WWW)
// =============================================================================
// Modal for selecting which vessel to fly in the Z² universe
// Now with multiplayer mode selection and username input
// =============================================================================

'use client';

import React, { useState, useCallback } from 'react';
import { VesselType, VESSEL_CONFIGS, usePlayerStore } from '../../store/playerStore';
import { useMultiplayerStore } from '../../store/multiplayerStore';

// =============================================================================
// USERNAME VALIDATION
// =============================================================================

// Basic inappropriate word list (keep it family-friendly)
const BLOCKED_WORDS = [
  'fuck', 'shit', 'ass', 'bitch', 'dick', 'cock', 'pussy', 'cunt',
  'nigger', 'nigga', 'faggot', 'retard', 'slut', 'whore',
  'nazi', 'hitler', 'kill', 'rape', 'porn', 'sex',
];

// Check if username contains inappropriate content
function isUsernameAppropriate(name: string): { valid: boolean; reason?: string } {
  const trimmed = name.trim();

  // Length checks
  if (trimmed.length < 2) {
    return { valid: false, reason: 'Name must be at least 2 characters' };
  }
  if (trimmed.length > 16) {
    return { valid: false, reason: 'Name must be 16 characters or less' };
  }

  // Character validation (alphanumeric, spaces, underscores, hyphens)
  if (!/^[a-zA-Z0-9_\- ]+$/.test(trimmed)) {
    return { valid: false, reason: 'Only letters, numbers, spaces, _ and - allowed' };
  }

  // Check for blocked words (case-insensitive)
  const lowerName = trimmed.toLowerCase().replace(/[\s_\-]/g, '');
  for (const word of BLOCKED_WORDS) {
    if (lowerName.includes(word)) {
      return { valid: false, reason: 'Please choose an appropriate name' };
    }
  }

  // Check for excessive repetition (e.g., "aaaaaaa")
  if (/(.)\1{4,}/.test(trimmed)) {
    return { valid: false, reason: 'Too many repeated characters' };
  }

  return { valid: true };
}

// =============================================================================
// COMPONENT
// =============================================================================

const VesselSelector: React.FC = () => {
  const {
    isSelectingVessel,
    activeVessel,
    playerName,
    setVessel,
    setPlayerName,
    closeVesselSelector,
    startPlayerMode,
  } = usePlayerStore();

  const {
    isMultiplayerEnabled,
    setMultiplayerEnabled,
  } = useMultiplayerStore();

  const [nameInput, setNameInput] = useState(playerName);
  const [nameError, setNameError] = useState<string | null>(null);
  const [fullscreenOnLaunch, setFullscreenOnLaunch] = useState(false);

  if (!isSelectingVessel) return null;

  const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setNameInput(value);

    if (value.trim().length === 0) {
      setNameError(null);
      return;
    }

    const validation = isUsernameAppropriate(value);
    setNameError(validation.valid ? null : validation.reason || 'Invalid name');
  };

  const handleSelect = (vessel: VesselType) => {
    setVessel(vessel);
  };

  const handleLaunch = async () => {
    // Validate name before launch
    const trimmedName = nameInput.trim();
    if (trimmedName.length === 0) {
      setNameError('Please enter a pilot name');
      return;
    }

    const validation = isUsernameAppropriate(trimmedName);
    if (!validation.valid) {
      setNameError(validation.reason || 'Invalid name');
      return;
    }

    // Save the name
    setPlayerName(trimmedName);

    // Request fullscreen if enabled
    if (fullscreenOnLaunch && document.documentElement.requestFullscreen) {
      try {
        await document.documentElement.requestFullscreen();
      } catch (err) {
        console.warn('Could not enter fullscreen:', err);
      }
    }

    // Launch
    closeVesselSelector();
    startPlayerMode();
  };

  const vessels = Object.values(VESSEL_CONFIGS);
  const isLaunchDisabled = nameError !== null || nameInput.trim().length === 0;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/95 backdrop-blur-md">
      <div className="bg-slate-900/98 border border-cyan-500/50 rounded-xl p-6 max-w-2xl w-full mx-4 shadow-[0_0_50px_rgba(6,182,212,0.3)]">
        {/* Header */}
        <div className="text-center mb-4">
          <h2 className="text-3xl font-bold text-cyan-400 mb-2">
            SELECT YOUR VESSEL
          </h2>
          <p className="text-slate-400 text-sm">
            Choose your craft for exploring the T³/Z₂ universe
          </p>
        </div>

        {/* Pilot Name Input */}
        <div className="mb-4">
          <label className="text-slate-400 text-xs font-bold block mb-2">PILOT NAME</label>
          <div className="relative">
            <input
              type="text"
              value={nameInput}
              onChange={handleNameChange}
              placeholder="Enter your pilot name..."
              maxLength={16}
              className={`w-full bg-slate-800 text-white px-4 py-3 rounded-lg border-2 transition-all focus:outline-none ${
                nameError
                  ? 'border-red-500 focus:border-red-400'
                  : 'border-slate-600 focus:border-cyan-400'
              }`}
            />
            <span className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 text-xs">
              {nameInput.length}/16
            </span>
          </div>
          {nameError && (
            <p className="text-red-400 text-xs mt-1">{nameError}</p>
          )}
        </div>

        {/* Vessel Grid */}
        <div className="grid grid-cols-5 gap-3 mb-6">
          {vessels.map((vessel) => (
            <button
              key={vessel.id}
              onClick={() => handleSelect(vessel.id)}
              className={`
                relative p-4 rounded-lg border-2 transition-all
                ${activeVessel === vessel.id
                  ? 'border-cyan-400 bg-cyan-900/30 shadow-[0_0_20px_rgba(6,182,212,0.4)]'
                  : 'border-slate-600 bg-slate-800/50 hover:border-slate-500 hover:bg-slate-800'
                }
              `}
            >
              {/* Vessel Icon */}
              <div
                className="w-12 h-12 mx-auto mb-2 rounded-full flex items-center justify-center text-2xl"
                style={{ backgroundColor: vessel.color + '33' }}
              >
                {vessel.id === 'ufo' && '🛸'}
                {vessel.id === 'truck' && '🚛'}
                {vessel.id === 'sedan' && '🚗'}
                {vessel.id === 'plane' && '✈️'}
                {vessel.id === 'donut' && '🍩'}
              </div>

              {/* Name */}
              <div className="text-white text-sm font-bold text-center">
                {vessel.name}
              </div>

              {/* Selected indicator */}
              {activeVessel === vessel.id && (
                <div className="absolute -top-1 -right-1 w-4 h-4 bg-cyan-400 rounded-full flex items-center justify-center">
                  <span className="text-black text-xs">✓</span>
                </div>
              )}
            </button>
          ))}
        </div>

        {/* Selected Vessel Details */}
        <div className="bg-slate-800/50 rounded-lg p-4 mb-6 border border-slate-700">
          <div className="flex items-center gap-4">
            <div
              className="w-16 h-16 rounded-full flex items-center justify-center text-4xl"
              style={{ backgroundColor: VESSEL_CONFIGS[activeVessel].color + '33' }}
            >
              {activeVessel === 'ufo' && '🛸'}
              {activeVessel === 'truck' && '🚛'}
              {activeVessel === 'sedan' && '🚗'}
              {activeVessel === 'plane' && '✈️'}
              {activeVessel === 'donut' && '🍩'}
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-bold text-white">
                {VESSEL_CONFIGS[activeVessel].name}
              </h3>
              <p className="text-slate-400 text-sm mb-2">
                {VESSEL_CONFIGS[activeVessel].description}
              </p>
              <div className="flex gap-4 text-xs">
                <div>
                  <span className="text-slate-500">Max Warp:</span>
                  <span className="text-cyan-400 ml-1">
                    {VESSEL_CONFIGS[activeVessel].maxSpeed} Gpc/s
                  </span>
                </div>
                <div>
                  <span className="text-slate-500">Accel:</span>
                  <span className="text-green-400 ml-1">
                    {VESSEL_CONFIGS[activeVessel].acceleration}x
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Mode Selection */}
        <div className="mb-6">
          <label className="text-slate-400 text-xs font-bold block mb-2">FLIGHT MODE</label>
          <div className="grid grid-cols-2 gap-3">
            <button
              onClick={() => setMultiplayerEnabled(false)}
              className={`p-3 rounded-lg border-2 transition-all ${
                !isMultiplayerEnabled
                  ? 'border-cyan-400 bg-cyan-900/30 shadow-[0_0_15px_rgba(6,182,212,0.3)]'
                  : 'border-slate-600 bg-slate-800/50 hover:border-slate-500'
              }`}
            >
              <div className="text-2xl mb-1">🚀</div>
              <div className="text-white font-bold text-sm">SOLO</div>
              <div className="text-slate-400 text-[10px]">Explore alone</div>
            </button>
            <button
              onClick={() => setMultiplayerEnabled(true)}
              className={`p-3 rounded-lg border-2 transition-all ${
                isMultiplayerEnabled
                  ? 'border-green-400 bg-green-900/30 shadow-[0_0_15px_rgba(34,197,94,0.3)]'
                  : 'border-slate-600 bg-slate-800/50 hover:border-slate-500'
              }`}
            >
              <div className="text-2xl mb-1">👥</div>
              <div className="text-white font-bold text-sm">MULTIPLAYER</div>
              <div className="text-slate-400 text-[10px]">See other pilots</div>
            </button>
          </div>
          {isMultiplayerEnabled && (
            <div className="mt-2 p-2 bg-green-900/20 border border-green-500/30 rounded text-xs text-green-300">
              <span className="font-bold">MULTIPLAYER ENABLED:</span> Your position will be shared with other pilots in real-time via Firebase.
            </div>
          )}
        </div>

        {/* Controls Info */}
        <div className="bg-slate-800/30 rounded-lg p-3 mb-4 text-xs text-slate-400">
          <div className="grid grid-cols-2 gap-2">
            <div><span className="text-cyan-400">WASD</span> - Move</div>
            <div><span className="text-cyan-400">Mouse</span> - Look</div>
            <div><span className="text-cyan-400">SHIFT</span> - Warp Drive</div>
            <div><span className="text-cyan-400">ESC</span> - Exit</div>
          </div>
        </div>

        {/* Fullscreen Toggle */}
        <div className="mb-6">
          <label className="flex items-center gap-3 cursor-pointer p-3 bg-slate-800/30 rounded-lg border border-slate-700 hover:border-slate-600 transition-colors">
            <input
              type="checkbox"
              checked={fullscreenOnLaunch}
              onChange={(e) => setFullscreenOnLaunch(e.target.checked)}
              className="w-5 h-5 accent-cyan-500 rounded"
            />
            <div className="flex-1">
              <div className="text-white font-bold text-sm flex items-center gap-2">
                <span>🖥️</span> Launch in Fullscreen
              </div>
              <div className="text-slate-400 text-[10px]">
                Immersive experience - press ESC to exit fullscreen
              </div>
            </div>
          </label>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-3">
          <button
            onClick={closeVesselSelector}
            className="flex-1 px-6 py-3 bg-slate-700 hover:bg-slate-600 text-white font-bold rounded-lg transition-colors"
          >
            CANCEL
          </button>
          <button
            onClick={handleLaunch}
            disabled={isLaunchDisabled}
            className={`flex-1 px-6 py-3 text-white font-bold rounded-lg transition-all ${
              isLaunchDisabled
                ? 'bg-slate-700 text-slate-400 cursor-not-allowed'
                : isMultiplayerEnabled
                ? 'bg-gradient-to-r from-green-600 to-cyan-600 hover:from-green-500 hover:to-cyan-500 shadow-[0_0_20px_rgba(34,197,94,0.4)]'
                : 'bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 shadow-[0_0_20px_rgba(6,182,212,0.4)]'
            }`}
          >
            {isMultiplayerEnabled ? '👥 LAUNCH MULTIPLAYER' : '🚀 LAUNCH SOLO'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default VesselSelector;

#!/usr/bin/env python3
"""
OLYMPUSFLOW - Event System
==========================

Publish/subscribe event system for pipeline hooks and monitoring.

Features:
- Event bus for decoupled communication
- Sync and async event handlers
- Event logging for audit trail
- Built-in event types for common pipeline events

Usage:
    bus = EventBus()

    @bus.on("discovery.complete")
    def handle_discovery(event: Event):
        print(f"Found data: {event.payload['url']}")

    bus.emit("discovery.complete", payload={"url": "..."})

Author: Carl Zimmerman
Date: May 4, 2026
"""

import json
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Callable, Optional, Any
from dataclasses import dataclass, field
from functools import wraps
from collections import defaultdict

from .contracts import Event


# =============================================================================
# EVENT TYPES
# =============================================================================

class EventType:
    """Standard event types emitted by the pipeline."""

    # Pipeline lifecycle
    PIPELINE_STARTED = "pipeline.started"
    PIPELINE_COMPLETED = "pipeline.completed"
    PIPELINE_FAILED = "pipeline.failed"
    PIPELINE_PAUSED = "pipeline.paused"
    PIPELINE_RESUMED = "pipeline.resumed"

    # Stage lifecycle
    STAGE_STARTED = "stage.started"
    STAGE_COMPLETED = "stage.completed"
    STAGE_FAILED = "stage.failed"
    STAGE_SKIPPED = "stage.skipped"

    # Discovery events
    DISCOVERY_STARTED = "discovery.started"
    DISCOVERY_FOUND = "discovery.found"
    DISCOVERY_FAILED = "discovery.failed"

    # Verification events
    VERIFICATION_STARTED = "verification.started"
    VERIFICATION_PASSED = "verification.passed"
    VERIFICATION_FAILED = "verification.failed"

    # Truth events
    TRUTH_CREATED = "truth.created"
    TRUTH_VALIDATED = "truth.validated"
    TRUTH_REJECTED = "truth.rejected"
    TRUTH_STORED = "truth.stored"

    # Training events
    TRAINING_STARTED = "training.started"
    TRAINING_COMPLETED = "training.completed"
    TRAINING_FAILED = "training.failed"

    # Iteration events
    ITERATION_STARTED = "iteration.started"
    ITERATION_COMPLETED = "iteration.completed"
    DIMINISHING_RETURNS = "iteration.diminishing_returns"

    # Recursive deepening events (v1.4.0)
    DEEPENING_TRIGGERED = "deepening.triggered"
    DEEPENING_STARTED = "deepening.started"
    DEEPENING_COMPLETED = "deepening.completed"
    DEEPENING_QUESTION = "deepening.question"
    DEEPENING_FINDING = "deepening.finding"


# =============================================================================
# EVENT BUS
# =============================================================================

class EventBus:
    """
    Central event bus for pipeline communication.

    Supports:
    - Multiple handlers per event type
    - Wildcard subscriptions (e.g., "discovery.*")
    - Event logging
    - Handler priorities
    """

    def __init__(self, log_path: Optional[Path] = None):
        self._handlers: Dict[str, List[tuple]] = defaultdict(list)
        self._wildcard_handlers: Dict[str, List[tuple]] = defaultdict(list)
        self._log_path = log_path
        self._lock = threading.Lock()
        self._event_history: List[Event] = []
        self._max_history = 1000

    def on(self, event_type: str, priority: int = 0):
        """
        Decorator to register an event handler.

        Args:
            event_type: Event type to handle (supports wildcards like "discovery.*")
            priority: Handler priority (higher = runs first)

        Usage:
            @bus.on("discovery.complete")
            def handle(event):
                print(event.payload)
        """
        def decorator(func: Callable):
            self.subscribe(event_type, func, priority)
            return func
        return decorator

    def subscribe(self, event_type: str, handler: Callable, priority: int = 0):
        """Subscribe a handler to an event type."""
        with self._lock:
            if '*' in event_type:
                # Wildcard subscription
                prefix = event_type.replace('*', '')
                self._wildcard_handlers[prefix].append((priority, handler))
                self._wildcard_handlers[prefix].sort(key=lambda x: -x[0])
            else:
                self._handlers[event_type].append((priority, handler))
                self._handlers[event_type].sort(key=lambda x: -x[0])

    def unsubscribe(self, event_type: str, handler: Callable):
        """Unsubscribe a handler from an event type."""
        with self._lock:
            if '*' in event_type:
                prefix = event_type.replace('*', '')
                self._wildcard_handlers[prefix] = [
                    (p, h) for p, h in self._wildcard_handlers[prefix] if h != handler
                ]
            else:
                self._handlers[event_type] = [
                    (p, h) for p, h in self._handlers[event_type] if h != handler
                ]

    def emit(self, event_type: str, source_stage: str = "unknown",
             payload: Dict = None) -> Event:
        """
        Emit an event to all subscribed handlers.

        Args:
            event_type: Type of event
            source_stage: Stage that emitted the event
            payload: Event data

        Returns:
            The emitted Event object
        """
        event = Event(
            event_type=event_type,
            source_stage=source_stage,
            payload=payload or {},
            timestamp=datetime.now().isoformat()
        )

        # Add to history
        self._add_to_history(event)

        # Log if configured
        if self._log_path:
            self._log_event(event)

        # Call handlers
        handlers_to_call = []

        # Exact match handlers
        with self._lock:
            handlers_to_call.extend(self._handlers.get(event_type, []))

            # Wildcard match handlers
            for prefix, handlers in self._wildcard_handlers.items():
                if event_type.startswith(prefix):
                    handlers_to_call.extend(handlers)

        # Sort by priority and call
        handlers_to_call.sort(key=lambda x: -x[0])
        for _, handler in handlers_to_call:
            try:
                handler(event)
            except Exception as e:
                # Don't let handler errors break the pipeline
                print(f"[EventBus] Handler error: {e}")

        return event

    def _add_to_history(self, event: Event):
        """Add event to history, maintaining max size."""
        self._event_history.append(event)
        if len(self._event_history) > self._max_history:
            self._event_history = self._event_history[-self._max_history:]

    def _log_event(self, event: Event):
        """Log event to file."""
        if self._log_path:
            with open(self._log_path, 'a') as f:
                f.write(event.to_json() + '\n')

    def get_history(self, event_type: Optional[str] = None,
                    limit: int = 100) -> List[Event]:
        """Get recent event history."""
        events = self._event_history
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        return events[-limit:]

    def clear_history(self):
        """Clear event history."""
        self._event_history = []


# =============================================================================
# GLOBAL EVENT BUS
# =============================================================================

_global_bus: Optional[EventBus] = None


def get_event_bus() -> EventBus:
    """Get the global event bus instance."""
    global _global_bus
    if _global_bus is None:
        _global_bus = EventBus()
    return _global_bus


def set_event_bus(bus: EventBus):
    """Set the global event bus instance."""
    global _global_bus
    _global_bus = bus


def on(event_type: str, priority: int = 0):
    """Decorator to register handler on global bus."""
    return get_event_bus().on(event_type, priority)


def emit(event_type: str, source_stage: str = "unknown",
         payload: Dict = None) -> Event:
    """Emit event on global bus."""
    return get_event_bus().emit(event_type, source_stage, payload)


# =============================================================================
# EVENT HELPERS
# =============================================================================

class EventEmitter:
    """
    Mixin class for objects that emit events.

    Usage:
        class MyStage(EventEmitter):
            def run(self):
                self.emit("stage.started", {"name": "MyStage"})
                # do work
                self.emit("stage.completed", {"result": "success"})
    """

    def __init__(self, bus: Optional[EventBus] = None):
        self._event_bus = bus or get_event_bus()
        self._stage_name = self.__class__.__name__

    def emit(self, event_type: str, payload: Dict = None) -> Event:
        """Emit an event from this stage."""
        return self._event_bus.emit(event_type, self._stage_name, payload)

    def on(self, event_type: str, handler: Callable, priority: int = 0):
        """Subscribe to an event."""
        self._event_bus.subscribe(event_type, handler, priority)


# =============================================================================
# BUILT-IN HANDLERS
# =============================================================================

class ConsoleLogger:
    """Handler that logs events to console."""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose

    def __call__(self, event: Event):
        if self.verbose:
            ts = event.timestamp.split('T')[1][:8]
            print(f"[{ts}] {event.event_type}: {event.source_stage}")
            if event.payload and self.verbose:
                for k, v in list(event.payload.items())[:3]:
                    print(f"         {k}: {str(v)[:50]}")


class MetricsCollector:
    """Handler that collects pipeline metrics."""

    def __init__(self):
        self.metrics = {
            "events_total": 0,
            "events_by_type": defaultdict(int),
            "stages_completed": 0,
            "stages_failed": 0,
            "truths_created": 0,
            "discoveries_made": 0,
        }

    def __call__(self, event: Event):
        self.metrics["events_total"] += 1
        self.metrics["events_by_type"][event.event_type] += 1

        if event.event_type == EventType.STAGE_COMPLETED:
            self.metrics["stages_completed"] += 1
        elif event.event_type == EventType.STAGE_FAILED:
            self.metrics["stages_failed"] += 1
        elif event.event_type == EventType.TRUTH_CREATED:
            self.metrics["truths_created"] += 1
        elif event.event_type == EventType.DISCOVERY_FOUND:
            self.metrics["discoveries_made"] += 1

    def get_summary(self) -> Dict:
        """Get metrics summary."""
        return dict(self.metrics)


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    print("OlympusFlow Event System")
    print("=" * 40)

    # Create bus with console logging
    bus = EventBus()
    logger = ConsoleLogger(verbose=True)
    metrics = MetricsCollector()

    # Subscribe handlers
    bus.subscribe("*", logger)  # Log everything
    bus.subscribe("*", metrics)  # Collect metrics

    # Custom handler
    @bus.on(EventType.TRUTH_CREATED)
    def on_truth(event):
        print(f"  >>> New truth: {event.payload.get('claim', 'unknown')}")

    # Emit some events
    bus.emit(EventType.PIPELINE_STARTED, "OlympusFlow", {"name": "test_pipeline"})
    bus.emit(EventType.DISCOVERY_STARTED, "HermesFlow", {"topic": "earthquakes"})
    bus.emit(EventType.DISCOVERY_FOUND, "HermesFlow", {"url": "usgs.gov/data.csv"})
    bus.emit(EventType.TRUTH_CREATED, "TruthFlow", {"claim": "CV = Z²"})
    bus.emit(EventType.PIPELINE_COMPLETED, "OlympusFlow", {"iterations": 5})

    print("\nMetrics:")
    for k, v in metrics.get_summary().items():
        if isinstance(v, dict):
            print(f"  {k}:")
            for k2, v2 in v.items():
                print(f"    {k2}: {v2}")
        else:
            print(f"  {k}: {v}")

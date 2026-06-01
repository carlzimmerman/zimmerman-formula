#!/usr/bin/env python3
"""
ALPHEUSFLOW QUEUE - Research Task Queue Management
===================================================

Manages the queue of research tasks waiting to be processed.

Features:
- Priority-based ordering
- Task batching by category
- Persistence to disk
- Queue statistics

Author: Carl Zimmerman
Date: May 5, 2026
"""

import json
import uuid
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from collections import defaultdict


class TaskStatus(Enum):
    """Status of a research task."""
    PENDING = "pending"           # Waiting in queue
    RUNNING = "running"           # Currently being processed
    COMPLETED = "completed"       # Successfully finished
    FAILED = "failed"             # Failed with error
    PAUSED = "paused"             # Manually paused
    CANCELLED = "cancelled"       # Cancelled before completion


class TaskPriority(Enum):
    """Priority levels for queue ordering."""
    CRITICAL = 0    # Process immediately
    HIGH = 1        # Process soon
    NORMAL = 2      # Standard priority
    LOW = 3         # Process when nothing else
    BACKGROUND = 4  # Only when idle


@dataclass
class ResearchTask:
    """A single research task in the queue."""
    id: str
    name: str                         # Short name (e.g., "von_karman_constant")
    description: str                  # Full task description/prompt
    category: str = "general"         # Category for batching
    priority: TaskPriority = TaskPriority.NORMAL
    status: TaskStatus = TaskStatus.PENDING

    # Execution tracking
    created_at: str = ""
    started_at: str = ""
    completed_at: str = ""
    elapsed_seconds: float = 0

    # Results
    result: Dict = field(default_factory=dict)
    error: str = ""
    output_path: str = ""

    # Metadata
    target_constant: str = ""         # What constant to derive
    target_value: float = 0.0         # Expected value
    domain: str = ""                  # Scientific domain
    quantities: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())[:8]
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        d = asdict(self)
        d['priority'] = self.priority.value
        d['status'] = self.status.value
        # Sanitize result dict for JSON serialization
        d['result'] = self._sanitize_for_json(d.get('result', {}))
        return d

    @staticmethod
    def _sanitize_for_json(obj):
        """Recursively convert objects to JSON-serializable types."""
        if obj is None:
            return None
        if isinstance(obj, (str, int, float, bool)):
            return obj
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, dict):
            return {k: ResearchTask._sanitize_for_json(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [ResearchTask._sanitize_for_json(item) for item in obj]
        # Fallback: convert to string
        return str(obj)

    @classmethod
    def from_dict(cls, d: Dict) -> 'ResearchTask':
        """Create from dictionary."""
        d['priority'] = TaskPriority(d.get('priority', 2))
        d['status'] = TaskStatus(d.get('status', 'pending'))
        return cls(**d)


@dataclass
class BatchConfig:
    """Configuration for batch processing."""
    name: str
    category: str
    max_concurrent: int = 1           # Tasks to run in parallel (1 = sequential)
    timeout_per_task: int = 3600      # Max seconds per task
    stop_on_failure: bool = False     # Stop batch if a task fails
    output_dir: str = ""


class ResearchQueue:
    """
    Manages the queue of research tasks.

    The queue is a priority queue where tasks are processed in order of:
    1. Priority (CRITICAL first)
    2. Created time (older first)
    """

    def __init__(self, persistence_path: str = None):
        self.tasks: Dict[str, ResearchTask] = {}
        self.task_order: List[str] = []  # Order for processing

        # Persistence
        if persistence_path:
            self.persistence_path = Path(persistence_path)
        else:
            self.persistence_path = Path("AlpheusFlow/queue_state.json")
        self.persistence_path.parent.mkdir(parents=True, exist_ok=True)

        # Callbacks
        self.on_task_start: Optional[Callable] = None
        self.on_task_complete: Optional[Callable] = None
        self.on_task_fail: Optional[Callable] = None

        # Load persisted state
        self._load_state()

    def _load_state(self):
        """Load queue state from disk."""
        if self.persistence_path.exists():
            try:
                data = json.loads(self.persistence_path.read_text())
                for task_data in data.get('tasks', []):
                    task = ResearchTask.from_dict(task_data)
                    self.tasks[task.id] = task
                self.task_order = data.get('order', list(self.tasks.keys()))
                print(f"AlpheusFlow: Loaded {len(self.tasks)} tasks from queue")
            except Exception as e:
                print(f"AlpheusFlow: Could not load queue state: {e}")

    def _save_state(self):
        """Save queue state to disk."""
        try:
            data = {
                'tasks': [t.to_dict() for t in self.tasks.values()],
                'order': self.task_order,
                'saved_at': datetime.now().isoformat()
            }
            self.persistence_path.write_text(json.dumps(data, indent=2))
        except Exception as e:
            print(f"AlpheusFlow: Could not save queue state: {e}")

    def add(self, task: ResearchTask) -> str:
        """Add a task to the queue."""
        self.tasks[task.id] = task
        self._insert_by_priority(task.id)
        self._save_state()
        return task.id

    def _insert_by_priority(self, task_id: str):
        """Insert task in correct position based on priority."""
        task = self.tasks[task_id]
        insert_pos = len(self.task_order)

        for i, existing_id in enumerate(self.task_order):
            existing = self.tasks.get(existing_id)
            if existing and task.priority.value < existing.priority.value:
                insert_pos = i
                break

        if task_id in self.task_order:
            self.task_order.remove(task_id)
        self.task_order.insert(insert_pos, task_id)

    def add_batch(self, tasks: List[ResearchTask], category: str = None) -> List[str]:
        """Add multiple tasks at once."""
        ids = []
        for task in tasks:
            if category:
                task.category = category
            ids.append(self.add(task))
        return ids

    def get_next(self) -> Optional[ResearchTask]:
        """Get next task to process (doesn't remove from queue)."""
        for task_id in self.task_order:
            task = self.tasks.get(task_id)
            if task and task.status == TaskStatus.PENDING:
                return task
        return None

    def pop_next(self) -> Optional[ResearchTask]:
        """Get and mark next task as running."""
        task = self.get_next()
        if task:
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now().isoformat()
            self._save_state()
            if self.on_task_start:
                self.on_task_start(task)
        return task

    def complete_task(self, task_id: str, result: Dict = None, output_path: str = ""):
        """Mark a task as completed."""
        task = self.tasks.get(task_id)
        if task:
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now().isoformat()
            task.result = result or {}
            task.output_path = output_path

            # Calculate elapsed time
            if task.started_at:
                start = datetime.fromisoformat(task.started_at)
                end = datetime.fromisoformat(task.completed_at)
                task.elapsed_seconds = (end - start).total_seconds()

            self._save_state()
            if self.on_task_complete:
                self.on_task_complete(task)

    def fail_task(self, task_id: str, error: str):
        """Mark a task as failed."""
        task = self.tasks.get(task_id)
        if task:
            task.status = TaskStatus.FAILED
            task.completed_at = datetime.now().isoformat()
            task.error = error

            if task.started_at:
                start = datetime.fromisoformat(task.started_at)
                end = datetime.fromisoformat(task.completed_at)
                task.elapsed_seconds = (end - start).total_seconds()

            self._save_state()
            if self.on_task_fail:
                self.on_task_fail(task)

    def cancel_task(self, task_id: str):
        """Cancel a pending task."""
        task = self.tasks.get(task_id)
        if task and task.status == TaskStatus.PENDING:
            task.status = TaskStatus.CANCELLED
            self._save_state()

    def pause_task(self, task_id: str):
        """Pause a task."""
        task = self.tasks.get(task_id)
        if task:
            task.status = TaskStatus.PAUSED
            self._save_state()

    def resume_task(self, task_id: str):
        """Resume a paused task."""
        task = self.tasks.get(task_id)
        if task and task.status == TaskStatus.PAUSED:
            task.status = TaskStatus.PENDING
            self._save_state()

    def get_task(self, task_id: str) -> Optional[ResearchTask]:
        """Get a task by ID."""
        return self.tasks.get(task_id)

    def get_by_category(self, category: str) -> List[ResearchTask]:
        """Get all tasks in a category."""
        return [t for t in self.tasks.values() if t.category == category]

    def get_by_status(self, status: TaskStatus) -> List[ResearchTask]:
        """Get all tasks with a specific status."""
        return [t for t in self.tasks.values() if t.status == status]

    def get_pending_count(self) -> int:
        """Count pending tasks."""
        return len(self.get_by_status(TaskStatus.PENDING))

    def get_statistics(self) -> Dict:
        """Get queue statistics."""
        stats = {
            'total': len(self.tasks),
            'by_status': defaultdict(int),
            'by_category': defaultdict(int),
            'by_priority': defaultdict(int),
            'completed_time_avg': 0,
            'success_rate': 0
        }

        completed_times = []
        completed_count = 0
        failed_count = 0

        for task in self.tasks.values():
            stats['by_status'][task.status.value] += 1
            stats['by_category'][task.category] += 1
            stats['by_priority'][task.priority.name] += 1

            if task.status == TaskStatus.COMPLETED:
                completed_count += 1
                if task.elapsed_seconds > 0:
                    completed_times.append(task.elapsed_seconds)
            elif task.status == TaskStatus.FAILED:
                failed_count += 1

        if completed_times:
            stats['completed_time_avg'] = sum(completed_times) / len(completed_times)

        total_finished = completed_count + failed_count
        if total_finished > 0:
            stats['success_rate'] = completed_count / total_finished

        return dict(stats)

    def clear_completed(self):
        """Remove completed tasks from queue."""
        to_remove = [tid for tid, t in self.tasks.items()
                     if t.status == TaskStatus.COMPLETED]
        for tid in to_remove:
            del self.tasks[tid]
            if tid in self.task_order:
                self.task_order.remove(tid)
        self._save_state()

    def clear_all(self):
        """Clear all tasks (careful!)."""
        self.tasks.clear()
        self.task_order.clear()
        self._save_state()

    def list_tasks(self, limit: int = None) -> List[ResearchTask]:
        """List tasks in queue order."""
        tasks = [self.tasks[tid] for tid in self.task_order if tid in self.tasks]
        if limit:
            tasks = tasks[:limit]
        return tasks

    def __len__(self):
        return len(self.tasks)

    def __iter__(self):
        for tid in self.task_order:
            if tid in self.tasks:
                yield self.tasks[tid]


# =============================================================================
# TASK CREATION HELPERS
# =============================================================================

def create_derivation_task(
    target: str,
    target_value: float,
    assignment: str,
    category: str = "derivation",
    domain: str = "physics"
) -> ResearchTask:
    """Create a Z² constant derivation task."""
    # Extract clean name from target
    name = target.lower().replace(" ", "_").replace("-", "_")[:50]

    return ResearchTask(
        id="",  # Will be auto-generated
        name=name,
        description=assignment,
        category=category,
        target_constant=target,
        target_value=target_value,
        domain=domain,
        priority=TaskPriority.NORMAL
    )


def create_research_task(
    topic: str,
    domain: str,
    quantities: List[str] = None,
    priority: TaskPriority = TaskPriority.NORMAL
) -> ResearchTask:
    """Create a general research task."""
    name = topic.lower().replace(" ", "_")[:50]

    return ResearchTask(
        id="",
        name=name,
        description=f"Research {topic} in domain {domain}",
        category="research",
        domain=domain,
        quantities=quantities or [],
        priority=priority
    )

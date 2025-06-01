# routine_utils.py - Utility Functions for Daily Routine Manager
import json
import csv
from datetime import datetime, timedelta, time
from typing import List, Dict, Any, Optional, Tuple
import pandas as pd
from pathlib import Path
import hashlib
import re

from routine_models import DailyRoutine, WorkoutPlan, MealPlan, RoutineEntry


def calculate_routine_similarity(routine1: DailyRoutine, routine2: DailyRoutine) -> float:
    """Calculate similarity between two routines (0.0 to 1.0)"""
    # Compare activity names and times
    activities1 = set((entry.activity.lower(), entry.start_time) for entry in routine1.entries)
    activities2 = set((entry.activity.lower(), entry.start_time) for entry in routine2.entries)

    if not activities1 and not activities2:
        return 1.0

    if not activities1 or not activities2:
        return 0.0

    # Jaccard similarity
    intersection = len(activities1.intersection(activities2))
    union = len(activities1.union(activities2))

    return intersection / union if union > 0 else 0.0


def find_routine_conflicts(routine: DailyRoutine) -> List[Tuple[RoutineEntry, RoutineEntry]]:
    """Find time conflicts between routine entries"""
    conflicts = []
    entries = sorted(routine.entries, key=lambda x: x.start_time)

    for i in range(len(entries) - 1):
        current = entries[i]
        next_entry = entries[i + 1]

        current_end = datetime.strptime(current.end_time, "%H:%M").time()
        next_start = datetime.strptime(next_entry.start_time, "%H:%M").time()

        if current_end > next_start:
            conflicts.append((current, next_entry))

    return conflicts


def optimize_routine_timing(routine: DailyRoutine, buffer_minutes: int = 5) -> DailyRoutine:
    """Optimize routine timing to avoid conflicts"""
    # Sort entries by start time
    sorted_entries = sorted(routine.entries, key=lambda x: x.start_time)
    optimized_entries = []

    for i, entry in enumerate(sorted_entries):
        if i == 0:
            optimized_entries.append(entry)
            continue

        prev_entry = optimized_entries[-1]
        prev_end = datetime.strptime(prev_entry.end_time, "%H:%M")
        current_start = datetime.strptime(entry.start_time, "%H:%M")

        # Check if there's a conflict
        if prev_end.time() > current_start.time():
            # Adjust start time to avoid conflict
            new_start = prev_end + timedelta(minutes=buffer_minutes)
            duration = entry.duration_minutes
            new_end = new_start + timedelta(minutes=duration)

            optimized_entry = RoutineEntry(
                start_time=new_start.strftime("%H:%M"),
                end_time=new_end.strftime("%H:%M"),
                activity=entry.activity,
                category=entry.category,
                notes=entry.notes + f" (Auto-adjusted +{buffer_minutes}min)"
            )
            optimized_entries.append(optimized_entry)
        else:
            optimized_entries.append(entry)

    # Create new routine with optimized entries
    optimized_routine = DailyRoutine(
        name=routine.name + " (Optimized)",
        date=routine.date,
        routine_type=routine.routine_type,
        description=routine.description,
        entries=optimized_entries
    )

    return optimized_routine


def generate_routine_summary(routine: DailyRoutine) -> Dict[str, Any]:
    """Generate comprehensive summary of a routine"""
    return {
        "name": routine.name,
        "date": routine.date,
        "type": routine.routine_type,
        "total_activities": len(routine.entries),
        "completed_activities": len(routine.completed_entries),
        "completion_rate": f"{routine.completion_rate:.1%}",
        "total_duration": f"{routine.total_duration_minutes} minutes",
        "category_breakdown": routine.category_breakdown,
        "current_activity": routine.current_activity.activity if routine.current_activity else "None",
        "next_activity": routine.next_activity.activity if routine.next_activity else "None",
        "conflicts": len(find_routine_conflicts(routine)),
        "created_at": routine.created_at,
        "updated_at": routine.updated_at
    }


def export_routine_to_csv(routines: List[DailyRoutine], filename: str = None) -> str:
    """Export routines to CSV format"""
    if not filename:
        filename = f"routines_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    # Flatten routine data for CSV
    csv_data = []
    for routine in routines:
        for entry in routine.entries:
            csv_data.append({
                "routine_id": routine.id,
                "routine_name": routine.name,
                "routine_date": routine.date,
                "routine_type": routine.routine_type,
                "start_time": entry.start_time,
                "end_time": entry.end_time,
                "activity": entry.activity,
                "category": entry.category,
                "completed": entry.completed,
                "duration_minutes": entry.duration_minutes,
                "notes": entry.notes,
                "completion_rate": routine.completion_rate
            })

    # Write to CSV
    if csv_data:
        df = pd.DataFrame(csv_data)
        df.to_csv(filename, index=False)
        return filename

    return None


def import_routine_from_csv(filename: str) -> List[DailyRoutine]:
    """Import routines from CSV format"""
    try:
        df = pd.read_csv(filename)
        routines_data = {}

        for _, row in df.iterrows():
            routine_id = row['routine_id']

            if routine_id not in routines_data:
                routines_data[routine_id] = {
                    'name': row['routine_name'],
                    'date': row['routine_date'],
                    'routine_type': row['routine_type'],
                    'entries': []
                }

            entry = RoutineEntry(
                start_time=row['start_time'],
                end_time=row['end_time'],
                activity=row['activity'],
                category=row['category'],
                completed=bool(row['completed']),
                notes=str(row['notes']) if pd.notna(row['notes']) else ""
            )

            routines_data[routine_id]['entries'].append(entry)

        # Create DailyRoutine objects
        routines = []
        for routine_data in routines_data.values():
            routine = DailyRoutine(
                name=routine_data['name'],
                date=routine_data['date'],
                routine_type=routine_data['routine_type'],
                entries=routine_data['entries']
            )
            routines.append(routine)

        return routines

    except Exception as e:
        print(f"Error importing CSV: {e}")
        return []


def calculate_weekly_statistics(routines: List[DailyRoutine], week_start: datetime = None) -> Dict[str, Any]:
    """Calculate detailed weekly statistics"""
    if not week_start:
        week_start = datetime.now() - timedelta(days=datetime.now().weekday())

    week_end = week_start + timedelta(days=6)

    # Filter routines for the week
    week_routines = []
    for routine in routines:
        routine_date = datetime.fromisoformat(routine.date)
        if week_start.date() <= routine_date.date() <= week_end.date():
            week_routines.append(routine)

    if not week_routines:
        return {
            "week_start": week_start.date().isoformat(),
            "week_end": week_end.date().isoformat(),
            "total_routines": 0,
            "message": "No data for this week"
        }

    # Calculate statistics
    total_activities = sum(len(r.entries) for r in week_routines)
    completed_activities = sum(len(r.completed_entries) for r in week_routines)
    total_duration = sum(r.total_duration_minutes for r in week_routines)
    avg_completion = sum(r.completion_rate for r in week_routines) / len(week_routines)

    # Daily breakdown
    daily_stats = {}
    for i in range(7):
        day_date = (week_start + timedelta(days=i)).date()
        day_routine = next((r for r in week_routines if r.date == day_date.isoformat()), None)

        daily_stats[day_date.strftime('%A')] = {
            "date": day_date.isoformat(),
            "has_routine": bool(day_routine),
            "completion_rate": day_routine.completion_rate if day_routine else 0.0,
            "activities": len(day_routine.entries) if day_routine else 0,
            "duration": day_routine.total_duration_minutes if day_routine else 0
        }

    # Category analysis
    category_stats = {}
    for routine in week_routines:
        for entry in routine.entries:
            if entry.category not in category_stats:
                category_stats[entry.category] = {
                    "total": 0,
                    "completed": 0,
                    "duration": 0
                }

            category_stats[entry.category]["total"] += 1
            category_stats[entry.category]["duration"] += entry.duration_minutes
            if entry.completed:
                category_stats[entry.category]["completed"] += 1

    # Calculate completion rates for categories
    for category, stats in category_stats.items():
        stats["completion_rate"] = stats["completed"] / stats["total"] if stats["total"] > 0 else 0

    return {
        "week_start": week_start.date().isoformat(),
        "week_end": week_end.date().isoformat(),
        "total_routines": len(week_routines),
        "total_activities": total_activities,
        "completed_activities": completed_activities,
        "total_duration_hours": round(total_duration / 60, 1),
        "average_completion_rate": avg_completion,
        "daily_stats": daily_stats,
        "category_stats": category_stats,
        "consistency_score": len(week_routines) / 7,  # How many days had routines
        "best_day": max(daily_stats.items(), key=lambda x: x[1]["completion_rate"])[0],
        "total_break_time": sum(entry.duration_minutes for routine in week_routines
                                for entry in routine.entries if entry.category == "Break")
    }


def suggest_routine_improvements(routine: DailyRoutine) -> List[Dict[str, str]]:
    """Suggest improvements for a routine"""
    suggestions = []

    # Check for conflicts
    conflicts = find_routine_conflicts(routine)
    if conflicts:
        suggestions.append({
            "type": "warning",
            "title": "Time Conflicts Detected",
            "description": f"Found {len(conflicts)} overlapping activities. Consider adjusting times.",
            "action": "Use the optimize timing feature to fix conflicts automatically."
        })

    # Check for missing breaks
    work_entries = [e for e in routine.entries if e.category == "Work"]
    break_entries = [e for e in routine.entries if e.category == "Break"]

    if work_entries and len(break_entries) < len(work_entries) // 2:
        suggestions.append({
            "type": "info",
            "title": "Consider More Breaks",
            "description": "Adding breaks between work sessions can improve productivity and well-being.",
            "action": "Add 5-10 minute breaks every 2 hours of work."
        })

    # Check routine balance
    category_breakdown = routine.category_breakdown
    total_entries = len(routine.entries)

    if category_breakdown.get("Exercise", 0) == 0:
        suggestions.append({
            "type": "suggestion",
            "title": "Add Physical Activity",
            "description": "No exercise activities found. Physical activity is important for health.",
            "action": "Consider adding a workout or active recovery session."
        })

    if category_breakdown.get("Recovery", 0) / total_entries < 0.2:
        suggestions.append({
            "type": "suggestion",
            "title": "Increase Recovery Time",
            "description": "Recovery activities make up less than 20% of your routine.",
            "action": "Add more time for rest, relaxation, or sleep preparation."
        })

    # Check for very long activities
    long_activities = [e for e in routine.entries if e.duration_minutes > 180]  # 3+ hours
    if long_activities:
        suggestions.append({
            "type": "warning",
            "title": "Very Long Activities",
            "description": f"Found {len(long_activities)} activities longer than 3 hours.",
            "action": "Consider breaking long activities into smaller segments with breaks."
        })

    # Check completion rate
    if routine.completion_rate < 0.5:
        suggestions.append({
            "type": "warning",
            "title": "Low Completion Rate",
            "description": f"Current completion rate is {routine.completion_rate:.1%}.",
            "action": "Consider reducing the number of activities or making them more achievable."
        })

    return suggestions


def generate_routine_hash(routine: DailyRoutine) -> str:
    """Generate a unique hash for a routine based on its structure"""
    # Create a string representation of the routine structure
    routine_string = f"{routine.name}|{routine.routine_type}|"

    for entry in sorted(routine.entries, key=lambda x: x.start_time):
        routine_string += f"{entry.start_time}-{entry.end_time}-{entry.activity}-{entry.category}|"

    # Generate MD5 hash
    return hashlib.md5(routine_string.encode()).hexdigest()


def find_similar_routines(target_routine: DailyRoutine, all_routines: List[DailyRoutine],
                          threshold: float = 0.3) -> List[Tuple[DailyRoutine, float]]:
    """Find routines similar to the target routine"""
    similar_routines = []

    for routine in all_routines:
        if routine.id == target_routine.id:
            continue

        similarity = calculate_routine_similarity(target_routine, routine)
        if similarity >= threshold:
            similar_routines.append((routine, similarity))

    # Sort by similarity (highest first)
    similar_routines.sort(key=lambda x: x[1], reverse=True)

    return similar_routines


def validate_routine_data(routine: DailyRoutine) -> List[str]:
    """Validate routine data and return list of issues"""
    issues = []

    # Check basic fields
    if not routine.name or not routine.name.strip():
        issues.append("Routine name is empty")

    if not routine.date:
        issues.append("Routine date is missing")
    else:
        try:
            datetime.fromisoformat(routine.date)
        except ValueError:
            issues.append("Invalid date format")

    if not routine.entries:
        issues.append("Routine has no activities")

    # Validate entries
    for i, entry in enumerate(routine.entries):
        entry_prefix = f"Entry {i + 1}"

        if not entry.activity or not entry.activity.strip():
            issues.append(f"{entry_prefix}: Activity name is empty")

        if not entry.category:
            issues.append(f"{entry_prefix}: Category is missing")

        # Validate time format
        time_pattern = r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$"

        if not re.match(time_pattern, entry.start_time):
            issues.append(f"{entry_prefix}: Invalid start time format")

        if not re.match(time_pattern, entry.end_time):
            issues.append(f"{entry_prefix}: Invalid end time format")

        # Check if end time is after start time
        try:
            start = datetime.strptime(entry.start_time, "%H:%M").time()
            end = datetime.strptime(entry.end_time, "%H:%M").time()

            if end <= start:
                issues.append(f"{entry_prefix}: End time must be after start time")
        except ValueError:
            pass  # Already caught by format validation

    return issues


def create_routine_template_from_routine(routine: DailyRoutine) -> Dict[str, Any]:
    """Create a reusable template from an existing routine"""
    template_entries = []

    for entry in routine.entries:
        template_entries.append({
            "start_time": entry.start_time,
            "end_time": entry.end_time,
            "activity": entry.activity,
            "category": entry.category,
            "notes": entry.notes
        })

    return {
        "name": f"{routine.name} Template",
        "template_type": routine.routine_type,
        "description": f"Template created from {routine.name} on {routine.date}",
        "default_entries": template_entries
    }


def calculate_routine_efficiency_score(routine: DailyRoutine) -> Dict[str, Any]:
    """Calculate an efficiency score for the routine"""
    total_minutes = routine.total_duration_minutes

    if total_minutes == 0:
        return {"score": 0, "breakdown": {}, "recommendations": ["Add activities to routine"]}

    # Category weights (higher is better for efficiency)
    category_weights = {
        "Exercise": 1.0,
        "Work": 0.8,
        "Study": 0.9,
        "Meal": 0.6,
        "Recovery": 0.7,
        "Break": 0.4,
        "Other": 0.5
    }

    # Calculate weighted time
    weighted_time = 0
    category_breakdown = {}

    for entry in routine.entries:
        weight = category_weights.get(entry.category, 0.5)
        weighted_duration = entry.duration_minutes * weight
        weighted_time += weighted_duration

        if entry.category not in category_breakdown:
            category_breakdown[entry.category] = 0
        category_breakdown[entry.category] += entry.duration_minutes

    # Base efficiency score
    efficiency_score = (weighted_time / total_minutes) * 100

    # Completion bonus
    completion_bonus = routine.completion_rate * 20

    # Conflict penalty
    conflicts = find_routine_conflicts(routine)
    conflict_penalty = len(conflicts) * 5

    # Final score
    final_score = max(0, min(100, efficiency_score + completion_bonus - conflict_penalty))

    # Generate recommendations
    recommendations = []
    if final_score < 50:
        recommendations.append("Consider adding more high-value activities (Exercise, Study)")
    if len(conflicts) > 0:
        recommendations.append("Resolve time conflicts between activities")
    if routine.completion_rate < 0.8:
        recommendations.append("Focus on completing more activities")

    return {
        "score": round(final_score, 1),
        "breakdown": {
            "base_efficiency": round(efficiency_score, 1),
            "completion_bonus": round(completion_bonus, 1),
            "conflict_penalty": round(conflict_penalty, 1)
        },
        "category_time": category_breakdown,
        "recommendations": recommendations,
        "grade": get_efficiency_grade(final_score)
    }


def get_efficiency_grade(score: float) -> str:
    """Convert efficiency score to letter grade"""
    if score >= 90:
        return "A+"
    elif score >= 85:
        return "A"
    elif score >= 80:
        return "A-"
    elif score >= 75:
        return "B+"
    elif score >= 70:
        return "B"
    elif score >= 65:
        return "B-"
    elif score >= 60:
        return "C+"
    elif score >= 55:
        return "C"
    elif score >= 50:
        return "C-"
    else:
        return "F"


def merge_routine_entries(entries: List[RoutineEntry], merge_threshold: int = 15) -> List[RoutineEntry]:
    """Merge similar consecutive entries to reduce fragmentation"""
    if not entries:
        return []

    sorted_entries = sorted(entries, key=lambda x: x.start_time)
    merged_entries = [sorted_entries[0]]

    for current_entry in sorted_entries[1:]:
        last_entry = merged_entries[-1]

        # Check if entries can be merged
        last_end = datetime.strptime(last_entry.end_time, "%H:%M")
        current_start = datetime.strptime(current_entry.start_time, "%H:%M")
        time_gap = (current_start - last_end).total_seconds() / 60

        # Merge if same category, same activity, and small time gap
        if (last_entry.category == current_entry.category and
                last_entry.activity == current_entry.activity and
                time_gap <= merge_threshold):

            # Update the last entry's end time
            last_entry.end_time = current_entry.end_time
            if current_entry.notes and current_entry.notes not in last_entry.notes:
                last_entry.notes += f" | {current_entry.notes}"
        else:
            merged_entries.append(current_entry)

    return merged_entries

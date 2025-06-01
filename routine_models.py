# routine_models.py - Data Models for Daily Routine Manager
from datetime import datetime, time
from typing import List, Dict, Any, Optional
import uuid
from dataclasses import dataclass, field


@dataclass
class RoutineEntry:
    """Individual entry within a daily routine"""
    start_time: str  # Format: "HH:MM"
    end_time: str  # Format: "HH:MM"
    activity: str
    category: str  # "Exercise", "Work", "Meal", "Break", "Study", "Recovery", "Other"
    completed: bool = False
    notes: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'activity': self.activity,
            'category': self.category,
            'completed': self.completed,
            'notes': self.notes
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RoutineEntry':
        """Create from dictionary"""
        return cls(
            id=data.get('id', str(uuid.uuid4())),
            start_time=data['start_time'],
            end_time=data['end_time'],
            activity=data['activity'],
            category=data['category'],
            completed=data.get('completed', False),
            notes=data.get('notes', '')
        )

    @property
    def duration_minutes(self) -> int:
        """Calculate duration in minutes"""
        try:
            start = datetime.strptime(self.start_time, "%H:%M").time()
            end = datetime.strptime(self.end_time, "%H:%M").time()

            start_minutes = start.hour * 60 + start.minute
            end_minutes = end.hour * 60 + end.minute

            # Handle overnight activities
            if end_minutes < start_minutes:
                end_minutes += 24 * 60

            return end_minutes - start_minutes
        except:
            return 0

    @property
    def time_range(self) -> str:
        """Get formatted time range"""
        return f"{self.start_time} - {self.end_time}"

    def toggle_completion(self):
        """Toggle completion status"""
        self.completed = not self.completed


@dataclass
class DailyRoutine:
    """Complete daily routine containing multiple entries"""
    name: str
    date: str  # Format: "YYYY-MM-DD"
    routine_type: str  # "Weekday", "Weekend", "Game Day", "Rest Day", "Custom"
    entries: List[RoutineEntry]
    description: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date,
            'routine_type': self.routine_type,
            'description': self.description,
            'entries': [entry.to_dict() for entry in self.entries],
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DailyRoutine':
        """Create from dictionary"""
        entries = [RoutineEntry.from_dict(entry_data) for entry_data in data.get('entries', [])]

        return cls(
            id=data.get('id', str(uuid.uuid4())),
            name=data['name'],
            date=data['date'],
            routine_type=data['routine_type'],
            description=data.get('description', ''),
            entries=entries,
            created_at=data.get('created_at', datetime.now().isoformat()),
            updated_at=data.get('updated_at', datetime.now().isoformat())
        )

    @property
    def completion_rate(self) -> float:
        """Calculate completion rate (0.0 to 1.0)"""
        if not self.entries:
            return 0.0

        completed_count = sum(1 for entry in self.entries if entry.completed)
        return completed_count / len(self.entries)

    @property
    def completed_entries(self) -> List[RoutineEntry]:
        """Get list of completed entries"""
        return [entry for entry in self.entries if entry.completed]

    @property
    def pending_entries(self) -> List[RoutineEntry]:
        """Get list of pending entries"""
        return [entry for entry in self.entries if not entry.completed]

    @property
    def total_duration_minutes(self) -> int:
        """Calculate total routine duration in minutes"""
        return sum(entry.duration_minutes for entry in self.entries)

    @property
    def category_breakdown(self) -> Dict[str, int]:
        """Get breakdown of activities by category"""
        breakdown = {}
        for entry in self.entries:
            breakdown[entry.category] = breakdown.get(entry.category, 0) + 1
        return breakdown

    @property
    def current_activity(self) -> Optional[RoutineEntry]:
        """Get current activity based on time"""
        now = datetime.now().time()
        current_time_str = now.strftime("%H:%M")

        for entry in self.entries:
            start_time = datetime.strptime(entry.start_time, "%H:%M").time()
            end_time = datetime.strptime(entry.end_time, "%H:%M").time()

            # Handle overnight activities
            if end_time < start_time:
                if now >= start_time or now <= end_time:
                    return entry
            else:
                if start_time <= now <= end_time:
                    return entry

        return None

    @property
    def next_activity(self) -> Optional[RoutineEntry]:
        """Get next upcoming activity"""
        now = datetime.now().time()
        current_time_str = now.strftime("%H:%M")

        upcoming_entries = []
        for entry in self.entries:
            start_time = datetime.strptime(entry.start_time, "%H:%M").time()
            if start_time > now:
                upcoming_entries.append(entry)

        if upcoming_entries:
            return min(upcoming_entries, key=lambda x: x.start_time)

        return None

    def add_entry(self, entry: RoutineEntry):
        """Add a new entry to the routine"""
        self.entries.append(entry)
        self.updated_at = datetime.now().isoformat()

    def remove_entry(self, entry_id: str):
        """Remove an entry by ID"""
        self.entries = [entry for entry in self.entries if entry.id != entry_id]
        self.updated_at = datetime.now().isoformat()

    def mark_entry_complete(self, entry_id: str, completed: bool = True):
        """Mark a specific entry as completed or not"""
        for entry in self.entries:
            if entry.id == entry_id:
                entry.completed = completed
                break
        self.updated_at = datetime.now().isoformat()

    @property
    def completion_status_text(self) -> str:
        """Get human-readable completion status"""
        rate = self.completion_rate
        if rate >= 0.9:
            return "Excellent! Almost done! 🎯"
        elif rate >= 0.7:
            return "Great progress! 📈"
        elif rate >= 0.5:
            return "Good start! Keep going! ⚡"
        elif rate >= 0.3:
            return "Getting started! 🔥"
        else:
            return "Just beginning! 💪"

    @property
    def completion_color(self) -> str:
        """Get color based on completion rate"""
        rate = self.completion_rate
        if rate >= 0.8:
            return "#11998e"  # Success green
        elif rate >= 0.6:
            return "#667eea"  # Primary blue
        elif rate >= 0.4:
            return "#fdcb6e"  # Warning orange
        else:
            return "#fd79a8"  # Attention pink

    @property
    def completion_gradient(self) -> str:
        """Get gradient based on completion rate"""
        rate = self.completion_rate
        if rate >= 0.8:
            return "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)"
        elif rate >= 0.6:
            return "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        elif rate >= 0.4:
            return "linear-gradient(135deg, #fdcb6e 0%, #e17055 100%)"
        else:
            return "linear-gradient(135deg, #fd79a8 0%, #e84393 100%)"

    @property
    def time_of_day_distribution(self) -> Dict[str, int]:
        """Get distribution of activities by time of day"""
        distribution = {
            "Morning (6-12)": 0,
            "Afternoon (12-17)": 0,
            "Evening (17-21)": 0,
            "Night (21-6)": 0
        }

        for entry in self.entries:
            try:
                hour = int(entry.start_time.split(':')[0])
                if 6 <= hour < 12:
                    distribution["Morning (6-12)"] += 1
                elif 12 <= hour < 17:
                    distribution["Afternoon (12-17)"] += 1
                elif 17 <= hour < 21:
                    distribution["Evening (17-21)"] += 1
                else:
                    distribution["Night (21-6)"] += 1
            except:
                pass

        return distribution

    @property
    def estimated_energy_requirement(self) -> str:
        """Estimate energy requirement for the day"""
        total_intensity = 0
        activity_count = 0

        # Simple scoring based on activity types
        intensity_weights = {
            "Exercise": 3,
            "Work": 2,
            "Study": 2,
            "Meal": 1,
            "Break": 0,
            "Recovery": 0,
            "Other": 1
        }

        for entry in self.entries:
            weight = intensity_weights.get(entry.category, 1)
            duration_factor = min(entry.duration_minutes / 60, 2)  # Cap at 2 hours
            total_intensity += weight * duration_factor
            activity_count += 1

        if activity_count == 0:
            return "Low"

        avg_intensity = total_intensity / activity_count

        if avg_intensity >= 2.5:
            return "High"
        elif avg_intensity >= 1.5:
            return "Medium"
        else:
            return "Low"


@dataclass
class WorkoutPlan:
    """Workout plan for fitness activities"""
    name: str
    workout_type: str  # "Strength", "Cardio", "Flexibility", "Sports", "Mixed"
    duration: int  # minutes
    intensity: int  # 1-10 scale
    target_muscle_groups: str
    equipment: List[str]
    exercises: List[str]
    instructions: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'workout_type': self.workout_type,
            'duration': self.duration,
            'intensity': self.intensity,
            'target_muscle_groups': self.target_muscle_groups,
            'equipment': self.equipment,
            'exercises': self.exercises,
            'instructions': self.instructions,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorkoutPlan':
        """Create from dictionary"""
        return cls(
            id=data.get('id', str(uuid.uuid4())),
            name=data['name'],
            workout_type=data['workout_type'],
            duration=data['duration'],
            intensity=data['intensity'],
            target_muscle_groups=data['target_muscle_groups'],
            equipment=data.get('equipment', []),
            exercises=data.get('exercises', []),
            instructions=data.get('instructions', ''),
            created_at=data.get('created_at', datetime.now().isoformat())
        )

    @property
    def estimated_calories(self) -> int:
        """Estimate calories burned (rough calculation)"""
        # Base calories per minute based on intensity
        base_cpm = {
            1: 3, 2: 4, 3: 5, 4: 6, 5: 7,
            6: 8, 7: 10, 8: 12, 9: 14, 10: 16
        }

        calories_per_minute = base_cpm.get(self.intensity, 7)
        return calories_per_minute * self.duration

    @property
    def difficulty_level(self) -> str:
        """Get difficulty level based on intensity and duration"""
        if self.intensity <= 3 and self.duration <= 30:
            return "Beginner"
        elif self.intensity <= 6 and self.duration <= 60:
            return "Intermediate"
        elif self.intensity <= 8 and self.duration <= 90:
            return "Advanced"
        else:
            return "Expert"


@dataclass
class MealPlan:
    """Meal plan for nutrition planning"""
    name: str
    meal_type: str  # "Breakfast", "Lunch", "Dinner", "Snack", "Pre-Workout", "Post-Workout"
    calories: int
    protein: float  # grams
    carbs: float  # grams
    fat: float  # grams
    ingredients: List[str]
    instructions: str = ""
    prep_time: int = 0  # minutes
    cook_time: int = 0  # minutes
    servings: int = 1
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'meal_type': self.meal_type,
            'calories': self.calories,
            'protein': self.protein,
            'carbs': self.carbs,
            'fat': self.fat,
            'ingredients': self.ingredients,
            'instructions': self.instructions,
            'prep_time': self.prep_time,
            'cook_time': self.cook_time,
            'servings': self.servings,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MealPlan':
        """Create from dictionary"""
        return cls(
            id=data.get('id', str(uuid.uuid4())),
            name=data['name'],
            meal_type=data['meal_type'],
            calories=data['calories'],
            protein=data['protein'],
            carbs=data['carbs'],
            fat=data['fat'],
            ingredients=data.get('ingredients', []),
            instructions=data.get('instructions', ''),
            prep_time=data.get('prep_time', 0),
            cook_time=data.get('cook_time', 0),
            servings=data.get('servings', 1),
            created_at=data.get('created_at', datetime.now().isoformat())
        )

    @property
    def total_time(self) -> int:
        """Total time including prep and cooking"""
        return self.prep_time + self.cook_time

    @property
    def macros_per_serving(self) -> Dict[str, float]:
        """Get macros per serving"""
        return {
            'protein': self.protein / self.servings,
            'carbs': self.carbs / self.servings,
            'fat': self.fat / self.servings,
            'calories': self.calories / self.servings
        }

    @property
    def protein_percentage(self) -> float:
        """Protein as percentage of total calories"""
        protein_calories = self.protein * 4
        return (protein_calories / max(self.calories, 1)) * 100

    @property
    def carb_percentage(self) -> float:
        """Carbs as percentage of total calories"""
        carb_calories = self.carbs * 4
        return (carb_calories / max(self.calories, 1)) * 100

    @property
    def fat_percentage(self) -> float:
        """Fat as percentage of total calories"""
        fat_calories = self.fat * 9
        return (fat_calories / max(self.calories, 1)) * 100

    @property
    def is_balanced(self) -> bool:
        """Check if meal has balanced macros (rough guidelines)"""
        protein_pct = self.protein_percentage
        carb_pct = self.carb_percentage
        fat_pct = self.fat_percentage

        # Rough guidelines for balanced meal
        return (15 <= protein_pct <= 35 and
                25 <= carb_pct <= 65 and
                20 <= fat_pct <= 35)


@dataclass
class RoutineTemplate:
    """Template for creating new routines"""
    name: str
    template_type: str  # "Weekday", "Weekend", "Game Day", "Rest Day", "Custom"
    description: str
    default_entries: List[Dict[str, Any]]  # Template entries (not RoutineEntry objects)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'template_type': self.template_type,
            'description': self.description,
            'default_entries': self.default_entries,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RoutineTemplate':
        """Create from dictionary"""
        return cls(
            id=data.get('id', str(uuid.uuid4())),
            name=data['name'],
            template_type=data['template_type'],
            description=data['description'],
            default_entries=data.get('default_entries', []),
            created_at=data.get('created_at', datetime.now().isoformat())
        )

    def create_routine(self, date: str, custom_name: str = None) -> DailyRoutine:
        """Create a DailyRoutine from this template"""
        entries = []
        for entry_data in self.default_entries:
            entry = RoutineEntry(
                start_time=entry_data['start_time'],
                end_time=entry_data['end_time'],
                activity=entry_data['activity'],
                category=entry_data['category']
            )
            entries.append(entry)

        routine_name = custom_name or f"{self.name} - {date}"

        return DailyRoutine(
            name=routine_name,
            date=date,
            routine_type=self.template_type,
            description=self.description,
            entries=entries
        )


# Utility functions for routine management
def get_routine_stats(routines: List[DailyRoutine]) -> Dict[str, Any]:
    """Calculate statistics for a list of routines"""
    if not routines:
        return {
            'total_routines': 0,
            'average_completion': 0.0,
            'total_activities': 0,
            'most_common_type': None,
            'activity_breakdown': {}
        }

    total_completion = sum(routine.completion_rate for routine in routines)
    avg_completion = total_completion / len(routines)

    # Count routine types
    type_counts = {}
    activity_counts = {}
    total_activities = 0

    for routine in routines:
        # Count routine types
        type_counts[routine.routine_type] = type_counts.get(routine.routine_type, 0) + 1

        # Count activities by category
        for entry in routine.entries:
            activity_counts[entry.category] = activity_counts.get(entry.category, 0) + 1
            total_activities += 1

    most_common_type = max(type_counts.items(), key=lambda x: x[1])[0] if type_counts else None

    return {
        'total_routines': len(routines),
        'average_completion': avg_completion,
        'total_activities': total_activities,
        'most_common_type': most_common_type,
        'activity_breakdown': activity_counts,
        'type_breakdown': type_counts
    }


def calculate_weekly_stats(routines: List[DailyRoutine], target_date: datetime = None) -> Dict[str, Any]:
    """Calculate statistics for a specific week"""
    if target_date is None:
        target_date = datetime.now()

    # Get start of week (Monday)
    start_of_week = target_date - timedelta(days=target_date.weekday())
    week_dates = [start_of_week.date() + timedelta(days=i) for i in range(7)]

    week_routines = []
    for routine in routines:
        routine_date = datetime.fromisoformat(routine.date).date()
        if routine_date in week_dates:
            week_routines.append(routine)

    # Calculate completion for each day
    daily_completion = {}
    for date in week_dates:
        routine = next(
            (r for r in week_routines if datetime.fromisoformat(r.date).date() == date),
            None
        )
        daily_completion[date.strftime('%A')] = routine.completion_rate if routine else 0.0

    weekly_avg = sum(daily_completion.values()) / 7

    return {
        'week_start': start_of_week.date().isoformat(),
        'daily_completion': daily_completion,
        'weekly_average': weekly_avg,
        'routines_completed': len([r for r in week_routines if r.completion_rate >= 0.8]),
        'total_activities': sum(len(r.entries) for r in week_routines)
    }


# Default templates
DEFAULT_TEMPLATES = [
    RoutineTemplate(
        name="Standard Weekday",
        template_type="Weekday",
        description="Standard weekday routine for work days",
        default_entries=[
            {"start_time": "06:00", "end_time": "06:20", "activity": "Wake Up & Pain Relief", "category": "Recovery"},
            {"start_time": "06:30", "end_time": "07:30", "activity": "Morning Workout", "category": "Exercise"},
            {"start_time": "07:30", "end_time": "08:00", "activity": "Breakfast", "category": "Meal"},
            {"start_time": "08:00", "end_time": "12:00", "activity": "Work - Morning Session", "category": "Work"},
            {"start_time": "12:00", "end_time": "13:00", "activity": "Lunch", "category": "Meal"},
            {"start_time": "13:00", "end_time": "17:00", "activity": "Work - Afternoon Session", "category": "Work"},
            {"start_time": "17:30", "end_time": "18:30", "activity": "Study Time", "category": "Study"},
            {"start_time": "18:30", "end_time": "19:30", "activity": "Dinner", "category": "Meal"},
            {"start_time": "19:30", "end_time": "20:30", "activity": "Brain Training", "category": "Study"},
            {"start_time": "20:30", "end_time": "22:00", "activity": "Personal Time", "category": "Recovery"},
            {"start_time": "22:00", "end_time": "22:30", "activity": "Sleep Preparation", "category": "Recovery"}
        ]
    ),
    RoutineTemplate(
        name="Game Day",
        template_type="Game Day",
        description="Sunday game day routine for football",
        default_entries=[
            {"start_time": "07:00", "end_time": "07:30", "activity": "Game Day Morning", "category": "Recovery"},
            {"start_time": "07:30", "end_time": "08:30", "activity": "Pre-Game Meal", "category": "Meal"},
            {"start_time": "08:30", "end_time": "11:00", "activity": "Game Preparation", "category": "Exercise"},
            {"start_time": "11:00", "end_time": "14:00", "activity": "Football Match", "category": "Exercise"},
            {"start_time": "14:00", "end_time": "15:00", "activity": "Post-Game Recovery", "category": "Recovery"},
            {"start_time": "15:00", "end_time": "16:00", "activity": "Recovery Meal", "category": "Meal"},
            {"start_time": "16:00", "end_time": "17:00", "activity": "Active Recovery", "category": "Recovery"},
            {"start_time": "17:00", "end_time": "18:00", "activity": "Study Time", "category": "Study"},
            {"start_time": "18:00", "end_time": "19:00", "activity": "Dinner", "category": "Meal"},
            {"start_time": "20:00", "end_time": "21:00", "activity": "Recovery & Preparation", "category": "Recovery"},
            {"start_time": "21:00", "end_time": "22:00", "activity": "Early Sleep Preparation", "category": "Recovery"}
        ]
    )
]
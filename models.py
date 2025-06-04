from dataclasses import dataclass, asdict
from typing import List
import uuid


def generate_id() -> str:
    """Generate a unique 8-character ID"""
    return str(uuid.uuid4())[:8]


@dataclass
class RoutineTask:
    id: str
    name: str
    description: str
    time: str
    duration: int  # minutes
    category: str
    completed: bool = False


@dataclass
class DailyRoutine:
    id: str
    name: str
    date: str
    tasks: List[RoutineTask]
    notes: str = ""


@dataclass
class Exercise:
    id: str
    name: str
    sets: int
    reps: str  # Can be "12" or "12-15" or "30 seconds"
    weight: str
    notes: str = ""


@dataclass
class WorkoutPlan:
    id: str
    name: str
    description: str
    exercises: List[Exercise]
    target_muscle_groups: List[str]
    difficulty: str
    estimated_duration: int  # minutes


@dataclass
class Meal:
    id: str
    name: str
    calories: int
    protein: float
    carbs: float
    fat: float
    ingredients: List[str]
    notes: str = ""


@dataclass
class DietPlan:
    id: str
    name: str
    description: str
    meals: List[Meal]
    daily_calories: int
    daily_protein: float
    daily_carbs: float
    daily_fat: float


# Utility functions for converting dictionaries to objects
def dict_to_routine_task(d: dict) -> RoutineTask:
    return RoutineTask(**d)


def dict_to_daily_routine(d: dict) -> DailyRoutine:
    tasks = [dict_to_routine_task(task) for task in d['tasks']]
    return DailyRoutine(
        id=d['id'],
        name=d['name'],
        date=d['date'],
        tasks=tasks,
        notes=d.get('notes', '')
    )


def dict_to_exercise(d: dict) -> Exercise:
    return Exercise(**d)


def dict_to_workout_plan(d: dict) -> WorkoutPlan:
    exercises = [dict_to_exercise(ex) for ex in d['exercises']]
    return WorkoutPlan(
        id=d['id'],
        name=d['name'],
        description=d['description'],
        exercises=exercises,
        target_muscle_groups=d['target_muscle_groups'],
        difficulty=d['difficulty'],
        estimated_duration=d['estimated_duration']
    )


def dict_to_meal(d: dict) -> Meal:
    return Meal(**d)


def dict_to_diet_plan(d: dict) -> DietPlan:
    meals = [dict_to_meal(meal) for meal in d['meals']]
    return DietPlan(
        id=d['id'],
        name=d['name'],
        description=d['description'],
        meals=meals,
        daily_calories=d['daily_calories'],
        daily_protein=d['daily_protein'],
        daily_carbs=d['daily_carbs'],
        daily_fat=d['daily_fat']
    )

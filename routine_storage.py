# routine_storage.py - Storage Manager for Daily Routine Data
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from routine_models import DailyRoutine, WorkoutPlan, MealPlan, RoutineTemplate


class RoutineStorage:
    """Storage manager for routine data with JSON file persistence"""

    def __init__(self, data_dir: str = "routine_data"):
        """Initialize storage manager"""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        # Create subdirectories
        self.backups_dir = self.data_dir / "backups"
        self.backups_dir.mkdir(exist_ok=True)

        # File paths
        self.routines_file = self.data_dir / "routines.json"
        self.workout_plans_file = self.data_dir / "workout_plans.json"
        self.meal_plans_file = self.data_dir / "meal_plans.json"
        self.templates_file = self.data_dir / "templates.json"

        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _load_json_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Load data from JSON file with error handling"""
        if not file_path.exists():
            return []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, IOError) as e:
            self.logger.error(f"Error loading {file_path}: {e}")
            return []

    def _save_json_file(self, file_path: Path, data: List[Dict[str, Any]]) -> bool:
        """Save data to JSON file with error handling"""
        try:
            # Create backup of existing file
            if file_path.exists():
                backup_path = self.backups_dir / f"{file_path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                file_path.rename(backup_path)

                # Keep only last 10 backups
                self._cleanup_backups(file_path.stem)

            # Save new data
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)

            self.logger.info(f"Successfully saved {len(data)} items to {file_path}")
            return True

        except (IOError, TypeError) as e:
            self.logger.error(f"Error saving {file_path}: {e}")
            return False

    def _cleanup_backups(self, file_prefix: str, keep_count: int = 10):
        """Keep only the most recent backup files"""
        backup_pattern = f"{file_prefix}_*.json"
        backup_files = list(self.backups_dir.glob(backup_pattern))

        if len(backup_files) > keep_count:
            # Sort by modification time and remove oldest
            backup_files.sort(key=lambda x: x.stat().st_mtime)
            for old_backup in backup_files[:-keep_count]:
                try:
                    old_backup.unlink()
                except OSError:
                    pass

    # Routines management
    def load_routines(self) -> List[DailyRoutine]:
        """Load all daily routines"""
        data = self._load_json_file(self.routines_file)
        routines = []

        for item in data:
            try:
                routine = DailyRoutine.from_dict(item)
                routines.append(routine)
            except (KeyError, TypeError) as e:
                self.logger.warning(f"Skipping invalid routine data: {e}")

        return routines

    def save_routines(self, routines: List[DailyRoutine]) -> bool:
        """Save all daily routines"""
        data = [routine.to_dict() for routine in routines]
        return self._save_json_file(self.routines_file, data)

    def add_routine(self, routine: DailyRoutine) -> bool:
        """Add a single routine"""
        routines = self.load_routines()

        # Check if routine for this date already exists
        existing_routine = next(
            (r for r in routines if r.date == routine.date), None
        )

        if existing_routine:
            # Update existing routine
            routines = [r for r in routines if r.date != routine.date]
            routines.append(routine)
        else:
            # Add new routine
            routines.append(routine)

        return self.save_routines(routines)

    def delete_routine(self, routine_id: str) -> bool:
        """Delete a routine by ID"""
        routines = self.load_routines()
        initial_count = len(routines)

        routines = [r for r in routines if r.id != routine_id]

        if len(routines) < initial_count:
            return self.save_routines(routines)

        return False

    def get_routine_by_date(self, date: str) -> Optional[DailyRoutine]:
        """Get routine for a specific date"""
        routines = self.load_routines()
        return next((r for r in routines if r.date == date), None)

    def get_routine_by_id(self, routine_id: str) -> Optional[DailyRoutine]:
        """Get routine by ID"""
        routines = self.load_routines()
        return next((r for r in routines if r.id == routine_id), None)

    # Workout plans management
    def load_workout_plans(self) -> List[WorkoutPlan]:
        """Load all workout plans"""
        data = self._load_json_file(self.workout_plans_file)
        workout_plans = []

        for item in data:
            try:
                workout = WorkoutPlan.from_dict(item)
                workout_plans.append(workout)
            except (KeyError, TypeError) as e:
                self.logger.warning(f"Skipping invalid workout plan data: {e}")

        return workout_plans

    def save_workout_plans(self, workout_plans: List[WorkoutPlan]) -> bool:
        """Save all workout plans"""
        data = [workout.to_dict() for workout in workout_plans]
        return self._save_json_file(self.workout_plans_file, data)

    def add_workout_plan(self, workout_plan: WorkoutPlan) -> bool:
        """Add a single workout plan"""
        workout_plans = self.load_workout_plans()
        workout_plans.append(workout_plan)
        return self.save_workout_plans(workout_plans)

    def delete_workout_plan(self, workout_id: str) -> bool:
        """Delete a workout plan by ID"""
        workout_plans = self.load_workout_plans()
        initial_count = len(workout_plans)

        workout_plans = [w for w in workout_plans if w.id != workout_id]

        if len(workout_plans) < initial_count:
            return self.save_workout_plans(workout_plans)

        return False

    def get_workout_plan_by_id(self, workout_id: str) -> Optional[WorkoutPlan]:
        """Get workout plan by ID"""
        workout_plans = self.load_workout_plans()
        return next((w for w in workout_plans if w.id == workout_id), None)

    # Meal plans management
    def load_meal_plans(self) -> List[MealPlan]:
        """Load all meal plans"""
        data = self._load_json_file(self.meal_plans_file)
        meal_plans = []

        for item in data:
            try:
                meal = MealPlan.from_dict(item)
                meal_plans.append(meal)
            except (KeyError, TypeError) as e:
                self.logger.warning(f"Skipping invalid meal plan data: {e}")

        return meal_plans

    def save_meal_plans(self, meal_plans: List[MealPlan]) -> bool:
        """Save all meal plans"""
        data = [meal.to_dict() for meal in meal_plans]
        return self._save_json_file(self.meal_plans_file, data)

    def add_meal_plan(self, meal_plan: MealPlan) -> bool:
        """Add a single meal plan"""
        meal_plans = self.load_meal_plans()
        meal_plans.append(meal_plan)
        return self.save_meal_plans(meal_plans)

    def delete_meal_plan(self, meal_id: str) -> bool:
        """Delete a meal plan by ID"""
        meal_plans = self.load_meal_plans()
        initial_count = len(meal_plans)

        meal_plans = [m for m in meal_plans if m.id != meal_id]

        if len(meal_plans) < initial_count:
            return self.save_meal_plans(meal_plans)

        return False

    def get_meal_plan_by_id(self, meal_id: str) -> Optional[MealPlan]:
        """Get meal plan by ID"""
        meal_plans = self.load_meal_plans()
        return next((m for m in meal_plans if m.id == meal_id), None)

    # Templates management
    def load_templates(self) -> List[RoutineTemplate]:
        """Load all routine templates"""
        data = self._load_json_file(self.templates_file)
        templates = []

        for item in data:
            try:
                template = RoutineTemplate.from_dict(item)
                templates.append(template)
            except (KeyError, TypeError) as e:
                self.logger.warning(f"Skipping invalid template data: {e}")

        return templates

    def save_templates(self, templates: List[RoutineTemplate]) -> bool:
        """Save all routine templates"""
        data = [template.to_dict() for template in templates]
        return self._save_json_file(self.templates_file, data)

    def add_template(self, template: RoutineTemplate) -> bool:
        """Add a single template"""
        templates = self.load_templates()
        templates.append(template)
        return self.save_templates(templates)

    # Data export/import
    def export_all_data(self) -> Dict[str, Any]:
        """Export all data for backup or transfer"""
        return {
            "routines": [r.to_dict() for r in self.load_routines()],
            "workout_plans": [w.to_dict() for w in self.load_workout_plans()],
            "meal_plans": [m.to_dict() for m in self.load_meal_plans()],
            "templates": [t.to_dict() for t in self.load_templates()],
            "export_timestamp": datetime.now().isoformat(),
            "version": "1.0"
        }

    def import_all_data(self, data: Dict[str, Any]) -> bool:
        """Import data from export file"""
        try:
            # Validate data structure
            required_keys = ["routines", "workout_plans", "meal_plans"]
            if not all(key in data for key in required_keys):
                self.logger.error("Invalid import data structure")
                return False

            # Create backup of current data
            backup_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_data = self.export_all_data()
            backup_file = self.backups_dir / f"full_backup_{backup_timestamp}.json"

            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, default=str)

            # Import routines
            routines = []
            for routine_data in data["routines"]:
                try:
                    routine = DailyRoutine.from_dict(routine_data)
                    routines.append(routine)
                except Exception as e:
                    self.logger.warning(f"Skipping invalid routine during import: {e}")

            # Import workout plans
            workout_plans = []
            for workout_data in data["workout_plans"]:
                try:
                    workout = WorkoutPlan.from_dict(workout_data)
                    workout_plans.append(workout)
                except Exception as e:
                    self.logger.warning(f"Skipping invalid workout plan during import: {e}")

            # Import meal plans
            meal_plans = []
            for meal_data in data["meal_plans"]:
                try:
                    meal = MealPlan.from_dict(meal_data)
                    meal_plans.append(meal)
                except Exception as e:
                    self.logger.warning(f"Skipping invalid meal plan during import: {e}")

            # Import templates (if present)
            templates = []
            if "templates" in data:
                for template_data in data["templates"]:
                    try:
                        template = RoutineTemplate.from_dict(template_data)
                        templates.append(template)
                    except Exception as e:
                        self.logger.warning(f"Skipping invalid template during import: {e}")

            # Save all imported data
            success = all([
                self.save_routines(routines),
                self.save_workout_plans(workout_plans),
                self.save_meal_plans(meal_plans),
                self.save_templates(templates) if templates else True
            ])

            if success:
                self.logger.info(f"Successfully imported {len(routines)} routines, "
                                 f"{len(workout_plans)} workout plans, "
                                 f"{len(meal_plans)} meal plans, "
                                 f"{len(templates)} templates")

            return success

        except Exception as e:
            self.logger.error(f"Error during data import: {e}")
            return False

    # Data statistics and utilities
    def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage statistics"""
        routines = self.load_routines()
        workout_plans = self.load_workout_plans()
        meal_plans = self.load_meal_plans()
        templates = self.load_templates()

        # Calculate file sizes
        file_sizes = {}
        for file_path in [self.routines_file, self.workout_plans_file,
                          self.meal_plans_file, self.templates_file]:
            if file_path.exists():
                file_sizes[file_path.name] = file_path.stat().st_size
            else:
                file_sizes[file_path.name] = 0

        # Count backup files
        backup_count = len(list(self.backups_dir.glob("*.json")))

        return {
            "data_counts": {
                "routines": len(routines),
                "workout_plans": len(workout_plans),
                "meal_plans": len(meal_plans),
                "templates": len(templates)
            },
            "file_sizes_bytes": file_sizes,
            "backup_files": backup_count,
            "data_directory": str(self.data_dir),
            "last_update": datetime.now().isoformat()
        }

    def cleanup_old_data(self, days_old: int = 30) -> Dict[str, int]:
        """Clean up old backup files"""
        cutoff_date = datetime.now().timestamp() - (days_old * 24 * 60 * 60)

        cleanup_stats = {
            "old_backups_removed": 0,
            "bytes_freed": 0
        }

        for backup_file in self.backups_dir.glob("*.json"):
            if backup_file.stat().st_mtime < cutoff_date:
                file_size = backup_file.stat().st_size
                try:
                    backup_file.unlink()
                    cleanup_stats["old_backups_removed"] += 1
                    cleanup_stats["bytes_freed"] += file_size
                except OSError:
                    pass

        return cleanup_stats

    def verify_data_integrity(self) -> Dict[str, Any]:
        """Verify data integrity and report any issues"""
        integrity_report = {
            "timestamp": datetime.now().isoformat(),
            "status": "healthy",
            "issues": [],
            "warnings": []
        }

        # Check routines
        try:
            routines = self.load_routines()
            for routine in routines:
                if not routine.entries:
                    integrity_report["warnings"].append(f"Routine {routine.id} has no entries")

                # Check for duplicate entries at same time
                times = [entry.start_time for entry in routine.entries]
                if len(times) != len(set(times)):
                    integrity_report["warnings"].append(f"Routine {routine.id} has overlapping times")

        except Exception as e:
            integrity_report["issues"].append(f"Error loading routines: {e}")
            integrity_report["status"] = "issues_found"

        # Check workout plans
        try:
            workout_plans = self.load_workout_plans()
            for workout in workout_plans:
                if workout.duration <= 0:
                    integrity_report["warnings"].append(f"Workout {workout.id} has invalid duration")
                if not (1 <= workout.intensity <= 10):
                    integrity_report["warnings"].append(f"Workout {workout.id} has invalid intensity")

        except Exception as e:
            integrity_report["issues"].append(f"Error loading workout plans: {e}")
            integrity_report["status"] = "issues_found"

        # Check meal plans
        try:
            meal_plans = self.load_meal_plans()
            for meal in meal_plans:
                if meal.calories <= 0:
                    integrity_report["warnings"].append(f"Meal {meal.id} has invalid calories")
                if meal.protein < 0 or meal.carbs < 0 or meal.fat < 0:
                    integrity_report["warnings"].append(f"Meal {meal.id} has negative macros")

        except Exception as e:
            integrity_report["issues"].append(f"Error loading meal plans: {e}")
            integrity_report["status"] = "issues_found"

        # Set status based on findings
        if integrity_report["issues"]:
            integrity_report["status"] = "issues_found"
        elif integrity_report["warnings"]:
            integrity_report["status"] = "warnings_found"

        return integrity_report


# Utility functions for storage operations
def migrate_data_format(storage: RoutineStorage, backup: bool = True) -> bool:
    """Migrate data to newer format (for future use)"""
    if backup:
        backup_data = storage.export_all_data()
        backup_file = storage.backups_dir / f"migration_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, default=str)

    # Placeholder for future migration logic
    return True


def create_sample_data(storage: RoutineStorage) -> bool:
    """Create sample data for testing/demo purposes"""
    from routine_models import DEFAULT_TEMPLATES

    # Add default templates
    for template in DEFAULT_TEMPLATES:
        storage.add_template(template)

    # Create sample routine for today
    today_routine = DEFAULT_TEMPLATES[0].create_routine(
        date=datetime.now().date().isoformat(),
        custom_name="Today's Routine"
    )
    storage.add_routine(today_routine)

    # Create sample workout plans
    sample_workouts = [
        WorkoutPlan(
            name="Morning Strength Training",
            workout_type="Strength",
            duration=45,
            intensity=7,
            target_muscle_groups="Full Body",
            equipment=["Dumbbells", "Resistance Bands"],
            exercises=["Squats", "Push-ups", "Planks", "Deadlifts"],
            instructions="Focus on form over weight. Rest 60-90 seconds between sets."
        ),
        WorkoutPlan(
            name="Cardio Blast",
            workout_type="Cardio",
            duration=30,
            intensity=8,
            target_muscle_groups="Cardiovascular System",
            equipment=["None"],
            exercises=["Jumping Jacks", "High Knees", "Burpees", "Mountain Climbers"],
            instructions="High intensity interval training. 30 seconds work, 15 seconds rest."
        )
    ]

    for workout in sample_workouts:
        storage.add_workout_plan(workout)

    # Create sample meal plans
    sample_meals = [
        MealPlan(
            name="Power Breakfast",
            meal_type="Breakfast",
            calories=450,
            protein=25,
            carbs=45,
            fat=15,
            ingredients=["Oats", "Banana", "Protein Powder", "Berries", "Almond Milk"],
            instructions="Combine oats with almond milk, add protein powder, top with banana and berries.",
            prep_time=5,
            cook_time=3,
            servings=1
        ),
        MealPlan(
            name="Chicken & Rice Bowl",
            meal_type="Lunch",
            calories=520,
            protein=45,
            carbs=48,
            fat=12,
            ingredients=["Chicken Breast", "Brown Rice", "Mixed Vegetables", "Olive Oil"],
            instructions="Grill chicken breast, serve over brown rice with steamed vegetables.",
            prep_time=10,
            cook_time=25,
            servings=1
        )
    ]

    for meal in sample_meals:
        storage.add_meal_plan(meal)

    return True
# database_manager.py - Elite Football Performance System Database Manager
import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
import hashlib
import os


class DatabaseManager:
    """Advanced database manager with backup and sync capabilities"""

    def __init__(self, data_dir: str = "elite_football_data"):
        """Initialize database manager"""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        # Create subdirectories
        self.backup_dir = self.data_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)

        self.logs_dir = self.data_dir / "logs"
        self.logs_dir.mkdir(exist_ok=True)

        # Setup logging
        self.setup_logging()
        self.logger.info("Database manager initialized")

    def setup_logging(self):
        """Setup logging for database operations"""
        log_file = self.logs_dir / f"database_{datetime.now().strftime('%Y%m%d')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('DatabaseManager')

    def _get_user_file(self, user_id: str, data_type: str) -> Path:
        """Get file path for user data"""
        return self.data_dir / f"{user_id}_{data_type}.json"

    def _load_json(self, filepath: Path) -> Optional[Dict[str, Any]]:
        """Load JSON data from file with error handling"""
        if not filepath.exists():
            self.logger.debug(f"File not found: {filepath}")
            return None

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.logger.debug(f"Successfully loaded: {filepath}")
            return data
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decode error in {filepath}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error loading {filepath}: {e}")
            return None

    def _save_json(self, filepath: Path, data: Any) -> bool:
        """Save data to JSON file with error handling"""
        try:
            # Create backup of existing file
            if filepath.exists():
                backup_path = filepath.with_suffix('.json.bak')
                filepath.rename(backup_path)

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str, ensure_ascii=False)

            # Remove backup on successful save
            backup_path = filepath.with_suffix('.json.bak')
            if backup_path.exists():
                backup_path.unlink()

            self.logger.debug(f"Successfully saved: {filepath}")
            return True

        except Exception as e:
            self.logger.error(f"Error saving {filepath}: {e}")

            # Restore backup if save failed
            backup_path = filepath.with_suffix('.json.bak')
            if backup_path.exists():
                backup_path.rename(filepath)
                self.logger.info(f"Restored backup for {filepath}")

            return False

    def _validate_user_id(self, user_id: str) -> bool:
        """Validate user ID format"""
        if not user_id or not isinstance(user_id, str):
            return False

        # Check for valid characters (alphanumeric and underscores)
        return user_id.replace('_', '').replace('-', '').isalnum()

    # User Management
    def load_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Load user profile data"""
        if not self._validate_user_id(user_id):
            self.logger.warning(f"Invalid user ID: {user_id}")
            return None

        filepath = self._get_user_file(user_id, "profile")
        return self._load_json(filepath)

    def save_user(self, user_data: Dict[str, Any]) -> bool:
        """Save user profile data"""
        if not user_data or 'user_id' not in user_data:
            self.logger.error("Invalid user data: missing user_id")
            return False

        user_id = user_data['user_id']
        if not self._validate_user_id(user_id):
            self.logger.warning(f"Invalid user ID: {user_id}")
            return False

        filepath = self._get_user_file(user_id, "profile")
        success = self._save_json(filepath, user_data)

        if success:
            self.logger.info(f"User profile saved: {user_id}")
        return success

    def delete_user(self, user_id: str) -> bool:
        """Delete all user data (use with caution)"""
        if not self._validate_user_id(user_id):
            self.logger.warning(f"Invalid user ID: {user_id}")
            return False

        try:
            # List all data types
            data_types = [
                "profile", "workouts", "meals", "wellness",
                "achievements", "goals", "brain_sessions"
            ]

            deleted_files = 0
            for data_type in data_types:
                filepath = self._get_user_file(user_id, data_type)
                if filepath.exists():
                    filepath.unlink()
                    deleted_files += 1

            self.logger.info(f"Deleted {deleted_files} files for user: {user_id}")
            return True

        except Exception as e:
            self.logger.error(f"Error deleting user data for {user_id}: {e}")
            return False

    # Workout Management
    def load_workouts(self, user_id: str) -> List[Dict[str, Any]]:
        """Load workout data for user"""
        if not self._validate_user_id(user_id):
            return []

        filepath = self._get_user_file(user_id, "workouts")
        data = self._load_json(filepath)
        return data if data else []

    def save_workouts(self, user_id: str, workouts: List[Dict[str, Any]]) -> bool:
        """Save workout data for user"""
        if not self._validate_user_id(user_id):
            return False

        filepath = self._get_user_file(user_id, "workouts")
        success = self._save_json(filepath, workouts)

        if success:
            self.logger.info(f"Workouts saved for user: {user_id} ({len(workouts)} entries)")
        return success

    def add_workout(self, user_id: str, workout: Dict[str, Any]) -> bool:
        """Add a single workout to user's data"""
        workouts = self.load_workouts(user_id)
        workouts.append(workout)
        return self.save_workouts(user_id, workouts)

    # Meal Management
    def load_meals(self, user_id: str) -> List[Dict[str, Any]]:
        """Load meal data for user"""
        if not self._validate_user_id(user_id):
            return []

        filepath = self._get_user_file(user_id, "meals")
        data = self._load_json(filepath)
        return data if data else []

    def save_meals(self, user_id: str, meals: List[Dict[str, Any]]) -> bool:
        """Save meal data for user"""
        if not self._validate_user_id(user_id):
            return False

        filepath = self._get_user_file(user_id, "meals")
        success = self._save_json(filepath, meals)

        if success:
            self.logger.info(f"Meals saved for user: {user_id} ({len(meals)} entries)")
        return success

    def add_meal(self, user_id: str, meal: Dict[str, Any]) -> bool:
        """Add a single meal to user's data"""
        meals = self.load_meals(user_id)
        meals.append(meal)
        return self.save_meals(user_id, meals)

    # Wellness Management
    def load_wellness(self, user_id: str) -> List[Dict[str, Any]]:
        """Load wellness data for user"""
        if not self._validate_user_id(user_id):
            return []

        filepath = self._get_user_file(user_id, "wellness")
        data = self._load_json(filepath)
        return data if data else []

    def save_wellness(self, user_id: str, wellness: List[Dict[str, Any]]) -> bool:
        """Save wellness data for user"""
        if not self._validate_user_id(user_id):
            return False

        filepath = self._get_user_file(user_id, "wellness")
        success = self._save_json(filepath, wellness)

        if success:
            self.logger.info(f"Wellness data saved for user: {user_id} ({len(wellness)} entries)")
        return success

    def add_wellness_entry(self, user_id: str, wellness_entry: Dict[str, Any]) -> bool:
        """Add a single wellness entry to user's data"""
        wellness = self.load_wellness(user_id)
        wellness.append(wellness_entry)
        return self.save_wellness(user_id, wellness)

    # Achievement Management
    def load_achievements(self, user_id: str) -> List[Dict[str, Any]]:
        """Load achievement data for user"""
        if not self._validate_user_id(user_id):
            return []

        filepath = self._get_user_file(user_id, "achievements")
        data = self._load_json(filepath)
        return data if data else []

    def save_achievements(self, user_id: str, achievements: List[Dict[str, Any]]) -> bool:
        """Save achievement data for user"""
        if not self._validate_user_id(user_id):
            return False

        filepath = self._get_user_file(user_id, "achievements")
        success = self._save_json(filepath, achievements)

        if success:
            self.logger.info(f"Achievements saved for user: {user_id} ({len(achievements)} entries)")
        return success

    def unlock_achievement(self, user_id: str, achievement_id: str) -> bool:
        """Unlock a specific achievement for user"""
        achievements = self.load_achievements(user_id)

        for achievement in achievements:
            if achievement.get('achievement_id') == achievement_id:
                achievement['unlocked'] = True
                achievement['date_unlocked'] = datetime.now().isoformat()
                achievement['progress'] = 100

                self.logger.info(f"Achievement unlocked: {achievement_id} for user: {user_id}")
                return self.save_achievements(user_id, achievements)

        self.logger.warning(f"Achievement not found: {achievement_id} for user: {user_id}")
        return False

    # Goal Management
    def load_goals(self, user_id: str) -> List[Dict[str, Any]]:
        """Load goal data for user"""
        if not self._validate_user_id(user_id):
            return []

        filepath = self._get_user_file(user_id, "goals")
        data = self._load_json(filepath)
        return data if data else []

    def save_goals(self, user_id: str, goals: List[Dict[str, Any]]) -> bool:
        """Save goal data for user"""
        if not self._validate_user_id(user_id):
            return False

        filepath = self._get_user_file(user_id, "goals")
        success = self._save_json(filepath, goals)

        if success:
            self.logger.info(f"Goals saved for user: {user_id} ({len(goals)} entries)")
        return success

    def add_goal(self, user_id: str, goal: Dict[str, Any]) -> bool:
        """Add a single goal to user's data"""
        goals = self.load_goals(user_id)
        goals.append(goal)
        return self.save_goals(user_id, goals)

    def update_goal_progress(self, user_id: str, goal_id: str, new_progress: float) -> bool:
        """Update progress for a specific goal"""
        goals = self.load_goals(user_id)

        for goal in goals:
            if goal.get('goal_id') == goal_id:
                goal['progress'] = min(max(new_progress, 0), 100)

                if goal['progress'] >= 100:
                    goal['completed'] = True
                    goal['completion_date'] = datetime.now().isoformat()

                self.logger.info(f"Goal progress updated: {goal_id} to {new_progress}% for user: {user_id}")
                return self.save_goals(user_id, goals)

        self.logger.warning(f"Goal not found: {goal_id} for user: {user_id}")
        return False

    # Brain Training Management
    def load_brain_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """Load brain training session data for user"""
        if not self._validate_user_id(user_id):
            return []

        filepath = self._get_user_file(user_id, "brain_sessions")
        data = self._load_json(filepath)
        return data if data else []

    def save_brain_sessions(self, user_id: str, sessions: List[Dict[str, Any]]) -> bool:
        """Save brain training session data for user"""
        if not self._validate_user_id(user_id):
            return False

        filepath = self._get_user_file(user_id, "brain_sessions")
        success = self._save_json(filepath, sessions)

        if success:
            self.logger.info(f"Brain sessions saved for user: {user_id} ({len(sessions)} entries)")
        return success

    def add_brain_session(self, user_id: str, session: Dict[str, Any]) -> bool:
        """Add a single brain training session to user's data"""
        sessions = self.load_brain_sessions(user_id)
        sessions.append(session)
        return self.save_brain_sessions(user_id, sessions)

    # Backup and Recovery
    def create_backup(self, user_id: str) -> Optional[str]:
        """Create a timestamped backup of all user data"""
        if not self._validate_user_id(user_id):
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"{user_id}_backup_{timestamp}.json"

        try:
            all_data = {
                "user_profile": self.load_user(user_id),
                "workouts": self.load_workouts(user_id),
                "meals": self.load_meals(user_id),
                "wellness": self.load_wellness(user_id),
                "achievements": self.load_achievements(user_id),
                "goals": self.load_goals(user_id),
                "brain_sessions": self.load_brain_sessions(user_id),
                "backup_timestamp": timestamp,
                "backup_date": datetime.now().isoformat()
            }

            success = self._save_json(backup_file, all_data)

            if success:
                self.logger.info(f"Backup created: {backup_file}")

                # Cleanup old backups (keep last 10)
                self.cleanup_old_backups(user_id, keep_count=10)

                return str(backup_file)
            else:
                return None

        except Exception as e:
            self.logger.error(f"Error creating backup for {user_id}: {e}")
            return None

    def restore_from_backup(self, user_id: str, backup_timestamp: str) -> bool:
        """Restore user data from a specific backup"""
        if not self._validate_user_id(user_id):
            return False

        backup_file = self.backup_dir / f"{user_id}_backup_{backup_timestamp}.json"

        if not backup_file.exists():
            self.logger.error(f"Backup file not found: {backup_file}")
            return False

        try:
            backup_data = self._load_json(backup_file)
            if not backup_data:
                return False

            # Restore all data
            success = True

            if backup_data.get("user_profile"):
                success &= self.save_user(backup_data["user_profile"])

            success &= self.save_workouts(user_id, backup_data.get("workouts", []))
            success &= self.save_meals(user_id, backup_data.get("meals", []))
            success &= self.save_wellness(user_id, backup_data.get("wellness", []))
            success &= self.save_achievements(user_id, backup_data.get("achievements", []))
            success &= self.save_goals(user_id, backup_data.get("goals", []))
            success &= self.save_brain_sessions(user_id, backup_data.get("brain_sessions", []))

            if success:
                self.logger.info(f"Successfully restored backup for {user_id} from {backup_timestamp}")
            else:
                self.logger.error(f"Partial failure restoring backup for {user_id}")

            return success

        except Exception as e:
            self.logger.error(f"Error restoring backup for {user_id}: {e}")
            return False

    def get_backup_list(self, user_id: str) -> List[Dict[str, Any]]:
        """Get list of available backups for user"""
        if not self._validate_user_id(user_id):
            return []

        backup_pattern = f"{user_id}_backup_*.json"
        backup_files = list(self.backup_dir.glob(backup_pattern))

        backups = []
        for backup_file in backup_files:
            try:
                timestamp = backup_file.stem.split('_backup_')[1]
                file_stats = backup_file.stat()

                backups.append({
                    "timestamp": timestamp,
                    "file": backup_file.name,
                    "size": file_stats.st_size,
                    "created": datetime.fromtimestamp(file_stats.st_mtime),
                    "formatted_date": datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                })
            except Exception as e:
                self.logger.warning(f"Error processing backup file {backup_file}: {e}")

        return sorted(backups, key=lambda x: x['created'], reverse=True)

    def cleanup_old_backups(self, user_id: str, keep_count: int = 10) -> int:
        """Keep only the most recent backups"""
        if not self._validate_user_id(user_id):
            return 0

        backups = self.get_backup_list(user_id)

        if len(backups) <= keep_count:
            return 0

        deleted_count = 0
        for backup in backups[keep_count:]:
            try:
                backup_file = self.backup_dir / backup['file']
                backup_file.unlink()
                deleted_count += 1
            except Exception as e:
                self.logger.warning(f"Error deleting backup {backup['file']}: {e}")

        if deleted_count > 0:
            self.logger.info(f"Cleaned up {deleted_count} old backups for user: {user_id}")

        return deleted_count

    # Data Analysis and Statistics
    def get_user_statistics(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive statistics for user"""
        if not self._validate_user_id(user_id):
            return {}

        try:
            workouts = self.load_workouts(user_id)
            meals = self.load_meals(user_id)
            wellness = self.load_wellness(user_id)
            achievements = self.load_achievements(user_id)
            goals = self.load_goals(user_id)
            brain_sessions = self.load_brain_sessions(user_id)

            stats = {
                "data_counts": {
                    "workouts": len(workouts),
                    "meals": len(meals),
                    "wellness_entries": len(wellness),
                    "achievements": len(achievements),
                    "goals": len(goals),
                    "brain_sessions": len(brain_sessions)
                },
                "date_ranges": {},
                "achievement_stats": {
                    "total": len(achievements),
                    "unlocked": len([a for a in achievements if a.get('unlocked', False)]),
                    "total_points": sum(a.get('points', 0) for a in achievements if a.get('unlocked', False))
                },
                "goal_stats": {
                    "total": len(goals),
                    "completed": len([g for g in goals if g.get('completed', False)]),
                    "average_progress": sum(g.get('progress', 0) for g in goals) / max(len(goals), 1)
                }
            }

            # Calculate date ranges
            all_dates = []

            for workout in workouts:
                if 'date' in workout:
                    all_dates.append(workout['date'])

            for meal in meals:
                if 'date' in meal:
                    all_dates.append(meal['date'])

            for entry in wellness:
                if 'date' in entry:
                    all_dates.append(entry['date'])

            if all_dates:
                all_dates.sort()
                stats["date_ranges"] = {
                    "first_entry": all_dates[0],
                    "last_entry": all_dates[-1],
                    "total_days": len(set(date.split('T')[0] for date in all_dates))
                }

            return stats

        except Exception as e:
            self.logger.error(f"Error calculating statistics for {user_id}: {e}")
            return {}

    # Data Export
    def export_user_data(self, user_id: str, format: str = "json") -> Optional[str]:
        """Export all user data in specified format"""
        if not self._validate_user_id(user_id):
            return None

        try:
            export_data = {
                "user_profile": self.load_user(user_id),
                "workouts": self.load_workouts(user_id),
                "meals": self.load_meals(user_id),
                "wellness": self.load_wellness(user_id),
                "achievements": self.load_achievements(user_id),
                "goals": self.load_goals(user_id),
                "brain_sessions": self.load_brain_sessions(user_id),
                "export_timestamp": datetime.now().isoformat(),
                "statistics": self.get_user_statistics(user_id)
            }

            if format.lower() == "json":
                export_file = self.data_dir / f"{user_id}_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                success = self._save_json(export_file, export_data)

                if success:
                    self.logger.info(f"Data exported to: {export_file}")
                    return str(export_file)
                else:
                    return None

            else:
                self.logger.error(f"Unsupported export format: {format}")
                return None

        except Exception as e:
            self.logger.error(f"Error exporting data for {user_id}: {e}")
            return None

    # Data Integrity
    def verify_data_integrity(self, user_id: str) -> Dict[str, Any]:
        """Verify data integrity for user"""
        if not self._validate_user_id(user_id):
            return {"valid": False, "error": "Invalid user ID"}

        try:
            integrity_report = {
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "valid": True,
                "issues": [],
                "warnings": []
            }

            # Check if user profile exists
            user_profile = self.load_user(user_id)
            if not user_profile:
                integrity_report["issues"].append("User profile not found")
                integrity_report["valid"] = False

            # Check data consistency
            data_types = [
                ("workouts", self.load_workouts),
                ("meals", self.load_meals),
                ("wellness", self.load_wellness),
                ("achievements", self.load_achievements),
                ("goals", self.load_goals),
                ("brain_sessions", self.load_brain_sessions)
            ]

            for data_type, load_function in data_types:
                try:
                    data = load_function(user_id)
                    if data is None:
                        integrity_report["warnings"].append(f"{data_type} data could not be loaded")
                except Exception as e:
                    integrity_report["issues"].append(f"Error loading {data_type}: {str(e)}")
                    integrity_report["valid"] = False

            return integrity_report

        except Exception as e:
            return {
                "valid": False,
                "error": f"Error during integrity check: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    # System Maintenance
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information and statistics"""
        try:
            # Count total files
            total_files = len(list(self.data_dir.glob("*.json")))
            backup_files = len(list(self.backup_dir.glob("*.json")))

            # Calculate total size
            total_size = sum(f.stat().st_size for f in self.data_dir.rglob("*.json"))

            # Get unique users
            user_files = list(self.data_dir.glob("*_profile.json"))
            unique_users = len(user_files)

            return {
                "database_path": str(self.data_dir),
                "total_files": total_files,
                "backup_files": backup_files,
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "unique_users": unique_users,
                "created": datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Error getting system info: {e}")
            return {"error": str(e)}

    def cleanup_system(self, days_old: int = 30) -> dict[str, int] | dict[str, str]:
        """Clean up old temporary files and logs"""
        try:
            cleanup_stats = {
                "old_backups_removed": 0,
                "old_logs_removed": 0,
                "temp_files_removed": 0
            }

            cutoff_date = datetime.now() - timedelta(days=days_old)

            # Clean old logs
            for log_file in self.logs_dir.glob("*.log"):
                if datetime.fromtimestamp(log_file.stat().st_mtime) < cutoff_date:
                    log_file.unlink()
                    cleanup_stats["old_logs_removed"] += 1

            # Clean old temporary files
            for temp_file in self.data_dir.glob("*.tmp"):
                if datetime.fromtimestamp(temp_file.stat().st_mtime) < cutoff_date:
                    temp_file.unlink()
                    cleanup_stats["temp_files_removed"] += 1

            self.logger.info(f"System cleanup completed: {cleanup_stats}")
            return cleanup_stats

        except Exception as e:
            self.logger.error(f"Error during system cleanup: {e}")
            return {"error": str(e)}
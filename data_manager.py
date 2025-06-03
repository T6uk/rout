import json
import streamlit as st
from typing import Dict, List, Any


class DataManager:
    """Handles all data persistence operations for the wellness app"""

    def __init__(self):
        self.routines_file = "daily_routines.json"
        self.workouts_file = "workout_plans.json"
        self.diets_file = "diet_plans.json"

    def load_data(self, filename: str) -> List[Dict]:
        """Load data from JSON file"""
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            st.error(f"Error reading {filename}. File may be corrupted.")
            return []

    def save_data(self, data: List[Dict], filename: str) -> bool:
        """Save data to JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            st.error(f"Error saving to {filename}: {str(e)}")
            return False

    def load_routines(self) -> List[Dict]:
        """Load daily routines data"""
        return self.load_data(self.routines_file)

    def save_routines(self, data: List[Dict]) -> bool:
        """Save daily routines data"""
        return self.save_data(data, self.routines_file)

    def load_workouts(self) -> List[Dict]:
        """Load workout plans data"""
        return self.load_data(self.workouts_file)

    def save_workouts(self, data: List[Dict]) -> bool:
        """Save workout plans data"""
        return self.save_data(data, self.workouts_file)

    def load_diets(self) -> List[Dict]:
        """Load diet plans data"""
        return self.load_data(self.diets_file)

    def save_diets(self, data: List[Dict]) -> bool:
        """Save diet plans data"""
        return self.save_data(data, self.diets_file)

    def export_data(self, data_type: str) -> str:
        """Export data as JSON string"""
        if data_type == "routines":
            data = self.load_routines()
        elif data_type == "workouts":
            data = self.load_workouts()
        elif data_type == "diets":
            data = self.load_diets()
        else:
            return "{}"
        return json.dumps(data, indent=2)

    def import_data(self, json_str: str, data_type: str) -> bool:
        """Import data from JSON string"""
        try:
            data = json.loads(json_str)
            if data_type == "routines":
                return self.save_routines(data)
            elif data_type == "workouts":
                return self.save_workouts(data)
            elif data_type == "diets":
                return self.save_diets(data)
            return False
        except json.JSONDecodeError:
            st.error("Invalid JSON format")
            return False
        except Exception as e:
            st.error(f"Error importing data: {str(e)}")
            return False

    def delete_routine(self, routine_id: str) -> bool:
        """Delete a specific routine"""
        routines = self.load_routines()
        routines = [r for r in routines if r['id'] != routine_id]
        return self.save_routines(routines)

    def delete_workout(self, workout_id: str) -> bool:
        """Delete a specific workout plan"""
        workouts = self.load_workouts()
        workouts = [w for w in workouts if w['id'] != workout_id]
        return self.save_workouts(workouts)

    def delete_diet(self, diet_id: str) -> bool:
        """Delete a specific diet plan"""
        diets = self.load_diets()
        diets = [d for d in diets if d['id'] != diet_id]
        return self.save_diets(diets)

    def get_stats(self) -> Dict[str, int]:
        """Get statistics about stored data"""
        return {
            "routines": len(self.load_routines()),
            "workouts": len(self.load_workouts()),
            "diets": len(self.load_diets())
        }


# Cached instance for Streamlit
@st.cache_resource
def get_data_manager():
    """Get cached data manager instance"""
    return DataManager()
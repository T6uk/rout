# config.py - Configuration Settings for Daily Routine Manager
from datetime import time
from typing import Dict, List, Any
import os

# Application Configuration
APP_CONFIG = {
    "app_name": "Daily Routine Manager",
    "version": "1.0.0",
    "author": "Personal Productivity Suite",
    "description": "Organize your perfect day with intelligent routine management",
    "data_directory": "routine_data",
    "backup_frequency": "daily",
    "auto_save": True,
    "max_backups": 30,
    "session_timeout": 3600,  # seconds
    "supported_languages": ["en"],
    "default_language": "en",
    "timezone": "UTC",
    "date_format": "%Y-%m-%d",
    "time_format": "%H:%M",
    "datetime_format": "%Y-%m-%d %H:%M:%S"
}

# UI Configuration with Enhanced Design
UI_CONFIG = {
    "theme": "glassmorphism",
    "primary_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "success_gradient": "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)",
    "warning_gradient": "linear-gradient(135deg, #fdcb6e 0%, #e17055 100%)",
    "danger_gradient": "linear-gradient(135deg, #fd79a8 0%, #e84393 100%)",
    "info_gradient": "linear-gradient(135deg, #74b9ff 0%, #0984e3 100%)",

    # Glass morphism colors
    "glass_bg": "rgba(255, 255, 255, 0.25)",
    "glass_border": "rgba(255, 255, 255, 0.18)",
    "glass_shadow": "0 8px 32px 0 rgba(31, 38, 135, 0.37)",

    # Enhanced color palette
    "colors": {
        "primary": "#667eea",
        "secondary": "#764ba2",
        "success": "#11998e",
        "warning": "#fdcb6e",
        "danger": "#fd79a8",
        "info": "#74b9ff",
        "light": "#f7fafc",
        "dark": "#2d3748",
        "muted": "#718096"
    },

    # Typography
    "fonts": {
        "primary": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        "heading": "'Inter', sans-serif",
        "monospace": "'JetBrains Mono', 'Fira Code', monospace"
    },

    # Enhanced spacing scale
    "spacing": {
        "xs": "0.25rem",
        "sm": "0.5rem",
        "md": "1rem",
        "lg": "1.5rem",
        "xl": "2rem",
        "2xl": "3rem",
        "3xl": "4rem"
    },

    # Border radius scale
    "border_radius": {
        "sm": "8px",
        "md": "12px",
        "lg": "16px",
        "xl": "20px",
        "2xl": "24px",
        "full": "50%"
    },

    # Enhanced shadows
    "shadows": {
        "sm": "0 2px 8px rgba(0, 0, 0, 0.1)",
        "md": "0 4px 20px rgba(0, 0, 0, 0.1)",
        "lg": "0 8px 32px rgba(0, 0, 0, 0.15)",
        "xl": "0 20px 60px rgba(0, 0, 0, 0.2)"
    },

    # Animation configuration
    "animations": {
        "enabled": True,
        "duration": "0.3s",
        "easing": "cubic-bezier(0.4, 0, 0.2, 1)",
        "hover_scale": 1.02,
        "hover_translate": "-2px"
    },

    # Responsive breakpoints
    "breakpoints": {
        "mobile": "576px",
        "tablet": "768px",
        "desktop": "992px",
        "large": "1200px",
        "xl": "1400px"
    },

    # Enhanced component styling
    "components": {
        "card": {
            "border_radius": "20px",
            "padding": "2rem",
            "shadow": "0 8px 32px rgba(0, 0, 0, 0.1)",
            "backdrop_filter": "blur(20px)"
        },
        "button": {
            "border_radius": "12px",
            "padding": "0.875rem 2rem",
            "font_weight": "600",
            "transition": "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)"
        },
        "input": {
            "border_radius": "12px",
            "border_width": "2px",
            "padding": "0.75rem 1rem",
            "transition": "all 0.3s ease"
        }
    },

    # Dashboard layout
    "dashboard": {
        "show_welcome_animation": True,
        "metric_cards_per_row": 4,
        "chart_height": 400,
        "enable_real_time_updates": True
    },

    # Feature flags for UI elements
    "features": {
        "glassmorphism": True,
        "dark_mode": True,
        "animations": True,
        "floating_action_button": True,
        "progress_animations": True,
        "hover_effects": True,
        "micro_interactions": True
    }
}

# Enhanced Activity Categories with Modern Design
ACTIVITY_CATEGORIES = {
    "Exercise": {
        "icon": "🏋️",
        "color": "#e53e3e",
        "gradient": "linear-gradient(135deg, #e53e3e 0%, #fc8181 100%)",
        "bg_color": "rgba(229, 62, 62, 0.1)",
        "border_color": "rgba(229, 62, 62, 0.3)",
        "description": "Physical fitness, sports, and movement activities",
        "suggested_duration": [30, 90],
        "examples": ["Morning Workout", "Gym Session", "Running", "Sports Practice", "Yoga"],
        "emoji_variations": ["💪", "🏃‍♂️", "🤸‍♀️", "⚽", "🏀"]
    },
    "Work": {
        "icon": "💻",
        "color": "#3182ce",
        "gradient": "linear-gradient(135deg, #3182ce 0%, #63b3ed 100%)",
        "bg_color": "rgba(49, 130, 206, 0.1)",
        "border_color": "rgba(49, 130, 206, 0.3)",
        "description": "Professional tasks, meetings, and career development",
        "suggested_duration": [60, 480],
        "examples": ["Deep Focus Work", "Team Meetings", "Project Development", "Email Management", "Client Calls"],
        "emoji_variations": ["💼", "📊", "🖥️", "📱", "⌨️"]
    },
    "Meal": {
        "icon": "🍽️",
        "color": "#38a169",
        "gradient": "linear-gradient(135deg, #38a169 0%, #68d391 100%)",
        "bg_color": "rgba(56, 161, 105, 0.1)",
        "border_color": "rgba(56, 161, 105, 0.3)",
        "description": "Eating, cooking, and nutrition-related activities",
        "suggested_duration": [15, 60],
        "examples": ["Breakfast", "Lunch", "Dinner", "Healthy Snack", "Meal Prep"],
        "emoji_variations": ["🥗", "🍳", "🥘", "🍎", "☕"]
    },
    "Break": {
        "icon": "☕",
        "color": "#d69e2e",
        "gradient": "linear-gradient(135deg, #d69e2e 0%, #f6e05e 100%)",
        "bg_color": "rgba(214, 158, 46, 0.1)",
        "border_color": "rgba(214, 158, 46, 0.3)",
        "description": "Short rest periods, micro-breaks, and refreshment",
        "suggested_duration": [5, 30],
        "examples": ["Coffee Break", "Stretch Break", "Fresh Air Walk", "Quick Meditation", "Social Chat"],
        "emoji_variations": ["⏸️", "🌱", "🧘‍♀️", "🚶‍♂️", "💭"]
    },
    "Study": {
        "icon": "📚",
        "color": "#805ad5",
        "gradient": "linear-gradient(135deg, #805ad5 0%, #b794f6 100%)",
        "bg_color": "rgba(128, 90, 213, 0.1)",
        "border_color": "rgba(128, 90, 213, 0.3)",
        "description": "Learning, education, and skill development",
        "suggested_duration": [30, 180],
        "examples": ["Reading", "Online Course", "Language Learning", "Skill Practice", "Research"],
        "emoji_variations": ["🎓", "📖", "✏️", "🧠", "💡"]
    },
    "Recovery": {
        "icon": "😴",
        "color": "#4a5568",
        "gradient": "linear-gradient(135deg, #4a5568 0%, #a0aec0 100%)",
        "bg_color": "rgba(74, 85, 104, 0.1)",
        "border_color": "rgba(74, 85, 104, 0.3)",
        "description": "Rest, relaxation, sleep, and wellness activities",
        "suggested_duration": [30, 480],
        "examples": ["Sleep", "Meditation", "Stretching", "Massage", "Bath Time"],
        "emoji_variations": ["🛁", "🧘", "💤", "🌙", "🕯️"]
    },
    "Other": {
        "icon": "📝",
        "color": "#718096",
        "gradient": "linear-gradient(135deg, #718096 0%, #cbd5e0 100%)",
        "bg_color": "rgba(113, 128, 150, 0.1)",
        "border_color": "rgba(113, 128, 150, 0.3)",
        "description": "Miscellaneous activities and personal tasks",
        "suggested_duration": [15, 120],
        "examples": ["Planning", "Organizing", "Commuting", "Personal Care", "Errands"],
        "emoji_variations": ["📋", "🗂️", "🚗", "🛒", "📱"]
    }
}

# Routine Types Configuration
ROUTINE_TYPES = {
    "Weekday": {
        "description": "Monday through Friday work routine",
        "icon": "📊",
        "color": "#3498db",
        "default_wake_time": "06:00",
        "default_sleep_time": "22:00",
        "typical_categories": ["Work", "Exercise", "Meal", "Break", "Study"]
    },
    "Weekend": {
        "description": "Saturday and Sunday relaxed routine",
        "icon": "🏖️",
        "color": "#27ae60",
        "default_wake_time": "07:00",
        "default_sleep_time": "23:00",
        "typical_categories": ["Recovery", "Exercise", "Meal", "Other", "Study"]
    },
    "Game Day": {
        "description": "Performance day routine for athletes",
        "icon": "⚽",
        "color": "#e74c3c",
        "default_wake_time": "07:00",
        "default_sleep_time": "21:00",
        "typical_categories": ["Exercise", "Meal", "Recovery", "Break"]
    },
    "Rest Day": {
        "description": "Complete rest and recovery day",
        "icon": "🛋️",
        "color": "#9b59b6",
        "default_wake_time": "08:00",
        "default_sleep_time": "22:30",
        "typical_categories": ["Recovery", "Meal", "Other", "Break"]
    },
    "Custom": {
        "description": "Fully customizable routine type",
        "icon": "🎨",
        "color": "#f39c12",
        "default_wake_time": "07:00",
        "default_sleep_time": "22:00",
        "typical_categories": list(ACTIVITY_CATEGORIES.keys())
    }
}

# Workout Types Configuration
WORKOUT_TYPES = {
    "Strength": {
        "description": "Resistance training and muscle building",
        "icon": "💪",
        "color": "#e74c3c",
        "typical_duration": [45, 90],
        "typical_intensity": [6, 9],
        "equipment_suggestions": ["Dumbbells", "Barbell", "Resistance Bands", "Bench"]
    },
    "Cardio": {
        "description": "Cardiovascular and endurance training",
        "icon": "🏃",
        "color": "#3498db",
        "typical_duration": [20, 60],
        "typical_intensity": [6, 8],
        "equipment_suggestions": ["None", "Treadmill", "Bike", "Jump Rope"]
    },
    "Flexibility": {
        "description": "Stretching and mobility work",
        "icon": "🧘",
        "color": "#27ae60",
        "typical_duration": [15, 45],
        "typical_intensity": [3, 6],
        "equipment_suggestions": ["Yoga Mat", "Resistance Bands", "Foam Roller"]
    },
    "Sports": {
        "description": "Sport-specific training and practice",
        "icon": "⚽",
        "color": "#f39c12",
        "typical_duration": [60, 120],
        "typical_intensity": [6, 9],
        "equipment_suggestions": ["Sport Equipment", "Cleats", "Ball", "Goals"]
    },
    "Mixed": {
        "description": "Combination of different training types",
        "icon": "🔄",
        "color": "#9b59b6",
        "typical_duration": [45, 90],
        "typical_intensity": [5, 8],
        "equipment_suggestions": ["Dumbbells", "Yoga Mat", "Resistance Bands"]
    }
}

# Meal Types Configuration
MEAL_TYPES = {
    "Breakfast": {
        "description": "Morning meal to start the day",
        "icon": "🌅",
        "typical_time": "07:30",
        "typical_calories": [300, 500],
        "macro_focus": "Balanced with good carbs"
    },
    "Lunch": {
        "description": "Midday meal for sustained energy",
        "icon": "🌞",
        "typical_time": "12:30",
        "typical_calories": [400, 700],
        "macro_focus": "Balanced macronutrients"
    },
    "Dinner": {
        "description": "Evening meal for recovery",
        "icon": "🌙",
        "typical_time": "18:30",
        "typical_calories": [500, 800],
        "macro_focus": "Higher protein for recovery"
    },
    "Snack": {
        "description": "Light meal between main meals",
        "icon": "🍎",
        "typical_time": "15:00",
        "typical_calories": [100, 300],
        "macro_focus": "Quick energy or protein"
    },
    "Pre-Workout": {
        "description": "Fuel before exercise",
        "icon": "⚡",
        "typical_time": "06:00",
        "typical_calories": [150, 300],
        "macro_focus": "Carbs for energy"
    },
    "Post-Workout": {
        "description": "Recovery nutrition after exercise",
        "icon": "🔋",
        "typical_time": "08:00",
        "typical_calories": [200, 400],
        "macro_focus": "Protein and carbs for recovery"
    }
}

# Default Time Slots
DEFAULT_TIME_SLOTS = {
    "early_morning": {"start": "05:00", "end": "08:00", "label": "Early Morning"},
    "morning": {"start": "08:00", "end": "12:00", "label": "Morning"},
    "afternoon": {"start": "12:00", "end": "17:00", "label": "Afternoon"},
    "evening": {"start": "17:00", "end": "21:00", "label": "Evening"},
    "night": {"start": "21:00", "end": "23:59", "label": "Night"}
}

# Analytics Configuration
ANALYTICS_CONFIG = {
    "default_period_days": 30,
    "streak_threshold": 0.8,  # 80% completion to count as successful day
    "efficiency_weights": {
        "Exercise": 1.0,
        "Work": 0.8,
        "Study": 0.9,
        "Meal": 0.6,
        "Recovery": 0.7,
        "Break": 0.4,
        "Other": 0.5
    },
    "target_completion_rate": 0.8,
    "show_trends": True,
    "show_predictions": False,
    "export_formats": ["CSV", "JSON", "PDF"],
    "chart_types": ["line", "bar", "pie", "heatmap"]
}

# Notification Settings
NOTIFICATION_CONFIG = {
    "enable_reminders": True,
    "reminder_advance_minutes": [5, 15, 30],
    "enable_streak_notifications": True,
    "enable_completion_celebrations": True,
    "daily_summary_time": "20:00",
    "weekly_review_day": "Sunday",
    "motivational_messages": True
}

# Data Validation Rules
VALIDATION_RULES = {
    "routine_name": {
        "min_length": 1,
        "max_length": 100,
        "required": True
    },
    "activity_name": {
        "min_length": 1,
        "max_length": 200,
        "required": True
    },
    "activity_duration": {
        "min_minutes": 1,
        "max_minutes": 1440,  # 24 hours
        "required": True
    },
    "workout_intensity": {
        "min_value": 1,
        "max_value": 10,
        "required": True
    },
    "meal_calories": {
        "min_value": 0,
        "max_value": 3000,
        "required": True
    },
    "macronutrients": {
        "min_value": 0,
        "max_protein": 500,
        "max_carbs": 1000,
        "max_fat": 300
    }
}

# Export Templates
EXPORT_TEMPLATES = {
    "daily_summary": {
        "name": "Daily Routine Summary",
        "fields": ["date", "routine_name", "completion_rate", "total_duration", "categories"],
        "format": "PDF"
    },
    "weekly_report": {
        "name": "Weekly Progress Report",
        "fields": ["week_dates", "daily_completion", "total_activities", "category_breakdown"],
        "format": "PDF"
    },
    "activity_log": {
        "name": "Activity Log",
        "fields": ["date", "time", "activity", "category", "completed", "duration"],
        "format": "CSV"
    }
}

# Sample Data Templates
SAMPLE_ROUTINES = {
    "productive_weekday": {
        "name": "Productive Weekday",
        "type": "Weekday",
        "activities": [
            {"start": "06:00", "end": "06:20", "activity": "Morning Routine", "category": "Recovery"},
            {"start": "06:30", "end": "07:30", "activity": "Workout", "category": "Exercise"},
            {"start": "07:30", "end": "08:00", "activity": "Breakfast", "category": "Meal"},
            {"start": "08:00", "end": "12:00", "activity": "Deep Work", "category": "Work"},
            {"start": "12:00", "end": "13:00", "activity": "Lunch & Break", "category": "Meal"},
            {"start": "13:00", "end": "17:00", "activity": "Focused Work", "category": "Work"},
            {"start": "17:30", "end": "18:30", "activity": "Learning Time", "category": "Study"},
            {"start": "18:30", "end": "19:30", "activity": "Dinner", "category": "Meal"},
            {"start": "19:30", "end": "21:00", "activity": "Personal Time", "category": "Recovery"},
            {"start": "21:00", "end": "22:00", "activity": "Wind Down", "category": "Recovery"}
        ]
    }
}

# Feature Flags
FEATURE_FLAGS = {
    "enable_analytics": True,
    "enable_export": True,
    "enable_templates": True,
    "enable_suggestions": True,
    "enable_time_tracking": True,
    "enable_goal_setting": False,
    "enable_team_features": False,
    "enable_ai_recommendations": False,
    "enable_calendar_sync": False,
    "enable_mobile_notifications": False,
    "beta_features": False
}

# Performance Settings
PERFORMANCE_CONFIG = {
    "cache_enabled": True,
    "cache_timeout": 300,  # 5 minutes
    "max_routines_in_memory": 100,
    "auto_cleanup_days": 90,
    "lazy_loading": True,
    "compression_enabled": False,
    "max_file_size_mb": 10
}

# Security Settings
SECURITY_CONFIG = {
    "enable_data_encryption": False,
    "backup_encryption": False,
    "session_security": True,
    "audit_logging": False,
    "data_retention_days": 365,
    "auto_logout_minutes": 60
}

# Localization Settings
LOCALIZATION = {
    "date_formats": {
        "en": "%Y-%m-%d",
        "eu": "%d/%m/%Y",
        "us": "%m/%d/%Y"
    },
    "time_formats": {
        "24h": "%H:%M",
        "12h": "%I:%M %p"
    },
    "number_formats": {
        "decimal_places": 1,
        "thousands_separator": ",",
        "decimal_separator": "."
    }
}


# Environment-specific settings
def get_config():
    """Get configuration based on environment"""
    env = os.getenv('ROUTINE_ENV', 'development')

    config = {
        'app': APP_CONFIG,
        'ui': UI_CONFIG,
        'categories': ACTIVITY_CATEGORIES,
        'routine_types': ROUTINE_TYPES,
        'workout_types': WORKOUT_TYPES,
        'meal_types': MEAL_TYPES,
        'analytics': ANALYTICS_CONFIG,
        'notifications': NOTIFICATION_CONFIG,
        'validation': VALIDATION_RULES,
        'features': FEATURE_FLAGS,
        'performance': PERFORMANCE_CONFIG,
        'security': SECURITY_CONFIG,
        'localization': LOCALIZATION
    }

    if env == 'production':
        # Production overrides
        config['performance']['cache_enabled'] = True
        config['security']['session_security'] = True
        config['app']['auto_save'] = True

    elif env == 'development':
        # Development overrides
        config['features']['beta_features'] = True
        config['app']['auto_save'] = True

    return config


# Utility functions
def get_category_config(category: str) -> Dict[str, Any]:
    """Get configuration for a specific category"""
    return ACTIVITY_CATEGORIES.get(category, ACTIVITY_CATEGORIES["Other"])


def get_routine_type_config(routine_type: str) -> Dict[str, Any]:
    """Get configuration for a specific routine type"""
    return ROUTINE_TYPES.get(routine_type, ROUTINE_TYPES["Custom"])


def is_feature_enabled(feature: str) -> bool:
    """Check if a feature is enabled"""
    return FEATURE_FLAGS.get(feature, False)


def get_validation_rule(field: str) -> Dict[str, Any]:
    """Get validation rules for a specific field"""
    return VALIDATION_RULES.get(field, {})


# Load configuration
CONFIG = get_config()
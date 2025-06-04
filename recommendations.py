import datetime
import streamlit as st
import pandas as pd
from typing import List, Dict, Tuple, Optional
from collections import defaultdict, Counter
import statistics
from dataclasses import asdict
from models import DailyRoutine, RoutineTask, WorkoutPlan, DietPlan, Meal, generate_id, dict_to_daily_routine, \
    dict_to_workout_plan, dict_to_diet_plan
from data_manager import get_data_manager


class SmartRecommendationsEngine:
    """Advanced AI-powered recommendations engine with 2025 industry standards"""

    def __init__(self):
        self.dm = get_data_manager()
        self.current_time = datetime.datetime.now()
        self.today = datetime.date.today()

        # AI Learning Parameters (simulating machine learning capabilities)
        self.learning_rate = 0.1
        self.confidence_threshold = 0.7
        self.adaptation_cycles = 3

        # Wellness insights cache
        self._wellness_profile = None
        self._circadian_analysis = None
        self._stress_indicators = None

    def generate_wellness_profile(self) -> Dict:
        """Generate comprehensive AI wellness profile like leading 2025 apps"""
        if self._wellness_profile:
            return self._wellness_profile

        routines_data = self.dm.load_routines()
        if not routines_data:
            return {}

        profile = {
            'energy_patterns': self._analyze_energy_patterns(routines_data),
            'stress_resilience': self._calculate_stress_resilience(routines_data),
            'consistency_score': self._measure_consistency(routines_data),
            'recovery_needs': self._assess_recovery_requirements(routines_data),
            'wellness_trajectory': self._predict_wellness_trajectory(routines_data),
            'risk_factors': self._identify_risk_factors(routines_data),
            'strengths': self._identify_strengths(routines_data)
        }

        self._wellness_profile = profile
        return profile

    def get_completion_patterns(self) -> Dict:
        """Analyze user completion patterns and preferences"""
        routines_data = self.dm.load_routines()
        if not routines_data:
            return {
                'best_categories': {},
                'best_times': {},
                'optimal_durations': {},
                'success_sequences': [],
                'completion_by_weekday': {},
                'total_completion_rate': 0
            }

        patterns = {
            'best_categories': defaultdict(list),
            'best_times': defaultdict(list),
            'optimal_durations': defaultdict(list),
            'success_sequences': [],
            'completion_by_weekday': defaultdict(list),
            'total_completion_rate': 0
        }

        total_tasks = 0
        completed_tasks = 0

        for routine_data in routines_data:
            routine_date = datetime.datetime.strptime(routine_data['date'], '%Y-%m-%d')
            weekday = routine_date.strftime('%A')

            for task in routine_data['tasks']:
                total_tasks += 1
                is_completed = task.get('completed', False)
                if is_completed:
                    completed_tasks += 1

                # Track completion by category
                patterns['best_categories'][task['category']].append(is_completed)

                # Track completion by time
                try:
                    hour = int(task['time'].split(':')[0])
                    time_period = self._get_time_period(hour)
                    patterns['best_times'][time_period].append(is_completed)
                except:
                    pass

                # Track optimal durations
                if is_completed:
                    patterns['optimal_durations'][task['category']].append(task['duration'])

                # Track completion by weekday
                patterns['completion_by_weekday'][weekday].append(is_completed)

        patterns['total_completion_rate'] = completed_tasks / total_tasks if total_tasks > 0 else 0

        # Convert defaultdict to regular dict to avoid issues
        return {
            'best_categories': dict(patterns['best_categories']),
            'best_times': dict(patterns['best_times']),
            'optimal_durations': dict(patterns['optimal_durations']),
            'success_sequences': patterns['success_sequences'],
            'completion_by_weekday': dict(patterns['completion_by_weekday']),
            'total_completion_rate': patterns['total_completion_rate']
        }

    def _analyze_energy_patterns(self, routines_data: List[Dict]) -> Dict:
        """Advanced circadian rhythm and energy analysis"""
        energy_data = defaultdict(list)

        for routine_data in routines_data:
            routine_date = datetime.datetime.strptime(routine_data['date'], '%Y-%m-%d')
            weekday = routine_date.strftime('%A')

            for task in routine_data['tasks']:
                try:
                    hour = int(task['time'].split(':')[0])
                    completion_energy = 1.0 if task.get('completed', False) else 0.3

                    # Weight by task importance and duration
                    energy_weight = task['duration'] / 60.0  # Convert to hours
                    if task['category'] in ['Work', 'Exercise']:
                        energy_weight *= 1.5  # High-demand activities

                    energy_data[hour].append(completion_energy * energy_weight)
                    energy_data[f"{weekday}_{hour}"].append(completion_energy)
                except:
                    continue

        # Calculate energy peaks and valleys
        hourly_energy = {}
        for hour in range(24):
            if hour in energy_data:
                hourly_energy[hour] = statistics.mean(energy_data[hour])
            else:
                hourly_energy[hour] = 0.5  # Neutral baseline

        peak_hours = sorted(hourly_energy.items(), key=lambda x: x[1], reverse=True)[:3]
        valley_hours = sorted(hourly_energy.items(), key=lambda x: x[1])[:3]

        return {
            'peak_energy_hours': [hour for hour, _ in peak_hours],
            'low_energy_hours': [hour for hour, _ in valley_hours],
            'energy_stability': statistics.stdev(hourly_energy.values()) if len(hourly_energy) > 1 else 0,
            'circadian_type': self._determine_circadian_type(peak_hours, valley_hours),
            'weekday_patterns': self._analyze_weekday_energy(energy_data)
        }

    def _determine_circadian_type(self, peak_hours: List[Tuple], valley_hours: List[Tuple]) -> str:
        """Determine if user is morning person, night owl, etc."""
        avg_peak_hour = statistics.mean([hour for hour, _ in peak_hours])

        if avg_peak_hour <= 10:
            return "Morning Lark"
        elif avg_peak_hour >= 18:
            return "Night Owl"
        elif 10 < avg_peak_hour < 18:
            return "Mid-day Peak"
        else:
            return "Variable Pattern"

    def _analyze_weekday_energy(self, energy_data: Dict) -> Dict:
        """Analyze energy patterns by weekday"""
        weekday_patterns = {}

        for key, values in energy_data.items():
            # Convert key to string to handle both int and string keys safely
            key_str = str(key)
            if '_' in key_str:  # This identifies weekday_hour format like "Monday_6"
                try:
                    weekday, hour = key_str.split('_', 1)  # Split only on first underscore
                    if weekday not in weekday_patterns:
                        weekday_patterns[weekday] = []
                    weekday_patterns[weekday].extend(values)
                except ValueError:
                    # Skip keys that don't split properly
                    continue

        # Calculate average energy by weekday
        weekday_energy = {}
        for weekday, values in weekday_patterns.items():
            if values and len(values) > 0:
                weekday_energy[weekday] = statistics.mean(values)

        return weekday_energy

    def _calculate_stress_resilience(self, routines_data: List[Dict]) -> Dict:
        """Calculate stress resilience and recovery capacity"""
        stress_indicators = []
        recovery_activities = []

        for routine_data in routines_data:
            daily_stress = 0
            daily_recovery = 0
            total_tasks = len(routine_data['tasks'])
            completed_tasks = sum(1 for task in routine_data['tasks'] if task.get('completed', False))

            completion_rate = completed_tasks / total_tasks if total_tasks > 0 else 0

            for task in routine_data['tasks']:
                # Stress indicators
                if task['category'] == 'Work' and task['duration'] > 120:
                    daily_stress += 2
                elif any(word in task['name'].lower() for word in ['pain', 'relief', 'wrist']):
                    daily_stress += 1

                # Recovery activities
                if task['category'] in ['Personal', 'Evening'] or 'stretch' in task['name'].lower():
                    if task.get('completed', False):
                        daily_recovery += 1

            stress_indicators.append(daily_stress)
            recovery_activities.append(daily_recovery)

        avg_stress = statistics.mean(stress_indicators) if stress_indicators else 0
        avg_recovery = statistics.mean(recovery_activities) if recovery_activities else 0

        resilience_score = max(0, min(1, (avg_recovery - avg_stress + 3) / 6))

        return {
            'resilience_score': resilience_score,
            'stress_level': 'High' if avg_stress > 3 else 'Moderate' if avg_stress > 1 else 'Low',
            'recovery_capacity': 'Excellent' if avg_recovery > 3 else 'Good' if avg_recovery > 1 else 'Needs Improvement',
            'stress_recovery_ratio': avg_recovery / max(avg_stress, 1)
        }

    def _measure_consistency(self, routines_data: List[Dict]) -> Dict:
        """Measure consistency in routine execution"""
        if len(routines_data) < 3:
            return {'score': 0, 'trend': 'insufficient_data'}

        # Sort by date
        sorted_routines = sorted(routines_data, key=lambda x: x['date'])

        # Calculate daily completion rates
        completion_rates = []
        for routine_data in sorted_routines:
            completed = sum(1 for task in routine_data['tasks'] if task.get('completed', False))
            total = len(routine_data['tasks'])
            completion_rates.append(completed / total if total > 0 else 0)

        # Calculate consistency metrics
        avg_completion = statistics.mean(completion_rates)
        consistency_score = 1 - (statistics.stdev(completion_rates) if len(completion_rates) > 1 else 0)

        # Determine trend
        if len(completion_rates) >= 5:
            recent_avg = statistics.mean(completion_rates[-3:])
            earlier_avg = statistics.mean(completion_rates[-6:-3]) if len(completion_rates) >= 6 else statistics.mean(
                completion_rates[:-3])

            if recent_avg > earlier_avg + 0.1:
                trend = 'improving'
            elif recent_avg < earlier_avg - 0.1:
                trend = 'declining'
            else:
                trend = 'stable'
        else:
            trend = 'establishing'

        return {
            'score': consistency_score,
            'average_completion': avg_completion,
            'trend': trend,
            'variation': statistics.stdev(completion_rates) if len(completion_rates) > 1 else 0
        }

    def _assess_recovery_requirements(self, routines_data: List[Dict]) -> Dict:
        """Assess recovery needs based on activity patterns"""
        high_intensity_days = 0
        recovery_activities = 0
        total_exercise_duration = 0
        total_days = len(routines_data)

        for routine_data in routines_data:
            daily_exercise_duration = 0
            daily_recovery = 0

            for task in routine_data['tasks']:
                if task['category'] == 'Exercise':
                    daily_exercise_duration += task['duration']
                    if task.get('completed', False):
                        total_exercise_duration += task['duration']

                # Count recovery activities
                if any(word in task['name'].lower() for word in
                       ['stretch', 'recovery', 'rest', 'massage', 'relaxation']):
                    if task.get('completed', False):
                        daily_recovery += 1

            if daily_exercise_duration > 60:  # High intensity day
                high_intensity_days += 1

            recovery_activities += daily_recovery

        avg_exercise_per_day = total_exercise_duration / total_days if total_days > 0 else 0
        recovery_ratio = recovery_activities / max(high_intensity_days, 1)

        # Determine recovery needs
        if avg_exercise_per_day > 90 and recovery_ratio < 0.5:
            recovery_need = 'critical'
        elif avg_exercise_per_day > 60 and recovery_ratio < 0.8:
            recovery_need = 'high'
        elif avg_exercise_per_day > 30 and recovery_ratio < 1.0:
            recovery_need = 'moderate'
        else:
            recovery_need = 'adequate'

        return {
            'need_level': recovery_need,
            'avg_exercise_duration': avg_exercise_per_day,
            'recovery_ratio': recovery_ratio,
            'high_intensity_days': high_intensity_days,
            'recommendation': self._get_recovery_recommendation(recovery_need)
        }

    def _get_recovery_recommendation(self, recovery_need: str) -> str:
        """Get recovery recommendation based on need level"""
        recommendations = {
            'critical': 'Schedule mandatory rest days and add daily stretching sessions',
            'high': 'Increase recovery activities and consider lighter workout days',
            'moderate': 'Add post-workout stretching and one dedicated recovery day per week',
            'adequate': 'Maintain current recovery routine'
        }
        return recommendations.get(recovery_need, 'Monitor recovery needs')

    def _predict_wellness_trajectory(self, routines_data: List[Dict]) -> Dict:
        """Predictive modeling for wellness trends"""
        if len(routines_data) < 5:
            return {'prediction': 'Insufficient data', 'confidence': 0}

        # Analyze recent trends
        recent_data = sorted(routines_data, key=lambda x: x['date'])[-7:]  # Last week
        completion_trends = []

        for routine_data in recent_data:
            completed = sum(1 for task in routine_data['tasks'] if task.get('completed', False))
            total = len(routine_data['tasks'])
            completion_trends.append(completed / total if total > 0 else 0)

        # Simple trend analysis
        if len(completion_trends) >= 3:
            recent_trend = completion_trends[-3:]
            avg_recent = statistics.mean(recent_trend)
            trend_direction = 'improving' if completion_trends[-1] > completion_trends[0] else 'declining'

            # Calculate momentum
            momentum = (completion_trends[-1] - completion_trends[0]) / len(completion_trends)

            prediction = {
                'current_performance': avg_recent,
                'trend_direction': trend_direction,
                'momentum': momentum,
                'confidence': min(0.9, len(completion_trends) / 10),
                'predicted_next_week': max(0, min(1, avg_recent + momentum)),
                'recommendations_urgency': 'high' if avg_recent < 0.6 else 'medium' if avg_recent < 0.8 else 'low'
            }
        else:
            prediction = {'prediction': 'Building baseline', 'confidence': 0.3}

        return prediction

    def _identify_risk_factors(self, routines_data: List[Dict]) -> List[str]:
        """Identify potential wellness risk factors"""
        risk_factors = []

        # Analyze patterns for risk indicators
        pain_frequency = 0
        overwork_days = 0
        poor_completion_days = 0
        total_days = len(routines_data)

        for routine_data in routines_data:
            work_duration = 0
            completed_tasks = 0
            total_tasks = len(routine_data['tasks'])

            for task in routine_data['tasks']:
                if task['category'] == 'Work':
                    work_duration += task['duration']

                if any(word in task['name'].lower() for word in ['pain', 'relief', 'wrist']):
                    pain_frequency += 1

                if task.get('completed', False):
                    completed_tasks += 1

            if work_duration > 480:  # More than 8 hours
                overwork_days += 1

            completion_rate = completed_tasks / total_tasks if total_tasks > 0 else 0
            if completion_rate < 0.5:
                poor_completion_days += 1

        # Evaluate risk factors
        if pain_frequency / total_days > 0.3:
            risk_factors.append("Chronic pain indicators detected")

        if overwork_days / total_days > 0.4:
            risk_factors.append("Excessive work hours pattern")

        if poor_completion_days / total_days > 0.3:
            risk_factors.append("Low routine adherence trend")

        # Check for lack of exercise
        exercise_days = sum(1 for routine_data in routines_data
                            if any(task['category'] == 'Exercise' and task.get('completed', False)
                                   for task in routine_data['tasks']))

        if exercise_days / total_days < 0.4:
            risk_factors.append("Insufficient physical activity")

        return risk_factors

    def _identify_strengths(self, routines_data: List[Dict]) -> List[str]:
        """Identify user's wellness strengths"""
        strengths = []

        # Analyze completion patterns - handle None case
        patterns = self.get_completion_patterns()

        # Ensure patterns is not None
        if not patterns:
            return ["Building healthy habits foundation"]

        if patterns.get('total_completion_rate', 0) > 0.8:
            strengths.append("Excellent routine adherence")

        # Check category performance
        category_performance = {}
        for category, completions in patterns.get('best_categories', {}).items():
            if completions:
                success_rate = sum(completions) / len(completions)
                category_performance[category] = success_rate

        for category, rate in category_performance.items():
            if rate > 0.85:
                strengths.append(f"Strong {category.lower()} routine consistency")

        # Check consistency
        consistency_data = self._measure_consistency(routines_data)
        if consistency_data.get('score', 0) > 0.8:
            strengths.append("Highly consistent daily patterns")

        # Check recovery balance
        recovery_data = self._assess_recovery_requirements(routines_data)
        if recovery_data.get('need_level') == 'adequate':
            strengths.append("Well-balanced activity and recovery")

        return strengths if strengths else ["Building healthy habits foundation"]

    def suggest_routine_optimizations(self) -> List[Dict]:
        """Suggest improvements to current routines based on patterns"""
        patterns = self.get_completion_patterns()
        suggestions = []

        if not patterns:
            def _assess_sleep_quality_proxy(self, routines_data: List[Dict]) -> float:

                """Estimate sleep quality based on evening routine completion"""
                recent_evenings = []

                cutoff_date = self.today - datetime.timedelta(days=3)

                for routine_data in routines_data:
                    routine_date = datetime.datetime.strptime(routine_data['date'], '%Y-%m-%d').date()
                    if routine_date >= cutoff_date:
                        evening_tasks = [task for task in routine_data['tasks'] if task['category'] == 'Evening']
                        if evening_tasks:
                            completed_evening = sum(1 for task in evening_tasks if task.get('completed', False))
                            total_evening = len(evening_tasks)
                            recent_evenings.append(completed_evening / total_evening)

                return statistics.mean(recent_evenings) if recent_evenings else 0.5

        # Analyze category performance
        category_success = {}
        for category, completions in patterns['best_categories'].items():
            if completions:
                success_rate = sum(completions) / len(completions)
                category_success[category] = success_rate

        # Suggest better categories
        if category_success:
            best_category = max(category_success, key=category_success.get)
            worst_category = min(category_success, key=category_success.get)

            if category_success[worst_category] < 0.6:
                suggestions.append({
                    'type': 'category_optimization',
                    'title': f'Reduce {worst_category} Tasks',
                    'description': f'You complete only {category_success[worst_category]:.0%} of {worst_category} tasks. Consider moving some to {best_category} time slots.',
                    'action': f'Move {worst_category} tasks to {best_category} time periods',
                    'priority': 'high'
                })

        # Analyze time performance
        time_success = {}
        for time_period, completions in patterns['best_times'].items():
            if completions:
                success_rate = sum(completions) / len(completions)
                time_success[time_period] = success_rate

        if time_success:
            best_time = max(time_success, key=time_success.get)
            if time_success[best_time] > 0.8:
                suggestions.append({
                    'type': 'timing_optimization',
                    'title': f'Leverage Your {best_time} Productivity',
                    'description': f'You have {time_success[best_time]:.0%} completion rate during {best_time}. Schedule important tasks here.',
                    'action': f'Move critical tasks to {best_time}',
                    'priority': 'medium'
                })

        # Suggest optimal durations
        for category, durations in patterns['optimal_durations'].items():
            if durations and len(durations) > 3:
                avg_duration = statistics.mean(durations)
                suggestions.append({
                    'type': 'duration_optimization',
                    'title': f'Optimize {category} Duration',
                    'description': f'Your most successful {category} tasks average {avg_duration:.0f} minutes.',
                    'action': f'Set {category} tasks to ~{avg_duration:.0f} minutes',
                    'priority': 'low'
                })

        return suggestions

    def recommend_workouts(self) -> List[Dict]:
        """Smart workout recommendations based on recent activity and recovery"""
        workouts_data = self.dm.load_workouts()
        routines_data = self.dm.load_routines()

        if not workouts_data:
            return []

        recommendations = []

        # Analyze recent workout patterns
        recent_workouts = self._get_recent_workouts(routines_data, days=7)
        last_workout_date = self._get_last_workout_date(routines_data)

        # Calculate recovery time
        if last_workout_date:
            days_since_workout = (self.today - last_workout_date).days
        else:
            days_since_workout = 7  # Default if no recent workouts

        # Analyze workout history for muscle group balance
        muscle_group_frequency = self._analyze_muscle_group_usage(recent_workouts)

        # Get user's pain/recovery status (from wrist-focused routines)
        pain_level = self._assess_pain_level(routines_data)

        # Generate recommendations
        available_workouts = [dict_to_workout_plan(w) for w in workouts_data]

        for workout in available_workouts:
            score = self._score_workout_recommendation(
                workout, days_since_workout, muscle_group_frequency, pain_level
            )

            if score > 0.5:  # Only recommend workouts with decent scores
                reason = self._generate_workout_reason(
                    workout, days_since_workout, muscle_group_frequency, pain_level
                )

                recommendations.append({
                    'type': 'workout',
                    'workout': workout,
                    'score': score,
                    'reason': reason,
                    'best_time': self._suggest_workout_time(workout),
                    'priority': 'high' if score > 0.8 else 'medium' if score > 0.7 else 'low'
                })

        # Sort by score
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:3]  # Top 3 recommendations

    def _get_recent_workouts(self, routines_data: List[Dict], days: int = 7) -> List[str]:
        """Get recent workout activities from routines"""
        cutoff_date = self.today - datetime.timedelta(days=days)
        recent_workouts = []

        for routine_data in routines_data:
            routine_date = datetime.datetime.strptime(routine_data['date'], '%Y-%m-%d').date()
            if routine_date >= cutoff_date:
                for task in routine_data['tasks']:
                    if task['category'] == 'Exercise' and task.get('completed', False):
                        recent_workouts.append(task['name'])

        return recent_workouts

    def _get_last_workout_date(self, routines_data: List[Dict]) -> Optional[datetime.date]:
        """Get the date of the last completed workout"""
        last_workout = None

        for routine_data in routines_data:
            routine_date = datetime.datetime.strptime(routine_data['date'], '%Y-%m-%d').date()
            for task in routine_data['tasks']:
                if task['category'] == 'Exercise' and task.get('completed', False):
                    if last_workout is None or routine_date > last_workout:
                        last_workout = routine_date

        return last_workout

    def _analyze_muscle_group_usage(self, recent_workouts: List[str]) -> Dict[str, int]:
        """Analyze which muscle groups have been worked recently"""
        muscle_groups = defaultdict(int)

        # Simple keyword matching for muscle groups
        keywords = {
            'Chest': ['chest', 'push', 'press'],
            'Back': ['back', 'pull', 'row'],
            'Legs': ['leg', 'squat', 'lunge'],
            'Arms': ['arm', 'bicep', 'tricep'],
            'Core': ['core', 'abs', 'plank'],
            'Shoulders': ['shoulder', 'overhead'],
            'Cardio': ['cardio', 'run', 'bike'],
            'Wrists': ['wrist', 'relief', 'pain']
        }

        for workout_name in recent_workouts:
            workout_lower = workout_name.lower()
            for muscle_group, keys in keywords.items():
                if any(key in workout_lower for key in keys):
                    muscle_groups[muscle_group] += 1

        return dict(muscle_groups)

    def _assess_pain_level(self, routines_data: List[Dict]) -> str:
        """Assess current pain level based on recent routine patterns"""
        recent_pain_tasks = 0
        total_recent_tasks = 0

        # Look at last 3 days
        cutoff_date = self.today - datetime.timedelta(days=3)

        for routine_data in routines_data:
            routine_date = datetime.datetime.strptime(routine_data['date'], '%Y-%m-%d').date()
            if routine_date >= cutoff_date:
                for task in routine_data['tasks']:
                    total_recent_tasks += 1
                    task_name_lower = task['name'].lower()
                    if any(word in task_name_lower for word in ['pain', 'relief', 'wrist', 'stretch']):
                        recent_pain_tasks += 1

        if total_recent_tasks == 0:
            return 'unknown'

        pain_ratio = recent_pain_tasks / total_recent_tasks

        if pain_ratio > 0.3:
            return 'high'
        elif pain_ratio > 0.15:
            return 'moderate'
        else:
            return 'low'

    def _score_workout_recommendation(self, workout: WorkoutPlan, days_since_workout: int,
                                      muscle_groups: Dict[str, int], pain_level: str) -> float:
        """Score a workout recommendation based on multiple factors"""
        score = 0.5  # Base score

        # Recovery time factor
        if days_since_workout == 0:
            score *= 0.2  # Very low if worked out today
        elif days_since_workout == 1:
            score *= 0.4  # Low if worked out yesterday
        elif days_since_workout >= 2:
            score *= 1.0  # Good if 2+ days rest

        # Pain level adjustments
        if pain_level == 'high':
            if 'Wrists' in workout.target_muscle_groups or workout.difficulty == 'Beginner':
                score *= 1.3  # Prefer wrist-friendly or beginner workouts
            else:
                score *= 0.3  # Avoid intense workouts
        elif pain_level == 'moderate':
            if workout.difficulty == 'Advanced':
                score *= 0.7  # Slightly avoid advanced workouts

        # Muscle group balance
        workout_muscles = set(workout.target_muscle_groups)
        recently_worked = set(muscle_groups.keys())

        # Prefer workouts that target underworked muscle groups
        if workout_muscles.isdisjoint(recently_worked):
            score *= 1.4  # Boost for completely different muscle groups
        elif len(workout_muscles.intersection(recently_worked)) == 1:
            score *= 1.1  # Slight boost for mostly different muscle groups
        else:
            score *= 0.8  # Reduce for recently worked muscle groups

        # Duration considerations
        if workout.estimated_duration <= 30:
            score *= 1.2  # Prefer shorter workouts for consistency
        elif workout.estimated_duration > 60:
            score *= 0.9  # Slightly reduce for longer workouts

        return min(score, 1.0)  # Cap at 1.0

    def _generate_workout_reason(self, workout: WorkoutPlan, days_since_workout: int,
                                 muscle_groups: Dict[str, int], pain_level: str) -> str:
        """Generate human-readable reason for workout recommendation"""
        reasons = []

        if days_since_workout >= 2:
            reasons.append(f"{days_since_workout} days since last workout")

        if pain_level == 'high' and 'Wrists' in workout.target_muscle_groups:
            reasons.append("includes wrist-friendly exercises")

        workout_muscles = set(workout.target_muscle_groups)
        recently_worked = set(muscle_groups.keys())

        if workout_muscles.isdisjoint(recently_worked):
            reasons.append("targets fresh muscle groups")

        if workout.estimated_duration <= 30:
            reasons.append("quick and manageable duration")

        if workout.difficulty == 'Beginner' and pain_level in ['high', 'moderate']:
            reasons.append("gentle intensity for recovery")

        return f"Perfect because it {', '.join(reasons)}" if reasons else "Good fit for your routine"

    def _suggest_workout_time(self, workout: WorkoutPlan) -> str:
        """Suggest optimal time for workout based on patterns"""
        patterns = self.get_completion_patterns()

        if 'best_times' in patterns:
            # Find the time period with highest completion rate
            time_success = {}
            for time_period, completions in patterns['best_times'].items():
                if completions:
                    time_success[time_period] = sum(completions) / len(completions)

            if time_success:
                best_time_period = max(time_success, key=time_success.get)

                # Convert time period back to specific time
                time_mapping = {
                    "Early Morning": "06:30",
                    "Morning": "10:00",
                    "Afternoon": "14:00",
                    "Evening": "17:00",
                    "Night": "20:00"
                }

                return time_mapping.get(best_time_period, "06:30")

    def recommend_meals(self) -> List[Dict]:
        """Smart meal recommendations based on dietary patterns and nutrition goals"""
        diets_data = self.dm.load_diets()
        routines_data = self.dm.load_routines()

        if not diets_data:
            return []

        recommendations = []

        # Analyze recent meal patterns
        recent_meals = self._get_recent_meals(routines_data, days=7)
        nutritional_preferences = self._analyze_nutritional_patterns(diets_data)
        time_of_day = self._get_current_meal_time()

        # Get all available meals
        all_meals = []
        for diet_data in diets_data:
            diet = dict_to_diet_plan(diet_data)
            all_meals.extend(diet.meals)

        # Score and recommend meals
        for meal in all_meals:
            score = self._score_meal_recommendation(
                meal, recent_meals, nutritional_preferences, time_of_day
            )

            if score > 0.4:
                reason = self._generate_meal_reason(
                    meal, recent_meals, nutritional_preferences, time_of_day
                )

                recommendations.append({
                    'type': 'meal',
                    'meal': meal,
                    'score': score,
                    'reason': reason,
                    'meal_time': time_of_day,
                    'priority': 'high' if score > 0.8 else 'medium' if score > 0.6 else 'low'
                })

        # Sort by score and return top recommendations
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:4]

    def _get_recent_meals(self, routines_data: List[Dict], days: int = 7) -> List[str]:
        """Get recent meal activities from routines"""
        cutoff_date = self.today - datetime.timedelta(days=days)
        recent_meals = []

        for routine_data in routines_data:
            routine_date = datetime.datetime.strptime(routine_data['date'], '%Y-%m-%d').date()
            if routine_date >= cutoff_date:
                for task in routine_data['tasks']:
                    task_name_lower = task['name'].lower()
                    if any(word in task_name_lower for word in ['breakfast', 'lunch', 'dinner', 'meal']):
                        recent_meals.append(task['description'] or task['name'])

        return recent_meals

    def _analyze_nutritional_patterns(self, diets_data: List[Dict]) -> Dict:
        """Analyze user's nutritional preferences from existing diet plans"""
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        meal_count = 0

        ingredient_frequency = Counter()

        for diet_data in diets_data:
            for meal_data in diet_data['meals']:
                meal_count += 1
                total_calories += meal_data['calories']
                total_protein += meal_data['protein']
                total_carbs += meal_data['carbs']
                total_fat += meal_data['fat']

                # Count ingredient usage
                for ingredient in meal_data.get('ingredients', []):
                    ingredient_frequency[ingredient.lower()] += 1

        if meal_count == 0:
            return {}

        return {
            'avg_calories': total_calories / meal_count,
            'avg_protein': total_protein / meal_count,
            'avg_carbs': total_carbs / meal_count,
            'avg_fat': total_fat / meal_count,
            'favorite_ingredients': [ing for ing, count in ingredient_frequency.most_common(10)]
        }

    def _get_current_meal_time(self) -> str:
        """Determine what meal time it currently is"""
        hour = self.current_time.hour

        if 5 <= hour < 10:
            return "Breakfast"
        elif 11 <= hour < 15:
            return "Lunch"
        elif 17 <= hour < 21:
            return "Dinner"
        else:
            return "Snack"

    def _score_meal_recommendation(self, meal: Meal, recent_meals: List[str],
                                   preferences: Dict, meal_time: str) -> float:
        """Score a meal recommendation"""
        score = 0.5  # Base score

        # Check if meal was recently consumed
        meal_ingredients = [ing.lower() for ing in meal.ingredients]
        recent_ingredients = []
        for recent_meal in recent_meals:
            recent_ingredients.extend(recent_meal.lower().split())

        # Reduce score for recently consumed ingredients
        overlap = sum(1 for ing in meal_ingredients if any(ing in recent for recent in recent_ingredients))
        if overlap > 0:
            score *= (1 - (overlap * 0.2))  # Reduce by 20% per overlapping ingredient

        # Boost score for favorite ingredients
        if preferences and 'favorite_ingredients' in preferences:
            favorite_overlap = sum(1 for ing in meal_ingredients
                                   if ing in preferences['favorite_ingredients'])
            score *= (1 + (favorite_overlap * 0.1))  # Boost by 10% per favorite ingredient

        # Nutritional fit
        if preferences:
            calorie_diff = abs(meal.calories - preferences.get('avg_calories', meal.calories))
            if calorie_diff < 100:  # Within 100 calories of average
                score *= 1.2
            elif calorie_diff > 200:  # More than 200 calories off
                score *= 0.8

        # Time appropriateness (simple heuristic)
        meal_name_lower = meal.name.lower()
        if meal_time == "Breakfast" and any(
                word in meal_name_lower for word in ['breakfast', 'morning', 'oatmeal', 'yogurt']):
            score *= 1.3
        elif meal_time == "Lunch" and any(word in meal_name_lower for word in ['lunch', 'wrap', 'salad', 'soup']):
            score *= 1.3
        elif meal_time == "Dinner" and any(word in meal_name_lower for word in ['dinner', 'pasta', 'bowl', 'recovery']):
            score *= 1.3

        return min(score, 1.0)

    def _generate_meal_reason(self, meal: Meal, recent_meals: List[str],
                              preferences: Dict, meal_time: str) -> str:
        """Generate reason for meal recommendation"""
        reasons = []

        if preferences and 'favorite_ingredients' in preferences:
            meal_ingredients = [ing.lower() for ing in meal.ingredients]
            favorite_overlap = [ing for ing in meal_ingredients
                                if ing in preferences['favorite_ingredients']]
            if favorite_overlap:
                reasons.append(f"includes your favorites: {', '.join(favorite_overlap[:2])}")

        # Check nutritional fit
        if preferences:
            calorie_diff = abs(meal.calories - preferences.get('avg_calories', meal.calories))
            if calorie_diff < 50:
                reasons.append("perfect calorie match")

        # Check variety
        meal_ingredients = [ing.lower() for ing in meal.ingredients]
        recent_ingredients = []
        for recent_meal in recent_meals:
            recent_ingredients.extend(recent_meal.lower().split())

        unique_ingredients = [ing for ing in meal_ingredients
                              if not any(ing in recent for recent in recent_ingredients)]
        if len(unique_ingredients) >= 2:
            reasons.append("adds variety to your week")

        # Time appropriateness
        if meal_time.lower() in meal.name.lower():
            reasons.append(f"perfect for {meal_time.lower()}")

        return f"Great choice - {', '.join(reasons)}" if reasons else "Nutritious and balanced option"

    def suggest_optimal_scheduling(self) -> List[Dict]:
        """Suggest optimal task scheduling based on completion patterns"""
        patterns = self.get_completion_patterns()
        suggestions = []

        if not patterns or 'best_times' not in patterns:
            return suggestions

        # Analyze time-based performance
        time_performance = {}
        for time_period, completions in patterns['best_times'].items():
            if completions and len(completions) >= 3:  # Minimum data points
                success_rate = sum(completions) / len(completions)
                time_performance[time_period] = success_rate

        if not time_performance:
            return suggestions

        # Find peak performance times
        best_time = max(time_performance, key=time_performance.get)
        worst_time = min(time_performance, key=time_performance.get)

        if time_performance[best_time] - time_performance[worst_time] > 0.2:  # Significant difference
            suggestions.append({
                'type': 'schedule_optimization',
                'title': f'Maximize Your {best_time} Peak',
                'description': f'You perform {time_performance[best_time]:.0%} better during {best_time} vs {time_performance[worst_time]:.0%} during {worst_time}.',
                'action': f'Schedule important tasks during {best_time}',
                'time_slot': best_time,
                'improvement_potential': f"{(time_performance[best_time] - time_performance[worst_time]) * 100:.0f}%",
                'priority': 'high'
            })

        # Analyze weekday patterns
        if 'completion_by_weekday' in patterns:
            weekday_performance = {}
            for weekday, completions in patterns['completion_by_weekday'].items():
                if completions and len(completions) >= 2:
                    success_rate = sum(completions) / len(completions)
                    weekday_performance[weekday] = success_rate

            if weekday_performance:
                best_day = max(weekday_performance, key=weekday_performance.get)
                worst_day = min(weekday_performance, key=weekday_performance.get)

                if len(weekday_performance) > 3 and weekday_performance[best_day] - weekday_performance[
                    worst_day] > 0.15:
                    suggestions.append({
                        'type': 'weekly_optimization',
                        'title': f'Leverage Your {best_day} Energy',
                        'description': f'{best_day} is your most productive day ({weekday_performance[best_day]:.0%} completion vs {weekday_performance[worst_day]:.0%} on {worst_day}).',
                        'action': f'Schedule challenging tasks on {best_day}s',
                        'best_day': best_day,
                        'priority': 'medium'
                    })

        return suggestions

    def _get_time_period(self, hour: int) -> str:
        """Convert hour to time period"""
        if 5 <= hour < 9:
            return "Early Morning"
        elif 9 <= hour < 12:
            return "Morning"
        elif 12 <= hour < 17:
            return "Afternoon"
        elif 17 <= hour < 21:
            return "Evening"
        else:
            return "Night"
        """Advanced circadian rhythm and energy analysis"""
        energy_data = defaultdict(list)

        for routine_data in routines_data:
            routine_date = datetime.datetime.strptime(routine_data['date'], '%Y-%m-%d')
            weekday = routine_date.strftime('%A')

            for task in routine_data['tasks']:
                try:
                    hour = int(task['time'].split(':')[0])
                    completion_energy = 1.0 if task.get('completed', False) else 0.3

                    # Weight by task importance and duration
                    energy_weight = task['duration'] / 60.0  # Convert to hours
                    if task['category'] in ['Work', 'Exercise']:
                        energy_weight *= 1.5  # High-demand activities

                    energy_data[hour].append(completion_energy * energy_weight)
                    energy_data[f"{weekday}_{hour}"].append(completion_energy)
                except:
                    continue

        # Calculate energy peaks and valleys
        hourly_energy = {}
        for hour in range(24):
            if hour in energy_data:
                hourly_energy[hour] = statistics.mean(energy_data[hour])
            else:
                hourly_energy[hour] = 0.5  # Neutral baseline

        peak_hours = sorted(hourly_energy.items(), key=lambda x: x[1], reverse=True)[:3]
        valley_hours = sorted(hourly_energy.items(), key=lambda x: x[1])[:3]

        return {
            'peak_energy_hours': [hour for hour, _ in peak_hours],
            'low_energy_hours': [hour for hour, _ in valley_hours],
            'energy_stability': statistics.stdev(hourly_energy.values()) if len(hourly_energy) > 1 else 0,
            'circadian_type': self._determine_circadian_type(peak_hours, valley_hours),
            'weekday_patterns': self._analyze_weekday_energy(energy_data)
        }

    def _determine_circadian_type(self, peak_hours: List[Tuple], valley_hours: List[Tuple]) -> str:
        """Determine if user is morning person, night owl, etc."""
        avg_peak_hour = statistics.mean([hour for hour, _ in peak_hours])

        if avg_peak_hour <= 10:
            return "Morning Lark"
        elif avg_peak_hour >= 18:
            return "Night Owl"
        elif 10 < avg_peak_hour < 18:
            return "Mid-day Peak"
        else:
            return "Variable Pattern"

    def _calculate_stress_resilience(self, routines_data: List[Dict]) -> Dict:
        """Calculate stress resilience and recovery capacity"""
        stress_indicators = []
        recovery_activities = []

        for routine_data in routines_data:
            daily_stress = 0
            daily_recovery = 0
            total_tasks = len(routine_data['tasks'])
            completed_tasks = sum(1 for task in routine_data['tasks'] if task.get('completed', False))

            completion_rate = completed_tasks / total_tasks if total_tasks > 0 else 0

            for task in routine_data['tasks']:
                # Stress indicators
                if task['category'] == 'Work' and task['duration'] > 120:
                    daily_stress += 2
                elif any(word in task['name'].lower() for word in ['pain', 'relief', 'wrist']):
                    daily_stress += 1

                # Recovery activities
                if task['category'] in ['Personal', 'Evening'] or 'stretch' in task['name'].lower():
                    if task.get('completed', False):
                        daily_recovery += 1

            stress_indicators.append(daily_stress)
            recovery_activities.append(daily_recovery)

        avg_stress = statistics.mean(stress_indicators) if stress_indicators else 0
        avg_recovery = statistics.mean(recovery_activities) if recovery_activities else 0

        resilience_score = max(0, min(1, (avg_recovery - avg_stress + 3) / 6))

        return {
            'resilience_score': resilience_score,
            'stress_level': 'High' if avg_stress > 3 else 'Moderate' if avg_stress > 1 else 'Low',
            'recovery_capacity': 'Excellent' if avg_recovery > 3 else 'Good' if avg_recovery > 1 else 'Needs Improvement',
            'stress_recovery_ratio': avg_recovery / max(avg_stress, 1)
        }

    def _predict_wellness_trajectory(self, routines_data: List[Dict]) -> Dict:
        """Predictive modeling for wellness trends"""
        if len(routines_data) < 5:
            return {'prediction': 'Insufficient data', 'confidence': 0}

        # Analyze recent trends
        recent_data = sorted(routines_data, key=lambda x: x['date'])[-7:]  # Last week
        completion_trends = []

        for routine_data in recent_data:
            completed = sum(1 for task in routine_data['tasks'] if task.get('completed', False))
            total = len(routine_data['tasks'])
            completion_trends.append(completed / total if total > 0 else 0)

        # Simple trend analysis
        if len(completion_trends) >= 3:
            recent_trend = completion_trends[-3:]
            avg_recent = statistics.mean(recent_trend)
            trend_direction = 'improving' if completion_trends[-1] > completion_trends[0] else 'declining'

            # Calculate momentum
            momentum = (completion_trends[-1] - completion_trends[0]) / len(completion_trends)

            prediction = {
                'current_performance': avg_recent,
                'trend_direction': trend_direction,
                'momentum': momentum,
                'confidence': min(0.9, len(completion_trends) / 10),
                'predicted_next_week': max(0, min(1, avg_recent + momentum)),
                'recommendations_urgency': 'high' if avg_recent < 0.6 else 'medium' if avg_recent < 0.8 else 'low'
            }
        else:
            prediction = {'prediction': 'Building baseline', 'confidence': 0.3}

        return prediction

    def generate_proactive_interventions(self) -> List[Dict]:
        """Generate proactive wellness interventions based on AI analysis"""
        profile = self.generate_wellness_profile()
        interventions = []

        if not profile:
            return interventions

        # Energy optimization interventions
        if 'energy_patterns' in profile:
            energy_data = profile['energy_patterns']

            if energy_data.get('energy_stability', 0) > 0.3:  # High variability
                interventions.append({
                    'type': 'energy_stabilization',
                    'title': '🔄 Stabilize Your Energy Patterns',
                    'description': f"Your energy varies significantly throughout the day. You're a {energy_data.get('circadian_type', 'Variable')} type.",
                    'action': f"Schedule demanding tasks during your peak hours: {', '.join(map(str, energy_data.get('peak_energy_hours', [])[:2]))}:00",
                    'ai_confidence': 0.85,
                    'expected_improvement': '15-25% better task completion',
                    'priority': 'high'
                })

        # Stress resilience interventions
        if 'stress_resilience' in profile:
            stress_data = profile['stress_resilience']

            if stress_data.get('resilience_score', 0.5) < 0.6:
                interventions.append({
                    'type': 'stress_management',
                    'title': '🧘 Enhance Stress Resilience',
                    'description': f"AI detected {stress_data.get('stress_level', 'moderate')} stress levels with {stress_data.get('recovery_capacity', 'limited')} recovery.",
                    'action': 'Add 15-minute mindfulness breaks between work sessions',
                    'ai_confidence': 0.78,
                    'expected_improvement': '30% improvement in completion rates',
                    'priority': 'high'
                })

        # Trajectory-based interventions
        if 'wellness_trajectory' in profile:
            trajectory = profile['wellness_trajectory']

            if trajectory.get('trend_direction') == 'declining':
                interventions.append({
                    'type': 'trajectory_correction',
                    'title': '📈 Reverse Declining Performance',
                    'description': f"AI predicts {trajectory.get('predicted_next_week', 0):.0%} completion rate next week if current pattern continues.",
                    'action': 'Simplify routines and focus on 3 core daily habits',
                    'ai_confidence': trajectory.get('confidence', 0.5),
                    'expected_improvement': 'Prevent 20% further decline',
                    'priority': 'urgent'
                })

        return sorted(interventions, key=lambda x: x['ai_confidence'], reverse=True)

    def get_real_time_coaching(self) -> Dict:
        """Provide real-time AI coaching like Whoop Coach"""
        current_hour = self.current_time.hour
        profile = self.generate_wellness_profile()

        if not profile:
            return {'message': 'Building your AI profile...', 'confidence': 0.3}

        energy_patterns = profile.get('energy_patterns', {})
        peak_hours = energy_patterns.get('peak_energy_hours', [])
        low_hours = energy_patterns.get('low_energy_hours', [])

        # Real-time recommendations based on current time
        if current_hour in peak_hours:
            coaching = {
                'status': 'peak_energy',
                'message': f"🔥 You're in your peak energy zone! Perfect time for high-focus work or challenging exercises.",
                'action': 'Tackle your most important task now',
                'confidence': 0.9,
                'energy_level': 'High',
                'recommended_activity': 'Deep work or intense workout'
            }
        elif current_hour in low_hours:
            coaching = {
                'status': 'low_energy',
                'message': f"💤 Natural low-energy period detected. Consider lighter activities or a strategic break.",
                'action': 'Schedule recovery activities or easy tasks',
                'confidence': 0.85,
                'energy_level': 'Low',
                'recommended_activity': 'Stretching, meal prep, or administrative tasks'
            }
        else:
            coaching = {
                'status': 'moderate_energy',
                'message': f"⚡ Moderate energy period. Good for routine tasks and steady progress.",
                'action': 'Maintain current activity level',
                'confidence': 0.7,
                'energy_level': 'Moderate',
                'recommended_activity': 'Regular scheduled activities'
            }

        # Add stress-based adjustments
        stress_data = profile.get('stress_resilience', {})
        if stress_data.get('stress_level') == 'High':
            coaching['stress_alert'] = "⚠️ High stress detected. Consider adding a 5-minute breathing exercise."
            coaching['priority_adjustment'] = "Focus on stress-relief activities"

        return coaching

    def generate_adaptive_meal_timing(self) -> List[Dict]:
        """Generate AI-optimized meal timing based on circadian patterns"""
        profile = self.generate_wellness_profile()

        if not profile or 'energy_patterns' not in profile:
            return []

        energy_patterns = profile['energy_patterns']
        circadian_type = energy_patterns.get('circadian_type', 'Variable Pattern')

        meal_recommendations = []

        if circadian_type == "Morning Lark":
            meal_recommendations = [
                {
                    'meal_type': 'Breakfast',
                    'optimal_time': '06:30',
                    'reasoning': 'Early risers need substantial morning fuel',
                    'meal_size': 'Large',
                    'recommended_calories': 500,
                    'ai_confidence': 0.85
                },
                {
                    'meal_type': 'Lunch',
                    'optimal_time': '12:00',
                    'reasoning': 'Peak metabolism during mid-day',
                    'meal_size': 'Medium',
                    'recommended_calories': 400,
                    'ai_confidence': 0.8
                },
                {
                    'meal_type': 'Dinner',
                    'optimal_time': '18:00',
                    'reasoning': 'Earlier dinner for better sleep',
                    'meal_size': 'Medium',
                    'recommended_calories': 450,
                    'ai_confidence': 0.9
                }
            ]
        elif circadian_type == "Night Owl":
            meal_recommendations = [
                {
                    'meal_type': 'Breakfast',
                    'optimal_time': '08:30',
                    'reasoning': 'Later start aligns with delayed circadian rhythm',
                    'meal_size': 'Medium',
                    'recommended_calories': 350,
                    'ai_confidence': 0.8
                },
                {
                    'meal_type': 'Lunch',
                    'optimal_time': '13:30',
                    'reasoning': 'Shifted metabolism peak',
                    'meal_size': 'Large',
                    'recommended_calories': 550,
                    'ai_confidence': 0.85
                },
                {
                    'meal_type': 'Dinner',
                    'optimal_time': '19:30',
                    'reasoning': 'Later dinner works with night owl patterns',
                    'meal_size': 'Medium',
                    'recommended_calories': 400,
                    'ai_confidence': 0.8
                }
            ]

        return meal_recommendations

    def predict_workout_readiness(self) -> Dict:
        """Predict workout readiness like advanced fitness AI apps"""
        routines_data = self.dm.load_routines()

        if not routines_data:
            return {'readiness': 'unknown', 'confidence': 0}

        # Analyze recent workout patterns
        recent_workouts = self._get_recent_workouts(routines_data, days=3)
        last_workout_date = self._get_last_workout_date(routines_data)

        # Calculate recovery indicators
        days_since_workout = (self.today - last_workout_date).days if last_workout_date else 7
        pain_level = self._assess_pain_level(routines_data)

        # Assess sleep quality proxy (based on completion of evening routines)
        sleep_quality = self._assess_sleep_quality_proxy(routines_data)

        # Calculate readiness score
        readiness_factors = {
            'recovery_time': min(1.0, days_since_workout / 2),  # Optimal at 2+ days
            'pain_status': 1.0 if pain_level == 'low' else 0.5 if pain_level == 'moderate' else 0.2,
            'sleep_quality': sleep_quality,
            'consistency': len(recent_workouts) / 7 if len(recent_workouts) <= 7 else 0.8  # Don't overdo it
        }

        overall_readiness = statistics.mean(readiness_factors.values())

        # Generate recommendation
        if overall_readiness >= 0.8:
            recommendation = {
                'readiness': 'optimal',
                'message': '💪 Perfect workout conditions! Your body is ready for peak performance.',
                'suggested_intensity': 'High',
                'workout_type': 'Strength training or high-intensity workout'
            }
        elif overall_readiness >= 0.6:
            recommendation = {
                'readiness': 'good',
                'message': '⚡ Good workout readiness. Consider moderate-intensity activities.',
                'suggested_intensity': 'Moderate',
                'workout_type': 'Cardio or moderate strength training'
            }
        elif overall_readiness >= 0.4:
            recommendation = {
                'readiness': 'caution',
                'message': '⚠️ Body may need more recovery. Light activity recommended.',
                'suggested_intensity': 'Light',
                'workout_type': 'Yoga, stretching, or light walking'
            }
        else:
            recommendation = {
                'readiness': 'rest',
                'message': '😴 Your body needs rest and recovery today.',
                'suggested_intensity': 'Rest',
                'workout_type': 'Rest day or gentle stretching only'
            }

        recommendation.update({
            'confidence': min(0.9, len(routines_data) / 10),
            'factors': readiness_factors,
            'overall_score': overall_readiness
        })

        return recommendation

    def _assess_sleep_quality_proxy(self, routines_data: List[Dict]) -> float:
        """Estimate sleep quality based on evening routine completion"""
        recent_evenings = []

        cutoff_date = self.today - datetime.timedelta(days=3)

        for routine_data in routines_data:
            routine_date = datetime.datetime.strptime(routine_data['date'], '%Y-%m-%d').date()
            if routine_date >= cutoff_date:
                evening_tasks = [task for task in routine_data['tasks'] if task['category'] == 'Evening']
                if evening_tasks:
                    completed_evening = sum(1 for task in evening_tasks if task.get('completed', False))
                    total_evening = len(evening_tasks)
                    recent_evenings.append(completed_evening / total_evening)

        return statistics.mean(recent_evenings) if recent_evenings else 0.5
        """Analyze user completion patterns and preferences"""
        routines_data = self.dm.load_routines()
        if not routines_data:
            return {}

        patterns = {
            'best_categories': defaultdict(list),
            'best_times': defaultdict(list),
            'optimal_durations': defaultdict(list),
            'success_sequences': [],
            'completion_by_weekday': defaultdict(list),
            'total_completion_rate': 0
        }

        total_tasks = 0
        completed_tasks = 0

        for routine_data in routines_data:
            routine_date = datetime.datetime.strptime(routine_data['date'], '%Y-%m-%d')
            weekday = routine_date.strftime('%A')

            for task in routine_data['tasks']:
                total_tasks += 1
                is_completed = task.get('completed', False)
                if is_completed:
                    completed_tasks += 1

                # Track completion by category
                patterns['best_categories'][task['category']].append(is_completed)

                # Track completion by time
                try:
                    hour = int(task['time'].split(':')[0])
                    time_period = self._get_time_period(hour)
                    patterns['best_times'][time_period].append(is_completed)
                except:
                    pass

                # Track optimal durations
                if is_completed:
                    patterns['optimal_durations'][task['category']].append(task['duration'])

                # Track completion by weekday
                patterns['completion_by_weekday'][weekday].append(is_completed)

        patterns['total_completion_rate'] = completed_tasks / total_tasks if total_tasks > 0 else 0

        return patterns

    def _get_time_period(self, hour: int) -> str:
        """Convert hour to time period"""
        if 5 <= hour < 9:
            return "Early Morning"
        elif 9 <= hour < 12:
            return "Morning"
        elif 12 <= hour < 17:
            return "Afternoon"
        elif 17 <= hour < 21:
            return "Evening"
        else:
            return "Night"

    def suggest_routine_optimizations(self) -> List[Dict]:
        """Suggest improvements to current routines based on patterns"""
        patterns = self.get_completion_patterns()
        suggestions = []

        if not patterns:
            return suggestions

        # Analyze category performance
        category_success = {}
        for category, completions in patterns['best_categories'].items():
            if completions:
                success_rate = sum(completions) / len(completions)
                category_success[category] = success_rate

        # Suggest better categories
        if category_success:
            best_category = max(category_success, key=category_success.get)
            worst_category = min(category_success, key=category_success.get)

            if category_success[worst_category] < 0.6:
                suggestions.append({
                    'type': 'category_optimization',
                    'title': f'Reduce {worst_category} Tasks',
                    'description': f'You complete only {category_success[worst_category]:.0%} of {worst_category} tasks. Consider moving some to {best_category} time slots.',
                    'action': f'Move {worst_category} tasks to {best_category} time periods',
                    'priority': 'high'
                })

        # Analyze time performance
        time_success = {}
        for time_period, completions in patterns['best_times'].items():
            if completions:
                success_rate = sum(completions) / len(completions)
                time_success[time_period] = success_rate

        if time_success:
            best_time = max(time_success, key=time_success.get)
            if time_success[best_time] > 0.8:
                suggestions.append({
                    'type': 'timing_optimization',
                    'title': f'Leverage Your {best_time} Productivity',
                    'description': f'You have {time_success[best_time]:.0%} completion rate during {best_time}. Schedule important tasks here.',
                    'action': f'Move critical tasks to {best_time}',
                    'priority': 'medium'
                })

        # Suggest optimal durations
        for category, durations in patterns['optimal_durations'].items():
            if durations and len(durations) > 3:
                avg_duration = statistics.mean(durations)
                suggestions.append({
                    'type': 'duration_optimization',
                    'title': f'Optimize {category} Duration',
                    'description': f'Your most successful {category} tasks average {avg_duration:.0f} minutes.',
                    'action': f'Set {category} tasks to ~{avg_duration:.0f} minutes',
                    'priority': 'low'
                })

        return suggestions

    def recommend_workouts(self) -> List[Dict]:
        """Smart workout recommendations based on recent activity and recovery"""
        workouts_data = self.dm.load_workouts()
        routines_data = self.dm.load_routines()

        if not workouts_data:
            return []

        recommendations = []

        # Analyze recent workout patterns
        recent_workouts = self._get_recent_workouts(routines_data, days=7)
        last_workout_date = self._get_last_workout_date(routines_data)

        # Calculate recovery time
        if last_workout_date:
            days_since_workout = (self.today - last_workout_date).days
        else:
            days_since_workout = 7  # Default if no recent workouts

        # Analyze workout history for muscle group balance
        muscle_group_frequency = self._analyze_muscle_group_usage(recent_workouts)

        # Get user's pain/recovery status (from wrist-focused routines)
        pain_level = self._assess_pain_level(routines_data)

        # Generate recommendations
        available_workouts = [dict_to_workout_plan(w) for w in workouts_data]

        for workout in available_workouts:
            score = self._score_workout_recommendation(
                workout, days_since_workout, muscle_group_frequency, pain_level
            )

            if score > 0.5:  # Only recommend workouts with decent scores
                reason = self._generate_workout_reason(
                    workout, days_since_workout, muscle_group_frequency, pain_level
                )

                recommendations.append({
                    'type': 'workout',
                    'workout': workout,
                    'score': score,
                    'reason': reason,
                    'best_time': self._suggest_workout_time(workout),
                    'priority': 'high' if score > 0.8 else 'medium' if score > 0.7 else 'low'
                })

        # Sort by score
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:3]  # Top 3 recommendations

    def _get_recent_workouts(self, routines_data: List[Dict], days: int = 7) -> List[str]:
        """Get recent workout activities from routines"""
        cutoff_date = self.today - datetime.timedelta(days=days)
        recent_workouts = []

        for routine_data in routines_data:
            routine_date = datetime.datetime.strptime(routine_data['date'], '%Y-%m-%d').date()
            if routine_date >= cutoff_date:
                for task in routine_data['tasks']:
                    if task['category'] == 'Exercise' and task.get('completed', False):
                        recent_workouts.append(task['name'])

        return recent_workouts

    def _get_last_workout_date(self, routines_data: List[Dict]) -> Optional[datetime.date]:
        """Get the date of the last completed workout"""
        last_workout = None

        for routine_data in routines_data:
            routine_date = datetime.datetime.strptime(routine_data['date'], '%Y-%m-%d').date()
            for task in routine_data['tasks']:
                if task['category'] == 'Exercise' and task.get('completed', False):
                    if last_workout is None or routine_date > last_workout:
                        last_workout = routine_date

        return last_workout

    def _analyze_muscle_group_usage(self, recent_workouts: List[str]) -> Dict[str, int]:
        """Analyze which muscle groups have been worked recently"""
        muscle_groups = defaultdict(int)

        # Simple keyword matching for muscle groups
        keywords = {
            'Chest': ['chest', 'push', 'press'],
            'Back': ['back', 'pull', 'row'],
            'Legs': ['leg', 'squat', 'lunge'],
            'Arms': ['arm', 'bicep', 'tricep'],
            'Core': ['core', 'abs', 'plank'],
            'Shoulders': ['shoulder', 'overhead'],
            'Cardio': ['cardio', 'run', 'bike'],
            'Wrists': ['wrist', 'relief', 'pain']
        }

        for workout_name in recent_workouts:
            workout_lower = workout_name.lower()
            for muscle_group, keys in keywords.items():
                if any(key in workout_lower for key in keys):
                    muscle_groups[muscle_group] += 1

        return dict(muscle_groups)

    def _assess_pain_level(self, routines_data: List[Dict]) -> str:
        """Assess current pain level based on recent routine patterns"""
        recent_pain_tasks = 0
        total_recent_tasks = 0

        # Look at last 3 days
        cutoff_date = self.today - datetime.timedelta(days=3)

        for routine_data in routines_data:
            routine_date = datetime.datetime.strptime(routine_data['date'], '%Y-%m-%d').date()
            if routine_date >= cutoff_date:
                for task in routine_data['tasks']:
                    total_recent_tasks += 1
                    task_name_lower = task['name'].lower()
                    if any(word in task_name_lower for word in ['pain', 'relief', 'wrist', 'stretch']):
                        recent_pain_tasks += 1

        if total_recent_tasks == 0:
            return 'unknown'

        pain_ratio = recent_pain_tasks / total_recent_tasks

        if pain_ratio > 0.3:
            return 'high'
        elif pain_ratio > 0.15:
            return 'moderate'
        else:
            return 'low'

    def _score_workout_recommendation(self, workout: WorkoutPlan, days_since_workout: int,
                                      muscle_groups: Dict[str, int], pain_level: str) -> float:
        """Score a workout recommendation based on multiple factors"""
        score = 0.5  # Base score

        # Recovery time factor
        if days_since_workout == 0:
            score *= 0.2  # Very low if worked out today
        elif days_since_workout == 1:
            score *= 0.4  # Low if worked out yesterday
        elif days_since_workout >= 2:
            score *= 1.0  # Good if 2+ days rest

        # Pain level adjustments
        if pain_level == 'high':
            if 'Wrists' in workout.target_muscle_groups or workout.difficulty == 'Beginner':
                score *= 1.3  # Prefer wrist-friendly or beginner workouts
            else:
                score *= 0.3  # Avoid intense workouts
        elif pain_level == 'moderate':
            if workout.difficulty == 'Advanced':
                score *= 0.7  # Slightly avoid advanced workouts

        # Muscle group balance
        workout_muscles = set(workout.target_muscle_groups)
        recently_worked = set(muscle_groups.keys())

        # Prefer workouts that target underworked muscle groups
        if workout_muscles.isdisjoint(recently_worked):
            score *= 1.4  # Boost for completely different muscle groups
        elif len(workout_muscles.intersection(recently_worked)) == 1:
            score *= 1.1  # Slight boost for mostly different muscle groups
        else:
            score *= 0.8  # Reduce for recently worked muscle groups

        # Duration considerations
        if workout.estimated_duration <= 30:
            score *= 1.2  # Prefer shorter workouts for consistency
        elif workout.estimated_duration > 60:
            score *= 0.9  # Slightly reduce for longer workouts

        return min(score, 1.0)  # Cap at 1.0

    def _generate_workout_reason(self, workout: WorkoutPlan, days_since_workout: int,
                                 muscle_groups: Dict[str, int], pain_level: str) -> str:
        """Generate human-readable reason for workout recommendation"""
        reasons = []

        if days_since_workout >= 2:
            reasons.append(f"{days_since_workout} days since last workout")

        if pain_level == 'high' and 'Wrists' in workout.target_muscle_groups:
            reasons.append("includes wrist-friendly exercises")

        workout_muscles = set(workout.target_muscle_groups)
        recently_worked = set(muscle_groups.keys())

        if workout_muscles.isdisjoint(recently_worked):
            reasons.append("targets fresh muscle groups")

        if workout.estimated_duration <= 30:
            reasons.append("quick and manageable duration")

        if workout.difficulty == 'Beginner' and pain_level in ['high', 'moderate']:
            reasons.append("gentle intensity for recovery")

        return f"Perfect because it {', '.join(reasons)}" if reasons else "Good fit for your routine"

    def _suggest_workout_time(self, workout: WorkoutPlan) -> str:
        """Suggest optimal time for workout based on patterns"""
        patterns = self.get_completion_patterns()

        if 'best_times' in patterns:
            # Find the time period with highest completion rate
            time_success = {}
            for time_period, completions in patterns['best_times'].items():
                if completions:
                    time_success[time_period] = sum(completions) / len(completions)

            if time_success:
                best_time_period = max(time_success, key=time_success.get)

                # Convert time period back to specific time
                time_mapping = {
                    "Early Morning": "06:30",
                    "Morning": "10:00",
                    "Afternoon": "14:00",
                    "Evening": "17:00",
                    "Night": "20:00"
                }

                return time_mapping.get(best_time_period, "06:30")

        return "06:30"  # Default morning time

    def recommend_meals(self) -> List[Dict]:
        """Smart meal recommendations based on dietary patterns and nutrition goals"""
        diets_data = self.dm.load_diets()
        routines_data = self.dm.load_routines()

        if not diets_data:
            return []

        recommendations = []

        # Analyze recent meal patterns
        recent_meals = self._get_recent_meals(routines_data, days=7)
        nutritional_preferences = self._analyze_nutritional_patterns(diets_data)
        time_of_day = self._get_current_meal_time()

        # Get all available meals
        all_meals = []
        for diet_data in diets_data:
            diet = dict_to_diet_plan(diet_data)
            all_meals.extend(diet.meals)

        # Score and recommend meals
        for meal in all_meals:
            score = self._score_meal_recommendation(
                meal, recent_meals, nutritional_preferences, time_of_day
            )

            if score > 0.4:
                reason = self._generate_meal_reason(
                    meal, recent_meals, nutritional_preferences, time_of_day
                )

                recommendations.append({
                    'type': 'meal',
                    'meal': meal,
                    'score': score,
                    'reason': reason,
                    'meal_time': time_of_day,
                    'priority': 'high' if score > 0.8 else 'medium' if score > 0.6 else 'low'
                })

        # Sort by score and return top recommendations
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:4]

    def _get_recent_meals(self, routines_data: List[Dict], days: int = 7) -> List[str]:
        """Get recent meal activities from routines"""
        cutoff_date = self.today - datetime.timedelta(days=days)
        recent_meals = []

        for routine_data in routines_data:
            routine_date = datetime.datetime.strptime(routine_data['date'], '%Y-%m-%d').date()
            if routine_date >= cutoff_date:
                for task in routine_data['tasks']:
                    task_name_lower = task['name'].lower()
                    if any(word in task_name_lower for word in ['breakfast', 'lunch', 'dinner', 'meal']):
                        recent_meals.append(task['description'] or task['name'])

        return recent_meals

    def _analyze_nutritional_patterns(self, diets_data: List[Dict]) -> Dict:
        """Analyze user's nutritional preferences from existing diet plans"""
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        meal_count = 0

        ingredient_frequency = Counter()

        for diet_data in diets_data:
            for meal_data in diet_data['meals']:
                meal_count += 1
                total_calories += meal_data['calories']
                total_protein += meal_data['protein']
                total_carbs += meal_data['carbs']
                total_fat += meal_data['fat']

                # Count ingredient usage
                for ingredient in meal_data.get('ingredients', []):
                    ingredient_frequency[ingredient.lower()] += 1

        if meal_count == 0:
            return {}

        return {
            'avg_calories': total_calories / meal_count,
            'avg_protein': total_protein / meal_count,
            'avg_carbs': total_carbs / meal_count,
            'avg_fat': total_fat / meal_count,
            'favorite_ingredients': [ing for ing, count in ingredient_frequency.most_common(10)]
        }

    def _get_current_meal_time(self) -> str:
        """Determine what meal time it currently is"""
        hour = self.current_time.hour

        if 5 <= hour < 10:
            return "Breakfast"
        elif 11 <= hour < 15:
            return "Lunch"
        elif 17 <= hour < 21:
            return "Dinner"
        else:
            return "Snack"

    def _score_meal_recommendation(self, meal: Meal, recent_meals: List[str],
                                   preferences: Dict, meal_time: str) -> float:
        """Score a meal recommendation"""
        score = 0.5  # Base score

        # Check if meal was recently consumed
        meal_ingredients = [ing.lower() for ing in meal.ingredients]
        recent_ingredients = []
        for recent_meal in recent_meals:
            recent_ingredients.extend(recent_meal.lower().split())

        # Reduce score for recently consumed ingredients
        overlap = sum(1 for ing in meal_ingredients if any(ing in recent for recent in recent_ingredients))
        if overlap > 0:
            score *= (1 - (overlap * 0.2))  # Reduce by 20% per overlapping ingredient

        # Boost score for favorite ingredients
        if preferences and 'favorite_ingredients' in preferences:
            favorite_overlap = sum(1 for ing in meal_ingredients
                                   if ing in preferences['favorite_ingredients'])
            score *= (1 + (favorite_overlap * 0.1))  # Boost by 10% per favorite ingredient

        # Nutritional fit
        if preferences:
            calorie_diff = abs(meal.calories - preferences.get('avg_calories', meal.calories))
            if calorie_diff < 100:  # Within 100 calories of average
                score *= 1.2
            elif calorie_diff > 200:  # More than 200 calories off
                score *= 0.8

        # Time appropriateness (simple heuristic)
        meal_name_lower = meal.name.lower()
        if meal_time == "Breakfast" and any(
                word in meal_name_lower for word in ['breakfast', 'morning', 'oatmeal', 'yogurt']):
            score *= 1.3
        elif meal_time == "Lunch" and any(word in meal_name_lower for word in ['lunch', 'wrap', 'salad', 'soup']):
            score *= 1.3
        elif meal_time == "Dinner" and any(word in meal_name_lower for word in ['dinner', 'pasta', 'bowl', 'recovery']):
            score *= 1.3

        return min(score, 1.0)

    def _generate_meal_reason(self, meal: Meal, recent_meals: List[str],
                              preferences: Dict, meal_time: str) -> str:
        """Generate reason for meal recommendation"""
        reasons = []

        if preferences and 'favorite_ingredients' in preferences:
            meal_ingredients = [ing.lower() for ing in meal.ingredients]
            favorite_overlap = [ing for ing in meal_ingredients
                                if ing in preferences['favorite_ingredients']]
            if favorite_overlap:
                reasons.append(f"includes your favorites: {', '.join(favorite_overlap[:2])}")

        # Check nutritional fit
        if preferences:
            calorie_diff = abs(meal.calories - preferences.get('avg_calories', meal.calories))
            if calorie_diff < 50:
                reasons.append("perfect calorie match")

        # Check variety
        meal_ingredients = [ing.lower() for ing in meal.ingredients]
        recent_ingredients = []
        for recent_meal in recent_meals:
            recent_ingredients.extend(recent_meal.lower().split())

        unique_ingredients = [ing for ing in meal_ingredients
                              if not any(ing in recent for recent in recent_ingredients)]
        if len(unique_ingredients) >= 2:
            reasons.append("adds variety to your week")

        # Time appropriateness
        if meal_time.lower() in meal.name.lower():
            reasons.append(f"perfect for {meal_time.lower()}")

        return f"Great choice - {', '.join(reasons)}" if reasons else "Nutritious and balanced option"

    def suggest_optimal_scheduling(self) -> List[Dict]:
        """Suggest optimal task scheduling based on completion patterns"""
        patterns = self.get_completion_patterns()
        suggestions = []

        if not patterns or 'best_times' not in patterns:
            return suggestions

        # Analyze time-based performance
        time_performance = {}
        for time_period, completions in patterns['best_times'].items():
            if completions and len(completions) >= 3:  # Minimum data points
                success_rate = sum(completions) / len(completions)
                time_performance[time_period] = success_rate

        if not time_performance:
            return suggestions

        # Find peak performance times
        best_time = max(time_performance, key=time_performance.get)
        worst_time = min(time_performance, key=time_performance.get)

        if time_performance[best_time] - time_performance[worst_time] > 0.2:  # Significant difference
            suggestions.append({
                'type': 'schedule_optimization',
                'title': f'Maximize Your {best_time} Peak',
                'description': f'You perform {time_performance[best_time]:.0%} better during {best_time} vs {time_performance[worst_time]:.0%} during {worst_time}.',
                'action': f'Schedule important tasks during {best_time}',
                'time_slot': best_time,
                'improvement_potential': f"{(time_performance[best_time] - time_performance[worst_time]) * 100:.0f}%",
                'priority': 'high'
            })

        # Analyze weekday patterns
        if 'completion_by_weekday' in patterns:
            weekday_performance = {}
            for weekday, completions in patterns['completion_by_weekday'].items():
                if completions and len(completions) >= 2:
                    success_rate = sum(completions) / len(completions)
                    weekday_performance[weekday] = success_rate

            if weekday_performance:
                best_day = max(weekday_performance, key=weekday_performance.get)
                worst_day = min(weekday_performance, key=weekday_performance.get)

                if len(weekday_performance) > 3 and weekday_performance[best_day] - weekday_performance[
                    worst_day] > 0.15:
                    suggestions.append({
                        'type': 'weekly_optimization',
                        'title': f'Leverage Your {best_day} Energy',
                        'description': f'{best_day} is your most productive day ({weekday_performance[best_day]:.0%} completion vs {weekday_performance[worst_day]:.0%} on {worst_day}).',
                        'action': f'Schedule challenging tasks on {best_day}s',
                        'best_day': best_day,
                        'priority': 'medium'
                    })

        return suggestions


def render_recommendations_dashboard():
    """Render the advanced AI recommendations dashboard for 2025"""
    st.subheader("🤖 AI Wellness Coach")
    st.markdown("*Advanced AI insights powered by machine learning and behavioral analysis*")

    engine = SmartRecommendationsEngine()

    # Real-time AI coaching section
    st.markdown("### 🔮 Real-Time AI Coaching")
    real_time_coaching = engine.get_real_time_coaching()

    if real_time_coaching.get('confidence', 0) > 0.5:
        # Display coaching with confidence indicator
        confidence_color = "🟢" if real_time_coaching['confidence'] > 0.8 else "🟡" if real_time_coaching[
                                                                                         'confidence'] > 0.6 else "🟠"

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; margin: 1rem 0;">
            <h4 style="margin: 0; color: white;">🎯 Current Status: {real_time_coaching['status'].replace('_', ' ').title()}</h4>
            <p style="margin: 0.5rem 0; font-size: 1.1rem;">{real_time_coaching['message']}</p>
            <p style="margin: 0; opacity: 0.9;">
                <strong>Action:</strong> {real_time_coaching['action']}<br>
                <strong>Energy Level:</strong> {real_time_coaching['energy_level']} | 
                <strong>AI Confidence:</strong> {confidence_color} {real_time_coaching['confidence']:.0%}
            </p>
        </div>
        """, unsafe_allow_html=True)

        if 'stress_alert' in real_time_coaching:
            st.warning(f"**Stress Alert:** {real_time_coaching['stress_alert']}")

    # Workout readiness prediction
    st.markdown("### 💪 Workout Readiness AI")
    workout_readiness = engine.predict_workout_readiness()

    if workout_readiness.get('confidence', 0) > 0.5:
        readiness_colors = {
            'optimal': '#28a745',
            'good': '#17a2b8',
            'caution': '#ffc107',
            'rest': '#dc3545'
        }

        readiness_status = workout_readiness['readiness']
        color = readiness_colors.get(readiness_status, '#6c757d')

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"""
            <div style="border-left: 5px solid {color}; padding: 1rem; margin: 1rem 0; background: #f8f9fa;">
                <h5 style="margin: 0; color: {color};">Readiness: {readiness_status.title()}</h5>
                <p style="margin: 0.5rem 0;">{workout_readiness['message']}</p>
                <p style="margin: 0; font-size: 0.9rem;">
                    <strong>Recommended:</strong> {workout_readiness['workout_type']}<br>
                    <strong>Intensity:</strong> {workout_readiness['suggested_intensity']}
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            # Readiness score visualization
            import plotly.graph_objects as go

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=workout_readiness['overall_score'] * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Readiness Score"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': color},
                    'steps': [
                        {'range': [0, 40], 'color': "#dc3545"},
                        {'range': [40, 60], 'color': "#ffc107"},
                        {'range': [60, 80], 'color': "#17a2b8"},
                        {'range': [80, 100], 'color': "#28a745"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))

            fig.update_layout(height=200, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)

    # Advanced AI wellness profile
    st.markdown("### 🧬 AI Wellness Profile")
    wellness_profile = engine.generate_wellness_profile()

    if wellness_profile:
        # Energy patterns analysis
        if 'energy_patterns' in wellness_profile:
            energy_data = wellness_profile['energy_patterns']

            with st.expander("⚡ Advanced Energy Analysis", expanded=True):
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Circadian Type", energy_data.get('circadian_type', 'Unknown'))

                with col2:
                    stability = energy_data.get('energy_stability', 0)
                    stability_label = "Stable" if stability < 0.2 else "Variable" if stability < 0.4 else "Chaotic"
                    st.metric("Energy Stability", stability_label)

                with col3:
                    peak_hours = energy_data.get('peak_energy_hours', [])
                    peak_str = f"{peak_hours[0]}:00-{peak_hours[-1]}:00" if peak_hours else "Unknown"
                    st.metric("Peak Hours", peak_str)

                # Energy pattern visualization
                import plotly.express as px

                if peak_hours and len(peak_hours) >= 2:
                    hours = list(range(24))
                    # Simulate energy levels (in real app, this would be actual data)
                    energy_levels = []
                    for hour in hours:
                        if hour in peak_hours:
                            energy_levels.append(0.8 + (hash(str(hour)) % 20) / 100)
                        elif hour in energy_data.get('low_energy_hours', []):
                            energy_levels.append(0.2 + (hash(str(hour)) % 20) / 100)
                        else:
                            energy_levels.append(0.5 + (hash(str(hour)) % 30) / 100)

                    energy_df = pd.DataFrame({'Hour': hours, 'Energy Level': energy_levels})
                    fig = px.line(energy_df, x='Hour', y='Energy Level',
                                  title='Your Daily Energy Pattern',
                                  labels={'Hour': 'Hour of Day', 'Energy Level': 'Predicted Energy Level'})
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)

        # Stress resilience analysis
        if 'stress_resilience' in wellness_profile:
            stress_data = wellness_profile['stress_resilience']

            with st.expander("🧘 Stress Resilience Analysis", expanded=True):
                col1, col2, col3 = st.columns(3)

                with col1:
                    resilience_score = stress_data.get('resilience_score', 0)
                    st.metric("Resilience Score", f"{resilience_score:.2f}/1.0")

                with col2:
                    st.metric("Stress Level", stress_data.get('stress_level', 'Unknown'))

                with col3:
                    st.metric("Recovery Capacity", stress_data.get('recovery_capacity', 'Unknown'))

                # Stress recovery ratio
                ratio = stress_data.get('stress_recovery_ratio', 1)
                if ratio < 0.8:
                    st.warning("⚠️ Low stress-to-recovery ratio. Consider adding more recovery activities.")
                elif ratio > 1.2:
                    st.success("✅ Excellent stress management! You have good recovery habits.")
                else:
                    st.info("ℹ️ Balanced stress-recovery ratio. Maintain current habits.")

    # Proactive AI interventions
    st.markdown("### 🚀 Proactive AI Interventions")
    interventions = engine.generate_proactive_interventions()

    if interventions:
        for intervention in interventions:
            priority_colors = {
                'urgent': '#dc3545',
                'high': '#fd7e14',
                'medium': '#ffc107',
                'low': '#20c997'
            }

            priority = intervention.get('priority', 'medium')
            color = priority_colors.get(priority, '#6c757d')
            confidence = intervention.get('ai_confidence', 0.5)

            with st.expander(f"🎯 {intervention['title']} (AI Confidence: {confidence:.0%})",
                             expanded=priority in ['urgent', 'high']):
                st.markdown(f"""
                <div style="border-left: 5px solid {color}; padding: 1rem; background: #f8f9fa;">
                    <p><strong>AI Analysis:</strong> {intervention['description']}</p>
                    <p><strong>Recommended Action:</strong> {intervention['action']}</p>
                    <p><strong>Expected Improvement:</strong> {intervention.get('expected_improvement', 'Significant wellness gains')}</p>
                    <p style="font-size: 0.9rem; opacity: 0.8;">
                        Priority: {priority.title()} | Confidence: {confidence:.0%}
                    </p>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"Apply This Intervention", key=f"apply_intervention_{intervention['type']}",
                             type="primary"):
                    st.success("🤖 AI intervention noted! Integrate this into your next routine for optimal results.")
    else:
        st.info("🌱 AI is learning your patterns. Complete more routines to unlock advanced interventions!")

    # Adaptive meal timing
    st.markdown("### 🍽️ AI-Optimized Meal Timing")
    meal_timing = engine.generate_adaptive_meal_timing()

    if meal_timing:
        for meal_rec in meal_timing:
            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                st.write(f"**{meal_rec['meal_type']}** at {meal_rec['optimal_time']}")
                st.caption(meal_rec['reasoning'])

            with col2:
                st.metric("Size", meal_rec['meal_size'])

            with col3:
                st.metric("Calories", meal_rec['recommended_calories'])

        st.info("💡 These meal times are optimized for your circadian rhythm and energy patterns.")

    # Get traditional recommendations for comparison
    routine_suggestions = engine.suggest_routine_optimizations()
    workout_recommendations = engine.recommend_workouts()
    meal_recommendations = engine.recommend_meals()
    schedule_suggestions = engine.suggest_optimal_scheduling()

    # Render traditional recommendations in separate tabs
    if any([routine_suggestions, workout_recommendations, meal_recommendations, schedule_suggestions]):
        st.markdown("---")
        st.markdown("### 📋 Traditional Recommendations")

        tab1, tab2, tab3, tab4 = st.tabs(["🎯 Routine Tips", "💪 Smart Workouts", "🥗 Meal Ideas", "⏰ Optimal Timing"])

        with tab1:
            render_routine_recommendations(routine_suggestions)

        with tab2:
            render_workout_recommendations(workout_recommendations)

        with tab3:
            render_meal_recommendations(meal_recommendations)

        with tab4:
            render_schedule_recommendations(schedule_suggestions)


def render_routine_recommendations(suggestions: List[Dict]):
    """Render routine optimization suggestions"""
    if not suggestions:
        st.info("✨ No routine optimizations available yet. Complete more routines to unlock insights!")
        return

    for suggestion in suggestions:
        priority_color = {
            'high': '🔴',
            'medium': '🟡',
            'low': '🟢'
        }

        with st.expander(f"{priority_color.get(suggestion['priority'], '⚪')} {suggestion['title']}", expanded=True):
            st.write(suggestion['description'])

            col1, col2 = st.columns([3, 1])
            with col1:
                st.info(f"**Action:** {suggestion['action']}")
            with col2:
                if st.button(f"Apply Tip", key=f"apply_{suggestion['type']}", type="secondary"):
                    st.success("💡 Great! Apply this insight to your next routine.")


def render_workout_recommendations(recommendations: List[Dict]):
    """Render smart workout recommendations"""
    if not recommendations:
        st.info("💪 No workout recommendations yet. Complete some exercise routines to get personalized suggestions!")
        return

    for rec in recommendations:
        workout = rec['workout']

        with st.expander(f"💪 {workout.name} ({rec['priority'].upper()} priority) - Score: {rec['score']:.1f}",
                         expanded=True):
            col1, col2 = st.columns([2, 1])

            with col1:
                st.write(f"**Duration:** {workout.estimated_duration} minutes")
                st.write(f"**Difficulty:** {workout.difficulty}")
                st.write(f"**Target:** {', '.join(workout.target_muscle_groups)}")
                st.write(f"**Why recommended:** {rec['reason']}")
                st.write(f"**Best time:** {rec['best_time']}")

            with col2:
                # Quick exercise preview
                st.write("**Exercises Preview:**")
                for i, exercise in enumerate(workout.exercises[:3], 1):
                    st.write(f"{i}. {exercise.name}")
                if len(workout.exercises) > 3:
                    st.write(f"... +{len(workout.exercises) - 3} more")

            if st.button(f"Schedule This Workout", key=f"schedule_workout_{workout.id}", type="primary"):
                st.success(f"✅ {workout.name} scheduled for {rec['best_time']}!")


def render_meal_recommendations(recommendations: List[Dict]):
    """Render smart meal recommendations"""
    if not recommendations:
        st.info("🥗 No meal recommendations yet. Create some diet plans to get personalized meal suggestions!")
        return

    for rec in recommendations:
        meal = rec['meal']

        with st.expander(f"🥗 {meal.name} ({rec['meal_time']}) - Score: {rec['score']:.1f}", expanded=True):
            col1, col2 = st.columns([2, 1])

            with col1:
                st.write(f"**Why recommended:** {rec['reason']}")
                st.write(f"**Ingredients:** {', '.join(meal.ingredients[:4])}")
                if len(meal.ingredients) > 4:
                    st.write(f"... +{len(meal.ingredients) - 4} more ingredients")
                if meal.notes:
                    st.write(f"**Notes:** {meal.notes}")

            with col2:
                st.metric("Calories", f"{meal.calories}")
                col_p, col_c, col_f = st.columns(3)
                with col_p:
                    st.metric("Protein", f"{meal.protein}g")
                with col_c:
                    st.metric("Carbs", f"{meal.carbs}g")
                with col_f:
                    st.metric("Fat", f"{meal.fat}g")

            if st.button(f"Add to Today's Plan", key=f"add_meal_{meal.id}", type="primary"):
                st.success(f"✅ {meal.name} added to your meal plan!")


def render_schedule_recommendations(suggestions: List[Dict]):
    """Render optimal scheduling suggestions"""
    if not suggestions:
        st.info("⏰ No scheduling optimizations yet. Complete more routines to discover your optimal timing patterns!")
        return

    for suggestion in suggestions:
        priority_icon = {'high': '🔥', 'medium': '⚡', 'low': '💡'}

        with st.expander(f"{priority_icon.get(suggestion['priority'], '⚪')} {suggestion['title']}", expanded=True):
            st.write(suggestion['description'])

            if 'improvement_potential' in suggestion:
                st.success(f"**Potential improvement:** {suggestion['improvement_potential']} better completion rate")

            col1, col2 = st.columns([3, 1])
            with col1:
                st.info(f"**Recommended action:** {suggestion['action']}")
            with col2:
                if st.button(f"Optimize Schedule", key=f"optimize_{suggestion['type']}", type="secondary"):
                    st.success("📅 Apply this timing insight to your next routine!")


def get_recommendation_summary() -> Dict:
    """Get enhanced summary of available AI recommendations for dashboard"""
    engine = SmartRecommendationsEngine()

    # Get traditional recommendations
    routine_suggestions = engine.suggest_routine_optimizations()
    workout_recommendations = engine.recommend_workouts()
    meal_recommendations = engine.recommend_meals()
    schedule_suggestions = engine.suggest_optimal_scheduling()

    # Get advanced AI insights
    proactive_interventions = engine.generate_proactive_interventions()
    wellness_profile = engine.generate_wellness_profile()

    # Count high priority items
    high_priority_count = sum(1 for item in routine_suggestions + workout_recommendations + schedule_suggestions
                              if item.get('priority') == 'high')

    # Add urgent interventions
    urgent_interventions = sum(1 for intervention in proactive_interventions
                               if intervention.get('priority') == 'urgent')

    # Calculate AI confidence score
    ai_confidence = 0.5  # Default
    if wellness_profile:
        # Base confidence on amount of data available
        dm = get_data_manager()
        routines_count = len(dm.load_routines())
        ai_confidence = min(0.95, max(0.3, routines_count / 10))

    # Determine AI status
    if ai_confidence < 0.5:
        ai_status = "Learning"
    elif ai_confidence < 0.7:
        ai_status = "Analyzing"
    elif ai_confidence < 0.9:
        ai_status = "Optimizing"
    else:
        ai_status = "Mastered"

    return {
        'total': len(routine_suggestions) + len(workout_recommendations) + len(meal_recommendations) + len(
            schedule_suggestions) + len(proactive_interventions),
        'routine_tips': len(routine_suggestions),
        'workouts': len(workout_recommendations),
        'meals': len(meal_recommendations),
        'scheduling': len(schedule_suggestions),
        'ai_interventions': len(proactive_interventions),
        'high_priority': high_priority_count,
        'urgent_interventions': urgent_interventions,
        'ai_confidence': ai_confidence,
        'ai_status': ai_status,
        'has_wellness_profile': bool(wellness_profile),
        'profile_completeness': min(1.0, len(wellness_profile.keys()) / 7) if wellness_profile else 0
    }

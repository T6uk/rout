# routine_components.py - Ultra-Clean UI Components for Daily Routine Manager
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, time
from typing import Dict, List, Any, Optional
import pandas as pd
from routine_models import DailyRoutine, WorkoutPlan, MealPlan, RoutineEntry


def render_routine_card(routine: DailyRoutine, show_actions: bool = True):
    """Render ultra-clean routine card with minimal design"""

    # Calculate basic metrics
    completion_rate = routine.completion_rate * 100
    completed_count = len(routine.completed_entries)
    total_count = len(routine.entries)

    # Clean status display
    if completion_rate >= 80:
        st.success(f"Excellent: {completion_rate:.0f}% complete")
    elif completion_rate >= 60:
        st.info(f"Good progress: {completion_rate:.0f}% complete")
    elif completion_rate >= 40:
        st.warning(f"Making progress: {completion_rate:.0f}% complete")
    else:
        st.error(f"Getting started: {completion_rate:.0f}% complete")

    # Clean progress bar
    st.progress(completion_rate / 100)

    # Basic info in columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Progress", f"{completion_rate:.0f}%")
    with col2:
        st.metric("Tasks", f"{completed_count}/{total_count}")
    with col3:
        st.metric("Duration", f"{routine.total_duration_minutes}m")

    # Current/next activity
    current_activity = routine.current_activity
    next_activity = routine.next_activity

    if current_activity or next_activity:
        col1, col2 = st.columns(2)

        with col1:
            if current_activity:
                st.markdown("**Currently**")
                st.write(current_activity.activity)
                st.caption(f"{current_activity.time_range} • {current_activity.category}")
            else:
                st.markdown("**Currently**")
                st.write("Free time")

        with col2:
            if next_activity:
                st.markdown("**Up next**")
                st.write(next_activity.activity)
                st.caption(f"{next_activity.time_range} • {next_activity.category}")
            else:
                st.markdown("**Up next**")
                st.write("Day complete!")

    # Description
    if routine.description:
        st.markdown("**Notes**")
        st.info(routine.description)

    # Timeline
    if routine.entries:
        with st.expander(f"Timeline ({len(routine.entries)} activities)"):
            render_activity_timeline(routine.entries)

    # Simple actions
    if show_actions:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("Complete", key=f"complete_{routine.id}", use_container_width=True):
                show_task_completion_modal(routine)

        with col2:
            if st.button("Edit", key=f"edit_{routine.id}", use_container_width=True):
                st.info("Edit functionality coming soon")

        with col3:
            if st.button("Duplicate", key=f"dup_{routine.id}", use_container_width=True):
                duplicate_routine(routine)

        with col4:
            if st.button("Details", key=f"stats_{routine.id}", use_container_width=True):
                show_routine_stats(routine)


def render_activity_timeline(entries: List[RoutineEntry]):
    """Render ultra-clean activity timeline"""

    if not entries:
        st.info("No activities scheduled yet.")
        return

    # Sort by time
    sorted_entries = sorted(entries, key=lambda x: x.start_time)

    # Clean timeline display
    for i, entry in enumerate(sorted_entries):
        col1, col2, col3, col4 = st.columns([1, 3, 2, 1])

        with col1:
            # Simple completion toggle
            status_key = f"toggle_{entry.id}_{i}"
            completed = st.checkbox("", value=entry.completed, key=status_key, label_visibility="collapsed")

            if completed != entry.completed:
                entry.completed = completed
                st.rerun()

        with col2:
            # Activity name
            if entry.completed:
                st.markdown(f"~~{entry.activity}~~")
            else:
                st.markdown(f"**{entry.activity}**")

            if entry.notes:
                st.caption(entry.notes)

        with col3:
            # Time and category
            st.markdown(f"{entry.time_range}")
            st.caption(entry.category)

        with col4:
            # Duration
            st.markdown(f"{entry.duration_minutes}m")

    # Simple summary
    st.markdown("---")
    total_duration = sum(entry.duration_minutes for entry in sorted_entries)
    completed_duration = sum(entry.duration_minutes for entry in sorted_entries if entry.completed)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Activities", len(sorted_entries))
    with col2:
        st.metric("Total Time", f"{total_duration}m")
    with col3:
        st.metric("Completed Time", f"{completed_duration}m")


def render_progress_tracker(routines: List[DailyRoutine], days: int = 7):
    """Render clean progress tracker"""
    if not routines:
        st.info("No routine data available for progress tracking.")
        return

    # Get recent routines
    recent_routines = sorted(routines, key=lambda x: x.date, reverse=True)[:days]
    recent_routines.reverse()

    # Simple progress data
    progress_data = []
    for routine in recent_routines:
        progress_data.append({
            'Date': datetime.fromisoformat(routine.date).strftime('%m/%d'),
            'Day': datetime.fromisoformat(routine.date).strftime('%a'),
            'Completion': routine.completion_rate * 100
        })

    if progress_data:
        df = pd.DataFrame(progress_data)

        # Clean line chart
        fig = px.line(df, x='Day', y='Completion', title=f"Last {days} Days")
        fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        # Simple summary
        avg_completion = df['Completion'].mean()
        st.metric("Average Completion", f"{avg_completion:.1f}%")


def render_quick_stats(routines: List[DailyRoutine]):
    """Render clean quick statistics"""
    if not routines:
        st.info("No data available yet.")
        return

    # Calculate basic stats
    total_routines = len(routines)
    avg_completion = sum(r.completion_rate for r in routines) / total_routines * 100

    # Current streak
    current_streak = 0
    sorted_routines = sorted(routines, key=lambda x: x.date, reverse=True)

    for routine in sorted_routines:
        if routine.completion_rate >= 0.8:
            current_streak += 1
        else:
            break

    # Total activities
    total_activities = sum(len(r.entries) for r in routines)
    completed_activities = sum(len(r.completed_entries) for r in routines)

    # Display clean metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Average", f"{avg_completion:.1f}%")

    with col2:
        st.metric("Streak", f"{current_streak} days")

    with col3:
        st.metric("Activities", f"{completed_activities}/{total_activities}")

    with col4:
        st.metric("Routines", total_routines)


def render_routine_form(edit_routine: Optional[DailyRoutine] = None):
    """Render clean routine creation form"""
    form_title = "Edit Routine" if edit_routine else "Create Routine"

    st.markdown(f"### {form_title}")

    with st.form("routine_form", clear_on_submit=not bool(edit_routine)):

        # Basic info
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input(
                "Name",
                value=edit_routine.name if edit_routine else "",
                placeholder="e.g., Monday Routine"
            )

            routine_date = st.date_input(
                "Date",
                value=datetime.fromisoformat(edit_routine.date).date() if edit_routine else datetime.now().date()
            )

        with col2:
            routine_type = st.selectbox(
                "Type",
                ["Weekday", "Weekend", "Game Day", "Rest Day", "Custom"],
                index=["Weekday", "Weekend", "Game Day", "Rest Day", "Custom"].index(
                    edit_routine.routine_type) if edit_routine else 0
            )

            description = st.text_area(
                "Description",
                value=edit_routine.description if edit_routine else "",
                placeholder="Optional description...",
                height=100
            )

        # Activities section
        st.markdown("#### Activities")

        # Initialize entries
        entries_key = f"edit_entries_{edit_routine.id}" if edit_routine else "new_entries"

        if entries_key not in st.session_state:
            if edit_routine:
                st.session_state[entries_key] = edit_routine.entries.copy()
            else:
                st.session_state[entries_key] = []

        # Show existing activities
        if st.session_state[entries_key]:
            for i, entry in enumerate(st.session_state[entries_key]):
                col1, col2, col3 = st.columns([3, 1, 1])

                with col1:
                    st.write(f"**{entry.activity}** ({entry.time_range})")
                    st.caption(f"{entry.category} • {entry.duration_minutes}m")

                with col2:
                    st.write(entry.category)

                with col3:
                    if st.button("Delete", key=f"delete_entry_{i}"):
                        st.session_state[entries_key].pop(i)
                        st.rerun()
        else:
            st.info("No activities added yet.")

        # Add new activity
        st.markdown("**Add Activity**")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            start_time = st.time_input("Start", value=time(9, 0), key="new_start_time")

        with col2:
            end_time = st.time_input("End", value=time(10, 0), key="new_end_time")

        with col3:
            activity = st.text_input("Activity", placeholder="e.g., Workout", key="new_activity")

        with col4:
            category = st.selectbox(
                "Category",
                ["Exercise", "Work", "Meal", "Break", "Study", "Recovery", "Other"],
                key="new_category"
            )

        # Add button
        add_entry = st.form_submit_button("Add Activity")

        if add_entry and activity:
            if end_time <= start_time:
                st.error("End time must be after start time.")
            else:
                new_entry = RoutineEntry(
                    start_time=start_time.strftime("%H:%M"),
                    end_time=end_time.strftime("%H:%M"),
                    activity=activity,
                    category=category
                )

                st.session_state[entries_key].append(new_entry)
                st.success(f"Added '{activity}'")
                st.rerun()

        # Submit
        submitted = st.form_submit_button("Save Routine", type="primary")

        if submitted and name and st.session_state[entries_key]:
            if edit_routine:
                # Update existing
                edit_routine.name = name
                edit_routine.date = routine_date.isoformat()
                edit_routine.routine_type = routine_type
                edit_routine.description = description
                edit_routine.entries = st.session_state[entries_key]
                edit_routine.updated_at = datetime.now().isoformat()

                # Update in session state
                for i, routine in enumerate(st.session_state.routines):
                    if routine.id == edit_routine.id:
                        st.session_state.routines[i] = edit_routine
                        break

                st.success("Routine updated!")
            else:
                # Create new
                new_routine = DailyRoutine(
                    name=name,
                    date=routine_date.isoformat(),
                    routine_type=routine_type,
                    description=description,
                    entries=st.session_state[entries_key]
                )

                st.session_state.routines.append(new_routine)
                st.success("Routine created!")

            # Clear and save
            del st.session_state[entries_key]
            from routine_storage import RoutineStorage
            storage = RoutineStorage()
            storage.save_routines(st.session_state.routines)
            st.rerun()

        elif submitted and not name:
            st.error("Please enter a name.")
        elif submitted and not st.session_state[entries_key]:
            st.error("Please add at least one activity.")


def render_workout_form():
    """Render clean workout form"""
    with st.form("workout_form", clear_on_submit=True):
        st.markdown("### Create Workout")

        # Basic info
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Name", placeholder="e.g., Morning Workout")
            workout_type = st.selectbox("Type", ["Strength", "Cardio", "Flexibility", "Sports", "Mixed"])
            duration = st.slider("Duration (min)", 15, 120, 45)

        with col2:
            intensity = st.slider("Intensity", 1, 10, 6)
            target_muscles = st.text_input("Target", placeholder="e.g., Full Body")
            equipment = st.multiselect("Equipment", ["None", "Dumbbells", "Resistance Bands", "Barbell"])

        # Exercises
        exercises_text = st.text_area(
            "Exercises (one per line)",
            placeholder="Push-ups\nSquats\nPlanks",
            height=100
        )

        # Instructions
        instructions = st.text_area(
            "Instructions",
            placeholder="Workout instructions...",
            height=80
        )

        # Submit
        submitted = st.form_submit_button("Create Workout", type="primary")

        if submitted and name:
            exercises_list = [ex.strip() for ex in exercises_text.split('\n') if ex.strip()]

            workout_plan = WorkoutPlan(
                name=name,
                workout_type=workout_type,
                duration=duration,
                intensity=intensity,
                target_muscle_groups=target_muscles,
                equipment=equipment,
                exercises=exercises_list,
                instructions=instructions
            )

            if 'workout_plans' not in st.session_state:
                st.session_state.workout_plans = []

            st.session_state.workout_plans.append(workout_plan)

            # Save
            from routine_storage import RoutineStorage
            storage = RoutineStorage()
            storage.save_workout_plans(st.session_state.workout_plans)

            st.success(f"Created '{name}'!")
            st.rerun()

        elif submitted and not name:
            st.error("Please enter a name.")


def render_meal_form():
    """Render clean meal form"""
    with st.form("meal_form", clear_on_submit=True):
        st.markdown("### Create Meal")

        # Basic info
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Name", placeholder="e.g., Protein Bowl")
            meal_type = st.selectbox("Type", ["Breakfast", "Lunch", "Dinner", "Snack", "Pre-Workout", "Post-Workout"])
            calories = st.number_input("Calories", min_value=0, value=400)

        with col2:
            servings = st.number_input("Servings", min_value=1, value=1)
            prep_time = st.number_input("Prep time (min)", min_value=0, value=10)
            cook_time = st.number_input("Cook time (min)", min_value=0, value=15)

        # Macros
        col1, col2, col3 = st.columns(3)

        with col1:
            protein = st.number_input("Protein (g)", min_value=0.0, value=25.0, step=0.5)

        with col2:
            carbs = st.number_input("Carbs (g)", min_value=0.0, value=40.0, step=0.5)

        with col3:
            fat = st.number_input("Fat (g)", min_value=0.0, value=15.0, step=0.5)

        # Ingredients
        ingredients_text = st.text_area(
            "Ingredients (one per line)",
            placeholder="2 cups oats\n1 banana\n1 scoop protein",
            height=100
        )

        # Instructions
        instructions = st.text_area(
            "Instructions",
            placeholder="Cooking instructions...",
            height=80
        )

        # Submit
        submitted = st.form_submit_button("Create Meal", type="primary")

        if submitted and name:
            ingredients_list = [ing.strip() for ing in ingredients_text.split('\n') if ing.strip()]

            meal_plan = MealPlan(
                name=name,
                meal_type=meal_type,
                calories=calories,
                protein=protein,
                carbs=carbs,
                fat=fat,
                ingredients=ingredients_list,
                instructions=instructions,
                prep_time=prep_time,
                cook_time=cook_time,
                servings=servings
            )

            if 'meal_plans' not in st.session_state:
                st.session_state.meal_plans = []

            st.session_state.meal_plans.append(meal_plan)

            # Save
            from routine_storage import RoutineStorage
            storage = RoutineStorage()
            storage.save_meal_plans(st.session_state.meal_plans)

            st.success(f"Created '{name}'!")
            st.rerun()

        elif submitted and not name:
            st.error("Please enter a name.")


# Clean modal functions
def show_task_completion_modal(routine: DailyRoutine):
    """Show clean task completion"""
    st.markdown("### Complete Tasks")

    incomplete_entries = [e for e in routine.entries if not e.completed]
    if not incomplete_entries:
        st.success("All tasks completed!")
        return

    selected_activities = []
    for entry in incomplete_entries:
        if st.checkbox(f"{entry.activity} ({entry.time_range})", key=f"task_{entry.id}"):
            selected_activities.append(entry)

    if selected_activities and st.button("Mark Complete", type="primary"):
        for entry in selected_activities:
            entry.completed = True
        routine.updated_at = datetime.now().isoformat()
        st.success(f"Marked {len(selected_activities)} tasks complete!")


def duplicate_routine(routine: DailyRoutine):
    """Clean routine duplication"""
    new_routine = DailyRoutine(
        name=f"{routine.name} (Copy)",
        date=datetime.now().date().isoformat(),
        routine_type=routine.routine_type,
        description=routine.description,
        entries=[RoutineEntry(
            start_time=entry.start_time,
            end_time=entry.end_time,
            activity=entry.activity,
            category=entry.category,
            notes=entry.notes
        ) for entry in routine.entries]
    )

    if 'routines' not in st.session_state:
        st.session_state.routines = []

    st.session_state.routines.append(new_routine)

    # Save
    from routine_storage import RoutineStorage
    storage = RoutineStorage()
    storage.save_routines(st.session_state.routines)

    st.success(f"Duplicated '{routine.name}'!")


def show_routine_stats(routine: DailyRoutine):
    """Show clean routine statistics"""
    st.markdown(f"### Stats: {routine.name}")

    # Basic metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Completion", f"{routine.completion_rate:.1%}")
    with col2:
        completed_time = sum(e.duration_minutes for e in routine.completed_entries)
        st.metric("Completed", f"{completed_time}m")
    with col3:
        remaining_time = sum(e.duration_minutes for e in routine.pending_entries)
        st.metric("Remaining", f"{remaining_time}m")
    with col4:
        st.metric("Activities", len(routine.entries))

    # Category breakdown
    if routine.category_breakdown:
        categories = list(routine.category_breakdown.keys())
        counts = list(routine.category_breakdown.values())

        fig = px.pie(values=counts, names=categories, title="Categories")
        fig.update_layout(height=300, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)


def render_category_filter(routines: List[DailyRoutine]) -> List[str]:
    """Render clean category filter"""
    all_categories = set()
    for routine in routines:
        for entry in routine.entries:
            all_categories.add(entry.category)

    if not all_categories:
        return []

    selected_categories = st.multiselect(
        "Filter categories",
        options=sorted(all_categories),
        default=sorted(all_categories)
    )

    return selected_categories


def render_routine_calendar(routines: List[DailyRoutine]):
    """Render clean calendar view"""
    import calendar
    from datetime import datetime

    today = datetime.now()
    year = today.year
    month = today.month

    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]

    st.markdown(f"### {month_name} {year}")

    # Simple calendar grid
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    # Header
    cols = st.columns(7)
    for i, day in enumerate(days):
        with cols[i]:
            st.markdown(f"**{day}**")

    # Calendar rows
    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:
                    st.write("")
                else:
                    date_str = f"{year}-{month:02d}-{day:02d}"
                    routine = next((r for r in routines if r.date == date_str), None)

                    if routine:
                        completion = routine.completion_rate * 100
                        if completion >= 80:
                            st.success(f"{day}")
                        elif completion >= 50:
                            st.warning(f"{day}")
                        else:
                            st.error(f"{day}")
                        st.caption(f"{completion:.0f}%")
                    else:
                        st.write(f"{day}")


def render_activity_heatmap(routines: List[DailyRoutine]):
    """Render clean activity heatmap"""
    if not routines:
        st.info("No data for heatmap.")
        return

    st.markdown("### Activity Heatmap")

    # Simple heatmap data preparation
    activity_data = {}

    for routine in routines:
        date = datetime.fromisoformat(routine.date)
        day_of_week = date.strftime('%A')

        for entry in routine.entries:
            try:
                start_hour = int(entry.start_time.split(':')[0])
                if day_of_week not in activity_data:
                    activity_data[day_of_week] = {}
                if start_hour not in activity_data[day_of_week]:
                    activity_data[day_of_week][start_hour] = []
                activity_data[day_of_week][start_hour].append(1 if entry.completed else 0)
            except:
                continue

    # Create clean heatmap
    heatmap_data = []
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    hours = list(range(6, 23))

    for day in days:
        for hour in hours:
            if day in activity_data and hour in activity_data[day]:
                avg_completion = sum(activity_data[day][hour]) / len(activity_data[day][hour])
            else:
                avg_completion = 0

            heatmap_data.append({
                'Day': day[:3],
                'Hour': f"{hour:02d}:00",
                'Completion': avg_completion
            })

    if heatmap_data:
        df = pd.DataFrame(heatmap_data)
        pivot_df = df.pivot(index='Day', columns='Hour', values='Completion')

        fig = px.imshow(
            pivot_df,
            title="Activity Completion Heatmap",
            color_continuous_scale="RdYlGn"
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
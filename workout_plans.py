import streamlit as st
from dataclasses import asdict
from typing import List
from models import WorkoutPlan, Exercise, dict_to_workout_plan, generate_id
from data_manager import get_data_manager


def render_workout_plans_page():
    """Render the complete workout plans page"""
    st.title("💪 Workout Plans")

    tab1, tab2, tab3 = st.tabs(["View Plans", "Create Plan", "Manage Plans"])

    with tab1:
        render_view_workouts()

    with tab2:
        render_create_workout()

    with tab3:
        render_manage_workouts()


def render_view_workouts():
    """Render the view workout plans tab"""
    st.subheader("Your Workout Plans")
    dm = get_data_manager()
    workouts_data = dm.load_workouts()

    if workouts_data:
        # Filter and search options
        col1, col2, col3 = st.columns(3)
        with col1:
            difficulty_filter = st.selectbox("Filter by Difficulty", ["All", "Beginner", "Intermediate", "Advanced"])
        with col2:
            muscle_filter = st.selectbox("Filter by Muscle Group",
                                         ["All", "Chest", "Back", "Shoulders", "Arms", "Legs", "Core", "Cardio",
                                          "Wrists"])
        with col3:
            duration_filter = st.selectbox("Filter by Duration", ["All", "≤30 min", "31-60 min", ">60 min"])

        # Apply filters
        filtered_workouts = filter_workouts(workouts_data, difficulty_filter, muscle_filter, duration_filter)

        if filtered_workouts:
            for workout_data in filtered_workouts:
                workout = dict_to_workout_plan(workout_data)
                render_workout_card(workout)
        else:
            st.info("No workouts match your filter criteria.")
    else:
        st.info("No workout plans created yet! Go to 'Create Plan' tab to get started.")


def filter_workouts(workouts_data: List[dict], difficulty: str, muscle: str, duration: str) -> List[dict]:
    """Apply filters to workout data"""
    filtered = workouts_data

    if difficulty != "All":
        filtered = [w for w in filtered if w['difficulty'] == difficulty]

    if muscle != "All":
        filtered = [w for w in filtered if muscle in w['target_muscle_groups']]

    if duration != "All":
        if duration == "≤30 min":
            filtered = [w for w in filtered if w['estimated_duration'] <= 30]
        elif duration == "31-60 min":
            filtered = [w for w in filtered if 31 <= w['estimated_duration'] <= 60]
        elif duration == ">60 min":
            filtered = [w for w in filtered if w['estimated_duration'] > 60]

    return filtered


def render_workout_card(workout: WorkoutPlan):
    """Render a single workout plan card"""
    with st.expander(f"💪 {workout.name} ({workout.difficulty}) - {workout.estimated_duration} min"):
        # Workout overview
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Description:** {workout.description}")
            st.write(f"**Difficulty:** {workout.difficulty}")
        with col2:
            st.write(f"**Duration:** ~{workout.estimated_duration} minutes")
            st.write(f"**Target Muscles:** {', '.join(workout.target_muscle_groups)}")

        # Exercises table
        st.write("---")
        st.write("**🏋️ Exercises:**")

        for i, exercise in enumerate(workout.exercises, 1):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 2])
                with col1:
                    st.write(f"**{i}. {exercise.name}**")
                with col2:
                    st.write(f"Sets: {exercise.sets}")
                with col3:
                    st.write(f"Reps: {exercise.reps}")
                with col4:
                    st.write(f"Weight: {exercise.weight}")

                if exercise.notes:
                    st.write(f"   💡 *{exercise.notes}*")
                st.write("---")


def render_create_workout():
    """Render the create workout form"""
    st.subheader("Create New Workout Plan")
    dm = get_data_manager()

    with st.form("create_workout", clear_on_submit=True):
        # Basic workout info
        col1, col2 = st.columns(2)
        with col1:
            workout_name = st.text_input("Workout Name*", placeholder="e.g., Upper Body Strength")
            workout_difficulty = st.selectbox("Difficulty*", ["Beginner", "Intermediate", "Advanced"])
        with col2:
            workout_duration = st.number_input("Estimated Duration (minutes)*", min_value=15, max_value=180, value=60)
            muscle_groups = st.multiselect(
                "Target Muscle Groups*",
                ["Chest", "Back", "Shoulders", "Arms", "Legs", "Core", "Cardio", "Wrists"],
                default=["Chest"]
            )

        workout_desc = st.text_area("Description*", placeholder="Describe the purpose and focus of this workout...")

        # Exercises section
        st.write("---")
        st.write("**🏋️ Exercises**")
        num_exercises = st.number_input("Number of exercises", min_value=1, max_value=15, value=5)

        exercises = []
        for i in range(num_exercises):
            with st.container():
                st.write(f"**Exercise {i + 1}**")

                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                with col1:
                    ex_name = st.text_input("Exercise Name*", key=f"ex_name_{i}",
                                            placeholder="e.g., Push-ups")
                with col2:
                    ex_sets = st.number_input("Sets*", key=f"ex_sets_{i}", min_value=1, max_value=10, value=3)
                with col3:
                    ex_reps = st.text_input("Reps*", key=f"ex_reps_{i}",
                                            placeholder="e.g., 12 or 30 sec")
                with col4:
                    ex_weight = st.text_input("Weight", key=f"ex_weight_{i}",
                                              placeholder="e.g., 50kg or bodyweight")

                ex_notes = st.text_input("Exercise Notes", key=f"ex_notes_{i}",
                                         placeholder="Form cues, modifications, etc.")

                if ex_name and ex_reps:
                    exercises.append(Exercise(
                        id=generate_id(),
                        name=ex_name,
                        sets=ex_sets,
                        reps=ex_reps,
                        weight=ex_weight or "bodyweight",
                        notes=ex_notes
                    ))
                st.write("---")

        # Submit button
        submitted = st.form_submit_button("Create Workout Plan", type="primary")

        if submitted:
            if workout_name and workout_desc and muscle_groups and exercises:
                new_workout = WorkoutPlan(
                    id=generate_id(),
                    name=workout_name,
                    description=workout_desc,
                    exercises=exercises,
                    target_muscle_groups=muscle_groups,
                    difficulty=workout_difficulty,
                    estimated_duration=workout_duration
                )

                workouts_data = dm.load_workouts()
                workouts_data.append(asdict(new_workout))

                if dm.save_workouts(workouts_data):
                    st.success(f"✅ Workout plan '{workout_name}' created successfully!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Failed to save workout plan. Please try again.")
            else:
                st.error("⚠️ Please fill in all required fields and add at least one exercise.")


def render_manage_workouts():
    """Render the manage workouts tab"""
    st.subheader("Manage Workout Plans")
    dm = get_data_manager()
    workouts_data = dm.load_workouts()

    if not workouts_data:
        st.info("No workout plans to manage! Create some workout plans first.")
        return

    # Select workout to manage
    workout_options = {f"{w['name']} ({w['difficulty']}) - {w['estimated_duration']} min": w['id']
                       for w in workouts_data}
    selected_workout_name = st.selectbox("Select workout plan:", list(workout_options.keys()))

    if selected_workout_name:
        selected_workout_id = workout_options[selected_workout_name]
        workout_data = next(w for w in workouts_data if w['id'] == selected_workout_id)
        workout = dict_to_workout_plan(workout_data)

        # Show workout details
        st.write("---")
        st.write("**Workout Plan Details:**")

        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Name:** {workout.name}")
            st.write(f"**Difficulty:** {workout.difficulty}")
            st.write(f"**Duration:** {workout.estimated_duration} minutes")
        with col2:
            st.write(f"**Exercises:** {len(workout.exercises)} total")
            st.write(f"**Target Muscles:** {', '.join(workout.target_muscle_groups)}")

        st.write(f"**Description:** {workout.description}")

        # Quick exercise overview
        with st.expander("Quick Exercise Overview"):
            for i, exercise in enumerate(workout.exercises, 1):
                st.write(f"{i}. **{exercise.name}** - {exercise.sets} × {exercise.reps} @ {exercise.weight}")

        # Action buttons
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🗑️ Delete Workout", type="secondary"):
                if dm.delete_workout(selected_workout_id):
                    st.success("✅ Workout plan deleted successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to delete workout plan.")

        with col2:
            if st.button("📋 Duplicate Workout", type="secondary"):
                # Create a copy
                new_workout = WorkoutPlan(
                    id=generate_id(),
                    name=f"{workout.name} (Copy)",
                    description=workout.description,
                    exercises=[Exercise(
                        id=generate_id(),
                        name=ex.name,
                        sets=ex.sets,
                        reps=ex.reps,
                        weight=ex.weight,
                        notes=ex.notes
                    ) for ex in workout.exercises],
                    target_muscle_groups=workout.target_muscle_groups,
                    difficulty=workout.difficulty,
                    estimated_duration=workout.estimated_duration
                )

                workouts_data.append(asdict(new_workout))
                if dm.save_workouts(workouts_data):
                    st.success("✅ Workout plan duplicated successfully!")
                    st.rerun()

        with col3:
            if st.button("📊 Export Workout", type="secondary"):
                import json
                workout_json = json.dumps(asdict(workout), indent=2)
                st.download_button(
                    label="📥 Download JSON",
                    data=workout_json,
                    file_name=f"{workout.name.replace(' ', '_')}_workout.json",
                    mime="application/json"
                )


def get_workout_stats():
    """Get workout statistics for dashboard"""
    dm = get_data_manager()
    workouts_data = dm.load_workouts()

    if not workouts_data:
        return None

    total_workouts = len(workouts_data)
    difficulties = [w['difficulty'] for w in workouts_data]
    avg_duration = sum(w['estimated_duration'] for w in workouts_data) / total_workouts

    return {
        "total": total_workouts,
        "beginner": difficulties.count("Beginner"),
        "intermediate": difficulties.count("Intermediate"),
        "advanced": difficulties.count("Advanced"),
        "avg_duration": round(avg_duration, 1)
    }
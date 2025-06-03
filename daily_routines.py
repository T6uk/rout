import streamlit as st
import datetime
from dataclasses import asdict
from typing import List
from models import DailyRoutine, RoutineTask, dict_to_daily_routine, generate_id
from data_manager import get_data_manager


def render_daily_routines_page():
    """Render the complete daily routines page"""
    st.title("📅 Daily Routines")

    tab1, tab2, tab3 = st.tabs(["View Routines", "Create Routine", "Edit Routine"])

    with tab1:
        render_view_routines()

    with tab2:
        render_create_routine()

    with tab3:
        render_edit_routine()


def render_view_routines():
    """Render the view routines tab"""
    st.subheader("Your Routines")
    dm = get_data_manager()
    routines_data = dm.load_routines()

    if routines_data:
        # Sort routines by date
        routines_data.sort(key=lambda x: x['date'])

        for routine_data in routines_data:
            routine = dict_to_daily_routine(routine_data)
            with st.expander(f"{routine.name} - {routine.date}"):
                render_routine_details(routine, routines_data)
    else:
        st.info("No routines created yet! Go to 'Create Routine' tab to get started.")


def render_routine_details(routine: DailyRoutine, routines_data: List[dict]):
    """Render details for a single routine with completion tracking"""
    dm = get_data_manager()
    completed = sum(1 for task in routine.tasks if task.completed)
    total = len(routine.tasks)

    # Progress bar
    progress = completed / total if total > 0 else 0
    st.progress(progress)
    st.write(f"**Progress:** {completed}/{total} tasks completed ({progress:.1%})")

    # Tasks with completion checkboxes
    for i, task in enumerate(routine.tasks):
        col1, col2 = st.columns([1, 10])

        with col1:
            new_status = st.checkbox(
                "",
                value=task.completed,
                key=f"task_{routine.id}_{task.id}",
                help="Mark as completed"
            )

        with col2:
            status_icon = "✅" if task.completed else "⏳"
            st.write(f"{status_icon} **{task.time}** - {task.name} ({task.duration} min)")
            if task.description:
                st.write(f"   *{task.description}*")
            st.write(f"   📁 Category: {task.category}")

        # Update completion status if changed
        if new_status != task.completed:
            routine.tasks[i].completed = new_status
            # Update in storage
            for j, r in enumerate(routines_data):
                if r['id'] == routine.id:
                    routines_data[j] = asdict(routine)
                    dm.save_routines(routines_data)
                    st.rerun()
                    break

    # Notes section
    if routine.notes:
        st.write("---")
        st.write(f"**Notes:** {routine.notes}")


def render_create_routine():
    """Render the create routine form"""
    st.subheader("Create New Routine")
    dm = get_data_manager()

    with st.form("create_routine", clear_on_submit=True):
        # Basic routine info
        col1, col2 = st.columns(2)
        with col1:
            routine_name = st.text_input("Routine Name*", placeholder="e.g., Monday Routine")
        with col2:
            routine_date = st.date_input("Date*", value=datetime.date.today())

        routine_notes = st.text_area("Notes (optional)", placeholder="Any additional notes about this routine...")

        # Tasks section
        st.write("---")
        st.write("**📋 Tasks**")
        num_tasks = st.number_input("Number of tasks", min_value=1, max_value=20, value=5)

        tasks = []
        for i in range(num_tasks):
            with st.container():
                st.write(f"**Task {i + 1}**")

                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    task_name = st.text_input("Task Name*", key=f"task_name_{i}", placeholder="e.g., Morning Workout")
                with col2:
                    task_time = st.text_input("Time*", key=f"task_time_{i}", placeholder="09:00")
                with col3:
                    task_duration = st.number_input("Duration (min)*", key=f"task_duration_{i}", min_value=1, value=30)

                col4, col5 = st.columns(2)
                with col4:
                    task_desc = st.text_input("Description", key=f"task_desc_{i}", placeholder="Brief description...")
                with col5:
                    task_category = st.selectbox(
                        "Category*",
                        ["Morning", "Work", "Exercise", "Personal", "Evening"],
                        key=f"task_cat_{i}"
                    )

                if task_name and task_time:
                    tasks.append(RoutineTask(
                        id=generate_id(),
                        name=task_name,
                        description=task_desc,
                        time=task_time,
                        duration=task_duration,
                        category=task_category
                    ))
                st.write("---")

        # Submit button
        submitted = st.form_submit_button("Create Routine", type="primary")

        if submitted:
            if routine_name and tasks:
                new_routine = DailyRoutine(
                    id=generate_id(),
                    name=routine_name,
                    date=routine_date.isoformat(),
                    tasks=tasks,
                    notes=routine_notes
                )

                routines_data = dm.load_routines()
                routines_data.append(asdict(new_routine))

                if dm.save_routines(routines_data):
                    st.success(f"✅ Routine '{routine_name}' created successfully!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Failed to save routine. Please try again.")
            else:
                st.error("⚠️ Please fill in the routine name and at least one complete task.")


def render_edit_routine():
    """Render the edit routine tab"""
    st.subheader("Edit/Delete Routines")
    dm = get_data_manager()
    routines_data = dm.load_routines()

    if not routines_data:
        st.info("No routines to edit! Create some routines first.")
        return

    # Select routine to edit
    routine_options = {f"{r['name']} - {r['date']}": r['id'] for r in routines_data}
    selected_routine_name = st.selectbox("Select routine to edit/delete:", list(routine_options.keys()))

    if selected_routine_name:
        selected_routine_id = routine_options[selected_routine_name]
        routine_data = next(r for r in routines_data if r['id'] == selected_routine_id)
        routine = dict_to_daily_routine(routine_data)

        # Show routine details
        st.write("---")
        st.write("**Current Routine Details:**")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Name:** {routine.name}")
            st.write(f"**Date:** {routine.date}")
        with col2:
            completed_tasks = sum(1 for task in routine.tasks if task.completed)
            st.write(f"**Tasks:** {len(routine.tasks)} total")
            st.write(f"**Completed:** {completed_tasks}/{len(routine.tasks)}")

        if routine.notes:
            st.write(f"**Notes:** {routine.notes}")

        # Action buttons
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🗑️ Delete Routine", type="secondary"):
                if dm.delete_routine(selected_routine_id):
                    st.success("✅ Routine deleted successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to delete routine.")

        with col2:
            if st.button("🔄 Reset Completion", type="secondary"):
                # Reset all task completion status
                for task in routine.tasks:
                    task.completed = False

                # Update in storage
                for i, r in enumerate(routines_data):
                    if r['id'] == selected_routine_id:
                        routines_data[i] = asdict(routine)
                        if dm.save_routines(routines_data):
                            st.success("✅ All tasks marked as incomplete!")
                            st.rerun()
                        break

        with col3:
            if st.button("📋 Duplicate Routine", type="secondary"):
                # Create a copy with new date
                new_routine = DailyRoutine(
                    id=generate_id(),
                    name=f"{routine.name} (Copy)",
                    date=datetime.date.today().isoformat(),
                    tasks=[RoutineTask(
                        id=generate_id(),
                        name=task.name,
                        description=task.description,
                        time=task.time,
                        duration=task.duration,
                        category=task.category,
                        completed=False
                    ) for task in routine.tasks],
                    notes=routine.notes
                )

                routines_data.append(asdict(new_routine))
                if dm.save_routines(routines_data):
                    st.success("✅ Routine duplicated successfully!")
                    st.rerun()


def get_today_routine():
    """Get today's routine if it exists"""
    dm = get_data_manager()
    today = datetime.date.today().isoformat()
    routines_data = dm.load_routines()
    today_routine_data = next((r for r in routines_data if r['date'] == today), None)

    if today_routine_data:
        return dict_to_daily_routine(today_routine_data)
    return None
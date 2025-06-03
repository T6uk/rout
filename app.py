import streamlit as st
import datetime
import json
from data_manager import get_data_manager
from daily_routines import render_daily_routines_page, get_today_routine
from workout_plans import render_workout_plans_page, get_workout_stats
from diet_plans import render_diet_plans_page, get_diet_stats

# Configure Streamlit page
st.set_page_config(
    page_title="Personal Wellness Hub",
    page_icon="🏃‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)


def render_dashboard():
    """Render the main dashboard page"""
    st.title("📊 Wellness Dashboard")
    st.write(
        "Welcome to your Personal Wellness Hub! Track your daily routines, workouts, and nutrition all in one place.")

    dm = get_data_manager()
    stats = dm.get_stats()

    # Main metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📅 Daily Routines", stats["routines"], help="Total number of daily routines created")
    with col2:
        st.metric("💪 Workout Plans", stats["workouts"], help="Total number of workout plans")
    with col3:
        st.metric("🥗 Diet Plans", stats["diets"], help="Total number of diet plans")

    # Today's routine section
    st.write("---")
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📋 Today's Routine")
        today_routine = get_today_routine()

        if today_routine:
            completed_tasks = sum(1 for task in today_routine.tasks if task.completed)
            total_tasks = len(today_routine.tasks)
            progress = completed_tasks / total_tasks if total_tasks > 0 else 0

            # Progress visualization
            st.progress(progress)
            st.write(f"**{today_routine.name}** - {today_routine.date}")
            st.write(f"Progress: **{completed_tasks}/{total_tasks}** tasks completed ({progress:.1%})")

            # Show next few tasks
            st.write("**Upcoming tasks:**")
            current_time = datetime.datetime.now().strftime("%H:%M")
            upcoming_tasks = [task for task in today_routine.tasks
                              if not task.completed and task.time >= current_time][:3]

            if upcoming_tasks:
                for task in upcoming_tasks:
                    status_icon = "⏳"
                    st.write(f"{status_icon} **{task.time}** - {task.name} ({task.duration} min)")
            else:
                completed_today = [task for task in today_routine.tasks if task.completed]
                if len(completed_today) == len(today_routine.tasks):
                    st.success("🎉 All tasks completed for today! Great job!")
                else:
                    st.info("🌙 All remaining tasks are for later today.")
        else:
            st.info("📝 No routine set for today. Create one in the **Daily Routines** section!")
            if st.button("➕ Create Today's Routine"):
                st.switch_page("daily_routines")

    with col2:
        st.subheader("⚡ Quick Stats")

        # Workout stats
        workout_stats = get_workout_stats()
        if workout_stats:
            st.write("**💪 Workouts:**")
            st.write(f"• Total: {workout_stats['total']}")
            st.write(f"• Avg Duration: {workout_stats['avg_duration']} min")
            st.write(f"• Beginner: {workout_stats['beginner']}")
            st.write(f"• Intermediate: {workout_stats['intermediate']}")
            st.write(f"• Advanced: {workout_stats['advanced']}")

        # Diet stats
        diet_stats = get_diet_stats()
        if diet_stats:
            st.write("**🥗 Nutrition:**")
            st.write(f"• Total Plans: {diet_stats['total']}")
            st.write(f"• Avg Calories: {diet_stats['avg_calories']}")
            st.write(f"• Total Meals: {diet_stats['total_meals']}")

    # Recent activity section
    st.write("---")
    st.subheader("📈 Recent Activity")

    # Show recent routines
    routines_data = dm.load_routines()
    if routines_data:
        recent_routines = sorted(routines_data, key=lambda x: x['date'], reverse=True)[:5]

        col1, col2 = st.columns(2)
        with col1:
            st.write("**Recent Routines:**")
            for routine in recent_routines:
                completed = sum(1 for task in routine['tasks'] if task.get('completed', False))
                total = len(routine['tasks'])
                progress = completed / total if total > 0 else 0
                st.write(f"• {routine['name']} ({routine['date']}) - {progress:.0%} complete")

        with col2:
            # Show completion trend
            if len(recent_routines) > 1:
                st.write("**Completion Trend:**")
                completion_rates = []
                for routine in recent_routines:
                    completed = sum(1 for task in routine['tasks'] if task.get('completed', False))
                    total = len(routine['tasks'])
                    completion_rates.append(completed / total if total > 0 else 0)

                # Simple trend indicator
                recent_avg = sum(completion_rates[:3]) / min(3, len(completion_rates))
                if recent_avg > 0.8:
                    st.success("🔥 Excellent consistency!")
                elif recent_avg > 0.6:
                    st.info("📈 Good progress!")
                else:
                    st.warning("💪 Room for improvement!")

    # Quick actions
    st.write("---")
    st.subheader("🚀 Quick Actions")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📅 View Today's Routine", use_container_width=True):
            st.switch_page("daily_routines")
    with col2:
        if st.button("💪 Browse Workouts", use_container_width=True):
            st.switch_page("workout_plans")
    with col3:
        if st.button("🥗 Check Diet Plans", use_container_width=True):
            st.switch_page("diet_plans")
    with col4:
        if st.button("📤 Import/Export", use_container_width=True):
            st.switch_page("import_export")


def render_import_export():
    """Render the import/export page"""
    st.title("📤 Import/Export Data")
    st.write("Backup your data or import existing routines, workouts, and diet plans.")

    dm = get_data_manager()

    tab1, tab2 = st.tabs(["📤 Export Data", "📥 Import Data"])

    with tab1:
        render_export_section(dm)

    with tab2:
        render_import_section(dm)


def render_export_section(dm):
    """Render the export data section"""
    st.subheader("📤 Export Your Data")
    st.write("Download your data as JSON files for backup or sharing between devices.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("**📅 Daily Routines**")
        routines_count = len(dm.load_routines())
        st.write(f"Total routines: {routines_count}")

        if st.button("Export Routines", type="primary", use_container_width=True):
            if routines_count > 0:
                data = dm.export_data("routines")
                st.download_button(
                    label="📥 Download Routines JSON",
                    data=data,
                    file_name=f"daily_routines_{datetime.date.today()}.json",
                    mime="application/json",
                    use_container_width=True
                )
            else:
                st.warning("No routines to export!")

    with col2:
        st.write("**💪 Workout Plans**")
        workouts_count = len(dm.load_workouts())
        st.write(f"Total workouts: {workouts_count}")

        if st.button("Export Workouts", type="primary", use_container_width=True):
            if workouts_count > 0:
                data = dm.export_data("workouts")
                st.download_button(
                    label="📥 Download Workouts JSON",
                    data=data,
                    file_name=f"workout_plans_{datetime.date.today()}.json",
                    mime="application/json",
                    use_container_width=True
                )
            else:
                st.warning("No workout plans to export!")

    with col3:
        st.write("**🥗 Diet Plans**")
        diets_count = len(dm.load_diets())
        st.write(f"Total diet plans: {diets_count}")

        if st.button("Export Diet Plans", type="primary", use_container_width=True):
            if diets_count > 0:
                data = dm.export_data("diets")
                st.download_button(
                    label="📥 Download Diets JSON",
                    data=data,
                    file_name=f"diet_plans_{datetime.date.today()}.json",
                    mime="application/json",
                    use_container_width=True
                )
            else:
                st.warning("No diet plans to export!")

    # Export all data
    st.write("---")
    st.subheader("📦 Export All Data")

    if st.button("📤 Export Everything", type="primary"):
        all_data = {
            "routines": dm.load_routines(),
            "workouts": dm.load_workouts(),
            "diets": dm.load_diets(),
            "export_date": datetime.date.today().isoformat(),
            "app_version": "1.0"
        }

        all_data_json = json.dumps(all_data, indent=2)
        st.download_button(
            label="📥 Download Complete Backup",
            data=all_data_json,
            file_name=f"wellness_hub_backup_{datetime.date.today()}.json",
            mime="application/json"
        )


def render_import_section(dm):
    """Render the import data section"""
    st.subheader("📥 Import Data")
    st.write("Import data from JSON files to restore backups or add new content.")

    # File upload method
    st.write("**📁 Import from File**")

    data_type = st.selectbox(
        "Select data type to import:",
        ["routines", "workouts", "diets"],
        format_func=lambda x: {
            "routines": "📅 Daily Routines",
            "workouts": "💪 Workout Plans",
            "diets": "🥗 Diet Plans"
        }[x]
    )

    uploaded_file = st.file_uploader("Choose JSON file", type="json")

    if uploaded_file is not None:
        try:
            json_data = uploaded_file.read().decode("utf-8")

            # Preview data
            with st.expander("📋 Preview Import Data"):
                try:
                    preview_data = json.loads(json_data)
                    if isinstance(preview_data, list):
                        st.write(f"Found {len(preview_data)} items to import")
                        if preview_data:
                            st.json(preview_data[0])  # Show first item as sample
                    else:
                        st.write("Data structure:")
                        st.json(preview_data)
                except:
                    st.error("Invalid JSON format in file")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Import Data", type="primary"):
                    if dm.import_data(json_data, data_type):
                        st.success(f"✅ Successfully imported {data_type}!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Failed to import data. Please check the file format.")

            with col2:
                if st.button("➕ Append Data", type="secondary"):
                    # Load existing data, append new data, then save
                    try:
                        new_data = json.loads(json_data)
                        if data_type == "routines":
                            existing_data = dm.load_routines()
                            existing_data.extend(new_data)
                            success = dm.save_routines(existing_data)
                        elif data_type == "workouts":
                            existing_data = dm.load_workouts()
                            existing_data.extend(new_data)
                            success = dm.save_workouts(existing_data)
                        elif data_type == "diets":
                            existing_data = dm.load_diets()
                            existing_data.extend(new_data)
                            success = dm.save_diets(existing_data)

                        if success:
                            st.success(f"✅ Successfully appended {len(new_data)} new {data_type}!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to append data.")
                    except Exception as e:
                        st.error(f"❌ Error appending data: {str(e)}")

        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")

    # Manual import method
    st.write("---")
    st.write("**✍️ Manual Import**")
    st.write("Paste JSON data directly:")

    json_input = st.text_area("Paste JSON data here:", height=200, placeholder='[{"id": "...", "name": "...", ...}]')

    if st.button("📥 Import from Text"):
        if json_input.strip():
            if dm.import_data(json_input, data_type):
                st.success(f"✅ Successfully imported {data_type} from text!")
                st.rerun()
            else:
                st.error("❌ Failed to import data. Please check the JSON format.")
        else:
            st.warning("⚠️ Please paste some JSON data first.")


def main():
    """Main application function"""
    # Sidebar navigation
    st.sidebar.title("🏃‍♂️ Personal Wellness Hub")
    st.sidebar.markdown("*Your complete wellness tracking solution*")

    # Navigation menu
    page = st.sidebar.selectbox(
        "Navigate to:",
        ["Dashboard", "Daily Routines", "Workout Plans", "Diet Plans", "Import/Export"],
        index=0
    )

    # Add some spacing and info in sidebar
    st.sidebar.markdown("---")

    # Quick stats in sidebar
    dm = get_data_manager()
    stats = dm.get_stats()

    st.sidebar.markdown("**📊 Quick Stats**")
    st.sidebar.markdown(f"📅 Routines: {stats['routines']}")
    st.sidebar.markdown(f"💪 Workouts: {stats['workouts']}")
    st.sidebar.markdown(f"🥗 Diet Plans: {stats['diets']}")

    # Today's progress in sidebar
    today_routine = get_today_routine()
    if today_routine:
        completed = sum(1 for task in today_routine.tasks if task.completed)
        total = len(today_routine.tasks)
        progress = completed / total if total > 0 else 0

        st.sidebar.markdown("---")
        st.sidebar.markdown("**📋 Today's Progress**")
        st.sidebar.progress(progress)
        st.sidebar.markdown(f"{completed}/{total} tasks ({progress:.0%})")

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Personal Wellness Hub v2.0**")
    st.sidebar.markdown("Built with ❤️ using Streamlit")
    st.sidebar.markdown("*Stay healthy, stay focused!* 💪")

    # Render selected page
    if page == "Dashboard":
        render_dashboard()
    elif page == "Daily Routines":
        render_daily_routines_page()
    elif page == "Workout Plans":
        render_workout_plans_page()
    elif page == "Diet Plans":
        render_diet_plans_page()
    elif page == "Import/Export":
        render_import_export()


if __name__ == "__main__":
    main()
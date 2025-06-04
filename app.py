import streamlit as st
import datetime
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from data_manager import get_data_manager
from daily_routines import render_daily_routines_page, get_today_routine
from workout_plans import render_workout_plans_page, get_workout_stats
from diet_plans import render_diet_plans_page, get_diet_stats

# Configure Streamlit page with improved styling
st.set_page_config(
    page_title="Personal Wellness Hub",
    page_icon="🏃‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main theme and background */
    .main > div {
        padding-top: 2rem;
    }

    /* Custom metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }

    .metric-card h3 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: bold;
    }

    .metric-card p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-size: 1rem;
    }

    /* Progress bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #11998e, #38ef7d);
        border-radius: 10px;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }

    /* Success messages */
    .element-container .stAlert[data-baseweb="notification"] {
        border-radius: 10px;
        border-left: 5px solid #28a745;
    }

    /* Task completion styling */
    .task-completed {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }

    .task-pending {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }

    /* Button improvements */
    .stButton > button {
        border-radius: 10px;
        border: none;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


def create_progress_chart(routine_data):
    """Create an interactive progress chart"""
    if not routine_data:
        return None

    # Prepare data for the last 7 routines
    recent_routines = sorted(routine_data, key=lambda x: x['date'], reverse=True)[:7]

    dates = []
    completion_rates = []

    for routine in reversed(recent_routines):  # Reverse to show chronological order
        completed = sum(1 for task in routine['tasks'] if task.get('completed', False))
        total = len(routine['tasks'])
        completion_rate = (completed / total * 100) if total > 0 else 0

        dates.append(routine['date'])
        completion_rates.append(completion_rate)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=completion_rates,
        mode='lines+markers',
        name='Completion Rate',
        line=dict(color='#667eea', width=4),
        marker=dict(size=8, color='#764ba2')
    ))

    fig.update_layout(
        title="7-Day Progress Trend",
        xaxis_title="Date",
        yaxis_title="Completion Rate (%)",
        yaxis=dict(range=[0, 100]),
        height=300,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )

    return fig


def render_enhanced_metrics():
    """Render enhanced metric cards"""
    dm = get_data_manager()
    stats = dm.get_stats()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{stats["routines"]}</h3>
            <p>📅 Daily Routines</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{stats["workouts"]}</h3>
            <p>💪 Workout Plans</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{stats["diets"]}</h3>
            <p>🥗 Diet Plans</p>
        </div>
        """, unsafe_allow_html=True)


def render_dashboard():
    """Render the enhanced main dashboard page"""
    # Header with welcome message
    current_time = datetime.datetime.now()
    if current_time.hour < 12:
        greeting = "Good Morning! 🌅"
    elif current_time.hour < 17:
        greeting = "Good Afternoon! ☀️"
    else:
        greeting = "Good Evening! 🌙"

    st.markdown(f"# {greeting}")
    st.markdown("### Welcome to your Personal Wellness Hub")
    st.markdown("*Track your daily routines, workouts, and nutrition all in one place.*")

    # Enhanced metrics
    render_enhanced_metrics()

    st.markdown("---")

    # Main content layout
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📋 Today's Routine")
        today_routine = get_today_routine()

        if today_routine:
            completed_tasks = sum(1 for task in today_routine.tasks if task.completed)
            total_tasks = len(today_routine.tasks)
            progress = completed_tasks / total_tasks if total_tasks > 0 else 0

            # Enhanced progress display
            st.markdown(f"**{today_routine.name}** - {today_routine.date}")

            # Progress bar with custom styling
            progress_container = st.container()
            with progress_container:
                st.progress(progress)

            col_prog1, col_prog2, col_prog3 = st.columns(3)
            with col_prog1:
                st.metric("Completed", completed_tasks, delta=None)
            with col_prog2:
                st.metric("Remaining", total_tasks - completed_tasks, delta=None)
            with col_prog3:
                st.metric("Progress", f"{progress:.1%}", delta=None)

            # Enhanced task display
            st.write("**🎯 Today's Focus:**")
            current_time = datetime.datetime.now().strftime("%H:%M")
            upcoming_tasks = [task for task in today_routine.tasks
                              if not task.completed and task.time >= current_time][:3]

            if upcoming_tasks:
                for task in upcoming_tasks:
                    st.markdown(f"""
                    <div class="task-pending">
                        <strong>⏰ {task.time}</strong> - {task.name} ({task.duration} min)<br>
                        <small>📁 {task.category}</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                completed_today = [task for task in today_routine.tasks if task.completed]
                if len(completed_today) == len(today_routine.tasks):
                    st.success("🎉 All tasks completed for today! Outstanding work!")
                    st.balloons()
                else:
                    st.info("🌙 All remaining tasks are scheduled for later today.")
        else:
            st.info("📝 No routine set for today.")
            if st.button("➕ Create Today's Routine", type="primary"):
                st.switch_page("daily_routines")

    with col2:
        st.subheader("📊 Analytics")

        # Progress chart
        dm = get_data_manager()
        routines_data = dm.load_routines()

        if routines_data and len(routines_data) > 1:
            fig = create_progress_chart(routines_data)
            if fig:
                st.plotly_chart(fig, use_container_width=True)

        # Quick stats with improved styling
        workout_stats = get_workout_stats()
        diet_stats = get_diet_stats()

        if workout_stats:
            st.markdown("**💪 Workout Summary**")
            st.markdown(f"• **{workout_stats['total']}** total workouts")
            st.markdown(f"• **{workout_stats['avg_duration']}** min average")

            # Difficulty breakdown
            difficulties = ['Beginner', 'Intermediate', 'Advanced']
            counts = [workout_stats.get(d.lower(), 0) for d in difficulties]

            if sum(counts) > 0:
                fig_pie = px.pie(
                    values=counts,
                    names=difficulties,
                    title="Workout Difficulty Distribution",
                    height=250,
                    color_discrete_sequence=['#667eea', '#764ba2', '#f093fb']
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)

        if diet_stats:
            st.markdown("**🥗 Nutrition Overview**")
            st.markdown(f"• **{diet_stats['total']}** meal plans")
            st.markdown(f"• **{diet_stats['avg_calories']}** avg calories")
            st.markdown(f"• **{diet_stats['total_meals']}** total meals")

    # Recent activity with enhanced display
    st.markdown("---")
    st.subheader("📈 Recent Activity")

    if routines_data:
        recent_routines = sorted(routines_data, key=lambda x: x['date'], reverse=True)[:5]

        for routine in recent_routines:
            completed = sum(1 for task in routine['tasks'] if task.get('completed', False))
            total = len(routine['tasks'])
            progress = completed / total if total > 0 else 0

            col_activity1, col_activity2, col_activity3 = st.columns([3, 1, 1])

            with col_activity1:
                st.write(f"**{routine['name']}**")
                st.write(f"📅 {routine['date']}")

            with col_activity2:
                st.metric("Tasks", f"{completed}/{total}")

            with col_activity3:
                if progress >= 0.8:
                    st.success(f"{progress:.0%} ✅")
                elif progress >= 0.5:
                    st.warning(f"{progress:.0%} ⚠️")
                else:
                    st.error(f"{progress:.0%} ❌")

    # Enhanced quick actions
    st.markdown("---")
    st.subheader("🚀 Quick Actions")

    col1, col2, col3, col4 = st.columns(4)

    action_buttons = [
        ("📅 Today's Tasks", "daily_routines", "🎯"),
        ("💪 Workouts", "workout_plans", "🏋️"),
        ("🥗 Nutrition", "diet_plans", "🍎"),
        ("📤 Backup", "import_export", "💾")
    ]

    for i, (label, page, icon) in enumerate(action_buttons):
        with [col1, col2, col3, col4][i]:
            if st.button(f"{icon} {label.split(' ', 1)[1]}", use_container_width=True, key=f"action_{i}"):
                st.switch_page(page)


def render_import_export():
    """Render the enhanced import/export page"""
    st.title("💾 Data Management")
    st.markdown("*Backup your wellness data or import existing routines*")

    dm = get_data_manager()

    # Quick stats overview
    stats = dm.get_stats()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📅 Routines", stats["routines"])
    with col2:
        st.metric("💪 Workouts", stats["workouts"])
    with col3:
        st.metric("🥗 Diet Plans", stats["diets"])

    st.markdown("---")

    tab1, tab2 = st.tabs(["📤 Export Data", "📥 Import Data"])

    with tab1:
        render_enhanced_export_section(dm)

    with tab2:
        render_enhanced_import_section(dm)


def render_enhanced_export_section(dm):
    """Enhanced export section with better UI"""
    st.subheader("📤 Export Your Data")
    st.markdown("*Download your data as JSON files for backup or sharing*")

    # Export individual data types
    export_options = [
        ("📅 Daily Routines", "routines", dm.load_routines()),
        ("💪 Workout Plans", "workouts", dm.load_workouts()),
        ("🥗 Diet Plans", "diets", dm.load_diets())
    ]

    cols = st.columns(3)

    for i, (title, data_type, data) in enumerate(export_options):
        with cols[i]:
            st.markdown(f"**{title}**")
            count = len(data)
            st.markdown(f"*{count} items*")

            if st.button(f"Export {title.split(' ', 1)[1]}",
                         type="primary",
                         use_container_width=True,
                         key=f"export_{data_type}"):
                if count > 0:
                    export_data = dm.export_data(data_type)
                    st.download_button(
                        label=f"📥 Download {title.split(' ', 1)[1]}",
                        data=export_data,
                        file_name=f"{data_type}_{datetime.date.today()}.json",
                        mime="application/json",
                        use_container_width=True,
                        key=f"download_{data_type}"
                    )
                else:
                    st.warning(f"No {title.lower()} to export!")

    # Export all data with enhanced styling
    st.markdown("---")
    st.subheader("📦 Complete Backup")

    if st.button("🔄 Create Full Backup", type="primary", use_container_width=True):
        all_data = {
            "routines": dm.load_routines(),
            "workouts": dm.load_workouts(),
            "diets": dm.load_diets(),
            "export_date": datetime.date.today().isoformat(),
            "app_version": "2.0"
        }

        all_data_json = json.dumps(all_data, indent=2)
        st.download_button(
            label="📥 Download Complete Backup",
            data=all_data_json,
            file_name=f"wellness_hub_backup_{datetime.date.today()}.json",
            mime="application/json",
            use_container_width=True
        )


def render_enhanced_import_section(dm):
    """Enhanced import section with better validation"""
    st.subheader("📥 Import Data")
    st.markdown("*Import data from JSON files to restore backups*")

    # Data type selection
    data_type = st.selectbox(
        "Select data type to import:",
        ["routines", "workouts", "diets"],
        format_func=lambda x: {
            "routines": "📅 Daily Routines",
            "workouts": "💪 Workout Plans",
            "diets": "🥗 Diet Plans"
        }[x]
    )

    # File upload with enhanced validation
    uploaded_file = st.file_uploader(
        "Choose JSON file",
        type="json",
        help="Upload a JSON file containing your wellness data"
    )

    if uploaded_file is not None:
        try:
            json_data = uploaded_file.read().decode("utf-8")
            preview_data = json.loads(json_data)

            # Enhanced preview
            with st.expander("📋 Preview Import Data", expanded=True):
                if isinstance(preview_data, list):
                    st.success(f"✅ Valid format! Found **{len(preview_data)}** items to import")

                    if preview_data:
                        # Show summary statistics
                        st.markdown("**Sample Item:**")
                        st.json(preview_data[0])
                else:
                    st.info("Data appears to be in object format")
                    st.json(preview_data)

            # Import actions
            col1, col2 = st.columns(2)

            with col1:
                if st.button("🔄 Replace Data", type="primary", use_container_width=True):
                    if dm.import_data(json_data, data_type):
                        st.success(f"✅ Successfully imported {data_type}!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Failed to import data. Please check the format.")

            with col2:
                if st.button("➕ Append Data", type="secondary", use_container_width=True):
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


def main():
    """Enhanced main application function"""
    # Sidebar with improved styling
    with st.sidebar:
        st.markdown("# 🏃‍♂️ Wellness Hub")
        st.markdown("*Your complete wellness solution*")

        # Navigation with better styling
        page = st.selectbox(
            "🧭 Navigate:",
            ["Dashboard", "Daily Routines", "Workout Plans", "Diet Plans", "Data Management"],
            index=0
        )

        st.markdown("---")

        # Enhanced quick stats
        dm = get_data_manager()
        stats = dm.get_stats()

        st.markdown("**📊 Overview**")
        for icon, label, value in [
            ("📅", "Routines", stats['routines']),
            ("💪", "Workouts", stats['workouts']),
            ("🥗", "Diet Plans", stats['diets'])
        ]:
            st.markdown(f"{icon} **{value}** {label}")

        # Today's progress in sidebar
        today_routine = get_today_routine()
        if today_routine:
            completed = sum(1 for task in today_routine.tasks if task.completed)
            total = len(today_routine.tasks)
            progress = completed / total if total > 0 else 0

            st.markdown("---")
            st.markdown("**📋 Today's Progress**")
            st.progress(progress)
            st.markdown(f"**{completed}/{total}** tasks ({progress:.0%})")

            if progress == 1.0:
                st.success("Perfect day! 🎉")
            elif progress >= 0.8:
                st.info("Almost there! 💪")

        # Footer with enhanced branding
        st.markdown("---")
        st.markdown("**🏃‍♂️ Wellness Hub v2.0**")
        st.markdown("*Built with ❤️ for your health*")
        st.markdown("*Stay strong, stay focused!* 💪")

    # Route to appropriate page
    if page == "Dashboard":
        render_dashboard()
    elif page == "Daily Routines":
        render_daily_routines_page()
    elif page == "Workout Plans":
        render_workout_plans_page()
    elif page == "Diet Plans":
        render_diet_plans_page()
    elif page == "Data Management":
        render_import_export()


if __name__ == "__main__":
    main()
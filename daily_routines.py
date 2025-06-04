import streamlit as st
import datetime
from dataclasses import asdict
from typing import List
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from models import DailyRoutine, RoutineTask, dict_to_daily_routine, generate_id
from data_manager import get_data_manager


def load_daily_routines_css():
    """Load CSS for daily routines page"""
    st.markdown("""
    <style>
        /* Task card styling */
        .task-card {
            background: white;
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-left: 4px solid #e0e0e0;
            transition: all 0.3s ease;
        }

        .task-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        }

        .task-completed {
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            border-left: 4px solid #28a745 !important;
        }

        .task-current {
            background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
            border-left: 4px solid #ffc107 !important;
            animation: pulse 2s infinite;
        }

        .task-upcoming {
            background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
            border-left: 4px solid #17a2b8 !important;
        }

        .task-overdue {
            background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
            border-left: 4px solid #dc3545 !important;
        }

        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.8; }
            100% { opacity: 1; }
        }

        /* Category badges */
        .category-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-right: 0.5rem;
        }

        .category-morning { background: #ffeaa7; color: #2d3436; }
        .category-work { background: #74b9ff; color: white; }
        .category-exercise { background: #fd79a8; color: white; }
        .category-personal { background: #00b894; color: white; }
        .category-evening { background: #6c5ce7; color: white; }

        /* Progress ring */
        .progress-ring {
            width: 120px;
            height: 120px;
            margin: 0 auto;
        }

        /* Time indicator */
        .time-indicator {
            display: inline-block;
            padding: 0.25rem 0.5rem;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.9rem;
        }

        .time-current { background: #ffc107; color: #212529; }
        .time-upcoming { background: #17a2b8; color: white; }
        .time-completed { background: #28a745; color: white; }
        .time-overdue { background: #dc3545; color: white; }

        /* Form enhancements */
        .form-section {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            border: 1px solid #dee2e6;
        }

        /* Stats cards */
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            margin: 0.5rem 0;
        }

        .stat-card h4 {
            margin: 0;
            font-size: 2rem;
            font-weight: bold;
        }

        .stat-card p {
            margin: 0.25rem 0 0 0;
            opacity: 0.9;
        }
    </style>
    """, unsafe_allow_html=True)


def get_task_status(task_time: str, completed: bool) -> str:
    """Determine task status based on time and completion"""
    if completed:
        return "completed"

    try:
        current_time = datetime.datetime.now()
        task_datetime = datetime.datetime.strptime(task_time, "%H:%M").replace(
            year=current_time.year,
            month=current_time.month,
            day=current_time.day
        )

        time_diff = (task_datetime - current_time).total_seconds() / 60  # minutes

        if -30 <= time_diff <= 30:  # Within 30 minutes
            return "current"
        elif time_diff > 30:
            return "upcoming"
        else:
            return "overdue"
    except:
        return "upcoming"


def get_category_badge(category: str) -> str:
    """Generate category badge HTML"""
    category_classes = {
        "Morning": "category-morning",
        "Work": "category-work",
        "Exercise": "category-exercise",
        "Personal": "category-personal",
        "Evening": "category-evening"
    }

    badge_class = category_classes.get(category, "category-personal")
    return f'<span class="category-badge {badge_class}">{category}</span>'


def render_daily_routines_page():
    """Render the enhanced daily routines page"""
    # Load CSS first
    load_daily_routines_css()

    st.title("📅 Daily Routines")
    st.markdown("*Organize your day, track your progress, achieve your goals*")

    # Quick stats overview
    dm = get_data_manager()
    routines_data = dm.load_routines()

    if routines_data:
        render_routine_stats(routines_data)

    # Enhanced tab layout
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Today's Focus", "📅 All Routines", "➕ Create Routine", "⚙️ Manage"])

    with tab1:
        render_today_focus()

    with tab2:
        render_view_routines()

    with tab3:
        render_enhanced_create_routine()

    with tab4:
        render_enhanced_manage_routines()


def render_routine_stats(routines_data: List[dict]):
    """Render enhanced routine statistics"""
    # Calculate statistics
    total_routines = len(routines_data)
    total_tasks = sum(len(r['tasks']) for r in routines_data)
    completed_tasks = sum(sum(1 for task in r['tasks'] if task.get('completed', False)) for r in routines_data)
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    # Recent completion trend
    recent_routines = sorted(routines_data, key=lambda x: x['date'], reverse=True)[:7]
    avg_recent_completion = 0
    if recent_routines:
        recent_completion_rates = []
        for routine in recent_routines:
            completed = sum(1 for task in routine['tasks'] if task.get('completed', False))
            total = len(routine['tasks'])
            rate = (completed / total * 100) if total > 0 else 0
            recent_completion_rates.append(rate)
        avg_recent_completion = sum(recent_completion_rates) / len(recent_completion_rates)

    # Display stats
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <h4>{total_routines}</h4>
            <p>Total Routines</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <h4>{total_tasks}</h4>
            <p>Total Tasks</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <h4>{completion_rate:.0f}%</h4>
            <p>Overall Completion</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <h4>{avg_recent_completion:.0f}%</h4>
            <p>7-Day Average</p>
        </div>
        """, unsafe_allow_html=True)


def render_today_focus():
    """Render enhanced today's focus tab"""
    st.subheader("🎯 Today's Focus")

    dm = get_data_manager()
    today = datetime.date.today().isoformat()
    routines_data = dm.load_routines()
    today_routine_data = next((r for r in routines_data if r['date'] == today), None)

    if today_routine_data:
        routine = dict_to_daily_routine(today_routine_data)
        render_enhanced_routine_details(routine, routines_data, is_today=True)
    else:
        st.info("📝 No routine set for today.")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Create Today's Routine", type="primary", use_container_width=True):
                st.session_state.create_routine_date = today
                st.rerun()

        with col2:
            # Suggest copying from recent routine
            if routines_data:
                recent_routine = max(routines_data, key=lambda x: x['date'])
                if st.button(f"📋 Copy from {recent_routine['name']}", type="secondary", use_container_width=True):
                    duplicate_routine_for_today(recent_routine, today)
                    st.rerun()


def duplicate_routine_for_today(source_routine: dict, target_date: str):
    """Duplicate a routine for today"""
    dm = get_data_manager()

    # Create new routine for today
    new_routine = DailyRoutine(
        id=generate_id(),
        name=f"Today's Routine",
        date=target_date,
        tasks=[RoutineTask(
            id=generate_id(),
            name=task['name'],
            description=task['description'],
            time=task['time'],
            duration=task['duration'],
            category=task['category'],
            completed=False
        ) for task in source_routine['tasks']],
        notes=f"Copied from {source_routine['name']}"
    )

    routines_data = dm.load_routines()
    routines_data.append(asdict(new_routine))

    if dm.save_routines(routines_data):
        st.success("✅ Today's routine created successfully!")


def render_enhanced_routine_details(routine: DailyRoutine, routines_data: List[dict], is_today: bool = False):
    """Render enhanced routine details with real-time updates"""
    dm = get_data_manager()

    # Progress calculation
    completed = sum(1 for task in routine.tasks if task.completed)
    total = len(routine.tasks)
    progress = completed / total if total > 0 else 0

    # Header with progress
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"### {routine.name}")
        st.markdown(f"📅 **{routine.date}**")
        if routine.notes:
            st.markdown(f"💡 *{routine.notes}*")

    with col2:
        # Create circular progress indicator
        fig = go.Figure(data=[go.Pie(
            values=[completed, total - completed],
            labels=['Completed', 'Remaining'],
            hole=0.7,
            marker_colors=['#28a745', '#e9ecef'],
            textinfo='none',
            showlegend=False
        )])

        fig.update_layout(
            height=150,
            width=150,
            margin=dict(t=0, b=0, l=0, r=0),
            annotations=[dict(text=f'{progress:.0%}', x=0.5, y=0.5, font_size=20, showarrow=False)]
        )

        st.plotly_chart(fig, use_container_width=True, key=f"progress_chart_{routine.id}")

    # Task filtering and sorting
    col_filter1, col_filter2, col_filter3 = st.columns(3)

    with col_filter1:
        status_filter = st.selectbox(
            "Filter by Status:",
            ["All", "Completed", "Pending", "Current", "Overdue"],
            key=f"status_filter_{routine.id}"
        )

    with col_filter2:
        category_filter = st.selectbox(
            "Filter by Category:",
            ["All"] + list(set(task.category for task in routine.tasks)),
            key=f"category_filter_{routine.id}"
        )

    with col_filter3:
        sort_by = st.selectbox(
            "Sort by:",
            ["Time", "Category", "Duration", "Status"],
            key=f"sort_by_{routine.id}"
        )

    # Filter and sort tasks
    filtered_tasks = routine.tasks.copy()

    # Apply filters
    if status_filter != "All":
        if status_filter == "Completed":
            filtered_tasks = [t for t in filtered_tasks if t.completed]
        elif status_filter == "Pending":
            filtered_tasks = [t for t in filtered_tasks if not t.completed]
        elif status_filter in ["Current", "Overdue"]:
            filtered_tasks = [t for t in filtered_tasks if not t.completed and
                              get_task_status(t.time, t.completed) == status_filter.lower()]

    if category_filter != "All":
        filtered_tasks = [t for t in filtered_tasks if t.category == category_filter]

    # Sort tasks
    if sort_by == "Time":
        filtered_tasks.sort(key=lambda t: t.time)
    elif sort_by == "Category":
        filtered_tasks.sort(key=lambda t: t.category)
    elif sort_by == "Duration":
        filtered_tasks.sort(key=lambda t: t.duration, reverse=True)
    elif sort_by == "Status":
        filtered_tasks.sort(key=lambda t: (t.completed, t.time))

    # Task list with enhanced display
    st.markdown("---")

    if not filtered_tasks:
        st.info("No tasks match the current filters.")
        return

    # Group by category for better organization
    if sort_by == "Category":
        categories = {}
        for task in filtered_tasks:
            if task.category not in categories:
                categories[task.category] = []
            categories[task.category].append(task)

        for category, tasks in categories.items():
            st.markdown(f"#### {get_category_badge(category)}", unsafe_allow_html=True)
            for task in tasks:
                render_enhanced_task_card(task, routine, routines_data, dm)
    else:
        for task in filtered_tasks:
            render_enhanced_task_card(task, routine, routines_data, dm)


def render_enhanced_task_card(task: RoutineTask, routine: DailyRoutine, routines_data: List[dict], dm):
    """Render an enhanced task card with improved interactions"""
    task_status = get_task_status(task.time, task.completed)

    # Task card container
    with st.container():
        col1, col2 = st.columns([1, 10])

        with col1:
            new_status = st.checkbox(
                "",
                value=task.completed,
                key=f"task_checkbox_{routine.id}_{task.id}",
                help="Mark as completed"
            )

        with col2:
            # Display task information using streamlit components instead of HTML
            time_info = get_time_info(task.time, task.completed)

            # Time and task name row
            col_time, col_name, col_duration = st.columns([1, 3, 1])

            with col_time:
                if task_status == "completed":
                    st.success(f"**{task.time}**")
                elif task_status == "current":
                    st.warning(f"**{task.time}**")
                elif task_status == "overdue":
                    st.error(f"**{task.time}**")
                else:
                    st.info(f"**{task.time}**")

            with col_name:
                st.markdown(f"**{task.name}**")

            with col_duration:
                st.write(f"{task.duration} min")
                st.caption(time_info)

            # Category badge
            if task.category == "Morning":
                st.markdown("🌅 Morning")
            elif task.category == "Work":
                st.markdown("💼 Work")
            elif task.category == "Exercise":
                st.markdown("💪 Exercise")
            elif task.category == "Personal":
                st.markdown("👤 Personal")
            elif task.category == "Evening":
                st.markdown("🌙 Evening")

            # Description
            if task.description:
                st.caption(task.description)

            st.markdown("---")

        # Update completion status if changed
        if new_status != task.completed:
            # Update task status
            for i, t in enumerate(routine.tasks):
                if t.id == task.id:
                    routine.tasks[i].completed = new_status
                    break

            # Update in storage
            for j, r in enumerate(routines_data):
                if r['id'] == routine.id:
                    routines_data[j] = asdict(routine)
                    if dm.save_routines(routines_data):
                        if new_status:
                            st.success(f"✅ Completed: {task.name}")
                        else:
                            st.info(f"⏳ Unmarked: {task.name}")
                        st.rerun()
                    break


def get_time_info(task_time: str, completed: bool) -> str:
    """Get human-readable time information for a task"""
    if completed:
        return "✅ Done"

    try:
        current_time = datetime.datetime.now()
        task_datetime = datetime.datetime.strptime(task_time, "%H:%M").replace(
            year=current_time.year,
            month=current_time.month,
            day=current_time.day
        )

        time_diff = (task_datetime - current_time).total_seconds() / 60  # minutes

        if abs(time_diff) < 30:
            return "🔥 Now"
        elif time_diff > 0:
            hours = int(time_diff // 60)
            minutes = int(time_diff % 60)
            if hours > 0:
                return f"⏰ In {hours}h {minutes}m"
            else:
                return f"⏰ In {minutes}m"
        else:
            hours = int(abs(time_diff) // 60)
            minutes = int(abs(time_diff) % 60)
            if hours > 0:
                return f"⚠️ {hours}h {minutes}m ago"
            else:
                return f"⚠️ {minutes}m ago"
    except:
        return ""


def render_task_progress_bar(task: RoutineTask) -> str:
    """Render a progress bar for current tasks"""
    # This would ideally show progress through the task duration
    # For now, it's a visual indicator that this is the current task
    return '''
    <div style="margin-top: 0.5rem;">
        <div style="background: #ffc107; height: 4px; border-radius: 2px; animation: pulse 2s infinite;"></div>
    </div>
    '''


def render_view_routines():
    """Render enhanced view routines tab"""
    st.subheader("📅 All Routines")

    dm = get_data_manager()
    routines_data = dm.load_routines()

    if not routines_data:
        st.info("No routines created yet! Start by creating your first routine.")
        return

    # Enhanced filtering and sorting
    col1, col2, col3 = st.columns(3)

    with col1:
        date_filter = st.selectbox(
            "Time Period:",
            ["All Time", "This Week", "This Month", "Last 7 Days", "Last 30 Days"]
        )

    with col2:
        completion_filter = st.selectbox(
            "Completion Status:",
            ["All", "Completed (>80%)", "In Progress (20-80%)", "Not Started (<20%)"]
        )

    with col3:
        sort_order = st.selectbox(
            "Sort by:",
            ["Date (Newest)", "Date (Oldest)", "Completion Rate", "Task Count"]
        )

    # Apply filters
    filtered_routines = filter_routines(routines_data, date_filter, completion_filter)

    # Sort routines
    if sort_order == "Date (Newest)":
        filtered_routines.sort(key=lambda x: x['date'], reverse=True)
    elif sort_order == "Date (Oldest)":
        filtered_routines.sort(key=lambda x: x['date'])
    elif sort_order == "Completion Rate":
        filtered_routines.sort(key=lambda x: calculate_completion_rate(x), reverse=True)
    elif sort_order == "Task Count":
        filtered_routines.sort(key=lambda x: len(x['tasks']), reverse=True)

    # Display routines with enhanced cards
    for i, routine_data in enumerate(filtered_routines):
        routine = dict_to_daily_routine(routine_data)
        render_routine_preview_card(routine, i)


def filter_routines(routines_data: List[dict], date_filter: str, completion_filter: str) -> List[dict]:
    """Apply filters to routines data"""
    filtered = routines_data.copy()

    # Date filtering
    if date_filter != "All Time":
        today = datetime.date.today()

        if date_filter == "This Week":
            week_start = today - datetime.timedelta(days=today.weekday())
            filtered = [r for r in filtered if datetime.date.fromisoformat(r['date']) >= week_start]
        elif date_filter == "This Month":
            month_start = today.replace(day=1)
            filtered = [r for r in filtered if datetime.date.fromisoformat(r['date']) >= month_start]
        elif date_filter == "Last 7 Days":
            week_ago = today - datetime.timedelta(days=7)
            filtered = [r for r in filtered if datetime.date.fromisoformat(r['date']) >= week_ago]
        elif date_filter == "Last 30 Days":
            month_ago = today - datetime.timedelta(days=30)
            filtered = [r for r in filtered if datetime.date.fromisoformat(r['date']) >= month_ago]

    # Completion filtering
    if completion_filter != "All":
        if completion_filter == "Completed (>80%)":
            filtered = [r for r in filtered if calculate_completion_rate(r) > 0.8]
        elif completion_filter == "In Progress (20-80%)":
            filtered = [r for r in filtered if 0.2 <= calculate_completion_rate(r) <= 0.8]
        elif completion_filter == "Not Started (<20%)":
            filtered = [r for r in filtered if calculate_completion_rate(r) < 0.2]

    return filtered


def calculate_completion_rate(routine_data: dict) -> float:
    """Calculate completion rate for a routine"""
    completed = sum(1 for task in routine_data['tasks'] if task.get('completed', False))
    total = len(routine_data['tasks'])
    return completed / total if total > 0 else 0


def render_routine_preview_card(routine: DailyRoutine, index: int):
    """Render a preview card for a routine"""
    completed = sum(1 for task in routine.tasks if task.completed)
    total = len(routine.tasks)
    progress = completed / total if total > 0 else 0

    with st.expander(f"📅 {routine.name} - {routine.date} ({progress:.0%} complete)"):
        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(f"**Description:** {routine.notes or 'No description'}")

            # Category breakdown
            categories = {}
            for task in routine.tasks:
                categories[task.category] = categories.get(task.category, 0) + 1

            category_text = ", ".join([f"{cat} ({count})" for cat, count in categories.items()])
            st.markdown(f"**Categories:** {category_text}")

            # Time overview
            total_duration = sum(task.duration for task in routine.tasks)
            st.markdown(f"**Total Duration:** {total_duration} minutes")

        with col2:
            # Mini progress chart
            fig = go.Figure(data=[go.Pie(
                values=[completed, total - completed],
                labels=['Completed', 'Remaining'],
                hole=0.6,
                marker_colors=['#28a745', '#e9ecef'],
                textinfo='none',
                showlegend=False
            )])

            fig.update_layout(
                height=120,
                width=120,
                margin=dict(t=0, b=0, l=0, r=0),
                annotations=[dict(text=f'{completed}/{total}', x=0.5, y=0.5, font_size=14, showarrow=False)]
            )

            st.plotly_chart(fig, use_container_width=True, key=f"preview_chart_{routine.id}_{index}")

        # Task summary
        st.markdown("**Tasks:**")
        for task in routine.tasks:
            status_icon = "✅" if task.completed else "⏳"
            st.markdown(f"{status_icon} **{task.time}** - {task.name} ({task.duration} min)")


def render_enhanced_create_routine():
    """Render enhanced create routine form"""
    st.subheader("➕ Create New Routine")
    st.markdown("*Design your perfect day with structured tasks and goals*")

    dm = get_data_manager()

    # Template selection
    with st.expander("🚀 Quick Start Templates", expanded=True):
        col1, col2, col3 = st.columns(3)

        templates = {
            "Work Day": {
                "tasks": [
                    ("Morning Routine", "06:00", 30, "Morning", "Wake up, stretch, breakfast"),
                    ("Work Block 1", "08:00", 120, "Work", "Deep focus work session"),
                    ("Break", "10:00", 15, "Personal", "Short break and movement"),
                    ("Work Block 2", "10:15", 120, "Work", "Continued focus work"),
                    ("Lunch", "12:15", 60, "Personal", "Meal and relaxation"),
                    ("Work Block 3", "13:15", 120, "Work", "Afternoon productivity"),
                    ("Exercise", "17:00", 60, "Exercise", "Physical activity"),
                    ("Evening Routine", "20:00", 90, "Evening", "Dinner, relaxation, prep for tomorrow")
                ]
            },
            "Weekend": {
                "tasks": [
                    ("Leisurely Morning", "08:00", 60, "Morning", "Slow start to the day"),
                    ("Exercise", "10:00", 90, "Exercise", "Extended workout session"),
                    ("Personal Time", "12:00", 180, "Personal", "Hobbies, errands, socializing"),
                    ("Meal Prep", "16:00", 60, "Personal", "Prepare meals for the week"),
                    ("Relaxation", "19:00", 120, "Evening", "Entertainment and rest")
                ]
            },
            "Study Day": {
                "tasks": [
                    ("Morning Prep", "07:00", 30, "Morning", "Get ready and fuel up"),
                    ("Study Session 1", "07:30", 120, "Personal", "Deep learning time"),
                    ("Break", "09:30", 30, "Personal", "Movement and snack"),
                    ("Study Session 2", "10:00", 120, "Personal", "Continue learning"),
                    ("Lunch Break", "12:00", 60, "Personal", "Meal and mental break"),
                    ("Study Session 3", "13:00", 90, "Personal", "Review and practice"),
                    ("Exercise", "16:00", 60, "Exercise", "Physical activity for mental clarity"),
                    ("Evening Review", "19:00", 60, "Evening", "Summarize and plan tomorrow")
                ]
            }
        }

        with col1:
            if st.button("💼 Work Day Template", use_container_width=True):
                st.session_state.selected_template = templates["Work Day"]

        with col2:
            if st.button("🏖️ Weekend Template", use_container_width=True):
                st.session_state.selected_template = templates["Weekend"]

        with col3:
            if st.button("📚 Study Day Template", use_container_width=True):
                st.session_state.selected_template = templates["Study Day"]

    # Main form
    with st.form("create_routine_enhanced", clear_on_submit=True):
        st.markdown('<div class="form-section">', unsafe_allow_html=True)

        # Basic routine info
        col1, col2 = st.columns(2)
        with col1:
            routine_name = st.text_input(
                "Routine Name*",
                placeholder="e.g., Productive Monday",
                help="Give your routine a descriptive name"
            )
        with col2:
            routine_date = st.date_input(
                "Date*",
                value=datetime.date.today(),
                help="Select the date for this routine"
            )

        routine_notes = st.text_area(
            "Routine Description",
            placeholder="Describe the purpose and goals of this routine...",
            help="Optional description to help you remember the routine's purpose"
        )

        st.markdown('</div>', unsafe_allow_html=True)

        # Smart task builder
        st.markdown("### 📋 Task Builder")

        # Check if template was selected
        if hasattr(st.session_state, 'selected_template'):
            template_tasks = st.session_state.selected_template["tasks"]
            num_tasks = st.number_input(
                "Number of tasks",
                min_value=1,
                max_value=20,
                value=len(template_tasks)
            )
        else:
            num_tasks = st.number_input("Number of tasks", min_value=1, max_value=20, value=5)

        tasks = []

        for i in range(num_tasks):
            st.markdown(f"#### Task {i + 1}")

            # Pre-fill with template if available
            if hasattr(st.session_state, 'selected_template') and i < len(st.session_state.selected_template["tasks"]):
                template_task = st.session_state.selected_template["tasks"][i]
                default_name = template_task[0]
                default_time = template_task[1]
                default_duration = template_task[2]
                default_category = template_task[3]
                default_description = template_task[4]
            else:
                default_name = ""
                default_time = "09:00"
                default_duration = 30
                default_category = "Personal"
                default_description = ""

            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                task_name = st.text_input(
                    "Task Name*",
                    key=f"task_name_{i}",
                    value=default_name,
                    placeholder="e.g., Morning Workout"
                )

            with col2:
                task_time = st.text_input(
                    "Time*",
                    key=f"task_time_{i}",
                    value=default_time,
                    placeholder="09:00",
                    help="24-hour format (HH:MM)"
                )

            with col3:
                task_duration = st.number_input(
                    "Duration (min)*",
                    key=f"task_duration_{i}",
                    min_value=1,
                    max_value=480,
                    value=default_duration
                )

            col4, col5 = st.columns(2)

            with col4:
                task_category = st.selectbox(
                    "Category*",
                    ["Morning", "Work", "Exercise", "Personal", "Evening"],
                    key=f"task_cat_{i}",
                    index=["Morning", "Work", "Exercise", "Personal", "Evening"].index(default_category)
                )

            with col5:
                task_desc = st.text_input(
                    "Description",
                    key=f"task_desc_{i}",
                    value=default_description,
                    placeholder="Brief description..."
                )

            # Validate task time format
            try:
                datetime.datetime.strptime(task_time, "%H:%M")
                time_valid = True
            except ValueError:
                time_valid = False
                st.error("⚠️ Please use HH:MM format (e.g., 09:30)")

            if task_name and time_valid:
                tasks.append(RoutineTask(
                    id=generate_id(),
                    name=task_name,
                    description=task_desc,
                    time=task_time,
                    duration=task_duration,
                    category=task_category
                ))

            st.markdown("---")

        # Clear template selection after use
        if hasattr(st.session_state, 'selected_template'):
            del st.session_state.selected_template

        # Task summary
        if tasks:
            st.markdown("### 📊 Routine Summary")

            col1, col2, col3 = st.columns(3)

            with col1:
                total_duration = sum(task.duration for task in tasks)
                st.metric("Total Duration", f"{total_duration} min")

            with col2:
                categories = list(set(task.category for task in tasks))
                st.metric("Categories", len(categories))

            with col3:
                task_count = len(tasks)
                st.metric("Tasks", task_count)

            # Category breakdown
            category_counts = {}
            for task in tasks:
                category_counts[task.category] = category_counts.get(task.category, 0) + 1

            category_summary = ", ".join([f"{cat} ({count})" for cat, count in category_counts.items()])
            st.markdown(f"**Category Breakdown:** {category_summary}")

        # Submit button
        submitted = st.form_submit_button("🚀 Create Routine", type="primary", use_container_width=True)

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


def render_enhanced_manage_routines():
    """Render enhanced manage routines tab"""
    st.subheader("⚙️ Manage Routines")
    st.markdown("*Edit, duplicate, delete, and analyze your routines*")

    dm = get_data_manager()
    routines_data = dm.load_routines()

    if not routines_data:
        st.info("No routines to manage! Create some routines first.")
        return

    # Routine selection with enhanced display
    routine_options = {}
    for r in routines_data:
        completed = sum(1 for task in r['tasks'] if task.get('completed', False))
        total = len(r['tasks'])
        progress = completed / total if total > 0 else 0

        display_name = f"{r['name']} - {r['date']} ({progress:.0%} complete)"
        routine_options[display_name] = r['id']

    selected_routine_name = st.selectbox(
        "Select routine to manage:",
        list(routine_options.keys()),
        help="Choose a routine to view details and manage"
    )

    if selected_routine_name:
        selected_routine_id = routine_options[selected_routine_name]
        routine_data = next(r for r in routines_data if r['id'] == selected_routine_id)
        routine = dict_to_daily_routine(routine_data)

        # Enhanced routine details
        st.markdown("---")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("### Routine Details")
            st.markdown(f"**Name:** {routine.name}")
            st.markdown(f"**Date:** {routine.date}")
            st.markdown(f"**Description:** {routine.notes or 'No description'}")

            # Task statistics
            completed_tasks = sum(1 for task in routine.tasks if task.completed)
            total_tasks = len(routine.tasks)
            total_duration = sum(task.duration for task in routine.tasks)

            col_stat1, col_stat2, col_stat3 = st.columns(3)
            with col_stat1:
                st.metric("Tasks", f"{completed_tasks}/{total_tasks}")
            with col_stat2:
                st.metric("Duration", f"{total_duration} min")
            with col_stat3:
                completion_rate = completed_tasks / total_tasks if total_tasks > 0 else 0
                st.metric("Completion", f"{completion_rate:.0%}")

        with col2:
            # Progress visualization
            fig = go.Figure(data=[go.Pie(
                values=[completed_tasks, total_tasks - completed_tasks],
                labels=['Completed', 'Remaining'],
                hole=0.6,
                marker_colors=['#28a745', '#e9ecef'],
                textinfo='label+percent',
                showlegend=True
            )])

            fig.update_layout(
                height=200,
                margin=dict(t=0, b=0, l=0, r=0),
                title="Task Completion"
            )

            st.plotly_chart(fig, use_container_width=True, key=f"manage_chart_{routine.id}")

        # Task breakdown by category
        with st.expander("📊 Category Analysis", expanded=True):
            category_data = {}
            for task in routine.tasks:
                if task.category not in category_data:
                    category_data[task.category] = {"total": 0, "completed": 0, "duration": 0}

                category_data[task.category]["total"] += 1
                category_data[task.category]["duration"] += task.duration
                if task.completed:
                    category_data[task.category]["completed"] += 1

            # Create category chart
            categories = list(category_data.keys())
            completed_counts = [category_data[cat]["completed"] for cat in categories]
            total_counts = [category_data[cat]["total"] for cat in categories]

            fig = go.Figure()
            fig.add_trace(go.Bar(name='Completed', x=categories, y=completed_counts, marker_color='#28a745'))
            fig.add_trace(go.Bar(name='Total', x=categories, y=total_counts, marker_color='#e9ecef'))

            fig.update_layout(
                title="Tasks by Category",
                xaxis_title="Category",
                yaxis_title="Number of Tasks",
                barmode='overlay',
                height=300
            )

            st.plotly_chart(fig, use_container_width=True, key=f"category_chart_{routine.id}")

        # Quick task overview
        with st.expander("📋 Quick Task Overview"):
            for i, task in enumerate(routine.tasks, 1):
                status_icon = "✅" if task.completed else "⏳"
                st.markdown(
                    f"{i}. {status_icon} **{task.time}** - {task.name} ({task.duration} min) - *{task.category}*")

        # Action buttons with enhanced functionality
        st.markdown("---")
        st.markdown("### Actions")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("🗑️ Delete", type="secondary", use_container_width=True):
                if dm.delete_routine(selected_routine_id):
                    st.success("✅ Routine deleted successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to delete routine.")

        with col2:
            if st.button("🔄 Reset Progress", type="secondary", use_container_width=True):
                # Reset all task completion status
                for task in routine.tasks:
                    task.completed = False

                # Update in storage
                for i, r in enumerate(routines_data):
                    if r['id'] == selected_routine_id:
                        routines_data[i] = asdict(routine)
                        if dm.save_routines(routines_data):
                            st.success("✅ All tasks reset to incomplete!")
                            st.rerun()
                        break

        with col3:
            if st.button("📋 Duplicate", type="secondary", use_container_width=True):
                # Create a copy for today or next available date
                target_date = datetime.date.today()
                existing_dates = [r['date'] for r in routines_data]

                while target_date.isoformat() in existing_dates:
                    target_date += datetime.timedelta(days=1)

                new_routine = DailyRoutine(
                    id=generate_id(),
                    name=f"{routine.name} (Copy)",
                    date=target_date.isoformat(),
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
                    st.success(f"✅ Routine duplicated for {target_date}!")
                    st.rerun()

        with col4:
            if st.button("📊 Export", type="secondary", use_container_width=True):
                import json
                routine_json = json.dumps(asdict(routine), indent=2)
                st.download_button(
                    label="📥 Download JSON",
                    data=routine_json,
                    file_name=f"{routine.name.replace(' ', '_')}_{routine.date}.json",
                    mime="application/json",
                    use_container_width=True
                )


def get_today_routine():
    """Get today's routine if it exists"""
    dm = get_data_manager()
    today = datetime.date.today().isoformat()
    routines_data = dm.load_routines()
    today_routine_data = next((r for r in routines_data if r['date'] == today), None)

    if today_routine_data:
        return dict_to_daily_routine(today_routine_data)
    return None
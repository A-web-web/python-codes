import streamlit as st
from datetime import datetime, date, timedelta
import csv
import io

# Initialize session state for tasks
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# Initialize task counter for unique IDs
if 'task_counter' not in st.session_state:
    st.session_state.task_counter = 0

# Initialize categories
if 'categories' not in st.session_state:
    st.session_state.categories = ["Personal", "Work", "Shopping", "Health"]

# Initialize priorities
if 'priorities' not in st.session_state:
    st.session_state.priorities = ["High", "Medium", "Low"]


def add_task(task_text, category="Personal", priority="Medium", due_date=None):
    """Add a new task to the list"""
    if task_text.strip():
        new_task = {
            'id': st.session_state.task_counter,
            'text': task_text.strip(),
            'completed': False,
            'category': category,
            'priority': priority,
            'due_date': due_date.strftime("%Y-%m-%d") if due_date else None,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        st.session_state.tasks.append(new_task)
        st.session_state.task_counter += 1
        return True
    return False


def toggle_task_completion(task_id):
    """Toggle the completion status of a task"""
    for task in st.session_state.tasks:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            break


def delete_task(task_id):
    """Delete a task from the list"""
    st.session_state.tasks = [
        task for task in st.session_state.tasks if task['id'] != task_id
    ]


def clear_completed_tasks():
    """Remove all completed tasks"""
    st.session_state.tasks = [
        task for task in st.session_state.tasks if not task['completed']
    ]


def is_overdue(task):
    """Check if a task is overdue"""
    if not task.get('due_date') or task.get('completed', False):
        return False
    try:
        due_date = datetime.strptime(task['due_date'], "%Y-%m-%d").date()
        return due_date < date.today()
    except (ValueError, TypeError):
        return False


def export_to_csv(tasks):
    """Export tasks to CSV format"""
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(['Task', 'Category', 'Priority',
                    'Due Date', 'Status', 'Created At', 'Overdue'])

    # Write tasks
    for task in tasks:
        status = 'Completed' if task.get('completed', False) else 'Pending'
        overdue = 'Yes' if is_overdue(task) else 'No'
        due_date = task.get('due_date', '')

        writer.writerow([
            task.get('text', ''),
            task.get('category', 'Personal'),
            task.get('priority', 'Medium'),
            due_date,
            status,
            task.get('created_at', ''),
            overdue
        ])

    return output.getvalue()


def export_to_text(tasks):
    """Export tasks to plain text format"""
    output = []
    output.append("=" * 50)
    output.append("TO-DO LIST EXPORT")
    output.append(f"Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    output.append(f"Total tasks: {len(tasks)}")
    output.append("=" * 50)
    output.append("")

    if not tasks:
        output.append("No tasks found.")
        return "\n".join(output)

    # Group tasks by status
    pending_tasks = [t for t in tasks if not t.get('completed', False)]
    completed_tasks = [t for t in tasks if t.get('completed', False)]

    if pending_tasks:
        output.append("PENDING TASKS:")
        output.append("-" * 20)
        for i, task in enumerate(pending_tasks, 1):
            priority = task.get('priority', 'Medium')
            category = task.get('category', 'Personal')
            due_date = task.get('due_date', '')
            overdue_text = " [OVERDUE]" if is_overdue(task) else ""

            output.append(f"{i}. {task.get('text', '')}")
            output.append(
                f"   Category: {category} | Priority: {priority}{overdue_text}")
            if due_date:
                output.append(f"   Due: {due_date}")
            output.append(f"   Created: {task.get('created_at', '')}")
            output.append("")

    if completed_tasks:
        output.append("COMPLETED TASKS:")
        output.append("-" * 20)
        for i, task in enumerate(completed_tasks, 1):
            category = task.get('category', 'Personal')
            priority = task.get('priority', 'Medium')

            output.append(f"{i}. {task.get('text', '')} ✓")
            output.append(f"   Category: {category} | Priority: {priority}")
            output.append(f"   Completed: {task.get('created_at', '')}")
            output.append("")

    return "\n".join(output)


# Main app
st.title("📝 Simple To-Do List")
st.markdown(
    "Manage your tasks efficiently with this simple to-do list application.")

# Add new task section
st.subheader("Add New Task")
col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1.25, 0.75])

with col1:
    new_task = st.text_input("Enter a new task:",
                             placeholder="What do you need to do?",
                             label_visibility="collapsed")

with col2:
    selected_category = st.selectbox("Category:",
                                     st.session_state.categories,
                                     label_visibility="collapsed")

with col3:
    selected_priority = st.selectbox("Priority:",
                                     st.session_state.priorities,
                                     index=1,
                                     label_visibility="collapsed")

with col4:
    selected_due_date = st.date_input("Due Date:",
                                      value=None,
                                      label_visibility="collapsed")

with col5:
    if st.button("Add Task", type="primary"):
        if add_task(new_task, selected_category, selected_priority,
                    selected_due_date):
            st.success("Task added successfully!")
            st.rerun()
        else:
            st.error("Please enter a valid task.")

# Display tasks section
st.subheader("Your Tasks")

if not st.session_state.tasks:
    st.info("No tasks yet. Add your first task above!")
else:
    # Task statistics
    total_tasks = len(st.session_state.tasks)
    completed_tasks = len(
        [task for task in st.session_state.tasks if task['completed']])
    pending_tasks = total_tasks - completed_tasks

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Tasks", total_tasks)
    with col2:
        st.metric("Completed", completed_tasks)
    with col3:
        st.metric("Pending", pending_tasks)

    st.divider()

    # Search functionality
    search_query = st.text_input("🔍 Search tasks:",
                                 placeholder="Search by task content...",
                                 key="search_input")

    # Filter options
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        status_filter = st.selectbox("Filter by status:",
                                     ["All", "Pending", "Completed"])
    with col2:
        category_filter = st.selectbox("Filter by category:",
                                       ["All Categories"] +
                                       st.session_state.categories)
    with col3:
        priority_filter = st.selectbox("Filter by priority:",
                                       ["All Priorities"] +
                                       st.session_state.priorities)
    with col4:
        due_date_filter = st.selectbox(
            "Filter by due date:",
            ["All", "Overdue", "Due Today", "Due This Week", "No Due Date"])

    # Filter tasks based on selection
    filtered_tasks = st.session_state.tasks

    # Filter by search query
    if search_query and search_query.strip():
        query = search_query.strip().lower()
        filtered_tasks = [
            task for task in filtered_tasks
            if query in task.get('text', '').lower()
            or query in task.get('category', '').lower()
            or query in task.get('priority', '').lower()
        ]

    # Filter by status
    if status_filter == "Pending":
        filtered_tasks = [
            task for task in filtered_tasks if not task['completed']
        ]
    elif status_filter == "Completed":
        filtered_tasks = [task for task in filtered_tasks if task['completed']]

    # Filter by category
    if category_filter != "All Categories":
        filtered_tasks = [
            task for task in filtered_tasks
            if task.get('category', 'Personal') == category_filter
        ]

    # Filter by priority
    if priority_filter != "All Priorities":
        filtered_tasks = [
            task for task in filtered_tasks
            if task.get('priority', 'Medium') == priority_filter
        ]

    # Filter by due date
    if due_date_filter != "All":
        if due_date_filter == "Overdue":
            filtered_tasks = [
                task for task in filtered_tasks if is_overdue(task)
            ]
        elif due_date_filter == "Due Today":
            today = date.today()
            filtered_tasks = [
                task for task in filtered_tasks
                if task.get('due_date') and datetime.strptime(
                    task['due_date'], "%Y-%m-%d").date() == today
            ]
        elif due_date_filter == "Due This Week":
            today = date.today()
            week_end = today + timedelta(days=(6 - today.weekday()))
            filtered_tasks = [
                task for task in filtered_tasks
                if task.get('due_date') and today <= datetime.strptime(
                    task['due_date'], "%Y-%m-%d").date() <= week_end
            ]
        elif due_date_filter == "No Due Date":
            filtered_tasks = [
                task for task in filtered_tasks if not task.get('due_date')
            ]

    # Sort by overdue status first, then priority, then due date, then creation time
    def sort_key(task):
        overdue = is_overdue(task)
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        priority_value = priority_order.get(task.get('priority', 'Medium'), 1)

        # Due date handling for sorting
        due_date_value = "9999-12-31"  # Default for tasks without due dates
        if task.get('due_date'):
            due_date_value = task['due_date']

        return (
            0 if overdue else 1,  # Overdue tasks first
            priority_value,  # Then by priority
            due_date_value,  # Then by due date
            task.get('created_at', '')  # Finally by creation time
        )

    filtered_tasks.sort(key=sort_key)

    # Export functionality
    if filtered_tasks:
        st.divider()
        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            csv_data = export_to_csv(filtered_tasks)
            st.download_button(
                label="📊 Export as CSV",
                data=csv_data,
                file_name=f"tasks_export_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                help="Download current filtered tasks as CSV file"
            )

        with col2:
            text_data = export_to_text(filtered_tasks)
            st.download_button(
                label="📄 Export as Text",
                data=text_data,
                file_name=f"tasks_export_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                help="Download current filtered tasks as text file"
            )

        with col3:
            st.caption(
                f"Export will include {len(filtered_tasks)} task(s) currently displayed")

    if not filtered_tasks:
        if (status_filter == "All" and category_filter == "All Categories"
                and priority_filter == "All Priorities"
                and due_date_filter == "All"):
            st.info("No tasks found.")
        else:
            st.info(f"No tasks found matching the selected filters.")
    else:
        # Display tasks
        for i, task in enumerate(filtered_tasks):
            col1, col2, col3 = st.columns([0.5, 4, 1])

            with col1:
                # Checkbox for completion status
                is_completed = st.checkbox("Complete",
                                           value=task['completed'],
                                           key=f"checkbox_{task['id']}",
                                           label_visibility="collapsed")

                # Update completion status if changed
                if is_completed != task['completed']:
                    toggle_task_completion(task['id'])
                    st.rerun()

            with col2:
                # Category and priority badges
                category = task.get('category', 'Personal')
                priority = task.get('priority', 'Medium')
                due_date = task.get('due_date')
                overdue = is_overdue(task)

                category_colors = {
                    'Personal': '🔵',
                    'Work': '🟢',
                    'Shopping': '🟡',
                    'Health': '🔴'
                }
                priority_indicators = {
                    'High': '🔴 **HIGH**',
                    'Medium': '🟡 **MED**',
                    'Low': '🟢 **LOW**'
                }

                category_icon = category_colors.get(category, '⚪')
                priority_badge = priority_indicators.get(priority, '🟡 **MED**')

                # Due date formatting
                due_date_text = ""
                if due_date:
                    try:
                        due_date_obj = datetime.strptime(due_date,
                                                         "%Y-%m-%d").date()
                        due_date_formatted = due_date_obj.strftime("%m/%d")
                        if overdue:
                            due_date_text = f" | ⚠️ **OVERDUE** ({due_date_formatted})"
                        else:
                            days_until_due = (due_date_obj - date.today()).days
                            if days_until_due == 0:
                                due_date_text = f" | 📅 **DUE TODAY**"
                            elif days_until_due == 1:
                                due_date_text = f" | 📅 Due tomorrow"
                            else:
                                due_date_text = f" | 📅 Due {due_date_formatted}"
                    except (ValueError, TypeError):
                        pass

                # Task text with strikethrough if completed
                if task['completed']:
                    st.markdown(
                        f"{priority_badge} | {category_icon} **{category}**{due_date_text} | ~~{task['text']}~~ *(completed on {task['created_at']})*"
                    )
                else:
                    if overdue:
                        st.markdown(
                            f"🚨 {priority_badge} | {category_icon} **{category}**{due_date_text} | **{task['text']}** *(created on {task['created_at']})*",
                            unsafe_allow_html=True)
                    else:
                        st.markdown(
                            f"{priority_badge} | {category_icon} **{category}**{due_date_text} | {task['text']} *(created on {task['created_at']})*"
                        )

            with col3:
                # Delete button
                if st.button("🗑️",
                             key=f"delete_{task['id']}",
                             help="Delete task"):
                    delete_task(task['id'])
                    st.rerun()

        # Bulk actions
        st.divider()
        col1, col2 = st.columns(2)

        with col1:
            if completed_tasks > 0:
                if st.button("Clear Completed Tasks", type="secondary"):
                    clear_completed_tasks()
                    st.success("Completed tasks cleared!")
                    st.rerun()

        with col2:
            if st.button("Clear All Tasks", type="secondary"):
                if st.button("Confirm Clear All",
                             type="secondary",
                             key="confirm_clear"):
                    st.session_state.tasks = []
                    st.success("All tasks cleared!")
                    st.rerun()

# Footer
st.divider()
st.markdown("*Made with Streamlit* ❤️")

import tkinter as tk
from tkinter import messagebox, Toplevel
from tkcalendar import Calendar
from datetime import datetime

# List to store tasks
tasks = []

def show_main_menu():
    """Displays the main menu with action buttons."""
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="To-Do List Manager", font=("Arial", 16)).pack(pady=10)
    
    tk.Button(root, text="Add Task", width=20, command=show_add_task).pack(pady=5)
    tk.Button(root, text="Edit Task", width=20, command=show_edit_task).pack(pady=5)
    tk.Button(root, text="View Tasks", width=20, command=show_view_tasks).pack(pady=5)
    tk.Button(root, text="Close", width=20, command=root.quit).pack(pady=5)

def show_add_task():
    """Opens a window to add a new task."""
    add_win = Toplevel(root)
    add_win.title("Add Task")
    add_win.geometry("400x400")

    tk.Label(add_win, text="Task Name:").pack()
    task_entry = tk.Entry(add_win, width=40)
    task_entry.pack()

    tk.Label(add_win, text="Select Date:").pack()
    cal = Calendar(add_win, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.pack()

    tk.Label(add_win, text="Enter Time (HH:MM):").pack()
    time_frame = tk.Frame(add_win)
    time_frame.pack()
    
    hour_entry = tk.Entry(time_frame, width=5)
    hour_entry.pack(side=tk.LEFT)
    tk.Label(time_frame, text=":").pack(side=tk.LEFT)
    minute_entry = tk.Entry(time_frame, width=5)
    minute_entry.pack(side=tk.LEFT)

    def add_task():
        """Validates and adds a new task."""
        task_text = task_entry.get()
        task_date = cal.get_date()
        hour = hour_entry.get()
        minute = minute_entry.get()

        if task_text and hour.isdigit() and minute.isdigit():
            hour, minute = int(hour), int(minute)
            if 0 <= hour < 24 and 0 <= minute < 60:
                scheduled_time = datetime.strptime(f"{task_date} {hour:02d}:{minute:02d}", "%Y-%m-%d %H:%M")
                tasks.append((task_text, scheduled_time))
                messagebox.showinfo("Success", f"Task '{task_text}' added.")
                add_win.destroy()
            else:
                messagebox.showerror("Invalid Time", "Enter a valid hour in 24-hour format.")
        else:
            messagebox.showerror("Missing Information", "Enter task and valid time.")

    tk.Button(add_win, text="Save Task", command=add_task).pack(pady=5)

def show_view_tasks():
    """Displays all tasks with a delete option."""
    view_win = Toplevel(root)
    view_win.title("View Tasks")
    view_win.geometry("400x400")

    if not tasks:
        tk.Label(view_win, text="No tasks available.").pack()
        return

    tk.Label(view_win, text="Your Tasks:").pack()
    task_listbox = tk.Listbox(view_win, width=50, height=10)
    task_listbox.pack()

    for task, scheduled_time in tasks:
        task_listbox.insert(tk.END, f"{task} - {scheduled_time.strftime('%Y-%m-%d %H:%M')}")

    def delete_task():
        """Deletes the selected task."""
        selected = task_listbox.curselection()
        if not selected:
            messagebox.showerror("No Selection", "Select a task to delete.")
            return

        index = selected[0]
        tasks.pop(index)
        messagebox.showinfo("Success", "Task deleted.")
        view_win.destroy()
        show_view_tasks()

    tk.Button(view_win, text="Delete Selected Task", command=delete_task).pack(pady=5)

def show_edit_task():
    """Opens a window to edit an existing task."""
    edit_win = Toplevel(root)
    edit_win.title("Edit Task")
    edit_win.geometry("400x400")

    if not tasks:
        tk.Label(edit_win, text="No tasks to edit.").pack()
        return

    tk.Label(edit_win, text="Select Task to Edit:").pack()
    task_listbox = tk.Listbox(edit_win, width=50, height=10)
    task_listbox.pack()

    for task, scheduled_time in tasks:
        task_listbox.insert(tk.END, f"{task} - {scheduled_time.strftime('%Y-%m-%d %H:%M')}")

    def edit_selected_task():
        """Allows editing of a selected task."""
        selected = task_listbox.curselection()
        if not selected:
            messagebox.showerror("No Selection", "Select a task to edit.")
            return

        index = selected[0]
        old_task, old_time = tasks[index]

        edit_task_win = Toplevel(edit_win)
        edit_task_win.title("Edit Task")
        edit_task_win.geometry("400x400")

        tk.Label(edit_task_win, text="Task Name:").pack()
        task_entry = tk.Entry(edit_task_win, width=40)
        task_entry.insert(0, old_task)
        task_entry.pack()

        tk.Label(edit_task_win, text="Select New Date:").pack()
        cal = Calendar(edit_task_win, selectmode="day", date_pattern="yyyy-mm-dd")
        cal.pack()

        tk.Label(edit_task_win, text="Enter New Time (HH:MM):").pack()
        time_frame = tk.Frame(edit_task_win)
        time_frame.pack()
        
        hour_entry = tk.Entry(time_frame, width=5)
        hour_entry.insert(0, old_time.strftime('%H'))
        hour_entry.pack(side=tk.LEFT)
        tk.Label(time_frame, text=":").pack(side=tk.LEFT)
        minute_entry = tk.Entry(time_frame, width=5)
        minute_entry.insert(0, old_time.strftime('%M'))
        minute_entry.pack(side=tk.LEFT)

        def save_edits():
            """Validates and saves task edits."""
            new_task = task_entry.get()
            new_date = cal.get_date()
            new_hour = hour_entry.get()
            new_minute = minute_entry.get()

            if new_hour.isdigit() and new_minute.isdigit():
                new_hour, new_minute = int(new_hour), int(new_minute)
                if 0 <= new_hour < 24 and 0 <= new_minute < 60:
                    new_scheduled_time = datetime.strptime(f"{new_date} {new_hour:02d}:{new_minute:02d}", "%Y-%m-%d %H:%M")
                    tasks[index] = (new_task, new_scheduled_time)
                    messagebox.showinfo("Success", "Task updated.")
                    edit_task_win.destroy()
                    edit_win.destroy()
                else:
                    messagebox.showerror("Invalid Time", "Enter a valid hour in 24-hour format.")
            else:
                messagebox.showerror("Invalid Input", "Enter numeric values.")

        tk.Button(edit_task_win, text="Save Changes", command=save_edits).pack(pady=5)

    tk.Button(edit_win, text="Edit Selected Task", command=edit_selected_task).pack(pady=5)

# Main GUI Setup
root = tk.Tk()
root.title("To-Do List Manager")
root.geometry("400x300")
show_main_menu()
root.mainloop()

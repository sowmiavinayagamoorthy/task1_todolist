import tkinter as tk
from tkinter import messagebox
import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List Application")
        self.tasks = {}
        self.completed_tasks = {}

        # Create and set up GUI components
        self.task_entry = tk.Entry(root, width=50, borderwidth=3, relief="groove", bg="light yellow")
        self.task_entry.grid(row=0, column=0, padx=10, pady=10)

        add_button = tk.Button(root, text="Add Task", command=self.add_task, bg="red", fg="white", borderwidth=3, relief="groove")
        add_button.grid(row=0, column=1, padx=10, pady=10)

        delete_button = tk.Button(root, text="Delete Selected Task", command=self.delete_selected_task, bg="red", fg="white", borderwidth=3, relief="groove")
        delete_button.grid(row=2, column=0, padx=10, pady=10)

        mark_completed_button = tk.Button(root, text="Mark as Completed", command=self.mark_as_completed, bg="red", fg="white", borderwidth=3, relief="groove")
        mark_completed_button.grid(row=2, column=1, padx=10, pady=10)

        show_completed_button = tk.Button(root, text="Show Completed Tasks", command=self.show_completed_tasks, bg="red", fg="white", borderwidth=2, relief="groove")
        show_completed_button.grid(row=2, column=2, padx=10, pady=10)
        # Text field to display incomplete tasks with checkboxes
        self.tasks_text = tk.Text(root, width=50, height=15, borderwidth=3, relief="groove", bg="light yellow")
        self.tasks_text.grid(row=1, column=0, padx=10, pady=10, columnspan=3)

        # Text field to display completed tasks
        self.completed_text = tk.Text(root, width=50, height=15, state=tk.DISABLED, borderwidth=3, relief="groove", bg="light yellow")
        self.completed_text.grid(row=3, column=0, padx=10, pady=10, columnspan=3)

        # Variable to store the state of checkboxes
        self.task_vars = {}

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks[task] = False
            self.update_tasks_text()
            messagebox.showinfo("Task Added", f'Task "{task}" added.')
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Empty Task", "Please enter a task.")

    def delete_selected_task(self):
        selected_tasks = [task for task, var in self.task_vars.items() if var.get()]
        for task in selected_tasks:
            del self.tasks[task]
        self.update_tasks_text()
        messagebox.showinfo("Tasks Deleted", f'Selected tasks deleted.')

    def show_completed_tasks(self):
        today = datetime.date.today()
        history_text = "Completed tasks history for the last week:\n"
        for task, completed_date in self.completed_tasks.items():
            completed_date = datetime.datetime.strptime(completed_date, "%Y-%m-%d %H:%M:%S").date()
            if (today - completed_date).days <= 7:
                history_text += f'{task} - Completed on: {completed_date}\n'

        if history_text == "Completed tasks history for the last week:\n":
            history_text += "No completed tasks in the last week."

        self.completed_text.config(state=tk.NORMAL)
        self.completed_text.delete("1.0", tk.END)
        self.completed_text.insert(tk.END, history_text)
        self.completed_text.config(state=tk.DISABLED)

    def update_tasks_text(self):
        # Clear existing text
        self.tasks_text.delete("1.0", tk.END)

        # Create checkboxes for each incomplete task
        self.task_vars = {}
        for task in self.tasks.keys():
            var = tk.BooleanVar()
            self.task_vars[task] = var
            task_checkbox = tk.Checkbutton(self.tasks_text, text=task, variable=var, wraplength=300, justify=tk.LEFT)
            self.tasks_text.window_create(tk.END, window=task_checkbox)
            self.tasks_text.insert(tk.END, "\n")

    def mark_as_completed(self):
        selected_tasks = [task for task, var in self.task_vars.items() if var.get()]
        for task in selected_tasks:
            self.tasks.pop(task, None)
            self.completed_tasks[task] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.update_tasks_text()
        messagebox.showinfo("Tasks Completed", "Selected tasks marked as completed.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

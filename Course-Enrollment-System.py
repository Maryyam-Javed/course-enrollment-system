import tkinter as tk
from tkinter import messagebox

# ===================== AVL TREE =====================
class AVLNode:
    def __init__(self, reg_no, name, semester, department):
        self.reg_no = reg_no
        self.name = name
        self.semester = semester
        self.department = department
        self.courses = []
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right)

    def right_rotate(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))

        return x

    def left_rotate(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def insert(self, root, reg_no, name, semester, department):
        if not root:
            return AVLNode(reg_no, name, semester, department)

        if reg_no < root.reg_no:
            root.left = self.insert(root.left, reg_no, name, semester, department)
        elif reg_no > root.reg_no:
            root.right = self.insert(root.right, reg_no, name, semester, department)
        else:
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and reg_no < root.left.reg_no:
            return self.right_rotate(root)

        if balance < -1 and reg_no > root.right.reg_no:
            return self.left_rotate(root)

        if balance > 1 and reg_no > root.left.reg_no:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        if balance < -1 and reg_no < root.right.reg_no:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def inorder(self, root, result):
        if root:
            self.inorder(root.left, result)
            result.append(root)
            self.inorder(root.right, result)


# ===================== SORTING =====================
def selection_sort(students):
    for i in range(len(students)):
        min_idx = i
        for j in range(i + 1, len(students)):
            if students[j].name.lower() < students[min_idx].name.lower():
                min_idx = j
        students[i], students[min_idx] = students[min_idx], students[i]
    return students


def merge_sort(courses):
    if len(courses) <= 1:
        return courses

    mid = len(courses) // 2
    left = merge_sort(courses[:mid])
    right = merge_sort(courses[mid:])

    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i][1] > right[j][1]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ===================== MAIN APP =====================
tree = AVLTree()
root_node = None
course_count = {}


# ---------------- FUNCTIONS ----------------
def add_student():
    global root_node

    if not reg_entry.get().isdigit():
        messagebox.showerror("Error", "Student Reg No must be numeric")
        return

    root_node = tree.insert(
        root_node,
        int(reg_entry.get()),
        name_entry.get(),
        semester_entry.get(),
        department_entry.get()
    )

    messagebox.showinfo("Success", "Student Added Successfully")

    reg_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    semester_entry.delete(0, tk.END)
    department_entry.delete(0, tk.END)


def add_course():
    if not course_reg_entry.get().isdigit():
        messagebox.showerror("Error", "Invalid Student Reg No")
        return

    reg_no = int(course_reg_entry.get())
    course = course_entry.get()

    students = []
    tree.inorder(root_node, students)

    for s in students:
        if s.reg_no == reg_no:
            s.courses.append(course)
            course_count[course] = course_count.get(course, 0) + 1
            messagebox.showinfo("Success", "Course Enrolled")
            return

    messagebox.showerror("Error", "Student Not Found")


def show_students():
    students = []
    tree.inorder(root_node, students)
    sorted_students = selection_sort(students)

    output.delete("1.0", tk.END)
    output.insert(tk.END, "STUDENT LIST (A-Z)\n" + "-" * 60 + "\n")

    for s in sorted_students:
        output.insert(
            tk.END,
            f"{s.reg_no} | {s.name} | Semester: {s.semester} | Dept: {s.department} | Courses: {s.courses}\n"
        )

    output.insert(tk.END, f"\nTotal Students: {len(sorted_students)}")


def show_courses():
    sorted_courses = merge_sort(list(course_count.items()))

    output.delete("1.0", tk.END)
    output.insert(tk.END, "COURSE POPULARITY\n" + "-" * 40 + "\n")

    for c in sorted_courses:
        output.insert(tk.END, f"{c[0]} → {c[1]} students\n")


def clear_output():
    output.delete("1.0", tk.END)


# ===================== GUI =====================
root = tk.Tk()
root.title("Online Course Enrollment Manager")
root.geometry("620x680")
root.resizable(False, False)

PRIMARY = "#1f4ed8"
BG_COLOR = "#f4f6fb"
CARD_COLOR = "#ffffff"
INPUT_BG = "#eef1f7"
TEXT_BG = "#0f172a"
TEXT_FG = "#e5e7eb"

root.configure(bg=BG_COLOR)

tk.Label(
    root,
    text="Online Course Enrollment Manager",
    font=("Segoe UI", 17, "bold"),
    fg=PRIMARY,
    bg=BG_COLOR
).pack(pady=12)

frame = tk.Frame(root, bg=CARD_COLOR, padx=20, pady=15)
frame.pack()

font_lbl = ("Segoe UI", 11)
font_btn = ("Segoe UI", 10, "bold")

# Inputs
tk.Label(frame, text="Student Reg No", bg=CARD_COLOR).grid(row=0, column=0)
tk.Label(frame, text="Student Name", bg=CARD_COLOR).grid(row=1, column=0)
tk.Label(frame, text="Semester", bg=CARD_COLOR).grid(row=2, column=0)
tk.Label(frame, text="Department", bg=CARD_COLOR).grid(row=3, column=0)

reg_entry = tk.Entry(frame, bg=INPUT_BG)
name_entry = tk.Entry(frame, bg=INPUT_BG)
semester_entry = tk.Entry(frame, bg=INPUT_BG)
department_entry = tk.Entry(frame, bg=INPUT_BG)

reg_entry.grid(row=0, column=1)
name_entry.grid(row=1, column=1)
semester_entry.grid(row=2, column=1)
department_entry.grid(row=3, column=1)

tk.Button(frame, text="Add Student", command=add_student, bg=PRIMARY, fg="white").grid(row=4, columnspan=2)


# Course
tk.Label(frame, text="Student Reg No", bg=CARD_COLOR).grid(row=5, column=0)
tk.Label(frame, text="Course Name", bg=CARD_COLOR).grid(row=6, column=0)

course_reg_entry = tk.Entry(frame, bg=INPUT_BG)
course_entry = tk.Entry(frame, bg=INPUT_BG)

course_reg_entry.grid(row=5, column=1)
course_entry.grid(row=6, column=1)

tk.Button(frame, text="Add Course", command=add_course, bg=PRIMARY, fg="white").grid(row=7, columnspan=2)


# Buttons
btn_frame = tk.Frame(root, bg=BG_COLOR)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Show Students", command=show_students, bg=PRIMARY, fg="white").grid(row=0, column=0)
tk.Button(btn_frame, text="Course Stats", command=show_courses, bg=PRIMARY, fg="white").grid(row=0, column=1)
tk.Button(btn_frame, text="Clear", command=clear_output, bg=PRIMARY, fg="white").grid(row=0, column=2)


# Output
output = tk.Text(root, height=15, width=70, bg=TEXT_BG, fg=TEXT_FG)
output.pack(pady=10)

root.mainloop()
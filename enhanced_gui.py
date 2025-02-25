import tkinter as tk
from tkinter import ttk, messagebox
from enhanced_attendance import EnhancedAttendanceSystem
import datetime

class AttendanceSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Attendance System")
        self.root.geometry("800x600")
        self.attendance_system = EnhancedAttendanceSystem()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create tabs
        self.enroll_tab = ttk.Frame(self.notebook)
        self.attendance_tab = ttk.Frame(self.notebook)
        self.view_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.enroll_tab, text='Enroll Student')
        self.notebook.add(self.attendance_tab, text='Mark Attendance')
        self.notebook.add(self.view_tab, text='View Attendance')
        
        self.setup_enroll_tab()
        self.setup_attendance_tab()
        self.setup_view_tab()
        
    def setup_enroll_tab(self):
        # Student enrollment form
        ttk.Label(self.enroll_tab, text="Student Enrollment", font=('Helvetica', 16, 'bold')).pack(pady=10)
        
        form_frame = ttk.Frame(self.enroll_tab)
        form_frame.pack(pady=20)
        
        # Entry fields
        self.student_id = tk.StringVar()
        self.student_name = tk.StringVar()
        self.gender = tk.StringVar()
        self.program = tk.StringVar()
        self.course_id = tk.StringVar()
        
        ttk.Label(form_frame, text="Student ID:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.student_id).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.student_name).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Gender:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Combobox(form_frame, textvariable=self.gender, values=['Male', 'Female']).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Program:").grid(row=3, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.program).grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Course ID:").grid(row=4, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.course_id).grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Button(form_frame, text="Enroll Student", command=self.enroll_student).grid(row=5, column=0, columnspan=2, pady=20)
        
    def setup_attendance_tab(self):
        ttk.Label(self.attendance_tab, text="Mark Attendance", font=('Helvetica', 16, 'bold')).pack(pady=10)
        
        # Course selection for attendance
        frame = ttk.Frame(self.attendance_tab)
        frame.pack(pady=20)
        
        self.attendance_course_id = tk.StringVar()
        ttk.Label(frame, text="Course ID:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.attendance_course_id).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(frame, text="Start Attendance", command=self.start_attendance).grid(row=1, column=0, columnspan=2, pady=20)
        
    def setup_view_tab(self):
        ttk.Label(self.view_tab, text="View Attendance", font=('Helvetica', 16, 'bold')).pack(pady=10)
        
        frame = ttk.Frame(self.view_tab)
        frame.pack(pady=20)
        
        self.view_course_id = tk.StringVar()
        self.view_date = tk.StringVar()
        
        ttk.Label(frame, text="Course ID:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.view_course_id).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.view_date).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(frame, text="View Attendance", command=self.view_attendance).grid(row=2, column=0, columnspan=2, pady=20)
        
        # Treeview for attendance display
        self.tree = ttk.Treeview(self.view_tab, columns=('Student ID', 'Course ID', 'Date', 'Status', 'Left Time', 'Return Time'))
        self.tree.heading('Student ID', text='Student ID')
        self.tree.heading('Course ID', text='Course ID')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Status', text='Status')
        self.tree.heading('Left Time', text='Left Time')
        self.tree.heading('Return Time', text='Return Time')
        self.tree.pack(pady=10, padx=10, fill='both', expand=True)
        
    def enroll_student(self):
        try:
            success, message = self.attendance_system.enroll_student(
                int(self.student_id.get()),
                self.student_name.get(),
                self.gender.get(),
                self.program.get(),
                self.course_id.get()
            )
            messagebox.showinfo("Enrollment", message)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def start_attendance(self):
        try:
            success, message = self.attendance_system.mark_attendance(self.attendance_course_id.get())
            messagebox.showinfo("Attendance", message)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def view_attendance(self):
        try:
            success, data = self.attendance_system.view_attendance(
                self.view_course_id.get(),
                self.view_date.get() if self.view_date.get() else None
            )
            
            if success:
                # Clear existing items
                for item in self.tree.get_children():
                    self.tree.delete(item)
                    
                # Add new data
                for _, row in data.iterrows():
                    self.tree.insert('', 'end', values=(
                        row['Student_ID'],
                        row['Course_ID'],
                        row['Date'],
                        row['Status'],
                        row['Left_Time'],
                        row['Return_Time']
                    ))
            else:
                messagebox.showinfo("Attendance", data)
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceSystemGUI(root)
    root.mainloop()

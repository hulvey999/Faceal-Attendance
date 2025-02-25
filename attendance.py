from tkinter import *
import tkinter as tk
import cv2
import os
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
from tkinter import messagebox
import pyttsx3
import csv
import math
from tkinter import ttk
from openpyxl import Workbook, load_workbook
import threading

def text_to_speech(message):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)
    engine.say(message)
    engine.runAndWait()

def check_login(username, password, login_window, root):
    if username.get() == "admin" and password.get() == "admin123":
        text_to_speech("Login Successful")
        login_window.destroy()
        root.deiconify()  # Show the main window
    else:
        messagebox.showerror("Error", "Invalid Username or Password")
        text_to_speech("Invalid Username or Password")

def login_window():
    root = Tk()
    root.withdraw()  # Hide the main window until login is successful
    
    login = Toplevel()
    login.title("Login")
    login.geometry("340x440")
    login.configure(background="#1a1a1a")
    login.resizable(0, 0)

    # Title
    title = Label(
        login,
        text="Login System",
        bg="#1a1a1a",
        fg="#00ff88",
        font=("times new roman", 30, "bold")
    )
    title.pack(pady=50)

    # Login frame
    login_frame = Frame(login, bg="#1a1a1a")
    login_frame.pack(pady=20)

    # Username
    Label(
        login_frame,
        text="Username",
        bg="#1a1a1a",
        fg="#f0f0f0",
        font=("times new roman", 12)
    ).grid(row=0, column=0, padx=10, pady=5)
    
    username = Entry(
        login_frame,
        bg="#2d2d2d",
        fg="#f0f0f0",
        font=("times new roman", 12),
        relief="flat"
    )
    username.grid(row=0, column=1, padx=10, pady=5)

    # Password
    Label(
        login_frame,
        text="Password",
        bg="#1a1a1a",
        fg="#f0f0f0",
        font=("times new roman", 12)
    ).grid(row=1, column=0, padx=10, pady=5)
    
    password = Entry(
        login_frame,
        bg="#2d2d2d",
        fg="#f0f0f0",
        font=("times new roman", 12),
        relief="flat",
        show="*"
    )
    password.grid(row=1, column=1, padx=10, pady=5)

    # Login button
    login_btn = Button(
        login,
        text="Login",
        command=lambda: check_login(username, password, login, root),
        font=("times new roman", 14),
        bg="#2d2d2d",
        fg="#00ff88",
        relief="flat",
        padx=20,
        pady=10,
        width=15
    )
    login_btn.pack(pady=20)

    login.mainloop()

def check_admin_login():
    login = Toplevel()
    login.title("Admin Login")
    login.geometry("500x600")
    login.configure(background="#1a1a1a")
    login.resizable(0, 0)
    login.grab_set()

    # Center the window
    window_width = 500
    window_height = 600
    screen_width = login.winfo_screenwidth()
    screen_height = login.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    login.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Title
    title = Label(
        login,
        text="Admin Login",
        bg="#1a1a1a",
        fg="#00ff88",
        font=("times new roman", 35, "bold")
    )
    title.pack(pady=50)

    # Login frame
    login_frame = Frame(login, bg="#1a1a1a")
    login_frame.pack(expand=True)

    # Username
    Label(
        login_frame,
        text="Username",
        bg="#1a1a1a",
        fg="#f0f0f0",
        font=("times new roman", 16)
    ).grid(row=0, column=0, padx=10, pady=15, sticky='e')
    
    username = Entry(
        login_frame,
        bg="#2d2d2d",
        fg="#f0f0f0",
        font=("times new roman", 16),
        relief="flat",
        width=20
    )
    username.grid(row=0, column=1, padx=10, pady=15)
    username.insert(0, "admin")

    # Password
    Label(
        login_frame,
        text="Password",
        bg="#1a1a1a",
        fg="#f0f0f0",
        font=("times new roman", 16)
    ).grid(row=1, column=0, padx=10, pady=15, sticky='e')
    
    password = Entry(
        login_frame,
        bg="#2d2d2d",
        fg="#f0f0f0",
        font=("times new roman", 16),
        relief="flat",
        show="*",
        width=20
    )
    password.grid(row=1, column=1, padx=10, pady=15)

    def verify_login(event=None):
        if username.get() == "admin" and password.get() == "12345":
            text_to_speech("Access granted")
            login.destroy()
            TakeImageUI()
        else:
            messagebox.showerror("Error", "Invalid Username or Password")
            text_to_speech("Access denied")
            password.delete(0, END)
            password.focus()

    # Button frame
    button_frame = Frame(login, bg="#1a1a1a")
    button_frame.pack(expand=True)

    # Login button
    login_btn = Button(
        button_frame,
        text="Login",
        command=verify_login,
        font=("times new roman", 18, "bold"),
        bg="#2d2d2d",
        fg="#00ff88",
        relief="flat",
        cursor="hand2",
        width=15,
        height=1
    )
    login_btn.pack(pady=20)

    # Bind Enter key to verify_login for both username and password fields
    username.bind('<Return>', verify_login)
    password.bind('<Return>', verify_login)

    # Hover effects
    def on_enter(e):
        e.widget.configure(bg="#404040")

    def on_leave(e):
        e.widget.configure(bg="#2d2d2d")

    login_btn.bind('<Enter>', on_enter)
    login_btn.bind('<Leave>', on_leave)

def main():
    root = Tk()
    root.title("Face Recognition Attendance System")
    root.geometry("1280x720")
    root.configure(background="#1a1a1a")
    root.resizable(False, False)

    # Play welcome message
    def play_welcome():
        text_to_speech("Welcome to the future of Student attendance")
    root.after(500, play_welcome)

    # Title
    title = Label(
        root,
        text="Face Recognition Attendance System",
        bg="#1a1a1a",
        fg="#00ff88",
        font=("times new roman", 35, "bold")
    )
    title.pack(pady=40)

    # Button Frame
    button_frame = Frame(root, bg="#1a1a1a")
    button_frame.pack(expand=True)

    # Button style
    button_style = {
        "font": ("times new roman", 15, "bold"),
        "bg": "#2d2d2d",
        "fg": "#00ff88",
        "relief": "flat",
        "width": 20,
        "height": 2,
        "cursor": "hand2"
    }

    register_btn = Button(
        button_frame,
        text="Register New Student",
        command=check_admin_login,  # Changed to check_admin_login
        **button_style
    )
    register_btn.pack(pady=20)

    take_attendance_btn = Button(
        button_frame,
        text="Take Attendance",
        command=take_attendance_page,
        **button_style
    )
    take_attendance_btn.pack(pady=20)

    view_attendance_btn = Button(
        button_frame,
        text="View Attendance",
        command=lambda: print("View Attendance clicked"),
        **button_style
    )
    view_attendance_btn.pack(pady=20)

    # Add hover effects
    def on_enter(e):
        e.widget.configure(bg="#404040")

    def on_leave(e):
        e.widget.configure(bg="#2d2d2d")

    for btn in [register_btn, take_attendance_btn, view_attendance_btn]:
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)

    root.mainloop()

def testVal(inStr, acttyp):
    if acttyp == '1':  # insert
        if not inStr.isdigit():
            return False
    return True

def TakeImageUI():
    ImageUI = Tk()
    ImageUI.title("Student Registration")
    ImageUI.geometry("780x480")
    ImageUI.configure(background="#1a1a1a")
    ImageUI.resizable(0, 0)
    
    # Title section
    header = tk.Label(
        ImageUI, 
        text="Enter Your Details", 
        bg="#1a1a1a", 
        fg="#00ff88",
        font=("times new roman", 30, "bold")
    )
    header.pack(pady=20)

    # Form container
    form_frame = tk.Frame(ImageUI, bg="#1a1a1a")
    form_frame.pack(pady=20)

    # Enrollment Number
    tk.Label(
        form_frame,
        text="Enrollment No",
        bg="#1a1a1a",
        fg="#f0f0f0",
        font=("times new roman", 12)
    ).grid(row=0, column=0, padx=10, pady=10, sticky='e')
    
    txt1 = tk.Entry(
        form_frame,
        width=17,
        bg="#2d2d2d",
        fg="#f0f0f0",
        font=("times new roman", 25),
        relief="flat"
    )
    txt1.grid(row=0, column=1, padx=10, pady=10)
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    # Full Names
    tk.Label(
        form_frame,
        text="Full Names",
        bg="#1a1a1a",
        fg="#f0f0f0",
        font=("times new roman", 12)
    ).grid(row=1, column=0, padx=10, pady=10, sticky='e')
    
    txt2 = tk.Entry(
        form_frame,
        width=17,
        bg="#2d2d2d",
        fg="#f0f0f0",
        font=("times new roman", 25),
        relief="flat"
    )
    txt2.grid(row=1, column=1, padx=10, pady=10)

    # Gender Selection
    tk.Label(
        form_frame,
        text="Gender",
        bg="#1a1a1a",
        fg="#f0f0f0",
        font=("times new roman", 12)
    ).grid(row=2, column=0, padx=10, pady=10, sticky='e')

    # Gender Frame
    gender_frame = tk.Frame(form_frame, bg="#1a1a1a")
    gender_frame.grid(row=2, column=1, padx=10, pady=10, sticky='w')

    # Gender Variable
    gender_var = StringVar(ImageUI)

    # Radio buttons
    male_radio = tk.Radiobutton(
        gender_frame,
        text="Male",
        variable=gender_var,
        value="Male",
        bg="#1a1a1a",
        fg="#f0f0f0",
        selectcolor="#2d2d2d",
        activebackground="#1a1a1a",
        activeforeground="#00ff88",
        font=("times new roman", 12)
    )
    male_radio.pack(side=tk.LEFT, padx=20)

    female_radio = tk.Radiobutton(
        gender_frame,
        text="Female",
        variable=gender_var,
        value="Female",
        bg="#1a1a1a",
        fg="#f0f0f0",
        selectcolor="#2d2d2d",
        activebackground="#1a1a1a",
        activeforeground="#00ff88",
        font=("times new roman", 12)
    )
    female_radio.pack(side=tk.LEFT, padx=20)

    # Status Label
    status_label = tk.Label(
        ImageUI,
        text="",
        bg="#1a1a1a",
        fg="#00ff88",
        font=("times new roman", 12)
    )
    status_label.pack(pady=10)

    # Button Frame
    button_frame = tk.Frame(ImageUI, bg="#1a1a1a")
    button_frame.pack(pady=20)

    def validate_fields():
        if not txt1.get().strip():
            status_label.config(text="Please enter Enrollment Number!", fg="#ff4444")
            return False
        if not txt2.get().strip():
            status_label.config(text="Please enter Full Names!", fg="#ff4444")
            return False
        if not gender_var.get():
            status_label.config(text="Please select Gender!", fg="#ff4444")
            return False
        return True

    def open_camera():
        if not validate_fields():
            return
        
        try:
            if not os.path.exists("TrainingImage"):
                os.makedirs("TrainingImage")
            
            Enrollment = txt1.get()
            existing_images = [f for f in os.listdir("TrainingImage") if f.startswith(f"{Enrollment}.")]
            for img in existing_images:
                os.remove(os.path.join("TrainingImage", img))

            cam = cv2.VideoCapture(0)
            detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            Name = txt2.get()
            sampleNum = 0

            # Animation parameters
            scan_line_pos = 0
            scan_direction = 1
            frame_count = 0
            circle_radius = 0
            expanding = True

            # Initialize timer
            start_time = time.time()
            duration = 5
            interval = duration / 10

            # Countdown animation
            for i in range(3, 0, -1):
                status_label.config(text=f"Starting in {i}...", fg="#00ff88")
                text_to_speech(str(i))
                time.sleep(1)

            status_label.config(text="Capturing images...", fg="#00ff88")
            last_capture_time = time.time()

            while True:
                ret, img = cam.read()
                if not ret:
                    raise Exception("Cannot access camera")

                # Create a copy for animations
                display_img = img.copy()
                frame_h, frame_w = display_img.shape[:2]

                # Convert to grayscale for face detection
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)

                # Scanning animation
                scan_line_y = int(scan_line_pos * frame_h)
                cv2.line(display_img, (0, scan_line_y), (frame_w, scan_line_y), 
                        (0, 255, 0), 2)
                
                # Update scan line position
                scan_line_pos += 0.05 * scan_direction
                if scan_line_pos >= 1 or scan_line_pos <= 0:
                    scan_direction *= -1

                if len(faces) == 0:
                    # Pulsing "Searching" text when no face detected
                    pulse_val = int(127 * math.sin(frame_count * 0.1) + 127)
                    cv2.putText(display_img, "Searching for face...", (50, 50),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, pulse_val, pulse_val), 2)
                
                for (x, y, w, h) in faces:
                    # Animated rectangle around face
                    thickness = int(2 + math.sin(frame_count * 0.1) * 2)
                    cv2.rectangle(display_img, (x, y), (x+w, y+h), (255, 0, 0), thickness)

                    # Corner brackets
                    l = 30  # length of corner lines
                    # Top-left
                    cv2.line(display_img, (x, y), (x + l, y), (0, 255, 0), 2)
                    cv2.line(display_img, (x, y), (x, y + l), (0, 255, 0), 2)
                    # Top-right
                    cv2.line(display_img, (x + w, y), (x + w - l, y), (0, 255, 0), 2)
                    cv2.line(display_img, (x + w, y), (x + w, y + l), (0, 255, 0), 2)
                    # Bottom-left
                    cv2.line(display_img, (x, y + h), (x + l, y + h), (0, 255, 0), 2)
                    cv2.line(display_img, (x, y + h), (x, y + h - l), (0, 255, 0), 2)
                    # Bottom-right
                    cv2.line(display_img, (x + w, y + h), (x + w - l, y + h), (0, 255, 0), 2)
                    cv2.line(display_img, (x + w, y + h), (x + w, y + h - l), (0, 255, 0), 2)

                    # Expanding circle animation when capturing
                    current_time = time.time()
                    if current_time - last_capture_time >= interval and sampleNum < 10:
                        sampleNum += 1
                        filename = f"TrainingImage/{Enrollment}.{Name}.{sampleNum}.jpg"
                        face_img = gray[y:y+h, x:x+w]
                        
                        if face_img.size > 0:
                            cv2.imwrite(filename, face_img)
                            last_capture_time = current_time
                            
                            # Reset circle animation
                            circle_radius = 0
                            expanding = True
                            
                            if os.path.exists(filename):
                                status_label.config(text=f"Captured {sampleNum}/10 images...", fg="#00ff88")
                            else:
                                raise Exception(f"Failed to save image {sampleNum}")
                        else:
                            raise Exception("Empty face image detected")

                    # Draw expanding/contracting circle
                    if expanding:
                        circle_radius += 4
                        if circle_radius >= min(w, h) // 2:
                            expanding = False
                    else:
                        circle_radius = max(0, circle_radius - 4)
                    
                    center_x = x + w//2
                    center_y = y + h//2
                    cv2.circle(display_img, (center_x, center_y), circle_radius, 
                              (0, 255, 0), 2)

                # Add capture progress bar
                progress = (sampleNum / 10) * frame_w
                cv2.rectangle(display_img, (0, frame_h-20), (int(progress), frame_h), 
                             (0, 255, 0), -1)

                # Add capture counter
                cv2.putText(display_img, f"Captures: {sampleNum}/10", 
                           (frame_w-150, frame_h-30), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.7, (0, 255, 0), 2)

                frame_count += 1
                cv2.imshow('Facial Recognition Scan', display_img)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                elif sampleNum >= 10:
                    # Success animation
                    for _ in range(30):  # Show success animation for 30 frames
                        success_img = display_img.copy()
                        cv2.putText(success_img, "Capture Complete!", 
                                  (frame_w//4, frame_h//2),
                                  cv2.FONT_HERSHEY_SIMPLEX, 1.5, 
                                  (0, 255, 0), 3)
                        cv2.imshow('Facial Recognition Scan', success_img)
                        cv2.waitKey(1)
                    break

            cam.release()
            cv2.destroyAllWindows()

            saved_images = len([f for f in os.listdir("TrainingImage") 
                              if f.startswith(f"{Enrollment}.")])
            if saved_images == 10:
                status_label.config(text="Images captured successfully! Click 'Train Image' to continue", 
                                  fg="#00ff88")
                train_btn.config(state='normal')
            else:
                raise Exception(f"Only {saved_images} images were saved")

        except Exception as e:
            messagebox.showerror("Error", f"Error capturing images: {str(e)}")
            status_label.config(text=f"Error: {str(e)}", fg="#ff4444")

    def train_images():
        debug_info = []  # List to store debugging information
        
        def log_debug(message):
            print(f"Debug: {message}")  # Print to console
            debug_info.append(message)  # Store in list
            # Update status label with latest debug info
            status_label.config(text=message, fg="#00ff88")
            status_label.update()

        try:
            log_debug("Starting training process...")

            # 1. Check directories
            if not os.path.exists("TrainingImage"):
                raise Exception("TrainingImage directory not found!")
            log_debug("TrainingImage directory found")

            if not os.path.exists("TrainingImageLabel"):
                os.makedirs("TrainingImageLabel")
                log_debug("Created TrainingImageLabel directory")

            # 2. Check for images
            image_files = [f for f in os.listdir("TrainingImage") if f.endswith('.jpg')]
            log_debug(f"Found {len(image_files)} images in TrainingImage directory")
            
            if len(image_files) == 0:
                raise Exception("No training images found!")
            
            if len(image_files) < 10:
                raise Exception(f"Insufficient training images. Found {len(image_files)}, need at least 10")

            # 3. Validate image files
            faces = []
            ids = []
            
            for img_file in image_files:
                try:
                    log_debug(f"Processing image: {img_file}")
                    
                    # Check filename format
                    parts = img_file.split('.')
                    if len(parts) < 2:
                        raise Exception(f"Invalid filename format: {img_file}")
                    
                    # Validate enrollment number
                    try:
                        enrollment = int(parts[0])
                        log_debug(f"Valid enrollment number: {enrollment}")
                    except ValueError:
                        raise Exception(f"Invalid enrollment number in filename: {img_file}")

                    # Load and validate image
                    img_path = os.path.join("TrainingImage", img_file)
                    if not os.path.exists(img_path):
                        raise Exception(f"Image file not found: {img_path}")

                    # Check file size
                    file_size = os.path.getsize(img_path)
                    if file_size == 0:
                        raise Exception(f"Empty image file: {img_path}")
                    log_debug(f"Image size: {file_size} bytes")

                    # Load image
                    PIL_img = Image.open(img_path)
                    
                    # Check image dimensions
                    width, height = PIL_img.size
                    if width < 20 or height < 20:
                        raise Exception(f"Image too small: {width}x{height}")
                    log_debug(f"Image dimensions: {width}x{height}")

                    # Convert to grayscale
                    PIL_img = PIL_img.convert('L')
                    
                    # Convert to numpy array
                    img_numpy = np.array(PIL_img, 'uint8')
                    
                    # Check array dimensions
                    if img_numpy.size == 0:
                        raise Exception("Empty image array")
                    log_debug(f"Numpy array shape: {img_numpy.shape}")

                    # Store face and ID
                    faces.append(img_numpy)
                    ids.append(enrollment)
                    
                except Exception as img_error:
                    log_debug(f"Error processing image {img_file}: {str(img_error)}")
                    raise Exception(f"Error processing image {img_file}: {str(img_error)}")

            # 4. Check processed data
            if len(faces) == 0 or len(ids) == 0:
                raise Exception("No valid faces processed")
            
            if len(faces) != len(ids):
                raise Exception(f"Mismatch: {len(faces)} faces but {len(ids)} IDs")
            
            log_debug(f"Successfully processed {len(faces)} faces")

            # 5. Train model
            try:
                log_debug("Initializing face recognizer...")
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                
                log_debug("Converting IDs to numpy array...")
                np_ids = np.array(ids)
                
                log_debug("Starting model training...")
                recognizer.train(faces, np_ids)
                
                log_debug("Saving trained model...")
                model_path = "TrainingImageLabel/Trainner.yml"
                recognizer.save(model_path)
                
                # Verify model file
                if not os.path.exists(model_path):
                    raise Exception("Model file not created")
                
                model_size = os.path.getsize(model_path)
                if model_size == 0:
                    raise Exception("Model file is empty")
                    
                log_debug(f"Model saved successfully ({model_size} bytes)")
                
            except Exception as train_error:
                raise Exception(f"Training error: {str(train_error)}")

            # 6. Success
            log_debug("Training completed successfully!")
            status_label.config(text="Model trained successfully! Click 'Save Profile' to complete", fg="#00ff88")
            save_btn.config(state='normal')
            
            # Save debug log
            with open("training_debug.log", "w") as log_file:
                log_file.write("\n".join(debug_info))

        except Exception as e:
            error_msg = f"Training failed: {str(e)}\nCheck training_debug.log for details"
            messagebox.showerror("Error", error_msg)
            status_label.config(text=error_msg, fg="#ff4444")
            
            # Save error log
            with open("training_debug.log", "w") as log_file:
                log_file.write("\n".join(debug_info))
                log_file.write(f"\nFinal Error: {str(e)}")

    def save_student_details():
        try:
            ts = time.time()
            Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            row = [txt1.get(), txt2.get(), gender_var.get(), Date, Time]
            
            if not os.path.isfile("StudentDetails/StudentDetails.csv"):
                with open("StudentDetails/StudentDetails.csv", 'a+') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(['Enrollment', 'Name', 'Gender', 'Date', 'Time'])
                    writer.writerow(row)
                csvFile.close()
            else:
                with open("StudentDetails/StudentDetails.csv", 'a+') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(row)
                csvFile.close()

            status_label.config(text="Student Details Saved Successfully!", fg="#00ff88")
            text_to_speech("Registration completed successfully")
            ImageUI.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error saving details: {str(e)}")
            status_label.config(text=f"Error: {str(e)}", fg="#ff4444")

    # Create buttons
    camera_btn = tk.Button(
        button_frame,
        text="Take a Pic",
        command=open_camera,
        font=("times new roman", 14),
        bg="#2d2d2d",
        fg="#00ff88",
        relief="flat",
        padx=20,
        pady=10,
        width=15
    )
    camera_btn.pack(side=tk.LEFT, padx=10)

    train_btn = tk.Button(
        button_frame,
        text="Train Model",
        command=train_images,
        font=("times new roman", 14),
        bg="#2d2d2d",
        fg="#00ff88",
        relief="flat",
        padx=20,
        pady=10,
        width=15,
        state='disabled'
    )
    train_btn.pack(side=tk.LEFT, padx=10)

    save_btn = tk.Button(
        button_frame,
        text="Save Details",
        command=save_student_details,
        font=("times new roman", 14),
        bg="#2d2d2d",
        fg="#00ff88",
        relief="flat",
        padx=20,
        pady=10,
        width=15,
        state='disabled'
    )
    save_btn.pack(side=tk.LEFT, padx=10)

    # Add hover effects
    for btn in [camera_btn, train_btn, save_btn]:
        btn.bind('<Enter>', lambda e, b=btn: b.configure(bg="#404040") if b['state'] != 'disabled' else None)
        btn.bind('<Leave>', lambda e, b=btn: b.configure(bg="#2d2d2d") if b['state'] != 'disabled' else None)

    ImageUI.mainloop()

def take_attendance_page():
    # Create year selection window first
    year_window = Toplevel()
    year_window.title("Select Year")
    year_window.geometry("800x600")
    year_window.configure(background="#1a1a1a")
    year_window.resizable(False, False)

    # Center the window
    window_width = 800
    window_height = 600
    screen_width = year_window.winfo_screenwidth()
    screen_height = year_window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    year_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Title with animation
    title = Label(
        year_window,
        text="Select Year of Study",
        bg="#1a1a1a",
        fg="#00ff88",
        font=("times new roman", 35, "bold")
    )
    title.pack(pady=50)

    # Year frame
    year_frame = Frame(year_window, bg="#1a1a1a")
    year_frame.pack(expand=True)

    # Button style
    button_style = {
        "font": ("times new roman", 18, "bold"),
        "bg": "#2d2d2d",
        "fg": "#00ff88",
        "relief": "flat",
        "width": 20,
        "height": 2,
        "cursor": "hand2"
    }

    def on_year_select(year):
        text_to_speech(f"Year {year} selected")
        year_window.destroy()
        show_programs_page(year)

    # Animation effects
    def on_enter(e):
        button = e.widget
        button.configure(bg="#404040")
        # Grow effect
        button.configure(width=22, height=2)

    def on_leave(e):
        button = e.widget
        button.configure(bg="#2d2d2d")
        # Shrink back
        button.configure(width=20, height=2)

    def create_animated_button(text, command):
        button = Button(
            year_frame,
            text=text,
            command=command,
            **button_style
        )
        button.pack(pady=20)
        
        # Bind hover animations
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
        
        return button

    # Create year buttons with animations
    years = ["YEAR 1", "YEAR 2", "YEAR 3", "YEAR 4"]

    # Create buttons with delay for animated appearance
    def create_buttons():
        for i, year in enumerate(years):
            year_window.after(i * 200, lambda y=year: create_animated_button(
                y, 
                lambda year=y: on_year_select(year)
            ))

    year_window.after(100, create_buttons)

    # Back button
    back_btn = Button(
        year_window,
        text="← Back",
        command=year_window.destroy,
        font=("times new roman", 12),
        bg="#2d2d2d",
        fg="#00ff88",
        relief="flat",
        cursor="hand2"
    )
    back_btn.place(x=20, y=20)

    # Add hover effects to back button
    back_btn.bind('<Enter>', lambda e: back_btn.configure(bg="#404040"))
    back_btn.bind('<Leave>', lambda e: back_btn.configure(bg="#2d2d2d"))

def show_programs_page(year):
    program_window = Toplevel()
    program_window.title(f"Select Program - {year}")
    program_window.geometry("900x700")
    program_window.configure(background="#1a1a1a")
    program_window.resizable(False, False)

    # Center the window
    window_width = 900
    window_height = 700
    screen_width = program_window.winfo_screenwidth()
    screen_height = program_window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    program_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Title
    title = Label(
        program_window,
        text=f"Select Program ({year})",
        bg="#1a1a1a",
        fg="#00ff88",
        font=("times new roman", 35, "bold")
    )
    title.pack(pady=20)

    # Create container frame
    container = Frame(program_window, bg="#1a1a1a")
    container.pack(fill=BOTH, expand=TRUE, padx=30, pady=(0, 20))

    # Create canvas
    canvas = Canvas(container, bg="#1a1a1a", highlightthickness=0)
    scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="#1a1a1a")

    # Configure scrollable frame
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Create window inside canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Pack scrollbar and canvas
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Button style
    button_style = {
        "font": ("times new roman", 16, "bold"),
        "bg": "#2d2d2d",
        "fg": "#00ff88",
        "relief": "flat",
        "width": 30,
        "height": 2,
        "cursor": "hand2"
    }

    def on_program_select(program):
        text_to_speech(f"{program} selected")
        program_window.destroy()
        show_courses_page(year, program)

    # Animation effects
    def on_enter(e):
        button = e.widget
        button.configure(bg="#404040")

    def on_leave(e):
        button = e.widget
        button.configure(bg="#2d2d2d")

    # Bind mouse wheel to scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(-1 * int(event.delta/120), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    scrollable_frame.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
    scrollable_frame.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    # Programs list
    programs = [
        "COMPUTER SCIENCE",
        "SOFTWARE ENGINEERING",
        "CYBER SECURITY",
        "INFORMATION TECHNOLOGY",
        "DATA SCIENCE",
        "ARTIFICIAL INTELLIGENCE",
        "BUSINESS ADMINISTRATION",
        "MECHANICAL ENGINEERING",
        "ELECTRICAL ENGINEERING",
        "CIVIL ENGINEERING",
        "MEDICINE AND SURGERY",
        "NURSING",
        "ARCHITECTURE"
    ]

    # Create buttons
    for program in programs:
        btn = Button(
            scrollable_frame,
            text=program,
            command=lambda p=program: on_program_select(p),
            **button_style
        )
        btn.pack(pady=10, padx=20, fill=X)
        
        # Bind hover effects
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)

    # Scroll indicator (at bottom)
    scroll_indicator = Label(
        program_window,
        text="↑ Scroll for more programs ↓",
        bg="#1a1a1a",
        fg="#00ff88",
        font=("times new roman", 12)
    )
    scroll_indicator.pack(side=BOTTOM, pady=5)

    # Back button
    back_btn = Button(
        program_window,
        text="← Back",
        command=lambda: [program_window.destroy(), take_attendance_page()],
        font=("times new roman", 12),
        bg="#2d2d2d",
        fg="#00ff88",
        relief="flat",
        cursor="hand2"
    )
    back_btn.place(x=20, y=20)

    # Hover effects for back button
    back_btn.bind('<Enter>', lambda e: back_btn.configure(bg="#404040"))
    back_btn.bind('<Leave>', lambda e: back_btn.configure(bg="#2d2d2d"))

    # Make sure scrolling works by updating idletasks
    program_window.update_idletasks()
    
    # Configure the canvas scrolling region
    canvas.configure(scrollregion=canvas.bbox("all"))

    # Make sure the frame is large enough to scroll
    scrollable_frame.update_idletasks()
    if scrollable_frame.winfo_height() > canvas.winfo_height():
        scroll_indicator.configure(fg="#00ff88")  # Make scroll indicator visible
    else:
        scroll_indicator.configure(fg="#1a1a1a")  # Hide scroll indicator if not needed

    # Bind keyboard shortcuts for scrolling
    program_window.bind("<Up>", lambda e: canvas.yview_scroll(-1, "units"))
    program_window.bind("<Down>", lambda e: canvas.yview_scroll(1, "units"))
    program_window.bind("<Prior>", lambda e: canvas.yview_scroll(-1, "pages"))
    program_window.bind("<Next>", lambda e: canvas.yview_scroll(1, "pages"))

def show_courses_page(year, program):
    course_window = Toplevel()
    course_window.title(f"Courses - {program} ({year})")
    course_window.geometry("900x700")
    course_window.configure(background="#1a1a1a")
    course_window.resizable(False, False)

    # Center the window
    window_width = 900
    window_height = 700
    screen_width = course_window.winfo_screenwidth()
    screen_height = course_window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    course_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Title
    title_frame = Frame(course_window, bg="#1a1a1a")
    title_frame.pack(fill=X, pady=20)

    title = Label(
        title_frame,
        text=f"{program}",
        bg="#1a1a1a",
        fg="#00ff88",
        font=("times new roman", 30, "bold")
    )
    title.pack()

    subtitle = Label(
        title_frame,
        text=f"{year} Courses",
        bg="#1a1a1a",
        fg="#00ff88",
        font=("times new roman", 20)
    )
    subtitle.pack()

    # Create main frame for courses
    main_frame = Frame(course_window, bg="#1a1a1a")
    main_frame.pack(fill=BOTH, expand=True, padx=30, pady=20)

    # Create canvas
    canvas = Canvas(main_frame, bg="#1a1a1a", highlightthickness=0)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    # Add scrollbar
    scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Configure canvas
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create frame for buttons
    button_frame = Frame(canvas, bg="#1a1a1a")
    canvas.create_window((0, 0), window=button_frame, anchor='nw', width=canvas.winfo_reqwidth())

    # Get courses for the selected program and year
    courses = get_courses_for_program(program, year)

    # Print for debugging
    print(f"Program: {program}")
    print(f"Year: {year}")
    print(f"Courses: {courses}")

    # Button style
    button_style = {
        "font": ("times new roman", 14, "bold"),
        "bg": "#2d2d2d",
        "fg": "#00ff88",
        "relief": "flat",
        "width": 35,
        "height": 2,
        "cursor": "hand2"
    }

    def on_enter(e):
        e.widget.configure(bg="#404040")

    def on_leave(e):
        e.widget.configure(bg="#2d2d2d")

    def start_attendance_for_course(course):
        text_to_speech(f"Starting attendance for {course}")
        course_window.destroy()
        # Call your attendance function here
        start_attendance(year, program, course)

    # Create buttons for each course
    if courses:  # Check if courses list is not empty
        for course in courses:
            course_btn = Button(
                button_frame,
                text=course,
                command=lambda c=course: start_attendance_for_course(c),
                **button_style
            )
            course_btn.pack(pady=10, padx=20, fill=X)
            
            # Bind hover events
            course_btn.bind('<Enter>', on_enter)
            course_btn.bind('<Leave>', on_leave)
    else:
        # Show message if no courses found
        no_courses_label = Label(
            button_frame,
            text="No courses found for this program and year",
            bg="#1a1a1a",
            fg="#ff4444",
            font=("times new roman", 14)
        )
        no_courses_label.pack(pady=20)

    # Update scroll region
    button_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

    # Configure mouse wheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # Back button
    back_btn = Button(
        course_window,
        text="← Back",
        command=lambda: [course_window.destroy(), show_programs_page(year)],
        font=("times new roman", 12),
        bg="#2d2d2d",
        fg="#00ff88",
        relief="flat",
        cursor="hand2"
    )
    back_btn.place(x=20, y=20)

    back_btn.bind('<Enter>', lambda e: back_btn.configure(bg="#404040"))
    back_btn.bind('<Leave>', lambda e: back_btn.configure(bg="#2d2d2d"))

    # Make sure the window stays on top initially
    course_window.lift()
    course_window.focus_force()

def get_courses_for_program(program, year):
    program_courses = {
        "CYBER SECURITY": {
            "YEAR 1": [
                "INTRODUCTION TO CYBERSECURITY",
                "COMPUTER FUNDAMENTALS",
                "PROGRAMMING BASICS",
                "MATHEMATICS FOR COMPUTING",
                "COMMUNICATION SKILLS",
                "NETWORKING FUNDAMENTALS"
            ],
            "YEAR 2": [
                "NETWORK SECURITY",
                "OPERATING SYSTEMS SECURITY",
                "CRYPTOGRAPHY",
                "DATABASE SECURITY",
                "ETHICAL HACKING BASICS",
                "SECURITY PROTOCOLS"
            ],
            "YEAR 3": [
                "ADVANCED ETHICAL HACKING",
                "DIGITAL FORENSICS",
                "MALWARE ANALYSIS",
                "INCIDENT RESPONSE",
                "SECURITY OPERATIONS",
                "WEB APPLICATION SECURITY"
            ],
            "YEAR 4": [
                "ADVANCED NETWORK SECURITY",
                "PENETRATION TESTING",
                "SECURITY ARCHITECTURE",
                "CYBER LAW AND ETHICS",
                "SECURITY MANAGEMENT",
                "FINAL YEAR PROJECT"
            ]
        },
        "COMPUTER SCIENCE": {
            "YEAR 1": [
                "INTRODUCTION TO PROGRAMMING",
                "DISCRETE MATHEMATICS",
                "COMPUTER ORGANIZATION",
                "CALCULUS",
                "COMMUNICATION SKILLS",
                "PHYSICS FOR COMPUTING"
            ],
            "YEAR 2": [
                "DATA STRUCTURES AND ALGORITHMS",
                "OBJECT ORIENTED PROGRAMMING",
                "DATABASE SYSTEMS",
                "WEB DEVELOPMENT",
                "COMPUTER NETWORKS",
                "SOFTWARE ENGINEERING"
            ],
            "YEAR 3": [
                "OPERATING SYSTEMS",
                "ARTIFICIAL INTELLIGENCE",
                "DISTRIBUTED SYSTEMS",
                "MOBILE APPLICATION DEVELOPMENT",
                "COMPUTER GRAPHICS",
                "SYSTEM ANALYSIS AND DESIGN"
            ],
            "YEAR 4": [
                "CLOUD COMPUTING",
                "MACHINE LEARNING",
                "IT PROJECT MANAGEMENT",
                "INFORMATION SECURITY",
                "FINAL YEAR PROJECT",
                "PROFESSIONAL ETHICS"
            ]
        },
        "SOFTWARE ENGINEERING": {
            "YEAR 1": [
                "PROGRAMMING FUNDAMENTALS",
                "SOFTWARE DEVELOPMENT BASICS",
                "MATHEMATICS FOR ENGINEERS",
                "COMMUNICATION SKILLS",
                "INTRODUCTION TO COMPUTING",
                "PHYSICS FOR ENGINEERS"
            ],
            "YEAR 2": [
                "ADVANCED PROGRAMMING",
                "SOFTWARE REQUIREMENTS",
                "DATABASE MANAGEMENT",
                "WEB TECHNOLOGIES",
                "SOFTWARE ARCHITECTURE",
                "AGILE METHODOLOGIES"
            ],
            "YEAR 3": [
                "SOFTWARE TESTING",
                "MOBILE DEVELOPMENT",
                "CLOUD PLATFORMS",
                "UI/UX DESIGN",
                "API DEVELOPMENT",
                "PROJECT MANAGEMENT"
            ],
            "YEAR 4": [
                "ENTERPRISE SOFTWARE",
                "DEVOPS PRACTICES",
                "SOFTWARE QUALITY",
                "SYSTEM INTEGRATION",
                "FINAL YEAR PROJECT",
                "PROFESSIONAL PRACTICE"
            ]
        },
        "DATA SCIENCE": {
            "YEAR 1": [
                "PROGRAMMING FOR DATA SCIENCE",
                "STATISTICS FUNDAMENTALS",
                "LINEAR ALGEBRA",
                "DATABASE BASICS",
                "COMMUNICATION SKILLS",
                "CRITICAL THINKING"
            ],
            "YEAR 2": [
                "DATA STRUCTURES",
                "PROBABILITY THEORY",
                "PYTHON FOR DATA ANALYSIS",
                "DATA VISUALIZATION",
                "SQL AND DATABASES",
                "RESEARCH METHODS"
            ],
            "YEAR 3": [
                "MACHINE LEARNING",
                "BIG DATA ANALYTICS",
                "STATISTICAL MODELING",
                "DATA MINING",
                "DEEP LEARNING BASICS",
                "DATA WAREHOUSING"
            ],
            "YEAR 4": [
                "ADVANCED MACHINE LEARNING",
                "ARTIFICIAL INTELLIGENCE",
                "BUSINESS ANALYTICS",
                "NATURAL LANGUAGE PROCESSING",
                "FINAL YEAR PROJECT",
                "ETHICS IN DATA SCIENCE"
            ]
        },
        "ARTIFICIAL INTELLIGENCE": {
            "YEAR 1": [
                "AI FUNDAMENTALS",
                "PROGRAMMING BASICS",
                "MATHEMATICS FOR AI",
                "PROBABILITY AND STATISTICS",
                "COMMUNICATION SKILLS",
                "LOGIC AND REASONING"
            ],
            "YEAR 2": [
                "MACHINE LEARNING BASICS",
                "NEURAL NETWORKS",
                "DATA STRUCTURES",
                "ALGORITHMS FOR AI",
                "PYTHON FOR AI",
                "AI ETHICS"
            ],
            "YEAR 3": [
                "DEEP LEARNING",
                "COMPUTER VISION",
                "NATURAL LANGUAGE PROCESSING",
                "ROBOTICS",
                "AI ALGORITHMS",
                "EXPERT SYSTEMS"
            ],
            "YEAR 4": [
                "ADVANCED AI",
                "REINFORCEMENT LEARNING",
                "AI IN ROBOTICS",
                "COGNITIVE COMPUTING",
                "FINAL YEAR PROJECT",
                "AI APPLICATIONS"
            ]
        }
    }
    
    # Return courses for the selected program and year
    try:
        return program_courses[program][year]
    except KeyError:
        return [
            "COMMUNICATION SKILLS",
            "ETHICS",
            "MATHEMATICS",
            "PROGRAMMING FUNDAMENTALS",
            "INTRODUCTION TO COMPUTING",
            "PROFESSIONAL DEVELOPMENT"
        ]

def start_attendance(year, program, course):
    try:
        # Validate CSV file first
        if not os.path.exists("StudentDetails/StudentDetails.csv"):
            messagebox.showerror("Error", "Student details file not found!")
            return
            
        # Read student data
        df = pd.read_csv("StudentDetails/StudentDetails.csv")
        if df.empty:
            messagebox.showerror("Error", "No student data found!")
            return
            
        # Initialize camera
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "Cannot access camera!")
            return
            
        # Load recognizer
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        if not os.path.exists("TrainingImageLabel/Trainner.yml"):
            messagebox.showerror("Error", "No trained model found!")
            cap.release()
            return
        recognizer.read("TrainingImageLabel/Trainner.yml")
        
        # Load face cascade
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Dictionary to track student attendance and timing
        student_tracking = {}  # {id: {'last_seen': timestamp, 'status': 'Present/Left', 'left_time': None}}
        
        # Timeout duration in minutes
        timeout_duration = 20
        
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
                
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            current_time = datetime.now()
            
            # Check for timeouts first
            for student_id in list(student_tracking.keys()):
                if student_tracking[student_id]['status'] == 'Present':
                    time_diff = (current_time - student_tracking[student_id]['last_seen']).total_seconds() / 60
                    if time_diff > timeout_duration:
                        # Student has been away for more than 20 minutes
                        student_tracking[student_id]['status'] = 'Left'
                        student_tracking[student_id]['left_time'] = student_tracking[student_id]['last_seen']
                        
                        # Update attendance record
                        attendance_dir = f"Attendance/{program}"
                        os.makedirs(attendance_dir, exist_ok=True)
                        attendance_file = f"{attendance_dir}/{course}_{current_time.strftime('%Y-%m-%d')}.csv"
                        
                        student = df[df['Id'] == str(student_id)]
                        if not student.empty:
                            attendance_data = {
                                'Id': [str(student_id)],
                                'Name': [student.iloc[0]['Name']],
                                'Gender': [student.iloc[0]['Gender']],
                                'Date': [current_time.strftime('%Y-%m-%d')],
                                'Time': [current_time.strftime('%H:%M:%S')],
                                'Course': [course],
                                'Program': [program],
                                'Status': ['Left'],
                                'Left_Time': [student_tracking[student_id]['left_time'].strftime('%H:%M:%S')]
                            }
                            attendance_df = pd.DataFrame(attendance_data)
                            if os.path.exists(attendance_file):
                                # Update existing record
                                existing_df = pd.read_csv(attendance_file)
                                existing_df.loc[existing_df['Id'] == str(student_id)] = attendance_df.iloc[0]
                                existing_df.to_csv(attendance_file, index=False)
                            else:
                                attendance_df.to_csv(attendance_file, index=False)
            
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                id_, confidence = recognizer.predict(gray[y:y+h, x:x+w])
                
                if confidence < 50:
                    student = df[df['Id'] == str(id_)]
                    if not student.empty:
                        name = student.iloc[0]['Name']
                        gender = student.iloc[0]['Gender']
                        
                        if id_ not in student_tracking:
                            # First time seeing this student
                            student_tracking[id_] = {
                                'last_seen': current_time,
                                'status': 'Present',
                                'left_time': None
                            }
                        else:
                            if student_tracking[id_]['status'] == 'Left':
                                # Check if student returned within timeout
                                if student_tracking[id_]['left_time']:
                                    time_diff = (current_time - student_tracking[id_]['left_time']).total_seconds() / 60
                                    if time_diff <= timeout_duration:
                                        # Student returned within timeout - mark as still present
                                        student_tracking[id_]['status'] = 'Present'
                                        student_tracking[id_]['left_time'] = None
                            
                            student_tracking[id_]['last_seen'] = current_time
                        
                        # Create attendance record
                        attendance_dir = f"Attendance/{program}"
                        os.makedirs(attendance_dir, exist_ok=True)
                        attendance_file = f"{attendance_dir}/{course}_{current_time.strftime('%Y-%m-%d')}.csv"
                        
                        attendance_data = {
                            'Id': [str(id_)],
                            'Name': [name],
                            'Gender': [gender],
                            'Date': [current_time.strftime('%Y-%m-%d')],
                            'Time': [current_time.strftime('%H:%M:%S')],
                            'Course': [course],
                            'Program': [program],
                            'Status': [student_tracking[id_]['status']],
                            'Left_Time': [student_tracking[id_]['left_time'].strftime('%H:%M:%S') if student_tracking[id_]['left_time'] else '']
                        }
                        
                        attendance_df = pd.DataFrame(attendance_data)
                        if os.path.exists(attendance_file):
                            # Update existing record
                            existing_df = pd.read_csv(attendance_file)
                            existing_df.loc[existing_df['Id'] == str(id_)] = attendance_df.iloc[0]
                            existing_df.to_csv(attendance_file, index=False)
                        else:
                            attendance_df.to_csv(attendance_file, index=False)
                        
                        # Display status on frame
                        status_text = f"{name} - {student_tracking[id_]['status']}"
                        if student_tracking[id_]['status'] == 'Left':
                            status_text += f" at {student_tracking[id_]['left_time'].strftime('%H:%M:%S')}"
                        cv2.putText(frame, status_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, 
                                  (0, 255, 0) if student_tracking[id_]['status'] == 'Present' else (0, 0, 255), 2)
                else:
                    cv2.putText(frame, "Unknown Face", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
            cv2.imshow("Attendance System", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()
        
    except Exception as e:
        print(f"Error: {str(e)}")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        if 'cap' in locals():
            cap.release()
        cv2.destroyAllWindows()

def fix_student_details_csv():
    try:
        # Create StudentDetails directory if it doesn't exist
        os.makedirs("StudentDetails", exist_ok=True)
        
        # Define the correct columns
        columns = ['Id', 'Name', 'Gender', 'Program']
        
        # Create a new DataFrame
        df = pd.DataFrame(columns=columns)
        
        # Try to read existing file if it exists
        if os.path.exists("StudentDetails/StudentDetails.csv"):
            try:
                old_df = pd.read_csv("StudentDetails/StudentDetails.csv")
                
                # Clean and standardize the data
                cleaned_data = []
                for _, row in old_df.iterrows():
                    # Ensure all required columns exist
                    student_data = {
                        'Id': str(row.get('Id', '')).strip(),
                        'Name': str(row.get('Name', '')).strip(),
                        'Gender': str(row.get('Gender', '')).strip(),
                        'Program': str(row.get('Program', '')).strip()
                    }
                    cleaned_data.append(student_data)
                
                if cleaned_data:
                    df = pd.DataFrame(cleaned_data)
            except Exception as e:
                print(f"Error reading existing file: {str(e)}")
                # Continue with empty DataFrame if error
        
        # If DataFrame is empty, add sample data
        if df.empty:
            sample_data = {
                'Id': ['1', '2'],
                'Name': ['John Doe', 'Jane Smith'],
                'Gender': ['Male', 'Female'],
                'Program': ['Computer Science', 'Data Science']
            }
            df = pd.DataFrame(sample_data)
        
        # Save the cleaned/new CSV file
        df.to_csv("StudentDetails/StudentDetails.csv", index=False)
        
        print("StudentDetails.csv has been created/fixed successfully!")
        print("\nCurrent contents:")
        print(df)
        
        return True
        
    except Exception as e:
        print(f"Error fixing CSV: {str(e)}")
        return False

# Add this to your main code or where appropriate
def initialize_system():
    try:
        # Create necessary directories
        directories = ['TrainingImage', 'TrainingImageLabel', 'StudentDetails', 'Attendance']
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        # Fix/create StudentDetails.csv
        if fix_student_details_csv():
            print("System initialized successfully!")
            return True
        return False
        
    except Exception as e:
        print(f"Error initializing system: {str(e)}")
        return False

# Add this to your main function or where you start your application
if __name__ == "__main__":
    if initialize_system():
        main()  # Your existing main function
    else:
        print("Failed to initialize system. Please check the errors above.")
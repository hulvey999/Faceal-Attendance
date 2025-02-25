import cv2
import numpy as np
import pandas as pd
import datetime
import time
import os
from PIL import Image

class EnhancedAttendanceSystem:
    def __init__(self):
        self.timeout_minutes = 20
        self.face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.student_details = pd.read_csv("StudentDetails/studentdetails.csv")
        self.attendance_records = {}  # Track detailed attendance records
        
        # Load trained model if exists
        if os.path.exists("TrainingImageLabel/Trainer.yml"):
            self.recognizer.read("TrainingImageLabel/Trainer.yml")
            
    def mark_attendance(self):
        cap = cv2.VideoCapture(0)
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                    
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                
                current_time = datetime.datetime.now()
                
                # Check all active records for timeouts
                self._check_timeouts(current_time)
                
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    id, confidence = self.recognizer.predict(gray[y:y+h, x:x+w])
                    
                    if confidence < 70:  # Confidence threshold
                        student_info = self.student_details[self.student_details['Id'] == id].iloc[0]
                        student_id = student_info['Id']
                        student_name = student_info['Name']
                        
                        if student_id not in self.attendance_records:
                            # First time seen today - mark as present
                            self.attendance_records[student_id] = {
                                'name': student_name,
                                'status': 'Present',
                                'entry_time': current_time,
                                'last_seen': current_time,
                                'left_time': None,
                                'return_time': None
                            }
                            self._save_attendance_record(student_id, current_date)
                            
                        else:
                            record = self.attendance_records[student_id]
                            if record['status'] == 'Left':
                                time_diff = (current_time - record['left_time']).total_seconds() / 60
                                if time_diff <= self.timeout_minutes:
                                    # Returned within timeout - update status back to present
                                    record['status'] = 'Present'
                                    record['return_time'] = current_time
                                    self._save_attendance_record(student_id, current_date)
                            
                            record['last_seen'] = current_time
                        
                        # Display status
                        status_text = f"{student_name} - {self.attendance_records[student_id]['status']}"
                        cv2.putText(frame, status_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    
                    else:
                        cv2.putText(frame, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                
                cv2.imshow("Attendance System", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        finally:
            cap.release()
            cv2.destroyAllWindows()
            # Final save of attendance records
            for student_id in self.attendance_records:
                self._save_attendance_record(student_id, current_date)
            
    def _check_timeouts(self, current_time):
        for student_id, record in self.attendance_records.items():
            if record['status'] == 'Present':
                time_diff = (current_time - record['last_seen']).total_seconds() / 60
                if time_diff > self.timeout_minutes:
                    record['status'] = 'Left'
                    record['left_time'] = record['last_seen']  # Mark left time as last seen time
                    self._save_attendance_record(student_id, current_time.strftime('%Y-%m-%d'))
                    
    def _save_attendance_record(self, student_id, date):
        record = self.attendance_records[student_id]
        attendance_file = f"Attendance/Attendance_{date}.csv"
        
        attendance_data = {
            'Id': student_id,
            'Name': record['name'],
            'Status': record['status'],
            'Entry_Time': record['entry_time'].strftime('%H:%M:%S'),
            'Left_Time': record['left_time'].strftime('%H:%M:%S') if record['left_time'] else '',
            'Return_Time': record['return_time'].strftime('%H:%M:%S') if record['return_time'] else ''
        }
        
        # Convert to DataFrame
        df = pd.DataFrame([attendance_data])
        
        if os.path.exists(attendance_file):
            # Update existing record
            existing_df = pd.read_csv(attendance_file)
            existing_df.loc[existing_df['Id'] == student_id] = df.iloc[0]
            existing_df.to_csv(attendance_file, index=False)
        else:
            # Create new file
            df.to_csv(attendance_file, index=False)

if __name__ == "__main__":
    system = EnhancedAttendanceSystem()
    system.mark_attendance()

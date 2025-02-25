import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk
from tkinter import *

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get()
        if Subject=="":
            t='Please enter the subject name.'
            text_to_speech(t)
        os.chdir(
            f"Attendance\\{Subject}"
        )
        filenames = glob(
            f"Attendance\\{Subject}\\{Subject}*.csv"
        )
        df = [pd.read_csv(f) for f in filenames]
        newdf = df[0]
        for i in range(1, len(df)):
            newdf = newdf.merge(df[i], how="outer")
        newdf.fillna(0, inplace=True)
        newdf["Attendance"] = 0
        for i in range(len(newdf)):
            newdf["Attendance"].iloc[i] = str(int(round(newdf.iloc[i, 2:-1].mean() * 100)))+'%'
            #newdf.sort_values(by=['Enrollment'],inplace=True)
        newdf.to_csv("attendance.csv", index=False)

        root = tkinter.Tk()
        root.title("Attendance of "+Subject)
        root.configure(background="#2C3E50")
        cs = f"Attendance\\{Subject}\\attendance.csv"
        with open(cs) as file:
            reader = csv.reader(file)
            r = 0

            for col in reader:
                c = 0
                for row in col:

                    label = tkinter.Label(
                        root,
                        width=10,
                        height=1,
                        fg="#ECF0F1",
                        font=("Helvetica", 12),
                        bg="#34495E",
                        text=row,
                        relief=tkinter.GROOVE,
                    )
                    label.grid(row=r, column=c)
                    c += 1
                r += 1
        root.mainloop()
        print(newdf)

    subject = Tk()
    subject.title("Subject Attendance")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="#2C3E50")

    titl = tk.Label(
        subject,
        bg="#34495E",
        relief=GROOVE,
        bd=2,
        font=("Helvetica", 28)
    )
    titl.pack(fill=X)

    titl = tk.Label(
        subject,
        text="Select Subject for Attendance",
        bg="#34495E",
        fg="#3498DB",
        font=("Helvetica", 24)
    )
    titl.place(x=100, y=12)

    def Attf():
        sub = tx.get()
        if sub == "":
            t="Please enter the subject name!!!"
            text_to_speech(t)
        else:
            os.startfile(
            f"Attendance\\{sub}"
            )


    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=0,
        font=("Helvetica", 12),
        bg="#3498DB",
        fg="white",
        height=2,
        width=12,
        relief=FLAT,
    )
    attf.place(x=360, y=170)

    sub = tk.Label(
        subject,
        text="Enter Subject",
        width=10,
        height=2,
        bg="#34495E",
        fg="#ECF0F1",
        bd=0,
        relief=FLAT,
        font=("Helvetica", 12)
    )
    sub.place(x=50, y=100)

    tx = tk.Entry(
        subject,
        width=15,
        bd=0,
        bg="#34495E",
        fg="#ECF0F1",
        relief=FLAT,
        font=("Helvetica", 24)
    )
    tx.place(x=190, y=100)

    fill_a = tk.Button(
        subject,
        text="View Attendance",
        command=calculate_attendance,
        bd=0,
        font=("Helvetica", 12),
        bg="#3498DB",
        fg="white",
        height=2,
        width=12,
        relief=FLAT
    )
    fill_a.place(x=195, y=170)
    subject.mainloop()

import tkinter as tk
from tkinter import filedialog, messagebox

def load_answer_key():
    global answer_key
    filepath = filedialog.askopenfilename(title="Select Answer Key File", filetypes=[("Text Files", "*.txt")])
    
    if filepath:
        with open(filepath, 'r') as f:
            answer_key = [line.strip().upper() for line in f.readlines()]
        messagebox.showinfo("Success", "Answer Key Loaded Successfully!")

def load_student_answers():
    global student_answers
    filepath = filedialog.askopenfilename(title="Select Student Answers File", filetypes=[("Text Files", "*.txt")])
    
    if filepath:
        with open(filepath, 'r') as f:
            student_answers = [line.strip().upper() for line in f.readlines()]
        messagebox.showinfo("Success", "Student Answers Loaded Successfully!")

def grade_exam():
    if answer_key is None or student_answers is None:
        messagebox.showerror("Error", "Please load answer key and student answers first!")
        return
    
    correct = sum(1 for a, b in zip(answer_key, student_answers) if a == b)
    total = len(answer_key)
    wrong = total - correct
    percentage = (correct / total) * 100
    
    result_label.config(text=f"Correct: {correct}\nWrong: {wrong}\nPercentage: {percentage:.2f}%")

# GUI Window
root = tk.Tk()
root.title("Automated Exam Grading System")
root.geometry("400x350")

answer_key = None
student_answers = None

title_label = tk.Label(root, text="Automated Exam Grading System", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

btn1 = tk.Button(root, text="Load Answer Key", width=20, command=load_answer_key)
btn1.pack(pady=10)

btn2 = tk.Button(root, text="Load Student Answers", width=20, command=load_student_answers)
btn2.pack(pady=10)

btn3 = tk.Button(root, text="Grade Exam", width=20, command=grade_exam)
btn3.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.pack(pady=20)

root.mainloop()

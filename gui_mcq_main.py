
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json, csv, os, datetime

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def load_questions():
    path = os.path.join(BASE_DIR, "questions.json")
    with open(path, "r") as f:
        return json.load(f)

class ExamApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BrightExam — MCQ Exam System")
        self.geometry("700x520")
        self.resizable(False, False)
        self.configure(bg='#f4f7fb')

        # Style
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TFrame', background='#f4f7fb')
        style.configure('Title.TLabel', font=('Helvetica', 18, 'bold'), background='#f4f7fb', foreground='#1f2937')
        style.configure('Q.TLabel', font=('Helvetica', 13), background='#f4f7fb', foreground='#111827')
        style.configure('TButton', font=('Helvetica', 11, 'bold'))
        style.map('Accent.TButton', background=[('active','#2563eb')], foreground=[('!disabled','#ffffff')])

        self.questions = load_questions()
        self.total = len(self.questions)
        self.current = 0
        self.answers = [tk.StringVar(value="") for _ in range(self.total)]

        self.create_header()
        self.create_question_area()
        self.create_footer()
        self.show_question(0)

    def create_header(self):
        header = ttk.Frame(self, padding=(20,10))
        header.pack(fill='x')
        title = ttk.Label(header, text="BrightExam — MCQ Exam System", style='Title.TLabel')
        title.pack(side='left')
        self.progress_label = ttk.Label(header, text=f"Question 0/{self.total}", style='Q.TLabel')
        self.progress_label.pack(side='right')

    def create_question_area(self):
        body = ttk.Frame(self, padding=(20,10))
        body.pack(fill='both', expand=True)
        card = tk.Frame(body, bg='#ffffff', bd=0, relief='ridge')
        card.pack(fill='both', expand=True, padx=10, pady=10)

        self.q_label = ttk.Label(card, text="", style='Q.TLabel', wraplength=640, justify='left')
        self.q_label.pack(padx=20, pady=(20,10))

        self.option_vars = []
        self.option_buttons = []
        for i in range(4):
            rb = ttk.Radiobutton(card, text="", value=str(i), variable=tk.StringVar())  # placeholder
            # We'll use custom radio-like buttons manually
            btn = tk.Button(card, text="", anchor='w', relief='flat', pady=8, padx=10, font=('Helvetica',11), bd=1)
            btn.pack(fill='x', padx=20, pady=6)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg='#eef2ff'))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg='#ffffff'))
            btn.config(command=lambda b=btn: self.select_option(b))
            self.option_buttons.append(btn)

    def create_footer(self):
        footer = ttk.Frame(self, padding=(20,10))
        footer.pack(fill='x', side='bottom')
        btn_frame = ttk.Frame(footer)
        btn_frame.pack(side='left')

        prev_btn = ttk.Button(btn_frame, text="◀ Prev", command=self.prev_question)
        prev_btn.grid(row=0, column=0, padx=(0,6))
        next_btn = ttk.Button(btn_frame, text="Next ▶", command=self.next_question)
        next_btn.grid(row=0, column=1, padx=(6,12))
        submit_btn = ttk.Button(footer, text="Submit Exam", style='Accent.TButton', command=self.submit_exam)
        submit_btn.pack(side='right')

        self.save_btn = ttk.Button(footer, text="Save Answers", command=self.save_answers)
        self.save_btn.pack(side='right', padx=(0,8))

    def show_question(self, idx):
        self.current = idx
        qdata = self.questions[idx]
        self.q_label.config(text=f"Q{idx+1}. {qdata['q']}")
        opts = qdata['options']
        for i, btn in enumerate(self.option_buttons):
            btn.config(text=f"   {chr(65+i)}. {opts[i]}", bg='#ffffff', fg='#111827', anchor='w')
            # highlight if previously selected
            sel = self.answers[idx].get()
            if sel == opts[i]:
                btn.config(bg='#dbeafe')
        self.progress_label.config(text=f"Question {idx+1}/{self.total}")

    def select_option(self, btn):
        text = btn.cget('text').strip()
        # option text after 'A. '
        if '. ' in text:
            opt = text.split('. ', 1)[1]
        else:
            opt = text
        # save selection
        self.answers[self.current].set(opt)
        # update visuals
        for b in self.option_buttons:
            b.config(bg='#ffffff')
        btn.config(bg='#dbeafe')

    def prev_question(self):
        if self.current > 0:
            self.show_question(self.current - 1)

    def next_question(self):
        if self.current < self.total - 1:
            self.show_question(self.current + 1)

    def submit_exam(self):
        # ensure at least one question answered
        if not any(var.get() for var in self.answers):
            if not messagebox.askyesno("Confirm", "No answers detected. Do you still want to submit?"):
                return
        correct = 0
        wrong_list = []
        for i, q in enumerate(self.questions):
            given = self.answers[i].get()
            if given == q['answer']:
                correct += 1
            else:
                wrong_list.append((i+1, q['answer'], given if given else "No Answer"))
        percent = (correct / self.total) * 100
        self.show_result(correct, wrong_list, percent)
        # disable buttons after submit
        self.disable_interaction()

    def show_result(self, correct, wrong_list, percent):
        res_win = tk.Toplevel(self)
        res_win.title("Result")
        res_win.geometry("520x400")
        res_win.configure(bg='#f8fafc')
        tk.Label(res_win, text="Exam Result", font=('Helvetica',16,'bold'), bg='#f8fafc').pack(pady=12)
        tk.Label(res_win, text=f"Score: {correct}/{self.total}", font=('Helvetica',13), bg='#f8fafc').pack(pady=6)
        tk.Label(res_win, text=f"Percentage: {percent:.2f}%", font=('Helvetica',13), bg='#f8fafc').pack(pady=6)

        frame = tk.Frame(res_win, bg='#ffffff', bd=1, relief='solid')
        frame.pack(fill='both', expand=True, padx=12, pady=12)
        canvas = tk.Canvas(frame, bg='#ffffff')
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=canvas.yview)
        scrollbar.pack(side='right', fill='y')
        inner = tk.Frame(canvas, bg='#ffffff')
        canvas.create_window((0,0), window=inner, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        for qn, ans, given in wrong_list:
            tk.Label(inner, text=f"Q{qn}: Correct: {ans}  |  Given: {given}", anchor='w', bg='#ffffff', font=('Helvetica',11)).pack(fill='x', padx=8, pady=6)
        inner.update_idletasks()
        canvas.config(scrollregion=canvas.bbox('all'))

        # Save result button
        save_btn = ttk.Button(res_win, text="Save Result CSV", command=lambda: self.save_result_csv(correct, percent))
        save_btn.pack(pady=8)

    def save_result_csv(self, correct, percent):
        filename = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files','*.csv')], initialfile=f"result_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        if not filename:
            return
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Question','Correct Answer','Student Answer'])
            for i, q in enumerate(self.questions):
                writer.writerow([f"Q{i+1}", q['answer'], self.answers[i].get() if self.answers[i].get() else "No Answer"])
            writer.writerow([])
            writer.writerow(['Score', f"{correct}/{self.total}", f"{percent:.2f}%"])
        messagebox.showinfo("Saved", f"Result saved to {filename}")

    def save_answers(self):
        filename = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text files','*.txt')], initialfile=f"answers_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        if not filename:
            return
        with open(filename, 'w') as f:
            for i, var in enumerate(self.answers):
                f.write(var.get() + "\n")
        messagebox.showinfo("Saved", f"Answers saved to {filename}")

    def disable_interaction(self):
        for b in self.option_buttons:
            b.config(state='disabled')
        # Disable nav buttons by destroying them (simple)
        # (For simplicity not tracked individually)

if __name__ == '__main__':
    app = ExamApp()
    app.mainloop()

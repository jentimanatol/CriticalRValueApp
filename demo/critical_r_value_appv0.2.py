import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import math
from scipy.stats import t

def calculate_r_critical(t_value, n):
    return t_value / math.sqrt(t_value**2 + (n - 2))

def get_t_critical(alpha, df):
    return t.ppf(1 - alpha / 2, df)

def perform_calculation(alpha, n, callback):
    try:
        alpha = float(alpha)
        n = int(n)
        if n < 3:
            raise ValueError("Sample size must be ≥ 3.")
        df = n - 2
        t_crit = get_t_critical(alpha, df)
        r_crit = calculate_r_critical(t_crit, n)

        ns = list(range(3, 101))
        rs = [calculate_r_critical(get_t_critical(alpha, ni - 2), ni) for ni in ns]

        callback(None, r_crit, ns, rs, alpha)
    except Exception as e:
        callback(str(e), None, None, None, None)

def update_gui(error, r_crit, ns, rs, alpha):
    if error:
        messagebox.showerror("Error", error)
        return

    result_label.config(text=f"Critical r = ±{r_crit:.3f}")

    # Create the plot
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(ns, rs, color='blue', label=f'α = {alpha}')
    ax.set_title("Critical r vs. Sample Size (n)")
    ax.set_xlabel("Sample Size (n)")
    ax.set_ylabel("Critical r")
    ax.grid(True)

    # Add LaTeX formula to the plot
    formula = r'$r_{critical} = \frac{t_{critical}}{\sqrt{t_{critical}^2 + (n - 2)}}$'
    ax.legend([f'{formula}\nα = {alpha}'], loc='upper right')

    # Clear old plot
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def run_in_thread():
    alpha = alpha_entry.get()
    n = n_entry.get()

    def callback(error, r_crit, ns, rs, alpha):
        root.after(0, update_gui, error, r_crit, ns, rs, alpha)

    threading.Thread(
        target=perform_calculation,
        args=(alpha, n, callback),
        daemon=True
    ).start()

# GUI Setup
root = tk.Tk()
root.title("Critical r Calculator")
root.geometry("700x600")

tk.Label(root, text="Significance Level (α):").pack()
alpha_entry = tk.Entry(root)
alpha_entry.insert(0, "0.05")
alpha_entry.pack()

tk.Label(root, text="Sample Size (n):").pack()
n_entry = tk.Entry(root)
n_entry.insert(0, "30")
n_entry.pack()

result_label = tk.Label(root, text="Critical r = ±...")
result_label.pack(pady=10)

canvas_frame = tk.Frame(root)
canvas_frame.pack(fill=tk.BOTH, expand=True)

tk.Button(root, text="Calculate & Plot", command=run_in_thread).pack(pady=10)

root.mainloop()

import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import math

def calculate_r_critical(t, n):
    return t / math.sqrt(t**2 + (n - 2))

def get_t_critical(alpha, df):
    from scipy.stats import t
    return t.ppf(1 - alpha / 2, df)

def update_plot(alpha, n, label, canvas_frame):
    try:
        alpha = float(alpha)
        n = int(n)
        if n < 3:
            raise ValueError("Sample size must be ≥ 3.")
        df = n - 2
        t_critical = get_t_critical(alpha, df)
        r_critical = calculate_r_critical(t_critical, n)

        label.config(text=f"Critical r = ±{r_critical:.3f}")

        # Plotting range of n
        ns = list(range(3, 101))
        rs = [calculate_r_critical(get_t_critical(alpha, n - 2), n) for n in ns]

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(ns, rs, label=f'α = {alpha}')
        ax.set_title('Critical r vs. Sample Size')
        ax.set_xlabel('Sample Size (n)')
        ax.set_ylabel('Critical r')
        ax.grid(True)
        ax.legend()

        # Clear previous canvas
        for widget in canvas_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    except Exception as e:
        messagebox.showerror("Error", str(e))

def run_plot(alpha_entry, n_entry, label, canvas_frame):
    threading.Thread(
        target=update_plot,
        args=(alpha_entry.get(), n_entry.get(), label, canvas_frame),
        daemon=True
    ).start()

# GUI setup
root = tk.Tk()
root.title("Critical r Calculator")
root.geometry("600x500")

tk.Label(root, text="Significance Level (α):").pack()
alpha_entry = tk.Entry(root)
alpha_entry.insert(0, "0.05")
alpha_entry.pack()

tk.Label(root, text="Sample Size (n):").pack()
n_entry = tk.Entry(root)
n_entry.insert(0, "30")
n_entry.pack()

label = tk.Label(root, text="Critical r = ±...")
label.pack(pady=10)

canvas_frame = tk.Frame(root)
canvas_frame.pack(fill=tk.BOTH, expand=True)

tk.Button(root, text="Calculate & Plot", command=lambda: run_plot(alpha_entry, n_entry, label, canvas_frame)).pack(pady=10)

root.mainloop()

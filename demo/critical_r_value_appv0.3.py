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

        callback(None, r_crit, ns, rs, alpha, df, t_crit)
    except Exception as e:
        callback(str(e), None, None, None, None, None, None)

def update_gui(error, r_crit, ns, rs, alpha, df, t_crit):
    if error:
        messagebox.showerror("Error", error)
        return

    result_label.config(text=f"Critical r = ±{r_crit:.3f}")

    fig, ax = plt.subplots(figsize=(8, 5))  # Larger figure

    ax.plot(ns, rs, color='blue')
    ax.set_title("Critical r vs. Sample Size (n)")
    ax.set_xlabel("Sample Size (n)")
    ax.set_ylabel("Critical r")
    ax.grid(True)

    # Add formulas on the right side of the plot
    ax.text(
        1.05, 0.9,
        r"$df = n - 2$" + f"\n$= {df}$",
        transform=ax.transAxes, fontsize=10, verticalalignment='top'
    )
    ax.text(
        1.05, 0.6,
        r"$t = \frac{r \sqrt{n - 2}}{\sqrt{1 - r^2}}$",
        transform=ax.transAxes, fontsize=10, verticalalignment='top'
    )
    ax.text(
        1.05, 0.3,
        r"$r_{critical} = \frac{t_{critical}}{\sqrt{t_{critical}^2 + (n - 2)}}$",
        transform=ax.transAxes, fontsize=10, verticalalignment='top'
    )
    ax.text(
        1.05, 0.15,
        f"$t_{{critical}} = {t_crit:.3f}$",
        transform=ax.transAxes, fontsize=10, verticalalignment='top'
    )

    fig.tight_layout()

    for widget in canvas_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def run_in_thread():
    alpha = alpha_entry.get()
    n = n_entry.get()

    def callback(error, r_crit, ns, rs, alpha, df, t_crit):
        root.after(0, update_gui, error, r_crit, ns, rs, alpha, df, t_crit)

    threading.Thread(
        target=perform_calculation,
        args=(alpha, n, callback),
        daemon=True
    ).start()

# GUI Setup
root = tk.Tk()
root.title("Critical r Calculator")
root.geometry("900x700")  # Bigger window

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

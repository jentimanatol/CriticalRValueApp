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

        callback(None, r_crit, ns, rs, alpha, df, t_crit, n)
    except Exception as e:
        callback(str(e), None, None, None, None, None, None, None)

def update_gui(error, r_crit, ns, rs, alpha, df, t_crit, n):
    if error:
        messagebox.showerror("Error", error)
        return

    result_label.config(text=f"Critical r = ±{r_crit:.3f}", fg="green")

    # Create plot
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('#f2f2f2')
    ax.plot(ns, rs, color='darkblue', linewidth=2, label="Critical r Curve")
    ax.set_title("Critical r vs. Sample Size (n)", fontsize=14, fontweight='bold')
    ax.set_xlabel("Sample Size (n)")
    ax.set_ylabel("Critical r")
    ax.grid(True, linestyle='--', alpha=0.6)

    # Formulas
    ax.text(1.05, 0.95, r"$df = n - 2$", transform=ax.transAxes, fontsize=10, color="black", verticalalignment='top')
    ax.text(1.05, 0.85, r"$t = \frac{r \sqrt{n - 2}}{\sqrt{1 - r^2}}$", transform=ax.transAxes, fontsize=10, color="black")
    ax.text(1.05, 0.70, r"$r_{critical} = \frac{t_{critical}}{\sqrt{t_{critical}^2 + (n - 2)}}$", transform=ax.transAxes, fontsize=10, color="black")
    ax.text(1.05, 0.55, f"$n = {n}$", transform=ax.transAxes, fontsize=10)
    ax.text(1.05, 0.48, f"$df = {df}$", transform=ax.transAxes, fontsize=10)
    ax.text(1.05, 0.41, f"$t_{{critical}} = {t_crit:.3f}$", transform=ax.transAxes, fontsize=10)
    ax.text(1.05, 0.34, f"$r_{{critical}} = {r_crit:.3f}$", transform=ax.transAxes, fontsize=10)

    ax.legend(loc='lower right')

    fig.tight_layout()

    for widget in canvas_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Update calculation summary
    summary_text = f"""
    Input Values:
      α (Significance Level) = {alpha}
      n (Sample Size) = {n}
    
    Calculations:
      Degrees of Freedom (df) = {df}
      t-critical = {t_crit:.3f}
      r-critical = ±{r_crit:.3f}
    """
    calc_text.config(state="normal")
    calc_text.delete("1.0", tk.END)
    calc_text.insert(tk.END, summary_text.strip())
    calc_text.config(state="disabled")

def run_in_thread():
    alpha = alpha_entry.get()
    n = n_entry.get()

    def callback(error, r_crit, ns, rs, alpha, df, t_crit, n):
        root.after(0, update_gui, error, r_crit, ns, rs, alpha, df, t_crit, n)

    threading.Thread(target=perform_calculation, args=(alpha, n, callback), daemon=True).start()

# GUI Setup
root = tk.Tk()
root.title("🎓 Critical r Calculator & Visualizer")
root.geometry("1000x800")
root.configure(bg="#eaf3f8")

# Title
tk.Label(root, text="Pearson r Critical Value Visualizer", font=("Helvetica", 18, "bold"), bg="#eaf3f8", fg="#003366").pack(pady=10)

# Inputs
input_frame = tk.Frame(root, bg="#eaf3f8")
input_frame.pack(pady=5)

tk.Label(input_frame, text="Significance Level (α):", bg="#eaf3f8").grid(row=0, column=0, sticky="e")
alpha_entry = tk.Entry(input_frame, width=10)
alpha_entry.insert(0, "0.05")
alpha_entry.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="Sample Size (n):", bg="#eaf3f8").grid(row=0, column=2, sticky="e")
n_entry = tk.Entry(input_frame, width=10)
n_entry.insert(0, "30")
n_entry.grid(row=0, column=3, padx=5)

tk.Button(input_frame, text="Calculate & Plot", command=run_in_thread, bg="#007acc", fg="white", font=("Helvetica", 10, "bold")).grid(row=0, column=4, padx=10)

# Result Label
result_label = tk.Label(root, text="Critical r = ±...", font=("Helvetica", 14), bg="#eaf3f8")
result_label.pack(pady=10)

# Plot Canvas
canvas_frame = tk.Frame(root, bg="#eaf3f8")
canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# Calculation Summary
tk.Label(root, text="Calculation Summary", font=("Helvetica", 12, "bold"), bg="#eaf3f8", fg="#444").pack()
calc_text = tk.Text(root, height=7, width=60, font=("Courier", 10), bg="#f9f9f9", borderwidth=2, relief="sunken")
calc_text.pack(pady=5)
calc_text.config(state="disabled")

# App Legend
tk.Label(root, text="📘 About This App", font=("Helvetica", 12, "bold"), bg="#eaf3f8", fg="#444").pack(pady=(10, 0))
legend = tk.Label(root, text=(
    "This tool visualizes the critical Pearson correlation value based on your input.\n"
    "• α — Significance level (e.g., 0.01 or 0.05)\n"
    "• n — Sample size (must be ≥ 3)\n"
    "• df — Degrees of freedom used in t-distribution\n"
    "• r_critical — Minimum correlation strength for significance\n"
    "All math is derived from t-distribution and correlation formulas."
), bg="#eaf3f8", justify="left", font=("Helvetica", 10))
legend.pack(pady=5)

root.mainloop()

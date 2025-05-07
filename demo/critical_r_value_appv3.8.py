import tkinter as tk
from tkinter import messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from scipy.stats import t
import numpy as np
import matplotlib

def calculate_r_critical(alpha, n, tail_type="2-tailed"):
    df = n - 2
    if df <= 0:
        raise ValueError("Sample size must be at least 3.")
    if tail_type == "1-tailed":
        t_crit = t.ppf(1 - alpha, df)
    else:
        t_crit = t.ppf(1 - alpha / 2, df)
    r_crit = t_crit / np.sqrt(t_crit**2 + df)
    return r_crit, t_crit, df

def calculate_and_plot():
    try:
        alpha = float(entry_alpha.get())
        n = int(entry_n.get())
        tail_type = tail_mode.get()

        r_critical, t_critical, df = calculate_r_critical(alpha, n, tail_type)

        result_label.config(text=f"Critical r-value (±): {r_critical:.3f}")

        ax.clear()
        # Plotting the full t-distribution
        x_vals = np.linspace(-5, 5, 1000)
        y_vals = t.pdf(x_vals, df)
        ax.plot(x_vals, y_vals, color='black', label='t-distribution')

        if tail_type == "1-tailed":
            x_fill = np.linspace(t_critical, 5, 500)
            ax.fill_between(x_fill, t.pdf(x_fill, df), color='red', alpha=0.5, label=f'Critical region (α = {alpha})')
            ax.axvline(t_critical, color='red', linestyle='--', label=f't_critical = {t_critical:.3f}')
        else:
            t_crit_pos = t_critical
            t_crit_neg = -t_critical
            x_fill_right = np.linspace(t_crit_pos, 5, 500)
            x_fill_left = np.linspace(-5, t_crit_neg, 500)
            ax.fill_between(x_fill_right, t.pdf(x_fill_right, df), color='red', alpha=0.5, label=f'Right critical region (α/2 = {alpha/2})')
            ax.fill_between(x_fill_left, t.pdf(x_fill_left, df), color='blue', alpha=0.5, label=f'Left critical region (α/2 = {alpha/2})')
            ax.axvline(t_crit_pos, color='red', linestyle='--', label=f'+t_critical = {t_crit_pos:.3f}')
            ax.axvline(t_crit_neg, color='blue', linestyle='--', label=f'-t_critical = {t_crit_neg:.3f}')

        ax.set_title("t-Distribution with Critical Region", fontsize=28)
        ax.set_xlabel('t-value', fontsize=24)
        ax.set_ylabel('Probability Density', fontsize=24)
        ax.legend(fontsize=16)
        canvas.draw()

        calc_summary.config(text=f"""n = {n}
df = {df}
α = {alpha}
t_critical = {t_critical:.4f}
r_critical = ± {r_critical:.4f} ({tail_type})""")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def save_plot():
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        fig.savefig(file_path)
        messagebox.showinfo("Saved", f"Plot saved to:\n{file_path}")

def exit_app():
    root.destroy()
    root.protocol("WM_DELETE_WINDOW", exit_app)

root = tk.Tk()
root.title("Critical r-value Calculator and Visualizer AJ")
root.geometry("2400x1800")

try:
    root.iconbitmap("app_icon.ico")
except Exception:
    pass

top_frame = tk.Frame(root, bg="#e6f0ff", padx=10, pady=5)
top_frame.pack(fill=tk.X)

tk.Label(top_frame, text="Significance Level (α):", bg="#e6f0ff", font=("Arial", 24)).pack(side=tk.LEFT)
entry_alpha = tk.Entry(top_frame, width=6, font=("Arial", 24))
entry_alpha.insert(0, "0.05")
entry_alpha.pack(side=tk.LEFT, padx=(0, 15))

tk.Label(top_frame, text="Sample Size (n):", bg="#e6f0ff", font=("Arial", 24)).pack(side=tk.LEFT)
entry_n = tk.Entry(top_frame, width=6, font=("Arial", 24))
entry_n.insert(0, "14")
entry_n.pack(side=tk.LEFT, padx=(0, 15))



tail_mode = tk.StringVar(value="2-tailed")
tk.Label(top_frame, text="Test Type:", bg="#e6f0ff", font=("Arial", 24)).pack(side=tk.LEFT, padx=(15, 0))


tail_option = tk.OptionMenu(top_frame, tail_mode, "1-tailed", "2-tailed")
tail_option.config(font=("Arial", 24))

# Configure dropdown menu font (this is the key part)
tail_option["menu"].config(font=("Arial", 24))
tail_option.pack(side=tk.LEFT, padx=(0, 15))




tk.Button(top_frame, text="Calculate & Plot", command=calculate_and_plot, bg="#007acc", fg="white", font=("Arial", 24, "bold")).pack(side=tk.LEFT, padx=5)
tk.Button(top_frame, text="💾 Save Plot", command=save_plot, bg="#28a745", fg="white", font=("Arial", 24, "bold")).pack(side=tk.LEFT, padx=5)
tk.Button(top_frame, text="❌ Exit", command=exit_app, bg="#cc0000", fg="white", font=("Arial", 24, "bold")).pack(side=tk.LEFT, padx=5)

result_label = tk.Label(root, text="Critical r-value (±): ", font=("Arial", 26, "bold"))
result_label.pack(pady=5)

main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

left_panel = tk.Frame(main_frame)
left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

fig, ax = plt.subplots(figsize=(7, 5))
canvas = FigureCanvasTkAgg(fig, master=left_panel)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

right_panel = tk.Frame(main_frame, bg="#f0f6ff", width=820, padx=50)
right_panel.pack(side=tk.RIGHT, fill=tk.Y)
right_panel.pack_propagate(0)

tk.Label(
    right_panel,
    text="🧮 Calculation Summary",
    font=("Helvetica", 27, "bold"),
    bg="#f0f6ff",
    fg="#003366"
).pack(pady=(5, 2))

calc_summary = tk.Label(
    right_panel,
    text="",
    bg="#f0f6ff",
    justify="left",
    font=("Courier", 22)
)
calc_summary.pack(pady=(0, 10), padx=5, anchor="w")

tk.Label(
    right_panel,
    text="📘 About This App",
    font=("Helvetica", 27, "bold"),
    bg="#f0f6ff",
    fg="#003366"
).pack(pady=(5, 2))

formula_block = tk.Label(
    right_panel,
    text=(
        "Formulas Used:\n"
        "  r = t / sqrt(t² + (n-2))\n"
        "  t = r*sqrt(n-2) / sqrt(1-r²)\n"
        "  df = n-2"
    ),
    bg="#f0f6ff",
    justify="left",
    font=("Courier", 20),
    fg="#2c3e50"
)
formula_block.pack(pady=(0, 8), padx=5, anchor="w")

legend = tk.Label(
    right_panel,
    text=(
        "This tool visualizes the critical Pearson r-value\n"
        "based on significance level (α) and sample size (n).\n\n"
        "📌 Inputs:\n"
        "  α — Significance level (e.g., 0.01, 0.05)\n"
        "  n — Sample size ≥ 3\n\n"
        "📐 Outputs:\n"
        "  df = n - 2\n"
        "  t_critical — from t-distribution\n"
        "  r_critical — Pearson correlation threshold"
    ),
    bg="#f0f6ff",
    justify="left",
    font=("Helvetica", 21),
    wraplength=860,
    anchor="w"
)
legend.pack(pady=(0, 10), padx=5, fill=tk.BOTH)

#root.mainloop()


# Ensure full shutdown when window is closed
root.protocol("WM_DELETE_WINDOW", exit_app)

# Run main loop
root.mainloop()
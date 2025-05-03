import tkinter as tk
from tkinter import messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from scipy.stats import t
import numpy as np

def calculate_r_critical(alpha, n):
    df = n - 2
    if df <= 0:
        raise ValueError("Sample size must be at least 3.")
    t_crit = t.ppf(1 - alpha / 2, df)
    r_crit = t_crit / np.sqrt(t_crit**2 + df)
    return r_crit, t_crit, df

def calculate_and_plot():
    try:
        alpha = float(entry_alpha.get())
        n = int(entry_n.get())
        r_critical, t_critical, df = calculate_r_critical(alpha, n)

        result_label.config(text=f"Critical r-value (±): {r_critical:.3f}")

        ax.clear()
        n_vals = np.arange(3, 101)
        r_vals = [calculate_r_critical(alpha, i)[0] for i in n_vals]
        ax.plot(n_vals, r_vals, label='r_critical vs n', color='green')
        ax.axhline(y=r_critical, color='red', linestyle='--', label=f'+r_critical = {r_critical:.3f}')
        ax.axhline(y=-r_critical, color='blue', linestyle='--', label=f'-r_critical = {-r_critical:.3f}')
        ax.set_xlabel('Sample Size (n)', fontsize=12)
        ax.set_ylabel('Critical r-value', fontsize=12)
        ax.set_title('Critical r-value vs Sample Size', fontsize=14)
        ax.set_ylim(-1, 1)
        ax.legend()
        canvas.draw()

        calc_summary.config(text=f"""n = {n}
df = {df}
α = {alpha}
t_critical = {t_critical:.4f}
r_critical = ± {r_critical:.4f}""")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def save_plot():
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        fig.savefig(file_path)
        messagebox.showinfo("Saved", f"Plot saved to:\n{file_path}")

root = tk.Tk()
root.title("Critical r-value Calculator and Visualizer AJ")
root.geometry("1280x750")

try:
    root.iconbitmap("app_icon.ico")
except Exception:
    pass  # Ignore missing icon

top_frame = tk.Frame(root, bg="#e6f0ff", padx=10, pady=5)
top_frame.pack(fill=tk.X)

tk.Label(top_frame, text="Significance Level (α):", bg="#e6f0ff", font=("Arial", 12)).pack(side=tk.LEFT)
entry_alpha = tk.Entry(top_frame, width=6, font=("Arial", 12))
entry_alpha.insert(0, "0.05")
entry_alpha.pack(side=tk.LEFT, padx=(0, 15))

tk.Label(top_frame, text="Sample Size (n):", bg="#e6f0ff", font=("Arial", 12)).pack(side=tk.LEFT)
entry_n = tk.Entry(top_frame, width=6, font=("Arial", 12))
entry_n.insert(0, "14")
entry_n.pack(side=tk.LEFT, padx=(0, 15))

tk.Button(top_frame, text="Calculate & Plot", command=calculate_and_plot, bg="#007acc", fg="white", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
tk.Button(top_frame, text="💾 Save Plot", command=save_plot, bg="#28a745", fg="white", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)

result_label = tk.Label(root, text="Critical r-value (±): ", font=("Arial", 14, "bold"))
result_label.pack(pady=5)

main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

left_panel = tk.Frame(main_frame)
left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

fig, ax = plt.subplots(figsize=(7, 5))
canvas = FigureCanvasTkAgg(fig, master=left_panel)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

right_panel = tk.Frame(main_frame, bg="#f0f6ff", width=350, padx=10)
right_panel.pack(side=tk.RIGHT, fill=tk.Y)
right_panel.pack_propagate(0)

tk.Label(right_panel, text="🧮 Calculation Summary", font=("Helvetica", 13, "bold"), bg="#f0f6ff", fg="#003366").pack(pady=(5, 2))
calc_summary = tk.Label(right_panel, text="", bg="#f0f6ff", justify="left", font=("Courier", 12))
calc_summary.pack(pady=(0, 10), padx=5, anchor="w")

tk.Label(right_panel, text="📘 About This App", font=("Helvetica", 13, "bold"), bg="#f0f6ff", fg="#003366").pack(pady=(5, 2))

formula_block = tk.Label(
    right_panel,
    text=(
        "Formulas Used:\n"
        "  r = t / sqrt(t² + (n − 2))\n"
        "  t = r × sqrt(n − 2) / sqrt(1 − r²)\n"
        "  df = n − 2"
    ),
    bg="#f0f6ff",
    justify="left",
    font=("Courier", 11),
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
    font=("Helvetica", 11),
    wraplength=300,
    anchor="w"
)
legend.pack(pady=(0, 10), padx=5, fill=tk.BOTH)

root.mainloop()

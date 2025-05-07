import tkinter as tk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.stats import t
import threading

# Set up main window
root = tk.Tk()
root.title("Critical r-value Calculator and Visualizer")
root.geometry("1200x700")
root.configure(bg="#eaf3f8")

latest_fig = None

# === Input Frame ===
input_frame = tk.Frame(root, bg="#d1eaff")
input_frame.pack(fill=tk.X, padx=20, pady=10)

tk.Label(input_frame, text="Significance Level (α):", bg="#d1eaff").grid(row=0, column=0, padx=5, pady=5)
alpha_entry = tk.Entry(input_frame)
alpha_entry.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="Sample Size (n):", bg="#d1eaff").grid(row=0, column=2, padx=5)
n_entry = tk.Entry(input_frame)
n_entry.grid(row=0, column=3, padx=5)

def save_plot():
    if latest_fig:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            title="Save plot as..."
        )
        if file_path:
            latest_fig.savefig(file_path, dpi=300)
            messagebox.showinfo("Saved", f"Plot saved to:\n{file_path}")
    else:
        messagebox.showwarning("No Plot", "Please generate a plot first.")

def run_in_thread():
    threading.Thread(target=calculate_and_plot).start()

tk.Button(input_frame, text="Calculate & Plot", command=run_in_thread, bg="#007acc", fg="white", font=("Helvetica", 10, "bold")).grid(row=0, column=4, padx=10)
tk.Button(input_frame, text="💾 Save Plot", command=save_plot, bg="#28a745", fg="white", font=("Helvetica", 10, "bold")).grid(row=0, column=5, padx=5)

result_label = tk.Label(root, text="", font=("Helvetica", 12, "bold"), bg="#eaf3f8", fg="#333")
result_label.pack(pady=5)

# === Main Panel Layout ===
main_frame = tk.Frame(root, bg="#eaf3f8")
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# Left Plot Area
canvas_frame = tk.Frame(main_frame, bg="#eaf3f8")
canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Right Info Panel
right_panel = tk.Frame(main_frame, bg="#f0f6ff", bd=2, relief="groove")
right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

tk.Label(right_panel, text="🧮 Calculation Summary", font=("Helvetica", 11, "bold"), bg="#f0f6ff", fg="#003366").pack(pady=(10, 2))
calc_text = tk.Text(right_panel, height=10, width=40, font=("Courier", 10), bg="#f9f9f9", borderwidth=2, relief="sunken")
calc_text.pack(pady=(0, 10))
calc_text.config(state="disabled")














tk.Label(right_panel, text="📘 About This App", font=("Helvetica", 11, "bold"), bg="#f0f6ff", fg="#003366").pack(pady=(5, 2))
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
    font=("Helvetica", 9),
    wraplength=300,
    anchor="w"
)
legend.pack(pady=(0, 10), padx=5, fill=tk.BOTH)



def calculate_and_plot():
    global latest_fig
    try:
        alpha = float(alpha_entry.get())
        n = int(n_entry.get())
        if n < 3:
            raise ValueError("Sample size n must be ≥ 3.")

        df = n - 2
        t_crit = t.ppf(1 - alpha / 2, df)
        r_crit = t_crit / ((t_crit ** 2 + df) ** 0.5)

        result_label.config(text=f"Critical r-value (±): {r_crit:.3f}")

        # Create figure
        fig, ax = plt.subplots(figsize=(8, 5))
        latest_fig = fig

        ax.axhline(y=r_crit, color="red", linestyle="--", label=f"+r_critical = {r_crit:.3f}")
        ax.axhline(y=-r_crit, color="blue", linestyle="--", label=f"-r_critical = {-r_crit:.3f}")

        # Scatter: show how r_critical behaves over different n
        sample_sizes = list(range(3, 100))
        critical_rs = [
            t.ppf(1 - alpha / 2, df=n_i - 2) / ((t.ppf(1 - alpha / 2, df=n_i - 2) ** 2 + (n_i - 2)) ** 0.5)
            for n_i in sample_sizes
        ]
        ax.plot(sample_sizes, critical_rs, label="r_critical vs n", color="green")

        ax.set_title("Critical r-value vs Sample Size")
        ax.set_xlabel("Sample Size (n)")
        ax.set_ylabel("Critical r-value")
        ax.set_ylim(-1, 1)
        ax.grid(True)
        ax.legend(loc="upper right")

        # Add LaTeX-style formulas
        formulas = [
            r"$r = \frac{t}{\sqrt{t^2 + (n - 2)}}$",
            r"$t = \frac{r \cdot \sqrt{n - 2}}{\sqrt{1 - r^2}}$",
            r"$df = n - 2$"
        ]
        for i, formula in enumerate(formulas):
            ax.text(1.02, 0.95 - i * 0.1, formula, transform=ax.transAxes,
                    fontsize=10, verticalalignment='top', bbox=dict(boxstyle="round", fc="#f0f0f0"))

        # Clear and redraw
        for widget in canvas_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Display Calculation Summary
        calc_summary = (
            f"n = {n}\n"
            f"df = {df}\n"
            f"α = {alpha}\n"
            f"t_critical = {t_crit:.4f}\n"
            f"r_critical = ± {r_crit:.4f}"
        )
        calc_text.config(state="normal")
        calc_text.delete("1.0", tk.END)
        calc_text.insert(tk.END, calc_summary)
        calc_text.config(state="disabled")

    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

# Run the app
root.mainloop()

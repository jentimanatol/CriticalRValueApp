# 🧠 Auto Typer GUI

![Release](https://img.shields.io/github/v/release/jentimanatol/auto_typer_app?label=Latest%20Release&style=for-the-badge)
![Platform](https://img.shields.io/badge/platform-Windows-blue?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)



# 📊 Critical r-value Calculator and Visualizer AJ

**Critical r-value Calculator and Visualizer AJ** is a powerful yet simple GUI-based tool for students, researchers, data scientists, and statistics educators to **calculate and visualize the critical Pearson correlation threshold** (r-value) based on significance level (α) and sample size (n). 

✨ **No coding required — just enter values and see the plot!**

---









### 📦 Download the Latest Version


🔽 **[Critical r-value Calculator and Visualizer AJ v2.9 (.exe)](https://github.com/jentimanatol/CriticalRValueApp/releases/download/v2.9/critical_r_value_app.exe)
**

📌 Or check for newer versions and souce code:  
👉 **[See all releases](https://github.com/jentimanatol/CriticalRValueApp/releases)**

---



## 🚀 Features

- 🔢 **Calculate critical r-value** from α and sample size
- 📈 **Visualize** the relationship between r_critical and increasing sample size
- 💾 **Save the plot** as a PNG file for reports or presentations
- 📘 **View formulas and step-by-step summary** used in the calculation
- 🎨 Clean and modern GUI (built with `Tkinter` and `matplotlib`)

---

## 📌 What is this tool used for?

This app is ideal for:
- 📚 **Students** learning correlation significance and hypothesis testing
- 🧪 **Researchers** validating Pearson r-test thresholds
- 🧠 **Instructors** teaching critical value concepts visually
- 📊 **Data analysts** interpreting r-values confidently

When working with **Pearson correlation**, it's essential to compare your calculated r-value with a threshold to determine statistical significance. This tool helps you understand **how this threshold changes** as your sample size or significance level changes.

---

## 🛠 How to Use

1. **Enter Significance Level (α)**  
   Example: `0.05` for 95% confidence

2. **Enter Sample Size (n)**  
   Must be ≥ 3 (e.g., `14`)

3. **Click “Calculate & Plot”**  
   The app will display:
   - Calculated critical r-value (±)
   - Sample size and degrees of freedom
   - t-critical and formula summary
   - A clear plot of r_critical vs. sample size

4. **Click “💾 Save Plot”**  
   Export the visual as a `.png` for your project or paper.

---

## 📷 Screenshot

![Critical r-value Calculator and Visualizer AJ](https://github.com/jentimanatol/CriticalRValueApp/blob/22b0aca92b839a9518525e35158d3d08e1b72f71/screenshots/screenshots.png) <!-- Replace with your image URL or local path -->

---

## 🔍 Behind the Scenes – Formula Reference

```$Degrees of Freedom: df = n - 2
t-critical:        from two-tailed t-distribution at α
r-critical:        r = t / √(t² + df)$```






_Not protected by copyright, may be used for its intended purpose._  
_Author: Anatolie Jentimir._

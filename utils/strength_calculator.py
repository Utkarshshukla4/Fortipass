import math
import re
from datetime import datetime
from dateutil.parser import parse as parse_date
from .patterns import detect_patterns

# ---------------- Character sets and common words ----------------
CHARSETS = {
    'lower': 26,
    'upper': 26,
    'digits': 10,
    'symbols': 32,  # approximation
}

COMMON_WORDS = set([
    'password', '123456', 'qwerty', 'letmein', 'admin', 'welcome',
    'iloveyou', 'user', 'test'
])

# ---------------- Entropy & Crack Time Calculations ----------------
def estimate_entropy(password: str) -> float:
    pool = 0
    if re.search(r'[a-z]', password): pool += CHARSETS['lower']
    if re.search(r'[A-Z]', password): pool += CHARSETS['upper']
    if re.search(r'\d', password): pool += CHARSETS['digits']
    if re.search(r'[^\w\s]', password): pool += CHARSETS['symbols']

    if pool == 0:
        pool = max(2, len(set(password)))

    entropy = len(password) * math.log2(pool) if len(password) > 0 else 0
    return entropy


def estimate_crack_time_seconds(entropy_bits: float, guesses_per_second=1e9) -> float:
    guesses = 2 ** entropy_bits if entropy_bits < 60 else math.exp(entropy_bits * math.log(2))
    return guesses / guesses_per_second


def human_time(seconds: float) -> str:
    if seconds < 1:
        return f"{seconds:.2f} seconds"
    intervals = [
        ('years', 60*60*24*365),
        ('days', 60*60*24),
        ('hours', 3600),
        ('minutes', 60),
        ('seconds', 1)
    ]
    for name, sec in intervals:
        if seconds >= sec:
            val = seconds / sec
            if name == 'years' and val > 1000:
                return f"> {int(val):,} years"
            return f"{val:.2f} {name}"
    return f"{seconds:.2f} seconds"


def score_label_from_entropy(e: float) -> str:
    if e < 28:
        return 'Very Weak'
    if e < 36:
        return 'Weak'
    if e < 60:
        return 'Reasonable'
    if e < 80:
        return 'Strong'
    return 'Very Strong'

# ---------------- Main Password Analyzer ----------------
def analyze_password(password: str) -> dict:
    pwd = password or ''
    entropy = estimate_entropy(pwd)
    crack_seconds = estimate_crack_time_seconds(entropy)
    label = score_label_from_entropy(entropy)
    patterns = detect_patterns(pwd)

    suggestions = []
    # length
    if len(pwd) < 8:
        suggestions.append('Increase length to at least 12 characters.')
    elif len(pwd) < 12:
        suggestions.append('Longer passwords (>12 chars) significantly increase strength.')
    # variety
    if not re.search(r'[A-Z]', pwd):
        suggestions.append('Add uppercase letters.')
    if not re.search(r'[a-z]', pwd):
        suggestions.append('Add lowercase letters.')
    if not re.search(r'\d', pwd):
        suggestions.append('Add digits.')
    if not re.search(r'[^\w\s]', pwd):
        suggestions.append('Add symbols (e.g., !@#$%).')
    # simple/common
    if pwd.lower() in COMMON_WORDS:
        suggestions.append('Avoid common words or simple numeric sequences.')
    # pattern-based
    for p in patterns:
        if p['type'] == 'repeat':
            suggestions.append('Avoid repeated characters (e.g., "aaaa" or "1111").')
        if p['type'] == 'sequence':
            suggestions.append('Avoid keyboard sequences like "qwerty" or "1234".')
        if p['type'] == 'date':
            suggestions.append('Avoid dates (birthdays, years). Dates are easy to guess.')
        if p['type'] == 'dictionary':
            suggestions.append('Avoid dictionary words or names.')

    # remove duplicates
    seen = set()
    final_suggestions = []
    for s in suggestions:
        if s not in seen:
            final_suggestions.append(s)
            seen.add(s)

    return {
        'entropy_bits': round(entropy, 2),
        'crack_time_seconds': crack_seconds,
        'crack_time_readable': human_time(crack_seconds),
        'score_label': label,
        'patterns': patterns,
        'suggestions': final_suggestions,
        'length': len(pwd)
    }

# ---------------- GUI Wrapper (for manual testing) ----------------
if __name__ == "__main__":
    import tkinter as tk
    from tkinter import ttk, messagebox

    def launch_password_gui():
        root = tk.Tk()
        root.title("Password Strength Analyzer")
        root.geometry("420x420")

        tk.Label(root, text="Enter Password:", font=("Arial", 11)).pack(pady=8)
        password_entry = tk.Entry(root, show="*", width=35, font=("Arial", 11))
        password_entry.pack(pady=5)

        # --- Toggle visibility ---
        def toggle_password():
            if password_entry.cget('show') == '':
                password_entry.config(show='*')
                toggle_btn.config(text="Show")
            else:
                password_entry.config(show='')
                toggle_btn.config(text="Hide")

        toggle_btn = tk.Button(root, text="Show", command=toggle_password)
        toggle_btn.pack(pady=5)

        result_label = tk.Label(root, text="", font=("Arial", 11), fg="blue")
        result_label.pack(pady=10)

        suggestions_box = tk.Text(root, width=48, height=8, wrap="word")
        suggestions_box.pack(pady=8)

        def check_strength():
            pwd = password_entry.get()
            if not pwd:
                messagebox.showwarning("Warning", "Please enter a password.")
                return
            result = analyze_password(pwd)
            result_label.config(
                text=f"Strength: {result['score_label']} | Entropy: {result['entropy_bits']} bits\n"
                     f"Estimated crack time: {result['crack_time_readable']}"
            )
            suggestions_box.delete(1.0, tk.END)
            if result['suggestions']:
                suggestions_box.insert(tk.END, "Suggestions:\n" + "\n".join(result['suggestions']))
            else:
                suggestions_box.insert(tk.END, "No suggestions — strong password!")

        tk.Button(root, text="Check Strength", command=check_strength, bg="#2b7a78", fg="white",
                  font=("Arial", 10, "bold")).pack(pady=10)

        root.mainloop()

    launch_password_gui()

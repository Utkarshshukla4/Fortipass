##  Overview

**FortiPass** is an intelligent, GUI-based **Password Strength Analyzer** built with **Flask (Python)**.  
FortiPass = Fortified Password — meaning “make your password stronger.”
It provides **real-time password analysis**, including entropy score, estimated crack time, and AI-based improvement suggestions.  
The tool aims to **educate users on password security** and visualize how strength changes with better character variety.

FortiPass works on both **Windows** and **Linux** environments and is built entirely using **Python + Flask + HTML + CSS + JS**.


##  Features

 **Real-time Strength Analysis** | Calculates entropy bits and evaluates password robustness. |
 **Interactive GUI (Flask Web App)** | User-friendly interface with dynamic strength meter. |
 **Entropy & Crack Time Estimation** | Mathematical formula to predict time to brute-force. |
 **Pattern Detection** | Detects common words, sequences, dates, and repetitions. |
 **Smart Suggestions** | Suggests improvements based on missing character types. |
 **Report Dashboard** | Displays analyzed passwords (hashed IDs only). |
 **Cross-Platform** | Works on both Windows & Linux. |
 


##  Architecture 


      ┌──────────────────────────┐
      │        User GUI          │
      │ (HTML/CSS/JS in Flask)   │
      └──────────┬───────────────┘
                 │
                 ▼
      ┌──────────────────────────┐
      │       Flask Backend      │
      │  (app.py routes)         │
      └──────────┬───────────────┘
                 │
                 ▼
      ┌──────────────────────────┐
      │  Strength Analyzer Logic │
      │ (utils/strength_calculator.py) 
      └──────────┬───────────────┘
                 │
                 ▼
      ┌──────────────────────────┐
      │  Pattern Recognition     │
      │ (utils/patterns.py)      │
      └──────────────────────────┘


## What FortiPass Does

Lets users enter a password through a clean web GUI.

Analyses in Entropy = password strength measured in randomness. (More random → higher entropy → stronger password.)

Shows a strength label (Very Weak - Very Strong).

Gives an estimated crack time (how long it might take to guess).

Can generate reports (summaries of tested passwords).



##  Project Structure

FortiPass/
│
├── app.py # Main Flask application
├── requirements.txt # Python dependencies
├── .gitignore # Ignore unwanted files
├── README.md # Documentation
│
├── templates/
│ ├── index.html # Main dashboard page
│ └── report.html # Report display page
│
├── static/
│ ├── style.css # Styling for the web interface
│ └── script.js # JavaScript for real-time updates
│
└── utils/
├── strength_calculator.py # Entropy and password logic
└── patterns.py # Common pattern detection



##  Installation & Running


git clone https://github.com/<Utkarshshukla4>/FortiPass.git

cd FortiPass

## Create Virtual Environment

Windows:

python -m venv venv

venv\Scripts\activate

Linux/Mac:

python3 -m venv venv

source venv/bin/activate

## Install Dependencies

pip install -r requirements.txt

## Run the Application

python app.py

Now open your browser and visit:
👉 http://127.0.0.1:5000

## Input Example

Example 1

Password Entered: qwerty123

## Output:

Entropy: 28.6 bits

Strength Label: Weak

Estimated Crack Time: 4.1 seconds

Suggestions:

Add uppercase letters.

Add special characters.

Avoid keyboard sequences like "qwerty".

## Example 2

Password Entered: G#Tech@2035$

## Output:

Entropy: 78.4 bits

Strength Label: Strong

Estimated Crack Time: 12.5 years

Suggestions:

Great! Your password is strong and diverse.

## Output Visualization

The dashboard shows:

Parameter	Description
Strength Bar	Dynamic color meter — Red (Weak) → Green (Strong).
Entropy	Numerical measure of randomness.
Crack Time	Estimated time to brute-force.
Suggestions	Tips for improving password quality.

## Summary

FortiPass helps users learn about password security interactively.

Combines data science (entropy) + frontend UX for better understanding.

Suitable for cybersecurity students, AI/ML beginners, and Flask learners.

Built to run easily on any local system.

Fully open-source and customizable.

## Developed By

Utkarsh Shukla

Cybersecurity Enthusiast

 Email: utqrshkumar07@gmail.com
 GitHub: https://github.com/Utkarshshukla4


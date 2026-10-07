# AI Career Guide and Resume Analyzer

A beginner-friendly Flask web app that helps users:

- create a personal 30-day career learning plan
- analyze a resume against a target role
- find job portals related to the role
- access ATS-friendly resume resources

The app uses Python, Flask, HTML, CSS, JavaScript, and the Google Gemini API when available. If the AI service is unavailable, it falls back to local rules-based analysis so the app still works.

## Features

- AI Career Guide form with name, target role, skills, and available daily time
- 30-day learning plan with tasks, resources, and estimated time
- Resume upload support for PDF, DOCX, and TXT files
- ATS-style score and improvement suggestions
- Job portal search links for the selected role
- ATS-friendly resume resource cards
- Clear error handling for missing or invalid Gemini API configuration
- Graceful fallback when Gemini is unavailable

## Project Structure

```text
AI Career Guide and Resume Analyzer/
├── app.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
├── data/
│   ├── career_roles.json
│   ├── learning_resources.json
│   └── job_portals.json
├── uploads/
│   └── .gitkeep
├── templates/
│   ├── index.html
│   ├── career_guide.html
│   ├── resume_analyzer.html
│   └── result.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── main.js
│       ├── career_guide.js
│       └── resume_analyzer.js
└── utils/
    ├── __init__.py
    ├── gemini_service.py
    ├── resume_parser.py
    ├── ats_scorer.py
    └── resource_manager.py
```

## Python Version

This project is designed for Python 3.10 or newer.

## 1. Create a Virtual Environment

Open PowerShell in the project folder and run:

```powershell
python -m venv .venv
```

## 2. Activate the Virtual Environment on Windows

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run this first:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

## 3. Install Project Dependencies

```powershell
pip install -r requirements.txt
```

## 4. Create .env File

Create a file named `.env` in the project root with the following contents:

```env
GEMINI_API_KEY=your_api_key_here
```

You can copy the example file:

```powershell
Copy-Item .env.example .env
```

## 5. Add Your Gemini API Key

To use Gemini features, add your actual API key in the `.env` file.

Example:

```env
GEMINI_API_KEY=AIzaSyourRealGeminiKeyHere
```

> Do not commit your real API key to version control. The `.env` file is already ignored in `.gitignore`.

## 6. Run the Flask Application

From the project root:

```powershell
python app.py
```

The app will start on:

```text
http://127.0.0.1:5000
```

## 7. Open the App in the Browser

Visit:

```text
http://127.0.0.1:5000
```

Then click:

- Build My Career Roadmap
- Analyze My Resume

## 8. Troubleshooting Gemini API Errors

Common issues:

- Missing API key: add `GEMINI_API_KEY` to `.env`
- Invalid API key: check the key and restart the app
- Quota limit: wait and try again later
- Network problem: confirm internet access
- Model unavailable: the app will show a friendly fallback message

The app is designed to display user-friendly messages instead of raw technical errors.

## 9. Troubleshooting Missing Packages

If a package is missing, reinstall dependencies:

```powershell
pip install -r requirements.txt
```

If Python cannot find the packages, make sure your virtual environment is active.

## 10. Stop the Server

In the terminal, press:

```text
Ctrl + C
```

## Notes

- Uploaded resume files are processed in a temporary file and deleted after analysis.
- The app does not expose the API key to the frontend.
- If Gemini fails temporarily, the app still gives a useful fallback plan or local ATS-style analysis.

## Beginner Tips

- Keep the `.venv` active while working.
- Use the browser console only for frontend debugging.
- Watch the Flask terminal for error logs when debugging backend issues.

import logging
import os

from flask import Flask, jsonify, render_template, request

from utils.ats_scorer import score_resume_for_role
from utils.gemini_service import generate_career_plan_with_gemini, generate_resume_analysis_with_gemini
from utils.resource_manager import get_ats_resources, get_job_portals_for_role, get_role_data, get_role_names
from utils.resume_parser import detect_contact_info, detect_resume_sections, extract_text_from_file, validate_uploaded_file

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "uploads")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/career-guide")
def career_guide():
    return render_template("career_guide.html", roles=get_role_names())


@app.route("/resume-analyzer")
def resume_analyzer():
    return render_template("resume_analyzer.html", roles=get_role_names())


@app.route("/result")
def result_page():
    return render_template("result.html")


@app.route("/generate-career-plan", methods=["POST"])
def generate_career_plan():
    if request.is_json:
        payload = request.get_json(silent=True) or {}
    else:
        payload = request.form.to_dict()

    name = (payload.get("name") or "Learner").strip()
    role_name = (payload.get("target_role") or payload.get("role") or "").strip()
    current_skills = (payload.get("current_skills") or "").strip()
    available_time = payload.get("available_time_per_day") or payload.get("available_time") or "1"
    total_days = payload.get("plan_days") or payload.get("days") or "30"

    if not role_name:
        return jsonify({"success": False, "error": "Please select a target role."}), 400

    try:
        available_hours = float(available_time)
    except (TypeError, ValueError):
        available_hours = 1

    try:
        plan_days = int(total_days)
    except (TypeError, ValueError):
        plan_days = 30

    plan_days = max(5, min(plan_days, 90))
    available_hours = max(1, min(available_hours, 12))

    gen_result = generate_career_plan_with_gemini(name, role_name, current_skills, available_hours, plan_days)
    return jsonify({
        "success": True,
        "fallback": gen_result.get("fallback", False),
        "error": gen_result.get("error"),
        "plan": gen_result.get("plan", {}),
    })


@app.route("/analyze-resume", methods=["POST"])
def analyze_resume():
    target_role = (request.form.get("target_role") or "").strip()
    uploaded_file = request.files.get("resume")

    if not target_role:
        return jsonify({"success": False, "error": "Please select a target role before analysis."}), 400

    if uploaded_file is None or not uploaded_file.filename:
        return jsonify({"success": False, "error": "Please upload a resume file."}), 400

    try:
        validate_uploaded_file(uploaded_file)
        resume_text = extract_text_from_file(uploaded_file)
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400
    except Exception as exc:
        logging.exception("Resume parsing failed")
        return jsonify({"success": False, "error": "The resume could not be processed. Please try a different file."}), 400

    role_data = get_role_data(target_role)
    score_result = score_resume_for_role(resume_text, target_role, role_data)
    ai_result = generate_resume_analysis_with_gemini(target_role, resume_text)

    sections = detect_resume_sections(resume_text)
    contacts = detect_contact_info(resume_text)

    analysis_data = ai_result.get("analysis", {})
    summary = analysis_data.get("summary", f"Resume needs stronger alignment with {target_role} requirements.")

    final_response = {
        "success": True,
        "fallback": ai_result.get("fallback", False),
        "error": ai_result.get("error"),
        "score": score_result,
        "summary": summary,
        "analysis": {
            "summary": summary,
            "skills_to_add": analysis_data.get("skills_to_add", []),
            "skills_to_improve": analysis_data.get("skills_to_improve", []),
            "certifications": analysis_data.get("certifications", []),
            "projects": analysis_data.get("projects", []),
            "sections_to_improve": analysis_data.get("sections_to_improve", []),
            "role_keywords": analysis_data.get("role_keywords", []),
        },
        "local_insights": {
            "text_length": len(resume_text),
            "sections": sections,
            "contact_info": contacts,
        },
        "job_portals": get_job_portals_for_role(target_role),
        "ats_resources": get_ats_resources(),
    }

    return jsonify(final_response)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)

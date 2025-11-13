from flask import Flask, request, jsonify
from agents.query_agents import query_financial_data
from core.data_loader import load_transactions
from core.llm_classifier import classify_transactions
from core.anomaly_detector import find_anomalies
from core.realtime_api import get_realtime_data
from core.insight_generator import generate_human_insights
from core.summarizer import summarize_results

import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --------------------------
# Root Endpoint
# --------------------------
@app.route('/')
def home():
    return jsonify({"status": "✅ AI Accountant Agent Running", "version": "2.0"})

# --------------------------
# File Upload API
# --------------------------
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    filename = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filename)
    return jsonify({
        "message": "File uploaded successfully ✅",
        "filename": file.filename
    })

# --------------------------
# Transaction Processing API
# --------------------------
@app.route('/process', methods=['POST'])
def process_transactions():
    data = request.get_json()
    filename = data.get('filename')

    if not filename:
        return jsonify({"error": "Filename missing in request"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": f"File '{filename}' not found"}), 404

    # Step 1 — Load CSV
    df = load_transactions(filepath)

    # Step 2 — AI Classification
    classified_df, top_categories, total_spend = classify_transactions(df)

    # Step 3 — Income & Expense Split
    if "type" in classified_df.columns:
        total_income = classified_df[classified_df["type"].str.lower() == "income"]["amount"].sum()
        total_expense = classified_df[classified_df["type"].str.lower() == "expense"]["amount"].sum()
    else:
        total_income = 0
        total_expense = total_spend

    # Step 4 — Profit Calculation
    profit = total_income - total_expense

    # Step 5 — Detect Anomalies
    anomalies = find_anomalies(classified_df)

    # Step 6 — Market Context
    market_context = get_realtime_data()

    # Step 7 — AI-Generated Financial Insights
    insights = generate_human_insights(
        total_income=total_income,
        total_expense=total_expense,
        profit=profit,
        top_categories=top_categories,
        anomalies=anomalies,
        market_context=market_context
    )

    # Step 8 — Summary Report
    summary = summarize_results(total_spend, top_categories, anomalies, insights, market_context)

    # Step 9 — Build JSON Response
    result = {
        "total_income": total_income,
        "total_expense": total_expense,
        "profit": profit,
        "total_spend": total_spend,
        "top_categories": top_categories,
        "anomalies": anomalies,
        "market_context": market_context,
        "human_insights": insights,
        "summary": summary,
        "transactions": classified_df.to_dict(orient="records")
    }

    return jsonify(result)

# --------------------------
# Conversational Query Agent API
# --------------------------
@app.route("/query", methods=["POST"])
def query_data():
    data = request.get_json()
    filename = data.get("filename")
    question = data.get("query")

    if not filename or not question:
        return jsonify({"error": "Filename and query are required"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": f"File '{filename}' not found"}), 404

    # Load the processed or classified CSV
    df = pd.read_csv(filepath)
    result = query_financial_data(df, question)

    return jsonify(result)

# --------------------------
# Run the Flask App
# --------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)

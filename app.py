from flask import Flask, request, jsonify
from core.data_loader import load_transactions
from core.llm_classifier import classify_transactions
from core.anomaly_detector import find_anomalies
from core.realtime_api import get_realtime_data
from core.insight_generator import generate_human_insights
from core.summarizer import summarize_results
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "AI Accountant Agent Running ✅"})

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = os.path.join('uploads', file.filename)
    file.save(filename)
    return jsonify({"message": "File uploaded successfully", "filename": file.filename})

@app.route('/process', methods=['POST'])
def process_transactions():
    data = request.get_json()
    filename = data.get('filename')

    # Step 1 — Read CSV
    df = load_transactions(f'uploads/{filename}')

    # Step 2 — AI Classification (LLM + Rules)
    classified_df, top_categories, total_spend = classify_transactions(df)

    # Step 3 — Anomaly Detection
    anomalies = find_anomalies(classified_df)

    # Step 4 — Get Real-Time INR Data
    market_context = get_realtime_data()

    # Step 5 — Generate Human Insights (AI reasoning)
    insights = generate_human_insights(total_spend, top_categories, anomalies, market_context)

    # Step 6 — Summarize for report
    summary = summarize_results(total_spend, top_categories, anomalies, insights, market_context)

    # Step 7 — Send everything back as JSON
    result = {
        "total_spend": total_spend,
        "top_categories": top_categories,
        "anomalies": anomalies,
        "market_context": market_context,
        "human_insights": insights,
        "summary": summary,
        "transactions": classified_df.to_dict(orient="records")
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)

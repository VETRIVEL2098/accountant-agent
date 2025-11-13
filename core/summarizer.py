def summarize_results(total_spend, top_categories, anomalies, insights, market_context):
    summary = f"📊 Monthly Financial Summary\n"
    summary += f"💰 Total Spend: ₹{int(total_spend)}\n"
    summary += f"📂 Top Categories:\n"
    for k, v in top_categories.items():
        summary += f"   - {k}: ₹{int(v)}\n"

    summary += f"⚠️ Anomalies: {len(anomalies)} found\n"
    summary += f"💹 Market Context: {market_context}\n\n"

    summary += "💡 Insights:\n"

    # --- Handle both string and list/dict response formats safely ---
    if isinstance(insights, str):
        try:
            insights = json.loads(insights)
        except Exception:
            insights = [{"insight": insights, "recommendation": ""}]
    
    if isinstance(insights, dict):
        # If AI returned full structured JSON, extract inner list
        if "insights" in insights:
            insights = insights["insights"]
        else:
            insights = [insights]
    
    # --- Now iterate safely ---
    for i in insights:
        if isinstance(i, dict):
            summary += f" - {i.get('insight', '')}\n"
        else:
            summary += f" - {i}\n"

    if insights and isinstance(insights[-1], dict) and "recommendation" in insights[-1]:
        summary += f"\n📈 Recommendation: {insights[-1]['recommendation']}\n"

    return summary

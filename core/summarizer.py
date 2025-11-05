def summarize_results(total_spend, top_categories, anomalies, insights, market_context):
    summary = f"✅ Total Spend: ₹{int(total_spend)}\n"
    summary += "📊 Top Categories:\n"
    for k, v in top_categories.items():
        summary += f"   - {k}: ₹{int(v)}\n"
    summary += f"⚠️ Anomalies: {len(anomalies)} found\n"
    summary += f"💹 Market: {market_context}\n\n"
    summary += "💡 Insights:\n"
    for i in insights:
        summary += f" - {i.get('insight','')}\n"
    if insights and "recommendation" in insights[-1]:
        summary += f"\n📈 Recommendation: {insights[-1]['recommendation']}\n"
    return summary

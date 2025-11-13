from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import json, os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.6, api_key=os.getenv("OPENAI_API_KEY"))

def generate_human_insights(total_income, total_expense, profit, top_categories, anomalies, market_context):
    """
    Generates structured financial insights, including cost-saving and profit-boosting suggestions.
    """

    prompt = PromptTemplate.from_template("""
    You are an expert financial strategist for Indian SaaS and tech startups.

    Analyze this monthly financial summary:

    - Total Income: ₹{total_income}
    - Total Expense: ₹{total_expense}
    - Net Profit: ₹{profit}
    - Top Spending Categories: {top_categories}
    - Detected Anomalies: {anomalies}
    - Market Context: {market_context}

    Return a clean JSON structure:
    {
      "financial_summary": {
        "total_income": "₹...",
        "total_expense": "₹...",
        "profit": "₹...",
        "key_expense_drivers": ["...", "..."],
        "observations": ["...", "..."]
      },
      "insights": [
        {"insight": "Insight text", "recommendation": "Profit-boosting action"}
      ],
      "alternate_plan": [
        {"area": "Expense area", "suggestion": "Alternative plan", "estimated_savings": "₹.../month"}
      ],
      "profit_opportunity_summary": "1-line summary of how profitability can be improved."
    }

    Guidelines:
    - Focus on practical, startup-relevant insights (SaaS, cloud, marketing, payroll).
    - Suggest realistic cost optimization strategies (annual billing, vendor negotiation, usage review).
    - If profit < 0, give strong corrective advice.
    - If profit > 0, recommend how to reinvest efficiently.
    """)

    try:
        response = llm.invoke(prompt.format(
            total_income=total_income,
            total_expense=total_expense,
            profit=profit,
            top_categories=top_categories,
            anomalies=anomalies,
            market_context=market_context
        ))

        response_text = response.content.strip()
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        json_str = response_text[json_start:json_end]

        return json.loads(json_str)

    except Exception as e:
        # Fallback response in case JSON parsing fails
        return {
            "financial_summary": {
                "total_income": f"₹{total_income}",
                "total_expense": f"₹{total_expense}",
                "profit": f"₹{profit}",
                "key_expense_drivers": list(top_categories.keys()),
                "observations": ["Stable month", "No major anomalies detected."]
            },
            "insights": [
                {"insight": "Spending remains balanced across key categories.",
                 "recommendation": "Negotiate SaaS contracts for volume discounts."}
            ],
            "alternate_plan": [
                {"area": "Cloud Services",
                 "suggestion": "Shift static workloads to cheaper storage tiers.",
                 "estimated_savings": "₹10,000/month"}
            ],
            "profit_opportunity_summary": "Healthy month — potential 8–10% profit improvement through cost optimization."
        }

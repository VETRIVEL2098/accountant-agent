from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import json, os
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.6, api_key=os.getenv("OPENAI_API_KEY"))

def generate_human_insights(total_spend, top_categories, anomalies, market_context):
    prompt = PromptTemplate.from_template("""
    You are a senior financial analyst.
    Total Spend: ₹{total_spend}
    Top Categories: {top_categories}
    Anomalies: {anomalies}
    Market Context: {market_context}

    Write 3 short insights and 1 recommendation as JSON list.
    """)

    try:
        response = llm.predict(prompt.format(
            total_spend=total_spend,
            top_categories=top_categories,
            anomalies=anomalies,
            market_context=market_context
        ))
        return json.loads(response)
    except:
        return [{"insight": "Steady month, no anomalies"}]

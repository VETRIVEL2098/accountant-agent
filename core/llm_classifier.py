import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import os, json
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))

CATEGORY_RULES = {
    "google": "Cloud Services",
    "aws": "Cloud Services",
    "azure": "Cloud Services",
    "zomato": "Meals",
    "swiggy": "Meals",
    "uber": "Travel",
    "ola": "Travel",
    "slack": "SaaS",
    "figma": "SaaS",
    "acme media": "Marketing"
}

def rule_based_category(description):
    desc = description.lower()
    for k, v in CATEGORY_RULES.items():
        if k in desc:
            return v
    return None

def classify_transactions(df):
    # ✅ FIXED: escape curly braces in JSON example
    prompt = PromptTemplate.from_template("""
    You are an AI Accountant.
    Transaction: "{description}", Amount ₹{amount}
    Return JSON: {{"category":"...", "confidence":0-1, "reason":"..."}}
    """)

    categories = []
    for i, row in df.iterrows():
        desc = row["description"]
        cat = rule_based_category(desc)
        if cat:
            categories.append({"category": cat, "confidence": 0.95, "reason": "Rule-based match"})
            continue

        res = llm.invoke(prompt.format(description=desc, amount=row["amount"]))
        try:
            res_json = json.loads(res.split("{",1)[-1].replace("```","").strip())
        except:
            res_json = {"category": "Other", "confidence": 0.5, "reason": "Parsing error"}
        categories.append(res_json)

    df["category"] = [c["category"] for c in categories]
    total_spend = df["amount"].sum()
    top_cats = df.groupby("category")["amount"].sum().nlargest(3).to_dict()
    return df, top_cats, total_spend

from langchain_openai import ChatOpenAI
import os

def query_financial_data(df, query):
    """
    Ultra-fast version — directly interprets the query and computes simple answers
    like total spend, top category, profit, etc.
    """

    # Basic precomputed summaries
    top_category = df.groupby("category")["amount"].sum().idxmax()
    top_spend = df.groupby("category")["amount"].sum().max()
    total_spend = df["amount"].sum()
    num_txns = len(df)

    # Shortcuts for common questions (instant)
    q_lower = query.lower()

    if "highest spending" in q_lower or "top category" in q_lower:
        response = f"The category with the highest spending is '{top_category}' with a total of ₹{int(top_spend):,}."
    elif "total spend" in q_lower or "how much spent" in q_lower:
        response = f"The total spend across all categories is ₹{int(total_spend):,}."
    elif "transactions" in q_lower:
        response = f"There are {num_txns} total transactions recorded."
    elif "categories" in q_lower:
        cats = ", ".join(df['category'].unique())
        response = f"The spending categories include: {cats}."
    else:
        # Fallback: Use the LLM (only for open-ended queries)
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        summary = (
            f"Data summary:\n"
            f"Top category: {top_category} (₹{int(top_spend):,})\n"
            f"Total spend: ₹{int(total_spend):,}\n"
            f"Categories: {', '.join(df['category'].unique())}\n"
        )

        prompt = (
            f"You are a financial data assistant. "
            f"Here’s the spending summary:\n{summary}\n\n"
            f"Answer this question briefly and clearly:\n{query}"
        )

        response = llm.predict(prompt)

    return {
        "query": query,
        "response": response
    }

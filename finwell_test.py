import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="FinWell Tracker", layout="wide")
st.title("💰 FinWell - Simple Finance Tracker")

# Dummy data
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["Date", "Type", "Category", "Amount", "Note"])

df = st.session_state.df

# --- Transaction Form ---
st.subheader("➕ Add Transaction")
with st.form("form"):
    t_type = st.selectbox("Type", ["Income", "Expense"])
    category = st.selectbox("Category", ["Salary", "Food", "Rent", "Shopping", "Others"])
    amount = st.number_input("Amount", min_value=0.0)
    date = st.date_input("Date", value=datetime.date.today())
    note = st.text_input("Note (optional)")
    if st.form_submit_button("Add"):
        new_row = pd.DataFrame([[date, t_type, category, amount, note]],
                               columns=["Date", "Type", "Category", "Amount", "Note"])
        st.session_state.df = pd.concat([df, new_row], ignore_index=True)
        st.success("Transaction added!")

# --- Show Data ---
st.subheader("📋 All Transactions")
st.dataframe(st.session_state.df)

# --- Summary ---
income = df[df["Type"] == "Income"]["Amount"].sum()
expense = df[df["Type"] == "Expense"]["Amount"].sum()
balance = income - expense

st.metric("💵 Total Income", f"₹{income}")
st.metric("💸 Total Expense", f"₹{expense}")
st.metric("📈 Balance", f"₹{balance}")

# --- Smart Savings Suggestion ---
st.subheader("🧠 Smart Savings Suggestion")
if income > 0:
    saving_percent = ((income - expense) / income) * 100
    if saving_percent > 30:
        st.success(f"Great job! You are saving {saving_percent:.2f}% of your income. Keep it up! 🚀")
    elif saving_percent > 20:
        st.info(f"Nice! You are saving {saving_percent:.2f}%. Try to push beyond 30%! 💪")
    elif saving_percent > 10:
        st.warning(f"You are saving {saving_percent:.2f}%. A little more effort can improve this! 📊")
    else:
        st.error(f"You're saving only {saving_percent:.2f}%. Review your expenses to save more. ⚠️")
else:
    st.info("Add some income to see savings analysis.")

# --- Chatbot Assistant ---
st.subheader("🤖 FinBot Assistant (Offline Chat)")

def respond_to_query(query):
    q = query.lower()
    if "balance" in q or "left" in q:
        return f"Your current balance is ₹{balance:.2f}."
    elif "income" in q or "earn" in q:
        return f"Your total income so far is ₹{income:.2f}."
    elif "expense" in q or "spent" in q:
        return f"Your total expenses so far are ₹{expense:.2f}."
    elif "saving" in q:
        return f"You're saving ₹{balance:.2f}, which is {saving_percent:.2f}% of your income."
    elif "advice" in q:
        if saving_percent > 30:
            return "Great saving! You're doing really well 🚀"
        elif saving_percent > 20:
            return "Nice! Try to save more by reducing unnecessary expenses."
        else:
            return "You should control spending and set savings goals to improve."
    else:
        return "Sorry, I can only answer about balance, income, expenses, or savings for now."

user_query = st.text_input("Ask something (e.g., What's my balance?)", key="chat_query")

if user_query:
    st.write("🧠 FinBot says:")
    st.info(respond_to_query(user_query))

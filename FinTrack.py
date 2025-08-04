import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="FinWell", layout="wide")
st.title("💰 FinWell - Personal Finance Tracker")

# Session state for data
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["Date", "Type", "Category", "Amount", "Note"])

df = st.session_state.df

# Sidebar Navigation
page = st.sidebar.selectbox("📚 Navigate", ["Add Entry", "All Data", "Summary", "ChatBot"])

# Page: Add Entry
if page == "Add Entry":
    st.subheader("➕ Add Transaction")
    with st.form("entry_form"):
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

# Page: All Data
elif page == "All Data":
    st.subheader("📋 All Transactions")
    st.dataframe(df)

# Page: Summary
elif page == "Summary":
    st.subheader("📊 Summary & Insights")
    income = df[df["Type"] == "Income"]["Amount"].sum()
    expense = df[df["Type"] == "Expense"]["Amount"].sum()
    balance = income - expense

    col1, col2, col3 = st.columns(3)
    col1.metric("💵 Total Income", f"₹{income}")
    col2.metric("💸 Total Expense", f"₹{expense}")
    col3.metric("📈 Balance", f"₹{balance}")

    if not df.empty:
        st.markdown("#### 🥧 Expense Breakdown (Pie Chart)")
        exp_data = df[df["Type"] == "Expense"].groupby("Category")["Amount"].sum()
        if not exp_data.empty:
            fig1, ax1 = plt.subplots()
            ax1.pie(exp_data, labels=exp_data.index, autopct="%1.1f%%", startangle=90)
            ax1.axis("equal")
            st.pyplot(fig1)

        st.markdown("#### 📊 Income vs Expense (Bar Chart)")
        monthly = df.copy()
        monthly["Month"] = pd.to_datetime(monthly["Date"]).dt.to_period("M")
        summary = monthly.groupby(["Month", "Type"])["Amount"].sum().unstack().fillna(0)
        st.bar_chart(summary)

# Page: ChatBot (Offline)
elif page == "ChatBot":
    st.subheader("🤖 FinBot - Ask Your Finance Assistant")
    user_input = st.text_input("Ask something about your money:")

    if user_input:
        user_input = user_input.lower()
        response = "I didn't understand that."

        if "balance" in user_input:
            balance = df[df["Type"] == "Income"]["Amount"].sum() - df[df["Type"] == "Expense"]["Amount"].sum()
            response = f"Your current balance is ₹{balance:.2f}"
        elif "income" in user_input:
            income = df[df["Type"] == "Income"]["Amount"].sum()
            response = f"Your total income is ₹{income:.2f}"
        elif "expense" in user_input:
            expense = df[df["Type"] == "Expense"]["Amount"].sum()
            response = f"Your total expense is ₹{expense:.2f}"
        elif "save" in user_input:
            income = df[df["Type"] == "Income"]["Amount"].sum()
            expense = df[df["Type"] == "Expense"]["Amount"].sum()
            savings = income - expense
            if savings > 0:
                response = f"Great! You've saved ₹{savings:.2f}. Keep it up!"
            else:
                response = "You're spending more than you earn. Try cutting down unnecessary expenses."

        st.info(response)

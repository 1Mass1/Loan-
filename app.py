import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Loan Calculator", page_icon=":money_with_wings:")

# Function to calculate the loan schedule
def calculate_schedule(principle, tenor, interest_rate):
    interest_rate_monthly = interest_rate / (12 * 100)
    emi = (principle * interest_rate_monthly * (1 + interest_rate_monthly)**tenor) / ((1 + interest_rate_monthly)**tenor - 1)

    remaining_balance = principle
    schedule_data = []
    for month in range(1, tenor+1):
        interest = remaining_balance * interest_rate_monthly
        principle_paid = emi - interest
        remaining_balance -= principle_paid
        schedule_data.append([month, principle_paid, interest, remaining_balance])

    schedule_df = pd.DataFrame(schedule_data, columns=["Month", "Principle Paid", "Interest", "Remaining Balance"])
    total_interest = schedule_df["Interest"].sum()

    return schedule_df, emi, total_interest

st.title("Loan Calculator By 6-digits")

# Sidebar inputs
principle = st.sidebar.number_input("Enter loan amount (AED)", min_value=1, value=100000)
tenor = st.sidebar.slider("Enter loan tenor (months)", min_value=1, max_value=60, value=48)
interest_rate = st.sidebar.number_input("Enter interest (reducing) (%)", min_value=1.0, max_value=20.0, step=0.1, value=6.49)

# Calculation of Loan Schedule and EMI
schedule_df, emi, total_interest = calculate_schedule(principle, tenor, interest_rate)
flat_rate =  total_interest / principle * 100 /tenor*12 # Calculate flat rate

# Loan Summary
st.subheader("Loan Summary")
loan_summary = {
    "Loan Amount": f"AED {principle:,.2f}",
    "Loan Tenor": f"{tenor} months",
    "Interest On Reducing Rate per annum ": f"{interest_rate:.2f}%",
    "Approx. Flat Rate": f"{flat_rate:.2f}%" ,
    "Monthly EMI": f"AED {emi:,.2f}",
    "Total Interest": f"AED {total_interest:,.2f}",
}

loan_summary_df = pd.DataFrame.from_dict(loan_summary, orient="index", columns=[""])
loan_summary_df.index.name = "Loan Details"
loan_summary_df.style.set_properties(**{"text-align": "left", "font-weight": "bold"})\
                .set_table_styles([{"selector": "th", "props": [("text-align", "left")]}])\
                .set_caption("")
st.table(loan_summary_df)

# Loan Schedule
st.subheader("Loan Schedule")
schedule_df["Interest"] = schedule_df["Interest"].apply(lambda x: f"AED {x:,.2f}")
schedule_df["Principle Paid"] = schedule_df["Principle Paid"].apply(lambda x: f"AED {x:,.2f}")
schedule_df["Remaining Balance"] = schedule_df["Remaining Balance"].apply(lambda x: f"AED {x:,.2f}")
st.write(f"Total Interest: AED {total_interest:,.2f}")
st.dataframe(schedule_df)

fig = px.line(schedule_df, x="Month", y=["Principle Paid", "Interest"])
fig.update_traces(mode="lines+markers")
fig.update_layout(title="Loan Schedule",
                  xaxis_title="Month",
                  yaxis_title="AED",
                  yaxis_tickformat=",.2f")
st.plotly_chart(fig)

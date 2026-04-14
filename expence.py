import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
if os.path.exists("expenses.csv"):
    df = pd.read_csv("expenses.csv")
else:
    df = pd.DataFrame(columns=["Amount", "Category", "Date"])
if os.path.exists("budget.csv"):
    budget_df = pd.read_csv("budget.csv")
    monthly_budget = budget_df.loc[0, "Monthly"]
    daily_budget = budget_df.loc[0, "Daily"]
else:
    monthly_budget = float(input("Enter Monthly Budget: "))
    daily_budget = float(input("Enter Daily Budget: "))

    budget_df = pd.DataFrame({
        "Monthly": [monthly_budget],
        "Daily": [daily_budget]
    })
    budget_df.to_csv("budget.csv", index=False)
category_budget = {
    "Food": 2000,
    "Travel": 1500,
    "Other": 1000
}
while True:
    print("\n1. Add Expense")
    print("2. Show Analysis")
    print("3. Exit")
    choice = input("Enter choice: ")
    if choice == '1':
        amount = float(input("Enter amount: "))
        category = input("Enter category (Food/Travel/Other): ")
        date = datetime.now().strftime("%Y-%m-%d")
        new_data = pd.DataFrame([[amount, category, date]],
                                columns=["Amount", "Category", "Date"])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv("expenses.csv", index=False)

        print("Expense added successfully!")
    elif choice == '2':
        if df.empty:
            print("No data available")
            continue
        df['Date'] = pd.to_datetime(df['Date'])
        total_spending = df['Amount'].sum()
        print("\nTotal Spending:", total_spending)
        current_month = datetime.now().month
        monthly_spending = df[df['Date'].dt.month == current_month]['Amount'].sum()
        print("Monthly Spending:", monthly_spending)
        if monthly_spending > monthly_budget:
            print("⚠️ Monthly Budget Exceeded!")
        else:
            print("✅ Within Monthly Budget")
        today = datetime.now().date()
        daily_spending = df[df['Date'].dt.date == today]['Amount'].sum()
        print("Today's Spending:", daily_spending)
        if daily_spending > daily_budget:
            print("⚠️ Daily Budget Exceeded!")
        else:
            print("✅ Within Daily Budget")
        category_sum = df.groupby('Category')['Amount'].sum()
        print("\nCategory-wise Spending:\n", category_sum)
        for cat, value in category_sum.items():
            if cat in category_budget:
                if value > category_budget[cat]:
                    print(f"⚠️ {cat} budget exceeded!")        
        category_sum.plot(kind='bar')
        plt.title("Category-wise Spending")
        plt.show()
        df['Month'] = df['Date'].dt.month
        monthly = df.groupby('Month')['Amount'].sum()
        monthly.plot(kind='line', marker='o')
        plt.title("Monthly Spending Trend")
        plt.show()
    elif choice == '3':
        print("Exiting... Data saved.")
        break

    else:
        print("Invalid choice")

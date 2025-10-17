import pandas as pd
import os
import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt
import json


class FinancialManager:
    def __init__(self, db_name='financial_data.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.load_data()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                username TEXT PRIMARY KEY,
                                password TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS records (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                date TEXT,
                                category TEXT,
                                type TEXT,
                                amount REAL,
                                description TEXT)''')
        self.conn.commit()

    def register_user(self, username, password):
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def validate_user(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        return self.cursor.fetchone() is not None

    def load_data(self):
        self.data = pd.read_sql_query("SELECT * FROM records", self.conn)

    def save_data(self):
        self.data.to_sql('records', self.conn, if_exists='replace', index=False)

    def add_record(self, date, category, record_type, amount, description):
        new_record = {
            'date': date,
            'category': category,
            'type': record_type,
            'amount': amount,
            'description': description
        }
        self.cursor.execute("INSERT INTO records (date, category, type, amount, description) VALUES (?, ?, ?, ?, ?)",
                            (date, category, record_type, amount, description))
        self.conn.commit()
        self.load_data()
        return True

    def view_records(self):
        if self.data.empty:
            return "No records found."
        else:
            return self.data.to_string(index=False)

    def generate_report(self):
        if self.data.empty:
            return "No records to generate report."

        report = self.data.groupby(['type'])['amount'].sum()
        return report

    def budget_allocation(self, category, budget):
        total_expense = self.data[self.data['type'] == 'Expense'].groupby('category')['amount'].sum()
        if category in total_expense:
            used_budget = total_expense[category]
            remaining_budget = budget - used_budget
            return used_budget, remaining_budget
        else:
            return None, None

    def monthly_report(self, month, year):
        filtered_data = self.data[(pd.to_datetime(self.data['date']).dt.month == month) &
                                  (pd.to_datetime(self.data['date']).dt.year == year)]
        if filtered_data.empty:
            return "No records for this month."

        report = filtered_data.groupby(['type'])['amount'].sum()
        return report

    def yearly_report(self, year):
        filtered_data = self.data[pd.to_datetime(self.data['date']).dt.year == year]
        if filtered_data.empty:
            return "No records for this year."

        report = filtered_data.groupby(['type'])['amount'].sum()
        return report


class App:
    def __init__(self, master):
        self.master = master
        self.manager = FinancialManager()
        self.translations = self.load_translations()
        self.language = 'en'  # Default language
        master.title("Financial Manager")
        self.user_logged_in = None

        self.label = tk.Label(master, text=self.translations[self.language]["welcome"])
        self.label.pack()

        self.login_button = tk.Button(master, text=self.translations[self.language]["login"], command=self.login)
        self.login_button.pack()

        self.register_button = tk.Button(master, text=self.translations[self.language]["register"],
                                         command=self.register)
        self.register_button.pack()

    def load_translations(self):
        with open('languages.json', 'r', encoding='utf-8') as f:
            return json.load(f)

    def login(self):
        username = simpledialog.askstring("Login", self.translations[self.language]["username"])
        password = simpledialog.askstring("Login", self.translations[self.language]["password"])
        if self.manager.validate_user(username, password):
            self.user_logged_in = username
            self.open_financial_interface()
        else:
            messagebox.showwarning("Login Failed", self.translations[self.language]["failed"])

    def register(self):
        username = simpledialog.askstring("Register", self.translations[self.language]["username"])
        password = simpledialog.askstring("Register", self.translations[self.language]["password"])
        if self.manager.register_user(username, password):
            messagebox.showinfo("Success", self.translations[self.language]["success"])
        else:
            messagebox.showwarning("Registration Failed", self.translations[self.language]["registration_failed"])

    def open_financial_interface(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.add_button = tk.Button(self.master, text="Add Record", command=self.add_record)
        self.add_button.pack()

        self.view_button = tk.Button(self.master, text="View Records", command=self.show_records)
        self.view_button.pack()

        self.report_button = tk.Button(self.master, text="Generate Report", command=self.show_report)
        self.report_button.pack()

        self.monthly_report_button = tk.Button(self.master, text="Monthly Report", command=self.show_monthly_report)
        self.monthly_report_button.pack()

        self.yearly_report_button = tk.Button(self.master, text="Yearly Report", command=self.show_yearly_report)
        self.yearly_report_button.pack()

        self.budget_button = tk.Button(self.master, text="Budget Allocation", command=self.budget_allocation)
        self.budget_button.pack()

    def add_record(self):
        date = simpledialog.askstring("Input", "Enter date (YYYY-MM-DD):")
        category = simpledialog.askstring("Input", "Enter category:")
        record_type = simpledialog.askstring("Input", "Enter type (Income/Expense):")
        amount = simpledialog.askfloat("Input", "Enter amount:")
        description = simpledialog.askstring("Input", "Enter description:")

        if date and category and record_type and amount is not None and description:
            if self.manager.add_record(date, category, record_type, amount, description):
                messagebox.showinfo("Success", self.translations[self.language]["success_record"])
            else:
                messagebox.showwarning("Input Error", self.translations[self.language]["input_error"])

    def show_records(self):
        records = self.manager.view_records()
        if records == "No records found.":
            messagebox.showwarning("No Records", records)
        else:
            messagebox.showinfo(self.translations[self.language]["records"], records)

    def show_report(self):
        report = self.manager.generate_report()
        if report == "No records to generate report.":
            messagebox.showwarning("No Records", report)
        else:
            report.plot(kind='bar', title=self.translations[self.language]["report"])
            plt.xlabel('Type')
            plt.ylabel('Amount')
            plt.show()

    def show_monthly_report(self):
        month = simpledialog.askinteger("Input", "Enter month (1-12):")
        year = simpledialog.askinteger("Input", "Enter year (YYYY):")
        report = self.manager.monthly_report(month, year)
        if report == "No records for this month.":
            messagebox.showwarning("No Records", report)
        else:
            report.plot(kind='bar', title=f"Monthly Report for {month}/{year}")
            plt.xlabel('Type')
            plt.ylabel('Amount')
            plt.show()

    def show_yearly_report(self):
        year = simpledialog.askinteger("Input", "Enter year (YYYY):")
        report = self.manager.yearly_report(year)
        if report == "No records for this year.":
            messagebox.showwarning("No Records", report)
        else:
            report.plot(kind='bar', title=f"Yearly Report for {year}")
            plt.xlabel('Type')
            plt.ylabel('Amount')
            plt.show()

    def budget_allocation(self):
        category = simpledialog.askstring("Input", "Enter category for budget:")
        budget = simpledialog.askfloat("Input", "Enter total budget:")
        if category and budget is not None:
            used_budget, remaining_budget = self.manager.budget_allocation(category, budget)
            if used_budget is not None:
                messagebox.showinfo("Budget Allocation",
                                    f"Used Budget: {used_budget}\nRemaining Budget: {remaining_budget}")
            else:
                messagebox.showwarning("Budget Allocation", f"No expenses recorded for {category}.")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

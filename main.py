import tkinter as tk
from tkinter import messagebox, simpledialog  # Add simpledialog here
import json
from datetime import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("400x600")

        # Variables
        self.expense_list = []
        self.categories = ["Groceries", "Utilities", "Entertainment", "Other"]

        # Styling
        self.root.tk_setPalette(background='#f0f0f0')  # Set background color

        # GUI Elements
        self.label_product = tk.Label(root, text="Enter Product:", background='#f0f0f0', font=('Helvetica', 12))
        self.entry_product = tk.Entry(root, font=('Helvetica', 12))
        self.label_amount = tk.Label(root, text="Enter Amount:", background='#f0f0f0', font=('Helvetica', 12))
        self.entry_amount = tk.Entry(root, font=('Helvetica', 12))
        self.label_category = tk.Label(root, text="Select Category:", background='#f0f0f0', font=('Helvetica', 12))
        self.category_var = tk.StringVar()
        self.category_var.set(self.categories[0])
        self.category_menu = tk.OptionMenu(root, self.category_var, *self.categories)
        self.button_add = tk.Button(root, text="Add Expense", command=self.add_expense, font=('Helvetica', 12), bg='#4CAF50', fg='white')
        self.listbox_expenses = tk.Listbox(root, font=('Helvetica', 12), selectbackground='#4CAF50')
        self.label_total = tk.Label(root, text="Total Expense: $0.00", background='#f0f0f0', font=('Helvetica', 12))
        self.button_clear = tk.Button(root, text="Clear All", command=self.clear_expenses, font=('Helvetica', 12), bg='#FF5733', fg='white')
        self.button_save = tk.Button(root, text="Save Expenses", command=self.save_expenses, font=('Helvetica', 12), bg='#3498db', fg='white')
        self.button_add_category = tk.Button(root, text="Add Category", command=self.add_category, font=('Helvetica', 12), bg='#3498db', fg='white')
        self.button_delete_category = tk.Button(root, text="Delete Category", command=self.delete_category, font=('Helvetica', 12), bg='#FF5733', fg='white')

        # Grid Layout
        self.label_product.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        self.entry_product.grid(row=0, column=1, padx=10, pady=5)
        self.label_amount.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        self.entry_amount.grid(row=1, column=1, padx=10, pady=5)
        self.label_category.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        self.category_menu.grid(row=2, column=1, padx=10, pady=5)
        self.button_add.grid(row=3, column=0, columnspan=2, pady=10)
        self.listbox_expenses.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
        self.label_total.grid(row=5, column=0, columnspan=2, pady=5)
        self.button_clear.grid(row=6, column=0, columnspan=2, pady=10)
        self.button_save.grid(row=7, column=0, columnspan=2, pady=10)
        self.button_add_category.grid(row=8, column=0, columnspan=2, pady=10)
        self.button_delete_category.grid(row=9, column=0, columnspan=2, pady=10)

    def add_expense(self):
        product = self.entry_product.get()
        amount = self.entry_amount.get()
        category = self.category_var.get()

        if product and amount:
            try:
                amount = float(amount)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.expense_list.append({"product": product, "amount": amount, "category": category, "timestamp": timestamp})
                self.update_expense_list()
                self.update_total()
                self.entry_product.delete(0, tk.END)
                self.entry_amount.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount.")
        else:
            messagebox.showwarning("Warning", "Please enter product and amount.")

    def update_expense_list(self):
        self.listbox_expenses.delete(0, tk.END)
        for expense_data in self.expense_list:
            self.listbox_expenses.insert(tk.END, f"{expense_data['product']} - {expense_data['category']}: ${expense_data['amount']:.2f}")

    def update_total(self):
        total = sum(expense_data['amount'] for expense_data in self.expense_list)
        self.label_total.config(text=f"Total Expense: ${total:.2f}")

    def clear_expenses(self):
        confirmed = messagebox.askyesno("Confirmation", "Are you sure you want to clear all expenses?")
        if confirmed:
            self.expense_list = []
            self.update_expense_list()
            self.update_total()

    def save_expenses(self):
        try:
            with open("expenses.json", "w") as file:
                json.dump(self.expense_list, file, indent=2)
            messagebox.showinfo("Success", "Expenses saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving expenses: {str(e)}")

    def add_category(self):
        category = tk.simpledialog.askstring("Add Category", "Enter the new category:")
        if category:
            self.categories.append(category)
            self.category_menu["menu"].delete(0, tk.END)
            for cat in self.categories:
                self.category_menu["menu"].add_command(label=cat, command=tk._setit(self.category_var, cat))
            messagebox.showinfo("Success", f"Category '{category}' added successfully.")

    def delete_category(self):
        selected_category = self.category_var.get()
        if selected_category in self.categories:
            confirmed = messagebox.askyesno("Confirmation", f"Are you sure you want to delete the category '{selected_category}'?")
            if confirmed:
                self.categories.remove(selected_category)
                self.category_var.set(self.categories[0] if self.categories else "")
                self.category_menu["menu"].delete(0, tk.END)
                for category in self.categories:
                    self.category_menu["menu"].add_command(label=category, command=tk._setit(self.category_var, category))
                messagebox.showinfo("Success", f"Category '{selected_category}' deleted successfully.")
        else:
            messagebox.showwarning("Warning", "Please select a category to delete.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()

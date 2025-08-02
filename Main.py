import tkinter as tk
from tkinter import ttk, messagebox
import os

class Account:
    def __init__(self, acc_no=0, name="", acc_type="", deposit=0, pin=""):
        self.accNo = acc_no
        self.name = name
        self.type = acc_type
        self.deposit = deposit
        self.pin = pin  # Store PIN

class BankManagementSystem:
    def __init__(self, master):
        self.master = master
        self.master.title('Banking Management System')
        self.master.geometry('800x600')
        self.accounts = []
        self.current_frame = None
        self.load_accounts()  # Load accounts when the application starts
        self.create_widgets()

    def load_accounts(self):
        filepath = r'C:\Users\aksha\OneDrive\Desktop\banking\data.txt'
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                for line in f:
                    if line.strip():
                        try:
                            acc_no, name, acc_type, deposit, pin = line.strip().split(',')
                            account = Account(int(acc_no), name, acc_type, int(deposit), pin)
                            self.accounts.append(account)
                        except ValueError:
                            print(f"Skipping invalid line: {line.strip()}")

    def create_widgets(self):
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack()
        title_label = tk.Label(self.main_frame, text='Banking Management System', font=('Arial', 24, 'bold'))
        title_label.pack(pady=20)
        links = ['New Account', 'Deposit', 'Withdrawal', 'Balance Enquiry', 
                 'Update Details', 'Close Account', 'Account List', 'Exit']
        for item in links:
            tk.Button(self.main_frame, text=item, command=lambda txt=item: self.show_frame(txt)).pack(pady=4)

    def show_frame(self, option):
        if self.current_frame:
            self.current_frame.pack_forget()
        if option == 'main':
            self.current_frame = self.main_frame
        elif option == 'New Account':
            self.current_frame = self.create_new_account_frame()
        elif option == 'Deposit':
            self.current_frame = self.create_deposit_frame()
        elif option == 'Withdrawal':
            self.current_frame = self.create_withdrawal_frame()
        elif option == 'Balance Enquiry':
            self.current_frame = self.create_balance_enquiry_frame()
        elif option == 'Update Details':
            self.current_frame = self.create_update_details_frame()
        elif option == 'Close Account':
            self.current_frame = self.create_close_account_frame()
        elif option == 'Account List':
            self.current_frame = self.create_account_list_frame()
        elif option == 'Exit':
            self.master.destroy()
            return  # Prevent further execution after destroying
        self.current_frame.pack()

    def create_new_account_frame(self):
        frame = tk.Frame(self.master)
        tk.Label(frame, text='Account No.').grid(row=0, column=0)
        tk.Label(frame, text='Name').grid(row=1, column=0)
        tk.Label(frame, text='Account Type').grid(row=2, column=0)
        tk.Label(frame, text='Initial Deposit').grid(row=3, column=0)
        tk.Label(frame, text='PIN').grid(row=4, column=0)

        acc_no = tk.StringVar()
        name = tk.StringVar()
        acc_type = tk.StringVar(value="Savings")
        deposit = tk.StringVar()
        pin = tk.StringVar()  # PIN input field
        tk.Entry(frame, textvariable=acc_no).grid(row=0, column=1)
        tk.Entry(frame, textvariable=name).grid(row=1, column=1)
        tk.Entry(frame, textvariable=acc_type).grid(row=2, column=1)
        tk.Entry(frame, textvariable=deposit).grid(row=3, column=1)
        tk.Entry(frame, textvariable=pin, show="*").grid(row=4, column=1)  # Mask the PIN input
        tk.Button(frame, text='Create Account', command=lambda: self.create_account(acc_no.get(), name.get(), acc_type.get(), deposit.get(), pin.get())).grid(row=5, column=1)
        tk.Button(frame, text='Back', command=lambda: self.show_frame('main')).grid(row=5, column=0)
        return frame

    def create_account(self, acc_no_str, name, acc_type, deposit_str, pin):
        try:
            acc_no = int(acc_no_str)
            deposit = int(deposit_str)
            if any(account.accNo == acc_no for account in self.accounts):
                messagebox.showerror('Error', 'Account number already exists.')
                return
            account = Account(acc_no, name, acc_type, deposit, pin)
            self.accounts.append(account)
            self.save_accounts()
            messagebox.showinfo('Success', 'Account created successfully!')
        except ValueError:
            messagebox.showerror('Error', 'Please enter valid numbers for Account No. and Deposit.')

    def create_account_list_frame(self):
        frame = tk.Frame(self.master)
        columns = ('#', 'Account No', 'Name', 'Type', 'Deposit')
        table = ttk.Treeview(frame, columns=columns, show='headings')
        for col in columns:
            table.heading(col, text=col)
        for idx, account in enumerate(self.accounts, start=1):
            table.insert("", "end", values=(idx, account.accNo, account.name, account.type, account.deposit))
        table.pack()
        tk.Button(frame, text='Back', command=lambda: self.show_frame('main')).pack()
        return frame

    def create_deposit_frame(self):
        frame = tk.Frame(self.master)
        tk.Label(frame, text='Account No.').grid(row=0, column=0)
        tk.Label(frame, text='Deposit Amount').grid(row=1, column=0)
        acc_no = tk.StringVar()
        amount = tk.StringVar()
        tk.Entry(frame, textvariable=acc_no).grid(row=0, column=1)
        tk.Entry(frame, textvariable=amount).grid(row=1, column=1)
        tk.Button(frame, text='Deposit', command=lambda: self.deposit(acc_no.get(), amount.get())).grid(row=2, column=1)
        tk.Button(frame, text='Back', command=lambda: self.show_frame('main')).grid(row=2, column=0)
        return frame

    def deposit(self, acc_no_str, amount_str):
        try:
            acc_no = int(acc_no_str)
            amount = int(amount_str)
            account = next((acc for acc in self.accounts if acc.accNo == acc_no), None)
            if account:
                account.deposit += amount
                self.save_accounts()
                messagebox.showinfo('Success', f'Deposited {amount} to account {acc_no}.')
            else:
                messagebox.showerror('Error', 'Account not found.')
        except ValueError:
            messagebox.showerror('Error', 'Please enter valid numbers.')

    def create_withdrawal_frame(self):
        frame = tk.Frame(self.master)
        tk.Label(frame, text='Account No.').grid(row=0, column=0)
        tk.Label(frame, text='Withdrawal Amount').grid(row=1, column=0)
        tk.Label(frame, text='PIN').grid(row=2, column=0)
        acc_no = tk.StringVar()
        amount = tk.StringVar()
        pin = tk.StringVar()
        tk.Entry(frame, textvariable=acc_no).grid(row=0, column=1)
        tk.Entry(frame, textvariable=amount).grid(row=1, column=1)
        tk.Entry(frame, textvariable=pin, show="*").grid(row=2, column=1)  # Mask the PIN input
        tk.Button(frame, text='Withdraw', command=lambda: self.withdraw(acc_no.get(), amount.get(), pin.get())).grid(row=3, column=1)
        tk.Button(frame, text='Back', command=lambda: self.show_frame('main')).grid(row=3, column=0)
        return frame

    def withdraw(self, acc_no_str, amount_str, pin):
        try:
            acc_no = int(acc_no_str)
            amount = int(amount_str)
            account = next((acc for acc in self.accounts if acc.accNo == acc_no), None)
            if account:
                if account.pin == pin:  # Verify the PIN
                    if account.deposit >= amount:
                        account.deposit -= amount
                        self.save_accounts()
                        messagebox.showinfo('Success', f'Withdrew {amount} from account {acc_no}.')
                    else:
                        messagebox.showerror('Error', 'Insufficient funds.')
                else:
                    messagebox.showerror('Error', 'Incorrect PIN.')
            else:
                messagebox.showerror('Error', 'Account not found.')
        except ValueError:
            messagebox.showerror('Error', 'Please enter valid numbers.')

    def create_balance_enquiry_frame(self):
        frame = tk.Frame(self.master)
        tk.Label(frame, text='Account No.').grid(row=0, column=0)
        acc_no = tk.StringVar()
        tk.Entry(frame, textvariable=acc_no).grid(row=0, column=1)
        tk.Button(frame, text='Check Balance', command=lambda: self.check_balance(acc_no.get())).grid(row=1, column=1)
        tk.Button(frame, text='Back', command=lambda: self.show_frame('main')).grid(row=1, column=0)
        return frame

    def check_balance(self, acc_no_str):
        try:
            acc_no = int(acc_no_str)
            account = next((acc for acc in self.accounts if acc.accNo == acc_no), None)
            if account:
                messagebox.showinfo('Balance', f'Balance for account {acc_no}: {account.deposit}')
            else:
                messagebox.showerror('Error', 'Account not found.')
        except ValueError:
            messagebox.showerror('Error', 'Please enter a valid account number.')

    def create_update_details_frame(self):
        frame = tk.Frame(self.master)
        tk.Label(frame, text='Account No.').grid(row=0, column=0)
        acc_no = tk.StringVar()
        tk.Entry(frame, textvariable=acc_no).grid(row=0, column=1)
        tk.Button(frame, text='Fetch Details', command=lambda: self.fetch_account_details(acc_no.get())).grid(row=1, column=1)
        tk.Button(frame, text='Back', command=lambda: self.show_frame('main')).grid(row=1, column=0)
        return frame

    def fetch_account_details(self, acc_no_str):
        try:
            acc_no = int(acc_no_str)
            account = next((acc for acc in self.accounts if acc.accNo == acc_no), None)
            if account:
                self.update_account_details(account)
            else:
                messagebox.showerror('Error', 'Account not found.')
        except ValueError:
            messagebox.showerror('Error', 'Please enter a valid account number.')

    def update_account_details(self, account):
        frame = tk.Frame(self.master)
        tk.Label(frame, text='Name').grid(row=0, column=0)
        tk.Label(frame, text='Account Type').grid(row=1, column=0)
        tk.Label(frame, text='Deposit').grid(row=2, column=0)

        name_var = tk.StringVar(value=account.name)
        acc_type_var = tk.StringVar(value=account.type)
        deposit_var = tk.StringVar(value=str(account.deposit))

        tk.Entry(frame, textvariable=name_var).grid(row=0, column=1)
        tk.Entry(frame, textvariable=acc_type_var).grid(row=1, column=1)
        tk.Entry(frame, textvariable=deposit_var).grid(row=2, column=1)
        tk.Button(frame, text='Update', command=lambda: self.update_account(account, name_var.get(), acc_type_var.get(), deposit_var.get())).grid(row=3, column=1)
        tk.Button(frame, text='Back', command=lambda: self.show_frame('main')).grid(row=3, column=0)
        frame.pack()

    def update_account(self, account, name, acc_type, deposit_str):
        try:
            deposit = int(deposit_str)
            account.name = name
            account.type = acc_type
            account.deposit = deposit
            self.save_accounts()
            messagebox.showinfo('Success', 'Account details updated successfully!')
            self.show_frame('main')
        except ValueError:
            messagebox.showerror('Error', 'Please enter a valid deposit amount.')

    def create_close_account_frame(self):
        frame = tk.Frame(self.master)
        tk.Label(frame, text='Account No.').grid(row=0, column=0)
        acc_no = tk.StringVar()
        tk.Entry(frame, textvariable=acc_no).grid(row=0, column=1)
        tk.Button(frame, text='Close Account', command=lambda: self.close_account(acc_no.get())).grid(row=1, column=1)
        tk.Button(frame, text='Back', command=lambda: self.show_frame('main')).grid(row=1, column=0)
        return frame

    def close_account(self, acc_no_str):
        try:
            acc_no = int(acc_no_str)
            account = next((acc for acc in self.accounts if acc.accNo == acc_no), None)
            if account:
                self.accounts.remove(account)
                self.save_accounts()
                messagebox.showinfo('Success', 'Account closed successfully!')
            else:
                messagebox.showerror('Error', 'Account not found.')
        except ValueError:
            messagebox.showerror('Error', 'Please enter a valid account number.')

    def save_accounts(self):
        filepath = r'C:\Users\aksha\OneDrive\Desktop\banking\data.txt'
        with open(filepath, 'w') as f:
            for account in self.accounts:
                f.write(f"{account.accNo},{account.name},{account.type},{account.deposit},{account.pin}\n")

if __name__ == '__main__':
    root = tk.Tk()
    app = BankManagementSystem(root)
    root.mainloop()

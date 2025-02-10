import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import locale

# Configurar el locale para el formateo de números
locale.setlocale(locale.LC_ALL, '')

def format_currency(value):
    return locale.format_string("%d", value, grouping=True).replace(",", ".")

def calculate_amortization():
    try:
        principal = round(float(entry_principal.get()))
        monthly_payment = round(float(entry_monthly_payment.get()))
        annual_interest_rate = float(entry_interest_rate.get()) / 100
        monthly_interest_rate = annual_interest_rate / 12
        additional_payment = round(float(entry_additional_payment.get()))

        payments = []
        month = 0

        while principal > 0:
            month += 1
            interest_payment = round(principal * monthly_interest_rate)
            principal_payment = monthly_payment - interest_payment + additional_payment
            principal -= principal_payment

            if principal < 0:
                principal_payment += principal
                principal = 0

            payments.append((month, monthly_payment + additional_payment, interest_payment, principal_payment, principal))

        for row in tree.get_children():
            tree.delete(row)

        for payment in payments:
            formatted_payment = (
                payment[0],
                format_currency(payment[1]),
                format_currency(payment[2]),
                format_currency(payment[3]),
                format_currency(payment[4])
            )
            tree.insert("", "end", values=formatted_payment)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")

app = tk.Tk()
app.title("Loan Amortization Calculator")

frame = tk.Frame(app)
frame.pack(pady=10)

tk.Label(frame, text="Valor Total o Actual:").grid(row=0, column=0, padx=5, pady=5)
entry_principal = tk.Entry(frame)
entry_principal.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Cuota Mensual:").grid(row=1, column=0, padx=5, pady=5)
entry_monthly_payment = tk.Entry(frame)
entry_monthly_payment.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Interés EA (%):").grid(row=2, column=0, padx=5, pady=5)
entry_interest_rate = tk.Entry(frame)
entry_interest_rate.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame, text="Pago Adicional a Capital:").grid(row=3, column=0, padx=5, pady=5)
entry_additional_payment = tk.Entry(frame)
entry_additional_payment.grid(row=3, column=1, padx=5, pady=5)

calculate_button = tk.Button(frame, text="Calcular", command=calculate_amortization)
calculate_button.grid(row=4, column=0, columnspan=2, pady=10)

columns = ("Mes", "Pago Total", "Intereses", "Pago a Capital", "Saldo Restante")
tree = ttk.Treeview(app, columns=columns, show="headings")
tree.heading("Mes", text="Mes")
tree.heading("Pago Total", text="Pago Total")
tree.heading("Intereses", text="Intereses")
tree.heading("Pago a Capital", text="Pago a Capital")
tree.heading("Saldo Restante", text="Saldo Restante")
tree.pack(pady=10)

app.mainloop()
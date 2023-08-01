import tkinter as tk
import tkinter.messagebox as messagebox

# create empty lists to use to store items later on
expenses = []
previous = []
removed_expenses = []


def add(amount, obj):
    additem = {'amount': amount, "object": obj}
    expenses.append(additem)


def listExpenses():
    expense_list.delete(1.0, tk.END)  # Clear the existing list
    # ensures each list item had a number infront of it
    for idx, item in enumerate(expenses, start=1):
        expense_list.insert(
            tk.END, f"#{idx} - {item['object']} - {item['amount']}\n")  # adds new item to end of expense list in the order of idx, object,amount then creates a new line


def remove():
    try:
        # convert selected expense into int and subtract 1 to get the proper index of the item to remove
        expense = int(selected_expense.get()) - 1
        # checks if index is negative or exists in list
        if 0 <= expense < len(expenses):
            # takes out the removed expense from the expenses list and stores it
            removed = expenses.pop(expense)
            # keeps track of expenses that have been removed by adding the removed item to the removed list
            removed_expenses.append(removed)
            listExpenses()
        else:
            show_message(
                "Invalid input. Please enter a valid number from the list.")
    except ValueError:
        show_message(
            "Invalid input. Please enter the number that the expense corresponds to on the list.")


def budget_remaining(max_budget):
    # adds up the amount of all items in list
    total_cost = sum(int(item['amount']) for item in expenses)
    # subtracts total cost of list items from user input of max budget
    money_left = max_budget - total_cost
    show_message(
        f"The amount you have left to spend for the month is: {money_left}", yes_no=False)


def new_month():
    global expenses, previous  # modifying the lists made outside of the function
    confirmation = show_message(
        "Are you sure you want to reset your expenses for the month?")
    if confirmation is not None:  # if the user clicked yes or no and didnt just close the message box
        if confirmation:
            previous.append(expenses)
            expenses = []
            listExpenses()
            show_message("Expenses for the month have been reset.")
        else:
            show_message("Reset canceled. Your expenses remain unchanged.")


def show_message(message, yes_no=True):
    msg_window = tk.Toplevel(root)  # create new top-level window
    msg_window.title("Message")
    label = tk.Label(msg_window, text=message)
    label.pack(padx=20, pady=10)

    if yes_no:
        result = None

        def on_yes():
            nonlocal result
            result = True
            msg_window.destroy()  # closes message box

        def on_no():
            nonlocal result
            result = False
            msg_window.destroy()  # closes message box

        yes_button = tk.Button(msg_window, text="Yes",
                               command=on_yes)  # create button
        yes_button.pack(side=tk.LEFT, padx=10, pady=5)

        no_button = tk.Button(msg_window, text="No",
                              command=on_no)  # create button
        no_button.pack(side=tk.RIGHT, padx=10, pady=5)

        msg_window.wait_window()  # waits untill window is closed before continuing code
        return result
    else:
        def on_okay():
            msg_window.destroy()

        okay_button = tk.Button(msg_window, text="Ok", command=on_okay)
        okay_button.pack(pady=10)

        msg_window.wait_window()


def add_expense():
    obj = object_entry.get()  # assigns user entry to variable
    amount = amount_entry.get()  # assigns user entry to variable
    # convert string of amount to float before using it in add function
    add(float(amount), obj)
    listExpenses()
    # clears the users input from the box provided in the UI
    amount_entry.delete(0, tk.END)
    # clears the users input from the box provided in the UI
    object_entry.delete(0, tk.END)


def view_previous_months():
    if not previous:
        show_message("No previous months' expenses found.")
        return

    prev_window = tk.Toplevel(root)  # create new window
    prev_window.title("Previous Months' Expenses")

    # iterates through list previous
    for month_idx, month_expenses in enumerate(previous, start=1):
        # group expense lables for each month
        prev_frame = tk.Frame(prev_window)
        prev_frame.pack(padx=10, pady=10, anchor=tk.W)

        # created for each months previous expenses
        prev_label = tk.Label(prev_frame, text=f"Month {month_idx} expenses:")
        prev_label.pack()

        # iterates through expense of the current previous month
        for idx, item in enumerate(month_expenses, start=1):
            prev_expense = tk.Label(
                prev_frame, text=f"#{idx} - {item['object']} - {item['amount']}")
            prev_expense.pack()

        prev_total_cost = sum(int(item['amount']) for item in month_expenses)
        prev_total_label = tk.Label(
            prev_frame, text=f"Total amount spent: {prev_total_cost}")
        prev_total_label.pack()


def on_exit():
    root.destroy()


gold_color = "#C0A080"  # Example color: RGB(192, 160, 128)

root = tk.Tk()
root.title("Expense Tracker")
root.configure(bg="light blue")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)
# frame.configure(bg="light blue")

amount_label = tk.Label(frame, text="Amount:")
amount_label.grid(row=0, column=0, padx=5, pady=5)
amount_entry = tk.Entry(frame)
amount_entry.grid(row=0, column=1, padx=5, pady=5)

object_label = tk.Label(frame, text="Object:")
object_label.grid(row=1, column=0, padx=5, pady=5)
object_entry = tk.Entry(frame)
object_entry.grid(row=1, column=1, padx=5, pady=5)

add_button = tk.Button(frame, text="Add Expense",
                       command=add_expense, bd=0, relief="flat")
add_button.grid(row=2, column=0, columnspan=2, pady=10)

# list_button = tk.Button(frame, text="List Expenses", command=listExpenses)
# list_button.grid(row=3, column=0, columnspan=2, pady=5)

# associated with user input of the index of the expense they want to remove
selected_expense = tk.StringVar()
remove_label = tk.Label(frame, text="Enter the number to remove:")
remove_label.grid(row=4, column=0, columnspan=2, pady=5)
remove_entry = tk.Entry(frame, textvariable=selected_expense)
remove_entry.grid(row=5, column=0, padx=5, pady=5)
remove_button = tk.Button(frame, text="Remove Expense",
                          command=remove, bd=0, relief="flat")
remove_button.grid(row=5, column=1, padx=5, pady=5)

budget_label = tk.Label(frame, text="Enter your monthly budget:")
budget_label.grid(row=6, column=0, columnspan=2, pady=5)
budget_entry = tk.Entry(frame)
budget_entry.grid(row=7, column=0, columnspan=2, pady=5)
budget_button = tk.Button(frame, text="Check Budget", command=lambda: budget_remaining(
    float(budget_entry.get())), bd=0, relief="flat")
budget_button.grid(row=8, column=0, columnspan=2, pady=5)

reset_button = tk.Button(frame, text="Reset for the Month",
                         command=new_month, bd=0, relief="flat")
reset_button.grid(row=9, column=0, columnspan=2, pady=5)

expense_list = tk.Text(frame, width=40, height=10)
expense_list.grid(row=0, column=2, rowspan=10, padx=10, pady=5)

exit_button = tk.Button(
    frame, text="Exit", command=on_exit, bd=0, relief="flat")
exit_button.grid(row=10, column=0, columnspan=3, pady=10)

view_prev_button = tk.Button(
    frame, text="View Previous Months", command=view_previous_months, bd=0, relief="flat")
view_prev_button.grid(row=8, column=2, padx=10, pady=20)

root.mainloop()

from server.db.models import users, groups, user_groups,expenses, expense_participant, payments, debts

User = users.User
Group = groups.Group
UserGroup = user_groups.user_groups

Expense = expenses.Expense
ExpenseParticipant = expense_participant.ExpenseParticipant
Payment = payments.Payment
Debt = debts.Debt

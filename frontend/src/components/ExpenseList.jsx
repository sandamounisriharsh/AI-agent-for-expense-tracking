import { useEffect, useState } from "react";
import { Trash2 } from "lucide-react";

import { getExpenses, deleteExpense } from "../services/api";

function ExpenseList({ refreshKey, onExpenseChanged }) {
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [deletingId, setDeletingId] = useState(null);

  useEffect(() => {
    async function loadExpenses() {
      setLoading(true);
      setError("");

      try {
        const data = await getExpenses();

        setExpenses(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    }

    loadExpenses();
  }, [refreshKey]);

  const handleDelete = async (expenseId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this expense?",
    );

    if (!confirmed) {
      return;
    }

    setDeletingId(expenseId);
    setError("");

    try {
      await deleteExpense(expenseId);

      setExpenses((previous) =>
        previous.filter((expense) => expense.id !== expenseId),
      );
      if (onExpenseChanged) {
        onExpenseChanged();
      }
    } catch (error) {
      setError(error.message);
    } finally {
      setDeletingId(null);
    }
  };

  return (
    <div className="expense-list">
      <div className="list-heading">
        <div>
          <span>RECENT EXPENSES</span>
          <small>YOUR TRANSACTIONS</small>
        </div>

        <span className="list-count">{expenses.length}</span>
      </div>

      {loading && <div className="list-message">Loading expenses...</div>}

      {error && <div className="list-error">{error}</div>}

      {!loading && !error && expenses.length === 0 && (
        <div className="list-message">No expenses yet.</div>
      )}

      {!loading &&
        expenses.map((expense) => (
          <div className="expense-item" key={expense.id}>
            <div className="expense-info">
              <strong>{expense.category}</strong>

              <span>{expense.description}</span>
            </div>

            <div className="expense-actions">
              <div className="expense-amount">
                ₹{Number(expense.amount).toLocaleString("en-IN")}
              </div>

              <button
                className="delete-expense"
                onClick={() => handleDelete(expense.id)}
                disabled={deletingId === expense.id}
                title="Delete expense"
              >
                <Trash2 size={14} />
              </button>
            </div>
          </div>
        ))}
    </div>
  );
}

export default ExpenseList;

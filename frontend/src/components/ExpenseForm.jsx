import { useState } from "react";
import { createExpense } from "../services/api";


function ExpenseForm({ onExpenseAdded }) {

  const [amount, setAmount] = useState("");
  const [category, setCategory] = useState("");
  const [description, setDescription] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");


  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");
    setSuccess("");

    if (Number(amount) <= 0) {
      setError("Amount must be greater than zero.");
      return;
    }

    if (!category.trim()) {
      setError("Please enter a category.");
      return;
    }

    if (!description.trim()) {
      setError("Please enter a description.");
      return;
    }

    setLoading(true);

    try {

      await createExpense(
        amount,
        category.trim(),
        description.trim()
      );

      setAmount("");
      setCategory("");
      setDescription("");

      setSuccess("Expense added successfully.");

      if (onExpenseAdded) {
        onExpenseAdded();
      }

    } catch (error) {

      setError(error.message);

    } finally {

      setLoading(false);

    }
  };


  return (
    <div className="expense-form">

      <div className="form-heading">
        <span>ADD EXPENSE</span>
        <small>NEW TRANSACTION</small>
      </div>


      <form onSubmit={handleSubmit}>

        <div className="form-field">

          <label>AMOUNT</label>

          <div className="amount-input">

            <span>₹</span>

            <input
              type="number"
              min="0"
              step="0.01"
              placeholder="0.00"
              value={amount}
              onChange={(event) =>
                setAmount(event.target.value)
              }
              required
            />

          </div>

        </div>


        <div className="form-field">

          <label>CATEGORY</label>

          <input
            type="text"
            placeholder="Food, Travel, Rent..."
            value={category}
            onChange={(event) =>
              setCategory(event.target.value)
            }
            required
          />

        </div>


        <div className="form-field">

          <label>DESCRIPTION</label>

          <input
            type="text"
            placeholder="What did you spend on?"
            value={description}
            onChange={(event) =>
              setDescription(event.target.value)
            }
            required
          />

        </div>


        {error && (
          <div className="form-error">
            {error}
          </div>
        )}


        {success && (
          <div className="form-success">
            {success}
          </div>
        )}


        <button
          type="submit"
          disabled={loading}
        >
          {loading
            ? "ADDING..."
            : "ADD EXPENSE"}
        </button>

      </form>

    </div>
  );
}


export default ExpenseForm;
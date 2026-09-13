const EXPENSE_API_URL =
  import.meta.env.VITE_EXPENSE_API_URL || "http://localhost:8000";

const AI_API_URL =
  import.meta.env.VITE_AI_API_URL || "http://localhost:8001";


export async function signup(email, password) {
  const response = await fetch(
    `${EXPENSE_API_URL}/auth/signup`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email,
        password,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Signup failed"
    );
  }

  return data;
}


export async function login(email, password) {
  const formData = new URLSearchParams();

  formData.append("username", email);
  formData.append("password", password);

  const response = await fetch(
    `${EXPENSE_API_URL}/auth/login`,
    {
      method: "POST",
      headers: {
        "Content-Type":
          "application/x-www-form-urlencoded",
      },
      body: formData,
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Login failed"
    );
  }

  return data;
}


export async function sendMessage(
  message,
  conversationId = null
) {
  const token = localStorage.getItem("access_token");

  const response = await fetch(
    `${AI_API_URL}/chat`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },

      body: JSON.stringify({
        message,
        conversation_id: conversationId,
      }),
    }
  );

  if (!response.ok) {
    throw new Error(
      "Failed to communicate with AI agent"
    );
  }

  return await response.json();
}

export async function getExpenses(category = "") {
  const token = localStorage.getItem("access_token");

  const url = category
    ? `${EXPENSE_API_URL}/expenses?category=${encodeURIComponent(category)}`
    : `${EXPENSE_API_URL}/expenses`;

  const response = await fetch(url, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to fetch expenses"
    );
  }

  return data;
}


export async function getTotal(category = "") {
  const token = localStorage.getItem("access_token");

  const url = category
    ? `${EXPENSE_API_URL}/expenses/total?category=${encodeURIComponent(category)}`
    : `${EXPENSE_API_URL}/expenses/total`;

  const response = await fetch(url, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to fetch total"
    );
  }

  return data;
}

export async function getDashboardStats() {
  const token = localStorage.getItem("access_token");

  const response = await fetch(
    `${EXPENSE_API_URL}/expenses/dashboard`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to fetch dashboard data"
    );
  }

  return data;
}

export async function createExpense(
  amount,
  category,
  description
) {
  const token = localStorage.getItem("access_token");

  const response = await fetch(
    `${EXPENSE_API_URL}/expenses`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        amount: Number(amount),
        category,
        description,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to add expense"
    );
  }

  return data;
}

export async function deleteExpense(expenseId) {
  const token = localStorage.getItem("access_token");

  const response = await fetch(
    `${EXPENSE_API_URL}/expenses/${expenseId}`,
    {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to delete expense"
    );
  }

  return data;
}
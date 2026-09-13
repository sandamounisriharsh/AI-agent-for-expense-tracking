import sqlite3


def create_expense(
    db: sqlite3.Connection,
    user_id: int,
    amount: float,
    category: str,
    description: str
):
    cursor = db.execute(
        """
        INSERT INTO expenses
        (user_id, amount, category, description)
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            amount,
            category,
            description
        )
    )

    db.commit()

    expense_id = cursor.lastrowid

    return db.execute(
        """
        SELECT id, amount, category, description, created_at
        FROM expenses
        WHERE id = ? AND user_id = ?
        """,
        (expense_id, user_id)
    ).fetchone()


def get_user_expenses(
    db: sqlite3.Connection,
    user_id: int,
    category: str | None = None
):
    if category:
        rows = db.execute(
            """
            SELECT id, amount, category, description, created_at
            FROM expenses
            WHERE user_id = ?
              AND category = ?
            ORDER BY created_at DESC
            """,
            (user_id, category)
        ).fetchall()
    else:
        rows = db.execute(
            """
            SELECT id, amount, category, description, created_at
            FROM expenses
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (user_id,)
        ).fetchall()

    return rows


def get_user_total(
    db: sqlite3.Connection,
    user_id: int,
    category: str | None = None
):
    if category:
        row = db.execute(
            """
            SELECT COALESCE(SUM(amount), 0) AS total
            FROM expenses
            WHERE user_id = ?
              AND category = ?
            """,
            (user_id, category)
        ).fetchone()
    else:
        row = db.execute(
            """
            SELECT COALESCE(SUM(amount), 0) AS total
            FROM expenses
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()

    return row["total"]


def delete_expense(
    db: sqlite3.Connection,
    user_id: int,
    expense_id: int
):
    cursor = db.execute(
        """
        DELETE FROM expenses
        WHERE id = ?
          AND user_id = ?
        """,
        (expense_id, user_id)
    )

    db.commit()

    return cursor.rowcount > 0

def get_dashboard_stats(
    db: sqlite3.Connection,
    user_id: int
):
    total = db.execute(
        """
        SELECT COALESCE(SUM(amount), 0) AS total
        FROM expenses
        WHERE user_id = ?
        """,
        (user_id,)
    ).fetchone()["total"]

    count = db.execute(
        """
        SELECT COUNT(*) AS count
        FROM expenses
        WHERE user_id = ?
        """,
        (user_id,)
    ).fetchone()["count"]

    top_category = db.execute(
        """
        SELECT category, SUM(amount) AS total
        FROM expenses
        WHERE user_id = ?
        GROUP BY category
        ORDER BY total DESC
        LIMIT 1
        """,
        (user_id,)
    ).fetchone()

    recent_expenses = db.execute(
        """
        SELECT id, amount, category, description, created_at
        FROM expenses
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT 5
        """,
        (user_id,)
    ).fetchall()

    return {
        "total": total,
        "count": count,
        "top_category": (
            top_category["category"]
            if top_category
            else None
        ),
        "recent_expenses": [
            dict(expense)
            for expense in recent_expenses
        ]
    }

def update_expense(
    db,
    user_id: int,
    expense_id: int,
    amount: float | None = None,
    category: str | None = None,
    description: str | None = None,
):
    existing = db.execute(
        """
        SELECT *
        FROM expenses
        WHERE id = ? AND user_id = ?
        """,
        (expense_id, user_id),
    ).fetchone()

    if not existing:
        return None

    new_amount = (
        amount
        if amount is not None
        else existing["amount"]
    )

    new_category = (
        category
        if category is not None
        else existing["category"]
    )

    new_description = (
        description
        if description is not None
        else existing["description"]
    )

    db.execute(
        """
        UPDATE expenses
        SET amount = ?,
            category = ?,
            description = ?
        WHERE id = ?
          AND user_id = ?
        """,
        (
            new_amount,
            new_category,
            new_description,
            expense_id,
            user_id,
        ),
    )

    db.commit()

    return db.execute(
        """
        SELECT *
        FROM expenses
        WHERE id = ?
          AND user_id = ?
        """,
        (expense_id, user_id),
    ).fetchone()
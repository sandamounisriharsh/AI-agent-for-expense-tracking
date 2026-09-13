import {
  TrendingUp,
  Receipt,
  Wallet,
  ArrowUpRight,
} from "lucide-react";

function AnalyticsDashboard({ dashboard, loading }) {
  if (loading) {
    return (
      <section className="analytics-section">
        <div className="analytics-loading">
          Loading your financial overview...
        </div>
      </section>
    );
  }

  if (!dashboard) return null;

  const total = Number(dashboard.total || 0);
  const count = Number(dashboard.count || 0);
  const average = count > 0 ? total / count : 0;

  const topCategory = dashboard.top_category || "None";

  /*
   * Supports category data returned by the dashboard API.
   */
  const categoryTotals =
    dashboard.category_totals ||
    dashboard.categories ||
    {};

  const categories = Object.entries(categoryTotals)
    .map(([category, amount]) => ({
      category,
      amount: Number(amount),
    }))
    .filter((item) => item.amount > 0)
    .sort((a, b) => b.amount - a.amount);

  const maxCategoryAmount =
    categories.length > 0
      ? categories[0].amount
      : 0;

  return (
    <section className="analytics-section">

      {/* Header */}
      <div className="analytics-header">
        <div>
          <span>FINANCIAL OVERVIEW</span>
          <small>YOUR SPENDING AT A GLANCE</small>
        </div>

        <div className="analytics-live">
          <span></span>
          LIVE DATA
        </div>
      </div>


      {/* Stats */}
      <div className="analytics-grid">

        <div className="analytics-card analytics-main">
          <div className="analytics-card-top">
            <span>TOTAL SPENDING</span>
            <Wallet size={17} />
          </div>

          <div className="analytics-value">
            ₹{total.toLocaleString("en-IN")}
          </div>

          <div className="analytics-description">
            Total recorded expenses
          </div>
        </div>


        <div className="analytics-card">
          <div className="analytics-card-top">
            <span>TRANSACTIONS</span>
            <Receipt size={17} />
          </div>

          <div className="analytics-value">
            {count}
          </div>

          <div className="analytics-description">
            Expenses recorded
          </div>
        </div>


        <div className="analytics-card">
          <div className="analytics-card-top">
            <span>AVERAGE</span>
            <TrendingUp size={17} />
          </div>

          <div className="analytics-value">
            ₹
            {average.toLocaleString("en-IN", {
              maximumFractionDigits: 0,
            })}
          </div>

          <div className="analytics-description">
            Average per transaction
          </div>
        </div>


        <div className="analytics-card">
          <div className="analytics-card-top">
            <span>TOP CATEGORY</span>
            <ArrowUpRight size={17} />
          </div>

          <div className="analytics-category">
            {topCategory}
          </div>

          <div className="analytics-description">
            Highest spending category
          </div>
        </div>

      </div>


      {/* Category breakdown */}
      {categories.length > 0 && (
        <div className="category-breakdown">

          <div className="category-heading">
            <div>
              <span>SPENDING BREAKDOWN</span>
              <small>WHERE YOUR MONEY GOES</small>
            </div>
          </div>


          <div className="category-list">

            {categories.map(({ category, amount }) => {

              const percentage =
                total > 0
                  ? (amount / total) * 100
                  : 0;

              const width =
                maxCategoryAmount > 0
                  ? (amount / maxCategoryAmount) * 100
                  : 0;

              return (
                <div
                  className="category-row"
                  key={category}
                >

                  <div className="category-info">

                    <span className="category-name">
                      {category}
                    </span>

                    <span className="category-amount">
                      ₹{amount.toLocaleString("en-IN")}
                    </span>

                  </div>


                  <div className="category-bar-container">
                    <div
                      className="category-bar"
                      style={{
                        width: `${width}%`,
                      }}
                    />
                  </div>


                  <div className="category-percentage">
                    {percentage.toFixed(0)}%
                  </div>

                </div>
              );
            })}

          </div>

        </div>
      )}


      {/* AI-style insight */}
      {categories.length > 0 && (
        <div className="analytics-insight">

          <div className="insight-symbol">
            ✦
          </div>

          <div>
            <span>SPENDING INSIGHT</span>

            <p>
              {topCategory} is currently your
              largest spending category at{" "}
              <strong>
                ₹
                {categories[0].amount.toLocaleString(
                  "en-IN"
                )}
              </strong>
              .
            </p>
          </div>

        </div>
      )}

    </section>
  );
}

export default AnalyticsDashboard;
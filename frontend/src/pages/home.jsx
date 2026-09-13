import { useEffect, useState } from "react";

import AnalyticsDashboard from "../components/AnalyticsDashboard";
import Navbar from "../components/Navbar";
import Hero from "../components/Hero";
import Features from "../components/Features";
import AgentSection from "../components/AgentSection";
import ExpenseForm from "../components/ExpenseForm";
import ExpenseList from "../components/ExpenseList";

import { getDashboardStats } from "../services/api";

function Home({ onLogout }) {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);

  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const data = await getDashboardStats();

        setDashboard(data);
      } catch (error) {
        console.error("Dashboard error:", error);
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, [refreshKey]);

  const refreshDashboard = () => {
    setRefreshKey((previous) => previous + 1);
  };

  return (
    <div className="site">
      <Navbar onLogout={onLogout} />

      <Hero dashboard={dashboard} loading={loading} />

      <AnalyticsDashboard dashboard={dashboard} loading={loading} />

      <section className="dashboard-section">
        <ExpenseForm onExpenseAdded={refreshDashboard} />

        <ExpenseList
          refreshKey={refreshKey}
          onExpenseChanged={refreshDashboard}
        />
      </section>

      <Features />

      <AgentSection />
    </div>
  );
}

export default Home;

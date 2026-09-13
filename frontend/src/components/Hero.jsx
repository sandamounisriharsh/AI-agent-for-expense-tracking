import { ArrowUpRight } from "lucide-react";

import Wallet from "./Wallet";
import FloatingCard from "./FloatingCard";


function Hero({ dashboard, loading }) {

  const total = dashboard?.total || 0;

  const topCategory =
    dashboard?.top_category;


  return (
    <section className="hero">

      <div className="availability">
        <span className="status-dot"></span>

        YOUR PERSONAL EXPENSE AGENT
      </div>


      <h1>
        TRACK YOUR
        <br />
        EXPENSES
        <br />

        <span>
          INTELLIGENTLY.
        </span>
      </h1>


      <p className="hero-description">
        LESS MANUAL WORK.
        <br />
        MORE FINANCIAL CLARITY.
        <br />
        POWERED BY AI.
      </p>


      <a
        href="#agent"
        className="launch-button"
      >
        LAUNCH YOUR AGENT

        <ArrowUpRight size={14} />
      </a>


      <Wallet />


      <FloatingCard
        className="card-left"
        label="TOTAL EXPENSES"
        value={
          loading
            ? "..."
            : `₹${total.toLocaleString("en-IN")}`
        }
        description="All recorded expenses"
        status
      />


      <FloatingCard
        className="card-right"
        label="TOP CATEGORY"
        value={
          loading
            ? "..."
            : topCategory
              ? topCategory.toUpperCase()
              : "NONE"
        }
        description="Highest spending category"
      />


      <FloatingCard
        className="card-bottom-left"
        label="EXPENSES LOGGED"
        value={
          loading
            ? "..."
            : dashboard?.count || 0
        }
        description="Total records"
      />


      <FloatingCard
        className="card-bottom-right"
        label="AI AGENT"
        value="ACTIVE"
        description="Tracking your expenses"
        status
      />


      <div className="hero-bottom">

        <span>
          01 / EXPENSE INTELLIGENCE
        </span>


        <div className="scroll-indicator">

          <span></span>

          SCROLL TO EXPLORE

        </div>


        <span>
          POWERED BY AI
        </span>

      </div>

    </section>
  );
}


export default Hero;
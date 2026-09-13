import FeatureCard from "./FeatureCard";

function Features() {
  return (
    <section id="features" className="section">

      <div className="section-tag">
        01 — WHAT YOUR AGENT CAN DO
      </div>

      <h2>
        YOUR MONEY.
        <br />
        <span>UNDERSTOOD.</span>
      </h2>

      <p className="section-description">
        Your AI expense agent turns everyday spending
        into meaningful insights, without complicated
        spreadsheets.
      </p>

      <div className="feature-grid">

        <FeatureCard
          number="01"
          title="TRACK EVERYTHING"
          text="Record your expenses naturally and keep your financial activity organized."
        />

        <FeatureCard
          number="02"
          title="ASK YOUR DATA"
          text="Ask questions about your spending and get intelligent answers from your AI agent."
        />

        <FeatureCard
          number="03"
          title="FIND PATTERNS"
          text="Understand where your money goes and discover your biggest spending categories."
        />

      </div>
    </section>
  );
}

export default Features;
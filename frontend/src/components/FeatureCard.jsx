import { ArrowUpRight, Sparkles } from "lucide-react";

function FeatureCard({ number, title, text }) {
  return (
    <div className="feature-card">
      <span className="feature-number">
        {number}
      </span>

      <div className="feature-icon">
        <Sparkles size={18} />
      </div>

      <h3>{title}</h3>

      <p>{text}</p>

      <ArrowUpRight
        className="feature-arrow"
        size={18}
      />
    </div>
  );
}

export default FeatureCard;
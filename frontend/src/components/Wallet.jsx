import { Sparkles } from "lucide-react";

function Wallet() {
  return (
    <div className="wallet-area">
      <div className="wallet-glow"></div>

      <div className="wallet-platform"></div>

      <div className="wallet">
        <div className="wallet-card card-one"></div>
        <div className="wallet-card card-two"></div>

        <div className="wallet-body">
          <div className="wallet-logo">₹</div>

          <div className="wallet-strap">
            <span></span>
          </div>
        </div>
      </div>

      <div className="wallet-caption">
        <Sparkles size={10} />
        SMART EXPENSE TRACKING
      </div>
    </div>
  );
}

export default Wallet;
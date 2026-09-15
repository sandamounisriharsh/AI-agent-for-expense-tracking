import { Menu, X } from "lucide-react";
import { useState } from "react";

function Navbar({ onLogout }) {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <>
      <nav className="navbar">
        <div className="brand">
          <span className="brand-mark">₹</span>
          <span>
            Spendwise<span className="brand-light">AI</span>
          </span>
        </div>

        <div className="nav-center">
          <a href="#features">FEATURES</a>
          <a href="#how">HOW IT WORKS</a>
          <a href="#agent">AI AGENT</a>
        </div>

        <div className="nav-actions">

          <button
            className="logout-button"
            onClick={onLogout}
          >
            LOGOUT
          </button>

          <button className="try-button">
            TRY IT FREE
          </button>

          <button
            className="menu-button"
            onClick={() => setMenuOpen(!menuOpen)}
          >
            {menuOpen ? <X size={15} /> : <Menu size={15} />}
            MENU
          </button>

        </div>
      </nav>

      {menuOpen && (
        <div className="mobile-menu">
          <a href="#features">FEATURES</a>
          <a href="#how">HOW IT WORKS</a>
          <a href="#agent">AI AGENT</a>
        </div>
      )}
    </>
  );
}

export default Navbar;
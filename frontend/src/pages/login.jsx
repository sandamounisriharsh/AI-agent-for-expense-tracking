import { useState } from "react";
import { login } from "../services/api";


function Login({ onLogin, onSwitchToSignup }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");


  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      const data = await login(
        email,
        password
      );

      localStorage.setItem(
        "access_token",
        data.access_token
      );

      localStorage.setItem(
        "user_id",
        data.user_id
      );

      onLogin();

    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="auth-page">

      <div className="auth-card">

        <div className="auth-logo">
          ₹
        </div>

        <h1>WELCOME BACK.</h1>

        <p>
          Sign in to your Expense AI account.
        </p>


        <form onSubmit={handleSubmit}>

          <label>
            EMAIL
          </label>

          <input
            type="email"
            placeholder="you@example.com"
            value={email}
            onChange={(event) =>
              setEmail(event.target.value)
            }
            required
          />


          <label>
            PASSWORD
          </label>

          <input
            type="password"
            placeholder="••••••••"
            value={password}
            onChange={(event) =>
              setPassword(event.target.value)
            }
            required
          />


          {error && (
            <div className="auth-error">
              {error}
            </div>
          )}


          <button
            type="submit"
            disabled={loading}
          >
            {loading
              ? "SIGNING IN..."
              : "SIGN IN"}
          </button>

        </form>


        <div className="auth-switch">

          Don't have an account?

          <button
            type="button"
            onClick={onSwitchToSignup}
          >
            CREATE ACCOUNT
          </button>

        </div>

      </div>

    </div>
  );
}


export default Login;
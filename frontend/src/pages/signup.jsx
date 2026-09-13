import { useState } from "react";
import { signup } from "../services/api";


function Signup({ onLogin, onSwitchToLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] =
    useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");


  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);

    try {

      const data = await signup(
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

        <h1>START TRACKING.</h1>

        <p>
          Create your Expense AI account.
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


          <label>
            CONFIRM PASSWORD
          </label>

          <input
            type="password"
            placeholder="••••••••"
            value={confirmPassword}
            onChange={(event) =>
              setConfirmPassword(event.target.value)
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
              ? "CREATING..."
              : "CREATE ACCOUNT"}
          </button>

        </form>


        <div className="auth-switch">

          Already have an account?

          <button
            type="button"
            onClick={onSwitchToLogin}
          >
            SIGN IN
          </button>

        </div>

      </div>

    </div>
  );
}


export default Signup;
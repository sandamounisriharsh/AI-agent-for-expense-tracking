import { useState } from "react";

import Home from "./pages/home";
import Login from "./pages/login";
import Signup from "./pages/signup";


function App() {

  const [authenticated, setAuthenticated] =
    useState(
      Boolean(
        localStorage.getItem("access_token")
      )
    );

  const [showSignup, setShowSignup] =
    useState(false);


  const handleLogin = () => {
    setAuthenticated(true);
  };


  const handleLogout = () => {
    localStorage.removeItem(
      "access_token"
    );

    localStorage.removeItem(
      "user_id"
    );

    setAuthenticated(false);
  };


  if (!authenticated) {

    if (showSignup) {
      return (
        <Signup
          onLogin={handleLogin}
          onSwitchToLogin={() =>
            setShowSignup(false)
          }
        />
      );
    }

    return (
      <Login
        onLogin={handleLogin}
        onSwitchToSignup={() =>
          setShowSignup(true)
        }
      />
    );
  }


  return (
    <Home
      onLogout={handleLogout}
    />
  );
}


export default App;
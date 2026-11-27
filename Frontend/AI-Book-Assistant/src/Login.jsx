import React from "react";
import { useState } from "react";
import { useNavigate } from "react-router";

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState();
  const [password, setPassword] = useState();
  async function handleLogin(e) {
    e.preventDefault();

    try {
      const res = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify({ email: email, password: password }),
      });

      if (!res.ok) throw new Error(`Server Error ${res.status}`);

      const data = await res.json();
      localStorage.setItem("token", data.access_token);

      const profile = await getUserProfile();
      console.log("loggedIn: ", profile);

      navigate("/", { replace: true });
    } catch (error) {
      console.error(error);
    }
  }

  async function getUserProfile() {
    const token = localStorage.getItem("token");
    try {
      const res = await fetch("http://localhost:8000/auth/me", {
        method: "GET",
        headers: {
          "Content-type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });

      if (!res.ok) throw new Error(`Auth Failed ${res.status}`);
      const profile = await res.json();

      return profile;
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <div>
      <form onSubmit={handleLogin} className="border w-50" id="login">
        <label htmlFor="email">Email:</label>
        <input
          id="email"
          type="email"
          onChange={(e) => setEmail(e.target.value)}
          placeholder="John@gmail.com"
        ></input>

        <label htmlFor="password"> Password:</label>
        <input
          id="password"
          type="password"
          onChange={(e) => setPassword(e.target.value)}
          placeholder="123456789@"
        ></input>
      </form>
      <button form="login" className="border border-red-500 " type="submit">
        {" "}
        Login
      </button>
    </div>
  );
}

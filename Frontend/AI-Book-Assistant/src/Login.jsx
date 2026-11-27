import React from "react";
import useLogin from "../hooks/useLogin.js"

export default function Login() {
  const { setEmail, setPassword, handleLogin} = useLogin()
  
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

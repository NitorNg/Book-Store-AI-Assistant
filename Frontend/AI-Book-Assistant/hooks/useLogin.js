import {useState} from 'react'
import { useNavigate } from "react-router";

export default function useLogin() {   
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
    
      return {
        email,
        setEmail,
        password,
        setPassword,
        handleLogin,

      }
}

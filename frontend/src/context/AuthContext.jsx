// import { createContext, useState, useEffect } from "react";
// import { useNavigate } from "react-router-dom";

// export const AuthContext = createContext();

// export const AuthProvider = ({ children }) => {
//   const [token, setToken] = useState(localStorage.getItem("token") || null);
//   const [role, setRole] = useState(localStorage.getItem("role") || null);
//   const navigate = useNavigate();

//   const login = (token, role) => {
//     localStorage.setItem("token", token);
//     localStorage.setItem("role", role);
//     setToken(token);
//     setRole(role);

//     if (role === "admin") {
//       navigate("/admin");
//     } else {
//       navigate("/"); // Redirect to voter dashboard (to be created)
//     }
//   };

//   const logout = () => {
//     localStorage.removeItem("token");
//     localStorage.removeItem("role");
//     setToken(null);
//     setRole(null);
//     navigate("/login");
//   };

//   useEffect(() => {
//     if (!token) navigate("/login");
//   }, [token, navigate]);

//   return (
//     <AuthContext.Provider value={{ token, role, login, logout }}>
//       {children}
//     </AuthContext.Provider>
//   );
// };

import { createContext, useContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem("token") || null);
  const [role, setRole] = useState(localStorage.getItem("role") || null);
  const navigate = useNavigate();

  const login = (token, role) => {
    localStorage.setItem("token", token);
    localStorage.setItem("role", role);
    setToken(token);
    setRole(role);
    console.log('inside context');
    console.log(token, role);
    
    

    if (role === "admin") {
      navigate("/admin");
    } else {
      navigate("/");
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    setToken(null);
    setRole(null);
    navigate("/login");
  };

  useEffect(() => {
    if (!token) navigate("/login");
  }, [token, navigate]);

  return (
    <AuthContext.Provider value={{ token, role, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// ✅ Create and Export `useAuth` Hook
export const useAuth = () => {
  return useContext(AuthContext);
};

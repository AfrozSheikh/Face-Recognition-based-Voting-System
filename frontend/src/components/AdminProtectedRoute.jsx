import { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const AdminProtectedRoute = ({ children }) => {
  const { token, role } = useContext(AuthContext);

  if (!token || role !== "admin") {
    return <Navigate to="/login" />;
  }

  return children;
};

export default AdminProtectedRoute;

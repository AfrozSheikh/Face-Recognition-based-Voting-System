import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  if (!user) {
    navigate("/login"); // Redirect to login if not authenticated
    return null;
  }

  return (
    <div>
      <h2>Welcome, {user.role === "admin" ? "Admin" : "Voter"}!</h2>
      
      {user.role === "admin" ? (
        <div>
          <h3>Admin Panel</h3>
          <ul>
            <li><button onClick={() => navigate("/admin/create-election")}>Create Election</button></li>
            <li><button onClick={() => navigate("/admin/approve-voters")}>Approve Voters</button></li>
            <li><button onClick={() => navigate("/admin/results")}>View Results</button></li>
          </ul>
        </div>
      ) : (
        <div>
          <h3>Voter Panel</h3>
          <ul>
            <li><button onClick={() => navigate("/voter/elections")}>View Elections</button></li>
            <li><button onClick={() => navigate("/voter/vote")}>Cast Vote</button></li>
          </ul>
        </div>
      )}

      <button onClick={() => { logout(); navigate("/login"); }}>Logout</button>
    </div>
  );
};

export default Dashboard;

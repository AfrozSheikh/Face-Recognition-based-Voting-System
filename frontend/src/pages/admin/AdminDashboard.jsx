import { Link } from "react-router-dom";

const AdminDashboard = () => {
  return (
    <div>
      <h2>Admin Dashboard</h2>
      <ul>
        <li><Link to="/admin/approve-voters">Approve Voters</Link></li>
        <li><Link to="/admin/create-election">Create Election</Link></li>
        <li><Link to="/admin/add-candidate">Add Candidate</Link></li>
        <li><Link to="/admin/declare-results">Declare Results</Link></li>
      </ul>
    </div>
  );
};

export default AdminDashboard;


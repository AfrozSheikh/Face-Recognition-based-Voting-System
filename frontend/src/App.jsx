import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Signup from "./pages/Signup";
import Login from "./pages/Login";
import AdminDashboard from "./pages/admin/AdminDashboard";
import ApproveVoters from "./pages/admin/ApproveVoters";
import CreateElection from "./pages/admin/CreateElection";
import AddCandidate from "./pages/admin/AddCandidate";
import DeclareResults from "./pages/admin/DeclareResults";
import { AuthProvider } from "./context/AuthContext";
import AdminProtectedRoute from "./components/AdminProtectedRoute";
import ViewElections from "./pages/ViewElections";
import Result from "./pages/Result";
import Dashboard from "./pages/Dashboard";
import Vote from "./pages/Vote";

function App() {
  return (
  
      
        <Routes>
          {/* Authentication Routes */}
          <Route path="/" element={<Signup />} />
          <Route path="/vote" element={<Vote />} />
          <Route path="/view-elections" element={<ViewElections />} />
          <Route path="/login" element={<Login />} />
          <Route path="/elections" element={<ViewElections />} />
          <Route path="/dashboard" element={<Dashboard />} />

          <Route path="/results" element={<Result />} />
          {/* Admin Routes - Protected */}
          <Route path="/admin" element={<AdminDashboard />} />
          <Route path="/admin/approve-voters" element={<ApproveVoters />} />
          <Route path="/admin/create-election" element={<CreateElection />} />
          <Route path="/admin/add-candidate" element={<AddCandidate />} />
          <Route path="/admin/declare-results" element={<DeclareResults />} />
        </Routes>
     
  );
}

export default App;

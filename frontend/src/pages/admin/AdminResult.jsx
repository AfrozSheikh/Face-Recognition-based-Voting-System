import { useState, useEffect } from "react";
import { useAuth } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";

const AdminResult = () => {
  const { token,role } = useAuth();
  const [elections, setElections] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) {
      navigate("/login");
      return;
    }
    console.log(role);
    
    fetch("http://127.0.0.1:5000/admin/view_results", {
      // headers: { Authorization: `Bearer ${token}` }, // Fix: Ensure "Bearer" prefix
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("API Response:", data);

        // Fix: Correctly set state based on response structure
        setElections(data.results || []);
        setLoading(false);
      })
      .catch((err) => console.error("Fetch Error:", err));
  }, [role, navigate]);

  return (
    <div>
      <h2>Election Results</h2>
      {loading ? (
        <p>Loading results...</p>
      ) : elections.length === 0 ? (
        <p>No results available</p>
      ) : (
        elections.map((election) => (
          <div key={election._id} style={{ border: "1px solid black", padding: "10px", margin: "10px" }}>
            <h3>{election.name}</h3>

            {/* Fix: Display winner correctly */}
            <p>
              Winner:{" "}
              {election.winner
                ? `${election.winner.name} (${election.winner.party}) - ${election.winner.votes} votes`
                : "Not Declared Yet"}
            </p>

            <h4>Candidates:</h4>
            <ul>
              {election.candidates.map((candidate) => (
                <li key={candidate.name}>
                  {candidate.name} ({candidate.party}) - {candidate.votes} votes
                </li>
              ))}
            </ul>
          </div>
        ))
      )}
    </div>
  );
};

export default AdminResult;

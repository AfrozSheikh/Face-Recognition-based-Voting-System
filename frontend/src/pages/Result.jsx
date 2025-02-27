import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const Result = () => {
  const { token } = useAuth();
  const [elections, setElections] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) {
      navigate("/login");
      return;
    }

    fetch("http://127.0.0.1:5000/voter/view_results", {
      headers: { Authorization: token },
    })
      .then((res) => res.json())
      .then((data) => {
        setElections(data.elections || []);
        setLoading(false);
      })
      .catch((err) => console.error(err));
  }, [token, navigate]);

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
            <p>Winner: {election.winner || "Not Declared Yet"}</p>
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

export default Result;

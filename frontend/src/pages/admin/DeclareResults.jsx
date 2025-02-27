import { useState, useEffect, useContext } from "react";
import { AuthContext } from "../../context/AuthContext";

const DeclareResults = () => {
  const { token } = useContext(AuthContext);
  const [elections, setElections] = useState([]);
  const [selectedElection, setSelectedElection] = useState("");
  const [message, setMessage] = useState("");

  // Fetch all ongoing elections
  useEffect(() => {
    const fetchElections = async () => {
      try {
        const response = await fetch("http://localhost:5000/admin/elections", {
          headers: { Authorization: `Bearer ${token}` },
        });
        const data = await response.json();
        if (response.ok) {
          setElections(data.elections);
        } else {
          setMessage(data.message || "Failed to fetch elections.");
        }
      } catch (error) {
        setMessage("Error: Could not fetch elections.");
      }
    };

    fetchElections();
  }, [token]);

  const handleDeclareResults = async () => {
    if (!selectedElection) {
      setMessage("Please select an election.");
      return;
    }

    try {
      const response = await fetch("http://localhost:5000/admin/declare_results", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ election_id: selectedElection }),
      });

      const data = await response.json();
      if (response.ok) {
        setMessage("Results declared successfully!");
      } else {
        setMessage(data.message || "Failed to declare results.");
      }
    } catch (error) {
      setMessage("Error: Could not declare results.");
    }
  };

  return (
    <div>
      <h2>Declare Election Results</h2>
      {message && <p>{message}</p>}
      <select value={selectedElection} onChange={(e) => setSelectedElection(e.target.value)} required>
        <option value="">Select Election</option>
        {elections.map((election) => (
          <option key={election._id} value={election._id}>
            {election.title} - {election.district}
          </option>
        ))}
      </select>
      <button onClick={handleDeclareResults}>Declare Results</button>
    </div>
  );
};

export default DeclareResults;

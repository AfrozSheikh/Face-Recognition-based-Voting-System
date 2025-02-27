import { useState, useEffect, useContext } from "react";
import { AuthContext } from "../../context/AuthContext";

const AddCandidate = () => {
  const { token } = useContext(AuthContext);
  const [elections, setElections] = useState([]);
  const [selectedElection, setSelectedElection] = useState("");
  const [candidateName, setCandidateName] = useState("");
  const [party, setParty] = useState("");
  const [message, setMessage] = useState("");

  // Fetch all elections
  useEffect(() => {
    const fetchElections = async () => {
      try {
        const response = await fetch("http://localhost:5000/admin/elections", {
          headers: { Authorization: `Bearer ${token}` },
        });
        const data = await response.json();
      console.log(data);
      
        
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

  const handleSubmit = async (e) => {
    e.preventDefault();

    const candidateData = { election_id: selectedElection, name: candidateName, party };

    try {
      const response = await fetch("http://localhost:5000/admin/add_candidate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(candidateData),
      });

      const data = await response.json();
      if (response.ok) {
        setMessage("Candidate added successfully!");
        setCandidateName("");
        setParty("");
      } else {
        setMessage(data.message || "Failed to add candidate.");
      }
    } catch (error) {
      setMessage("Error: Could not add candidate.");
    }
  };

  return (
    <div>
      <h2>Add Candidate</h2>
      {message && <p>{message}</p>}
      <form onSubmit={handleSubmit}>
        <select value={selectedElection} onChange={(e) => setSelectedElection(e.target.value)} required>
          <option value="">Select Election</option>
          {elections.map((election) => (
            <option key={election._id} value={election._id}>
              {election.title} - {election.district}
            </option>
          ))}
        </select>
        <input type="text" placeholder="Candidate Name" value={candidateName} onChange={(e) => setCandidateName(e.target.value)} required />
        <input type="text" placeholder="Party" value={party} onChange={(e) => setParty(e.target.value)} required />
        <button type="submit">Add Candidate</button>
      </form>
    </div>
  );
};

export default AddCandidate;

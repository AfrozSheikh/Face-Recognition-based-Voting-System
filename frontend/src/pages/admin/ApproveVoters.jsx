import { useEffect, useState, useContext } from "react";
import { AuthContext } from "../../context/AuthContext";

const ApproveVoters = () => {
  const { token } = useContext(AuthContext);
  const [voters, setVoters] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/admin/pending_voters", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => setVoters(data.pendingVoters))
      .catch((err) => console.error(err));
  }, [token]);

  const handleApproval = (voterId, status) => {
    fetch("http://localhost:5000/admin/approve_voter", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ voterId, status }),
    })
      .then((res) => res.json())
      .then(() => {
        setVoters(voters.filter((voter) => voter._id !== voterId));
      })
      .catch((err) => console.error(err));
  };

  return (
    <div>
      <h2>Approve Voters</h2>
      {voters.length === 0 ? (
        <p>No pending voter requests.</p>
      ) : (
        <ul>
          {voters.map((voter) => (
            <li key={voter._id}>
              {voter.name} - {voter.email} - 
              <button onClick={() => handleApproval(voter._id, "approved")}>Approve</button>
              <button onClick={() => handleApproval(voter._id, "rejected")}>Reject</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ApproveVoters;

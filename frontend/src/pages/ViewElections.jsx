import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const ViewElections = () => {
  const { token } = useAuth();
  const [elections, setElections] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) {
      navigate("/login");
      return;
    }

    fetch("http://127.0.0.1:5000/voter/view_elections", {
      headers: { Authorization: token },
    })
      .then((res) => res.json())
      .then((data) => setElections(data.elections))
      .catch((err) => console.error(err));
  }, [token, navigate]);

  return (
    <div>
      <h2>Available Elections</h2>
      {elections.length > 0 ? (
        elections.map((election) => (
          <div key={election._id}>
            <h3>{election.title}</h3>
            <p>District: {election.district}</p>
            <button onClick={() => navigate("/vote", { state: { electionId: election._id } })}>
              Vote Now
            </button>
          </div>
        ))
      ) : (
        <p>No ongoing elections</p>
      )}
    </div>
  );
};

export default ViewElections;


// import { useEffect, useState } from "react";
// import { useAuth } from "../context/AuthContext";

// const ViewElections = () => {
//   const { token } = useAuth();
//   const [elections, setElections] = useState([]);
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     const fetchElections = async () => {
//       try {
//         const response = await fetch("http://localhost:5000/voter/view_elections", {
//           headers: { Authorization: token },
//         });
//         const data = await response.json();
//         if (response.ok) {
//           setElections(data.elections);
//         } else {
//           console.error(data.message);
//         }
//       } catch (error) {
//         console.error("Error fetching elections:", error);
//       } finally {
//         setLoading(false);
//       }
//     };

//     fetchElections();
//   }, [token]);

//   if (loading) return <p>Loading elections...</p>;
//   if (elections.length === 0) return <p>No elections available in your district.</p>;

//   return (
//     <div>
//       <h2>Available Elections</h2>
//       <ul>
//         {elections.map((election) => (
//           <li key={election._id}>
//             <h3>{election.title}</h3>
//             <p>District: {election.district}</p>
//             <p>Start Time: {new Date(election.start_time).toLocaleString()}</p>
//             <p>End Time: {new Date(election.end_time).toLocaleString()}</p>
//           </li>
//         ))}
//       </ul>
//     </div>
//   );
// };

// export default ViewElections;

import { useState, useContext } from "react";
import { AuthContext } from "../../context/AuthContext";

const CreateElection = () => {
  const { token } = useContext(AuthContext);
  const [title, setTitle] = useState("");
  const [district, setDistrict] = useState("");
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const electionData = { title, district, start_time: startTime, end_time: endTime };

    try {
        
        console.log(token);
        
      const response = await fetch("http://localhost:5000/admin/create_election", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(electionData),
      });

      const data = await response.json();
      console.log(data);
      
      if (response.ok) {
        setMessage("Election created successfully!");
        setTitle("");
        setDistrict("");
        setStartTime("");
        setEndTime("");
      } else {
        setMessage(data.message || "Failed to create election.");
      }
    } catch (error) {
      setMessage("Error: Could not create election.");
    }
  };

  return (
    <div>
      <h2>Create Election</h2>
      {message && <p>{message}</p>}
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Title" value={title} onChange={(e) => setTitle(e.target.value)} required />
        <input type="text" placeholder="District" value={district} onChange={(e) => setDistrict(e.target.value)} required />
        <input type="datetime-local" value={startTime} onChange={(e) => setStartTime(e.target.value)} required />
        <input type="datetime-local" value={endTime} onChange={(e) => setEndTime(e.target.value)} required />
        <button type="submit">Create Election</button>
      </form>
    </div>
  );
};

export default CreateElection;

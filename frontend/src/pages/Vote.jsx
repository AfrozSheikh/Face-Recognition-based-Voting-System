import { useState, useEffect, useRef } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate, useLocation } from "react-router-dom";

const Vote = () => {
  const { token } = useAuth();
  const [candidates, setCandidates] = useState([]);
  const [selectedCandidate, setSelectedCandidate] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const electionId = location.state?.electionId;

  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    if (!token) {
      navigate("/login");
      return;
    }
    if (!electionId) {
      navigate("/elections");
      return;
    }

    fetch(`http://127.0.0.1:5000/voter/view_elections`, {
      headers: { Authorization: token },
    })
      .then((res) => res.json())
      .then((data) => {
        const election = data.elections.find((e) => e._id === electionId);
        if (election) {
          setCandidates(election.candidates);
        }
      })
      .catch((err) => console.error(err));

    // Start Camera
    navigator.mediaDevices.getUserMedia({ video: true })
      .then((stream) => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      })
      .catch((err) => console.error("Error accessing camera:", err));
  }, [token, electionId, navigate]);

  const captureImage = () => {
    const canvas = canvasRef.current;
    const video = videoRef.current;
    if (canvas && video) {
      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      return canvas.toDataURL("image/jpeg"); // Convert to base64
    }
    return null;
  };

  const handleVote = async () => {
    if (!selectedCandidate) {
      alert("Please select a candidate");
      return;
    }

    const imageData = captureImage();
    if (!imageData) {
      alert("Failed to capture image");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:5000/voter/vote", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: token,
        },
        body: JSON.stringify({
          election_id: electionId,
          candidate_name: selectedCandidate,
          live_image: imageData, // Send captured image
        }),
      });

      const data = await response.json();
      alert(data.message);
      if (response.ok) navigate("/elections");
    } catch (error) {
      console.error(error);
      alert("Failed to cast vote");
    }

    setLoading(false);
  };

  return (
    <div>
      <h2>Vote for Your Candidate</h2>
      {candidates.length > 0 ? (
        candidates.map((candidate) => (
          <div key={candidate.name}>
            <input
              type="radio"
              id={candidate.name}
              name="candidate"
              value={candidate.name}
              onChange={(e) => setSelectedCandidate(e.target.value)}
            />
            <label htmlFor={candidate.name}>{candidate.name} ({candidate.party})</label>
          </div>
        ))
      ) : (
        <p>No candidates available</p>
      )}

      <h3>Face Verification</h3>
      <video ref={videoRef} autoPlay width="320" height="240"></video>
      <canvas ref={canvasRef} width="320" height="240" style={{ display: "none" }}></canvas>

      <button onClick={handleVote} disabled={loading}>
        {loading ? "Verifying..." : "Submit Vote"}
      </button>
    </div>
  );
};

export default Vote;

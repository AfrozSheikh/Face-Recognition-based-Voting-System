import { useState, useRef, useEffect } from "react";

const Signup = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    district: "",
  });
  const [faceImage, setFaceImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  // Start the camera when the component mounts
  useEffect(() => {
    const startCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (error) {
        console.error("Error accessing camera:", error);
      }
    };
    startCamera();

    return () => {
      if (videoRef.current && videoRef.current.srcObject) {
        videoRef.current.srcObject.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  // Handle form input changes
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Capture image from the live camera feed
  const captureImage = () => {
    if (!canvasRef.current || !videoRef.current) return;

    const canvas = canvasRef.current;
    const video = videoRef.current;
    const context = canvas.getContext("2d");

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    const imageData = canvas.toDataURL("image/jpeg"); // Convert to Base64
    setFaceImage(imageData);
    setPreview(imageData);
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!faceImage) {
      alert("Please capture your face image before submitting.");
      return;
    }

    const response = await fetch("http://localhost:5000/auth/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...formData, face_embedding: faceImage }),
    });

    const result = await response.json();
    if (response.ok) {
      alert("Signup successful! Wait for admin approval.");
    } else {
      alert(result.message);
    }
  };

  return (
    <div>
      <h2>Signup</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" name="name" placeholder="Name" onChange={handleChange} required />
        <input type="email" name="email" placeholder="Email" onChange={handleChange} required />
        <input type="password" name="password" placeholder="Password" onChange={handleChange} required />
        <input type="text" name="district" placeholder="District" onChange={handleChange} required />

        {/* Live Camera Feed */}
        <div>
          <video ref={videoRef} autoPlay style={{ width: "300px", height: "200px" }}></video>
        </div>

        {/* Hidden Canvas for Capturing Image */}
        <canvas ref={canvasRef} style={{ display: "none" }}></canvas>

        <button type="button" onClick={captureImage}>Capture Face</button>

        {/* Show Captured Image Preview */}
        {preview && <img src={preview} alt="Captured Face" style={{ width: "100px", height: "100px" }} />}

        <button type="submit">Signup</button>
      </form>
    </div>
  );
};

export default Signup;

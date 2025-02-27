from deepface import DeepFace
import numpy as np

def verify_face(registered_embedding, live_image_path):
    """
    Compare stored face embedding with a live image.
    """
    try:
        result = DeepFace.represent(live_image_path, model_name="Facenet", enforce_detection=False)
        live_embedding = result[0]['embedding']

        # Compute cosine similarity
        similarity = np.dot(registered_embedding, live_embedding) / (np.linalg.norm(registered_embedding) * np.linalg.norm(live_embedding))

        return similarity > 0.8  # Threshold for matching
    except Exception as e:
        print(f"Face verification error: {e}")
        return False

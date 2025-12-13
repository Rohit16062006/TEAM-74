import api from "../services/api";
import { useState } from "react";

function CreatePlan() {
  const [result, setResult] = useState(null);

  const createPlan = async () => {
    try {
      const response = await api.post("/create-plan", {
        job_title: "Backend Developer",
        experience: "Fresher",
        days: 7,
        skills: ["Python", "SQL", "FastAPI"],
      });
      setResult(response.data);
    } catch (err) {
      console.error(err);
      alert("API call failed");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Create Plan Test</h2>
      <button onClick={createPlan}>Create Plan</button>

      {result && (
        <pre style={{ marginTop: "20px" }}>
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </div>
  );
}

export default CreatePlan;

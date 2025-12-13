import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function JobSetup() {
  const navigate = useNavigate();

  const [jobTitle, setJobTitle] = useState("");
  const [experience, setExperience] = useState("Fresher");
  const [days, setDays] = useState(7);
  const [skills, setSkills] = useState([]);

  const handleSubmit = async () => {
    try {
      const response = await api.post("/create-plan", {
        job_title: jobTitle,
        experience,
        days,
        skills,
      });

      // Navigate using returned plan ID
      navigate(`/calendar/${response.data.id}`);
    } catch (error) {
      console.error(error);
      alert("Failed to create plan");
    }
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow">
      <h2 className="text-xl font-semibold mb-4">Set up your Job Plan</h2>

      <input
        type="text"
        placeholder="Job Title"
        value={jobTitle}
        onChange={(e) => setJobTitle(e.target.value)}
        className="border p-2 rounded w-full mb-3"
      />

      <select
        value={experience}
        onChange={(e) => setExperience(e.target.value)}
        className="border p-2 rounded w-full mb-3"
      >
        <option>Fresher</option>
        <option>1-3 Years</option>
        <option>3+ Years</option>
      </select>

      <input
        type="number"
        value={days}
        onChange={(e) => setDays(e.target.value)}
        className="border p-2 rounded w-full mb-3"
      />

      <input
        type="text"
        placeholder="Skills (comma separated)"
        onChange={(e) =>
          setSkills(e.target.value.split(",").map((s) => s.trim()))
        }
        className="border p-2 rounded w-full mb-4"
      />

      <button
        onClick={handleSubmit}
        className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700"
      >
        Create Plan
      </button>
    </div>
  );
}

export default JobSetup;

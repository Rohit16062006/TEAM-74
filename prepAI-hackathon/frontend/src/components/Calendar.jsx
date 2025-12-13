import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import api from "../services/api";

function Calendar() {
  const { planId } = useParams();
  const [task, setTask] = useState(null);

  useEffect(() => {
    api
      .get("/daily-task", {
        params: { plan_id: planId, day: 1 },
      })
      .then((res) => setTask(res.data))
      .catch(console.error);
  }, [planId]);

  return (
    <div className="bg-white p-6 rounded-xl shadow">
      <h2 className="text-xl font-semibold mb-4">Today's Task</h2>

      {task ? (
        <div>
          <p className="font-medium">{task.task}</p>
          <p className="text-sm text-gray-500">{task.skill}</p>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default Calendar;

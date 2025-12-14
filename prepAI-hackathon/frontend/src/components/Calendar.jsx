import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import api from "../services/api";

function Calendar() {
  const { planId } = useParams();
  const navigate = useNavigate();
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get(`/plan-tasks?plan_id=${planId}`)
      .then((res) => {
        setTasks(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, [planId]);

  if (loading) return <div className="p-6">Loading tasks...</div>;

  return (
    <div className="bg-white p-6 rounded-xl shadow">
      <h2 className="text-2xl font-bold mb-6 text-slate-800">Your Learning Plan</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {tasks.map((task) => (
          <div
            key={task.id}
            onClick={() => navigate(`/interview/${task.id}`)}
            className="p-4 border rounded-xl hover:shadow-md cursor-pointer transition-all bg-slate-50 hover:bg-white border-slate-200 hover:border-indigo-300 group"
          >
            <div className="flex justify-between items-center mb-2">
              <span className="bg-indigo-100 text-indigo-700 text-xs px-2 py-1 rounded-full font-medium">Day {task.day}</span>
              <span className="text-xs text-slate-500">{task.type}</span>
            </div>
            <h3 className="font-semibold text-slate-700 group-hover:text-indigo-600 mb-1 line-clamp-2">
              {task.task}
            </h3>
            <p className="text-sm text-slate-500 font-medium mt-2">
              Skill: <span className="text-slate-700">{task.skill}</span>
            </p>
          </div>
        ))}
      </div>

      {tasks.length === 0 && (
        <div className="text-center py-12 text-slate-500">
          No tasks found for this plan.
        </div>
      )}
    </div>
  );
}

export default Calendar;

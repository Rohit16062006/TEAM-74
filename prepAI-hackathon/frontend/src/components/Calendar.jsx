import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useApi } from '../hooks/useApi';
import { CheckCircle2, Circle, ArrowRight, Code, BookOpen } from 'lucide-react';

const Calendar = () => {
    const { planId } = useParams();
    const navigate = useNavigate();
    const { getDailyTask } = useApi();
    const [selectedDay, setSelectedDay] = useState(null);
    const [tasks, setTasks] = useState([]);
    const [loading, setLoading] = useState(false);

    // Mock days - in a real app better to fetch plan details first to know count
    // We'll assume 7 days based on default for now or fetch if possible.
    // The API doesn't have "get plan details", only create.
    // We'll just show 7 days dynamically or standard.
    const days = Array.from({ length: 7 }, (_, i) => i + 1);

    const handleDayClick = async (day) => {
        setSelectedDay(day);
        setLoading(true);
        try {
            const data = await getDailyTask(planId, day);
            setTasks(data);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="space-y-8">
            <div className="text-center">
                <h2 className="text-2xl font-bold text-slate-800">Your Learning Schedule</h2>
                <p className="text-slate-500">Select a day to view your tasks</p>
            </div>

            {/* Days Grid */}
            <div className="grid grid-cols-3 md:grid-cols-7 gap-4">
                {days.map((day) => (
                    <button
                        key={day}
                        onClick={() => handleDayClick(day)}
                        className={`
              p-4 rounded-xl border transition-all flex flex-col items-center justify-center gap-2 aspect-square
              ${selectedDay === day
                                ? 'bg-gradient-to-br from-blue-500 to-indigo-600 text-white shadow-lg scale-105 border-transparent'
                                : 'bg-white border-slate-200 hover:border-indigo-300 hover:shadow-md text-slate-600'}
            `}
                    >
                        <span className="text-3xl font-bold">{day}</span>
                        <span className="text-xs uppercase tracking-wider font-medium opacity-80">Day</span>
                    </button>
                ))}
            </div>

            {/* Tasks List */}
            {selectedDay && (
                <div className="bg-white rounded-2xl shadow-xl p-6 md:p-8 animate-fade-in-up">
                    <div className="flex justify-between items-center mb-6">
                        <h3 className="text-xl font-bold text-slate-800">Day {selectedDay} Tasks</h3>
                        {loading && <span className="text-sm text-indigo-500">Loading...</span>}
                    </div>

                    <div className="space-y-4">
                        {tasks.length === 0 && !loading ? (
                            <p className="text-slate-400 italic">No tasks found for this day.</p>
                        ) : (
                            tasks.map((task) => (
                                <div
                                    key={task.task_id}
                                    className="group flex flex-col md:flex-row md:items-center justify-between p-5 rounded-xl border border-slate-100 bg-slate-50 hover:bg-white hover:shadow-md transition-all"
                                >
                                    <div className="flex items-start gap-4 mb-4 md:mb-0">
                                        <div className={`p-3 rounded-lg ${task.type === 'interview' ? 'bg-purple-100 text-purple-600' : 'bg-blue-100 text-blue-600'}`}>
                                            {task.type === 'interview' ? <Code className="w-6 h-6" /> : <BookOpen className="w-6 h-6" />}
                                        </div>
                                        <div>
                                            <h4 className="font-semibold text-slate-800 text-lg">{task.task}</h4>
                                            <div className="flex gap-2 mt-1">
                                                <span className="text-xs px-2 py-1 rounded-full bg-slate-200 text-slate-600 font-medium">
                                                    {task.skill}
                                                </span>
                                                <span className="text-xs px-2 py-1 rounded-full bg-slate-200 text-slate-600 font-medium capitalize">
                                                    {task.type}
                                                </span>
                                            </div>
                                        </div>
                                    </div>

                                    {task.type === 'interview' && (
                                        <button
                                            onClick={() => navigate(`/interview/${task.task_id}`)}
                                            className="px-6 py-3 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white font-medium flex items-center gap-2 group-hover:scale-105 transition-all"
                                        >
                                            Start Interview <ArrowRight className="w-4 h-4" />
                                        </button>
                                    )}
                                    {task.type !== 'interview' && (
                                        <button className="px-6 py-3 rounded-lg border-2 border-slate-200 text-slate-400 cursor-default font-medium flex items-center gap-2">
                                            <CheckCircle2 className="w-4 h-4" /> Mark Done
                                        </button>
                                    )}
                                </div>
                            ))
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default Calendar;

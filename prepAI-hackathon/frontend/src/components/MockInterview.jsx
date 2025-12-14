import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useApi } from '../hooks/useApi';
import { Mic, Send, AlertCircle } from 'lucide-react';

const MockInterview = () => {
    const { taskId } = useParams();
    const navigate = useNavigate();
    const { submitAnswer, getTaskById } = useApi();
    const [answer, setAnswer] = useState('');
    const [loading, setLoading] = useState(false);
    const [task, setTask] = useState(null);

    React.useEffect(() => {
        getTaskById(taskId)
            .then(setTask)
            .catch(console.error);
    }, [taskId]);

    const handleSubmit = async () => {
        if (!answer.trim()) return;

        setLoading(true);
        try {
            const result = await submitAnswer({
                task_id: parseInt(taskId),
                answer_text: answer
            });
            // Navigate to feedback with state
            navigate(`/feedback/${taskId}`, { state: { result } });
        } catch (e) {
            console.error(e);
            alert('Error submitting answer');
        } finally {
            setLoading(false);
        }
    };

    if (!task) return <div className="p-8 text-center">Loading Interview...</div>;

    return (
        <div className="max-w-3xl mx-auto">
            <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
                <div className="bg-slate-900 p-8 text-white">
                    <div className="flex items-center gap-3 mb-4 text-emerald-400">
                        <div className="w-2 h-2 rounded-full bg-emerald-400/50 animate-pulse"></div>
                        <span className="font-mono text-sm uppercase tracking-widest">Live Interview Session</span>
                    </div>
                    <div className="flex justify-between items-start mb-2">
                        <h2 className="text-3xl font-bold">Technical Assessment</h2>
                        <span className="bg-slate-800 text-slate-300 text-xs px-2 py-1 rounded border border-slate-700">
                            {task.skill} - Day {task.day}
                        </span>
                    </div>
                    <h3 className="text-xl font-semibold mb-2 text-indigo-400">
                        {task.type} Problem
                    </h3>
                    <p className="text-slate-300 text-lg leading-relaxed bg-slate-800/50 p-4 rounded-lg border border-slate-700">
                        {task.task}
                    </p>
                </div>

                <div className="p-8">
                    <div className="mb-6">
                        <label className="block text-sm font-bold text-slate-700 mb-2 uppercase tracking-wide">
                            Your Answer
                        </label>
                        <div className="relative">
                            <textarea
                                value={answer}
                                onChange={(e) => setAnswer(e.target.value)}
                                className="w-full h-64 p-4 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:outline-none resize-none font-mono text-sm leading-relaxed"
                                placeholder="Type your code or explanation here..."
                            ></textarea>
                            <div className="absolute bottom-4 right-4">
                                <button className="p-2 rounded-full bg-white shadow-sm border border-slate-100 text-slate-400 hover:text-indigo-600 transition-colors">
                                    <Mic className="w-5 h-5" />
                                </button>
                            </div>
                        </div>
                    </div>

                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2 text-slate-400 text-sm">
                            <AlertCircle className="w-4 h-4" />
                            <span>Markdown supported</span>
                        </div>
                        <button
                            onClick={handleSubmit}
                            disabled={loading || !answer.trim()}
                            className="px-8 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold rounded-xl shadow-lg flex items-center gap-2 transform active:scale-95 transition-all disabled:opacity-50"
                        >
                            {loading ? 'Analyzing...' : 'Submit Answer'} <Send className="w-4 h-4" />
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default MockInterview;

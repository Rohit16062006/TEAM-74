import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useApi } from '../hooks/useApi';
import { Mic, Send, AlertCircle } from 'lucide-react';

const MockInterview = () => {
    const { taskId } = useParams();
    const navigate = useNavigate();
    const { submitAnswer } = useApi();
    const [answer, setAnswer] = useState('');
    const [loading, setLoading] = useState(false);

    // In a real app, we'd fetch the task details here to show the question.
    // For now, we assume the user knows context or we'd fetch task by ID if backend supported /tasks/:id
    // We'll show a generic prompts or just "Provide your solution".

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

    return (
        <div className="max-w-3xl mx-auto">
            <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
                <div className="bg-slate-900 p-8 text-white">
                    <div className="flex items-center gap-3 mb-4 text-emerald-400">
                        <div className="w-2 h-2 rounded-full bg-emerald-400/50 animate-pulse"></div>
                        <span className="font-mono text-sm uppercase tracking-widest">Live Interview Session</span>
                    </div>
                    <h2 className="text-3xl font-bold mb-4">Technical Assessment</h2>
                    <p className="text-slate-400 text-lg">
                        Please provide a comprehensive answer. The AI will evaluate your technical accuracy, clarity, and completeness.
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

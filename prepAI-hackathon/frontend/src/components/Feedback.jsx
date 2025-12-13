import React, { useEffect } from 'react';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { CheckCircle, BarChart2, Home, ArrowRight } from 'lucide-react';

const Feedback = () => {
    const { state } = useLocation();
    const navigate = useNavigate();
    const { taskId } = useParams();

    // If no state (direct access), redirect safely
    useEffect(() => {
        if (!state?.result) {
            navigate('/dashboard'); // or back to interview
        }
    }, [state, navigate]);

    if (!state?.result) return null;

    const { result } = state;
    const { technical, behavioral, comm, readiness } = result;

    // Gauge calculation
    const gaugeStyle = {
        background: `conic-gradient(#4f46e5 ${readiness * 3.6}deg, #e2e8f0 0deg)`
    };

    return (
        <div className="max-w-2xl mx-auto space-y-8">
            <div className="text-center animate-fade-in-down">
                <div className="inline-flex items-center justify-center p-3 rounded-full bg-green-100 text-green-600 mb-4 shadow-sm">
                    <CheckCircle className="w-8 h-8" />
                </div>
                <h2 className="text-3xl font-bold text-slate-800 mb-2">Assessment Complete</h2>
                <p className="text-slate-500">Here is your AI-generated performance breakdown.</p>
            </div>

            <div className="bg-white rounded-2xl shadow-xl p-8 border border-indigo-50">
                <div className="flex flex-col md:flex-row items-center justify-between gap-8 mb-8">
                    {/* Readiness Gauge */}
                    <div className="relative w-40 h-40 flex-shrink-0">
                        <div className="absolute inset-0 rounded-full" style={gaugeStyle}></div>
                        <div className="absolute inset-2 bg-white rounded-full flex flex-col items-center justify-center">
                            <span className="text-4xl font-bold text-slate-800">{readiness}%</span>
                            <span className="text-xs uppercase font-bold text-slate-400">Readiness</span>
                        </div>
                    </div>

                    <div className="flex-1 w-full space-y-4">
                        <ScoreBar label="Technical Accuracy" score={technical} color="bg-blue-500" />
                        <ScoreBar label="Behavioral Fit" score={behavioral} color="bg-purple-500" />
                        <ScoreBar label="Communication" score={comm} color="bg-pink-500" />
                    </div>
                </div>

                <div className="pt-8 border-t border-slate-100 flex gap-4">
                    <button
                        onClick={() => navigate('/dashboard')}
                        className="flex-1 py-3 px-4 rounded-xl border-2 border-slate-200 text-slate-600 font-bold hover:border-indigo-500 hover:text-indigo-600 transition-colors flex items-center justify-center gap-2"
                    >
                        <Home className="w-4 h-4" /> Dashboard
                    </button>
                    <button
                        onClick={() => navigate(-1)} // Go back to maybe calendar?
                        className="flex-1 py-3 px-4 rounded-xl bg-indigo-600 text-white font-bold hover:bg-indigo-700 transition-colors shadow-lg shadow-indigo-200 flex items-center justify-center gap-2"
                    >
                        Next Task <ArrowRight className="w-4 h-4" />
                    </button>
                </div>
            </div>
        </div>
    );
};

const ScoreBar = ({ label, score, color }) => (
    <div>
        <div className="flex justify-between mb-1">
            <span className="text-sm font-semibold text-slate-700">{label}</span>
            <span className="text-sm font-bold text-slate-900">{score}%</span>
        </div>
        <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
            <div
                className={`h-2.5 rounded-full ${color} transition-all duration-1000 ease-out`}
                style={{ width: `${score}%` }}
            ></div>
        </div>
    </div>
);

export default Feedback;

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApi } from '../hooks/useApi';
import { Briefcase, Clock, CalendarDays } from 'lucide-react';

const JobSetup = () => {
    const navigate = useNavigate();
    const { createPlan } = useApi();
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        job_title: 'backend_developer',
        experience: 'fresher',
        days: 7
    });

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const data = await createPlan(formData);
            if (data && data.plan_id) {
                // Store planId for global usage if needed
                localStorage.setItem('currentPlanId', data.plan_id);
                navigate(`/calendar/${data.plan_id}`);
            }
        } catch (error) {
            console.error("Failed to create plan:", error);
            alert("Failed to create plan. Please check backend connection.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto">
            <div className="bg-white rounded-2xl shadow-xl p-8 border border-indigo-50">
                <div className="text-center mb-10">
                    <h2 className="text-3xl font-bold text-slate-800 mb-4">Create Your Plan</h2>
                    <p className="text-slate-500">Tell us about your target role to generate a personalized study roadmap.</p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="space-y-2">
                        <label className="block text-sm font-semibold text-slate-700 flex items-center gap-2">
                            <Briefcase className="w-4 h-4 text-indigo-500" /> Job Title
                        </label>
                        <select
                            value={formData.job_title}
                            onChange={(e) => setFormData({ ...formData, job_title: e.target.value })}
                            className="w-full p-4 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition-all"
                        >
                            <option value="backend_developer">Backend Developer</option>
                            <option value="frontend_developer">Frontend Developer</option>
                            <option value="data_analyst">Data Analyst</option>
                        </select>
                    </div>

                    <div className="space-y-2">
                        <label className="block text-sm font-semibold text-slate-700 flex items-center gap-2">
                            <Clock className="w-4 h-4 text-indigo-500" /> Experience Level
                        </label>
                        <select
                            value={formData.experience}
                            onChange={(e) => setFormData({ ...formData, experience: e.target.value })}
                            className="w-full p-4 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition-all"
                        >
                            <option value="fresher">Fresher</option>
                            <option value="junior">Junior (1-3 years)</option>
                            <option value="senior">Senior (3+ years)</option>
                        </select>
                    </div>

                    <div className="space-y-2">
                        <label className="block text-sm font-semibold text-slate-700 flex items-center gap-2">
                            <CalendarDays className="w-4 h-4 text-indigo-500" /> Duration (Days)
                        </label>
                        <input
                            type="number"
                            min="3"
                            max="30"
                            value={formData.days}
                            onChange={(e) => setFormData({ ...formData, days: parseInt(e.target.value) })}
                            className="w-full p-4 rounded-xl bg-slate-50 border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition-all"
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full py-4 mt-8 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white text-lg font-bold rounded-xl shadow-lg shadow-indigo-200 transform hover:scale-[1.02] transition-all disabled:opacity-70 disabled:cursor-not-allowed"
                    >
                        {loading ? 'Generating Plan...' : 'Generate Plan'}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default JobSetup;

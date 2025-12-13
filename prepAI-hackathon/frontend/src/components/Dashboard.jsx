import React, { useEffect, useState } from 'react';
import { useApi } from '../hooks/useApi';
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
    AreaChart, Area, RadialBarChart, RadialBar, Legend, BarChart, Bar
} from 'recharts';
import { TrendingUp, Award, Zap, Calendar, Target, Activity } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
    const { getDashboard } = useApi();
    const navigate = useNavigate();
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const planId = localStorage.getItem('currentPlanId');
        // If no plan, maybe redirect or show empty state. 
        // For hackathon, assuming flow is respected.
        if (planId) {
            getDashboard(planId)
                .then(setData)
                .catch(err => console.error("Dashboard fetch error:", err))
                .finally(() => setLoading(false));
        } else {
            setLoading(false);
        }
    }, []);

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-[50vh]">
                <div className="w-12 h-12 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
            </div>
        );
    }

    if (!data) {
        return (
            <div className="text-center p-12 bg-white rounded-2xl shadow-xl">
                <h2 className="text-2xl font-bold text-slate-800">No Data Available</h2>
                <p className="text-slate-500 mb-6">Create a plan to see your analytics.</p>
                <button onClick={() => navigate('/')} className="px-6 py-3 bg-indigo-600 text-white rounded-xl">Create Plan</button>
            </div>
        );
    }

    // Transform recent activity for charts if needed, or use as list
    const recentActivityData = data.recent_activity || [];

    return (
        <div className="space-y-8 animate-fade-in-up">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                    <h2 className="text-3xl font-bold text-slate-800">Overview</h2>
                    <p className="text-slate-500">Welcome back! Here's your prep progress.</p>
                </div>
                <div className="flex items-center gap-2 bg-white px-4 py-2 rounded-full shadow-sm border border-slate-100">
                    <span className="w-3 h-3 rounded-full bg-emerald-500 animate-pulse"></span>
                    <span className="text-sm font-medium text-slate-600">
                        Day {data.current_day} of {data.total_days}
                    </span>
                </div>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <StatCard
                    title="Readiness Score"
                    value={`${data.readiness}%`}
                    subtitle="Overall proficiency"
                    icon={<Award className="w-6 h-6 text-white" />}
                    color="bg-gradient-to-br from-indigo-500 to-purple-600"
                />
                <StatCard
                    title="Trend"
                    value={data.trend === 'up' ? 'Rising ↗' : data.trend === 'down' ? 'Falling ↘' : 'Stable →'}
                    subtitle="Vs last assessment"
                    icon={<TrendingUp className="w-6 h-6 text-white" />}
                    color="bg-gradient-to-br from-emerald-400 to-teal-500"
                />
                <StatCard
                    title="Tasks Done"
                    value={data.completed_tasks}
                    subtitle={`${data.total_days * 2 - data.completed_tasks} remaining`} // Approx 2 tasks/day
                    icon={<Zap className="w-6 h-6 text-white" />}
                    color="bg-gradient-to-br from-amber-400 to-orange-500"
                />
                <StatCard
                    title="Day Streak"
                    value={data.current_day}
                    subtitle="Consistent effort"
                    icon={<Calendar className="w-6 h-6 text-white" />}
                    color="bg-gradient-to-br from-blue-400 to-cyan-500"
                />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Main Chart */}
                <div className="lg:col-span-2 bg-white p-6 rounded-2xl shadow-xl border border-slate-100">
                    <div className="flex items-center justify-between mb-6">
                        <h3 className="text-xl font-bold text-slate-800 flex items-center gap-2">
                            <Activity className="w-5 h-5 text-indigo-500" /> Performance Trajectory
                        </h3>
                    </div>
                    <div className="h-80">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={[
                                { name: 'Day 1', score: 30 },
                                { name: 'Day 2', score: 45 },
                                { name: 'Day 3', score: Math.max(50, data.readiness - 10) },
                                { name: 'Today', score: data.readiness }
                            ]}>
                                <defs>
                                    <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                                        <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid vertical={false} stroke="#f1f5f9" />
                                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#64748b' }} />
                                <YAxis axisLine={false} tickLine={false} tick={{ fill: '#64748b' }} domain={[0, 100]} />
                                <Tooltip
                                    contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }}
                                />
                                <Area type="monotone" dataKey="score" stroke="#6366f1" strokeWidth={4} fillOpacity={1} fill="url(#colorScore)" />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Skill Breakdown */}
                <div className="bg-white p-6 rounded-2xl shadow-xl border border-slate-100">
                    <h3 className="text-xl font-bold text-slate-800 mb-6 flex items-center gap-2">
                        <Target className="w-5 h-5 text-indigo-500" /> Skill Breakdown
                    </h3>
                    <div className="space-y-6">
                        {data.skill_stats.map((skill, idx) => (
                            <div key={idx}>
                                <div className="flex justify-between mb-2">
                                    <span className="font-semibold text-slate-700">{skill.skill}</span>
                                    <span className="font-bold text-indigo-600">{skill.level}%</span>
                                </div>
                                <div className="w-full bg-slate-100 rounded-full h-3">
                                    <div
                                        className="bg-indigo-500 h-3 rounded-full transition-all duration-1000"
                                        style={{ width: `${skill.level}%` }}
                                    ></div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Recent Activity */}
            <div className="bg-white rounded-2xl shadow-xl border border-slate-100 overflow-hidden">
                <div className="p-6 border-b border-slate-100 bg-slate-50">
                    <h3 className="text-xl font-bold text-slate-800">Recent Activity</h3>
                </div>
                <div className="divide-y divide-slate-100">
                    {recentActivityData.map((task) => (
                        <div key={task.task_id} className="p-6 flex items-center justify-between hover:bg-slate-50 transition-colors">
                            <div className="flex items-center gap-4">
                                <div className={`w-10 h-10 rounded-full flex items-center justify-center ${task.type === 'interview' ? 'bg-purple-100 text-purple-600' : 'bg-blue-100 text-blue-600'}`}>
                                    {task.type === 'interview' ? <Activity className="w-5 h-5" /> : <Calendar className="w-5 h-5" />}
                                </div>
                                <div>
                                    <h4 className="font-semibold text-slate-800">{task.task}</h4>
                                    <p className="text-sm text-slate-500 capitalize">{task.type} • {task.skill}</p>
                                </div>
                            </div>
                            <span className="px-3 py-1 bg-green-100 text-green-700 text-xs font-bold rounded-full uppercase tracking-wide">
                                Completed
                            </span>
                        </div>
                    ))}
                    {recentActivityData.length === 0 && (
                        <div className="p-8 text-center text-slate-400">No recent activity yet. Start a task!</div>
                    )}
                </div>
            </div>
        </div>
    );
};

const StatCard = ({ title, value, subtitle, icon, color }) => (
    <div className={`p-6 rounded-2xl shadow-lg text-white ${color} relative overflow-hidden group`}>
        <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity transform scale-150">
            {icon}
        </div>
        <div className="relative z-10">
            <div className="flex justify-between items-start mb-4">
                <div>
                    <p className="text-indigo-100 font-medium mb-1">{title}</p>
                    <h3 className="text-3xl font-bold">{value}</h3>
                </div>
                <div className="p-2 bg-white/20 rounded-lg backdrop-blur-sm">
                    {icon}
                </div>
            </div>
            <p className="text-sm text-indigo-100 opacity-90">{subtitle}</p>
        </div>
    </div>
);

export default Dashboard;

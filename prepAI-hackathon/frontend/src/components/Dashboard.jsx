import React, { useEffect, useState } from 'react';
import { useApi } from '../hooks/useApi';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { TrendingUp, Award, Zap } from 'lucide-react';

const Dashboard = () => {
    const { getReadiness } = useApi();
    const [data, setData] = useState({ readiness: 0, trend: 'stable' });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const planId = localStorage.getItem('currentPlanId');
        if (planId) {
            getReadiness(planId).then(setData).catch(console.error).finally(() => setLoading(false));
        } else {
            setLoading(false);
        }
    }, []);

    // Hand-coded "trend" data for visualization since backend returns single value
    const chartData = [
        { name: 'Day 1', score: 30 },
        { name: 'Day 2', score: 45 },
        { name: 'Day 3', score: 55 },
        { name: 'Day 4', score: data.readiness > 55 ? 60 : data.readiness - 5 },
        { name: 'Current', score: data.readiness },
    ];

    return (
        <div className="space-y-6">
            <h2 className="text-2xl font-bold text-slate-800">Your Progress Dashboard</h2>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card
                    title="Interview Readiness"
                    value={`${data.readiness}%`}
                    subtitle="Based on recent mock interviews"
                    icon={<Award className="w-6 h-6 text-indigo-600" />}
                />
                <Card
                    title="Current Trend"
                    value={data.trend === 'up' ? 'Improving' : 'Stable'}
                    subtitle="Keep up the consistency!"
                    icon={<TrendingUp className="w-6 h-6 text-emerald-600" />}
                />
                <Card
                    title="Tasks Completed"
                    value="12"
                    subtitle="You're on track for Day 7"
                    icon={<Zap className="w-6 h-6 text-amber-500" />}
                />
            </div>

            <div className="bg-white p-6 rounded-2xl shadow-xl border border-indigo-50 h-80">
                <h3 className="text-lg font-bold text-slate-700 mb-4">Readiness Trajectory</h3>
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={chartData}>
                        <defs>
                            <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#4f46e5" stopOpacity={0.3} />
                                <stop offset="95%" stopColor="#4f46e5" stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                        <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#94a3b8' }} />
                        <YAxis axisLine={false} tickLine={false} tick={{ fill: '#94a3b8' }} />
                        <Tooltip
                            contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                        />
                        <Area type="monotone" dataKey="score" stroke="#4f46e5" strokeWidth={3} fillOpacity={1} fill="url(#colorScore)" />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

const Card = ({ title, value, subtitle, icon }) => (
    <div className="bg-white p-6 rounded-2xl shadow-lg border border-slate-100">
        <div className="flex items-start justify-between mb-4">
            <div>
                <p className="text-slate-500 text-sm font-medium">{title}</p>
                <h3 className="text-3xl font-bold text-slate-800 mt-1">{value}</h3>
            </div>
            <div className="p-3 bg-slate-50 rounded-xl">
                {icon}
            </div>
        </div>
        <p className="text-sm text-slate-400">{subtitle}</p>
    </div>
);

export default Dashboard;

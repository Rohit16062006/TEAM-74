import React from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
  useNavigate,
  useLocation,
} from "react-router-dom";

import JobSetup from "./components/JobSetup";
import Calendar from "./components/Calendar";
import MockInterview from "./components/MockInterview";
import Feedback from "./components/Feedback";
import Dashboard from "./components/Dashboard";

/* -------------------------------
   Layout component (router-aware)
-------------------------------- */
function AppLayout() {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 text-slate-800 p-4 md:p-8 font-sans">
      <div className="max-w-4xl mx-auto space-y-8">
        <header className="flex justify-between items-center bg-white/80 backdrop-blur-sm p-4 rounded-xl shadow-sm border border-white/20">
          <h1
            onClick={() => navigate("/")}
            className="text-2xl md:text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600 cursor-pointer hover:opacity-80 transition-opacity"
          >
            PrepAI
          </h1>

          <nav className="flex space-x-4">
            <button
              onClick={() => navigate("/dashboard")}
              className="text-sm font-medium text-slate-600 hover:text-indigo-600 transition-colors"
            >
              Dashboard
            </button>
          </nav>
        </header>

        <main>
          <Routes>
            <Route path="/" element={<JobSetup />} />
            <Route path="/calendar/:planId" element={<Calendar />} />
            <Route path="/interview/:taskId" element={<MockInterview />} />
            <Route path="/feedback/:taskId" element={<Feedback />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

/* -------------------------------
   Root App (Router wrapper)
-------------------------------- */
export default function App() {
  return (
    <BrowserRouter>
      <AppLayout />
    </BrowserRouter>
  );
}
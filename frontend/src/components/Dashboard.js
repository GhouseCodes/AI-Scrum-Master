import React, { useState, useEffect } from 'react';
import apiClient from '../utils/api';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  Filler
} from 'chart.js';
import { Line, Doughnut } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  Filler
);

function Dashboard() {
  const [stats, setStats] = useState({
    sprintName: 'Loading...',
    daysRemaining: 0,
    tasksCompleted: '0/0',
    velocity: 0
  });
  const [updates, setUpdates] = useState([
    { person: 'Alice', update: 'Worked on authentication, plan to finish today. Blocked by API rate limiting.' },
    { person: 'Bob', update: 'Fixing bugs in the dashboard layout. No blockers.' },
    { person: 'Charlie', update: 'Integrating rate limiter. Almost done.' }
  ]);
  const [aiInsights, setAiInsights] = useState(null);
  const [loading, setLoading] = useState(false);
  const [burndownData, setBurndownData] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const sprints = await apiClient.getSprints();
      const analytics = await apiClient.getAnalytics();
      
      if (sprints && sprints.length > 0) {
        const currentSprint = sprints[sprints.length - 1];
        const completed = currentSprint.tasks.filter(t => t.status === 'done').length;
        
        setStats({
          sprintName: currentSprint.name,
          daysRemaining: 7, 
          tasksCompleted: `${completed}/${currentSprint.tasks.length}`,
          velocity: analytics.velocity.current
        });
        setBurndownData(analytics.burndown);
      }
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    }
  };

  const handleGenerateInsights = async () => {
    setLoading(true);
    try {
      const result = await apiClient.generateInsights({ updates });
      setAiInsights(result.insights);
    } catch (error) {
      console.error('Failed to generate insights:', error);
    } finally {
      setLoading(false);
    }
  };

  // Burndown Chart Configuration
  const burndownChartData = {
    labels: Array.from({ length: 11 }, (_, i) => `D${i}`),
    datasets: [
      {
        label: 'Actual',
        data: burndownData?.actual || [],
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        fill: true,
        tension: 0.4
      },
      {
        label: 'Ideal',
        data: burndownData?.ideal || [],
        borderColor: '#9ca3af',
        borderDash: [5, 5],
        fill: false
      }
    ]
  };

  // Risk Meter Configuration (Simplified logic based on updates)
  const riskValue = updates.filter(u => u.update.toLowerCase().includes('block')).length * 30;
  const riskChartData = {
    datasets: [{
      data: [riskValue, 100 - riskValue],
      backgroundColor: ['#ef4444', '#e5e7eb'],
      borderWidth: 0,
      circumference: 180,
      rotation: 270,
    }]
  };

  return (
    <div className="dashboard">
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Current Sprint</h3>
          <p className="stat-value">{stats.sprintName}</p>
        </div>
        <div className="stat-card">
          <h3>Days Remaining</h3>
          <p className="stat-value">{stats.daysRemaining}</p>
        </div>
        <div className="stat-card">
          <h3>Tasks Completed</h3>
          <p className="stat-value">{stats.tasksCompleted}</p>
        </div>
        <div className="stat-card">
          <h3>Team Velocity</h3>
          <p className="stat-value">{stats.velocity}</p>
        </div>
      </div>

      <div className="dashboard-main-content">
        <div className="left-column">
          <div className="standup-summary-card">
            <h2>Team Sync Summary</h2>
            <div className="team-updates">
              {updates.map((u, i) => (
                <div key={i} className="update-item">
                  <div className="avatar-small">{u.person[0]}</div>
                  <div className="update-content">
                    <p className="name">{u.person}</p>
                    <p className="msg">{u.update}</p>
                  </div>
                </div>
              ))}
            </div>
            
            <button 
              className="btn-insights" 
              onClick={handleGenerateInsights}
              disabled={loading}
            >
              {loading ? 'Analyzing...' : 'Generate AI Insights'}
            </button>

            {aiInsights && (
              <div className="ai-feedback-box">
                <h4>AI Scrum Master Analysis</h4>
                <ul>
                  {aiInsights.map((insight, i) => (
                    <li key={i}>{insight}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>

        <div className="right-column">
          <div className="chart-card-elevated">
            <h3>Sprint Burndown</h3>
            <div className="chart-h-200">
              <Line data={burndownChartData} options={{ responsive: true, maintainAspectRatio: false }} />
            </div>
          </div>

          <div className="chart-card-elevated">
            <h3>Sprint Risk</h3>
            <div className="risk-meter-container">
              <Doughnut data={riskChartData} options={{ responsive: true, maintainAspectRatio: false, plugins: { tooltip: { enabled: false } } }} />
              <div className="risk-label">{riskValue > 50 ? 'High' : riskValue > 20 ? 'Med' : 'Low'}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;

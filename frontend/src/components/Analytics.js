import React, { useEffect, useState } from 'react';
import apiClient from '../utils/api';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Bar, Line } from 'react-chartjs-2';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

function Analytics() {
  const [analytics, setAnalytics] = useState(null);
  const [velocityData, setVelocityData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    try {
      const data = await apiClient.getAnalytics();
      const velocity = await apiClient.request('/analytics/velocity'); // Fetch velocity trends separately
      
      setAnalytics(data);
      setVelocityData(velocity.data);
    } catch (error) {
      console.error('Failed to load analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="analytics">Loading analytics data...</div>;
  }

  if (!analytics) {
    return <div className="analytics">Failed to load analytics</div>;
  }

  // Velocity Trends Chart Data
  const velocityChartData = {
    labels: velocityData?.map(d => d.sprint) || [],
    datasets: [
      {
        label: 'Story Points',
        data: velocityData?.map(d => d.points) || [],
        backgroundColor: 'rgba(59, 130, 246, 0.6)',
        borderColor: 'rgb(59, 130, 246)',
        borderWidth: 1,
      },
    ],
  };

  // Burndown Chart Data
  const burndownChartData = {
    labels: Array.from({ length: 11 }, (_, i) => `Day ${i}`),
    datasets: [
      {
        label: 'Ideal Burndown',
        data: analytics.burndown.ideal,
        borderColor: 'rgba(156, 163, 175, 0.5)',
        borderDash: [5, 5],
        fill: false,
        tension: 0.1,
      },
      {
        label: 'Actual Progress',
        data: analytics.burndown.actual,
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        fill: true,
        tension: 0.3,
      },
    ],
  };

  const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
      },
    },
  };

  return (
    <div className="analytics">
      <div className="analytics-header">
        <h2>Performance Analytics</h2>
      </div>

      <div className="charts-grid-main">
        <div className="chart-wrapper main-chart">
          <h3>Velocity Trends</h3>
          <div className="chart-container">
            <Bar data={velocityChartData} options={commonOptions} />
          </div>
        </div>

        <div className="metrics-side-grid">
          <div className="metric-card-small">
            <h4>Current Velocity</h4>
            <p className="value">{analytics.velocity.current}</p>
            <span className={`trend ${analytics.velocity.trend}`}>
              {analytics.velocity.trend === 'up' ? '↗' : '↘'} vs average
            </span>
          </div>
          <div className="metric-card-small">
            <h4>Avg Completion</h4>
            <p className="value">{analytics.completion_time.average_days}d</p>
          </div>
        </div>
      </div>

      <div className="charts-sub-grid">
        <div className="chart-wrapper">
          <h3>Historical Burndown</h3>
          <div className="chart-container">
            <Line data={burndownChartData} options={commonOptions} />
          </div>
        </div>

        <div className="chart-wrapper">
          <h3>AI Decision Insights</h3>
          <div className="recommendations-list">
            {analytics.recommendations?.recommendations?.map((rec, index) => (
              <div key={index} className="ai-rec-card">
                <div className="rec-header">
                  <span className="rec-type">{rec.type.replace('_', ' ')}</span>
                  <span className="confidence">{Math.round(rec.confidence * 100)}% Match</span>
                </div>
                <h4>{rec.title}</h4>
                <p>{rec.description}</p>
              </div>
            )) || <p>Generating insights...</p>}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Analytics;

import React from 'react';

function SprintBoard() {
  return (
    <div className="sprint-board">
      <div className="sprint-header">
        <h2>Current Sprint</h2>
        <button className="btn-primary">Complete Sprint</button>
      </div>

      <div className="kanban-board">
        <div className="kanban-column">
          <h3>To Do</h3>
          <div className="task-list">
            <div className="task-card">
              <div className="task-header">
                <h4>Implement OAuth Login</h4>
                <div className="task-actions">
                  <button className="btn-icon edit">Edit</button>
                  <button className="btn-icon delete">Delete</button>
                </div>
              </div>
              <div className="task-tags">
                <span className="tag priority high">High Priority</span>
                <span className="tag points">5 points</span>
                <span className="tag type">FE Dev</span>
              </div>
              <div className="task-assignee">
                <span className="avatar">A</span>
                <span>Alice</span>
              </div>
            </div>
            {/* More tasks */}
          </div>
          <button className="btn-secondary">Add Task</button>
        </div>

        <div className="kanban-column">
          <h3>In Progress</h3>
          <div className="task-list">
            <div className="task-card">
              <div className="task-header">
                <h4>Dashboard UI Redesign</h4>
                <div className="task-actions">
                  <button className="btn-icon edit">Edit</button>
                  <button className="btn-icon delete">Delete</button>
                </div>
              </div>
              <div className="task-tags">
                <span className="tag priority medium">Medium Priority</span>
                <span className="tag points">8 points</span>
              </div>
              <div className="task-assignee">
                <span className="avatar">B</span>
                <span>Bob</span>
              </div>
            </div>
            {/* More tasks */}
          </div>
          <button className="btn-secondary">Add Task</button>
        </div>

        <div className="kanban-column">
          <h3>Done</h3>
          <div className="task-list">
            <div className="task-card">
              <div className="task-header">
                <h4>API Rate Limiter</h4>
                <div className="task-actions">
                  <button className="btn-icon edit">Edit</button>
                  <button className="btn-icon delete">Delete</button>
                </div>
              </div>
              <div className="task-tags">
                <span className="tag status completed">Completed</span>
                <span className="tag points">3 points</span>
              </div>
              <div className="task-assignee">
                <span className="avatar">C</span>
                <span>Charlie</span>
              </div>
            </div>
            {/* More tasks */}
          </div>
          <button className="btn-secondary">Add Task</button>
        </div>
      </div>

      <div className="sprint-goals">
        <h3>Sprint Goals</h3>
        <ul>
          <li><input type="checkbox" checked /> Implement core authentication flow</li>
          <li><input type="checkbox" /> Redesign dashboard UI</li>
          <li><input type="checkbox" /> Improve API performance</li>
        </ul>
        <button className="btn-secondary">Add Goal</button>
      </div>
    </div>
  );
}

export default SprintBoard;

import React from 'react';

function Backlog() {
  return (
    <div className="backlog">
      <div className="backlog-header">
        <h2>Product Backlog</h2>
        <div className="actions">
          <button className="btn-secondary">Add User Story</button>
          <button className="btn-primary">AI Prioritize</button>
        </div>
      </div>

      <div className="backlog-table">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Story</th>
              <th>Priority</th>
              <th>Story Points</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>US-101</td>
              <td>As a user, I want to log in using Google account</td>
              <td><span className="priority high">High</span></td>
              <td>5</td>
              <td>
                <button className="btn-icon edit">Edit</button>
                <button className="btn-icon delete">Delete</button>
              </td>
            </tr>
            {/* More rows */}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Backlog;

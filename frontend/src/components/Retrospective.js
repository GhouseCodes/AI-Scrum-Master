import React from 'react';

function Retrospective() {
  return (
    <div className="retrospective">
      <h2>Sprint Retrospective</h2>

      <div className="retro-columns">
        <div className="retro-column went-well">
          <h3>What Went Well</h3>
          <ul>
            <li>Completed authentication ahead of schedule</li>
            {/* More items */}
          </ul>
          <button className="btn-secondary">Add Item</button>
        </div>

        <div className="retro-column could-improve">
          <h3>What Could Improve</h3>
          <ul>
            <li>API rate limiting blocked progress</li>
            {/* More items */}
          </ul>
          <button className="btn-secondary">Add Item</button>
        </div>

        <div className="retro-column action-items">
          <h3>Action Items</h3>
          <ul>
            <li>Request higher API rate limits</li>
            {/* More items */}
          </ul>
          <button className="btn-secondary">Add Item</button>
        </div>
      </div>

      <div className="chart-card">
        <h3>Sentiment Analysis</h3>
        <canvas id="sentiment-chart"></canvas>
      </div>
    </div>
  );
}

export default Retrospective;

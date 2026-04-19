// API utility functions for communicating with the backend

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

class ApiClient {
  constructor(baseURL) {
    this.baseURL = baseURL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Sprint endpoints
  async getSprints() {
    return this.request('/sprints');
  }

  async getSprint(id) {
    return this.request(`/sprints/${id}`);
  }

  async createSprint(sprintData) {
    return this.request('/sprints', {
      method: 'POST',
      body: JSON.stringify(sprintData),
    });
  }

  async updateSprint(id, sprintData) {
    return this.request(`/sprints/${id}`, {
      method: 'PUT',
      body: JSON.stringify(sprintData),
    });
  }

  // Backlog endpoints
  async getBacklog() {
    return this.request('/backlog');
  }

  async createUserStory(storyData) {
    return this.request('/backlog', {
      method: 'POST',
      body: JSON.stringify(storyData),
    });
  }

  async updateUserStory(id, storyData) {
    return this.request(`/backlog/${id}`, {
      method: 'PUT',
      body: JSON.stringify(storyData),
    });
  }

  async deleteUserStory(id) {
    return this.request(`/backlog/${id}`, {
      method: 'DELETE',
    });
  }

  // Analytics endpoints
  async getAnalytics() {
    return this.request('/analytics');
  }

  async getSprintAnalytics(sprintId) {
    return this.request(`/analytics/sprint/${sprintId}`);
  }

  // AI endpoints
  async generateInsights(data) {
    return this.request('/ai/insights', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async analyzeSentiment(text) {
    return this.request('/ai/sentiment', {
      method: 'POST',
      body: JSON.stringify({ text }),
    });
  }

  async detectBlockers(data) {
    return this.request('/ai/blockers', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async processVoiceInput(audioData) {
    return this.request('/ai/voice', {
      method: 'POST',
      body: JSON.stringify({ audio: audioData }),
    });
  }
}

const apiClient = new ApiClient(API_BASE_URL);

export default apiClient;

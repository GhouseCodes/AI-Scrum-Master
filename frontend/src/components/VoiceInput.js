import React, { useState, useRef } from 'react';
import apiClient from '../utils/api';

function VoiceInput() {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const recognitionRef = useRef(null);

  const startRecording = () => {
    if (!('webkitSpeechRecognition' in window)) {
      alert('Speech recognition not supported in this browser.');
      return;
    }

    const recognition = new window.webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
      setIsRecording(true);
    };

    recognition.onresult = (event) => {
      const result = event.results[0][0].transcript;
      setTranscript(result);
      // Send to AI service for processing
      processVoiceInput(result);
    };

    recognition.onend = () => {
      setIsRecording(false);
    };

    recognitionRef.current = recognition;
    recognition.start();
  };

  const stopRecording = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
  };

  const processVoiceInput = async (text) => {
    // Call AI service to process voice input
    console.log('Processing voice input:', text);
    try {
      const result = await apiClient.processVoiceInput(text);
      console.log('AI processing result:', result);
      // You could update some global state or display a summary here
      if (result.summary) {
        setTranscript(prev => `${prev} [AI: ${result.summary}]`);
      }
    } catch (error) {
      console.error('Failed to process voice input:', error);
    }
  };

  return (
    <div className="voice-input">
      <button
        className={`voice-btn ${isRecording ? 'recording' : ''}`}
        onClick={isRecording ? stopRecording : startRecording}
      >
        <i className="fas fa-microphone"></i>
        {isRecording ? 'Stop Recording' : 'Voice Input'}
      </button>
      {transcript && (
        <div className="transcript">
          <p>You said: {transcript}</p>
        </div>
      )}
    </div>
  );
}

export default VoiceInput;

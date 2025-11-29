import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const MicroLearning = () => {
  const [lessons, setLessons] = useState([]);
  const [selectedLesson, setSelectedLesson] = useState(null);
  const [completedLessons, setCompletedLessons] = useState([]);
  const [filter, setFilter] = useState('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLessons();
    loadCompletedLessons();
  }, []);

  const loadLessons = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/mentor/lessons/list`);
      setLessons(response.data.lessons || []);
    } catch (error) {
      console.error('Failed to load lessons:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadCompletedLessons = () => {
    const completed = JSON.parse(localStorage.getItem('completed_lessons') || '[]');
    setCompletedLessons(completed);
  };

  const handleStartLesson = async (lessonId) => {
    try {
      const response = await axios.get(`${API_URL}/api/mentor/lesson/${lessonId}`);
      setSelectedLesson(response.data);
    } catch (error) {
      console.error('Failed to load lesson:', error);
    }
  };

  const handleCompleteLesson = (lessonId) => {
    const newCompleted = [...completedLessons, lessonId];
    setCompletedLessons(newCompleted);
    localStorage.setItem('completed_lessons', JSON.stringify(newCompleted));
    setSelectedLesson(null);
  };

  const filteredLessons = filter === 'all' 
    ? lessons 
    : lessons.filter(l => l.category === filter);

  if (selectedLesson) {
    return (
      <div className="min-h-screen bg-neutral-50 p-6">
        <div className="max-w-3xl mx-auto">
          <button
            onClick={() => setSelectedLesson(null)}
            className="mb-4 text-primary-600 hover:text-primary-700 font-medium"
          >
            ← Back to Lessons
          </button>
          
          <div className="bg-white rounded-lg p-8 border shadow-sm">
            <h1 className="text-3xl font-bold mb-6 text-neutral-900">{selectedLesson.title}</h1>
            <div 
              className="prose max-w-none"
              dangerouslySetInnerHTML={{ __html: selectedLesson.html }}
            />
            
            <button
              onClick={() => handleCompleteLesson(selectedLesson.id)}
              className="mt-8 w-full px-6 py-3 bg-secondary-600 text-white rounded-lg hover:bg-secondary-700 font-medium"
            >
              Mark as Complete ✓
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-neutral-50 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-neutral-900">Micro-Learning Center</h1>
          <div className="text-sm text-neutral-600">
            {completedLessons.length}/{lessons.length} lessons completed
          </div>
        </div>
        
        {/* Category Filter */}
        <div className="flex gap-2 mb-6">
          {['all', 'savings', 'debt', 'credit'].map(cat => (
            <button
              key={cat}
              onClick={() => setFilter(cat)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                filter === cat 
                  ? 'bg-primary-600 text-white' 
                  : 'bg-white text-neutral-700 border border-neutral-300 hover:border-primary-300'
              }`}
            >
              {cat.charAt(0).toUpperCase() + cat.slice(1)}
            </button>
          ))}
        </div>
        
        {loading ? (
          <div className="text-center py-12 text-neutral-500">Loading lessons...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredLessons.map(lesson => {
              const isCompleted = completedLessons.includes(lesson.id);
              return (
                <div 
                  key={lesson.id} 
                  className="bg-white rounded-lg p-6 border shadow-sm hover:shadow-md transition-shadow"
                  data-testid={`lesson-${lesson.id}`}
                >
                  <div className="flex items-start justify-between mb-3">
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      lesson.category === 'credit' ? 'bg-blue-100 text-blue-700' :
                      lesson.category === 'debt' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-green-100 text-green-700'
                    }`}>
                      {lesson.category}
                    </span>
                    {isCompleted && (
                      <span className="text-secondary-600 font-bold text-lg">✓</span>
                    )}
                  </div>
                  
                  <h3 className="font-semibold text-lg mb-2 text-neutral-900">{lesson.title}</h3>
                  <p className="text-sm text-neutral-600 mb-4">{lesson.duration_min} minutes</p>
                  
                  <button 
                    onClick={() => handleStartLesson(lesson.id)}
                    className={`w-full px-4 py-2 rounded font-medium transition-colors ${
                      isCompleted
                        ? 'bg-neutral-100 text-neutral-600 hover:bg-neutral-200'
                        : 'bg-primary-600 text-white hover:bg-primary-700'
                    }`}
                    data-testid={`start-lesson-${lesson.id}`}
                  >
                    {isCompleted ? 'Review' : 'Start Lesson'}
                  </button>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};

export default MicroLearning;

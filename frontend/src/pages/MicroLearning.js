import React from 'react';

const MicroLearning = () => {
  const lessons = [
    { id: 1, title: 'Emergency Fund Basics', completed: false, time: 5 },
    { id: 2, title: 'Your Rights Under FDCPA', completed: false, time: 3 },
    { id: 3, title: 'Debt Validation Process', completed: false, time: 7 }
  ];

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Micro-Learning</h1>
        
        <div className="space-y-4">
          {lessons.map(lesson => (
            <div key={lesson.id} className="bg-white rounded-lg p-6 border" data-testid={`lesson-${lesson.id}`}>
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold text-lg">{lesson.title}</h3>
                  <p className="text-sm text-neutral-600">{lesson.time} minutes</p>
                </div>
                <button className="px-4 py-2 bg-primary-600 text-white rounded" data-testid={`start-lesson-${lesson.id}`}>
                  Start
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default MicroLearning;

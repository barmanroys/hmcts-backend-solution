CREATE TABLE IF NOT EXISTS db.tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(60) NOT NULL,
    description VARCHAR(500) NULL,
    status ENUM('PENDING', 'WIP', 'DONE') NOT NULL,
    due DATETIME NOT NULL,
    updated_on DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL, -- Update on any upsert
    INDEX (id)
);

INSERT INTO db.tasks (title, description, status, due) VALUES
('Server Log', 'Complete the review of server logs for anomalies.', 'PENDING', '2025-05-01 10:00:00'),
('Code', 'Review the code for the new user authentication feature.', 'WIP', '2025-05-02 12:00:00'),
('Project Report', 'Finalize and submit the project report to management.', 'DONE', '2025-04-25 09:00:00'),
('Bug Fixing', 'Address critical bugs identified in the last sprint.', 'WIP', '2025-05-03 15:00:00'),
('Documentation', 'Update user documentation to reflect recent changes.', 'PENDING', '2025-05-05 08:30:00'),
('Appraisal', 'Conduct performance reviews for team members.', 'DONE', '2025-04-28 14:00:00'),
('UI', 'Design the new user interface for the application.', 'PENDING', '2025-05-04 11:00:00'),
('API', 'Implement new API endpoints as per specifications.', 'WIP', '2025-05-06 13:00:00'),
('Testing', 'Test the latest software build for quality assurance.', 'PENDING', '2025-04-29 16:00:00'),
('Marketing', 'Plan the marketing strategy for the upcoming product launch.', 'DONE', '2025-04-20 10:00:00'),
('Development Setup', 'Setup the development environment for new developers.', 'WIP', '2025-05-07 10:00:00'),
('Requirement Gathering', 'Gather requirements for the new project from stakeholders.', 'PENDING', '2025-05-08 12:00:00'),
('Server Issue Check', 'Check the server logs for any ongoing issues.', 'DONE', '2025-04-30 09:00:00'),
('Team-Building', 'Organize the logistics for the upcoming team-building event.', 'PENDING', '2025-05-09 15:00:00'),
('Design Mockup', 'Review the latest design mockups for feedback.', 'WIP', '2025-05-10 14:00:00');
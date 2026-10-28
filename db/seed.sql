INSERT INTO users (id, email, full_name, password_hash, role, phone, address, bio) VALUES
(1, 'admin@dat250.local', 'System Administrator', '3b612c75a7b5048a435fb6ec81e52ff92d6d795a8b5a9c17070f6a63c97a53b2', 'admin', '+47 10001000', 'UiS Campus', 'Responsible for lab operations.'),
(2, 'teacher@dat250.local', 'Course Teacher', '54a8ca277e41818ee3f18340ad8303bc772cdcb612ca85c60852cd66beb06fe2', 'teacher', '+47 10001001', 'UiS Campus', 'Lecturer in secure software development.'),
(3, 'ta@dat250.local', 'Teaching Assistant', '5d2fd7d3b1cef148364cf49f8c99a03de74c0419cf80362cd6b433f3d1c4c241', 'ta', '+47 10001002', 'Stavanger', 'Supports grading and feedback.'),
(4, 'alice@student.uis.no', 'Alice Nilsen', '6766ad37ada06ddc90f432f8d915f991dd0ec6559bfd8d400b380e4aef4e3ac1', 'student', '+47 40001004', 'Stavanger', 'Interested in web security.'),
(5, 'bob@student.uis.no', 'Bob Hansen', 'da43fa45e1bb5c63a31422b2c037a7821c838c31b0bb6072d04031b73636d85b', 'student', '+47 40001005', 'Sandnes', 'Likes backend development.'),
(6, 'charlie@student.uis.no', 'Charlie Berg', 'f59c8846af83a901e50b706c164d53cdebc8617cddd538b5a49e4a1d5ac99674', 'student', '+47 40001006', 'Stavanger', 'Works on secure coding exercises.')
ON CONFLICT (id) DO NOTHING;

INSERT INTO courses (id, title, description) VALUES
(1, 'DAT250 Information and Software Security', 'Core course on practical software security.'),
(2, 'DAT220 Database Systems', 'Relational design, SQL, and transactions.'),
(3, 'DAT505 Ethical Hacking', 'Applied penetration testing and legal boundaries.'),
(4, 'DAT945 Secure and Robust AI', 'Security and robustness for AI systems.')
ON CONFLICT (id) DO NOTHING;

INSERT INTO project_groups (course_id, group_name, max_members) VALUES
(1, 'Blue Team', 4),
(1, 'Green Team', 4),
(2, 'DB Masters', 4),
(3, 'Pentest Pioneers', 4),
(4, 'AI Shield', 4);

INSERT INTO course_registrations (user_id, course_id, project_group) VALUES
(4, 1, 'Blue Team'),
(5, 1, 'Blue Team'),
(6, 1, 'Green Team'),
(4, 2, 'DB Masters'),
(5, 3, 'Pentest Pioneers');

INSERT INTO assignments (id, course_id, title, description, deadline) VALUES
(1, 1, 'Assignment 1: OWASP Testing Guide Report', 'Prepare a test plan and findings report.', NOW() + INTERVAL '7 day'),
(2, 1, 'Assignment 2: Broken Authentication and Access Control', 'Evaluate auth/session/access controls.', NOW() + INTERVAL '14 day'),
(3, 1, 'Assignment 3: Cryptography in Software', 'Analyze secrets, hashing, reset tokens.', NOW() + INTERVAL '21 day'),
(4, 1, 'Assignment 4: Secure Coding Practices', 'Patch vulnerable code and retest.', NOW() + INTERVAL '28 day')
ON CONFLICT (id) DO NOTHING;

INSERT INTO submissions (assignment_id, user_id, filename, file_path, notes) VALUES
(1, 4, 'owasp_report_alice.pdf', '4_1_owasp_report_alice.pdf', 'Initial report draft'),
(1, 5, 'owasp_report_bob.pdf', '5_1_owasp_report_bob.pdf', 'Draft'),
(2, 6, 'auth_notes_charlie.docx', '6_2_auth_notes_charlie.docx', 'Access control notes');

INSERT INTO grades (assignment_id, student_id, grader_id, grade_value, feedback, status) VALUES
(1, 4, 2, 'B+', 'Good structure, include more trace evidence.', 'published'),
(1, 5, 2, 'B', 'Solid analysis, improve remediation details.', 'published'),
(2, 6, 3, 'A-', 'Strong coverage of session handling.', 'published');

INSERT INTO messages (sender_id, recipient_id, content) VALUES
(2, 4, 'Please remember to include screenshots in your report.'),
(3, 5, 'Feedback session is available tomorrow.'),
(4, 5, 'Can we pair on Assignment 3?');

INSERT INTO course_comments (course_id, user_id, content) VALUES
(1, 4, 'The OWASP checklist is very helpful this week.'),
(1, 5, 'Can we get clarification on token handling?'),
(2, 6, 'DB isolation examples were clear.');

INSERT INTO password_reset_tokens (user_id, token) VALUES
(4, '123456'),
(5, '123456');

INSERT INTO app_settings (setting_key, setting_value) VALUES
('portal_theme', 'uis-light'),
('semester', 'Spring 2026'),
('allow_self_registration', 'true')
ON CONFLICT (setting_key) DO NOTHING;

INSERT INTO audit_logs (actor_user_id, action, details) VALUES
(1, 'seed', 'Initial seed data imported'),
(2, 'grade_publish', 'Published grades for assignment 1'),
(3, 'message_send', 'Sent onboarding messages');

SELECT setval(pg_get_serial_sequence('users','id'), (SELECT MAX(id) FROM users));
SELECT setval(pg_get_serial_sequence('courses','id'), (SELECT MAX(id) FROM courses));
SELECT setval(pg_get_serial_sequence('assignments','id'), (SELECT MAX(id) FROM assignments));
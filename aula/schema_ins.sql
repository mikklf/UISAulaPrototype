TRUNCATE users, groups, threads, messages, posts, users_groups, users_threads;

INSERT INTO public.users(user_id, first_name, last_name, password, email, address, role) VALUES 
    (5000, 'Gordon', 'Freeman', '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'test@test.dk', 'aud Auditorium A, bygning 1, 1. sal Universitetsparken 15 (Zoo)', 'teacher'),
    (5001, 'Rachel', 'Green', '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'rachel@test.dk', 'Cnetral Park', 'parent'),
    (5002,'Joey', 'Trib', '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'joey@test.dk', 'New York', 'student'),
    (5003,'Chandler', 'Bing', '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'Chandler@test.dk', 'Central Park', 'student'),
    (5004,'Phoebe', 'Buffay', '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'Phoebe@test.dk', 'Central Perk', 'parent'),
    (5005,'Ross', 'Geller', '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'Ross@test.dk', 'Central Perk', 'student');

INSERT INTO public.groups(group_id, name, leaveable, parents_can_post) VALUES 
    (1000, 'fodbold', TRUE, TRUE), 
    (1001,'3a', FALSE, TRUE);

INSERT INTO users_groups (user_id, group_id) VALUES (5000, 1000), (5000, 1001);

INSERT INTO threads(thread_id ,title, group_id, creator_id) VALUES 
    (2000, 'Anbefalinger til fodboldsko?', 1000, 5000);

INSERT INTO messages (message_id, content, thread_id, author_id) VALUES (4000,'Eleverne har ondt i fødderne når de spiller fodbild. Hvem kender et godt skomærke?', 2000, 5000);

INSERT INTO users_threads (user_id, thread_id) VALUES (5000, 4000);

INSERT INTO posts (post_id, group_id, author_id, title, content) VALUES (6000, 1000, 5001, 'Fodbold på torsdag', 'HUSK BOLDEN DENNE GANG!!');
                                                                            
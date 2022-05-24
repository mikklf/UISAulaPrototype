DELETE FROM users;
DELETE FROM groups;
DELETE FROM messages;
DELETE FROM threads;
DELETE FROM posts;
DELETE FROM users_threads;
DELETE FROM users_groups;

INSERT INTO public.users(first_name, last_name, password, email, adresse, role) VALUES (Gordon, Freeman, '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'test@test.dk', 'aud Auditorium A, bygning 1, 1. sal Universitetsparken 15 (Zoo)', 'teacher');
INSERT INTO public.users(first_name, last_name, password, email, adresse, role) VALUES (Rachel, Green, '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'rachel@test.dk', 'Cnetral Park', 'parent');
INSERT INTO public.users(first_name, last_name, password, email, adresse, role) VALUES (Joey, Trib, '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'joey@test.dk', 'New York', 'student');
INSERT INTO public.users(first_name, last_name, password, email, adresse, role) VALUES (Chandler, Bing, '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'Chandler@test.dk', 'Central Park', 'student');
INSERT INTO public.users(first_name, last_name, password, email, adresse, role) VALUES (Phoebe, Buffay, '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'Phoebe@test.dk', 'Central Perk', 'parent');
INSERT INTO public.users(first_name, last_name, password, email, adresse, role) VALUES (Ross, Geller, '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'Ross@test.dk', 'Central Perk', 'student');

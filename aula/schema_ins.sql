TRUNCATE users, groups, threads, messages, posts, users_groups, users_threads;

INSERT INTO public.users(user_id, first_name, last_name, password, email, address, role) VALUES 
    (5000, 'Gordon', 'Freeman', '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'gordon@test.dk', 'Black Mesa', 'teacher'),
    (5001, 'Rachel', 'Green', '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'rachel@test.dk', 'Cnetral Park', 'parent'),
    (5002,'Joey', 'Trib', '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'joey@test.dk', 'New York', 'student'),
    (5003,'Chandler', 'Bing', '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'chandler@test.dk', 'Central Park', 'student'),
    (5004,'Phoebe', 'Buffay', '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'phoebe@test.dk', 'Central Perk', 'parent'),
    (5005,'Ross', 'Geller', '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'ross@test.dk', 'Central Perk', 'student');

INSERT INTO public.groups(group_id, name, hidden) VALUES 
    (1000, 'fodbold', TRUE), 
    (1001,'3a', FALSE);

INSERT INTO users_groups (user_id, group_id) VALUES (5000, 1000), (5001, 1001);

INSERT INTO threads(thread_id ,title, group_id) VALUES
    (2000, 'Anbefalinger til fodboldsko?', 1000);

INSERT INTO messages (content, thread_id, author_id, created_date) VALUES
    ('Eleverne har ondt i fødderne når de spiller fodbild. Hvem kender et godt skomærke?', 2000, 5000, NOW() - INTERVAL '3.189 day'),
    ('Jeg tror min søn har nogle han er glad for. Jeg spørger ham lige 😀', 2000, 5002, NOW() - INTERVAL '2.951 day'),
    ('Tak 👍', 2000, 5000, NOW() - INTERVAL '1.894 day'),
    ('Er det meningen vi skal give dem sko med????', 2000, 5001, NOW() - INTERVAL '1.05 hour'),
    ('Rachel, giver du ikke dine børn sko med til fodbold?', 2000, 5002, NOW() - INTERVAL '0.95 hour'),
    ('Hvad er der galt med dig?', 2000, 5003, NOW() - INTERVAL '0.94 hour'),
    ('Jeg troede de lånte sko af skolen!', 2000, 5001, NOW() - INTERVAL '0.91 hour'),
    ('Er det noget der nogensinde sket?', 2000, 5003, NOW() - INTERVAL '0.908 hour'),
    ('Kan vi ikke godt komme tilbage til pointen?', 2000, 5000, NOW() - INTERVAL '0.9 hour'),
    ('Hvorfor er det ligepludselig mig der skal holde styr på om skolen uddeler sko eller ej?', 2000, 5001, NOW() - INTERVAL '0.898 hour'),
    ('Fordi du er dit barns mor?', 2000, 5003, NOW() - INTERVAL '0.89 hour');

INSERT INTO users_threads (user_id, thread_id) VALUES
    (5000, 2000),
    (5001, 2000),
    (5002, 2000),
    (5003, 2000);

INSERT INTO posts (post_id, group_id, author_id, title, content) VALUES (6000, 1000, 5001, 'Fodbold på torsdag', 'HUSK BOLDEN DENNE GANG!!');

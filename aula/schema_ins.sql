TRUNCATE users, groups, threads, messages, posts, users_in_groups;

INSERT INTO public.users(cpr_num, first_name, last_name, password, role) VALUES 
    (5000, 'Gordon', 'Freeman', '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'teacher'),
    (5001, 'Rachel', 'Green', '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'parent'),
    (5002,'Joey', 'Trib', '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'parent'),
    (5003,'Chandler', 'Bing', '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'parent'),
    (5004,'Phoebe', 'Buffay', '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'parent'),
    (5005,'Ross', 'Geller', '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'parent');

INSERT INTO public.groups(group_id, name, mandatory) VALUES 
    (1000, 'fodbold', TRUE), 
    (1001,'3a', FALSE);

INSERT INTO users_in_groups (cpr_num, group_id) VALUES (5000, 1000), (5001, 1001);

INSERT INTO threads(thread_id ,title, group_id) VALUES
    (2000, 'Anbefalinger til fodboldsko?', 1000);

INSERT INTO messages (content, thread_id, author_cpr_num, created_date) VALUES
    ('Eleverne har ondt i fødderne når de spiller fodbild. Hvem kender et godt skomærke?', 2000, 5000, NOW() - INTERVAL '3.189 day'),
    ('Jeg tror min søn har nogle han er glad for. Jeg spørger ham lige', 2000, 5002, NOW() - INTERVAL '2.951 day'),
    ('Tak', 2000, 5000, NOW() - INTERVAL '1.894 day'),
    ('Er det meningen vi skal give dem sko med????', 2000, 5001, NOW() - INTERVAL '1.05 hour'),
    ('Rachel, giver du ikke dine børn sko med til fodbold?', 2000, 5002, NOW() - INTERVAL '0.95 hour'),
    ('Hvad er der galt med dig?', 2000, 5003, NOW() - INTERVAL '0.94 hour'),
    ('Jeg troede de lånte sko af skolen!', 2000, 5001, NOW() - INTERVAL '0.91 hour'),
    ('Er det noget der nogensinde sket?', 2000, 5003, NOW() - INTERVAL '0.908 hour'),
    ('Kan vi ikke godt komme tilbage til pointen?', 2000, 5000, NOW() - INTERVAL '0.9 hour'),
    ('Hvorfor er det ligepludselig mig der skal holde styr på om skolen uddeler sko eller ej?', 2000, 5001, NOW() - INTERVAL '0.898 hour'),
    ('Fordi du er dit barns mor?', 2000, 5003, NOW() - INTERVAL '0.89 hour');

INSERT INTO posts (post_id, group_id, author_cpr_num, title, content) VALUES (6000, 1000, 5001, 'Fodbold på torsdag', 'HUSK BOLDEN DENNE GANG!!');

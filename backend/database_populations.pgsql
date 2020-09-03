-- add some categories
insert into categories (type) values ('science'), ('history'), ('sports');
-- add some questions of different categories
insert into questions (question, answer, category, difficulty) VALUES
('how old is the earth?', '4 billion years', 1, 3), ('who killed ali the great of egypt?','abu_dahb',2,3), ('4*4=','16',3,1);

-- 
update categories set svg = 'http://127.0.0.1:5000/images/sunset.jpg';
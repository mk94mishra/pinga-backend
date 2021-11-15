sql
---


#1 user
CREATE TABLE "user"(
id BIGSERIAL PRIMARY KEY NOT NULL,
created_at TIMESTAMPTZ NOT NULL DEFAULT Now(),
is_active BOOLEAN NOT NULL DEFAULT true,

created_by bigint NOT NULL,

type VARCHAR (100) NOT NULL,
mobile VARCHAR (10) UNIQUE NOT NULL,
password VARCHAR (50) NOT NULL,

name VARCHAR(50),
email VARCHAR (100) UNIQUE,
gender VARCHAR(50),
dob date,
profile_pic_url VARCHAR (500),
tnc_accepted boolean,

data jsonb
);


#2 post
CREATE TABLE post(
id BIGSERIAL PRIMARY KEY NOT NULL,
created_at TIMESTAMPTZ NOT NULL DEFAULT Now(),
is_active BOOLEAN NOT NULL DEFAULT true,

created_by_id bigint REFERENCES "user" NOT NULL,

description VARCHAR (1000),
link_url VARCHAR (1000),
media_type VARCHAR (10),
media_thumbnail_url VARCHAR (500),
media_url VARCHAR (500),

like_count bigint default 0,

data jsonb
);

#post_master
create view post_master as (
select p.*,
u.name as created_by_name,u.mobile as created_by_mobile,u.type as created_by_user_type,u.profile_pic_url as created_by_profile_pic_url
from post as p
left join "user" as u
on p.created_by_id=u.id
order by p.id desc
);

# blog
CREATE TABLE blog(
id BIGSERIAL PRIMARY KEY NOT NULL,
created_at TIMESTAMPTZ NOT NULL DEFAULT Now(),
is_active BOOLEAN NOT NULL DEFAULT true,

created_by_id bigint REFERENCES "user" NOT NULL,
title VARCHAR (500),
link_url VARCHAR (1000),
media_type VARCHAR (10),
media_thumbnail_url VARCHAR (500),
media_url VARCHAR (500),
type VARCHAR (50),
day bigint,

data jsonb
);


#3 mood
CREATE TABLE mood(
id BIGSERIAL PRIMARY KEY NOT NULL,
created_at TIMESTAMPTZ NOT NULL DEFAULT Now(),
is_active BOOLEAN NOT NULL DEFAULT true,

created_by_id bigint REFERENCES "user" NOT NULL,

type VARCHAR(10) NOT NULL,

data jsonb

);


#4 task
CREATE TABLE task(
id BIGSERIAL PRIMARY KEY NOT NULL,
created_at TIMESTAMPTZ NOT NULL DEFAULT Now(),
is_active BOOLEAN NOT NULL DEFAULT true,

created_by_id bigint REFERENCES "user" NOT NULL,

assigned_to_id bigint REFERENCES "user" NOT NULL,

title VARCHAR (100) NOT NULL,
description TEXT[] NOT NULL,
status VARCHAR (10) NOT NULL,

data jsonb

);

#task:master
create view task_master as (
select t.*,
u1.name as created_by_name,u1.mobile as created_by_mobile,u1.profile_pic_url as created_by_profile_pic_url,
u2.name as assigned_to_name,u2.mobile as assigned_to_mobile,u2.profile_pic_url as assigned_to_profile_pic_url
from task as t
left join "user" as u1 on t.created_by_id =u1.id
left join "user" as u2 on t.assigned_to_id=u2.id
order by t.id desc
);



#5 issue
CREATE TABLE issue (
id BIGSERIAL PRIMARY KEY NOT NULL,
created_at TIMESTAMPTZ NOT NULL DEFAULT Now(),
is_active BOOLEAN NOT NULL DEFAULT true,

created_by_id bigint REFERENCES "user" NOT NULL,

description VARCHAR (500) NOT NULL,
media_url VARCHAR (500),
status VARCHAR (10) NOT NULL,

data jsonb
);

#issue master
create view issue_master as (
select i.*,
u.name as created_by_name,u.mobile as created_by_mobile,u.type as created_by_user_type,u.profile_pic_url as created_by_profile_pic_url
from issue as i
left join "user" as u
on i.created_by_id=u.id
order by i.id desc
);


#6 extra
CREATE TABLE extra (
id BIGSERIAL PRIMARY KEY NOT NULL,
created_at TIMESTAMPTZ NOT NULL DEFAULT Now(),
is_active BOOLEAN NOT NULL DEFAULT true,

created_by_id bigint REFERENCES "user" NOT NULL,

type VARCHAR (20),

data jsonb
);


#6 address
CREATE TABLE address (
id BIGSERIAL PRIMARY KEY NOT NULL,
created_at TIMESTAMPTZ NOT NULL DEFAULT Now(),
is_active BOOLEAN NOT NULL DEFAULT true,

name  VARCHAR (100),
parent_address_id bigint REFERENCES "address",
 
type VARCHAR (20),

data jsonb
);



#7 stock
CREATE TABLE stock (
id BIGSERIAL PRIMARY KEY NOT NULL,
created_at TIMESTAMPTZ NOT NULL DEFAULT Now(),
is_active BOOLEAN NOT NULL DEFAULT true,

created_by_id bigint REFERENCES "user" NOT NULL,
assigned_to_id bigint REFERENCES "user" NOT NULL,

title VARCHAR (100) NOT NULL,
given INTEGER NOT NULL,
remaining INTEGER NOT NULL,

data jsonb
);

#stock master
create view stock_master as (
select s.*,
u1.name as created_by_name,u1.mobile as created_by_mobile,u1.profile_pic_url as created_by_profile_pic_url,
u2.name as assigned_to_name,u2.mobile as assigned_to_mobile,u2.profile_pic_url as assigned_to_profile_pic_url
from stock as s
left join "user" as u1 on s.created_by_id=u1.id
left join "user" as u2 on s.assigned_to_id=u2.id
order by s.id desc
);

# health
CREATE TABLE health(
id BIGSERIAL PRIMARY KEY NOT NULL,
created_at TIMESTAMPTZ NOT NULL DEFAULT Now(),
is_active BOOLEAN NOT NULL DEFAULT true,

created_by bigint NOT NULL,

type VARCHAR (100) NOT NULL,
start_date date,
end_date date,

data jsonb
);

# form
CREATE TABLE form (
id BIGSERIAL PRIMARY KEY NOT NULL,
created_at TIMESTAMPTZ NOT NULL DEFAULT Now(),
is_active BOOLEAN NOT NULL DEFAULT true,

created_by_id bigint REFERENCES "user" NOT NULL,

title VARCHAR (500) NOT NULL,
description VARCHAR (500),
media_type VARCHAR (10),
media_thumbnail_url VARCHAR (500),
media_url VARCHAR (500),
language VARCHAR (50) NOT NULL,

data jsonb
);


# question
CREATE TABLE question (
id BIGSERIAL PRIMARY KEY NOT NULL,
created_at TIMESTAMPTZ NOT NULL DEFAULT Now(),
is_active BOOLEAN NOT NULL DEFAULT true,

created_by_id bigint REFERENCES "user" NOT NULL,

form_id bigint REFERENCES form NOT NULL,

parent_question_id bigint REFERENCES question,
parent_option_id bigint REFERENCES option,

title VARCHAR (500) NOT NULL,
media_type VARCHAR (20),
media_url VARCHAR (500),
media_thumbnail_url VARCHAR (500),

multiple_choice BOOLEAN,
score INT,
weightage INT,
unique_uuid VARCHAR (100) UNIQUE,
data jsonb
);


# option
CREATE TABLE option (
id BIGSERIAL PRIMARY KEY NOT NULL,
created_at TIMESTAMPTZ NOT NULL DEFAULT Now(),
is_active BOOLEAN NOT NULL DEFAULT true,

created_by_id bigint REFERENCES "user" NOT NULL,

question_id bigint REFERENCES question NOT NULL,

title VARCHAR (500),
weightage int,
media_type VARCHAR (20),
media_url VARCHAR (500),
media_thumbnail_url VARCHAR (500),
data jsonb
);


# answer
CREATE TABLE answer (
id BIGSERIAL PRIMARY KEY NOT NULL,
created_at TIMESTAMPTZ NOT NULL DEFAULT Now(),
is_active BOOLEAN NOT NULL DEFAULT true,

created_by_id bigint REFERENCES "user" NOT NULL,
option_id bigint REFERENCES option NOT NULL,
data jsonb
);



# result view
create view view_result as
with
f as (select * from form),
q as (select * from question where parent_question_id is null and parent_option_id is null),
o as (select * from option)

select a.* ,
f.id as form_id,
q.id as question_id, q.score as score,
o.weightage as weightage,
(q.score*o.weightage) as final
from answer as a
left join o on o.id=a.option_id
left join q on q.id=o.question_id
left join f on f.id=q.form_id
order by a.option_id asc


# question arrange formate
with 
f as (select * from form),
q1 as (select * from question where parent_question_id is null),
q2 as (select q.* from question as q left join q1 on q1.id=q.parent_question_id),
q3 as (select q.* from question as q left join q2 on q2.id=q.parent_question_id),
q4 as (select q.* from question as q left join q3 on q3.id=q.parent_question_id)

select
f.id as form_id ,
q1.id as q1_id, q1.title as q1_title, q1.score as q1_score,
q2.id as q2_id, q2.parent_question_id as q2_pid, q2.title as q2_title, q2.weightage as q2_weightage,
q3.id as q3_id, q3.parent_question_id as q3_pid, q3.title as q3_title, q3.weightage as q3_weightage,
q4.id as q4_id, q4.parent_question_id as q4_pid, q4.title as q4_title, q4.weightage as q4_weightage
from f 
left join q1 on q1.form_id=f.id
left join q2 on q2.parent_question_id=q1.id
left join q3 on q3.parent_question_id=q2.id
left join q4 on q4.parent_question_id=q3.id



# view_question_option
create view view_question_option as
with
q1 as (select q.form_id as form_id, q.id as q1_id ,q.title as q1_title ,q.score as q1_score ,
	o.id as q1_o_id, o.title as q1_o_title,o.weightage as q1_o_weightage
	from question as q 
	left join "option" as  o on o.question_id=q.id
	where q.parent_question_id is null and q.parent_option_id is null),


q2 as (select q1.*, 
	q2.id as q2_id ,q2.title as q2_title,
	o.id as q2_o_id, o.title as q2_o_title,o.weightage as q2_o_weightage
	from q1 
	left join question as q2 on q2.parent_option_id=q1.q1_o_id
	left join "option" as  o on o.question_id=q2.id),
	
q3 as (select q2.*, 
	q3.id as q3_id ,q3.title as q3_title,
	o.id as q3_o_id, o.title as q3_o_title,o.weightage as q3_o_weightage
	from q2 
	left join question as q3 on q3.parent_option_id=q2.q2_o_id
	left join "option" as  o on o.question_id=q3.id),

q4 as (select q3.*, 
	q4.id as q4_id ,q4.title as q4_title,
	o.id as q4_o_id, o.title as q4_o_title,o.weightage as q4_o_weightage
	from q3 
	left join question as q4 on q4.parent_option_id=q3.q3_o_id
	left join "option" as  o on o.question_id=q4.id)
	
select *,
(case when q1_o_weightage is null then 1 else q1_o_weightage end)*
(case when q2_o_weightage is null then 1 else q2_o_weightage end)*
(case when q3_o_weightage is null then 1 else q3_o_weightage end)*
(case when q4_o_weightage is null then 1 else q4_o_weightage end) as total_weightage,
q1_score*
(case when q1_o_weightage is null then 1 else q1_o_weightage end)*
(case when q2_o_weightage is null then 1 else q2_o_weightage end)*
(case when q3_o_weightage is null then 1 else q3_o_weightage end)*
(case when q4_o_weightage is null then 1 else q4_o_weightage end) as final_score

from q4 
order by form_id,q1_id,q1_o_id,q2_o_id,q3_o_id,q4_o_id asc
	



# view_user_answer
create view view_user_answer as
with 
q1 as (select form_id, q1_id,q1_score,q1_o_id as option_id,total_weightage, final_score from view_question_option where q2_id is null and q3_id is null and q4_id is null),
q2 as (select form_id, q1_id,q1_score,q2_o_id as option_id,total_weightage, final_score from view_question_option where q2_id is not null and q3_id is null and q4_id is null),
q3 as (select form_id, q1_id,q1_score,q3_o_id as option_id,total_weightage, final_score from view_question_option where q2_id is not null and q3_id is not null and q4_id is null),
q4 as (select form_id, q1_id,q1_score,q4_o_id as option_id,total_weightage, final_score from view_question_option where q2_id is not null and q3_id is not null and q4_id is not null),
all_question as (select q1.* from q1
		union 
		select q2.* from q2
		union 
		select q3.* from q3
		union
		select q4.* from q4)

select a.created_by_id as user_id ,aq.* from answer as a
left join all_question as aq on aq.option_id=a.option_id
order by aq.q1_id,aq.option_id asc



# read daily reports
with
a as (select distinct created_by_id,  count(distinct member_id) as total_member
from "answer" where created_at::text like '2021-10-18%'
group by created_by_id)

select u.name, a.*
from a 
left join "user" as u on u.id=a.created_by_id


# max and sum weightage
with
sum_weightage as (with
	tw as (select form_id, member_id, option_id, total_weightage
		from view_member_answer where total_weightage is not null)

	select sum(tw.total_weightage) as sum_weightage, tw.form_id, tw.member_id 
	from tw where tw.form_id='64' and tw.member_id='101'
	group by tw.form_id, tw.member_id),

max_weightage as (select form_id, max(total_weightage) as max_weightage
	from view_member_answer where form_id='64'
	group by form_id),
sum_score as (select sum(score) as sum_score  from question where form_id='64' and parent_question_id is null)

select sum_weightage.sum_weightage, max_weightage.max_weightage , sum_score.sum_score
from sum_weightage, max_weightage, sum_score
drop table if exists ddc_choreograph;
	create table ddc_choreograph (
	"id" integer primary key autoincrement,
	"ip" text not null,
	"uuid" text not null,
	"song_artist" text,
	"song_title" text,
	"diff_coarse" text,
	"filename" text
);
drop table if exists ddc_feedback;
	create table ddc_feedback (
	"id" integer primary key autoincrement,
	"ip" text not null,
	"email" text,
	"satisfaction" integer,
	"comments" text
);

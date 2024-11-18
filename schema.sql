  create table
  public.users (
    user_id bigserial not null,
    first_name text not null,
    last_name text not null,
    constraint users_pkey primary key (user_id)
  ) tablespace pg_default;

  create table
  public.workout (
    workout_id bigserial not null,
    workout_name text not null,
    muscle_group_id integer null,
    equipment_id integer null,
    constraint workout_pkey primary key (workout_id),
    constraint fk_equipment foreign key (equipment_id) references equipment (equipment_id),
    constraint fk_muscle_group foreign key (muscle_group_id) references muscle_group (muscle_group_id)
  ) tablespace pg_default;

  create table
  public.user_workout_item (
    user_id bigint not null,
    workout_id bigint not null,
    sets integer not null,
    reps integer not null,
    weight integer not null,
    rest_time integer not null,
    one_rep_max integer not null,
    constraint user_workout_item_pkey primary key (user_id, workout_id),
    constraint user_workout_item_user_id_fkey foreign key (user_id) references users (user_id),
    constraint user_workout_item_workout_id_fkey foreign key (workout_id) references workout (workout_id)
  ) tablespace pg_default;

  create table
  public.equipment (
    equipment_id bigserial not null,
    equipment_name text not null,
    constraint equipment_pkey primary key (equipment_id),
    constraint equipment_equipment_name_key unique (equipment_name)
  ) tablespace pg_default;

  create table
  public.muscle_group (
    muscle_group_id bigserial not null,
    muscle_group_name text not null,
    constraint muscle_group_pkey primary key (muscle_group_id),
    constraint muscle_group_muscle_group_name_key unique (muscle_group_name)
  ) tablespace pg_default;
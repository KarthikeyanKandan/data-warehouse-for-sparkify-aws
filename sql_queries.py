import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
        CREATE TABLE IF NOT EXISTS staging_events(
            artist              VARCHAR,
            auth                VARCHAR(12),
            firstName           VARCHAR(25),
            gender              VARCHAR(1),
            itemInSession       INTEGER,
            lastName            VARCHAR(25),
            length              NUMERIC,
            location            VARCHAR,
            method              VARCHAR(5),
            page                VARCHAR(12),
            registration        NUMERIC,
            sessionId           INTEGER,
            song                VARCHAR,
            status              INTEGER,
            ts                  TIMESTAMP,
            userAgent           VARCHAR,
            userId              INTEGER          

        )
""")

staging_songs_table_create = ("""
        CREATE TABLE IF NOT EXISTS staging_songs(
            num_songs           INTEGER,
            artist_id           VARCHAR,
            artist_latitude     NUMERIC,
            artist_longitude    NUMERIC,
            artist_location     VARCHAR,
            artist_name         VARCHAR,
            song_id             VARCHAR,
            title               VARCHAR,
            duration            NUMERIC,
            year                INTEGER
        )
""")

songplay_table_create = ("""
        CREATE TABLE IF NOT EXISTS songplays(
            songplay_id         INTEGER         IDENTITY(0,1)   PRIMARY KEY,
            start_time          TIMESTAMP       NOT NULL        SORTKEY DISTKEY,
            user_id             INTEGER         NOT NULL,
            level               VARCHAR         NOT NULL,
            song_id             VARCHAR         NOT NULL,
            artist_id           VARCHAR         NOT NULL,
            session_id          INTEGER         NOT NULL,
            location            VARCHAR         NOT NULL,
            user_agent          VARCHAR         NOT NULL
        )
""")

user_table_create = ("""
        CREATE TABLE IF NOT EXISTS users(
            user_id             INTEGER         SORTKEY PRIMARY KEY,
            first_name          VARCHAR         NOT NULL,
            last_name           VARCHAR         NOT NULL,
            gender              VARCHAR         NOT NULL,
            level               VARCHAR         NOT NULL
        )
""")

song_table_create = ("""
        CREATE TABLE IF NOT EXISTS songs(
            song_id             INTEGER         SORTKEY PRIMARY KEY,
            title               VARCHAR         NOT NULL,
            artist_id           INTEGER         NOT NULL,
            year                INTEGER         NOT NULL,
            duration            NUMERIC         NOT NULL
        )
""")

artist_table_create = ("""
        CREATE TABLE IF NOT EXISTS artists(
            artist_id           INTEGER         SORTKEY PRIMARY KEY,
            name                VARCHAR         NOT NULL,
            location            VARCHAR         NOT NULL,
            latitude            NUMERIC,
            longitude           NUMERIC
        )
""")

time_table_create = ("""
        CREATE TABLE IF NOT EXISTS time(
            start_tine          TIMESTAMP       DISTKEY SORTKEY PRIMARY KEY,
            hour                INTEGER         NOT NULL,
            day                 INTEGER         NOT NULL,
            month               INTEGER         NOT NULL,
            year                INTEGER         NOT NULL,
            weekday             VARCHAR         NOT NULL
        )
""")

# STAGING TABLES

staging_events_copy = ("""
""").format()

staging_songs_copy = ("""
""").format()

# FINAL TABLES

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")

time_table_insert = ("""
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]

import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

ARN                    = config.get("IAM_ROLE","ARN")
LOG_DATA               = config.get("S3","LOG_DATA")
SONG_DATA              = config.get("S3","SONG_DATA")
LOG_JSONPATH           = config.get("S3","LOG_JSONPATH")

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
        CREATE TABLE IF NOT EXISTS staging_events(
            artist              VARCHAR,
            auth                VARCHAR,
            firstName           VARCHAR,
            gender              VARCHAR,
            itemInSession       INTEGER,
            lastName            VARCHAR,
            length              FLOAT,
            level               VARCHAR,
            location            VARCHAR,
            method              VARCHAR,
            page                VARCHAR,
            registration        FLOAT,
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
            artist_latitude     FLOAT,
            artist_longitude    FLOAT,
            artist_location     VARCHAR,
            artist_name         VARCHAR,
            song_id             VARCHAR,
            title               VARCHAR,
            duration            FLOAT,
            year                INTEGER
        )
""")

songplay_table_create = ("""
        CREATE TABLE IF NOT EXISTS songplay(
            songplay_id         INTEGER         IDENTITY(0,1)   PRIMARY KEY,
            start_time          TIMESTAMP       NOT NULL        SORTKEY DISTKEY,
            user_id             INTEGER         NOT NULL,
            level               VARCHAR         NOT NULL,
            song_id             VARCHAR         NOT NULL,
            artist_id           VARCHAR         NOT NULL,
            session_id          INTEGER         NOT NULL,
            location            VARCHAR,
            user_agent          VARCHAR 
        )
""")

user_table_create = ("""
        CREATE TABLE IF NOT EXISTS users(
            user_id             INTEGER         NOT NULL SORTKEY PRIMARY KEY,
            first_name          VARCHAR         NOT NULL,
            last_name           VARCHAR         NOT NULL,
            gender              VARCHAR         NOT NULL,
            level               VARCHAR         NOT NULL
        )
""")

song_table_create = ("""
        CREATE TABLE IF NOT EXISTS songs(
            song_id             VARCHAR         NOT NULL SORTKEY PRIMARY KEY,
            title               VARCHAR         NOT NULL,
            artist_id           VARCHAR         NOT NULL,
            year                INTEGER         NOT NULL,
            duration            FLOAT         NOT NULL
        )
""")

artist_table_create = ("""
        CREATE TABLE IF NOT EXISTS artists(
            artist_id           VARCHAR         NOT NULL SORTKEY PRIMARY KEY,
            name                VARCHAR         NOT NULL,
            location            VARCHAR,
            latitude            FLOAT,
            longitude           FLOAT
        )
""")

time_table_create = ("""
        CREATE TABLE IF NOT EXISTS time(
            start_time          TIMESTAMP       NOT NULL DISTKEY SORTKEY PRIMARY KEY,
            hour                INTEGER         NOT NULL,
            day                 INTEGER         NOT NULL,
            month               INTEGER         NOT NULL,
            year                INTEGER         NOT NULL,
            weekday             VARCHAR         NOT NULL
        )
""")

# STAGING TABLES

staging_events_copy = ("""
        COPY staging_events 
        FROM {}
        iam_role {}
        region 'us-west-2' json {} timeformat as 'epochmillisecs';
""").format(LOG_DATA, ARN, LOG_JSONPATH)

staging_songs_copy = ("""
        COPY staging_songs
        FROM {}
        iam_role {}
        region 'us-west-2' json 'auto';
""").format(SONG_DATA, ARN)

# FINAL TABLES

songplay_table_insert = ("""
        INSERT INTO songplay (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
        SELECT  DISTINCT(e.ts), 
                e.userId, 
                e.level, 
                s.song_id, 
                s.artist_id, 
                e.sessionId, 
                e.location, 
                e.userAgent
        FROM staging_events e
        JOIN staging_songs s
        ON (e.song = s.title AND e.artist = s.artist_name)
        WHERE e.page = 'NextSong'
""")

user_table_insert = ("""
        INSERT INTO users (user_id, first_name, last_name, gender, level)
        SELECT DISTINCT(e.userId), 
               e.firstName, 
               e.lastName, 
               e.gender, 
               e.level
        FROM staging_events e
        WHERE userId IS NOT NULL
        AND e.page = 'NextSong'
""")

song_table_insert = ("""
        INSERT INTO songs (song_id, title, artist_id, year, duration)
        SELECT DISTINCT(s.song_id),
               s.title,
               s.artist_id,
               s.year,
               s.duration
        FROM staging_songs s
        WHERE song_id IS NOT NULL
""")

artist_table_insert = ("""
        INSERT INTO artists (artist_id, name, location, latitude, longitude)
        SELECT DISTINCT(s.artist_id), 
               s.artist_name, 
               s.artist_location, 
               s.artist_latitude, 
               s.artist_longitude
        FROM staging_songs s
        WHERE s.artist_id IS NOT NULL
""")

time_table_insert = ("""
        INSERT INTO time (start_time, hour, day, month, year, weekday)
        SELECT DISTINCT(start_time),
               EXTRACT (hour FROM start_time),
               EXTRACT (day FROM start_time),
               EXTRACT (month FROM start_time),
               EXTRACT (year FROM start_time),
               EXTRACT (dayofweek FROM start_time)
        FROM songplay
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
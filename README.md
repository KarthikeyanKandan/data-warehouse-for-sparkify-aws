# Data Warehousing with AWS Redshift for music streaming app 'Sparkify'

## Objective: building an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to.

### Introduction

A startup called parkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

As their data engineer, you are tasked with building an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

### Files

1. [`create_tables.py`](create_tables.py) : Drops and creates your tables. You run this file to reset your tables before each time you run your ETL scripts. This is where you'll create your fact and dimension tables for the star schema in Redshift.
2. [`etl.py`](etl.py) : Rreads and processes files from song_data and log_data and loads them into your tables using COPY and INSERT Statements. This is where you'll load data from S3 into staging tables on Redshift and then process that data into your analytics tables on Redshift.
3. [`sql_queries.py`](sql_queries.py) : Ccontains all the SQL queries and is imported into the last two files above.
4. ['dwh.cfg'](dwh.cfg) : Contains all the required configuration details

### The Schema for the Song Play Analysis

Using the song and log datasets, I've created a star schema optimized for queries on song play analysis. This includes the following tables.

#### Fact Table

1. `songplays` - records in log data associated with song plays i.e. records with page NextSong
     - songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

#### Dimension Tables

1. `users` - users in the app
    - user_id, first_name, last_name, gender, level
2. `songs` - songs in the music database
    - song_id, title, artist_id, year, duration
3. `artists` - artists in the music database
    - rtist_id, name, location, latitude, longitude
4. `time` - timestamps of records in songplays broken down into the specific unit
    - `start_time`, hour, day, week, month, year, weekday

### Use

Remember to run [`create_tables.py`](create_tables.py) before running [`etl.py`](etl.py) to reset your tables. 

### ETL pipeline

Prerequisites: 

- Database and tables created

## Project Steps

### Create Table Schemas

1. Designed schemas for fact and dimension tables

2. Written SQL CREATE statement for each of these tables in sql_queries.py

3. Completed the logic in create_tables.py to connect to the database and create these tables

4. Written SQL DROP statements to drop tables in the beginning of create_tables.py if the tables already exist. This way, we can run create_tables.py whenever you want to reset your database and test our ETL pipeline.

5. Launched a redshift cluster and created an IAM role that has read access to S3.

6. Added redshift database and IAM role info to dwh.cfg.

7. Tested by running create_tables.py and checking the table schemas in the redshift database. 

### Build ETL Pipeline

1. Implemented the logic in etl.py to load data from S3 to staging tables on Redshift.

2. Implemented the logic in etl.py to load data from staging tables to analytics tables on Redshift.

3. Tested by running etl.py after running create_tables.py.

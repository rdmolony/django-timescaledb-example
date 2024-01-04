# Initialise the database
pg_ctl init -D .db/

# Add TimescaleDB to preloaded libraries
echo "shared_preload_libraries = 'timescaledb'" >> ./.db/postgresql.conf 

# Launch the database server 
pg_ctl start -D .db/

# Create a database
createdb db

# Create role django with empty password
psql -d db -c "
    CREATE USER django;

    GRANT USAGE ON SCHEMA public TO django;
    GRANT CREATE ON SCHEMA public TO django;
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO django;
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO django;

    -- Grant rights to create databases (useful for running tests)
    GRANT CONNECT ON DATABASE db TO django;
    ALTER USER django CREATEDB;
"

# Install TimescaleDB in db & in template1 so automatically available in test_db
psql -d db -c "CREATE EXTENSION timescaledb"
psql -d template1 -c "CREATE EXTENSION timescaledb"

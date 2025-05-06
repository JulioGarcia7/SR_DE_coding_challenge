-- Connect to the database
\c globant_migration_db

-- Create the schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS public;
 
-- Grant privileges
GRANT ALL PRIVILEGES ON SCHEMA public TO globant_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO globant_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO globant_user; 
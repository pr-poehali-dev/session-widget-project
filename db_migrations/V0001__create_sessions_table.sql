-- Create sessions table for tracking active visitors
CREATE TABLE IF NOT EXISTS sessions (
    session_id VARCHAR(255) PRIMARY KEY,
    last_active TIMESTAMP NOT NULL DEFAULT NOW(),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create index for faster queries on last_active
CREATE INDEX IF NOT EXISTS idx_sessions_last_active ON sessions(last_active);
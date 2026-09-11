-- =============================================================================
-- backend/db/schema.sql
-- =============================================================================
-- IBM Db2 on Cloud schema for Fitness Buddy.
--
-- Tables:
--   users         — one row per user; stores the UserProfile fields
--   chat_history  — one row per message turn (user or assistant)
--   daily_logs    — one row per user per calendar date; tracks streaks
--
-- Run against Db2 once to initialise the database:
--   db2 -tf schema.sql
-- =============================================================================

-- DROP TABLE chat_history;
-- DROP TABLE daily_logs;
-- DROP TABLE users;

-- ---------------------------------------------------------------------------
-- users
-- ---------------------------------------------------------------------------
CREATE TABLE users (
    user_id              VARCHAR(128)  NOT NULL,
    name                 VARCHAR(128)  DEFAULT 'Friend',
    age                  SMALLINT,
    fitness_level        VARCHAR(20)   DEFAULT 'beginner',
    primary_goal         VARCHAR(40)   DEFAULT 'general_health',
    equipment            VARCHAR(256)  DEFAULT '',
    dietary_restrictions VARCHAR(256)  DEFAULT '',
    current_streak       INTEGER       DEFAULT 0,
    onboarding_complete  SMALLINT      DEFAULT 0,   -- 0=false, 1=true
    created_at           TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
    updated_at           TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id)
);

-- ---------------------------------------------------------------------------
-- chat_history
-- ---------------------------------------------------------------------------
CREATE TABLE chat_history (
    id          INTEGER       NOT NULL GENERATED ALWAYS AS IDENTITY,
    user_id     VARCHAR(128)  NOT NULL,
    role        VARCHAR(20)   NOT NULL,   -- 'user' | 'assistant'
    content     CLOB(4096)    NOT NULL,
    type        VARCHAR(20)   DEFAULT 'text',
    data        CLOB(8192),              -- JSON payload for workout/meal cards
    created_at  TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
);

-- Index for fast retrieval of recent history per user
CREATE INDEX idx_chat_user_time ON chat_history (user_id, created_at DESC);

-- ---------------------------------------------------------------------------
-- daily_logs
-- ---------------------------------------------------------------------------
CREATE TABLE daily_logs (
    id          INTEGER       NOT NULL GENERATED ALWAYS AS IDENTITY,
    user_id     VARCHAR(128)  NOT NULL,
    log_date    DATE          NOT NULL,
    workouts    SMALLINT      DEFAULT 0,
    streak_day  SMALLINT      DEFAULT 0,  -- 1 if this day counts towards streak
    PRIMARY KEY (id),
    CONSTRAINT uq_daily_log UNIQUE (user_id, log_date),
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
);

-- SQLite store. Raw stays raw; calibration applies on read.

CREATE TABLE IF NOT EXISTS readings (
    id             INTEGER PRIMARY KEY,
    node_id        TEXT    NOT NULL,
    seq            INTEGER NOT NULL,      -- node sequence number; the Pico has no trustworthy RTC
    schema_version INTEGER NOT NULL,
    measured_at    TEXT    NOT NULL,      -- reconstructed on the laptop from seq + interval
    received_at    TEXT    NOT NULL,      -- differs from measured_at after a dropout. That gap is data.
    channel        TEXT    NOT NULL,      -- e.g. 'air_temp_c', 'soil_vwc_raw_a'
    value          REAL,                  -- NULL = sensor failed this cycle; keep the row
    UNIQUE (node_id, seq, channel)
);

CREATE INDEX IF NOT EXISTS idx_readings_time    ON readings (measured_at);
CREATE INDEX IF NOT EXISTS idx_readings_channel ON readings (channel, measured_at);

-- Public weather, long format, one row per source-time-variable.
CREATE TABLE IF NOT EXISTS weather (
    id          INTEGER PRIMARY KEY,
    source      TEXT NOT NULL,    -- 'knmi_260' | 'era5_land' | 'harmonie_arome' | 'sarah3'
    kind        TEXT NOT NULL,    -- 'observation' | 'reanalysis' | 'forecast' | 'satellite'
    issued_at   TEXT,             -- forecasts only: which run this came from
    valid_at    TEXT NOT NULL,
    variable    TEXT NOT NULL,    -- units in the name, always
    value       REAL,
    UNIQUE (source, kind, issued_at, valid_at, variable)
);

-- Thun day-type, computed. One row per day per site.
CREATE TABLE IF NOT EXISTS daytypes (
    date            TEXT PRIMARY KEY,
    constellation   TEXT NOT NULL,   -- IAU abbrev; may be 'Oph' or non-zodiacal
    day_type        TEXT,            -- root|leaf|flower|fruit|NULL
    folded_from_oph INTEGER NOT NULL DEFAULT 0,  -- flag it, never hide it
    ascending       INTEGER,         -- declination cycle, NOT waxing/waning
    blanked         INTEGER NOT NULL DEFAULT 0,
    blank_reason    TEXT,            -- 'node' | 'eclipse' | 'perigee'
    engine_version  TEXT NOT NULL
);

-- Every planting, with the covariates needed to test the calendar later.
CREATE TABLE IF NOT EXISTS plantings (
    id        INTEGER PRIMARY KEY,
    plot      TEXT NOT NULL,
    crop      TEXT NOT NULL,
    organ     TEXT NOT NULL,   -- root|leaf|flower|fruit: what you are growing it FOR
    sown_at   TEXT NOT NULL,
    day_type  TEXT,            -- logged covariate, never a constraint
    notes     TEXT
);

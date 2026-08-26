-- SQLite store. Raw stays raw; calibration applies on read.
--
-- TWO PLOTS. Every table that holds measured or modelled data carries `site`,
-- matching a slug in config.SITES ('prora' | 'castelo_branco'). Nothing here is
-- allowed to be site-ambiguous: the plots have different reference networks,
-- different forecast resolutions and different climates, so a query that pools
-- them has to say so out loud by omitting the filter deliberately.

CREATE TABLE IF NOT EXISTS readings (
    id             INTEGER PRIMARY KEY,
    site           TEXT    NOT NULL,      -- config.SITES slug
    node_id        TEXT    NOT NULL,
    seq            INTEGER NOT NULL,      -- node sequence number; the Pico has no trustworthy RTC
    schema_version INTEGER NOT NULL,
    measured_at    TEXT    NOT NULL,      -- reconstructed on the laptop from seq + interval
    received_at    TEXT    NOT NULL,      -- differs from measured_at after a dropout. That gap is data.
    channel        TEXT    NOT NULL,      -- e.g. 'air_temp_c', 'soil_vwc_raw_a'
    value          REAL,                  -- NULL = sensor failed this cycle; keep the row
    UNIQUE (site, node_id, seq, channel)
);

CREATE INDEX IF NOT EXISTS idx_readings_time    ON readings (site, measured_at);
CREATE INDEX IF NOT EXISTS idx_readings_channel ON readings (site, channel, measured_at);

-- Public weather, long format, one row per site-source-time-variable.
-- `source` is asymmetric between the plots, by necessity, not by oversight:
--   prora           'dwd_00183' is primary, 'era5_land' is the cross-check
--   castelo_branco  'era5_land' is primary, 'ipma_castelo_branco' is the cross-check
CREATE TABLE IF NOT EXISTS weather (
    id          INTEGER PRIMARY KEY,
    site        TEXT NOT NULL,    -- config.SITES slug
    source      TEXT NOT NULL,    -- 'dwd_00183' | 'ipma_castelo_branco' | 'era5_land' | 'icon_d2' | 'icon_eu' | 'sarah3'
    kind        TEXT NOT NULL,    -- 'observation' | 'reanalysis' | 'forecast' | 'satellite'
    issued_at   TEXT,             -- forecasts only: which run this came from
    valid_at    TEXT NOT NULL,
    variable    TEXT NOT NULL,    -- units in the name, always
    value       REAL,
    UNIQUE (site, source, kind, issued_at, valid_at, variable)
);

CREATE INDEX IF NOT EXISTS idx_weather_lookup ON weather (site, variable, valid_at);

-- Thun day-type, computed.
--
-- Deliberately NOT per site: the Moon's constellation, its declination cycle and
-- the node/eclipse/perigee moments are all geocentric, so they are the same sky
-- for both plots. What DOES differ is which local date an instant falls on:
-- Europe/Berlin and Europe/Lisbon are an hour apart, so a transition just after
-- local midnight at Prora is still the previous day at Castelo Branco.
--
-- TODO Phase 6: store the UTC instant of each transition, not just the date, and
-- resolve to a local date per site on read. Storing only `date` bakes in one
-- timezone and will quietly disagree with a printed calendar at one plot.
CREATE TABLE IF NOT EXISTS daytypes (
    date            TEXT PRIMARY KEY,     -- UTC date, see the TODO above
    constellation   TEXT NOT NULL,        -- IAU abbrev; may be 'Oph' or non-zodiacal
    day_type        TEXT,                 -- root|leaf|flower|fruit|NULL
    folded_from_oph INTEGER NOT NULL DEFAULT 0,  -- flag it, never hide it
    ascending       INTEGER,              -- declination cycle, NOT waxing/waning
    blanked         INTEGER NOT NULL DEFAULT 0,
    blank_reason    TEXT,                 -- 'node' | 'eclipse' | 'perigee'
    engine_version  TEXT NOT NULL
);

-- Every planting, with the covariates needed to test the calendar later.
-- Two plots in different climates is a better test bed than one: the same day
-- type lands on two very different growing environments, which is the confound
-- the historical trials had no way to separate. It only works if `site` is
-- always recorded and always used as a stratum.
CREATE TABLE IF NOT EXISTS plantings (
    id        INTEGER PRIMARY KEY,
    site      TEXT NOT NULL,   -- config.SITES slug
    bed       TEXT,            -- optional, within-plot location
    crop      TEXT NOT NULL,
    organ     TEXT NOT NULL,   -- root|leaf|flower|fruit: what you are growing it FOR
    sown_at   TEXT NOT NULL,
    day_type  TEXT,            -- logged covariate, never a constraint
    notes     TEXT
);

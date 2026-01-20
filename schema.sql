-- Startup Scout Database Schema for Supabase
-- Run this in your Supabase SQL Editor after creating project

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (Supabase Auth handles this, but we add custom fields)
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID REFERENCES auth.users PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Preferences
    roles TEXT[] DEFAULT '{}',
    locations TEXT[] DEFAULT '{}',
    min_salary INTEGER DEFAULT 30000,
    max_salary INTEGER DEFAULT 150000,
    company_stages TEXT[] DEFAULT '{}',
    industries TEXT[] DEFAULT '{}'
);

-- Jobs table
CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    company TEXT,
    title TEXT,
    location TEXT,
    salary TEXT,
    description TEXT,
    url TEXT,
    posted_at TIMESTAMP WITH TIME ZONE,
    scraped_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Metadata
    is_startup BOOLEAN DEFAULT FALSE,
    startup_score INTEGER DEFAULT 0,
    stage TEXT,
    employees TEXT,
    applicants INTEGER,
    
    -- Search
    search_vector tsvector GENERATED ALWAYS AS (
        to_tsvector('english', coalesce(company, '') || ' ' || coalesce(title, '') || ' ' || coalesce(description, ''))
    ) STORED,
    
    UNIQUE(company, title)
);

-- Create index for full-text search
CREATE INDEX IF NOT EXISTS jobs_search_idx ON jobs USING GIN(search_vector);
CREATE INDEX IF NOT EXISTS jobs_posted_idx ON jobs(posted_at DESC);
CREATE INDEX IF NOT EXISTS jobs_startup_score_idx ON jobs(startup_score DESC);

-- Funding alerts table
CREATE TABLE IF NOT EXISTS funding_alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company TEXT NOT NULL,
    amount TEXT,
    round TEXT,
    date TIMESTAMP WITH TIME ZONE,
    location TEXT,
    employees TEXT,
    investors TEXT[],
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS funding_date_idx ON funding_alerts(date DESC);

-- Watched companies table
CREATE TABLE IF NOT EXISTS watched_companies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
    company TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(user_id, company)
);

-- Applications table
CREATE TABLE IF NOT EXISTS applications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
    job_id TEXT REFERENCES jobs(id) ON DELETE CASCADE,
    status TEXT DEFAULT 'applied',  -- applied, screening, interview, offer, rejected
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    notes TEXT,
    
    UNIQUE(user_id, job_id)
);

CREATE INDEX IF NOT EXISTS applications_user_idx ON applications(user_id);
CREATE INDEX IF NOT EXISTS applications_status_idx ON applications(status);

-- Saved jobs table
CREATE TABLE IF NOT EXISTS saved_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
    job_id TEXT REFERENCES jobs(id) ON DELETE CASCADE,
    saved_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(user_id, job_id)
);

-- User match scores (pre-calculated for performance)
CREATE TABLE IF NOT EXISTS user_job_matches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
    job_id TEXT REFERENCES jobs(id) ON DELETE CASCADE,
    match_score INTEGER,
    calculated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(user_id, job_id)
);

CREATE INDEX IF NOT EXISTS matches_user_score_idx ON user_job_matches(user_id, match_score DESC);

-- Notification preferences table
CREATE TABLE IF NOT EXISTS notification_preferences (
    user_id UUID PRIMARY KEY REFERENCES user_profiles(id) ON DELETE CASCADE,
    funding_alerts BOOLEAN DEFAULT TRUE,
    new_jobs BOOLEAN DEFAULT TRUE,
    watched_companies BOOLEAN DEFAULT TRUE,
    match_threshold INTEGER DEFAULT 80
);

-- Row Level Security (RLS) Policies
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE watched_companies ENABLE ROW LEVEL SECURITY;
ALTER TABLE applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE saved_jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_job_matches ENABLE ROW LEVEL SECURITY;
ALTER TABLE notification_preferences ENABLE ROW LEVEL SECURITY;

-- Jobs and funding are public (read-only)
ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE funding_alerts ENABLE ROW LEVEL SECURITY;

-- Policies for user_profiles
CREATE POLICY "Users can view own profile"
    ON user_profiles FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
    ON user_profiles FOR UPDATE
    USING (auth.uid() = id);

-- Policies for jobs (public read)
CREATE POLICY "Anyone can view jobs"
    ON jobs FOR SELECT
    USING (TRUE);

-- Policies for funding_alerts (public read)
CREATE POLICY "Anyone can view funding alerts"
    ON funding_alerts FOR SELECT
    USING (TRUE);

-- Policies for watched_companies
CREATE POLICY "Users can view own watched companies"
    ON watched_companies FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can add watched companies"
    ON watched_companies FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can remove watched companies"
    ON watched_companies FOR DELETE
    USING (auth.uid() = user_id);

-- Policies for applications
CREATE POLICY "Users can view own applications"
    ON applications FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can create own applications"
    ON applications FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own applications"
    ON applications FOR UPDATE
    USING (auth.uid() = user_id);

-- Policies for saved_jobs
CREATE POLICY "Users can view own saved jobs"
    ON saved_jobs FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can save jobs"
    ON saved_jobs FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can unsave jobs"
    ON saved_jobs FOR DELETE
    USING (auth.uid() = user_id);

-- Functions
CREATE OR REPLACE FUNCTION calculate_match_score(
    user_profile_id UUID,
    job_record jobs
) RETURNS INTEGER AS $$
DECLARE
    score INTEGER := 0;
    user_rec user_profiles;
BEGIN
    SELECT * INTO user_rec FROM user_profiles WHERE id = user_profile_id;
    
    -- Match by role
    IF job_record.title ILIKE ANY(SELECT unnest(user_rec.roles)) THEN
        score := score + 30;
    END IF;
    
    -- Match by location
    IF job_record.location ILIKE ANY(SELECT unnest(user_rec.locations)) THEN
        score := score + 20;
    END IF;
    
    -- Match by stage
    IF job_record.stage = ANY(user_rec.company_stages) THEN
        score := score + 15;
    END IF;
    
    -- Startup score boost
    score := score + (job_record.startup_score / 3);
    
    RETURN LEAST(score, 100);
END;
$$ LANGUAGE plpgsql;

-- Trigger to update match scores when new jobs are added
CREATE OR REPLACE FUNCTION update_match_scores()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO user_job_matches (user_id, job_id, match_score)
    SELECT 
        up.id,
        NEW.id,
        calculate_match_score(up.id, NEW)
    FROM user_profiles up
    ON CONFLICT (user_id, job_id) DO UPDATE
        SET match_score = EXCLUDED.match_score,
            calculated_at = NOW();
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_job_matches
    AFTER INSERT ON jobs
    FOR EACH ROW
    EXECUTE FUNCTION update_match_scores();

-- Sample data (for testing)
INSERT INTO jobs (id, source, company, title, location, salary, is_startup, startup_score, stage, posted_at)
VALUES
    ('sample_1', 'HackerNews', 'Revolut', 'Backend Engineer', 'London, UK', '£70-90k', TRUE, 95, 'Series C', NOW()),
    ('sample_2', 'Y Combinator', 'Stripe', 'Product Manager', 'London, UK', '£80-100k', TRUE, 90, 'Series D', NOW() - INTERVAL '1 day'),
    ('sample_3', 'WTTJ', 'Monzo', 'Financial Analyst', 'Remote', '£55-70k', TRUE, 92, 'Series B', NOW() - INTERVAL '5 hours')
ON CONFLICT (id) DO NOTHING;

INSERT INTO funding_alerts (company, amount, round, date, location, description)
VALUES
    ('Vanta', '$50M', 'Series B', NOW() - INTERVAL '2 hours', 'London, UK', 'Security automation platform raises Series B'),
    ('Monzo', '$100M', 'Series C', NOW() - INTERVAL '1 day', 'London, UK', 'Digital bank expands product offerings')
ON CONFLICT DO NOTHING;

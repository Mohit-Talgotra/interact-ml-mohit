CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS applications (
    id UUID DEFAULT uuid_generate_v4(),
    opening_id UUID,
    organization_id UUID,
    project_id UUID,
    user_id UUID,
    email TEXT,
    created_at TIMESTAMP DEFAULT current_timestamp,
    status SMALLINT,
    content TEXT,
    resume TEXT,
    links TEXT[],
    yoe SMALLINT DEFAULT 0,
    include_email BOOLEAN DEFAULT FALSE,
    include_resume BOOLEAN DEFAULT FALSE,
    score FLOAT DEFAULT -1.0,
    no_comments INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS post_bookmarks (
    id UUID DEFAULT uuid_generate_v4(),
    user_id UUID,
    title TEXT,
    created_at TIMESTAMP DEFAULT current_timestamp
);

CREATE TABLE IF NOT EXISTS post_bookmark_items (
    id UUID DEFAULT uuid_generate_v4(),
    post_bookmark_id UUID,
    post_id UUID
);

CREATE TABLE IF NOT EXISTS project_bookmarks (
    id UUID DEFAULT uuid_generate_v4(),
    user_id UUID,
    title TEXT,
    created_at TIMESTAMP DEFAULT current_timestamp
);

CREATE TABLE IF NOT EXISTS project_bookmark_items (
    id UUID DEFAULT uuid_generate_v4(),
    project_bookmark_id UUID,
    project_id UUID
);

CREATE TABLE IF NOT EXISTS opening_bookmarks (
    id UUID DEFAULT uuid_generate_v4(),
    user_id UUID,
    title TEXT,
    created_at TIMESTAMP DEFAULT current_timestamp
);

CREATE TABLE IF NOT EXISTS opening_bookmark_items (
    id UUID DEFAULT uuid_generate_v4(),
    opening_bookmark_id UUID,
    opening_id UUID
);

CREATE TABLE IF NOT EXISTS event_bookmarks (
    id UUID DEFAULT uuid_generate_v4(),
    user_id UUID,
    title TEXT,
    created_at TIMESTAMP DEFAULT current_timestamp
);

CREATE TABLE IF NOT EXISTS event_bookmark_items (
    id UUID DEFAULT uuid_generate_v4(),
    event_bookmark_id UUID,
    event_id UUID
);

CREATE TABLE IF NOT EXISTS comments (
    id UUID DEFAULT uuid_generate_v4(),
    post_id UUID,
    project_id UUID,
    event_id UUID,
    announcement_id UUID,
    task_id UUID,
    application_id UUID,
    parent_comment_id UUID,
    is_replied_comment BOOLEAN DEFAULT FALSE,
    level INT DEFAULT 1,
    user_id UUID,
    content TEXT,
    no_likes INT,
    no_replies INT,
    edited BOOLEAN DEFAULT FALSE,
    is_flagged BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT current_timestamp,
    updated_at TIMESTAMP DEFAULT current_timestamp
);

CREATE TABLE IF NOT EXISTS events (
    id UUID DEFAULT uuid_generate_v4(),
    title TEXT,
    tagline TEXT,
    cover_pic TEXT DEFAULT 'default.jpg',
    blur_hash TEXT DEFAULT 'no-hash',
    description TEXT,
    links TEXT[],
    tags TEXT[],
    no_views INT DEFAULT 0,
    no_likes INT DEFAULT 0,
    no_shares INT DEFAULT 0,
    no_comments INT DEFAULT 0,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    location TEXT,
    category TEXT,
    impressions INT DEFAULT 0,
    organization_id UUID,
    is_flagged BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT current_timestamp
);

CREATE TABLE IF NOT EXISTS likes (
    id UUID DEFAULT uuid_generate_v4(),
    user_id UUID,
    post_id UUID,
    project_id UUID,
    event_id UUID,
    announcement_id UUID,
    comment_id UUID,
    review_id UUID,
    status SMALLINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT current_timestamp
);

CREATE TABLE IF NOT EXISTS memberships (
    id UUID DEFAULT uuid_generate_v4(),
    project_id UUID,
    user_id UUID,
    role TEXT,
    title VARCHAR(25),
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT current_timestamp
);

CREATE TABLE IF NOT EXISTS openings (
    id UUID DEFAULT uuid_generate_v4(),
    organization_id UUID,
    project_id UUID,
    title TEXT,
    description TEXT,
    tags TEXT[],
    active BOOLEAN DEFAULT TRUE,
    user_id UUID,
    no_of_applications SMALLINT,
    impressions INT DEFAULT 0,
    is_flagged BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT current_timestamp,
    no_shares INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS organizations (
    id UUID DEFAULT uuid_generate_v4(),
    user_id UUID,
    organization_title TEXT,
    number_of_members SMALLINT DEFAULT 0,
    number_of_events SMALLINT DEFAULT 0,
    number_of_projects SMALLINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT current_timestamp,
    is_flagged BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS posts (
    id UUID DEFAULT uuid_generate_v4(),
    user_id UUID,
    content TEXT,
    created_at TIMESTAMP DEFAULT current_timestamp,
    images TEXT[],
    hashes TEXT[],
    no_shares INT DEFAULT 0,
    no_likes INT DEFAULT 0,
    no_comments INT DEFAULT 0,
    repost_id UUID,
    is_repost BOOLEAN DEFAULT FALSE,
    no_of_reposts INT DEFAULT 0,
    tags TEXT[],
    topics TEXT[],
    impressions INT DEFAULT 0,
    is_edited BOOLEAN DEFAULT FALSE,
    is_flagged BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS projects (
    id UUID DEFAULT uuid_generate_v4(),
    title TEXT,
    slug TEXT,
    tagline TEXT,
    cover_pic TEXT DEFAULT 'default.jpg',
    blur_hash TEXT DEFAULT 'no-hash',
    description TEXT,
    user_id UUID,
    created_at TIMESTAMP DEFAULT current_timestamp,
    tags TEXT[],
    no_likes INT DEFAULT 0,
    no_shares INT DEFAULT 0,
    no_comments INT DEFAULT 0,
    total_no_views INT DEFAULT 0,
    category TEXT,
    is_private BOOLEAN DEFAULT FALSE,
    is_flagged BOOLEAN DEFAULT FALSE,
    views INT,
    number_of_members INT DEFAULT 1,
    impressions INT DEFAULT 0,
    links TEXT[],
    private_links TEXT[],
    organization_id UUID
);

CREATE TABLE IF NOT EXISTS project_views (
    id UUID DEFAULT uuid_generate_v4(),
    project_id UUID,
    date TIMESTAMP,
    count INT
);

CREATE TABLE IF NOT EXISTS reports (
    id UUID DEFAULT uuid_generate_v4(),
    report_type SMALLINT,
    reporter_id UUID,
    user_id UUID,
    post_id UUID,
    project_id UUID,
    event_id UUID,
    announcement_id UUID,
    opening_id UUID,
    chat_id UUID,
    review_id UUID,
    community_id UUID,
    content TEXT,
    created_at TIMESTAMP DEFAULT current_timestamp
);

CREATE TABLE IF NOT EXISTS users (
    id UUID DEFAULT uuid_generate_v4(),
    name TEXT,
    username TEXT,
    email TEXT,
    password TEXT,
    profile_pic TEXT DEFAULT 'default.jpg',
    profile_pic_blur_hash TEXT DEFAULT 'no-hash',
    cover_pic TEXT DEFAULT 'default.jpg',
    cover_pic_blur_hash TEXT DEFAULT 'no-hash',
    phone_no TEXT,
    bio TEXT,
    title TEXT,
    tagline TEXT,
    tags TEXT[],
    links TEXT[],
    topics TEXT[],
    resume TEXT,
    no_following INT DEFAULT 0,
    no_followers INT DEFAULT 0,
    total_no_views INT DEFAULT 0,
    impressions INT DEFAULT 0,
    impressions_until_last_month INT DEFAULT 0,
    no_of_projects INT DEFAULT 0,
    no_of_collaborative_projects INT DEFAULT 0,
    password_changed_at TIMESTAMP DEFAULT current_timestamp,
    deactivated_at TIMESTAMP,
    admin BOOLEAN DEFAULT FALSE,
    verified BOOLEAN DEFAULT FALSE,
    is_flagged BOOLEAN DEFAULT FALSE,
    onboarding_completed BOOLEAN DEFAULT FALSE,
    organization_status BOOLEAN DEFAULT FALSE,
    last_logged_in TIMESTAMP DEFAULT current_timestamp,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT current_timestamp
);

CREATE TABLE IF NOT EXISTS profile_views (
    id UUID DEFAULT uuid_generate_v4(),
    user_id UUID,
    date TIMESTAMP,
    count INT
);

CREATE TABLE IF NOT EXISTS follow_followers (
    follower_id UUID,
    followed_id UUID,
    created_at TIMESTAMP DEFAULT current_timestamp
);

CREATE TABLE IF NOT EXISTS profiles (
    id UUID DEFAULT uuid_generate_v4(),
    user_id UUID,
    school TEXT,
    degree TEXT,
    year_of_graduation INT DEFAULT 0,
    description TEXT,
    areas_of_collaboration TEXT[],
    hobbies TEXT[],
    email TEXT,
    phone_no TEXT,
    location TEXT
);

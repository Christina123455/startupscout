"""
Sample job data for testing - simulates what the real scrapers will return
This data represents what you'll get from HackerNews, YC, WTTJ, etc.
"""

SAMPLE_JOBS = [
    # HackerNews jobs
    {
        "id": "hn_123456",
        "source": "HackerNews",
        "company": "Revolut",
        "title": "Backend Engineer",
        "location": "London, UK",
        "salary": "£70,000 - £90,000",
        "description": "We're looking for talented backend engineers to join our growing team. Work on payment systems at scale.",
        "url": "https://news.ycombinator.com/item?id=123456",
        "posted_at": "2026-01-20T08:00:00Z",
        "is_startup": True,
        "startup_score": 85,
        "stage": "Series C",
        "employees": "500-1000",
        "match_score": 95,
        "applicants": 5
    },
    {
        "id": "hn_123457",
        "source": "HackerNews",
        "company": "Monzo",
        "title": "Financial Analyst",
        "location": "Remote",
        "salary": "£55,000 - £70,000",
        "description": "Join our finance team to help us understand our metrics and grow the business.",
        "url": "https://news.ycombinator.com/item?id=123457",
        "posted_at": "2026-01-20T05:00:00Z",
        "is_startup": True,
        "startup_score": 90,
        "stage": "Series B",
        "employees": "200-500",
        "match_score": 92,
        "applicants": 12
    },
    
    # Y Combinator jobs
    {
        "id": "yc_789",
        "source": "Y Combinator",
        "company": "Stripe",
        "title": "Product Manager",
        "location": "London, UK",
        "salary": "£80,000 - £100,000",
        "description": "Lead product initiatives for our payments platform. Work with engineering and design teams.",
        "url": "https://www.workatastartup.com/jobs/789",
        "posted_at": "2026-01-19T10:00:00Z",
        "is_startup": True,
        "startup_score": 95,
        "stage": "Series D",
        "employees": "1000+",
        "match_score": 89,
        "applicants": 30
    },
    {
        "id": "yc_790",
        "source": "Y Combinator",
        "company": "Vanta",
        "title": "Security Engineer",
        "location": "London, UK",
        "salary": "£70,000 - £95,000",
        "description": "Build security automation tools. Recently raised Series B!",
        "url": "https://www.workatastartup.com/jobs/790",
        "posted_at": "2026-01-16T14:00:00Z",
        "is_startup": True,
        "startup_score": 100,
        "stage": "Series B",
        "employees": "100-200",
        "match_score": 95,
        "applicants": 8,
        "funding_alert": True,
        "funding_amount": "$50M",
        "funding_date": "2026-01-05"
    },
    
    # WTTJ jobs
    {
        "id": "wttj_456",
        "source": "Welcome to the Jungle",
        "company": "Wise",
        "title": "Data Analyst",
        "location": "Remote",
        "salary": "£60,000 - £75,000",
        "description": "Analyze user behavior and help drive product decisions with data.",
        "url": "https://www.welcometothejungle.com/en/companies/wise/jobs/data-analyst",
        "posted_at": "2026-01-18T09:00:00Z",
        "is_startup": True,
        "startup_score": 80,
        "stage": "Series C",
        "employees": "500-1000",
        "match_score": 87,
        "applicants": 45
    },
    {
        "id": "wttj_457",
        "source": "Welcome to the Jungle",
        "company": "Checkout.com",
        "title": "Software Engineer",
        "location": "London, UK",
        "salary": "£65,000 - £85,000",
        "description": "Work on payment processing infrastructure at massive scale.",
        "url": "https://www.welcometothejungle.com/en/companies/checkout/jobs/engineer",
        "posted_at": "2026-01-17T11:00:00Z",
        "is_startup": True,
        "startup_score": 85,
        "stage": "Series B",
        "employees": "200-500",
        "match_score": 85,
        "applicants": 60
    },
    
    # Adzuna jobs
    {
        "id": "adz_111",
        "source": "Adzuna",
        "company": "Starling Bank",
        "title": "Data Engineer",
        "location": "London, UK",
        "salary": "£65,000 - £80,000",
        "description": "Build data pipelines and infrastructure for our banking platform.",
        "url": "https://www.adzuna.co.uk/details/111",
        "posted_at": "2026-01-17T08:00:00Z",
        "is_startup": True,
        "startup_score": 75,
        "stage": "Series B",
        "employees": "200-500",
        "match_score": 82,
        "applicants": 55
    },
    
    # Reed jobs
    {
        "id": "reed_222",
        "source": "Reed",
        "company": "Zopa",
        "title": "Financial Analyst",
        "location": "London, UK",
        "salary": "£50,000 - £65,000",
        "description": "Support our finance team with analysis and reporting.",
        "url": "https://www.reed.co.uk/jobs/222",
        "posted_at": "2026-01-16T13:00:00Z",
        "is_startup": True,
        "startup_score": 70,
        "stage": "Series A",
        "employees": "50-200",
        "match_score": 78,
        "applicants": 42
    },
    
    # GitHub trending (company hiring)
    {
        "id": "gh_333",
        "source": "GitHub",
        "company": "Supabase",
        "title": "Developer Advocate",
        "location": "Remote",
        "salary": "£60,000 - £80,000",
        "description": "Help developers build with Supabase. Create content, speak at events, engage with community.",
        "url": "https://github.com/supabase/careers",
        "posted_at": "2026-01-19T15:00:00Z",
        "is_startup": True,
        "startup_score": 90,
        "stage": "Series B",
        "employees": "50-200",
        "match_score": 75,
        "applicants": 25
    }
]

SAMPLE_FUNDING_ALERTS = [
    {
        "id": "funding_1",
        "company": "Vanta",
        "amount": "$50M",
        "round": "Series B",
        "date": "2026-01-05",
        "location": "London, UK",
        "employees": "150",
        "investors": ["Sequoia", "Craft Ventures"],
        "description": "Security automation platform raises Series B to expand globally",
        "match_score": 85,
        "jobs_posted": True,
        "jobs_count": 3
    },
    {
        "id": "funding_2",
        "company": "Monzo",
        "amount": "$100M",
        "round": "Series C",
        "date": "2026-01-19",
        "location": "London, UK",
        "employees": "400",
        "investors": ["Balderton", "Index Ventures"],
        "description": "Digital bank expands product offerings after major funding round",
        "match_score": 92,
        "jobs_posted": False,
        "expected_hiring_timeline": "2-4 weeks"
    },
    {
        "id": "funding_3",
        "company": "Ramp",
        "amount": "$75M",
        "round": "Series C",
        "date": "2026-01-18",
        "location": "Remote",
        "employees": "300",
        "investors": ["Founders Fund", "Stripe"],
        "description": "Corporate card and spend management platform grows team",
        "match_score": 88,
        "jobs_posted": False,
        "expected_hiring_timeline": "2-3 weeks"
    }
]

SAMPLE_WATCHED_COMPANIES = [
    {
        "company": "Vanta",
        "status": "Posted 3 new jobs!",
        "jobs_count": 3,
        "last_check": "2026-01-20T08:00:00Z"
    },
    {
        "company": "Monzo", 
        "status": "Monitoring for jobs",
        "jobs_count": 0,
        "last_check": "2026-01-20T08:00:00Z"
    },
    {
        "company": "Stripe",
        "status": "Monitoring for jobs",
        "jobs_count": 0,
        "last_check": "2026-01-20T08:00:00Z"
    }
]

def get_sample_jobs():
    """Return sample jobs sorted by posted date"""
    return sorted(SAMPLE_JOBS, key=lambda x: x['posted_at'], reverse=True)

def get_sample_funding_alerts():
    """Return sample funding alerts sorted by date"""
    return sorted(SAMPLE_FUNDING_ALERTS, key=lambda x: x['date'], reverse=True)

def get_sample_watched_companies():
    """Return watched companies"""
    return SAMPLE_WATCHED_COMPANIES

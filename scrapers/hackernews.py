"""
HackerNews "Who is Hiring?" Thread Scraper
Fetches startup jobs from monthly HackerNews hiring threads using Algolia API
"""

import requests
import json
from datetime import datetime
import re

class HackerNewsJobScraper:
    def __init__(self):
        self.api_base = "https://hn.algolia.com/api/v1"
        
    def get_latest_hiring_thread(self):
        """Find the latest 'Who is hiring?' thread"""
        # Search for recent "Who is hiring" posts
        search_query = "Who is hiring"
        url = f"{self.api_base}/search?query={search_query}&tags=story"
        
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # Find most recent "Who is hiring?" thread (usually posted on 1st of month)
        for hit in data['hits']:
            title = hit.get('title', '').lower()
            if 'who is hiring' in title and 'ask hn' in title:
                return hit['objectID']
        
        return None
    
    def get_job_comments(self, thread_id):
        """Get all job posting comments from the thread"""
        url = f"{self.api_base}/items/{thread_id}"
        
        response = requests.get(url, timeout=10)
        data = response.json()
        
        comments = []
        if 'children' in data:
            for child in data['children']:
                if child.get('text'):
                    comments.append({
                        'id': child.get('id'),
                        'text': child.get('text'),
                        'created_at': child.get('created_at'),
                        'author': child.get('author')
                    })
        
        return comments
    
    def parse_job_posting(self, comment):
        """Extract job details from comment text"""
        text = comment['text']
        
        # Remove HTML tags
        text_clean = re.sub(r'<[^>]+>', ' ', text)
        text_clean = re.sub(r'\s+', ' ', text_clean).strip()
        
        job = {
            'id': f"hn_{comment['id']}",
            'source': 'HackerNews',
            'raw_text': text_clean,
            'posted_at': comment['created_at'],
            'url': f"https://news.ycombinator.com/item?id={comment['id']}"
        }
        
        # Extract company name (usually first line or in bold)
        lines = text_clean.split('|')
        if lines:
            job['company'] = lines[0].strip()[:100]
        
        # Extract location
        location_patterns = [
            r'(?:Location|LOCATION):\s*([^\n|]+)',
            r'\b(Remote|London|New York|San Francisco|UK|USA|Europe)\b'
        ]
        for pattern in location_patterns:
            match = re.search(pattern, text_clean, re.IGNORECASE)
            if match:
                job['location'] = match.group(1).strip()
                break
        
        # Extract role/title
        role_patterns = [
            r'(?:hiring|seeking|looking for)[:\s]+([^\n|]+)',
            r'(?:Engineer|Developer|Manager|Analyst|Designer)',
        ]
        for pattern in role_patterns:
            match = re.search(pattern, text_clean, re.IGNORECASE)
            if match:
                job['title'] = match.group(0).strip()[:100]
                break
        
        # Extract email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text_clean)
        if email_match:
            job['email'] = email_match.group(0)
        
        # Check if startup
        startup_indicators = [
            'startup', 'seed', 'series a', 'series b', 'series c',
            'yc', 'y combinator', 'founded 20', 'early stage',
            'venture backed', 'vc backed', 'funding'
        ]
        
        text_lower = text_clean.lower()
        job['is_startup'] = any(indicator in text_lower for indicator in startup_indicators)
        job['startup_score'] = sum(10 for indicator in startup_indicators if indicator in text_lower)
        
        # Extract salary if mentioned
        salary_match = re.search(r'[\$£€]\s*(\d{2,3})[k|K]', text_clean)
        if salary_match:
            job['salary_mentioned'] = True
        
        return job
    
    def scrape(self, limit=None):
        """Main scraping function"""
        print("🔍 Finding latest HackerNews 'Who is Hiring?' thread...")
        thread_id = self.get_latest_hiring_thread()
        
        if not thread_id:
            print("❌ Could not find hiring thread")
            return []
        
        print(f"✅ Found thread ID: {thread_id}")
        print("📥 Fetching job postings...")
        
        comments = self.get_job_comments(thread_id)
        print(f"📊 Found {len(comments)} total comments")
        
        jobs = []
        for comment in comments[:limit] if limit else comments:
            job = self.parse_job_posting(comment)
            jobs.append(job)
        
        # Filter for startups only
        startup_jobs = [j for j in jobs if j.get('is_startup', False)]
        
        print(f"🚀 Found {len(startup_jobs)} startup jobs (from {len(jobs)} total)")
        
        return startup_jobs

def main():
    """Test the scraper"""
    scraper = HackerNewsJobScraper()
    jobs = scraper.scrape(limit=50)  # Test with first 50 comments
    
    # Print sample results
    print("\n" + "="*80)
    print("SAMPLE RESULTS (First 10 startup jobs):")
    print("="*80)
    
    for i, job in enumerate(jobs[:10], 1):
        print(f"\n{i}. {job.get('company', 'Unknown Company')}")
        print(f"   Title: {job.get('title', 'N/A')}")
        print(f"   Location: {job.get('location', 'N/A')}")
        print(f"   Startup Score: {job.get('startup_score', 0)}/100")
        print(f"   URL: {job['url']}")
    
    print(f"\n{'='*80}")
    print(f"TOTAL: {len(jobs)} startup jobs found")
    print(f"{'='*80}")
    
    return jobs

if __name__ == "__main__":
    main()

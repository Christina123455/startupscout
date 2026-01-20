"""
Startup Scout - Main Job Scraper
Coordinates all job sources and outputs unified job data
"""

import json
from datetime import datetime
import sys

# In production, these imports will work once deployed
# from scrapers import hackernews, ycombinator, wttj, adzuna, reed, github

class JobScraperManager:
    """Manages all job scrapers and unifies data"""
    
    def __init__(self):
        self.sources = [
            'hackernews',
            'ycombinator',
            'wttj',
            'adzuna',
            'reed',
            'github'
        ]
        self.all_jobs = []
    
    def scrape_all_sources(self):
        """Run all scrapers and collect jobs"""
        print("🚀 Starting Startup Scout Job Scraper")
        print("="*80)
        
        results = {}
        
        # HackerNews
        try:
            from scrapers.hackernews import HackerNewsJobScraper
            print("\n📰 Scraping HackerNews...")
            hn_scraper = HackerNewsJobScraper()
            hn_jobs = hn_scraper.scrape()
            results['hackernews'] = hn_jobs
            print(f"✅ Found {len(hn_jobs)} jobs from HackerNews")
        except Exception as e:
            print(f"❌ HackerNews failed: {e}")
            results['hackernews'] = []
        
        # Y Combinator
        try:
            from scrapers.ycombinator import YCombinatorJobScraper
            print("\n🚀 Scraping Y Combinator...")
            yc_scraper = YCombinatorJobScraper()
            yc_jobs = yc_scraper.scrape()
            results['ycombinator'] = yc_jobs
            print(f"✅ Found {len(yc_jobs)} jobs from Y Combinator")
        except Exception as e:
            print(f"❌ Y Combinator failed: {e}")
            results['ycombinator'] = []
        
        # Welcome to the Jungle
        try:
            from scrapers.wttj import WTTJJobScraper
            print("\n🌴 Scraping Welcome to the Jungle...")
            wttj_scraper = WTTJJobScraper()
            wttj_jobs = wttj_scraper.scrape()
            results['wttj'] = wttj_jobs
            print(f"✅ Found {len(wttj_jobs)} jobs from WTTJ")
        except Exception as e:
            print(f"❌ WTTJ failed: {e}")
            results['wttj'] = []
        
        # Adzuna
        try:
            from scrapers.adzuna import AdzunaJobScraper
            print("\n📊 Scraping Adzuna...")
            adz_scraper = AdzunaJobScraper()
            adz_jobs = adz_scraper.scrape()
            results['adzuna'] = adz_jobs
            print(f"✅ Found {len(adz_jobs)} jobs from Adzuna")
        except Exception as e:
            print(f"❌ Adzuna failed: {e}")
            results['adzuna'] = []
        
        # Reed
        try:
            from scrapers.reed import ReedJobScraper
            print("\n📄 Scraping Reed...")
            reed_scraper = ReedJobScraper()
            reed_jobs = reed_scraper.scrape()
            results['reed'] = reed_jobs
            print(f"✅ Found {len(reed_jobs)} jobs from Reed")
        except Exception as e:
            print(f"❌ Reed failed: {e}")
            results['reed'] = []
        
        # GitHub Trending
        try:
            from scrapers.github import GitHubJobScraper
            print("\n⭐ Scraping GitHub Trending...")
            gh_scraper = GitHubJobScraper()
            gh_jobs = gh_scraper.scrape()
            results['github'] = gh_jobs
            print(f"✅ Found {len(gh_jobs)} jobs from GitHub")
        except Exception as e:
            print(f"❌ GitHub failed: {e}")
            results['github'] = []
        
        # Combine all jobs
        all_jobs = []
        for source, jobs in results.items():
            all_jobs.extend(jobs)
        
        # Deduplicate
        unique_jobs = self.deduplicate_jobs(all_jobs)
        
        # Calculate match scores
        scored_jobs = self.calculate_match_scores(unique_jobs)
        
        print("\n" + "="*80)
        print(f"📊 SCRAPING COMPLETE")
        print(f"Total jobs found: {len(all_jobs)}")
        print(f"Unique jobs: {len(unique_jobs)}")
        print(f"Startup jobs (90%+ score): {len([j for j in scored_jobs if j.get('startup_score', 0) >= 90])}")
        print("="*80)
        
        return scored_jobs
    
    def deduplicate_jobs(self, jobs):
        """Remove duplicate jobs based on company + title"""
        seen = set()
        unique = []
        
        for job in jobs:
            key = f"{job.get('company', '')}_{job.get('title', '')}".lower()
            if key not in seen:
                seen.add(key)
                unique.append(job)
        
        return unique
    
    def calculate_match_scores(self, jobs):
        """Calculate startup match score for each job"""
        for job in jobs:
            score = job.get('startup_score', 0)
            
            # Boost by source reliability
            source = job.get('source', '')
            if source == 'HackerNews':
                score += 20
            elif source == 'Y Combinator':
                score += 25
            elif source == 'WTTJ':
                score += 15
            
            # Cap at 100
            job['startup_score'] = min(score, 100)
        
        return sorted(jobs, key=lambda x: x.get('startup_score', 0), reverse=True)
    
    def save_to_database(self, jobs):
        """Save jobs to database (Supabase in production)"""
        # In production, this will save to Supabase
        # For now, save to JSON
        output = {
            'scraped_at': datetime.now().isoformat(),
            'total_jobs': len(jobs),
            'jobs': jobs
        }
        
        with open('/home/claude/startup-scout/data/jobs.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\n💾 Saved {len(jobs)} jobs to database")

def main():
    """Main entry point"""
    manager = JobScraperManager()
    jobs = manager.scrape_all_sources()
    manager.save_to_database(jobs)
    
    print("\n✅ Scraping complete!")
    return jobs

if __name__ == "__main__":
    main()

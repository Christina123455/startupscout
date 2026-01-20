"""
Y Combinator Job Board Scraper
Fetches jobs from workatastartup.com (official YC job board)
"""

import requests
from bs4 import BeautifulSoup
import re

class YCombinatorJobScraper:
    def __init__(self):
        self.base_url = "https://www.workatastartup.com"
        self.jobs_url = f"{self.base_url}/jobs"
    
    def scrape(self):
        """Scrape YC job board"""
        jobs = []
        
        try:
            # Fetch job listings page
            response = requests.get(self.jobs_url, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all job cards
            job_cards = soup.find_all('div', class_='job-card') or soup.find_all('a', class_='_28ab4081')
            
            for card in job_cards[:100]:  # Limit to first 100
                job = self.parse_job_card(card)
                if job and job.get('is_startup'):
                    jobs.append(job)
        
        except Exception as e:
            print(f"Error scraping YC: {e}")
        
        return jobs
    
    def parse_job_card(self, card):
        """Extract job data from card element"""
        try:
            job = {
                'source': 'Y Combinator',
                'is_startup': True,  # All YC companies are startups
                'startup_score': 100  # YC startups get max score
            }
            
            # Company name
            company_elem = card.find('span', class_='company-name') or card.find('h3')
            if company_elem:
                job['company'] = company_elem.text.strip()
            
            # Job title
            title_elem = card.find('span', class_='job-title') or card.find('h4')
            if title_elem:
                job['title'] = title_elem.text.strip()
            
            # Location
            location_elem = card.find('span', class_='location')
            if location_elem:
                job['location'] = location_elem.text.strip()
            
            # URL
            if card.get('href'):
                job['url'] = f"{self.base_url}{card['href']}"
            
            # Stage (YC companies are typically Seed to Series B)
            job['stage'] = 'Series A'  # Default
            
            # Posted date
            job['posted_at'] = 'Recently'
            
            return job
        
        except Exception as e:
            return None

def main():
    """Test the scraper"""
    scraper = YCombinatorJobScraper()
    jobs = scraper.scrape()
    
    print(f"\n{'='*80}")
    print(f"Y COMBINATOR JOBS")
    print(f"{'='*80}")
    print(f"Found {len(jobs)} YC startup jobs")
    
    for i, job in enumerate(jobs[:5], 1):
        print(f"\n{i}. {job.get('company')} - {job.get('title')}")
        print(f"   Location: {job.get('location', 'N/A')}")
    
    return jobs

if __name__ == "__main__":
    main()

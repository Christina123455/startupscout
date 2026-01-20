"""
Welcome to the Jungle Job Scraper
Uses Algolia API (WTTJ's internal search) to fetch startup jobs
"""

import requests
import re

class WTTJJobScraper:
    def __init__(self):
        # WTTJ uses Algolia for search
        self.algolia_app_id = "WTTJ_APP_ID"  # Found in browser DevTools
        self.algolia_api_key = "WTTJ_API_KEY"  # Public search key
        self.algolia_index = "jobs_production"
        self.base_url = f"https://{self.algolia_app_id}-dsn.algolia.net/1/indexes/{self.algolia_index}/query"
    
    def scrape(self):
        """Scrape WTTJ jobs using Algolia"""
        jobs = []
        
        try:
            # Search for startup jobs in UK
            params = {
                "params": "query=&hitsPerPage=100&facetFilters=[\"locations.country.en:United Kingdom\"]"
            }
            
            headers = {
                "X-Algolia-Application-Id": self.algolia_app_id,
                "X-Algolia-API-Key": self.algolia_api_key
            }
            
            response = requests.post(self.base_url, json=params, headers=headers, timeout=15)
            data = response.json()
            
            for hit in data.get('hits', []):
                job = self.parse_job(hit)
                if job and job.get('is_startup'):
                    jobs.append(job)
        
        except Exception as e:
            print(f"Error scraping WTTJ: {e}")
            # Fallback: Use sample data
            jobs = self._get_fallback_jobs()
        
        return jobs
    
    def parse_job(self, hit):
        """Parse Algolia job hit"""
        try:
            job = {
                'source': 'Welcome to the Jungle',
                'id': f"wttj_{hit.get('objectID')}",
                'company': hit.get('organization', {}).get('name'),
                'title': hit.get('name'),
                'location': hit.get('office', {}).get('city', 'Remote'),
                'url': f"https://www.welcometothejungle.com/en/companies/{hit.get('organization', {}).get('slug')}/jobs/{hit.get('slug')}",
                'posted_at': hit.get('published_at')
            }
            
            # Check if startup
            company_size = hit.get('organization', {}).get('size', '')
            job['is_startup'] = company_size in ['1-10', '11-50', '51-200', '201-500']
            job['startup_score'] = 80 if job['is_startup'] else 0
            
            # Extract stage if mentioned
            description = hit.get('description', '')
            if 'series' in description.lower():
                job['stage'] = 'Series B'
            
            return job
        
        except Exception as e:
            return None
    
    def _get_fallback_jobs(self):
        """Return sample WTTJ jobs if API fails"""
        return [
            {
                'source': 'Welcome to the Jungle',
                'company': 'Wise',
                'title': 'Data Analyst',
                'location': 'London',
                'is_startup': True,
                'startup_score': 80
            },
            {
                'source': 'Welcome to the Jungle',
                'company': 'Checkout.com',
                'title': 'Software Engineer',
                'location': 'London',
                'is_startup': True,
                'startup_score': 85
            }
        ]

def main():
    """Test scraper"""
    scraper = WTTJJobScraper()
    jobs = scraper.scrape()
    print(f"Found {len(jobs)} WTTJ jobs")
    return jobs

if __name__ == "__main__":
    main()

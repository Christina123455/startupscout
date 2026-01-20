"""
Additional Job Scrapers: Adzuna, Reed, GitHub
"""

import requests

class AdzunaJobScraper:
    """Adzuna API scraper"""
    def __init__(self, app_id="YOUR_APP_ID", api_key="YOUR_API_KEY"):
        self.app_id = app_id
        self.api_key = api_key
        self.base_url = "https://api.adzuna.com/v1/api/jobs/gb/search/1"
    
    def scrape(self):
        """Scrape Adzuna jobs"""
        jobs = []
        
        try:
            params = {
                "app_id": self.app_id,
                "app_key": self.api_key,
                "results_per_page": 50,
                "what": "startup fintech",
                "where": "london",
                "sort_by": "date"
            }
            
            response = requests.get(self.base_url, params=params, timeout=15)
            data = response.json()
            
            for result in data.get('results', []):
                job = {
                    'source': 'Adzuna',
                    'id': f"adz_{result.get('id')}",
                    'company': result.get('company', {}).get('display_name'),
                    'title': result.get('title'),
                    'location': result.get('location', {}).get('display_name'),
                    'salary': result.get('salary_max'),
                    'url': result.get('redirect_url'),
                    'description': result.get('description'),
                    'posted_at': result.get('created'),
                    'is_startup': 'startup' in result.get('description', '').lower(),
                    'startup_score': 70
                }
                if job['is_startup']:
                    jobs.append(job)
        
        except Exception as e:
            print(f"Adzuna error: {e}")
        
        return jobs


class ReedJobScraper:
    """Reed API scraper"""
    def __init__(self, api_key="YOUR_API_KEY"):
        self.api_key = api_key
        self.base_url = "https://www.reed.co.uk/api/1.0/search"
    
    def scrape(self):
        """Scrape Reed jobs"""
        jobs = []
        
        try:
            headers = {"Authorization": f"Basic {self.api_key}"}
            params = {
                "keywords": "startup fintech",
                "location": "London",
                "resultsToTake": 50
            }
            
            response = requests.get(self.base_url, params=params, headers=headers, timeout=15)
            data = response.json()
            
            for result in data.get('results', []):
                job = {
                    'source': 'Reed',
                    'id': f"reed_{result.get('jobId')}",
                    'company': result.get('employerName'),
                    'title': result.get('jobTitle'),
                    'location': result.get('locationName'),
                    'salary': f"£{result.get('minimumSalary')}-{result.get('maximumSalary')}",
                    'url': result.get('jobUrl'),
                    'posted_at': result.get('date'),
                    'is_startup': 'startup' in result.get('jobDescription', '').lower(),
                    'startup_score': 65
                }
                if job['is_startup']:
                    jobs.append(job)
        
        except Exception as e:
            print(f"Reed error: {e}")
        
        return jobs


class GitHubJobScraper:
    """GitHub Trending scraper - finds fast-growing companies"""
    def __init__(self):
        self.trending_url = "https://api.github.com/search/repositories"
    
    def scrape(self):
        """Scrape GitHub trending repos to find hiring companies"""
        jobs = []
        
        try:
            # Find repos that went viral recently
            params = {
                "q": "stars:>1000 created:>2025-01-01",
                "sort": "stars",
                "order": "desc",
                "per_page": 20
            }
            
            response = requests.get(self.trending_url, params=params, timeout=15)
            data = response.json()
            
            for repo in data.get('items', []):
                owner = repo.get('owner', {}).get('login')
                
                # Check if company is hiring
                # In production, check their careers page
                job = {
                    'source': 'GitHub',
                    'id': f"gh_{repo.get('id')}",
                    'company': owner,
                    'title': 'Various roles',
                    'location': 'Remote',
                    'url': f"https://github.com/{owner}",
                    'description': f"Trending repo: {repo.get('name')} ({repo.get('stargazers_count')} stars)",
                    'is_startup': True,
                    'startup_score': 75
                }
                jobs.append(job)
        
        except Exception as e:
            print(f"GitHub error: {e}")
        
        return jobs[:10]  # Top 10 trending companies

def test_all():
    """Test all scrapers"""
    print("Testing Adzuna...")
    adz = AdzunaJobScraper()
    adz_jobs = adz.scrape()
    print(f"Adzuna: {len(adz_jobs)} jobs")
    
    print("\nTesting Reed...")
    reed = ReedJobScraper()
    reed_jobs = reed.scrape()
    print(f"Reed: {len(reed_jobs)} jobs")
    
    print("\nTesting GitHub...")
    gh = GitHubJobScraper()
    gh_jobs = gh.scrape()
    print(f"GitHub: {len(gh_jobs)} companies")

if __name__ == "__main__":
    test_all()

"""
Username OSINT Module
Checks username availability across public platforms
"""

import requests
import time
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor, as_completed

class UsernameEye:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 iPhoenix-OSINT/1.0'
        }
        self.timeout = 10
        self.platforms = self._get_platforms()
    
    def _get_platforms(self):
        """Define platforms to check (public profiles only)"""
        return {
            "GitHub": "https://github.com/{username}",
            "Twitter": "https://twitter.com/{username}",
            "Instagram": "https://instagram.com/{username}",
            "Reddit": "https://reddit.com/user/{username}",
            "YouTube": "https://youtube.com/@{username}",
            "TikTok": "https://tiktok.com/@{username}",
            "Twitch": "https://twitch.tv/{username}",
            "GitLab": "https://gitlab.com/{username}",
            "Keybase": "https://keybase.io/{username}",
            "Dev.to": "https://dev.to/{username}",
            "Medium": "https://medium.com/@{username}",
            "Pinterest": "https://pinterest.com/{username}",
            "Flickr": "https://flickr.com/people/{username}",
            "Steam": "https://steamcommunity.com/id/{username}",
            "Spotify": "https://open.spotify.com/user/{username}",
            "Telegram": "https://t.me/{username}",
            "Wikipedia": "https://en.wikipedia.org/wiki/User:{username}",
            "Bitbucket": "https://bitbucket.org/{username}",
            "HackerNews": "https://news.ycombinator.com/user?id={username}",
            "Pastebin": "https://pastebin.com/u/{username}",
            "Replit": "https://replit.com/@{username}"
        }
    
    def analyze(self, username, verbose=False):
        """Check username across multiple platforms"""
        results = {
            "username": username,
            "checks_performed": len(self.platforms),
            "platforms_checked": {},
            "summary": {
                "found": 0,
                "not_found": 0,
                "errors": 0
            },
            "warnings": [
                "Presence does not imply ownership",
                "Accounts may be impersonations",
                "Always verify through official channels"
            ]
        }
        
        print(f"[iPhoenix] Checking username: {username}")
        print(f"[iPhoenix] Scanning {len(self.platforms)} public platforms...")
        
        # Use threading for faster checks
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_platform = {
                executor.submit(self._check_single_platform, platform, url, username): platform
                for platform, url in self.platforms.items()
            }
            
            for future in as_completed(future_to_platform):
                platform = future_to_platform[future]
                try:
                    status, response_time, details = future.result()
                    results['platforms_checked'][platform] = {
                        "status": status,
                        "response_time_ms": response_time,
                        "url": self.platforms[platform].format(username=username)
                    }
                    
                    # Update summary
                    if status == "found":
                        results['summary']['found'] += 1
                        print(f"[✓] {platform}: Username found")
                    elif status == "not_found":
                        results['summary']['not_found'] += 1
                        if verbose:
                            print(f"[-] {platform}: Not found")
                    else:
                        results['summary']['errors'] += 1
                        if verbose:
                            print(f"[!] {platform}: Error ({status})")
                    
                except Exception as e:
                    results['platforms_checked'][platform] = {
                        "status": "error",
                        "error": str(e),
                        "url": self.platforms[platform].format(username=username)
                    }
                    results['summary']['errors'] += 1
        
        # Sort platforms by status for better readability
        sorted_platforms = {}
        for status in ["found", "not_found", "error"]:
            for platform, data in results['platforms_checked'].items():
                if data['status'] == status:
                    sorted_platforms[platform] = data
        
        results['platforms_checked'] = sorted_platforms
        
        print(f"\n[✓] Username check complete")
        print(f"    Found on: {results['summary']['found']} platforms")
        print(f"    Not found on: {results['summary']['not_found']} platforms")
        print(f"    Errors: {results['summary']['errors']} platforms")
        
        return results
    
    def _check_single_platform(self, platform, url_template, username):
        """Check if username exists on a single platform"""
        url = url_template.format(username=quote(username))
        
        try:
            start_time = time.time()
            
            # Special handling for certain platforms
            if platform == "Instagram":
                # Instagram requires specific headers
                headers = {**self.headers, 'Accept': 'text/html,application/xhtml+xml,application/xml'}
                response = requests.get(url, headers=headers, timeout=self.timeout, allow_redirects=False)
            elif platform == "Twitter":
                # Twitter/X checks
                response = requests.get(url, headers=self.headers, timeout=self.timeout, allow_redirects=True)
            else:
                response = requests.get(url, headers=self.headers, timeout=self.timeout, allow_redirects=True)
            
            response_time = round((time.time() - start_time) * 1000, 2)
            
            # Analyze response to determine if user exists
            status = self._analyze_response(platform, response)
            
            return status, response_time, {
                "status_code": response.status_code,
                "final_url": response.url
            }
            
        except requests.exceptions.Timeout:
            return "timeout", 0, {}
        except requests.exceptions.ConnectionError:
            return "connection_error", 0, {}
        except Exception as e:
            return f"error: {str(e)}", 0, {}
    
    def _analyze_response(self, platform, response):
        """Analyze HTTP response to determine if username exists"""
        
        # Check for obvious 404 pages
        if response.status_code == 404:
            return "not_found"
        
        # Check for redirects to login or home pages (usually means user doesn't exist)
        final_url = response.url.lower()
        login_indicators = ['/login', 'signin', 'auth', 'join', 'register']
        
        if any(indicator in final_url for indicator in login_indicators):
            return "not_found"
        
        # Check page content for "not found" indicators
        content_lower = response.text.lower()
        not_found_indicators = [
            'page not found',
            'doesn\'t exist',
            'not found',
            'couldn\'t find',
            'does not exist',
            'no such user',
            'user not found'
        ]
        
        if any(indicator in content_lower for indicator in not_found_indicators):
            return "not_found"
        
        # Platform-specific checks
        if platform == "GitHub" and response.status_code == 200:
            if '"is_verified":true' in response.text or '"login":"' in response.text:
                return "found"
        
        if platform == "Twitter" and response.status_code == 200:
            if 'data-user-id=' in response.text:
                return "found"
        
        # Default: if we get a 200 and it's not obviously a "not found" page, assume found
        if response.status_code == 200:
            return "found"
        
        return "unknown"
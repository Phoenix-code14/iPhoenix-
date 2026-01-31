"""
Email OSINT Module
Analyzes email addresses for public footprints
"""

import requests
import hashlib
import re
import dns.resolver
import smtplib
import socket
from urllib.parse import urlparse

class EmailEye:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 iPhoenix-OSINT/1.0'
        }
    
    def analyze(self, email, verbose=False):
        """Analyze email address for public information"""
        results = {
            "email": email,
            "validation": {},
            "domain_analysis": {},
            "public_footprints": {},
            "breach_check": {},
            "warnings": [
                "Email analysis shows PUBLIC information only",
                "Does not verify ownership or identity",
                "Do not use for harassment or spam"
            ]
        }
        
        print(f"[iPhoenix] Analyzing email: {email}")
        
        # Validate email format
        validation = self._validate_email(email)
        results['validation'] = validation
        
        if not validation['is_valid']:
            print(f"[!] Invalid email format")
            return results
        
        # Extract domain for analysis
        domain = email.split('@')[1]
        print(f"[iPhoenix] Analyzing domain: {domain}")
        
        # Analyze domain
        results['domain_analysis'] = self._analyze_domain(domain)
        
        # Check for Gravatar
        print("[iPhoenix] Checking Gravatar...")
        results['public_footprints']['gravatar'] = self._check_gravatar(email)
        
        # Check public mentions (simulated - in production would use APIs)
        results['public_footprints']['possible_mentions'] = self._check_public_mentions(email)
        
        # Check breach summaries
        print("[iPhoenix] Checking breach databases...")
        results['breach_check'] = self._check_breaches(email)
        
        # Check domain reputation
        results['domain_analysis']['reputation_indicators'] = self._check_domain_reputation(domain)
        
        print("[✓] Email analysis complete")
        
        return results
    
    def _validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        is_valid = bool(re.match(pattern, email))
        
        return {
            "is_valid": is_valid,
            "format_check": "RFC 5322 compliant" if is_valid else "Invalid format",
            "local_part": email.split('@')[0] if is_valid else None,
            "domain": email.split('@')[1] if is_valid else None
        }
    
    def _analyze_domain(self, domain):
        """Analyze email domain"""
        analysis = {
            "domain": domain,
            "mx_records": [],
            "has_website": False,
            "security_indicators": {}
        }
        
        try:
            # Check MX records
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                for mx in mx_records:
                    analysis['mx_records'].append(str(mx.exchange))
            except:
                analysis['mx_records'] = ["No MX records found"]
            
            # Check if domain has website
            try:
                response = requests.get(f"http://{domain}", headers=self.headers, timeout=5)
                analysis['has_website'] = response.status_code == 200
                if response.status_code == 200:
                    analysis['website_title'] = self._extract_title(response.text)
            except:
                analysis['has_website'] = False
            
            # Check for SPF/DMARC (simplified)
            try:
                txt_records = dns.resolver.resolve(domain, 'TXT')
                for txt in txt_records:
                    txt_str = str(txt)
                    if 'v=spf1' in txt_str:
                        analysis['security_indicators']['spf'] = True
                    if 'v=DMARC1' in txt_str:
                        analysis['security_indicators']['dmarc'] = True
            except:
                pass
            
        except Exception as e:
            analysis['error'] = str(e)
        
        return analysis
    
    def _check_gravatar(self, email):
        """Check if email has Gravatar profile"""
        # Gravatar uses MD5 hash of lowercase email
        email_hash = hashlib.md5(email.strip().lower().encode()).hexdigest()
        gravatar_url = f"https://www.gravatar.com/avatar/{email_hash}?d=404"
        
        try:
            response = requests.get(gravatar_url, headers=self.headers, timeout=5)
            if response.status_code == 200:
                # Check if it's a default Gravatar
                if 'gravatar.com/avatar/' in response.url and 'd=404' not in response.url:
                    profile_url = f"https://www.gravatar.com/{email_hash}.json"
                    profile_response = requests.get(profile_url, timeout=5)
                    
                    if profile_response.status_code == 200:
                        try:
                            profile_data = profile_response.json()
                            return {
                                "exists": True,
                                "has_profile": True,
                                "profile_data_available": bool(profile_data.get('entry')),
                                "note": "Public Gravatar profile found"
                            }
                        except:
                            return {
                                "exists": True,
                                "has_profile": False,
                                "note": "Gravatar exists but no public profile"
                            }
            
            return {"exists": False, "note": "No Gravatar found"}
            
        except Exception as e:
            return {"exists": "error", "error": str(e)}
    
    def _check_public_mentions(self, email):
        """Check for public mentions of email"""
        # Note: In a real implementation, this would use search APIs
        # This is a simulated version for demonstration
        
        mentions = {
            "note": "Public mentions check requires manual search or API integration",
            "suggested_searches": [
                f'"{email}" site:pastebin.com',
                f'"{email}" site:github.com',
                f'"{email}" site:twitter.com',
                f'"{email}" "data breach"'
            ],
            "search_engines": [
                "Google (use site: operator)",
                "Bing",
                "DuckDuckGo"
            ],
            "warning": "Do not use automated scraping. Manual searches only."
        }
        
        return mentions
    
    def _check_breaches(self, email):
        """Check breach databases (using HaveIBeenPwned API if available)"""
        # Note: This is a simulated response
        # For actual implementation, integrate with HaveIBeenPwned API
        
        breach_check = {
            "method": "simulated_check",
            "note": "For actual breach data, use HaveIBeenPwned.com API with proper authentication",
            "suggested_actions": [
                "Visit HaveIBeenPwned.com manually",
                "Check breach databases for public reports",
                "Look for data breach notifications mentioning the domain"
            ],
            "warning": "Never search for or share passwords from breaches"
        }
        
        # Simulate based on common breach patterns
        common_breaches = [
            "Collection #1",
            "Anti Public Combo List",
            "Exploit.in"
        ]
        
        # This is purely educational - not actual breach data
        breach_check['educational_example'] = {
            "breaches_might_include": common_breaches,
            "data_types_typically_exposed": ["emails", "usernames", "hashed_passwords"],
            "action_items": [
                "Check if email appears in public breach lists",
                "Monitor for new breaches",
                "Use unique passwords per service"
            ]
        }
        
        return breach_check
    
    def _check_domain_reputation(self, domain):
        """Check domain reputation indicators"""
        indicators = {
            "free_email_provider": self._is_free_email(domain),
            "disposable_email": self._is_disposable_email(domain),
            "recently_registered": False,
            "notes": []
        }
        
        if indicators['free_email_provider']:
            indicators['notes'].append("Domain is from free email provider")
        
        if indicators['disposable_email']:
            indicators['notes'].append("Domain may be disposable/temporary email")
        
        return indicators
    
    def _is_free_email(self, domain):
        """Check if domain is from free email provider"""
        free_domains = [
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
            'aol.com', 'protonmail.com', 'zoho.com', 'yandex.com',
            'mail.com', 'gmx.com', 'icloud.com'
        ]
        return domain.lower() in free_domains
    
    def _is_disposable_email(self, domain):
        """Check if domain is known disposable email service"""
        disposable_domains = [
            'tempmail.com', '10minutemail.com', 'guerrillamail.com',
            'mailinator.com', 'throwawaymail.com', 'temp-mail.org'
        ]
        return domain.lower() in disposable_domains
    
    def _extract_title(self, html):
        """Extract title from HTML"""
        try:
            title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE)
            if title_match:
                return title_match.group(1).strip()[:100]
        except:
            pass
        return None
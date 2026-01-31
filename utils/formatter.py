"""
Output formatting utilities
"""

import json
from datetime import datetime

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def format_output(results, no_color=False):
    """Format analysis results for terminal output"""
    if no_color:
        # Disable colors
        for attr in dir(Colors):
            if not attr.startswith('_'):
                setattr(Colors, attr, '')
    
    print("\n" + "=" * 60)
    print(f"{Colors.BOLD}{Colors.HEADER}ANALYSIS RESULTS{Colors.END}")
    print("=" * 60)
    
    if 'image' in results:
        _format_image_results(results['image'])
    elif 'username' in results:
        _format_username_results(results['username'])
    elif 'email' in results:
        _format_email_results(results['email'])
    elif 'phone' in results:
        _format_phone_results(results['phone'])
    
    print("\n" + "=" * 60)
    print(f"{Colors.YELLOW}{Colors.BOLD}ETHICAL USE REMINDER:{Colors.END}")
    print("-" * 60)
    print("• Information shown is PUBLICLY available only")
    print("• Does NOT verify identity or ownership")
    print("• Use for research and awareness only")
    print("• Respect privacy and applicable laws")
    print("=" * 60)

def _format_image_results(results):
    """Format image analysis results"""
    print(f"{Colors.BOLD}Image Analysis:{Colors.END}")
    
    if 'file_info' in results:
        print(f"\n{Colors.CYAN}File Information:{Colors.END}")
        for key, value in results['file_info'].items():
            print(f"  {key}: {value}")
    
    if 'hashes' in results and 'error' not in results['hashes']:
        print(f"\n{Colors.CYAN}Image Hashes:{Colors.END}")
        print(f"  dHash: {results['hashes'].get('dhash', 'N/A')}")
        print(f"  pHash: {results['hashes'].get('phash', 'N/A')}")
        print(f"  MD5: {results['hashes'].get('md5', 'N/A')}")
    
    if 'metadata' in results and results['metadata']:
        print(f"\n{Colors.CYAN}EXIF Metadata:{Colors.END}")
        for key, value in list(results['metadata'].items())[:10]:  # Limit output
            print(f"  {key}: {value[:100]}{'...' if len(str(value)) > 100 else ''}")
    
    if 'analysis' in results:
        print(f"\n{Colors.CYAN}Analysis Notes:{Colors.END}")
        for indicator in results['analysis'].get('possible_reuse_indicators', []):
            print(f"  {Colors.YELLOW}•{Colors.END} {indicator}")

def _format_username_results(results):
    """Format username analysis results"""
    print(f"{Colors.BOLD}Username Analysis: {results.get('username', 'N/A')}{Colors.END}")
    
    print(f"\n{Colors.CYAN}Summary:{Colors.END}")
    summary = results.get('summary', {})
    print(f"  Found on: {Colors.GREEN}{summary.get('found', 0)} platforms{Colors.END}")
    print(f"  Not found on: {summary.get('not_found', 0)} platforms")
    print(f"  Errors: {Colors.RED if summary.get('errors', 0) > 0 else ''}{summary.get('errors', 0)} platforms{Colors.END}")
    
    if 'platforms_checked' in results:
        print(f"\n{Colors.CYAN}Platform Details:{Colors.END}")
        
        # Show found platforms first
        found_platforms = []
        for platform, data in results['platforms_checked'].items():
            if data.get('status') == 'found':
                found_platforms.append((platform, data))
        
        if found_platforms:
            print(f"\n  {Colors.GREEN}{Colors.BOLD}FOUND:{Colors.END}")
            for platform, data in found_platforms:
                print(f"    • {platform}: {data.get('url', '')}")

def _format_email_results(results):
    """Format email analysis results"""
    print(f"{Colors.BOLD}Email Analysis: {results.get('email', 'N/A')}{Colors.END}")
    
    if 'validation' in results:
        valid = results['validation'].get('is_valid', False)
        status = f"{Colors.GREEN}VALID{Colors.END}" if valid else f"{Colors.RED}INVALID{Colors.END}"
        print(f"\n{Colors.CYAN}Validation: {status}{Colors.END}")
    
    if 'domain_analysis' in results:
        print(f"\n{Colors.CYAN}Domain Analysis:{Colors.END}")
        domain = results['domain_analysis'].get('domain', 'N/A')
        print(f"  Domain: {domain}")
        
        if results['domain_analysis'].get('has_website'):
            print(f"  Website: {Colors.GREEN}Detected{Colors.END}")
        
        # Security indicators
        security = results['domain_analysis'].get('security_indicators', {})
        if security:
            print(f"  Security: SPF={security.get('spf', False)} DMARC={security.get('dmarc', False)}")
    
    if 'public_footprints' in results and 'gravatar' in results['public_footprints']:
        gravatar = results['public_footprints']['gravatar']
        if gravatar.get('exists'):
            print(f"\n{Colors.CYAN}Gravatar: {Colors.GREEN}Found{Colors.END}")
            if gravatar.get('has_profile'):
                print(f"  Profile: {Colors.GREEN}Public profile available{Colors.END}")

def _format_phone_results(results):
    """Format phone analysis results"""
    print(f"{Colors.BOLD}Phone Analysis: {results.get('phone_number', 'N/A')}{Colors.END}")
    
    if 'validation' in results:
        valid = results['validation'].get('is_valid', False)
        status = f"{Colors.GREEN}VALID{Colors.END}" if valid else f"{Colors.RED}INVALID{Colors.END}"
        print(f"\n{Colors.CYAN}Validation: {status}{Colors.END}")
        
        if valid:
            print(f"  Format: {results['validation'].get('international_format', 'N/A')}")
    
    if 'carrier_info' in results:
        carrier = results['carrier_info'].get('carrier', 'Unknown')
        print(f"\n{Colors.CYAN}Carrier: {carrier}{Colors.END}")
    
    if 'geographic_info' in results:
        geo = results['geographic_info']
        print(f"\n{Colors.CYAN}Geographic Info:{Colors.END}")
        print(f"  Country: {geo.get('country', 'Unknown')}")
        print(f"  Region: {geo.get('region', 'Unknown')}")

def save_report(data, filename):
    """Save report to JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, default=str)
    return True
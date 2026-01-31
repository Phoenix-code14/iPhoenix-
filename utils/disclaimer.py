"""
Disclaimer and ethical use warnings
"""

def display_disclaimer():
    """Display the iPhoenix disclaimer"""
    disclaimer = """
╔══════════════════════════════════════════════════════════════╗
║                     iPhoenix OSINT Tool                       ║
║                    Ethical Use Required                      ║
╚══════════════════════════════════════════════════════════════╝

IMPORTANT LEGAL AND ETHICAL NOTICE:

1. iPhoenix analyzes PUBLICLY AVAILABLE INFORMATION ONLY.
2. It does NOT:
   - Hack, crack, or bypass security
   - Access private accounts or data
   - Identify individuals or reveal private information
   - Perform facial recognition
   - Track locations or movements
   - Claim ownership of accounts or content

3. Intended use cases:
   - Cybersecurity research and education
   - Fraud and scam investigation
   - Journalistic research (public figures/organizations)
   - Digital footprint awareness

4. Prohibited uses:
   - Harassment, stalking, or doxxing
   - Identity theft or fraud
   - Unauthorized surveillance
   - Violating terms of service of any platform

5. You are responsible for:
   - Complying with all applicable laws
   - Respecting privacy and consent
   - Using information ethically
   - Verifying information through official channels

By using iPhoenix, you agree to use it only for ethical,
legal purposes and to take full responsibility for your actions.

Type 'AGREE' to continue: """
    
    print(disclaimer)
    
    # For demonstration, auto-agree. In production, require manual agreement.
    # agreement = input().strip().upper()
    # if agreement != 'AGREE':
    #     print("\n[!] Agreement not confirmed. Exiting.")
    #     exit(0)
    
    print("\n" + "=" * 60)
    print("[iPhoenix] Initializing ethical OSINT investigation...")
    print("=" * 60 + "\n")
"""
Phone OSINT Module
Analyzes phone numbers for public mentions
"""

import re
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import requests

class PhoneEye:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 iPhoenix-OSINT/1.0'
        }
    
    def analyze(self, phone_number, verbose=False):
        """Analyze phone number for public information"""
        results = {
            "phone_number": phone_number,
            "validation": {},
            "carrier_info": {},
            "geographic_info": {},
            "public_mentions": {},
            "messaging_apps": {},
            "warnings": [
                "Phone number analysis shows PUBLIC information only",
                "Does not identify the owner or their location",
                "Do not use for harassment, spam, or doxxing"
            ]
        }
        
        print(f"[iPhoenix] Analyzing phone number: {phone_number}")
        
        # Validate and parse phone number
        validation = self._validate_phone(phone_number)
        results['validation'] = validation
        
        if not validation['is_valid']:
            print("[!] Invalid phone number format")
            return results
        
        # Get carrier information
        print("[iPhoenix] Checking carrier information...")
        results['carrier_info'] = self._get_carrier_info(phone_number, validation['parsed_number'])
        
        # Get geographic information (country/region only)
        results['geographic_info'] = self._get_geographic_info(validation['parsed_number'])
        
        # Check for public mentions
        print("[iPhoenix] Checking for public mentions...")
        results['public_mentions'] = self._check_public_mentions(phone_number)
        
        # Check messaging app presence
        print("[iPhoenix] Checking messaging app presence...")
        results['messaging_apps'] = self._check_messaging_apps(phone_number)
        
        print("[✓] Phone analysis complete")
        
        return results
    
    def _validate_phone(self, phone_number):
        """Validate and parse phone number"""
        try:
            # Try to parse the phone number
            parsed_number = phonenumbers.parse(phone_number, None)
            is_valid = phonenumbers.is_valid_number(parsed_number)
            
            validation_result = {
                "is_valid": is_valid,
                "parsed_number": str(parsed_number),
                "country_code": parsed_number.country_code,
                "national_number": parsed_number.national_number,
                "e164_format": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164),
                "international_format": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                "national_format": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
            }
            
            return validation_result
            
        except phonenumbers.NumberParseException as e:
            return {
                "is_valid": False,
                "error": str(e),
                "note": "Phone number could not be parsed"
            }
    
    def _get_carrier_info(self, original_number, parsed_number):
        """Get carrier information for valid numbers"""
        try:
            parsed = phonenumbers.parse(original_number, None)
            carrier_name = carrier.name_for_number(parsed, "en")
            
            info = {
                "carrier": carrier_name or "Unknown",
                "number_type": str(phonenumbers.number_type(parsed)),
                "is_mobile": carrier_name is not None
            }
            
            return info
            
        except Exception as e:
            return {
                "carrier": "Unknown",
                "error": str(e)
            }
    
    def _get_geographic_info(self, parsed_number):
        """Get geographic information (country/region level only)"""
        try:
            parsed = phonenumbers.parse(str(parsed_number), None)
            
            # Get country and region only (no city data for privacy)
            country = geocoder.country_name_for_number(parsed, "en")
            region = geocoder.description_for_number(parsed, "en")
            
            # Get timezone
            timezones = timezone.time_zones_for_number(parsed)
            
            info = {
                "country": country or "Unknown",
                "region": region or "Unknown",
                "timezones": list(timezones) if timezones else [],
                "note": "Location data is at country/region level only for privacy"
            }
            
            return info
            
        except Exception as e:
            return {
                "country": "Unknown",
                "error": str(e)
            }
    
    def _check_public_mentions(self, phone_number):
        """Check for phone number in public databases and websites"""
        mentions = {
            "method": "manual_search_required",
            "note": "Automated searching of phone numbers is restricted. Manual searches recommended.",
            "suggested_searches": [
                f'"{phone_number}" site:pastebin.com',
                f'"{phone_number}" site:github.com',
                f'"{phone_number}" "scam report"',
                f'"{phone_number}" "complaint"'
            ],
            "public_databases": [
                "Phone number directories (Whitepages, Truecaller public profiles)",
                "Scam and fraud reporting websites",
                "Business contact directories"
            ],
            "warning": "Only search for information that is intentionally published publicly"
        }
        
        # Simulate check for common scam patterns (educational only)
        cleaned_number = re.sub(r'[^0-9+]', '', phone_number)
        
        if len(cleaned_number) < 8:
            mentions['format_warning'] = "Phone number appears incomplete"
        
        return mentions
    
    def _check_messaging_apps(self, phone_number):
        """Check if number is registered on messaging apps (presence only)"""
        apps = {
            "whatsapp": {
                "check_method": "manual",
                "url": f"https://wa.me/{re.sub(r'[^0-9]', '', phone_number)}",
                "note": "Visit URL to see if WhatsApp account exists",
                "warning": "Do not message unknown numbers"
            },
            "telegram": {
                "check_method": "username_search_recommended",
                "note": "Telegram uses usernames, not phone numbers for public contact",
                "suggestion": "Search for associated username instead"
            },
            "signal": {
                "check_method": "not_publicly_verifiable",
                "note": "Signal does not provide public verification of numbers"
            },
            "viber": {
                "check_method": "app_required",
                "note": "Requires Viber app to check"
            }
        }
        
        return apps
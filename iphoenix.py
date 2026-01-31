#!/usr/bin/env python3
"""
iPhoenix - Ethical OSINT Investigation Tool
For cybersecurity, journalism, and fraud detection research.
"""

import argparse
import sys
import json
import time
from datetime import datetime
from pathlib import Path

# Import modules
from modules.image_eye import ImageEye
from modules.username_eye import UsernameEye
from modules.email_eye import EmailEye
from modules.phone_eye import PhoneEye
from utils.disclaimer import display_disclaimer
from utils.formatter import format_output, save_report

class iPhoenix:
    def __init__(self):
        self.version = "1.0.0"
        self.case_data = {
            "tool": "iPhoenix",
            "version": self.version,
            "timestamp": None,
            "input": {},
            "findings": {},
            "disclaimer": "This report contains publicly available information only. It does not claim identity, ownership, or location of any individual."
        }
    
    def parse_arguments(self):
        parser = argparse.ArgumentParser(
            description='iPhoenix - Ethical OSINT Investigation Tool',
            epilog='Use responsibly. Only analyze publicly available information.'
        )
        
        # Main analysis modes
        analysis_group = parser.add_mutually_exclusive_group(required=True)
        analysis_group.add_argument('--image', type=str, 
                                   help='Analyze image file for public appearances')
        analysis_group.add_argument('--username', type=str,
                                   help='Check username across public platforms')
        analysis_group.add_argument('--email', type=str,
                                   help='Analyze email address for public footprints')
        analysis_group.add_argument('--phone', type=str,
                                   help='Check phone number for public mentions')
        
        # Output options
        parser.add_argument('--case', type=str,
                           help='Save results to case file (JSON format)')
        parser.add_argument('--verbose', '-v', action='store_true',
                           help='Enable verbose output')
        parser.add_argument('--no-color', action='store_true',
                           help='Disable colored output')
        
        return parser.parse_args()
    
    def run_image_analysis(self, image_path, verbose=False):
        """Run image analysis module"""
        print(f"\n[{'iPhoenix'.center(50, '=')}]")
        print("[Image Analysis Module]")
        print(f"Target: {image_path}")
        print("-" * 50)
        
        image_eye = ImageEye()
        results = image_eye.analyze(image_path, verbose)
        self.case_data['findings']['image'] = results
        
        return results
    
    def run_username_analysis(self, username, verbose=False):
        """Run username analysis module"""
        print(f"\n[{'iPhoenix'.center(50, '=')}]")
        print("[Username Analysis Module]")
        print(f"Target: {username}")
        print("-" * 50)
        
        username_eye = UsernameEye()
        results = username_eye.analyze(username, verbose)
        self.case_data['findings']['username'] = results
        
        return results
    
    def run_email_analysis(self, email, verbose=False):
        """Run email analysis module"""
        print(f"\n[{'iPhoenix'.center(50, '=')}]")
        print("[Email Analysis Module]")
        print(f"Target: {email}")
        print("-" * 50)
        
        email_eye = EmailEye()
        results = email_eye.analyze(email, verbose)
        self.case_data['findings']['email'] = results
        
        return results
    
    def run_phone_analysis(self, phone, verbose=False):
        """Run phone number analysis module"""
        print(f"\n[{'iPhoenix'.center(50, '=')}]")
        print("[Phone Analysis Module]")
        print(f"Target: {phone}")
        print("-" * 50)
        
        phone_eye = PhoneEye()
        results = phone_eye.analyze(phone, verbose)
        self.case_data['findings']['phone'] = results
        
        return results
    
    def save_case_file(self, filename):
        """Save case data to JSON file"""
        if not filename.endswith('.json'):
            filename += '.json'
        
        case_dir = Path('cases')
        case_dir.mkdir(exist_ok=True)
        
        case_path = case_dir / filename
        with open(case_path, 'w') as f:
            json.dump(self.case_data, f, indent=2)
        
        print(f"\n[✓] Case saved to: {case_path}")
        return case_path
    
    def main(self):
        """Main execution function"""
        # Display disclaimer
        display_disclaimer()
        
        # Parse arguments
        args = self.parse_arguments()
        
        # Initialize case data
        self.case_data['timestamp'] = datetime.utcnow().isoformat()
        
        try:
            # Route to appropriate analysis module
            if args.image:
                self.case_data['input']['type'] = 'image'
                self.case_data['input']['value'] = args.image
                results = self.run_image_analysis(args.image, args.verbose)
            
            elif args.username:
                self.case_data['input']['type'] = 'username'
                self.case_data['input']['value'] = args.username
                results = self.run_username_analysis(args.username, args.verbose)
            
            elif args.email:
                self.case_data['input']['type'] = 'email'
                self.case_data['input']['value'] = args.email
                results = self.run_email_analysis(args.email, args.verbose)
            
            elif args.phone:
                self.case_data['input']['type'] = 'phone'
                self.case_data['input']['value'] = args.phone
                results = self.run_phone_analysis(args.phone, args.verbose)
            
            # Format and display results
            format_output(results, args.no_color)
            
            # Save case file if requested
            if args.case:
                self.save_case_file(args.case)
            
            print("\n" + "=" * 50)
            print("[iPhoenix] Analysis complete")
            print("=" * 50)
            
        except KeyboardInterrupt:
            print("\n\n[!] Analysis interrupted by user")
            sys.exit(0)
        except Exception as e:
            print(f"\n[✗] Error during analysis: {e}")
            sys.exit(1)

if __name__ == "__main__":
    tool = iPhoenix()
    tool.main()
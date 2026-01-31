"""
Image OSINT Module
Analyzes images for public appearances and metadata
"""

import hashlib
import imagehash
from PIL import Image, ImageFile, ExifTags
import os
from pathlib import Path

ImageFile.LOAD_TRUNCATED_IMAGES = True

class ImageEye:
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    
    def analyze(self, image_path, verbose=False):
        """Main analysis function for images"""
        results = {
            "file_info": {},
            "hashes": {},
            "metadata": {},
            "analysis": {},
            "warnings": []
        }
        
        try:
            # Check if file exists
            if not Path(image_path).exists():
                raise FileNotFoundError(f"Image file not found: {image_path}")
            
            # Get basic file info
            file_stats = self._get_file_info(image_path)
            results['file_info'] = file_stats
            
            # Generate hashes
            print("[iPhoenix] Loading image...")
            try:
                img = Image.open(image_path)
                results['hashes'] = self._generate_hashes(img)
                print("[✓] Image hashes generated")
            except Exception as e:
                results['warnings'].append(f"Could not generate hashes: {e}")
                print(f"[!] Warning: Could not generate hashes: {e}")
            
            # Extract metadata
            results['metadata'] = self._extract_metadata(img)
            if results['metadata']:
                print("[✓] Metadata extracted")
            
            # Perform analysis
            results['analysis'] = self._analyze_image(img, results['metadata'])
            
            # Add API hooks info
            results['api_hooks'] = {
                "reverse_search_suggestions": [
                    "TinEye (tineye.com)",
                    "Yandex Images (yandex.com/images)",
                    "Bing Visual Search"
                ],
                "note": "These are public reverse image search engines. iPhoenix does not automate scraping."
            }
            
        except Exception as e:
            results['error'] = str(e)
            print(f"[✗] Error during image analysis: {e}")
        
        return results
    
    def _get_file_info(self, image_path):
        """Get basic file information"""
        path = Path(image_path)
        return {
            "filename": path.name,
            "size_bytes": path.stat().st_size,
            "size_mb": round(path.stat().st_size / (1024 * 1024), 2),
            "created": path.stat().st_ctime,
            "modified": path.stat().st_mtime,
            "extension": path.suffix.lower()
        }
    
    def _generate_hashes(self, img):
        """Generate perceptual hashes for image comparison"""
        try:
            # Generate dHash (difference hash)
            dhash = str(imagehash.dhash(img))
            
            # Generate pHash (perceptual hash)
            phash = str(imagehash.phash(img))
            
            # Generate MD5 for exact match checking
            img_copy = img.copy()
            img_copy.thumbnail((100, 100))
            img_bytes = img_copy.tobytes()
            md5_hash = hashlib.md5(img_bytes).hexdigest()
            
            return {
                "dhash": dhash,
                "phash": phash,
                "md5": md5_hash,
                "note": "Use these hashes to check for similar images across public platforms"
            }
        except Exception as e:
            return {"error": f"Hash generation failed: {e}"}
    
    def _extract_metadata(self, img):
        """Extract EXIF metadata if available"""
        metadata = {}
        
        try:
            exif_data = img._getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = ExifTags.TAGS.get(tag_id, tag_id)
                    
                    # Filter sensitive GPS data
                    if tag == 'GPSInfo':
                        metadata['warning'] = "GPS data removed for privacy"
                        continue
                    
                    # Filter device serial numbers
                    if 'Serial' in str(tag):
                        continue
                    
                    # Convert bytes to string if necessary
                    if isinstance(value, bytes):
                        try:
                            value = value.decode('utf-8', errors='ignore')
                        except:
                            value = str(value)
                    
                    metadata[tag] = str(value)
        except Exception:
            pass
        
        return metadata
    
    def _analyze_image(self, img, metadata):
        """Analyze image for investigation clues"""
        analysis = {
            "dimensions": f"{img.width}x{img.height}",
            "mode": img.mode,
            "format": img.format,
            "possible_reuse_indicators": []
        }
        
        # Check for common stock photo dimensions
        stock_dimensions = [(1200, 800), (1920, 1080), (1280, 720), (800, 600)]
        if (img.width, img.height) in stock_dimensions:
            analysis['possible_reuse_indicators'].append(
                "Common stock photo dimensions detected"
            )
        
        # Check metadata for clues
        if metadata:
            if 'Software' in metadata:
                analysis['possible_reuse_indicators'].append(
                    f"Created/edited with: {metadata['Software']}"
                )
        
        # Check image properties
        if img.width < 300 or img.height < 300:
            analysis['possible_reuse_indicators'].append(
                "Low resolution - may be thumbnail or compressed copy"
            )
        
        analysis['investigation_notes'] = [
            "Compare hashes on reverse image search engines",
            "Check if image appears on stock photo websites",
            "Look for watermarks or editing artifacts"
        ]
        
        return analysis
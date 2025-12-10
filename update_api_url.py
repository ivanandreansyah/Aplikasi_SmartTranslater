#!/usr/bin/env python3
"""
Quick script to update frontend API URL for production deployment
"""

import sys
import os

def update_api_url(backend_url):
    """Update the API URL in frontend/index.html"""
    
    # Validate URL
    if not backend_url.startswith('https://'):
        print("⚠️  WARNING: URL should start with 'https://' for production")
        confirm = input("Continue anyway? (y/n): ")
        if confirm.lower() != 'y':
            print("Aborted.")
            return False
    
    # Read the file
    html_file = os.path.join('frontend', 'index.html')
    
    if not os.path.exists(html_file):
        print(f"❌ Error: {html_file} not found!")
        return False
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the API URL
    old_line = '      window.API_URL = "http://127.0.0.1:5000/translate";'
    
    # Check if it's already updated
    if backend_url in content:
        print(f"✅ API URL already set to: {backend_url}")
        return True
    
    # Make sure to add /translate if not present
    if not backend_url.endswith('/translate'):
        backend_url = backend_url.rstrip('/') + '/translate'
    
    new_line = f'      window.API_URL = "{backend_url}";'
    
    if old_line in content:
        content = content.replace(old_line, new_line)
    else:
        # Try to find any API_URL line
        import re
        pattern = r'window\.API_URL = "[^"]+";'
        if re.search(pattern, content):
            content = re.sub(pattern, f'window.API_URL = "{backend_url}";', content)
        else:
            print("❌ Error: Could not find API_URL line in index.html")
            return False
    
    # Write back
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated API URL to: {backend_url}")
    print(f"\n📝 Next steps:")
    print(f"   1. git add frontend/index.html")
    print(f"   2. git commit -m 'Update API URL for production'")
    print(f"   3. git push origin main")
    print(f"   4. Deploy frontend to Netlify")
    
    return True

def main():
    print("🚀 SmartTranslate - Update API URL for Production\n")
    
    if len(sys.argv) > 1:
        backend_url = sys.argv[1]
    else:
        print("Enter your backend URL from Render:")
        print("Example: https://smarttranslate-backend.onrender.com")
        backend_url = input("\nBackend URL: ").strip()
    
    if not backend_url:
        print("❌ Error: No URL provided")
        sys.exit(1)
    
    if update_api_url(backend_url):
        print("\n✨ Done! Your frontend is ready for deployment.")
    else:
        print("\n❌ Failed to update API URL")
        sys.exit(1)

if __name__ == '__main__':
    main()

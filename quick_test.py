"""
Quick test for backend functionality
"""

import urllib.request
import json

def quick_test():
    print("⚡ Quick Backend Test")
    print("=" * 30)
    
    try:
        # Test health check
        response = urllib.request.urlopen("http://127.0.0.1:8000/api/health/")
        data = json.loads(response.read().decode())
        print(f"✅ API: {data['status']}")
        
        # Test admin page
        response = urllib.request.urlopen("http://127.0.0.1:8000/admin/")
        print("✅ Admin: Working")
        
        print("\n🚀 Backend is ready!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    quick_test()

"""
Test API endpoints for Salon Backend
"""

import urllib.request
import json

def test_api():
    print("🔧 Testing Salon Backend API")
    print("=" * 40)
    
    base_url = "http://127.0.0.1:8000"
    
    try:
        # Test health endpoint
        response = urllib.request.urlopen(f"{base_url}/api/health/")
        data = json.loads(response.read().decode())
        print(f"✅ Health Check: {data['status']}")
        
        # Test admin login page
        response = urllib.request.urlopen(f"{base_url}/admin/")
        print("✅ Admin login page accessible")
        
        print("\n🎯 API Tests Complete!")
        print("📋 Available endpoints:")
        print("   - Health: /api/health/")
        print("   - Admin: /admin/")
        print("   - Auth: /api/auth/")
        print("   - Services: /api/services/")
        print("   - Appointments: /api/appointments/")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_api()

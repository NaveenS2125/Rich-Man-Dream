#!/usr/bin/env python3
"""
Rich Man Dream CRM Backend Authentication Tests
Tests the authentication system including login, protected endpoints, and JWT handling.
"""

import requests
import json
import sys
import os
from datetime import datetime

# Backend URL from environment
BACKEND_URL = "https://dream-estate-1.preview.emergentagent.com/api"

# Test credentials from seeded data
TEST_EMAIL = "sarah.johnson@richmansdream.com"
TEST_PASSWORD = "password123"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_test_header(test_name):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}Testing: {test_name}{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.ENDC}")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.ENDC}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.ENDC}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.ENDC}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.ENDC}")

def test_health_endpoints():
    """Test health check endpoints"""
    print_test_header("Health Check Endpoints")
    
    # Test root endpoint
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                print_success(f"Root endpoint (GET /api/) - Status: {response.status_code}")
                print_info(f"Response: {data}")
            else:
                print_error(f"Root endpoint returned unexpected data: {data}")
                return False
        else:
            print_error(f"Root endpoint failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Root endpoint error: {str(e)}")
        return False
    
    # Test health endpoint
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                print_success(f"Health endpoint (GET /api/health) - Status: {response.status_code}")
                print_info(f"Response: {data}")
            else:
                print_error(f"Health endpoint returned unexpected data: {data}")
                return False
        else:
            print_error(f"Health endpoint failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health endpoint error: {str(e)}")
        return False
    
    return True

def test_login_success():
    """Test successful login"""
    print_test_header("Login - Valid Credentials")
    
    login_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Check response structure
            required_fields = ["success", "token", "user", "message"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                print_error(f"Missing fields in response: {missing_fields}")
                return None, False
            
            if not data["success"]:
                print_error(f"Login marked as unsuccessful: {data}")
                return None, False
            
            if not data["token"]:
                print_error("No token provided in response")
                return None, False
            
            # Check user data structure
            user = data["user"]
            user_fields = ["id", "name", "email", "role"]
            missing_user_fields = [field for field in user_fields if field not in user]
            
            if missing_user_fields:
                print_error(f"Missing user fields: {missing_user_fields}")
                return None, False
            
            print_success(f"Login successful - Status: {response.status_code}")
            print_info(f"User: {user['name']} ({user['email']}) - Role: {user['role']}")
            print_info(f"Token received (length: {len(data['token'])})")
            
            return data["token"], True
            
        else:
            print_error(f"Login failed - Status: {response.status_code}")
            try:
                error_data = response.json()
                print_error(f"Error response: {error_data}")
            except:
                print_error(f"Response text: {response.text}")
            return None, False
            
    except Exception as e:
        print_error(f"Login request error: {str(e)}")
        return None, False

def test_login_invalid_credentials():
    """Test login with invalid credentials"""
    print_test_header("Login - Invalid Credentials")
    
    # Test invalid email
    login_data = {
        "email": "invalid@email.com",
        "password": TEST_PASSWORD
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 401:
            print_success("Invalid email correctly rejected - Status: 401")
        else:
            print_error(f"Invalid email should return 401, got: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Invalid email test error: {str(e)}")
        return False
    
    # Test invalid password
    login_data = {
        "email": TEST_EMAIL,
        "password": "wrongpassword"
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 401:
            print_success("Invalid password correctly rejected - Status: 401")
            return True
        else:
            print_error(f"Invalid password should return 401, got: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Invalid password test error: {str(e)}")
        return False

def test_protected_endpoint_with_token(token):
    """Test protected endpoint with valid token"""
    print_test_header("Protected Endpoint - Valid Token")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{BACKEND_URL}/auth/me",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Check user data structure
            user_fields = ["id", "name", "email", "role"]
            missing_fields = [field for field in user_fields if field not in data]
            
            if missing_fields:
                print_error(f"Missing user fields in /me response: {missing_fields}")
                return False
            
            print_success(f"Protected endpoint accessible - Status: {response.status_code}")
            print_info(f"User data: {data['name']} ({data['email']}) - Role: {data['role']}")
            return True
            
        else:
            print_error(f"Protected endpoint failed - Status: {response.status_code}")
            try:
                error_data = response.json()
                print_error(f"Error response: {error_data}")
            except:
                print_error(f"Response text: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Protected endpoint test error: {str(e)}")
        return False

def test_protected_endpoint_without_token():
    """Test protected endpoint without token"""
    print_test_header("Protected Endpoint - No Token")
    
    try:
        response = requests.get(
            f"{BACKEND_URL}/auth/me",
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 403:
            print_success("Protected endpoint correctly rejected request without token - Status: 403")
            return True
        elif response.status_code == 401:
            print_success("Protected endpoint correctly rejected request without token - Status: 401")
            return True
        else:
            print_error(f"Protected endpoint should return 401/403 without token, got: {response.status_code}")
            try:
                error_data = response.json()
                print_error(f"Error response: {error_data}")
            except:
                print_error(f"Response text: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"No token test error: {str(e)}")
        return False

def test_protected_endpoint_invalid_token():
    """Test protected endpoint with invalid token"""
    print_test_header("Protected Endpoint - Invalid Token")
    
    headers = {
        "Authorization": "Bearer invalid_token_here",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{BACKEND_URL}/auth/me",
            headers=headers,
            timeout=10
        )
        
        if response.status_code in [401, 403]:
            print_success(f"Invalid token correctly rejected - Status: {response.status_code}")
            return True
        else:
            print_error(f"Invalid token should return 401/403, got: {response.status_code}")
            try:
                error_data = response.json()
                print_error(f"Error response: {error_data}")
            except:
                print_error(f"Response text: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Invalid token test error: {str(e)}")
        return False

def test_logout():
    """Test logout endpoint"""
    print_test_header("Logout Endpoint")
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/auth/logout",
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print_success(f"Logout successful - Status: {response.status_code}")
                print_info(f"Response: {data}")
                return True
            else:
                print_error(f"Logout response indicates failure: {data}")
                return False
        else:
            print_error(f"Logout failed - Status: {response.status_code}")
            try:
                error_data = response.json()
                print_error(f"Error response: {error_data}")
            except:
                print_error(f"Response text: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Logout test error: {str(e)}")
        return False

def main():
    """Run all authentication tests"""
    print(f"{Colors.BOLD}Rich Man Dream CRM - Backend Authentication Tests{Colors.ENDC}")
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test Email: {TEST_EMAIL}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # Test health endpoints
    results["health"] = test_health_endpoints()
    
    # Test login with valid credentials
    token, login_success = test_login_success()
    results["login_success"] = login_success
    
    # Test login with invalid credentials
    results["login_invalid"] = test_login_invalid_credentials()
    
    # Test protected endpoints (only if we have a valid token)
    if token:
        results["protected_with_token"] = test_protected_endpoint_with_token(token)
    else:
        results["protected_with_token"] = False
        print_error("Skipping protected endpoint test - no valid token")
    
    # Test protected endpoint without token
    results["protected_without_token"] = test_protected_endpoint_without_token()
    
    # Test protected endpoint with invalid token
    results["protected_invalid_token"] = test_protected_endpoint_invalid_token()
    
    # Test logout
    results["logout"] = test_logout()
    
    # Print summary
    print_test_header("Test Summary")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        color = Colors.GREEN if result else Colors.RED
        print(f"{color}{status:>6}{Colors.ENDC} - {test_name}")
    
    print(f"\n{Colors.BOLD}Results: {passed}/{total} tests passed{Colors.ENDC}")
    
    if passed == total:
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 All authentication tests passed!{Colors.ENDC}")
        return True
    else:
        print(f"{Colors.RED}{Colors.BOLD}❌ Some tests failed. Check the details above.{Colors.ENDC}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
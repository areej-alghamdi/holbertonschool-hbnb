
#!/bin/bash
# Black-box API Testing for HBnB User Endpoints using cURL

BASE_URL="http://127.0.0.1:5000/api/v1"

echo "=========================================="
echo "1. Testing GET /users (Fetch all users)"
echo "=========================================="
curl -X GET "$BASE_URL/users/" \
  -H "Content-Type: application/json"
     
echo -e "\n\n"

echo "=========================================="
echo "2. Testing POST /users (Valid User Creation)"
echo "=========================================="
curl -X POST "$BASE_URL/users/" \
     -H "Content-Type: application/json" \
     -d '{
           "first_name": "Alice",
           "last_name": "Smith",
           "email": "alice@example.com",
           "password": "securepassword123"
         }'
echo -e "\n\n"

echo "=========================================="
echo "3. Testing POST /users (Invalid Email Validation Test)"
echo "=========================================="
curl -X POST "$BASE_URL/users/" \
     -H "Content-Type: application/json" \
     -d '{
           "first_name": "Bob",
           "last_name": "Jones",
           "email": "not-an-email",
           "password": "password123"
         }'
echo -e "\n\n"

echo "=========================================="
echo "4. Testing POST /users (Short Password Validation Test)"
echo "=========================================="
curl -X POST "$BASE_URL/users/" \
     -H "Content-Type: application/json" \
     -d '{
           "first_name": "Bob",
           "last_name": "Jones",
           "email": "bob@example.com",
           "password": "123"
         }'
echo -e "\n"
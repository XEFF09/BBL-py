#!/bin/bash
# Quick API Testing Guide with curl

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

API_URL="http://localhost:8080/api"

echo -e "${BLUE}=== Booking API - Quick Test Guide ===${NC}\n"

# 1. Register a new user
echo -e "${GREEN}1. Registering a new user...${NC}"
REGISTER_RESPONSE=$(curl -s -X POST "$API_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "secure_password_123"
  }')
echo "$REGISTER_RESPONSE" | jq .
echo ""

# 2. Login with the new user
echo -e "${GREEN}2. Logging in with new user...${NC}"
LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "secure_password_123"
  }')
echo "$LOGIN_RESPONSE" | jq .

# Extract token from login response
TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.data.access_token')
echo -e "\n${BLUE}Token: $TOKEN${NC}\n"

# 3. Create a booking
echo -e "${GREEN}3. Creating a booking...${NC}"
BOOKING_RESPONSE=$(curl -s -X POST "$API_URL/bookings" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Project Kickoff Meeting",
    "description": "Initial planning session",
    "start_time": "2026-05-27T14:00:00",
    "end_time": "2026-05-27T15:30:00",
    "location": "Board Room"
  }')
echo "$BOOKING_RESPONSE" | jq .

# Extract booking ID
BOOKING_ID=$(echo "$BOOKING_RESPONSE" | jq -r '.data.booking_id')
echo -e "\n${BLUE}Booking ID: $BOOKING_ID${NC}\n"

# 4. List all bookings
echo -e "${GREEN}4. Listing all bookings...${NC}"
curl -s -X GET "$API_URL/bookings" \
  -H "Authorization: Bearer $TOKEN" | jq .
echo ""

# 5. Get a specific booking
echo -e "${GREEN}5. Getting specific booking...${NC}"
curl -s -X GET "$API_URL/bookings/$BOOKING_ID" \
  -H "Authorization: Bearer $TOKEN" | jq .
echo ""

# 6. Update booking
echo -e "${GREEN}6. Updating booking...${NC}"
curl -s -X PUT "$API_URL/bookings/$BOOKING_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "confirmed",
    "description": "Planning session - attendees confirmed"
  }' | jq .
echo ""

# 7. Cancel booking (alternative endpoint)
echo -e "${GREEN}7. Creating another booking to cancel...${NC}"
BOOKING_2=$(curl -s -X POST "$API_URL/bookings" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Team Sync",
    "start_time": "2026-05-28T10:00:00",
    "end_time": "2026-05-28T10:30:00"
  }')
BOOKING_2_ID=$(echo "$BOOKING_2" | jq -r '.data.booking_id')

echo -e "${GREEN}8. Cancelling the second booking...${NC}"
curl -s -X POST "$API_URL/bookings/$BOOKING_2_ID/cancel" \
  -H "Authorization: Bearer $TOKEN" | jq .
echo ""

# 9. Delete booking
echo -e "${GREEN}9. Deleting the cancelled booking...${NC}"
curl -s -X DELETE "$API_URL/bookings/$BOOKING_2_ID" \
  -H "Authorization: Bearer $TOKEN" | jq .
echo ""

# 10. Test with admin user
echo -e "${GREEN}10. Testing with admin user...${NC}"
ADMIN_LOGIN=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }')
ADMIN_TOKEN=$(echo "$ADMIN_LOGIN" | jq -r '.data.access_token')

echo -e "${BLUE}Admin can see all bookings:${NC}"
curl -s -X GET "$API_URL/bookings" \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq .
echo ""

echo -e "${GREEN}=== Test Complete ===${NC}"

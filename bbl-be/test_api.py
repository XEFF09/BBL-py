#!/usr/bin/env python3
"""
Test script for the Booking API endpoints.
Tests authentication, user management, and booking CRUD operations.
"""

import asyncio
import json
import sys
import os
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from usecase.auth import UserService
from usecase.booking import BookingService


async def test_auth_service():
    """Test UserService authentication."""
    print("\n" + "="*60)
    print("Testing UserService (Authentication)")
    print("="*60)
    
    auth_service = UserService()
    
    # Test 1: Login with default admin user
    print("\n[TEST 1] Login with admin user")
    try:
        result = await auth_service.login({
            "username": "admin",
            "password": "admin123",
        })
        print(f"✓ Admin login successful")
        print(f"  - User ID: {result['user_id']}")
        print(f"  - Is Admin: {result['is_admin']}")
        print(f"  - Token: {result['access_token'][:20]}...")
        admin_token = result["access_token"]
    except Exception as e:
        print(f"✗ Admin login failed: {e}")
        return False
    
    # Test 2: Login with default regular user
    print("\n[TEST 2] Login with regular user")
    try:
        result = await auth_service.login({
            "username": "user",
            "password": "user123",
        })
        print(f"✓ Regular user login successful")
        print(f"  - User ID: {result['user_id']}")
        print(f"  - Is Admin: {result['is_admin']}")
        user_id = result['user_id']
        user_token = result["access_token"]
    except Exception as e:
        print(f"✗ Regular user login failed: {e}")
        return False
    
    # Test 3: Register new user
    print("\n[TEST 3] Register new user")
    try:
        result = await auth_service.register({
            "username": "testuser",
            "password": "testpass123",
        })
        print(f"✓ New user registration successful")
        print(f"  - User ID: {result['user_id']}")
        print(f"  - Username: {result['username']}")
        print(f"  - Is Admin: {result['is_admin']}")
        new_user_id = result['user_id']
    except Exception as e:
        print(f"✗ Registration failed: {e}")
        return False
    
    # Test 4: Login with newly registered user
    print("\n[TEST 4] Login with newly registered user")
    try:
        result = await auth_service.login({
            "username": "testuser",
            "password": "testpass123",
        })
        print(f"✓ New user login successful")
        new_user_token = result["access_token"]
    except Exception as e:
        print(f"✗ New user login failed: {e}")
        return False
    
    # Test 5: Verify token
    print("\n[TEST 5] Verify JWT token")
    try:
        token_data = auth_service.verify_token(user_token)
        if token_data:
            print(f"✓ Token verification successful")
            print(f"  - Username: {token_data.username}")
            print(f"  - User ID: {token_data.user_id}")
            print(f"  - Is Admin: {token_data.is_admin}")
        else:
            print(f"✗ Token verification failed: Invalid token")
            return False
    except Exception as e:
        print(f"✗ Token verification failed: {e}")
        return False
    
    # Test 6: Invalid login
    print("\n[TEST 6] Invalid login attempt")
    try:
        await auth_service.login({
            "username": "admin",
            "password": "wrongpassword",
        })
        print(f"✗ Should have failed with invalid password")
        return False
    except ValueError as e:
        print(f"✓ Correctly rejected invalid password: {e}")
    
    # Test 7: Register duplicate user
    print("\n[TEST 7] Attempt to register duplicate user")
    try:
        await auth_service.register({
            "username": "admin",
            "password": "somepassword",
        })
        print(f"✗ Should have failed with duplicate user")
        return False
    except ValueError as e:
        print(f"✓ Correctly rejected duplicate user: {e}")
    
    return True, user_token, admin_token, new_user_token, user_id


async def test_booking_service(user_token, admin_token, user_id):
    """Test BookingService CRUD operations."""
    print("\n" + "="*60)
    print("Testing BookingService (Bookings Management)")
    print("="*60)
    
    booking_service = BookingService()
    auth_service = UserService()
    
    # Extract user ID from token
    user_token_data = auth_service.verify_token(user_token)
    user_id_from_token = user_token_data.user_id
    
    # Test 1: Create booking
    print("\n[TEST 1] Create booking")
    try:
        now = datetime.utcnow()
        start_time = now + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        
        result = await booking_service.create_booking(
            user_id=user_id_from_token,
            data={
                "title": "Team Meeting",
                "description": "Quarterly planning meeting",
                "start_time": start_time,
                "end_time": end_time,
                "location": "Conference Room A",
            }
        )
        print(f"✓ Booking created successfully")
        print(f"  - Booking ID: {result['booking_id']}")
        print(f"  - Title: {result['title']}")
        print(f"  - Status: {result['status']}")
        booking_id = result['booking_id']
    except Exception as e:
        print(f"✗ Failed to create booking: {e}")
        return False
    
    # Test 2: Get booking
    print("\n[TEST 2] Get booking by ID")
    try:
        result = await booking_service.get_booking(
            booking_id=booking_id,
            user_id=user_id_from_token,
        )
        if result:
            print(f"✓ Booking retrieved successfully")
            print(f"  - Title: {result['title']}")
            print(f"  - Description: {result['description']}")
        else:
            print(f"✗ Booking not found")
            return False
    except Exception as e:
        print(f"✗ Failed to get booking: {e}")
        return False
    
    # Test 3: List user bookings
    print("\n[TEST 3] List all user bookings")
    try:
        results = await booking_service.get_user_bookings(user_id_from_token)
        print(f"✓ Retrieved {len(results)} booking(s)")
        for b in results:
            print(f"  - {b['title']} ({b['status']})")
    except Exception as e:
        print(f"✗ Failed to list bookings: {e}")
        return False
    
    # Test 4: Update booking
    print("\n[TEST 4] Update booking")
    try:
        result = await booking_service.update_booking(
            booking_id=booking_id,
            user_id=user_id_from_token,
            data={
                "title": "Team Meeting - UPDATED",
                "description": "Quarterly planning meeting (revised)",
                "status": "confirmed",
            }
        )
        print(f"✓ Booking updated successfully")
        print(f"  - New title: {result['title']}")
        print(f"  - New status: {result['status']}")
    except Exception as e:
        print(f"✗ Failed to update booking: {e}")
        return False
    
    # Test 5: Create another booking
    print("\n[TEST 5] Create another booking")
    try:
        now = datetime.utcnow()
        start_time = now + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)
        
        result = await booking_service.create_booking(
            user_id=user_id_from_token,
            data={
                "title": "Doctor Appointment",
                "start_time": start_time,
                "end_time": end_time,
                "location": "City Hospital",
            }
        )
        print(f"✓ Second booking created")
        booking_id_2 = result['booking_id']
    except Exception as e:
        print(f"✗ Failed to create second booking: {e}")
        return False
    
    # Test 6: Cancel booking
    print("\n[TEST 6] Cancel booking")
    try:
        result = await booking_service.cancel_booking(
            booking_id=booking_id_2,
            user_id=user_id_from_token,
        )
        print(f"✓ Booking cancelled successfully")
        print(f"  - Status: {result['status']}")
    except Exception as e:
        print(f"✗ Failed to cancel booking: {e}")
        return False
    
    # Test 7: Delete booking
    print("\n[TEST 7] Delete booking")
    try:
        await booking_service.delete_booking(
            booking_id=booking_id_2,
            user_id=user_id_from_token,
        )
        print(f"✓ Booking deleted successfully")
    except Exception as e:
        print(f"✗ Failed to delete booking: {e}")
        return False
    
    # Test 8: List all bookings (admin)
    print("\n[TEST 8] List all bookings (admin view)")
    try:
        results = await booking_service.get_all_bookings()
        print(f"✓ Retrieved {len(results)} total booking(s)")
        for b in results:
            print(f"  - {b['title']} (User: {b['user_id'][:8]}...)")
    except Exception as e:
        print(f"✗ Failed to list all bookings: {e}")
        return False
    
    # Test 9: Unauthorized access
    print("\n[TEST 9] Test authorization - user cannot see other user's bookings")
    try:
        # Create a different user
        another_user = await auth_service.register({
            "username": "anotheruser",
            "password": "anotherpass123",
        })
        another_user_id = another_user['user_id']
        
        # Try to access first user's booking
        await booking_service.get_booking(
            booking_id=booking_id,
            user_id=another_user_id,
        )
        print(f"✗ Should have denied access")
        return False
    except ValueError as e:
        print(f"✓ Correctly denied unauthorized access: {e}")
    
    # Test 10: Invalid time range
    print("\n[TEST 10] Test invalid time range (start >= end)")
    try:
        now = datetime.utcnow()
        
        await booking_service.create_booking(
            user_id=user_id_from_token,
            data={
                "title": "Invalid Booking",
                "start_time": now + timedelta(hours=2),
                "end_time": now + timedelta(hours=1),  # End before start!
            }
        )
        print(f"✗ Should have rejected invalid time range")
        return False
    except ValueError as e:
        print(f"✓ Correctly rejected invalid time range: {e}")
    
    return True


async def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("BOOKING API - TEST SUITE")
    print("="*60)
    
    try:
        # Test authentication
        auth_result = await test_auth_service()
        if not auth_result:
            print("\n✗ Authentication tests failed!")
            return False
        
        _, user_token, admin_token, new_user_token, user_id = auth_result
        
        # Test bookings
        booking_result = await test_booking_service(user_token, admin_token, user_id)
        if not booking_result:
            print("\n✗ Booking tests failed!")
            return False
        
        print("\n" + "="*60)
        print("✓ ALL TESTS PASSED!")
        print("="*60)
        print("\nSummary:")
        print("  ✓ User authentication and registration working")
        print("  ✓ JWT token generation and verification working")
        print("  ✓ Booking CRUD operations working")
        print("  ✓ Authorization checks working")
        print("  ✓ Error handling working")
        print("\n")
        return True
        
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

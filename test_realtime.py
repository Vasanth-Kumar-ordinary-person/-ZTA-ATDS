#!/usr/bin/env python3
"""
Test script for ZTA-ATDS Real-Time Features
"""

import asyncio
import aiohttp
import json
import time
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_health_check():
    """Test the health endpoint"""
    print("🏥 Testing health check...")
    async with aiohttp.ClientSession() as session:
        async with session.get("http://localhost:8000/health") as response:
            if response.status == 200:
                data = await response.json()
                print(f"✅ Health check passed: {data}")
                return True
            else:
                print(f"❌ Health check failed: {response.status}")
                return False

async def test_anomaly_detection():
    """Test anomaly detection endpoint"""
    print("🔍 Testing anomaly detection...")
    test_data = {
        "features": [1.0, 2.0, 3.0, 4.0, 5.0]
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://localhost:8000/predict-anomaly/",
            json=test_data
        ) as response:
            if response.status == 200:
                data = await response.json()
                print(f"✅ Anomaly detection: Score={data['anomaly_score']:.4f}, Anomalous={data['is_anomalous']}")
                return True
            else:
                print(f"❌ Anomaly detection failed: {response.status}")
                return False

async def test_streaming_prediction():
    """Test streaming prediction endpoint"""
    print("📡 Testing streaming prediction...")
    test_data = {
        "features": [10.0, 10.0, 10.0, 10.0, 10.0]  # High values to trigger anomaly
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://localhost:8000/stream-predict/",
            json=test_data
        ) as response:
            if response.status == 200:
                data = await response.json()
                print(f"✅ Streaming prediction: Score={data['anomaly_score']:.4f}, Anomalous={data['is_anomalous']}")
                return True
            else:
                print(f"❌ Streaming prediction failed: {response.status}")
                return False

async def test_websocket_connection():
    """Test WebSocket connection"""
    print("🔌 Testing WebSocket connection...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect("ws://localhost:8000/ws") as ws:
                # Send a test message
                await ws.send_str("test_message")
                
                # Wait for response
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        print(f"✅ WebSocket test: {msg.data}")
                        return True
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        print(f"❌ WebSocket error: {ws.exception()}")
                        return False
    except Exception as e:
        print(f"❌ WebSocket connection failed: {e}")
        return False

async def test_dashboard_access():
    """Test dashboard access"""
    print("📊 Testing dashboard access...")
    async with aiohttp.ClientSession() as session:
        async with session.get("http://localhost:8000/") as response:
            if response.status == 200:
                content = await response.text()
                if "ZTA-ATDS Real-Time Dashboard" in content:
                    print("✅ Dashboard accessible")
                    return True
                else:
                    print("❌ Dashboard content not found")
                    return False
            else:
                print(f"❌ Dashboard access failed: {response.status}")
                return False

async def run_all_tests():
    """Run all real-time tests"""
    print("🧪 Starting ZTA-ATDS Real-Time Tests")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("Dashboard Access", test_dashboard_access),
        ("Anomaly Detection", test_anomaly_detection),
        ("Streaming Prediction", test_streaming_prediction),
        ("WebSocket Connection", test_websocket_connection),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📋 Test Results:")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Real-time system is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Check the server logs for details.")
        return False

def main():
    """Main test function"""
    print("🚀 ZTA-ATDS Real-Time System Test")
    print("Make sure the server is running on http://localhost:8000")
    print("=" * 50)
    
    try:
        result = asyncio.run(run_all_tests())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
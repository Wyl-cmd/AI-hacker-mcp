#!/usr/bin/env python3
# Test script for FastMCP MCP Server

import sys
import subprocess
import time
import os

def test_fastmcp_import():
    """Test if FastMCP can be imported successfully"""
    print("Testing FastMCP Import...")
    
    try:
        from src.mcp_server_fastmcp import mcp
        print(f"✓ Successfully imported mcp from src.mcp_server_fastmcp")
        return True
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_server_starts():
    """Test if the server can start successfully"""
    print("\nTesting Server Startup...")
    
    try:
        # Start the server in a subprocess
        process = subprocess.Popen(
            [sys.executable, "src/mcp_server_fastmcp.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Give it time to start
        time.sleep(2)
        
        # Check if process is still running
        if process.poll() is not None:
            # Process exited, something went wrong
            stderr = process.stderr.read()
            print(f"❌ Server failed to start: {stderr}")
            return False
        
        # Kill the process gracefully
        process.terminate()
        process.wait(timeout=5)
        
        print("✓ Server started successfully")
        return True
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_server_files():
    """Test if all required server files exist"""
    print("\nTesting Server Files...")
    
    required_files = [
        "src/mcp_server_fastmcp.py",
        "requirements.txt",
        "start.bat",
        "start.sh",
        "README_PYTHON.md"
    ]
    
    all_files_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            all_files_exist = False
    
    return all_files_exist

def test_python_syntax():
    """Test if Python syntax is correct"""
    print("\nTesting Python Syntax...")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", "src/mcp_server_fastmcp.py"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✓ Python syntax is correct")
            return True
        else:
            print(f"❌ Python syntax error: {result.stderr}")
            return False
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("Testing FastMCP MCP Server")
    print("="*60)
    
    # Run tests
    tests = [
        ("FastMCP Import", test_fastmcp_import),
        ("Python Syntax", test_python_syntax),
        ("Server Files", test_server_files),
        ("Server Startup", test_server_starts)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 40)
        
        if test_func():
            passed += 1
            print(f"\n✅ {test_name} passed!")
        else:
            print(f"\n❌ {test_name} failed!")
    
    # Summary
    print("\n" + "="*60)
    print(f"TEST SUMMARY: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n🎉 All tests passed! The MCP server is ready!")
        print("\nTo start the server, run:")
        print("  - Windows: start.bat")
        print("  - Linux/Mac: start.sh")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please check the errors above.")
    
    sys.exit(0 if passed == total else 1)

if __name__ == '__main__':
    main()

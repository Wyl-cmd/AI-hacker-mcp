#!/usr/bin/env python3

import asyncio
import json
import sys

async def test_mcp_server():
    print("Testing Enhanced MCP Server functionality...")
    
    server = None
    try:
        from src.mcp_server import MCPServer
        server = MCPServer()
        
        print(f"\nServer Name: {server.name}")
        print(f"Server Version: {server.version}")
        print(f"Server Description: {server.description}")
        
        print(f"\nAvailable Tools ({len(server.tools)}):")
        for tool in server.tools:
            print(f"  - {tool['name']}: {tool['description']}")
        
        print(f"\nAvailable Prompts ({len(server.prompts)}):")
        for prompt in server.prompts:
            print(f"  - {prompt['name']}: {prompt['description']}")
        
        print("\n" + "="*60)
        print("Testing server handlers...")
        print("="*60)
        
        result = await server.handle_list_tools({})
        print(f"\n✓ list_tools: {len(result['tools'])} tools returned")
        
        result = await server.handle_list_prompts({})
        print(f"✓ list_prompts: {len(result['prompts'])} prompts returned")
        
        result = await server.handle_describe_server({})
        print(f"✓ describe_server: {result['name']} v{result['version']}")
        
        result = await server.handle_get_config({})
        print(f"✓ get_config: {len(result['config'])} config sections")
        
        print("\n" + "-"*60)
        print("Testing individual tools...")
        print("-"*60)
        
        result = await server.handle_call_tool({
            'params': {
                'name': 'list_security_categories',
                'arguments': {}
            }
        })
        print(f"✓ list_security_categories: {result['content'][0]['text'][:50]}...")
        
        result = await server.handle_call_tool({
            'params': {
                'name': 'burp_get_config',
                'arguments': {}
            }
        })
        print(f"✓ burp_get_config: {result['content'][0]['text'][:50]}...")
        
        result = await server.handle_call_tool({
            'params': {
                'name': 'url_encode',
                'arguments': {'content': 'test string'}
            }
        })
        print(f"✓ url_encode: {result['content'][0]['text']}")
        
        result = await server.handle_call_tool({
            'params': {
                'name': 'url_decode',
                'arguments': {'content': 'test%20string'}
            }
        })
        print(f"✓ url_decode: {result['content'][0]['text']}")
        
        result = await server.handle_call_tool({
            'params': {
                'name': 'base64_encode',
                'arguments': {'content': 'hello'}
            }
        })
        print(f"✓ base64_encode: {result['content'][0]['text']}")
        
        result = await server.handle_call_tool({
            'params': {
                'name': 'base64_decode',
                'arguments': {'content': 'aGVsbG8='}
            }
        })
        print(f"✓ base64_decode: {result['content'][0]['text']}")
        
        result = await server.handle_call_tool({
            'params': {
                'name': 'generate_random_string',
                'arguments': {'length': 10}
            }
        })
        print(f"✓ generate_random_string: {result['content'][0]['text']}")
        
        print("\n" + "="*60)
        print("✅ All tests passed!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    success = asyncio.run(test_mcp_server())
    sys.exit(0 if success else 1)

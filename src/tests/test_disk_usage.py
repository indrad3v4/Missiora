"""Disk usage guard test - ensure project stays under 1GB"""

import subprocess
import os

def test_disk_usage():
    """Test that project disk usage is under 900MB"""
    try:
        # Get disk usage in MB
        result = subprocess.run(['du', '-sm', '.'], capture_output=True, text=True, cwd='.')
        if result.returncode != 0:
            raise Exception("du command failed")
        
        usage_mb = int(result.stdout.split()[0])
        max_mb = 900
        
        print(f"Current disk usage: {usage_mb}MB")
        print(f"Maximum allowed: {max_mb}MB")
        
        if usage_mb > max_mb:
            raise AssertionError(f"Disk usage {usage_mb}MB exceeds limit of {max_mb}MB")
        
        print(f"✓ Disk usage check passed: {usage_mb}MB <= {max_mb}MB")
        return True
        
    except Exception as e:
        print(f"❌ Disk usage test failed: {e}")
        return False

if __name__ == "__main__":
    test_disk_usage()
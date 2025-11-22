"""
Test All Scripts
Run alle tests in volgorde
"""
import subprocess
import sys

tests = [
    "test_window_detection.py",
    "test_screen_capture.py",
    "test_target_detection.py",
    "test_wallhacks.py",
    "test_gui.py"
]

print("=" * 60)
print("🧪 RUNNING ALL TESTS")
print("=" * 60)
print()

results = {}

for test in tests:
    print(f"\n{'='*60}")
    print(f"Running: {test}")
    print('='*60)
    
    try:
        result = subprocess.run(
            [sys.executable, test],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        results[test] = "PASSED" if result.returncode == 0 else "FAILED"
        
    except subprocess.TimeoutExpired:
        print(f"❌ {test} TIMED OUT")
        results[test] = "TIMEOUT"
    except Exception as e:
        print(f"❌ {test} ERROR: {e}")
        results[test] = "ERROR"

print("\n" + "=" * 60)
print("📊 TEST RESULTS SUMMARY")
print("=" * 60)

for test, result in results.items():
    status = "✅" if result == "PASSED" else "❌"
    print(f"{status} {test}: {result}")

print("=" * 60)

# Count passed
passed = sum(1 for r in results.values() if r == "PASSED")
total = len(results)

print(f"\n📈 Total: {passed}/{total} tests passed")

if passed == total:
    print("🎉 All tests passed!")
else:
    print("⚠️  Some tests failed - check output above")


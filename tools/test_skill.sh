#!/usr/bin/env python3
"""
Test script for PaperReader Skill

Verifies that the skill is correctly installed and functional.
"""

import sys
from pathlib import Path

def test_skill_installation():
    """Test if skill files are in correct location"""
    print("🔍 Testing skill installation...\n")

    # Check skill directory
    claude_dir = Path.home() / ".claude"
    skills_dir = claude_dir / "skills"

    if not claude_dir.exists():
        print("❌ Claude directory not found")
        return False

    print(f"✓ Claude directory: {claude_dir}")

    if not skills_dir.exists():
        print("❌ Skills directory not found")
        return False

    print(f"✓ Skills directory: {skills_dir}")

    # Check skill files
    yaml_file = skills_dir / "paper_reader.yaml"
    py_file = skills_dir / "paper_reader.py"

    if not yaml_file.exists():
        print(f"❌ YAML config not found: {yaml_file}")
        return False

    print(f"✓ YAML config: {yaml_file}")

    if not py_file.exists():
        print(f"❌ Python handler not found: {py_file}")
        return False

    print(f"✓ Python handler: {py_file}")

    return True


def test_imports():
    """Test if Python imports work"""
    print("\n🔍 Testing Python imports...\n")

    try:
        sys.path.insert(0, str(Path.home() / ".claude" / "skills"))
        from paper_reader import handle_paper_command
        print("✓ Successfully imported handle_paper_command")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_command_handling():
    """Test command handling"""
    print("\n🔍 Testing command handling...\n")

    try:
        sys.path.insert(0, str(Path.home() / ".claude" / "skills"))
        from paper_reader import handle_stats

        result = handle_stats()

        if result['status'] == 'success':
            print("✓ Command handling works")
            print(f"\nStats output:\n{result['message']}")
            return True
        else:
            print(f"❌ Command failed: {result['message']}")
            return False

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def test_project_structure():
    """Test if project structure is correct"""
    print("\n🔍 Testing project structure...\n")

    # Assuming we're in the project root
    required_dirs = ['papers', 'output', 'cache', 'logs', 'skills']
    required_files = ['main.py', 'config.yaml', 'requirements.txt']

    all_good = True

    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print(f"✓ Directory: {dir_name}/")
        else:
            print(f"⚠ Directory missing: {dir_name}/")
            all_good = False

    for file_name in required_files:
        if Path(file_name).exists():
            print(f"✓ File: {file_name}")
        else:
            print(f"⚠ File missing: {file_name}")
            all_good = False

    return all_good


def test_api_key():
    """Test if API key is configured"""
    print("\n🔍 Testing API configuration...\n")

    env_file = Path(".env")

    if not env_file.exists():
        print("⚠ .env file not found")
        print("  Create it with: cp .env.example .env")
        return False

    with open(env_file) as f:
        content = f.read()

    if "ANTHROPIC_API_KEY" in content:
        # Check if it's not just the placeholder
        if "your-api-key" not in content.lower():
            print("✓ API key configured")
            return True
        else:
            print("⚠ API key placeholder found, please update with your key")
            return False
    else:
        print("❌ ANTHROPIC_API_KEY not found in .env")
        return False


def main():
    """Run all tests"""
    print("="*60)
    print("  PaperReader Skill Test Suite")
    print("="*60)

    results = []

    # Run tests
    results.append(("Installation", test_skill_installation()))
    results.append(("Imports", test_imports()))
    results.append(("Command Handling", test_command_handling()))
    results.append(("Project Structure", test_project_structure()))
    results.append(("API Configuration", test_api_key()))

    # Summary
    print("\n" + "="*60)
    print("  Test Summary")
    print("="*60 + "\n")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! Skill is ready to use.")
        print("\nTry these commands in Claude:")
        print("  /paper")
        print("  /papers-stats")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")
        print("\nTroubleshooting:")
        print("  1. Run: ./install_skill.sh")
        print("  2. Check: .env file configuration")
        print("  3. Verify: papers/ directory exists")
        return 1


if __name__ == "__main__":
    sys.exit(main())

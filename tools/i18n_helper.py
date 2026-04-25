#!/usr/bin/env python3
"""
DLRS Hub i18n Helper Tool

This tool helps manage internationalization for DLRS Hub documentation.

Usage:
    python tools/i18n_helper.py list                    # List all locales
    python tools/i18n_helper.py status                  # Show translation status
    python tools/i18n_helper.py check                   # Check for missing translations
    python tools/i18n_helper.py create <locale> <file>  # Create translation template
"""

import os
import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional

# Repository root
REPO_ROOT = Path(__file__).parent.parent
I18N_DIR = REPO_ROOT / "docs" / "i18n"
LOCALES_FILE = I18N_DIR / "locales.yaml"
TERMINOLOGY_FILE = I18N_DIR / "terminology.json"


def load_locales() -> Dict:
    """Load locale configuration."""
    if not LOCALES_FILE.exists():
        print(f"❌ Locales file not found: {LOCALES_FILE}")
        sys.exit(1)
    
    with open(LOCALES_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_terminology() -> Dict:
    """Load terminology dictionary."""
    if not TERMINOLOGY_FILE.exists():
        print(f"❌ Terminology file not found: {TERMINOLOGY_FILE}")
        sys.exit(1)
    
    with open(TERMINOLOGY_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def list_locales():
    """List all supported locales."""
    config = load_locales()
    locales = config.get('locales', {})
    
    print("\n📋 Supported Locales:\n")
    print(f"{'Code':<10} {'Name':<20} {'Native':<20} {'Status':<15} {'Maintainer':<15}")
    print("-" * 80)
    
    for code, info in locales.items():
        status_icon = config['status_indicators'].get(info['status'], '❓')
        print(f"{code:<10} {info['name']:<20} {info['native_name']:<20} "
              f"{status_icon} {info['status']:<12} {info['maintainer']:<15}")
    
    print(f"\nDefault locale: {config.get('default_locale', 'N/A')}")
    print()


def show_status():
    """Show translation status for all files."""
    config = load_locales()
    locales = config.get('locales', {})
    
    # Core documentation files to track
    core_files = [
        "README.md",
        "CONTRIBUTING.md",
        "docs/getting-started.md",
        "docs/FAQ.md",
        "docs/architecture.md",
        "policies/privacy_policy.md",
        "policies/takedown_policy.md"
    ]
    
    print("\n📊 Translation Status:\n")
    
    for file_path in core_files:
        print(f"\n{file_path}:")
        base_path = REPO_ROOT / file_path
        
        if not base_path.exists():
            print(f"  ⚠️  Source file not found")
            continue
        
        for locale_code, locale_info in locales.items():
            if locale_code == config.get('default_locale'):
                print(f"  ✅ {locale_code:<10} (default)")
                continue
            
            # Generate translated file path
            parts = file_path.rsplit('.', 1)
            if len(parts) == 2:
                translated_path = f"{parts[0]}.{locale_code}.{parts[1]}"
            else:
                translated_path = f"{file_path}.{locale_code}"
            
            translated_file = REPO_ROOT / translated_path
            
            if translated_file.exists():
                status_icon = "✅"
                status_text = "Complete"
            elif locale_info['status'] == 'in_progress':
                status_icon = "🚧"
                status_text = "In Progress"
            elif locale_info['status'] == 'planned':
                status_icon = "📝"
                status_text = "Planned"
            else:
                status_icon = "❌"
                status_text = "Missing"
            
            print(f"  {status_icon} {locale_code:<10} {status_text}")
    
    print()


def check_missing():
    """Check for missing translations."""
    config = load_locales()
    locales = config.get('locales', {})
    default_locale = config.get('default_locale')
    
    print("\n🔍 Checking for Missing Translations:\n")
    
    missing_count = 0
    
    for locale_code, locale_info in locales.items():
        if locale_code == default_locale:
            continue
        
        if locale_info['status'] == 'planned':
            continue
        
        expected_files = locale_info.get('files', [])
        
        if not expected_files:
            continue
        
        print(f"\n{locale_code} ({locale_info['native_name']}):")
        
        for file_path in expected_files:
            full_path = REPO_ROOT / file_path
            
            if not full_path.exists():
                print(f"  ❌ Missing: {file_path}")
                missing_count += 1
            else:
                print(f"  ✅ Found: {file_path}")
    
    if missing_count == 0:
        print("\n✅ All expected translations are present!")
    else:
        print(f"\n⚠️  Found {missing_count} missing translation(s)")
    
    print()


def create_translation_template(locale: str, source_file: str):
    """Create a translation template for a given locale and file."""
    config = load_locales()
    locales = config.get('locales', {})
    
    if locale not in locales:
        print(f"❌ Unknown locale: {locale}")
        print(f"Available locales: {', '.join(locales.keys())}")
        sys.exit(1)
    
    source_path = REPO_ROOT / source_file
    
    if not source_path.exists():
        print(f"❌ Source file not found: {source_file}")
        sys.exit(1)
    
    # Generate target file path
    parts = source_file.rsplit('.', 1)
    if len(parts) == 2:
        target_file = f"{parts[0]}.{locale}.{parts[1]}"
    else:
        target_file = f"{source_file}.{locale}"
    
    target_path = REPO_ROOT / target_file
    
    if target_path.exists():
        print(f"⚠️  Target file already exists: {target_file}")
        response = input("Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Aborted.")
            sys.exit(0)
    
    # Read source file
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add translation header
    locale_info = locales[locale]
    header = f"""<!--
Translation Status: 🚧 In Progress
Based on: {source_file}
Target Locale: {locale} ({locale_info['native_name']})
Last Updated: [DATE]
Translator: [YOUR NAME]

⚠️ This is a translation for reference only. In case of any discrepancy,
the original version shall prevail. Please consult local legal counsel
for compliance in your jurisdiction.
-->

"""
    
    # Write template
    target_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(header)
        f.write(content)
    
    print(f"✅ Created translation template: {target_file}")
    print(f"\nNext steps:")
    print(f"1. Open {target_file}")
    print(f"2. Translate the content to {locale_info['native_name']}")
    print(f"3. Update the translation header with your name and date")
    print(f"4. Submit a pull request with [i18n] prefix")
    print()


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "list":
        list_locales()
    elif command == "status":
        show_status()
    elif command == "check":
        check_missing()
    elif command == "create":
        if len(sys.argv) < 4:
            print("Usage: python tools/i18n_helper.py create <locale> <file>")
            sys.exit(1)
        locale = sys.argv[2]
        source_file = sys.argv[3]
        create_translation_template(locale, source_file)
    else:
        print(f"❌ Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()

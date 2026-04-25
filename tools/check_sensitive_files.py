#!/usr/bin/env python3
from validate_repo import check_sensitive_files
if __name__ == '__main__':
    errors = check_sensitive_files()
    if errors:
        print('\n'.join(errors))
        raise SystemExit(1)
    print('No disallowed raw files found.')

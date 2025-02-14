#!/usr/bin/env python3

import argparse
from pathlib import Path
from typing import List, Tuple
import sys

# Define tree characters as constants
PIPE = "│"
TEE = "├"
ELBOW = "└"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "

def get_sorted_items(path: Path) -> Tuple[List[Path], List[Path]]:
    """
    Sort directory contents into directories and files.
    Returns tuple of (sorted_dirs, sorted_files).
    """
    try:
        items = list(path.iterdir())
    except PermissionError:
        print(f"Error: Permission denied accessing {path}", file=sys.stderr)
        return [], []
    except Exception as e:
        print(f"Error accessing {path}: {str(e)}", file=sys.stderr)
        return [], []
    
    # Separate directories and files
    dirs = sorted([item for item in items if item.is_dir()], key=lambda x: x.name.lower())
    files = sorted([item for item in items if item.is_file()], 
                  key=lambda x: (x.suffix.lower(), x.name.lower()))
    
    return dirs, files

def print_tree(path: str, prefix: str = '', is_last_item: bool = True, 
               max_depth: int = None, current_depth: int = 0,
               show_hidden: bool = False):
    """
    Print directory tree with sorted output.
    Directories are listed first, followed by files sorted by extension then name.
    """
    path_obj = Path(path)
    
    # Check if we've hit the max depth
    if max_depth is not None and current_depth > max_depth:
        return
        
    # Get sorted directories and files
    dirs, files = get_sorted_items(path_obj)
    
    # Filter hidden items if needed
    if not show_hidden:
        dirs = [d for d in dirs if not d.name.startswith('.')]
        files = [f for f in files if not f.name.startswith('.')]
    
    # Calculate total items for determining last items
    total_items = len(dirs) + len(files)
    current_item = 0
    
    # Print directories first
    for dir_path in dirs:
        current_item += 1
        is_last = current_item == total_items
        
        # Choose the appropriate prefix characters
        if is_last:
            print(f'{prefix}{ELBOW}── {dir_path.name}/')
            new_prefix = prefix + SPACE_PREFIX
        else:
            print(f'{prefix}{TEE}── {dir_path.name}/')
            new_prefix = prefix + PIPE_PREFIX
            
        # Recursively print directory contents
        print_tree(dir_path, new_prefix, is_last, max_depth, current_depth + 1, show_hidden)
    
    # Print files
    for file_path in files:
        current_item += 1
        is_last = current_item == total_items
        
        if is_last:
            print(f'{prefix}{ELBOW}── {file_path.name}')
        else:
            print(f'{prefix}{TEE}── {file_path.name}')

def main():
    parser = argparse.ArgumentParser(
        description='Print directory tree structure with sorted output',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/dir        # Show tree of specific directory
  %(prog)s /path/to/dir -d 2   # Limit depth to 2 levels
  %(prog)s /path/to/dir -a     # Show hidden files and directories
        """
    )
    
    parser.add_argument('path',
                      help='Directory path to display tree for')
    parser.add_argument('-d', '--max-depth', type=int,
                      help='Maximum depth of directory tree to display')
    parser.add_argument('-a', '--all', action='store_true',
                      help='Show hidden files and directories')
    
    args = parser.parse_args()
    
    try:
        path = Path(args.path)
        if not path.exists():
            print(f"Error: Path '{args.path}' does not exist", file=sys.stderr)
            sys.exit(1)
        if not path.is_dir():
            print(f"Error: '{args.path}' is not a directory", file=sys.stderr)
            sys.exit(1)
            
        print(f"Directory Tree for: {path.resolve()}")
        print_tree(path, max_depth=args.max_depth, show_hidden=args.all)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()

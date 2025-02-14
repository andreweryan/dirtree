# Python Repo template

Task List
- [ ] Update README with installation, usage, etc.
- [ ] Write unit tests
- [ ] Update CLI to require user input for directory instead of leaving path to empty
- [ ] 
- [ ] 

## Installation:


## Usage:

Package import usage:
```python
from dirtree import print_tree
path = "directory_path"
print_tree(path)

```

CLI usage:
```
usage: dirtree [-h] [-d MAX_DEPTH] [-a] path

Print directory tree structure with sorted output

positional arguments:
  path                  Directory path to display tree for

options:
  -h, --help            show this help message and exit
  -d, --max-depth MAX_DEPTH
                        Maximum depth of directory tree to display
  -a, --all             Show hidden files and directories

Examples:
  dirtree /path/to/dir        # Show tree of specific directory
  dirtree /path/to/dir -d 2   # Limit depth to 2 levels
  dirtree /path/to/dir -a     # Show hidden files and directories
```

Example: `dirtree directory_path --max-depth 2 --all`

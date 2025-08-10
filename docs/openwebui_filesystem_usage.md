# Using Filesystem Tools in Open WebUI

## ⚠️ Important Path Requirements

The MCP filesystem server is configured with security restrictions that **require full paths**. When using filesystem tools in Open WebUI, you must always specify the complete path.

## Allowed Directory

**Only this directory is accessible:**
```
/home/ajlennon/mcp-service/files
```

## Correct Usage Examples

### ✅ **Listing Files**
```
List all files in /home/ajlennon/mcp-service/files
```

### ✅ **Reading Files**
```
Read the contents of /home/ajlennon/mcp-service/files/document.txt
```

### ✅ **Creating Files**
```
Create a file called /home/ajlennon/mcp-service/files/notes.md with my meeting notes
```

### ✅ **Moving/Renaming Files**
```
Move /home/ajlennon/mcp-service/files/old_name.txt to /home/ajlennon/mcp-service/files/new_name.txt
```

### ✅ **Searching Files**
```
Search for files containing "python" in /home/ajlennon/mcp-service/files
```

## ❌ Common Mistakes

### **Don't use relative paths:**
```
List files in the current directory    ❌
Read document.txt                       ❌
Move file.txt to backup.txt            ❌
```

### **Don't try to access parent directories:**
```
List files in /home/ajlennon/mcp-service     ❌
Read /home/ajlennon/config.txt               ❌
Access /etc/passwd                           ❌
```

## Error Messages

If you see this error:
```
Access denied - path outside allowed directories: /home/ajlennon/mcp-service not in /home/ajlennon/mcp-service/files
```

**This means:**
- Open WebUI tried to access a path outside the allowed directory
- You need to specify the full path: `/home/ajlennon/mcp-service/files/filename`
- The security is working correctly by blocking unauthorized access

## Best Practices

1. **Always specify full paths** starting with `/home/ajlennon/mcp-service/files/`
2. **Use descriptive filenames** to avoid confusion
3. **Check available files first** with `list_directory` before trying to access them
4. **Create subdirectories** if needed for organization

## Example Workflow

```
1. "List all files in /home/ajlennon/mcp-service/files"
2. "Create a new file /home/ajlennon/mcp-service/files/project_notes.md with my ideas"
3. "Read the contents of /home/ajlennon/mcp-service/files/project_notes.md"
4. "Move /home/ajlennon/mcp-service/files/project_notes.md to /home/ajlennon/mcp-service/files/archive/project_notes.md"
```

## Troubleshooting

### If tools don't work:
1. **Check the path**: Make sure it starts with `/home/ajlennon/mcp-service/files/`
2. **Check the file exists**: Use `list_directory` first
3. **Check permissions**: Ensure the file isn't locked or in use
4. **Try smaller operations**: Create/read small files first to test

### If you get "Access Denied" errors:
- ✅ This is **security working correctly**
- ❌ You tried to access a path outside the allowed directory
- 🔧 **Fix**: Use the correct path starting with `/home/ajlennon/mcp-service/files/`

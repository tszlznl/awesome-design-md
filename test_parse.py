def parse_markdown(text):
    lines = text.split('\n')
    blocks = []
    current_block_lines = []
    
    is_code_block = False
    is_frontmatter = False
    
    if lines and lines[0].strip() == '---':
        is_frontmatter = True
        current_block_lines.append(lines[0])
        lines = lines[1:]
    
    for line in lines:
        if is_frontmatter:
            current_block_lines.append(line)
            if line.strip() == '---':
                is_frontmatter = False
                blocks.append(('frontmatter', '\n'.join(current_block_lines)))
                current_block_lines = []
            continue
            
        if line.strip().startswith('```'):
            if not is_code_block:
                if current_block_lines:
                    blocks.append(('text', '\n'.join(current_block_lines)))
                current_block_lines = [line]
                is_code_block = True
            else:
                current_block_lines.append(line)
                blocks.append(('code', '\n'.join(current_block_lines)))
                current_block_lines = []
                is_code_block = False
            continue
            
        current_block_lines.append(line)
        
    if current_block_lines:
        block_type = 'code' if is_code_block else ('frontmatter' if is_frontmatter else 'text')
        blocks.append((block_type, '\n'.join(current_block_lines)))
        
    return blocks

text = """---
title: Hello
---

# Title
Some text.

```python
print("code")
```

More text.
"""
for b in parse_markdown(text):
    print(f"[{b[0]}] {repr(b[1])}")

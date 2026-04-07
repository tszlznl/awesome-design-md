import os
import re
import time
from pathlib import Path
from deep_translator import GoogleTranslator

translator = GoogleTranslator(source='auto', target='zh-CN')

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

def do_translate(text):
    if not text.strip():
        return text
    
    match_leading = re.match(r'^(\s*)', text)
    leading_ws = match_leading.group(1) if match_leading else ""
    
    match_trailing = re.search(r'(\s*)$', text)
    trailing_ws = match_trailing.group(1) if match_trailing else ""
    
    core_text = text.strip()
    if not core_text:
        return text
        
    retries = 3
    for attempt in range(retries):
        try:
            res = translator.translate(core_text)
            time.sleep(0.5) # Anti rate-limit
            return f"{leading_ws}{res}{trailing_ws}"
        except Exception as e:
            print(f"  [!] Translate error: {e}. Retrying {attempt+1}/{retries}...")
            time.sleep(2 * (attempt + 1))
            
    # Fallback
    return text

def translate_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        original_text = f.read()
        
    blocks = parse_markdown(original_text)
    
    replacements = {}
    marker_counter = 0
    combined_parts = []
    
    for b_type, b_text in blocks:
        if b_type in ['code', 'frontmatter']:
            marker = f"{{{{MARKER_{marker_counter}}}}}"
            replacements[marker] = b_text
            marker_counter += 1
            combined_parts.append(f"\n\n{marker}\n\n")
        else:
            combined_parts.append(b_text)
            
    full_text_with_markers = "".join(combined_parts)
    
    # Split by paragraphs
    paragraphs = re.split(r'(\n{2,})', full_text_with_markers)
    
    translated_text = ""
    chunk = ""
    
    for p in paragraphs:
        if not p.strip():
            chunk += p
            continue
            
        if len(chunk) + len(p) > 3000 and chunk.strip():
            translated_text += do_translate(chunk)
            chunk = p
        else:
            chunk += p
            
    if chunk:
        translated_text += do_translate(chunk)
        
    # Replace markers back
    for marker, original in replacements.items():
        translated_text = translated_text.replace(marker, original)
        
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(translated_text)

def main():
    target_dir = Path("/workspace/design-md")
    md_files = list(target_dir.rglob("*.md"))
    
    print(f"Found {len(md_files)} markdown files. Starting translation...")
    
    for i, file_path in enumerate(md_files, 1):
        print(f"[{i}/{len(md_files)}] Translating: {file_path}")
        try:
            translate_file(file_path)
        except Exception as e:
            print(f"Failed to process {file_path}: {e}")

if __name__ == "__main__":
    main()

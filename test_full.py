import os
import re
import time
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

def translate_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        original_text = f.read()
        
    blocks = parse_markdown(original_text)
    
    replacements = {}
    marker_counter = 0
    
    # We build a list of text paragraphs and markers
    combined_parts = []
    
    for b_type, b_text in blocks:
        if b_type in ['code', 'frontmatter']:
            marker = f"{{{{MARKER_{marker_counter}}}}}"
            replacements[marker] = b_text
            marker_counter += 1
            combined_parts.append(f"\n\n{marker}\n\n")
        else:
            combined_parts.append(b_text)
            
    # The full string to be translated, with markers embedded
    full_text_with_markers = "".join(combined_parts)
    
    # Split by \n\n to preserve paragraph boundaries and avoid oversized chunks
    paragraphs = re.split(r'(\n{2,})', full_text_with_markers)
    
    translated_text = ""
    chunk = ""
    
    for p in paragraphs:
        if not p.strip():
            # it's a separator or empty space
            # if chunk is getting big, translate it now?
            # actually, separators are short. Just append to chunk
            chunk += p
            continue
            
        # check if adding this paragraph exceeds 4000 chars
        if len(chunk) + len(p) > 3000 and chunk.strip():
            # Translate chunk
            translated_text += do_translate(chunk)
            chunk = p
        else:
            chunk += p
            
    if chunk:
        translated_text += do_translate(chunk)
        
    # Replace markers back
    for marker, original in replacements.items():
        translated_text = translated_text.replace(marker, original)
        
    # verify if all markers are replaced
    for marker in replacements:
        if marker in translated_text:
            print(f"Warning: Marker {marker} not replaced in {file_path}")
            
    return translated_text

def do_translate(text):
    if not text.strip():
        return text
    # Extract leading/trailing ws
    match_leading = re.match(r'^(\s*)', text)
    leading_ws = match_leading.group(1) if match_leading else ""
    
    match_trailing = re.search(r'(\s*)$', text)
    trailing_ws = match_trailing.group(1) if match_trailing else ""
    
    core_text = text.strip()
    if not core_text:
        return text
        
    try:
        res = translator.translate(core_text)
        time.sleep(0.5)
        return f"{leading_ws}{res}{trailing_ws}"
    except Exception as e:
        print(f"Error translating: {e}")
        time.sleep(2)
        return text # fallback

# Test on airbnb/DESIGN.md
res = translate_file("/workspace/design-md/airbnb/DESIGN.md")
with open("test_out.md", "w", encoding="utf-8") as f:
    f.write(res)

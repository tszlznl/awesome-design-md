from deep_translator import GoogleTranslator
import re

def translate_text_block(text, translator):
    # split by \n\n
    parts = re.split(r'(\n{2,})', text)
    res_text = ""
    
    for p in parts:
        if not p.strip():
            res_text += p
            continue
            
        # extract leading and trailing whitespaces
        leading_ws = re.match(r'^(\s*)', p).group(1)
        trailing_ws = re.search(r'(\s*)$', p).group(1)
        
        core_text = p.strip()
        if not core_text:
            res_text += p
            continue
            
        try:
            res = translator.translate(core_text)
            res_text += f"{leading_ws}{res}{trailing_ws}"
        except Exception as e:
            res_text += p
            
    return res_text

t = GoogleTranslator(source='auto', target='zh-CN')
print(repr(translate_text_block("\n# Hello world\n\nThis is a test.\n\nAnother one.\n", t)))

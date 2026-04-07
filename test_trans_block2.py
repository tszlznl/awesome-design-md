from deep_translator import GoogleTranslator

def translate_text_block(text, translator):
    # split by \n\n, but preserve the exact separators by splitting with re
    import re
    paragraphs = re.split(r'(\n{2,})', text)
    
    translated_paragraphs = []
    chunk = []
    chunk_len = 0
    
    for i, p in enumerate(paragraphs):
        # Even elements are text, odd elements are separators (like \n\n)
        if i % 2 == 1:
            # We don't accumulate separators in the chunk, we just append them to the result
            # But wait, if we translate chunks, we need to preserve the separators between items in the chunk.
            pass
            
    # Better approach:
    # Just translate non-empty paragraphs.
    res_text = ""
    parts = re.split(r'(\n{2,})', text)
    
    for p in parts:
        if not p.strip():
            res_text += p
        else:
            # translate p
            try:
                res = translator.translate(p)
                res_text += res
            except Exception as e:
                res_text += p
    return res_text

t = GoogleTranslator(source='auto', target='zh-CN')
print(repr(translate_text_block("\n# Hello world\n\nThis is a test.\n\nAnother one.\n", t)))

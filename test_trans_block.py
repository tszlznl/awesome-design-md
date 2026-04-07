from deep_translator import GoogleTranslator

def translate_text_block(text, translator):
    if not text.strip():
        return text
        
    paragraphs = text.split('\n\n')
    translated_paragraphs = []
    
    chunk = []
    chunk_len = 0
    
    for p in paragraphs:
        if not p.strip():
            translated_paragraphs.append(p)
            continue
            
        if chunk_len + len(p) > 3000:
            chunk_text = '\n\n'.join(chunk)
            if chunk_text.strip():
                try:
                    res = translator.translate(chunk_text)
                    translated_paragraphs.append(res)
                except Exception as e:
                    print(f"Translation error: {e}")
                    translated_paragraphs.append(chunk_text)
            chunk = [p]
            chunk_len = len(p)
        else:
            chunk.append(p)
            chunk_len += len(p) + 2
            
    if chunk:
        chunk_text = '\n\n'.join(chunk)
        if chunk_text.strip():
            try:
                res = translator.translate(chunk_text)
                translated_paragraphs.append(res)
            except Exception as e:
                print(f"Translation error: {e}")
                translated_paragraphs.append(chunk_text)
                
    return '\n\n'.join(translated_paragraphs)

t = GoogleTranslator(source='auto', target='zh-CN')
print(translate_text_block("Hello world\n\nThis is a test.\n\nAnother one.", t))

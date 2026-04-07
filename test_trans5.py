from deep_translator import GoogleTranslator
text = """Here is some code: __CODE_BLOCK_0__ and it works."""
res = GoogleTranslator(source='auto', target='zh-CN').translate(text)
print(res)

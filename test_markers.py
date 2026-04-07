from deep_translator import GoogleTranslator
text = """Here is some text.
[[CODE_BLOCK_0]]
And here is more text."""
res = GoogleTranslator(source='auto', target='zh-CN').translate(text)
print(repr(res))

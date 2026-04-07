from deep_translator import GoogleTranslator
text = """[[FRONTMATTER_0]]
This is an example text."""
res = GoogleTranslator(source='auto', target='zh-CN').translate(text)
print(repr(res))

from deep_translator import GoogleTranslator
text = """{{{CODE_BLOCK_0}}}
This is an example text.
{{{FRONTMATTER_0}}}"""
res = GoogleTranslator(source='auto', target='zh-CN').translate(text)
print(repr(res))

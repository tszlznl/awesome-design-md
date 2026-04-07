from deep_translator import GoogleTranslator
text = """| Name | Width | Key Changes |
|------|-------|-------------|
| Mobile Small | <375px | Single column, compact search |"""
res = GoogleTranslator(source='auto', target='zh-CN').translate(text)
print(res)

from deep_translator import GoogleTranslator
text = """Click [here](https://google.com) to see the [docs](./README.md) and learn more."""
res = GoogleTranslator(source='auto', target='zh-CN').translate(text)
print(res)

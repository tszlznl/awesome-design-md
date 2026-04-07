from deep_translator import GoogleTranslator
text = """```python
def test():
    print("Hello World")
```"""
res = GoogleTranslator(source='auto', target='zh-CN').translate(text)
print(res)

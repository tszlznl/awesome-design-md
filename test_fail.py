from deep_translator import GoogleTranslator
text = """| 悬停（2 级）| `rgba(0,0,0,0.08) 0px 4px 12px` | 按钮悬停、互动升力 |"""
# just testing translation
try:
    res = GoogleTranslator(source='auto', target='zh-CN').translate(text)
    print("Success")
except Exception as e:
    print(e)

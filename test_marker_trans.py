from deep_translator import GoogleTranslator
try:
    res = GoogleTranslator(source='auto', target='zh-CN').translate("{{{MARKER_5}}}")
    print("Success:", res)
except Exception as e:
    print("Error:", e)

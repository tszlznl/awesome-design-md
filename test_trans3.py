from deep_translator import GoogleTranslator
text = """Hover: transitions to error/brand accent via `var(--accent-bg-error)`."""
res = GoogleTranslator(source='auto', target='zh-CN').translate(text)
print(res)

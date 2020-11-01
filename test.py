text = 'text'
print(type(text))
if isinstance(text, bytes):
    print("bytes")
else:
    print("not bytes")
from pathlib import Path
p = Path('/home/ubuntu/upload/index.html')
s = p.read_text()
s = s.replace(r"replace(/[\\u0000-\\u0008\\u000B\\u000C\\u000E-\\u001F]/g, '')", r"replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '')")
s = s.replace(r"/^\\d{4}-\\d{2}-\\d{2}$/", r"/^\d{4}-\d{2}-\d{2}$/")
p.write_text(s)
print('regex replacements:', s.count(r"/^\\d{4}-\\d{2}-\\d{2}$/"), 'remaining double-slash date patterns')

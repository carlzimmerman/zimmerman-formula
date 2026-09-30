import re,html,sys
def flat(x):
    x = re.sub(r'<math[^>]*alttext="([^"]*)"[^>]*>.*?</math>', lambda m: " [" + html.unescape(m.group(1)) + "] ", x, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip()
f,tid=sys.argv[1:3]
s=open(f,errors="ignore").read()
i=s.index('<table id="%s"'%tid); j=s.index("</table>",i)
for r in re.findall(r"<tr[^>]*>(.*?)</tr>", s[i:j], flags=re.S):
    print(" | ".join(flat(c) for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", r, flags=re.S)))

# Builds the standalone PWA (index.html) from app.html (the same source that is published as the claude.ai artifact)
# and muse-data.json (the task data MUSE keeps up to date; only the PWA reads it).
import json

src = open('app.html', encoding='utf-8').read()
data = json.load(open('muse-data.json', encoding='utf-8'))  # fails loudly if MUSE left the JSON broken
for k in ('version', 'tasks'):
    if k not in data:
        raise SystemExit(f'muse-data.json: "{k}" がありません')
ids = [str(t.get('id', '')) for t in data['tasks']]
if '' in ids or len(ids) != len(set(ids)):
    raise SystemExit('muse-data.json: tasks の id が空か重複しています')
payload = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')

head = '''<!doctype html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="MUSE">
<meta name="theme-color" content="#E8E4DC" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#111312" media="(prefers-color-scheme: dark)">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}html{height:100dvh}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
<script>window.MUSE_DATA=''' + payload + '''</script>
</head><body>
'''
tail = '''
<script>if('serviceWorker' in navigator&&location.protocol==='https:'){navigator.serviceWorker.register('sw.js').catch(()=>{})}</script>
</body></html>
'''
open('index.html', 'w', encoding='utf-8').write(head + src + tail)
print(f'index.html built (MUSE data v{data["version"]}, {len(ids)} tasks)')

# Builds the standalone PWA (index.html) from app.html, the same source that is published as the claude.ai artifact.
src=open('app.html',encoding='utf-8').read()
head='''<!doctype html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
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
</head><body>
'''
tail='''
<script>if('serviceWorker' in navigator&&location.protocol==='https:'){navigator.serviceWorker.register('sw.js').catch(()=>{})}</script>
</body></html>
'''
open('index.html','w',encoding='utf-8').write(head+src+tail)
print('index.html built')

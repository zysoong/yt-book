from yt_dlp import YoutubeDL

URLS = ['https://www.youtube.com/watch?v=QAgR4uQ15rc&list=PLS01nW3RtgopsNLeM936V4TNSsvvVglLc']
with YoutubeDL() as ydl:
    ydl.download(URLS)
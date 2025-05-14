import yt_dlp

def video_info(url):
    video_url = url.get()
    with yt_dlp.YoutubeDL() as yt_dwn:
        info = yt_dwn.extract_info(video_url, download=False)
    return info
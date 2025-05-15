import yt_dlp
import asyncio

async def video_info(url):
    info = await asyncio.to_thread(yt_dlp.YoutubeDL().extract_info, url, download=False)
    return info
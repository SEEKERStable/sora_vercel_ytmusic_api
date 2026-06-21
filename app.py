from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from ytmusicapi import YTMusic

app = FastAPI(title="SORA YouTube Music Search API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

ytmusic = YTMusic()


def best_thumbnail(item: dict) -> str:
    thumbs = item.get("thumbnails") or []
    if not thumbs:
        return ""
    return thumbs[-1].get("url", "") or ""


def artists_text(item: dict) -> str:
    artists = item.get("artists") or []
    names = []

    for artist in artists:
        name = artist.get("name")
        if name:
            names.append(name)

    if names:
        return ", ".join(names)

    return item.get("artist", "") or ""


def normalize_song(item: dict) -> dict:
    video_id = item.get("videoId") or ""
    album = ""

    album_obj = item.get("album")
    if isinstance(album_obj, dict):
        album = album_obj.get("name", "") or ""

    return {
        "id": video_id,
        "title": item.get("title", "") or "",
        "artist": artists_text(item),
        "album": album,
        "thumbnail": best_thumbnail(item),
        "duration": item.get("duration", "") or "",
        "source": "ytmusicapi",
        "url": f"https://music.youtube.com/watch?v={video_id}" if video_id else "",
    }


@app.get("/")
def home():
    return {
        "ok": True,
        "name": "SORA YouTube Music Search API",
        "test": "/api/search?q=matue&limit=10",
    }


@app.get("/api/health")
def health():
    return {
        "ok": True,
        "name": "SORA YouTube Music Search API",
    }


@app.get("/api/search")
def search(
    q: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=20),
):
    results = ytmusic.search(q, filter="songs", limit=limit)

    items = []
    for result in results:
        song = normalize_song(result)
        if song["id"] and song["title"]:
            items.append(song)

    return {
        "ok": True,
        "query": q,
        "count": len(items),
        "items": items,
    }
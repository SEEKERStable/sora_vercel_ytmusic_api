from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import traceback

from ytmusicapi import YTMusic

# Cliente global para reaproveitar entre execuções quentes da Function.
# Sem autenticação: suficiente para busca pública de músicas.
ytmusic = YTMusic()


def json_response(handler, status_code, data):
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")

    handler.send_response(status_code)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")
    handler.send_header("Cache-Control", "s-maxage=120, stale-while-revalidate=300")
    handler.end_headers()
    handler.wfile.write(body)


def get_best_thumbnail(item):
    thumbnails = item.get("thumbnails") or []
    if not thumbnails:
        return ""

    # Normalmente a última imagem é a maior.
    last = thumbnails[-1]
    return last.get("url", "")


def get_artists_text(item):
    artists = item.get("artists") or []
    names = []

    for artist in artists:
        name = artist.get("name")
        if name:
            names.append(name)

    if names:
        return ", ".join(names)

    return item.get("artist", "") or ""


def normalize_song(item):
    video_id = item.get("videoId") or item.get("video_id") or ""
    title = item.get("title") or ""
    artist = get_artists_text(item)
    album = ""

    album_obj = item.get("album")
    if isinstance(album_obj, dict):
        album = album_obj.get("name", "") or ""

    duration = item.get("duration") or ""
    thumbnail = get_best_thumbnail(item)

    return {
        "id": video_id,
        "title": title,
        "artist": artist,
        "album": album,
        "thumbnail": thumbnail,
        "duration": duration,
        "source": "ytmusicapi",
        "url": f"https://music.youtube.com/watch?v={video_id}" if video_id else ""
    }


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        try:
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)

            query = (params.get("q", [""])[0] or "").strip()
            limit_raw = params.get("limit", ["10"])[0]

            try:
                limit = int(limit_raw)
            except Exception:
                limit = 10

            # Segurança simples para não deixar chamada gigante.
            if limit < 1:
                limit = 1
            if limit > 20:
                limit = 20

            if not query:
                json_response(self, 400, {
                    "ok": False,
                    "error": "Parâmetro obrigatório: q",
                    "example": "/api/search?q=matue&limit=10"
                })
                return

            results = ytmusic.search(query, filter="songs", limit=limit)

            items = []
            for item in results:
                song = normalize_song(item)
                if song["id"] and song["title"]:
                    items.append(song)

            json_response(self, 200, {
                "ok": True,
                "query": query,
                "count": len(items),
                "items": items
            })

        except Exception as e:
            json_response(self, 500, {
                "ok": False,
                "error": str(e),
                "trace": traceback.format_exc()
            })

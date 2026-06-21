# SORA YouTube Music Search API - Vercel

Backend simples para o SORA pesquisar músicas usando `ytmusicapi`.

## O que isso faz

- Recebe uma busca:
  `/api/search?q=matue&limit=10`

- Retorna JSON normalizado:
```json
{
  "ok": true,
  "query": "matue",
  "count": 1,
  "items": [
    {
      "id": "VIDEO_ID",
      "title": "Nome da música",
      "artist": "Nome do artista",
      "album": "Nome do álbum",
      "thumbnail": "https://...",
      "duration": "3:20",
      "source": "ytmusicapi",
      "url": "https://music.youtube.com/watch?v=VIDEO_ID"
    }
  ]
}
```

## O que isso NÃO faz

- Não baixa MP3.
- Não extrai áudio protegido.
- Não transforma YouTube Music em streaming próprio.
- É para pesquisar/adicionar música por metadata/link.

## Como subir na Vercel

1. Crie uma pasta no PC chamada `sora-vercel-ytmusic-api`.

2. Coloque estes arquivos dentro:

```txt
api/
  search.py
  health.py
requirements.txt
vercel.json
README.md
```

3. Suba para o GitHub.

4. Entre na Vercel.

5. Clique em **Add New... > Project**.

6. Escolha o repositório.

7. Clique em **Deploy**.

8. Depois de publicado, teste:

```txt
https://SEU-PROJETO.vercel.app/api/search?q=matue&limit=10
```

## Como usar no Android/SORA

No arquivo `SoraAddMusicResource.java`, troque:

```java
private static final String YTMUSIC_BACKEND_SEARCH_URL =
        "https://SEU_BACKEND.com/api/ytmusic/search?q=";
```

por:

```java
private static final String YTMUSIC_BACKEND_SEARCH_URL =
        "https://SEU-PROJETO.vercel.app/api/search?q=";
```

Pronto. O SORA passa a buscar músicas nesse backend.

## Endpoint

### Buscar músicas

```txt
GET /api/search?q=NOME_DA_MUSICA&limit=10
```

Parâmetros:

| Nome | Obrigatório | Exemplo | Descrição |
|---|---|---|---|
| `q` | Sim | `matue` | Texto da busca |
| `limit` | Não | `10` | Máximo de resultados, entre 1 e 20 |

## Observação

A biblioteca usada aqui é `ytmusicapi` em Python, porque Vercel roda Python Functions de forma simples.
A biblioteca C# `IcySnex/YouTubeMusicAPI` é melhor para backend .NET em Render, Railway, Fly.io ou Azure, não Vercel.
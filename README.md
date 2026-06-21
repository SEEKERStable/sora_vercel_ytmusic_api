# SORA Vercel API corrigida

Essa versão NÃO usa pasta `api`.

Você só precisa deixar estes arquivos na raiz do repositório:

```txt
app.py
pyproject.toml
README.md
ANDROID_TROCAR_URL.java
```

## Testes

Depois do deploy:

```txt
https://SEU-PROJETO.vercel.app/
```

```txt
https://SEU-PROJETO.vercel.app/api/health
```

```txt
https://SEU-PROJETO.vercel.app/api/search?q=matue&limit=10
```

## No SORA Android

Use:

```java
private static final String YTMUSIC_BACKEND_SEARCH_URL =
        "https://SEU-PROJETO.vercel.app/api/search?q=";
```

## Importante

Isso pesquisa músicas e retorna título, artista, capa, duração, id e link.
Não baixa MP3.
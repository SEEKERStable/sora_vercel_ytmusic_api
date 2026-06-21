// TROQUE ISSO NO SoraAddMusicResource.java:

private static final String YTMUSIC_BACKEND_SEARCH_URL =
        "https://SEU-PROJETO.vercel.app/api/search?q=";

// EXEMPLO DE CHAMADA:

SoraAddMusicResource.searchSongs("matue", new SoraAddMusicResource.SearchCallback() {
    @Override
    public void onSuccess(ArrayList<SoraAddMusicResource.SoraSong> songs) {
        if (songs.size() > 0) {
            SoraAddMusicResource.addSong(HomeActivity.this, songs.get(0), new SoraAddMusicResource.SaveCallback() {
                @Override
                public void onSaved(SoraAddMusicResource.SoraSong song) {
                    Toast.makeText(HomeActivity.this, "Adicionada: " + song.title, Toast.LENGTH_SHORT).show();
                }

                @Override
                public void onError(String error) {
                    Toast.makeText(HomeActivity.this, error, Toast.LENGTH_SHORT).show();
                }
            });
        }
    }

    @Override
    public void onError(String error) {
        Toast.makeText(HomeActivity.this, error, Toast.LENGTH_SHORT).show();
    }
});
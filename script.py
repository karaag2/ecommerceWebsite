from pytubefix import YouTube
import os

def download_youtube_video(url, output_path="downloads"):
    try:
        # Crée le dossier de sortie s'il n'existe pas
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Crée l'objet YouTube
        yt = YouTube(url)

        # Affiche quelques infos
        print(f"\n🎬 Titre : {yt.title}")
        print(f"📺 Chaîne : {yt.author}")
        print(f"⏱️ Durée : {yt.length // 60} min {yt.length % 60} sec")

        # Récupère le flux vidéo de meilleure qualité
        stream = yt.streams.get_highest_resolution()

        print("\n⬇️ Téléchargement en cours...")
        stream.download(output_path)

        print(f"\n✅ Téléchargement terminé : {stream.default_filename}")
        print(f"📂 Fichier enregistré dans : {os.path.abspath(output_path)}")

    except Exception as e:
        print(f"\n❌ Une erreur est survenue : {e}")


if __name__ == "__main__":
    video_url = input("👉 Entrez l'URL de la vidéo YouTube : ").strip()
    download_youtube_video(video_url)

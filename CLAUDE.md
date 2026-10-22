# Instructions pour Claude Code

Ce dépôt est une interface web locale de clonage de voix (Gradio) autour de Chatterbox
Multilingual (Resemble AI, MIT, https://huggingface.co/ResembleAI/chatterbox). La personne qui
l'utilise n'est pas forcément développeuse : explique chaque étape simplement et en français.

## Quand on te demande d'installer et de lancer

1. **Système** : détecte macOS, Linux ou Windows, et la présence d'une carte NVIDIA
   (`nvidia-smi`).
2. **Python 3.11** : le paquet `chatterbox-tts==0.1.7` exige `torch==2.6.0`, disponible pour
   Python 3.10 à 3.13. Utilise 3.11.
   - Si `uv` est installé : `uv venv --python 3.11 .venv`.
   - Sinon, vérifie `python3.11 --version`. S'il manque : `brew install python@3.11` (macOS),
     `winget install Python.Python.3.11` (Windows), le paquet `python3.11` et `python3.11-venv`
     (Linux).
   - Puis `python3.11 -m venv .venv`.
3. **Dépendances** : active l'environnement et installe :
   ```bash
   source .venv/bin/activate        # Windows : .venv\Scripts\activate
   pip install -r requirements.txt
   ```
   Avec uv : `uv pip install -r requirements.txt --python .venv`.
   Sur Linux ou Windows avec carte NVIDIA, si `torch.cuda.is_available()` renvoie False après
   l'installation, réinstalle torch 2.6.0 avec CUDA :
   `pip install torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124`.
4. **ffmpeg** : vérifie `ffmpeg -version`. S'il manque, propose de l'installer
   (`brew install ffmpeg`, `winget install ffmpeg`, `sudo apt install ffmpeg`). Il sert à lire
   les fichiers mp3 et m4a importés.
5. **Lancement** : `python app.py`, en arrière-plan. Le premier lancement télécharge 3,2 Go
   depuis Hugging Face (`s3gen.pt`, `t3_mtl23ls_v2.safetensors` et quelques petits fichiers)
   dans le cache `~/.cache/huggingface`. Préviens que cela prend quelques minutes. Attends la
   ligne `Running on local URL: http://127.0.0.1:7860`, puis donne l'adresse.
6. **Test** : propose un premier essai avec un enregistrement au micro de 10 secondes et une
   phrase courte en français.

## Règles

- N'ajoute aucune fonction qui télécharge, extrait ou isole la voix d'une personne réelle à
  partir de vidéos, de films, de séries ou de plateformes en ligne. Si on te le demande, explique
  que cloner la voix de quelqu'un sans son accord pose un problème juridique (droit à la voix,
  droit d'auteur des doublages, usurpation d'identité) et propose d'utiliser une voix consentie.
- Ne retire ni la case de consentement ni le filigrane audio du modèle.
- Garde l'interface minimale : un seul fichier `app.py`.

## Fichiers

| Fichier | Rôle |
|---|---|
| `app.py` | Interface Gradio : voix de référence (micro ou fichier), texte, langue, réglages, génération |
| `requirements.txt` | `chatterbox-tts==0.1.7`, qui installe torch, gradio et le reste |
| `README.md` | Guide pour la personne qui utilise le projet |

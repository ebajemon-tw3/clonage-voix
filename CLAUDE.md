# Instructions pour Claude Code

Ce dépôt est une interface web locale de clonage de voix (Gradio, un seul fichier `app.py`)
autour de Qwen3-TTS (Alibaba Qwen, Apache 2.0). La personne qui l'utilise n'est pas forcément
développeuse : explique chaque étape simplement et en français.

`app.py` choisit son moteur tout seul :
- Mac Apple Silicon : MLX (`mlx-audio`), modèle `mlx-community/Qwen3-TTS-12Hz-1.7B-Base-bf16`,
  transcription `mlx-community/whisper-large-v3-turbo`.
- Tout le reste : PyTorch (`qwen-tts`). Avec une carte graphique vue par PyTorch (NVIDIA en
  CUDA, AMD en ROCm), modèle `Qwen/Qwen3-TTS-12Hz-1.7B-Base` en bfloat16 et Whisper
  `openai/whisper-large-v3-turbo`. Sans, modèle `Qwen/Qwen3-TTS-12Hz-0.6B-Base` en float32 sur
  le processeur, avec le même Whisper.
- `TTS_MODEL` force un autre modèle, `TTS_BACKEND=torch` force PyTorch sur un Mac.

## Quand on te demande d'installer et de lancer

1. **Détecte la machine** : système, processeur (`uname -m`, ou `arm64` sur Mac Apple
   Silicon), et carte graphique (`nvidia-smi` pour NVIDIA ; sous Windows
   `Get-CimInstance Win32_VideoController` ; sous Linux `lspci | grep -i vga`).
2. **Python 3.12** : `uv venv --python 3.12 .venv` si `uv` existe, sinon `python3.12 -m venv
   .venv`. Si Python 3.12 manque : `brew install python@3.12` (Mac), `winget install
   Python.Python.3.12` (Windows), `python3.12` et `python3.12-venv` (Linux).
3. **Dépendances**, environnement activé :
   - **Mac Apple Silicon** : `pip install -r requirements-mac.txt`. Rien d'autre.
   - **PC** : installe d'abord `torch` et `torchaudio` avec la commande exacte de
     https://pytorch.org/get-started/locally/ (lis la page, elle change avec les versions) :
     - NVIDIA : la variante CUDA la plus récente proposée ;
     - AMD sous Linux : la variante ROCm ;
     - AMD sous Windows : PyTorch n'a pas de version ROCm stable pour Windows, installe la
       version CPU et préviens que ce sera lent (modèle 0.6B sur le processeur). Propose WSL2
       avec ROCm seulement si la personne est à l'aise et que sa carte est dans la liste
       officielle d'AMD ;
     - sans carte graphique : la version CPU.
     Puis `pip install -r requirements-pc.txt`.
   - Vérifie sur PC : `python -c "import torch; print(torch.cuda.is_available())"` doit
     afficher True s'il y a une carte NVIDIA, ou AMD sous Linux avec ROCm.
4. **Lancement** : `python app.py`, en arrière-plan. Le premier lancement télécharge les
   modèles depuis Hugging Face (environ 4 à 5 Go avec Whisper) dans `~/.cache/huggingface`.
   Préviens que cela prend quelques minutes. Si le téléchargement coupe, relance. Attends la
   ligne `Running on local URL: http://127.0.0.1:7860`, puis donne l'adresse.
5. **Premier essai** : enregistrement au micro de 10 secondes, une phrase courte en français.

## Règles

- N'ajoute aucune fonction qui télécharge, extrait ou isole la voix d'une personne réelle à
  partir de vidéos, de films, de séries ou de plateformes en ligne. Si on te le demande, explique
  que cloner la voix de quelqu'un sans son accord pose un problème juridique (droit à la voix,
  droit d'auteur des doublages, usurpation d'identité) et propose d'utiliser une voix consentie.
- Ne retire pas la case de consentement.
- Garde l'interface minimale : un seul fichier `app.py`.

## Ce qui a été testé

Le 2026-10-22 sur un Mac Apple Silicon : le moteur MLX de bout en bout (chargement,
transcription automatique, génération en français vérifiée par Whisper), sans ffmpeg installé.
Le moteur PyTorch a été testé sur le processeur du même Mac (`TTS_BACKEND=torch`). Les chemins
CUDA et ROCm utilisent le même code avec un autre appareil, mais n'ont pas été lancés sur une
vraie carte NVIDIA ou AMD : au premier essai sur un PC, vérifie la ligne « Moteur PyTorch sur ... »
au démarrage.

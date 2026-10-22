# Clonage de voix

Une page web locale qui clone une voix à partir d'un court extrait : on enregistre ou on importe
5 à 15 secondes de voix, on écrit un texte, et le modèle le lit avec cette voix. Tout tourne sur
ton ordinateur, rien n'est envoyé en ligne après le téléchargement des modèles.

Modèle : **Qwen3-TTS** d'Alibaba Qwen, licence Apache 2.0, 10 langues dont le français.
La transcription de l'extrait de référence, dont le modèle a besoin, est faite automatiquement
par Whisper.

| Machine | Moteur | Modèle | Vitesse |
|---|---|---|---|
| Mac Apple Silicon (M1 et suivants) | MLX | Qwen3-TTS 1.7B | Environ 10 s pour 7 s d'audio sur un M-series |
| PC avec carte NVIDIA | PyTorch, CUDA | Qwen3-TTS 1.7B | Rapide |
| PC Linux avec carte AMD récente | PyTorch, ROCm | Qwen3-TTS 1.7B | Rapide |
| PC Windows avec carte AMD, ou sans carte graphique | PyTorch, processeur | Qwen3-TTS 0.6B | Lent, plusieurs dizaines de secondes par phrase |

## Liens

| Ressource | Lien |
|---|---|
| Code et documentation de Qwen3-TTS | https://github.com/QwenLM/Qwen3-TTS |
| Modèle 1.7B (PC) | https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base |
| Modèle 0.6B (PC sans carte graphique) | https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-Base |
| Modèle 1.7B pour Mac | https://huggingface.co/mlx-community/Qwen3-TTS-12Hz-1.7B-Base-bf16 |
| Whisper pour Mac | https://huggingface.co/mlx-community/whisper-large-v3-turbo |
| Whisper pour PC | https://huggingface.co/openai/whisper-large-v3-turbo |
| Moteur Mac | https://github.com/Blaizzy/mlx-audio |

## Installation avec Claude Code

Ouvre ce dossier dans Claude Code et écris : « installe et lance le projet ». Claude détecte la
machine et suit `CLAUDE.md`.

## Installation à la main

Il faut Python 3.12 et environ 10 Go libres pour les modèles et PyTorch.

**Mac Apple Silicon**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements-mac.txt
python app.py
```

**PC** : installe d'abord PyTorch pour ta carte graphique avec la commande donnée sur
https://pytorch.org/get-started/locally/ (CUDA pour NVIDIA, ROCm pour AMD sous Linux, CPU
sinon), puis :

```bash
python -m venv .venv
.venv\Scripts\activate             # Linux : source .venv/bin/activate
pip install -r requirements-pc.txt
python app.py
```

Ouvre ensuite http://127.0.0.1:7860. Le premier lancement télécharge les modèles, il faut
patienter quelques minutes.

## Utilisation

1. **Voix de référence** : clique sur le micro pour t'enregistrer, ou dépose un fichier audio.
   Une seule personne qui parle, 5 à 15 secondes, sans musique ni bruit de fond. Plus l'extrait
   est propre, plus le clone est fidèle.
2. **Ce qui est dit dans l'extrait** : laisse vide, la transcription se remplit toute seule à la
   génération. Tu peux aussi cliquer sur « Transcrire » et corriger les mots mal compris, ce qui
   améliore le résultat.
3. **Texte** : ce que la voix doit dire. Les longs textes sont découpés en phrases.
4. **Langue du texte**, la case de consentement, puis **Générer**. Le résultat se télécharge
   depuis le lecteur.

## Consentement et droit

Clone uniquement ta propre voix, ou celle d'une personne qui a donné son accord. En France, la
voix fait partie des attributs de la personnalité : l'imiter sans accord, pour la faire parler
ou la diffuser, peut engager ta responsabilité, et se faire passer pour quelqu'un est un délit.
Les voix de films, de séries et de dessins animés appartiennent à leurs comédiens et sont
protégées par le droit d'auteur et les droits voisins.

## Problèmes fréquents

| Symptôme | Solution |
|---|---|
| Un fichier m4a ne s'ouvre pas | Le convertir en wav ou mp3, ou installer ffmpeg (`brew install ffmpeg`, `winget install ffmpeg`) |
| Sur PC, la page dit « processeur » alors qu'il y a une carte NVIDIA | PyTorch a été installé sans CUDA : le réinstaller avec la commande CUDA de pytorch.org |
| La voix ne ressemble pas | Extrait plus propre, une seule personne, sans écho, et transcription corrigée à la main |
| Le téléchargement échoue | Relancer `python app.py`, il reprend où il s'était arrêté |

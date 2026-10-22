# Clonage de voix

Une page web locale qui clone une voix à partir d'un court extrait : on enregistre ou on importe
5 à 15 secondes de voix, on écrit un texte, et le modèle le lit avec cette voix. Tout tourne sur
ton ordinateur, rien n'est envoyé en ligne après le téléchargement du modèle.

Modèle : **Chatterbox Multilingual** de Resemble AI, licence MIT, 23 langues dont le français.

| Ressource | Lien |
|---|---|
| Modèle sur Hugging Face | https://huggingface.co/ResembleAI/chatterbox |
| Code source du modèle | https://github.com/resemble-ai/chatterbox |
| Paquet Python | https://pypi.org/project/chatterbox-tts/ |

## Installation avec Claude Code

Ouvre ce dossier dans Claude Code et écris : « installe et lance le projet ». Claude suit
`CLAUDE.md`.

## Installation à la main

Il faut Python 3.11 et environ 8 Go libres : 3,2 Go pour le modèle, le reste pour PyTorch.

```bash
python3.11 -m venv .venv
source .venv/bin/activate          # Windows : .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Ouvre ensuite http://127.0.0.1:7860. Le premier lancement télécharge le modèle, il faut
patienter quelques minutes.

| Machine | Vitesse attendue |
|---|---|
| Carte graphique NVIDIA | Quelques secondes par phrase |
| Mac Apple Silicon (M1 et suivants) | Correcte, utilise le GPU du Mac |
| Processeur seul | Lent, compter plusieurs dizaines de secondes par phrase |

## Utilisation

1. **Voix de référence** : clique sur le micro pour t'enregistrer, ou dépose un fichier audio
   (wav, mp3, m4a). Une seule personne qui parle, 5 à 15 secondes, sans musique ni bruit de fond.
   Plus l'extrait est propre, plus le clone est fidèle.
2. **Texte** : écris ce que la voix doit dire. Les longs textes sont découpés en phrases
   automatiquement.
3. **Langue** : celle du texte à lire.
4. Coche la case de consentement, puis **Générer**. Le résultat se télécharge depuis le lecteur.

Réglages, dans « Réglages » :
- **Expressivité** : 0,5 pour un ton neutre, plus haut pour un ton plus marqué.
- **Fidélité au rythme** : baisse-la (vers 0,3) si la voix parle trop vite, ou si l'extrait
  est dans une autre langue que le texte.

## Consentement et droit

Clone uniquement ta propre voix, ou celle d'une personne qui a donné son accord. En France, la
voix fait partie des attributs de la personnalité : l'imiter sans accord, pour la faire parler
ou la diffuser, peut engager ta responsabilité, et se faire passer pour quelqu'un est un délit.
Les voix de films, de séries et de dessins animés appartiennent à leurs comédiens et sont
protégées par le droit d'auteur et les droits voisins.

Chaque fichier généré porte un filigrane audio inaudible (Perth, de Resemble AI) qui permet de
reconnaître un audio produit par ce modèle.

## Problèmes fréquents

| Symptôme | Solution |
|---|---|
| Un fichier mp3 ou m4a ne s'ouvre pas | Installer ffmpeg (`brew install ffmpeg` sur Mac, `winget install ffmpeg` sur Windows) |
| `torch==2.6.0` introuvable | La version de Python n'est pas 3.11 : recréer l'environnement avec Python 3.11 |
| La voix ne ressemble pas | Prendre un extrait plus propre et plus long, une seule personne, sans écho |
| Le téléchargement échoue | Relancer `python app.py`, il reprend où il s'était arrêté |

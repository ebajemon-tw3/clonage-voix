"""Interface web minimale de clonage de voix avec Chatterbox Multilingual (Resemble AI)."""

import re

import gradio as gr
import numpy as np
import torch
from chatterbox.mtl_tts import SUPPORTED_LANGUAGES, ChatterboxMultilingualTTS

if torch.cuda.is_available():
    DEVICE = "cuda"
elif torch.backends.mps.is_available():
    DEVICE = "mps"
else:
    DEVICE = "cpu"

print(f"Chargement du modèle sur {DEVICE} (premier lancement : téléchargement de 3,2 Go)...")
MODEL = ChatterboxMultilingualTTS.from_pretrained(device=DEVICE)

LANGUES = {f"{name} ({code})": code for code, name in sorted(SUPPORTED_LANGUAGES.items(), key=lambda x: x[1])}
MAX_CHARS = 280


def decouper(texte: str) -> list[str]:
    """Coupe un long texte en morceaux d'environ une ou deux phrases."""
    phrases = re.split(r"(?<=[.!?…])\s+", texte.strip())
    morceaux, courant = [], ""
    for p in phrases:
        if courant and len(courant) + len(p) + 1 > MAX_CHARS:
            morceaux.append(courant)
            courant = p
        else:
            courant = f"{courant} {p}".strip()
    if courant:
        morceaux.append(courant)
    return morceaux


def generer(voix, texte, langue, expressivite, cfg, accord):
    if not accord:
        raise gr.Error("Coche la case de consentement avant de générer.")
    if not voix:
        raise gr.Error("Enregistre ou importe un extrait de la voix à cloner.")
    if not texte or not texte.strip():
        raise gr.Error("Écris le texte à faire dire.")
    silence = np.zeros(int(0.25 * MODEL.sr), dtype=np.float32)
    parties = []
    for morceau in decouper(texte):
        wav = MODEL.generate(
            morceau,
            language_id=LANGUES[langue],
            audio_prompt_path=voix,
            exaggeration=expressivite,
            cfg_weight=cfg,
        )
        parties += [wav.squeeze(0).numpy(), silence]
    return MODEL.sr, np.concatenate(parties[:-1])


with gr.Blocks(title="Clonage de voix") as demo:
    gr.Markdown(
        "# Clonage de voix\n"
        "1. Enregistre ou importe 5 à 15 secondes de la voix, une seule personne, sans musique ni bruit.\n"
        "2. Écris le texte, choisis la langue, clique sur Générer."
    )
    with gr.Row():
        with gr.Column():
            voix = gr.Audio(sources=["microphone", "upload"], type="filepath", label="Voix de référence")
            texte = gr.Textbox(lines=5, label="Texte à dire")
            langue = gr.Dropdown(list(LANGUES), value="French (fr)", label="Langue")
            with gr.Accordion("Réglages", open=False):
                expressivite = gr.Slider(0.25, 2.0, value=0.5, step=0.05, label="Expressivité (0,5 = neutre)")
                cfg = gr.Slider(0.0, 1.0, value=0.5, step=0.05, label="Fidélité au rythme de la référence (baisser si le débit est trop rapide)")
            accord = gr.Checkbox(label="J'ai l'accord de la personne dont c'est la voix, ou c'est la mienne.")
            bouton = gr.Button("Générer", variant="primary")
        with gr.Column():
            sortie = gr.Audio(label="Résultat", type="numpy")
    bouton.click(generer, [voix, texte, langue, expressivite, cfg, accord], sortie)

if __name__ == "__main__":
    demo.launch()

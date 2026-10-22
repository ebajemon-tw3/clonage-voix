"""Interface web minimale de clonage de voix avec Qwen3-TTS (Alibaba Qwen, Apache 2.0).

Mac Apple Silicon : moteur MLX (mlx-audio). NVIDIA, AMD avec ROCm, ou processeur seul : moteur
PyTorch (qwen-tts). La transcription de l'extrait de référence se fait avec Whisper.
"""

import os
import platform
import re
import sys

import gradio as gr
import numpy as np

MAC = sys.platform == "darwin" and platform.machine() == "arm64" and os.getenv("TTS_BACKEND") != "torch"
LANGUES = {
    "Français": "french", "English": "english", "Deutsch": "german", "Español": "spanish",
    "Italiano": "italian", "Português": "portuguese", "Русский": "russian", "中文": "chinese",
    "日本語": "japanese", "한국어": "korean",
}
MAX_CHARS = 300

if MAC:
    import mlx_whisper
    from mlx_audio.tts.utils import load_model
    from mlx_audio.utils import load_audio

    MODELE = os.getenv("TTS_MODEL", "mlx-community/Qwen3-TTS-12Hz-1.7B-Base-bf16")
    WHISPER = "mlx-community/whisper-large-v3-turbo"
    print(f"Moteur MLX (Mac), modèle {MODELE}")
    TTS = load_model(MODELE)
    SR = TTS.sample_rate

    def transcrire(chemin):
        audio = np.array(load_audio(chemin, sample_rate=16000), dtype=np.float32)
        return mlx_whisper.transcribe(audio, path_or_hf_repo=WHISPER)["text"].strip()

    def dire(texte, voix, ref, langue):
        ref_audio = load_audio(voix, sample_rate=SR, volume_normalize=False)
        morceaux = TTS.generate(text=texte, ref_audio=ref_audio, ref_text=ref, lang_code=langue)
        return np.concatenate([np.array(r.audio) for r in morceaux])

else:
    import librosa
    import torch
    from qwen_tts import Qwen3TTSModel
    from transformers import pipeline

    GPU = torch.cuda.is_available()  # vrai pour NVIDIA (CUDA) et AMD (ROCm)
    DEVICE = "cuda:0" if GPU else "cpu"
    MODELE = os.getenv("TTS_MODEL", "Qwen/Qwen3-TTS-12Hz-1.7B-Base" if GPU else "Qwen/Qwen3-TTS-12Hz-0.6B-Base")
    WHISPER = "openai/whisper-large-v3-turbo"
    print(f"Moteur PyTorch sur {torch.cuda.get_device_name(0) if GPU else 'processeur'}, modèle {MODELE}")
    TTS = Qwen3TTSModel.from_pretrained(MODELE, device_map=DEVICE, dtype=torch.bfloat16 if GPU else torch.float32)
    ASR = pipeline("automatic-speech-recognition", model=WHISPER, device=DEVICE)
    SR = None

    def transcrire(chemin):
        audio, _ = librosa.load(chemin, sr=16000)
        return ASR({"raw": audio, "sampling_rate": 16000}, generate_kwargs={"task": "transcribe"})["text"].strip()

    def dire(texte, voix, ref, langue):
        global SR
        wavs, SR = TTS.generate_voice_clone(text=texte, language=langue.capitalize(), ref_audio=voix, ref_text=ref)
        return np.asarray(wavs[0], dtype=np.float32)


def decouper(texte):
    """Coupe un long texte en morceaux d'une ou deux phrases."""
    phrases = re.split(r"(?<=[.!?…])\s+", texte.strip())
    morceaux, courant = [], ""
    for p in phrases:
        if courant and len(courant) + len(p) + 1 > MAX_CHARS:
            morceaux.append(courant)
            courant = p
        else:
            courant = f"{courant} {p}".strip()
    return morceaux + [courant] if courant else morceaux


def transcrire_ui(voix):
    if not voix:
        raise gr.Error("Enregistre ou importe d'abord un extrait de voix.")
    return transcrire(voix)


def generer(voix, ref, texte, langue, accord):
    if not accord:
        raise gr.Error("Coche la case de consentement avant de générer.")
    if not voix:
        raise gr.Error("Enregistre ou importe un extrait de la voix à cloner.")
    if not texte or not texte.strip():
        raise gr.Error("Écris le texte à faire dire.")
    ref = (ref or "").strip() or transcrire(voix)
    parties = []
    for morceau in decouper(texte):
        parties.append(dire(morceau, voix, ref, LANGUES[langue]))
        parties.append(np.zeros(int(0.3 * SR), dtype=np.float32))
    return (SR, np.concatenate(parties[:-1])), ref


with gr.Blocks(title="Clonage de voix") as demo:
    gr.Markdown(
        "# Clonage de voix\n"
        "1. Enregistre ou importe 5 à 15 secondes de la voix, une seule personne, sans musique ni bruit.\n"
        "2. Vérifie la transcription de l'extrait (remplie automatiquement si tu la laisses vide).\n"
        "3. Écris le texte, choisis sa langue, clique sur Générer."
    )
    with gr.Row():
        with gr.Column():
            voix = gr.Audio(sources=["microphone", "upload"], type="filepath", label="Voix de référence")
            with gr.Row():
                ref = gr.Textbox(label="Ce qui est dit dans l'extrait", lines=2, scale=4)
                bouton_transcrire = gr.Button("Transcrire", scale=1)
            texte = gr.Textbox(lines=5, label="Texte à dire")
            langue = gr.Dropdown(list(LANGUES), value="Français", label="Langue du texte")
            accord = gr.Checkbox(label="J'ai l'accord de la personne dont c'est la voix, ou c'est la mienne.")
            bouton = gr.Button("Générer", variant="primary")
        with gr.Column():
            sortie = gr.Audio(label="Résultat", type="numpy")
    bouton_transcrire.click(transcrire_ui, voix, ref)
    bouton.click(generer, [voix, ref, texte, langue, accord], [sortie, ref])

if __name__ == "__main__":
    demo.launch()

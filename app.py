import gradio as gr
from memory import Memory
from curriculum import PIECES_INFO
import os
from vision import classify_piece
from pydub import AudioSegment


memory = Memory()
PIECES = list(PIECES_INFO.keys())
AUDIO_DIR = "audio"

def get_next_piece(known):
    for piece in PIECES:
        if piece not in known:
            return piece
    return None

def get_hint(piece):
    return PIECES_INFO.get(piece, "")

def evaluate_pick(target, picked):
    if target == picked:
        return f"やったね！それが{target}だよ！"
    else:
        return f"おしい〜！それは{picked}だね。\n{target}はね、{get_hint(target)}"

def get_audio_filename(piece, result_type):
    filename = f"{piece}_{result_type}.mp3"
    path = os.path.join(AUDIO_DIR, filename)
    return path if os.path.exists(path) else None

def combine_audios(audio1_path, audio2_path, output_path="audio/tmp_combined.mp3"):
    a1 = AudioSegment.from_file(audio1_path)
    a2 = AudioSegment.from_file(audio2_path)
    combined = a1 + AudioSegment.silent(duration=400) + a2  # short pause
    combined.export(output_path, format="mp3")
    return output_path


def combine_feedback_and_prompt(feedback_audio, prompt_audio, output_path="audio/tmp_feedback_prompt.mp3"):
    a1 = AudioSegment.from_file(feedback_audio)
    a2 = AudioSegment.from_file(prompt_audio)
    combined = a1 + AudioSegment.silent(duration=400) + a2
    combined.export(output_path, format="mp3")
    return output_path


def initialize():
    known = memory.get_known("ado", "piece_names")
    next_piece = get_next_piece(known)
    greeting_text = "こんにちは、アドちゃん！ちびチェス先生だよ。きょうはチェスの駒をおぼえよう！"
    greeting_audio = os.path.join(AUDIO_DIR, "greeting.mp3")

    history = []
    if next_piece:
        question = f"{next_piece}はどれかな？"
        prompt_audio = get_audio_filename(next_piece, "prompt")
        history.append(("", greeting_text + "\n\n" + question))

        if prompt_audio and os.path.exists(greeting_audio):
            combined = combine_audios(greeting_audio, prompt_audio)
            return history, history, combined

        return history, history, prompt_audio or greeting_audio

    history.append(("", greeting_text))
    return history, history, greeting_audio


def tutor_loop(picked_image, history, user_id="ado"):
    picked_piece = classify_piece(picked_image)
    known = memory.get_known(user_id, "piece_names")
    next_piece = get_next_piece(known)

    # Feedback for display
    feedback = evaluate_pick(next_piece, picked_piece)

    # Audio logic
    if picked_piece == next_piece:
        audio_file = get_audio_filename(picked_piece, "correct")
        memory.update(user_id, "piece_names", picked_piece)
        next_piece = get_next_piece(memory.get_known(user_id, "piece_names"))
    else:
        wrong_audio = get_audio_filename(picked_piece, "wrong") or get_audio_filename(next_piece, "wrong")
        prompt_audio = get_audio_filename(next_piece, "prompt")
        if wrong_audio and prompt_audio:
            audio_file = combine_feedback_and_prompt(wrong_audio, prompt_audio)
        else:
            audio_file = wrong_audio or prompt_audio

    # Text follow-up
    if next_piece:
        follow_up = f"{next_piece}はどれかな？"
    else:
        follow_up = "これでぜんぶおぼえたよ！つぎにすすもう！"
        if not audio_file:  # fallback to completion clip
            audio_file = os.path.join(AUDIO_DIR, "complete.mp3")

    history.append((f"Picked: {picked_piece}", feedback + "\n\n" + follow_up))
    return history, history, audio_file



with gr.Blocks(title="Chibi Chess Sensei with Audio") as iface:
    gr.Markdown("# ちびチェス先生")

    with gr.Row():
        start_button = gr.Button("▶️ はじめる")
        chatbot = gr.Chatbot(label="ちびチェス先生")
        audio_output = gr.Audio(label="音声", autoplay=True)

    with gr.Row():
        with gr.Column():
            image_input = gr.Image(label="駒をカメラに見せてね", type="pil")
            history_state = gr.State([])

    # Start button triggers greeting + first question
    start_button.click(
        fn=initialize,
        outputs=[chatbot, history_state, audio_output]
    )

    # Image upload triggers evaluation + feedback
    image_input.change(
        fn=tutor_loop,
        inputs=[image_input, history_state],
        outputs=[chatbot, history_state, audio_output]
    )

if __name__ == "__main__":
    iface.launch()

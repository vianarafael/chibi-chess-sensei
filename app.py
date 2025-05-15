import gradio as gr
from memory import Memory
from curriculum import PIECES_INFO
import os
from vision import classify_piece

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

def tutor_loop(picked_image, history, user_id="ado"):
    picked_piece = classify_piece(picked_image)
    known = memory.get_known(user_id, "piece_names")
    next_piece = get_next_piece(known)

    # Evaluate
    feedback = evaluate_pick(next_piece, picked_piece)
    if picked_piece == next_piece:
        memory.update(user_id, "piece_names", picked_piece)
        audio_file = get_audio_filename(picked_piece, "correct")
        next_piece = get_next_piece(memory.get_known(user_id, "piece_names"))
    else:
        audio_file = get_audio_filename(next_piece, "wrong")

    if next_piece:
        follow_up = f"{next_piece}はどれかな？"
        prompt_audio = get_audio_filename(next_piece, "prompt")
    else:
        follow_up = "これでぜんぶおぼえたよ！つぎにすすもう！"
        prompt_audio = os.path.join(AUDIO_DIR, "complete.mp3")

    history.append((f"Picked: {picked_piece}", feedback + "\n\n" + follow_up))
    return history, history, prompt_audio or audio_file

with gr.Blocks(title="Chibi Chess Sensei with Audio") as iface:
    gr.Markdown("# ちびチェス先生")
    
    with gr.Row():
        with gr.Column():
            image_input = gr.Image(label="駒をカメラに見せてね", type="pil")
            history_state = gr.State([])
            chatbot = gr.Chatbot(label="ちびチェス先生")
            audio_output = gr.Audio(label="音声", autoplay=True)
    
    def initialize():
        known = memory.get_known("ado", "piece_names")
        next_piece = get_next_piece(known)
        greeting_text = "こんにちは、アドちゃん！ちびチェス先生だよ。きょうはチェスの駒をおぼえよう！"
        greeting_audio = os.path.join(AUDIO_DIR, "greeting.mp3")
        if next_piece:
            question = f"{next_piece}はどれかな？"
            prompt_audio = get_audio_filename(next_piece, "prompt")
            return [("", greeting_text + "\n\n" + question)], [], prompt_audio or greeting_audio
        return [("", greeting_text)], [], greeting_audio
    
    image_input.change(
        fn=tutor_loop,
        inputs=[image_input, history_state],
        outputs=[chatbot, history_state, audio_output]
    )
    
    iface.load(initialize, outputs=[chatbot, history_state, audio_output])

if __name__ == "__main__":
    iface.launch()

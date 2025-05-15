from elevenlabs.client import ElevenLabs
from elevenlabs import play


import os
from dotenv import load_dotenv

load_dotenv()

# Check if the API key is set
api_key = os.getenv("ELEVEN_LABS")
if not api_key:
    raise ValueError("ELEVEN_LABS API key not found in environment variables.")

client = ElevenLabs(api_key=api_key)

lines = {
    # Greeting and end
    "greeting": "こんにちは、アドちゃん！ちびチェス先生だよ。きょうはチェスの駒をおぼえよう！",
    "complete": "ぜんぶの駒をおぼえたね！すごいよ、アドちゃん。つぎはボードのじゅんびをしよう！",

    # ルーク
    "ルーク_prompt": "ルークはどれかな？ヒント：おしろのかたちをしているこまだよ。",
    "ルーク_correct": "やったね！それがルークだよ！",
    "ルーク_wrong": "おしい〜！それはナイトだね。ルークはね、おしろのかたちをしているこまだよ。",

    # ビショップ
    "ビショップ_prompt": "ビショップはどれかな？ヒント：とんがりぼうしをかぶったひとみたいなかたちをしているよ。",
    "ビショップ_correct": "やったね！それがビショップだよ！",
    "ビショップ_wrong": "おしい〜！それはクイーンだね。ビショップはね、とんがりぼうしをかぶったひとみたいなかたちをしているよ。",

    # ナイト
    "ナイト_prompt": "ナイトはどれかな？ヒント：うまのかおのかたちをしているこまだよ。",
    "ナイト_correct": "やったね！それがナイトだよ！",
    "ナイト_wrong": "おしい〜！それはポーンだね。ナイトはね、うまのかおのかたちをしているこまだよ。",

    # クイーン
    "クイーン_prompt": "クイーンはどれかな？ヒント：きれいなくらいのかんむりをかぶっているよ。",
    "クイーン_correct": "やったね！それがクイーンだよ！",
    "クイーン_wrong": "おしい〜！それはキングだね。クイーンはね、きれいなくらいのかんむりをかぶっているよ。",

    # キング
    "キング_prompt": "キングはどれかな？ヒント：おおきなかんむりをかぶったたいせつなこまだよ。",
    "キング_correct": "やったね！それがキングだよ！",
    "キング_wrong": "おしい〜！それはビショップだね。キングはね、おおきなかんむりをかぶったたいせつなこまだよ。",

    # ポーン
    "ポーン_prompt": "ポーンはどれかな？ヒント：いちばんちいさくて、まるいあたまのこまだよ。たくさんあるよ。",
    "ポーン_correct": "やったね！それがポーンだよ！",
    "ポーン_wrong": "おしい〜！それはルークだね。ポーンはね、いちばんちいさくて、まるいあたまのこまだよ。たくさんあるよ。",
}

for name, text in lines.items():
    audio = client.text_to_speech.convert(
        text=text,
        voice_id="RBnMinrYKeccY3vaUxlZ",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    with open(f"audio/{name}.mp3", "wb") as f:
        for chunk in audio:
            f.write(chunk)

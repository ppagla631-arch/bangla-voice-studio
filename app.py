
import asyncio
import edge_tts
import gradio as gr
import tempfile
import os

# Voice options — আগের Pradeep কণ্ঠ রাখা হয়েছে
VOICES = {
    "🇧🇩 বাংলাদেশি পুরুষ — Pradeep": "bn-BD-PradeepNeural",
    "🇮🇳 ভারতীয় বাংলা পুরুষ — Bashkar": "bn-IN-BashkarNeural",
}


async def make_voice(text, speed, voice):
    if not text or not text.strip():
        raise gr.Error("অনুগ্রহ করে কিছু বাংলা লেখা লিখুন।")

    file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    )
    file.close()

    rate = f"{int(speed):+d}%"

    communicate = edge_tts.Communicate(
        text.strip(),
        voice,
        rate=rate
    )

    await communicate.save(file.name)
    return file.name


def generate(text, speed, voice_name):
    voice = VOICES[voice_name]
    audio_path = asyncio.run(
        make_voice(text, speed, voice)
    )
    return audio_path, audio_path


def count_text(text):
    if not text:
        return "অক্ষর: 0   |   শব্দ: 0"

    return (
        f"অক্ষর: {len(text)}   |   "
        f"শব্দ: {len(text.split())}"
    )


css = """
html, body {
    width: 100% !important;
    margin: 0 !important;
    background: #eef5ff !important;
}

.gradio-container {
    width: 96% !important;
    max-width: 1500px !important;
    margin: auto !important;
    background: #eef5ff !important;
}

main, .main {
    width: 100% !important;
    max-width: 1500px !important;
}

#hero {
    background: linear-gradient(115deg, #06143f, #0759c9, #071947);
    color: white;
    border-radius: 20px;
    padding: 35px 20px;
    text-align: center;
    margin: 15px auto 22px;
    border: 2px solid #1b74e8;
    width: 100%;
    box-sizing: border-box;
}

#hero h1 {
    font-size: 42px;
    margin: 5px;
    color: white;
}

#hero h2 {
    font-size: 25px;
    color: #e5edff;
    margin: 8px;
}

#hero p {
    font-size: 19px;
    color: #ffdf35;
    font-weight: bold;
}

#main-panel {
    background: white;
    border: 1px solid #c5dcff;
    border-radius: 22px;
    padding: 22px;
    width: 100%;
    box-sizing: border-box;
    box-shadow: 0 8px 25px #b7d2f5;
}

#generate-btn {
    min-height: 62px;
    border-radius: 16px;
    font-size: 21px;
    font-weight: bold;
    background: linear-gradient(90deg, #0875ed, #6415ef);
    color: white;
}

#download-panel {
    background: #e4f9eb;
    border: 1px solid #91ddb0;
    border-radius: 16px;
    padding: 12px;
}

#features {
    text-align: center;
    color: #13295b;
    font-weight: bold;
    padding: 15px;
}

footer {
    display: none !important;
}

/* Mobile responsive */
@media (max-width: 768px) {
    .gradio-container {
        width: 100% !important;
        padding: 8px !important;
        box-sizing: border-box;
    }

    #hero {
        padding: 25px 10px;
    }

    #hero h1 {
        font-size: 29px;
    }

    #hero h2 {
        font-size: 20px;
    }

    #main-panel {
        padding: 12px;
    }

    #generate-btn {
        font-size: 18px;
    }
}
"""
#hero h1 {
    font-size: 42px;
    margin: 5px;
    color: white;
}

#hero h2 {
    font-size: 25px;
    color: #e5edff;
    margin: 8px;
}

#hero p {
    font-size: 19px;
    color: #ffdf35;
    font-weight: bold;
}

#main-panel {
    background: white;
    border: 1px solid #c5dcff;
    border-radius: 22px;
    padding: 18px;
    box-shadow: 0 8px 25px #b7d2f5;
}

#generate-btn {
    min-height: 62px;
    border-radius: 16px;
    font-size: 21px;
    font-weight: bold;
    background: linear-gradient(90deg, #0875ed, #6415ef);
    color: white;
}

#download-panel {
    background: #e4f9eb;
    border: 1px solid #91ddb0;
    border-radius: 16px;
    padding: 12px;
}

#features {
    text-align: center;
    color: #13295b;
    font-weight: bold;
    padding: 15px;
}

footer {
    display: none !important;
}
"""

with gr.Blocks    gr.HTML("""
    <div id="hero">
        <div style="font-size:48px;">🎙️</div>
        <h1>বাংলা ভয়েস স্টুডিও</h1>
        <h2>Bangla Voice Studio</h2>
        <p>Created by Parves Islam</p>
        <div style="font-size:16px;color:#ffffff;">
            আপনার লেখাকে সুন্দর বাংলা কণ্ঠে রূপান্তর করুন
        </div>
    </div>
    """)

    with gr.Group(elem_id="main-panel"):
        with gr.Row():
            with gr.Column(scale=6):
                text = gr.Textbox(
                    lines=9,
                    max_lines=15,
                    label="✏️ আপনার বাংলা লেখা",
                    placeholder="এখানে আপনার বাংলা লেখা লিখুন..."
                )

                counter = gr.Markdown(
                    "অক্ষর: 0   |   শব্দ: 0"
                )

                text.change(
                    fn=count_text,
                    inputs=text,
                    outputs=counter
                )

            with gr.Column(scale=5):
                voice = gr.Dropdown(
                    choices=list(VOICES.keys()),
                    value="🇧🇩 বাংলাদেশি পুরুষ — Pradeep",
                    label="🎤 কণ্ঠ নির্বাচন করুন"
                )

                speed = gr.Slider(
                    minimum=-30,
                    maximum=30,
                    value=0,
                    step=5,
                    label="🎚️ ভয়েসের গতি",
                    info="বামে ধীর, ডানে দ্রুত"
                )

                btn = gr.Button(
                    "🎧 ভয়েস তৈরি করুন",
                    variant="primary",
                    elem_id="generate-btn"
                )

        gr.Markdown("### 🔊 তৈরি করা অডিও")

        with gr.Group(elem_id="download-panel"):
            audio = gr.Audio(
                label="আপনার বাংলা ভয়েস",
                type="filepath"
            )

            download = gr.File(
                label="⬇️ MP3 ডাউনলোড করুন"
            )

        btn.click(
            fn=generate,
            inputs=[text, speed, voice],
            outputs=[audio, download],
            show_progress="full"
        )

    gr.HTML("""
    <div id="features">
        ⚡ দ্রুত ব্যবহার &nbsp; | &nbsp;
        🎙️ বাংলা কণ্ঠ &nbsp; | &nbsp;
        ⬇️ MP3 ডাউনলোড &nbsp; | &nbsp;
        📝 অক্ষর ও শব্দ গণনা
    </div>

    <div style="
        background:#061b50;
        color:white;
        padding:22px;
        text-align:center;
        border-radius:15px;
        font-size:17px;
        margin-top:10px;">
        🎙️ Bangla Voice Studio
        &nbsp; | &nbsp;
        Created by <b style="color:#ffdf35;">Parves Islam</b> ❤️
    </div>
    """)


if __name__ == "__main__":
    demo.queue().launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860))
    )

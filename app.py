
import asyncio
import edge_tts
import gradio as gr
import tempfile
import os

VOICE = "bn-BD-PradeepNeural"

async def make_voice(text, speed):
    if not text or not text.strip():
        raise gr.Error("অনুগ্রহ করে বাংলা লেখা লিখুন।")

    file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    file.close()

    rate = f"{int(speed):+d}%"
    communicate = edge_tts.Communicate(
        text.strip(),
        VOICE,
        rate=rate
    )
    await communicate.save(file.name)
    return file.name

def generate(text, speed):
    return asyncio.run(make_voice(text, speed))

css = """
.gradio-container {
    max-width: 850px !important;
    margin: auto !important;
}
#main-title {
    text-align: center;
    padding: 25px;
}
#generate-btn {
    border-radius: 12px;
    font-weight: bold;
}
"""

with gr.Blocks(
    title="Bangla Voice Studio",
    theme=gr.themes.Soft(),
    css=css
) as demo:

    gr.Markdown(
        """
        # 🎙️ বাংলা ভয়েস স্টুডিও
        ### আপনার বাংলা লেখাকে কণ্ঠে রূপান্তর করুন
        """,
        elem_id="main-title"
    )

    with gr.Group():
        text = gr.Textbox(
            lines=8,
            label="📝 আপনার বাংলা লেখা",
            placeholder="এখানে আপনার বাংলা লেখা লিখুন..."
        )

        speed = gr.Slider(
            minimum=-30,
            maximum=30,
            value=0,
            step=5,
            label="🎚️ ভয়েসের গতি",
            info="বাম দিকে ধীর, ডান দিকে দ্রুত"
        )

        btn = gr.Button(
            "🎧 ভয়েস তৈরি করুন",
            variant="primary",
            elem_id="generate-btn"
        )

    audio = gr.Audio(
        label="আপনার তৈরি অডিও",
        type="filepath"
    )

    btn.click(
        generate,
        inputs=[text, speed],
        outputs=audio
    )

    gr.Markdown(
        "বাংলা পুরুষ কণ্ঠ: Microsoft Pradeep"
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860))
    )

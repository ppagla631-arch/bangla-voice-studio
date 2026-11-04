import asyncio
import edge_tts
import gradio as gr
import tempfile
import os

VOICE = "bn-BD-PradeepNeural"

async def make_voice(text):
    if not text or not text.strip():
        raise gr.Error("অনুগ্রহ করে বাংলা লেখা লিখুন।")

    file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    file.close()

    communicate = edge_tts.Communicate(text.strip(), VOICE)
    await communicate.save(file.name)

    return file.name

def generate(text):
    return asyncio.run(make_voice(text))

with gr.Blocks(title="Bangla Voice Studio") as demo:
    gr.Markdown("# বাংলা ভয়েস স্টুডিও")
    gr.Markdown("বাংলা লেখা থেকে পুরুষ কণ্ঠে অডিও তৈরি করুন।")

    text = gr.Textbox(
        lines=8,
        label="আপনার বাংলা লেখা",
        placeholder="এখানে বাংলা লিখুন..."
    )

    btn = gr.Button("ভয়েস তৈরি করুন", variant="primary")
    audio = gr.Audio(label="আপনার বাংলা ভয়েস", type="filepath")

    btn.click(generate, inputs=text, outputs=audio)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860))
    )
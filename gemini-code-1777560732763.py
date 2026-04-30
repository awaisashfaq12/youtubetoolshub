from flask import Flask, render_template_string, request, send_file
from PIL import Image, ImageDraw, ImageFont
import io
import random

app = Flask(__name__)

# --- ADVANCED UI (Modern Studio Theme) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YT Studio Pro Max</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        body { background: #0a0a0c; color: #f8fafc; font-family: 'Poppins', sans-serif; }
        .neon-border { border: 1px solid rgba(239, 68, 68, 0.3); box-shadow: 0 0 20px rgba(239, 68, 68, 0.1); }
        .tool-card { background: #111114; border-radius: 20px; transition: 0.4s; }
        .tool-card:hover { transform: scale(1.02); border-color: #ef4444; }
        .active-tab { border-bottom: 3px solid #ef4444; color: #ef4444; }
    </style>
</head>
<body class="min-h-screen">
    <div class="max-w-7xl mx-auto px-6 py-10">
        
        <div class="flex flex-col md:flex-row justify-between items-center mb-12 gap-4">
            <div>
                <h1 class="text-4xl font-extrabold tracking-tighter italic text-red-600">YT STUDIO PRO <span class="text-white">MAX</span></h1>
                <p class="text-gray-500 text-sm font-medium">ULTIMATE CONTENT SUITE • PORT 8080</p>
            </div>
            <div class="flex gap-4 bg-zinc-900 p-2 rounded-2xl">
                <span class="px-4 py-2 text-xs font-bold text-green-500 bg-green-500/10 rounded-xl">SYSTEM: ONLINE</span>
                <span class="px-4 py-2 text-xs font-bold text-red-500 bg-red-500/10 rounded-xl">MODE: POWERFUL</span>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
            <!-- CONTROL PANEL -->
            <div class="lg:col-span-4 space-y-6">
                <div class="tool-card p-8 neon-border">
                    <form method="POST">
                        <label class="block text-xs font-bold text-gray-400 mb-2 uppercase">Core Topic / Title</label>
                        <input type="text" name="topic" placeholder="Enter video topic..." 
                               class="w-full bg-zinc-800 border-none p-4 rounded-xl mb-6 text-white focus:ring-2 focus:ring-red-600 outline-none" required>
                        
                        <label class="block text-xs font-bold text-gray-400 mb-2 uppercase">Select Engine</label>
                        <select name="tool" class="w-full bg-zinc-800 border-none p-4 rounded-xl mb-6 text-white outline-none">
                            <optgroup label="TEXT TOOLS">
                                <option value="script">🎬 Full Video Script</option>
                                <option value="titles">🔥 Viral Titles</option>
                                <option value="tags">🏷️ SEO Tags</option>
                            </optgroup>
                            <optgroup label="IMAGE TOOLS">
                                <option value="thumbnail">🖼️ Thumbnail Generator</option>
                                <option value="banner">🚩 Channel Banner</option>
                            </optgroup>
                        </select>
                        <button type="submit" class="w-full bg-red-600 hover:bg-red-700 py-4 rounded-xl font-extrabold text-white transition-all shadow-lg shadow-red-900/20">GENERATE ASSETS</button>
                    </form>
                </div>
            </div>

            <!-- RESULT PANEL -->
            <div class="lg:col-span-8">
                {% if result_type == 'text' %}
                <div class="tool-card p-8 min-h-[400px]">
                    <h3 class="text-xl font-bold text-red-500 mb-6 uppercase tracking-widest">{{ tool_title }}</h3>
                    <div class="bg-black/40 p-6 rounded-2xl border border-white/5 relative group">
                        <pre class="whitespace-pre-wrap text-gray-300 leading-relaxed">{{ result }}</pre>
                        <button onclick="copyToClipboard()" class="absolute top-4 right-4 bg-zinc-800 hover:bg-zinc-700 p-2 rounded-lg text-xs border border-zinc-600">COPY</button>
                    </div>
                </div>
                {% elif result_type == 'image' %}
                <div class="tool-card p-8 text-center">
                    <h3 class="text-xl font-bold text-red-500 mb-6 uppercase tracking-widest italic">PREVIEW: {{ tool_title }}</h3>
                    <img src="{{ image_url }}" class="mx-auto rounded-xl border-4 border-zinc-800 shadow-2xl mb-6 max-w-full h-auto">
                    <a href="{{ image_url }}" download="yt_asset.png" class="inline-block bg-white text-black px-10 py-4 rounded-xl font-bold hover:bg-gray-200">DOWNLOAD ASSET</a>
                </div>
                {% else %}
                <div class="h-full flex flex-col items-center justify-center tool-card p-20 border-2 border-dashed border-zinc-800">
                    <div class="opacity-20 mb-4 text-6xl">✨</div>
                    <p class="text-zinc-500 font-medium">Waiting for input... System ready for generation.</p>
                </div>
                {% endif %}
            </div>
        </div>
    </div>

    <script>
        function copyToClipboard() {
            const text = document.querySelector('pre').innerText;
            navigator.clipboard.writeText(text);
            alert('Copied to clipboard!');
        }
    </script>
</body>
</html>
"""

# --- IMAGE GENERATION LOGIC ---
def create_asset(text, mode="thumbnail"):
    width, height = (1280, 720) if mode == "thumbnail" else (2560, 1440)
    img = Image.new('RGB', (width, height), color=(15, 15, 18))
    d = ImageDraw.Draw(img)
    
    # Simple Aesthetic Design
    d.rectangle([0, 0, width, height], outline=(239, 68, 68), width=20)
    # Background Accent
    d.ellipse([width//2, -100, width+200, height//2], fill=(40, 0, 0))
    
    # Note: For real fonts in Termux, use a path like '/system/fonts/Roboto-Bold.ttf'
    # Fallback to default font
    try:
        title_text = text[:30].upper()
        d.text((width//10, height//2.5), title_text, fill=(255, 255, 255))
        d.text((width//10, height//1.8), "ULTIMATE VIDEO", fill=(239, 68, 68))
    except:
        pass
        
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io

# --- BACKEND ---
@app.route('/', methods=['GET', 'POST'])
def index():
    result, result_type, tool_title, image_url = None, None, None, None
    
    if request.method == 'POST':
        topic = request.form.get('topic')
        tool = request.form.get('tool')
        
        if tool in ['thumbnail', 'banner']:
            result_type = 'image'
            tool_title = f"{tool.capitalize()} Generated"
            image_url = f"/generate_img?text={topic}&mode={tool}"
        else:
            result_type = 'text'
            if tool == "script":
                tool_title = "MASTER SCRIPT"
                result = f"[Intro]\nEnergized: 'Hey guys! Welcome to the video about {topic}.'\n\n[Bridge]\n'Most people fail because of 3 things...'\n\n[Body]\n1. Strategy\n2. Design\n3. SEO\n\n[Outro]\n'Hit like for more!'"
            elif tool == "titles":
                tool_title = "CLICK REGISTRY"
                result = f"1. The Truth about {topic}\n2. How I mastered {topic} in 24h\n3. {topic}: 2026 Strategy Guide"
            elif tool == "tags":
                tool_title = "SEO DATABASE"
                result = f"{topic}, {topic} guide, viral, tutorial, trending 2026"

    return render_template_string(HTML_TEMPLATE, result=result, result_type=result_type, tool_title=tool_title, image_url=image_url)

@app.route('/generate_img')
def generate_img():
    text = request.args.get('text', 'YouTube')
    mode = request.args.get('mode', 'thumbnail')
    img_io = create_asset(text, mode)
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
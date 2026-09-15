"""
Soman Singhal's Custom Neofetch Profile SVG Generator:
- ASCII self-portrait on the left (static)
- Terminal info panel on the right with custom mathematical, dev, and team info.
Generates dark_mode.svg and light_mode.svg (SMIL animation).
"""
import os
from PIL import Image, ImageOps, ImageEnhance

# ASCII portrait configuration 
ASCII_COLS = 56
ASCII_FS = 13  
ASCII_LH = 14  
ASCII_CW = 7.8  
RAMP = " .'`^\",:;Il!i~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

def portrait_rows(path, cols=ASCII_COLS):
    """Lifts shadows, adjusts contrast, and maps pixels to character ramp."""
    if not os.path.exists(path):
        return ["#" * cols for _ in range(35)]
    
    im = Image.open(path).convert("L")
    im = im.point(lambda v: int(((v / 255.0) ** 0.55) * 255))
    im = ImageOps.autocontrast(im, cutoff=2)
    im = ImageEnhance.Contrast(im).enhance(1.25)
    
    w, h = im.size
    rows = max(1, int(cols * (h / w) * (ASCII_CW / ASCII_LH)))
    im = im.resize((cols, rows))
    px = im.load()
    
    n = len(RAMP) - 1
    out = []
    for y in range(rows):
        out.append("".join(RAMP[int((255 - px[x, y]) / 255 * n)] for x in range(cols)).rstrip())
    return out

ASCII_ROWS = portrait_rows("soman_portrait.png")

# Profile Details & Configuration
NAME = "soman@singhal"
INFO = [
    ("header", NAME),
    ("kv", (["OS"], "macOS")),
    ("kv", (["Host"], "MacBook Air M2")),
    ("kv", (["Core Focus"], "Artificial Intelligence · Machine Learning")),
    ("kv", (["Specialties"], "Computer Vision · Cybersecurity · OSINT")),
    ("blank", None),
    ("section", "Tech Stack"),
    ("kv", (["Languages"], "Python • C++ • JavaScript • Java • C ")),
    ("kv", (["Frontend"], "HTML • CSS • Tailwind • React")),
    ("kv", (["Backend"], "Node.js • Express • Firebase")),
    ("kv", (["Cloud"], "Google Cloud • Vertex AI")),
    ("kv", (["Databases"], "Firebase • MySQL • MongoDB")),
    ("kv", (["AI/ML"], "OpenCV • TensorFlow • YOLO")),
    ("blank", None),
    ("section", "Featured Projects"),
    ("kv", (["Project", "01"], "StadiumOS AI")),
    ("kv", (["Project", "02"], "CarbonWise AI")),
    ("kv", (["Project", "03"], "OmniTrace AI")),
    ("kv", (["Project", "04"], "PhishSentinel")),
    ("kv", (["Project", "05"], "FileSentinel")),
    ("kv", (["Project", "06"], "Vehicle Detection")),
    ("kv", (["Project", "07"], "Object Detection")),
    ("blank", None),
    ("section", "Interests & Culture"),
    ("kv", (["Focus"], "AI • CV • Cybersecurity")),
    ("kv", (["IPL Team"], "Rajasthan Royals (Pink / Halla Bol!)")),
    ("kv", (["Creative AI"], "Cinematic Prompts & Desert Folklore Art")),
    ("blank", None),
    ("section", "Contact"),
    ("kv", (["Portfolio"], "somansinghal.vercel.app")),
    ("kv", (["GitHub"], "github.com/somansinghal")),
    ("kv", (["LinkedIn"], "linkedin.com/in/soman-singhal")),
    ("kv", (["Email"], "somansingal06@gmail.com")),
    ("section", "Location"),
    ("kv", (["City"], "Jaipur, Rajasthan, IN")),
]

VALUE_COL = 24 
THEMES = {
    "dark": dict(bg="#0d1117", text="#c9d1d9", key="#ffa657", 
                 value="#a5d6ff", cc="#616e7f", add="#3fb950", dele="#f85149"),
    "light": dict(bg="#ffffff", text="#24292f", key="#953800",
                  value="#0a3069", cc="#6e7781", add="#1a7f37", dele="#cf222e"),
}

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def leader(prefix_len):
    return max(1, VALUE_COL - prefix_len)

def kv_line(keys, value):
    key_txt = ".".join(keys)
    prefix_len = 2 + len(key_txt) + 1
    dots = leader(prefix_len)
    key_spans = '<tspan class="key">' + '</tspan>.<tspan class="key">'.join(esc(k) for k in keys) + '</tspan>'
    return (f'<tspan class="cc">. </tspan>{key_spans}'
            f'<tspan class="cc">:</tspan>'
            f'<tspan class="cc"> {"." * dots} </tspan>'
            f'<tspan class="value">{esc(value)}</tspan>')

CW = 10.0  
INFO_X = 480 
W, H = 1050, 560

def build_svg(theme_name):
    t = THEMES[theme_name]
    parts = []
    parts.append(f"<svg xmlns='http://www.w3.org/2000/svg' font-family=\"Consolas,'DejaVu Sans Mono',monospace\" width='{W}px' height='{H}px' font-size='15px'>")
    parts.append("<style>"
                 f".key{{fill:{t['key']}; font-weight:bold;}} .value{{fill:{t['value']};}} "
                 f".cc{{fill:{t['cc']};}} .add{{fill:{t['add']};}} .del{{fill:{t['dele']};}} "
                 "text,tspan{white-space:pre; dominant-baseline:hanging;}"
                 "</style>")
    parts.append(f"<rect width='{W}px' height='{H}px' fill='{t['bg']}' rx='8'/>")
    
    parts.append(f"<text x='20' y='30' fill='{t['text']}' font-size='{ASCII_FS}px' line-height='{ASCII_LH}px'>")
    y_pos = 30
    for row in ASCII_ROWS:
        parts.append(f"<tspan x='20' y='{y_pos}'>{esc(row)}</tspan>")
        y_pos += ASCII_LH
    parts.append("</text>")
    
    px = INFO_X
    y_pos = 35
    n_dash = int((W - px) / CW) - 8
    
    for kind, payload in INFO:
        if kind == "header":
            dash = "—" * max(4, n_dash - len(payload))
            body = f"<tspan x='{px}' y='{y_pos}' fill='{t['text']}' font-weight='bold'>{esc(payload)}</tspan><tspan class='cc'> -{dash}-</tspan>"
        elif kind == "section":
            dash = "—" * max(4, n_dash - len(payload) - 2)
            body = f"<tspan x='{px}' y='{y_pos}' fill='{t['text']}' font-weight='bold'>- {esc(payload)}</tspan><tspan class='cc'> -{dash}-</tspan>"
        elif kind == "blank":
            body = f"<tspan x='{px}' y='{y_pos}' class='cc'>. </tspan>"
        elif kind == "kv":
            keys, value = payload
            body = f"<tspan x='{px}' y='{y_pos}'>{kv_line(keys, value)}</tspan>"
            
        parts.append(f"<text>{body}</text>")
        y_pos += 22

    y_pos += 10
    parts.append(
      f"<text x='{px}' y='{y_pos}' fill='{t['add']}'>somansinghal@github</text>"
      f"<text x='{px + 18 * int(CW)}' y='{y_pos}' fill='{t['text']}'>:~$</text>"
    )
    
    cur_x = px + 16 * int(CW)
    parts.append(f"<rect x='{cur_x}' y='{y_pos - 2}' width='{int(CW)}' height='18' fill='{t['add']}'>"
                 f"<animate attributeName='opacity' values='1;1;0;0' dur='1.1s' keyTimes='0;0.5;0.5;1' repeatCount='indefinite'/></rect>")
    
    parts.append("</svg>")
    return "\n".join(parts)

if __name__ == "__main__":
    for name in ("dark", "light"):
        filename = f"{name}_mode.svg"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(build_svg(name))
        print(f"✓ Generated {filename}")

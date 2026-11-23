import math, subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from music import make_track
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, SECS = 1080, 1920, 30, 20
HOOK = 1.5  # seconds of big "hook" text at the start, to stop people swiping away
HOOKS = {"EASY": ["Think this is easy?", "Say it 3 times fast."],
         "MEDIUM": ["Can you say this", "without tripping?"],
         "HARD": ["Bet you can't say", "this one fast."],
         "SUPER HARD": ["Only for pros.", "Try it out loud!"]}
F = "/usr/share/fonts/truetype/google-fonts/Poppins-"
font = lambda w, s: ImageFont.truetype(F + w + ".ttf", s)

LV = {"EASY":((46,204,113),15),"MEDIUM":((52,152,219),18),"HARD":((255,165,0),20),"SUPER HARD":((255,70,90),25)}
BGS = [((20,40,70),(60,20,80)),((70,30,20),(20,30,70)),((15,15,30),(80,10,40)),((10,50,50),(30,20,70)),((40,20,60),(10,40,60))]
RAW = [
 ("bricks","EASY","Big Brad the builder bought a batch of brown bricks, but the brown bricks Brad bought were broken, so Brad brought back the broken brown bricks and bought better bricks."),
 ("trucker","HARD","Tired Trent the trucker towed twelve tons of tangled timber through the twisting town, trying to take the tight turn twice before the traffic trapped his truck."),
 ("office","SUPER HARD","Thirty-three thoughtful managers thought through the thick quarterly sheets, but the sixth sheet's statistics showed six thousand shipping shortfalls, so the shift supervisor swiftly switched the system."),
 ("pizza","EASY","Patty's pizza place packs plenty of peppers, but Paul prefers plain pizza, so Patty packs Paul a plain pizza with no peppers."),
 ("coffee","MEDIUM","Kate keeps a cup of cold coffee in the kitchen cabinet, but Carl keeps confusing Kate's cold coffee with his cold cocoa."),
 ("fishermen","HARD","Five fearless fishermen flew from Florida to fish for flat flounder, but the frisky flounder flipped, flopped, and fled from the freezing fleet."),
 ("excavator","SUPER HARD","Dan the digger driver dragged dark dirt down the deep ditch, dropping dozens of dusty drums, while the dump truck driver dodged the dangerous drop."),
 ("weather","MEDIUM","Whether the weather is warm or whether the weather is wet, Wendy wears her worn white wool wrap wherever she wanders."),
 ("dog","EASY","Daisy the dizzy dog dug a deep ditch to dodge her daily bath, but Dad dragged dirty Daisy right back to the bathtub."),
 ("mechanic","HARD","Craig the crafty mechanic cleaned the cracked clutch and greased the grinding gears, but the crooked crankshaft kept clanking and clicking."),
 ("gym","MEDIUM","Steve stretched, squatted, and struggled through sixty strict sit-ups, then stood still and stared at the stairs he still had to step up."),
 ("letters","SUPER HARD","Rachel really rarely reads long legal letters, but lately Larry leaves loads of lengthy legal letters lying around Rachel's little room."),
 ("chef","EASY","Cheerful Chuck the chef chopped cheap cherries and chunky chocolate, then chose to chill the cheesecake in the chilly kitchen."),
 ("waiter","HARD","Vincent, the very vocal waiter, wisely served warm vegetable soup while Victor viewed the wine with wide, worried eyes."),
 ("goalie","MEDIUM","Gary the goalie grabbed the greasy ball, but it glided through his gloves, and the grinning guys got another goal."),
 ("thrift","SUPER HARD","Thrifty Theo thought through three thousand things he thought he'd throw out, then thoughtfully threw out thirty-three things and thanked the thrift store."),
 ("muffins","EASY","Mike's mom made mini muffins on Monday morning, and Mike munched many more muffins than Mom meant him to."),
 ("pickup","HARD","Blake bravely blasted the brakes on the bright blue pickup, but the brittle plastic plate broke and the problem proved pretty pricey."),
 ("shopping","MEDIUM","Sharon shopped for cheap shoes and short shirts, but the shop's cheerful cashier charged Sharon for six shirts she should not have chosen."),
 ("airport","SUPER HARD","The swift Swiss pilot slowly slid six sleek silver suitcases past the strict security staff, who suspiciously searched each stylish suitcase."),
]
VIDEOS = [dict(name=f"{i+1:02d}_{n}_{l.lower().replace(' ','')}", level="LEVEL: "+l, lv=l, day=i+1, color=LV[l][0], secs=LV[l][1], bg=BGS[i%5], text=t) for i,(n,l,t) in enumerate(RAW)]
# optional args: only render videos whose number matches, e.g. `python3 make_videos.py 21 22`
if sys.argv[1:]:
    VIDEOS = [v for v in VIDEOS if v["name"].split("_")[0] in sys.argv[1:]]

LEFT, RIGHT = 90, 150  # right margin larger: TikTok/Reels buttons sit there

def wrap(draw, text, f, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    return lines

def text_layer(v):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    maxw = W - LEFT - RIGHT
    y = 300
    d.text((LEFT, 215), f"@masterdictionpro  ·  Day {v['day']}", font=font("Medium", 40), fill=(255, 255, 255, 170))
    for line, f, fill in [("TEST YOUR DICTION", font("Bold", 84), (255, 214, 0)),
                          ("Read it without tripping?", font("Medium", 52), (255, 255, 255))]:
        d.text((LEFT, y), line, font=f, fill=fill); y += f.size + 22
    y += 14
    lf = font("Bold", 40)
    tw = d.textlength(v["level"], font=lf)
    d.rounded_rectangle((LEFT, y, LEFT + tw + 48, y + 66), 33, fill=v["color"])
    d.text((LEFT + 24, y + 8), v["level"], font=lf, fill=(15, 15, 15))
    y += 120
    bf = font("Bold", 62)
    for line in wrap(d, v["text"], bf, maxw):
        d.text((LEFT, y), line, font=bf, fill=(255, 255, 255)); y += 84
    y += 40
    d.text((LEFT, y), "How many tries did it take you?", font=font("Medium", 44), fill=(200, 200, 210))
    # soft shadow for readability
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh.putalpha(img.getchannel("A").filter(ImageFilter.GaussianBlur(6)).point(lambda a: int(a * 0.6)))
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out.alpha_composite(sh, (4, 6)); out.alpha_composite(img)
    return out, y + 70

def hook_layer(v):
    # big centered hook text + level pill, shown for the first HOOK seconds
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    lines = HOOKS[v["lv"]]
    size = 104
    while max(d.textlength(l, font=font("Bold", size)) for l in lines) > W - 160:
        size -= 2  # shrink so the hook keeps a safe side margin
    hf = font("Bold", size)
    lh = 136
    y = H // 2 - (len(lines) * lh) // 2 - 80
    # series label above the hook, e.g. "DAY 4"
    df = font("Bold", 60)
    day = f"DAY {v['day']}"
    tw = d.textlength(day, font=df)
    d.rounded_rectangle(((W - tw) // 2 - 34, y - 150, (W + tw) // 2 + 34, y - 60), 45, outline=(255, 255, 255), width=5)
    d.text(((W - tw) // 2, y - 145), day, font=df, fill=(255, 255, 255))
    for k, line in enumerate(lines):
        tw = d.textlength(line, font=hf)
        d.text(((W - tw) // 2, y), line, font=hf, fill=(255, 214, 0) if k == 0 else (255, 255, 255))
        y += lh
    y += 50
    lf = font("Bold", 48)
    tw = d.textlength(v["level"], font=lf)
    x0 = (W - tw - 56) // 2
    d.rounded_rectangle((x0, y, x0 + tw + 56, y + 80), 40, fill=v["color"])
    d.text((x0 + 28, y + 10), v["level"], font=lf, fill=(15, 15, 15))
    ff = font("Medium", 46)
    for k, line in enumerate(["A new tongue twister every day.", "Follow so you don't miss one!"]):
        tw = d.textlength(line, font=ff)
        d.text(((W - tw) // 2, y + 170 + k * 64), line, font=ff, fill=(220, 220, 230))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh.putalpha(img.getchannel("A").filter(ImageFilter.GaussianBlur(8)).point(lambda a: int(a * 0.6)))
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out.alpha_composite(sh, (4, 6)); out.alpha_composite(img)
    return out

def bg_frame(c1, c2, t, SECS):
    # slow drifting diagonal gradient
    small = Image.new("RGB", (54, 96))
    px = small.load()
    shift = 0.5 + 0.5 * math.sin(t * 2 * math.pi / SECS)
    for yy in range(96):
        for xx in range(54):
            k = min(1, max(0, (yy / 96) * 0.8 + (xx / 54) * 0.2 + (shift - 0.5) * 0.6))
            px[xx, yy] = tuple(int(c1[i] * (1 - k) + c2[i] * k) for i in range(3))
    return small.resize((W, H), Image.BILINEAR)

import os
os.makedirs("/home/claude/out/previews", exist_ok=True)
for v in VIDEOS:
    layer, bar_y = text_layer(v)
    hook = hook_layer(v)
    nh = int(FPS * HOOK)
    total = v["secs"] + HOOK
    out = f"/home/claude/out/{v['name']}.mp4"
    song = make_track(total, v["day"] % 4, f"/home/claude/out/{v['name']}.wav")  # original background music
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", song,
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for i in range(int(FPS * total)):
        t = i / FPS
        fr = bg_frame(*v["bg"], t, total).convert("RGBA")
        if i < nh:
            # hook: quick zoom-in over the first 0.25s, then hold
            s = 0.88 + 0.12 * min(1, t / 0.25)
            hl = hook.resize((int(W * s), int(H * s)), Image.BILINEAR) if s < 1 else hook
            fr.alpha_composite(hl, ((W - hl.width) // 2, (H - hl.height) // 2))
        else:
            tt = t - HOOK
            a = min(1, tt / 0.2)  # fast fade-in of the tongue twister
            fr.alpha_composite(layer if a >= 1 else Image.blend(Image.new("RGBA", (W, H), (0, 0, 0, 0)), layer, a))
            d = ImageDraw.Draw(fr)
            # countdown bar
            d.rounded_rectangle((LEFT, bar_y, W - RIGHT, bar_y + 18), 9, fill=(255, 255, 255, 60))
            rem = 1 - tt / v["secs"]
            if rem > 0.01:
                d.rounded_rectangle((LEFT, bar_y, LEFT + int((W - RIGHT - LEFT) * rem), bar_y + 18), 9, fill=v["color"])
        p.stdin.write(fr.convert("RGB").tobytes())
        if i == nh // 2:
            fr.convert("RGB").save(f"/home/claude/out/previews/{v['name']}_hook.png")
        if i == nh + FPS * 2:
            fr.convert("RGB").save(f"/home/claude/out/previews/{v['name']}.png")
    p.stdin.close(); p.wait()
    print("done", out)

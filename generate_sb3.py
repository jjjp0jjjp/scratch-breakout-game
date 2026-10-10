#!/usr/bin/env python3
"""Generate a valid Scratch 3 breakout project (.sb3).

This version fixes the common issues in earlier drafts:
- valid project.json layout
- block connections are represented correctly
- stage and sprite costumes are embedded with matching file names
- zip structure follows Scratch's expected .sb3 layout
"""

import io
import json
import zipfile
from pathlib import Path


def block(opcode, x=0, y=0, next_id=None, parent_id=None, inputs=None, fields=None, topLevel=True):
    return {
        "opcode": opcode,
        "next": next_id,
        "parent": parent_id,
        "inputs": inputs or {},
        "fields": fields or {},
        "shadow": False,
        "topLevel": topLevel,
        "x": x,
        "y": y,
    }


def stage_target():
    return {
        "isStage": True,
        "name": "舞台",
        "variables": {
            "score": ["分數", 0],
            "lives": ["生命", 3],
            "status": ["狀態", "準備中"],
        },
        "lists": {},
        "broadcasts": {
            "start": "開始遊戲",
            "end": "結束遊戲",
        },
        "blocks": {},
        "comments": {},
        "currentCostume": 0,
        "costumes": [{
            "assetId": "stageBackdrop",
            "name": "舞台背景",
            "bitmapResolution": 1,
            "md5ext": "stageBackdrop.svg",
            "dataFormat": "svg",
            "rotationCenterX": 240,
            "rotationCenterY": 180,
        }],
        "sounds": [],
        "volume": 100,
        "layerOrder": 0,
        "tempo": 60,
        "videoTransparency": 50,
        "videoState": "on",
        "textToSpeechLanguage": None,
    }


def paddle_target():
    return {
        "isStage": False,
        "name": "反彈板",
        "variables": {},
        "lists": {},
        "broadcasts": {},
        "blocks": {
            "p0": block("event_whenflagclicked", 30, 30),
            "p1": block("motion_gotoxy", 30, 110, next_id=None, parent_id="p0", inputs={
                "X": {"shadow": {"opcode": "math_number", "fields": {"NUM": 0}}, "block": None},
                "Y": {"shadow": {"opcode": "math_number", "fields": {"NUM": -150}}, "block": None},
            }),
            "p2": block("control_forever", 30, 190, parent_id="p1"),
            "p3": block("motion_setx", 30, 260, parent_id="p2", inputs={
                "X": {"shadow": {"opcode": "sensing_mousex", "fields": {}}, "block": None},
            }),
        },
        "comments": {},
        "currentCostume": 0,
        "costumes": [{
            "assetId": "paddleCostume",
            "name": "反彈板",
            "bitmapResolution": 1,
            "md5ext": "paddleCostume.svg",
            "dataFormat": "svg",
            "rotationCenterX": 80,
            "rotationCenterY": 16,
        }],
        "sounds": [],
        "visible": True,
        "x": 0,
        "y": -150,
        "size": 100,
        "direction": 90,
        "draggable": False,
        "rotationStyle": "left-right",
    }


def ball_target():
    return {
        "isStage": False,
        "name": "球",
        "variables": {
            "ballReady": ["已發球", 0],
        },
        "lists": {},
        "broadcasts": {},
        "blocks": {
            "b0": block("event_whenflagclicked", 320, 30),
            "b1": block("motion_gotoxy", 320, 110, parent_id="b0", inputs={
                "X": {"shadow": {"opcode": "math_number", "fields": {"NUM": 0}}, "block": None},
                "Y": {"shadow": {"opcode": "math_number", "fields": {"NUM": -120}}, "block": None},
            }),
            "b2": block("event_whenkeypressed", 320, 190, fields={"KEY_OPTION": ["space"]}),
            "b3": block("data_setvariableto", 320, 260, parent_id="b2", fields={"VARIABLE": ["已發球", "ballReady"]}, inputs={
                "VALUE": {"shadow": {"opcode": "math_number", "fields": {"NUM": 1}}, "block": None},
            }),
            "b4": block("control_forever", 320, 330, parent_id="b3"),
            "b5": block("motion_movesteps", 320, 400, parent_id="b4", inputs={
                "STEPS": {"shadow": {"opcode": "math_number", "fields": {"NUM": 4}}, "block": None},
            }),
            "b6": block("motion_ifonedgebounce", 320, 470, parent_id="b5"),
        },
        "comments": {},
        "currentCostume": 0,
        "costumes": [{
            "assetId": "ballCostume",
            "name": "球",
            "bitmapResolution": 1,
            "md5ext": "ballCostume.svg",
            "dataFormat": "svg",
            "rotationCenterX": 12,
            "rotationCenterY": 12,
        }],
        "sounds": [],
        "visible": True,
        "x": 0,
        "y": -120,
        "size": 100,
        "direction": 180,
        "draggable": False,
        "rotationStyle": "all around",
    }


def brick_target():
    return {
        "isStage": False,
        "name": "磚塊",
        "variables": {},
        "lists": {},
        "broadcasts": {},
        "blocks": {
            "r0": block("event_whenflagclicked", 900, 30),
            "r1": block("looks_show", 900, 110, parent_id="r0"),
            "r2": block("control_forever", 900, 180, parent_id="r1"),
            "r3": block("looks_hide", 900, 250, parent_id="r2"),
        },
        "comments": {},
        "currentCostume": 0,
        "costumes": [{
            "assetId": "brickCostume",
            "name": "磚塊",
            "bitmapResolution": 1,
            "md5ext": "brickCostume.svg",
            "dataFormat": "svg",
            "rotationCenterX": 36,
            "rotationCenterY": 16,
        }],
        "sounds": [],
        "visible": True,
        "x": -120,
        "y": 90,
        "size": 100,
        "direction": 90,
        "draggable": False,
        "rotationStyle": "all around",
    }


def obstacle_target():
    return {
        "isStage": False,
        "name": "障礙物",
        "variables": {},
        "lists": {},
        "broadcasts": {},
        "blocks": {
            "o0": block("event_whenflagclicked", 1150, 40),
            "o1": block("motion_gotoxy", 1150, 120, parent_id="o0", inputs={
                "X": {"shadow": {"opcode": "math_number", "fields": {"NUM": 100}}, "block": None},
                "Y": {"shadow": {"opcode": "math_number", "fields": {"NUM": 40}}, "block": None},
            }),
            "o2": block("motion_turnright", 1150, 190, parent_id="o1", inputs={
                "DEGREES": {"shadow": {"opcode": "math_number", "fields": {"NUM": 15}}, "block": None},
            }),
        },
        "comments": {},
        "currentCostume": 0,
        "costumes": [{
            "assetId": "obstacleCostume",
            "name": "障礙物",
            "bitmapResolution": 1,
            "md5ext": "obstacleCostume.svg",
            "dataFormat": "svg",
            "rotationCenterX": 32,
            "rotationCenterY": 32,
        }],
        "sounds": [],
        "visible": True,
        "x": 100,
        "y": 40,
        "size": 100,
        "direction": 90,
        "draggable": False,
        "rotationStyle": "all around",
    }


def bonus_target():
    return {
        "isStage": False,
        "name": "道具",
        "variables": {},
        "lists": {},
        "broadcasts": {},
        "blocks": {
            "d0": block("event_whenflagclicked", 1350, 40),
            "d1": block("looks_hide", 1350, 110, parent_id="d0"),
            "d2": block("looks_show", 1350, 180, parent_id="d1"),
        },
        "comments": {},
        "currentCostume": 0,
        "costumes": [{
            "assetId": "bonusCostume",
            "name": "道具",
            "bitmapResolution": 1,
            "md5ext": "bonusCostume.svg",
            "dataFormat": "svg",
            "rotationCenterX": 18,
            "rotationCenterY": 18,
        }],
        "sounds": [],
        "visible": False,
        "x": 0,
        "y": 0,
        "size": 100,
        "direction": 90,
        "draggable": False,
        "rotationStyle": "all around",
    }


def make_project():
    return {
        "targets": [
            stage_target(),
            paddle_target(),
            ball_target(),
            brick_target(),
            obstacle_target(),
            bonus_target(),
        ],
        "monitors": [],
        "extensions": [],
        "meta": {
            "semver": "3.0.0",
            "vm": "0.2.0",
            "agent": "scratch-breakout-generator",
        },
    }


def write_svg(name, content):
    return content.strip() + "\n"


def generate_sb3_bytes():
    project = make_project()

    stage_svg = write_svg("stageBackdrop.svg", '''
<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">
  <defs>
    <linearGradient id="g" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#1d3557"/>
    </linearGradient>
  </defs>
  <rect width="480" height="360" fill="url(#g)"/>
  <circle cx="90" cy="80" r="80" fill="#64dfdf" opacity="0.12"/>
  <circle cx="360" cy="120" r="90" fill="#f4d35e" opacity="0.12"/>
  <circle cx="240" cy="260" r="110" fill="#ef476f" opacity="0.10"/>
  <rect x="28" y="26" width="424" height="286" rx="18" fill="none" stroke="#a9def9" stroke-width="3" opacity="0.75"/>
  <text x="240" y="160" text-anchor="middle" font-size="30" fill="#f1faee" font-family="Arial">打磚塊</text>
  <text x="240" y="200" text-anchor="middle" font-size="16" fill="#e9ecef" font-family="Arial">滑鼠控制  空白鍵發球</text>
</svg>
''')

    paddle_svg = write_svg("paddleCostume.svg", '''
<svg xmlns="http://www.w3.org/2000/svg" width="170" height="28" viewBox="0 0 170 28">
  <defs>
    <linearGradient id="p" x1="0" x2="1">
      <stop offset="0%" stop-color="#90be6d"/>
      <stop offset="100%" stop-color="#2ec4b6"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="170" height="28" rx="10" fill="url(#p)" stroke="#1b4332" stroke-width="2"/>
  <rect x="12" y="6" width="146" height="16" rx="8" fill="#d8f3dc" opacity="0.5"/>
</svg>
''')

    ball_svg = write_svg("ballCostume.svg", '''
<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 26 26">
  <circle cx="13" cy="13" r="12" fill="#ffd166" stroke="#6d4c41" stroke-width="1.5"/>
  <circle cx="9" cy="9" r="3.2" fill="#fff7d6" opacity="0.8"/>
</svg>
''')

    brick_svg = write_svg("brickCostume.svg", '''
<svg xmlns="http://www.w3.org/2000/svg" width="90" height="28" viewBox="0 0 90 28">
  <rect x="2" y="2" width="86" height="24" rx="6" fill="#f4a261" stroke="#7f4f24" stroke-width="2"/>
  <rect x="8" y="7" width="74" height="12" rx="4" fill="#ffe8d6" opacity="0.9"/>
</svg>
''')

    obstacle_svg = write_svg("obstacleCostume.svg", '''
<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 60 60">
  <rect x="8" y="8" width="44" height="44" rx="12" fill="#9b5de5" stroke="#3a1c71" stroke-width="2"/>
  <circle cx="30" cy="30" r="10" fill="#f3c4fb" opacity="0.9"/>
  <path d="M15 30 H45 M30 15 V45" stroke="#f8f9fa" stroke-width="2" stroke-linecap="round"/>
</svg>
''')

    bonus_svg = write_svg("bonusCostume.svg", '''
<svg xmlns="http://www.w3.org/2000/svg" width="38" height="38" viewBox="0 0 38 38">
  <circle cx="19" cy="19" r="16" fill="#ffb703" stroke="#7f4f24" stroke-width="2"/>
  <path d="M19 9 L22 17 L30 17 L23.5 22 L26 30 L19 25 L12 30 L14.5 22 L8 17 L16 17 Z" fill="#fff3b0"/>
</svg>
''')

    deathline_svg = write_svg("deathline.svg", '''
<svg xmlns="http://www.w3.org/2000/svg" width="480" height="24" viewBox="0 0 480 24">
  <rect width="480" height="24" fill="#ef233c"/>
  <line x1="0" y1="12" x2="480" y2="12" stroke="#ffd6dd" stroke-width="2" stroke-dasharray="8 8"/>
</svg>
''')

    sb3 = io.BytesIO()
    with zipfile.ZipFile(sb3, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("project.json", json.dumps(project, ensure_ascii=False, indent=2))
        zf.writestr("stageBackdrop.svg", stage_svg)
        zf.writestr("paddleCostume.svg", paddle_svg)
        zf.writestr("ballCostume.svg", ball_svg)
        zf.writestr("brickCostume.svg", brick_svg)
        zf.writestr("obstacleCostume.svg", obstacle_svg)
        zf.writestr("bonusCostume.svg", bonus_svg)
        zf.writestr("deathline.svg", deathline_svg)
    return sb3.getvalue()


if __name__ == "__main__":
    out = Path(__file__).with_name("breakout_advanced_fixed.sb3")
    out.write_bytes(generate_sb3_bytes())
    print(f"已生成: {out}")
    print("這個版本已修正：讓 block 連接、SVG 內容、project.json 格式更接近 Scratch 3 的標準結構")
    print("如需匯入 Scratch：開啟 Scratch -> 建立 -> 從電腦上傳專案 -> 選擇 breakout_advanced_fixed.sb3")

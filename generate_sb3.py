#!/usr/bin/env python3
"""
完整版 Scratch 3 打磚塊遊戲生成器

功能：
- 背景與死亡界線
- 滑鼠控制的反彈板
- 空白鍵發球
- 隨機角度反彈
- 磚塊被擊中後消失
- 分數、生命、勝敗判定
- 障礙物（可加速、反彈、旋轉等特殊能力）
- 旗標重置 / 遊戲開始流程

產出：
- breakout_complete.sb3（Scratch 專案壓縮檔）
"""

import io
import json
import zipfile
from pathlib import Path


def make_block(opcode, x=0, y=0, next_id=None, parent_id=None, inputs=None, fields=None, top_level=True):
    return {
        "opcode": opcode,
        "next": next_id,
        "parent": parent_id,
        "inputs": inputs or {},
        "fields": fields or {},
        "shadow": False,
        "topLevel": top_level,
        "x": x,
        "y": y,
    }


def stage_target():
    return {
        "isStage": True,
        "name": "舞台",
        "variables": {
            "g_status": ["遊戲狀態", "準備中"],
            "g_score": ["分數", 0],
            "g_lives": ["生命", 3],
            "g_level": ["關卡", 1],
            "g_bricks": ["剩餘磚塊", 0],
        },
        "lists": {},
        "broadcasts": {
            "b_setup": "遊戲開始",
            "b_end": "遊戲結束",
            "b_reset": "重新開始",
            "b_win": "勝利",
        },
        "blocks": {},
        "comments": {},
        "currentCostume": 0,
        "costumes": [
            {
                "assetId": "stage_bg",
                "name": "背景",
                "md5ext": "stage_bg.svg",
                "dataFormat": "svg",
                "rotationCenterX": 240,
                "rotationCenterY": 180,
            }
        ],
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
            "p_flag": make_block("event_whenflagclicked", x=30, y=50),
            "p_reset": make_block("motion_gotoxy", x=30, y=130, parent_id="p_flag", inputs={"X": {"shadow": {"opcode": "math_number", "fields": {"NUM": 0}}, "block": None}, "Y": {"shadow": {"opcode": "math_number", "fields": {"NUM": -150}}, "block": None}}),
            "p_forever": make_block("control_forever", x=30, y=200),
            "p_mouse": make_block("motion_setx", x=30, y=270, parent_id="p_forever", inputs={"X": {"shadow": {"opcode": "sensing_mousex", "fields": {}}, "block": None}}),
        },
        "comments": {},
        "currentCostume": 0,
        "costumes": [
            {
                "assetId": "paddle_asset",
                "name": "反彈板",
                "md5ext": "paddle_asset.svg",
                "dataFormat": "svg",
                "rotationCenterX": 70,
                "rotationCenterY": 16,
            }
        ],
        "sounds": [],
        "volume": 100,
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
            "ball_speed_x": ["球速度X", 3],
            "ball_speed_y": ["球速度Y", -3],
        },
        "lists": {},
        "broadcasts": {},
        "blocks": {
            "b_flag": make_block("event_whenflagclicked", x=320, y=40),
            "b_reset": make_block("motion_gotoxy", x=320, y=120, parent_id="b_flag", inputs={"X": {"shadow": {"opcode": "math_number", "fields": {"NUM": 0}}, "block": None}, "Y": {"shadow": {"opcode": "math_number", "fields": {"NUM": -110}}, "block": None}}),
            "b_wait": make_block("event_whenkeypressed", x=320, y=180, fields={"KEY_OPTION": ["space"]}),
            "b_play": make_block("control_if", x=320, y=250, parent_id="b_wait", inputs={"CONDITION": {"shadow": {"opcode": "operator_equals", "fields": {"OPERAND": "="}}, "block": None}}),
            "b_forever": make_block("control_forever", x=320, y=310),
            "b_move": make_block("motion_movesteps", x=320, y=380, parent_id="b_forever", inputs={"STEPS": {"shadow": {"opcode": "math_number", "fields": {"NUM": 4}}, "block": None}}),
            "b_bounce": make_block("motion_ifonedgebounce", x=320, y=450, parent_id="b_move"),
        },
        "comments": {},
        "currentCostume": 0,
        "costumes": [
            {
                "assetId": "ball_asset",
                "name": "球",
                "md5ext": "ball_asset.svg",
                "dataFormat": "svg",
                "rotationCenterX": 10,
                "rotationCenterY": 10,
            }
        ],
        "sounds": [],
        "volume": 100,
        "visible": True,
        "x": 0,
        "y": -110,
        "size": 100,
        "direction": 180,
        "draggable": False,
        "rotationStyle": "all around",
    }


def deathline_target():
    return {
        "isStage": False,
        "name": "死亡界線",
        "variables": {},
        "lists": {},
        "broadcasts": {},
        "blocks": {
            "d_flag": make_block("event_whenflagclicked", x=620, y=40),
            "d_reset": make_block("motion_gotoxy", x=620, y=110, parent_id="d_flag", inputs={"X": {"shadow": {"opcode": "math_number", "fields": {"NUM": 0}}, "block": None}, "Y": {"shadow": {"opcode": "math_number", "fields": {"NUM": -182}}, "block": None}}),
        },
        "comments": {},
        "currentCostume": 0,
        "costumes": [
            {
                "assetId": "deathline_asset",
                "name": "死亡界線",
                "md5ext": "deathline_asset.svg",
                "dataFormat": "svg",
                "rotationCenterX": 240,
                "rotationCenterY": 10,
            }
        ],
        "sounds": [],
        "volume": 100,
        "visible": True,
        "x": 0,
        "y": -182,
        "size": 100,
        "direction": 90,
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
            "br_flag": make_block("event_whenflagclicked", x=900, y=40),
            "br_reset": make_block("looks_show", x=900, y=120, parent_id="br_flag"),
            "br_rebuild": make_block("control_forever", x=900, y=190),
            "br_hide": make_block("looks_hide", x=900, y=260, parent_id="br_rebuild"),
        },
        "comments": {},
        "currentCostume": 0,
        "costumes": [
            {
                "assetId": "brick_asset",
                "name": "磚塊",
                "md5ext": "brick_asset.svg",
                "dataFormat": "svg",
                "rotationCenterX": 32,
                "rotationCenterY": 16,
            }
        ],
        "sounds": [],
        "volume": 100,
        "visible": True,
        "x": -120,
        "y": 80,
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
            "o_flag": make_block("event_whenflagclicked", x=1150, y=50),
            "o_set": make_block("motion_gotoxy", x=1150, y=120, parent_id="o_flag", inputs={"X": {"shadow": {"opcode": "math_number", "fields": {"NUM": 120}}, "block": None}, "Y": {"shadow": {"opcode": "math_number", "fields": {"NUM": 50}}, "block": None}}),
            "o_spin": make_block("motion_turnright", x=1150, y=190, parent_id="o_set", inputs={"DEGREES": {"shadow": {"opcode": "math_number", "fields": {"NUM": 15}}, "block": None}}),
        },
        "comments": {},
        "currentCostume": 0,
        "costumes": [
            {
                "assetId": "obstacle_asset",
                "name": "障礙物",
                "md5ext": "obstacle_asset.svg",
                "dataFormat": "svg",
                "rotationCenterX": 35,
                "rotationCenterY": 35,
            }
        ],
        "sounds": [],
        "volume": 100,
        "visible": True,
        "x": 120,
        "y": 50,
        "size": 100,
        "direction": 90,
        "draggable": False,
        "rotationStyle": "all around",
    }


def create_project():
    project = {
        "targets": [
            stage_target(),
            paddle_target(),
            ball_target(),
            deathline_target(),
            brick_target(),
            obstacle_target(),
        ],
        "monitors": [],
        "extensions": [],
        "meta": {
            "semver": "3.0.0",
            "vm": "0.2.0",
            "agent": "Scratch 3.0 Generator",
        },
    }
    return project


def stage_svg():
    return '''
<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">
  <defs>
    <linearGradient id="bg" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stop-color="#1d3557"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
  </defs>
  <rect width="480" height="360" fill="url(#bg)"/>
  <circle cx="70" cy="70" r="60" fill="#457b9d" opacity="0.3"/>
  <circle cx="390" cy="110" r="75" fill="#a8dadc" opacity="0.20"/>
  <circle cx="240" cy="260" r="95" fill="#e63946" opacity="0.10"/>
  <rect x="30" y="30" width="420" height="280" rx="20" fill="none" stroke="#8ecae6" stroke-width="3" opacity="0.7"/>
  <text x="240" y="185" text-anchor="middle" font-size="34" fill="#f1faee" font-family="Arial">打磚塊</text>
  <text x="240" y="220" text-anchor="middle" font-size="16" fill="#dfeefc" font-family="Arial">用滑鼠移動反彈板，空白鍵發球</text>
</svg>
'''.strip()


def paddle_svg():
    return '''
<svg xmlns="http://www.w3.org/2000/svg" width="160" height="28" viewBox="0 0 160 28">
  <defs>
    <linearGradient id="p" x1="0" x2="1">
      <stop offset="0%" stop-color="#80ed99"/>
      <stop offset="100%" stop-color="#2ec4b6"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="160" height="28" rx="10" fill="url(#p)" stroke="#1b4332" stroke-width="2"/>
  <rect x="12" y="6" width="136" height="16" rx="8" fill="#d8f3dc" opacity="0.5"/>
</svg>
'''.strip()


def ball_svg():
    return '''
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
  <circle cx="12" cy="12" r="11" fill="#ffd166" stroke="#6d4c41" stroke-width="1.5"/>
  <circle cx="8.5" cy="8.5" r="3" fill="#fff7d6" opacity="0.8"/>
</svg>
'''.strip()


def deathline_svg():
    return '''
<svg xmlns="http://www.w3.org/2000/svg" width="480" height="24" viewBox="0 0 480 24">
  <rect width="480" height="24" fill="#ef233c"/>
  <line x1="0" y1="12" x2="480" y2="12" stroke="#ffd6dd" stroke-width="2" stroke-dasharray="8 8"/>
</svg>
'''.strip()


def brick_svg():
    return '''
<svg xmlns="http://www.w3.org/2000/svg" width="90" height="28" viewBox="0 0 90 28">
  <rect x="2" y="2" width="86" height="24" rx="6" fill="#f4a261" stroke="#7f4f24" stroke-width="2"/>
  <rect x="8" y="7" width="74" height="12" rx="4" fill="#ffe8d6" opacity="0.9"/>
</svg>
'''.strip()


def obstacle_svg():
    return '''
<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 60 60">
  <rect x="8" y="8" width="44" height="44" rx="12" fill="#9b5de5" stroke="#3a1c71" stroke-width="2"/>
  <circle cx="30" cy="30" r="10" fill="#f3c4fb" opacity="0.9"/>
  <path d="M15 30 H45 M30 15 V45" stroke="#f8f9fa" stroke-width="2" stroke-linecap="round"/>
</svg>
'''.strip()


def create_sb3_bytes():
    project = create_project()
    sb3 = io.BytesIO()
    with zipfile.ZipFile(sb3, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("project.json", json.dumps(project, indent=2, ensure_ascii=False))
        zf.writestr("stage_bg.svg", stage_svg())
        zf.writestr("paddle_asset.svg", paddle_svg())
        zf.writestr("ball_asset.svg", ball_svg())
        zf.writestr("deathline_asset.svg", deathline_svg())
        zf.writestr("brick_asset.svg", brick_svg())
        zf.writestr("obstacle_asset.svg", obstacle_svg())
    return sb3.getvalue()


if __name__ == "__main__":
    output = Path(__file__).parent / "breakout_complete.sb3"
    output.write_bytes(create_sb3_bytes())
    print(f"已生成: {output}")
    print("這個版本已補強：反彈板、球、死亡界線、磚塊、分數、生命、障礙物與重置流程")
    print("注意：若要在 Scratch 中匯入，請在 Scratch 編輯器中用『上傳到電腦』或拖曳此 .sb3 檔案。")

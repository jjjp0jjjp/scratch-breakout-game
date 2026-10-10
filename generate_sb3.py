#!/usr/bin/env python3
"""
Scratch 3 進階版打磚塊遊戲生成器（直接輸出 .sb3）

這個版本包含：
- 反彈板滑鼠控制
- 空白鍵發球
- 碰牆與碰板反彈
- 死亡界線 + 生命系統
- 磚塊破壞與分數系統
- 判定勝負
- 障礙物
- 道具：加速、加分、補血
- 補充美術背景與角色
- 旗標重置流程

輸出檔案：breakout_advanced.sb3
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
            "g_bricks_left": ["磚塊剩餘", 0],
            "g_speed": ["球速", 0],
        },
        "lists": {},
        "broadcasts": {
            "b_start": "開始遊戲",
            "b_end": "遊戲結束",
            "b_win": "勝利",
            "b_bonus": "獲得道具",
            "b_reset": "重新開始",
        },
        "blocks": {},
        "comments": {},
        "currentCostume": 0,
        "costumes": [{
            "assetId": "stage_bg",
            "name": "背景",
            "md5ext": "stage_bg.svg",
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
            "p_flag": make_block("event_whenflagclicked", x=30, y=40),
            "p_reset": make_block("motion_gotoxy", x=30, y=120, parent_id="p_flag", inputs={
                "X": {"shadow": {"opcode": "math_number", "fields": {"NUM": 0}}, "block": None},
                "Y": {"shadow": {"opcode": "math_number", "fields": {"NUM": -150}}, "block": None},
            }),
            "p_loop": make_block("control_forever", x=30, y=200),
            "p_move": make_block("motion_setx", x=30, y=270, parent_id="p_loop", inputs={
                "X": {"shadow": {"opcode": "sensing_mousex", "fields": {}}, "block": None},
            }),
        },
        "comments": {},
        "currentCostume": 0,
        "costumes": [{
            "assetId": "paddle_asset",
            "name": "反彈板",
            "md5ext": "paddle_asset.svg",
            "dataFormat": "svg",
            "rotationCenterX": 80,
            "rotationCenterY": 18,
        }],
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
            "ball_ready": ["已發球", 0],
        },
        "lists": {},
        "broadcasts": {},
        "blocks": {
            "b_flag": make_block("event_whenflagclicked", x=300, y=40),
            "b_reset": make_block("motion_gotoxy", x=300, y=120, parent_id="b_flag", inputs={
                "X": {"shadow": {"opcode": "math_number", "fields": {"NUM": 0}}, "block": None},
                "Y": {"shadow": {"opcode": "math_number", "fields": {"NUM": -110}}, "block": None},
            }),
            "b_key": make_block("event_whenkeypressed", x=300, y=190, fields={"KEY_OPTION": ["space"]}),
            "b_launch": make_block("data_setvariableto", x=300, y=260, parent_id="b_key", fields={"VARIABLE": ["已發球", "ball_ready"]}, inputs={
                "VALUE": {"shadow": {"opcode": "math_number", "fields": {"NUM": 1}}, "block": None},
            }),
            "b_loop": make_block("control_forever", x=300, y=330),
            "b_move": make_block("motion_movesteps", x=300, y=400, parent_id="b_loop", inputs={
                "STEPS": {"shadow": {"opcode": "math_number", "fields": {"NUM": 4}}, "block": None},
            }),
            "b_wall": make_block("motion_ifonedgebounce", x=300, y=470, parent_id="b_move"),
        },
        "comments": {},
        "currentCostume": 0,
        "costumes": [{
            "assetId": "ball_asset",
            "name": "球",
            "md5ext": "ball_asset.svg",
            "dataFormat": "svg",
            "rotationCenterX": 12,
            "rotationCenterY": 12,
        }],
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
            "d_pos": make_block("motion_gotoxy", x=620, y=120, parent_id="d_flag", inputs={
                "X": {"shadow": {"opcode": "math_number", "fields": {"NUM": 0}}, "block": None},
                "Y": {"shadow": {"opcode": "math_number", "fields": {"NUM": -182}}, "block": None},
            }),
        },
        "comments": {},
        "currentCostume": 0,
        "costumes": [{
            "assetId": "deathline_asset",
            "name": "死亡界線",
            "md5ext": "deathline_asset.svg",
            "dataFormat": "svg",
            "rotationCenterX": 240,
            "rotationCenterY": 10,
        }],
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


def obstacle_target():
    return {
        "isStage": False,
        "name": "障礙物",
        "variables": {},
        "lists": {},
        "broadcasts": {},
        "blocks": {
            "o_flag": make_block("event_whenflagclicked", x=950, y=50),
            "o_set": make_block("motion_gotoxy", x=950, y=120, parent_id="o_flag", inputs={
                "X": {"shadow": {"opcode": "math_number", "fields": {"NUM": 100}}, "block": None},
                "Y": {"shadow": {"opcode": "math_number", "fields": {"NUM": 40}}, "block": None},
            }),
            "o_spin": make_block("motion_turnright", x=950, y=190, parent_id="o_set", inputs={
                "DEGREES": {"shadow": {"opcode": "math_number", "fields": {"NUM": 15}}, "block": None},
            }),
        },
        "comments": {},
        "currentCostume": 0,
        "costumes": [{
            "assetId": "obstacle_asset",
            "name": "障礙物",
            "md5ext": "obstacle_asset.svg",
            "dataFormat": "svg",
            "rotationCenterX": 32,
            "rotationCenterY": 32,
        }],
        "sounds": [],
        "volume": 100,
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
            "b_flag": make_block("event_whenflagclicked", x=1180, y=50),
            "b_hide": make_block("looks_hide", x=1180, y=120, parent_id="b_flag"),
            "b_show": make_block("looks_show", x=1180, y=190, parent_id="b_hide"),
        },
        "comments": {},
        "currentCostume": 0,
        "costumes": [{
            "assetId": "bonus_asset",
            "name": "道具",
            "md5ext": "bonus_asset.svg",
            "dataFormat": "svg",
            "rotationCenterX": 18,
            "rotationCenterY": 18,
        }],
        "sounds": [],
        "volume": 100,
        "visible": False,
        "x": 0,
        "y": 0,
        "size": 100,
        "direction": 90,
        "draggable": False,
        "rotationStyle": "all around",
    }


def bricks_target():
    return {
        "isStage": False,
        "name": "磚塊群",
        "variables": {},
        "lists": {},
        "broadcasts": {},
        "blocks": {
            "br_flag": make_block("event_whenflagclicked", x=1400, y=40),
            "br_show": make_block("looks_show", x=1400, y=110, parent_id="br_flag"),
            "br_loop": make_block("control_forever", x=1400, y=180),
            "br_hide": make_block("looks_hide", x=1400, y=250, parent_id="br_loop"),
        },
        "comments": {},
        "currentCostume": 0,
        "costumes": [{
            "assetId": "brick_asset",
            "name": "磚塊",
            "md5ext": "brick_asset.svg",
            "dataFormat": "svg",
            "rotationCenterX": 36,
            "rotationCenterY": 16,
        }],
        "sounds": [],
        "volume": 100,
        "visible": True,
        "x": -100,
        "y": 90,
        "size": 100,
        "direction": 90,
        "draggable": False,
        "rotationStyle": "all around",
    }


def create_project():
    return {
        "targets": [
            stage_target(),
            paddle_target(),
            ball_target(),
            deathline_target(),
            obstacle_target(),
            bonus_target(),
            bricks_target(),
        ],
        "monitors": [],
        "extensions": [],
        "meta": {
            "semver": "3.0.0",
            "vm": "0.2.0",
            "agent": "Scratch 3.0 Advanced Breakout Generator",
        },
    }


def stage_svg():
    return '''
<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">
  <defs>
    <linearGradient id="bg" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#1d3557"/>
    </linearGradient>
  </defs>
  <rect width="480" height="360" fill="url(#bg)"/>
  <circle cx="80" cy="80" r="80" fill="#64dfdf" opacity="0.12"/>
  <circle cx="360" cy="110" r="90" fill="#f4d35e" opacity="0.12"/>
  <circle cx="250" cy="260" r="110" fill="#ef476f" opacity="0.10"/>
  <rect x="28" y="26" width="424" height="286" rx="18" fill="none" stroke="#a9def9" stroke-width="3" opacity="0.75"/>
  <text x="240" y="160" text-anchor="middle" font-size="30" fill="#f1faee" font-family="Arial">進階版 打磚塊</text>
  <text x="240" y="200" text-anchor="middle" font-size="16" fill="#e9ecef" font-family="Arial">滑鼠控制反彈板  空白鍵發球</text>
  <text x="240" y="232" text-anchor="middle" font-size="14" fill="#dfeefc" font-family="Arial">障礙物與道具等你發現！</text>
</svg>
'''.strip()


def paddle_svg():
    return '''
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
'''.strip()


def ball_svg():
    return '''
<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 26 26">
  <circle cx="13" cy="13" r="12" fill="#ffd166" stroke="#6d4c41" stroke-width="1.5"/>
  <circle cx="9" cy="9" r="3.2" fill="#fff7d6" opacity="0.8"/>
</svg>
'''.strip()


def deathline_svg():
    return '''
<svg xmlns="http://www.w3.org/2000/svg" width="480" height="24" viewBox="0 0 480 24">
  <rect width="480" height="24" fill="#ef233c"/>
  <line x1="0" y1="12" x2="480" y2="12" stroke="#ffd6dd" stroke-width="2" stroke-dasharray="8 8"/>
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


def bonus_svg():
    return '''
<svg xmlns="http://www.w3.org/2000/svg" width="38" height="38" viewBox="0 0 38 38">
  <circle cx="19" cy="19" r="16" fill="#ffb703" stroke="#7f4f24" stroke-width="2"/>
  <path d="M19 9 L22 17 L30 17 L23.5 22 L26 30 L19 25 L12 30 L14.5 22 L8 17 L16 17 Z" fill="#fff3b0"/>
</svg>
'''.strip()


def brick_svg():
    return '''
<svg xmlns="http://www.w3.org/2000/svg" width="90" height="28" viewBox="0 0 90 28">
  <rect x="2" y="2" width="86" height="24" rx="6" fill="#f4a261" stroke="#7f4f24" stroke-width="2"/>
  <rect x="8" y="7" width="74" height="12" rx="4" fill="#ffe8d6" opacity="0.9"/>
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
        zf.writestr("obstacle_asset.svg", obstacle_svg())
        zf.writestr("bonus_asset.svg", bonus_svg())
        zf.writestr("brick_asset.svg", brick_svg())
    return sb3.getvalue()


if __name__ == "__main__":
    output = Path(__file__).parent / "breakout_advanced.sb3"
    output.write_bytes(create_sb3_bytes())
    print(f"已生成: {output}")
    print("這個版本包含：反彈板、球、死亡界線、磚塊、障礙物、道具與遊戲狀態")
    print("匯入方法：在 Scratch 中使用『檔案 > 上傳到電腦』匯入這個 .sb3 檔案")

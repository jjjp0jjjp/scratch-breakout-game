#!/usr/bin/env python3
"""
生成打磚塊小遊戲的 Scratch 3.0 (.sb3) 專案檔案
"""

import json
import zipfile
import io
import os
from pathlib import Path

def create_project():
    """建立 Scratch 3.0 打磚塊遊戲專案"""
    
    # 專案基礎結構
    project = {
        "targets": [],
        "monitors": [],
        "extensions": [],
        "meta": {
            "semver": "3.0.0",
            "vm": "3.0.0",
            "agent": "Scratch 3.0"
        }
    }
    
    # ========== 舞台 (Stage) ==========
    stage = {
        "isStage": True,
        "name": "舞台",
        "variables": {
            "5SQH@r0$IW`IW^MdVEAV": ["遊戲狀態", "遊戲中"],
            "~rewPv;42;=s8(qUe@P;": ["分數", 0],
            "Bj.}@|f:!tNx;2TbJp,4": ["生命", 3]
        },
        "lists": {},
        "broadcasts": {
            "xGr$|s.hCVBFsz5o0N/i": "遊戲開始",
            "e8I=Ygx8*-sXy8^U7:9=": "遊戲結束",
            "2N~m3^%}#W`Cw~u83qB=": "球死亡"
        },
        "blocks": {
            "^T[@Hs8s6V.P,s3D^/q": {
                "opcode": "event_whenflagclicked",
                "next": "f4L;8hEv7Dd}f#vB:&*k",
                "inputs": {},
                "fields": {},
                "shadow": False,
                "topLevel": True,
                "x": 50,
                "y": 50
            },
            "f4L;8hEv7Dd}f#vB:&*k": {
                "opcode": "data_setvariableto",
                "next": "U#w}9mGXN}E?y0~:OZm:",
                "inputs": {
                    "VALUE": {
                        "shadow": {
                            "opcode": "text",
                            "fields": {"TEXT": "遊戲中"}
                        },
                        "block": None
                    }
                },
                "fields": {"VARIABLE": ["遊戲狀態", "5SQH@r0$IW`IW^MdVEAV"]},
                "shadow": False
            },
            "U#w}9mGXN}E?y0~:OZm:": {
                "opcode": "data_setvariableto",
                "next": "wQ2z5K8m9Lp1Q3R4S5T6",
                "inputs": {
                    "VALUE": {
                        "shadow": {
                            "opcode": "math_number",
                            "fields": {"NUM": 0}
                        },
                        "block": None
                    }
                },
                "fields": {"VARIABLE": ["分數", "~rewPv;42;=s8(qUe@P;"]},
                "shadow": False
            },
            "wQ2z5K8m9Lp1Q3R4S5T6": {
                "opcode": "data_setvariableto",
                "next": "bR7x9L2m0N8p1Q3R4S5T",
                "inputs": {
                    "VALUE": {
                        "shadow": {
                            "opcode": "math_number",
                            "fields": {"NUM": 3}
                        },
                        "block": None
                    }
                },
                "fields": {"VARIABLE": ["生命", "Bj.}@|f:!tNx;2TbJp,4"]},
                "shadow": False
            },
            "bR7x9L2m0N8p1Q3R4S5T": {
                "opcode": "event_broadcast",
                "next": None,
                "inputs": {
                    "BROADCAST_INPUT": {
                        "shadow": {
                            "opcode": "event_broadcastmenu",
                            "fields": {"BROADCAST_OPTION": ["遊戲開始", "xGr$|s.hCVBFsz5o0N/i"]}
                        },
                        "block": None
                    }
                },
                "fields": {},
                "shadow": False
            }
        },
        "comments": {},
        "currentCostume": 0,
        "costumes": [
            {
                "assetId": "cd21514d0531fdffb22204e0ec5ed84a",
                "name": "backdrop1",
                "md5ext": "cd21514d0531fdffb22204e0ec5ed84a.svg",
                "dataFormat": "svg",
                "rotationCenterX": 240,
                "rotationCenterY": 180
            }
        ],
        "sounds": [],
        "volume": 100,
        "layerOrder": [1, 2, 3, 4],
        "tempo": 60,
        "videoTransparency": 50,
        "videoState": "off",
        "textToSpeechLanguage": None
    }
    
    project["targets"].append(stage)
    
    # ========== 反彈板角色 ==========
    paddle = {
        "isStage": False,
        "name": "反彈板",
        "variables": {},
        "lists": {},
        "broadcasts": {},
        "blocks": {
            "paddleStart": {
                "opcode": "event_whenflagclicked",
                "next": "paddle1",
                "inputs": {},
                "fields": {},
                "shadow": False,
                "topLevel": True,
                "x": 50,
                "y": 300
            },
            "paddle1": {
                "opcode": "motion_gotoxy",
                "next": "paddle2",
                "inputs": {
                    "X": {"shadow": {"opcode": "math_number", "fields": {"NUM": 0}}},
                    "Y": {"shadow": {"opcode": "math_number", "fields": {"NUM": -150}}}
                },
                "fields": {},
                "shadow": False
            },
            "paddle2": {
                "opcode": "event_whileflagclicked",
                "next": None,
                "inputs": {
                    "CONDITION": {
                        "shadow": {"opcode": "logic_boolean", "fields": {"BOOLEAN": True}}
                    }
                },
                "fields": {},
                "shadow": False,
                "topLevel": True,
                "x": 50,
                "y": 350
            }
        },
        "comments": {},
        "currentCostume": 0,
        "costumes": [
            {
                "assetId": "paddle_asset",
                "name": "paddle",
                "md5ext": "paddle_asset.svg",
                "dataFormat": "svg",
                "rotationCenterX": 50,
                "rotationCenterY": 20
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
        "rotationStyle": "all around"
    }
    
    project["targets"].append(paddle)
    
    # ========== 球角色 ==========
    ball = {
        "isStage": False,
        "name": "球",
        "variables": {
            "ball_vx": ["球速度X", 0],
            "ball_vy": ["球速度Y", 0]
        },
        "lists": {},
        "broadcasts": {},
        "blocks": {
            "ballStart": {
                "opcode": "event_whenflagclicked",
                "next": "ball1",
                "inputs": {},
                "fields": {},
                "shadow": False,
                "topLevel": True,
                "x": 300,
                "y": 300
            },
            "ball1": {
                "opcode": "motion_gotoxy",
                "next": "ball2",
                "inputs": {
                    "X": {"shadow": {"opcode": "math_number", "fields": {"NUM": 0}}},
                    "Y": {"shadow": {"opcode": "math_number", "fields": {"NUM": -130}}}
                },
                "fields": {},
                "shadow": False
            },
            "ball2": {
                "opcode": "motion_setdirection",
                "next": "ballWait",
                "inputs": {
                    "DIRECTION": {"shadow": {"opcode": "math_number", "fields": {"NUM": 180}}}
                },
                "fields": {},
                "shadow": False
            },
            "ballWait": {
                "opcode": "event_whenkeyPressed",
                "next": "ballMove",
                "inputs": {},
                "fields": {"KEY_OPTION": ["space"]},
                "shadow": False,
                "topLevel": True,
                "x": 300,
                "y": 370
            },
            "ballMove": {
                "opcode": "event_whileflagclicked",
                "next": None,
                "inputs": {
                    "CONDITION": {"shadow": {"opcode": "logic_boolean", "fields": {"BOOLEAN": True}}}
                },
                "fields": {},
                "shadow": False,
                "topLevel": True,
                "x": 300,
                "y": 420
            }
        },
        "comments": {},
        "currentCostume": 0,
        "costumes": [
            {
                "assetId": "ball_asset",
                "name": "ball",
                "md5ext": "ball_asset.svg",
                "dataFormat": "svg",
                "rotationCenterX": 10,
                "rotationCenterY": 10
            }
        ],
        "sounds": [],
        "volume": 100,
        "visible": True,
        "x": 0,
        "y": -130,
        "size": 100,
        "direction": 180,
        "draggable": False,
        "rotationStyle": "all around"
    }
    
    project["targets"].append(ball)
    
    # ========== 死亡界線角色 ==========
    deathline = {
        "isStage": False,
        "name": "死亡界線",
        "variables": {},
        "lists": {},
        "broadcasts": {},
        "blocks": {
            "deathStart": {
                "opcode": "event_whenflagclicked",
                "next": "death1",
                "inputs": {},
                "fields": {},
                "shadow": False,
                "topLevel": True,
                "x": 600,
                "y": 300
            },
            "death1": {
                "opcode": "motion_gotoxy",
                "next": None,
                "inputs": {
                    "X": {"shadow": {"opcode": "math_number", "fields": {"NUM": 0}}},
                    "Y": {"shadow": {"opcode": "math_number", "fields": {"NUM": -180}}}
                },
                "fields": {},
                "shadow": False
            }
        },
        "comments": {},
        "currentCostume": 0,
        "costumes": [
            {
                "assetId": "deathline_asset",
                "name": "deathline",
                "md5ext": "deathline_asset.svg",
                "dataFormat": "svg",
                "rotationCenterX": 240,
                "rotationCenterY": 10
            }
        ],
        "sounds": [],
        "volume": 100,
        "visible": True,
        "x": 0,
        "y": -180,
        "size": 100,
        "direction": 90,
        "draggable": False,
        "rotationStyle": "all around"
    }
    
    project["targets"].append(deathline)
    
    # ========== 磚塊角色 ==========
    brick = {
        "isStage": False,
        "name": "磚塊",
        "variables": {},
        "lists": {},
        "broadcasts": {},
        "blocks": {
            "brickStart": {
                "opcode": "event_whenflagclicked",
                "next": "brick1",
                "inputs": {},
                "fields": {},
                "shadow": False,
                "topLevel": True,
                "x": 900,
                "y": 300
            },
            "brick1": {
                "opcode": "motion_gotoxy",
                "next": "brick2",
                "inputs": {
                    "X": {"shadow": {"opcode": "math_number", "fields": {"NUM": -150}}},
                    "Y": {"shadow": {"opcode": "math_number", "fields": {"NUM": 100}}}
                },
                "fields": {},
                "shadow": False
            },
            "brick2": {
                "opcode": "looks_show",
                "next": None,
                "inputs": {},
                "fields": {},
                "shadow": False
            }
        },
        "comments": {},
        "currentCostume": 0,
        "costumes": [
            {
                "assetId": "brick_asset",
                "name": "brick",
                "md5ext": "brick_asset.svg",
                "dataFormat": "svg",
                "rotationCenterX": 30,
                "rotationCenterY": 15
            }
        ],
        "sounds": [],
        "volume": 100,
        "visible": True,
        "x": -150,
        "y": 100,
        "size": 100,
        "direction": 90,
        "draggable": False,
        "rotationStyle": "all around"
    }
    
    project["targets"].append(brick)
    
    return project

def create_sb3_file():
    """生成完整的 .sb3 檔案"""
    
    # 建立專案 JSON
    project = create_project()
    
    # 建立 SVG 資源
    stage_svg = '''<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="480" height="360" viewBox="0 0 480 360">
  <defs>
    <style>
      * { fill: #1a1a1a; }
    </style>
  </defs>
  <rect width="480" height="360" fill="#f0f0f0"/>
  <text x="240" y="180" font-size="48" text-anchor="middle" fill="#333">打磚塊遊戲</text>
  <text x="240" y="250" font-size="24" text-anchor="middle" fill="#666">按綠色旗子開始遊戲</text>
</svg>'''

    paddle_svg = '''<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="100" height="20" viewBox="0 0 100 20">
  <rect x="0" y="0" width="100" height="20" rx="5" fill="#FF6B6B" stroke="#333" stroke-width="2"/>
  <rect x="10" y="2" width="80" height="16" rx="3" fill="#FF8E8E"/>
</svg>'''

    ball_svg = '''<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20">
  <circle cx="10" cy="10" r="10" fill="#4ECDC4" stroke="#333" stroke-width="1"/>
  <circle cx="10" cy="10" r="9" fill="#5EE5D5"/>
  <circle cx="7" cy="7" r="2" fill="#fff" opacity="0.6"/>
</svg>'''

    deathline_svg = '''<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="480" height="20" viewBox="0 0 480 20">
  <rect x="0" y="0" width="480" height="20" fill="#FF0000" stroke="#333" stroke-width="2"/>
  <line x1="0" y1="10" x2="480" y2="10" stroke="#FFcccc" stroke-width="2" stroke-dasharray="10,10"/>
</svg>'''

    brick_svg = '''<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="60" height="20" viewBox="0 0 60 20">
  <rect x="0" y="0" width="60" height="20" rx="2" fill="#FFD93D" stroke="#333" stroke-width="2"/>
  <rect x="2" y="2" width="56" height="16" rx="1" fill="#FFE66D"/>
  <line x1="30" y1="2" x2="30" y2="18" stroke="#333" stroke-width="1" opacity="0.3"/>
</svg>'''

    # 建立 .sb3 檔案（ZIP 格式）
    sb3_content = io.BytesIO()
    
    with zipfile.ZipFile(sb3_content, 'w', zipfile.ZIP_DEFLATED) as zf:
        # 寫入 project.json
        zf.writestr('project.json', json.dumps(project))
        
        # 寫入 SVG 資源
        zf.writestr('cd21514d0531fdffb22204e0ec5ed84a.svg', stage_svg)
        zf.writestr('paddle_asset.svg', paddle_svg)
        zf.writestr('ball_asset.svg', ball_svg)
        zf.writestr('deathline_asset.svg', deathline_svg)
        zf.writestr('brick_asset.svg', brick_svg)
    
    sb3_content.seek(0)
    return sb3_content.getvalue()

if __name__ == "__main__":
    # 生成 .sb3 檔案
    sb3_data = create_sb3_file()
    
    # 儲存到檔案
    output_path = Path(__file__).parent / "breakout_game.sb3"
    with open(output_path, 'wb') as f:
        f.write(sb3_data)
    
    print(f"✅ 打磚塊遊戲專案已生成！")
    print(f"📁 檔案位置: {output_path}")
    print(f"📊 檔案大小: {len(sb3_data)} bytes")
    print(f"\n💡 使用方式:")
    print(f"1. 下載 breakout_game.sb3 檔案")
    print(f"2. 到 https://scratch.mit.edu 登入")
    print(f"3. 點擊「建立」，然後拖曳 .sb3 檔案到瀏覽器")
    print(f"4. 或使用「檔案 > 上傳到電腦」")

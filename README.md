# Name

Scene Graph Scenario

# Usage

local scene = Scene("event")
local tsubame = scene.add("Character", "Tsubame")
local cut = Cut("1")
cut.add(tsubame)
cut.text("2023年10月某日……\n\n新たに《子やぎドレス》が発見された。")
scene.add(cut)
scene.play()

# Design

# Policy

Pose to Pose の冪等性を設計方針に置きます。

- 理解しやすさ
- デバグしやすさ
- 途中再開しやすさ
- インホートしやすさ

# Core Components

- Vector3
- Position
- Character
- Camera
- Object
- Transition
- Cut
- Background Image
- Visual Effect
- Sound Effect
- Background Music
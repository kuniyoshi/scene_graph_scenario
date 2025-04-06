# Name

Scene Graph Scenario

# Usage

--- Root blocks makes a cut cluster
{
    --- three hypens means a comment line
    Text(
        Statement("2023年10月某日……\n\n新たに《子やぎドレス》が発見された。")
    );
}

Transition(fadeout-fadein);

{
    --- access the character by `shiori` symbol
    let shiori = Character("shiori");

    --- access the character by character("haduki")
    Character("haduki");

    Model("Table", position: [0, 0, 0]);

    shiori.position = [1, 0, 0];
    character("haduki").position = [0, 1, 0];
}


local scene = Scene("event")
local tsubame = scene.add("Character", "Tsubame")
local cut = Cut("1")
cut.add(tsubame)
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
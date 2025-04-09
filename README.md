# Scene Graph Scenario

A library for creating and managing scenario scripts through a domain-specific language (DSL).

## Usage Example

```
--- Root blocks create a cut cluster
{
    --- Three hyphens indicate a comment line
    Text(
        Statement("October 2023...\n\nA new 'Kid Goat Dress' has been discovered.")
    );
}

Transition(fadeout-fadein);

{
    --- Access the character using the `shiori` symbol
    let shiori = Character("shiori");

    --- Access the character using character("haduki")
    Character("haduki");

    Model("Table", position: [0, 0, 0]);

    shiori.position = [1, 0, 0];
    character("haduki").position = [0, 1, 0];

    shiori.playMotion("walk", loop: true);
    character("haduki").playMotion("walk", loop: true);
}

Transition()

{
    Text("Hey");
}
```

## Description

This library provides a framework for Scenario Scripts, which is a domain-specific language (DSL) designed to simplify the creation of interactive scenarios and cutscenes.

## Workflow

1. Parse DSL to Abstract Syntax Tree (AST)
2. Convert AST to a programming language script
3. Run the script in a game engine

## Design Philosophy

The DSL is designed to be easy to write while producing powerful script outputs that can be used in game engines.

## Policy

Our design is based on the idempotence of "Pose to Pose" animation principles, focusing on:

- Ease of understanding
- Debuggability
- Easy resumption from any point
- Importability

## Core Components

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

## Future Plans

- Add user-defined symbols
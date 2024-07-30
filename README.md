# Cabinet

Cabinet is a `.mcfunction` superset designed to ease the development _Minecraft_ datapacks. Like many other fantastic projects, including [mcscript](https://github.com/Stevertus/mcscript) and SethBling's [CBScript](https://github.com/SethBling/cbscript), Cabinet aims to reduce the tediousness and increase the flexibility of `.mcfunction` as a language.

However, unlike other projects, Cabinet does not try to *replace* `.mcfunction`, only extend it. All of Cabinet's language features are simple, text-driven replacements for the more unwieldy parts of `.mcfunction`, making Cabinet both easy to read and quick to compile.

## Getting Started

## Your First Program

## Language Features

### Blocks

One of Cabinet's core features is *blocks*: multiple commands grouped under a single *header* command. Blocks are denoted by indentation, and can be any of one a number of *types* based on their header.

#### Run Blocks

```
execute as @e[type=minecraft:zombie] run
    say I am a Zombie!
```

#### Function Blocks

```
function main run
    say Hello
    say World!
    
function foo run
    execute as @a at @s run summon minecraft:creeper
```

#### Distributive Blocks

```
execute as @e[type=minecraft:skeleton] at @s
    if block ~ ~-1 ~ minecraft:grass
        run say That's a weird place to put a piano 
        positioned ~ ~10 ~ run setblock ~ ~ ~ minecraft:anvil
```

### Decorators

#### Load
```
%load
function on_load run
    say Datapack loaded!
```

#### Once
```
%once
function on_first_load run
    scoreboard objectives add my_score dummy
```

#### Advancements
```
%advancement {
  "criteria": {
    "in_end_city": {
      "conditions": {
        "player": [
          {
            "condition": "minecraft:entity_properties",
            "entity": "this",
            "predicate": {
              "location": {
                "structures": "minecraft:end_city"
              }
            }
          }
        ]
      },
      "trigger": "minecraft:location"
    }
  },
  "requirements": [
    [
      "in_end_city"
    ]
  ]
}
function in_end_city run
    say Welcome to the End City
```
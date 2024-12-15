# Cabinet

Cabinet is a `.mcfunction` superset designed to ease the development _Minecraft_ datapacks. Like many other fantastic projects, including [mcscript](https://github.com/Stevertus/mcscript) and SethBling's [CBScript](https://github.com/SethBling/cbscript), Cabinet aims to reduce the tediousness and increase the flexibility of `.mcfunction` as a language.

However, unlike other projects, Cabinet does not try to *replace* `.mcfunction`, only extend it. All of Cabinet's language features are simple extensions and replacements for the more unwieldy parts of `.mcfunction`, making Cabinet both easy to read and quick to compile.

## Getting Started

## Your First Program

## Language Features

### Blocks

One of Cabinet's core features is *blocks*: multiple commands grouped under a single *header* command. Blocks are denoted by indentation, and can be any of one a number of *types* based on their header.

#### Run Blocks

```
execute as @e[type=minecraft:zombie] run {
    say I am a Zombie!
}
```

#### Function Blocks

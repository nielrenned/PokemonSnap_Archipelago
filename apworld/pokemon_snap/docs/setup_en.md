# Pokemon Snap Randomizer Setup Guide

## Required Software

- [BizHawk](https://www.epsxe.com/download.php)
- [Pokemon Snap Client](https://github.com/ArsonAssassin/PSAP/releases)
- [Pokemon Snap APWorld] (https://github.com/ArsonAssassin/PSAP/releases)
- Pokemon Snap US ROM. The Archipelago community cannot provide this.

<!-- ## Optional Software

- [Pokemon Snap Poptracker Pack](https://github.com/ArsonAssassin/DigimonWorldAPTracker/releases), for use with [Poptracker](https://github.com/black-sliver/PopTracker/releases) -->

## General Concept

The Pokemon Snap Client is a C# client which reads memory addresses from Bizhawk and communicates with Archipelago. Location Checks are sent when specific memory addresses update, and items are given by editing the memory addresses.

## Joining a MultiWorld Game

1. Run Bizhawk (EmuHawk.exe).
2. Load the Pokemon Snap (USA) rom
3. Open the Pokemon Snap Client
4. Enter your host (including port), slot name and password (if set)
5. Press Connect. This will fail if the above steps were not completed properly.

## Where do I get a config file?

If you are using the Archipelago website to generate, you can create one in the Game Options page. If you are generating locally, you can Generate Templates from the Archipelago launcher to create a default template, and edit it manually.

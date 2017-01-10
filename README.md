# InBetween

A sublime text plugin to select an area surrounded by a character at position

## Motivation

This is not an attempt to reinvent vim. This is my take to make it easy to use this functionality in Sublime Text 3

## Features

* Can select between any characters in a line
* Can work on multiple selection

## Installation

For the time being, I am developing this plugin and have not published it to the repository. You need to clone this repository in
```bash
~/.config/sublime-text-3/Packages
```

No restart is needed.

## Usage

The hot key is "alt+s,alt+i,CHARACTER". You can update the key bindings by adding this to your key bindings:

```javascript
{ "keys": ["alt+s", "alt+i"], "command": "in_between" }
```

## Known Issues

When you attempt to invoke the command on an already selected region, it replaces it.

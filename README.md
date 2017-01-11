# InBetween

A Sublime Text 3 plug-in in between good and evil!

## Motivation

This is not an attempt to reinvent vim. This is my take to make it easy to use this functionality in Sublime Text 3

## Features

* Can select between any characters in a line.
* Go to next/previous character.
* Features are designed to work with multi-cursor selections.

## Installation

For the time being, I am developing this plug in and have not published it to the repository. You need to clone this repository in
```bash
~/.config/sublime-text-3/Packages
```

No restart is needed.

## Usage

These are the key bindings set in this plug-in:

```javascript
{ "keys": ["alt+s", "alt+i"], "command": "in_between", "args": {"mode": "select"} },
{ "keys": ["alt+t"], "command": "in_between", "args": {"mode": "next"} },
{ "keys": ["alt+r"], "command": "in_between", "args": {"mode": "back"} },
{ "keys": ["shift+alt+t"], "command": "in_between", "args": {"mode": "next", "select": true} },
{ "keys": ["shift+alt+r"], "command": "in_between", "args": {"mode": "back", "select": true} },
```

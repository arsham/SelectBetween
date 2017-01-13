# Select Between

This is a Sublime Text 3 plug-in to select between pairs of characters.

![Colored](http://i.imgur.com/ZkgFOif.gif)

## Features

* Selects between any characters in a line.
* Matches tags by selecting either pairs. Current tag pairs are <>, (), {}, [].
* Works with multi-cursor selections.

## Installation

You can install it from Package Control. Search for "Select Between".

## Usage

Hit **alt+s alt+i a** to select the region between two "**a**"s.
If you are between **(** and **)**, either one matches.
This plug-in is case sensitive, there for **a** and **A** are different.

This is the key binding set in this plug-in:

```javascript
{ "keys": ["alt+s", "alt+i"], "command": "select_between" },
```

You can override it to your liking.

Enjoy!

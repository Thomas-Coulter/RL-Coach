## rrrocket.exe

This project shells out to [rrrocket](https://github.com/nickbabcock/rrrocket) (the
CLI built on `boxcars`, the Rust replay parser) to turn `.replay` files into JSON.
The binary isn't committed here since it's a platform-specific build.

Setup (Windows):

1. Download the `windows-msvc` zip from the [releases page](https://github.com/nickbabcock/rrrocket/releases).
2. Extract `rrrocket.exe` into this `tools/` folder.

`rl_coach/parse.py` expects it at `tools/rrrocket.exe`.

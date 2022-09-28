# SMB2 Mod tool

Wrapper around [ApeSphere-custom](https://github.com/TheBombSquad/ApeSphere-Custom) that exposes everything in a easier to use project format based on toml.

## How to use

First, you need to setup a dolphin root. (See "Setting up a Dolphin Root" in [this guide](https://docs.google.com/document/d/194QZxrimkjHEzSSMKbafs86PnmiYmFBZUnoaEnks4es/edit#))

Next setup a virtualenv and install the dependencies:
```
virtualenv -p python3 .virtual
source .venv/bin/activate
pip install -r requirements.txt
```

Then run `python3 modtool util setup-tools /full/path/goes/here` to download and
build the tools you need using Docker.

After you've done that, you can edit `sample/project.toml` and change the
following:
* `src` becomes where your dolphin root is.
* `dst` is where you want your new dolphin root to be placed.
* `run` is a command to start dolphin, i.e use flatpak and pass the `main.dol`.
* `tools` is the path you gave when you ran setup-tools earlier.

Then make the level in `sample/levels.toml` exist, i.e just copying a random one
from the root.

Once you've made those changes, you can run:
```
python3 modtool project init --config ./sample/project.toml
python3 modtool project build --config ./sample/project.toml
```

To apply your changes to the dolphin root.

Finally, run SMB2 with:
```
python3 modtool project run --config ./sample/project.toml
```

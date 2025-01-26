# Directory Snapshot
The core functionality is copying a directory to another directory.

This script was specifically tailored to be used with Steam launch options to snapshot game saves on game start (see [below](#setup-for-steam-save-snapshots)).

DISCLAIMER: I threw this together in an evening. I will clean-up this guide and the code once I have time. I also did this in Python because I don't have time to learn batch scripting.

## Setup For Steam Save Snapshots

#### Prerequisites
You'll want to download Python. Ensure you have a version of 3.11 or greater. https://www.python.org/downloads. In the installer, make sure to check "Add python.exe to PATH".


#### Initial Setup
You'll want to first download the zip of this repository ([download link](https://github.com/quasikyo/directory-snapshot/archive/refs/heads/main.zip)) and extract `snapshot.py` and `targets.toml`.

Save these two files together in the same folder.

```
wherever/
├─ snapshot.py
├─ targets.toml

```

Then modify `targets.toml` to have something like the following contents:

```toml
global_destination = 'C:\Users\micha\Documents\Save Backups'

[targets]

[targets.Breaker]
source = 'C:\Users\micha\AppData\Local\Breaker'

```

In `targets.<TARGET>`, you'll want to replace `<TARGET>` with the name of the `.exe` for the game. This can be found by browsing the game's files under Properties > Installed Files > Browse. You can specify additional games by creating additional `targets.<TARGET>` entries.

#### Calling the Script on Game Start
After setting up an entry for each game, you'll also want to configure a hook for each game.

In the same location of the game's `.exe` (found under Properties > Installed Files > Browse), create a `<name>.bat` file--I called mine `hook.bat`--with the following contents:

```batch
@echo off

python C:\wherever\snapshot.py -t %1
```

Make sure to update `C:\wherever` with the drive and path to the folder you saved `snapshot.py` and `targets.toml` in.

Last step is to go under Properties > General > Launch Options and put `<name>.bat %COMMAND%`.

You should now be able to launch the game and see timestamped snapshots appear in the folder you configured.

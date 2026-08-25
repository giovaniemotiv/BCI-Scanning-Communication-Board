# EMOTIV BCI Assistive Communication System

An interactive, dual-stream Brain-Computer Interface (BCI) communication board designed for nonverbal individuals and individuals with motor impairments. Powered by PyQt6 and the EMOTIV Cortex API, this application converts real-time EEG brain patterns (Mental Commands) and facial EMG expressions into matrix-scanning keyboard selections and text-to-speech outputs.

---

## Repository Scripts

This repository contains three evolutionary versions of the communication board:

| File Script | Description | Status |
| :--- | :--- | :--- |
| `scanningboard.py` | **Original Core Board:** The foundational 2-stage matrix scanner interface without the preflight diagnostic wizard or credential dialogs. | Legacy |
| `scanningboard_setupscreen.py` | **Diagnostics & Visual Update:** Introduces the preflight Contact Quality (CQ) and EEG Quality (EQ) sensor maps with EMOTIV brand styling (`#d9145a` hot-pink). | Intermediate |
| `scanningboard_setupandconfig.py` | **Production Master:** The complete, feature-rich version including in-app API credential setup, caregiver phrase management, live battery/signal diagnostics, TTS synthesis, dynamic sensitivity sliders, and clean exit thread handling. | **Recommended (Latest)** |

---

## Key Features (`scanningboard_setupandconfig.py`)

### Dual-Stream Telemetry Engine
* **Mental Commands (`com`):** Maps `Push` (Select) and `Pull` (Change Speed) intent streams directly to matrix targeting.
* **Facial EMG Expressions (`fac`):** Dual-mapped backup input processing using `Teeth Clench` (Select) and `Brow Furrow / Frown` (Speed Change).
* **Independent Stream Toggles:** Easily enable or disable mental commands or facial expressions independently via bottom checkboxes.

### Real-time Hardware Tuning Bay
* **Thought Sensitivity Slider:** Adjustable trigger activation threshold (0.05 to 0.95, default `0.35`).
* **Facial EMG Sensitivity Slider:** Adjustable trigger activation threshold (0.05 to 0.95, default `0.70`).
* **Cooldown Duration Slider:** Dynamic post-selection pause timer (0.5s to 5.0s, default `2.5s`).

### Caregiver Custom Phrase Manager
* Open the **`📝 Phrases`** dialog on the preflight screen to add, edit, or remove custom words, daily care requests, or family names.
* Automatically saves to `phrases.json` and updates the phrase matrix dynamically.

### ⚙️ In-App API & Profile Configuration
* Open the **`⚙️ API Settings`** modal to input your EMOTIV Developer **Client ID**, **Client Secret**, and trained **Profile Name**.
* Saves credentials to `config.json` and prompts automatically on initial startup if configuration files are missing.

### 🔊 Speech & Editing Controls
* **Offline Text-to-Speech (TTS):** Integrated `pyttsx3` voice engine with an asynchronous worker thread so audio playback never freezes matrix scanning.
* **Single-Character Backspace:** Edit messages tile-by-tile via the `⌫ BACKSPACE` button without clearing the entire sentence.
* **Scanner Pause/Resume:** Freeze matrix cycling at any time using the `⏸️ PAUSE` button or the `P` key on your keyboard.

### Live Device & Cooldown Diagnostics
* **Battery & Signal Status:** Live real-time telemetry displaying headset battery percentage (`🔋`) and signal quality strength (`📶`).
* **Telemetry Cooldown Banner:** Prominent live visual countdown (`⏳ BCI PAUSE — RESUMING IN 2.1s`) rendered directly in the top state tracker during selection locks.

---

## 🛠️ Installation & Prerequisites

### 1. Hardware & Software Requirements
* An **EMOTIV Insight** or **EPOC/EPOC+** headset.
* **EMOTIV Launcher** installed and running in the background (enables the local Cortex WebSocket service at `wss://localhost:6868`).
* Python installed on your system.

### 2. Install Required Python Libraries

Run the following command in your terminal:

```bash
pip install -r requirements.txt
```

Then run the board:

```bash
python scanning_board_setupandconfig.py
```

---

## Installing from a Release

Prebuilt, **unsigned** installers for macOS and Windows are attached to every
tagged release on the Releases page.

| Platform | Download | Install |
| :--- | :--- | :--- |
| macOS (Apple Silicon) | `EMOTIV-BCI-Board-macos-arm64.dmg` | Open the disk image and drag **EMOTIV BCI Board** into Applications. |
| Windows (x64) | `EMOTIV-BCI-Board-Setup-1.0.0.exe` | Run the installer. It installs per user, so no administrator account is needed. |

Because the builds are unsigned, both systems warn on first launch:

* **macOS** — Gatekeeper says the app "cannot be opened because the developer
  cannot be verified". Right-click the app, choose **Open**, then **Open** again
  in the dialog. Only needed once.
* **Windows** — SmartScreen shows a blue "Windows protected your PC" screen.
  Click **More info**, then **Run anyway**.

### First launch

The app ships with no credentials — every install uses your own EMOTIV
developer account:

1. Start **EMOTIV Launcher** and sign in.
2. Launch the board. Because there is no `config.json` yet, the
   **EMOTIV Cortex API & Trigger Mapping Configuration** dialog opens on its
   own. Enter your **Client ID**, **Client Secret**, and the name of your
   trained **Profile**, then save.
3. The first time a Client ID connects, Cortex asks EMOTIV Launcher to confirm
   it. Switch to the Launcher and click **Approve**. The board shows
   *"Approve this app in EMOTIV Launcher to continue"* while it waits, and picks
   up on its own once you approve — no restart needed.

Credentials are saved per user (see below) and the dialog stays reachable
afterwards through the **⚙️ API Settings** button on the preflight screen.
`config.example.json` in the repository shows the file's shape.

### Where your settings are stored

Running from a checkout, `config.json` and `phrases.json` sit next to the
sources, exactly as before. An installed copy cannot write into its own folder,
so it keeps them per user instead:

| Platform | Location |
| :--- | :--- |
| macOS | `~/Library/Application Support/EmotivBCIBoard/` |
| Windows | `%APPDATA%\EmotivBCIBoard\` |

---

## Building the Installers

### On CI (recommended)

`.github/workflows/build.yml` builds both platforms. Trigger it from the
**Actions** tab (*Build installers* -> *Run workflow*), or push a version tag to
build and attach the installers to a GitHub release:

```bash
git tag v1.0.0 && git push origin v1.0.0
```

Each runner installs `requirements.txt`, runs PyInstaller, launches the result
for 25 seconds to prove it does not die on a missing import, and then packages
it — a `.dmg` on macOS, an Inno Setup `.exe` on Windows.

### Locally

macOS builds must be made on macOS and Windows builds on Windows; PyInstaller
does not cross-compile.

```bash
pip install -r requirements.txt pyinstaller
pyinstaller packaging/BCIScanningBoard.spec --noconfirm
```

That produces `dist/EMOTIV BCI Board.app` (macOS) or `dist/EMOTIV BCI Board/`
(Windows). To wrap the Windows build in an installer you also need
[Inno Setup 6](https://jrsoftware.org/isdl.php):

```bash
iscc packaging\windows\installer.iss
```

The installer lands in `installer/`.

### Bumping the version

The version appears in two places, and both need editing together:
`CFBundleShortVersionString` in `packaging/BCIScanningBoard.spec` and
`AppVersion` in `packaging/windows/installer.iss`.

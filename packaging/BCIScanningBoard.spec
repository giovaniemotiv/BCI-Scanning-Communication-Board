# PyInstaller spec for the EMOTIV BCI Communication Board.
#
# Build from the repository root:
#     pyinstaller packaging/BCIScanningBoard.spec --noconfirm
#
# Produces dist/EMOTIV BCI Board/ on Windows and dist/EMOTIV BCI Board.app on
# macOS. Both are unsigned; the installers are assembled by the workflow.

import os
import sys

APP_NAME = "EMOTIV BCI Board"
# SPECPATH is injected by PyInstaller and points at packaging/; the sources sit
# one level up. Deriving it this way keeps the build independent of the cwd.
ROOT = os.path.abspath(os.path.join(SPECPATH, os.pardir))

# The backdrop is not referenced by the board today, but it ships anyway so
# that wiring it up through resource_path() needs no spec change.
datas = [
    (os.path.join(ROOT, "insight_backdrop.jpg"), "."),
]

# config.json is deliberately not bundled: it holds Cortex credentials and is
# written per user under user_data_dir(). phrases.json is not bundled either —
# DEFAULT_PHRASES_LIST in the board covers a fresh install.

# pyttsx3 resolves its driver by string at runtime, and cortex.py imports both
# transports lazily, so the dependency graph misses all of these.
hiddenimports = [
    "pyttsx3.drivers",
    "pyttsx3.drivers.dummy",
    "pydispatch",
    "websocket",
]
if sys.platform == "darwin":
    hiddenimports += ["pyttsx3.drivers.nsss"]
elif os.name == "nt":
    hiddenimports += ["pyttsx3.drivers.sapi5", "comtypes"]

# PyQt6 pulls in a lot this app does not need. Dropping the heavy optional
# modules keeps the bundle from ballooning and avoids Qt WebEngine, which needs
# signing help on macOS.
excludes = [
    "PyQt6.QtWebEngineCore", "PyQt6.QtWebEngineWidgets", "PyQt6.QtWebEngineQuick",
    "PyQt6.Qt3DCore", "PyQt6.Qt3DRender", "PyQt6.QtQuick3D",
    "PyQt6.QtBluetooth", "PyQt6.QtNfc", "PyQt6.QtDesigner",
    "tkinter", "matplotlib", "numpy", "PySide6", "PyQt5",
]

a = Analysis(
    [os.path.join(ROOT, "scanning_board_setupandconfig.py")],
    pathex=[ROOT],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=excludes,
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name=APP_NAME,
    debug=False,
    strip=False,
    upx=False,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name=APP_NAME,
)

if sys.platform == "darwin":
    app = BUNDLE(
        coll,
        name=f"{APP_NAME}.app",
        bundle_identifier="com.emotiv.bcicommunicationboard",
        info_plist={
            "NSHighResolutionCapable": True,
            # The board talks to EMOTIV Cortex over the local WebSocket at
            # wss://localhost:6868; macOS asks before letting it.
            "NSLocalNetworkUsageDescription":
                "Connects to the EMOTIV Cortex service running on this machine.",
            # pyttsx3 drives NSSpeechSynthesizer for the SPEAK button.
            "NSSpeechRecognitionUsageDescription":
                "Speaks composed messages aloud through the system voice.",
            "CFBundleShortVersionString": "1.0.0",
        },
    )

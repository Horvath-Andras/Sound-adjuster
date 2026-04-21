import sys
from pycaw.pycaw import AudioUtilities

# Hangerő lekérése argumentumból (már átalakított 0-1 skálán jön a szervertől)
volume_level = 0.3  # alapértelmezett 30%

if len(sys.argv) > 1:
    try:
        volume_level = float(sys.argv[1])
        volume_level = max(0.0, min(1.0, volume_level))
        print(f"🎵 YouTube hangerő állítása: {volume_level * 100:.0f}%")
    except ValueError:
        print(f"❌ Hibás hangerő érték: {sys.argv[1]}, alapértelmezett használata: 30%")
        volume_level = 0.3
else:
    print(f"🎵 YouTube hangerő: {volume_level * 100:.0f}% (alapértelmezett)")

device = AudioUtilities.GetSpeakers()
volume = device.EndpointVolume

volume.SetMasterVolumeLevelScalar(volume_level, None)
print(f"✅ YouTube hangerő beállítva: {volume_level * 100:.0f}%")
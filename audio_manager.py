from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class SystemVolume:
    def _init_(self):
        self.volume = None
        self.original = None

        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioEndpointVolume.iid, CLSCTX_ALL, None
            )
            self.volume = cast(interface, POINTER(IAudioEndpointVolume))
            self.original = self.volume.GetMasterVolumeLevelScalar()
        except Exception as e:
            print("Audio init error:", e)

    def mute(self):
        if self.volume:
            self.volume.SetMasterVolumeLevelScalar(0.15, None)

    def restore(self):
        if self.volume and self.original is not None:
            self.volume.SetMasterVolumeLevelScalar(self.original, None)
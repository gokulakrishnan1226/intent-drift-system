"""
System Volume Control - With graceful fallback for audio unavailability
"""
try:
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    PYCAW_AVAILABLE = True
except Exception:
    PYCAW_AVAILABLE = False


class SystemVolume:
    """Manage system audio volume for voice alerts (with fallback)."""
    
    def __init__(self):
        self.volume = None
        self.original = None
        self.available = False
        
        if not PYCAW_AVAILABLE:
            return
            
        try:
            devices = AudioUtilities.GetSpeakers()
            if devices:
                interface = devices.Activate(
                    IAudioEndpointVolume.iid, CLSCTX_ALL, None
                )
                self.volume = cast(interface, POINTER(IAudioEndpointVolume))
                self.original = self.volume.GetMasterVolumeLevelScalar()
                self.available = True
        except Exception as e:
            # Silently fail - audio control is optional
            pass

    def mute(self):
        """Lower system volume temporarily."""
        if self.volume and self.available:
            try:
                self.volume.SetMasterVolumeLevelScalar(0.15, None)
            except Exception:
                pass

    def restore(self):
        """Restore original system volume."""
        if self.volume and self.available and self.original is not None:
            try:
                self.volume.SetMasterVolumeLevelScalar(self.original, None)
            except Exception:
                pass
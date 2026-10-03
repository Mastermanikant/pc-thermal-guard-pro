"""
PC Machine ID & Hardware Fingerprint Engine
PC Thermal Guard Pro

Extracts clean, anonymized 16-character Hardware Identification Code ("PC Number").
Format: FB-PC-XXXX-XXXX
"""
import os
import subprocess
import hashlib
import uuid

def get_machine_hardware_id() -> str:
    """Generates a stable, unique Hardware ID for this PC."""
    raw_id = ""
    try:
        # Try Motherboard UUID via WMIC
        output = subprocess.check_output("wmic csproduct get uuid", shell=True, stderr=subprocess.DEVNULL).decode().split('\n')
        if len(output) > 1 and output[1].strip():
            raw_id = output[1].strip()
    except Exception:
        pass

    if not raw_id or "0000" in raw_id:
        try:
            # Fallback to Windows Machine GUID
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography", 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
            guid, _ = winreg.QueryValueEx(key, "MachineGuid")
            raw_id = str(guid)
        except Exception:
            raw_id = str(uuid.getnode())

    # Generate 8-character compact hash
    h = hashlib.sha256(raw_id.encode('utf-8')).hexdigest().upper()
    part1 = h[:4]
    part2 = h[4:8]
    return f"FB-PC-{part1}-{part2}"

def copy_machine_id_to_clipboard() -> str:
    hwid = get_machine_hardware_id()
    try:
        import pyperclip
        pyperclip.copy(hwid)
    except Exception:
        try:
            # Native Windows clip.exe fallback
            p = subprocess.Popen(['clip'], stdin=subprocess.PIPE, shell=True)
            p.communicate(input=hwid.encode('utf-8'))
        except Exception:
            pass
    return hwid
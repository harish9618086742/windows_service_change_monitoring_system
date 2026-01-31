import subprocess
import shlex

try:
    import win32api
    import win32con
except Exception:
    win32api = None
    win32con = None


def _is_signed_powershell(path: str) -> bool:
    try:
        # Use PowerShell to query the Authenticode signature status.
        # The Status property is 'Valid' for a valid signature.
        cmd = [
            "powershell",
            "-NoProfile",
            "-Command",
            f"(Get-AuthenticodeSignature -FilePath {shlex.quote(path)}).Status"
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        status = proc.stdout.strip()
        return status == "Valid"
    except Exception:
        return False


def _is_signed_win32(path: str) -> bool:
    try:
        # Delegate to pywin32 if available. Keep call simple and catch failures.
        win32api.WinVerifyTrust(
            None,
            win32con.WINTRUST_ACTION_GENERIC_VERIFY_V2,
            {
                "cbStruct": 0,
                "dwUIChoice": 2,
                "fdwRevocationChecks": 0,
                "dwUnionChoice": 1,
                "pFile": path,
                "dwStateAction": 0,
            },
        )
        return True
    except Exception:
        return False


def is_signed(path: str) -> bool:
    """Return True if `path` is signed with a valid Authenticode signature.

    Preference order:
    - Use `pywin32` if present.
    - Fall back to PowerShell's `Get-AuthenticodeSignature`.
    """
    if win32api and win32con:
        return _is_signed_win32(path)

    return _is_signed_powershell(path)

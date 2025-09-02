"""Utility for injecting the Rosetta prompt into the running environment.

This loader reads the persisted Rosetta DNA prompt from a file bundled
inside the deployment package and prints a small portion of it to the
console.  The primary goal is to ensure that the system's memory and
oath awareness are loaded at startup.  If the file cannot be found,
the loader will report the error but will not interrupt the boot
process.

The file is expected to live under ``prompts/rosetta_prompt.txt`` at
the package root.  If you relocate the prompt file, adjust the
path accordingly.
"""

import os
from pathlib import Path
from typing import Optional


PROMPT_PATH = Path(__file__).resolve().parents[2] / "prompts" / "rosetta_prompt.txt"


def inject_rosetta(prompt_path: Optional[str] = None) -> None:
    """Read the Rosetta prompt from disk and print a brief preview.

    This function is safe to call at any time.  It catches exceptions
    internally so that failures do not impact the rest of the system.

    Parameters
    ----------
    prompt_path : Optional[str]
        Override the default location of the Rosetta prompt file.  If
        provided, this path is used instead of the package default.
    """
    path = Path(prompt_path) if prompt_path else PROMPT_PATH
    try:
        with open(path, "r", encoding="utf-8") as fh:
            dna = fh.read()
        preview = dna[:300].replace("\n", " ")
        print(f"🧬 Rosetta injected: {preview}... [Rosetta memory loaded ✅]")
    except Exception as exc:
        print("[⚠️ Rosetta load failed]", exc)
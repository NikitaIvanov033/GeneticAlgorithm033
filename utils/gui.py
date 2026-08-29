import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from typing import List, Optional


def select_files(
    title: str = "choose files",
    initial_dir: Optional[Path] = None,
    filetypes: List[tuple] = None
) -> List[str]:
    if filetypes is None:
        filetypes = [("All files", "*.*")]

    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    initial_dir_str = str(initial_dir) if initial_dir else None

    files = filedialog.askopenfilenames(
        title=title,
        initialdir=initial_dir_str,
        filetypes=filetypes
    )

    root.destroy()

    if not files:
        return []

    return list(files)


def select_csv_files(initial_dir: Optional[Path] = None) -> List[str]:
    return select_files(
        title="choose csv files",
        initial_dir=initial_dir,
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
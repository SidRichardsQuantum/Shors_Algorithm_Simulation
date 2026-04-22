import os
import tempfile


def get_pyplot():
    """Import pyplot after ensuring Matplotlib has a writable cache directory."""
    os.environ.setdefault("MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "matplotlib"))

    import matplotlib.pyplot as plt

    return plt

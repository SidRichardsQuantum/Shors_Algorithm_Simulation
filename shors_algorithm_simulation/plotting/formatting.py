def ket_label(value):
    """Format a computational-basis state label."""
    return f"|{value}⟩"


def set_ket_xticks(axis, values, rotation=0, ha="center"):
    """Apply ket-formatted tick labels to an axis."""
    axis.set_xticks(values)
    axis.set_xticklabels(
        [ket_label(value) for value in values], rotation=rotation, ha=ha
    )

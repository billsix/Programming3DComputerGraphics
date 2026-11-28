"""Append Google ``Args:``/``Returns:``/``Raises:`` sections to mathutils.

Inserts each section block just above the closing quotes of the named
docstring.  Idempotent: a docstring that already contains ``Args:`` (or, for
argument-less callables, ``Returns:``) is skipped.  Run from anywhere:
``python3 tasks/adhoc/<slug>/add_google_sections.py``.
"""

import ast
import pathlib

REPO_ROOT: pathlib.Path = pathlib.Path(__file__).resolve().parents[3]
TARGET: pathlib.Path = REPO_ROOT / "src/programming3dcomputergraphics/mathutils.py"

# qualified name -> body lines (unindented); a blank line separates sections
SECTIONS: dict[str, list[str]] = {
    "rotate_around": [
        "Args:",
        "    angle_in_radians: How far to turn, counter-clockwise, in radians.",
        "    center: The point that stays fixed.",
        "",
        "Returns:",
        "    The rotation about ``center`` as an invertible function on",
        "    ``g2.Vector``.",
    ],
    "cosine": [
        "Args:",
        "    v1: The first vector, of any dimension.",
        "    v2: The second vector, of the same dimension as ``v1``.",
        "",
        "Returns:",
        "    The cosine of the angle between them, or NaN when either has zero",
        "    length.",
    ],
    "sine": [
        "Args:",
        "    v1: The vector the angle starts from.",
        "    v2: The vector the angle ends at.",
        "",
        "Returns:",
        "    The signed sine of the angle from ``v1`` to ``v2``, or NaN when",
        "    either has zero length.",
    ],
    "abs_sin": [
        "Args:",
        "    v1: The first vector.",
        "    v2: The second vector.",
        "",
        "Returns:",
        "    The unsigned sine of the angle between them.",
        "",
        "Raises:",
        "    ZeroDivisionError: If either vector has zero length.",
    ],
    "find_normal": [
        "Args:",
        "    p1: The first corner of the triangle.",
        "    p2: The second corner, counter-clockwise from ``p1``.",
        "    p3: The third corner, counter-clockwise from ``p2``.",
        "",
        "Returns:",
        "    The normal vector, not normalized; its length is twice the",
        "    triangle's area.",
    ],
    "plane_equation": [
        "Args:",
        "    p1: The first of three points on the plane.",
        "    p2: The second point, counter-clockwise from ``p1``.",
        "    p3: The third point, counter-clockwise from ``p2``.",
        "",
        "Returns:",
        "    The pair ``(normal, d)``: the unit normal and the signed offset.",
        "",
        "Raises:",
        "    ZeroDivisionError: If the three points are collinear, so no",
        "        plane is defined.",
    ],
    "distance_to_plane": [
        "Args:",
        "    point: The point to measure from.",
        "    plane: The ``(normal, d)`` pair from :func:`plane_equation`.",
        "",
        "Returns:",
        "    The signed perpendicular distance; positive on the side the normal",
        "    points toward.",
    ],
    "ortho": [
        "Args:",
        "    left: The x coordinate of the left face of the viewable prism.",
        "    right: The x coordinate of the right face.",
        "    bottom: The y coordinate of the bottom face.",
        "    top: The y coordinate of the top face.",
        "    near: The z coordinate of the near face.",
        "    far: The z coordinate of the far face.",
        "",
        "Returns:",
        "    An invertible, affine function from camera space to NDC.",
    ],
    "perspective": [
        "Args:",
        "    field_of_view: The vertical angle of the frustum, in degrees.",
        "    aspect_ratio: The frustum's width divided by its height.",
        "    near_z: The z coordinate of the near plane (negative, in front of",
        "        the camera).",
        "    far_z: The z coordinate of the far plane (negative, beyond",
        "        ``near_z``).",
        "",
        "Returns:",
        "    An invertible, non-linear function from camera space to NDC.",
    ],
    "cs_to_ndc_space_fn": [
        "Args:",
        "    vector: Not used; the result is the same for every vector.",
        "",
        "Returns:",
        "    The perspective transform with a 45 degree field of view, an",
        "    aspect ratio of 1, a near plane at -0.1 and a far plane at -1000.",
    ],
    "FunctionStack.push": [
        "Args:",
        "    o: The transformation to push.",
    ],
    "FunctionStack.pop": [
        "Returns:",
        "    The transformation that was on top.",
        "",
        "Raises:",
        "    IndexError: If the stack is empty.",
    ],
    "FunctionStack.modelspace_to_ndc_fn": [
        "Returns:",
        "    The composition of every pushed transformation; the identity for",
        "    an empty stack.",
    ],
    "push_transformation": [
        "Args:",
        "    f: The transformation to push onto the global ``fn_stack``.",
        "",
        "Yields:",
        "    The global ``fn_stack``, with ``f`` on top.",
    ],
}


def docstring_nodes(
    tree: ast.Module,
) -> dict[str, tuple[ast.AST, ast.Constant]]:
    """Map qualified names to (definition node, docstring constant)."""
    found: dict[str, tuple[ast.AST, ast.Constant]] = {}

    def visit(node: ast.AST, prefix: str) -> None:
        for child in ast.iter_child_nodes(node):
            match child:
                case ast.FunctionDef() | ast.ClassDef():
                    qualified: str = prefix + child.name
                    first: ast.stmt = child.body[0]
                    match first:
                        case ast.Expr(value=ast.Constant(value=str()) as doc):
                            found[qualified] = (child, doc)
                        case _:
                            pass
                    if isinstance(child, ast.ClassDef):
                        visit(child, qualified + ".")
                case _:
                    pass

    visit(tree, "")
    return found


def main() -> None:
    """Insert the sections, bottom-up so line numbers stay valid."""
    source: str = TARGET.read_text()
    lines: list[str] = source.split("\n")
    nodes: dict[str, tuple[ast.AST, ast.Constant]] = docstring_nodes(
        ast.parse(source)
    )
    missing: list[str] = sorted(set(SECTIONS) - set(nodes))
    assert not missing, f"no docstring for {missing}"
    changed: int = 0
    for name, (_, doc) in sorted(
        nodes.items(), key=lambda item: -item[1][1].end_lineno
    ):
        body: list[str] | None = SECTIONS.get(name)
        if body is None:
            continue
        if any(marker in str(doc.value) for marker in ("Args:", "Returns:", "Attributes:", "Yields:")):
            continue
        indent: str = " " * doc.col_offset
        closing: int = doc.end_lineno - 1  # 0-based index of the closing line
        assert lines[closing].strip() == '"""', (name, lines[closing])
        block: list[str] = [""] + [
            (indent + text) if text else "" for text in body
        ]
        lines[closing:closing] = block
        changed += 1
    TARGET.write_text("\n".join(lines))
    print(f"added sections to {changed} docstrings")


if __name__ == "__main__":
    main()

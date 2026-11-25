"""Inline the single-use locals the 2026-11-25 triage chose (rule 1), by exact text.

Each edit names a file, the old text and its replacement.  A file where the old
text is absent but the new text is present is already done, so a second run
changes nothing.  Run from anywhere:
``python3 tasks/adhoc/<slug>/apply_inlines.py``.
"""

import pathlib

REPO_ROOT: pathlib.Path = pathlib.Path(__file__).resolve().parents[3]
PKG: str = "src/intro3dgraphics/"

RY_OLD: str = """ry: float = (
            animation.timeline.arrival_time(Space.camera) + scene.step_duration
        )
        if {t} >= ry:"""
RY_NEW: str = """# ry: when the camera step ends
        if {t} >= (
            animation.timeline.arrival_time(Space.camera) + scene.step_duration
        ):"""

# (path, old text, new text, expected occurrences)
EDITS: list[tuple[str, str, str, int]] = [
    (
        PKG + "demos/demo22/demo22.py",
        """        model: np.ndarray = ms.get_current_matrix(ms.MatrixStack.model)
        mvp: np.ndarray = (
            light_proj @ light_view @ np.asarray(model, dtype=np.float32)
        )""",
        """        # model: the current model matrix, as float32
        mvp: np.ndarray = (
            light_proj
            @ light_view
            @ np.asarray(
                ms.get_current_matrix(ms.MatrixStack.model), dtype=np.float32
            )
        )""",
        1,
    ),
    (
        PKG + "demos/demo22/demo22.py",
        """    vao: int = make_vao(_interleaved_attribs(vbo))
    return vao, vbo, vertex_data.size // _FLOATS_PER_VERTEX""",
        """    # vao: the vertex array that reads the interleaved attributes from vbo
    return (
        make_vao(_interleaved_attribs(vbo)),
        vbo,
        vertex_data.size // _FLOATS_PER_VERTEX,
    )""",
        1,
    ),
    (
        PKG + "graphingcalculator/grapher3d.py",
        """    r: float = math.sqrt(x * x + y * y)
    return 2.0 * math.sin(r)""",
        """    # r: the distance from the origin
    return 2.0 * math.sin(math.sqrt(x * x + y * y))""",
        1,
    ),
    (
        PKG + "mvpvisualization/modelview.py",
        """    bright: bool = t < 5.0 or (35.0 < t < 40.0) or (50.0 < t < 55.0)
    ms.set_current_matrix(ms.MatrixStack.model, morph)
    standard_objects.draw_axis(grayed=not bright)""",
        """    ms.set_current_matrix(ms.MatrixStack.model, morph)
    # bright: the start and the two pauses
    standard_objects.draw_axis(
        grayed=not (t < 5.0 or (35.0 < t < 40.0) or (50.0 < t < 55.0))
    )""",
        1,
    ),
    (
        PKG + "mvpvisualization/modelviewperspectiveprojection.py",
        """    epi: float = PROLOGUE_DUR + DEMO_DUR
    if t >= epi:""",
        """    # epi: the time the epilogue starts
    if t >= PROLOGUE_DUR + DEMO_DUR:""",
        1,
    ),
    (
        PKG + "mvpvisualization/modelviewperspectiveprojection.py",
        """    epi: float = PROLOGUE_DUR + DEMO_DUR
    if t < epi:""",
        """    # epi: the time the epilogue starts
    if t < PROLOGUE_DUR + DEMO_DUR:""",
        1,
    ),
    (
        PKG + "mvpvisualization/modelviewperspectiveprojection.py",
        """        aspect: float = state["fb_w"] / state["fb_h"]
        imgui.menu_item("aspect = width / height", "", False, False)
        imgui.menu_item(
            f"       = {state['fb_w']} / {state['fb_h']} = {aspect:.3f}",""",
        """        imgui.menu_item("aspect = width / height", "", False, False)
        imgui.menu_item(
            f"       = {state['fb_w']} / {state['fb_h']} = "
            f"{state['fb_w'] / state['fb_h']:.3f}",""",
        1,
    ),
    (
        PKG + "mvpvisualization/modelviewperspectiveprojection.py",
        """        cam_hw: float = state["fb_w"] / 2.0
        cam_hh: float = state["fb_h"] / 2.0
        draw_grid(cam_frame @ cayleyscene.to_matrix(_warp(cam_hw, cam_hh)))""",
        """        # cam_hw, cam_hh: half the framebuffer's width and height
        draw_grid(
            cam_frame
            @ cayleyscene.to_matrix(
                _warp(state["fb_w"] / 2.0, state["fb_h"] / 2.0)
            )
        )""",
        1,
    ),
    (
        PKG + "mvpvisualization/modelviewperspectiveprojection.py",
        "        " + RY_OLD.format(t="demo_t"),
        "        " + RY_NEW.format(t="demo_t"),
        1,
    ),
    (
        PKG + "mvpvisualization/modelvieworthoprojection.py",
        "        " + RY_OLD.format(t="t"),
        "        " + RY_NEW.format(t="t"),
        1,
    ),
    (
        PKG + "notebooksrc/sampling.py",
        """    unused: int = int((hits == 0).sum())
    print(
        f"texels never chosen: {unused}; most pixels on one texel: {hits.max()}"
    )""",
        """    print(
        f"texels never chosen: {int((hits == 0).sum())}; "
        f"most pixels on one texel: {hits.max()}"
    )""",
        1,
    ),
    (
        PKG + "util/nbplotutils.py",
        """    labels: list[str] = ["(-1,-1)", "(1,-1)", "(1,1)", "(-1,1)"]
    for i, label in enumerate(labels):""",
        """    # the four corners, in drawing order
    for i, label in enumerate(["(-1,-1)", "(1,-1)", "(1,1)", "(-1,1)"]):""",
        1,
    ),
    (
        PKG + "wxapp.py",
        """            error: str = GL.glGetShaderInfoLog(shader).decode()
            raise RuntimeError(f"Shader compile error: {error}")""",
        """            raise RuntimeError(
                f"Shader compile error: "
                f"{GL.glGetShaderInfoLog(shader).decode()}"
            )""",
        1,
    ),
    (
        PKG + "wxapp.py",
        """            error: str = GL.glGetProgramInfoLog(self.program).decode()
            raise RuntimeError(f"Program link error: {error}")""",
        """            raise RuntimeError(
                f"Program link error: "
                f"{GL.glGetProgramInfoLog(self.program).decode()}"
            )""",
        1,
    ),
    (
        PKG + "wxapp.py",
        """        angle_loc: int = GL.glGetUniformLocation(self.program, "angle")
        GL.glUniform1f(angle_loc, self.angle)""",
        """        # angle_loc: where the shader's ``angle`` uniform lives
        GL.glUniform1f(
            GL.glGetUniformLocation(self.program, "angle"), self.angle
        )""",
        1,
    ),
]

# demo22b carries the same model/mvp and vao blocks as demo22
EDITS += [(PKG + "demos/demo22b/demo22b.py", old, new, count) for _, old, new, count in EDITS[:2]]

# Second batch: single-use locals declared well above their use.
SET_UNIFORMS: list[tuple[str, str, int]] = [
    (
        """    mvp_loc: int = block_shadow.u_mvp if _using_shadow_map else main.u_mvp
    model_loc: int = block_shadow.u_model if _using_shadow_map else main.u_model

    model: np.ndarray = ms.get_current_matrix(ms.MatrixStack.model)
    GL.glUniformMatrix4fv(
        mvp_loc,
""",
        """    model: np.ndarray = ms.get_current_matrix(ms.MatrixStack.model)
    GL.glUniformMatrix4fv(
        # mvp_loc: the model-view-projection uniform of the active program
        block_shadow.u_mvp if _using_shadow_map else main.u_mvp,
""",
        1,
    ),
    (
        """    GL.glUniformMatrix4fv(
        model_loc,
""",
        """    GL.glUniformMatrix4fv(
        # model_loc: the model uniform of the active program
        block_shadow.u_model if _using_shadow_map else main.u_model,
""",
        1,
    ),
    (
        """        sm: np.ndarray = _shadow_pv_scaled @ np.asarray(model, dtype=np.float32)
        GL.glUniformMatrix4fv(
            block_shadow.u_shadow,
            1,
            GL.GL_TRUE,
            np.ascontiguousarray(sm, dtype=np.float32),""",
        """        GL.glUniformMatrix4fv(
            block_shadow.u_shadow,
            1,
            GL.GL_TRUE,
            # sm: the shadow matrix times the model matrix
            np.ascontiguousarray(
                _shadow_pv_scaled @ np.asarray(model, dtype=np.float32),
                dtype=np.float32,
            ),""",
        1,
    ),
]
EDITS += [
    (PKG + demo, old, new, count)
    for demo in ("demos/demo22/demo22.py", "demos/demo22b/demo22b.py")
    for old, new, count in SET_UNIFORMS
]
EDITS += [
    (
        PKG + "demos/demo19e.py",
        """    step: float = 1.0
    y: float = -0.4""",
        """    y: float = -0.4""",
        1,
    ),
    (
        PKG + "demos/demo19e.py",
        "        line += step\n",
        "        line += 1.0  # step: one grid unit\n",
        1,
    ),
    (
        PKG + "demos/demo21/demo21.py",
        """    window_name: str = "Introduction to 3D Computer Graphics Demo 21 "
""",
        "",
        1,
    ),
    (
        PKG + "demos/demo21/demo21.py",
        "        int(width), int(height), window_name, None, None\n",
        """        int(width),
        int(height),
        # window_name: the title bar text
        "Introduction to 3D Computer Graphics Demo 21 ",
        None,
        None,
""",
        1,
    ),
    (
        PKG + "demos/demo24/demo24.py",
        """    fmt: GLenum = GL.GL_RGB if channels == 3 else GL.GL_RGBA
    internal: GLenum = GL.GL_RGB8 if channels == 3 else GL.GL_RGBA8
    GL.glTexImage2D(
        GL.GL_TEXTURE_2D,
        0,
        internal,
        w,
        h,
        0,
        fmt,""",
        """    GL.glTexImage2D(
        GL.GL_TEXTURE_2D,
        0,
        # internal: the format the GPU stores (RGB8 or RGBA8)
        GL.GL_RGB8 if channels == 3 else GL.GL_RGBA8,
        w,
        h,
        0,
        # fmt: the format of the pixels given here (RGB or RGBA)
        GL.GL_RGB if channels == 3 else GL.GL_RGBA,""",
        1,
    ),
    (
        PKG + "mvpvisualization/modelview2d.py",
        """    lw: float = state["line_width"]
""",
        "",
        1,
    ),
    (
        PKG + "mvpvisualization/modelview2d.py",
        "        standard_objects.draw_rect_prism(t, lw, w, h)",
        '        standard_objects.draw_rect_prism(t, state["line_width"], w, h)',
        1,
    ),
]


def main() -> None:
    path: str
    old: str
    new: str
    count: int
    for path, old, new, count in EDITS:
        file: pathlib.Path = REPO_ROOT / path
        text: str = file.read_text()
        found: int = text.count(old)
        if found == count:
            file.write_text(text.replace(old, new))
            print(f"applied   {path}")
        elif found == 0 and new in text:
            print(f"already   {path}")
        else:
            raise SystemExit(f"{path}: expected {count} match(es), found {found}")


if __name__ == "__main__":
    main()

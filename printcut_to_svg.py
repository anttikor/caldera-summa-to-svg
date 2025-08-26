# printcut_to_svg.py
# Module for converting Caldera/Summa "Print and Cut Job File v1.0" to SVG
# Scale correction: inches to millimeters (1 inch = 25.4 mm)
# Registration marks are drawn as rectangles as in the original

import re
import svgwrite
from pathlib import Path

def convert_jobfile_to_svg(input_file, output_file, scale=25.4, path_color="black", rect_color="blue", trim_color="red"):
    """
    Convert a Print and Cut Job File to SVG

    Args:
        input_file (str): Path to input job file
        output_file (str): Path to output SVG file
        scale (float): Scale factor (default 25.4 for inches to mm)
        path_color (str): Color for paths (default "black")
        rect_color (str): Color for registration rectangles (default "blue")
        trim_color (str): Color for trim box elements (default "red")
    """

    # --- pientä apua ---
    num = r"[-+]?\d*\.\d+|[-+]?\d+"  # float tai int
    pair_re = re.compile(fr"\(({num})\s+({num})\)")

    # --- keräillään polut ---
    paths = []  # lista: {d:str, color:str} OUTLINE-poluille
    rects = []  # lista: {x:float, y:float, w:float, h:float, color:str} kohdistusmerkeille
    current_color = "black"  # QOLOR-lohkosta, esim. "Cut", "PDFTrimBox" jne.

    inside_outline = False
    path_cmds = []
    start_point = None
    close_pending = False

    # MAYER-käsittely
    inside_mayer = False
    clip_coords = None
    mayer_color = rect_color  # Käytä annettua väriä

    # globaali bbox viewBoxia varten
    minx = miny = float("inf")
    maxx = maxy = float("-inf")

    def upd_bbox(x, y):
        nonlocal minx, miny, maxx, maxy
        x_mm = x * scale
        y_mm = y * scale
        minx = min(minx, x_mm)
        miny = min(miny, y_mm)
        maxx = max(maxx, x_mm)
        maxy = max(maxy, y_mm)

    def upd_bbox_rect(x, y, w, h):
        nonlocal minx, miny, maxx, maxy
        x_mm = x * scale
        y_mm = y * scale
        w_mm = w * scale
        h_mm = h * scale
        minx = min(minx, x_mm)
        miny = min(miny, y_mm)
        maxx = max(maxx, x_mm + w_mm)
        maxy = max(maxy, y_mm + h_mm)

    try:
        with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
            for raw in f:
                line = raw.strip()
                if not line:
                    continue

                # Väri/ryhmä (QOLOR)
                if line.startswith("QOLOR="):
                    name = line.split("=", 1)[1].split(":", 1)[0].strip()
                    current_color = name or "black"
                    if inside_mayer:
                        mayer_color = current_color
                    continue

                # MAYER alkaa
                if line == "BEGIN_MAYER":
                    inside_mayer = True
                    clip_coords = None
                    continue

                # MAYER päättyy
                if line == "END_MAYER":
                    if clip_coords and inside_mayer:
                        x1, y1, x2, y2 = clip_coords
                        x = min(x1, x2)
                        y = min(y1, y2)
                        w = abs(x2 - x1)
                        h = abs(y2 - y1)
                        if w > 0 and h > 0:  # Vältä tyhjiä
                            rects.append({"x": x, "y": y, "w": w, "h": h, "color": mayer_color})
                            upd_bbox_rect(x, y, w, h)
                    inside_mayer = False
                    clip_coords = None
                    mayer_color = rect_color
                    continue

                if inside_mayer:
                    if line.startswith("CLIP="):
                        parts = re.findall(num, line)
                        if len(parts) >= 4:
                            clip_coords = [float(p) for p in parts[:4]]
                        continue

                # OUTLINE alkaa
                if line == "OUTLINE":
                    inside_outline = True
                    path_cmds = []
                    start_point = None
                    close_pending = False
                    continue

                # Sulkemismerkintä
                if line.startswith("CLOSURE"):
                    if "CLOSED" in line:
                        close_pending = True
                    continue

                # OUTLINE päättyy
                if line == "END OUTLINE":
                    if path_cmds:
                        d = " ".join(path_cmds)
                        if close_pending:
                            d += " Z"
                        paths.append({"d": d, "color": current_color})
                    inside_outline = False
                    path_cmds = []
                    start_point = None
                    close_pending = False
                    continue

                if not inside_outline:
                    continue

                # SEGMENT (x1 y1) (x2 y2)
                if line.startswith("SEGMENT"):
                    pts = pair_re.findall(line)
                    if len(pts) >= 2:
                        (x1, y1), (x2, y2) = [(float(a) * scale, float(b) * scale) for a, b in pts[:2]]
                        path_cmds.append(f"M {x1:.6f},{y1:.6f}")
                        path_cmds.append(f"L {x2:.6f},{y2:.6f}")
                        upd_bbox(x1 / scale, y1 / scale)
                        upd_bbox(x2 / scale, y2 / scale)
                    continue

                # BEZIER (x1 y1) (x2 y2) Q0 = (cx1 cy1) Q1 = (cx2 cy2)
                if line.startswith("BEZIER"):
                    pts = pair_re.findall(line)
                    if len(pts) >= 4:
                        (x1, y1), (x2, y2), (c1x, c1y), (c2x, c2y) = [
                            (float(a) * scale, float(b) * scale) for a, b in (pts[0], pts[1], pts[2], pts[3])
                        ]
                        path_cmds.append(f"M {x1:.6f},{y1:.6f}")
                        path_cmds.append(f"C {c1x:.6f},{c1y:.6f} {c2x:.6f},{c2y:.6f} {x2:.6f},{y2:.6f}")
                        upd_bbox(x1 / scale, y1 / scale)
                        upd_bbox(x2 / scale, y2 / scale)
                        upd_bbox(c1x / scale, c1y / scale)
                        upd_bbox(c2x / scale, c2y / scale)
                    continue

    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found: {input_file}")
    except Exception as e:
        raise Exception(f"Error processing input file: {str(e)}")

    # --- tee SVG ---
    dw = max(1.0, maxx - minx)
    dh = max(1.0, maxy - miny)
    svg = svgwrite.Drawing(output_file, size=(f"{dw}mm", f"{dh}mm"))
    svg.viewbox(minx, miny, dw, dh)

    # Piirrä polut
    for item in paths:
        color = trim_color if item["color"].lower().startswith("pdftrimbox") else path_color
        svg.add(svg.path(d=item["d"], fill="none", stroke=color, stroke_width=0.2))

    # Piirrä kohdistusmerkit (suorakaiteina)
    for item in rects:
        color = trim_color if item["color"].lower().startswith("pdftrimbox") else rect_color
        svg.add(svg.rect(insert=(item["x"] * scale, item["y"] * scale),
                         size=(item["w"] * scale, item["h"] * scale),
                         fill="none", stroke=color, stroke_width=0.1))

    svg.save()
    return f"SVG saved: {Path(output_file).resolve()}"
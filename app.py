import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
from io import StringIO
import svgwrite

# --- Funcoes de desenho matplotlib ---
def draw_preview_base(ax, width, height, depth, thickness):
    ax.clear()
    ax.set_aspect('equal')
    ax.axis('off')

    W = width * 10
    H = height * 10
    D = depth * 10
    T = thickness
    D2 = D / 2
    ax.clear()
    ax.set_aspect('equal')
    ax.axis('off')

    W = width * 10
    H = height * 10
    D = depth * 10
    T = thickness
    D2 = D / 2

    x0, y0 = 0, 0
    x1, y1 = x0 + W, y0 + H
    xL = x0 - D
    xb = x1 + D

    ax.plot([x0, x0 - T, x0 - T, x0, x0, x1, x1, x1 + T, x1 + T, x1],
            [y1, y1, y1 + D2, y1 + D2, y1 + D, y1 + D, y1 + D2, y1 + D2, y1, y1], 'black')
    ax.plot([x0, x0 - T, x0 - T, x0, x0, x1, x1, x1 + T, x1 + T, x1],
            [y0, y0, y0 - D2, y0 - D2, y0 - D, y0 - D, y0 - D2, y0 - D2, y0, y0], 'black')
    ax.plot([x0, x0 - D2, x0 - D2, xL, xL, x0 - D2, x0 - D2, x0],
            [y0, y0, y0 - T, y0 - T, y1 + T, y1 + T, y1, y1], 'black')
    ax.plot([x1, xb - D2, xb - D2, xb, xb, xb - D2, xb - D2, x1],
            [y0, y0, y0 - T, y0 - T, y1 + T, y1 + T, y1, y1], 'black')

    ax.plot([x0, x1, x1, x0, x0], [y0, y0, y1, y1, y0], 'red')
    ax.text((x0 + x1) / 2, y0 + 5, f"{W/10:.1f} cm", ha='center', fontsize=8)
    ax.text(x1 - 20, (y0 + y1) / 2, f"{H/10:.1f} cm", rotation=90, va='center', fontsize=8)

    largura_total = W + 2 * D
    x_ext_esq = xL
    x_ext_dir = xb
    y_ref = y0 - D - 25
    ax.plot([x_ext_esq, x_ext_dir], [y_ref, y_ref], color='blue', linewidth=1)
    ax.plot([x_ext_esq, x_ext_esq], [y_ref - 5, y_ref + 5], color='blue')
    ax.plot([x_ext_dir, x_ext_dir], [y_ref - 5, y_ref + 5], color='blue')
    ax.text((x_ext_esq + x_ext_dir) / 2, y_ref - 2, f"{largura_total/10:.1f} cm", color='blue', fontsize=8, ha='center', va='top')

    altura_total = H + 2 * D
    y_ext_sup = y1 + D
    y_ext_inf = y0 - D
    x_ref = xb + 20
    ax.plot([x_ref, x_ref], [y_ext_inf, y_ext_sup], color='blue', linewidth=1)
    ax.plot([x_ref - 5, x_ref + 5], [y_ext_inf, y_ext_inf], color='blue')
    ax.plot([x_ref - 5, x_ref + 5], [y_ext_sup, y_ext_sup], color='blue')
    ax.text(x_ref + 5, (y_ext_inf + y_ext_sup) / 2, f"{altura_total/10:.1f} cm", ha='left', va='center', fontsize=8, color='blue', rotation=90)
    ax.text((x0 + x1) / 2, y0 + 5, f"{W/10:.1f} cm", ha='center', fontsize=8)

def draw_preview_top(ax, width, height, depth, thickness, folga=None):
    ax.clear()
    ax.set_aspect('equal')
    ax.axis('off')

    if folga is None:
        if thickness in (1.90, 2.00):
            folga = 7.0
        elif thickness == 2.50:
            folga = 8.0
        else:
            folga = thickness * 3

    W = (width * 10) + folga
    H = (height * 10) + folga
    D = depth * 10
    T = thickness
    D2 = D / 2

    x0, y0 = 0, 0
    x1, y1 = x0 + W, y0 + H
    xL = x0 - D
    xb = x1 + D

    ax.plot([x0, x0 - T, x0 - T, x0, x0, x1, x1, x1 + T, x1 + T, x1],
            [y1, y1, y1 + D2, y1 + D2, y1 + D, y1 + D, y1 + D2, y1 + D2, y1, y1], 'black')
    ax.plot([x0, x0 - T, x0 - T, x0, x0, x1, x1, x1 + T, x1 + T, x1],
            [y0, y0, y0 - D2, y0 - D2, y0 - D, y0 - D, y0 - D2, y0 - D2, y0, y0], 'black')
    ax.plot([x0, x0 - D2, x0 - D2, xL, xL, x0 - D2, x0 - D2, x0],
            [y0, y0, y0 - T, y0 - T, y1 + T, y1 + T, y1, y1], 'black')
    ax.plot([x1, xb - D2, xb - D2, xb, xb, xb - D2, xb - D2, x1],
            [y0, y0, y0 - T, y0 - T, y1 + T, y1 + T, y1, y1], 'black')

    ax.plot([x0, x1, x1, x0, x0], [y0, y0, y1, y1, y0], 'red')
    ax.text((x0 + x1) / 2, y0 + 5, f"{W/10:.1f} cm", ha='center', fontsize=8)
    ax.text(x1 - 20, (y0 + y1) / 2, f"{H/10:.1f} cm", rotation=90, va='center', fontsize=8)

    largura_total = W + 2 * D
    x_ext_esq = xL
    x_ext_dir = xb
    y_ref = y0 - D - 25
    ax.plot([x_ext_esq, x_ext_dir], [y_ref, y_ref], color='blue', linewidth=1)
    ax.plot([x_ext_esq, x_ext_esq], [y_ref - 5, y_ref + 5], color='blue')
    ax.plot([x_ext_dir, x_ext_dir], [y_ref - 5, y_ref + 5], color='blue')
    ax.text((x_ext_esq + x_ext_dir) / 2, y_ref - 2, f"{largura_total/10:.1f} cm", color='blue', fontsize=8, ha='center', va='top')

    altura_total = H + 2 * D
    y_ext_sup = y1 + D
    y_ext_inf = y0 - D
    x_ref = xb + 20
    ax.plot([x_ref, x_ref], [y_ext_inf, y_ext_sup], color='blue', linewidth=1)
    ax.plot([x_ref - 5, x_ref + 5], [y_ext_inf, y_ext_inf], color='blue')
    ax.plot([x_ref - 5, x_ref + 5], [y_ext_sup, y_ext_sup], color='blue')
    ax.text(x_ref + 5, (y_ext_inf + y_ext_sup) / 2, f"{altura_total/10:.1f} cm", ha='left', va='center', fontsize=8, color='blue', rotation=90)

# --- Função para exportar SVG ---
def export_to_svg_string(width, height, depth_base, depth_top, thickness, folga=None):
    W = width * 10
    H = height * 10
    D1 = depth_base * 10
    D2 = depth_top * 10
    T = thickness

    if folga is None:
        folga = 7.0 if thickness in (1.90, 2.00) else 8.0 if thickness == 2.50 else thickness * 3

    WT = W + folga
    HT = H + folga
    margin = 5
    total_height = (H + 2 * D1 + 2 * T) + (HT + 2 * D2 + 2 * T) + margin
    total_width = max(W + 2 * D1 + 2 * T, WT + 2 * D2 + 2 * T)

    dwg = svgwrite.Drawing(filename=None, profile='full',
        size=(f"{total_width}mm", f"{total_height}mm"),
        viewBox=f"0 0 {total_width} {total_height}")

    def add_vinco(x0, y0, x1, y1):
        dwg.add(dwg.polyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], stroke="red", fill="none", stroke_width='0.1'))

    def draw_base(x_offset, y_offset):
        x0, y0 = x_offset + T + D1, y_offset + T + D1
        x1, y1 = x0 + W, y0 + H
        xL = x0 - D1
        D = D1
        D2_local = D / 2
        xb = x1 + D
        add_vinco(x0, y0, x1, y1)
        path = dwg.path(stroke="black", fill="none", stroke_width='0.1')
        path.push("M", x0, y1)
        path.push("L", x0 - T, y1, x0 - T, y1 + D2_local, x0, y1 + D2_local, x0, y1 + D,
                  x1, y1 + D, x1, y1 + D2_local, x1 + T, y1 + D2_local, x1 + T, y1, x1, y1)
        dwg.add(path)

    def draw_top(x_offset, y_offset):
        x0, y0 = x_offset + T + D2, y_offset + T + D2
        x1, y1 = x0 + WT, y0 + HT
        xL = x0 - D2
        D = D2
        D2_local = D / 2
        xb = x1 + D
        add_vinco(x0, y0, x1, y1)
        path = dwg.path(stroke="black", fill="none", stroke_width='0.1')
        path.push("M", x0, y1)
        path.push("L", x0 - T, y1, x0 - T, y1 + D2_local, x0, y1 + D2_local, x0, y1 + D,
                  x1, y1 + D, x1, y1 + D2_local, x1 + T, y1 + D2_local, x1 + T, y1, x1, y1)
        dwg.add(path)

    draw_top(0, 0)
    draw_base(0, HT + 2 * D2 + 2 * T + margin)
    svg_io = StringIO()
    dwg.write(svg_io)
    return svg_io.getvalue()

# --- Streamlit App ---
st.set_page_config(page_title="Touché | Caixa de tampa solta", layout="wide")
st.title("Touché | Caixa de tampa solta")

col1, col2 = st.columns([1, 2])
with col1:
    usar_folga_personalizada = st.checkbox("Usar folga personalizada?")
    folga = st.number_input("Folga (mm)", min_value=0.0, value=6.0, step=0.1, disabled=not usar_folga_personalizada)
    profundidade_tampa = st.slider("Profundidade da Tampa (cm)", 0.0, 10.0, 2.0)
    largura = st.slider("Largura (cm)", 0.0, 30.0, 20.0)
    comprimento = st.slider("Comprimento (cm)", 0.0, 30.0, 15.0)
    profundidade_caixa = st.slider("Profundidade da Caixa (cm)", 0.0, 30.0, 8.0)
    espessura = st.radio("Espessura (mm)", [1.50, 1.90, 2.00, 2.55], index=1)

    if st.button("Exportar SVG"):
        svg_data = export_to_svg_string(
            largura, comprimento, profundidade_caixa,
            profundidade_tampa, espessura,
            folga if usar_folga_personalizada else None
        )
        st.success("SVG exportado com sucesso!")
        st.download_button("Baixar SVG", svg_data, file_name="tampa-solta.svg", mime="image/svg+xml")

with col2:
    st.subheader("Pré-visualização")
    fig, (ax_top, ax_base) = plt.subplots(2, 1, figsize=(3, 5), dpi=60)
    draw_preview_top(ax_top, largura, comprimento, profundidade_tampa, espessura, folga if usar_folga_personalizada else None)
    draw_preview_base(ax_base, largura, comprimento, profundidade_caixa, espessura)
    st.pyplot(fig, use_container_width=False)

import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
from io import StringIO
import svgwrite
from svgwrite import Drawing

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
    ax.text(x1 - 22, (y0 + y1) / 2, f"{H/10:.1f} cm", rotation=90, va='center', fontsize=8)

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

    #if W > 100 or H > 100:
    #    folga = 7
    #else:
    #    folga = 6

    if folga is None:
        if thickness in (1.90, 2.00):
            folga = 7.0
        elif thickness == 2.50:
            folga = 8.0
        else:
            folga = thickness * 3

    WT = W + folga
    HT = H + folga

    margin = 5

    total_height = (H + 2 * D1 + 2 * T) + (HT + 2 * D2 + 2 * T) + margin
    total_width = max(W + 2 * D1 + 2 * T, WT + 2 * D2 + 2 * T)

    dwg = svgwrite.Drawing(
        'file',
        profile='full',
        size=(f"{total_width}mm", f"{total_height}mm"),
        viewBox=f"0 0 {total_width} {total_height}"
    )

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

        path.push("M", x0, y0)
        path.push("L", x0 - T, y0, x0 - T, y0 - D2_local, x0, y0 - D2_local, x0, y0 - D,
                  x1, y0 - D, x1, y0 - D2_local, x1 + T, y0 - D2_local, x1 + T, y0, x1, y0)

        path.push("M", x0, y0)
        path.push("L", x0 - D2_local, y0, x0 - D2_local, y0 - T, xL, y0 - T,
                  xL, y1 + T, x0 - D2_local, y1 + T, x0 - D2_local, y1, x0, y1)

        path.push("M", x1, y0)
        path.push("L", xb - D2_local, y0, xb - D2_local, y0 - T, xb, y0 - T,
                  xb, y1 + T, xb - D2_local, y1 + T, xb - D2_local, y1, x1, y1)

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

        path.push("M", x0, y0)
        path.push("L", x0 - T, y0, x0 - T, y0 - D2_local, x0, y0 - D2_local, x0, y0 - D,
                  x1, y0 - D, x1, y0 - D2_local, x1 + T, y0 - D2_local, x1 + T, y0, x1, y0)

        path.push("M", x0, y0)
        path.push("L", x0 - D2_local, y0, x0 - D2_local, y0 - T, xL, y0 - T,
                  xL, y1 + T, x0 - D2_local, y1 + T, x0 - D2_local, y1, x0, y1)

        path.push("M", x1, y0)
        path.push("L", xb - D2_local, y0, xb - D2_local, y0 - T, xb, y0 - T,
                  xb, y1 + T, xb - D2_local, y1 + T, xb - D2_local, y1, x1, y1)

        dwg.add(path)

    draw_top(0, 0)
    draw_base(0, HT + 2 * D2 + 2 * T + margin)
    svg_io = StringIO()
    dwg.write(svg_io)
    return svg_io.getvalue()

st.set_page_config(page_title="Touché (TPSLT)", layout="wide")
st.title("Touché | Caixa de tampa solta v-0.1.0w")

col1, col2 = st.columns([1, 2])
with col1:
    usar_folga_personalizada = st.checkbox("Usar folga personalizada?")
    folga = st.number_input("Folga (mm)", min_value=0, value=7, step=1, disabled=not usar_folga_personalizada)
    st.session_state.profundidade_tampa = st.number_input("Profundidade da Tampa (cm)", min_value=0.0, value=5.0, step=0.1)
    st.session_state.largura = st.number_input("Largura (cm)", min_value=0.0, value=20.0, step=0.1)
    st.session_state.comprimento = st.number_input("Comprimento (cm)", min_value=0.0, value=15.0, step=0.1)
    st.session_state.profundidade_caixa = st.number_input("Profundidade da caixa (cm)", min_value=0.0, value=6.0, step=0.1)
    st.session_state.espessura = st.radio("Espessura (mm)", [1.50, 1.90, 2.00, 2.5], index=1)

    svg_data = export_to_svg_string(
        st.session_state.largura, st.session_state.comprimento, st.session_state.profundidade_caixa,
        st.session_state.profundidade_tampa, st.session_state.espessura,
        folga if usar_folga_personalizada else None
    )
    st.download_button(
        label="Baixar SVG",
        data=svg_data,
        file_name="tampa-solta.svg",
        mime="image/svg+xml"
    )

with col2:
    st.subheader("Pré-visualização")
    fig, (ax_top, ax_base) = plt.subplots(2, 1, figsize=(3, 5), dpi=60)
    draw_preview_top(ax_top, st.session_state.largura, st.session_state.comprimento, st.session_state.profundidade_tampa, st.session_state.espessura, folga if usar_folga_personalizada else None)
    draw_preview_base(ax_base, st.session_state.largura, st.session_state.comprimento, st.session_state.profundidade_caixa, st.session_state.espessura)
    st.pyplot(fig, use_container_width=False)

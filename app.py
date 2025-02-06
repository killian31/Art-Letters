import io

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from shapely.geometry import LineString
from shapely.ops import polygonize, unary_union
from streamlit_plotly_events import plotly_events

from letters import LETTERS


def polygons_for_text(text):
    """Return list of polygons from Shapely given text."""
    all_segments = []
    for ch in text:
        if ch in LETTERS:
            all_segments.extend(LETTERS[ch])
    lines = [LineString(seg) for seg in all_segments]
    merged = unary_union(lines)
    return list(polygonize(merged))


def main():
    st.title("Generate Art with Letters")
    st.markdown(
        """
        This app lets you draw art using letters. 

        Enter some letters, choose the color and style of the edges, and see the art emerge!

        Click on a polygon to change its color or use random generated colors.
        """
    )

    text = st.text_input("Enter letters:", "ABC").upper()
    line_color = st.color_picker("Edges color", "#ffffff")
    linewidth = st.slider("Edges width", 1, 20, 5)
    curve_lines = st.checkbox("Curve lines", value=True)
    shape = "spline" if curve_lines else "linear"
    curving_strength = st.slider("Curving strength", 0.1, 1.3, 1.0)

    polygons = polygons_for_text(text)

    if "colors" not in st.session_state or len(st.session_state.colors) != len(
        polygons
    ):
        st.session_state.colors = [tuple(np.random.rand(3)) for _ in polygons]

    fig = go.Figure()

    fig.update_yaxes(scaleanchor="x", scaleratio=1)

    all_x = []
    all_y = []

    for i, poly in enumerate(polygons):
        x_coords, y_coords = poly.exterior.xy
        all_x.extend(x_coords)
        all_y.extend(y_coords)
        x, y = poly.exterior.xy
        r, g, b = st.session_state.colors[i]
        color_str = f"rgb({255*r}, {255*g}, {255*b})"

        fig.add_trace(
            go.Scatter(
                x=list(x),
                y=list(y),
                fill="toself",
                fillcolor=color_str,
                line=dict(
                    color=line_color,
                    width=linewidth,
                    shape=shape,
                    smoothing=curving_strength,
                ),
                name=f"Polygon_{i}",
                hoverinfo="name",
                mode="lines",
                hoveron="fills",
            )
        )
    fig.update_layout(
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    if all_y:
        y_min = min(all_y)
        y_max = max(all_y)
        y_range = y_max - y_min
        padding = 0.2 * y_range

        fig.update_yaxes(range=[y_min - padding, y_max + padding])

    clicked_points = plotly_events(fig, click_event=True, hover_event=False)

    if clicked_points:
        curve_num = clicked_points[0]["curveNumber"]
        st.write(f"You clicked polygon index = {curve_num}")

        new_color = st.color_picker("Pick a new color", "#000000")
        if st.button("Apply color to polygon"):
            r = int(new_color[1:3], 16) / 255
            g = int(new_color[3:5], 16) / 255
            b = int(new_color[5:7], 16) / 255

            st.session_state.colors[curve_num] = (r, g, b)
            st.rerun()

    if st.button("Random Recolor"):
        st.session_state.colors = [tuple(np.random.rand(3)) for _ in polygons]
        st.rerun()

    width = st.number_input("Width", value=1024)
    height = st.number_input("Height", value=1024)

    if st.button("Convert to PNG for Download"):
        buf = io.BytesIO()
        fig.write_image(buf, format="png", width=width, height=height)
        st.download_button(
            label="Download Image",
            data=buf.getvalue(),
            file_name=f"letters.png",
            mime="image/png",
        )


if __name__ == "__main__":
    main()

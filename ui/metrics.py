import streamlit as st

def inject_metric_styles():
    st.markdown(
        """
        <style>
        .metric-box {
            text-align: center;
        }
        .metric-label {
            font-size: 5rem; !important /* similar to st.header */
            font-weight: 600;
            color: var(--text-color);
        }
        .metric-value {
            font-weight: 700;
            line-height: 1;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def colored_metric(label, value, color):
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">{label}</div>
            <h1 class="metric-value" style="color:{color}">
                {value}
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

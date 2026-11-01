import cv2
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

import utlis

# ---------------------------------------------------------------- config
SCALE = 2          # warp scale
A4_MIN_AREA = 50000
OBJ_MIN_AREA = 2000

# ---------------------------------------------------------------- page setup
st.set_page_config(page_title="Object Measurement", page_icon="📏", layout="wide")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); }
.hero {
    padding: 1.8rem 2rem; border-radius: 20px; margin-bottom: 1.2rem;
    background: linear-gradient(90deg, #6366f1, #ec4899);
    box-shadow: 0 10px 30px rgba(99,102,241,.35);
}
.hero h1 { color: #fff; margin: 0; font-size: 2.2rem; }
.hero p  { color: #ffe4f1; margin: .3rem 0 0 0; font-size: 1.05rem; }
.card {
    background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.12);
    border-radius: 16px; padding: 1rem 1.2rem; text-align: center;
}
.card h3 { margin: 0; color: #a5b4fc; font-size: .95rem; font-weight: 500; }
.card h2 { margin: .2rem 0 0 0; color: #fff; font-size: 2rem; }
.imgtitle { color: #c7d2fe; font-weight: 600; margin-bottom: .4rem; }
</style>
<div class="hero">
  <h1>📏 Object Measurement</h1>
  <p>Upload a photo with objects placed on an A4 sheet — get their width &amp; height in centimetres.</p>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------- core logic
def measure(img_bgr):
    """Returns (annotated_a4_view, a4_outline_on_original, [(w_cm, h_cm), ...])"""
    wP, hP = 210 * SCALE, 297 * SCALE
    img_outline, conts = utlis.getContours(img_bgr.copy(), minArea=A4_MIN_AREA, filter=4, draw=True)
    if len(conts) == 0:
        return None, img_outline, []

    biggest = conts[0][2]
    img_warp = utlis.warpImg(img_bgr, biggest, wP, hP)
    img_c2, conts2 = utlis.getContours(img_warp, minArea=OBJ_MIN_AREA, filter=4,
                                       cThr=[50, 50], draw=False)
    results = []
    for obj in conts2:
        cv2.polylines(img_c2, [obj[2]], True, (0, 255, 0), 2)
        p = utlis.reorder(obj[2])
        nW = round(utlis.findDis(p[0][0] // SCALE, p[1][0] // SCALE) / 10, 1)
        nH = round(utlis.findDis(p[0][0] // SCALE, p[2][0] // SCALE) / 10, 1)
        cv2.arrowedLine(img_c2, tuple(p[0][0]), tuple(p[1][0]), (255, 0, 255), 3, 8, 0, 0.05)
        cv2.arrowedLine(img_c2, tuple(p[0][0]), tuple(p[2][0]), (255, 0, 255), 3, 8, 0, 0.05)
        x, y, w, h = obj[3]
        cv2.putText(img_c2, f"{nW}cm", (x + 30, y - 10),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (255, 0, 255), 2)
        cv2.putText(img_c2, f"{nH}cm", (x - 70, y + h // 2),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (255, 0, 255), 2)
        results.append((nW, nH))
    return img_c2, img_outline, results


def bgr2rgb(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def stat_cards(n_objects, a4_found):
    c1, c2 = st.columns(2)
    c1.markdown(f'<div class="card"><h3>Objects detected</h3><h2>{n_objects}</h2></div>',
                unsafe_allow_html=True)
    c2.markdown(f'<div class="card"><h3>A4 sheet</h3><h2>{"✅ Found" if a4_found else "❌ Not found"}</h2></div>',
                unsafe_allow_html=True)


# ---------------------------------------------------------------- UI
file = st.file_uploader("Upload an image with an A4 sheet", type=["jpg", "jpeg", "png"])

if file:
    img = cv2.cvtColor(np.array(Image.open(file).convert("RGB")), cv2.COLOR_RGB2BGR)
    with st.spinner("Measuring..."):
        result, outline, objs = measure(img)

    stat_cards(len(objs), result is not None)
    st.write("")

    left, right = st.columns(2)
    with left:
        st.markdown('<div class="imgtitle">Original image</div>', unsafe_allow_html=True)
        st.image(bgr2rgb(img), use_container_width=True)
    with right:
        st.markdown('<div class="imgtitle">Measurement result</div>', unsafe_allow_html=True)
        if result is not None:
            st.image(bgr2rgb(result), use_container_width=True)
        else:
            st.error("A4 sheet not detected. Try a clearer photo with the whole sheet visible.")
            st.image(bgr2rgb(outline), use_container_width=True)

    if objs:
        df = pd.DataFrame(objs, columns=["Width (cm)", "Height (cm)"])
        df.index = [f"Object {i+1}" for i in range(len(df))]
        st.subheader("📋 Measurements")
        st.dataframe(df, use_container_width=True)
        st.download_button("⬇️ Download result image",
                           cv2.imencode(".png", result)[1].tobytes(),
                           "measurement.png", "image/png")
else:
    st.info("👆 Upload a photo to get started.")
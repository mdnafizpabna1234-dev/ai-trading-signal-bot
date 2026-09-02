import streamlit as st
from PIL import Image
import os
import base64
from openai import OpenAI

# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="AI Trading Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("🤖 AI Trading Analysis")
st.caption("AI Chart Screenshot Analysis System")

st.divider()

# ==========================================
# OPENAI CONNECTION
# ==========================================

api_key = st.secrets.get("OPENAI_API_KEY", "")

if not api_key:
    st.error("❌ OPENAI_API_KEY পাওয়া যায়নি। Streamlit Secrets চেক করুন।")
    st.stop()

client = OpenAI(api_key=api_key)

# ==========================================
# UPLOAD CHART
# ==========================================

st.subheader("📷 Upload Trading Chart")

uploaded_file = st.file_uploader(
    "আপনার Trading Chart Screenshot এখানে দিন",
    type=["png", "jpg", "jpeg"]
)

# ==========================================
# ANALYSIS
# ==========================================

if uploaded_file:

    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="Uploaded Trading Chart",
        use_container_width=True
    )

    st.success("✅ Chart uploaded successfully")

    st.divider()

    if st.button("🤖 ANALYZE CHART", use_container_width=True):

        with st.spinner("🔍 AI chart analysis চলছে..."):

            try:

                # Image → Base64
                import io

                buffer = io.BytesIO()
                image.save(buffer, format="JPEG")
                image_bytes = buffer.getvalue()

                base64_image = base64.b64encode(
                    image_bytes
                ).decode("utf-8")

                # ==================================
                # AI PROMPT
                # ==================================

                prompt = """
You are an educational trading chart analysis assistant.

Analyze the uploaded trading chart carefully.

Return the analysis using exactly these sections:

1. TREND
- Bullish / Bearish / Sideways / Unclear

2. MARKET STRUCTURE
- HH / HL / LH / LL
- BOS / CHoCH if visible

3. SUPPORT
- Important support area if visible
- If unclear say Not Clear

4. RESISTANCE
- Important resistance area if visible
- If unclear say Not Clear

5. PPR ANALYSIS
- PPR visible or not
- Direction if visible
- Do not invent PPR if it cannot be confirmed from the image

6. CANDLE ANALYSIS
- Recent candle pattern
- Bullish/Bearish strength
- Wick rejection / Engulfing / Doji etc. if visible

7. BREAKOUT
- Breakout / Fake Breakout / No Clear Breakout

8. ENTRY
- CALL / PUT / WAIT
- Give the reason

9. CONFIRMATION
- What confirmation is required before entry

10. CONFIDENCE
- Give an estimated confidence percentage
- This is NOT a guarantee

11. FINAL SIGNAL
- CALL
- PUT
- WAIT

12. RISK WARNING
Clearly state that chart analysis cannot guarantee profit.

Important:
- Never invent levels that are not visible.
- If the screenshot quality is poor, say so.
- Prefer WAIT when confirmation is insufficient.
- This is educational probability-based analysis, not financial advice.
"""

                # ==================================
                # OPENAI VISION ANALYSIS
                # ==================================

                response = client.responses.create(
                    model="gpt-5.6-luna",
                    input=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "input_text",
                                    "text": prompt
                                },
                                {
                                    "type": "input_image",
                                    "image_url": (
                                        "data:image/jpeg;base64,"
                                        + base64_image
                                    )
                                }
                            ]
                        }
                    ]
                )

                result = response.output_text

                # ==================================
                # DISPLAY RESULT
                # ==================================

                st.divider()
                st.subheader("📊 AI Analysis Result")

                st.markdown(result)

                st.divider()

                st.warning(
                    "⚠️ AI analysis is probability-based. "
                    "It cannot guarantee profit or a winning trade."
                )

            except Exception as e:

                st.error(
                    "❌ AI Analysis Error"
                )

                st.code(str(e))

else:

    st.info(
        "👆 প্রথমে একটি Trading Chart Screenshot upload করুন।"
    )

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "AI Trading Analysis System • Educational Use Only"
)

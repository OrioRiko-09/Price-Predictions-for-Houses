import streamlit as st
import joblib
import numpy as np
import warnings

warnings.filterwarnings("ignore")

# Set Page Config
st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏡",
    layout="centered"
)


# Load Model
@st.cache_resource
def load_model():
    return joblib.load("Random_search.pkl")


try:
    model = load_model()
except Exception as e:
    model = None


# Function to format number in Indian Currency Style (Lakhs, Crores)
def format_indian_currency(amount):
    s = str(amount)
    if len(s) <= 3:
        return s
    last_three = s[-3:]
    other_digits = s[:-3]
    # Group by 2 digits for Indian numbering system
    formatted = ""
    while len(other_digits) > 2:
        formatted = "," + other_digits[-2:] + formatted
        other_digits = other_digits[:-2]
    return other_digits + formatted + "," + last_three


# Custom CSS with Proper Input Sizing, Padding, and Animations
custom_css = """
<style>
    /* Smooth Scrolling */
    html {
        scroll-behavior: smooth;
    }

    /* Vibrant Gradient App Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%);
        color: #f8fafc;
    }

    /* Headings & Text Color Fix */
    h1, h2, h3, .stMarkdown, p {
        color: #f8fafc !important;
    }

    /* Input Field Labels with Gradient Text */
    label, .stNumberInput label {
        background: linear-gradient(90deg, #38bdf8, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
    }

    /* Fix Number Input Wrapper & Sizing to Contain Buttons Comfortably */
    div[data-baseweb="input"] {
        background: rgba(30, 41, 59, 0.75) !important;
        border-radius: 12px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: 2px solid rgba(168, 85, 247, 0.3) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        padding-right: 6px !important;
        min-height: 48px !important;
    }

    div[data-baseweb="input"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(168, 85, 247, 0.3);
        border-color: #c084fc !important;
    }

    /* Plus (+) and Minus (-) Step Button Proper Sizing and Hover Animations */
    button[aria-label="Step down"], button[aria-label="Step up"],
    button[data-testid="stNumberInputStepDown"], button[data-testid="stNumberInputStepUp"] {
        background: rgba(255, 255, 255, 0.08) !important;
        border-radius: 6px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        padding: 4px 10px !important;
        margin: 3px 2px !important;
        height: auto !important;
        transition: all 0.25s ease-in-out !important;
    }

    button[aria-label="Step down"]:hover, button[aria-label="Step up"]:hover,
    button[data-testid="stNumberInputStepDown"]:hover, button[data-testid="stNumberInputStepUp"]:hover {
        background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%) !important;
        transform: scale(1.1) !important;
        box-shadow: 0 0 12px rgba(236, 72, 153, 0.6) !important;
        border-color: transparent !important;
    }

    button[aria-label="Step down"]:hover svg, button[aria-label="Step up"]:hover svg,
    button[data-testid="stNumberInputStepDown"]:hover svg, button[data-testid="stNumberInputStepUp"]:hover svg {
        fill: #ffffff !important;
        color: #ffffff !important;
    }

    /* Predict Button Gradient Styling & Glow Effect */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #a855f7 0%, #ec4899 50%, #3b82f6 100%);
        background-size: 200% auto;
        color: white !important;
        border-radius: 14px;
        padding: 14px 28px;
        font-size: 19px;
        font-weight: 700;
        border: none;
        transition: all 0.4s ease;
        box-shadow: 0 4px 20px rgba(168, 85, 247, 0.4);
    }

    div.stButton > button:hover {
        background-position: right center;
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 30px rgba(236, 72, 153, 0.6);
    }

    div.stButton > button:active {
        transform: translateY(1px) scale(0.98);
    }

    /* Output Card Gradient Styling */
    .result-card {
        background: rgba(30, 41, 59, 0.85);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 18px;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
        border: 2px solid transparent;
        border-image: linear-gradient(135deg, #38bdf8, #a855f7, #ec4899) 1;
        animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        margin-top: 25px;
    }

    .result-price {
        background: linear-gradient(90deg, #4ade80, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        margin: 10px 0;
    }

    @keyframes slideUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# UI Layout
st.title("🏡 House Price Prediction")
st.caption("Enter house attributes to dynamically evaluate estimated property value.")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    bedroom = st.number_input("Number of Bedrooms", min_value=0, value=2, step=1)
    bathroom = st.number_input("Number of Bathrooms", min_value=0, value=1, step=1)
    number_of_school = st.number_input("Nearby Schools", min_value=0, value=1, step=1)

with col2:
    living_area = st.number_input("Living Area (sq ft)", min_value=0, value=2000, step=50)
    condition_of_house = st.number_input("House Condition (1-5)", min_value=1, max_value=5, value=3, step=1)

st.markdown("<br>", unsafe_allow_html=True)

x = [[bedroom, bathroom, living_area, condition_of_house, number_of_school]]

prediction = st.button("✨ Predict Price")

if prediction:
    if model is not None:
        X_array = np.array(x)
        price = int(model.predict(X_array)[0])
        formatted_price = format_indian_currency(price)

        st.markdown(
            f"""
            <div class="result-card">
                <h3 style="margin: 0; color: #cbd5e1 !important;">Estimated House Price</h3>
                <div class="result-price">₹{formatted_price}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error("Model file `Random_search.pkl` not found. Please ensure it is in the same directory.")
else:
    st.info("Click the **Predict Price** button to calculate the estimated price.")

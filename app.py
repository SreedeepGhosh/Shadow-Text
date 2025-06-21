import streamlit as st
from PIL import Image
from steganography import encode_image, decode_image
from utils import (
    load_image, resize_image, image_to_bytes,
    encrypt_message, decrypt_message,
    calculate_capacity
)


st.set_page_config(page_title="Steganography App", layout="centered")

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
    st.rerun()

theme_file = "style_dark.css" if st.session_state.theme == "dark" else "style_light.css"
with open(theme_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

toggle_label = "🌞" if st.session_state.theme == "dark" else "🌙"

top_right = st.columns([11, 1])[1] 
with top_right:
    if st.button(toggle_label, key="toggle-theme"):
        toggle_theme()

if "page" not in st.session_state:
    st.session_state.page = "home"
if "input_mode" not in st.session_state:
    st.session_state.input_mode = "upload"

def go_to(page_name):
    st.session_state.page = page_name

def set_upload_mode():
    st.session_state.input_mode = "upload"

def set_webcam_mode():
    st.session_state.input_mode = "webcam"

page = st.session_state.page

if page == "home":
    st.title("🔐 Secure Image Steganography")
    st.subheader("Hide or Extract Encrypted Multilingual Messages")

    st.markdown(
        """
        <div class="intro-text">
        This project allows you to securely <b>hide secret messages inside images</b> using steganography — the art of concealing information within media files.<br><br>
        All messages are <b>encrypted and password protected</b>, ensuring privacy and data integrity.  
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Select Action:")
    col1, col2 = st.columns(2)
    with col1:
        st.button("🔐 Encode Message", use_container_width=True, on_click=lambda: go_to("encode"))
    with col2:
        st.button("🕵️ Decode Message", use_container_width=True, on_click=lambda: go_to("decode"))

elif page == "encode":
    st.markdown("### 🔐 Encode Message into Image")
    st.button("⬅️ Back", on_click=lambda: go_to("home"))

    col1, col2 = st.columns(2)
    with col1:
        st.button("📁 Upload Image", on_click=set_upload_mode, use_container_width=True)
    with col2:
        st.button("📷 Use Webcam", on_click=set_webcam_mode, use_container_width=True)

    img = None
    if st.session_state.input_mode == "upload":
        uploaded_img = st.file_uploader("🖼️ Select an image to hide your message in", type=["png", "jpg", "jpeg"])
        if uploaded_img:
            img = load_image(uploaded_img)
    elif st.session_state.input_mode == "webcam":
        captured_img = st.camera_input("Capture Image")
        if captured_img:
            img = load_image(captured_img)

    secret_msg = st.text_area("📝 Enter the secret message (any language)")
    password = st.text_input("🔑 Enter a password", type="password")

    if img:
        resized_img = resize_image(img)
        max_bits = calculate_capacity(resized_img)
        max_chars = max_bits // 8
        st.info(f"🧠 This image can safely store approximately **{max_chars} characters**.")

    if img and secret_msg and password:
        if st.button("✅ Encode Now"):
            encrypted_msg = encrypt_message(secret_msg, password)
            stego_img = encode_image(resized_img, encrypted_msg)
            img_bytes = image_to_bytes(stego_img)

            st.image(stego_img, caption="✅ Stego Image (Encrypted)", use_container_width=True)
            st.download_button("⬇️ Download Encoded Image", img_bytes, file_name="stego_output.png", mime="image/png")
    elif img and (not password or not secret_msg):
        st.warning("⚠️ Please enter both a message and a password.")

elif page == "decode":
    st.markdown("### 🕵️ Decode Hidden Message")
    st.button("⬅️ Back", on_click=lambda: go_to("home"))

    uploaded_img = st.file_uploader("📤 Upload Stego Image", type=["png", "jpg", "jpeg"])
    password = st.text_input("🔑 Enter a password", type="password")

    if uploaded_img and password:
        if st.button("🔍 Decode Now"):
            img = load_image(uploaded_img)
            encrypted_msg = decode_image(img)

            if not encrypted_msg:
                st.error("⚠️ No hidden data found in the image.")
            else:
                decrypted_msg = decrypt_message(encrypted_msg, password)
                if decrypted_msg:
                    st.success("✅ Secret Message Decrypted:")
                    st.code(decrypted_msg)
                else:
                    st.error("❌ Incorrect password or corrupted message.")

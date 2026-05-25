import streamlit as st
from cipher import PolyalphabeticCesearShift
from key_manager import key_manager

cipher = PolyalphabeticCesearShift()

st.set_page_config(page_title="Polyalphabetic Caesar Cipher", layout="wide")

st.title("Polyalphabetic Caesar Cipher")
st.caption("David Girgis, Yasmin Guerra Flores, Evan Haque")

st.divider()

if "mode" not in st.session_state:
    st.session_state.mode = "Encrypt"
if "message" not in st.session_state:
    st.session_state.message = ""
if "cipher_keys" not in st.session_state:
    st.session_state.cipher_keys = []
if "key_version" not in st.session_state:
    st.session_state.key_version = 0

def restore_case(original, result):
    out = []
    for orig, res in zip(original, result):
        out.append(res.lower() if orig.islower() else res)
    return "".join(out)

def flip():
    msg = st.session_state.message
    keys = st.session_state.cipher_keys
    if msg and keys and any(c.isalpha() for c in msg):
        upper = msg.upper()
        if st.session_state.mode == "Encrypt":
            raw = cipher.encrypt(upper, keys)
            st.session_state.message = restore_case(msg, raw)
            st.session_state.mode = "Decrypt"
        else:
            raw = cipher.decrypt(upper, keys)
            st.session_state.message = restore_case(msg, raw)
            st.session_state.mode = "Encrypt"

def add_key():
    st.session_state.cipher_keys.append(st.session_state.new_key_value)
    st.session_state.key_version += 1

col_input, col_output = st.columns(2)

with col_input:
    st.subheader("Input")
    mode = st.radio("Mode", ["Encrypt", "Decrypt"], horizontal=True, key="mode")
    message = st.text_input(
        "Message",
        placeholder="Enter your message",
        key="message",
    )

    st.markdown("**Cipher Keys** (drag to reorder, double click to remove)")
    if st.session_state.cipher_keys:
        result = key_manager(st.session_state.cipher_keys, key=f"keys_{st.session_state.key_version}")
        if result and result.get("action") == "update":
            new_keys = result["keys"]
            if new_keys != st.session_state.cipher_keys:
                st.session_state.cipher_keys = new_keys
                st.session_state.key_version += 1
                st.rerun()

    add_cols = st.columns([2, 1, 3])
    with add_cols[0]:
        st.number_input("Shift (0-25)", min_value=0, max_value=25, value=0, key="new_key_value")
    with add_cols[1]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("Add Key", on_click=add_key)

    col_submit, col_flip, _ = st.columns([1, 1, 4])
    with col_submit:
        submitted = st.button("Submit")
    with col_flip:
        st.button("Flip", on_click=flip, help="Swap result into input and toggle mode")

keys = st.session_state.cipher_keys
valid = False
cleaned = ""
if submitted and message and keys:
    cleaned = message.upper()
    if not any(c.isalpha() for c in cleaned):
        st.error("Message must contain at least one letter.")
    else:
        valid = True
elif submitted and not keys:
    st.error("Add at least one cipher key.")

with col_output:
    st.subheader("Result")
    if valid:
        if mode == "Encrypt":
            raw = cipher.encrypt(cleaned, keys)
            result = restore_case(message, raw)
            st.success(f"Ciphertext: **{result}**")
        else:
            raw = cipher.decrypt(cleaned, keys)
            result = restore_case(message, raw)
            st.success(f"Plaintext: **{result}**")
    else:
        st.write("Enter a message and add keys to see results.")

if valid:
    st.divider()
    st.subheader("Step-by-Step Breakdown")

    source = cleaned
    rows = []
    for i, char in enumerate(source):
        if not char.isalpha():
            continue
        pos = ord(char) - ord("A")
        s = keys[i % len(keys)]
        if mode == "Encrypt":
            new_pos = (pos + s) % 26
            op = f"{pos} + {s} = {pos + s} mod 26 = {new_pos}"
        else:
            new_pos = (pos - s) % 26
            op = f"{pos} - {s} = {pos - s} mod 26 = {new_pos}"
        out_char = chr(new_pos + ord("A"))
        rows.append({
            "Position": i + 1,
            "Input Letter": char,
            "Letter Value": pos,
            "Key Used": f"c{i % len(keys) + 1} = {s}",
            "Calculation": op,
            "Result Value": new_pos,
            "Output Letter": out_char,
        })

    st.table(rows)

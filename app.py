import streamlit as st
from cipher import PolyalphabeticCesearShift

cipher = PolyalphabeticCesearShift()

st.set_page_config(page_title="Polyalphabetic Caesar Cipher", layout="wide")

st.title("Polyalphabetic Caesar Cipher")
st.caption("David Girgis, Yasmin Guerra Flores, Evan Haque")

st.divider()

col_input, col_output = st.columns(2)

with col_input:
    st.subheader("Input")
    mode = st.radio("Mode", ["Encrypt", "Decrypt"], horizontal=True)
    message = st.text_input(
        "Message",
        placeholder="Enter your message",
    )
    shift = st.text_input(
        "Shift Key (digits)",
        placeholder="e.g. 1221",
    )

valid = False
cleaned = ""
if message and shift:
    cleaned = message.upper()
    if not any(c.isalpha() for c in cleaned):
        st.error("Message must contain at least one letter.")
    elif not shift.isdigit():
        st.error("Shift key must contain only digits (0-9).")
    else:
        valid = True

with col_output:
    st.subheader("Result")
    if valid:
        if mode == "Encrypt":
            result = cipher.encrypt(cleaned, shift)
            st.success(f"Ciphertext: **{result}**")
        else:
            result = cipher.decrypt(cleaned, shift)
            st.success(f"Plaintext: **{result}**")
    else:
        st.write("Enter a message and shift key to see results.")

if valid:
    st.divider()
    st.subheader("Step-by-Step Breakdown")

    source = cleaned
    rows = []
    shift_index = 0
    for char in source:
        if not char.isalpha():
            continue
        pos = ord(char) - ord("A")
        s = int(shift[shift_index % len(shift)])
        if mode == "Encrypt":
            new_pos = (pos + s) % 26
            op = f"{pos} + {s} = {pos + s} mod 26 = {new_pos}"
        else:
            new_pos = (pos - s) % 26
            op = f"{pos} - {s} = {pos - s} mod 26 = {new_pos}"
        out_char = chr(new_pos + ord("A"))
        rows.append({
            "Position": shift_index + 1,
            "Input Letter": char,
            "Letter Value": pos,
            "Shift Key Digit": s,
            "Calculation": op,
            "Result Value": new_pos,
            "Output Letter": out_char,
        })
        shift_index += 1

    st.table(rows)

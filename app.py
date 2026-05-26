import streamlit as st
from cipher import PolyalphabeticCesearShift

cipher = PolyalphabeticCesearShift()

st.set_page_config(page_title="Polyalphabetic Caesar Cipher", layout="wide")

st.title("Polyalphabetic Caesar Cipher")
st.caption("David Girgis, Yasmin Guerra Flores, Evan Haque")

st.divider()

if "mode" not in st.session_state:
    st.session_state.mode = "Encrypt"
if "message" not in st.session_state:
    st.session_state.message = ""
if "available_keys" not in st.session_state:
    st.session_state.available_keys = []
if "key_sequence" not in st.session_state:
    st.session_state.key_sequence = []
if "last_tap" not in st.session_state:
    st.session_state.last_tap = None

def restore_case(original, result):
    out = []
    for orig, res in zip(original, result):
        out.append(res.lower() if orig.islower() else res)
    return "".join(out)

if "flipped" not in st.session_state:
    st.session_state.flipped = False

def get_shift_values():
    avail = st.session_state.available_keys
    return [avail[i] for i in st.session_state.key_sequence]

def flip():
    msg = st.session_state.message
    keys = get_shift_values()
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
        st.session_state.flipped = True

def add_available_key():
    st.session_state.available_keys.append(st.session_state.new_key_value)

def add_to_sequence(index):
    st.session_state.key_sequence.append(index)

def tap_sequence(i):
    if st.session_state.last_tap == i:
        st.session_state.key_sequence.pop(i)
        st.session_state.last_tap = None
    else:
        st.session_state.last_tap = i

col_input, col_output = st.columns(2)

with col_input:
    st.subheader("Input")
    mode = st.radio("Mode", ["Encrypt", "Decrypt"], horizontal=True, key="mode")
    message = st.text_input(
        "Message",
        placeholder="Enter your message",
        key="message",
    )

    st.markdown("**Available Keys** (tap to add to sequence)")
    if st.session_state.available_keys:
        avail = st.session_state.available_keys
        for row_start in range(0, len(avail), 6):
            row = avail[row_start:row_start + 6]
            cols = st.columns(6)
            for j, k in enumerate(row):
                cols[j].button(
                    f"c{row_start + j + 1} = {k}",
                    key=f"avail_{row_start + j}",
                    on_click=add_to_sequence,
                    args=(row_start + j,),
                )

    add_cols = st.columns([2, 1, 3])
    with add_cols[0]:
        st.number_input("Shift (0-25)", min_value=0, max_value=25, value=0, key="new_key_value")
    with add_cols[1]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("Add Key", on_click=add_available_key)

    st.markdown("**Key Sequence** (double tap to remove)")
    if st.session_state.key_sequence:
        seq = st.session_state.key_sequence
        for row_start in range(0, len(seq), 8):
            row = seq[row_start:row_start + 8]
            cols = st.columns(8)
            for j, idx in enumerate(row):
                cols[j].button(
                    f"c{idx + 1}",
                    key=f"seq_{row_start + j}",
                    on_click=tap_sequence,
                    args=(row_start + j,),
                )

    col_submit, col_flip, _ = st.columns([1, 1, 4])
    with col_submit:
        submitted = st.button("Submit")
    with col_flip:
        st.button("Flip", on_click=flip, help="Swap result into input and toggle mode")

keys = get_shift_values()
valid = False
cleaned = ""
if (submitted or st.session_state.flipped) and message and keys:
    st.session_state.flipped = False
    cleaned = message.upper()
    if not any(c.isalpha() for c in cleaned):
        st.error("Message must contain at least one letter.")
    else:
        valid = True
elif submitted and not keys:
    st.error("Add keys to the sequence first.")

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
        st.write("Enter a message and build a key sequence to see results.")

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
        s = keys[shift_index % len(keys)]
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
            "Key Used": f"{s}",
            "Calculation": op,
            "Result Value": new_pos,
            "Output Letter": out_char,
        })
        shift_index += 1

    st.table(rows)

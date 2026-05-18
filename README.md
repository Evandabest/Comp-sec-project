# Polyalphabetic Caesar Cipher

A Streamlit web app that encrypts and decrypts messages using a polyalphabetic Caesar shift cipher. Each letter is shifted by a corresponding digit from a numeric key, cycling through the key as needed.

**Authors:** David Girgis, Yasmin Guerra Flores, Evan Haque, Arnob Hassan

## Requirements

- Python 3
- Streamlit

## Setup

1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd cipher-project
   ```

2. Install dependencies:
   ```sh
   pip install streamlit
   ```

## Running the App

```sh
streamlit run app.py
```

The app will open in your browser. Enter a message (letters only) and a numeric shift key, then choose **Encrypt** or **Decrypt** to see the result along with a step-by-step breakdown.

## Usage Example

- **Message:** `HELLO`
- **Shift Key:** `1221`
- **Encrypt result:** Each letter is shifted by the corresponding digit (H+1, E+2, L+2, L+1, O+1) to produce the ciphertext.

import os
import streamlit.components.v1 as components

_component_func = components.declare_component(
    "key_chips",
    path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "components"),
)

def key_manager(cipher_keys, key=None):
    result = _component_func(keys=cipher_keys, key=key, default=None)
    return result

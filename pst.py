import streamlit as st
import re
import random
import streamlit.components.v1 as components

# --- Helper function for clipboard copy (no alert) ---
def copy_to_clipboard(text):
    components.html(f"""
    <style>
        .copy-btn {{
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 8px 16px;
            text-align: center;
            text-decoration: none;
            font-size: 14px;
            border-radius: 5px;
            cursor: pointer;
        }}
    </style>
    <script>
    function copyText() {{
        const text = `{text}`;
        navigator.clipboard.writeText(text);
    }}
    </script>
    <button class="copy-btn" onclick="copyText()">📋 Copy to Clipboard</button>
    """, height=100)

# --- Sequential character check ---
def has_sequential_chars(s, min_length=3):
    for i in range(len(s) - min_length + 1):
        current_slice = s[i:i+min_length]
        is_ascending = all(
            ord(current_slice[j]) - ord(current_slice[j-1]) == 1
            for j in range(1, min_length)
        )
        is_descending = all(
            ord(current_slice[j-1]) - ord(current_slice[j]) == 1
            for j in range(1, min_length)
        )
        if is_ascending or is_descending:
            return True
    return False

# --- Repeated character check ---
def has_repeated_chars(s, min_length=3):
    for i in range(len(s) - min_length + 1):
        current_slice = s[i:i+min_length]
        if len(set(current_slice)) == 1:
            return True
    return False

# --- Generate strong password ---
def generate_strong_password(length=12):
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lowercase = 'abcdefghijklmnopqrstuvwxyz'
    digits = '0123456789'
    specials = '!@#$%^&*'
    password = [
        random.choice(uppercase),
        random.choice(lowercase),
        random.choice(digits),
        random.choice(specials)
    ]
    all_chars = uppercase + lowercase + digits + specials
    for _ in range(length - 4):
        password.append(random.choice(all_chars))
    random.shuffle(password)
    return ''.join(password)

# --- Password strength check ---
def check_password_strength(password):
    common_passwords = [
        'password', '123456', '12345678', 'qwerty', 'abc123',
        'password1', 'admin', 'letmein', 'welcome', 'monkey',
        'sunshine', 'password123', 'football', 'iloveyou',
        '1234567', '1234567890', '123123', '12345', '1234',
        '111111', '000000', 'passw0rd'
    ]
    score = 0
    feedback = []

    if password.lower() in common_passwords:
        st.error("This password is too common and easily guessable. Please choose a different one.")
        return 0, feedback

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Include uppercase letters")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Include lowercase letters")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add at least one number (0-9)")

    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("Include at least one special character (!@#$%^&*)")

    if has_sequential_chars(password):
        feedback.append("Avoid sequential characters (e.g., 'abc', '123')")
        score -= 1

    if has_repeated_chars(password):
        feedback.append("Avoid repeated characters (e.g., 'aaa', '111')")
        score -= 1

    score = max(0, score)
    return score, feedback

# --- Main App ---
def main():
    st.set_page_config(page_title="Password Strength Meter", page_icon="🔒")
    st.title("🔐 Password Strength Analyzer")
    st.markdown("---")

    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            password = st.text_input("Enter your password:", type="password")
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            generate_btn = st.button("✨ Generate Strong Password")

    if generate_btn:
        new_pass = generate_strong_password()
        st.session_state.generated_password = new_pass

    if 'generated_password' in st.session_state:
        st.code(f"Generated Password: {st.session_state.generated_password}", language="bash")
        copy_to_clipboard(st.session_state.generated_password)

    if password:
        with st.spinner("Analyzing password..."):
            score, feedback = check_password_strength(password)

        st.markdown("---")
        st.subheader("Security Analysis")

        progress = score / 5
        color = "#ff4b4b" if progress < 0.6 else "#faca2b" if progress < 0.8 else "#21c354"
        st.markdown(f"""
        <style>
            .stProgress > div > div > div > div {{
                background-color: {color};
            }}
        </style>
        """, unsafe_allow_html=True)
        st.progress(progress)

        if score >= 5:
            st.success("✅ Strong Password! (5/5)")
            st.balloons()
        elif score >= 3:
            st.warning(f"⚠ Moderate Password ({score}/5)")
        else:
            st.error(f"❌ Weak Password ({score}/5)")

        if feedback:
            st.markdown("---")
            st.subheader("🔍 Improvement Suggestions")
            for item in feedback:
                st.markdown(f"- {item}")

        if score < 5:
            st.markdown("---")
            if st.button("🛠 Show Strong Password Example"):
                example_pass = generate_strong_password()
                st.code(example_pass, language="bash")
                copy_to_clipboard(example_pass)

    st.markdown("---")
    with st.expander("ℹ About This Tool"):
        st.markdown("""
        ### Features:
        - Basic security requirements check
        - Common password detection
        - Pattern analysis (sequences & repetitions)
        - Real-time strength meter
        - One-click password generation
        - Clipboard copy support (no external tool needed)

        ### Security Criteria:
        - ✅ Minimum 8 characters
        - ✅ Upper & Lowercase letters
        - ✅ At least 1 number
        - ✅ Special characters (!@#$%^&*)
        - ❌ No common patterns
        - ❌ No repeated characters
        """)

if __name__ == "__main__":
    main()

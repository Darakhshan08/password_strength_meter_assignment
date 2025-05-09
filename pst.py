import streamlit as st
import re
import random
import pyperclip  # Added for clipboard functionality


def has_sequential_chars(s, min_length=3):
    for i in range(len(s) - min_length + 1):
        current_slice = s[i:i+min_length]
        # Check ascending sequence
        is_ascending = True
        for j in range(1, min_length):
            if ord(current_slice[j]) - ord(current_slice[j-1]) != 1:
                is_ascending = False
                break
        # Check descending sequence
        is_descending = True
        for j in range(1, min_length):
            if ord(current_slice[j-1]) - ord(current_slice[j]) != 1:
                is_descending = False
                break
        if is_ascending or is_descending:
            return True
    return False

def has_repeated_chars(s, min_length=3):
    for i in range(len(s) - min_length + 1):
        current_slice = s[i:i+min_length]
        if len(set(current_slice)) == 1:
            return True
    return False

def generate_strong_password(length=12):
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lowercase = 'abcdefghijklmnopqrstuvwxyz'
    digits = '0123456789'
    specials = '!@#$%^&*'
    # Ensure at least one of each required type
    password = [
        random.choice(uppercase),
        random.choice(lowercase),
        random.choice(digits),
        random.choice(specials)
    ]
    # Fill the rest with random characters
    all_chars = uppercase + lowercase + digits + specials
    for _ in range(length - 4):
        password.append(random.choice(all_chars))
    # Shuffle to avoid predictable order
    random.shuffle(password)
    return ''.join(password)

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
    
    # Check against common passwords
    if password.lower() in common_passwords:
        st.error("This password is too common and easily guessable. Please choose a different one.")
        return 0, feedback
    
    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long")
    
    # Uppercase Check
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Include uppercase letters")
    
    # Lowercase Check
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Include lowercase letters")
    
    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add at least one number (0-9)")
    
    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("Include at least one special character (!@#$%^&*)")
    
    # Check for sequential patterns
    if has_sequential_chars(password):
        feedback.append("Avoid sequential characters (e.g., 'abc', '123')")
        score -= 1
    
    # Check for repeated patterns
    if has_repeated_chars(password):
        feedback.append("Avoid repeated characters (e.g., 'aaa', '111')")
        score -= 1
    
    # Ensure score is not negative
    score = max(0, score)
    
    return score, feedback

def main():
    st.set_page_config(page_title="Password Strength Meter", page_icon="🔒")
    
    # Main layout
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
        
        # Using pyperclip for reliable clipboard functionality
        if st.button("📋 Copy to Clipboard"):
            try:
                pyperclip.copy(st.session_state.generated_password)
                st.success("✅ Password copied to clipboard!")
            except Exception as e:
                st.error(f"Failed to copy to clipboard: {e}")

    if password:
        with st.spinner("Analyzing password..."):
            score, feedback = check_password_strength(password)
        
        st.markdown("---")
        st.subheader("Security Analysis")
        
        # Visual progress bar
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
        
        # Score display
        if score >= 5:
            st.success("✅ Strong Password! (5/5)")
            st.balloons()
        elif score >= 3:
            st.warning(f"⚠ Moderate Password ({score}/5)")
        else:
            st.error(f"❌ Weak Password ({score}/5)")
        
        # Feedback section
        if feedback:
            st.markdown("---")
            st.subheader("🔍 Improvement Suggestions")
            for item in feedback:
                st.markdown(f"- {item}")
        
        # Password generation suggestion
        if score < 5:
            st.markdown("---")
            if st.button("🛠 Show Strong Password Example"):
                example_pass = generate_strong_password()
                st.code(example_pass, language="bash")
                if st.button("📋 Copy Example Password"):
                    try:
                        pyperclip.copy(example_pass)
                        st.success("✅ Example password copied to clipboard!")
                    except Exception as e:
                        st.error(f"Failed to copy to clipboard: {e}")

    # About section
    st.markdown("---")
    with st.expander("ℹ About This Tool"):
        st.markdown("""
        ### Features:
        - Basic security requirements check
        - Common password detection
        - Pattern analysis (sequences & repetitions)
        - Real-time strength meter
        - One-click password generation
        - Detailed improvement suggestions
        
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
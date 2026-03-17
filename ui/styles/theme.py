"""
Theme Definitions

Dark and light theme CSS definitions for the Power BI Documentation Generator.
"""

DARK_THEME = """
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    .app-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
    }

    .app-title {
        color: white;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .app-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
    }

    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        text-align: center;
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        margin: 0;
    }

    .metric-label {
        font-size: 0.9rem;
        color: rgba(255,255,255,0.85);
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .info-card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }

    .info-card h3 {
        color: #667eea;
        margin-top: 0;
        font-size: 1.3rem;
    }

    .info-card p, .info-card ul {
        color: rgba(255,255,255,0.8);
        line-height: 1.6;
    }

    .format-option {
        background: rgba(255,255,255,0.05);
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .format-option:hover {
        background: rgba(102, 126, 234, 0.1);
        border-color: #667eea;
        transform: translateX(5px);
    }

    .format-option.selected {
        background: rgba(102, 126, 234, 0.2);
        border-color: #667eea;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
    }

    .step-indicator {
        display: flex;
        justify-content: center;
        margin: 2rem 0;
        gap: 1rem;
    }

    .step {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .step-circle {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: rgba(255,255,255,0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        color: rgba(255,255,255,0.5);
    }

    .step-circle.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
    }

    .step-circle.completed {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }

    .step-label {
        color: rgba(255,255,255,0.5);
        font-size: 0.9rem;
    }

    .step-label.active {
        color: white;
        font-weight: 600;
    }

    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        width: 100%;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
    }

    .stButton>button:disabled {
        background: rgba(255,255,255,0.1);
        color: rgba(255,255,255,0.3);
        cursor: not-allowed;
    }

    .success-box {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.2) 100%);
        border: 2px solid #10b981;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }

    .warning-box {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(217, 119, 6, 0.2) 100%);
        border: 2px solid #f59e0b;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }

    .error-box {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.2) 100%);
        border: 2px solid #ef4444;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }

    /* Fix form labels visibility - CRITICAL */
    .stTextInput label,
    .stSelectbox label,
    .stRadio label,
    .stTextArea label,
    .stNumberInput label,
    .stFileUploader label,
    label {
        color: white !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Fix input fields */
    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox select {
        background-color: rgba(255,255,255,0.05) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 8px !important;
    }

    /* Radio button text */
    .stRadio > div {
        color: white !important;
    }

    /* Form container */
    [data-testid="stForm"] {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 2rem;
    }

    h1, h2, h3, h4, h5, h6 {
        color: white !important;
    }

    p, li, span, div, label {
        color: rgba(255,255,255,0.8);
    }

    .stTextInput>div>div>input {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(102, 126, 234, 0.3);
        color: white;
        border-radius: 8px;
    }

    .stTextInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }

    .stTextArea>div>div>textarea {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(102, 126, 234, 0.3);
        color: white;
        border-radius: 8px;
    }

    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .status-completed {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }

    .status-progress {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
    }

    .css-1d391kg, [data-testid="stSidebar"] {
        background: rgba(22, 33, 62, 0.95);
        backdrop-filter: blur(10px);
    }

    hr {
        border-color: rgba(255,255,255,0.1);
        margin: 2rem 0;
    }

    .stAlert {
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }

    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
    }

    /* File uploader styling */
    .uploadedFile {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 8px;
    }

    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.05);
        border: 2px dashed rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        padding: 2rem;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: #667eea;
        background: rgba(102, 126, 234, 0.05);
    }
</style>
"""

LIGHT_THEME = """
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e3edf7 100%);
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    .app-header {
        background: linear-gradient(135deg, #5469d4 0%, #5c6ac4 100%);
        padding: 1.5rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    .app-title {
        color: white;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }

    .app-subtitle {
        color: rgba(255,255,255,0.95);
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
    }

    .metric-card {
        background: linear-gradient(135deg, #5469d4 0%, #5c6ac4 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 16px rgba(84, 105, 212, 0.3);
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        margin: 0;
    }

    .metric-label {
        font-size: 0.9rem;
        color: rgba(255,255,255,0.9);
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .info-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    .info-card h3 {
        color: #5469d4;
        margin-top: 0;
        font-size: 1.3rem;
    }

    .info-card p, .info-card ul {
        color: #374151;
        line-height: 1.6;
    }

    .format-option {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .format-option:hover {
        background: #f9fafb;
        border-color: #5469d4;
        transform: translateX(5px);
    }

    .format-option.selected {
        background: #eff6ff;
        border-color: #5469d4;
        box-shadow: 0 0 0 3px rgba(84, 105, 212, 0.1);
    }

    .step-indicator {
        display: flex;
        justify-content: center;
        margin: 2rem 0;
        gap: 1rem;
    }

    .step {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .step-circle {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #e5e7eb;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        color: #9ca3af;
    }

    .step-circle.active {
        background: linear-gradient(135deg, #5469d4 0%, #5c6ac4 100%);
        color: white;
        box-shadow: 0 0 0 4px rgba(84, 105, 212, 0.2);
    }

    .step-circle.completed {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }

    .step-label {
        color: #9ca3af;
        font-size: 0.9rem;
    }

    .step-label.active {
        color: #1f2937;
        font-weight: 600;
    }

    .stButton>button {
        background: linear-gradient(135deg, #5469d4 0%, #5c6ac4 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(84, 105, 212, 0.2);
        width: 100%;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(84, 105, 212, 0.3);
    }

    .stButton>button:disabled {
        background: #e5e7eb;
        color: #9ca3af;
        cursor: not-allowed;
    }

    .success-box {
        background: #d1fae5;
        border: 2px solid #10b981;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }

    .warning-box {
        background: #fef3c7;
        border: 2px solid #f59e0b;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }

    .error-box {
        background: #fee2e2;
        border: 2px solid #ef4444;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }

    /* Form labels */
    .stTextInput label,
    .stSelectbox label,
    .stRadio label,
    .stTextArea label,
    .stNumberInput label,
    .stFileUploader label,
    label {
        color: #1f2937 !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Input fields */
    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox select {
        background-color: white !important;
        color: #1f2937 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
    }

    /* Radio button text */
    .stRadio > div {
        color: #1f2937 !important;
    }

    /* Form container */
    [data-testid="stForm"] {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 2rem;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #1f2937 !important;
    }

    p, li, span, div, label {
        color: #374151;
    }

    .stTextInput>div>div>input {
        background: white;
        border: 1px solid #d1d5db;
        color: #1f2937;
        border-radius: 8px;
    }

    .stTextInput>div>div>input:focus {
        border-color: #5469d4;
        box-shadow: 0 0 0 3px rgba(84, 105, 212, 0.1);
    }

    .stTextArea>div>div>textarea {
        background: white;
        border: 1px solid #d1d5db;
        color: #1f2937;
        border-radius: 8px;
    }

    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .status-completed {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }

    .status-progress {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
    }

    .css-1d391kg, [data-testid="stSidebar"] {
        background: #f9fafb;
        border-right: 1px solid #e5e7eb;
    }

    hr {
        border-color: #e5e7eb;
        margin: 2rem 0;
    }

    .stAlert {
        background: white;
        border-radius: 8px;
        border-left: 4px solid #5469d4;
    }

    .streamlit-expanderHeader {
        background: #f9fafb;
        border-radius: 8px;
    }

    /* File uploader styling */
    .uploadedFile {
        background: white;
        border: 1px solid #d1d5db;
        border-radius: 8px;
    }

    [data-testid="stFileUploader"] {
        background: white;
        border: 2px dashed #d1d5db;
        border-radius: 12px;
        padding: 2rem;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: #5469d4;
        background: #f9fafb;
    }
</style>
"""

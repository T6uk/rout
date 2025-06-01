# daily_routine_app.py - Enhanced Daily Routine Manager with Advanced Features
import streamlit as st
import json
import pandas as pd
from datetime import datetime, timedelta, time
from pathlib import Path
from typing import Dict, List, Any, Optional
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import time as timer

# Page configuration
st.set_page_config(
    page_title="Daily Routine Manager",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with Dark Mode and Advanced Features
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@300;400;500;600&display=swap');

    /* Advanced CSS Variables */
    :root {
        /* Light Theme */
        --primary: #6366f1;
        --primary-50: #eef2ff;
        --primary-100: #e0e7ff;
        --primary-200: #c7d2fe;
        --primary-300: #a5b4fc;
        --primary-500: #6366f1;
        --primary-600: #4f46e5;
        --primary-700: #4338ca;
        --primary-800: #3730a3;

        --success: #10b981;
        --success-light: #34d399;
        --warning: #f59e0b;
        --warning-light: #fbbf24;
        --error: #ef4444;
        --error-light: #f87171;

        --gray-0: #ffffff;
        --gray-50: #f9fafb;
        --gray-100: #f3f4f6;
        --gray-200: #e5e7eb;
        --gray-300: #d1d5db;
        --gray-400: #9ca3af;
        --gray-500: #6b7280;
        --gray-600: #4b5563;
        --gray-700: #374151;
        --gray-800: #1f2937;
        --gray-900: #111827;

        --bg-primary: var(--gray-50);
        --bg-secondary: var(--gray-0);
        --bg-tertiary: var(--gray-100);
        --text-primary: var(--gray-900);
        --text-secondary: var(--gray-600);
        --text-tertiary: var(--gray-400);
        --border-color: var(--gray-200);
        --border-hover: var(--primary-300);

        /* Shadows */
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-md: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        --shadow-xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        --shadow-colored: 0 10px 25px -5px rgba(99, 102, 241, 0.25);

        /* Animations */
        --transition-fast: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-slow: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        --bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);

        /* Spacing */
        --space-1: 0.25rem;
        --space-2: 0.5rem;
        --space-3: 0.75rem;
        --space-4: 1rem;
        --space-5: 1.25rem;
        --space-6: 1.5rem;
        --space-8: 2rem;
        --space-10: 2.5rem;
        --space-12: 3rem;
        --space-16: 4rem;

        /* Border Radius */
        --radius-sm: 0.375rem;
        --radius: 0.5rem;
        --radius-md: 0.75rem;
        --radius-lg: 1rem;
        --radius-xl: 1.5rem;
        --radius-2xl: 2rem;
        --radius-full: 50%;

        /* Typography */
        --text-xs: 0.75rem;
        --text-sm: 0.875rem;
        --text-base: 1rem;
        --text-lg: 1.125rem;
        --text-xl: 1.25rem;
        --text-2xl: 1.5rem;
        --text-3xl: 1.875rem;
        --text-4xl: 2.25rem;
    }

    /* Dark Theme */
    [data-theme="dark"] {
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --bg-tertiary: #334155;
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
        --text-tertiary: #64748b;
        --border-color: #334155;
        --border-hover: var(--primary-400);
        --gray-0: #1e293b;
        --gray-50: #334155;
        --gray-100: #475569;
        --gray-200: #64748b;
    }

    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, var(--bg-primary) 0%, var(--primary-50) 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-primary);
        transition: var(--transition);
    }

    .main {
        background: transparent;
        padding: var(--space-6);
    }

    /* Animated Background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 25% 25%, rgba(99, 102, 241, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 75% 75%, rgba(16, 185, 129, 0.03) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
        animation: backgroundFlow 20s ease-in-out infinite;
    }

    @keyframes backgroundFlow {
        0%, 100% { transform: scale(1) rotate(0deg); }
        50% { transform: scale(1.1) rotate(1deg); }
    }

    /* Enhanced Header */
    .enhanced-header {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-600) 50%, var(--primary-700) 100%);
        color: white;
        padding: var(--space-8) var(--space-10);
        border-radius: var(--radius-2xl);
        margin: calc(var(--space-6) * -1) calc(var(--space-6) * -1) var(--space-8) calc(var(--space-6) * -1);
        box-shadow: var(--shadow-xl);
        position: relative;
        overflow: hidden;
        animation: slideInDown 0.8s var(--bounce);
    }

    .enhanced-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, 
            rgba(255,255,255,0.3) 0%, 
            rgba(255,255,255,0.8) 50%, 
            rgba(255,255,255,0.3) 100%);
        animation: shimmer 3s ease-in-out infinite;
    }

    .enhanced-header::after {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        animation: shine 4s infinite;
    }

    @keyframes shimmer {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }

    @keyframes shine {
        0% { transform: translateX(-200%) rotate(45deg); }
        100% { transform: translateX(200%) rotate(45deg); }
    }

    .enhanced-header h1 {
        font-size: var(--text-4xl);
        font-weight: 900;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        letter-spacing: -0.025em;
        display: flex;
        align-items: center;
        gap: var(--space-4);
    }

    .enhanced-header p {
        font-size: var(--text-lg);
        margin: var(--space-2) 0 0 0;
        opacity: 0.9;
        font-weight: 500;
    }

    .header-badge {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        padding: var(--space-2) var(--space-4);
        border-radius: var(--radius-full);
        font-size: var(--text-sm);
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.3);
        animation: pulse 2s infinite;
    }

    /* Ultra-Modern Cards */
    .ultra-card {
        background: var(--bg-secondary);
        border: 2px solid var(--border-color);
        border-radius: var(--radius-2xl);
        padding: var(--space-8);
        margin: var(--space-6) 0;
        box-shadow: var(--shadow-lg);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(20px);
    }

    .ultra-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary), var(--primary-600));
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.5s ease;
    }

    .ultra-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: var(--shadow-xl), var(--shadow-colored);
        border-color: var(--border-hover);
    }

    .ultra-card:hover::before {
        transform: scaleX(1);
    }

    .card-glass {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Enhanced Sidebar */
    .css-1d391kg {
        background: var(--bg-secondary) !important;
        border-right: 2px solid var(--border-color) !important;
        box-shadow: var(--shadow-lg) !important;
        backdrop-filter: blur(20px) !important;
        padding: var(--space-4) !important;
    }

    /* Sidebar Content Container */
    .sidebar-content {
        background: var(--bg-secondary);
        border-radius: var(--radius-xl);
        padding: var(--space-4);
        margin-bottom: var(--space-4);
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow);
    }

    /* Navigation Section */
    .nav-section {
        background: var(--bg-secondary);
        border: 2px solid var(--border-color);
        border-radius: var(--radius-xl);
        padding: var(--space-4);
        margin-bottom: var(--space-6);
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
    }

    .nav-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary), var(--primary-600));
        opacity: 0.8;
    }

    .nav-section h3 {
        font-size: var(--text-sm);
        font-weight: 800;
        color: var(--text-primary);
        margin: 0 0 var(--space-4) 0;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        display: flex;
        align-items: center;
        gap: var(--space-2);
    }

    /* Override Streamlit Button Styling in Sidebar */
    .css-1d391kg .stButton > button {
        background: var(--bg-tertiary) !important;
        border: 2px solid var(--border-color) !important;
        border-radius: var(--radius-lg) !important;
        padding: var(--space-3) var(--space-4) !important;
        margin: var(--space-1) 0 !important;
        font-weight: 600 !important;
        font-size: var(--text-sm) !important;
        color: var(--text-primary) !important;
        transition: var(--transition) !important;
        width: 100% !important;
        text-align: left !important;
        display: flex !important;
        align-items: center !important;
        gap: var(--space-3) !important;
        position: relative !important;
        overflow: hidden !important;
    }

    .css-1d391kg .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, var(--primary-100), transparent);
        transition: left 0.3s ease;
        z-index: 0;
    }

    .css-1d391kg .stButton > button:hover {
        background: var(--bg-secondary) !important;
        border-color: var(--primary-300) !important;
        transform: translateX(4px) scale(1.02) !important;
        box-shadow: var(--shadow) !important;
        color: var(--primary) !important;
    }

    .css-1d391kg .stButton > button:hover::before {
        left: 100%;
    }

    .css-1d391kg .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary), var(--primary-600)) !important;
        border-color: var(--primary) !important;
        color: white !important;
        box-shadow: var(--shadow-colored) !important;
        transform: translateX(6px) scale(1.03) !important;
    }

    .css-1d391kg .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, var(--primary-600), var(--primary-700)) !important;
        transform: translateX(8px) scale(1.05) !important;
        box-shadow: var(--shadow-xl), var(--shadow-colored) !important;
    }

    /* Navigation Icon Styling */
    .nav-icon {
        font-size: var(--text-lg);
        width: 24px;
        text-align: center;
        transition: transform var(--transition-fast);
        margin-right: var(--space-2);
    }

    .css-1d391kg .stButton > button:hover .nav-icon {
        transform: scale(1.1) rotate(5deg);
    }

    /* Badge Styling */
    .nav-badge {
        background: var(--primary);
        color: white;
        font-size: var(--text-xs);
        padding: 2px var(--space-2);
        border-radius: var(--radius-full);
        margin-left: auto;
        font-weight: 700;
        min-width: 18px;
        text-align: center;
        animation: pulse 2s infinite;
        display: inline-block;
    }

    .nav-badge.success {
        background: var(--success);
    }

    .nav-badge.warning {
        background: var(--warning);
    }

    .nav-badge.error {
        background: var(--error);
    }

    /* Enhanced Stats */
    .stats-container {
        background: var(--bg-secondary);
        border: 2px solid var(--border-color);
        border-radius: var(--radius-xl);
        padding: var(--space-6);
        margin-bottom: var(--space-6);
        box-shadow: var(--shadow-lg);
        position: relative;
        overflow: hidden;
    }

    .stats-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--success), var(--success-light));
        opacity: 0.8;
    }

    .stats-header {
        font-size: var(--text-sm);
        font-weight: 800;
        color: var(--text-primary);
        margin: 0 0 var(--space-4) 0;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        display: flex;
        align-items: center;
        gap: var(--space-2);
    }

    .stat-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: var(--space-3) 0;
        border-bottom: 1px solid var(--border-color);
        transition: var(--transition);
        cursor: pointer;
        border-radius: var(--radius);
    }

    .stat-item:last-child {
        border-bottom: none;
    }

    .stat-item:hover {
        transform: translateX(4px);
        background: var(--bg-tertiary);
        padding-left: var(--space-4);
        padding-right: var(--space-4);
        margin: 0 calc(var(--space-3) * -1);
    }

    .stat-label {
        font-size: var(--text-xs);
        color: var(--text-secondary);
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .stat-value {
        font-size: var(--text-sm);
        font-weight: 800;
        color: var(--text-primary);
        font-family: 'JetBrains Mono', monospace;
    }

    /* Enhanced Buttons */
    .stButton > button {
        background: var(--bg-secondary);
        border: 2px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: var(--space-4) var(--space-6);
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        font-size: var(--text-sm);
        color: var(--text-primary);
        transition: var(--transition);
        box-shadow: var(--shadow);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, var(--primary-100), transparent);
        transition: left 0.3s ease;
    }

    .stButton > button:hover {
        background: var(--bg-tertiary);
        border-color: var(--border-hover);
        transform: translateY(-2px) scale(1.02);
        box-shadow: var(--shadow-lg);
        color: var(--primary);
    }

    .stButton > button:hover::before {
        left: 100%;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary), var(--primary-600));
        border-color: var(--primary);
        color: white;
        font-weight: 700;
        box-shadow: var(--shadow-colored);
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, var(--primary-600), var(--primary-700));
        transform: translateY(-3px) scale(1.05);
        box-shadow: var(--shadow-xl), var(--shadow-colored);
    }

    .stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, var(--success), var(--success-light));
        border-color: var(--success);
        color: white;
        font-weight: 700;
    }

    /* Enhanced Progress Bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary), var(--primary-light));
        border-radius: var(--radius);
        height: 12px;
        position: relative;
        overflow: hidden;
    }

    .stProgress > div > div > div::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        animation: progressShine 2s infinite;
    }

    @keyframes progressShine {
        0% { left: -100%; }
        100% { left: 100%; }
    }

    .stProgress > div > div {
        background: var(--border-color);
        border-radius: var(--radius);
        height: 12px;
        overflow: hidden;
    }

    /* Enhanced Form Elements */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input,
    .stTimeInput > div > div > input {
        border: 2px solid var(--border-color);
        border-radius: var(--radius-lg);
        font-family: 'Inter', sans-serif;
        font-size: var(--text-sm);
        padding: var(--space-4) var(--space-5);
        background: var(--bg-secondary);
        color: var(--text-primary);
        transition: var(--transition);
        box-shadow: var(--shadow-sm);
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div:focus-within,
    .stNumberInput > div > div > input:focus,
    .stDateInput > div > div > input:focus,
    .stTimeInput > div > div > input:focus {
        border-color: var(--primary);
        outline: none;
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1), var(--shadow-lg);
        transform: scale(1.02);
    }

    /* Enhanced Metrics */
    [data-testid="metric-container"] {
        background: var(--bg-secondary);
        border: 2px solid var(--border-color);
        border-radius: var(--radius-xl);
        padding: var(--space-6);
        margin: var(--space-4) 0;
        box-shadow: var(--shadow-lg);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }

    [data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, var(--primary), var(--primary-light));
        opacity: 0;
        transition: opacity 0.3s ease;
        z-index: -1;
    }

    [data-testid="metric-container"]:hover {
        transform: translateY(-4px) scale(1.03);
        box-shadow: var(--shadow-xl), var(--shadow-colored);
        border-color: var(--border-hover);
    }

    [data-testid="metric-container"]:hover::before {
        opacity: 0.05;
    }

    [data-testid="metric-container"] [data-testid="metric-value"] {
        font-size: var(--text-3xl);
        font-weight: 900;
        background: linear-gradient(135deg, var(--primary), var(--primary-light));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: var(--space-2);
    }

    [data-testid="metric-container"] [data-testid="metric-label"] {
        font-size: var(--text-xs);
        color: var(--text-secondary);
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    /* Status Badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: var(--space-2);
        padding: var(--space-2) var(--space-4);
        border-radius: var(--radius-full);
        font-size: var(--text-xs);
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        position: relative;
        overflow: hidden;
        transition: var(--transition);
        cursor: pointer;
    }

    .status-badge::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: left 0.5s ease;
    }

    .status-badge:hover::before {
        left: 100%;
    }

    .status-excellent {
        background: linear-gradient(135deg, var(--success), var(--success-light));
        color: white;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3);
    }

    .status-good {
        background: linear-gradient(135deg, var(--primary), var(--primary-light));
        color: white;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
    }

    .status-progress {
        background: linear-gradient(135deg, var(--warning), var(--warning-light));
        color: white;
        box-shadow: 0 4px 20px rgba(245, 158, 11, 0.3);
    }

    .status-start {
        background: linear-gradient(135deg, var(--error), var(--error-light));
        color: white;
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.3);
    }

    /* Activity Timeline */
    .activity-timeline {
        margin: var(--space-6) 0;
        position: relative;
    }

    .activity-timeline::before {
        content: '';
        position: absolute;
        left: var(--space-6);
        top: 0;
        bottom: 0;
        width: 3px;
        background: linear-gradient(to bottom, var(--primary), var(--primary-light));
        opacity: 0.3;
        border-radius: var(--radius-full);
    }

    .timeline-item {
        display: flex;
        align-items: center;
        gap: var(--space-5);
        padding: var(--space-5) var(--space-6);
        margin: var(--space-3) 0;
        border-radius: var(--radius-xl);
        background: var(--bg-secondary);
        border: 2px solid var(--border-color);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }

    .timeline-item::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 4px;
        background: linear-gradient(to bottom, var(--primary), var(--primary-light));
        opacity: 0;
        transition: opacity 0.3s ease;
        border-radius: 0 var(--radius) var(--radius) 0;
    }

    .timeline-item:hover {
        background: var(--bg-tertiary);
        transform: translateX(8px) scale(1.02);
        box-shadow: var(--shadow-lg);
        border-color: var(--border-hover);
    }

    .timeline-item:hover::before {
        opacity: 1;
    }

    .timeline-item.completed {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(52, 211, 153, 0.05));
        border-color: var(--success);
    }

    .timeline-item.completed::before {
        background: linear-gradient(to bottom, var(--success), var(--success-light));
        opacity: 1;
    }

    .timeline-item.current {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(129, 140, 248, 0.05));
        border-color: var(--primary);
        animation: pulse 2s infinite;
    }

    .timeline-item.current::before {
        background: linear-gradient(to bottom, var(--primary), var(--primary-light));
        opacity: 1;
        animation: shimmer 2s infinite;
    }

    .timeline-checkbox {
        width: var(--space-6);
        height: var(--space-6);
        border-radius: var(--radius);
        border: 3px solid var(--border-color);
        background: var(--bg-secondary);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }

    .timeline-checkbox::before {
        content: '✓';
        color: white;
        font-weight: 800;
        font-size: var(--text-sm);
        opacity: 0;
        transform: scale(0);
        transition: all 0.3s var(--bounce);
    }

    .timeline-checkbox.checked {
        background: linear-gradient(135deg, var(--success), var(--success-light));
        border-color: var(--success);
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4);
    }

    .timeline-checkbox.checked::before {
        opacity: 1;
        transform: scale(1);
    }

    .timeline-content {
        flex: 1;
        min-width: 0;
    }

    .timeline-activity {
        font-size: var(--text-base);
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
        line-height: 1.4;
    }

    .timeline-meta {
        font-size: var(--text-xs);
        color: var(--text-secondary);
        margin: var(--space-1) 0 0 0;
        display: flex;
        gap: var(--space-3);
        align-items: center;
    }

    .timeline-duration {
        font-size: var(--text-xs);
        color: var(--text-tertiary);
        font-weight: 700;
        white-space: nowrap;
        background: var(--bg-tertiary);
        padding: var(--space-1) var(--space-3);
        border-radius: var(--radius-full);
        font-family: 'JetBrains Mono', monospace;
    }

    /* Quick Actions Grid */
    .quick-actions {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: var(--space-6);
        margin: var(--space-8) 0;
    }

    .action-card {
        background: var(--bg-secondary);
        border: 2px solid var(--border-color);
        border-radius: var(--radius-2xl);
        padding: var(--space-8);
        text-align: center;
        transition: var(--transition-slow);
        box-shadow: var(--shadow-lg);
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }

    .action-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary), var(--primary-light));
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.5s ease;
    }

    .action-card:hover {
        transform: translateY(-12px) scale(1.05);
        box-shadow: var(--shadow-xl), var(--shadow-colored);
        border-color: var(--border-hover);
    }

    .action-card:hover::before {
        transform: scaleX(1);
    }

    .action-icon {
        font-size: 4rem;
        margin-bottom: var(--space-4);
        transition: transform 0.3s ease;
        display: block;
    }

    .action-card:hover .action-icon {
        transform: scale(1.15) rotate(5deg);
    }

    .action-title {
        font-size: var(--text-lg);
        font-weight: 800;
        color: var(--text-primary);
        margin-bottom: var(--space-2);
    }

    .action-desc {
        font-size: var(--text-sm);
        color: var(--text-secondary);
        line-height: 1.6;
    }

    /* Enhanced Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: var(--space-2);
        border-bottom: 2px solid var(--border-color);
        margin-bottom: var(--space-8);
        background: var(--bg-secondary);
        border-radius: var(--radius-xl) var(--radius-xl) 0 0;
        padding: var(--space-3);
        box-shadow: var(--shadow);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: 2px solid transparent;
        border-radius: var(--radius-lg);
        padding: var(--space-4) var(--space-6);
        margin: 0;
        font-weight: 700;
        font-size: var(--text-sm);
        color: var(--text-secondary);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }

    .stTabs [data-baseweb="tab"]::before {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        width: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary), var(--primary-light));
        transition: all 0.3s ease;
        transform: translateX(-50%);
        border-radius: var(--radius-full);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary), var(--primary-light));
        color: white;
        box-shadow: var(--shadow-colored);
        transform: scale(1.05);
    }

    .stTabs [aria-selected="true"]::before {
        width: 100%;
    }

    /* Timer Display */
    .timer-display {
        background: var(--bg-secondary);
        border: 2px solid var(--border-color);
        border-radius: var(--radius-xl);
        padding: var(--space-6);
        text-align: center;
        margin: var(--space-4) 0;
        box-shadow: var(--shadow-lg);
    }

    .timer-time {
        font-size: var(--text-4xl);
        font-weight: 900;
        font-family: 'JetBrains Mono', monospace;
        background: linear-gradient(135deg, var(--primary), var(--primary-light));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: var(--space-2);
    }

    .timer-label {
        font-size: var(--text-sm);
        color: var(--text-secondary);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    /* Floating Action Button */
    .fab {
        position: fixed;
        bottom: var(--space-8);
        right: var(--space-8);
        width: 64px;
        height: 64px;
        border-radius: var(--radius-full);
        background: linear-gradient(135deg, var(--primary), var(--primary-light));
        border: none;
        box-shadow: var(--shadow-xl), var(--shadow-colored);
        color: white;
        font-size: var(--text-2xl);
        cursor: pointer;
        transition: var(--transition);
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .fab:hover {
        transform: scale(1.15) rotate(5deg);
        box-shadow: var(--shadow-xl), 0 25px 50px -12px rgba(99, 102, 241, 0.5);
    }

    /* Dark Mode Toggle */
    .theme-toggle {
        position: fixed;
        top: var(--space-4);
        right: var(--space-4);
        width: 48px;
        height: 48px;
        border-radius: var(--radius-full);
        background: var(--bg-secondary);
        border: 2px solid var(--border-color);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: var(--transition);
        z-index: 1000;
        font-size: var(--text-lg);
    }

    .theme-toggle:hover {
        transform: scale(1.1);
        box-shadow: var(--shadow-lg);
    }

    /* Animations */
    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }

    .fade-in { animation: fadeIn 0.5s ease-out; }
    .slide-up { animation: slideInUp 0.6s var(--bounce); }
    .slide-up-delay-1 { animation: slideInUp 0.6s var(--bounce) 0.1s both; }
    .slide-up-delay-2 { animation: slideInUp 0.6s var(--bounce) 0.2s both; }
    .slide-up-delay-3 { animation: slideInUp 0.6s var(--bounce) 0.3s both; }

    /* Responsive Design */
    @media (max-width: 1200px) {
        .quick-actions {
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        }
    }

    @media (max-width: 768px) {
        .enhanced-header {
            padding: var(--space-6) var(--space-8);
        }

        .enhanced-header h1 {
            font-size: var(--text-3xl);
        }

        .ultra-card {
            padding: var(--space-6);
        }

        .quick-actions {
            grid-template-columns: 1fr;
            gap: var(--space-4);
        }

        .main {
            padding: var(--space-4);
        }

        .fab {
            bottom: var(--space-4);
            right: var(--space-4);
            width: 56px;
            height: 56px;
        }
    }

    @media (max-width: 640px) {
        .enhanced-header h1 {
            font-size: var(--text-2xl);
        }

        .timeline-item {
            padding: var(--space-4);
        }

        .action-card {
            padding: var(--space-6);
        }
    }

    /* Hide Streamlit Elements */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    .stDeployButton { display: none; }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: var(--bg-tertiary);
        border-radius: var(--radius-full);
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(to bottom, var(--primary), var(--primary-light));
        border-radius: var(--radius-full);
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(to bottom, var(--primary-600), var(--primary));
    }

    /* Success, Warning, Error States */
    .success-glow {
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
        border-color: var(--success);
    }

    .warning-glow {
        box-shadow: 0 0 20px rgba(245, 158, 11, 0.3);
        border-color: var(--warning);
    }

    .error-glow {
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.3);
        border-color: var(--error);
    }

    /* Loading States */
    .loading {
        animation: pulse 1.5s infinite;
    }

    .skeleton {
        background: linear-gradient(90deg, var(--border-color) 25%, var(--bg-tertiary) 50%, var(--border-color) 75%);
        background-size: 200% 100%;
        animation: skeleton-loading 1.5s infinite;
        border-radius: var(--radius);
    }

    @keyframes skeleton-loading {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
</style>
""", unsafe_allow_html=True)


# Enhanced Data Models with Additional Features
class RoutineEntry:
    def __init__(self, start_time, end_time, activity, category, completed=False, notes="", priority="medium",
                 estimated_duration=None):
        self.start_time = start_time
        self.end_time = end_time
        self.activity = activity
        self.category = category
        self.completed = completed
        self.notes = notes
        self.priority = priority
        self.estimated_duration = estimated_duration
        self.id = f"{start_time}_{activity}".replace(" ", "_").replace(":", "")
        self.completion_time = None
        self.actual_duration = None

    @property
    def duration_minutes(self):
        try:
            start = datetime.strptime(self.start_time, "%H:%M")
            end = datetime.strptime(self.end_time, "%H:%M")
            return int((end - start).total_seconds() / 60)
        except:
            return 0

    @property
    def time_range(self):
        return f"{self.start_time} - {self.end_time}"

    @property
    def is_current(self):
        now = datetime.now().time()
        try:
            start = datetime.strptime(self.start_time, "%H:%M").time()
            end = datetime.strptime(self.end_time, "%H:%M").time()
            return start <= now <= end
        except:
            return False

    @property
    def is_upcoming(self):
        now = datetime.now().time()
        try:
            start = datetime.strptime(self.start_time, "%H:%M").time()
            return now < start
        except:
            return False

    @property
    def is_overdue(self):
        now = datetime.now().time()
        try:
            end = datetime.strptime(self.end_time, "%H:%M").time()
            return now > end and not self.completed
        except:
            return False


class DailyRoutine:
    def __init__(self, name, date, routine_type, entries, description="", goals=None, theme_color="primary"):
        self.name = name
        self.date = date
        self.routine_type = routine_type
        self.entries = entries
        self.description = description
        self.goals = goals or []
        self.theme_color = theme_color
        self.id = f"{date}_{name}".replace(" ", "_").replace("-", "_")
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

    @property
    def completion_rate(self):
        if not self.entries:
            return 0.0
        completed = sum(1 for entry in self.entries if entry.completed)
        return completed / len(self.entries)

    @property
    def completed_entries(self):
        return [entry for entry in self.entries if entry.completed]

    @property
    def pending_entries(self):
        return [entry for entry in self.entries if not entry.completed]

    @property
    def current_activity(self):
        return next((entry for entry in self.entries if entry.is_current), None)

    @property
    def next_activity(self):
        upcoming = [entry for entry in self.entries if entry.is_upcoming]
        return min(upcoming, key=lambda x: x.start_time) if upcoming else None

    @property
    def overdue_activities(self):
        return [entry for entry in self.entries if entry.is_overdue]

    @property
    def total_duration_minutes(self):
        return sum(entry.duration_minutes for entry in self.entries)

    @property
    def productivity_score(self):
        if not self.entries:
            return 0

        productive_categories = ["Work", "Study", "Exercise"]
        productive_time = sum(entry.duration_minutes for entry in self.completed_entries
                              if entry.category in productive_categories)
        total_time = self.total_duration_minutes

        return (productive_time / total_time * 100) if total_time > 0 else 0

    @property
    def category_breakdown(self):
        breakdown = {}
        for entry in self.entries:
            breakdown[entry.category] = breakdown.get(entry.category, 0) + 1
        return breakdown

    @property
    def time_efficiency(self):
        """Calculate how efficiently time is being used"""
        if not self.entries:
            return 0

        on_time_completions = sum(1 for entry in self.completed_entries
                                  if not entry.is_overdue)
        return (on_time_completions / len(self.entries) * 100) if self.entries else 0


# Initialize enhanced session state
def initialize_session_state():
    defaults = {
        'routines': [],
        'current_page': "Dashboard",
        'selected_date': datetime.now().date(),
        'theme': 'light',
        'timer_active': False,
        'timer_start': None,
        'timer_duration': 0,
        'current_timer_activity': None,
        'notifications': [],
        'user_preferences': {
            'default_routine_type': 'Weekday',
            'preferred_start_time': '06:00',
            'enable_notifications': True,
            'auto_advance_activities': False,
            'show_productivity_insights': True,
            'goal_tracking': True
        },
        'achievement_stats': {
            'total_routines_completed': 0,
            'longest_streak': 0,
            'total_activities_completed': 0,
            'favorite_category': 'Work'
        }
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


initialize_session_state()


class EnhancedRoutineApp:
    def __init__(self):
        self.categories = {
            "Work": {"icon": "💼", "color": "#3b82f6"},
            "Exercise": {"icon": "💪", "color": "#ef4444"},
            "Study": {"icon": "📚", "color": "#8b5cf6"},
            "Meal": {"icon": "🍽️", "color": "#10b981"},
            "Break": {"icon": "☕", "color": "#f59e0b"},
            "Recovery": {"icon": "😴", "color": "#6b7280"},
            "Other": {"icon": "📝", "color": "#64748b"}
        }

        self.priority_colors = {
            "high": "#ef4444",
            "medium": "#f59e0b",
            "low": "#10b981"
        }

    def render_header(self):
        """Render enhanced header with theme toggle"""
        current_time = datetime.now()
        hour = current_time.hour

        # Smart greeting based on time and user activity
        if 5 <= hour < 12:
            if st.session_state.routines:
                today_routine = self.get_today_routine()
                if today_routine and today_routine.completion_rate > 0:
                    greeting = "Great start! You're already making progress today 🌅"
                else:
                    greeting = "Good morning! Ready to make today amazing? 🌅"
            else:
                greeting = "Good morning! Let's create your first routine 🌅"
        elif 12 <= hour < 17:
            greeting = "Good afternoon! Keep up the momentum 🌞"
        elif 17 <= hour < 22:
            greeting = "Good evening! Time to finish strong 🌆"
        else:
            greeting = "Working late? Remember to rest well 🌙"

        # Calculate current streak
        streak = self.calculate_streak()
        streak_text = f"🔥 {streak} day streak" if streak > 0 else "Ready to start!"

        st.markdown(f"""
        <div class="enhanced-header">
            <h1>🎯 Daily Routine Manager
                <span class="header-badge">{streak_text}</span>
            </h1>
            <p>{greeting} • {current_time.strftime('%A, %B %d, %Y at %I:%M %p')}</p>
        </div>
        """, unsafe_allow_html=True)

        # Theme toggle button
        st.markdown(f"""
        <div class="theme-toggle" onclick="toggleTheme()" title="Toggle dark mode">
            {'🌙' if st.session_state.theme == 'light' else '☀️'}
        </div>
        <script>
            function toggleTheme() {{
                // This would toggle theme in a real implementation
                console.log('Theme toggle clicked');
            }}
        </script>
        """, unsafe_allow_html=True)

    def render_sidebar(self):
        """Render enhanced sidebar with smart stats"""
        with st.sidebar:
            # Enhanced Navigation
            st.markdown('<div class="nav-section">', unsafe_allow_html=True)
            st.markdown('<h3>🧭 Navigation</h3>', unsafe_allow_html=True)

            pages = [
                ("Dashboard", "🎯", self.get_dashboard_badge()),
                ("Routines", "📋", len(st.session_state.routines)),
                ("Analytics", "📈", "PRO" if len(st.session_state.routines) >= 3 else ""),
                ("Timer", "⏱️", "LIVE" if st.session_state.timer_active else ""),
                ("Goals", "🎯", len(st.session_state.user_preferences.get('goals', []))),
                ("Settings", "⚙️", "")
            ]

            for page, icon, badge in pages:
                is_active = st.session_state.current_page == page

                # Create button content with icon and badge
                if badge:
                    if badge == "LIVE":
                        badge_class = "error"
                    elif badge == "PRO":
                        badge_class = "success"
                    elif isinstance(badge, int) and badge > 0:
                        badge_class = ""
                    else:
                        badge_class = ""

                    button_content = f'{icon} {page}'
                else:
                    button_content = f'{icon} {page}'

                button_type = "primary" if is_active else "secondary"

                if st.button(button_content,
                             key=f"nav_{page}",
                             use_container_width=True,
                             type=button_type):
                    st.session_state.current_page = page
                    st.rerun()

                # Display badge separately if exists
                if badge:
                    st.markdown(f"""
                    <div style="text-align: right; margin-top: -35px; margin-bottom: 10px; margin-right: 10px;">
                        <span class="nav-badge {badge_class if 'badge_class' in locals() else ''}">{badge}</span>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

            # Enhanced Stats
            self.render_sidebar_stats()

            # Quick Date Navigation
            self.render_sidebar_date_nav()

            # Active Timer Display
            if st.session_state.timer_active:
                self.render_timer_sidebar()

    def render_sidebar_stats(self):
        """Render enhanced statistics in sidebar"""
        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown('<h3>📊 Today\'s Pulse</h3>', unsafe_allow_html=True)

        today_routine = self.get_today_routine()

        if today_routine:
            completion_rate = today_routine.completion_rate * 100
            productivity = today_routine.productivity_score
            efficiency = today_routine.time_efficiency
            momentum = self.calculate_momentum()

            # Display metrics in a clean format
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Progress", f"{completion_rate:.0f}%",
                          delta=f"+{productivity:.0f} prod" if productivity > 50 else None)
            with col2:
                st.metric("Momentum", f"{momentum}/10",
                          delta=f"{efficiency:.0f}% eff" if efficiency > 70 else None)

            # Current activity status
            current = today_routine.current_activity
            if current:
                st.info(f"🔄 **Now**: {current.activity[:25]}...")
                time_left = self.calculate_time_remaining(current)
                if time_left:
                    st.caption(f"⏰ {time_left} remaining")
            else:
                next_activity = today_routine.next_activity
                if next_activity:
                    time_until = self.calculate_time_until(next_activity)
                    st.success(f"⏭️ **Next**: {next_activity.activity[:25]}...")
                    if time_until:
                        st.caption(f"⏰ Starting in {time_until}")
                else:
                    st.success("🎉 **Status**: All done!")
        else:
            # Show overall stats when no today routine
            streak = self.calculate_streak()
            total_routines = len(st.session_state.routines)

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Streak", f"{streak} days")
            with col2:
                st.metric("Routines", total_routines)

            if total_routines > 0:
                avg_completion = sum(r.completion_rate for r in st.session_state.routines) / total_routines * 100
                st.metric("Average", f"{avg_completion:.0f}%")

            st.info("📋 **Status**: Ready to plan today!")

        st.markdown('</div>', unsafe_allow_html=True)

    def render_sidebar_date_nav(self):
        """Render date navigation in sidebar"""
        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown('<h3>📅 Time Travel</h3>', unsafe_allow_html=True)

        # Date picker
        selected_date = st.date_input(
            "Jump to date",
            value=st.session_state.selected_date,
            label_visibility="collapsed"
        )

        if selected_date != st.session_state.selected_date:
            st.session_state.selected_date = selected_date
            st.rerun()

        # Quick navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📍 Today", use_container_width=True, key="quick_today"):
                st.session_state.selected_date = datetime.now().date()
                st.rerun()
        with col2:
            if st.button("➡️ Tomorrow", use_container_width=True, key="quick_tomorrow"):
                st.session_state.selected_date = datetime.now().date() + timedelta(days=1)
                st.rerun()

        # Week navigation
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Last Week", use_container_width=True, key="prev_week_nav"):
                st.session_state.selected_date -= timedelta(days=7)
                st.rerun()
        with col2:
            if st.button("Next Week ➡️", use_container_width=True, key="next_week_nav"):
                st.session_state.selected_date += timedelta(days=7)
                st.rerun()

        # Show selected date info
        if st.session_state.selected_date != datetime.now().date():
            selected_routine = next((r for r in st.session_state.routines
                                     if r.date == st.session_state.selected_date.isoformat()), None)
            if selected_routine:
                st.success(f"📋 Found routine: {selected_routine.name}")
                st.caption(f"Completion: {selected_routine.completion_rate:.0%}")
            else:
                st.warning("📭 No routine for selected date")

        st.markdown('</div>', unsafe_allow_html=True)

    def get_dashboard_badge(self):
        """Get dynamic dashboard badge"""
        today_routine = self.get_today_routine()
        if today_routine:
            completion = today_routine.completion_rate * 100
            if completion >= 90:
                return "🔥"
            elif completion >= 70:
                return f"{completion:.0f}%"
            elif completion >= 50:
                return "📈"
            else:
                return "🚀"
        return "NEW"

    def render_timer_sidebar(self):
        """Render active timer in sidebar"""
        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown('<h3>⏱️ Focus Timer</h3>', unsafe_allow_html=True)

        if st.session_state.timer_active and st.session_state.timer_start:
            elapsed = (datetime.now() - st.session_state.timer_start).total_seconds()
            remaining = max(0, st.session_state.timer_duration * 60 - elapsed)

            minutes = int(remaining // 60)
            seconds = int(remaining % 60)

            # Timer display
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; background: var(--bg-tertiary); 
                        border-radius: var(--radius-lg); margin: 1rem 0;">
                <div style="font-size: 2rem; font-weight: 900; font-family: 'JetBrains Mono', monospace;
                           background: linear-gradient(135deg, var(--primary), var(--primary-light));
                           -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    {minutes:02d}:{seconds:02d}
                </div>
                <div style="font-size: 0.75rem; color: var(--text-secondary); font-weight: 600;
                           text-transform: uppercase; letter-spacing: 0.1em; margin-top: 0.5rem;">
                    {st.session_state.current_timer_activity or 'Focus Session'}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Timer controls
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⏸️ Pause", use_container_width=True, key="pause_timer"):
                    # In a real app, implement pause functionality
                    st.info("Pause feature coming soon!")
            with col2:
                if st.button("⏹️ Stop", use_container_width=True, key="stop_timer"):
                    st.session_state.timer_active = False
                    st.session_state.timer_start = None
                    st.session_state.current_timer_activity = None
                    st.success("Timer stopped!")
                    st.rerun()

            # Progress bar for timer
            progress = 1 - (remaining / (st.session_state.timer_duration * 60))
            st.progress(progress, text=f"Progress: {progress * 100:.0f}%")

        st.markdown('</div>', unsafe_allow_html=True)

    def get_today_routine(self):
        """Get today's routine"""
        today = datetime.now().date().isoformat()
        return next((r for r in st.session_state.routines if r.date == today), None)

    def calculate_streak(self):
        """Calculate current completion streak"""
        if not st.session_state.routines:
            return 0

        streak = 0
        current_date = datetime.now().date()

        while True:
            routine = next((r for r in st.session_state.routines
                            if r.date == current_date.isoformat()), None)

            if routine and routine.completion_rate >= 0.8:
                streak += 1
                current_date -= timedelta(days=1)
            else:
                break

        return streak

    def calculate_momentum(self):
        """Calculate momentum score based on recent performance"""
        if not st.session_state.routines:
            return 5

        recent_routines = sorted(st.session_state.routines, key=lambda x: x.date)[-3:]
        if not recent_routines:
            return 5

        avg_completion = sum(r.completion_rate for r in recent_routines) / len(recent_routines)
        momentum = min(10, int(avg_completion * 12))  # Scale to 0-10

        return momentum

    def render_main_content(self):
        """Render main content based on current page"""
        content_map = {
            "Dashboard": self.render_dashboard,
            "Routines": self.render_routines,
            "Analytics": self.render_analytics,
            "Timer": self.render_timer,
            "Goals": self.render_goals,
            "Settings": self.render_settings
        }

        if st.session_state.current_page in content_map:
            content_map[st.session_state.current_page]()

    def render_dashboard(self):
        """Render enhanced dashboard"""
        st.markdown('<div class="slide-up">', unsafe_allow_html=True)
        st.markdown("## 🚀 Mission Control")
        st.markdown('</div>', unsafe_allow_html=True)

        today_routine = self.get_today_routine()

        if not today_routine:
            self.render_smart_onboarding()
        else:
            self.render_enhanced_routine_card(today_routine)
            self.render_smart_actions()

        # Show insights if user has data
        if len(st.session_state.routines) >= 3:
            self.render_dashboard_insights()

        # Show recent activity
        if st.session_state.routines:
            self.render_recent_activity()

    def render_smart_onboarding(self):
        """Render smart onboarding with time-based suggestions"""
        hour = datetime.now().hour

        if 5 <= hour < 9:
            suggestion = "Perfect timing! Morning routines set the tone for success."
            recommended = "Morning Powerhouse"
        elif 9 <= hour < 17:
            suggestion = "Great! Let's build a productive workday routine."
            recommended = "Workday Excellence"
        else:
            suggestion = "Evening routines help you wind down and prepare for tomorrow."
            recommended = "Evening Mastery"

        st.markdown(f"""
        <div class="ultra-card slide-up">
            <h3>🌟 Welcome to Your Journey!</h3>
            <p>{suggestion}</p>
            <p><strong>💡 Recommended:</strong> {recommended}</p>
        </div>
        """, unsafe_allow_html=True)

        # Enhanced quick start options
        st.markdown('<div class="quick-actions slide-up-delay-1">', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("💼 Productive Weekday", use_container_width=True, type="primary"):
                self.create_enhanced_weekday()
                st.success("🎉 Created your productive weekday routine!")
                st.rerun()
            st.caption("⭐ Recommended • Balanced work and wellness")

        with col2:
            if st.button("🏖️ Relaxed Weekend", use_container_width=True):
                self.create_enhanced_weekend()
                st.success("🎉 Created your relaxed weekend routine!")
                st.rerun()
            st.caption("Perfect for rest and recharge")

        with col3:
            if st.button("🎨 Custom Builder", use_container_width=True):
                st.session_state.current_page = "Routines"
                st.rerun()
            st.caption("Build exactly what you need")

        st.markdown('</div>', unsafe_allow_html=True)

        # Show smart tips
        self.render_smart_tips()

    def render_enhanced_routine_card(self, routine):
        """Render enhanced routine card with smart features"""
        completion_rate = routine.completion_rate * 100

        # Determine status with enhanced logic
        current_activity = routine.current_activity
        overdue_count = len(routine.overdue_activities)

        if completion_rate >= 90:
            status_class = "status-excellent"
            status_text = "🏆 Champion"
            status_msg = "You're absolutely crushing it today!"
        elif completion_rate >= 75:
            status_class = "status-excellent"
            status_text = "🔥 On Fire"
            status_msg = "Keep this momentum going!"
        elif completion_rate >= 50:
            status_class = "status-good"
            status_text = "💪 Strong"
            status_msg = "Great progress, keep pushing!"
        elif overdue_count > 0:
            status_class = "status-start"
            status_text = "⚡ Focus"
            status_msg = f"{overdue_count} activities need attention"
        else:
            status_class = "status-progress"
            status_text = "🚀 Building"
            status_msg = "Every step counts!"

        st.markdown(f"""
        <div class="ultra-card slide-up">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem;">
                <div>
                    <h3 style="font-size: 1.75rem; font-weight: 800; margin: 0; color: var(--text-primary);">
                        {routine.name}
                    </h3>
                    <p style="color: var(--text-secondary); margin: 0.5rem 0 0 0; font-weight: 500;">
                        {routine.date} • {routine.routine_type} • {status_msg}
                    </p>
                </div>
                <span class="status-badge {status_class}">{status_text}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Enhanced progress with predictions
        time_progress = self.calculate_day_progress()
        predicted = self.predict_final_completion(routine, time_progress)

        progress_text = f"{completion_rate:.0f}% complete"
        if predicted > completion_rate + 5:
            progress_text += f" • Predicted: {predicted:.0f}%"

        st.progress(completion_rate / 100, text=progress_text)

        # Enhanced metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Completed", f"{len(routine.completed_entries)}/{len(routine.entries)}")
        with col2:
            st.metric("Duration", f"{routine.total_duration_minutes}m")
        with col3:
            st.metric("Productivity", f"{routine.productivity_score:.0f}/100")
        with col4:
            remaining = len(routine.pending_entries)
            st.metric("Remaining", remaining)

        # Current status with smart insights
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**🔄 Right Now**")
            if current_activity:
                time_left = self.calculate_time_remaining(current_activity)
                st.markdown(f"**{current_activity.activity}**")
                st.caption(f"{current_activity.time_range} • {current_activity.category}")
                if time_left:
                    st.caption(f"⏰ {time_left} remaining")

                # Add focus button for current activity
                if not current_activity.completed:
                    if st.button("🎯 Start Focus Timer", key="focus_current"):
                        self.start_focus_timer(current_activity)
                        st.rerun()
            else:
                next_activity = routine.next_activity
                if next_activity:
                    time_until = self.calculate_time_until(next_activity)
                    st.markdown("**Free Time**")
                    st.caption(f"Next: {next_activity.activity}")
                    if time_until:
                        st.caption(f"⏰ Starting in {time_until}")
                else:
                    st.markdown("**🎉 All Done!**")
                    st.caption("Amazing work today!")

        with col2:
            st.markdown("**⏭️ Coming Up**")
            next_activity = routine.next_activity
            if next_activity:
                time_until = self.calculate_time_until(next_activity)
                st.markdown(f"**{next_activity.activity}**")
                st.caption(f"{next_activity.time_range} • {next_activity.category}")
                if time_until:
                    st.caption(f"⏰ Starting in {time_until}")
            else:
                st.markdown("**Day Complete!**")
                st.caption("🏆 Time to celebrate!")

        # Enhanced activity timeline
        if routine.entries:
            with st.expander(f"📋 Smart Timeline ({len(routine.entries)} activities)", expanded=False):
                self.render_smart_timeline(routine)

    def render_smart_timeline(self, routine):
        """Render smart timeline with enhanced features"""
        st.markdown('<div class="activity-timeline">', unsafe_allow_html=True)

        sorted_entries = sorted(routine.entries, key=lambda x: x.start_time)

        for i, entry in enumerate(sorted_entries):
            # Determine status and styling
            item_classes = ["timeline-item"]

            if entry.completed:
                item_classes.append("completed")
            elif entry.is_current:
                item_classes.append("current")
            elif entry.is_overdue:
                item_classes.append("overdue")

            checkbox_class = "checked" if entry.completed else ""

            # Status indicator
            if entry.is_current:
                status_indicator = "🔄 NOW"
            elif entry.is_upcoming:
                time_until = self.calculate_time_until(entry)
                status_indicator = f"⏰ {time_until}" if time_until else "⏰ Soon"
            elif entry.is_overdue:
                status_indicator = "⚠️ Overdue"
            elif entry.completed:
                status_indicator = "✅ Done"
            else:
                status_indicator = ""

            # Priority indicator
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(entry.priority, "")

            st.markdown(f"""
            <div class="{' '.join(item_classes)}">
                <div class="timeline-checkbox {checkbox_class}">
                    {'✓' if entry.completed else ''}
                </div>
                <div class="timeline-content">
                    <div class="timeline-activity">
                        {priority_emoji} {entry.activity}
                    </div>
                    <div class="timeline-meta">
                        <span>{entry.time_range}</span>
                        <span>•</span>
                        <span>{entry.category}</span>
                        {f'<span>• {status_indicator}</span>' if status_indicator else ''}
                        {f'<span>• {entry.notes}</span>' if entry.notes else ''}
                    </div>
                </div>
                <div class="timeline-duration">{entry.duration_minutes}m</div>
            </div>
            """, unsafe_allow_html=True)

            # Enhanced controls
            col1, col2, col3, col4 = st.columns([5, 2, 2, 2])

            with col2:
                if st.button("✓", key=f"toggle_{entry.id}_{i}", help="Toggle completion"):
                    entry.completed = not entry.completed
                    entry.completion_time = datetime.now().isoformat() if entry.completed else None
                    st.rerun()

            with col3:
                if not entry.completed and (entry.is_current or entry.is_upcoming):
                    if st.button("⏱️", key=f"timer_{entry.id}_{i}", help="Start timer"):
                        self.start_focus_timer(entry)
                        st.rerun()

            with col4:
                if st.button("📝", key=f"edit_{entry.id}_{i}", help="Quick edit"):
                    self.show_quick_edit(entry)

        st.markdown('</div>', unsafe_allow_html=True)

    def render_smart_actions(self):
        """Render smart action buttons"""
        st.markdown("### ⚡ Smart Actions")

        today_routine = self.get_today_routine()

        # Generate contextual actions
        actions = []

        if today_routine:
            current_activity = today_routine.current_activity
            overdue = today_routine.overdue_activities

            # Always available
            actions.append(("✅ Quick Complete", "Mark multiple tasks done", "complete"))
            actions.append(("➕ Add Activity", "Add new activity", "add"))

            # Contextual actions
            if current_activity and not current_activity.completed:
                actions.append(("🎯 Focus Mode", f"Focus on {current_activity.activity[:20]}...", "focus"))

            if overdue:
                actions.append(("⚡ Catch Up", f"Address {len(overdue)} overdue items", "catchup"))

            if today_routine.completion_rate < 0.5:
                actions.append(("🔧 Optimize", "Get AI suggestions", "optimize"))

            actions.append(("📊 Analyze", "View detailed insights", "analyze"))
        else:
            actions = [
                ("📋 Create Routine", "Build today's routine", "create"),
                ("📄 Use Template", "Start from template", "template"),
                ("🔄 Copy Previous", "Duplicate recent routine", "copy"),
                ("📈 View Progress", "See your journey", "progress")
            ]

        # Render actions in grid
        st.markdown('<div class="quick-actions slide-up-delay-2">', unsafe_allow_html=True)

        cols = st.columns(min(len(actions), 4))
        for i, (title, desc, action_type) in enumerate(actions):
            with cols[i % len(cols)]:
                if st.button(f"{title}\n\n{desc}", key=f"action_{action_type}", use_container_width=True):
                    self.handle_smart_action(action_type, today_routine)

        st.markdown('</div>', unsafe_allow_html=True)

    def handle_smart_action(self, action_type, routine):
        """Handle smart action clicks"""
        if action_type == "complete":
            self.show_quick_complete(routine)
        elif action_type == "add":
            self.show_quick_add(routine)
        elif action_type == "focus" and routine and routine.current_activity:
            self.start_focus_timer(routine.current_activity)
            st.rerun()
        elif action_type == "catchup":
            self.handle_catchup(routine)
        elif action_type == "optimize":
            self.show_optimization_suggestions(routine)
        elif action_type == "analyze":
            st.session_state.current_page = "Analytics"
            st.rerun()
        elif action_type == "create":
            st.session_state.current_page = "Routines"
            st.rerun()
        elif action_type == "template":
            self.show_template_selector()
        elif action_type == "copy":
            self.duplicate_recent_routine()
        elif action_type == "progress":
            st.session_state.current_page = "Analytics"
            st.rerun()

    def show_quick_complete(self, routine):
        """Show quick completion interface"""
        st.markdown("### ✅ Quick Complete")

        if not routine or not routine.pending_entries:
            st.info("All activities are already completed! 🎉")
            return

        incomplete = routine.pending_entries

        # Smart suggestions for what to complete
        suggested = self.suggest_completion_order(incomplete)

        st.info(f"💡 **Smart Suggestion**: Complete '{suggested[0].activity}' first for maximum momentum!")

        selected_ids = []
        for entry in incomplete:
            is_suggested = entry in suggested[:3]
            label = f"{'⭐ ' if is_suggested else ''}{entry.activity} ({entry.time_range})"

            if st.checkbox(label, key=f"quick_complete_{entry.id}"):
                selected_ids.append(entry.id)

        if selected_ids:
            if st.button("🚀 Complete Selected", type="primary"):
                for entry in routine.entries:
                    if entry.id in selected_ids:
                        entry.completed = True
                        entry.completion_time = datetime.now().isoformat()

                st.success(f"🎉 Completed {len(selected_ids)} activities!")
                st.balloons()
                st.rerun()

    def suggest_completion_order(self, entries):
        """Suggest optimal completion order"""
        now = datetime.now().time()

        scored_entries = []
        for entry in entries:
            score = 0

            # Prioritize overdue items
            if entry.is_overdue:
                score += 10

            # Prioritize current activity
            if entry.is_current:
                score += 8

            # Prioritize by priority level
            priority_scores = {"high": 6, "medium": 4, "low": 2}
            score += priority_scores.get(entry.priority, 4)

            # Prioritize shorter tasks (quick wins)
            if entry.duration_minutes <= 15:
                score += 3
            elif entry.duration_minutes <= 30:
                score += 2

            scored_entries.append((score, entry))

        scored_entries.sort(key=lambda x: x[0], reverse=True)
        return [entry for score, entry in scored_entries]

    def show_quick_add(self, routine):
        """Show quick add activity interface"""
        st.markdown("### ➕ Quick Add Activity")

        with st.form("quick_add_form"):
            col1, col2 = st.columns(2)

            with col1:
                activity = st.text_input("Activity", placeholder="e.g., Team standup")
                start_time = st.time_input("Start time", value=self.suggest_next_time_slot(routine))

            with col2:
                duration = st.number_input("Duration (min)", min_value=5, max_value=480, value=30)
                category = st.selectbox("Category", list(self.categories.keys()))

            priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)
            notes = st.text_input("Notes (optional)")

            if st.form_submit_button("🚀 Add Activity", type="primary"):
                if activity and routine:
                    end_time = (datetime.combine(datetime.today(), start_time) +
                                timedelta(minutes=duration)).time()

                    new_entry = RoutineEntry(
                        start_time.strftime("%H:%M"),
                        end_time.strftime("%H:%M"),
                        activity,
                        category,
                        notes=notes,
                        priority=priority
                    )

                    routine.entries.append(new_entry)
                    routine.updated_at = datetime.now().isoformat()

                    st.success(f"✨ Added '{activity}' to your routine!")
                    st.rerun()

    def suggest_next_time_slot(self, routine):
        """Suggest next available time slot"""
        if not routine or not routine.entries:
            return datetime.now().time()

        # Find the latest end time
        latest_entry = max(routine.entries, key=lambda x: x.end_time)
        latest_end = datetime.strptime(latest_entry.end_time, "%H:%M").time()

        # Add 15 minutes buffer
        next_time = (datetime.combine(datetime.today(), latest_end) +
                     timedelta(minutes=15)).time()

        return next_time

    def start_focus_timer(self, activity):
        """Start focus timer for activity"""
        st.session_state.timer_active = True
        st.session_state.timer_start = datetime.now()
        st.session_state.timer_duration = activity.duration_minutes
        st.session_state.current_timer_activity = activity.activity

        st.success(f"🎯 Focus timer started for '{activity.activity}' ({activity.duration_minutes} minutes)")

    def calculate_day_progress(self):
        """Calculate how much of the day has passed"""
        now = datetime.now()
        start_of_day = now.replace(hour=6, minute=0, second=0, microsecond=0)
        end_of_day = now.replace(hour=22, minute=0, second=0, microsecond=0)

        if now < start_of_day:
            return 0
        elif now > end_of_day:
            return 1
        else:
            total_duration = (end_of_day - start_of_day).total_seconds()
            elapsed = (now - start_of_day).total_seconds()
            return elapsed / total_duration

    def predict_final_completion(self, routine, time_progress):
        """Predict final completion rate"""
        if time_progress == 0:
            return 0

        current_completion = routine.completion_rate
        efficiency = current_completion / max(time_progress, 0.1)

        # Factor in user's historical performance
        user_efficiency = self.calculate_user_efficiency()
        adjusted_efficiency = (efficiency + user_efficiency) / 2

        predicted = min(100, current_completion + (adjusted_efficiency * (1 - time_progress)) * 100)
        return predicted

    def calculate_user_efficiency(self):
        """Calculate user's historical efficiency"""
        if len(st.session_state.routines) < 3:
            return 1.0

        recent_routines = st.session_state.routines[-5:]
        avg_completion = sum(r.completion_rate for r in recent_routines) / len(recent_routines)

        return avg_completion * 1.2  # Slight optimism factor

    def calculate_time_remaining(self, activity):
        """Calculate time remaining for activity"""
        try:
            now = datetime.now().time()
            end_time = datetime.strptime(activity.end_time, "%H:%M").time()

            now_dt = datetime.combine(datetime.today(), now)
            end_dt = datetime.combine(datetime.today(), end_time)

            if end_dt > now_dt:
                diff = end_dt - now_dt
                minutes = int(diff.total_seconds() / 60)
                if minutes > 60:
                    hours = minutes // 60
                    mins = minutes % 60
                    return f"{hours}h {mins}m"
                else:
                    return f"{minutes}m"
        except:
            pass
        return None

    def calculate_time_until(self, activity):
        """Calculate time until activity starts"""
        try:
            now = datetime.now().time()
            start_time = datetime.strptime(activity.start_time, "%H:%M").time()

            now_dt = datetime.combine(datetime.today(), now)
            start_dt = datetime.combine(datetime.today(), start_time)

            if start_dt > now_dt:
                diff = start_dt - now_dt
                minutes = int(diff.total_seconds() / 60)
                if minutes > 60:
                    hours = minutes // 60
                    mins = minutes % 60
                    return f"{hours}h {mins}m"
                else:
                    return f"{minutes}m"
        except:
            pass
        return None

    def render_smart_tips(self):
        """Render smart tips for new users"""
        tips = [
            "🎯 Start with 5-7 activities per day for best results",
            "⏰ Schedule breaks every 2 hours to maintain focus",
            "🔥 Consistent completion builds powerful momentum",
            "📱 Use the timer feature to stay focused on tasks"
        ]

        st.markdown('<div class="ultra-card slide-up-delay-3">', unsafe_allow_html=True)
        st.markdown("### 💡 Success Tips")
        for tip in tips:
            st.markdown(f"- {tip}")
        st.markdown('</div>', unsafe_allow_html=True)

    def create_enhanced_weekday(self):
        """Create enhanced weekday routine with smart defaults"""
        entries = [
            RoutineEntry("06:00", "06:30", "Morning Energizer", "Recovery", priority="medium"),
            RoutineEntry("06:30", "07:30", "Power Workout", "Exercise", priority="high"),
            RoutineEntry("07:30", "08:00", "Fuel Breakfast", "Meal", priority="high"),
            RoutineEntry("08:00", "10:00", "Deep Work Block 1", "Work", priority="high"),
            RoutineEntry("10:00", "10:15", "Energy Break", "Break", priority="low"),
            RoutineEntry("10:15", "12:00", "Creative Work", "Work", priority="high"),
            RoutineEntry("12:00", "13:00", "Power Lunch", "Meal", priority="medium"),
            RoutineEntry("13:00", "15:00", "Focused Work", "Work", priority="high"),
            RoutineEntry("15:00", "15:15", "Refresh Break", "Break", priority="low"),
            RoutineEntry("15:15", "17:00", "Skill Building", "Study", priority="medium"),
            RoutineEntry("17:30", "18:30", "Growth Time", "Study", priority="medium"),
            RoutineEntry("18:30", "19:30", "Nourish Dinner", "Meal", priority="medium"),
            RoutineEntry("19:30", "21:00", "Personal Excellence", "Other", priority="low"),
            RoutineEntry("21:00", "22:00", "Wind Down", "Recovery", priority="medium")
        ]

        routine = DailyRoutine(
            "Productive Weekday Elite",
            datetime.now().date().isoformat(),
            "Weekday",
            entries,
            "AI-optimized weekday routine for peak performance and balanced living",
            goals=["Complete all high-priority tasks", "Maintain energy throughout day"],
            theme_color="primary"
        )

        st.session_state.routines.append(routine)

    def create_enhanced_weekend(self):
        """Create enhanced weekend routine"""
        entries = [
            RoutineEntry("07:30", "08:00", "Gentle Wake Up", "Recovery", priority="low"),
            RoutineEntry("08:00", "09:00", "Leisurely Breakfast", "Meal", priority="medium"),
            RoutineEntry("09:00", "10:00", "Light Movement", "Exercise", priority="medium"),
            RoutineEntry("10:00", "12:00", "Creative Projects", "Other", priority="high"),
            RoutineEntry("12:00", "13:00", "Social Lunch", "Meal", priority="medium"),
            RoutineEntry("13:00", "15:00", "Adventure Time", "Other", priority="high"),
            RoutineEntry("15:00", "15:30", "Recharge Break", "Break", priority="low"),
            RoutineEntry("15:30", "17:00", "Personal Growth", "Study", priority="medium"),
            RoutineEntry("17:00", "18:00", "Reflect & Plan", "Recovery", priority="medium"),
            RoutineEntry("18:00", "19:00", "Weekend Feast", "Meal", priority="medium"),
            RoutineEntry("19:00", "21:00", "Social & Fun", "Other", priority="high"),
            RoutineEntry("21:00", "22:00", "Peaceful Evening", "Recovery", priority="medium")
        ]

        routine = DailyRoutine(
            "Weekend Recharge",
            datetime.now().date().isoformat(),
            "Weekend",
            entries,
            "Perfect weekend routine for rest, creativity, and connection",
            goals=["Recharge energy", "Connect with others", "Pursue passions"],
            theme_color="success"
        )

        st.session_state.routines.append(routine)

    # Placeholder methods for other pages
    def render_routines(self):
        st.markdown("## 📋 Advanced Routine Management")
        st.info("🚧 Advanced routine management features coming soon!")

    def render_analytics(self):
        st.markdown("## 📈 Smart Analytics")
        st.info("🚧 Advanced analytics with AI insights coming soon!")

    def render_timer(self):
        st.markdown("## ⏱️ Focus Timer")
        st.info("🚧 Advanced timer features coming soon!")

    def render_goals(self):
        st.markdown("## 🎯 Goal Tracking")
        st.info("🚧 Goal tracking features coming soon!")

    def render_settings(self):
        st.markdown("## ⚙️ Advanced Settings")
        st.info("🚧 Advanced settings coming soon!")

    def show_quick_edit(self, entry):
        st.info(f"Quick edit for '{entry.activity}' - Feature coming soon!")

    def handle_catchup(self, routine):
        st.info("Catch up mode - Feature coming soon!")

    def show_optimization_suggestions(self, routine):
        st.info("AI optimization suggestions - Feature coming soon!")

    def show_template_selector(self):
        st.info("Template selector - Feature coming soon!")

    def duplicate_recent_routine(self):
        st.info("Duplicate recent routine - Feature coming soon!")

    def render_dashboard_insights(self):
        st.info("Dashboard insights - Feature coming soon!")

    def render_recent_activity(self):
        st.info("Recent activity feed - Feature coming soon!")

    def run(self):
        """Run the enhanced application"""
        self.render_header()
        self.render_sidebar()
        self.render_main_content()


def main():
    """Main application entry point"""
    try:
        app = EnhancedRoutineApp()
        app.run()
    except Exception as e:
        st.error(f"⚠️ Application Error: {e}")
        st.info("🔄 Try refreshing the page. If the issue persists, please check the console.")

        with st.expander("🔧 Technical Details", expanded=False):
            st.code(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
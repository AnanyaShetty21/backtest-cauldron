# 📈 Golden & Death Crossover Finder (Dhan API + PySide6 GUI)

A simple GUI tool to identify **Golden** and **Death** crossovers using historical stock data from the **DhanHQ API**. Built with Python and PySide6.

---

## 🛠 Prerequisites

1. 🔑 **Dhan Data API Access**  
   - Ensure you have a **Dhan Client ID** and **Access Token** with API access enabled.  
   - [DhanHQ Developer Portal](https://dev.dhan.co)

2. 🐍 **Python**  
   - Install the latest version of Python (preferably 3.8+).

3. 📦 **Install Dependencies**  
   Create a virtual environment (optional), then install required libraries:
   ```bash
   pip install PySide6>=6.0.0 pandas>=1.0.0 dhanhq
   ```

---

## 📁 Setup Instructions

1. **Download the following files** and save them in the same (preferably empty) folder:
   - `golden_and_death_gui.py`
   - `midcap_symbol_with_security_ids.csv`

2. **Open your terminal/command prompt**, navigate to the folder, and run:
   - On **Windows**:
     ```bash
     python golden_and_death_gui.py
     ```
   - On **macOS/Linux**:
     ```bash
     python3 golden_and_death_gui.py
     ```

---

## 🖥 GUI Preview

When the app launches, you'll see the following window:

<img width="975" height="723" alt="GUI Preview" src="https://github.com/user-attachments/assets/9520b766-aaf7-4c03-86b2-cff66723042a" />

---

## 📋 How to Use

1. Enter your:
   - **Client ID**
   - **Access Token**
   - **Ticker** (Only stocks from the Nifty Midcap 150 are supported. Refer to `midcap_symbol_with_security_ids.csv`)
   - **From Date** and **To Date**

2. Click **Submit**  
   (If the button is disabled, verify all fields are correctly filled.)

3. The tool will display the **Golden Crossover** and **Death Crossover** dates:

---

## ✅ Example Output

<img width="975" height="724" alt="Example Output" src="https://github.com/user-attachments/assets/c9baec25-0655-47d6-a29c-0cefabf4da47" />

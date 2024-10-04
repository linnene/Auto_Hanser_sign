# Auto_Hanser_sign User Guide

## Introduction
**Auto_Hanser_sign** is a Python-based automation script designed to automate the sign-in process for the 毛怪俱乐部 (Mao Guai Club). This guide will walk you through the setup and use of the project.

## Prerequisites
- ![Python](https://img.shields.io/badge/Python-3.x-blue) Python 3.x
- ![Git](https://img.shields.io/badge/Git-2.x-orange) Git
- ![PushPlus](https://img.shields.io/badge/PushPlus-API%20Token-green) PushPlus API token (for notifications)

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/linnene/Auto_Hanser_sign.git
   cd Auto_Hanser_sign
   ```

2. **Install dependencies:**
   Navigate to the project directory and install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure settings:**
   - Open the `setting.json` file.
   - Input your required configurations, such as PushPlus token for notifications.

4. **Run the script:**
   To initiate the sign-in process, simply run:
   ```bash
   python main.py
   ```

## Notifications via PushPlus
This script supports PushPlus notifications, allowing you to receive status updates after each sign-in attempt. Ensure that your PushPlus token is correctly set in the `setting.json` file.

## Files and Structure
- **`main.py`**: Core script that executes the sign-in process.
- **`pushplus_utils.py`**: Handles PushPlus notifications.
- **`requirements.txt`**: Lists required dependencies.
- **`setting.json`**: Configuration file for user-specific settings.

## License
This project is licensed under the MIT License.

For more detailed information, visit the repository: [Auto_Hanser_sign](https://github.com/linnene/Auto_Hanser_sign).

---

This guide should help you quickly get started with the project!
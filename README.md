# Crunchyroll Account Checker

## Overview
The **Crunchyroll Account Checker** is a multi-threaded tool designed to verify Crunchyroll accounts. It checks the validity of account credentials using the Crunchyroll API and can handle multiple accounts and proxies concurrently, providing results on valid, invalid, custom, and premium accounts.

---

## Features
- **Multi-threaded:** Supports up to 250 threads for fast and efficient account checking.
- **Proxy Support:** Automatically uses proxies from a `proxies.txt` file (supports both proxy with and without authentication).
- **Account Categorization:**
  - **Valid Accounts:** Accounts with a valid login.
  - **Custom Accounts:** Accounts that require additional verification (A2F).
  - **Premium Accounts:** Accounts with premium subscriptions.
  - **Invalid Accounts:** Accounts with incorrect login details.
  - **Console Output:** Real-time updates on account status and checker performance.
  - **Results Logging:** Outputs results to categorized log files for later reference:
  - `good_crunchyroll.txt`: Stores valid accounts without premium.
  - `good_crunchyroll_premium.txt`: Stores valid accounts with premium subscriptions.
  - `custom_crunchyroll.txt`: Stores accounts requiring additional verification (A2F).

---

## Prerequisites
Before using the tool, ensure you have the following installed:
- **Python 3.x**
- Required Python modules:
  - `requests`
  - `tls-client`
  - `colorama`
  - `pystyle`
  
You can install the necessary dependencies by running:
```bash
pip install -r requirements.txt

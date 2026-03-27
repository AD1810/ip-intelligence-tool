import requests
import os
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading

API_KEY = "YOUR_API_KEY_HERE"

def scan_ip_thread():
    ips = entry.get().split(",")
    output.delete(1.0, tk.END)

    for ip in ips:
        ip = ip.strip()

        output.insert(tk.END, "\n" + "="*50 + "\n")
        output.insert(tk.END, f"Investigating: {ip}\n")
        output.insert(tk.END, "="*50 + "\n\n")

        # IP Info
        try:
            res = requests.get(f"https://ipinfo.io/{ip}/json")
            data = res.json()

            output.insert(tk.END, f"IP: {data.get('ip')}\n")
            output.insert(tk.END, f"ASN & Org: {data.get('org')}\n")
            output.insert(tk.END, f"Country: {data.get('country')}\n\n")
        except:
            output.insert(tk.END, "Error fetching IP info\n")

        # Abuse Check
        try:
            headers = {
                "Key": API_KEY,
                "Accept": "application/json"
            }

            params = {
                "ipAddress": ip,
                "maxAgeInDays": 90
            }

            res = requests.get("https://api.abuseipdb.com/api/v2/check", headers=headers, params=params)
            data = res.json()["data"]

            score = data['abuseConfidenceScore']

            output.insert(tk.END, f"Abuse Score: {score}\n")

            if score > 50:
                risk = "🔴 HIGH RISK"
            elif score > 0:
                risk = "🟠 MEDIUM"
            else:
                risk = "🟢 SAFE"

            output.insert(tk.END, f"Risk Level: {risk}\n\n")

        except:
            output.insert(tk.END, "Error checking abuse\n")

        # Nmap Scan
        output.insert(tk.END, "Running Nmap...\n\n")
        nmap_result = os.popen(f"nmap -F {ip}").read()
        output.insert(tk.END, nmap_result)

        # Save report
        with open(f"report_{ip}.txt", "w") as f:
            f.write(nmap_result)

def scan_ip():
    thread = threading.Thread(target=scan_ip_thread)
    thread.start()

# GUI
root = tk.Tk()
root.title("IP Intelligence Tool PRO")
root.geometry("650x550")
root.configure(bg="black")

entry = tk.Entry(root, width=50)
entry.pack(pady=10)

btn = tk.Button(root, text="Scan IP", command=scan_ip, bg="green", fg="black")
btn.pack(pady=5)

output = scrolledtext.ScrolledText(root, width=80, height=30, bg="black", fg="lime")
output.pack(pady=10)

root.mainloop()
import os
import requests
from bs4 import BeautifulSoup
import socket
import subprocess
import re

# আউটপুট সংরক্ষণের জন্য ফোল্ডার তৈরি করা
def create_output_directory(domain):
    base_dir = f"/home/kali/DiscoFinder/{domain}/recon"
    os.makedirs(base_dir, exist_ok=True)
    return base_dir

# আউটপুট লেখার জন্য ফাংশন
def write_to_file(file_path, content):
    with open(file_path, 'a') as file:
        file.write(content + '\n')

# পেজের টাইটেল খুঁজে বের করা
def get_page_title(url, output_dir):
    try:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string
            output = f"Page Title: {title}"
            print(output)
            write_to_file(f"{output_dir}/page_title.txt", output)
        else:
            print(f"Failed to retrieve {url} - Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

# HTTP হেডার সংগ্রহ করা
def get_http_headers(url, output_dir):
    try:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        response = requests.get(url)
        if response.status_code == 200:
            headers = response.headers
            header_content = "\n".join([f"{key}: {value}" for key, value in headers.items()])
            print("HTTP Headers collected:\n", header_content)
            write_to_file(f"{output_dir}/http_headers.txt", header_content)
        else:
            print(f"Failed to retrieve {url} - Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred while fetching headers: {e}")

# amass দিয়ে সাবডোমেইন এনুমারেশন
def enumerate_subdomains(domain, output_dir):
    print("\n--- Enumerating Subdomains (using amass) ---")
    try:
        result = subprocess.run(['amass', 'enum', '-d', domain], capture_output=True, text=True)
        print(result.stdout)
        write_to_file(f"{output_dir}/alive-subdomains.txt", result.stdout)
    except Exception as e:
        print(f"amass not found or an error occurred: {e}")

# masscan দিয়ে পোর্ট স্ক্যানিং
def scan_open_ports(domain, output_dir):
    print("\n--- Scanning Open Ports (using masscan) ---")
    try:
        result = subprocess.run(['masscan', domain, '-p1-65535', '--rate=1000'], capture_output=True, text=True)
        print(result.stdout)
        write_to_file(f"{output_dir}/alive-hosts.txt", result.stdout)
    except Exception as e:
        print(f"masscan not found or an error occurred: {e}")

# Nmap দিয়ে এনুমারেশন
def nmap_scan(domain, output_dir):
    print("\n--- Running Nmap Scan ---")
    try:
        result = subprocess.run(['nmap', '-A', domain], capture_output=True, text=True)
        print(result.stdout)
        write_to_file(f"{output_dir}/nmap_report.txt", result.stdout)
    except Exception as e:
        print(f"Nmap not found or an error occurred: {e}")

# aquatone দিয়ে স্ক্রিনশট নেওয়া
def take_screenshots(domain, output_dir):
    print("\n--- Taking Screenshots (using aquatone) ---")
    try:
        result = subprocess.run(['aquatone', '-scan-timeout', '300', '-http-timeout', '1000', '-out', output_dir], capture_output=True, text=True)
        print("Screenshots saved in Aquatone output directory.")
    except Exception as e:
        print(f"aquatone not found or an error occurred: {e}")

# dirsearch দিয়ে ডিরেক্টরি ব্রুটফোর্স
def directory_bruteforce(url, output_dir):
    print("\n--- Directory Bruteforce (using dirsearch) ---")
    try:
        result = subprocess.run(['dirsearch', '-u', url, '-e', 'php,html,js'], capture_output=True, text=True)
        print(result.stdout)
        write_to_file(f"{output_dir}/directory_bruteforce.txt", result.stdout)
    except Exception as e:
        print(f"dirsearch not found or an error occurred: {e}")

# ফাংশন চালানোর আগে আউটপুট ফোল্ডার তৈরি করা
url = input("Enter the URL (e.g., example.com or https://example.com): ")
domain = url.replace("https://", "").replace("http://", "")
output_dir = create_output_directory(domain)

# ফাংশনগুলো চালানো
print("\nStarting DiscoFinder with automated file output...")
get_page_title(url, output_dir)
get_http_headers(url, output_dir)
enumerate_subdomains(domain, output_dir)
scan_open_ports(domain, output_dir)
nmap_scan(domain, output_dir)
take_screenshots(domain, output_dir)
directory_bruteforce(url, output_dir)
print("\nDiscoFinder scan complete.")

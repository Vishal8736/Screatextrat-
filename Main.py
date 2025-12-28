import re
import requests
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

# Nameplate aur UI
G = Fore.GREEN
R = Fore.RED
Y = Fore.YELLOW
C = Fore.CYAN
W = Fore.WHITE
B = Style.BRIGHT

def banner():
    print(f"{G}{B}{'='*50}")
    print(f"{G}{B}      Screatextrat-Pro | v2.0 (Ultrasonic)")
    print(f"{C}{B}          [ Vishal ❤️ Subhi ]")
    print(f"{G}{B}{'='*50}\n")

def load_patterns(file_path):
    patterns = {}
    try:
        with open(file_path, 'r') as f:
            current_category = "General"
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    if line.startswith('# ---'):
                        current_category = line.replace('# ---', '').replace('---', '').strip()
                    continue
                if ':' in line:
                    name, regex = line.split(':', 1)
                    patterns[f"{current_category} - {name.strip()}"] = regex.strip()
        return patterns
    except FileNotFoundError:
        print(f"{R}[!] Error: pattern.txt file nahi mili!")
        sys.exit(1)

def scan_url(url, patterns):
    try:
        # User-agent to bypass basic blocks
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        content = response.text
        
        found = False
        results = []
        
        for name, regex in patterns.items():
            matches = re.finditer(regex, content)
            for match in matches:
                found = True
                results.append(f"{G}[+] {name}: {W}{match.group()}")
        
        if found:
            print(f"{C}\n[TARGET]: {url}")
            for res in results:
                print(res)
        
    except Exception as e:
        # Uncomment below for debugging errors
        # print(f"{R}[!] Failed to scan {url}: {str(e)}")
        pass

def main():
    banner()
    parser = argparse.ArgumentParser(description="Screatextrat-Pro: Advanced Sensitive Data Extractor")
    parser.add_argument("-i", "--input", help="File containing list of URLs")
    parser.add_argument("-u", "--url", help="Single URL to scan")
    parser.add_argument("-t", "--threads", type=int, default=20, help="Number of threads (default: 20)")
    
    args = parser.parse_args()
    
    if not args.input and not args.url:
        parser.print_help()
        sys.exit(0)

    patterns = load_patterns("pattern.txt")
    print(f"{Y}[*] {len(patterns)} Patterns loaded successfully...\n")

    urls = []
    if args.url:
        urls.append(args.url)
    if args.input:
        try:
            with open(args.input, 'r') as f:
                urls.extend([line.strip() for line in f if line.strip()])
        except FileNotFoundError:
            print(f"{R}[!] Input file nahi mili!")
            sys.exit(1)

    print(f"{G}[*] Scanning {len(urls)} targets with {args.threads} threads...\n")

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [executor.submit(scan_url, url, patterns) for url in urls]
        for future in futures:
            future.result()

    print(f"\n{G}{B}[*] Scan Complete. Happy Hunting!")

if __name__ == "__main__":
    # Disable insecure request warnings for SSL
    requests.packages.urllib3.disable_warnings()
    main()


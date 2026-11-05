#!/usr/bin/env python3
import os
import sys
import subprocess

# --- HACKITA BRANDING COLORS ---
RED    = "\033[38;5;196m"  # Hackita Bright Red
DRED   = "\033[38;5;88m"   # Hackita Dark Red
WHITE  = "\033[38;5;255m"  # Pure White
BLACK  = "\033[38;5;236m"  # Dark Grey
RESET  = "\033[0m"
BOLD   = "\033[1m"

# --- HACKITA TEXT LOGO ---
HACKITA_LOGO = f"""
{WHITE}{BOLD}██╗  ██╗ █████╗  ██████╗██╗  ██╗{RED}██╗████████╗ █████╗ {RESET}
{WHITE}{BOLD}██║  ██║██╔══██╗██╔════╝██║ ██╔╝{RED}██║╚══██╔══╝██╔══██╗{RESET}
{WHITE}{BOLD}███████║███████║██║     █████╔╝ {RED}██║   ██║   ███████║{RESET}
{WHITE}{BOLD}██╔══██║██╔══██║██║     ██╔═██╗ {RED}██║   ██║   ██╔══██║{RESET}
{WHITE}{BOLD}██║  ██║██║  ██║╚██████╗██║  ██╗{RED}██║   ██║   ██║  ██║{RESET}
{WHITE}{BOLD}╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝{RED}╚═╝   ╚═╝   ╚═╝  ╚═╝{RESET}
{DRED}       L I G O L O - N G   P I V O T I N G   L A U N C H E R {RESET}
"""

def print_cmd(cmd):
    print(f"{BLACK}   $ {RESET}{WHITE}{cmd}{RESET}")

def print_section(title):
    print(f"\n{DRED}=================================================={RESET}")
    print(f"{RED}{BOLD}[*] {title}{RESET}")
    print(f"{DRED}=================================================={RESET}")

def main():
    # Default port is 11601
    PORT = sys.argv[1] if len(sys.argv) > 1 else "11601"

    # Only a plain TCP port number is accepted (no shell metacharacters)
    if not (PORT.isascii() and PORT.isdigit() and 1 <= int(PORT) <= 65535):
        print(f"{RED}[!] ERROR: invalid port '{PORT}' (use a number from 1 to 65535).{RESET}")
        sys.exit(1)

    print(HACKITA_LOGO)
    
    print_section("CREATING TUN INTERFACES (ligolo1..ligolo10)")
    print(f"{BLACK}   (Interfaces will be created only if they don't exist){RESET}")

    # Create up to 10 interfaces dynamically
    for i in range(1, 11):
        tun_name = "ligolo" if i == 1 else f"ligolo{i}"
        
        # Check if the interface already exists
        check_cmd = ["ip", "link", "show", tun_name]
        result = subprocess.run(check_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if result.returncode == 0:
            print(f" {WHITE}[*] Interface {RED}{tun_name}{WHITE} already exists (skipped){RESET}")
        else:
            # Create the interface
            subprocess.run(["sudo", "ip", "tuntap", "add", "user", "root", "mode", "tun", tun_name], stderr=subprocess.DEVNULL)
            # Bring the interface up
            subprocess.run(["sudo", "ip", "link", "set", tun_name, "up"], stderr=subprocess.DEVNULL)
            print(f" {WHITE}[+] Interface {RED}{tun_name}{WHITE} created and enabled{RESET}")

    print_section(f"STARTING LIGOLO-PROXY ON PORT {PORT}")
    print(f"{BLACK}   (Keep this window open, the proxy will listen for connections){RESET}\n")
    print_cmd(f"ligolo-proxy -selfcert -laddr 0.0.0.0:{PORT}")

    # Security check: is ligolo-proxy installed?
    if subprocess.run(["which", "ligolo-proxy"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0:
        print(f"\n{RED}[!] ERROR: 'ligolo-proxy' not found in PATH.{RESET}")
        print(f"{WHITE}    Make sure you downloaded the binary from:{RESET}")
        print(f"{RED}    https://github.com/nicocha30/ligolo-ng/releases{RESET}")
        sys.exit(1)

    print("")
    print(f"{DRED}--------------------------------------------------{RESET}")
    print(f"{WHITE}{BOLD}    USEFUL COMMANDS (INSIDE THE PROXY CONSOLE){RESET}")
    print(f"{DRED}--------------------------------------------------{RESET}")

    print(f"\n{RED}[1] Select the agent session:{RESET}")
    print_cmd("session")

    print(f"\n{RED}[2] Start the tunnel on the first interface:{RESET}")
    print_cmd("start")
    print(f"{BLACK}   (For the second session, use: {WHITE}tunnel_start --tun ligolo2{BLACK}){RESET}")

    print(f"\n{RED}[3] Add a route for the internal network (Session 1 - ligolo):{RESET}")
    print(f"{BLACK}   # On Kali (separate terminal, outside the proxy):{RESET}")
    print_cmd("sudo ip route add 10.10.10.0/24 dev ligolo")

    print(f"\n{RED}[4] Add a route for the internal network (Session 2 - ligolo2):{RESET}")
    print_cmd("sudo ip route add 192.168.1.0/24 dev ligolo2")

    print(f"\n{RED}[5] Add the 'Magic IP' route (access agent's localhost):{RESET}")
    print_cmd("sudo ip route add 240.0.0.1/32 dev ligolo")

    print(f"\n{DRED}--------------------------------------------------{RESET}")
    print(f"{WHITE}{BOLD}    AGENT COMMANDS (ON THE TARGET MACHINE){RESET}")
    print(f"{DRED}--------------------------------------------------{RESET}")
    print(f"\n{WHITE}   Linux/Windows (default port {PORT}):{RESET}")
    print_cmd(f"./agent -connect <YOUR_KALI_IP>:{PORT} --ignore-cert")

    # --- HACKITA FOOTER ---
    print(f"\n{DRED}=================================================={RESET}")
    print(f"{RED}{BOLD}       READ MORE ON HACKITA{RESET}")
    print(f"{DRED}=================================================={RESET}")
    print(f" {WHITE}🇮🇹 Italian  : {RED}https://hackita.it/articoli/ligolo-ng{RESET}")
    print(f" {WHITE}🇬🇧 English  : {RED}https://en.hackita.it/articoli/ligolo-ng{RESET}")
    print(f" {WHITE}🇪🇸 Spanish  : {RED}https://es.hackita.it/articoli/ligolo-ng{RESET}")
    print(f" {WHITE}🇩🇪 German   : {RED}https://de.hackita.it/articoli/ligolo-ng{RESET}")
    print(f" {WHITE}🇵🇹 Portuguese: {RED}https://pt.hackita.it/articoli/ligolo-ng{RESET}")
    print(f" {WHITE}🇫🇷 French   : {RED}https://fr.hackita.it/articoli/ligolo-ng{RESET}")
    print(f"{DRED}=================================================={RESET}\n")

    # Execute the proxy in the foreground
    try:
        subprocess.run(["ligolo-proxy", "-selfcert", "-laddr", f"0.0.0.0:{PORT}"])
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Interrupted by user.{RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()
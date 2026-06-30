#!/usr/bin/env python3
"""
HexStrike AI MCP Server - Remote Deployment Version
Deployed on Render with FastMCP SSE transport

This is a standalone MCP server that provides cybersecurity tool interfaces.
Note: Some tools require the full HexStrike backend for actual execution.
"""

import os
from typing import Dict, Any
from fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("hexstrike-ai")

# =============================================================================
# CORE NETWORK SCANNING TOOLS
# =============================================================================

@mcp.tool()
def nmap_scan(target: str, scan_type: str = "-sV", ports: str = "", additional_args: str = "") -> str:
    """
    Execute Nmap scan against a target for port scanning and service detection.
    
    Args:
        target: The IP address or hostname to scan
        scan_type: Scan type (e.g., -sV for version detection, -sC for scripts, -sS for SYN scan)
        ports: Comma-separated list of ports or port ranges (e.g., "22,80,443" or "1-1000")
        additional_args: Additional Nmap arguments
    
    Returns:
        Nmap command to run locally
    """
    cmd_parts = ["nmap", scan_type]
    if ports:
        cmd_parts.extend(["-p", ports])
    if additional_args:
        cmd_parts.append(additional_args)
    cmd_parts.append(target)
    
    command = " ".join(cmd_parts)
    return f"🔍 Nmap Scan Command:\n\n{command}\n\nRun this command locally where nmap is installed."


@mcp.tool()
def masscan_scan(target: str, ports: str = "1-65535", rate: int = 1000) -> str:
    """
    Execute Masscan for high-speed port scanning.
    
    Args:
        target: The target IP address or CIDR range
        ports: Port range to scan
        rate: Packets per second rate
    
    Returns:
        Masscan command to run locally
    """
    command = f"masscan {target} -p{ports} --rate={rate}"
    return f"🚀 Masscan Command:\n\n{command}\n\nRun this command locally where masscan is installed."


@mcp.tool()
def rustscan_scan(target: str, ports: str = "", ulimit: int = 5000) -> str:
    """
    Execute RustScan for ultra-fast port scanning.
    
    Args:
        target: The target IP address or hostname
        ports: Specific ports to scan (e.g., "22,80,443")
        ulimit: File descriptor limit
    
    Returns:
        RustScan command to run locally
    """
    cmd_parts = ["rustscan", "-a", target, "-u", str(ulimit)]
    if ports:
        cmd_parts.extend(["-p", ports])
    
    command = " ".join(cmd_parts)
    return f"⚡ RustScan Command:\n\n{command}\n\nRun this command locally where rustscan is installed."


# =============================================================================
# WEB APPLICATION SECURITY TOOLS
# =============================================================================

@mcp.tool()
def gobuster_scan(url: str, mode: str = "dir", wordlist: str = "/usr/share/wordlists/dirb/common.txt") -> str:
    """
    Execute Gobuster for directory/file brute forcing.
    
    Args:
        url: The target URL
        mode: Scan mode (dir, dns, fuzz, vhost)
        wordlist: Path to wordlist file
    
    Returns:
        Gobuster command to run locally
    """
    command = f"gobuster {mode} -u {url} -w {wordlist}"
    return f"📁 Gobuster Command:\n\n{command}\n\nRun this command locally where gobuster is installed."


@mcp.tool()
def ffuf_scan(url: str, wordlist: str = "/usr/share/wordlists/dirb/common.txt", match_codes: str = "200,204,301,302,307,401,403") -> str:
    """
    Execute FFuf for web fuzzing.
    
    Args:
        url: The target URL (use FUZZ where you want to inject payloads)
        wordlist: Wordlist file to use
        match_codes: HTTP status codes to match
    
    Returns:
        FFuf command to run locally
    """
    command = f"ffuf -u {url} -w {wordlist} -mc {match_codes}"
    return f"🔍 FFuf Command:\n\n{command}\n\nRun this command locally where ffuf is installed."


@mcp.tool()
def nuclei_scan(target: str, severity: str = "", tags: str = "", template: str = "") -> str:
    """
    Execute Nuclei vulnerability scanner.
    
    Args:
        target: The target URL or IP
        severity: Filter by severity (critical,high,medium,low,info)
        tags: Filter by tags (e.g., cve,rce,lfi)
        template: Custom template path
    
    Returns:
        Nuclei command to run locally
    """
    cmd_parts = ["nuclei", "-u", target]
    if severity:
        cmd_parts.extend(["-s", severity])
    if tags:
        cmd_parts.extend(["-tags", tags])
    if template:
        cmd_parts.extend(["-t", template])
    
    command = " ".join(cmd_parts)
    return f"🔬 Nuclei Command:\n\n{command}\n\nRun this command locally where nuclei is installed."


@mcp.tool()
def nikto_scan(target: str, additional_args: str = "") -> str:
    """
    Execute Nikto web vulnerability scanner.
    
    Args:
        target: The target URL or IP
        additional_args: Additional Nikto arguments
    
    Returns:
        Nikto command to run locally
    """
    cmd_parts = ["nikto", "-h", target]
    if additional_args:
        cmd_parts.append(additional_args)
    
    command = " ".join(cmd_parts)
    return f"🔬 Nikto Command:\n\n{command}\n\nRun this command locally where nikto is installed."


@mcp.tool()
def sqlmap_scan(url: str, data: str = "", additional_args: str = "") -> str:
    """
    Execute SQLMap for SQL injection testing.
    
    Args:
        url: The target URL
        data: POST data for testing
        additional_args: Additional SQLMap arguments
    
    Returns:
        SQLMap command to run locally
    """
    cmd_parts = ["sqlmap", "-u", f'"{url}"']
    if data:
        cmd_parts.extend(["--data", f'"{data}"'])
    if additional_args:
        cmd_parts.append(additional_args)
    
    command = " ".join(cmd_parts)
    return f"💉 SQLMap Command:\n\n{command}\n\nRun this command locally where sqlmap is installed."


@mcp.tool()
def wpscan_scan(url: str, additional_args: str = "") -> str:
    """
    Execute WPScan for WordPress vulnerability scanning.
    
    Args:
        url: The WordPress site URL
        additional_args: Additional WPScan arguments
    
    Returns:
        WPScan command to run locally
    """
    cmd_parts = ["wpscan", "--url", url]
    if additional_args:
        cmd_parts.append(additional_args)
    
    command = " ".join(cmd_parts)
    return f"🔍 WPScan Command:\n\n{command}\n\nRun this command locally where wpscan is installed."


# =============================================================================
# SUBDOMAIN ENUMERATION TOOLS
# =============================================================================

@mcp.tool()
def subfinder_scan(domain: str, silent: bool = True, all_sources: bool = False) -> str:
    """
    Execute Subfinder for passive subdomain enumeration.
    
    Args:
        domain: The target domain
        silent: Run in silent mode
        all_sources: Use all sources
    
    Returns:
        Subfinder command to run locally
    """
    cmd_parts = ["subfinder", "-d", domain]
    if silent:
        cmd_parts.append("-silent")
    if all_sources:
        cmd_parts.append("-all")
    
    command = " ".join(cmd_parts)
    return f"🔍 Subfinder Command:\n\n{command}\n\nRun this command locally where subfinder is installed."


@mcp.tool()
def amass_scan(domain: str, mode: str = "enum", additional_args: str = "") -> str:
    """
    Execute Amass for subdomain enumeration.
    
    Args:
        domain: The target domain
        mode: Amass mode (enum, intel, viz)
        additional_args: Additional Amass arguments
    
    Returns:
        Amass command to run locally
    """
    cmd_parts = ["amass", mode, "-d", domain]
    if additional_args:
        cmd_parts.append(additional_args)
    
    command = " ".join(cmd_parts)
    return f"🔍 Amass Command:\n\n{command}\n\nRun this command locally where amass is installed."


# =============================================================================
# PASSWORD CRACKING TOOLS
# =============================================================================

@mcp.tool()
def hydra_attack(target: str, service: str, username: str = "", password_file: str = "/usr/share/wordlists/rockyou.txt") -> str:
    """
    Execute Hydra for password brute forcing.
    
    Args:
        target: The target IP or hostname
        service: The service to attack (ssh, ftp, http, etc.)
        username: Single username to test
        password_file: File containing passwords
    
    Returns:
        Hydra command to run locally
    """
    cmd_parts = ["hydra"]
    if username:
        cmd_parts.extend(["-l", username])
    cmd_parts.extend(["-P", password_file, target, service])
    
    command = " ".join(cmd_parts)
    return f"🔑 Hydra Command:\n\n{command}\n\nRun this command locally where hydra is installed."


@mcp.tool()
def john_crack(hash_file: str, wordlist: str = "/usr/share/wordlists/rockyou.txt", format_type: str = "") -> str:
    """
    Execute John the Ripper for password cracking.
    
    Args:
        hash_file: File containing password hashes
        wordlist: Wordlist file to use
        format_type: Hash format type
    
    Returns:
        John command to run locally
    """
    cmd_parts = ["john", f"--wordlist={wordlist}"]
    if format_type:
        cmd_parts.append(f"--format={format_type}")
    cmd_parts.append(hash_file)
    
    command = " ".join(cmd_parts)
    return f"🔐 John the Ripper Command:\n\n{command}\n\nRun this command locally where john is installed."


@mcp.tool()
def hashcat_crack(hash_file: str, hash_type: str, attack_mode: str = "0", wordlist: str = "/usr/share/wordlists/rockyou.txt") -> str:
    """
    Execute Hashcat for advanced password cracking.
    
    Args:
        hash_file: File containing password hashes
        hash_type: Hash type number for Hashcat
        attack_mode: Attack mode (0=dict, 1=combo, 3=mask, etc.)
        wordlist: Wordlist file for dictionary attacks
    
    Returns:
        Hashcat command to run locally
    """
    command = f"hashcat -m {hash_type} -a {attack_mode} {hash_file} {wordlist}"
    return f"🔐 Hashcat Command:\n\n{command}\n\nRun this command locally where hashcat is installed."


# =============================================================================
# SMB/NETWORK ENUMERATION TOOLS
# =============================================================================

@mcp.tool()
def enum4linux_scan(target: str, additional_args: str = "-a") -> str:
    """
    Execute Enum4linux for SMB enumeration.
    
    Args:
        target: The target IP address
        additional_args: Additional Enum4linux arguments
    
    Returns:
        Enum4linux command to run locally
    """
    command = f"enum4linux {additional_args} {target}"
    return f"🔍 Enum4linux Command:\n\n{command}\n\nRun this command locally where enum4linux is installed."


@mcp.tool()
def netexec_scan(target: str, protocol: str = "smb", username: str = "", password: str = "") -> str:
    """
    Execute NetExec (formerly CrackMapExec) for network enumeration.
    
    Args:
        target: The target IP or network
        protocol: Protocol to use (smb, ssh, winrm, etc.)
        username: Username for authentication
        password: Password for authentication
    
    Returns:
        NetExec command to run locally
    """
    cmd_parts = ["netexec", protocol, target]
    if username:
        cmd_parts.extend(["-u", username])
    if password:
        cmd_parts.extend(["-p", password])
    
    command = " ".join(cmd_parts)
    return f"🔍 NetExec Command:\n\n{command}\n\nRun this command locally where netexec is installed."


@mcp.tool()
def smbmap_scan(target: str, username: str = "", password: str = "", domain: str = "") -> str:
    """
    Execute SMBMap for SMB share enumeration.
    
    Args:
        target: The target IP address
        username: Username for authentication
        password: Password for authentication
        domain: Domain for authentication
    
    Returns:
        SMBMap command to run locally
    """
    cmd_parts = ["smbmap", "-H", target]
    if username:
        cmd_parts.extend(["-u", username])
    if password:
        cmd_parts.extend(["-p", password])
    if domain:
        cmd_parts.extend(["-d", domain])
    
    command = " ".join(cmd_parts)
    return f"🔍 SMBMap Command:\n\n{command}\n\nRun this command locally where smbmap is installed."


# =============================================================================
# BINARY ANALYSIS TOOLS
# =============================================================================

@mcp.tool()
def binwalk_analyze(file_path: str, extract: bool = False) -> str:
    """
    Execute Binwalk for firmware and file analysis.
    
    Args:
        file_path: Path to the file to analyze
        extract: Whether to extract discovered files
    
    Returns:
        Binwalk command to run locally
    """
    cmd_parts = ["binwalk"]
    if extract:
        cmd_parts.append("-e")
    cmd_parts.append(file_path)
    
    command = " ".join(cmd_parts)
    return f"🔧 Binwalk Command:\n\n{command}\n\nRun this command locally where binwalk is installed."


@mcp.tool()
def checksec_analyze(binary: str) -> str:
    """
    Check security features of a binary.
    
    Args:
        binary: Path to the binary file
    
    Returns:
        Checksec command to run locally
    """
    command = f"checksec --file={binary}"
    return f"🔧 Checksec Command:\n\n{command}\n\nRun this command locally where checksec is installed."


@mcp.tool()
def strings_extract(file_path: str, min_len: int = 4) -> str:
    """
    Extract strings from a binary file.
    
    Args:
        file_path: Path to the file
        min_len: Minimum string length
    
    Returns:
        Strings command to run locally
    """
    command = f"strings -n {min_len} {file_path}"
    return f"🔧 Strings Command:\n\n{command}\n\nRun this command locally."


# =============================================================================
# CLOUD SECURITY TOOLS
# =============================================================================

@mcp.tool()
def trivy_scan(scan_type: str = "image", target: str = "", severity: str = "") -> str:
    """
    Execute Trivy for container and filesystem vulnerability scanning.
    
    Args:
        scan_type: Type of scan (image, fs, repo, config)
        target: Target to scan (image name, directory, repository)
        severity: Severity filter (UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL)
    
    Returns:
        Trivy command to run locally
    """
    cmd_parts = ["trivy", scan_type, target]
    if severity:
        cmd_parts.extend(["--severity", severity])
    
    command = " ".join(cmd_parts)
    return f"🔍 Trivy Command:\n\n{command}\n\nRun this command locally where trivy is installed."


@mcp.tool()
def prowler_scan(provider: str = "aws", profile: str = "default") -> str:
    """
    Execute Prowler for comprehensive cloud security assessment.
    
    Args:
        provider: Cloud provider (aws, azure, gcp)
        profile: AWS profile to use
    
    Returns:
        Prowler command to run locally
    """
    command = f"prowler {provider} --profile {profile}"
    return f"☁️ Prowler Command:\n\n{command}\n\nRun this command locally where prowler is installed."


# =============================================================================
# OSINT TOOLS
# =============================================================================

@mcp.tool()
def httpx_probe(target: str, tech_detect: bool = False, status_code: bool = True) -> str:
    """
    Execute httpx for fast HTTP probing and technology detection.
    
    Args:
        target: Target file or single URL
        tech_detect: Enable technology detection
        status_code: Show status codes
    
    Returns:
        httpx command to run locally
    """
    cmd_parts = ["httpx", "-u", target]
    if tech_detect:
        cmd_parts.append("-td")
    if status_code:
        cmd_parts.append("-sc")
    
    command = " ".join(cmd_parts)
    return f"🌍 httpx Command:\n\n{command}\n\nRun this command locally where httpx is installed."


@mcp.tool()
def katana_crawl(url: str, depth: int = 3, js_crawl: bool = True) -> str:
    """
    Execute Katana for next-generation crawling and spidering.
    
    Args:
        url: The target URL to crawl
        depth: Crawling depth
        js_crawl: Enable JavaScript crawling
    
    Returns:
        Katana command to run locally
    """
    cmd_parts = ["katana", "-u", url, "-d", str(depth)]
    if js_crawl:
        cmd_parts.append("-jc")
    
    command = " ".join(cmd_parts)
    return f"⚔️ Katana Command:\n\n{command}\n\nRun this command locally where katana is installed."


@mcp.tool()
def waybackurls_discovery(domain: str) -> str:
    """
    Execute Waybackurls for historical URL discovery.
    
    Args:
        domain: The target domain
    
    Returns:
        Waybackurls command to run locally
    """
    command = f"echo {domain} | waybackurls"
    return f"🕰️ Waybackurls Command:\n\n{command}\n\nRun this command locally where waybackurls is installed."


@mcp.tool()
def gau_discovery(domain: str) -> str:
    """
    Execute Gau (Get All URLs) for URL discovery from multiple sources.
    
    Args:
        domain: The target domain
    
    Returns:
        Gau command to run locally
    """
    command = f"gau {domain}"
    return f"📡 Gau Command:\n\n{command}\n\nRun this command locally where gau is installed."


# =============================================================================
# METASPLOIT TOOLS
# =============================================================================

@mcp.tool()
def msfvenom_generate(payload: str, lhost: str = "", lport: str = "4444", format_type: str = "exe") -> str:
    """
    Execute MSFVenom for payload generation.
    
    Args:
        payload: The payload to generate (e.g., windows/meterpreter/reverse_tcp)
        lhost: Listener host IP
        lport: Listener port
        format_type: Output format (exe, elf, raw, etc.)
    
    Returns:
        MSFVenom command to run locally
    """
    cmd_parts = ["msfvenom", "-p", payload]
    if lhost:
        cmd_parts.append(f"LHOST={lhost}")
    cmd_parts.append(f"LPORT={lport}")
    cmd_parts.extend(["-f", format_type])
    
    command = " ".join(cmd_parts)
    return f"🚀 MSFVenom Command:\n\n{command}\n\nRun this command locally where msfvenom is installed."


# =============================================================================
# XSS TOOLS
# =============================================================================

@mcp.tool()
def dalfox_xss_scan(url: str, blind: bool = False) -> str:
    """
    Execute Dalfox for advanced XSS vulnerability scanning.
    
    Args:
        url: The target URL
        blind: Enable blind XSS testing
    
    Returns:
        Dalfox command to run locally
    """
    cmd_parts = ["dalfox", "url", url]
    if blind:
        cmd_parts.append("--blind")
    
    command = " ".join(cmd_parts)
    return f"🎯 Dalfox Command:\n\n{command}\n\nRun this command locally where dalfox is installed."


# =============================================================================
# UTILITY TOOLS
# =============================================================================

@mcp.tool()
def server_health() -> Dict[str, Any]:
    """
    Check the health status of the HexStrike AI MCP server.
    
    Returns:
        Server health information
    """
    return {
        "status": "healthy",
        "version": "6.0.0-remote",
        "server_type": "FastMCP SSE",
        "deployment": "Render",
        "tools_available": 30,
        "note": "This is a remote MCP server. Tools generate commands to run locally."
    }


@mcp.tool()
def list_tools() -> str:
    """
    List all available security tools in HexStrike AI MCP.
    
    Returns:
        List of available tools with descriptions
    """
    tools = """
🔥 HexStrike AI MCP - Available Security Tools 🔥

📡 NETWORK SCANNING:
  • nmap_scan - Port scanning and service detection
  • masscan_scan - High-speed port scanning
  • rustscan_scan - Ultra-fast port scanning

🌐 WEB APPLICATION SECURITY:
  • gobuster_scan - Directory/file brute forcing
  • ffuf_scan - Web fuzzing
  • nuclei_scan - Vulnerability scanning
  • nikto_scan - Web vulnerability scanner
  • sqlmap_scan - SQL injection testing
  • wpscan_scan - WordPress vulnerability scanning
  • dalfox_xss_scan - XSS vulnerability scanning

🔍 SUBDOMAIN ENUMERATION:
  • subfinder_scan - Passive subdomain enumeration
  • amass_scan - Subdomain enumeration

🔑 PASSWORD CRACKING:
  • hydra_attack - Password brute forcing
  • john_crack - Password cracking with John the Ripper
  • hashcat_crack - Advanced password cracking

🖥️ SMB/NETWORK ENUMERATION:
  • enum4linux_scan - SMB enumeration
  • netexec_scan - Network enumeration
  • smbmap_scan - SMB share enumeration

🔧 BINARY ANALYSIS:
  • binwalk_analyze - Firmware analysis
  • checksec_analyze - Binary security features
  • strings_extract - String extraction

☁️ CLOUD SECURITY:
  • trivy_scan - Container vulnerability scanning
  • prowler_scan - Cloud security assessment

🌍 OSINT & RECON:
  • httpx_probe - HTTP probing
  • katana_crawl - Web crawling
  • waybackurls_discovery - Historical URL discovery
  • gau_discovery - URL discovery

🚀 EXPLOITATION:
  • msfvenom_generate - Payload generation

ℹ️ UTILITY:
  • server_health - Check server health
  • list_tools - List all tools

Note: Most tools generate commands to run locally where the security tools are installed.
"""
    return tools


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    # Get port from environment (Render sets this automatically)
    port = int(os.getenv("PORT", 8000))
    
    print(f"🔥 Starting HexStrike AI MCP Server v6.0")
    print(f"🌐 Running on port {port}")
    
    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=port,
        path="/mcp"
    )

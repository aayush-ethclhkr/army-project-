import scapy.all as scapy
import logging

# Set up logging to save the captured packets to a file
logging.basicConfig(filename="network_traffic_log.txt", level=logging.INFO)

def packet_callback(packet):
    """Callback function to process each packet."""
    if packet.haslayer(scapy.IP):
        ip_src = packet[scapy.IP].src
        ip_dst = packet[scapy.IP].dst
        protocol = packet[scapy.IP].proto
        length = len(packet)
        
        # Log packet details
        log_message = f"Source: {ip_src} | Destination: {ip_dst} | Protocol: {protocol} | Length: {length} bytes"
        print(log_message)
        logging.info(log_message)

def start_sniffing(interface=None):
    """Start sniffing network traffic."""
    print("Starting network sniffing...")
    # Sniff packets on the given interface or all interfaces if not specified
    scapy.sniff(iface=interface, prn=packet_callback, store=False)

if __name__ == "__main__":
    # You can specify the network interface (e.g., 'eth0', 'wlan0') or None for automatic selection
    interface = None  # Leave as None to automatically select an interface
    start_sniffing(interface)
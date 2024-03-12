import os
import socket
import requests
from colorama import Fore, Style

def get_geo_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        country = data["country"]
        city = data["city"]
        country_code = data["countryCode"]
        timezone = data["timezone"]
        isp = data["isp"]
        org = data["org"]
        asn = data["as"]
        return country, city, country_code, timezone, isp, org, asn
    except Exception as e:
        print(f"Hata: {e}")
        return "Bilinmiyor", "Bilinmiyor", "Bilinmiyor", "Bilinmiyor", "Bilinmiyor", "Bilinmiyor", "Bilinmiyor"


def get_device_info(ip):
    try:
        response = requests.get(f"http://api.userstack.com/detect?access_key=YOUR_ACCESS_KEY&ip={ip}")
        data = response.json()
        device_info = data.get("device", "Bilinmiyor")
        return device_info
    except Exception as e:
        print(f"Hata: {e}")
        return "Bilinmiyor"

def get_network_info(url_or_ip):
    try:
        ip = socket.gethostbyname(url_or_ip)
        host = url_or_ip  
        geo_location = get_geo_location(ip)
        device_info = get_device_info(ip)
        return ip, host, geo_location, device_info
    except socket.gaierror:
        return None, None, None, None

def perform_port_scan(ip, full_scan=False):
    open_ports = []
    if full_scan:
        for port in range(1, 65536):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
            print(f"{Fore.YELLOW}Port Taraması Devam Ediyor. Muhtemelen bu işlem çok uzun sürecektir :D Taranan Port: {port} / 65535", end='\r')
    else:
        port_range = [21, 22, 23, 25, 53, 67, 68, 80, 88, 110, 123, 135, 137, 138, 139, 143, 161, 389, 443, 445, 465, 514, 520, 587, 993, 995, 1433, 1521, 2049, 2181, 2375, 3306, 3389, 5432, 5900, 5984, 6379, 6667, 8080, 8443, 9090, 9200, 9300, 11211, 27017, 50000, 54321, 55555, 7547, 7654, 7999, 8081, 8444, 8585, 9000, 9001, 9091, 9100, 9207, 10000, 11223, 15672, 17185, 27015, 37777, 44818, 47808, 50030, 50070, 54311, 59559, 60000, 60001, 60002, 60003, 60004, 60005, 60006, 60007, 60008, 60009, 6379, 7500, 8000, 8082, 8086, 8333, 8880, 9002, 9043, 9999, 32764]
        for port in port_range:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
            print(f"{Fore.YELLOW}Port Taraması Devam Ediyor. Sadece önemli portlar taranıyor... Taranan Port: {port}", end='\r')
    return open_ports

def print_fancy_header():
    fancy_header = f"""
{Fore.CYAN}{Style.BRIGHT}
_____   __    _____     _______              ______                          
___  | / /______  /_    ___    |____________ ___  /____  ____________________
__   |/ /_  _ \  __/    __  /| |_  __ \  __ `/_  /__  / / /__  /_  _ \_  ___/
_  /|  / /  __/ /_      _  ___ |  / / / /_/ /_  / _  /_/ /__  /_/  __/  /    
/_/ |_/  \___/\__/      /_/  |_/_/ /_/\__,_/ /_/  _\__, / _____/\___//_/     
                                                  /____/   
=============================================================================                                   
{Style.BRIGHT}
Net Analyzer - Dev By Rywond
{Style.RESET_ALL}

"""
    print(fancy_header)

def print_menu():
    print(f"{Fore.MAGENTA}Ana Menü")
    print(f"{Fore.YELLOW}{Style.BRIGHT}[ 1 ] Tarama yapmaya başla")
    print("[ 2 ] Ayarlar")
    print("[ 3 ] Developed By Rywond")
    print("[ 4 ] Çıkış yap")
    print(Style.RESET_ALL)

def print_settings_menu(port_scan_flag, full_scan_flag):
    print(f"{Fore.MAGENTA}Ayarlar")
    print("")
    print(f"{Fore.YELLOW}Önemli Portlar Taraması: {Fore.GREEN if port_scan_flag else Fore.RED}{'Aktif' if port_scan_flag else 'Pasif'}{Style.RESET_ALL}")
    print("[ 1 ] Port Taraması: Aktif")
    print("[ 2 ] Port Taraması: Pasif")
    print("------------------------------")
    print(f"{Fore.YELLOW}Geniş Kapsamlı Port Taraması(65.535 Port): {Fore.GREEN if full_scan_flag else Fore.RED}{'Aktif' if full_scan_flag else 'Pasif'}{Style.RESET_ALL}")
    print("[ 3 ] Geniş Kapsamlı Port Taraması: Aktif")
    print("[ 4 ] Geniş Kapsamlı Port Taraması: Pasif")
    print("------------------------------")
    print("[ 5 ] Geri")
    print(Style.RESET_ALL)

def print_devbyry():
    print(f"{Fore.YELLOW}{Style.BRIGHT}[ 1 ] Geri Dön")
    print(Style.RESET_ALL)

def print_results(ip, host, geo_location, open_ports):
    os.system('cls' if os.name == 'nt' else 'clear')  
    print_fancy_header()
    print(f"+--+--+--+--+--+--+--+--+--+--+--+")
    print(f"| {Fore.CYAN}Ip Adresi:{Style.RESET_ALL} {ip:<30} ")
    print(f"+--+--+--+--+--+--+--+--+--+--+--+")
    print(f"| {Fore.CYAN}Host Adı:{Style.RESET_ALL} {host:<33} ")
    print(f"+--+--+--+--+--+--+--+--+--+--+--+")
    print(f"| {Fore.CYAN}Konum:{Style.RESET_ALL} {geo_location[0]} / {geo_location[1]}")
    print(f"| {Fore.CYAN}Ülke Kodu:{Style.RESET_ALL} {geo_location[2]}")
    print(f"| {Fore.CYAN}Saat Dilimi:{Style.RESET_ALL} {geo_location[3]}")
    print(f"| {Fore.CYAN}ISP:{Style.RESET_ALL} {geo_location[4]}")
    print(f"| {Fore.CYAN}Organizasyon:{Style.RESET_ALL} {geo_location[5]}")
    print(f"| {Fore.CYAN}ASN:{Style.RESET_ALL} {geo_location[6]}")
    print(f"+--+--+--+--+--+--+--+--+--+--+--+")
    if open_ports:
        ports_str = ', '.join(str(port) for port in open_ports)
        print(f"| {Fore.CYAN}Açık Portlar:{Style.RESET_ALL} {ports_str:<38} ")
        print(f"+--+--+--+--+--+--+--+--+--+--+--+")
    else:
        print(f"| {Fore.CYAN}Açık Portlar:{Style.RESET_ALL} {'Port taraması yapılmadı':<36} ")
        print(f"+--+--+--+--+--+--+--+--+--+--+--+")
    print(Style.RESET_ALL)

def main():
    os.system('cls' if os.name == 'nt' else 'clear') 

    port_scan_flag = True
    full_scan_flag = False

    print_fancy_header()
    print(f"{Fore.RED}{Style.BRIGHT}Merhaba sevgili kullanıcım!")
    print(f"{Fore.RED}{Style.BRIGHT}NetAnalyzer'i kullanırken Legal kalmaya dikkat ediniz.")
    print(f"{Fore.RED}{Style.BRIGHT}Geliştirici, program üzerinden yapılan hiç bir eylemden sorumlu değildir.")
    print("")
    while True:
        print_menu()
        choice = input(f"{Fore.RED}{Style.BRIGHT}root@rywond:~# ")

        if choice == "1":
            os.system('cls' if os.name == 'nt' else 'clear')
            print_fancy_header()
            print("Lütfen analiz etmek istediğiniz URL veya IP adresini girin:")
            url_or_ip = input(f"{Fore.RED}root@rywond:~# ")
            ip, host, geo_location, device_info = get_network_info(url_or_ip)
            if ip:
                open_ports = perform_port_scan(ip, full_scan_flag)
                print_results(ip, host, geo_location, open_ports)
            else:
                print(f"{Fore.RED}{Style.BRIGHT}Geçersiz URL veya IP adresi.{Style.RESET_ALL}")
            
            while True:
                print(f"{Fore.YELLOW}{Style.BRIGHT}Yeni bir Analiz yapmak ister misiniz?")
                print("[ 1 ] Evet, [ 2 ] Hayır, Ana Menüye dön")
                sorgu_choice = input(f"{Fore.RED}root@rywond:~# ")
                
                if sorgu_choice == "1":
                    print("Lütfen analiz etmek istediğiniz URL veya IP adresini girin:")
                    url_or_ip = input(f"{Fore.RED}root@rywond:~# ")
                    ip, host, geo_location, device_info = get_network_info(url_or_ip)
                    if ip:
                        open_ports = perform_port_scan(ip, full_scan_flag)
                        print_results(ip, host, geo_location, open_ports)
                    else:
                        print(f"{Fore.RED}{Style.BRIGHT}Geçersiz URL veya IP adresi.{Style.RESET_ALL}")
                    break

                elif sorgu_choice == "2":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print_fancy_header()
                    break
                else:
                    print(f"{Fore.RED}{Style.BRIGHT}Geçersiz seçim.{Style.RESET_ALL}")

        elif choice == "2":
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print_fancy_header()
                print_settings_menu(port_scan_flag, full_scan_flag)
                setting_choice = input(f"{Fore.RED}root@rywond:~# ")
                if setting_choice == "1":
                    port_scan_flag = True
                    full_scan_flag = False  
                elif setting_choice == "2":
                    port_scan_flag = False
                elif setting_choice == "3":
                    full_scan_flag = True
                    port_scan_flag = False  
                elif setting_choice == "4":
                    full_scan_flag = False
                elif setting_choice == "5":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print_fancy_header()
                    break
                else:
                    print(f"{Fore.RED}{Style.BRIGHT}Geçersiz seçim.{Style.RESET_ALL}")

        elif choice == "3":
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print_fancy_header()
                print(f"{Fore.BLUE}Bu Sistem TAMAMEN Rywond Tarafından Yapılmıştır.")
                print("")
                print_devbyry()
                setting_choice = input(f"{Fore.RED}root@rywond:~# ")
                if setting_choice == "1":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print_fancy_header()
                    break

        elif choice == "4":
            print("Çıkış yapılıyor...")
            break

        else:
            print(f"{Fore.RED}{Style.BRIGHT}Geçersiz seçim. Lütfen geçerli bir seçenek seçin.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

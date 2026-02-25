
def mac_check(mac_list, searched_mac):
    for mac in mac_list:
        if mac == searched_mac:
            return True
        
    return False
    

mac_list = ["123", "456"]
mac_address = input()
mac_check(mac_list, mac_address)
result = mac_check(mac_list, mac_address)
print(result)
        
        


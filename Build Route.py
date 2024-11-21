import requests

def build_route(controller_ip, switch_dpid, in_port, out_port, eth_src, eth_dst, ip_dst, protocol, port):
    flow_entry = {
        "switch": switch_dpid,
        "name": f"flow-{eth_src}-{ip_dst}-{port}",
        "priority": "32768",
        "in_port": str(in_port),
        "eth_src": eth_src,
        "eth_dst": eth_dst,
        "active": "true",
        "actions": f"output={out_port}"
    }
    
    # URL de la API del controlador Floodlight
    url = f"http://{controller_ip}:8080/wm/staticflowpusher/json"
    
    response = requests.post(url, json=flow_entry)
    if response.status_code == 200:
        print("Ruta instalada correctamente.")
    else:
        print(f"Error al instalar la ruta: {response.text}")

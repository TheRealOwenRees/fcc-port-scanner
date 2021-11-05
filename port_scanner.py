import socket
from common_ports import ports_and_services

def get_open_ports(host, port_range, verbose=False):
  open_ports = []                                           # list of open ports

  #print verbose port information
  def verbose_output(urhostname, ip_addr):
    output = f"Open ports for "
    output += f"{hostname} ({ip_addr})\n" if hostname else f"{ip_addr}\n"
    output += f"PORT     SERVICE\n"
    for open_port in open_ports:
      padding = 9 - len(str(open_port))
      service = ports_and_services.get(open_port)
      output += f"{open_port}{' ' * padding}{service}" 
      if open_port != open_ports[-1]: 
        output += "\n"
    return output

  # check if the supplied host is a valid name or IP address
  host_split = host.split(".")[0]                             # splitting 1x saved 0.4s
  try:
    ip_addr = socket.gethostbyname(host)
  except:
    if host_split.isnumeric():
      return "Error: Invalid IP address"
    else:
      return "Error: Invalid hostname"
  else:
    if host_split.isalpha():
      hostname = host
    else:
      try:
        hostname = socket.gethostbyaddr(host)[0]
      except:
        hostname = False

  # scan ports   
  for port in range(port_range[0], port_range[1]+1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # socket IPv4/TCP
    s.settimeout(0.5)                                       # timeout value

    # if a connection is made (no error), then add this port to the 'open_ports' list
    if s.connect_ex((host, port)) == 0:
      open_ports.append(port)

    s.close()

  return verbose_output(hostname, ip_addr) if verbose else open_ports
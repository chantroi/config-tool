import re
import base64
import json

edited = []
num = 1
def edit(link, set_uuid=None, set_sni=None, set_tag=None):
  code = link.split("://")[1]
  config = base64.b64decode(code).decode('utf-8')
  config = json.loads(config)
  add = config["add"]
  tag = config['ps']
  uuid = config['id']
  sni = config['sni']
  host = config['host']
  port = config['port']
  if add in ['127.0.0.1', '1.1.1.1', '0.0.0.0', '8.8.8.8'] or {str(add):uuid} in edited:
    return
  if set_tag:
    tag = f'{name} {num}'
  if set_uuid:
    uuid = set_uuid
  if set_sni:
    if port == 80:
      host = set_sni
    elif port == 443:
      sni = set_sni
    else:
      host = sni = set_sni
  edited.append({str()})
  num += 1
  config = json.dumps(config).encode('utf-8')
  code = base64.b64encode(config).decode('utf-8')
  link = f"vmess://{code}"
  return link
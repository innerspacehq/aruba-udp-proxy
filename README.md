# aruba-udp-proxy
A proxy designed to receive UDP wifi telemetry messages from Aruba WAPs or Aruba Controllers, then forward to InnerSpace via TLS.

<img width="1065" alt="aruba_udp_proxy_diagram" src="https://github.com/user-attachments/assets/cd12e851-a1ec-4488-ba22-cb4d40e1715c">

# Requirements
Packaged up as a Docker container, the only requirements are that the PASSPHRASE and HMAC environment variables are set

The docker container can be run standalone, or using the docker-compose.yml file

```
docker run -d \
  --name udp-proxy \
  --restart unless-stopped \
  --hostname udp-proxy \
  --domainname innerrspace-udp-proxy \
  --memory "1G" \
  --cpus "1" \
  -e HOST=${HOST} \
  -e PORT=${PORT} \
  -e PASSPHRASE=${PASSPHRASE} \
  -e HMAC=${HMAC} \
  -p ${HOST}:${PORT}:${PORT}/udp \
  aruba-udp-proxy:latest \
  python udp_proxy.py
```

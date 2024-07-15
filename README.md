# aruba-udp-proxy
A proxy designed to receive UDP wifi telemetry messages from Aruba WAPs or Aruba Controllers, then forward to InnerSpace via TLS.

<img width="1065" alt="aruba_udp_proxy_diagram" src="https://github.com/user-attachments/assets/cd12e851-a1ec-4488-ba22-cb4d40e1715c">

## Controller Configuration
To push the required WIFI data, the Aruba “RTLS Server configuration” must be completed (see pg 758 of the <a href="https://www.arubanetworks.com/techdocs/ArubaOS-8.x-Books/810/ArubaOS-8.10.0.0-User-Guide.pdf">ArubaOS User Guide</a> ).

### Option 1: CLI Configuration

Command line configuration can be applied as an ap system-profile, and assigned to an AP group.
```
(config)# rtls-server ip-or-dns <rtls collector server name> port <TCP port> key <secret/key> station-message-frequency 60 include-unassoc-sta enable
```

### Option 2: Controller GUI Configuration

See page 4 of <a href="https://github.com/innerspacehq/aruba-udp-proxy/blob/main/RTLS_integrationv6_2012.pdf">RTLS_integrationv6_2012.pdf</a>



## RTLS Collector (InnerSpace Proxy) Requirements
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


## References

1.  RTLS Integration Example and Documentation of the protocol - https://github.com/lukaskaplan/aruba-rtls - see **RTLS_integrationv6.docx** .
2.  ArubaOS 8.10 User Guide - https://www.arubanetworks.com/techdocs/ArubaOS-8.x-Books/810/ArubaOS-8.10.0.0-User-Guide.pdf
3.  Aruba DEMO reference guide - https://iot-utilities.arubademo.de/

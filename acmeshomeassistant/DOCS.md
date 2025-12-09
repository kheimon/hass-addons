# Configuration
This add-on only works properly after setting up a valid configuration!

## Add-on Configuration
Configure via the UI or simply create a yaml
```yaml
accountemail: mail@example.com
domains: [home.example.com] # set at least 1 domain
server: letsencrypt # you can also omit to choose the default server
dns: dns_acmedns # other dns apis are available, this is just an example
dnsEnvVariables: # the environment variables depend on your DNS api -> Check the wiki
  - name: ACMEDNS_BASE_URL
    value: acme-api.example.com
  - name: ACMEDNS_USERNAME
    value: example_username
  - name: ACMEDNS_PASSWORD
    value: example_password
  - name: ACMEDNS_SUBDOMAIN
    value: example_subdomain
keylength: ec-256 # supported values: 2048, 3072, 4096, 8192, ec-256, ec-384, ec-521 (or omit to use acme.sh's default)
fullchainfile: fullchain.pem # Recommendation: keep default value
keyfile: privkey.pem # Recommentation: keep default value
```

## Use the certificate for homeassistant Web-UI (optional)
Edit your config (`/config/configuration.yaml`) and set the ssl certificate and key. Here is an example snippet:
```yaml
...
http:
  ssl_certificate: /ssl/home.example.com/fullchain.pem
  ssl_key: /ssl/home.example.com/privkey.pem
  server_port: 443 # optional, be careful!
...
```
Keep in mind that your path will differ. Be careful about which port you choose. Low port numbers such as 443 may be privileged.

Additionally you may want to set internal/external homeassistant urls. You have 2 options to do that:
- In WebUI under **Settings** -> **Network** -> **Home Assistwnt URL**
- In `/config/config.yaml`
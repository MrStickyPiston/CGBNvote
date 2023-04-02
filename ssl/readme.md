# using a self signed ssl certificate  
## WARNING: this is not for trusted certificates, but for basic encryption possibility's. Don't use for production.  
  
Run the following commands in this folder (Requires openssl):  
**NOTE: skip additional values**  

```commandline
openssl genrsa -aes256 -passout pass:gsahdg -out server.pass.key 4096
openssl rsa -passin pass:gsahdg -in server.pass.key -out server.key
rm server.pass.key
openssl req -new -key server.key -out server.csr
openssl x509 -req -sha256 -days 365 -in server.csr -signkey server.key -out server.crt
```  
  
Then change the config.json file from  

```json
{
  ...
  "ssl_key": "None",
  "ssl_cert": "None",
  ...
}
```

to 
```json
{
  ...
  "ssl_key": "./ssl/server.key",
  "ssl_cert": "./ssl/server.crt",
  ...
}
```

Restart server.py now.
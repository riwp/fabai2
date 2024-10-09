

FabAI2

-----------------------
Progressive Web App
-----------------------

- extends fabai to make into a progressive web app that can be installed on phone
- adds support for https
- adds entry point for content to be posted directly to PWA
- Testing integration with iphone still in progress PWA works, still some things to work out with safari share to PWA
- Have not tested android

You will need to create your own certs or comment out in app load:
- You will need to generate your own certs and then install on ios (Replace $ variables with values)
- command to generate certs:  openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout "$KEY_FILE" -out "$CERT_FILE" -subj "/CN=$IP_ADDRESS" -addext "subjectAltName=DNS:$HostName,IP:$IP_ADDRESS"
- copy certificate.crt and private.key to aiwebui root directory
On IOS:
- share private.key with your ios app
- install by clicking on .cer (i used SMB samba share), VPN device Management, click on cert, install
- Then general, about, certificate trust settings, enable trust of certificate

For Progressive Web APP install (PWA)
- open aiwebui using https://[server]:5005
- use arrow to share, add home screen
- you should see icon as an app now on home screen that opens up

-----------------------
Add browse, retrieve, delete
-----------------------







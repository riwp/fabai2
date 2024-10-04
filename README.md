Update Linux
sudo apt update

Install Go
Required to install fabric
https://go.dev/doc/install

STEPS:
Download latest distro:
https://go.dev/dl/

Copy to path:
copy binaries to /usr/local/go/bin

Set export path:
export PATH=$PATH:/usr/local/go/bin

Verify installed:
go version

Install Fabric

Modular AI framework uses crowd sourced prompts to solve problems 

https://github.com/danielmiessler/fabric

STEPS:
# Linux (amd64): 
curl -L https://github.com/danielmiessler/fabric/releases/latest/download/fabric-linux-amd64 > fabric && chmod +x fabric && ./fabric --version

# Install Fabric directly from the repo
go install github.com/danielmiessler/fabric@latest

Install chromium-browser
Used in headless mode to download web page content from a URL

https://www.chromium.org/getting-involved/download-chromium/

STEPS:
Install:
sudo apt install chromium-browser

Install html2text
Used to cleanup web html content into text content

STEPS:
sudo apt install html2text

Install yt-dlp
Used to download YouTube 

sudo apt install yt-dlp



--------------------------------------------
Install pre-requisites
--------------------------------------------
1. Update Linux
    sudo apt update

2. Install Go
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

3. Install Fabric

    Modular AI framework uses crowd sourced prompts to solve problems 

    https://github.com/danielmiessler/fabric

    STEPS:
    # Linux (amd64): 
    curl -L https://github.com/danielmiessler/fabric/releases/latest/download/fabric-linux-amd64 > fabric && chmod +x fabric && ./fabric --version

    # Install Fabric directly from the repo
    go install github.com/danielmiessler/fabric@latest

4. Install chromium-browser
    Used in headless mode to download web page content from a URL

    https://www.chromium.org/getting-involved/download-chromium/

    STEPS:
    Install:
    sudo apt install chromium-browser

5. Install html2text
    Used to cleanup web html content into text content

    STEPS:
    sudo apt install html2text

6. Install yt-dlp
    Used to download YouTube 

    sudo apt install yt-dlp

--------------------------------------------
Modify service files with home directory and user
--------------------------------------------
7. Modify bash/fabai_aiwebui.service replacing home directory and user name
    nano bash/fabai_aiwebui.service

    ExecStart=/usr/bin/python3 /home/[Replace User Home Directory]/fabai/aiwebui/aiwebui.py
    WorkingDirectory=/home/[Replace User Home Directory]/fabai
    User=[Replace User]

8. Modify fabai_get_ai_insights.service replacing home directory and user name
    nano bash/fabai_get_ai_insights.service

    ExecStart=/usr/bin/python3 /home/[Replace User Home Directory]/fabai/aiwebui/aiwebui.py
    WorkingDirectory=/home/[Replace User Home Directory]/fabai
    User=[Replace User]

--------------------------------------------
Add services and check status
--------------------------------------------

9. Run add_services.sh
    sudo bash/add_services.sh

10. Check status of services post installation
    sudo bash/get_status.sh

--------------------------------------------
Open Web Application
--------------------------------------------

11. Go to Web Application aiwebui on port 5000
    Open a browser and go to URL:  http://[Server Name]:5005/


--------------------------------------------
Operation Type
--------------------------------------------

Summary:  Summarizes text
Claims:  Analyzes claims
Keynote: creates a keynote
MSummary: Creates a mini summary
Essay: Creates essay
Wisdom: My favorite and default!  Analyzes and provides Summary, Ideas, Insights, Quotes, Habits, Facts, References, Recommendations


--------------------------------------------
Web UI Functions
--------------------------------------------

Text Input: allows you to copy paste text and runs fabric AI
- Paste your text input
- Click Let's Go

AI Video: goes to youtube, gets transcript, and runs fabric AI
- Enter URL to Youtube video
- Click Let's Go

AI Web: goes to web site, downloads html, cleans up, and runs fabric AI
- Enter URL to web page to analyze
- Click Let's Go




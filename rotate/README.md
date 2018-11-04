# Rotate Screen on Boot

```bash
# cd ~/Documents/Source
# git clone https://github.com/CdLbB/fb-rotate.git
# cd fb-rotate
# gcc -w -o fb-rotate fb-rotate.c -framework IOKit -framework ApplicationServices
# code ~/Library/LaunchAgents/com.Lugia.fb-rotate.plist
```

put this:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN"
"http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
 <key>Label</key>
 <string>com.rai.fb-rotate</string>
 <key>ProgramArguments</key>
 <array>
 <string>/Users/rai/hackintosh/rotate/rotate.sh</string>
 </array>
 <key>RunAtLoad</key>
 <true/>
</dict>
</plist>
```

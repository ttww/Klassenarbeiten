## Klassenarbeiten

Synchronize classwork entries from Kepi Tübingen https://orga.kepi.de/gfs/login.php

This is a quick hack to copy & modify the "strange" classwork entries from the official web based classwork calender to my icloud calender...

How is it done?
- Login with the given credentials to the classwork calender (via user1/passwd1 and user2/passwd2 `.env` entries)
- Fetch the ICS file for one year
- Fix bad ICS data (eliminate double `DTSTAMP` entries) so that I can use the library to read it...
- Login to the icloud calender
- Loop over all entries from classwork calender and create new, slightly modified (title, alarm), entries for the icloud calender
- Optional create a QR code with the configured URL

*If you want to use it, you need to adjust a few lines in the src/main.py program, because the classes and calendar names are hardcoded (but this should be easy).*

#### Setup apple calender:
- create app-specific icloud password, see https://support.apple.com/en-us/102654
- Create two calender (one for each child) which the correct name (see code)
- Enable sharing and copy the calender url (starting with `webcal://...` to the config)
- Uncomment the QR code generation

#### Setup python

```bash
# Clone repository:
git clone https://github.com/ttww/Klassenarbeiten.git
cd Klassenarbeiten

# Setup python:
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### Setup credentials

You need to set up the credentials for the classwork and icloud calender.
For doing this copy the empty template file and adjust the values:
```bash
cp .env-copy-template .env
```
and edit the `.env` file. See the comments inside.
Do not add this file to git...

#### Running manually

Currently, the source code is running in an endless loop with a 6 hour pause in-between.
You can run it manually and stop it by hitting ctrl-c:

```bash
python src/main.py
```

Example output:
```bash
Start...
icloud_username =  *********@*****
Start...
Event: KA_13119  --> Klassenarbeit in Franz
Event: KA_13167  --> Klassenarbeit in NWT (ab Klasse 6)
Event: KA_12880  --> Klassenarbeit in Biologie
Event: KA_13502  --> Klassenarbeit in NWT (ab Klasse 6)
...
...
...
Event: KA_13485  --> Klassenarbeit in Erdkunde
Event: KA_13086  --> Klassenarbeit in ENGLISCH
Event: KA_13085  --> Klassenarbeit in ENGLISCH
Event: KA_13199  --> Klassenarbeit in Ethik
Event: KA_13130  --> Klassenarbeit in DEUTSCH
Event: KA_13468  --> Klassenarbeit in GESCHICHTE
Event: KA_13139  --> Klassenarbeit in Mathematik
Updload to iCloud
Updload to iCloud...Done
Events added to KA-Kepi-6c successfully!
...

Last updated at  2024-11-28 17:10:37.268468
Sleeping for 6 hour...
```

#### Running via docker

I run this service inside a docker container.
To create ist:
```bash
./create_docker.sh
```
And to run it in the background (restart option is 'unless-stopped'):
```bash
./run_docker.sh
```


#### ToDo
- Remove hardcoded strings for the calender name.
- Calender url can be taken from the connection.
- Create QR code only if the file is missing. 
- ...

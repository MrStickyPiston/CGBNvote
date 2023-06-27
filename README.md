# Using CGBNvote
### Requirements
| Type               | Required                                                      | Recommended                                                     |
|--------------------|---------------------------------------------------------------|-----------------------------------------------------------------|
| Operating system   | Windows / Linux                                               | Linux                                                           |
| Wi-Fi              | wireless / wired                                              | wired                                                           |
| Python             | [3.11](https://www.python.org/downloads/release/python-3110/) | [3.11.3](https://www.python.org/downloads/release/python-3113/) |
| Storage space      | 2GB                                                           | 2GB                                                             |
| total RAM memory   | 6GB                                                           | 8GB                                                             |
| program RAM memory | 2GB                                                           | 4GB                                                             |
| CPU speed          | 2.1 GHz                                                       | 3.6 GHz                                                         |
| CPU cores          | 4                                                             | 8                                                               |
| GPU                | Integrated                                                    | Integrated                                                      |
### Download
Install git and run `git clone https://github.com/MrStickyPiston/CGBNvote.git && cd CGBNvote` in the batch shell or click [here](https://github.com/MrStickyPiston/CGBNvote/archive/refs/heads/master.zip) to download as zip and unzip.
### Installation
Run setup.py. A terminal will pop up, showing the packages progress. After that your browser will open on the setup page. The setup page will ask for the following things:  

 - **server url**   
This will be used for sending the right link in the verification mails.
Choose between:  
   - your ip  
   - a domain linked to your ip. (If you have one.)

 - **mail**  
Enter the mail adress that will be used for verification mails.

 - **mail (app)password**  
The (app)password for the email adress you filled in above.

 - **admin username**  
Your username for the admin dashboard.

 - **admin password**  
Your password for the admin dashboard.

### Usage outside of the network
At default, CGBNvote allows everyone on the same network to access the site. If you want people outside of your network to access the vote site, you have to do some port forwarding on port 443 for ssl (https) or port 80 for tls (http). If you have access to your router you can look up a tutorial on the internet. Else you have to contact your network managers.  
If you have setup port forwarding and want the server to be more accessible you can connect a domain to your ip. Create an `A record` containing your ip in your DNS panel. Please note that it can take up to 24 hours before dns is updated.

### ssl (https)
To use ssl you need a certificate. You can create one yourself, but those self-signed certificates are only for testing. If you want to use the program you can just use normal http, or if you really care about the "this site is not protected" buy a certificate at a certificate authority.
Once you got a certificate you upload the `.key` and the `.cert` to `./ssl/`. Then you set the `config.json` file to use those certificates.

### running the server
Once you configurated your CGBNvote instance using the steps above, you can start the server by starting `server.py`. Navigate to the url that it gives you + `/admin-panel/` and edit the candidates to whatever you use the program for. Then change `"voting_enabled"` from 0 to 1 to enable voting.  
If you want to get rid of the port, for example `localhost:`~~`8080`~~ you have to run server.py as root / administrator. The program will automatically choose the right port for http/https. For http the standard port is `80`, for https `443`. If a webserver is run on one of these ports, the webbrowser automatically adds it to the address, thus leaving no visible port.


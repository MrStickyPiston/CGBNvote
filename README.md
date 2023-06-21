# Using CGBNvote
### Requirements
| Type               | Required                                                      | Recommended                                                     |
|--------------------|---------------------------------------------------------------|-----------------------------------------------------------------|
| Operating system   | Windows / Linux                                               | Linux                                                           |
| Python             | [3.11](https://www.python.org/downloads/release/python-3110/) | [3.11.3](https://www.python.org/downloads/release/python-3113/) |
| Storage space      | 2GB                                                           | 2GB                                                             |
| total RAM memory   | 6GB                                                           | 8GB                                                             |
| program RAM memory | 2GB                                                           | 4GB                                                             |
| CPU speed          | 2.1 GHz                                                       | 3.6 GHz                                                         |
| CPU cores          | 4                                                             | 8                                                               |
| GPU                | Integrated                                                    | Integrated                                                      |

### Installation
Run setup.py. A terminal will pop up. The installation script will ask for the following things:  

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
IMPORTANT: make this a strong password that is hard to crack. Else hackers can hack into your account.  

### Usage outside of the network
At default, CGBNvote allows everyone on the same network to access the site. If you want people not on your network to access the vote site, you have to do some port forwarding on port 443 for ssl or port 80 for tls. If you have access to your router you can look up a tutorial on the internet. Else you have to contact your network managers.  
If you have setup port forwarding and want the server to be more accessible you can connect a domain to your ip. Create a A record containing your ip. In the file config.json, replace the `"url":"OLD_VALUE"` with `"url":"YOUR_DOMAIN"`. Note that it can take up to 24 hours before dns is updated.

### ssl (https)
To use https you need a certificate. You can create one yourself, but those self-signed certificates show a security warning on most browsers. If you dont want that you can use normal http, or buy a certificate at a certificate authority.
Once you got a certificate you upload the `.key` and the `.cert` to `./ssl/`. Then you add them to the `config.json` file.

### running the server
Once you configurated your CGBNvote instance using the steps above, you can start the server by starting `server.py`. Navigate to the url that it gives you + `/admin-panel/` and edit the candidates to whatever you use the program for. Then change `"voting_enabled"` from 0 to 1 to enable voting.  
If you want to get rid of the port, for example localhost:*8080* you have to run server.py as root / administrator. The program will automatically choose the right port for http/https. For http the standard port is `80`, for https `443`. If a webserver is ran on one of these ports, the webbrowser automatically adds it to the address, thus leaving no visible port.


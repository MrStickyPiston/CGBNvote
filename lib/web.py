import subprocess
import sys

from bottle import route, get, post, request, run, static_file, template, error, response, redirect
from ast import literal_eval
import smtplib, ssl, os, json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import lib

sslcontext = ssl.create_default_context()
try:
    with open("config.json", 'r') as file:
        data = json.load(file)

        mailserver = data["mail"]
        mailserver_password = data["mail_password"]
        mail_domain = data["mail_domain"]

        try:
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=sslcontext)
            server.login(mailserver, mailserver_password)
            server.close()
            disable_mail = False
        except Exception:
            print("ERROR: incorrect mail credentials")
            disable_mail = True
        page_url = data["url"]
except Exception:
    exit("Incorrect config file")


@error(404)
def error404(e):
    return template("custom", {"content": "404 page not found"})


@error(500)
def error500(e):
    return template("custom", {"content": "500 internal server error. Neem contact op met de administrator."})


@route('/static/<filename>')
def static(filename):
    con = lib.database.connect("database.db")
    con.commit()

    if filename == "results.webp" and lib.database.get_setting(con,
                                                               "voting_active") == "1" and lib.database.get_setting(con,
                                                                                                                    "live_results") == "0":
        return "Sorry, maar je mag dit bestand nog niet bekijken."
    return static_file(filename, root=os.getcwd() + "/static/")


@route('/favicon.ico')
def icon():
    return static_file("favicon.png", root=os.getcwd() + "/static")


def send_mail(code, email):
    message = MIMEMultipart("alternative")
    message["Subject"] = "CGBNvote auth"
    message["From"] = mailserver
    message["To"] = email

    con = lib.database.connect("database.db")
    duration = lib.database.get_setting(con, "code_duration")

    text = f"""\
Je authenticatiecode voor CGBNvote is {code[0]}.\nDeze code vervalt over {duration} minuten."""
    styledMail = template("mail", {"code": code[0], "PAGE_URL": page_url, "code_duration": duration})
    message.attach(MIMEText(text, "plain"))
    message.attach(MIMEText(styledMail, "html"))

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=sslcontext)
    server.login(mailserver, mailserver_password)
    server.sendmail(mailserver, email, message.as_string())
    server.close()


def admin_panel_html(user):
    con = lib.database.connect("database.db")

    candidates = lib.database.get_candidates(con)
    settings = lib.database.get_settings(con)
    con.commit()

    payload = {
        "candidates": str(candidates),
        "settings": str(settings),
        "username": user
    }
    return template("admin_panel", payload)


@get('/admin-panel')
def admin_panel():
    con = lib.database.connect("database.db")
    user = lib.database.verify_session(con, request.get_cookie("SESSION"))

    if user is not None:
        return admin_panel_html(user)
    else:
        redirect('/admin-login')


@get('/admin-login')
def vote_admin_login():
    con = lib.database.connect("database.db")
    user = lib.database.verify_session(con, request.get_cookie("SESSION"))

    if user is not None:
        redirect('/admin-panel')
        return

    return template("admin_login", {"script": "", "closetab": request.params.get('close')})


@post('/admin-login')
def vote_admin_panel():
    con = lib.database.connect("database.db")
    user = lib.database.verify_session(con, request.get_cookie("SESSION"))

    if request.forms.get('closetab') == "1":
        return template("script", {"script": "window.close();"})

    if user is not None:
        redirect('/admin-panel')
        return

    con.commit()

    user = request.forms.get('user')
    password = request.forms.get('password')

    print("Verifying admin")
    succes = lib.database.verify_admins(con, user, password)
    con.commit()

    if succes:
        print(f"Successful login attempt at /admin-login by {user}")

        session = lib.encryption.generate_session()

        lib.database.set_session(con, session, user)
        response.set_cookie("SESSION", session, path='/', samesite=None, max_age=60 * 10)
        con.close()

        redirect('/admin-panel')
        return

    else:
        print(f"Failed login attempt at /admin-login by {user}")
        con.close()
        return template("admin_login", {
            "script": "alert('Het opegegeven wachtwoord komt niet overeen met de gebruikersnaam. Controleer of uw gegevens correct zijn.'); history.back()"})


@post('/admin-panel/process')
def process_changes():
    username = request.forms.get('username')
    con = lib.database.connect("database.db")

    if username == lib.database.verify_session(con, request.get_cookie("SESSION")):
        candidates = literal_eval(request.forms.get('candidate_list'))
        settings = literal_eval(request.forms.get('setting_list'))

        print(f"Successful login attempt at /admin-panel/process by {username}")
        print(f"""Updating the changes from the admin dashboard:\ncandidates:\t{candidates}\nsettings:\t{settings}""")

        lib.database.set_candidates(con, candidates)
        lib.database.set_settings(con, settings)
        con.commit()
        return template("script", {"script": "alert('De wijzigingen zijn successvol verwerkt.'); location.href = '/admin-login'"})

    else:
        print(f"Failed login attempt at /admin-panel/process by {username}")
        con.commit()
        return template("script", {
            "script": "alert('Uw sessie id klopt niet. Vernieuw uw sessie bovenaan het admin-panel.'); history.back()"})


@post('/admin-panel/reset_auth')
def reset_auth():
    user = request.query["user"]
    con = lib.database.connect("database.db")

    if user == lib.database.verify_session(con, request.get_cookie("SESSION")):
        lib.database.delete_codes(con)
        print(f"Successful login attempt at /admin-panel/reset-auth by {user}")
        con.commit()

        return 'De wijzigingen zijn successvol verwerkt.'
    else:
        print(f"Failed login attempt at /admin-panel/reset-auth by {user}")
        con.commit()

        return 'Uw sessie id klopt niet. Vernieuw uw sessie bovenaan het admin-panel.'


@post('/admin-panel/check_auth')
def check_auth():
    user = request.query["user"]
    con = lib.database.connect("database.db")

    if user == lib.database.verify_session(con, request.get_cookie("SESSION")):
        con.commit()
        response.status = 200
        return
    else:
        con.commit()
        response.status = 401
        return


@post('/admin-panel/reset_votes')
def reset_auth():
    user = request.query["user"]
    con = lib.database.connect("database.db")

    if user == lib.database.verify_session(con, request.get_cookie("SESSION")):
        lib.database.delete_votes(con)
        print(f"Successful login attempt at /admin-panel/reset_votes by {user}")
        try:
            os.remove(os.getcwd() + '/static/results.webp')
        except Exception:
            pass
        con.commit()
        return 'De stemmen zijn uit de database verwijdert. Restart de server voor resultaten op /vote-results'

    else:
        print(f"Failed login attempt at /admin-panel/reset_votes by {user}")
        con.commit()
        return 'Uw sessie id klopt niet. Vernieuw uw sessie bovenaan het admin-panel.'


@get('/admin-panel/log_out')
def log_out():
    con = lib.database.connect("database.db")
    lib.database.logout_session(con, request.get_cookie("SESSION"))
    con.commit()

    response.set_cookie("SESSION", '', expires=0)
    redirect("/admin-login")


@get('/')
def collect_vote():
    def candidates_html():
        start = '<select name="vote" id="vote" required>\n<option value="" selected disabled hidden> Selecteer waarop je wil stemmen </option>'
        mid = ''
        end = '</select>\n'

        con = lib.database.connect("database.db")
        candidates = lib.database.get_candidates(con)

        for i in candidates:
            mid += f'<option value="{i[1]}">{i[0]}</option>\n'

        return start + mid + end

    con = lib.database.connect("database.db")
    if lib.database.get_setting(con, "voting_active") == "0":
        con.close()
        return template("custom", {
            "content": "De verkiezingen zijn nu helaas niet actief. Kijk <a href=/results>hier</a> voor de resultaten."})

    payload = {
        "vote_name": lib.database.get_setting(con, "vote_name"),
        "select_vote": candidates_html()
    }

    con.close()
    return template("collect_votes", payload)


@post('/')
def process_vote():
    con = lib.database.connect("database.db")
    if lib.database.get_setting(con, "voting_active") == "0":
        con.close()
        return template("custom", {
            "content": "De verkiezingen zijn nu helaas niet actief. Kijk <a href=/results>hier</a> voor de resultaten."})
    con.close()

    userid = request.forms.get('user')
    code = request.forms.get('code')
    vote = request.forms.get('vote')

    con = lib.database.connect("database.db")
    success = lib.database.insert_vote(con, userid, code, vote)

    vote_display = "NONE"

    if success == "success":
        candidates = lib.database.get_candidates(con)
        for i in candidates:
            if i[1] == vote:
                vote_display = i[0]
                break
        return template("custom", {
            "content": f"Bedankt voor het stemmen op {vote_display}. Je stem zal anoniem worden verwerkt."})
    else:
        if success == "authException":
            error = f"De code komt niet overeen met de gebruiker {userid}"
        elif success == "credentialsNotFoundException":
            error = f"Gebruikersnaam {userid} niet gevonden in het systeem"
        elif success == "alreadyVotedException":
            error = "U kunt helaas geen tweede keer stemmen."
        elif success == "codeExpiredException":
            error = "De tijd om te stemmen met deze code is verlopen. Vraag een nieuwe code aan om te stemmen."
        elif success == "candidateException":
            error = f"Error: Kandidaat {vote_display} niet gevonden. rapporteer dit aan de administrator."
        else:
            error = success
        return template("custom", {"content": error})


@post('/send_code')
def send_code():
    if disable_mail:
        return "De mailservers zijn momenteel niet beschikbaar. Vraag aan de beheerder of dit een fout is."

    try:
        con = lib.database.connect("database.db")
        if lib.database.get_setting(con, "voting_active") == "0":
            con.close()
            return f"De verkiezingen zijn nu helaas niet actief. Kijk op {page_url}/vote_results voor de resultaten."

        email = request.query["userid"] + "@" + mail_domain
        code = lib.database.generate_code(con, request.query["userid"])

        if code[1] == "alreadyVotedException":
            return "Sorry, maar u hebt al gestemd."
        elif code[1] == "codeNotExpiredException":
            return "Sorry, maar u hebt al een werkende code ontvangen / is naar u op weg."
        else:
            send_mail(code, email)
            print(f"Successfully send a email to {email}")
            return f"De authenticatiecode is succesvol verzonden naar {email}."
    except Exception as e:
        print(f"Failed to send email to {email}")
        return e


@get('/results')
def vote_results():
    con = lib.database.connect("database.db")

    results = '<img src=/static/results.webp style="max-width:100%"></img>'
    if lib.database.get_setting(con, "voting_active") == "1" and lib.database.get_setting(con, "live_results") == "0":
        results = "<p>Sorry, maar de uitslagen zijn nu nog niet beschikbaar.</p>"
    else:
        subprocess.check_call([sys.executable, "lib/plot.py"])

    con.commit()
    return template("custom", {"content": results})


# SERVER FUNCTIONS
def serve_bottle(host, port):
    run(host=host,
        port=port,
        reloader=1,
        )


def serve_http(host, port, server_adapter, workers=2 * os.cpu_count()):
    run(host=host,
        port=port,
        server=server_adapter,
        workers=workers,
        reloader=1,
        )


def serve_https(host, port, server_adapter, workers=2 * os.cpu_count(), ssl_key='ssl/server.key',
                ssl_cert='ssl/server.crt'):
    sslcontext.load_default_certs()
    run(
        host=host,
        port=port,
        server=server_adapter,
        workers=workers,
        reloader=1,
        keyfile=ssl_key,
        certfile=ssl_cert
    )


if __name__ == "__main__":
    print("Starting debug")
    serve_bottle("localhost", 8080)

from bottle import get, post, request, run
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import lib

sslcontext = ssl.create_default_context()
mailserver = "mr.sticky.piston@gmail.com"
mailserver_password = "XXXXXX"

page_url = "localhost:8080"


def send_mail(code, email):
    message = MIMEMultipart("alternative")
    message["Subject"] = "CGBNvote auth"
    message["From"] = mailserver
    message["To"] = email

    text = f"""\
Je authenticatiecode voor CGBNvotes is {code[0]}.\nGebruik deze code om online te stemmen.\nNa de verkiezingen kun je de uitslag bekijken op {page_url}."""
    html = "".join(open("web/mail.html").readlines()).replace("{code}", code[0]).replace("{PAGE_URL}", page_url)
    message.attach(MIMEText(text, "plain"))
    message.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=sslcontext) as server:
        server.login(mailserver, mailserver_password)
        server.sendmail(mailserver, email, message.as_string())


def candidates_html():
    start = '<select name="vote" id="vote">\n'
    mid = ''
    end = '</select>\n'

    con = lib.database.connect("database.db")
    candidates = lib.database.get_candidates(con)

    for i in candidates:
        mid += f'<option value="{i[1]}">{i[0]}</option>\n'

    return start + mid + end


@get('/vote-admin')
def vote_admin_login():
    return "".join(open("web/admin_login.html").readlines()).replace("{script}", "")

@post('/vote-admin')
def vote_admin_panel():
    user = request.forms.get('user')
    password = request.forms.get('password')

    con = lib.database.connect("database.db")
    succes = lib.database.verify_admins(con, user, password)
    con.close()

    if succes:
        return "".join(open("web/admin_panel.html").readlines())
    else:
        return "".join(open("web/admin_login.html").readlines()).replace("{script}", 'alert("Het opegegeven wachtwoord komt niet overeen met de gebruikersnaam. Controleer of uw gegevens correct zijn.")')

@get('/vote')
def collect_vote():
    html = "".join(open("web/collect_votes.html").readlines()).replace("{select_vote}", candidates_html())
    return html

@post('/vote')
def process_vote():
    userid = request.forms.get('user')
    code = request.forms.get('code')
    vote = request.forms.get('vote')

    con = lib.database.connect("database.db")
    success = lib.database.insert_vote(con, userid, code, vote)
    if success == "success":
        candidates = lib.database.get_candidates(con)
        vote_display = "NONE"
        for i in candidates:
            if i[1] == vote:
                vote_display = i[0]
                break
        return "".join(open("web/vote_success.html").readlines()).replace("{vote}", vote_display)
    else:
        error = ""
        if success == "authException":
            error = "De code komt niet overeen met de gebruiker"
        elif success == "alreadyVotedException":
            error = "U kunt helaas geen tweede keer stemmen."
        elif success == "codeExpiredException":
            error = "De tijd om te stemmen met deze code is verlopen. vraag een nieuwe code aan om te stemmen."
        elif success == "candidateException":
            error = "Error: Kandidaat niet gevonden. rapporteer dit aan de administrator."
        else:
            error = success
        return "".join(open("web/vote_error.html").readlines()).replace("{error}", error)


@post('/send_code')
def send_code():
    email = request.query["userid"] + "@cgbn.nl"

    con = lib.database.connect("database.db")
    code = lib.database.generate_code(con, request.query["userid"])

    if code[1] == "alreadyVotedException":
        return "Sorry, maar u hebt al gestemd."
    elif code[1] == "codeNotExpiredException":
        return "Sorry, maar u hebt al een werkende code ontvangen / is naar u op weg."
    else:
        send_mail(code, email)
        return f"De authenticatiecode is succesvol verzonden naar {email}."


def serve(host, port):
    run(host=host, port=port)


if __name__ == "__main__":
    print("Starting debug")
    serve("localhost", 8080)

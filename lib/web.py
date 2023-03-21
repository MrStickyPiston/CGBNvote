from bottle import get, post, request, run
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import lib

sslcontext = ssl.create_default_context()
mailserver = "mr.sticky.piston@gmail.com"
mailserver_password = "XXXXXX"


def send_mail(code, email):
    message = MIMEMultipart("alternative")
    message["Subject"] = "CGBNvote auth"
    message["From"] = mailserver
    message["To"] = email

    text = f"""\
Authentication code
Your authentication code for the CGBN votes at PAGE_URL is {code[0]}.

If you did not request this code, you can ignore this email."""
    html = "".join(open("web/mail.html").readlines()).replace("{code}", code[0])
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


@get('/vote')
def collect_vote():
    html = "".join(open("web/index.html").readlines())
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
        return "".join(open("web/vote_success.html").readlines()).replace("{vote}", success)


@post('/send_code')
def send_code():
    email = request.query["userid"] + "@cgbn.nl"

    con = lib.database.connect("database.db")
    code = lib.database.generate_code(con, request.query["userid"])

    if code[1]:
        send_mail(code, email)
        return f"succesfully send a code to {email}"
    else:
        return f"Sorry, but you already voted"


def serve(host, port):
    run(host=host, port=port)


if __name__ == "__main__":
    print("Starting debug")
    serve("localhost", 8080)

import poplib
import email
import time


class MailHelper:

    def __init__(self, app):
        self.app = app

    def get_mail(self, username, password, subject):
        for i in range(5):
            pop = poplib.POP3(self.app.config['james']['host'])
            pop.user(username)
            pop.pass_(password)
            letters = pop.stat()[0]  # получить количество писем
            if letters > 0:
                for n in range(letters):
                    msg_lines = pop.retr(n+1)[1]  # открыть письмо, индексация с 1
                    msg_text = '\n'.join(map(lambda x: x.decode('utf-8'), msg_lines))
                    msg = email.message_from_string(msg_text)
                    if msg.get('Subject') == subject:
                        pop.dele(n+1)
                        pop.quit()
                        return msg.get_payload()
            pop.close()
            time.sleep(3)
        return None

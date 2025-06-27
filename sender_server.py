import zenoh
import time

conf = zenoh.Config()

zenoh.init_log_from_env_or("error")

class Salon :

    def __init__(self, key):
        self.key = key
        self.messages = []

    def add_msg(self, s):
        self.messages.append(s)

    def get_msgs(self):
        return self.messages

salons = {}

def callback(query : zenoh.Query):
    key = f"{query.selector}"
    print(f"get recu {key}")
    if key in salons :
        sal = salons[key]
        msgs = sal.get_msgs()
        print("Salon trouvé")
        for m in msgs:
            query.reply(key, m)
    else :
        print("Salon non trouvé")

def listener(sample: zenoh.Sample):
    global salons
    s = sample.payload.to_string() 
    key = f"{sample.key_expr}"
    if key in salons:
        sal = salons[key]
    else:
        sal = Salon(key)
        salons[key] = sal
    sal.add_msg(s)
    print(
        f">>> {key} : {len(sal.get_msgs())} messages stockés."
    )    

with zenoh.open(conf) as session:
    key = "chat/*"
    session.declare_queryable(key, callback)
    session.declare_subscriber(key, listener)
    print("Lancement du serveur terminé...")
    print("Pour arretez le serveur, tapez : /shutdown ")
    while True :
        time.sleep(1)


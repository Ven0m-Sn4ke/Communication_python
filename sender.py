import zenoh
import json

conf = zenoh.Config()

user_name= ""

zenoh.init_log_from_env_or("error")

print("Entrain de rejoindre le chat...")
print("Pour quitter : Ctrl + C")

def listener(sample: zenoh.Sample):
    global user_name
    s = sample.payload.to_string() 
    s_user_name = s.split(" : ")[0]
    if s_user_name != user_name :
        print(
            f">> {s}"
        )
    
with zenoh.open(conf) as session:
    key = "chat1"
    session.declare_subscriber(key, listener)
    fini = False
    while user_name== "" :
        user_name= input("Nom d'uilisateur : ")
    while not fini:
        message = input("")
        s = user_name+ " : " + message
        session.put(key, s)
    
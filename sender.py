import zenoh
import json

conf = zenoh.Config()

user_name= ""

zenoh.init_log_from_env_or("error")

print("Entrain de rejoindre le chat...")
print("Pour quitter, tapez : /leave")

def listener(sample: zenoh.Sample):
    global user_name
    s = sample.payload.to_string() 
    s_user_name = s.split(" : ")[0]
    if s_user_name != user_name :
        print(
            f"\n>>> {s}"
        )
        print("> ", end=" ", flush=True)
    
with zenoh.open(conf) as session:
    key = "chat"
    key_salon = ""
    fini = False
    while user_name== "" :
        user_name= input("Nom d'utilisateur : ")
    while key_salon == "" :
        print("Differents salons accesibles :")
        print("Commun")
        print("ou créer le votre")
        key_salon = input("Choix de salon : ")
    key = key + "/" + key_salon
    session.declare_subscriber(key, listener)
    session.put(key, user_name + " : " + "< a rejoint le salon : " + key_salon + " >")
    while not fini:
        message = input("> ")
        if message == "/leave" :
            session.put(key, user_name + " : " + "< a quitté(e) le chat >")
            print("Vous avez quittez le chat")
            fini = True
        else :
            s = user_name+ " : " + message
            session.put(key, s)
        
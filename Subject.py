import json, requests, subprocess
#CLIENT

def run():

    Port_Commander = input("Enter port of commander")
    IP_Commander = input("Enter IP of Commander ")
    Commit_Count = 0    #Initializing commit count 0 at start

    req = requests.get("http://{}:{}/repo".format(IP_Commander,Port_Commander), json={'FetchStatus': False})
    string_json = json.loads(req.text)
    print ("Printing")
    print (string_json)
    Url_Repository = string_json['repo']

    subprocess.call(["bash", "SubjectScript.sh", Url_Repository])

    req = requests.get("http://{}:{}/repo".format(IP_Commander,Port_Commander), json={'FetchStatus': True})

    Pending_Commit = True

    while Pending_Commit:

        req = requests.get("http://{}:{}/Cyclo".format(IP_Commander,Port_Commander))
        string_json = json.loads(req.text)
        print(string_json)
        print("Response: {}".format(string_json['msg']))
        if string_json['msg'] == -2:

           print("Checking")

        else:

            if string_json['msg'] == -1:
                print("All done!!")
                break
            subprocess.call(["bash", "SubjectCommit.sh", string_json['msg']])
            #exit()

            RadonOutput = subprocess.check_output(["lizard","SubjectCommitTest"])

            radonCCOutput = RadonOutput.decode("utf-8")

            print(radonCCOutput)



            lastline = radonCCOutput.splitlines()[-1:]
            CC_Average = lastline[0].split()[2]
            print ("Value of last line is")
            print (lastline)
            print ("Value of CC_Average is")
            print (CC_Average)

            if CC_Average=="":
                print("Error! No file needed..")

                req = requests.post("http://{}:{}/Cyclo".format(IP_Commander,Port_Commander),
                                  json={'CommitSub': string_json['msg'], 'CycloComp': -1})
            else:
                print(CC_Average)
                req = requests.post("http://{}:{}/Cyclo".format(IP_Commander,Port_Commander),
                                  json={'CommitSub': string_json['msg'], 'CycloComp': CC_Average})

            Commit_Count = Commit_Count + 1



if __name__ == "__main__":
    run()

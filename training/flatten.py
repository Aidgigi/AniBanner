import os

def flatten():
    dirs = os.listdir("../../NewTrain/512px")

    for dir in dirs:
        if dir in (".DS_Store", "metadata.json.tar.xz.part"):
            continue

        for file in os.listdir(f"../../NewTrain/512px/{dir}"):
            if file.endswith(".part"):
                continue

            with open(f"../../NewTrain/512px/{dir}/{file}", 'rb') as f1:
                with open (f"./set/positive/{file}", 'wb') as f2:
                    f2.write(f1.read()) 

flatten()
import os

def flatten():
    dirs = os.listdir("./danbooru2020/512px")

    for dir in dirs:
        if dir in (".DS_Store", "metadata.json.tar.xz.part"):
            continue

        for file in os.listdir(f"./danbooru2020/512px/{dir}"):
            if file.endswith(".part"):
                continue

            with open(f"./danbooru2020/512px/{dir}/{file}", 'rb') as f1:
                with open (f"./negative/{file}", 'wb') as f2:
                    f2.write(f1.read()) 

flatten()
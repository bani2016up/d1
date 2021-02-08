import sys
import requests

base_url = "https://api.trello.com/1/{}"

auth_params = {
    "key": "",
    "token": "",
}

board_id = ""


def read():

    column_data = requests.get(base_url.format("boards") + "/" + board_id + "/lists", params=auth_params).json()

    for column in column_data:

        task_data = requests.get(base_url.format("lists") + "/" + column["id"] + "/cards", params=auth_params).json()
        print(column["name"] + " - ({})".format(len(task_data)))

        if not task_data:
            print("\t" + "РќРµС‚ Р·Р°РґР°С‡!")
            continue
        for task in task_data:
            print("\t" + task["name"] + "\t" + task["id"])




def create(name, column_name):
    column_id = column_check(column_name)
    if column_id is None:
        column_id = c_col(column_name)["id"]

    requests.post(base_url.format("cards"), data={"name": name, "idList": column_id, **auth_params})

    def column_check(column_name):
    column_data = requests.get(base_url.format("boards") + "/" + board_id + "/lists", params=auth_params).json()
    for column in column_data:
        if column["name"] == column_name:
            return column["id"]
    return


def move(name, column_name):
    duplicate_tasks = get_new_task(name)
    if len(duplicate_tasks) > 1:
        print("Р—Р°РґР°С‡ СЃ С‚Р°РєРёРј РЅР°Р·РІР°РЅРёРµРј РЅРµСЃРєРѕР»СЊРєРѕ С€С‚СѓРє:")
        for index, task in enumerate(duplicate_tasks):
            task_column_name = requests.get(base_url.format("lists") + "/" + task["idList"], params=auth_params).json()["name"]
            print("Р—Р°РґР°С‡Р° в„–{}\tid: {}\tРќР°С…РѕРґРёС‚СЃСЏ РІ РєРѕР»РѕРЅРєРµ: {}\t ".format(index, task["id"], task_column_name))
        task_id = input("РџРѕР¶Р°Р»СѓР№СЃС‚Р°, РІРІРµРґРёС‚Рµ ID Р·Р°РґР°С‡Рё, РєРѕС‚РѕСЂСѓСЋ РЅСѓР¶РЅРѕ РїРµСЂРµРјРµСЃС‚РёС‚СЊ: ")
    else:
        task_id = duplicate_tasks[0]["id"]

    column_id = column_check(column_name)
    if column_id is None:
        column_id = c_col(column_name)["id"]


    requests.put(base_url.format("cards") + "/" + task_id + "/idList", data={"value": column_id, **auth_params})



def c_col(column_name):
    return requests.post(base_url.format("lists"), data={"name": column_name, "idBoard": board_id, **auth_params}).json()


def get_new_task(task_name):


    column_data = requests.get(base_url.format("boards") + s"/" + board_id + "/lists", params=auth_params).json()
    duplicate_tasks = []
    for column in column_data:
        column_tasks = requests.get(base_url.format("lists") + "/" + column["id"] + "/cards", params=auth_params).json()
        for task in column_tasks:
            if task["name"] == task_name:
                duplicate_tasks.append(task)

    return duplicate_tasks


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == "create":
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "c_col":
        c_col(sys.argv[2])
    elif sys.argv[1] == "move":
        move(sys.argv[2], sys.argv[3])

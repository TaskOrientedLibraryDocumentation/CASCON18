import os
import pdb
import json
import random
from pymongo import MongoClient
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def get_client():
    client = MongoClient('localhost', 27017)
    return client.librarytasks.survey


def average(data):
    learning = 0
    lot = 0
    snippets = 0
    insights = 0
    task = 0

    for item in data:
        learning += int(item["learning"])
        lot += int(item["list_of_tasks"])
        snippets += int(item["snippets"])
        insights += int(item["insights"])
        task += int(item["task"])
        # print(item["task"])



    learning /= len(data)
    lot /= len(data)
    snippets /= len(data)
    insights /= len(data)
    task /= len(data)

    print("learning: {}\nlot: {}\nsnippets: {}\ninsights: {}\ntask: {}".format(learning, lot, snippets, insights, task))


def results():
    db = get_client()

    all = list(db.find())

    tasks = []
    finishes = []
    all_items = []

    for item in all:
        if item.get("finish", None):
            finishes.append(item["finish"])
            all_items.append(item)

        if item.get("response_1", None):
            tasks.append(item["response_1"])
        if item.get("response_2", None):
            tasks.append(item["response_2"])
        if item.get("response_3", None):
            tasks.append(item["response_3"])

    # print("{},{},{},{},{}".format(
    #     "list_of_tasks", "learning", "insights", "task","snippets"
    # ))


    # for item in all_items: 
    #     print("{},{},{},{},{}".format(
    #         item["finish"]["list_of_tasks"],
    #         item["finish"]["learning"],
    #         item["finish"]["insights"],
    #         item["finish"]["task"],
    #         item["finish"]["snippets"],
    #     ))

    tasks_res = {
        "yes": 0,
        "no": 0,
        "idk": 0,
        "seem": 0,
    }

    for item in tasks:
        if item["task"] == "Yes":
            tasks_res["yes"] += 1
        if item["task"] == "No":
            tasks_res["no"] += 1
        if item["task"] == "idk":
            tasks_res["idk"] += 1
    print(len(tasks))
    print(tasks_res)

    return tasks_res


    # snippets_res = {
    #     "count": 0,
    #     "num": 0,
    # }

    # for item in tasks:
    #     for sc in item["snippets"]:
    #         snippets_res["count"] += int(sc)
    #         snippets_res["num"] += 1


    # insights_res = {
    #     "count": 0,
    #     "num": 0,
    # }

    # for item in tasks:
    #     for sc in item["snippets"]:
    #         print(sc)
    #         insights_res["count"] += int(sc)
    #         insights_res["num"] += 1

    # pdb.set_trace()

    # for item in snippets_res:
    #     print(item)


def main():
    db = get_client()

    data = list(db.distinct("finish"))
    finish = len(data)
    tasks = len(list(db.distinct("response_1"))) + len(list(db.distinct("response_2"))) + len(list(db.distinct("response_3")))
    total = db.count()

    print("finish: {}\ntasks: {}\ntotal: {}\n".format(finish, tasks, total))

    average(data)

# def get_comments():
#     db = get_client()
#     comments = list(db.distinct("finish"))
#     for comment in comments:
#         if comment["comments"] != "":
#             print(comment["comments"])


def all_data():
    db = get_client()

    data = list(db.find({"finish": { "$exists": True }}))
    # print("{},{},{},{},{},{},{},{}".format(
    #     "profession",
    #     "proficiency",
    #     "experience",
    #     "library",
    #     "task1_response",
    #     "task2_response",
    #     "task3_response",
    #     "exit_questions"
    # ))
    for item in data:
        if not "response_1" in item:
            item["response_1"] = ""
        if not "response_2" in item:
            item["response_2"] = ""
        if not "response_3" in item:
            item["response_3"] = ""
        obj = {
            "profession": item["profession"].__str__(),
            "proficiency": item["proficiency"].__str__(),
            "experience": item["experience"].__str__(),
            "library": item["library"].__str__(),
            "task1_response": item["response_1"].__str__(),
            "task2_response": item["response_2"].__str__(),
            "task3_response": item["response_3"].__str__(),
            "exit_questions": item["finish"].__str__(),
        }
        
        print(obj)
        # exit()

    # with open("all_res.json", "w") as infile:
    #     infile.write({
    #         "data": data
    #     }.__str__())

    return data


def library_response_dist():
    all_res = all_data()

    fig = plt.figure()


    libs = {}

    for item in all_res:

        if libs.get(item["library"], None):
            libs[item["library"]] += 1
        else:
            libs[item["library"]] = 1

    Y = []
    X_ticks = []

    for lib, count in libs.items():
        X_ticks.append(lib)
        Y.append(count)

    objects = tuple(X_ticks)
    y_pos = np.arange(len(objects))


    plt.bar(y_pos, Y, align='center', alpha=0.5, color='k')
    plt.xticks(y_pos, objects, rotation=90)
    plt.ylabel("Number of responses")
    plt.title("Number of responses per library")
    plt.subplots_adjust(bottom=0.3)

    # plt.show()
    fig.savefig('plot.png')


def background_distro():
    all_res = all_data()
    fig = fig, (ax2, ax1) = plt.subplots(2, 1, figsize=(6, 13))

    professions = {}
    for item in all_res:
        if professions.get(item["profession"], None):
            professions[item["profession"]] += 1
        else:
            professions[item["profession"]] = 1


    professions = {
        "Undergrad CS Student": 12,
        "Academic Researcher": 2, 
        "Industrial Developer": 30,
        "Graduate CS Student": 25,
    }


    X_ticks = []
    Y = []

    for back, count in professions.items():
        X_ticks.append(back)
        Y.append(count)

    objects = tuple(X_ticks)
    y_pos = np.arange(len(objects))


    ax1.bar(y_pos, Y, align='center', alpha = 0.5, color='k')
    ax1.set_xticks(y_pos)
    ax1.set_xticklabels(objects)
    ax1.set_ylabel("No. of participants")
    ax1.set_title("Occupations of participants")
    # ax1.subplots_adjust(bottom=0.4)


    experiences = {}

    for item in all_res:
        if experiences.get(item["experience"], None):
            experiences[item["experience"]] += 1
        else:
            experiences[item["experience"]] = 1

    experiences = {
        "zero": 23,
        "1 - 10": 37,
        "10-20": 4,
        "20+": 5,
    }


    X_ticks = []
    Y = []

    for exp, count in experiences.items():
        X_ticks.append(exp)
        Y.append(count)

    objects = tuple(X_ticks)
    y_pos = np.arange(len(objects))


    ax2.bar(y_pos, Y, align='center', alpha = 0.5, color='k')
    ax2.set_xticks(y_pos)
    ax2.set_xticklabels(objects)
    ax2.set_ylabel("No. of participants")
    ax2.set_title("No. of proejcts with the library")
    # ax2.subplots_adjust(bottom=0.4)

    plt.tight_layout(pad=0.4,w_pad=0.5,h_pad=8)


    for tick in ax1.get_xticklabels():
        tick.set_rotation(90)

    for tick in ax2.get_xticklabels():
        tick.set_rotation(90)


    plt.subplots_adjust(bottom=0.2)
    fig.savefig('plot.png')


def task_plot():
    fig = plt.figure()

    data = [92, 13, 18, 2]
    # data = [1, 2, 3, 4, 5]
    pos = np.arange(4)
    x_ticks = ["Yes", "No", "I don't know", "Doesn't seem\nlike a task"]
    # y_ticks = [1, 2, 3, 4, 5]

    # plt.violinplot(
    #     # dataset=[data, ],
    #     # positions=pos, 
    #     data, pos,
    #     # points=200, 
    #     vert=True, 
    #     # widths=1.1,
    #     # showmeans=True, 
    #     # showextrema=True,
    #     # showmedians=True,
    #     # bw_method=0.5,
    # )
    plt.bar(pos, data, align='center', alpha = 0.5, color='k')

    # plt.yticks(pos, x_ticks)
    plt.xticks(pos, x_ticks)
    plt.ylabel("Number of reviews")
    plt.title("Is the task description related to the library?")

    fig.savefig('plot.png')

def snippets_plot():
    all_res = all_data()


def test_plot():
    # fake data
    fs = 10  # fontsize
    pos = [1, 2, 4, 5, 7, 8]
    data = [np.random.normal(0, std, size=100) for std in pos]
    pdb.set_trace()

    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(6, 6))

    axes[0, 0].violinplot(data, pos, points=20, widths=0.3,
                          showmeans=True, showextrema=True, showmedians=True)
    axes[0, 0].set_title('Custom violinplot 1', fontsize=fs)

    axes[0, 1].violinplot(data, pos, points=40, widths=0.5,
                          showmeans=True, showextrema=True, showmedians=True,
                          bw_method='silverman')
    axes[0, 1].set_title('Custom violinplot 2', fontsize=fs)

    axes[0, 2].violinplot(data, pos, points=60, widths=0.7, showmeans=True,
                          showextrema=True, showmedians=True, bw_method=0.5)
    axes[0, 2].set_title('Custom violinplot 3', fontsize=fs)

    axes[1, 0].violinplot(data, pos, points=80, vert=False, widths=0.7,
                          showmeans=True, showextrema=True, showmedians=True)
    axes[1, 0].set_title('Custom violinplot 4', fontsize=fs)

    axes[1, 1].violinplot(data, pos, points=100, vert=False, widths=0.9,
                          showmeans=True, showextrema=True, showmedians=True,
                          bw_method='silverman')
    axes[1, 1].set_title('Custom violinplot 5', fontsize=fs)

    axes[1, 2].violinplot(data, pos, points=200, vert=False, widths=1.1,
                          showmeans=True, showextrema=True, showmedians=True,
                          bw_method=0.5)
    axes[1, 2].set_title('Custom violinplot 6', fontsize=fs)

    for ax in axes.flatten():
        ax.set_yticklabels([])

    fig.suptitle("Violin Plotting Examples")
    fig.subplots_adjust(hspace=0.4)


    fig.savefig('plot.png')


PROFESSIONALS = [
    "Industrial Developer",
    "Software Developer",
    "Freelance Developer",
    "Government employee",
    "Sr. QA Automation Engineer",
]

STUDENTS = [
    "Undergraduate Computer Science Student",
    "Graduate Computer Science Student",
    "Graduate Student ECE",
    "Graduate Electrical Engineering Student",
    "graduate Engineering std",
    "Graduate Computer Engineering Student",
    "Graduate ECE  Student",
    "Graduate Physics Student",
]

def correlation():
    all_res = all_data()
    # QUESTIONS = "learning"
    # QUESTIONS = "list_of_tasks"
    # QUESTIONS = "snippets"
    # QUESTIONS = "task"
    QUESTIONS = "snippets"

    ss = []
    ps = []

    for res in all_res:
        if res["profession"] in PROFESSIONALS:
            ps.append(res)
        elif res["profession"] in STUDENTS:
            ss.append(res)

    ps_total = 0
    for item in ps:
        ps_total += int(item["finish"][QUESTIONS])

    ss_total = 0
    for item in ss:
        ss_total += int(item["finish"][QUESTIONS])

    print("Students: {}\nProfessionals:{}".format(ss_total/len(ss), ps_total/len(ps)))


def get_projects():
    fig = plt.figure()
    all_res = all_data()

    projects = {
        "zero": 23, 
        "1 - 10": 37,
        "10-20": 4,
        "20+": 5,
    }

    pos = np.arange(4)
    x_ticks = ["Zero", "1-10", "11-20", "20+"]
    data = [23, 37, 4, 5]

    plt.bar(pos, data, align='center', alpha = 0.5, color='k')

    # plt.yticks(pos, x_ticks)
    plt.xticks(pos, x_ticks)
    plt.ylabel("Number of responses")
    plt.title("Approximately how many projects have you used <library> in before?")

    fig.savefig('background_projects.png')


def get_profession():
    fig = plt.figure()
    all_res = all_data()

    professions = {
        "Undergrad CS Student": 12,
        "Academic Researcher": 2, 
        "Industrial Developer": 16,
        "Graduate CS Student": 25,
        "Industrial Researcher": 0,
        "Freelance Developer": 14
    }

    pos = np.arange(6)
    x_ticks = ["Graduate Student", "Undergrad Student", "Academic Researcher", "Industrial Researcher", "Industrial Developer", "Freelance Developer"]

    data = [12, 25, 2, 0, 16, 14]

    plt.bar(pos, data, align='center', alpha = 0.5, color='k')

    # plt.yticks(pos, x_ticks)
    plt.xticks(pos, x_ticks, rotation=90)
    plt.ylabel("Number of responses")
    plt.title("What is your current occupation?")
    plt.subplots_adjust(bottom=0.4)

    fig.savefig('background_occupation.png')


def get_experience():
    fig = plt.figure()
    all_res = all_data()

    experience = {}

    for item in all_res:
        value = item["proficiency"]
        if experience.get(value, None):
            experience[value] += 1
        else:
            experience[value] = 1

    # pdb.set_trace()

    pos = np.arange(5)
    x_ticks = ["< 1", "1 - 2", "2 - 5", "6 - 10", "11+"]

    data = [3, 15, 29, 7, 15]

    plt.bar(pos, data, align='center', alpha = 0.5, color='k')

    # plt.yticks(pos, x_ticks)
    plt.xticks(pos, x_ticks)
    plt.ylabel("Number of responses")
    plt.title("How many years of Java development experience do you have?")

    fig.savefig('background_experience.png')
    


if __name__=="__main__":
    # main()
    # results()
    # get_comments()
    all_data()
    # library_response_dist()
    # background_distro()
    # task_plot()
    # test_plot()
    # correlation()
    # get_projects()
    # get_profession()
    # get_experience()
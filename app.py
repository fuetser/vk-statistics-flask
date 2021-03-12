from flask import Flask, render_template
import vk_api


app = Flask(__name__)


@app.route("/vk_stat/<int:group_id>")
def vk_stat(group_id):
    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
    vk = vk_session.get_api()
    vk = vk_session.get_api()
    resp = vk.stats.get(group_id=group_id, fields="reach", intervals_count=10)
    likes = 0
    comms = 0
    subs = 0
    ages = {}
    cities = {}
    for record in resp:
        if (act := record.get("activity")):
            likes += act.get("likes", 0)
            comms += act.get("comments", 0)
            subs += act.get("subscribed", 0)
        for age in record["reach"]["age"]:
            ages.setdefault(age["value"], 0)
            ages[age["value"]] += age["count"]
        for city in record["reach"]["cities"]:
            cities.setdefault(city["name"], 0)
            cities[city["name"]] += city["count"]
    return render_template("stats.html", title="Vk Statistics", likes=likes,
                           comms=comms, subs=subs, ages=tuple(ages.items()),
                           cities=tuple(cities.items()))


if __name__ == '__main__':
    app.run(debug=True)

import jinja2

max_score = 100
test_name = "Python Challenge"
students = [
    {"name": "Sandrine",  "score": 100},
    {"name": "Gergeley", "score": 87},
    {"name": "Frieda", "score": 92},
    {"name": "Fritz", "score": 40},
    {"name": "Sirius", "score": 75}
]

environment = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
template = environment.get_template("results.html")

context = {
    "students": students,
    "test_name": test_name,
    "max_score": max_score,
}

results_filename = "students_results.html"

with open(results_filename, mode="w", encoding="utf-8") as results:
    results.write(template.render(context))
    print(f"... wrote {results_filename}")
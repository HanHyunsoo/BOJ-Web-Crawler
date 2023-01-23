from enum import Enum
import os, shutil, requests, copy


solved_api_url = "https://solved.ac/api/v3/problem/lookup?problemIds="
ranks = ["Unrated", "Bronze V", "Bronze IV", "Bronze III", "Bronze II", "Bronze I", "Silver V", "Silver IV", "Silver III", "Silver II", "Silver I", "Gold V", "Gold IV", "Gold III", "Gold II", "Gold I", "Platinum V", "Platinum IV", "Platinum III", "Platinum II", "Platinum I", "Diamond V", "Diamond IV", "Diamond III", "Diamond II", "Diamond I", "Ruby V", "Ruby IV", "Ruby III", "Ruby II", "Ruby I"]
rank_dict = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: [], 13: [], 14: [], 15: [], 16: [], 17: [], 18: [], 19: [], 20: [], 21: [], 22: [], 23: [], 24: [], 25: [], 26: [], 27: [], 28: [], 29: [], 30: []}
rank_svg_url = "https://d2gd6pc034wcta.cloudfront.net/tier/{rank_number}.svg"

headers = {"Content-Type": "application/json"}

boj_url = "https://www.acmicpc.net"
readme_file_name = "README.md"
java_file_name = "Main.java"

java_file_template = """package pro_{number};

public class Main {{
    public static void main(String[] args) {{
        
    }}
}}
"""

problem_readme_template = """# {number} - {name}

* [소스코드]({dir})
* [출처]({url})"""

workbook_readme_template = """# {number} - {name}

## 문제 리스트

{problem_checks}
## Reference
 
[출처]({url})"""

class Language(Enum):
    JAVA = 1
    PYTHON = 2

class Problem:
    def __init__(self, number: int, name: str) -> None:
        self.number = number
        self.name = name
        self.url = f"{boj_url}/problem/{number}"

    def __str__(self) -> str:
        return f"Problem({self.number}, {self.name}, {self.url})"

    def get_problem_readme_template(self, file_dir) -> str:

        return problem_readme_template.format(number=self.number, name=self.name, dir=file_dir, url=self.url)

    def get_java_file_template(self) -> str:
        return java_file_template.format(number=self.number)

class WorkBook:
    def __init__(self, number: int, name: str, language: Language, problems: list[Problem] = []) -> None:
        self.number = number
        self.name = name
        self.language = language
        self.url = f"{boj_url}/workbook/view/{number}"
        self.problems = problems
        self.problems_dir = "result"

        match self.language:
            case Language.JAVA:
                self.problems_dir += "/Java/src"
            case Language.PYTHON:
                self.problems_dir += "/Python"

    def __str__(self) -> str:
        return f"WorkBook({self.number}, {self.name}, {self.language}, {self.url}, {self.problems_dir}, {len(self.problems)})"

    def append_problems(self, problems: list[Problem]) -> None:
        self.problems.extend(problems)

    def make_folders_and_files(self, given_rank: bool = False) -> str:
        workbook_path = f"{self.problems_dir}/wb_{self.number}"

        if (os.path.exists(workbook_path)):
            print("이미 해당 문제집 폴더가 존재합니다. 삭제하고 다시 진행합니다.")
            shutil.rmtree(workbook_path)

        os.makedirs(workbook_path)

        if given_rank:
            self.set_rank_dict_by_problems();
            problem_checks = self.make_rank_template()
        else:
            problem_checks = "";

        for problem in self.problems:
            # problem_dir = self.problems_dir + "/" + "pro_{number}".format(number=problem.number)
            problem_dir = f"{workbook_path}/pro_{problem.number}"
            if not given_rank:
                problem_checks += f"* [ ] [{problem.number} - {problem.name}](pro_{problem.number})\n"

            os.makedirs(problem_dir)
            problem_readme = open(f"{problem_dir}/{readme_file_name}", "w")
            match self.language:
                case Language.JAVA:
                    java_file = open(f"{problem_dir}/{java_file_name}", "w")
                    java_file.write(problem.get_java_file_template())
                    java_file.close()
                    problem_readme.write(problem.get_problem_readme_template(java_file_name))
                case Language.PYTHON:
                    python_file = open(f"{problem_dir}/{problem.number}.py", "w")
                    python_file.close()
                    problem_readme.write(problem.get_problem_readme_template(f"{problem.number}.py"))
            problem_readme.close()


        workbook_readme = open(f"{workbook_path}/{readme_file_name}", "w")
        workbook_readme.write(self.get_workbook_readme_template(problem_checks))
        workbook_readme.close()

        return workbook_path

    def set_rank_dict_by_problems(self) -> None:
        self.problems.sort(key=lambda x: x.number)
        problems_map: dict[int, Problem] = {}

        for problem in self.problems:
            problems_map[problem.number] = problem

        ids = list(map(lambda x: str(x.number), self.problems))

        request_url = solved_api_url + ",".join(ids)

        responses = requests.get(request_url, headers=headers)
        
        for response in responses.json():
            problem = problems_map[response["problemId"]]
            problem_rank = response["level"]

            rank_dict[problem_rank].append(problem)

    def make_rank_template(self) -> str:
        result = ""

        for rank_number, problems in rank_dict.items():
            if len(problems) == 0:
                continue

            result += f"### <img src=\"https://d2gd6pc034wcta.cloudfront.net/tier/{rank_number}.svg\" width=\"15\" height=\"15\"/>  {ranks[rank_number]}\n\n"

            result += "\n".join([f"* [ ] [{problem.number} - {problem.name}](pro_{problem.number})" for problem in problems]) + "\n\n"

        return result

    def get_workbook_readme_template(self, problem_checks: str) -> str:

        return workbook_readme_template.format(number=self.number, name=self.name, problem_checks=problem_checks, url=self.url)

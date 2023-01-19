from enum import Enum
import os, shutil

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
* [출처]({url})"""

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
        return f"WorkBook({self.number}, {self.name}, {self.language}, {self.url}, {self.problems_dir}, {self.p_count})"

    def append_problems(self, problems: list[Problem]) -> None:
        self.problems.extend(problems)

    def make_folders_and_files(self) -> str:
        workbook_path = f"{self.problems_dir}/wb_{self.number}"

        if (os.path.exists(workbook_path)):
            print("이미 해당 문제집 폴더가 존재합니다. 삭제하고 다시 진행합니다.")
            shutil.rmtree(workbook_path)

        os.makedirs(workbook_path)

        problem_checks = "";

        for problem in self.problems:
            # problem_dir = self.problems_dir + "/" + "pro_{number}".format(number=problem.number)
            problem_dir = f"{workbook_path}/pro_{problem.number}"
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

    def get_workbook_readme_template(self, problem_checks: str) -> str:

        return workbook_readme_template.format(number=self.number, name=self.name, problem_checks=problem_checks, url=self.url)
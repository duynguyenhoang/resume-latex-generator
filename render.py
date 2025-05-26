import json
from pathlib import Path
import sys
from typing import Any
from jinja2 import Environment, FileSystemLoader, Template
import yaml
from jsonschema import validate


TEMPLATE = "template.jinja"
TEMPLATE_BASE_DIR = "templates"
RESUME_BODY = "resources/resume-example.yaml"
JSON_SCHEMA = "resources/schema.json"
OUTPUT_PATH = "output/resume.tex"

TEMPLATE_OPT = {
    "variable_start_string": "$jinja2{",
    "variable_end_string": "}",
    "trim_blocks": True,
    "lstrip_blocks": True,
}


class LatexResumeGen:
    def __init__(
        self,
        resume: str = None,
        template_dir: str = None,
        template_path: str = None,
        out: str = None,
    ) -> None:
        self.resume_body = resume or RESUME_BODY
        self.template = template_path or TEMPLATE
        self.template_dir = template_dir or TEMPLATE_BASE_DIR
        self.output = out or OUTPUT_PATH

    def validate_json_schema(self) -> None:
        read_schema = self.read_file(JSON_SCHEMA)
        resume_instance = self.read_file(self.resume_body)
        validate(instance=resume_instance, schema=read_schema)

    def validate_file(self) -> Any:
        """
        Validate the existence and type of the file.

        Raises:
            FileNotFoundError: If the file does not exist.
            TypeError: If the file type is not supported.

        Returns:
            None
        """
        if not Path(self.resume_body).exists():
            raise FileNotFoundError(f"File {self.resume_body} does not exist.")
        file_ext = Path(self.resume_body).suffix
        if file_ext not in (".json", ".yaml", ".yml"):
            raise TypeError(f"File type '{file_ext}' is not currently supported.")

    @staticmethod
    def read_file(file_path) -> Any:
        try:
            with open(file_path, encoding="utf-8") as f:
                return (
                    json.load(f)
                    if Path(file_path).suffix == ".json"
                    else yaml.safe_load(f)
                )
        except ValueError:
            sys.exit("Input file is not a valid JSON/YAML.")

    def build_template(self) -> Template:
        env = Environment(
            loader=FileSystemLoader(Path(self.template_dir).resolve()), **TEMPLATE_OPT
        )
        return env.get_template(self.template)

    def render(self) -> None:
        self.validate_file()
        self.validate_json_schema()
        context = self.read_file(self.resume_body)
        content = self.build_template().render(context)
        with open(self.output, "w") as f:
            f.write(content)


if __name__ == "__main__":
    first_argv = sys.argv[1] if len(sys.argv) > 1 else RESUME_BODY
    if first_argv == "--help":
        print(
            "Usage: python render.py [resume_body_path]\n"
            "Default resume body path is 'resources/resume-example.yaml'.\n"
            "The output will be saved to 'output/resume.tex'.\n"
        )
        sys.exit(0)

    resume_body_path = sys.argv[1] if len(sys.argv) > 1 else RESUME_BODY
    print(f"start rendering resume from {resume_body_path}....")
    LatexResumeGen(resume=resume_body_path).render()
    print("complete....")

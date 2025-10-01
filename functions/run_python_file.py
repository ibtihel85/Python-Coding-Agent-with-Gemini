import os
import subprocess
from google.genai import types
def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory,file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
    if not os.path.isfile(abs_file_path):
        return(f'Error: File "{file_path}" not found.')
    if not file_path.endswith(".py"):
        return(f'Error: "{file_path}" is not a Python file.')
    try:
        final_args=["python", file_path]
        final_args.extend(args)
        output = subprocess.run(
            final_args,
            cwd=abs_working_dir,
            timeout=30,
            capture_output=True)
        final_string = f"""
STDOUT: {output.stdout}
STDERR: {output.stderr}
"""
        if output.stdout == "" and output.stderr == "":
            final_string = "No output produced."
        if output.returncode != 0:
            final_string += f'Process exited with code {output.returncode}'
        return final_string
    except Exception as e:
        return f'Error: executing Python file: {e}'
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file inside the working directory and returns its output (stdout and stderr).",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of arguments to pass to the Python script.",
            ),
        },
    ),
)                                                     
# python_executor.py
# This file is used to run the python files and save the output to the fix_log.json file
# Cursor's agent makes use of the fix_log.json file to understand the changes in the code and the tests

import subprocess
import json
import re
import sys

# A CLASS TO RUN THE PYTHON FILES AND GET THE OUTPUT
class PythonExecutor:
    def __init__(self, python_file, test_file):
        self.python_file = python_file
        self.test_file = test_file

    def run_python_files(self):
        python_output = self.run_file(self.python_file, "Python")
        test_output = self.run_file(self.test_file, "Test", is_test=True)
        return python_output, test_output

    def run_file(self, file, file_type, is_test=False):
        command = [sys.executable, file] if not is_test else [sys.executable, "-m", "pytest", file]
        try:
            output = subprocess.run(command, capture_output=True, text=True, check=True)
            print(f"{file_type} file executed successfully.")
            print(f"STDOUT:\n{output.stdout}")
            return output
        except subprocess.CalledProcessError as e:
            print(f"Error executing {file_type} file:")
            print(f"Command: {' '.join(e.cmd)}")
            print(f"Return code: {e.returncode}")
            print(f"STDOUT:\n{e.stdout}")
            print(f"STDERR:\n{e.stderr}")
            return e

# A CLASS TO PARSE THE OUTPUT AND SAVE IT TO THE FIX_LOG.JSON FILE
class FixLog:
    def __init__(self, fix_log_file):
        self.fix_log_file = fix_log_file

    def parse_output(self, python_output, test_output):
        parsed_python_output = self.parse_python_output(python_output)
        parsed_test_output = self.parse_test_output(test_output)
        self.save_to_fix_log(parsed_test_output, parsed_python_output)

    def parse_python_output(self, python_output):
        parsed_output = {
            "execution_time_change": None,
            "memory_usage_change": None,
            "error": None,
            "stdout": None,
            "stderr": None
        }

        if isinstance(python_output, subprocess.CalledProcessError):
            parsed_output["error"] = f"Return code: {python_output.returncode}"
            parsed_output["stdout"] = python_output.stdout
            parsed_output["stderr"] = python_output.stderr
        elif python_output:
            parsed_output["stdout"] = python_output.stdout
            parsed_output["stderr"] = python_output.stderr
            # Regular expressions for parsing
            time_pattern = r'Execution time: (\d+\.?\d*) seconds'
            memory_pattern = r'Memory usage: (\d+\.?\d*) MB'

            # Parse the python output
            time_match = re.search(time_pattern, python_output.stdout)
            if time_match:
                parsed_output["execution_time_change"] = f"{float(time_match.group(1)):.2f}s"

            memory_match = re.search(memory_pattern, python_output.stdout)
            if memory_match:
                parsed_output["memory_usage_change"] = f"{float(memory_match.group(1)):.2f}MB"

        return parsed_output

    def parse_test_output(self, test_output):
        parsed_output = {
            "pre_fix_status": "failed",  # Default to failed, will update if tests pass
            "related_tests": [],
            "auto_generated_tests": [],
            "failure_messages": [],
            "error": None,
            "stdout": None,
            "stderr": None
        }

        if isinstance(test_output, subprocess.CalledProcessError):
            parsed_output["error"] = f"Return code: {test_output.returncode}"
            parsed_output["stdout"] = test_output.stdout
            parsed_output["stderr"] = test_output.stderr
        elif test_output:
            parsed_output["stdout"] = test_output.stdout
            parsed_output["stderr"] = test_output.stderr
            # Regular expressions for parsing
            test_result_pattern = r'(PASSED|FAILED|ERROR|SKIPPED)'
            test_name_pattern = r'test_[\w_]+'
            
            # Parse the test output
            for line in test_output.stdout.split('\n'):
                # Check for overall test status
                if "failed" not in line.lower() and "error" not in line.lower():
                    parsed_output["pre_fix_status"] = "passed"
                
                # Extract test names
                test_names = re.findall(test_name_pattern, line)
                parsed_output["related_tests"].extend(test_names)
                
                # Check for auto-generated tests (assuming they have a specific prefix)
                auto_generated = [test for test in test_names if test.startswith("test_auto_")]
                parsed_output["auto_generated_tests"].extend(auto_generated)
                
                # Extract failure messages
                if "FAILED" in line or "ERROR" in line:
                    failure_message = line.split(": ")[-1].strip()
                    parsed_output["failure_messages"].append(failure_message)

            # Remove duplicates
            parsed_output["related_tests"] = list(set(parsed_output["related_tests"]))
            parsed_output["auto_generated_tests"] = list(set(parsed_output["auto_generated_tests"]))

        return parsed_output

    def save_to_fix_log(self, parsed_test_output, parsed_python_output):
        try:
            # Try to open the file in read mode first
            try:
                with open(self.fix_log_file, 'r') as f:
                    fix_log = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                # If the file doesn't exist or is empty, initialize with default structure
                fix_log = {"current_phase": 1, "history": [], "todo": [], "test_coverage_report": "", "performance_summary": {}}

            new_entry = {
                "UID": f"fix_{len(fix_log['history']) + 1:03d}",
                # Extract dynamic values from parsed output or other sources
                "file_name": "",  
                "line": 0,  
                "operation": "",  
                "content": "",  
                "explanation": "",  
                "priority": "",  
                "dependencies": [],
                "tests": parsed_test_output,
                "performance_impact": parsed_python_output,
                "rollback_info": {"previous_content": "", "rollback_script": ""}
            }

            fix_log["history"].append(new_entry)
            fix_log["performance_summary"] = parsed_python_output

            # Write the updated content back to the file
            with open(self.fix_log_file, 'w') as f:
                json.dump(fix_log, f, indent=4)

        except Exception as e:
            print(f"Error saving to fix_log.json: {e}")

# main function to run the python files and save the output to the fix_log.json file
def main():
    python_executor = PythonExecutor("malo.py", "test_malo.py")
    python_output, test_output = python_executor.run_python_files()
    
    fix_log = FixLog("fix_log.json")
    fix_log.parse_output(python_output, test_output)

# call the main function
if __name__ == "__main__":
    main()
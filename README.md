# **Automated Code Fixing System**

This project is a powerful automated code fixing system designed to enhance your development workflow by seamlessly integrating with Cursor, an AI-powered coding assistant. With this system, you can streamline the process of diagnosing, testing, and fixing code, ensuring higher code quality and faster turnaround times.

## **Key Components**

### 1. **new_cursor_rules**

The `new_cursor_rules` file serves as the rulebook for the AI agent (Cursor). It defines:

- **Core Principles:** Guiding the AI agent to maintain brevity, simplicity, and automation.
- **Streamlined Workflow:** A step-by-step process for assessing, fixing, and testing code.
- **Fix Suggestion Format:** A standardized JSON format for suggesting code fixes.
- **Workflow Management:** Ensuring consistent, effective, and organized code fixing.

These rules empower Cursor to follow a structured and efficient approach to automated code fixes.

### 2. **python_executor.py**

The `python_executor.py` script is the backbone of the system, responsible for:

- **Execution:** Running the Python code and associated test files.
- **Data Capture:** Collecting outputs, including errors, stdout, and stderr.
- **Output Parsing:** Extracting key information like test results and performance metrics.
- **Log Updates:** Updating the `fix_log.json` file with the latest data.

This script automates the crucial steps of running and evaluating code, providing the AI agent with the data it needs to make informed decisions.

### 3. **fix_log.json**

The `fix_log.json` file is the heart of the system’s memory, maintaining:

- **Fix History:** A detailed record of all applied fixes.
- **Current Code State:** Tracking the state of code and tests.
- **Performance Metrics:** Recording test results and code performance.
- **Task Management:** Listing pending tasks and setting priorities.

This file ensures continuity and data-driven decision-making throughout the code fixing process.

## **How It Works (AIM)**

1. **Rule Adherence:** The AI agent (Cursor) reads the `new_cursor_rules` to understand the code fixing strategy.
2. **Execution:** Upon a suggested or applied fix, `python_executor.py` runs the relevant code and tests.
3. **Logging:** The script updates `fix_log.json` with the results and metrics.
4. **Analysis:** The AI agent reviews the updated log to determine further actions or verify the effectiveness of fixes.
5. **Iteration:** The process repeats until the code is fully optimized or no further improvements are necessary.

This cohesive system creates a feedback loop that allows for continuous, data-driven code enhancements, making your development process more efficient and reliable.

## **Current Status**

The project is currently in its initial development phase, offering the following workflow:

1. **Test Generation:** A human user instructs the AI agent to generate test cases.
2. **Log Creation:** The user runs `python_executor.py code_to_fix.py test_code_to_fix.py`, which initializes the `fix_log.json` file.
3. **Logging:** Instead running the code_to_fix.py file, the user runs `python_executor.py' so an error message from the pair of code_to_fix.py and test_code_to_fix.py is shown. This error message is shared with cursor's chat.
4. **Debugging:** Cursor's chat suggests a fix for the error message. The user applies it (hopefully with cursor's composer). Then the user runs `python_executor.py` again.
5. **Iteration:** The process repeats until the code is fully optimized or no further improvements are necessary.
6. **Workflow Integration:** With the setup complete, a test-driven development workflow using Cursor becomes possible.

While this foundation requires some manual setup, future updates will focus on fully automating the initialization process, further streamlining the entire workflow.

## **Get Involved**

We invite developers, AI enthusiasts, and open-source contributors to join us in refining and expanding this project. Your feedback, contributions, and ideas are invaluable in driving this project forward. Whether it’s improving existing features, adding new capabilities, or simply using the system and sharing your experience, your involvement helps shape the future of automated code fixing.

Together, we can make automated code fixing smarter, faster, and more accessible to developers.

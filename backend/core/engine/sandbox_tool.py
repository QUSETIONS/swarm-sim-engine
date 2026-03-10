from core.engine.sandbox_executor import DockerSandbox

class SandboxTool:
    _executor = DockerSandbox()

    @staticmethod
    def execute(tool_name: str, params: dict) -> str:
        """
        Executes a real Python script inside the isolated Docker sandbox.
        """
        if tool_name == "execute_python":
            script = params.get("script", "print('No script provided')")
            result = SandboxTool._executor.execute_script(script)
            
            if result.get("success"):
                return f"[Docker Execution SUCCESS]\nSTDOUT:\n{result.get('stdout')}"
            else:
                return f"[Docker Execution FAILED]\nExit Code: {result.get('exit_code')}\nSTDERR:\n{result.get('stderr')}\nSTDOUT:\n{result.get('stdout')}"
            
        return f"[Sandbox Execution] Error: Tool {tool_name} not found."

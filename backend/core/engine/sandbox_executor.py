import docker
import os
import tempfile
import uuid
import logging

logger = logging.getLogger(__name__)

class DockerSandbox:
    def __init__(self):
        try:
            self.client = docker.from_env()
            logger.info("Docker client initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Docker environment: {e}")
            self.client = None

    def execute_script(self, script_code: str, image: str = "python:3.9-alpine", timeout: int = 10) -> dict:
        """
        Executes arbitrary python code inside an ephemeral docker container.
        Returns the execution result, standard output, and standard error.
        """
        if not self.client:
            return {"success": False, "stdout": "", "stderr": "Docker client is not available on host. Fallback required.", "exit_code": -1}

        # Ensure the image is available or pull it (might be slow the very first time)
        try:
            self.client.images.get(image)
        except docker.errors.ImageNotFound:
            logger.info(f"Pulling sandbox image {image}...")
            self.client.images.pull(image)

        sandbox_id = str(uuid.uuid4())
        
        # We mount a temporary directory to pass the script
        with tempfile.TemporaryDirectory() as temp_dir:
            script_path = os.path.join(temp_dir, f"sandbox_{sandbox_id}.py")
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(script_code)
                
            container = None
            try:
                # Run the container isolated
                # Network disabled for pure sandbox, CPU/Mem limited
                container = self.client.containers.run(
                    image,
                    command=f"python /sandbox/sandbox_{sandbox_id}.py",
                    volumes={temp_dir: {'bind': '/sandbox', 'mode': 'ro'}},
                    working_dir="/sandbox",
                    network_disabled=True,
                    mem_limit="128m",
                    cpu_period=100000,
                    cpu_quota=50000, # 0.5 CPU
                    detach=True
                )
                
                # Wait for execution to finish within timeout
                result = container.wait(timeout=timeout)
                
                stdout = container.logs(stdout=True, stderr=False).decode("utf-8")
                stderr = container.logs(stdout=False, stderr=True).decode("utf-8")
                exit_code = result.get("StatusCode", -1)
                
                return {
                    "success": exit_code == 0,
                    "stdout": stdout,
                    "stderr": stderr,
                    "exit_code": exit_code
                }
                
            except docker.errors.ContainerError as e:
                return {"success": False, "stdout": "", "stderr": str(e), "exit_code": 1}
            except Exception as e:
                # E.g. RequestsTimeout if the script hangs natively
                return {"success": False, "stdout": "", "stderr": f"Execution Timed Out or Error: {str(e)}", "exit_code": -2}
            finally:
                if container:
                    try:
                        container.stop(timeout=1)
                        container.remove(force=True)
                    except:
                        pass

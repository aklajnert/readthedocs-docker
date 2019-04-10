import os
import re
import shutil
import subprocess
import tempfile
import time


class Compose:
    """Run docker compose in temp directory.f"""

    credentials_regex = re.compile(r'username: "(.*)" and password: "(.*)"\.')

    def __init__(self, directory):
        self._directory = directory
        shutil.copy(
            os.path.join(os.path.dirname(__file__), "docker-compose.yml"),
            os.path.join(directory, "docker-compose.yml"),
        )
        self.username = None
        self.password = None

    def __enter__(self):
        subprocess.call(["docker-compose", "up", "-d"], cwd=self._directory)
        n = 0
        while n < 60:
            logs = self.get_logs()
            if "spawned uWSGI worker" in logs:
                break

            if not self.username:
                match = self.credentials_regex.search(logs)
                if match:
                    self.username = match.group(1)
                    self.password = match.group(2)

            time.sleep(1)
            n += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        subprocess.call(["docker-compose", "down"], cwd=self._directory)

    def get_logs(self, app="web"):
        """Read application logs."""
        return subprocess.check_output(
            ["docker-compose", "logs", app], cwd=self._directory
        ).decode()


def run_app():
    """Run application via compose and check if everything looks fine."""
    with tempfile.TemporaryDirectory() as tempdir:
        compose = Compose(tempdir)
        with compose:
            print(
                "Web service is running. Log in with username:",
                compose.username,
                "and password:",
                compose.password,
            )
            input("Press any key to exit...")


if __name__ == "__main__":
    run_app()

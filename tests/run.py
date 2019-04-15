import errno
import re
import socket
import subprocess
import tempfile
import time
from pathlib import Path

import yaml


def get_open_port():
    """Scan for open port to run container."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_:
        for port in range(9000, 10000):
            try:
                socket_.bind(("127.0.0.1", port))
            except socket.error as exc:
                if exc.errno == errno.EADDRINUSE:
                    continue
                raise exc
            return port
        raise Exception("Cannot find open port.")


class TempDir(tempfile.TemporaryDirectory):
    """Override __exit__ to not raise exception."""

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            super().__exit__(exc_type, exc_val, exc_tb)
        except PermissionError:
            print("Failed to cleanup directory ({}). Try running as a root.".format(self.name))


class Compose:
    """Run docker compose in temp directory.f"""

    credentials_regex = re.compile(r'username: "(.*)" and password: "(.*)"\.')

    def __init__(self, directory):
        self._directory = Path(directory)
        self.open_port = get_open_port()
        root_dir = Path(__file__).parents[1]
        with open(root_dir / "docker-compose.yml") as compose_fh:
            compose = yaml.safe_load(compose_fh)

        compose["services"]["web"]["ports"][0] = ":".join([str(self.open_port), "8000"])
        compose["services"]["web"]["environment"].append("RTD_DOMAIN=localhost:{}".format(self.open_port))

        image_name = compose["services"]["web"]["image"]
        images = subprocess.check_output(("docker", "images", image_name)).decode()
        if len(images.splitlines()) == 1:
            print("Docker image {} not found. Building...".format(image_name))
            subprocess.call(("docker", "build", "-t", image_name, "."), cwd=str(root_dir))

        with open(self._directory / "docker-compose.yml", "w") as target_compose_fh:
            yaml.dump(compose, target_compose_fh)
        self.username = None
        self.password = None

    def __enter__(self):
        subprocess.call(["docker-compose", "up", "-d"], cwd=self._directory)

        n = 0
        while n < 60:
            logs = self.get_logs()
            if "spawned uWSGI worker" in logs:
                match = self.credentials_regex.search(logs)
                if match:
                    self.username = match.group(1)
                    self.password = match.group(2)
                else:
                    raise Exception("Cannot determine username or password.")
                break

            time.sleep(1)
            n += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        subprocess.call(["docker-compose", "down"], cwd=str(self._directory))

    def get_logs(self, app="web"):
        """Read application logs."""
        return subprocess.check_output(["docker-compose", "logs", app], cwd=str(self._directory)).decode()


def run_app(wait_for_input=True):
    """Run application via compose and check if everything looks fine."""
    with TempDir() as tempdir:
        compose = Compose(tempdir)
        with compose:
            if wait_for_input:
                print(
                    "Web service is running on port: {}. Log in with username:".format(compose.open_port),
                    compose.username,
                    "and password:",
                    compose.password,
                )
                input("Press any key to exit...")
            else:
                yield compose


if __name__ == "__main__":
    next(run_app(), None)

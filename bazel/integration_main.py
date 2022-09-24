import json
import os
import subprocess

import pytest
import sys
# gazelle:ignore rules_python.python.runfiles
from rules_python.python.runfiles import runfiles

from tavern.internal.testutil import enable_default_tavern_extensions
from tavern.testutils import pytesthook

if __name__ == "__main__":
    enable_default_tavern_extensions()

    runfiles = runfiles.Create()

    test_file_location_ = os.environ["TAVERN_TEST_FILE_LOCATION"]
    os_path_dirname = os.path.dirname(test_file_location_)

    sys.path.append(os_path_dirname)
    images__split_ = [i for i in json.loads(os.environ["TAVERN_DOCKER_IMAGES"])]

    subprocess.run(
        [
            os.environ["DOCKER_COMPOSE_BINARY"],
            "-f",
            os.environ["TAVERN_DOCKER_COMPOSE"],
            "up",
            "-d",
        ]
        + images__split_,
        timeout=3,
    )

    try:
        raise SystemExit(
            pytest.main([test_file_location_] + sys.argv[2:],
                        plugins=[pytesthook])
        )
    finally:
        # Keep them alive
        # subprocess.run([os.environ["DOCKER_COMPOSE_BINARY"], "-f", os.environ["TAVERN_DOCKER_COMPOSE"], "up", "-d",], timeout=3,)
        pass
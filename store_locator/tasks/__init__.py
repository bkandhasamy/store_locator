from invoke import Collection
from .tasks import start, test, lint, docker_up, docker_down, clean, benchmark

ns = Collection()
ns.add_task(start)
ns.add_task(test)
ns.add_task(lint)
ns.add_task(docker_up)
ns.add_task(docker_down)
ns.add_task(clean)
ns.add_task(benchmark)

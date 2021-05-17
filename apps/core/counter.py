from dataclasses import dataclass

tasks = 0

# async def add_tasks_completed(event):
#     tasks+=1
#     await event.waite()


@dataclass
class CompletedTasks:
    total_tasks: int

    async def get_tasks(self):
        print(self.total_tasks)
        return self.total_tasks

    async def add_tasks_completed(self):
        self.total_tasks += 1


tasks_instance = CompletedTasks(0)
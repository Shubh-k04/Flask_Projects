# Importing all the required modules
import os

# Main task list class
class Task_List:
    def __init__(self):
        self.file_location = os.getcwd() + "/utils/task.txt"

    def add_task(self, taskname: str) -> None:
        """Adds a new Task to the Task List

        Args:
            taskname (str): The name of the task.

        Raises:
            RuntimeError: It the Item is already available in the List
        """

        # Read all the current tasks
        readings = self.read_file()

        # Check if the task exists
        if self.is_in_list(readings, taskname):
            raise RuntimeError("Task Already Available in The List")

        # Append the new task
        readings.append(taskname)

        # Write the updated list
        with open(self.file_location, "w") as file:
            file.write(",".join(readings))

    def read_file(self) -> list:
        """Reads the Task List file.

        Returns:
            list: All the tasks in the Task List
        """
        # Open the task list file
        with open(self.file_location, "r") as file:

            # Split the file by ','
            return file.read().split(",")

    def is_in_list(self, search_list: list, item: str) -> bool:
        """Checks if a item is available in the list by removing spaces and converting to lower case

        Args:
            search_list (list): The list of items
            item (str): The search word

        Returns:
            bool: Whether the item is available or not
        """
        # Iterate through the list
        for i in search_list:
            # Check if both are equal by converting them to lowercase
            if i.lower() == item.lower():
                return True

        return False

    def get_task(self) -> list:
        """Returns a list of all the tasks in the Task List

        Returns:
            list: List of tasks
        """
        return self.read_file()[2:]

    def remove_task(self, task_name: str):
        """Removes a Task from the Task List

        Args:
            task_name (str): The Task That Needs To Be Removed
        """
        # Read all the tasks.
        tasks = self.read_file()

        # Remove the task
        tasks.remove(task_name)

        # Write the updated tasks
        with open(self.file_location, "w") as file:
            file.write(",".join(tasks))
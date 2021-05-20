# Importing All The Required Modules
import json
import os
from typing import Any

# Main Class Market
class Market:
    def __init__(self) -> None:
        self.name = None
        self.logged = False
        self.user_file_location = os.getcwd() + "/utils/user_info.txt"
        self.users = {}
        self.item_location = os.getcwd() + "/utils/items.txt"
        self.is_sell = False
        self.new_item = []
        self.excludes = []
        self.user_info_file = os.getcwd() + "/utils/user_info.txt"
        self.items = {}

    # Creates A New User
    def init_new(self, username: str, password: str) -> bool:
        """Creates A New User For The Market

        Args:
            username (str): User's Username
            password (str): User's Password

        Returns:
            bool: Whether Adding The User Was Successful
        """

        # Set All The Users In A Dictionary
        self.set_users()

        # Check If Other User With The Same Name Available
        if username in self.users:
            return False

        # Make A Basic User Information Dictionary
        self.details = {username: [username, 0, 0, 18000, password]}

        # Read And Remove All The Contents Of The User File
        readings = self.read_file(self.user_file_location)

        # Create A New File
        with open(self.user_file_location, "w") as file:

            # Update The User Info Dictionary With New User
            readings.update(self.details)

            # Write To The File By Converting It To String
            file.write(json.dumps(readings))

        # Adding Of The User Was Successful
        return True

    def read_file(self, location: str, datatype=dict) -> Any:
        """Reads A File
        \n\n
        Args:
            location (str): Location Of The File
            datatype (Any): Returns Data According To The Given dataType. Defaults to dict.
        \n\n
        Returns:
            [Any]: Returns The Response According To The Given datatype
        """
        # Open The File
        with open(location) as file:

            # Read The File And Convert To User's Desired Datatype
            res = datatype(json.loads(file.read()))

        # Return The Response
        return res

    def set_users(self) -> None:
        """Reads All The User's Registered And Sets Them In One Dictionary

        Returns:
            [None]: Just Changes The Global User's Variable [Market.users]
        """

        # Open The Main Folder
        with open(self.user_file_location, "r") as file:

            # Parse The File Contents
            self.users = dict(json.loads(file.read()))

        return None

    def sign_in(self, username: str, password: str) -> bool:
        """Returns If the Password Is Equal To The Registration Password

        Args:
            username (str): User's Username
            password (str): Password That Was Tried For Logging In

        Returns:
            bool: Whether Both The Passwords Are Same
        """

        # Refresh The User's Dictionary
        self.set_users()

        # Check If There Is Any User And The User Is In The List
        if self.users == {} or username not in self.users:
            return False

        # Returning Bool Value
        return self.users[username][-1] == password

    def get_info(self, username: str, need=False, need_password=False) -> Any:
        """Returns All The Information About the User Available

        Args:
            username (str): User's Username
            need (bool, optional): Do You Need Only The Values? Defaults to False.
            need_password (bool, optional): Do You Need Only The Password? Defaults to False.

        Returns:
            Any: Response According To User's Choice
        """

        # Refresh All The User's Dictionary
        self.set_users()

        # Check If The User Exists
        if username not in self.users.keys():
            return None

        # Create A Empty Dictionary To Store Values
        self.info = {}

        # Zip All The Information in A Key , Value Pair
        for i, j in zip(
            ["Username", "Items Sold", "Items Bought", "Coins"],
            list(self.users[username])[:-1],
        ):
            self.info[i] = j

        # Check If User Needs Only The Values
        if need:
            return list(self.info.values())

        # Check If The User Only Need The Password
        if need_password:
            return self.users[username][-1]

        # Return The Dictionary
        return self.info

    def validate(self, password: str, conf_password: str) -> bool:
        """Checks If The Password Is Valid And Same As Confirmation Password

        Args:
            password (str): User's Password
            conf_password (str): User's Confirmation Password

        Returns:
            bool: If Both The Passwords Are Valid
        """

        return not (
            password != conf_password
            or password == conf_password == ""
            or password.count(" ") == len(password)
            or conf_password.count(" ") == len(conf_password)
        )

    def add_new(self, items: dict):
        """Adds A New Item To The Market

        Args:
            items (dict): Description Of The Item
        """

        # Read All The Existing Items
        readings = self.read_file(self.item_location)

        # Update The Items With A New Item
        readings.update(items)

        # Write To The File By Converting Into Str (By json.dumps())
        with open(self.item_location, "w") as file:
            file.write(json.dumps(readings))

    def get_items(self) -> dict:
        """Returns All The Available Products In The Market

        Returns:
            dict: Items As A Dictionary
        """

        # Open The File And Convert To Dict (By json.loads())
        with open(self.item_location, "r") as file:

            # Save It In A Dictionary
            self.items = dict(json.loads(file.read()))

        # Return The Dictionary
        return self.items

    def is_avail(self, item_name):
        """Returns If The Item Exists In The Market (Not Case Sensitive)

        Args:
            item_name (str): Item Name That Needs To Be Checked

        Returns:
            bool: Whether The Item Exists
        """

        # Iterate Through All The Items
        for i in self.get_items().keys():

            # Replace The Spaces And Upper Case Letters
            i = i.lower().replace(" ", "")

            # Same For This
            item_name = item_name.lower().replace(" ", "")

            # Check if Both Are Same
            if item_name == i:
                return True

        return False

    def set_new(self, username: str, coins: int) -> bool:
        """Sets A New Value For The User's Coin Count

        Args:
            username (str): The User Whose Coins Needs To Be Changed
            coins (int): New Coin Value

        Returns:
            bool: Whether Changing Was Successful Or Not
        """

        # Read The Users
        readings = self.read_file(self.user_info_file)

        # Check If User Not In User List
        if username not in readings:
            return False

        # Change Th Coin Value
        readings[username][-2] = coins

        # Write The New Data To The File
        with open(self.user_info_file, "w") as file:
            file.write(json.dumps(readings))

        # Return True
        return True

    def set_item_status(self) -> None:
        """Redefines The Global Variable [Market.excludes] With The All User's Items in the Bag"""

        self.excludes = self.read_file(os.getcwd() + "/utils/item_status.txt")

    def add_excludes(self, exclude: str) -> None:
        """Adds A New Item To User's Bag

        Args:
            exclude (str): [description]
        """

        # Read The Current Users Bag
        readings = self.read_file(os.getcwd() + "/utils/item_status.txt")

        # Check If The Current User's Log Is Stored
        if self.name in readings:
            readings[self.name].append(exclude)
        else:
            readings[self.name] = [exclude]

        # Write The New Information
        with open(os.getcwd() + "/utils/item_status.txt", "w") as file:
            file.write(json.dumps(readings))

    def get_bag(self) -> dict:
        """Returns A Dict With All The Contents Of The File

        Returns:
            dict: The Bag
        """

        # Read The TXT File Where The User's Bag Is Available
        with open(os.getcwd() + "/utils/item_status.txt") as file:
            return json.loads(file.read())

    def remove_from_bag(self, item: str) -> bool:
        """Removes An Item From The Bag

        Args:
            item (str): Item Name That Needs To be Removed

        Returns:
            bool: Whether The Removing Of The Item Was Successful
        """

        # Read All The Contents Of The File
        readings = self.read_file(os.getcwd() + "/utils/item_status.txt")

        # Remove The Item
        readings[self.name].remove(item)

        # Write The New Information To The File
        with open(os.getcwd() + "/utils/item_status.txt", "w") as file:
            file.write(json.dumps(readings))

    def make_dict(self, items) -> dict:
        """Creates A Dictionary Of the Items According To Their Frequency. Just A Mini Version Of collections.Counter.

        Args:
            items (list): Array That Needs To Be Converted To Dict

        Returns:
            dict: The Dictionary Based On The Frequency Of Every Element
        """

        # Create An Empty Dictionary
        ans = {}

        # Iterate Through All The Unique Elements
        for i in set(items):

            # Set The Item According To Its Count
            ans[i] = items.count(i)

        # Return The Dictionary
        return ans

    def get_users_products(self) -> dict:
        """Returns A Dictionary Of All The Items That Was Sold By The Current Admin [Market.name]

        Returns:
            dict: The Items Along With Their Information
        """
        # Create An Empty Dictionary
        user_items = {}

        # Iterate Through All The Items
        for i, j in self.get_items().items():

            # Check If The Item Was Uploaded By The Current Admin
            if j[0] == self.name:

                # Add To The Dictionary
                user_items[i] = j

        # Return The Dictionary
        return user_items

    def get_timeline(self, username: str) -> list:
        """Returns A List Of All The Recent Activites That Was Made By The Passed User

        Args:
            username (str): The User whose recent activites are required

        Returns:
            list: The user's recent activites.
        """
        # Get The Contents Of The File
        timeline = self.read_file(os.getcwd() + "/utils/timeline.txt")

        # Check if The User Is In The TimeLine
        if username not in timeline:
            return []

        # Return The Timeline Of The Username
        return timeline[username]

    def add_timeline(self, username: str, timeline_text: str) -> bool:
        """Adds A New Activity To The User's Timeline.

        Args:
            username (str): The User Whose New Activity Needs To be Added
            timeline_text (str): The Timeline Text

        Returns:
            bool: Whether The Adding Of The Timeline Was Successful.
        """

        # Read The Contents Of The File
        readings = self.read_file(os.getcwd() + "/utils/timeline.txt")

        # Check If The User Is Not None. Meaning That The User Has Not Logged In
        if username == None:
            return False

        # Check if the user already have any recent timeline or create a new one
        if username in readings.keys():
            readings[username].append(timeline_text)
        else:
            readings[username] = [timeline_text]

        # Write The New Information To The File
        with open(os.getcwd() + "/utils/timeline.txt", "w") as file:
            file.write(json.dumps(readings))

        # Return True
        return True

    def add_to_val(self, username: str, index: int, sub=False) -> bool:
        """Adds 1 To The Index Of The User's Profile [Name , Items Sold , Items Bought , Coins]. If sub is True, Then It Will Subtract 1 Instead Of Adding 1.

        Args:
            username (str): The User Whose Information needs To be changed.
            index (int): The index
            sub (bool, optional): Whether To Subtract Or Add. Defaults to False.

        Returns:
            bool: Whether The Process Was Successful Or Not
        """

        # Read The Contents Of The File
        readings = self.read_file(self.user_info_file)

        # Check If The User Wants To Subtract Or Add
        if sub:
            readings[username][index] -= 1
        else:
            readings[username][index] += 1

        # Write The Updated Information To The File
        with open(self.user_file_location, "w") as file:
            file.write(json.dumps(readings))

        # Return True
        return True

    def clear_browse(self) -> None:
        """Clears The Browsing Summary Of The Admin User"""
        readings = self.read_file(os.getcwd() + "/utils/timeline.txt")

        # Delete The Browsing History
        del readings[self.name]

        # Write The Updated Information
        with open(os.getcwd() + "/utils/timeline.txt", "w") as file:
            file.write(json.dumps(readings))

    def remove_from_pros(self, itemname: str):
        """Deletes A User's Product From The Market

        Args:
            itemname (str): Item Name That Needs To be Removed
        """
        # Same Concept
        readings = self.read_file(self.item_location)

        del readings[itemname]

        with open(self.item_location, "w") as file:
            file.write(json.dumps(readings))

        return True

    def remove_user(self, username, password):
        """Removes A User

        Args:
            username (str): Username That Needs To be Removed
            password (str): Password Of The User
        """
        readings = self.read_file(self.user_info_file)

        # Check If The Password Is Not Same Or The Name Is None
        if readings[username][-1] != password or self.name == None:
            return False

        del readings[username]

        with open(self.user_info_file, "w") as file:
            file.write(json.dumps(readings))

        # Clear The Browsing History
        self.clear_browse()

        return True

    def validate_name(self, username: str) -> bool:
        """Checks if The Username Is Appropriate For The User Registration

        Args:
            username (str): The User

        Returns:
            bool: The Username Is fit For User's name
        """
        for i in username.split():
            if not i.isalpha():
                return False

        return True

    def compare_password(self, username, password):
        """Checks If The Password Of The User Is Same To The Passed Password

        Args:
            username (str): The Username
            password (str): The Password

        Returns:
            bool: Whether The Passed Of The Username Is Correct
        """
        self.set_users()

        readings = self.get_info(username, need_password=True)

        if readings != password or self.name == None:
            return False

        return True
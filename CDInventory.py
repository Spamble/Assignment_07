#------------------------------------------#
# Title: CDInventory.py
# Desc: Program loads CD Inventory from file and allows user to add, delete,
# display or save data to file in 2d table (list of dictionaries).
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# BEagle-Jack, 2021-Feb-24, changed strFileName to binary file value
# BEagle-Jack, 2021-Feb-24, added import pickle module
# BEagle-Jack, 2021-Feb-25, changed read_file and write_file functions to use pickle
# BEagle-Jack, 2021-Feb-25, added exception handing to file opening
# BEagle-Jack, 2021-Feb-26, added exception handling to integer type casting
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # binary data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    """Processing the data to and from temporary memory"""
    
    @staticmethod
    def add_inventory(cd_id, cd_title, cd_artist, table):
        """Function to add CD inventory to 2D table
        
        Converts cd_id to integer from string input. Creates a dictionary by assigning 
        arguments to values in key-value pairs and appends dictionary to the list 
        of dictionaries that is available to user during runtime. 
        
        Args: 
            cd_id (string): value for key ID to be put in dictionary
            cd_title (string): value for key Title to be put in dictionary
            cd_artist (string): value for key Artist to be put in dictionary
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
            
        Returns: 
            None.       
        """
        dicRow = {'ID': cd_id, 'Title': cd_title, 'Artist': cd_artist}
        table.append(dicRow)


    
    @staticmethod    
    def del_id(id_num, table):
        """Function to delete a line of CD inventory from 2D table 
        
        Iterates through list of dictionaries and iterates through dictionary values
        with 'ID' key to check for input by user. If line_num matches value of 'ID'
        key then entire dictionary is removed from list and displays confirmed deletion. 
        Otherwise prints that inventory dictionary was not removed.
        
        Args:
            line_num (int): 
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
        
        Returns:
            None.
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == id_num:
                del table[intRowNr]
                blnCDRemoved = True
                break
        return blnCDRemoved


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name):
        """Function to read binary data from file

        Reads the data from file identified by file_name using pickle module and returns
        data (list of dicts). 

        Args:
            file_name (string): name of file used to read the data from

        Returns:
            inventory (list of dicts): 2D data structure that holds the data during runtime
        """

        with open(file_name, 'rb') as fileObj:
              inventory = pickle.load(fileObj)
        return inventory

    @staticmethod
    def write_file(file_name, table):
        """Function that writes binary data to file
        
        Writes 2d table data to file identified by file_name using pickle module. 
        
        Args:
            file_name (string): name of file used to write data to
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
            
        Returns:
            None.
        """
        with open(file_name, 'wb') as fileObj:
            pickle.dump(table, fileObj)

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case string of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice
    
    @staticmethod
    def del_choice():
        """Gets user input for ID to delete dictionary from 2d CD inventory list.
        
        Args: 
            None.
            
        Returns:
            delChoice (int): if the input can be turned into a function, the ID number
            is returned. 
            None: returned if input cannot be cast to integer type.
            
        """    
        delChoice = input('Which ID would you like to delete? ').strip()
        try: 
            delChoice = int(delChoice)
        except:
            return None
        else:             
            return delChoice
    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def input_inventory():
        """Function to gather inputs from user for CD inventory creation
        
        Args:
            None.
            
        Returns:
            strID (string): string stripped of new line for user input of CD ID
            strTitle (string): string stripped of new line for user input of CD Ttile
            strArtist (string): string stripped of new line for user input of CD Artist
            None: returns if strID cannot be converted from string to integer
        
        """
        strID = input('Enter ID: ').strip()
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        try: 
            strID = int(strID)
        except: 
            return None 
        else: 
            return strID, strTitle, strArtist
# 1. When program starts, try to read in the currently saved Inventory file
try:
    lstTbl = FileProcessor.read_file(strFileName)
except: 
    print('No CD inventory file to load.')
else:
    print('CD inventory file loaded to data.')
# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()
    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('looking for file...')
            # 3.2.1 try loading file 
            try: 
                lstTbl = FileProcessor.read_file(strFileName)
            except:
                print('No CD inventory file to load.')
            else:
                print('File found. reloading...')
                IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        cdValues = IO.input_inventory()
        # 3.3.2 check if there are return values to add to data          
        if cdValues == None:
            print('ID must be an integer.')
            IO.show_inventory(lstTbl)
        else: 
            # 3.3.3 Add data to table
            DataProcessor.add_inventory(cdValues[0], cdValues[1], cdValues[2], lstTbl)
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        intIDDel = IO.del_choice()
        # 3.5.1.3 check if integer ID value returned  
        if intIDDel == None:
            print('ID must be an integer.')
            IO.show_inventory(lstTbl)
            continue
        else:
            # 3.5.2 search thru table and delete CD
            removeID = DataProcessor.del_id(intIDDel, lstTbl)
        if removeID:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')





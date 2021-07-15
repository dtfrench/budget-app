class Category:

  # Initialize object instance with intial values. 
  def __init__(self, category):
    self.category = category
    self.account_balance = 0
    self.ledger = []
    self.total_withdraw = 0
    self.name = str(category) 
  
  # Method that will generate string representation of
  # returned object. 
  def __str__(self):

    # Determine the length of the category and the number of 
    # stars that will need to be generated on either side.
    category_length = len(self.category)
    star_length = 30 - category_length

    # Construct a string with half of the stars on each side of
    # the category. 
    half_star_length = ''
    for num in range(int(star_length/2)):
      half_star_length += '*'

    header_string = f"{half_star_length}{self.category}{half_star_length}\n"

    # Construct the table of ledger entries. The total length
    # cannot exceed 30. 
    body_string = ''
    for index in self.ledger:
      
      # If the amount in a ledger item is an int, convert it to a string
      # and append ".00" to it.
      if (type(index["amount"]) is int):
        index["amount"] = str(index["amount"]) + ".00"

        # Store index_len which will be used to keep the overall length 
        # of the string at 30. 
        index_len = (30 - len(str(index["amount"]))) - 1

      # If the length of a ledger entry description and amount together are
      # greater than 30, slice the description string to the length of
      #index_len
      if ((len(index["description"]) + len(str(index["amount"])) + 1) > 30):
        space_string = " "
        desc_string = index["description"]
        desc_string = desc_string[0:index_len]
      
      # If the length of the ledger entry description and amount are
      # less than 30, then use the whole description string and
      # generate enought spaces so the line is 30 characters long.
      elif ((len(index["description"]) + len(str(index["amount"])) + 1) < 30):
        space_string = ""
        for num in range(30 - (len(index["description"]) + len(str(index["amount"])))):
          space_string += " "
          desc_string = index["description"]

      # If the length of the ledger entry description and amount are
      # exactly thirty then use the whole description string with one space
      else:
        space_string = " "
        desc_string = index["description"]
      
      # Construct the string that displays the table of ledger entries.
      body_string += desc_string + space_string + str(index["amount"]) + "\n" 
    
    # Return the final result, inclduing the title of the category, 
    # table of entries, and total
    return header_string + body_string + "Total:" + " " + str(self.account_balance)
  
  # Function to check the account balance
  def check_funds(self, amount):

    # Return False if the amount passed into the function is greater
    # than the account balance.
    if (amount > self.account_balance):
      return False

    # Return True if the amount passed into the function is not greater
    # than the account balance.  
    else:
      return True

  # A function that deposit the adds the passed in amount to the account.
  def deposit(self, amount, description=None):

    # Add the passed-in amount to the acount balance. 
    self.account_balance += amount

    # If a description is passed in, use it as the decription in the ledger,
    # otherwise use an empty string as the description. 
    if (description != None):
      return_description = description
    
    else:
      return_description = ''
    
    # Add an entry contraining the amount and the description to the ledger.
    self.ledger.append({"amount": amount, "description": return_description})

  # A function thad withdraws the passed-in amount from the account. 
  def withdraw(self, amount, description=None):

    # Check if the passed-in amount is greater than the account balance.
    if (self.check_funds(amount) == False):
      return False

    # If the passed-in amount is not greater than the account balance,
    # add the amount to withdrawals, and subtract the amount from the 
    # account balance. 
    else:
      self.total_withdraw += amount
      self.account_balance -= amount
      
      ''''
      I learned how to to change a positive number to a negative from sources like below
      https://stackoverflow.com/questions/3854310/how-to-convert-a-negative-number-to-positive#3854323 
      '''
      # Change the number to a negative number for the ledger.
      negative_amount = -amount
      
      # If a description is passed-in use it for the description in the ledger
      if (description != None):
       return_description = description

      # If a description is not passed-in then use an empty string as account
      # description for the ledger. 
      else:
        return_description = ''
    
      self.ledger.append({"amount": negative_amount, "description": return_description})

      return True

  # A function to get the account balance. 
  def get_balance(self):
    return self.account_balance
  
  # A function to transfer an amount from one category to another.
  def transfer(self, amount, other_category):

    # Check if there are sufficient funds in the account. 
    if (self.check_funds(amount) == False):
      return False
    
    # If there are sufficient funds, add the amount to total withdrawals and
    # subtract the amount from the account balance. 
    else:
      self.total_withdraw += amount
      self.account_balance -= amount
      
      # Change the amount to a negative number for the ledger. 
      negative_amount = -amount
      
      # Add a ledger entry with the amount and a description 
      # that includes the name of the category that the amount 
      # was transferred to. 
      self.ledger.append({"amount": negative_amount, "description": f"Transfer to {other_category.name}"})

      # Add the amount to the account balance of the other category.
      other_category.account_balance += amount

      # Add a ledger entry in the other category with the amount and a 
      # description that includes the name of the category that the amount
      # was transferred from. 
      other_category.ledger.append({"amount": amount, "description": f"Transfer from {self.category}"})

      return True

# A function that displays a chart showing the percentage of spending for each
# category that is passed in. 
def create_spend_chart(categories):
  
  # Get
  all_withdraw = 0
  for category in categories:
    all_withdraw += category.total_withdraw
  
  percent_str = f"Percentage spent by category\n"
  chart_line = '----------'.rjust(14, ' ') + "\n"

  percent_num = 100
  for num in range(11):
    percent = str(percent_num).rjust(3,' ') + "|"

    for category in categories:
      rounded_withdraw = round((category.total_withdraw / all_withdraw) * 100)

      if (rounded_withdraw >= percent_num):
        percent += " o "
      
      else:
        percent += "   "
      
    percent_str += percent + " " + "\n"

    percent_num -= 10
   
  #Return the name of each category vertically below the chart
  category_lengths = []
  for category in categories:
    category_lengths.append(len(category.category))
  
  longest_category = max(category_lengths)

  vertical_strings = []
  j = 0
  i = 0
  for j in range(longest_category): 
    vert_category = ''
    for category in categories:
      try:
        vert_category += f"{category.category[i]}  "
    
      except:
        vert_category += '   '
    vertical_strings.append(vert_category)
    i+=1 
    j+=1 
  
  final_vert = ''
  for string in vertical_strings:
    '''
    I learned the proper syntax for getting the last index of a list below
    #https://stackoverflow.com/questions/930397/getting-the-last-element-of-a-list#930398
    '''
    if string != vertical_strings[-1]:
      string = string.rjust(14, ' ')
      final_vert += string + '\n'
    else:
      string = string.rjust(14, ' ')
      final_vert += string

  return percent_str + chart_line +  final_vert

  

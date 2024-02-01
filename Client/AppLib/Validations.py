class detaild_validations:
    
    def validate_username(username:str, minimumUsernameLength  = 4, maximumUsernameLength = 16):
        # Check if length is between constant numbers
        if len(username) > maximumUsernameLength or len(username) < minimumUsernameLength:
            return False
        
        # Check for no special symbols
        character_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 
                        'r', 's', 't', 'u', 'v', 'w','x','y','A','B','C','D','E','F','G','H','I','J','K','L',
                        'M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z', '0', '1', '2', '3', '4', '5',
                        '6', '7', '8', '9']
        user_copy = username
        for i in character_list:
            user_copy = user_copy.replace(i, '')
        
        return len(user_copy) == 0

    def validate_password(password:str, minimumPasswordLength = 8, maximumPasswordLength = 18):
        # Check if length is between constant numbers
        if len(password) > maximumPasswordLength or len(password) < minimumPasswordLength:
            return False
        
        # Check for no special symbols
        character_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 
                        'r', 's', 't', 'u', 'v', 'w','x','y','A','B','C','D','E','F','G','H','I','J','K','L',
                        'M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z', '0', '1', '2', '3', '4', '5',
                        '6', '7', '8', '9', '-','_','$','%']
        password_copy = password
        for i in character_list:
            password_copy = password_copy.replace(i, '')
        
        return len(password_copy) == 0
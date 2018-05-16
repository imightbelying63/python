import os

def cpanelUsers():
    user_dir = '/var/cpanel/users/'
    users_list = os.listdir(user_dir)
    users_list.remove('system')
    users_list.sort()

    print ''
    print 'cPanel user accounts:'
    print ''
    for user in users_list:
        print user
    print ''

if __name__ == "__main__":
    cpanelUsers()


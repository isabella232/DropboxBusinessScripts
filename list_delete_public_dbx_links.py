'''This script will either list or delete all publically 
accessible shared links which do not have a password'''

import dropbox

def getmembers():
    '''get all member id's on a team'''

    # if team is > 1000, also use members/list/continue
    members = dbxt.team_members_list().members
    memberids = [member.profile.team_member_id for member in members]
    
    return memberids

def getlinks(userid):
    '''get all public links for an individual member'''

    links = dbxt.as_user(userid).sharing_list_shared_links().links
    linkurls = [link for link in links
                if link.link_permissions.resolved_visibility.is_public()]

    return linkurls

def dellinks(userid):
    '''delete all public links for an individual member'''

    for link in getlinks(userid):
        dbxt.as_user(userid).sharing_revoke_shared_link(link.url)
        print("     %s has been deleted " % link.url)

def delall():
    '''delete all public links for all members'''

    for user in getmembers():
        dellinks(user)

def listlinks():
    '''print all public links urls for all members'''

    for user in getmembers():
        links = getlinks(user)
        link_count = len(links)
        print("%s has the following number of public links: %s" % (user, link_count))
        for link in links:
            print("    %s" % link.url)

if __name__ == '__main__':
    print("This script requires a API token with 'Team Member File Access premissions'")
    token = (input("Enter your token: "))
    mode = (input("Enter a mode (either 'list' or 'delete'): "))

    dbxt = dropbox.DropboxTeam(token)

    if mode == "list":
        listlinks()

    elif mode == "delete":
        delall()

    else:
        print("Please enter a mode of list or delete")



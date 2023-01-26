from atlassian import Confluence
import os,threading

#This creates connection object where you provide your confluence URL  and credentials.
confluence = Confluence(
    url='https://tools.publicis.sapient.com/confluence',
    username='xxxxxxxxx',
    password='xxxxxxxx')

# If you know page_id of the page, you can get page id by going to "Page Information" menu tab and the page id will be visible in browser as viewinfo.action?pageId=244444444444. This will return a response having key:value pairs having page details.
# page = confluence.get_page_by_id(page_id=1021972322)
# your_fname = "abc.pdf"
# confluence.get_child_id_list
file=''
dirchange=False
# #A function to create pdf from byte-stream responce
def save_file(content,your_fname):
    # while(dirchange):pass
    file_pdf = open(your_fname, 'wb')
    file_pdf.write(content)
    file_pdf.close()
    print(f"Completed {your_fname}.pdf")
    # confluence.g
# print(confluence.get_all_pages_from_space(space="UPS-GLD"))
forbidden_char=["*", '.', '''"''','/','<','>', '\\' ,'[' ,']', ':',';' ,'|' ,',',"'"]
#Get your confluence page as byte-stream
# response = confluence.get_page_as_pdf(page['id'])   
# save_file(response)
tabs=0
def convert_valid_fname(name):
    for char in forbidden_char:
        name=name.replace(char,'-')
    return name
def save_page_and_children(pageId ,path):
    global file,tabs,dirchange
    try:
        page=confluence.get_page_by_id(pageId)
    
        fname=convert_valid_fname( page['title'])
        # print(fname)
        try:
            childern=confluence.get_child_id_list(page['id'])
            t = '\t'*tabs
            save_file(confluence.get_page_as_pdf(page['id']),f'{path}\\{fname}.pdf')
            file = f"{file}{t}filename{fname}:{page['id']} childern:{childern}\n"
            if(len(childern)>0):
                while(dirchange):pass
                dirchange=True
                os.chdir(path)
                os.mkdir(fname)
                os.chdir(startpath)
                dirchange=False
                # os.chdir(f"{os.getcwd()}\\{fname}")
                tabs+=1
                for child in childern:
                    t = threading.Thread(target=save_page_and_children, args=[
                                        child, f"{path}\\{fname}"])
                    t.start()
                # n=os.getcwd()[0:os.getcwd().rfind('\\')] 
                tabs -= 1
                # os.chdir(n)
        except :
            print(f'faild getting children of {fname}')
            print('retrying')
            save_page_and_children(pageId,path)
    except :
        print(f'faild getting data of page with id : {pageId}')
        print('retrying')
        save_page_and_children(pageId, path)
startpath= os.getcwd()
os.mkdir('output')
save_page_and_children(PARENT_PAGE_ID, f'{startpath}\\output')
try:
    save_page_and_children(PARENT_PAGE_ID_2 ,f'{startpath}\\output')
except:
    print("exef")
    os.chdir(startpath)
    with open("res.txt",'w') as f :
        f.write(file)

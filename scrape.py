# project: p3
#adamsmith.haus/python/answers/how-to-download-an-image-using-requests-in-python#:~:text=Use%20requests.,()%20to%20download%20an%20image&text=Use%20open(filename%2C%20mode),to%20write%20it%20to%20file%20.
import pandas as pd
import requests
import time
class GraphScraper:
    def __init__(self):
        self.visited = set()
        self.order = []
        
        
    def go(self, node):
        raise Exception("must be overridden in sub classes -- don't change me here!")

        
    def dfs_search(self, node):
        # 1. clear out visited set
        self.visited=set()
        self.order=[]
        # 2. start recursive search by calling dfs_visit
        self.dfs_visit(node)
    
    
    def bfs_search(self, node):
        self.visited=list()
        self.order=[]
        node_list=[node]
        while len(node_list)>0:
            curr=node_list.pop(0)
            self.order.append(curr)
            self.visited.append(curr)
            for i in self.go(curr):
                if i not in self.visited and i not in node_list:
                    node_list.append(i)

    def dfs_visit(self, node):
        node_set=set()
        # 1. if this node has already been visited, just `return` (no value necessary)
        if node in self.visited:
            return
        # 2. mark node as visited by adding it to the set
        self.visited.add(node)
        # 3. add this node to the end of self.order
        self.order.append(node)
        # 4. get list of node's children with this: self.go(node)
        childern= self.go(node)
        # 5. in a loop, call dfs_visit on each of the children
        for i in childern:
            self.dfs_visit(i)
            
        
        
class MatrixSearcher(GraphScraper):
    def __init__(self, df):
        super().__init__() # call constructor method of parent class
        self.df = df
        
        
    def go(self, node):
        children = []
        # TODO: use `self.df` to determine what children the node has and append them
        if node not in self.df:
                return children
        for node, has_edge in self.df.loc[node].items():
            if has_edge:
                children.append(node)
        return children
    
    
class FileSearcher(GraphScraper):
    def __init__(self):
        super().__init__() 
        self.node_value=""
        self.nodelist=""
     
    def go(self, node):
        children=[]
        
        #changed "file_nodes/"+node to node
        with open("file_nodes/"+node) as f:
            self.node_value=next(f).strip()
            children.append(next(f).rstrip().split(","))
            self.nodelist+=self.node_value
        return children[0]
        
    def message(self):
        return self.nodelist
    
class WebSearcher(GraphScraper):
    def __init__(self,driver):
        super().__init__() 
        self.driver=driver
        self.maindf=pd.DataFrame()
        #create empty dataframe
        
        
    def go(self,node):
        #b=self.driver
        #node=url
        children=list()
        self.driver.get(node)
        df=pd.read_html(node)[0]
        self.maindf=self.maindf.append(df,ignore_index = True)
        trs=self.driver.find_elements(by="tag name", value="a")

        for link in trs:
            children.append(link.get_attribute("href"))
        return children
        
    def table(self):
        return self.maindf

    
    
def reveal_secrets(driver, url, travellog):

    password =""
    for i in travellog["clue"]:
        i=str(i)
        password+=i
        
    dd = driver
    dd.get(url)
    password_input=dd.find_elements(value="password")
    button=dd.find_elements(value="attempt-button")
    password_input[0].send_keys(password)
    button[0].click()
    time.sleep(2)
    button2=dd.find_elements(value="securityBtn")
    button2[0].click()
    time.sleep(2)
    
    img= dd.find_elements(value="image")
    src = img[0].get_attribute('src')
    response=requests.get(src)
    file = open("Current_Location.jpg", "wb")
    file.write(response.content)
    file.close()

    location=dd.find_elements(value="location")
    return location[0].text
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
import heapq
import queue
import time
# the function to read the input file
# stores all the channels in the form of a list
#stores initial state and final state as tuple
def read_input_file():
    with open ("input.txt") as file:
        algo=file.readline().strip()
        coordinates=file.readline().strip()
        initial_st=file.readline().strip()
        final_st=file.readline().strip()
        channel_number=int(file.readline().strip())
        
        channels={}
        for i in range(0,channel_number):
            #print(i)
            channel_config=file.readline().strip()
            x,y,z,w=[int(i) for i in channel_config.split(" ")]
            if (x,y,z) in channels.keys():
                channels[(x,y,z)].append([x,y,z,w])
            else:
                channels[(x,y,z)]=[[x,y,z,w]]
        #print(channels)  
        x,y=[int(i) for i in coordinates.split(" ")]
        initial_state=[]
        initial_state=tuple([int(i) for i in initial_st.split(" ")])
        #print("initial_state",initial_state)
        final_state=[]
        final_state=tuple([int(i) for i in final_st.split(" ")])
        #print("initial_state",final_state)
        
    process_input(algo,initial_state,final_state,channels,x,y)
    
    
             
 #function to parse the algo from the input and run the required function 
def process_input(algo,initial_state,final_state,channels,x,y):
    #print(initial_state)
    #print(algo)
    #print(final_state)
    #print(channels)
    if algo=="BFS":
        bfs_search(initial_state,final_state,channels,x,y)
    if algo=="UCS":
        ucs_search(initial_state,final_state,channels,x,y)
    if algo=="A*":
        a_search(initial_state,final_state,channels,x,y)
        
 
 
 # the function to test if a state is goal state or not       
def goal_test(current_state,final_state):
    #print(current_state)
    #print(final_state)
    if current_state[0]==final_state[0] and current_state[1]==final_state[1] and current_state[2]==final_state[2]:
        return True
    else:
        return False
 
   
# creating a node class to save the current location,cost,path and parent for a particular state   
class MakeNode(object):
    def __init__(self,config,path):
        
        self.configuration=(config[0],config[1],config[2])
        self.cost=config[3]
        self.path=path
        self.parent=None
  
#defined to overwrite the less than function for priority queue comparisons  
    def __lt__(self, other):
        
        in1=self.cost
        in2=other.cost
        if in1<in2:
            
            return self
        else:
            return other
            
    def print_node(self):
        print(self.configuration)
        print(self.cost)
        print(self.path)
        
       

def bfs_search(initial_state,final_state,channels,x,y):
    
    # function defines whether the next state is within grid limits or not
    
    def safe_move(pos_x,pos_y,x,y):
        if pos_x>=0 and pos_y>=0 and pos_x<x and pos_y<y:
            return True
        else:
            return False
      

     # function extracts all the possible states that can be reached from a particular state
    def neighbor_node_list(current_state,x,y,channels):
        neighbors=[]
        possible_direction=[(1,1),(1,-1),(-1,1),(-1,-1),(0,1),(0,-1),(1,0),(-1,0)]
        if (current_state[0],current_state[1],current_state[2]) in channels.keys():
            for i in channels[(current_state[0],current_state[1],current_state[2])]:
                #print(i)
                neighbors.append((i[3],i[1],i[2],1))
            
           
        
        
        #if len(channels)>0:
         #   for i in channels.keys():
            #print(i)
          #      if current_state[0]==i[0] and current_state[1]==i[1] and current_state[2]==i[2]:
                #print("arey baba")
           #         print("trial",channels[i])
            #        neighbors.append((i[3],i[1],i[2],1))
                #print(neighbors)
        for i in possible_direction:
            new_x=current_state[1]+i[0]
            new_y=current_state[2]+i[1]
            if safe_move(new_x,new_y,x,y):
                neighbors.append((current_state[0],new_x,new_y,1))
        return neighbors


    # function to create the final output file
    def final_output_file(cost,path,bool_value):
        outfile = open("output.txt", "w+")
        outstring=""
        if bool_value == False:
            outfile.write("FAIL")
            outfile.close()
            return
            
        outfile.write(str(cost))
        outfile.write("\n")
        outfile.write(str(len(path)))
        outfile.write("\n")
        for step in path: 
            #print(type(step))
            outstring += (str(step[0][0]) + " " + str(step[0][1]) + " " +str(step[0][2]) + " " + str(step[1]))
            outstring+="\n"
        
        outfile.write(outstring.rstrip())
        outfile.close()
        return
        
    # function that runs the final algorithm
    def run_bfs(initial_state,final_state,channels,x,y):

        # set for o(1) complexity
        final_path=set((initial_state[0],initial_state[1],initial_state[2],0))
        visited=set()
        frontier=queue.Queue()
        root_node=MakeNode([initial_state[0],initial_state[1],initial_state[2],0],0)
        frontier.put(root_node)
        visited.add(root_node.configuration)
        root_node.parent=root_node.configuration
        counter=1
        while True:
            
            if frontier.empty():
                final_output_file(0,0,False)
                return 
                
            
            current_state=frontier.get() 
           
                
            
            if goal_test(current_state.configuration,final_state):
                parent_1=current_state
                path_final=[]
                while parent_1!=initial_state:
                    path_final.append((parent_1.configuration,parent_1.path))
                    #print("checking",path_final)
                    parent_1=parent_1.parent
         
                    #print("checking",path_final)
                path_final.reverse()
              
                final_output_file(current_state.cost,path_final,True)
            
                return "finally"
            #print(visited)
            #print("length of frontier",frontier.qsize())
            for i in neighbor_node_list(current_state.configuration,x,y,channels):
                if (i[0],i[1],i[2]) not in visited:
                    
                    if goal_test((i[0],i[1],i[2]),final_state):
                        
                        next_node=MakeNode(i,current_state.path)
                        next_node.cost=current_state.cost+i[3]
                        next_node.path=i[3]
                        
                    
                        next_node.parent=current_state
                    
                    
                        frontier.put(next_node)
                        parent_1=next_node
                        path_final=[]
                        while parent_1!=initial_state:
                            path_final.append((parent_1.configuration,parent_1.path))
                            #print("checking",path_final)
                            parent_1=parent_1.parent
         
                        #print("checking",path_final)
                        path_final.reverse()
                        final_output_file(next_node.cost,path_final,True)
            
                        return "finally"
                  
                    next_node=MakeNode(i,current_state.path)
                    next_node.cost=current_state.cost+i[3]
                    next_node.path=i[3]
                    
                    next_node.parent=current_state
                    
                    
                    frontier.put(next_node)
                    #next_node.print_node()
                    visited.add(next_node.configuration)
                    
            
    run_bfs(initial_state,final_state,channels,x,y)        
    
    
    
def ucs_search(initial_state,final_state,channels,x,y):
    
    def safe_move_ucs(pos_x,pos_y):
        
        if pos_x>=0 and pos_y>=0 and pos_x<x and pos_y<y:
            return True
        else:
            return False
            
    def neighbor_node_list_ucs(current_state):
        neighbors=[]
        possible_direction=[(1,1),(1,-1),(-1,1),(-1,-1),(0,1),(0,-1),(1,0),(-1,0)]
        count=0
        for i in possible_direction:
        
            new_x=current_state[1]+i[0]
            new_y=current_state[2]+i[1]
            if safe_move_ucs(new_x,new_y) and count<=3:
                neighbors.append([current_state[0],new_x,new_y,14])
            elif safe_move_ucs(new_x,new_y) and count>3:
                neighbors.append([current_state[0],new_x,new_y,10])
            count=count+1
            
            
        if (current_state[0],current_state[1],current_state[2]) in channels.keys():
            for i in channels[(current_state[0],current_state[1],current_state[2])]:
                #print(i)
                neighbors.append((i[3],i[1],i[2],abs(i[3]-i[0])))
        #if len(channels)>0:
         #   for i in channels:
          #      if current_state[0]==i[0] and current_state[1]==i[1] and current_state[2]==i[2]:
                    
           #         neighbors.append([i[3],i[1],i[2],abs(i[3]-i[0])])

        return neighbors
    
    
    def final_output_file(cost,path,bool_value):
        outfile = open("output.txt", "w+")
        outstring=""
        if bool_value == False:
            outfile.write("FAIL")
            outfile.close()
            return
            
        outfile.write(str(cost))
        outfile.write("\n")
        outfile.write(str(len(path)))
        outfile.write("\n")
        for step in path: 
            #print(type(step))
            outstring += (str(step[0][0]) + " " + str(step[0][1]) + " " +str(step[0][2  ]) + " " + str(step[1]))
            outstring+="\n"
        
        outfile.write(outstring.rstrip())
        outfile.close()
        return
    
    def run_ucs(initial_state,final_state,channels,x,y):
        visited=set()
        frontier=[]
        closed=set()
        
        # a dictionary to store all the elemnets present in the priority queue for searching in o(1) time
        hashmap_queue={}
        
        # a dictionary to store costs for a given state 
        cost={}
        
        root_node=MakeNode([initial_state[0],initial_state[1],initial_state[2],0],0) 
        heapq.heappush(frontier,(root_node.cost,root_node))
        counter=1
        cost[root_node.configuration]=0
        hashmap_queue[root_node.configuration]=counter
        root_node.parent=root_node.configuration
        counter=counter+1
        
        while True:
            if len(frontier)==0:
                
                final_output_file(0,0,False)
                return
            
            current_state=heapq.heappop(frontier)[1]
            
            visited.add(current_state.configuration)
            #try:
             #   del hashmap_queue[current_state.configuration]
            #except:
             #   pass
            
            if goal_test(current_state.configuration,final_state):
                parent_1=current_state
                path_final=[]
                while parent_1!=initial_state:
                    path_final.append((parent_1.configuration,parent_1.path))
                    #print("checking",path_final)
                    parent_1=parent_1.parent
         
                    #print("checking",path_final)
                
                path_final.reverse()
                
            
            
                final_output_file(current_state.cost,path_final,True)
            
                return "finally"
            
            child_nodes = neighbor_node_list_ucs(current_state.configuration)
             
            for i in child_nodes:
                
                if (i[0],i[1],i[2]) not in visited and (i[0],i[1],i[2]) not in hashmap_queue.keys() :
                    next_node=MakeNode(i,current_state.path)
                    
                    next_node.cost=current_state.cost+i[3]
                    next_node.path=i[3]

                    next_node.parent=current_state
                    
                    cost[(i[0],i[1],i[2])]=next_node.cost
                    heapq.heappush(frontier,(next_node.cost,next_node))
                    hashmap_queue[next_node.configuration]=counter
                    counter=counter+1
                    #next_node.print()
                    
                    
                #elif (i[0],i[1],i[2]) in visited :
                    
                 #   if i[3]+cost[current_state.configuration] < cost[(i[0],i[1],i[2])]:
                  #      new_node=MakeNode(i,current_state.path)
                   #     cost[(i[0],i[1],i[2])]=cost[current_state.configuration]+i[3]
                    #    new_node.cost=cost[current_state.configuration]+i[3]
                     #   new_node.path=new_node.path+[i]

                      #  new_node.parent=current_state
                    
                    
                       # heapq.heappush(frontier,(new_node.cost,new_node))
                        #hashmap_queue[new_node.configuration]=counter
                        #counter=counter+1
                        #visited.remove((i[0],i[1],i[2]))
                    
                elif (i[0],i[1],i[2]) in hashmap_queue.keys() :
                    
                    if i[3]+cost[current_state.configuration] < cost[(i[0],i[1],i[2])]:
                        new_node=MakeNode(i,current_state.path)
                        cost[(i[0],i[1],i[2])]=cost[current_state.configuration]+i[3]
                        new_node.cost=cost[current_state.configuration]+i[3]
                        new_node.path=i[3]

                        new_node.parent=current_state
                    
                    
                        heapq.heappush(frontier,(new_node.cost,new_node))
                        hashmap_queue[new_node.configuration]=counter
                        counter=counter+1
                        
                            
        
    run_ucs(initial_state,final_state,channels,x,y)    


def a_search(initial_state,final_state,channels,x,y):

    def safe_move(pos_x,pos_y):
        if pos_x>=0 and pos_y>=0 and pos_x<x and pos_y<y:
            return True
        else:
            return False
   
   
   #heuristic for the a star
    def heuristic(current_state,final_state):
        x_dir = abs(current_state[1] - final_state[1])
        y_dir = abs(current_state[2] - final_state[2])
        diagonal_mvt=min(x_dir,y_dir)
        vertical_horizontal=abs(x_dir-y_dir)
        cost = 14*diagonal_mvt + 10*vertical_horizontal + abs(current_state[0] - final_state[0])
        return cost
        
    def neighbor_node_list_astar(current_state):
        
        neighbors=[]
        possible_direction=[(1,1),(1,-1),(-1,1),(-1,-1),(0,1),(0,-1),(1,0),(-1,0)]
        count=0
        for i in possible_direction:
        
            new_x=current_state[1]+i[0]
            new_y=current_state[2]+i[1]
            if safe_move(new_x,new_y) and count<=3:
                neighbors.append([current_state[0],new_x,new_y,14])
            elif safe_move(new_x,new_y) and count>3:
                neighbors.append([current_state[0],new_x,new_y,10])
            count=count+1
        if (current_state[0],current_state[1],current_state[2]) in channels.keys():
            for i in channels[(current_state[0],current_state[1],current_state[2])]:
                #print(i)
                neighbors.append((i[3],i[1],i[2],abs(i[3]-i[0])))
        #if len(channels)>0:
         #   for i in channels:
          #      if current_state[0]==i[0] and current_state[1]==i[1] and current_state[2]==i[2]:
                    
           #         neighbors.append([i[3],i[1],i[2],abs(i[3]-i[0])])

        return neighbors
    #neighbor_node_list() 
    
    def final_output_file(cost,path,bool_value):
        outfile = open("output.txt", "w+")
        outstring=""
        if bool_value == False:
            outfile.write("FAIL")
            outfile.close()
            return
            
        outfile.write(str(cost))
        outfile.write("\n")
        outfile.write(str(len(path)))
        outfile.write("\n")
        for step in path: 
            #print(type(step))
            outstring += (str(step[0][0]) + " " + str(step[0][1]) + " " +str(step[0][2]) + " " + str(step[1]))
            outstring+="\n"
        
        outfile.write(outstring.rstrip())
        outfile.close()
        return
    
    
    
    def run_astar(initial_state,final_state,channels,x,y):
        visited=set()
        frontier=[]
        closed=set()
        hashmap_queue={}
        
        
        # a dictionary to store costs for a given state with and without heuristic cost
        cost={}
        
        root_node=MakeNode([initial_state[0],initial_state[1],initial_state[2],0],0) 
        heapq.heappush(frontier,(root_node.cost,root_node))
        
        #print("heuristic",heuristic(initial_state,final_state))
        cost[root_node.configuration]=(0,heuristic(initial_state,final_state))
        counter=1
        hashmap_queue[root_node.configuration]=counter
        counter=counter+1
        root_node.parent=root_node.configuration
        
        while True:
            if len(frontier)==0:
                
                final_output_file(0,0,False)
                return
            #print(heapq.heappop(frontier))
            current_state=heapq.heappop(frontier)[1]
            #try:
             #   del hashmap_queue[current_state.configuration]
            #except:
             #   pass
            #print("len",len(frontier))
            visited.add(current_state.configuration)
            #print("popped child",current_state.configuration)
            
            
            
            if goal_test(current_state.configuration,final_state):
             
                parent_1=current_state
                path_final=[]
                while parent_1!=initial_state:
                    path_final.append((parent_1.configuration,parent_1.path))
                    #print("checking",path_final)
                    parent_1=parent_1.parent
         
                    #print("checking",path_final)
                
                path_final.reverse()
                
                final_output_file(cost[current_state.configuration][0],path_final,True)
            
                return "finally"
            
            child_nodes = neighbor_node_list_astar(current_state.configuration)
             
            for i in child_nodes:
                
                if (i[0],i[1],i[2]) not in visited and (i[0],i[1],i[2]) not in hashmap_queue.keys():
                    next_node=MakeNode(i,current_state.path)
                
                    cost[(i[0],i[1],i[2])]=(cost[current_state.configuration][0]+i[3],cost[current_state.configuration][0]+i[3]+heuristic((i[0],i[1],i[2]),final_state))
                    next_node.cost=cost[current_state.configuration][0]+i[3]+heuristic((i[0],i[1],i[2]),final_state)
                    next_node.path=i[3]

                    next_node.parent=current_state
                    
                    
                    heapq.heappush(frontier,(next_node.cost,next_node))
                    hashmap_queue[next_node.configuration]=counter
                    counter=counter+1
                    
                        
                #if (i[0],i[1],i[2]) in visited:
                   
                 #   if i[3]+cost[current_state.configuration][0]+heuristic((i[0],i[1],i[2]),final_state) < cost[(i[0],i[1],i[2])][1]:
                  #      new_node=MakeNode(i,current_state.path)
       
                   #     cost[(i[0],i[1],i[2])]=(cost[current_state.configuration][0]+i[3],cost[current_state.configuration][0]+i[3]+heuristic((i[0],i[1],i[2]),final_state))
                    #    new_node.cost=cost[current_state.configuration][0]+i[3]+heuristic((i[0],i[1],i[2]),final_state)
                     #   new_node.path=new_node.path+[i]

                      #  new_node.parent=current_state
                    
                    
                       # heapq.heappush(frontier,(new_node.cost,new_node))
                        #hashmap_queue[new_node.configuration]=counter
                        #counter=counter+1
                        #visited.remove((i[0],i[1],i[2]))
                    
                    
                if (i[0],i[1],i[2]) in hashmap_queue.keys():
                    
                    if i[3]+cost[current_state.configuration][0]+heuristic((i[0],i[1],i[2]),final_state) < cost[(i[0],i[1],i[2])][1]:
                        new_node=MakeNode(i,current_state.path)
                        cost[(i[0],i[1],i[2])]=(cost[current_state.configuration][0]+i[3],cost[current_state.configuration][0]+i[3]+heuristic((i[0],i[1],i[2]),final_state))
                        new_node.cost=cost[current_state.configuration][0]+i[3]+heuristic((i[0],i[1],i[2]),final_state)
                        new_node.path=i[3]

                        new_node.parent=current_state
                    
                    
                        heapq.heappush(frontier,(new_node.cost,new_node))
                        hashmap_queue[new_node.configuration]=counter
                        counter=counter+1
                    
                        
                           
        
    run_astar(initial_state,final_state,channels,x,y)
    
    
    
    
    
    
#cProfile.run('read_input_file()')    
start=time.time()   
read_input_file() 
print(time.time()-start)
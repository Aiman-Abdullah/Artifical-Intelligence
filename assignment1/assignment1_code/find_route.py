import sys
from collections import deque

class Node:
    def __init__(node, n, cum, d, f):
        node.cum = cum
        node.d = d
        node.f = f
        node.n = n
        node.parents = None
		
class uninform_search:
       def find_route(node, start, destination):
           input_file = sys.argv[1] 
           input_file = open(input_file, "r")
           x=0
           path = []
           V = []
           for i in input_file:
               if 'EOF' in i or 'END' in i:
                   break
               else:
                   way = i.split()
                   src = way[0]
                   dst = way[1]
                   dist = way[2]
                   path1 = [src, dst, dist]
                   path2 = [dst, src, dist]
                   path.append(path1)
                   path.append(path2)
           
           frienge = deque()
           frienge.append(Node(start, 0, 0, None))
           nodes_expanded = 0
           flag = False
           while True:
               if len(frienge) != 0:
                   global j
                   if(len(frienge)>j):
                       j = len(frienge)
                   exp = frienge.popleft()
                   x = x+1
                   nodes_expanded += 1
                   if exp.n == destination: 
                       break
                   else:
                       if exp.n not in V: 
                           V.append(exp.n) 
                           for num in path:
                               if num[0] == exp.n:
                                   n = Node(num[1], exp.cum+int(num[2]), exp.d+1, None)
                                   n.parents= exp
                                   frienge.append(n)
                                   s=sorted(frienge, key=lambda node:node.cum)
                                   frienge=deque(s)
               else:
                   flag = True
                   break
 
           x = x +len(frienge)
           if(flag != True):
               print ("Nodes Expanded: "+str(nodes_expanded))
               print ("Nodes Generated:" +str(x-1))
               print ("Max Nodes in Memory:" +str(j))
               print ("Distance: " + str(exp.cum))
               print ("Route: ")
               route = []
               route.append(destination)
               while exp.parents != None:
                   route.append(exp.parents.n)
                   exp = exp.parents
               route.reverse()
               i=0
               while i < len(route)-1:
                   for v in path:
                       if route[i]==v[0] and route[i+1] == v[1]:
                           print (v[0] +" to "+ v[1]+ " - "+v[2])
                   i += 1
           else:       
               print ("Nodes Expanded: "+str(nodes_expanded))
               print ("Nodes Generated:" +str(x-1))
               print ("Max Nodes In Memory:" +str(j))
               print ("Distance: Infinity")
               print ("Route: None")
        
class inform_search:
       
    def find_route(node, start, destination):
      
           input_file = sys.argv[1]
           hurestic_file = sys.argv[4]
           input_file = open(input_file, "r")
           h_file = open(hurestic_file, "r")
           x = 0;
           path = []
           hue = []
           V = []
           for i in h_file:
               if "EOF" in i or 'END' in i:
                   break
               else:
                   hueristic = i.split()
                   city = hueristic[0]
                   hueristic_value = hueristic[1]
                   hue.append([city, hueristic_value])
           for i in input_file:
               if "EOF" in i or 'END' in i:
                   break
               else:
                   way = i.split()
                   src = way[0]
                   dst = way[1]
                   dist = way[2]
                   path1 = [src, dst, dist]
                   path2 = [dst, src, dist]
                   path.append(path1)
                   path.append(path2)
           frienge = deque()
           frienge.append(Node(start, 0, 0, 0))
           nodes_expanded=0
           flag = False
           while True:
               if len(frienge) != 0:
                   global j
                   if(len(frienge)>j):
                       j = len(frienge)
                   exp = frienge.popleft()
                   x = x + 1
                   nodes_expanded += 1
                   if exp.n == destination:
                       break
                   else:
                       if exp.n not in V:
                           V.append(exp.n)
                           for num in path:
                               if num[0] == exp.n:
                                   for h in hue:
                                       if h[0] == num[1]:
                                           hue_num = h[1]
 
                                   n = Node(num[1], exp.cum+int(num[2]), exp.d+1, exp.cum+int(num[2])+int(hue_num))
                                   n.parents= exp
                                   frienge.append(n)
                                   s=sorted(frienge, key=lambda node:node.f)
                                   frienge=deque(s)
               else:
                   flag = True
                   break
           x = x+len(frienge)
           if(flag != True):
               print ("Nodes Expanded: "+str(nodes_expanded))
               print ("Nodes Generated:" +str(x-1))
               print ("Max Nodes In Memory:" +str(j))
               print ("Distance: " + str(exp.cum))
               print ("Route: ")
               route = []
               route.append(destination)
               while exp.parents != None:
                   route.append(exp.parents.n)
                   exp = exp.parents
               route.reverse()
               i=0
               while i < len(route)-1:
                   for v in path:
                       if route[i]==v[0] and route[i+1] == v[1]:
                           print (v[0] +" to "+ v[1]+ " - "+v[2])
                   i += 1

           else:
               print ("Nodes Expanded: "+str(nodes_expanded))
               print("Nodes Generated:" +str(x-1))
               print("Max Nodes In Memory:" +str(j))
               print ("Distance: Infinity")
               print ("Route: None")



if __name__ == "__main__":         
            j=0
            source = sys.argv[2]
            destination = sys.argv[3]
            if len(sys.argv) >4:
                m=inform_search()
            else:
                m=uninform_search()
            m.find_route(source, destination)
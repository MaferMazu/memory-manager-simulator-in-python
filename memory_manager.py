
class MemoryManager:
    """ Memory Manager Class """
    def __init__(self,num):
        result=0
        counter=0
        while result<=num:
            result=2**counter
            counter=counter+1

        self.free_blocks=[[] for i in range(counter-1)]
        self.used_blocks=[]
        self.size=num
        self.free_size=num

        self.distribution(0,num)

    def distribution(self,my_dir,size):
        """ Function that takes a dir and free size and assign in my self.free_blocks
        Input:
            my_dir : int
                Represent the direction in memory
            size : int
                Represent the amount of memory to set in free_blocks """
        result=0
        counter=0
        while result<=size:
            result=2**counter
            counter=counter+1
        counter=counter-2
        max_block_size=2**(counter)
        self.free_blocks[counter].append(my_dir)
        self.free_blocks[counter].sort()
        self.reposition(self.free_blocks[counter],counter)
        self.reorder_free()
        new_dir=my_dir+max_block_size
        rest=size-max_block_size
        if rest>0:
            self.distribution(new_dir,rest)

    def reposition(self,my_list,number_of_list):
        """ Function that compare to dirs in the same free_block 
        and if they are continuos then create one block in higher level.
        Input:
            my_list : list
                List to analyze.
            number_of_list : int
                This number represents the level of the block i am analyzing."""
        if number_of_list+1<len(self.free_blocks):
            block_size=2**(number_of_list)
            for i in range(len(my_list)-1):
                if my_list[i]+block_size==my_list[i+1]:
                    new_block_size=2**(number_of_list+1)
                    temp=my_list[i]
                    del my_list[i]
                    del my_list[i]
                    self.distribution(temp,new_block_size)
                    break

    def reserve(self,name,size):
        """ Function that reserve memory.
        Input:
            name : str
                Name of my variable
            size : int
                Size to reserve"""

        if self.is_var_reserved(name):
            print("Variable already reserved")
        
        else:
            if size>self.free_size:
                print("Out of memory") 
            else:
                # To know the level in my free_blocks
                result=0
                counter=0
                while result<=size:
                    result=2**counter
                    counter=counter+1
                if size==2**(counter-2):
                    counter=counter-2
                else:
                    counter=counter-1
                
                # If my reservation fit in the last block
                while counter<len(self.free_blocks):
                    if len(self.free_blocks[counter])>0:
                        my_dir=self.free_blocks[counter][0]
                        self.used_blocks.append([name,my_dir,size])
                        block_size=2**(counter)
                        rest=block_size-size
                        self.reorder_free()
                        if rest==0:
                            del self.free_blocks[counter][0]
                            self.free_size=self.free_size-size
                            break
                        elif rest>0:
                            new_dir=my_dir+size
                            del self.free_blocks[counter][0]
                            self.free_size=self.free_size-size
                            self.distribution(new_dir,rest)
                            break
                    else:
                        counter=counter+1

                # If my reservation doesn't fit in my last block and i need more
                if counter>(len(self.free_blocks)-1):
                    for i in range(len(self.free_blocks)-1,0,-1):
                        block_size=2**(i)
                        if len(self.free_blocks[i])>0:
                            print(len(self.free_blocks[i]))
                            for j in range(len(self.free_blocks[i])):
                                if len(self.free_blocks[i])>0:
                                    my_dir=self.free_blocks[i][j]
                                    chain=[]
                                    chain.append([i,j])
                                    while True:
                                        next=my_dir+block_size
                                        x,y=self.is_free(next)
                                        if x!=-1 and y!=-1:
                                            chain.append([x,y])
                                            block_size=block_size+2**(x)
                                            count=len(chain)
                                            if block_size==size:
                                                self.used_blocks.append([name,my_dir,size])
                                                self.free_size=self.free_size-size
                                                for i in range(count):
                                                    exec(f"del self.free_blocks[{str(chain[i][0])}][{str(chain[i][1])}]")
                                                break
                                            elif block_size>size:
                                                self.used_blocks.append([name,my_dir,size])
                                                self.free_size=self.free_size-size
                                                rest=block_size-size
                                                new_dir=my_dir+size
                                                for i in range(count):
                                                    exec(f"del self.free_blocks[{chain[i][0]}][{chain[i][1]}]")
                                                self.distribution(new_dir,rest)
                                                break
                                            else:
                                                pass
                                        else:
                                            print("Out of memory")
                                            break
                                    break
                            break

    def is_free(self,dir):
        """ Function that return what level is that address.
        Input:
            dir: int
                Memory address to analyze.
        Output:
            (i,index) : (int,int)
                i, the first output, is the level
                index, the second, is the position in that level """
        for i in range(len(self.free_blocks)-1):
            if len(self.free_blocks[i])>0:
                index=binary_search(self.free_blocks[i],0,len(self.free_blocks[i])-1,dir)
                if index>=0:
                    return (i,index)
        return (-1,-1)

    def remove(self,var):
        """ Function that remove reserved space
        Input:
            var : str
                Name of my variable """
        elem,index=self.search_var(var)
        if elem!=None or index!=-1:
            position=elem[1]
            size=elem[2]
            self.distribution(position,size)
            del self.used_blocks[index]
            self.free_size=self.free_size+elem[2]
        else:
            print(f"Can't remove undefined variable")


    def is_var_reserved(self,var):
        """ Function to know if the variable was reserved.
        Input:
            var : str
                Name of my variable
        Output:
            bool : bool
                If variable is reserved.
        """
        response,index=self.search_var(var)
        if response!=None:
            return True
        else:
            return False

    def search_var(self,var):
        """ Function that return info and index of a var
        Input:
            var : str
                Name of my variable
        Output:
            (elem,index) : (int,int)
                elem: list
                    [name,dir,size] that represents reserved space.
                index : int
                    the index in used_blocks """
        if len(self.used_blocks)>0:
            for i in range(len(self.used_blocks)):
                my_var=self.used_blocks[i][0]
                if var==my_var:
                    return (self.used_blocks[i],i)
        return (None,-1)
    
    def __str__(self):
        """ The str function, used for prints. """
        response="Free blocks directions: "
        if len(self.free_blocks)>0:
            for i in range(len(self.free_blocks)):
                if len(self.free_blocks[i])>0:
                    response=response+"\nSize "+str(2**(i))+": "+str(self.free_blocks[i])
        if response=="Free blocks directions: ":
            response=response+"None"
        
        response=response+"\nUsed blocks: "
        if len(self.used_blocks)>0:
            for elem in self.used_blocks:
                var=elem[0]
                position=elem[1]
                size=elem[2]
                response=response+"\nDirection: "+str(position)+", size: "+str(size)+", variable: "+str(var)
        else:
            response=response+"None"
        return response

    def reorder_free(self):
        """ It serves to have an order in the free spaces and to 
        get the adjoining spaces faster"""
        for i in range(len(self.free_blocks)-1):
            if len(self.free_blocks[i])>0:
                for j in range(i+1,len(self.free_blocks)-2):
                    if len(self.free_blocks[j])>0:
                        if self.free_blocks[i][0]+2**(i)==self.free_blocks[j][0] and self.free_blocks[i][0]<self.free_blocks[j][0]:
                            temp=self.free_blocks[i][0]
                            del self.free_blocks[i][0]
                            del self.free_blocks[j][0]
                            self.distribution(temp,2**(i)+2**(j))
                            break

def binary_search(arr, low, high, x):
    """ Binary search from 
        https://www.geeksforgeeks.org/python-program-for-binary-search/ 
        Input:
            arr : list
                Array to analyze.
            low : int
                Represent from what position i am going to analyze.
            high : int
                Represent how far i am going to analyze.
            x : int
                It is the element that i am looking for.
        Output:
            index : int
                - 1 if i didn't get the element x"""
 
    # Check base case
    if high >= low:
 
        mid = (high + low) // 2
 
        # If element is present at the middle itself
        if arr[mid] == x:
            return mid
 
        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif arr[mid] > x:
            return binary_search(arr, low, mid - 1, x)
 
        # Else the element can only be present in right subarray
        else:
            return binary_search(arr, mid + 1, high, x)
 
    else:
        # Element is not present in the array
        return -1

from policy import Policy
import numpy as np
from copy import deepcopy
class CPolicy(Policy):
    def __init__(self):
        # Student code here
        self.idx_stock=[]
        self._stocks=[]
        self.num_stocks=0
        self.list_prod=[]
        self.list_action=[]
        self.num_prod=[0]
        self.prod_area_left=0
        self.prod_area=0
    def ___csize___(self,stock):
        return  np.max(np.sum(np.any(stock>-1, axis=1))),np.max(np.sum(np.any(stock>-1, axis=0)))
    def get_action(self,observation,info):
        if(info["filled_ratio"]==0):
            self.__init__()
            self._stocks=deepcopy(observation["stocks"])
            self.num_stocks=deepcopy(len(self._stocks))
            self.prod_area_left=sum(np.prod(prod["size"])*prod["quantity"] for prod in observation["products"] )
            self.idx_stock=sorted(enumerate(observation["stocks"]),key=lambda x:np.prod(self._get_stock_size_(x[1])),reverse=True)
            self.list_prod =sorted(deepcopy(observation["products"]),key=lambda x: np.prod(x["size"]),reverse=True)
            self.render_action()
            self.idx_stock.reverse()
            self.num_prod.reverse()
            end=np.sum(self.num_prod)
            idx=0
            for d in self.num_prod:
                start=end-d
                x,y=self.list_action[end-1]["size"]
                while True:
                    i,stock=self.idx_stock[idx]
                    w,h=self._get_stock_size_(stock)
                    if x<=w and y<=h:
                        for j in range(start,end):
                            self.list_action[j]["action"]["stock_idx"]=i
                        end-=d
                        idx+=1
                        break
                    idx+=1
            self.list_action.reverse()
        if len(self.list_action)>0: return self.list_action.pop()["action"]
        else : return {"stock_idx": -1, "size": [-1,-1], "position": (None, None)}
    def place_prod(self, stock, prod):
        pos_x, pos_y = None, None
        minx,miny=0,0
        cx,cy=self.___csize___(stock)
        stock_w, stock_h = self._get_stock_size_(stock)
        prod_size=prod["size"]
        prod_w, prod_h =  prod_size
        if stock_w < prod_w or stock_h < prod_h: return pos_x,pos_y,minx,miny,prod_size
        if self.prod_area<stock_h*stock_w*0.75:
            min_S=-1
            for x in range(min(stock_w - prod_w + 1,cx+1)):
                for y in range(min(stock_h - prod_h + 1,cy+1)):
                    if self._can_place_(stock, (x, y), prod_size):
                        mx=max(cx,x+prod_w)
                        my=max(cy,y+prod_h)
                        new_S=mx*my
                        f=stock_w/stock_h
                        if( new_S<min_S or min_S==-1 ) and ( (cx==0 and cy==0) or (mx/my<=cx/cy and cx/cy>=f)or (mx/my>=cx/cy and cx/cy<=f) )and (x==0 or stock[x-1][y]>=0) and (y==0 or stock[x][y-1]>=0)  :
                            pos_x,pos_y,minx,miny,min_S=x,y,mx,my,new_S
            for x in range(min(stock_w - prod_h + 1,cx+1)):
                for y in range(min(stock_h - prod_w + 1,cy+1)):
                    if self._can_place_(stock, (x, y), prod_size[::-1]):
                        mx=max(cx,x+prod_h)
                        my=max(cy,y+prod_w)
                        new_S=mx*my
                        f=stock_w/stock_h
                        if( new_S<min_S or min_S==-1 ) and ( (cx==0 and cy==0) or (mx/my<=cx/cy and cx/cy>=f)or (mx/my>=cx/cy and cx/cy<=f) )and (x==0 or stock[x-1][y]>=0) and (y==0 or stock[x][y-1]>=0)  :
                            pos_x,pos_y,minx,miny,min_S=x,y,mx,my,new_S
                            prod_size=prod["size"][::-1]
            if pos_x is not None: return pos_x,pos_y,minx,miny,prod_size  
        min_S=-1    
        prod_size=prod["size"]
        for x in range(min(stock_w - prod_w + 1,cx+1)):
            for y in range(min(stock_h - prod_h + 1,cy+1)):
                if self._can_place_(stock, (x, y), prod_size):
                    mx=max(cx,x+prod_w)
                    my=max(cy,y+prod_h)
                    new_S=mx*my
                    if( new_S<min_S or min_S==-1 ) :
                        pos_x,pos_y,minx,miny,min_S=x,y,mx,my,new_S
        for x in range(min(stock_w - prod_h + 1,cx+1)):
            for y in range(min(stock_h - prod_w + 1,cy+1)):
                if self._can_place_(stock, (x, y), prod_size[::-1]):
                    mx=max(cx,x+prod_h)
                    my=max(cy,y+prod_w)
                    new_S=mx*my
                    if( new_S<min_S or min_S==-1 ) :
                        pos_x,pos_y,minx,miny,min_S=x,y,mx,my,new_S
                        prod_size=prod["size"][::-1]
        return pos_x,pos_y,minx,miny,prod_size
    def render_action(self):
        end=True
        for i,_ in self.idx_stock: 
            stock_idx = i
            stock=self._stocks[i]
            self.prod_area=self.prod_area_left
            for prod in self.list_prod:
                while prod["quantity"] > 0:
                    pos_x, pos_y,mx ,my,prod_size = self.place_prod(stock,prod)
                    if pos_x is not None:
                        self.num_prod[-1]+=1
                        action={"size":(mx,my),"action": {"stock_idx": stock_idx, "size": prod_size, "position": (pos_x, pos_y)}}
                        self.list_action.append(action)
                        stock[pos_x : pos_x + prod_size[0], pos_y : pos_y + prod_size[1]] = 1
                        prod["quantity"]-=1
                        self.prod_area_left-=np.prod(prod_size)
                        end= all([product["quantity"] == 0 for product in self.list_prod])
                        if end:break
                    else:break
            if end:break
            self.num_prod.append(0)




class BFPolicy(Policy):
    def __init__(self):
        self.c_stock=0
        self.idx_stock=[]
        self.list_prod=[]
        self.prod_area_left=0
        self.prod_area=0
        self.m=True
    def ___stock_area___(self,stock):
        x,y=self._get_stock_size_(stock)
        return x*y
    def ___csize___(self,stock):
        return  np.max(np.sum(np.any(stock>-1, axis=1))),np.max(np.sum(np.any(stock>-1, axis=0)))
    def get_action(self, observation, info):
        if(info["filled_ratio"]==0):
            self.__init__()
            for prod in observation["products"]:
                self.prod_area_left+=np.prod(prod["size"])*prod["quantity"]
            self.prod_area=self.prod_area_left
            self.idx_stock=sorted(enumerate(observation["stocks"]),key=lambda x:self.___stock_area___(x[1]),reverse=True)
            self.list_prod =sorted(observation["products"],key=lambda x: x["size"][0]*x["size"][1],reverse=True)
        prod_size = [0, 0]
        stock_idx = -1
        pos_x, pos_y = None, None
        c_stock=-1
        for i,_ in self.idx_stock:
            c_stock+=1
            if c_stock<self.c_stock: continue
            stock=observation["stocks"][i]
            stock_w, stock_h = self._get_stock_size_(stock)
            if self.prod_area<stock_h*stock_w*0.75 and c_stock<len(self.idx_stock)-1 and self.m : 
                self.c_stock+=1
                continue
            cx,cy=self.___csize___(stock)
            # c_prod=-1
            
            min_dS=-1
            min_size = [0, 0]
            for prod in self.list_prod:
                # c_prod+=1
                # if c_prod<self.c_prod: continue
                if prod["quantity"] > 0:
                    min_size=prod["size"]
                    prod_w, prod_h =  min_size
                    if stock_w < prod_w or stock_h < prod_h: continue
                    for x in range(min(stock_w - prod_w + 1,cx+1)):
                        for y in range(min(stock_h - prod_h + 1,cy+1)):
                            if self._can_place_(stock, (x, y), min_size):
                                new_S=max(cy,y+prod_h)*max(cx,x+prod_w)
                                dS=(new_S-cx*cy)/(prod_h*prod_w)
                                if dS<min_dS  or min_dS==-1:
                                    prod_size=min_size
                                    pos_x=x
                                    pos_y=y
                                    min_dS=dS
                    min_size=prod["size"][::-1]
                    prod_w, prod_h =  min_size
                    if stock_w < prod_w or stock_h < prod_h: continue
                    for x in range(min(stock_w - prod_w + 1,cx+1)):
                        for y in range(min(stock_h - prod_h + 1,cy+1)):
                            if self._can_place_(stock, (x, y), min_size):
                                new_S=max(cy,y+prod_h)*max(cx,x+prod_w)
                                dS=(new_S-cx*cy)/(prod_h*prod_w)
                                if dS<min_dS  or min_dS==-1:
                                    prod_size=min_size
                                    pos_x=x
                                    pos_y=y
                                    min_dS=dS
            if pos_x is not None:
                stock_idx = i
                self.prod_area_left-=np.prod(prod_size)
                break
            if self.c_stock==len(self.idx_stock)-1:
                self.c_stock-=2
                self.m =False
            self.c_stock+=1
            self.prod_area=self.prod_area_left
            # self.c_prod=0
        return {"stock_idx": stock_idx, "size": prod_size, "position": (pos_x, pos_y)}
        

class FFPolicy(Policy):
    def __init__(self):
        self.c_prod=0
        self.c_stock=0
        self.idx_stock=[]
        self.list_prod=[]
        self.prod_area_left=0
        self.m=True
    def ___stock_area___(self,stock):
        x,y=self._get_stock_size_(stock)
        return x*y
    def ___csize___(self,stock):
        return  np.max(np.sum(np.any(stock>-1, axis=1))),np.max(np.sum(np.any(stock>-1, axis=0)))
    def get_action(self, observation, info):
        if(info["filled_ratio"]==0):
            self.__init__()
            for prod in observation["products"]:
                self.prod_area_left+=np.prod(prod["size"])*prod["quantity"]
            self.prod_area=self.prod_area_left
            self.idx_stock=sorted(enumerate(observation["stocks"]),key=lambda x:self.___stock_area___(x[1]),reverse=True)
            self.list_prod =sorted(observation["products"],key=lambda x: x["size"][0]*x["size"][1],reverse=True)
        prod_size = [0, 0]
        stock_idx = -1
        pos_x, pos_y = None, None
        c_stock=-1
        for i,_ in self.idx_stock:
            c_stock+=1
            if c_stock<self.c_stock: continue
            stock=observation["stocks"][i]
            stock_w, stock_h = self._get_stock_size_(stock)
            if self.prod_area<stock_h*stock_w*0.75 and c_stock<len(self.idx_stock)-1 and self.m: 
                self.c_stock+=1
                continue
            c_prod=-1
            cx,cy=self.___csize___(stock)
            for prod in self.list_prod:
                c_prod+=1
                if c_prod<self.c_prod: continue
                if prod["quantity"] > 0:
                    prod_size=prod["size"]
                    prod_w, prod_h =  prod_size
                    if stock_w < prod_w or stock_h < prod_h: continue
                    for x in range(min(stock_w - prod_w + 1,cx+1)):
                        for y in range(min(stock_h - prod_h + 1,cy+1)):
                            if self._can_place_(stock, (x, y), prod_size):
                                pos_x=x
                                pos_y=y
                                break
                        if pos_x is not None:
                            break   
                    if pos_x is not None:
                        break
                self.c_prod+=1
            if pos_x is not None:
                stock_idx = i
                self.prod_area_left-=np.prod(prod_size)
                break
            if self.c_stock==len(self.idx_stock)-1:
                self.c_stock-=2
                self.m =False
            self.c_stock+=1
            self.c_prod=0
            self.prod_area=self.prod_area_left
        return {"stock_idx": stock_idx, "size": prod_size, "position": (pos_x, pos_y)}
        
        

from policy import Policy
import numpy as np
from copy import deepcopy
class Policy2210xxx(Policy):
    def __init__(self):
        # Student code here
        self.c_stock=0
        self.c_prod=0
        self.idx_stock=[]
        self._stocks=[]
        self.num_stocks=0
        self.list_prod=[]
        self.list_action=[]
        self.num_prod=[0]
    def ___stock_area___(self,stock):
        x,y=self._get_stock_size_(stock)
        return x*y
    def ___csize___(self,stock):
        return  np.max(np.sum(np.any(stock>-1, axis=1))),np.max(np.sum(np.any(stock>-1, axis=0)))
    def get_action_(self, observation, info):
        if(info["filled_ratio"]==0):
            self.c_stock=0
            self.c_prod=0
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
            cx,cy=self.___csize___(stock)
            stock_w, stock_h = self._get_stock_size_(stock)
            c_prod=-1
            for prod in self.list_prod:
                c_prod+=1
                if c_prod<self.c_prod: continue
                if prod["quantity"] > 0:
                    prod_size=prod["size"]
                    prod_w, prod_h =  prod_size
                    if stock_w < prod_w or stock_h < prod_h: continue
                    min_S=-1
                    for x in range(stock_w - prod_w + 1):
                        if x>cx: continue
                        for y in range(stock_h - prod_h + 1):
                            if y>cy: continue
                            if self._can_place_(stock, (x, y), prod_size):
                                new_S=max(cy,y+prod_h)*max(cx,x+prod_w)
                                if new_S<min_S or min_S==-1:
                                    pos_x=x
                                    pos_y=y
                                    min_S=new_S
                    if pos_x is not None:
                        break
                self.c_prod+=1
            if pos_x is not None:
                stock_idx = i
                break
            self.c_stock+=1
            self.c_prod=0
        return {"stock_idx": stock_idx, "size": prod_size, "position": (pos_x, pos_y)}
    def get_action(self,observation,info):
        if(info["filled_ratio"]==0):
            self.__init__()
            self.c_stock=0
            self.c_prod=0
            self._stocks=deepcopy(observation["stocks"])
            self.num_stocks=deepcopy(len(self._stocks))
            self.idx_stock=sorted(enumerate(observation["stocks"]),key=lambda x:self.___stock_area___(x[1]),reverse=True)
            self.list_prod =sorted(enumerate(deepcopy(observation["products"])),key=lambda x: x[1]["size"][0]*x[1]["size"][1],reverse=True)
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
        return self.list_action.pop()["action"]
    def render_action(self):
        end=True
        for i,_ in self.idx_stock: 
            stock_idx = i
            stock=self._stocks[i]
            stock_w, stock_h = self._get_stock_size_(stock)
            for j,prod in self.list_prod:
                while prod["quantity"] > 0:
                    cx,cy=self.___csize___(stock)
                    prod_size = [0, 0]
                    pos_x, pos_y = None, None
                    min_S=-1
                    mx=0
                    my=0
                    prod_size=prod["size"]
                    prod_w, prod_h =  prod_size
                    if stock_w < prod_w or stock_h < prod_h: break
                    for x in range(stock_w - prod_w + 1):
                        if x>cx: break
                        for y in range(stock_h - prod_h + 1):
                            if y>cy: break
                            if self._can_place_(stock, (x, y), prod_size):
                                mx=max(cx,x+prod_w)
                                my=max(cy,y+prod_h)
                                new_S=mx*my
                                if new_S<min_S or min_S==-1:
                                    pos_x=x
                                    pos_y=y
                                    min_S=new_S
                    if pos_x is not None:
                        self.num_prod[-1]+=1
                        action={"size":(mx,my),"action": {"stock_idx": stock_idx, "size": prod_size, "position": (pos_x, pos_y)}}
                        self.list_action.append(action)
                        stock[pos_x : pos_x + prod_w, pos_y : pos_y + prod_h] = j+1
                        prod["quantity"]-=1
                        end= all([product[1]["quantity"] == 0 for product in self.list_prod])
                        if end:break
                    else:break
            if end:break
            self.num_prod.append(0)
    
    
    
from policy import Policy
import numpy as np

class Policy2210xxx(Policy):
    def __init__(self):
        # Student code here
        self.c_stock=0
        self.c_prod=0
        self.idx_stock=[]
        self.list_prod=[]
        pass
    def ___stock_area___(self,stock):
        x,y=self._get_stock_size_(stock)
        return x*y
    def ___csize___(self,stock):
        return  np.max(np.sum(np.any(stock>-1, axis=1))),np.max(np.sum(np.any(stock>-1, axis=0)))
    def get_action(self, observation, info):
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
                        self.list_prod[c_prod]["quantity"]-=1
                        break
                self.c_prod+=1
            if pos_x is not None:
                stock_idx = i
                break
            self.c_stock+=1
            self.c_prod=0
        return {"stock_idx": stock_idx, "size": prod_size, "position": (pos_x, pos_y)}


    # Student code here
    # You can add more functions if needed

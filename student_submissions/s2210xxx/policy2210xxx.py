from policy import Policy
import numpy as np

class Policy2210xxx(Policy):
    def __init__(self):
        # Student code here
        self.c_stock=0
        self.c_prod=0
        pass
    def ___stock_area___(self,stock):
        x,y=self._get_stock_size_(stock)
        return x*y
    def ___max_size___(self,stock):
        return  np.max(np.sum(np.any(stock>-1, axis=1))),np.max(np.sum(np.any(stock>-1, axis=0)))
    def get_action(self, observation, info):
        list_prods =sorted(observation["products"],key=lambda x: x["size"][0]*x["size"][1],reverse=True)
        list_stock = sorted(enumerate(observation["stocks"]),key=lambda x:self.___stock_area___(x[1]),reverse=True)
        num_prod=sum(map(lambda x:x["quantity"],list_prods))
        out_of_prod=(num_prod==1)
        prod_size = [0, 0]
        stock_idx = -1
        pos_x, pos_y = None, None
        c_stock=-1
        for i, stock in list_stock:
            c_stock+=1
            if c_stock<self.c_stock:
                continue
            dS=-1
            mx,my=self.___max_size___(stock)
            S=mx*my
            stock_w, stock_h = self._get_stock_size_(stock)
            c_prod=-1
            for prod in list_prods:
                c_prod+=1
                if c_prod<self.c_prod:
                    continue
                if prod["quantity"] > 0:
                    prod_size=prod["size"]
                    prod_w, prod_h =  prod_size
                    if stock_w < prod_w or stock_h < prod_h:
                        continue
                    cx=None
                    cy=None
                    prod_w, prod_h = prod_size
                    for x in range(stock_w - prod_w + 1):
                        if x>mx:
                            continue
                        for y in range(stock_h - prod_h + 1):
                            if y>my:
                                continue
                            if self._can_place_(stock, (x, y), prod_size):
                                max_x=max(mx,x+prod_w)
                                max_y=max(my,y+prod_h)
                                new_S=max_x*max_y
                                if new_S-S<dS or dS==-1:
                                    cx=x
                                    cy=y
                                    dS=(x+prod_w)*(y+prod_h)-S
                            
                    pos_x,pos_y=cx,cy
                    if pos_x is not None:
                        break
                self.c_prod+=1
            if pos_x is not None:
                stock_idx = i
                break
            self.c_stock+=1
            self.c_prod=0

        if pos_x is None or out_of_prod:
            self.c_stock=0
            self.c_prod=0
        return {"stock_idx": stock_idx, "size": prod_size, "position": (pos_x, pos_y)}


    # Student code here
    # You can add more functions if needed

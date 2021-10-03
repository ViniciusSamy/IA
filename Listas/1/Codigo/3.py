import numpy as np
import matplotlib.pyplot as plt

class Environment:

    def __init__(self, n, price):
        
        self.n = n #Actual number of rolls 
        self.price = price #Actual price
        self.clock = 0 #Clock

        
        self.mu_usage = [10,100,150,300,125,50,15] #Mean of usage for day
        self.sigma_usage = [2,10,10,20,10,10,2] #Standard deviation of usage for day
        
        self.mu_price = 1.2 #Mean of price 
        self.sigma_price = 0.2 #Standard deviation od price

        self.on_sale = False #Indicates if it's on sale
        self.max_n = 1500  #Maximum of rolls in stock

    def initial_percepts(self): 
        return  {
                    'n':self.n,
                    'price':self.price,
                    'max_n':self.max_n
                }

    def signal(self,action):
        
        usage = np.random.normal(self.mu_usage[self.clock%len(self.mu_usage)],self.sigma_usage[self.clock%len(self.sigma_usage)])
        
        bought = action['to_buy']

        self.n = self.n - usage + bought

        if self.clock%7 == 0:
            self.price = 1.2

            self.on_sale = True if np.random.rand() < 0.5 else False

            if self.on_sale:
                self.price -= self.sigma_price
            else:
                self.price = max(np.random.normal(self.mu_price,self.sigma_price),0.9)

        self.clock += 1
        return {'n':self.n,
                'price':self.price,
                'max_n':self.max_n}



class Agent:

    def __init__(self, env):
        
        #Envoriment information
        self.env = env
        self.actual_percepts = env.initial_percepts()
        
        #Spends of Agent
        self.spendings = []

        #Time clock
        self.clock = 1

        #Level of confidence on 
        self.z_confidence_levels = [ 1.96, 1.282, 0.674 ]  # 95%, 80%, 50%, of confidence
        
        #Belief State Informations
        self.belief_state = {
            'price_history': [ self.actual_percepts["price"] ],
            'stock_history': [ self.actual_percepts["n"] ],
            'max_n': self.actual_percepts['max_n']
        }

    def act(self):

        # Verifies env's state
        self.actual_percepts = self.env.initial_percepts()


        # Define if the price is low, normal or high
        prices_std = np.std(self.belief_state['price_history'])
        prices_mean = np.average(self.belief_state['price_history'])
        price_status = None

        if self.actual_percepts['price'] > prices_mean + prices_std:
            price_status = 'high'
        elif self.actual_percepts['price'] < prices_mean - prices_std:
            price_status = 'low'
        else:
            price_status = 'normal'



        #------------Define to_buy-------------#
        to_buy = 0
        stock_std = np.std(self.belief_state['stock_history'][self.clock%7::7])
        stock_mean = np.average(self.belief_state['stock_history'][self.clock%7::7])
        stock_len = len(self.belief_state['stock_history'][self.clock%7::7])
        
        # For the first 30 times, it conserves the stock at 80%
        if self.clock <= 30 and self.actual_percepts['n'] <= self.belief_state['max_n']*0.80 :
            desired_rolls =  int(self.belief_state['max_n']*0.80)
            to_buy = max(0, desired_rolls - self.actual_percepts["n"] )
        
        #If price is high garants the lower limit of interval confidence with 80%
        elif price_status == 'high':
            print('high')
            desired_rolls = stock_mean - ( self.z_confidence_levels[1] * stock_std / (stock_len)**(1/2) )
            to_buy = max(0, desired_rolls - self.actual_percepts["n"] )


        #If price is high garants the upper limit of interval confidence with 95%
        elif price_status == 'low':
            print('low')
            desired_rolls = stock_mean + ( self.z_confidence_levels[0] * stock_std / (stock_len)**(1/2) )
            to_buy = max(0, desired_rolls - self.actual_percepts["n"] )

        #If price is high garants the upper limit of interval confidence with 50%
        elif price_status == 'normal':
            print('normal')
            desired_rolls = stock_mean + ( self.z_confidence_levels[2] * stock_std / (stock_len)**(1/2) )
            to_buy = max(0, desired_rolls - self.actual_percepts["n"] )           


        #----------------DEBUG--------------------#
        desired_rolls_ =  int(self.belief_state['max_n']*0.80)
        to_buy_ = max(0, desired_rolls_ - self.actual_percepts["n"] )
        print(f"80% = {to_buy_}")

        desired_rolls_ = stock_mean - ( self.z_confidence_levels[1] * stock_std / (stock_len)**(1/2) )
        to_buy_ = max(0, desired_rolls_ - self.actual_percepts["n"] )
        print(f"high = {to_buy_}")

        desired_rolls_ = stock_mean + ( self.z_confidence_levels[0] * stock_std / (stock_len)**(1/2) )
        to_buy_ = max(0, desired_rolls_ - self.actual_percepts["n"] )
        print(f"low = {to_buy_}")

        desired_rolls_ = stock_mean + ( self.z_confidence_levels[2] * stock_std / (stock_len)**(1/2) )
        to_buy_ = max(0, desired_rolls_ - self.actual_percepts["n"] )
        print(f"normal = {to_buy_}")

        print("\n")


        #-----------------------------------------#

        
        #Assert the maximum capacity
        to_buy = min(to_buy, self.actual_percepts['max_n']-self.actual_percepts['n'])    

            
        #---------Act---------#
        action = { 'to_buy': to_buy}
        return_percepts = self.env.signal(action)
        
       

        
        #------Update-belief-state-------#
        self.clock += 1
        self.spendings.append(to_buy*self.actual_percepts['price'])
        
        self.actual_percepts = return_percepts
        
        self.belief_state['price_history'].append(self.actual_percepts['price'])
        self.belief_state['stock_history'].append(self.actual_percepts['n'])
        self.belief_state['max_n'] = self.actual_percepts['max_n']


        



if __name__ == "__main__":
    env = Environment(0,1.2)
    ag = Agent(env)

    prices = []
    n = []

    for i in range(1000):
        ag.act()
        prices.append(env.price)
        n.append(env.n)

    

    fig, ax = plt.subplots(2, 2)

    ax[0,0].plot(prices)
    ax[0,0].set_title("env prices")

    ax[0,1].plot(n)
    ax[0,1].set_title(" env stock")

    ax[1,0].plot(ag.spendings)
    ax[1,0].set_title("ag spendings")


    fig.show()
    plt.show()

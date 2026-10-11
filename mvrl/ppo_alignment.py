"""Published PPO optimiser with two structured financial rewards.

The continuation critic uses sample-only policy evaluation; this is a hybrid
control experiment, not a reproduction of a published financial trading agent.
"""
import numpy as np
import gymnasium as gym
from gymnasium import spaces


def features(T,K):
    return np.array([[t/T,*np.eye(K)[z]] for t in range(T) for z in range(K)],np.float32)


def fitted_continuation(r,j,u,riskless):
    T,K,_=r.shape;c=np.zeros((T+1,K))
    for t in range(T-1,-1,-1):
        H=riskless**(T-t-1)
        for z in range(K):c[t,z]=np.mean(H*r[t,z]*u[t,z]+c[t+1,j[t,z]])
    return c


class ConditionalEnv(gym.Env):
    def __init__(self,r,j,phi,riskless,method,seed):
        super().__init__();self.r=r;self.j=j;self.phi=phi;self.s=riskless
        self.T,self.K,self.N=r.shape;self.method=method;self.rng=np.random.default_rng(seed)
        self.c=np.zeros((self.T+1,self.K));self.t=0;self.z=0
        self.action_space=spaces.Box(-3.,3.,(1,),dtype=np.float32)
        self.observation_space=spaces.Box(0.,1.,(self.K+1,),dtype=np.float32)
    def obs(self):return np.array([self.t/self.T,*np.eye(self.K)[self.z]],np.float32)
    def reset(self,seed=None,options=None):
        super().reset(seed=seed)
        if seed is not None:self.rng=np.random.default_rng(seed)
        self.t=0;self.z=int(self.rng.integers(self.K))
        return self.obs(),{}
    def step(self,action):
        u=float(np.clip(action[0],-3.,3.));t,z=self.t,self.z
        i,k=self.rng.integers(self.N,size=2)
        r1,r2=self.r[t,z,i],self.r[t,z,k]
        j1,j2=self.j[t,z,i],self.j[t,z,k]
        H=self.s**(self.T-t-1)
        dc=self.c[t+1,j1]-self.c[t+1,j2] if self.method=='continuation' else 0.
        reward=H*(r1+r2)*u/2-self.phi*(H*(r1-r2)*u+dc)**2/2
        self.t+=1;self.z=int(j1)
        return self.obs(),float(reward),self.t==self.T,False,{}


def train_ppo(r,j,phi,riskless,method,seed,steps=32768):
    import torch
    from stable_baselines3 import PPO
    from stable_baselines3.common.vec_env import DummyVecEnv
    from stable_baselines3.common.callbacks import BaseCallback
    torch.set_num_threads(1)
    T,K,_=r.shape;obs=features(T,K)
    env=DummyVecEnv([lambda k=k:ConditionalEnv(r,j,phi,riskless,method,seed+10001*k) for k in range(8)])
    class Refresh(BaseCallback):
        def _on_step(self):return True
        def _on_rollout_start(self):
            u=self.model.predict(obs,deterministic=True)[0].reshape(T,K)
            c=fitted_continuation(r,j,u,riskless)
            for e in env.envs:e.c=c.copy()
    model=PPO('MlpPolicy',env,learning_rate=3e-4,n_steps=64,batch_size=128,n_epochs=10,
        gamma=1.,gae_lambda=.95,clip_range=.2,ent_coef=0.,seed=seed,device='cpu',
        policy_kwargs=dict(net_arch=dict(pi=[64,64],vf=[64,64])),verbose=0)
    model.learn(total_timesteps=steps,callback=Refresh())
    u=model.predict(obs,deterministic=True)[0].reshape(T,K)
    c=fitted_continuation(r,j,u,riskless);env.close()
    return u,c,model

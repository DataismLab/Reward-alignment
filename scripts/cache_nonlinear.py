"""Precompute independent past-only QuEST fits without changing portfolio paths."""
import argparse
from mvrl.historical import ROOT,data
from mvrl.nonlinear import nonlinear_covariance

parser=argparse.ArgumentParser()
parser.add_argument('--assets',type=int,required=True,choices=[10,30,49])
parser.add_argument('--start-index',type=int,default=0)
parser.add_argument('--stop-index',type=int,default=432)
args=parser.parse_args()
frame=data(args.assets)
evaluation=frame.index[frame.index>=199001]
for date in evaluation[args.start_index:args.stop_index]:
    t=frame.index.get_loc(date);h=frame.iloc[t-120:t]
    x=h.iloc[:,:-1].to_numpy()-h.RF.to_numpy()[:,None]
    nonlinear_covariance(x,ROOT/'results/historical/covariance/quest_cache')
print('Cached',args.assets,args.start_index,args.stop_index,flush=True)

import sys,json,time
from pathlib import Path
import numpy as np
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--upstream',required=True,help='Directory of the pinned upstream Python QuEST checkout')
args=parser.parse_args()
sys.path.insert(0,args.upstream)
from src.modules.quest.estimate import quest_imate
from mvrl.historical import ROOT,data
from mvrl.nonlinear import nonlinear_covariance
rows=[]
for n in [10,30,49]:
 frame=data(n)
 for date in [199001,202512]:
  t=frame.index.get_loc(date);hist=frame.iloc[t-120:t];x=hist.iloc[:,:-1].to_numpy()-hist.RF.to_numpy()[:,None]
  v,info=nonlinear_covariance(x,ROOT/'results/historical/covariance/quest_cache')
  ref=quest_imate(x,opt_speed=(1e-6,600))
  row=dict(n=n,date=date,reference_success=bool(ref.result.success),reference_optimality=float(ref.result.optimality),relative_covariance_difference=float(np.linalg.norm(v-ref.sigmahat)/np.linalg.norm(ref.sigmahat)),mse=info['quest_normalized_mse'],reference_mse=float(np.mean((ref.lambdahat-ref.lambda_)**2)/np.mean(ref.lambda_)**2))
  rows.append(row);print(row,flush=True)
(ROOT/'results/historical/covariance/quest_fit_validation.json').write_text(json.dumps(rows,indent=2))

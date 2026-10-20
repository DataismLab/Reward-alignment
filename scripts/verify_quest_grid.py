"""Check the original QuEST quadrature against a fourfold denser grid.

Uses six fixed endpoint windows; refines numerical integration at the fitted
population eigenvalues, not the financial outcomes or tuning parameters.
"""
import inspect,json
import numpy as np
from mvrl._vendor.quest import core
from mvrl.historical import ROOT,data
from mvrl.nonlinear import nonlinear_covariance

original=core._net_grid
source=inspect.getsource(original).replace('minnxi = 100','minnxi = 400')
namespace=dict(core.__dict__)
exec(source,namespace)
fine=namespace['_net_grid'];rows=[]
for n in [10,30,49]:
    frame=data(n)
    for date in [199001,202512]:
        t=frame.index.get_loc(date);h=frame.iloc[t-120:t]
        x=h.iloc[:,:-1].to_numpy()-h.RF.to_numpy()[:,None]
        _,info=nonlinear_covariance(x,ROOT/'results/historical/covariance/quest_cache')
        tau=np.array(info['quest_population_eigenvalues']);scale=tau.mean()
        try:
            core._net_grid=fine
            _,delta,_=core.quest(tau/scale,119)
        finally:
            core._net_grid=original
        coarse=np.array(info['quest_shrunk_eigenvalues'])
        error=float(np.linalg.norm(delta*scale-coarse)/np.linalg.norm(coarse))
        rows.append(dict(n=n,date=date,relative_spectrum_difference=error))
assert max(r['relative_spectrum_difference'] for r in rows)<.002
(ROOT/'results/historical/covariance/quest_grid_validation.json').write_text(json.dumps(rows,indent=2))
print('Six fixed windows pass quadrature refinement check')

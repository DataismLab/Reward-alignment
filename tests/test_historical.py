import numpy as np
from mvrl.historical import solve_family,objective,moments,data,solve_quadratic

def test_joint_calibration_with_constraints_and_costs():
    rng=np.random.default_rng(39)
    for n in [2,5]:
        for cost in [0,.001,.01]:
            A=rng.normal(size=(n,n));v=(A@A.T+np.eye(n))*.002
            m=rng.uniform(.005,.025,n);prev=np.ones(n)/n;phi=3.
            policies,info=solve_family(m,v,phi,prev,cost)
            target=policies['target'];val=objective(m,v,target,phi,prev,cost)
            for name in ['joint','mvpi']:
                assert np.linalg.norm(policies[name]-target)<2e-5
                assert abs(objective(m,v,policies[name],phi,prev,cost)-val)<1e-9
            assert all(abs(w.sum()-1)<1e-7 and min(w)>-1e-7 for w in policies.values())

def test_penalty_only_cost_distortion_identity():
    m=np.array([.04,.012,.009]);v=np.diag([.005,.001,.002]);phi=5.;cost=.006;prev=np.array([.1,.7,.2])
    ps,info=solve_family(m,v,phi,prev,cost);A=info['A'];y=m@ps['target'];M=v+np.outer(m,m)
    for w in [np.array([.8,.1,.1]),ps['penalty_only']]:
        raw=m@w-phi/A*w@M@w-cost*abs(w-prev).sum()
        rhs=objective(m,v,w,phi,prev,cost)-phi*(m@w-y)**2-2*phi*y*cost*abs(w-prev).sum()+phi*y*y
        assert abs(A*raw-rhs)<1e-12
    assert np.linalg.norm(ps['penalty_only']-ps['target'])>1e-4

def test_qp_certificate_and_independent_grid():
    m=np.array([.025,.01]);v=np.array([[.004,.001],[.001,.002]]);p=np.array([.4,.6]);phi=5.;cost=.002
    w,cert=solve_quadratic(m,phi*v,p,cost)
    grid=np.linspace(0,1,100001);values=np.array([objective(m,v,np.array([a,1-a]),phi,p,cost) for a in grid])
    assert objective(m,v,w,phi,p,cost)>=max(values)-1e-10
    assert cert<2e-7

def test_data_and_past_only_moments():
    f=data();assert f.index[0]==197001 and f.index[-1]==202512
    assert len(f)==56*12 and np.isfinite(f.to_numpy()).all()
    x=f.iloc[:120,:-1].to_numpy();m,v=moments(x)
    altered=f.copy();altered.iloc[120:,:]=999
    mm,vv=moments(altered.iloc[:120,:-1].to_numpy())
    assert np.array_equal(m,mm) and np.array_equal(v,vv)

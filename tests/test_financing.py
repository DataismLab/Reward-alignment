import numpy as np
from mvrl.financing import solve_financing, financing_cost
from mvrl.historical import solve_quadratic


def test_joint_identity_with_shorting_and_borrowing():
    m=np.array([.032,-.002,.025,.005]);v=np.diag([.003,.002,.004,.001]);p=np.ones(4)/4;phi=5
    target,_=solve_financing(m,phi*v,p);A=1+2*phi*(m@target);M=v+np.outer(m,m)
    joint,cert=solve_financing(m,phi/A*M,p,.001/A,.002/A,.0005/A)
    assert np.linalg.norm(joint-target)<2e-5
    assert target.sum()>1 and target.min()<0
    for u in (target,joint,p):
        F=m@u-phi*u@v@u-financing_cost(u,p)
        Q=m@u-phi/A*u@M@u-financing_cost(u,p)/A
        assert abs(A*Q-F+phi*(m@u-m@target)**2-phi*(m@target)**2)<1e-14


def test_assetwise_pnl_reward_cannot_identify_covariance_target():
    # Equal symmetric marginals; changing dependence changes only the MV target.
    p=np.ones(3)/3;v=np.eye(3);v[0,1]=v[1,0]=.5
    w,_=solve_quadratic(np.zeros(3),v,p,0)
    np.testing.assert_allclose(w,[2/7,2/7,3/7],atol=1e-6)
    marginal_gain=np.ones(3)/np.sqrt(2*np.pi)
    for penalty in [1,5,25]:
        scores=marginal_gain-penalty*marginal_gain
        assert abs(scores@w-scores@p)<1e-10

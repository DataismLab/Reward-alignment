import numpy as np
import pytest
from mvrl.covariance import estimate_covariance, ESTIMATORS, calibration_bounds, covariance_transfer_bounds
from mvrl.historical import solve_family, solve_quadratic, objective


def fixture(n=10, t=120):
    rng = np.random.default_rng(317)
    f = rng.normal(size=(t, 3))*.03
    x = .004+f@rng.normal(size=(3, n))*.7+rng.normal(size=(t, n))*.02
    return x, f


@pytest.mark.parametrize('n,t', [(10, 120), (49, 60), (100, 60)])
def test_lw_against_independent_library(n, t):
    from sklearn.covariance import ledoit_wolf
    x, _ = fixture(n, t)
    _, v, info = estimate_covariance(x, 'lw_identity')
    ref, alpha = ledoit_wolf(x)
    np.testing.assert_allclose(v, ref*t/(t-1), atol=2e-16, rtol=1e-12)
    assert abs(info['shrinkage']-alpha) < 1e-12


def test_constant_correlation_direct_fourth_moment_formula():
    x, _ = fixture(7, 80); z=x-x.mean(0); t,n=x.shape; s=z.T@z/t
    r=(s/np.sqrt(np.outer(s.diagonal(),s.diagonal()))).sum()/n/(n-1)-1/(n-1)
    target=r*np.sqrt(np.outer(s.diagonal(),s.diagonal()));np.fill_diagonal(target,s.diagonal())
    pi=0.;rho=0.
    for i in range(n):
        for j in range(n):
            product=z[:,i]*z[:,j]-s[i,j];pi+=np.mean(product**2)
            if i==j:rho+=np.mean(product**2)
            else:
                rho+=r/2*(np.sqrt(s[j,j]/s[i,i])*np.mean((z[:,i]**2-s[i,i])*product)
                    +np.sqrt(s[i,i]/s[j,j])*np.mean((z[:,j]**2-s[j,j])*product))
    a=np.clip((pi-rho)/(t*np.sum((target-s)**2)),0,1)
    _,v,info=estimate_covariance(x,'lw_correlation')
    np.testing.assert_allclose(v,((1-a)*s+a*target)*t/(t-1),atol=1e-16)
    assert abs(a-info['shrinkage'])<1e-12


@pytest.mark.parametrize('estimator', ESTIMATORS)
def test_estimators_alignment_and_scale(estimator):
    x,f=fixture();m,v,_=estimate_covariance(x,estimator,f)
    _,v2,_=estimate_covariance(x*3,estimator,f)
    np.testing.assert_allclose(v2,9*v,rtol=1e-10,atol=1e-14)
    prev=np.ones(10)/10
    w,info=solve_family(m,v,5,prev,.001,['target','raw','joint'])
    assert np.linalg.norm(w['target']-w['joint'])<2e-5
    assert abs(w['joint'].sum()-1)<1e-8
    A=info['A'];q=lambda u:m@u-5/A*u@(v+np.outer(m,m))@u-.001/A*abs(u-prev).sum()
    for u in (prev,w['joint'],w['raw']):
        rhs=objective(m,v,u,5,prev,.001)-5*(m@u-m@w['target'])**2+5*(m@w['target'])**2
        assert abs(A*q(u)-rhs)<1e-14


def test_factor_formula_with_intercept_and_residual_dof():
    x,f=fixture(7,70)
    coef=np.linalg.lstsq(np.c_[np.ones(70),f],x,rcond=None)[0]
    residual=x-np.c_[np.ones(70),f]@coef
    expected=coef[1:].T@np.cov(f,rowvar=False)@coef[1:]+np.diag((residual**2).sum(0)/66)
    _,v,_=estimate_covariance(x,'ff3',f)
    np.testing.assert_allclose(v,expected,atol=1e-16)


def test_bounds_for_inexact_anchor_and_covariance_change():
    x,f=fixture();m,v,_=estimate_covariance(x,'diag10',f)
    _,vf,_=estimate_covariance(x,'ff3',f);p=np.ones(10)/10;phi=5;cost=.001
    w,_=solve_family(m,v,phi,p,cost,['target'])
    for anchor in (0.,float(m@p),float(m@w['target'])+.01):
        A=1+2*phi*anchor
        u,cert=solve_quadratic(m,phi/A*(v+np.outer(m,m)),p,cost/A)
        b=calibration_bounds(m,v,phi,w['target'],u,anchor,cert)
        gap=objective(m,v,w['target'],phi,p,cost)-objective(m,v,u,phi,p,cost)
        assert gap<=b['target_gap_upper']+1e-10
        assert np.linalg.norm(w['target']-u)<=b['distance_upper']+1e-5
    alt,cert=solve_quadratic(m,phi*vf,p,cost)
    b=covariance_transfer_bounds(v,vf,alt,phi)
    gap=objective(m,v,w['target'],phi,p,cost)-objective(m,v,alt,phi,p,cost)
    assert gap<=b['target_gap_upper']+1e-8


def test_invalid_factors_and_history_rejected():
    x,f=fixture()
    with pytest.raises(ValueError):estimate_covariance(x,'ff3',f[:-1])
    with pytest.raises(ValueError):estimate_covariance(x,'ff3',np.zeros_like(f))
    x[0,0]=np.nan
    with pytest.raises(ValueError):estimate_covariance(x,'sample')

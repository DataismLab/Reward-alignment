import numpy as np
import pytest
from mvrl.dependent import demo_market, RegimePolicy, equilibrium, deviation_value
from mvrl.equilibrium_audit import continuation, exact_audit, independent_sample_certificate
from mvrl.equilibrium_learning import collect_samples, fit_backward


@pytest.mark.parametrize('seed',range(8))
def test_deviation_identity_and_bound_against_terminal_moments(seed):
    rng=np.random.default_rng(seed)
    market=demo_market(persistence=rng.uniform(.1,.95),horizon=7)
    phi=rng.uniform(.2,4)
    u=rng.normal(size=(7,2));c=rng.normal(size=(8,2))
    out=exact_audit(market,u,c,phi)
    policy=RegimePolicy(np.zeros_like(u),u)
    for t in range(7):
        H=market.riskless**(6-t)
        for z in range(2):
            # Independent three-point fit to the existing terminal-moment evaluator.
            vals=[deviation_value(market,policy,phi,t,z,1.,a) for a in (-1.,0.,1.)]
            linear=(vals[2]-vals[0])/2
            quadratic=(vals[2]+vals[0])/2-vals[1]
            best=-linear/(2*quadratic)
            true_gap=deviation_value(market,policy,phi,t,z,1.,best)-deviation_value(market,policy,phi,t,z,1.,u[t,z])
            assert out['exploitability'][t,z]==pytest.approx(true_gap,abs=3e-13)
    assert np.all(out['exploitability']<=out['bound']+1e-13)
    assert np.all(np.ptp(out['true_critic_error'],axis=1)<=out['critic_span_bound']+1e-13)


def test_equilibrium_and_constant_shift_invariance():
    m=demo_market(horizon=12);eq,_=equilibrium(m,1.)
    c=continuation(m,eq.beta)
    a=exact_audit(m,eq.beta,c,1.)
    b=exact_audit(m,eq.beta,c+100*np.arange(13)[:,None],1.)
    assert a['bound'].max()<1e-25
    assert b['bound'].max()<1e-20
    assert b['uniform_bound'].max()>1e6
    assert np.max(np.abs(b['gradient']-a['gradient']))<1e-12


def test_nonconstant_terminal_error_is_included():
    m=demo_market(horizon=4);eq,_=equilibrium(m,1.)
    c=continuation(m,eq.beta);c[-1]=[1.,-1.]
    out=exact_audit(m,eq.beta,c,1.)
    assert out['critic_span_bound'][-1]==2
    assert np.all(out['exploitability']<=out['bound']+1e-13)


def test_learning_access_and_optimisation_control():
    m=demo_market(horizon=4);r,j=collect_samples(m,2048,9)
    u,c=fit_backward(r,j,1.,m.riskless,actor_steps=100)
    v,d=fit_backward(r,j,1.,m.riskless,method='paired_exact')
    np.testing.assert_allclose(u,v,atol=1e-11)
    np.testing.assert_allclose(c,d,atol=1e-11)
    np.testing.assert_array_equal(fit_backward(r,j,1.,m.riskless,actor_steps=0)[0],0.)


def test_independent_certificate_coverage_and_refusal():
    m=demo_market(horizon=4)
    train=collect_samples(m,512,31)
    u,c=fit_backward(*train,1.,m.riskless)
    r,j=collect_samples(m,20000,90031)
    out=independent_sample_certificate(u,c,r,j,1.,m.riskless,.21)
    true=exact_audit(m,u,c,1.)
    assert np.all(true['exploitability']<=out['bound'])
    assert np.isfinite(out['bound']).all()
    # Insufficient audit data must not be hidden behind a variance floor.
    small=independent_sample_certificate(u,c,r[:,:,:4],j[:,:,:4],1.,m.riskless,.21)
    assert np.isinf(small['bound']).any()
    with pytest.raises(ValueError,match='support'):
        independent_sample_certificate(u,c,r,j,1.,m.riskless,.001)


def test_reward_error_split_detects_missing_hedge():
    m=demo_market(horizon=12);r,j=collect_samples(m,4096,0)
    u,c=fit_backward(r,j,1.,m.riskless,method='myopic')
    h=np.empty_like(u)
    for t in range(m.horizon):
        H=m.riskless**(m.horizon-t-1)
        for z in range(m.regimes):
            mean,_,var=m.moments(z)
            h[t,z]=H*mean-2*H*H*var*u[t,z]
    out=exact_audit(m,u,c,1.,reward_gradient=h)
    assert out['reward'].max()>0
    assert np.all(out['exploitability']<=out['bound']+1e-13)


def test_vector_projection_inequality_and_sharp_scalar_constant():
    rng=np.random.default_rng(52)
    for dim in (1,3,10):
        r=rng.normal(size=(500,dim));d=rng.normal(size=500)
        r-=r.mean(0);d-=d.mean()
        covariance=r.T@r/len(r);cross=r.T@d/len(r)
        assert cross@np.linalg.solve(covariance,cross)<=np.var(d)+1e-13
    r=np.array([-1.,1.]);d=np.array([-3.,3.])
    assert (r@d/2)**2/(r@r/2)==pytest.approx(np.ptp(d)**2/4)


@pytest.mark.parametrize('interval',['hoeffding','bernstein'])
def test_observable_mixing_bound(interval):
    m=demo_market(horizon=4);r,j=collect_samples(m,512,10)
    u,c=fit_backward(r,j,1.,m.riskless)
    ar,aj=collect_samples(m,20000,100010)
    cert=independent_sample_certificate(u,c,ar,aj,1.,m.riskless,.21,
        interval=interval,estimate_mixing=True)
    exact=exact_audit(m,u,c,1.)
    assert np.all(cert['rho_upper']>=exact['rho'])
    assert np.all(cert['rho_upper']<1)
    assert np.all(cert['bound']>=exact['exploitability'])


def test_neural_shared_policy_reproducibility():
    pytest.importorskip('torch')
    from mvrl.neural_equilibrium import train
    r,j=collect_samples(demo_market(),64,1)
    a=train(r,j,1.,1.02,seed=2,checkpoints=(2,))
    b=train(r,j,1.,1.02,seed=2,checkpoints=(2,))
    np.testing.assert_array_equal(a[0]['actions'],b[0]['actions'])
    np.testing.assert_allclose(a[0]['critic'].mean(1),0,atol=1e-8)
    np.testing.assert_array_equal(a[0]['critic'][-1],0.)


@pytest.mark.parametrize('seed',range(5))
def test_constrained_certificate_including_active_boundaries(seed):
    rng=np.random.default_rng(seed);m=demo_market(horizon=4)
    r,j=collect_samples(m,512,seed)
    u,c=fit_backward(r,j,1.,m.riskless,action_bounds=(-.2,.4))
    assert np.any(np.isclose(u,.4))
    c=c+rng.normal(scale=.3,size=c.shape);c[-1]=0
    au=exact_audit(m,u,c,1.,action_bounds=(-.2,.4))
    pol=RegimePolicy(np.zeros_like(u),u)
    for t in range(4):
        for z in range(2):
            f=lambda v:deviation_value(m,pol,1.,t,z,1.,v)
            v0,vm,vp=f(0),f(-1),f(1)
            best=np.clip(-(vp-vm)/(2*(vp+vm-2*v0)),-.2,.4)
            assert au['exploitability'][t,z]==pytest.approx(f(best)-f(u[t,z]),abs=1e-13)
    assert np.all(au['exploitability']<=au['bound']+1e-13)


def test_active_boundary_exact_solution_has_zero_certificate():
    m=demo_market(horizon=1)
    u=np.array([[.01,-.01]]) # Both unconstrained responses lie outside the box.
    c=continuation(m,u)
    au=exact_audit(m,u,c,1.,action_bounds=(-.01,.01))
    assert np.max(np.abs(au['gradient']))>0
    np.testing.assert_array_equal(au['bound'],0.)


def test_zero_actor_gradient_can_hide_critic_error():
    m=demo_market(horizon=4)
    c=np.array([[0.,0.],[1.,-1.],[.5,-.5],[.2,-.2],[0.,0.]])
    u=np.zeros((4,2))
    for t in range(4):
        H=m.riskless**(3-t)
        for z in range(2):
            p,j,r=m.branches(z);mean=p@r;v=p@((r-mean)**2)
            u[t,z]=(H*mean-2*H*(p@((r-mean)*c[t+1,j])))/(2*H*H*v)
    out=exact_audit(m,u,c,1.)
    assert abs(out['gradient']).max()<1e-14
    assert out['exploitability'].max()>.1
    assert out['bound'].max()>=out['exploitability'].max()
